#!/usr/bin/env bash
# Plantão GTA 6: a cada 2 min verifica os canais (em ordem de prioridade); o primeiro AO VIVO na categoria
# "Grand Theft Auto VI" é gravado por 30 min (1080p60) + chat em gravacoes/<canal>/. Uso: plantao-gta.sh <nome-do-plantao> canal1 canal2 ...
cd "$(dirname "$0")/../gravacoes"
nome=$1; shift
log="plantao-$nome.log"
for i in $(seq 1 360); do   # até 12 h
  for canal in "$@"; do
    cat=$(timeout 40 streamlink --json "https://www.twitch.tv/$canal" 2>/dev/null | python3 -c "import sys,json
try:
  d=json.load(sys.stdin); print((d.get('metadata') or {}).get('category') or '' if d.get('streams') else '')
except: print('')")
    if echo "$cat" | grep -qi "grand theft auto vi"; then
      echo "$(date -u +%H:%M) $canal AO VIVO em GTA 6 - gravando" >> "$log"
      mkdir -p "$canal" && cp speed/chat.py "$canal/" && cd "$canal"
      date +%s > inicio.txt
      nohup python3 chat.py "$canal" 1800 chat.jsonl > chat.log 2>&1 &
      timeout 1830 streamlink --twitch-disable-ads --hls-duration 00:30:00 -o live.ts "https://www.twitch.tv/$canal" 1080p60,1080p,best > rec.log 2>&1
      cd ..
      echo "$(date -u +%H:%M) GRAVACAO_PRONTA $canal" >> "$log"
      exit 0
    fi
  done
  sleep 120
done
echo "$(date -u +%H:%M) nenhum entrou em GTA 6 em 12 h" >> "$log"
