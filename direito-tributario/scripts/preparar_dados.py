#!/usr/bin/env python3
"""Prepara o post para o Remotion: tempo por palavra (Whisper local, grátis) + envelope de volume (boca do
apresentador) por quadro. Copia os áudios para video/public/<post>/ e grava dados.json.

    python3 scripts/preparar_dados.py testes/teste-01
"""
import json, re, shutil, subprocess, sys, wave
from pathlib import Path
import numpy as np

FPS = 30
PROJ = Path(__file__).resolve().parents[1]


def norm(t):
    t = re.sub(r"[^\w]", "", t.lower())
    return {"pra": "para", "pro": "para o"}.get(t, t)


def alinhar(roteiro, ws):
    """Tempo de cada palavra do roteiro a partir do Whisper; trechos que não batem são interpolados."""
    import difflib
    a = [norm(w) for w in roteiro]
    b = [norm(w["word"]) for w in ws]
    tempos = [None] * len(roteiro)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
            for k in range(i1, i2):
                tempos[k] = (ws[j1 + k - i1]["start"], ws[j1 + k - i1]["end"])
        elif tag == "replace":
            ini, fim = ws[j1]["start"], ws[j2 - 1]["end"]
            for k in range(i1, i2):
                tempos[k] = (ini + (fim - ini) * (k - i1) / (i2 - i1), ini + (fim - ini) * (k - i1 + 1) / (i2 - i1))
    for k in range(len(tempos)):  # palavras sem par: encosta na anterior
        if tempos[k] is None:
            prev = tempos[k - 1][1] if k else ws[0]["start"]
            tempos[k] = (prev, prev + 0.25)
    return [{"t": w, "ini": round(t[0], 3), "fim": round(t[1], 3)} for w, t in zip(roteiro, tempos)]


def envelope(arq):
    with wave.open(str(arq)) as w:
        sr = w.getframerate(); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float)
    passo = sr // FPS
    n = len(a) // passo
    rms = np.sqrt((a[:n * passo].reshape(n, passo) ** 2).mean(axis=1))
    return [round(float(x), 3) for x in np.clip(rms / (np.percentile(rms, 95) + 1e-9), 0, 1)], len(a) / sr


def main(post):
    post = post.resolve()
    d = json.loads((post / "falas.json").read_text(encoding="utf-8"))
    pub = PROJ / "video/public" / post.name
    pub.mkdir(parents=True, exist_ok=True)
    import whisper
    modelo = whisper.load_model("small")
    saida = []
    for f in d["falas"]:
        arq = post / "audio" / f"{f['id']}.wav"
        vel = d.get("velocidade", 1)
        if vel != 1:  # acelera sem mudar o tom (falas.json: "velocidade": 1.15)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(arq), "-af", f"atempo={vel}", str(pub / arq.name)], check=True)
        else:
            shutil.copy(arq, pub / arq.name)
        arq = pub / arq.name
        env, dur = envelope(arq)
        r = modelo.transcribe(str(arq), language="pt", word_timestamps=True, fp16=False)
        ws = [w for s in r["segments"] for w in s["words"]]
        roteiro = f["texto"].split()
        palavras = alinhar(roteiro, ws)
        saida.append({**f, "audio": f"{post.name}/{arq.name}", "duracao": round(dur, 3), "palavras": palavras, "volume": env})
        print(f"{f['id']}: {dur:.2f}s, {len(palavras)} palavras")
    (PROJ / "video/src" / f"dados-{post.name}.json").write_text(json.dumps({"falas": saida}, ensure_ascii=False))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
