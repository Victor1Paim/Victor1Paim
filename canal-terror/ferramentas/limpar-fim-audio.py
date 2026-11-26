#!/usr/bin/env python3
"""Remove o estalo/ruído que o Gemini TTS deixa nos últimos ~150 ms do áudio.
Procura, do fim para o começo, o trecho final barulhento depois de um silêncio e corta no silêncio, com fade de 40 ms.
Uso: limpar-fim-audio.py entrada.mp3 [saida.mp3]  (sem saída: sobrescreve)"""
import subprocess, sys, numpy as np, os, tempfile
ent = sys.argv[1]; sai = sys.argv[2] if len(sys.argv) > 2 else ent
sr = 24000
pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', ent, '-f', 's16le', '-ac', '1', '-ar', str(sr), '-'], capture_output=True, check=True).stdout
a = np.frombuffer(pcm, np.int16).astype(float) / 32768
jan = int(0.02 * sr)
rms = [20 * np.log10(np.sqrt(np.mean(a[i:i + jan] ** 2)) + 1e-9) for i in range(0, len(a) - jan, jan)]
i = len(rms) - 1
while i > 0 and rms[i] > -45:      # rajada final
    i -= 1
silencio_fim = i
while i > 0 and rms[i] <= -45:     # silêncio antes dela
    i -= 1
if len(rms) - silencio_fim > 15 or silencio_fim == i:   # nada de rajada curta no fim: não mexe
    corte = len(a) / sr
else:
    corte = min((i + 1) * jan / sr + 0.25, silencio_fim * jan / sr - 0.04)
tmp = tempfile.mktemp(suffix='.mp3')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', ent, '-t', f'{corte:.3f}', '-af', f'afade=t=out:st={max(corte - 0.04, 0):.3f}:d=0.04', '-b:a', '128k', tmp], check=True)
os.replace(tmp, sai)
print(f'{ent}: {len(a) / sr:.2f}s -> {corte:.2f}s')
