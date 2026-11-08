#!/usr/bin/env python3
"""Transcreve com o Whisper local: palavras com tempo (JSON), SRT, texto e conferência com o roteiro."""
import argparse, difflib, json, re, sys
from pathlib import Path


def srt_tempo(s):
    ms = int(round(s * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


EQUIVALENTES = {"pra": "para", "pro": "para o", "tá": "está", "tô": "estou", "cê": "você", "né": "não é"}


def normalizar(t):
    """Minúsculas, sem pontuação, números por extenso e formas faladas iguais às escritas,
    para a conferência não reprovar '25' x 'vinte e cinco' ou 'pra' x 'para'."""
    try:
        from num2words import num2words
    except ImportError:
        num2words = None
    t = t.lower()
    if num2words:
        t = re.sub(r"\d+", lambda m: " " + num2words(int(m.group()), lang="pt_BR") + " ", t)
    palavras = []
    for w in re.sub(r"[^\w\s]", " ", t).split():
        palavras.extend(EQUIVALENTES.get(w, w).split())
    return palavras


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--saida", default=".")
    ap.add_argument("--roteiro")
    ap.add_argument("--modelo", default="turbo")
    ap.add_argument("--idioma", default="pt")
    a = ap.parse_args()

    import whisper
    modelo = whisper.load_model(a.modelo)
    r = modelo.transcribe(a.audio, language=a.idioma, word_timestamps=True, fp16=False)

    saida = Path(a.saida); saida.mkdir(parents=True, exist_ok=True)
    nome = Path(a.audio).stem
    palavras = [{"palavra": w["word"].strip(), "inicio": round(w["start"], 3), "fim": round(w["end"], 3)}
                for seg in r["segments"] for w in seg.get("words", [])]
    (saida / f"{nome}.palavras.json").write_text(json.dumps(palavras, ensure_ascii=False, indent=1))
    srt = [f"{i}\n{srt_tempo(s['start'])} --> {srt_tempo(s['end'])}\n{s['text'].strip()}\n"
           for i, s in enumerate(r["segments"], 1)]
    (saida / f"{nome}.srt").write_text("\n".join(srt))
    (saida / f"{nome}.txt").write_text(r["text"].strip() + "\n")
    print(f"{len(palavras)} palavras -> {saida}/{nome}.palavras.json, .srt, .txt")

    if a.roteiro:
        esperado = normalizar(Path(a.roteiro).read_text())
        falado = normalizar(r["text"])
        sm = difflib.SequenceMatcher(None, esperado, falado)
        linhas = [f"semelhança: {sm.ratio():.1%}"]
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op != "equal":
                linhas.append(f"{op}: roteiro='{' '.join(esperado[i1:i2])}' voz='{' '.join(falado[j1:j2])}'")
        (saida / f"{nome}.conferencia.txt").write_text("\n".join(linhas) + "\n")
        print("\n".join(linhas[:15]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
