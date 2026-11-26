#!/usr/bin/env python3
"""Miniatura 1280x720: imagem base + texto grande (aplicado aqui, letras perfeitas).

Uso: python3 -I motor/miniatura.py BASE.png SAIDA.jpg "LINHA 1" ["LINHA 2" ...] [--destaque 2] [--lado esq|dir]
A linha --destaque (1 = primeira) sai em vermelho; as outras em branco. Texto com contorno e sombra.
"""
import argparse, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument('base'); ap.add_argument('saida'); ap.add_argument('linhas', nargs='+')
ap.add_argument('--destaque', type=int, default=0); ap.add_argument('--lado', default='esq')
a = ap.parse_args()

W, H = 1280, 720
im = Image.open(a.base).convert('RGB')
r = max(W / im.width, H / im.height)
im = im.resize((int(im.width * r + .5), int(im.height * r + .5)), Image.LANCZOS)
x0, y0 = (im.width - W) // 2, (im.height - H) // 2
im = im.crop((x0, y0, x0 + W, y0 + H))
im = ImageEnhance.Contrast(ImageEnhance.Color(im).enhance(0.85)).enhance(1.12)

# escurece o lado do texto
grad = Image.new('L', (W, H))
gd = ImageDraw.Draw(grad)
for x in range(W):
    f = (1 - x / (W * 0.62)) if a.lado == 'esq' else (x - W * 0.38) / (W * 0.62)
    gd.line([(x, 0), (x, H)], fill=int(255 * max(0, min(1, f)) * 0.78))
im = Image.composite(Image.new('RGB', (W, H), (4, 5, 8)), im, grad)

fonte = '/usr/share/fonts/opentype/inter/Inter-Black.otf'
if not os.path.exists(fonte):
    fonte = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
d = ImageDraw.Draw(im)
margem, y = 64, None
tam = []
for ln in a.linhas:
    s = 150
    while s > 40:
        f = ImageFont.truetype(fonte, s)
        if d.textlength(ln, font=f) <= W * 0.56: break
        s -= 4
    tam.append((ln, f, s))
alt = sum(int(s * 1.02) for _, _, s in tam)
y = (H - alt) // 2
sombra = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sombra)
pos = []
for i, (ln, f, s) in enumerate(tam, 1):
    x = margem if a.lado == 'esq' else W - margem - d.textlength(ln, font=f)
    pos.append((x, y, ln, f, i)); sd.text((x + 6, y + 8), ln, font=f, fill=(0, 0, 0, 220)); y += int(s * 1.02)
im.paste(sombra.filter(ImageFilter.GaussianBlur(10)), (0, 0), sombra.filter(ImageFilter.GaussianBlur(10)))
d = ImageDraw.Draw(im)
for x, y, ln, f, i in pos:
    cor = (214, 28, 28) if i == a.destaque else (245, 242, 235)
    d.text((x, y), ln, font=f, fill=cor, stroke_width=4, stroke_fill=(0, 0, 0))
im.save(a.saida, quality=92)
print('ok:', a.saida)
