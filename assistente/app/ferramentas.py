"""Ferramentas que o modelo pode chamar (Agenda e Gmail) e o despachante."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from .memoria import Memoria


def _funcao(nome: str, descricao: str, propriedades: dict, obrigatorios: list[str]) -> dict:
    return {
        "type": "function",
        "function": {
            "name": nome,
            "description": descricao,
            "parameters": {
                "type": "object",
                "properties": propriedades,
                "required": obrigatorios,
                "additionalProperties": False,
            },
        },
    }


DATA_HORA = "Data/hora ISO 8601 com fuso, ex.: 2026-11-10T14:00:00-03:00"

DEFINICOES = [
    _funcao(
        "listar_eventos",
        "Lista eventos do Google Agenda num intervalo.",
        {
            "inicio": {"type": "string", "description": DATA_HORA},
            "fim": {"type": "string", "description": DATA_HORA},
        },
        ["inicio", "fim"],
    ),
    _funcao(
        "criar_evento",
        "Cria um evento no Google Agenda. Se faltar horário de término, use 1 hora de duração.",
        {
            "titulo": {"type": "string"},
            "inicio": {"type": "string", "description": DATA_HORA + " (ou AAAA-MM-DD se dia inteiro)"},
            "fim": {"type": "string", "description": DATA_HORA + " (ou AAAA-MM-DD do dia seguinte se dia inteiro)"},
            "descricao": {"type": ["string", "null"]},
            "local": {"type": ["string", "null"]},
            "dia_inteiro": {"type": "boolean"},
        },
        ["titulo", "inicio", "fim", "descricao", "local", "dia_inteiro"],
    ),
    _funcao(
        "buscar_emails",
        "Busca e-mails no Gmail usando a sintaxe de busca do Gmail "
        "(ex.: 'is:unread newer_than:1d', 'from:fulano', 'subject:boleto').",
        {
            "consulta": {"type": "string"},
            "maximo": {"type": "integer", "description": "1 a 20"},
        },
        ["consulta", "maximo"],
    ),
    _funcao(
        "ler_email",
        "Lê o conteúdo completo de um e-mail pelo id (obtido em buscar_emails).",
        {"email_id": {"type": "string"}},
        ["email_id"],
    ),
    _funcao(
        "criar_rascunho",
        "Cria um RASCUNHO de e-mail no Gmail (não envia). Use responder_a_id para responder a um e-mail.",
        {
            "para": {"type": "string"},
            "assunto": {"type": "string"},
            "corpo": {"type": "string"},
            "responder_a_id": {"type": ["string", "null"]},
        },
        ["para", "assunto", "corpo", "responder_a_id"],
    ),
    _funcao(
        "enviar_rascunho",
        "Envia o último rascunho criado. Só funciona depois que o dono viu o rascunho "
        "e confirmou o envio numa mensagem seguinte.",
        {},
        [],
    ),
]


@dataclass
class Contexto:
    numero: str
    turno: int  # id da mensagem do usuário que iniciou esta rodada


class Ferramentas:
    def __init__(self, google: Any, memoria: Memoria):
        self.google = google
        self.memoria = memoria

    def executar(self, nome: str, argumentos_json: str, ctx: Contexto) -> str:
        try:
            args = json.loads(argumentos_json or "{}")
            resultado = self._executar(nome, args, ctx)
        except Exception as erro:  # o modelo recebe o erro e explica ao usuário
            resultado = {"erro": f"{type(erro).__name__}: {erro}"}
        return json.dumps(resultado, ensure_ascii=False, default=str)

    def _executar(self, nome: str, a: dict, ctx: Contexto) -> Any:
        g = self.google
        if nome == "listar_eventos":
            return g.listar_eventos(a["inicio"], a["fim"])
        if nome == "criar_evento":
            return g.criar_evento(
                a["titulo"], a["inicio"], a["fim"], a.get("descricao"), a.get("local"), bool(a.get("dia_inteiro"))
            )
        if nome == "buscar_emails":
            maximo = max(1, min(int(a.get("maximo") or 10), 20))
            return g.buscar_emails(a["consulta"], maximo)
        if nome == "ler_email":
            return g.ler_email(a["email_id"])
        if nome == "criar_rascunho":
            r = g.criar_rascunho(a["para"], a["assunto"], a["corpo"], a.get("responder_a_id"))
            self.memoria.registrar_rascunho(ctx.numero, r["rascunho_id"], ctx.turno)
            r["aviso"] = "Rascunho criado. Mostre-o ao dono e peça confirmação antes de enviar."
            return r
        if nome == "enviar_rascunho":
            pendente = self.memoria.ultimo_rascunho(ctx.numero)
            if pendente is None:
                return {"erro": "Não há rascunho pendente. Crie um com criar_rascunho primeiro."}
            rascunho_id, turno = pendente
            if turno >= ctx.turno:
                return {
                    "erro": "Envio bloqueado: o dono ainda não confirmou. "
                    "Mostre o rascunho e espere ele responder confirmando."
                }
            r = g.enviar_rascunho(rascunho_id)
            self.memoria.remover_rascunho(rascunho_id)
            return r
        return {"erro": f"Ferramenta desconhecida: {nome}"}
