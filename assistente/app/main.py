"""Servidor do webhook do WhatsApp.

Rodar:  uvicorn app.main:criar_app --factory --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

import logging

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse

from .agente import Assistente
from .config import Config
from .ferramentas import Ferramentas
from .google_servicos import Google
from .memoria import Memoria
from .whatsapp import WhatsApp, assinatura_valida, extrair_mensagens

log = logging.getLogger("assistente")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


def criar_app(
    config: Config | None = None,
    assistente: Assistente | None = None,
    whatsapp: WhatsApp | None = None,
    memoria: Memoria | None = None,
) -> FastAPI:
    config = config or Config()
    memoria = memoria or Memoria(config.pasta_dados / "assistente.db")
    whatsapp = whatsapp or WhatsApp(config)
    if assistente is None:
        from openai import OpenAI

        assistente = Assistente(config, memoria, Ferramentas(Google(config), memoria), OpenAI())

    app = FastAPI(title="Assistente pessoal (WhatsApp)")

    @app.get("/")
    def saude() -> dict:
        return {"ok": True}

    @app.get("/webhook")
    def verificar(request: Request):
        p = request.query_params
        if p.get("hub.mode") == "subscribe" and p.get("hub.verify_token") == config.whatsapp_verify_token:
            return PlainTextResponse(p.get("hub.challenge", ""))
        raise HTTPException(status_code=403, detail="token de verificação inválido")

    @app.post("/webhook")
    async def receber(request: Request, tarefas: BackgroundTasks) -> dict:
        corpo = await request.body()
        if not assinatura_valida(config.whatsapp_app_secret, corpo, request.headers.get("X-Hub-Signature-256")):
            raise HTTPException(status_code=401, detail="assinatura inválida")
        payload = await request.json()
        for msg in extrair_mensagens(payload):
            tarefas.add_task(processar, msg)
        return {"ok": True}  # responder rápido; a Meta reenvia se demorar

    def processar(msg: dict) -> None:
        numero = msg.get("from", "")
        msg_id = msg.get("id", "")
        if not config.numero_permitido(numero):
            log.warning("Mensagem ignorada de número não autorizado: %s", numero)
            return
        if not memoria.marcar_processada(msg_id):
            return
        try:
            whatsapp.marcar_lida(msg_id)
            tipo = msg.get("type")
            if tipo == "text":
                texto = msg["text"]["body"]
            elif tipo == "audio":
                audio, mime = whatsapp.baixar_midia(msg["audio"]["id"])
                texto = assistente.transcrever(audio, mime)
                if not texto:
                    whatsapp.enviar_texto(numero, "Não consegui entender o áudio 😕 Pode repetir?")
                    return
            else:
                whatsapp.enviar_texto(numero, "Por enquanto entendo texto e áudio. 🙂")
                return
            resposta = assistente.responder(numero, texto)
            whatsapp.enviar_texto(numero, resposta)
        except Exception:
            log.exception("Erro ao processar mensagem %s", msg_id)
            try:
                whatsapp.enviar_texto(numero, "Deu um erro aqui do meu lado 😓 Tenta de novo daqui a pouco.")
            except Exception:
                log.exception("Falha ao avisar o erro")

    return app

