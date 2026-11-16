#!/bin/bash
# Instalação do kit (Mac/Linux). Antes: Node.js LTS, Python 3.11+ e FFmpeg (no Mac: brew install node python ffmpeg).
set -e
cd "$(dirname "$0")"
command -v node >/dev/null || { echo "FALTA o Node.js (brew install node)"; exit 1; }
command -v python3 >/dev/null || { echo "FALTA o Python (brew install python)"; exit 1; }
command -v ffmpeg >/dev/null || { echo "FALTA o FFmpeg (brew install ffmpeg)"; exit 1; }
python3 -m pip install -r requirements.txt
(cd video && npm install)
echo; echo "Tudo instalado. Teste com:  python3 scripts/kit.py tudo demo-cafezinho"
