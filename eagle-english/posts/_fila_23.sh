#!/bin/bash
set -x
cd /home/user/Victor1Paim/eagle-english
S=/tmp/claude-0/-home-user-Victor1Paim/47b42f0e-b7c1-5615-b6eb-ba2706ed2548/scratchpad
export GEMINI_KEY_FILES=$S/gemini.key:$S/gemini_paga.key:$S/gemini_antiga.key PYTHONWARNINGS=ignore CHROMIUM_PATH=/opt/pw-browsers/chromium-1243/chrome-linux64/chrome
V=posts/2026-11-23_verbo-aula04-go; L=posts/2026-11-23_lista12-restaurante
python3 -u scripts/vozes.py gerar $V --so falas_en pt1 pt2 pt3 pt4 pt5 pt6 pt7 pt8 pt9 pt10 pt11 --minimo 85
python3 -u scripts/recortar_whisper.py $V/audio/falas_en.wav en $V/audio/en "Go." "I go to work." "Let's go!" "Went." "We went home."
python3 -u scripts/montar_verbo.py $V
python3 -u scripts/vozes.py gerar $L --so perguntas_pt respostas_en rg1 rg2 rg3 cta --minimo 85
python3 - <<'PY'
import json,subprocess
L="posts/2026-11-23_lista12-restaurante"; d=json.load(open(L+"/lista.json")); f={x["id"]:x["texto"] for x in json.load(open(L+"/falas.json"))["falas"]}
qs=[f[f"q{i+1}"] for i in range(12)]; rs=[f[f"r{i+1}"] for i in range(12)]
subprocess.run(["python3","-u","scripts/recortar_whisper.py",L+"/audio/perguntas_pt.wav","pt",L+"/audio/q",*qs],check=True)
subprocess.run(["python3","-u","scripts/recortar_whisper.py",L+"/audio/respostas_en.wav","en",L+"/audio/r",*rs],check=True)
PY
python3 -u scripts/montar_lista12.py $L
python3 -u scripts/carrossel_tt.py posts/2026-11-23_carrossel-repita-4
echo FIM23
