#!/usr/bin/env python3
"""Trilha de efeitos sonoros do vídeo, planejada por tipo de plano (lê build-out.json).

- Efeitos reais: biblioteca offline da skill media-use (motor/sfx-lib/, licença Pixabay) para whoosh, pop, impacto, ping, erro, sparkle, sino.
- Efeitos sintetizados (o que a biblioteca não tem): cronômetro (tique-taque), contagem de números (roleta de cliques), zíper de traço,
  líquido (água enchendo, gota, respingo), "plips" de empilhamento, subida e queda, baque.
- Cada efeito nasce de algo que aparece na tela (regra do HyperFrames): o pico cai ~1 quadro depois da imagem.
Só biblioteca padrão + ffmpeg. Determinístico (semente fixa). Saída: assets/sfx/sfx-mix.wav (estéreo, 48 kHz).
"""
import json, math, os, random, struct, subprocess, wave

import sys
ROOT = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.getcwd()   # pasta do vídeo
MOTOR = os.path.dirname(os.path.abspath(__file__))
SR = 48000
info = json.load(open(os.path.join(ROOT, 'build-out.json')))
shots, beats = info['shots'], info['beats']
N = int((info['total'] + 0.6) * SR)
BUF = [[0.0] * N, [0.0] * N]
rng = random.Random(20261029)
LIB = os.path.join(MOTOR, 'sfx-lib')
FRAME = 1 / 30
COUNT = {}

