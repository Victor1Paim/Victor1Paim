#!/usr/bin/env python3
"""Trilha própria (sintetizada, sem licença de terceiros): drone grave contínuo, sting de virada e impacto da vinheta.

Uso: python3 -I motor/trilha.py PASTA_SAIDA --duracao SEGUNDOS [--semente 7]
Saída: drone.wav (estéreo 48 kHz, na duração pedida), sting.wav (~5 s), vinheta.wav (~7 s).
Desenho tirado das referências: drone concentrado em 20–120 Hz, sem melodia; sting curto e grave.
"""
import argparse, os
import numpy as np, soundfile as sf

ap = argparse.ArgumentParser()
ap.add_argument('saida'); ap.add_argument('--duracao', type=float, required=True); ap.add_argument('--semente', type=int, default=7)
a = ap.parse_args()
os.makedirs(a.saida, exist_ok=True)
SR = 48000
rng = np.random.default_rng(a.semente)


def ruido_marrom(n):
    w = rng.standard_normal(n) * 0.02
    b = np.cumsum(w); b -= np.linspace(b[0], b[-1], n)
    return b / (np.abs(b).max() + 1e-9)


def lfo(n, f, fase=0.0):
    t = np.arange(n) / SR
    return 0.5 + 0.5 * np.sin(2 * np.pi * f * t + fase)


def normalizar(x, db):
    return x / (np.abs(x).max() + 1e-9) * 10 ** (db / 20)


def drone(seg):
    n = int(seg * SR); t = np.arange(n) / SR
    canais = []
    for c, det in enumerate((0.0, 0.31)):
        x = np.zeros(n)
        for f, amp in [(41.2, 1.0), (55.0 + det, 0.55), (61.7 - det, 0.35), (82.4 + det, 0.25), (110.0, 0.08)]:
            # leve deriva de afinação, ondas lentas de volume
            vib = 1 + 0.002 * np.sin(2 * np.pi * (0.05 + 0.01 * c) * t)
            x += amp * np.sin(2 * np.pi * f * vib * t + rng.uniform(0, 6)) * (0.6 + 0.4 * lfo(n, 0.031 + 0.007 * c, rng.uniform(0, 6)))
        ar = ruido_marrom(n) * 0.9 * (0.5 + 0.5 * lfo(n, 0.017, c))          # "vento" grave
        x = x + ar
        canais.append(x)
    x = np.stack(canais, 1)
    fade = np.minimum(1, np.minimum(t / 6, (seg - t) / 10))[:, None]
    return normalizar(x * fade, -6)


def impacto(seg, f0=38, queda=2.2):
    n = int(seg * SR); t = np.arange(n) / SR
    corpo = np.sin(2 * np.pi * f0 * t * (1 + 0.6 * np.exp(-t * 6))) * np.exp(-t * queda)
    ruido = rng.standard_normal(n) * np.exp(-t * 9) * 0.35
    ruido = np.convolve(ruido, np.ones(40) / 40, 'same')               # tira o agudo
    return corpo + ruido


def swell_reverso(seg):
    n = int(seg * SR); t = np.arange(n) / SR
    x = ruido_marrom(n) * 0.7 + 0.3 * np.sin(2 * np.pi * 73.4 * t) * np.sin(2 * np.pi * 0.7 * t)
    env = (t / seg) ** 3
    return x * env


def metal(seg):
    """Raspado metálico grave (parciais inarmônicos com decaimento)."""
    n = int(seg * SR); t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) * np.exp(-t * d) * g
            for f, d, g in [(233, 1.1, .5), (377, 1.6, .35), (521, 2.3, .25), (811, 3.1, .12), (1187, 4.0, .06)])
    return x * np.minimum(1, t / 0.02)


def estereo(x, larg=0.15):
    atraso = int(0.011 * SR)
    r = np.concatenate([np.zeros(atraso), x[:-atraso]])
    return np.stack([x, (1 - larg) * x + larg * r], 1)


# sting: swell reverso de 1,6 s → impacto grave + metal, cauda até 5 s
sw = swell_reverso(1.6)
imp = impacto(3.4) + metal(3.4) * 0.25
sting = np.concatenate([sw * 0.6, imp])
sf.write(os.path.join(a.saida, 'sting.wav'), normalizar(estereo(sting), -3), SR)

# vinheta: 1 s de ar + impacto mais longo + metal com cauda
vin = np.concatenate([swell_reverso(2.2) * 0.5, impacto(4.8, f0=34, queda=1.2) + metal(4.8) * 0.35])
sf.write(os.path.join(a.saida, 'vinheta.wav'), normalizar(estereo(vin), -3), SR)

sf.write(os.path.join(a.saida, 'drone.wav'), drone(a.duracao).astype(np.float32), SR)
print('ok:', a.saida)
