#!/bin/bash
cd /home/user/Victor1Paim/eagle-english
S=/tmp/claude-0/-home-user-Victor1Paim/47b42f0e-b7c1-5615-b6eb-ba2706ed2548/scratchpad
export GEMINI_KEY_FILES=$S/gemini_paga.key:$S/gemini.key:$S/gemini_antiga.key PYTHONWARNINGS=ignore CHROMIUM_PATH=/opt/pw-browsers/chromium
V=assets/cta_produto/variantes
for v in pc_meio pc_mae pc_nao_so_prova pc_ja_tentou pc_viagem; do python3 -u scripts/vozes.py gerar $V/$v --minimo 85; done
# a chamada do meio: apara silêncio + 8% mais rápida (6,5 s), como em 25/11
mkdir -p $V/pc_meio/orig; for f in c1 c2 c3; do cp $V/pc_meio/audio/$f.wav $V/pc_meio/orig/$f.wav
  ffmpeg -nostdin -y -loglevel error -i $V/pc_meio/orig/$f.wav -af "silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.08,areverse,atempo=1.08" $V/pc_meio/audio/$f.wav; done
python3 -u scripts/montar_cta_produto.py pc_meio pc_mae pc_nao_so_prova pc_ja_tentou pc_viagem
P=posts/2026-11-26_verbo-aula07-say; A=posts/2026-11-26_abc-thanksgiving
python3 -u scripts/vozes.py gerar $P --so pt1 pt2 pt3 pt4 pt5 pt6 pt7 pt8 pt9 pt10 pt11 --minimo 85
python3 -u scripts/vozes.py gerar $A --so perguntas_pt cta --minimo 85
python3 -u scripts/recortar_whisper.py $A/audio/perguntas_pt.wav pt $A/audio/q "Hoje é Thanksgiving nos Estados Unidos! Em inglês, como se diz: feliz Dia de Ação de Graças?" "Como se diz: eu sou grato?" "Como se diz: peru, a comida?"
rm -f $P/video/final_sem_cta.mp4 $A/video/final_sem_cta.mp4
python3 -u scripts/montar_verbo.py $P
python3 -u scripts/montar_abc.py $A
echo FIMBR
