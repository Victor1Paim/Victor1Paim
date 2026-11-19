#!/usr/bin/env python3
"""Corta uma fala única (várias frases com pausas) em N pedaços usando o tempo das PALAVRAS do Whisper.

Por que: o corte só por silêncio (cortar_respostas) às vezes deixa o fim da frase anterior no começo do pedaço
(soa como travada) ou come a consoante fraca do fim ("Stop", "Wait"). Aqui:
  1. o Whisper marca onde cada frase começa e termina (frases conhecidas, em ordem);
  2. a fronteira entre duas frases vai no ponto de MENOR energia entre o fim de uma e o começo da outra;
  3. cada pedaço é aparado com limiar baixo (-50 dB) + margem (não come consoante), com fade curto;
  4. pausas internas longas (> 0,35 s) viram 0,22 s;
  5. confere cada pedaço no Whisper e procura estalos (salto brusco de amostra).

Uso: python3 scripts/recortar_whisper.py <fala.wav> <lingua> <prefixo_saida> "frase 1" "frase 2" ...
"""
import re, sys, unicodedata, wave
from pathlib import Path

import numpy as np


def ler(arq):
    with wave.open(str(arq)) as w:
        sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        if w.getnchannels() > 1:
            x = x.reshape(-1, w.getnchannels()).mean(1)
    return x, sr


def gravar(arq, x, sr):
    with wave.open(str(arq), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9 ]", " ", "".join(c for c in s if unicodedata.category(c) != "Mn")).split()


def rms(x, sr, passo=0.01):
    k = int(sr * passo); n = len(x) // k
    return np.sqrt((x[:n * k].reshape(n, k) ** 2).mean(1) + 1e-12), k


def recortar(arq, lingua, frases, modelo=None):
    import whisper
    modelo = modelo or whisper.load_model("turbo")
    x, sr = ler(arq)
    r = modelo.transcribe(str(arq), language=lingua, word_timestamps=True)
    ws = [(w["word"], w["start"], w["end"]) for s in r["segments"] for w in s.get("words", [])]
    # alinha as palavras do Whisper às frases conhecidas (em ordem, pela contagem de palavras normalizadas)
    toks = []
    for w, a, b in ws:
        for t in norm(w):
            toks.append((t, a, b))
    alvo = [norm(f) for f in frases]
    if sum(map(len, alvo)) != len(toks):
        # contagem não bate: procura o começo de cada frase pela 1ª palavra dela, em ordem
        print(f"  aviso: whisper {len(toks)} palavras x roteiro {sum(map(len, alvo))}; alinhando pela 1ª palavra")
    limites, i = [], 0
    for k, fr in enumerate(alvo):
        n = len(fr)
        if sum(map(len, alvo)) != len(toks):
            # pula até achar a 1ª palavra da frase (para "Como se diz" repetido usa a palavra seguinte também)
            while i < len(toks) and not (toks[i][0] == fr[0] and (n < 2 or i + 1 >= len(toks) or toks[i + 1][0] == fr[1])):
                i += 1
            j = i
            while j < len(toks) and (k + 1 >= len(alvo) or not (toks[j][0] == alvo[k + 1][0] and j > i)):
                j += 1
            seg = toks[i:j] if j > i else toks[i:i + n]
            i = j
        else:
            seg = toks[i:i + n]; i += n
        limites.append((seg[0][1], seg[-1][2]))
    env, k = rms(x, sr)
    def vale(a, b):
        a, b = int(a / 0.01), int(b / 0.01)
        if b <= a:
            a, b = max(0, a - 10), b + 10
        return (a + int(np.argmin(env[a:b + 1]))) * 0.01
    cortes = [0.0] + [vale(limites[m][1], limites[m + 1][0]) for m in range(len(limites) - 1)] + [len(x) / sr]
    pecas = []
    lim = 10 ** (-50 / 20)
    for m in range(len(frases)):
        a, b = int(cortes[m] * sr), int(cortes[m + 1] * sr)
        y = x[a:b].copy()
        e, kk = rms(y, sr)
        on = np.where(e > lim)[0]
        if len(on):
            y = y[max(0, on[0] * kk - int(0.04 * sr)): min(len(y), (on[-1] + 1) * kk + int(0.09 * sr))]
        # pausas internas longas → 0,22 s
        e, kk = rms(y, sr); quieto = e < 10 ** (-42 / 20)
        partes, ini, j = [], 0, 0
        while j < len(quieto):
            if quieto[j]:
                f = j
                while f < len(quieto) and quieto[f]:
                    f += 1
                if (f - j) * 0.01 > 0.35 and j > 0 and f < len(quieto):
                    meio = (j + f) // 2
                    partes.append(y[ini:(j + 11) * kk]); ini = (f - 11) * kk
                j = f
            else:
                j += 1
        partes.append(y[ini:])
        if len(partes) > 1:   # junta com crossfade de 10 ms
            z = partes[0]; c = int(0.01 * sr)
            for p in partes[1:]:
                rampa = np.linspace(0, 1, c)
                z = np.concatenate([z[:-c], z[-c:] * (1 - rampa) + p[:c] * rampa, p[c:]])
            y = z
        fi, fo = int(0.006 * sr), int(0.03 * sr)
        y[:fi] *= np.linspace(0, 1, fi); y[-fo:] *= np.linspace(1, 0, fo)
        y = np.concatenate([y, np.zeros(int(0.08 * sr), np.float32)])
        pecas.append(y)
    return pecas, sr, modelo


def estalos(y, sr):
    d = np.abs(np.diff(y))
    return int((d > 0.35).sum())


def main():
    arq, lingua, pref = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
    frases = sys.argv[4:]
    pecas, sr, modelo = recortar(arq, lingua, frases)
    for m, y in enumerate(pecas, 1):
        out = Path(f"{pref}{m}.wav"); gravar(out, y, sr)
        t = modelo.transcribe(str(out), language=lingua)["text"].strip()
        print(f"{out.name} {len(y) / sr:.2f}s estalos={estalos(y, sr)} | {t}", flush=True)


if __name__ == "__main__":
    main()
