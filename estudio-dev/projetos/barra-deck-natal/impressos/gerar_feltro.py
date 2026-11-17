"""Gera a textura de feltro do site (tile sem emenda, fundo transparente).

Fibras curtas e curvas, claras e escuras, que funcionam sobre o creme e sobre o marrom.
Uso: python3 impressos/gerar_feltro.py  ->  assets/img/feltro.webp
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(os.path.dirname(AQUI), 'assets', 'img', 'feltro.webp')
N = 360          # lado do tile (px)
FIBRAS = 26000
random.seed(24)  # sempre a mesma textura

img = Image.new('RGBA', (N, N), (0, 0, 0, 0))
d = ImageDraw.Draw(img, 'RGBA')


def fibra():
    x, y = random.uniform(0, N), random.uniform(0, N)
    ang = random.uniform(0, math.tau)
    passos = random.randint(2, 5)
    tam = random.uniform(1.2, 2.4)
    pts = [(x, y)]
    for _ in range(passos):
        ang += random.uniform(-0.55, 0.55)
        x += math.cos(ang) * tam
        y += math.sin(ang) * tam
        pts.append((x, y))
    if random.random() < 0.55:
        cor = (70, 34, 14, random.randint(8, 18))       # fibra escura (marrom)
    else:
        cor = (255, 250, 244, random.randint(10, 24))   # fibra clara (creme)
    # desenha também deslocada nas bordas para o tile não ter emenda
    for dx in (-N, 0, N):
        for dy in (-N, 0, N):
            d.line([(px + dx, py + dy) for px, py in pts], fill=cor, width=1, joint='curve')


for _ in range(FIBRAS):
    fibra()

t3 = Image.new('RGBA', (N * 3, N * 3))
for i in range(3):
    for j in range(3):
        t3.paste(img, (i * N, j * N))
img = t3.filter(ImageFilter.GaussianBlur(0.6)).crop((N, N, 2 * N, 2 * N))

# manchas suaves (o "mesclado" do feltro), sem emenda: ruído em baixa resolução repetido em 3x3
import numpy as np
rng = np.random.default_rng(7)
base = rng.random((9, 9))
grande = np.tile(base, (3, 3))
m = Image.fromarray((grande * 255).astype('uint8')).resize((N * 3, N * 3), Image.BICUBIC)
m = m.filter(ImageFilter.GaussianBlur(18)).crop((N, N, 2 * N, 2 * N))  # desfoca antes de cortar: sem emenda
m = np.asarray(m, dtype=np.float32) / 255
mancha = np.zeros((N, N, 4), dtype=np.uint8)
escuro = m < 0.5
mancha[..., :3] = np.where(escuro[..., None], [70, 34, 14], [255, 250, 244])
mancha[..., 3] = (np.abs(m - 0.5) * 2 * 12).astype(np.uint8)
img = Image.alpha_composite(Image.fromarray(mancha, 'RGBA'), img)
img.save(SAIDA, 'WEBP', quality=80, method=6)
print(SAIDA, os.path.getsize(SAIDA), 'bytes')
