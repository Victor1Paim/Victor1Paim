#!/usr/bin/env bash
# Prepara o notebook para produzir os vídeos do Eagle English.
# Uso (na pasta eagle-english/):  bash scripts/preparar.sh
set -e
cd "$(dirname "$0")/.."
command -v ffmpeg >/dev/null || echo "!! Instale o ffmpeg (Windows: winget install ffmpeg | Mac: brew install ffmpeg | Linux: apt install ffmpeg)"
python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate
pip install -q --upgrade pip
pip install -q playwright pillow pydub numpy requests python-dotenv openai-whisper
python3 -m playwright install chromium
[ -f .env ] || { cp .env.example .env; echo "Criado .env: coloque sua GEMINI_API_KEY nele."; }
echo "Pronto. Ative o ambiente com: source .venv/bin/activate"
