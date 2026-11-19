#!/usr/bin/env bash
# Plantão em ciclos: espera o canal entrar ao vivo em GTA 6 e grava ciclos de 20 min (1080p60 + chat) em gravacoes/<canal>/cN/.
# Uso: plantao-ciclos.sh <canal> <n_ciclos>
cd "$(dirname "$0")/../gravacoes"
canal=$1; n=${2:-5}; log="ciclos-$canal.log"
categoria(){ timeout 40 streamlink --json "https://www.twitch.tv/$canal" 2>/dev/null | python3 -c "import sys,json
try:
  d=json.load(sys.stdin); print((d.get('metadata') or {}).get('category') or '' if d.get('streams') else '')
except: print('')"; }
until categoria | grep -qi "grand theft auto vi"; do sleep 60; done
echo "$(date -u +%H:%M) $canal começou GTA 6" >> "$log"
for k in $(seq 1 $n); do
  d="$canal/c$k"; mkdir -p "$d"; cp speed/chat.py "$d/"
  ( cd "$d" && date +%s > inicio.txt && nohup python3 chat.py "$canal" 1200 chat.jsonl > chat.log 2>&1 &
    timeout 1230 streamlink --twitch-disable-ads --hls-duration 00:20:00 -o live.ts "https://www.twitch.tv/$canal" 1080p60,1080p,best > rec.log 2>&1 )
  echo "$(date -u +%H:%M) CICLO_PRONTO $k" >> "$log"
  categoria | grep -qi "grand theft auto vi" || { echo "$(date -u +%H:%M) saiu do GTA 6 / live acabou" >> "$log"; break; }
done
echo "$(date -u +%H:%M) FIM" >> "$log"
