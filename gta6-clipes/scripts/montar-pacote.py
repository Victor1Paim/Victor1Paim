#!/usr/bin/env python3
"""Monta o pacote de postagem: uma pasta por dia com vídeo, carrossel e legendas por rede, e um .zip por dia."""
import json, os, shutil
raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
posts = json.load(open(os.path.join(raiz, 'noticias', 'pacote.json')))
destino = os.path.join(raiz, 'pacote-postagens')
os.makedirs(destino, exist_ok=True)
faltando = []
for p in posts:
    pasta = os.path.join(destino, f"{p['dia']}-{p['nome']}")
    os.makedirs(pasta, exist_ok=True)
    video = os.path.join(raiz, 'modelo', 'out', f"{p['video']}-leve.mp4")
    if os.path.exists(video):
        shutil.copy(video, os.path.join(pasta, f"video-{p['nome']}.mp4"))
    else:
        faltando.append(p['video'])
    if p.get('carrossel'):
        for i in range(1, 6):
            shutil.copy(os.path.join(raiz, 'noticias', 'carrossel', f"{p['carrossel']}-{i}.png"), os.path.join(pasta, f"carrossel-{i}.png"))
    with open(os.path.join(pasta, 'legendas.txt'), 'w') as f:
        f.write(f"POST {p['dia']} — {p['nome']}\n\n")
        f.write("=== TIKTOK / REELS (vídeo) ===\n" + p['tiktok'] + "\n\n")
        f.write("=== YOUTUBE SHORTS ===\nTítulo: " + p['shorts_titulo'] + "\nDescrição:\n" + p['shorts_desc'] + "\n\n")
        f.write("=== INSTAGRAM (" + ("carrossel" if p.get('carrossel') else "legenda do Reels") + ") ===\n" + p['instagram'] + "\n")
    shutil.make_archive(pasta, 'zip', pasta)
print('faltando:', faltando or 'nada')
