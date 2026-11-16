"""Baixa as fontes da marca (Google Fonts) para public/fontes e gera src/fontes.json."""
import json
import os
import re
import urllib.request

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(AQUI, 'public', 'fontes')
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'
CSS = ('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600'
       '&family=Karla:wght@500;600;700&display=swap')


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60).read()


os.makedirs(DEST, exist_ok=True)
css = get(CSS).decode()
faces = []
for sub, bloco in re.findall(r'/\* ([\w-]+) \*/\s*@font-face \{(.*?)\}', css, re.S):
    if sub not in ('latin', 'latin-ext'):
        continue
    fam = re.search(r"font-family: '([^']+)'", bloco).group(1)
    estilo = re.search(r'font-style: (\w+)', bloco).group(1)
    peso = re.search(r'font-weight: (\d+)', bloco).group(1)
    url = re.search(r'url\((https://[^)]+)\)', bloco).group(1)
    rng = re.search(r'unicode-range: ([^;]+);', bloco).group(1)
    nome = f"{fam.replace(' ', '')}-{estilo}-{peso}-{sub}.woff2"
    caminho = os.path.join(DEST, nome)
    if not os.path.exists(caminho):
        open(caminho, 'wb').write(get(url))
    faces.append({'family': fam, 'style': estilo, 'weight': peso, 'file': f'fontes/{nome}', 'unicodeRange': rng})
json.dump(faces, open(os.path.join(AQUI, 'src', 'fontes.json'), 'w'), indent=1)
print(len(faces), 'fontes')
