#!/bin/bash
cd /home/user/Victor1Paim/eagle-english
S=/tmp/claude-0/-home-user-Victor1Paim/47b42f0e-b7c1-5615-b6eb-ba2706ed2548/scratchpad
export GEMINI_KEY_FILES=$S/gemini_paga.key:$S/gemini.key:$S/gemini_antiga.key PYTHONWARNINGS=ignore CHROMIUM_PATH=/opt/pw-browsers/chromium
V=posts/2026-11-27_verbo-aula08-see; L=posts/2026-11-27_lista12-compras
python3 -u scripts/vozes.py gerar $V --so pt1 pt2 pt3 pt4 pt5 pt6 pt7 pt8 pt9 pt10 pt11 en1 en2 en3 en4 en5 --minimo 85
python3 -u scripts/vozes.py gerar $L --so perguntas_pt respostas_en rg1 rg2 rg3 cta --minimo 85
python3 - <<'PY'
import json,subprocess
L="posts/2026-11-27_lista12-compras"; f={x["id"]:x["texto"] for x in json.load(open(L+"/falas.json"))["falas"]}
subprocess.run(["python3","-u","scripts/recortar_whisper.py",L+"/audio/perguntas_pt.wav","pt",L+"/audio/q",*[f[f"q{i}"] for i in range(1,13)]],check=True)
subprocess.run(["python3","-u","scripts/recortar_whisper.py",L+"/audio/respostas_en.wav","en",L+"/audio/r",*[f[f"r{i}"] for i in range(1,13)]],check=True)
PY
python3 -u scripts/montar_verbo.py $V
python3 -u scripts/montar_lista12.py $L
echo FIM27
