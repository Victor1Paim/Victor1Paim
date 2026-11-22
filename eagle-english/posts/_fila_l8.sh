#!/bin/bash
cd /home/user/Victor1Paim/eagle-english
S=/tmp/claude-0/-home-user-Victor1Paim/47b42f0e-b7c1-5615-b6eb-ba2706ed2548/scratchpad
export GEMINI_KEY_FILES=$S/gemini_paga.key:$S/gemini.key:$S/gemini_antiga.key PYTHONWARNINGS=ignore CHROMIUM_PATH=/opt/pw-browsers/chromium-1243/chrome-linux64/chrome
P=posts/2026-11-23_lista12-restaurante
python3 -u scripts/vozes.py gerar $P --so perguntas2_pt respostas2_en --minimo 80
python3 -u scripts/recortar_whisper.py $P/audio/perguntas2_pt.wav pt $P/audio/qn "Em inglês, como se diz: sem gelo, por favor?" "Como se diz: só água?" "Como se diz: mais pão, por favor?" "Como se diz: sem açúcar, por favor?"
python3 -u scripts/recortar_whisper.py $P/audio/respostas2_en.wav en $P/audio/rn "No ice, please." "Just water." "More bread, please." "No sugar, please."
rm -f $P/video/final_sem_cta.mp4
python3 -u scripts/montar_lista12.py $P
python3 -u scripts/montar_cta_produto.py anexar $P facil_sem_gramatica
echo FIML8
