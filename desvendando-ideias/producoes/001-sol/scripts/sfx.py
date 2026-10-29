#!/usr/bin/env python3
"""Sintetiza o som de cronômetro (e um sino curto na revelação) e grava assets/sfx/sfx-mix.wav
com os eventos nos tempos de build-out.json. Só biblioteca padrão; determinístico (ruído com semente)."""
import json, math, random, struct, wave, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
info = json.load(open(os.path.join(ROOT, 'build-out.json')))
shots = {s['id']: s for s in info['shots']}
N = int((info['total'] + 0.5) * SR)
buf = [0.0] * N
rng = random.Random(20261029)

def add(t, samples, gain=1.0):
    i0 = int(t * SR)
    for k, v in enumerate(samples):
        if 0 <= i0 + k < N:
            buf[i0 + k] += v * gain

def tick(freq, dur=0.05, noise=0.5):
    n = int(dur * SR)
    return [(math.sin(2 * math.pi * freq * k / SR) * math.exp(-k / (0.007 * SR)) + noise * (rng.random() * 2 - 1) * math.exp(-k / (0.003 * SR))) for k in range(n)]

def beep(freq, dur=0.22):
    n = int(dur * SR); fade = int(0.012 * SR)
    out = []
    for k in range(n):
        env = min(1, k / fade, (n - k) / fade)
        out.append(math.sin(2 * math.pi * freq * k / SR) * env)
    return out

def chime(dur=0.7):
    n = int(dur * SR)
    return [(math.sin(2 * math.pi * 1318.5 * k / SR) + 0.6 * math.sin(2 * math.pi * 1760 * k / SR)) * math.exp(-k / (0.18 * SR)) for k in range(n)]

# cronômetro: tique-taque a cada 0,5 s do início do quiz com barra até o fim da contagem 3-2-1
quiz = shots.get('b0s4'); guess = next((s for s in info['shots'] if s['k'] == 'guess'), None)
if quiz and guess:
    t0, t1 = quiz['start'], guess['start'] + guess['dur']
    t, i = t0, 0
    while t < t1 - 0.05:
        loud = t >= guess['start']  # na contagem 3-2-1 os tiques ficam mais fortes
        add(t, tick(2300 if i % 2 == 0 else 1700), 0.55 if loud else 0.32)
        t += 0.5; i += 1
    add(t1 - 0.22, beep(880), 0.35)   # bipe de fim de tempo, antes da voz seguinte
ans = shots.get('b2s9')
if ans:
    add(ans['start'] + 0.05, chime(), 0.35)

peak = max(abs(x) for x in buf) or 1
scale = 0.85 / peak if peak > 0.85 else 1
os.makedirs(os.path.join(ROOT, 'assets/sfx'), exist_ok=True)
with wave.open(os.path.join(ROOT, 'assets/sfx/sfx-mix.wav'), 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(b''.join(struct.pack('<h', int(max(-1, min(1, x * scale)) * 32767)) for x in buf))
print('sfx ok')
