#!/usr/bin/env python3
"""Prepara o apresentador ilustrado para o Remotion: base + remendos (boca aberta, olhos fechados) com borda suave.

    python3 scripts/recortes_apresentador.py testes/teste-02
Lê <post>/imagens/{apresentador,boca-aberta,olhos-fechados}.png (gpt-image-2, 1024×1536)
e grava video/public/<post>/{apresentador.jpg,boca.png,olhos.png}.
As caixas abaixo valem para o rosto do teste-02 — ajuste (e em ApresentadorImagem.tsx) para outro personagem.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

BOCA = (430, 515, 595, 620)
OLHOS = (380, 415, 650, 515)

post = Path(sys.argv[1]).resolve()
I = post / "imagens"
D = Path(__file__).resolve().parents[1] / "video/public" / post.name
D.mkdir(parents=True, exist_ok=True)
Image.open(I / "apresentador.png").convert("RGB").save(D / "apresentador.jpg", quality=92)
for src, box, nome in [("boca-aberta.png", BOCA, "boca.png"), ("olhos-fechados.png", OLHOS, "olhos.png")]:
    im = Image.open(I / src).convert("RGB").crop(box)
    w, h = im.size
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).ellipse((14, 14, w - 14, h - 14), fill=255)
    im.putalpha(m.filter(ImageFilter.GaussianBlur(9)))
    im.save(D / nome)
print("ok", D)
