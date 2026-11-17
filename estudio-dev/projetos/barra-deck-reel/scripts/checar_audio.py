"""Checa narrações: palavras (Whisper), cortes/silêncios no meio de frase, picos e duração.

Uso: python3 scripts/checar_audio.py roteiro.txt audio1.mp3 [audio2.mp3 ...]
Grava <audio>.json com as palavras e tempos (usado para sincronizar o vídeo).
"""
import json
import os
import re
import subprocess
import sys
import unicodedata

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import narracao  # noqa: E402  (transcrever via Whisper)

NUM = {'10': 'dez', '24': 'vinte e quatro', '15': 'quinze'}


def norm(t):
    t = t.lower()
    for k, v in NUM.items():
        t = re.sub(rf'\b{k}\b', v, t)
    t = t.replace('barradec', 'barra deck').replace('barradeck', 'barra deck').replace('qr code', 'qr code')
    t = unicodedata.normalize('NFKD', t)
    t = ''.join(c for c in t if not unicodedata.combining(c))
    return re.findall(r"[a-z]+", t)


def checar(roteiro, mp3):
    wav = mp3 + '.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mp3, '-ac', '1', '-ar', '24000', '-f', 'f32le', wav], check=True)
    a = np.fromfile(wav, dtype=np.float32)
    os.unlink(wav)
    sr = 24000
    dur = len(a) / sr
    pico = 20 * np.log10(np.max(np.abs(a)) + 1e-9)
    t = narracao.transcrever(mp3)
    pal = t.get('words', [])
    json.dump({'duracao': dur, 'texto': t.get('text'), 'palavras': pal}, open(mp3 + '.json', 'w'), ensure_ascii=False, indent=1)
    esperado, ouvido = norm(roteiro), norm(t.get('text', ''))
    # diferença de palavras (multiconjunto)
    from collections import Counter
    faltam = Counter(esperado) - Counter(ouvido)
    sobram = Counter(ouvido) - Counter(esperado)
    # silêncio digital (< -65 dB) com mais de 120 ms entre o início e o fim da fala
    win = int(0.01 * sr)
    rms = np.array([np.sqrt(np.mean(a[i:i + win] ** 2) + 1e-12) for i in range(0, len(a) - win, win)])
    db = 20 * np.log10(rms)
    falando = np.nonzero(db > -45)[0]
    buracos = []
    if len(falando):
        i0, i1 = falando[0], falando[-1]
        run = 0
        for i in range(i0, i1):
            if db[i] < -65:
                run += 1
            else:
                if run * 0.01 >= 0.12:
                    buracos.append(((i - run) * 0.01, run * 0.01))
                run = 0
    # pausas entre palavras maiores que 0,9 s
    pausas = [(round(pal[i]['end'], 2), round(pal[i + 1]['start'] - pal[i]['end'], 2))
              for i in range(len(pal) - 1) if pal[i + 1]['start'] - pal[i]['end'] > 0.9]
    return {'arquivo': os.path.basename(mp3), 'duracao': round(dur, 2), 'pico_dB': round(float(pico), 1),
            'faltam': dict(faltam), 'sobram': dict(sobram), 'silencios_digitais': [(round(x, 2), round(y, 2)) for x, y in buracos],
            'pausas_longas': pausas, 'texto': t.get('text')}


if __name__ == '__main__':
    roteiro = open(sys.argv[1]).read()
    for mp3 in sys.argv[2:]:
        r = checar(roteiro, mp3)
        print(json.dumps(r, ensure_ascii=False))
