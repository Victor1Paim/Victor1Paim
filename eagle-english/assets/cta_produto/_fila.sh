#!/bin/bash
cd /home/user/Victor1Paim/eagle-english
S=/tmp/claude-0/-home-user-Victor1Paim/47b42f0e-b7c1-5615-b6eb-ba2706ed2548/scratchpad
export GEMINI_KEY_FILES=$S/gemini_paga.key:$S/gemini.key:$S/gemini_antiga.key PYTHONWARNINGS=ignore CHROMIUM_PATH=/opt/pw-browsers/chromium-1243/chrome-linux64/chrome
for v in facil_ler facil_sem_gramatica facil_dez_minutos; do python3 -u scripts/vozes.py gerar assets/cta_produto/variantes/$v --minimo 88; done
python3 -u scripts/montar_cta_produto.py facil_ler facil_sem_gramatica facil_dez_minutos imigracao
python3 -u scripts/montar_lista12.py posts/2026-11-23_lista12-restaurante
python3 -u scripts/montar_cta_produto.py anexar posts/2026-11-23_verbo-aula04-go facil_ler
python3 -u scripts/montar_cta_produto.py anexar posts/2026-11-23_lista12-restaurante facil_sem_gramatica
echo FIMCTA
