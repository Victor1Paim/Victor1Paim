#!/bin/sh
# Normaliza a voz de cada beat (alvo -13 LUFS, pico -1,5 dBTP) para assets/voz/proc/. A tocar no vídeo é a versão proc.
set -e
cd "$(dirname "$0")/.."
mkdir -p assets/voz/proc
for f in assets/voz/beat*.wav; do
  n=$(basename "$f")
  ffmpeg -hide_banner -loglevel error -y -i "$f" -af "loudnorm=I=-13:TP=-1.5:LRA=7" -ar 48000 -ac 1 "assets/voz/proc/$n"
done
echo "voz proc ok"
