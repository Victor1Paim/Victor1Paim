"""Cliente da WhatsApp Cloud API (Meta): validar webhook, enviar texto, baixar mídia."""

from __future__ import annotations

import hashlib
import hmac

import httpx

from .config import Config

LIMITE_TEXTO = 4000  # a API aceita até 4096 caracteres por mensagem


def assinatura_valida(app_secret: str, corpo: bytes, cabecalho: str | None) -> bool:
    """Confere o cabeçalho X-Hub-Signature-256 enviado pela Meta."""
    if not app_secret or not cabecalho or not cabecalho.startswith("sha256="):
        return False
    esperado = hmac.new(app_secret.encode(), corpo, hashlib.sha256).hexdigest()
    return hmac.compare_digest(esperado, cabecalho.removeprefix("sha256="))


def dividir_texto(texto: str, limite: int = LIMITE_TEXTO) -> list[str]:
    partes: list[str] = []
    restante = texto.strip()
    while len(restante) > limite:
        corte = restante.rfind("\n", 0, limite)
        if corte < limite // 2:
            corte = restante.rfind(" ", 0, limite)
        if corte <= 0:
            corte = limite
        partes.append(restante[:corte].rstrip())
        restante = restante[corte:].lstrip()
    if restante:
        partes.append(restante)
    return partes


def extrair_mensagens(payload: dict) -> list[dict]:
    """Extrai as mensagens recebidas de um payload de webhook (ignora status de entrega)."""
    mensagens: list[dict] = []
    for entrada in payload.get("entry", []):
        for mudanca in entrada.get("changes", []):
            valor = mudanca.get("value", {})
            for msg in valor.get("messages", []) or []:
                mensagens.append(msg)
    return mensagens


class WhatsApp:
    def __init__(self, config: Config, cliente: httpx.Client | None = None):
        self.config = config
        self._http = cliente or httpx.Client(timeout=30)

    @property
    def _base(self) -> str:
        return f"https://graph.facebook.com/{self.config.whatsapp_api_version}"

    @property
    def _cabecalhos(self) -> dict:
        return {"Authorization": f"Bearer {self.config.whatsapp_token}"}

    def enviar_texto(self, para: str, texto: str) -> None:
        url = f"{self._base}/{self.config.whatsapp_phone_number_id}/messages"
        for parte in dividir_texto(texto) or ["(sem resposta)"]:
            r = self._http.post(
                url,
                headers=self._cabecalhos,
                json={
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": para,
                    "type": "text",
                    "text": {"preview_url": False, "body": parte},
                },
            )
            r.raise_for_status()

    def marcar_lida(self, mensagem_id: str) -> None:
        url = f"{self._base}/{self.config.whatsapp_phone_number_id}/messages"
        self._http.post(
            url,
            headers=self._cabecalhos,
            json={"messaging_product": "whatsapp", "status": "read", "message_id": mensagem_id},
        )

    def baixar_midia(self, midia_id: str) -> tuple[bytes, str]:
        """Retorna (bytes, mime_type) de um áudio/imagem recebido."""
        info = self._http.get(f"{self._base}/{midia_id}", headers=self._cabecalhos)
        info.raise_for_status()
        dados = info.json()
        arquivo = self._http.get(dados["url"], headers=self._cabecalhos)
        arquivo.raise_for_status()
        return arquivo.content, dados.get("mime_type", "application/octet-stream")
