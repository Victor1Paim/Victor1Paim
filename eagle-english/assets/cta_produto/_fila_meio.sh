#!/bin/bash
cd /home/user/Victor1Paim/eagle-english
S=/tmp/claude-0/-home-user-Victor1Paim/47b42f0e-b7c1-5615-b6eb-ba2706ed2548/scratchpad
export GEMINI_KEY_FILES=$S/gemini_paga.key:$S/gemini.key:$S/gemini_antiga.key PYTHONWARNINGS=ignore CHROMIUM_PATH=/opt/pw-browsers/chromium
V=assets/cta_produto/variantes
python3 -u scripts/vozes.py gerar $V/pc_meio --minimo 85
for v in pc_mae pc_nao_so_prova pc_ja_tentou pc_viagem; do python3 -u scripts/vozes.py gerar $V/$v --so c3 --minimo 85; done
python3 -u scripts/montar_cta_produto.py pc_meio pc_mae pc_nao_so_prova pc_ja_tentou pc_viagem
python3 -u scripts/montar_cta_produto.py anexar posts/2026-11-25_verbo-aula06-do pc_mae
python3 -u scripts/montar_cta_produto.py anexar posts/2026-11-25_lista12-respostas-curtas pc_ja_tentou
echo FIMMEIO
