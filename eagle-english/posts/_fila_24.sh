#!/bin/bash
cd /home/user/Victor1Paim/eagle-english
S=/tmp/claude-0/-home-user-Victor1Paim/47b42f0e-b7c1-5615-b6eb-ba2706ed2548/scratchpad
export GEMINI_KEY_FILES=$S/gemini_paga.key:$S/gemini.key:$S/gemini_antiga.key PYTHONWARNINGS=ignore CHROMIUM_PATH=/opt/pw-browsers/chromium-1243/chrome-linux64/chrome
V=posts/2026-11-24_verbo-aula05-have; A=posts/2026-11-24_abc-comida
python3 -u scripts/vozes.py gerar $V --so falas_en pt1 pt2 pt3 pt4 pt5 pt6 pt7 pt8 pt9 pt10 pt11 --minimo 85
python3 -u scripts/recortar_whisper.py $V/audio/falas_en.wav en $V/audio/en "Have." "I have a dog." "I have a question." "Had." "I had lunch."
python3 -u scripts/vozes.py gerar $A --so perguntas_pt respostas_en cta --minimo 85
python3 -u scripts/recortar_whisper.py $A/audio/perguntas_pt.wav pt $A/audio/q "Em inglês, como se diz: tá uma delícia?" "Como se diz: muito bom?" "Como se diz: quero mais?"
python3 -u scripts/recortar_whisper.py $A/audio/respostas_en.wav en $A/audio/r "It's yummy!" "So good!" "I want more!"
python3 -u scripts/montar_verbo.py $V
python3 -u scripts/montar_cta_produto.py anexar $V facil_dez_minutos
python3 -u scripts/montar_abc.py $A
python3 -u scripts/montar_cta_produto.py anexar $A imigracao
echo FIM24
