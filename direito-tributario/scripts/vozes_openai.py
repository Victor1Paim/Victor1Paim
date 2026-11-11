#!/usr/bin/env python3
"""Narração com o gpt-4o-mini-tts (OpenAI), um arquivo por fala, custo registrado no post.

    python3 scripts/vozes_openai.py testes/teste-01 [--so 03_imposto]

Lê <post>/falas.json e grava <post>/audio/<id>.wav (24 kHz mono). Na nuvem o proxy injeta a chave
(OPENAI_API_KEY pode ser qualquer valor); no notebook, defina OPENAI_API_KEY. Nunca grave a chave no git.
"""
import argparse, json, os, subprocess, sys, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts"))
from custos import registrar  # noqa: E402


def duracao(arq):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(arq)],
                         capture_output=True, text=True).stdout
    return float(out.strip())


def gerar(post, so=None):
    d = json.loads((post / "falas.json").read_text(encoding="utf-8"))
    (post / "audio").mkdir(exist_ok=True)
    for f in d["falas"]:
        if so and f["id"] != so:
            continue
        corpo = json.dumps({"model": d["modelo"], "voice": d["voz"], "input": f["texto"],
                            "instructions": d["instrucoes"], "response_format": "wav"}).encode()
        req = urllib.request.Request("https://api.openai.com/v1/audio/speech", corpo, {
            "Authorization": f"Bearer {os.environ.get('OPENAI_API_KEY', 'proxy-injected')}",
            "Content-Type": "application/json"})
        arq = post / "audio" / f"{f['id']}.wav"
        arq.write_bytes(urllib.request.urlopen(req, timeout=120).read())
        seg = duracao(arq)
        registrar(post, d["modelo"], f"voz {f['id']}", minuto_audio=seg / 60)
        print(f"{f['id']}: {seg:.2f}s")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("post", type=Path)
    ap.add_argument("--so")
    a = ap.parse_args()
    gerar(a.post.resolve(), a.so)
