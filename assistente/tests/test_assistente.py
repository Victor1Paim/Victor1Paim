import hashlib
import hmac
import json
from datetime import datetime
from types import SimpleNamespace as NS
from zoneinfo import ZoneInfo

from fastapi.testclient import TestClient

from app.agente import Assistente
from app.config import Config
from app.ferramentas import Contexto, Ferramentas
from app.main import criar_app
from app.memoria import Memoria
from app.whatsapp import assinatura_valida, dividir_texto, extrair_mensagens

SEGREDO = "segredo-do-app"


def config(**extra):
    base = dict(
        whatsapp_verify_token="verifica",
        whatsapp_app_secret=SEGREDO,
        numeros_permitidos={"5511999999999"},
        memoria_mensagens=20,
    )
    base.update(extra)
    return Config(**base)


# ---------------- fakes ----------------
class GoogleFalso:
    def __init__(self):
        self.enviados = []
        self.eventos = []

    def listar_eventos(self, inicio, fim, maximo=20):
        return [{"titulo": "Dentista", "inicio": "2026-11-10T15:00:00-03:00"}]

    def criar_evento(self, titulo, inicio, fim, descricao=None, local=None, dia_inteiro=False):
        self.eventos.append(titulo)
        return {"id": "ev1", "titulo": titulo}

    def criar_rascunho(self, para, assunto, corpo, responder_a_id=None):
        return {"rascunho_id": "r1", "para": para, "assunto": assunto}

    def enviar_rascunho(self, rascunho_id):
        self.enviados.append(rascunho_id)
        return {"enviado": True}


def chamada(nome, args, id_="c1"):
    return NS(id=id_, function=NS(name=nome, arguments=json.dumps(args)))


class OpenAIFalso:
    """Devolve respostas roteirizadas, uma por chamada."""

    def __init__(self, roteiro):
        self.roteiro = list(roteiro)
        self.pedidos = []
        self.chat = NS(completions=NS(create=self._criar))

    def _criar(self, **kw):
        self.pedidos.append(kw)
        item = self.roteiro.pop(0)
        msg = NS(content=None, tool_calls=item) if isinstance(item, list) else NS(content=item, tool_calls=None)
        return NS(choices=[NS(message=msg)])


AGORA = datetime(2026, 11, 9, 10, 0, tzinfo=ZoneInfo("America/Sao_Paulo"))


def montar(roteiro):
    mem = Memoria(":memory:")
    google = GoogleFalso()
    oa = OpenAIFalso(roteiro)
    return Assistente(config(), mem, Ferramentas(google, mem), oa), mem, google, oa


# ---------------- whatsapp ----------------
def test_assinatura():
    corpo = b'{"a":1}'
    sig = "sha256=" + hmac.new(SEGREDO.encode(), corpo, hashlib.sha256).hexdigest()
    assert assinatura_valida(SEGREDO, corpo, sig)
    assert not assinatura_valida(SEGREDO, corpo, "sha256=errado")
    assert not assinatura_valida(SEGREDO, corpo, None)
    assert not assinatura_valida("", corpo, sig)


def test_dividir_texto():
    partes = dividir_texto("palavra " * 1500, limite=4000)
    assert len(partes) == 3 and all(len(p) <= 4000 for p in partes)
    assert dividir_texto("oi") == ["oi"]


def test_extrair_ignora_status():
    payload = {"entry": [{"changes": [{"value": {"statuses": [{"id": "x"}]}}]}]}
    assert extrair_mensagens(payload) == []


# ---------------- agente ----------------
def test_conversa_simples_guarda_memoria():
    a, mem, _, oa = montar(["Olá, Victor!"])
    assert a.responder("5511999999999", "oi", AGORA) == "Olá, Victor!"
    assert mem.historico("5511999999999", 10) == [
        {"role": "user", "content": "oi"},
        {"role": "assistant", "content": "Olá, Victor!"},
    ]
    sistema = oa.pedidos[0]["messages"][0]["content"]
    assert "segunda-feira, 09/11/2026 10:00" in sistema


