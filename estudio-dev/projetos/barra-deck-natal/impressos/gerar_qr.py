"""Gera o QR code do site e o cartão de impressão (A6 e A5, 300 dpi) do Barra Deck.

Uso: python3 impressos/gerar_qr.py   (precisa de: pip install segno pillow)
"""
import os

import segno
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(AQUI)
URL = 'https://barradeck.vercel.app'
FONTES = os.path.join(SITE, '..', 'barra-deck-reel', 'public', 'fontes')

CREME = (252, 243, 236)
MARROM = (76, 34, 14)
ESPRESSO = (42, 20, 9)
COBRE = (160, 78, 31)
COBRE_CLARO = (192, 101, 47)

qr = segno.make(URL, error='h')
qr.save(os.path.join(AQUI, 'qrcode-barradeck.svg'), scale=10, border=2, dark='#2A1409', light='#FFFFFF')
qr.save(os.path.join(AQUI, 'qrcode-barradeck.png'), scale=40, border=2, dark='#2A1409', light='#FFFFFF')


def fonte(nome, tam):
    return ImageFont.truetype(os.path.join(FONTES, nome), tam)


def centro(d, y, texto, f, cor, w):
    x = (w - d.textlength(texto, font=f)) / 2
    d.text((x, y), texto, font=f, fill=cor)


def cartao(w_mm, h_mm, nome):
    dpi = 300
    W, H = round(w_mm / 25.4 * dpi), round(h_mm / 25.4 * dpi)
    k = W / 1240  # escala relativa ao A6 (1240 px de largura)
    img = Image.new('RGB', (W, H), CREME)
    d = ImageDraw.Draw(img)
    serif = lambda t: fonte('CormorantGaramond-normal-600-latin.woff2', round(t * k))
    serif_i = lambda t: fonte('CormorantGaramond-italic-500-latin.woff2', round(t * k))
    sans = lambda t: fonte('Karla-normal-700-latin.woff2', round(t * k))
    sans_n = lambda t: fonte('Karla-normal-500-latin.woff2', round(t * k))

    m = round(40 * k)
    d.rounded_rectangle([m, m, W - m, H - m], radius=round(26 * k), outline=COBRE_CLARO, width=max(2, round(3 * k)))

    logo = Image.open(os.path.join(SITE, 'assets', 'img', 'logo.webp')).convert('RGBA')
    lw = round(380 * k)
    logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    y = round(110 * k)
    img.paste(logo, ((W - lw) // 2, y), logo)
    y += logo.height + round(40 * k)

    centro(d, y, 'CEIA DE NATAL 2026', sans(34), COBRE, W); y += round(70 * k)
    centro(d, y, 'O fogão é nosso.', serif(92), MARROM, W); y += round(100 * k)
    centro(d, y, 'A noite é sua.', serif_i(92), COBRE, W); y += round(140 * k)

    q = Image.open(os.path.join(AQUI, 'qrcode-barradeck.png')).convert('RGB')
    qs = round(560 * k)
    q = q.resize((qs, qs), Image.NEAREST)
    pad = round(24 * k)
    d.rounded_rectangle([(W - qs) // 2 - pad, y - pad, (W + qs) // 2 + pad, y + qs + pad], radius=round(22 * k), fill=(255, 255, 255), outline=(230, 210, 195), width=2)
    img.paste(q, ((W - qs) // 2, y))
    y += qs + pad + round(50 * k)

    centro(d, y, 'Aponte a câmera e monte sua ceia', sans(40), ESPRESSO, W); y += round(62 * k)
    centro(d, y, 'barradeck.vercel.app', sans_n(36), COBRE, W); y += round(90 * k)
    centro(d, y, 'Encomendas até 10/12  ·  Retirada 24/12, das 10h às 15h', sans_n(30), MARROM, W); y += round(50 * k)
    centro(d, y, 'WhatsApp (21) 98171-6022', sans(30), MARROM, W)

    png = os.path.join(AQUI, f'{nome}.png')
    img.save(png, dpi=(dpi, dpi))
    img.save(os.path.join(AQUI, f'{nome}.pdf'), resolution=dpi)
    return W, H


if __name__ == '__main__':
    print('A6', cartao(105, 148, 'cartao-qr-A6'))
    print('A5', cartao(148, 210, 'cartao-qr-A5'))
