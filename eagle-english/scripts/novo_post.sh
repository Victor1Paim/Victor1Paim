#!/usr/bin/env bash
# Cria a pasta de um post novo.  Uso: bash scripts/novo_post.sh 2026-11-17 lavanderia
set -e
[ $# -eq 2 ] || { echo "Uso: bash scripts/novo_post.sh AAAA-MM-DD tema"; exit 1; }
cd "$(dirname "$0")/.."
P="posts/$1_$2"
mkdir -p "$P"/{slides,audio,video}
[ -f "$P/frases.json" ] || cat > "$P/frases.json" <<JSON
{
  "tema": "$2",
  "versao": "",
  "gancho": "",
  "situacao_ebook": "",
  "formato": "A",
  "frases": [
    {"en": "", "pt": "", "pron": ""}
  ]
}
JSON
echo "Criado $P — cole as frases do ChatGPT em $P/frases.json e os slides em $P/slides/"
