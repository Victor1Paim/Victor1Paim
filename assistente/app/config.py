"""Configuração lida das variáveis de ambiente (arquivo .env na pasta assistente/)."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parent.parent
load_dotenv(RAIZ / ".env")


def _lista(valor: str) -> set[str]:
    return {so_digitos(v) for v in valor.split(",") if so_digitos(v)}


def so_digitos(numero: str) -> str:
    return "".join(c for c in numero if c.isdigit())


@dataclass(frozen=True)
class Config:
    whatsapp_token: str = field(default_factory=lambda: os.getenv("WHATSAPP_TOKEN", ""))
    whatsapp_phone_number_id: str = field(default_factory=lambda: os.getenv("WHATSAPP_PHONE_NUMBER_ID", ""))
    whatsapp_verify_token: str = field(default_factory=lambda: os.getenv("WHATSAPP_VERIFY_TOKEN", ""))
    whatsapp_app_secret: str = field(default_factory=lambda: os.getenv("WHATSAPP_APP_SECRET", ""))
    whatsapp_api_version: str = field(default_factory=lambda: os.getenv("WHATSAPP_API_VERSION", "v23.0"))
    numeros_permitidos: set[str] = field(default_factory=lambda: _lista(os.getenv("NUMEROS_PERMITIDOS", "")))

    openai_modelo: str = field(default_factory=lambda: os.getenv("OPENAI_MODELO", "gpt-5.4-mini"))
    openai_modelo_transcricao: str = field(
        default_factory=lambda: os.getenv("OPENAI_MODELO_TRANSCRICAO", "gpt-4o-mini-transcribe")
    )

    google_token_arquivo: Path = field(
        default_factory=lambda: RAIZ / os.getenv("GOOGLE_TOKEN_ARQUIVO", "token.json")
    )
    google_token_json: str = field(default_factory=lambda: os.getenv("GOOGLE_TOKEN_JSON", ""))
    google_agenda_id: str = field(default_factory=lambda: os.getenv("GOOGLE_AGENDA_ID", "primary"))

    fuso_horario: str = field(default_factory=lambda: os.getenv("FUSO_HORARIO", "America/Sao_Paulo"))
    nome_dono: str = field(default_factory=lambda: os.getenv("NOME_DONO", "Victor"))
    pasta_dados: Path = field(default_factory=lambda: RAIZ / os.getenv("PASTA_DADOS", "dados"))
    memoria_mensagens: int = field(default_factory=lambda: int(os.getenv("MEMORIA_MENSAGENS", "20")))

    def numero_permitido(self, numero: str) -> bool:
        return so_digitos(numero) in self.numeros_permitidos