# ---------------------------------------------------------------- utilidades
_cache = {}
def load(name):
    if name not in _cache:
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(LIB, name + '.mp3'), '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
        _cache[name] = list(struct.unpack('<%df' % (len(raw) // 4), raw))
    return _cache[name]

def peak_idx(a):
    m, ix = 0.0, 0
    for i, v in enumerate(a):
        if abs(v) > m: m, ix = abs(v), i
    return ix

def trim(a, dur, fade=0.06):
    n = min(len(a), int(dur * SR)); out = a[:n]; f = min(int(fade * SR), n)
    for k in range(f): out[n - f + k] *= 1 - k / f
    return out

def pitch(a, ratio):
    n = int(len(a) / ratio); out = []
    for i in range(n):
        x = i * ratio; j = int(x); fr = x - j
        out.append(a[j] * (1 - fr) + (a[j + 1] if j + 1 < len(a) else 0.0) * fr)
    return out

def place(a, t, g=1.0, pan=0.0, pan_to=None, peak_at=None, tag='fx'):
    start = int((peak_at - peak_idx(a) / SR) * SR) if peak_at is not None else int(t * SR)
    n = len(a); COUNT[tag] = COUNT.get(tag, 0) + 1
    for k in range(n):
        i = start + k
        if i < 0 or i >= N: continue
        p = pan if pan_to is None else pan + (pan_to - pan) * k / max(1, n - 1)
        th = (max(-1, min(1, p)) + 1) * math.pi / 4
        v = a[k] * g
        BUF[0][i] += v * math.cos(th); BUF[1][i] += v * math.sin(th)

# ---------------------------------------------------------------- sintetizados
def env_exp(n, tau): return [math.exp(-k / (tau * SR)) for k in range(n)]

def s_tick(freq=2300, dur=0.05, noise=0.5):
    n = int(dur * SR)
    return [(math.sin(2 * math.pi * freq * k / SR) * math.exp(-k / (0.007 * SR)) + noise * (rng.random() * 2 - 1) * math.exp(-k / (0.003 * SR))) for k in range(n)]

def s_plip(f=700, dur=0.035):
    n = int(dur * SR)
    return [math.sin(2 * math.pi * (f * (1 + 0.5 * k / n)) * k / SR) * math.exp(-k / (0.009 * SR)) for k in range(n)]

def s_thud(dur=0.25):
    n = int(dur * SR); ph = 0.0; out = []
    for k in range(n):
        f = 45 + 110 * math.exp(-k / (0.045 * SR)); ph += 2 * math.pi * f / SR
        out.append(math.sin(ph) * math.exp(-k / (0.07 * SR)) + 0.35 * (rng.random() * 2 - 1) * math.exp(-k / (0.004 * SR)))
    return out

def s_beep(freq=880, dur=0.22):
    n = int(dur * SR); fd = int(0.012 * SR)
    return [math.sin(2 * math.pi * freq * k / SR) * min(1, k / fd, (n - k) / fd) for k in range(n)]

def s_zip(dur=0.7, f0=350, f1=2800):
    n = int(dur * SR); ph = 0.0; out = []
    for k in range(n):
        x = k / n; ph += 2 * math.pi * (f0 * (f1 / f0) ** x) / SR
        out.append((math.sin(ph) * 0.6 + (rng.random() * 2 - 1) * 0.25) * math.sin(math.pi * min(1, x * 1.2)) ** 0.5 * (1 - 0.4 * x))
    return out

def s_rise(dur=1.0, f0=220, f1=1400):
    n = int(dur * SR); ph = 0.0; out = []
    for k in range(n):
        x = k / n; ph += 2 * math.pi * (f0 + (f1 - f0) * x * x) / SR
        out.append(math.sin(ph) * (0.15 + 0.85 * x) * (1 if x < 0.97 else (1 - x) / 0.03))
    return out

def s_fall(dur=0.5, f0=1000, f1=220):
    n = int(dur * SR); ph = 0.0; out = []
    for k in range(n):
        x = k / n; ph += 2 * math.pi * (f0 * (f1 / f0) ** x) / SR
        out.append(math.sin(ph) * (1 - x) ** 0.7)
    return out

def lowpass(a, cutoff):
    rc = 1 / (2 * math.pi * cutoff); dt = 1 / SR; al = dt / (rc + dt); y = 0.0; out = []
    for v in a: y += al * (v - y); out.append(y)
    return out

def s_splash(dur=0.45):
    n = int(dur * SR)
    return lowpass([(rng.random() * 2 - 1) * math.exp(-k / (0.11 * SR)) for k in range(n)], 2600)

def s_water(dur):
    n = int(dur * SR); out = lowpass([(rng.random() * 2 - 1) * 0.5 for _ in range(n)], 900)
    for _ in range(int(dur * 14)):  # bolhas
        t0 = int(rng.random() * (n - 3000)); f = 500 + rng.random() * 900; L = int(0.03 * SR)
        for k in range(L): out[t0 + k] += math.sin(2 * math.pi * f * (1 + k / L) * k / SR) * math.exp(-k / (0.008 * SR)) * 0.5
    for k in range(n): out[k] *= min(1, k / (0.1 * SR), (n - k) / (0.15 * SR))
    return out

def s_chime2(dur=0.7):
    n = int(dur * SR)
    return [(math.sin(2 * math.pi * 1318.5 * k / SR) + 0.6 * math.sin(2 * math.pi * 1760 * k / SR)) * math.exp(-k / (0.18 * SR)) for k in range(n)]

# ---------------------------------------------------------------- blocos reutilizáveis
def ratchet(t0, dur, n, g=0.3, f0=1100, f1=2300, ease_pow=3, tag='contagem'):
    """Roleta de cliques de contagem: rápida no começo e lenta no fim, como o número (ease power-N.out). Tom sobe com o valor."""
    for k in range(1, n + 1):
        x = k / n; t = t0 + dur * (1 - (1 - x) ** (1 / ease_pow))
        place(s_tick(f0 + (f1 - f0) * x, 0.04, 0.35), t, g=g, tag=tag)

def plips(t0, n, step, g=0.2, f0=0.8, f1=1.3, base=700, tag='empilha'):
    for i in range(n):
        r = f0 + (f1 - f0) * i / max(1, n - 1)
        place(s_plip(base * r), t0 + i * step, g=g, tag=tag)

def pan_for(cam):
    if 'panR' in cam: return (-0.7, 0.7)
    if 'panL' in cam: return (0.7, -0.7)
    if 'orbit' in cam: return (-0.4, 0.4)
    if 'tilt' in cam: return (0.0, 0.0)
    return None

# ---------------------------------------------------------------- plano
by_id = {s['id']: s for s in shots}
GAIN = {'whoosh': 0.55, 'pop': 0.4}

# transição entre beats
for b in beats[1:]:
    place(pitch(load('whoosh'), 0.95), b['G'] - 0.08, g=0.5, pan=-0.3, pan_to=0.3, tag='transicao')

# cronômetro do quiz: do pergunta aparecer até o fim da contagem 3-2-1 (tique, taque; acelera na contagem)
quiz_in = next((s for s in shots if s['k'] == 'quiz' and s['o'].get('mode') in ('in', 'inTimer')), None)
guess = next((s for s in shots if s['k'] == 'guess'), None)
if quiz_in and guess:
    t0, t_cd, t1 = quiz_in['start'] + 0.45, guess['start'], guess['start'] + guess['dur']
    t, i = t0, 0
    while t < t1 - 0.12:
        count_down = t >= t_cd
        place(s_tick(2300 if i % 2 == 0 else 1650, 0.06, 0.5), t, g=1.0 if count_down else 0.75, pan=-0.15 if i % 2 == 0 else 0.15, tag='cronometro')
        t += 0.25 if count_down else 0.5; i += 1
    place(s_beep(880, 0.24), t1 - 0.3, g=0.7, tag='cronometro-fim')

for s in shots:
    k, t0, D, cam, o, an = s['k'], s['start'], s['dur'], s['cam'], s['o'], s['anims']
    # câmera
    pp = pan_for(cam)
    if pp and ('panL' in cam or 'panR' in cam):
        place(pitch(load('whoosh-short'), 0.9), t0 - 0.03, g=0.5, pan=pp[0], pan_to=pp[1], tag='passagem')
    elif pp and ('orbit' in cam or 'tilt' in cam):
        place(pitch(load('whoosh-short'), 0.78), t0, g=0.28, pan=pp[0], pan_to=pp[1], tag='camera')
    if 'punch' in cam and k not in ('stamp', 'flash'):
        place(s_thud(), t0, g=0.55, peak_at=t0 + 0.03 + FRAME, tag='soco')
    if 'pushInBig' in cam:
        place(trim(pitch(load('whoosh-cinematic'), 1.2), min(D, 1.3), 0.25), t0, g=0.3, tag='aproximacao')

    # por tipo
    if k == 'sun':
        if s['id'] == 'b0s1': place(trim(load('impact-bass-1'), 0.9, 0.3), t0, g=0.55, peak_at=t0 + FRAME, tag='abertura')
    elif k == 'earthSun':
        place(load('pop'), t0 + 0.25, g=0.3, tag='pop')
    elif k == 'box':
        place(s_zip(0.7), t0, g=0.32, tag='traco'); place(load('click'), t0 + 0.72, g=0.3, tag='click')
    elif k == 'flash':
        place(s_thud(0.3), t0, g=0.65, peak_at=t0 + 0.05 + FRAME, tag='soco')
        place(trim(load('error'), 0.7, 0.2), t0 + 0.05, g=0.22, tag='alerta')
    elif k == 'stamp':
        place(s_thud(0.35), t0, g=0.75, peak_at=t0 + 0.2 + FRAME, tag='carimbo')
        place(trim(load('error'), 0.9, 0.25), t0 + 0.2, g=0.3, tag='alerta')
    elif k == 'ruler':
        place(s_zip(0.6), t0, g=0.3, tag='traco'); place(load('click'), t0 + 0.55, g=0.32, tag='click')
    elif k == 'bigNum':
        n = o['num']
        if n['dur'] > 0.05 and n['to'] != n['from']:
            cnt = int(max(10, min(34, n['dur'] * 24)))
            ratchet(t0, n['dur'], cnt, g=0.28)
            place(load('ping'), t0 + n['dur'], g=0.5, peak_at=t0 + n['dur'] + FRAME, tag='valor')
        else:
            place(load('pop'), t0 + 0.04, g=0.35, tag='pop')
        if o.get('label'): place(load('click-soft'), t0 + 0.18, g=0.22, tag='click')
    elif k == 'earthsRow':
        ratchet(t0 + 0.1, 0.66, 26, g=0.2, f0=1400, f1=2800, ease_pow=1, tag='contagem')
    elif k == 'macro':
        place(trim(load('whoosh-cinematic'), D, 0.3), t0, g=0.45, tag='zoom')
        place(load('pop'), t0 + D - 0.08, g=0.35, tag='pop')
    elif k == 'pin':
        place(pitch(load('whoosh-short'), 1.1), t0, g=0.3, tag='passagem'); place(load('click'), t0 + 0.38, g=0.3, tag='click')
    elif k == 'lineSquare':
        place(s_rise(min(1.1, D), 200, 900), t0 + 0.15, g=0.3, tag='crescer'); place(load('pop'), t0 + 0.15 + min(1.1, D), g=0.3, tag='pop')
    elif k == 'straightLine':
        place(s_zip(min(1.0, D), 300, 2200), t0 + 0.1, g=0.3, tag='traco')
    elif k == 'cube':
        if o.get('rot', [0])[0] == -20 or o.get('tone') == 'blue': place(load('pop'), t0 + 0.05, g=0.35, tag='pop')
    elif k == 'meltEarth':
        place(s_plip(420, 0.06), t0 + 0.28, g=0.35, tag='liquido'); place(s_fall(0.55, 900, 240), t0 + 0.72, g=0.28, tag='liquido')
        place(s_splash(), t0 + D - 0.3, g=0.5, tag='liquido')
    elif k == 'sunFill':
        place(s_water(D), t0, g=0.32, tag='liquido')
    elif k == 'earthSolo':
        place(load('pop'), t0 + 0.05, g=0.35, tag='pop')
    elif k == 'spherePile':
        plips(t0, 18 if o.get('rows', 3) <= 3 else 27, 0.03, g=0.2)
    elif k == 'gaps':
        plips(t0 + 0.1, 9, 0.03, g=0.2, f0=0.7, f1=0.9, base=600, tag='vaos')
    elif k == 'barFill':
        m = o.get('mode')
        if m == 'grow': place(s_rise(min(1.3, D), 180, 800), t0, g=0.3, tag='crescer')
        elif m == 'growPct': place(s_rise(min(1.5, D), 180, 800), t0, g=0.3, tag='crescer'); ratchet(t0, min(1.5, D), 26, g=0.26); place(load('ping'), t0 + min(1.5, D), g=0.5, peak_at=t0 + min(1.5, D) + FRAME, tag='valor')
        elif m == 'pct': ratchet(t0, 0.7, 20, g=0.28); place(load('ping'), t0 + 0.7, g=0.5, peak_at=t0 + 0.7 + FRAME, tag='valor')
        else: place(s_thud(0.3), t0, g=0.5, peak_at=t0 + 0.1 + FRAME, tag='soco'); place(pitch(load('whoosh-short'), 1.1), t0 + 0.05, g=0.3, tag='passagem')
    elif k == 'compare':
        place(pitch(load('whoosh-short'), 1.0), t0 + 0.05, g=0.25, tag='passagem')
    elif k == 'quiz':
        m = o.get('mode', 'in')
        if m in ('in', 'inTimer'):
            place(load('whoosh-short'), t0, g=0.35, tag='passagem')
            for i in range(4): place(pitch(load('pop'), 1 + 0.12 * i), t0 + 0.12 + 0.09 * i, g=0.38, tag='quiz-opcao')
        elif m == 'answer':
            place(load('ping'), t0, g=0.65, peak_at=t0 + 0.1 + FRAME, tag='acerto')
            place(s_chime2(), t0 + 0.12, g=0.35, tag='acerto'); place(load('sparkle'), t0 + 0.2, g=0.3, tag='acerto')
    elif k == 'guess':
        n = 3; seg = D / n
        for i in range(n):
            place(load('click'), t0 + i * seg, g=0.9, tag='contagem-regressiva')
            place(load('ping'), t0 + i * seg, g=0.45, pan=0.0, tag='contagem-regressiva')
    elif k == 'bigq':
        place(pitch(load('pop'), 0.8), t0 + 0.12, g=0.55, tag='pop'); place(s_rise(0.25, 300, 700), t0, g=0.2, tag='crescer')
    elif k == 'squares':
        plips(t0 + 0.05, 16, 0.03, g=0.2, f0=0.9, f1=1.4, base=650); place(load('pop'), t0 + 0.55, g=0.3, tag='pop')
    elif k == 'endcard':
        place(load('pop'), t0 + 0.2, g=0.45, tag='pop')
        if o.get('sub'): place(pitch(load('pop'), 1.1), t0 + o.get('subAt', 0.1) + 0.1, g=0.35, tag='pop')
        if o.get('handle'): place(load('sparkle'), t0 + o.get('handleAt', 0.3), g=0.35, tag='sparkle')

    # textos que entram "estourando" (anim pop) ganham um pop; os que deslizam ganham um passe curto
    for i, a in enumerate(an):
        tt = t0 + 0.05 + i * 0.08
        if a == 'pop': place(pitch(load('pop'), 1.05), tt + 0.08, g=0.26, tag='texto')
        elif a == 'slide': place(pitch(load('whoosh-short'), 1.25), tt, g=0.16, pan=-0.5, pan_to=0.0, tag='texto')

# ---------------------------------------------------------------- mix
peak = max(max(abs(v) for v in BUF[0]), max(abs(v) for v in BUF[1])) or 1
scale = 0.72 / peak
os.makedirs(os.path.join(ROOT, 'assets/sfx'), exist_ok=True)
with wave.open(os.path.join(ROOT, 'assets/sfx/sfx-mix.wav'), 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    out = bytearray()
    for i in range(N):
        out += struct.pack('<hh', int(max(-1, min(1, BUF[0][i] * scale)) * 32767), int(max(-1, min(1, BUF[1][i] * scale)) * 32767))
    w.writeframes(bytes(out))
print('sfx ok ·', sum(COUNT.values()), 'efeitos ·', ', '.join(f'{k}:{v}' for k, v in sorted(COUNT.items())))
