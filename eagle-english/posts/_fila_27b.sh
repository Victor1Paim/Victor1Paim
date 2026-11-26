#!/bin/bash
cd /home/user/Victor1Paim/eagle-english
until grep -qE "FIM27|Traceback" posts/_fila_27.log; do sleep 10; done
S=/tmp/claude-0/-home-user-Victor1Paim/47b42f0e-b7c1-5615-b6eb-ba2706ed2548/scratchpad
export GEMINI_KEY_FILES=$S/gemini_paga.key:$S/gemini.key:$S/gemini_antiga.key PYTHONWARNINGS=ignore CHROMIUM_PATH=/opt/pw-browsers/chromium
V=posts/2026-11-27_verbo-aula08-see; L=posts/2026-11-27_lista12-compras
python3 - <<'PY'
import json
from pathlib import Path
p=Path("posts/2026-11-27_lista12-compras/falas.json"); f=json.loads(p.read_text())
for x in f["falas"]:
    if x["id"]=="r8": x["texto"]="Cash, or card?"
p.write_text(json.dumps(f,ensure_ascii=False,indent=1))
PY
ok(){ python3 -W ignore -c "
import whisper,sys;t=whisper.load_model('base.en').transcribe('$1')['text'].strip().lower();print('   ->',t);sys.exit(0 if all(w in t for w in '$2'.split()) and '?' not in t[-1:] or '$3'=='q' and all(w in t for w in '$2'.split()) else 1)"; }
for i in 1 2 3 4 5; do python3 -u scripts/vozes.py gerar $V --so en1 --minimo 80 | grep tentativa; ok $V/audio/en1.wav "see" && break; done
for i in 1 2 3 4 5; do python3 -u scripts/vozes.py gerar $L --so r8 --minimo 80 | grep tentativa; ok $L/audio/r8.wav "cash card" q && break; done
rm -f $V/video/final_sem_cta.mp4 $L/video/final_sem_cta.mp4
python3 -u scripts/montar_verbo.py $V
python3 -u scripts/montar_lista12.py $L
echo FIM27B
