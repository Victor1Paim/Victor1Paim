#!/usr/bin/env python3
"""Gera o .zip do kit para a Isabela (tudo que ela precisa para rodar local, sem node_modules nem arquivos internos).

    python3 scripts/empacotar.py [saida.zip]
"""
import sys, zipfile
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
FORA = ["video/node_modules", "video/public/videos", "video/public/teste-", "video/out", "testes/", "__pycache__",
        ".remotion", "README.md", "scripts/vozes_openai.py", "scripts/imagem_openai.py", "scripts/preparar_dados.py",
        "scripts/recortes_apresentador.py", "scripts/empacotar.py"]
DEMO_OK = {"videos/demo-cafezinho/gravacao.mp4"}


def fora(rel):
    if rel in DEMO_OK:
        return False
    if rel.startswith("videos/") and (rel.endswith(".mp4") or rel.endswith(".mov")):
        return True  # gravações e vídeos finais ficam de fora (pesados / pessoais)
    return any(rel.startswith(f) or f"/{f}" in f"/{rel}" for f in FORA)


def main():
    saida = Path(sys.argv[1]) if len(sys.argv) > 1 else PROJ.parent / "kit-isabela-direito-tributario.zip"
    n = 0
    with zipfile.ZipFile(saida, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(PROJ.rglob("*")):
            rel = p.relative_to(PROJ).as_posix()
            if p.is_file() and not fora(rel):
                z.write(p, f"direito-tributario/{rel}")
                n += 1
    print(f"ok: {saida} ({n} arquivos, {saida.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
