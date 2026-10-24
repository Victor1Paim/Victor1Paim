#!/usr/bin/env bash
# Prepara uma sessão nova: submódulo do OpenMontage, dependências do Remotion e do OpenMontage.
# Idempotente. Pode virar um hook SessionStart em .claude/settings.json.
set -u
raiz="$(cd "$(dirname "$0")/.." && pwd)"
cd "$raiz"

git submodule update --init --depth 1 ferramentas/OpenMontage >/dev/null 2>&1 || echo "aviso: não consegui baixar o OpenMontage"

if [ -f halftone/package.json ] && [ ! -d halftone/node_modules ]; then
  (cd halftone && npm ci --no-audit --no-fund >/dev/null 2>&1) || echo "aviso: npm ci falhou em halftone/"
fi

if [ -f ferramentas/OpenMontage/requirements.txt ] && ! python3 -c "import pydantic, yaml, dotenv, openai" >/dev/null 2>&1; then
  pip install -q -r ferramentas/OpenMontage/requirements.txt >/dev/null 2>&1 || echo "aviso: pip install do OpenMontage falhou"
fi
exit 0
