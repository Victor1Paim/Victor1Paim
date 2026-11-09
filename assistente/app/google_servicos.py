"""Google Agenda e Gmail com a conta do dono (OAuth gerado por scripts/autorizar_google.py)."""

from __future__ import annotations

import base64
import json
from email.mime.text import MIMEText
from email.utils import parseaddr

from .config import Config

ESCOPOS = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
]


class GoogleNaoConfigurado(RuntimeError):
    pass


def carregar_credenciais(config: Config):
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials

    if config.google_token_json.strip():
        info = json.loads(config.google_token_json)
    elif config.google_token_arquivo.exists():
        info = json.loads(config.google_token_arquivo.read_text())
    else:
        raise GoogleNaoConfigurado(
            "Google não autorizado. Rode `python scripts/autorizar_google.py` e configure o token."
        )
    cred = Credentials.from_authorized_user_info(info, ESCOPOS)
    if not cred.valid and cred.refresh_token:
        cred.refresh(Request())
    return cred


class Google:
    def __init__(self, config: Config):
        self.config = config
        self._agenda = None
        self._gmail = None

    def _servico(self, nome: str, versao: str):
        from googleapiclient.discovery import build

        return build(nome, versao, credentials=carregar_credenciais(self.config), cache_discovery=False)

    @property
    def agenda(self):
        if self._agenda is None:
            self._agenda = self._servico("calendar", "v3")
        return self._agenda

    @property
    def gmail(self):
        if self._gmail is None:
            self._gmail = self._servico("gmail", "v1")
        return self._gmail

    # ---------------- Agenda ----------------
    def listar_eventos(self, inicio: str, fim: str, maximo: int = 20) -> list[dict]:
        r = (
            self.agenda.events()
            .list(
                calendarId=self.config.google_agenda_id,
                timeMin=inicio,
                timeMax=fim,
                maxResults=maximo,
                singleEvents=True,
                orderBy="startTime",
                timeZone=self.config.fuso_horario,
            )
            .execute()
        )
        return [
            {
                "id": e.get("id"),
                "titulo": e.get("summary", "(sem título)"),
                "inicio": e.get("start", {}).get("dateTime") or e.get("start", {}).get("date"),
                "fim": e.get("end", {}).get("dateTime") or e.get("end", {}).get("date"),
                "local": e.get("location"),
                "link": e.get("htmlLink"),
            }
            for e in r.get("items", [])
        ]

    def criar_evento(
        self,
        titulo: str,
        inicio: str,
        fim: str,
        descricao: str | None = None,
        local: str | None = None,
        dia_inteiro: bool = False,
    ) -> dict:
        if dia_inteiro:
            quando_ini, quando_fim = {"date": inicio[:10]}, {"date": fim[:10]}
        else:
            quando_ini = {"dateTime": inicio, "timeZone": self.config.fuso_horario}
            quando_fim = {"dateTime": fim, "timeZone": self.config.fuso_horario}
        corpo = {"summary": titulo, "start": quando_ini, "end": quando_fim}
        if descricao:
            corpo["description"] = descricao
        if local:
            corpo["location"] = local
        e = self.agenda.events().insert(calendarId=self.config.google_agenda_id, body=corpo).execute()
        return {"id": e.get("id"), "titulo": e.get("summary"), "link": e.get("htmlLink")}

    # ---------------- Gmail ----------------
    def buscar_emails(self, consulta: str, maximo: int = 10) -> list[dict]:
        r = self.gmail.users().messages().list(userId="me", q=consulta, maxResults=maximo).execute()
        saida = []
        for m in r.get("messages", []):
            d = (
                self.gmail.users()
                .messages()
                .get(userId="me", id=m["id"], format="metadata", metadataHeaders=["From", "Subject", "Date"])
                .execute()
            )
            cab = {h["name"]: h["value"] for h in d.get("payload", {}).get("headers", [])}
            saida.append(
                {
                    "id": d["id"],
                    "de": cab.get("From"),
                    "assunto": cab.get("Subject"),
                    "data": cab.get("Date"),
                    "trecho": d.get("snippet"),
                    "nao_lido": "UNREAD" in d.get("labelIds", []),
                }
            )
        return saida

    def ler_email(self, email_id: str, limite: int = 6000) -> dict:
        d = self.gmail.users().messages().get(userId="me", id=email_id, format="full").execute()
        cab = {h["name"]: h["value"] for h in d.get("payload", {}).get("headers", [])}
        texto = _texto_do_payload(d.get("payload", {})) or d.get("snippet", "")
        return {
            "id": d["id"],
            "thread_id": d.get("threadId"),
            "de": cab.get("From"),
            "para": cab.get("To"),
            "assunto": cab.get("Subject"),
            "data": cab.get("Date"),
            "message_id": cab.get("Message-ID") or cab.get("Message-Id"),
            "corpo": texto[:limite],
        }

    def criar_rascunho(self, para: str, assunto: str, corpo: str, responder_a_id: str | None = None) -> dict:
        msg = MIMEText(corpo, "plain", "utf-8")
        msg["To"] = para
        msg["Subject"] = assunto
        mensagem: dict = {}
        if responder_a_id:
            original = self.ler_email(responder_a_id, limite=0)
            if original.get("message_id"):
                msg["In-Reply-To"] = original["message_id"]
                msg["References"] = original["message_id"]
            mensagem["threadId"] = original["thread_id"]
        mensagem["raw"] = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        r = self.gmail.users().drafts().create(userId="me", body={"message": mensagem}).execute()
        return {"rascunho_id": r["id"], "para": parseaddr(para)[1] or para, "assunto": assunto}

    def enviar_rascunho(self, rascunho_id: str) -> dict:
        r = self.gmail.users().drafts().send(userId="me", body={"id": rascunho_id}).execute()
        return {"enviado": True, "email_id": r.get("id")}


def _texto_do_payload(parte: dict) -> str:
    """Pega o texto simples de um e-mail (procura text/plain nas partes)."""
    tipo = parte.get("mimeType", "")
    dados = parte.get("body", {}).get("data")
    if tipo == "text/plain" and dados:
        return base64.urlsafe_b64decode(dados).decode("utf-8", errors="replace")
    textos = [_texto_do_payload(p) for p in parte.get("parts", []) or []]
    textos = [t for t in textos if t]
    if textos:
        return "\n".join(textos)
    if tipo == "text/html" and dados:
        import re

        html = base64.urlsafe_b64decode(dados).decode("utf-8", errors="replace")
        return re.sub(r"<[^>]+>", " ", html)
    return ""
