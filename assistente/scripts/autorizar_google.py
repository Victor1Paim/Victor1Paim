"""Autoriza o assistente a usar seu Google Agenda e Gmail.

1. No Google Cloud Console, crie um "ID do cliente OAuth" do tipo *App para computador*
   e baixe o JSON como `credentials.json` dentro da pasta `assistente/`.
2. Rode no seu computador (abre o navegador para você entrar na conta):

       python scripts/autorizar_google.py

3. Será criado `token.json`. Em servidor, cole o conteúdo dele em GOOGLE_TOKEN_JSON.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from google_auth_oauthlib.flow import InstalledAppFlow  # noqa: E402

from app.google_servicos import ESCOPOS  # noqa: E402


def main() -> None:
    credenciais = RAIZ / "credentials.json"
    if not credenciais.exists():
        sys.exit(f"Não achei {credenciais}. Baixe o JSON do cliente OAuth (App para computador) e salve aí.")
    fluxo = InstalledAppFlow.from_client_secrets_file(str(credenciais), ESCOPOS)
    cred = fluxo.run_local_server(port=0, prompt="consent", access_type="offline")
    destino = RAIZ / "token.json"
    destino.write_text(cred.to_json())
    print(f"Pronto! Token salvo em {destino}")


if __name__ == "__main__":
    main()
