#!/bin/bash
cd /home/user/Victor1Paim/eagle-english
S=/tmp/claude-0/-home-user-Victor1Paim/47b42f0e-b7c1-5615-b6eb-ba2706ed2548/scratchpad
export GEMINI_KEY_FILES=$S/gemini_paga.key:$S/gemini.key:$S/gemini_antiga.key PYTHONWARNINGS=ignore CHROMIUM_PATH=/opt/pw-browsers/chromium
P=posts/2026-11-25_lista12-respostas-curtas
python3 -u scripts/vozes.py gerar $P --so perguntas2_pt respostas2_en rg3 cta --minimo 80
python3 -u scripts/recortar_whisper.py $P/audio/perguntas2_pt.wav pt $P/audio/qn "Como se diz: acho que sim?" "Como se diz: nem tanto?" "Como se diz: nunca?" "Como se diz: que ótimo?"
python3 -u scripts/recortar_whisper.py $P/audio/respostas2_en.wav en $P/audio/rn "I think so." "Not really." "Never!" "Great!"
for k in 1 2 3 4; do mv $P/audio/qn$k.wav $P/audio/q$((k+8)).wav; mv $P/audio/rn$k.wav $P/audio/r$((k+8)).wav; done
rm -f $P/video/final_sem_cta.mp4
python3 -u scripts/montar_lista12.py $P
python3 -u scripts/montar_cta_produto.py anexar $P pc_ja_tentou
echo FIML12B
