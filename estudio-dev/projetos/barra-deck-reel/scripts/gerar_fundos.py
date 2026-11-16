"""Gera fundos de motion graphics natalinos (sem produtos, sem texto) com a API de imagens da OpenAI.

Uso: python3 scripts/gerar_fundos.py [nome ...]
Grava em public/fundos/<nome>.png e registra uso em custos.jsonl.
"""
import base64
import json
import os
import sys
import time
import urllib.request

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(AQUI, 'public', 'fundos')
KEY = os.environ.get('OPENAI_API_KEY', 'proxy')

ESTILO = (
    'Vertical 9:16 abstract motion-graphics background for a premium Christmas restaurant ad. '
    'Brand palette only: deep espresso brown #2A1409, rich chocolate #4C220E, burnished copper #C0652F, '
    'soft peach copper highlights #F2B48A and warm cream #FCF3EC. Elegant, modern, editorial, high-end. '
    'Smooth 3D rendered shapes with soft studio lighting, subtle film grain, shallow depth of field. '
    'Absolutely no text, no letters, no numbers, no logos, no food, no people. '
    'Leave a calm, uncluttered area in the center for typography.'
)
FUNDOS = {
    'abertura': 'Flowing glossy copper silk ribbons swirling in elegant curves across a deep espresso background, '
                'tiny golden light particles and soft bokeh, a few minimalist copper Christmas baubles floating in depth.',
    'cardapio': 'Dynamic composition of floating geometric copper rings, thin metallic lines and concentric arcs '
                'on dark chocolate background, like a kinetic motion graphics frame, sparkling star glints, sense of movement.',
    'data': 'Radiant burst of thin copper light rays and glowing star sparkles from the center on deep espresso, '
            'soft volumetric glow, tiny floating particles, celebratory but refined.',
    'retirada': 'Minimalist stylized copper pine branches and abstract star shapes arranged around the edges, '
                'cream and copper gradient light, soft shadows, airy, festive, plenty of empty space in the middle.',
    'chamada': 'Warm cream background with elegant copper ornaments: thin arcs, circles, a few glossy copper baubles '
               'and gentle snow-like sparkles, luxurious minimal Christmas motion graphics frame, bright and inviting.',
}


def gerar(nome):
    corpo = {'model': 'gpt-image-2', 'prompt': f"{FUNDOS[nome]} {ESTILO}", 'size': '1024x1536',
             'quality': 'medium', 'n': 1}
    req = urllib.request.Request('https://api.openai.com/v1/images/generations', data=json.dumps(corpo).encode(),
                                 headers={'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=300) as r:
        d = json.loads(r.read())
    open(os.path.join(DEST, f'{nome}.png'), 'wb').write(base64.b64decode(d['data'][0]['b64_json']))
    with open(os.path.join(AQUI, 'custos.jsonl'), 'a') as f:
        f.write(json.dumps({'quando': time.strftime('%Y-%m-%d %H:%M'), 'api': 'openai', 'modelo': 'gpt-image-2',
                            'item': f'fundo {nome}', 'qualidade': 'medium', 'tamanho': '1024x1536',
                            'uso': d.get('usage')}) + '\n')
    print('ok', nome, d.get('usage'))


if __name__ == '__main__':
    os.makedirs(DEST, exist_ok=True)
    for n in (sys.argv[1:] or list(FUNDOS)):
        gerar(n)