def test_usa_ferramenta_de_agenda():
    a, _, google, oa = montar(
        [
            [chamada("criar_evento", {"titulo": "Dentista", "inicio": "2026-11-13T15:00:00-03:00",
                                      "fim": "2026-11-13T16:00:00-03:00", "descricao": None,
                                      "local": None, "dia_inteiro": False})],
            "Marquei *Dentista* sexta às 15h.",
        ]
    )
    assert "Dentista" in a.responder("5511999999999", "marca dentista sexta 15h", AGORA)
    assert google.eventos == ["Dentista"]
    resultado_ferramenta = oa.pedidos[1]["messages"][-1]
    assert resultado_ferramenta["role"] == "tool" and "ev1" in resultado_ferramenta["content"]


def test_email_nao_e_enviado_no_mesmo_turno_do_rascunho():
    a, _, google, oa = montar(
        [
            [chamada("criar_rascunho", {"para": "a@b.com", "assunto": "Oi", "corpo": "Teste",
                                        "responder_a_id": None}),
             chamada("enviar_rascunho", {}, "c2")],
            "Rascunho pronto. Posso enviar?",
            [chamada("enviar_rascunho", {})],
            "Enviado!",
        ]
    )
    a.responder("5511999999999", "manda um email pra a@b.com dizendo teste", AGORA)
    assert google.enviados == []  # bloqueado: ainda sem confirmação
    bloqueio = oa.pedidos[1]["messages"][-1]["content"]
    assert "bloqueado" in bloqueio

    a.responder("5511999999999", "pode enviar", AGORA)
    assert google.enviados == ["r1"]


def test_erro_de_ferramenta_vira_mensagem():
    mem = Memoria(":memory:")
    f = Ferramentas(GoogleFalso(), mem)
    saida = json.loads(f.executar("ler_email", '{"email_id": "x"}', Contexto("1", 1)))
    assert "erro" in saida


def test_comando_limpar():
    a, mem, _, _ = montar(["resposta"])
    a.responder("5511999999999", "oi", AGORA)
    assert "apagada" in a.responder("5511999999999", "/limpar", AGORA)
    assert mem.historico("5511999999999", 10) == []


# ---------------- servidor ----------------
class WhatsAppFalso:
    def __init__(self):
        self.enviados = []

    def enviar_texto(self, para, texto):
        self.enviados.append((para, texto))

    def marcar_lida(self, _id):
        pass


def payload_texto(numero, texto, id_="wamid.1"):
    return {"entry": [{"changes": [{"value": {"messages": [
        {"from": numero, "id": id_, "type": "text", "text": {"body": texto}}]}}]}]}


def postar(cliente, payload):
    corpo = json.dumps(payload).encode()
    sig = "sha256=" + hmac.new(SEGREDO.encode(), corpo, hashlib.sha256).hexdigest()
    return cliente.post("/webhook", content=corpo,
                        headers={"X-Hub-Signature-256": sig, "Content-Type": "application/json"})


def servidor(roteiro):
    mem = Memoria(":memory:")
    wa = WhatsAppFalso()
    assistente = Assistente(config(), mem, Ferramentas(GoogleFalso(), mem), OpenAIFalso(roteiro))
    return TestClient(criar_app(config(), assistente, wa, mem)), wa


def test_verificacao_do_webhook():
    c, _ = servidor([])
    ok = c.get("/webhook", params={"hub.mode": "subscribe", "hub.verify_token": "verifica", "hub.challenge": "123"})
    assert ok.status_code == 200 and ok.text == "123"
    assert c.get("/webhook", params={"hub.mode": "subscribe", "hub.verify_token": "x"}).status_code == 403


def test_webhook_responde_dono_ignora_estranhos_e_duplicadas():
    c, wa = servidor(["Oi Victor!"])
    assert postar(c, payload_texto("5511999999999", "oi")).status_code == 200
    assert postar(c, payload_texto("5511999999999", "oi")).status_code == 200  # reenvio da Meta
    assert postar(c, payload_texto("5521888888888", "me mostra os emails", "wamid.2")).status_code == 200
    assert wa.enviados == [("5511999999999", "Oi Victor!")]


def test_webhook_rejeita_sem_assinatura():
    c, _ = servidor([])
    r = c.post("/webhook", json=payload_texto("5511999999999", "oi"))
    assert r.status_code == 401
