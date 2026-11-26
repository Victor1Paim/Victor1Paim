#!/usr/bin/env python3
"""Identidade do canal The Quiet Hours (@thequiethours.0): foto de perfil, banner do YouTube e marca d'água.

Uso: python3 -I canal-terror/marca/gerar_marca.py
Saída em canal-terror/marca/: perfil-800.png, banner-2560x1440.jpg, marca-dagua.png, banner-previa-areas.jpg
Conceito: um relógio às 3h da manhã (traço fino, ponto vermelho no centro) + nome em serifa (Cormorant Garamond).
"""
import math, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SERIF = os.path.join(AQUI, 'fontes/CormorantGaramond-Medium.ttf')
SANS = '/usr/share/fonts/opentype/inter/Inter-Light.otf'
FUNDO, CLARO, VERMELHO = (11, 11, 13), (236, 232, 224), (196, 30, 36)


def grao(im, forca=10, semente=3):
    import random
    random.seed(semente)
    ruido = Image.effect_noise(im.size, forca).convert('L')
    return Image.blend(im.convert('RGB'), Image.merge('RGB', [ruido] * 3), 0.06)


def relogio(d, cx, cy, r, traco):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=CLARO, width=traco)
    for h in range(12):                                   # marcas das horas, discretas
        a = math.radians(h * 30 - 90); r1, r2 = r * (0.80 if h % 3 == 0 else 0.86), r * 0.92
        d.line([(cx + r1 * math.cos(a), cy + r1 * math.sin(a)), (cx + r2 * math.cos(a), cy + r2 * math.sin(a))],
               fill=CLARO, width=max(1, traco // (1 if h % 3 == 0 else 2)))
    d.line([(cx, cy), (cx + r * 0.50, cy)], fill=CLARO, width=int(traco * 1.6))     # ponteiro das horas: 3
    d.line([(cx, cy), (cx, cy - r * 0.72)], fill=CLARO, width=traco)                # ponteiro dos minutos: 12
    p = traco * 1.9
    d.ellipse([cx - p, cy - p, cx + p, cy + p], fill=VERMELHO)


# ---------- foto de perfil (YouTube recorta em círculo) ----------
S = 800
im = Image.new('RGB', (S, S), FUNDO)
g = Image.new('L', (S, S), 0); ImageDraw.Draw(g).ellipse([60, 60, S - 60, S - 60], fill=40)
im = Image.composite(Image.new('RGB', (S, S), (30, 30, 36)), im, g.filter(ImageFilter.GaussianBlur(120)))
relogio(ImageDraw.Draw(im), S // 2, S // 2, 250, 12)
grao(im).save(os.path.join(AQUI, 'perfil-800.png'))

# ---------- banner 2560x1440 (área segura em todos os aparelhos: 1546x423 no centro) ----------
W, H = 2560, 1440
base = Image.open(os.path.join(RAIZ, 'producoes/coletanea-01/imagens/v00.png')).convert('RGB')
r = max(W / base.width, H / base.height); base = base.resize((int(base.width * r + 1), int(base.height * r + 1)), Image.LANCZOS)
x0, y0 = (base.width - W) // 2, (base.height - H) // 2
im = ImageEnhance.Brightness(ImageEnhance.Color(base.crop((x0, y0, x0 + W, y0 + H))).enhance(0.7)).enhance(0.8)
sombra = Image.new('L', (W, H), 0)
ImageDraw.Draw(sombra).rectangle([W // 2 - 900, H // 2 - 260, W // 2 + 900, H // 2 + 260], fill=170)
im = Image.composite(Image.new('RGB', (W, H), FUNDO), im, sombra.filter(ImageFilter.GaussianBlur(140)))
d = ImageDraw.Draw(im)
f1 = ImageFont.truetype(SERIF, 124); f2 = ImageFont.truetype(SANS, 36)
t1 = 'THE QUIET HOURS'
rr, gap = 100, 50
larg = 2 * rr + gap + max(d.textlength(t1, font=f1), d.textlength('Scary stories for the hours you can’t sleep  ·  @thequiethours.0', font=f2))
x = W // 2 - larg / 2                                    # conjunto centralizado dentro da área segura (1546 px)
relogio(d, int(x + rr), H // 2, rr, 6)
d.text((x + 2 * rr + gap, H // 2 - 100), t1, font=f1, fill=CLARO)
d.text((x + 2 * rr + gap + 4, H // 2 + 52), 'Scary stories for the hours you can’t sleep  ·  @thequiethours.0', font=f2, fill=(200, 196, 188))
grao(im).save(os.path.join(AQUI, 'banner-2560x1440.jpg'), quality=92)
prev = Image.open(os.path.join(AQUI, 'banner-2560x1440.jpg')).copy(); pd = ImageDraw.Draw(prev)
pd.rectangle([W // 2 - 773, H // 2 - 211, W // 2 + 773, H // 2 + 211], outline=(255, 0, 0), width=4)   # área segura
prev.resize((1280, 720)).save(os.path.join(AQUI, 'banner-previa-areas.jpg'), quality=85)

# ---------- marca d'água (PNG transparente, para o canto dos vídeos) ----------
f = ImageFont.truetype(SERIF, 64)
tw = int(ImageDraw.Draw(Image.new('L', (1, 1))).textlength('The Quiet Hours', font=f))
mk = Image.new('RGBA', (tw + 90, 90), (0, 0, 0, 0)); md = ImageDraw.Draw(mk)
relogio_rgba = Image.new('RGBA', (90, 90), (0, 0, 0, 0)); relogio(ImageDraw.Draw(relogio_rgba), 40, 45, 28, 3)
mk.paste(relogio_rgba, (0, 0), relogio_rgba)
md.text((86, 4), 'The Quiet Hours', font=f, fill=CLARO + (255,))
mk.save(os.path.join(AQUI, 'marca-dagua.png'))
print('ok')
