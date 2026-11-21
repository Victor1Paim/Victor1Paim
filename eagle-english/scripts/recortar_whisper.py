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
    lim = 10 ** (-55 / 20)
    for m in range(len(frases)):
        a, b = int(cortes[m] * sr), int(cortes[m + 1] * sr)
        # o Whisper sabe onde a 1ª palavra começa e a última termina: respiração/ruído antes/depois fica de fora
        a = max(a, int((limites[m][0] - 0.12) * sr)); b = min(b, int((limites[m][1] + 0.35) * sr))
        y = x[a:b].copy()
        e, kk = rms(y, sr)
        lim_m = max(lim, e.max() * 10 ** (-38 / 20))   # relativo ao pico do pedaço: ruído de fundo não conta como fala
        on = np.where(e > lim_m)[0]
        if len(on):
            y = y[max(0, on[0] * kk - int(0.04 * sr)): min(len(y), (on[-1] + 1) * kk + int(0.16 * sr))]
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
        y, nb = remover_blips(y, sr)
        if nb:
            print(f"  (pedaço {m + 1}: {nb} blip(s) isolado(s) removido(s))")
        fi, fo = int(0.006 * sr), int(0.03 * sr)
        y[:fi] *= np.linspace(0, 1, fi); y[-fo:] *= np.linspace(1, 0, fo)
        y = np.concatenate([y, np.zeros(int(0.08 * sr), np.float32)])
        pecas.append(y)
    return pecas, sr, modelo


def remover_blips(y, sr, max_blip=0.08, silencio=0.12):
    """Tira "blips" isolados no começo/fim do pedaço: um estouro curto (≤ 80 ms) separado da fala por ≥ 120 ms de silêncio
    (clique do gerador de voz que o corte acaba pegando). Devolve (y_limpo, quantos removidos)."""
    k = int(sr * 0.01); n = len(y) // k
    if n < 5:
        return y, 0
    e = np.sqrt((y[:n * k].reshape(n, k) ** 2).mean(1)); som = e > 10 ** (-40 / 20)
    blocos, i = [], 0                       # trechos contíguos com som
    while i < n:
        if som[i]:
            j = i
            while j < n and som[j]:
                j += 1
            blocos.append([i, j]); i = j
        else:
            i += 1
    tirados = 0
    while len(blocos) > 1 and (blocos[0][1] - blocos[0][0]) * 0.01 <= max_blip and (blocos[1][0] - blocos[0][1]) * 0.01 >= silencio:
        y[:blocos[0][1] * k] = 0; blocos.pop(0); tirados += 1
    while len(blocos) > 1 and (blocos[-1][1] - blocos[-1][0]) * 0.01 <= max_blip and (blocos[-1][0] - blocos[-2][1]) * 0.01 >= silencio:
        y[blocos[-1][0] * k:] = 0; blocos.pop(); tirados += 1
    if tirados:   # reapara o silêncio que sobrou no começo (deixa 40 ms antes da fala)
        a = max(0, blocos[0][0] * k - int(0.04 * sr)); y = y[a:]
    return y, tirados


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


def limpar_arquivos(arqs):
    """Aplica remover_blips em arquivos já cortados (uso: python3 scripts/recortar_whisper.py --limpar a.wav b.wav …)."""
    for a in arqs:
        y, sr = ler(a); y2, nb = remover_blips(y.copy(), sr)
        if nb:
            gravar(a, y2, sr); print(f"{a}: {nb} blip(s) removido(s)")


if __name__ == "__main__":
    if sys.argv[1] == "--limpar":
        limpar_arquivos(sys.argv[2:])
    else:
        main()
