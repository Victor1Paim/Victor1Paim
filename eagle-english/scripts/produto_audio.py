#!/usr/bin/env python3
"""Áudio das frases de viagem (bônus do plano avançado): 1 MP3 por mapa do Eagle 350.
Cada frase: inglês → pausa para repetir → inglês de novo. Voz Achird (gemini-3.8-flash-lite-tts), 1 pedido por mapa
(6 frases) cortado pelo Whisper (recortar_whisper) e conferido frase a frase.

Uso: GEMINI_KEY_FILE=... python3 scripts/produto_audio.py produtos [--situacoes "Aeroporto" ...]
Saída: produtos/avancado/audio/<NN-situacao>/<mapa>-<titulo>.mp3  · custos em produtos/custos.jsonl
"""
import argparse, difflib, json, re, subprocess, sys, tempfile, unicodedata
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vozes  # noqa: E402
from recortar_whisper import recortar, gravar, norm  # noqa: E402

VIAGEM = ["Aeroporto", "Hotel", "Restaurante", "Transporte", "Compras", "Saúde", "Banco e dinheiro",
          "Cidade e passeios", "Emergências e problemas"]
SR = 48000


def slug(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


UN = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
DZ = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def num(n):
    n = int(n)
    if n < 20: return UN[n]
    if n < 100: return DZ[n // 10] + ("" if n % 10 == 0 else " " + UN[n % 10])
    if n < 1000: return UN[n // 100] + " hundred" + ("" if n % 100 == 0 else " " + num(n % 100))
    return str(n)


def nota(a, b):
    """semelhança 0–1 entre o texto e o que o Whisper ouviu, com números por extenso (12 → twelve)."""
    def f(t):
        t = t.lower().replace("’", "'").replace(",", "").replace("%", " percent").replace("-", "").replace("911", "nine one one").replace("catchup", "ketchup").replace("catch up", "ketchup")
        for a, b in [("n't", " not"), ("'m", " am"), ("'re", " are"), ("'ll", " will"), ("'ve", " have"), ("'d", " would"),
                     ("'s", " is"), ("can not", "cannot"), ("check in", "check-in")]:
            t = t.replace(a, b)
        return norm(re.sub(r"\d+", lambda m: " " + num(m.group()) + " ", t))
    return difflib.SequenceMatcher(None, f(a), f(b)).ratio()


def silencio(seg):
    return np.zeros(int(seg * SR), np.float32)


def para48(y, sr):
    if sr == SR:
        return y
    n = int(len(y) * SR / sr)
    return np.interp(np.linspace(0, len(y) - 1, n), np.arange(len(y)), y).astype(np.float32)


def main():
    vozes.carregar_env()
    ap = argparse.ArgumentParser(); ap.add_argument("pasta"); ap.add_argument("--situacoes", nargs="*")
    a = ap.parse_args()
    base = Path(a.pasta).resolve()
    mapas = json.load(open(base / "fonte" / "eagle350.json"))
    sits = a.situacoes or VIAGEM
    import whisper
    modelo_w = whisper.load_model("turbo")
    conf_w = whisper.load_model("base.en")   # conferência rápida de cada frase
    tmp = Path(tempfile.mkdtemp())
    falhas = []
    for si, sit in enumerate(VIAGEM, 1):
        if sit not in sits:
            continue
        pasta = base / "avancado" / "audio" / f"{si:02d}-{slug(sit)}"; pasta.mkdir(parents=True, exist_ok=True)
        for m in [x for x in mapas if x["situacao"] == sit]:
            mp3 = pasta / f"mapa-{m['mapa']:03d}-{slug(m['titulo'])}.mp3"
            if mp3.exists():
                continue
            frases = [f["en"] for f in m["frases"]]
            ok = False
            for tent in range(3):
                bruto = tmp / "bruto.wav"
                vozes.tts("\n\n".join(frases), "Achird", "gemini-3.8-flash-lite-tts", bruto, base, "en")
                try:
                    pecas, sr, _ = recortar(bruto, "en", frases, modelo_w)
                except Exception as e:
                    print(f"  mapa {m['mapa']}: corte falhou ({e}); de novo"); continue
                notas = []
                for k, (y, f) in enumerate(zip(pecas, frases)):
                    pw = tmp / f"p{k}.wav"; gravar(pw, y, sr)
                    ouvido = conf_w.transcribe(str(pw), language="en", fp16=False)["text"]
                    notas.append(nota(f, ouvido))
                print(f"  mapa {m['mapa']}: notas {[round(n, 2) for n in notas]}", flush=True)
                if min(notas) >= 0.7:
                    ok = True; break
                print(f"  mapa {m['mapa']}: tentativa {tent + 1} reprovada {[round(n, 2) for n in notas]}")
            if not ok:   # plano B: uma frase por pedido (números/siglas atrapalham o corte do lote)
                pecas = []
                for k, f in enumerate(frases):
                    for tent in range(3):
                        pw = tmp / f"p{k}.wav"
                        vozes.tts(f, "Achird", "gemini-3.8-flash-lite-tts", pw, base, "en")
                        ouvido = conf_w.transcribe(str(pw), language="en", fp16=False)["text"]
                        if nota(f, ouvido) >= 0.7:
                            break
                        print(f"  mapa {m['mapa']} frase {k + 1}: {round(nota(f, ouvido), 2)} '{ouvido.strip()}'", flush=True)
                    else:
                        break
                    from recortar_whisper import ler
                    y, sr = ler(pw); pecas.append(y)
                else:
                    ok = True
            if not ok:
                falhas.append(m["mapa"]); continue
            partes = [silencio(0.4)]
            for y in pecas:
                y = para48(y, sr)
                partes += [y, silencio(max(1.8, len(y) / SR * 1.3)), y, silencio(1.0)]
            wav = tmp / "mapa.wav"; gravar(wav, np.concatenate(partes), SR)
            subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", str(wav), "-af",
                            "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "44100", "-ac", "1", "-b:a", "96k",
                            "-metadata", f"title={m['titulo'].title()} (mapa {m['mapa']})",
                            "-metadata", "artist=Eagle English BR", "-metadata", f"album=Eagle 350 · {sit}", str(mp3)], check=True)
            print(f"ok {mp3.relative_to(base)}", flush=True)
    print("FALHAS:", falhas if falhas else "nenhuma")


if __name__ == "__main__":
    main()
