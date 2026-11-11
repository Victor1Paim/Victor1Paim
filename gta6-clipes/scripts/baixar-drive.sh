#!/usr/bin/env bash
# Baixa um vídeo da pasta compartilhada do Drive (acesso "qualquer pessoa com o link").
# Uso: scripts/baixar-drive.sh <id-do-arquivo> <nome.mp4>
# O id aparece no link do arquivo: drive.google.com/file/d/<id>/view
set -eu
id="$1"; nome="$2"
destino="$(cd "$(dirname "$0")/.." && pwd)/gravacoes/fontes"
mkdir -p "$destino"
curl -sSL -o "$destino/$nome" "https://drive.usercontent.google.com/download?id=$id&export=download&confirm=t"
if ! ffprobe -v error "$destino/$nome" >/dev/null 2>&1; then
  echo "Não é um vídeo válido: a pasta/arquivo ainda está como 'Restrito' no Drive?" >&2; rm -f "$destino/$nome"; exit 1
fi
ffprobe -v error -show_entries stream=codec_type,width,height:format=duration -of compact "$destino/$nome"
echo "ok: $destino/$nome"
