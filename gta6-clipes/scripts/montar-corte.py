#!/usr/bin/env python3
"""Monta um corte: recorta o vídeo-fonte em 9:16 (quadrado central + fundo desfocado) e gera o JSON de props do Remotion.

Uso: montar-corte.py <config.json>
config: {"fonte": "...mp4", "transcricoes": [{"arquivo": "p01.json", "offset": 480}, ...],
         "inicio": s, "fim": s, "nome": "...", "gancho": [...], "destaque": "...", "cabecalho": "...",
         "credito": "...", "canal": "...", "destaques": [...], "correcoes": {"errado": "certo"}}
"""
import json, subprocess, sys, os, re

cfg = json.load(open(sys.argv[1]))
base_dir = os.path.dirname(os.path.abspath(sys.argv[1]))
raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
modelo = os.path.join(raiz, 'modelo')

# 1) palavras com tempo, já no tempo do corte
palavras = []
for t in cfg['transcricoes']:
    d = json.load(open(os.path.join(base_dir, t['arquivo'])))
    for w in d['words']:
        ini, fim = w['start'] + t['offset'], w['end'] + t['offset']
        if ini >= cfg['inicio'] - 0.05 and fim <= cfg['fim'] + 0.3:
            palavras.append({'texto': w['word'].strip(), 'inicio': round(ini - cfg['inicio'], 2), 'fim': round(fim - cfg['inicio'], 2)})
# correções: {"frase errada": "frase certa"}; a frase certa ocupa o tempo da errada
for errado, certo in cfg.get('correcoes', {}).items():
    ew, cw = errado.split(' '), certo.split(' ')
    i = 0
    while i <= len(palavras) - len(ew):
        if [p['texto'].strip('.,?!').lower() for p in palavras[i:i + len(ew)]] == [e.lower() for e in ew]:
            ini, fim = palavras[i]['inicio'], palavras[i + len(ew) - 1]['fim']
            passo = (fim - ini) / len(cw)
            novas = [{'texto': c, 'inicio': round(ini + k * passo, 2), 'fim': round(ini + (k + 1) * passo, 2)} for k, c in enumerate(cw)]
            palavras[i:i + len(ew)] = novas
            i += len(cw)
        else:
            i += 1

# 2) vídeo base 9:16
dur = cfg['fim'] - cfg['inicio'] + 2.6  # + tela final
publico = os.path.join(modelo, 'public')
video = f"{cfg['nome']}.mp4"
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(cfg['inicio']), '-t', str(dur), '-i', cfg['fonte'],
    '-filter_complex', '[0:v]split[a][b];[a]scale=-2:1920,crop=1080:1920,boxblur=40:4,eq=brightness=-0.25:saturation=1.2[bg];'
    '[b]crop=1080:1080:420:0[fg];[bg][fg]overlay=0:400,format=yuv420p[v]',
    '-map', '[v]', '-map', '0:a', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-c:a', 'aac', '-b:a', '192k',
    os.path.join(publico, video)], check=True)

# 3) props
props = {'dados': {
    'video': video, 'duracao': round(dur - 0.05, 2), 'gancho': cfg['gancho'], 'destaque': cfg['destaque'],
    'cabecalho': cfg['cabecalho'], 'selo': cfg.get('selo', 'LANÇA 19/11'), 'credito': cfg['credito'], 'canal': cfg['canal'],
    'chamadaFinal': cfg.get('chamadaFinal', 'Segue pra não perder nada de GTA 6'),
    'inicioFinal': round(cfg['fim'] - cfg['inicio'] + 0.2, 2), 'legendas': [], 'destaques': cfg['destaques'], 'palavras': palavras}}
saida = os.path.join(modelo, 'cortes', f"{cfg['nome']}.json")
os.makedirs(os.path.dirname(saida), exist_ok=True)
json.dump(props, open(saida, 'w'), ensure_ascii=False, indent=1)
print(saida, len(palavras), 'palavras', round(dur, 1), 's')
print(' '.join(p['texto'] for p in palavras))
