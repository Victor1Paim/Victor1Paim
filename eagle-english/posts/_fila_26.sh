#!/bin/bash
cd /home/user/Victor1Paim/eagle-english
S=/tmp/claude-0/-home-user-Victor1Paim/47b42f0e-b7c1-5615-b6eb-ba2706ed2548/scratchpad
export GEMINI_KEY_FILES=$S/gemini_paga.key:$S/gemini.key:$S/gemini_antiga.key PYTHONWARNINGS=ignore CHROMIUM_PATH=/opt/pw-browsers/chromium
V=posts/2026-11-26_verbo-aula07-say; A=posts/2026-11-26_abc-thanksgiving
python3 -u scripts/vozes.py gerar $V --so falas_en pt1 pt2 pt3 pt4 pt5 pt6 pt7 pt8 pt9 pt10 pt11 --minimo 85
python3 -u scripts/recortar_whisper.py $V/audio/falas_en.wav en $V/audio/en "Say." "Say it again." "What did you say?" "Said." "She said yes."
python3 -u scripts/vozes.py gerar $A --so perguntas_pt respostas_en cta --minimo 85
python3 -u scripts/recortar_whisper.py $A/audio/perguntas_pt.wav pt $A/audio/q "Hoje é Thanksgiving nos Estados Unidos! Em inglês, como se diz: feliz Dia de Ação de Graças?" "Como se diz: eu sou grato?" "Como se diz: peru, a comida?"
python3 -u scripts/recortar_whisper.py $A/audio/respostas_en.wav en $A/audio/r "Happy Thanksgiving!" "I'm thankful." "Turkey."
python3 -u scripts/montar_verbo.py $V
python3 -u scripts/montar_cta_produto.py anexar $V pc_nao_so_prova
python3 -u scripts/montar_abc.py $A
python3 -u scripts/montar_cta_produto.py anexar $A pc_viagem
echo FIM26
