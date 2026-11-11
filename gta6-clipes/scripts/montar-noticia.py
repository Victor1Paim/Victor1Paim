#!/usr/bin/env python3
"""Monta um vídeo de notícia: narração + imagens do trailer em 9:16 + legenda alinhada ao roteiro + cartões.

Uso: montar-noticia.py <config.json>
config: {"nome","narracao" (mp3),"transcricao" (json whisper com words),"texto" (roteiro como deve aparecer),
         "fonte" (vídeo), "trechos": [[ini,fim],...], "gancho": [..], "destaque", "cabecalho", "credito", "canal",
         "destaques": [..], "cartoes": [{"em": "palavra do roteiro", "grande", "pequeno", "dur"?}]}
"""
import json, os, re, subprocess, sys, difflib

cfg = json.load(open(sys.argv[1]))
d = os.path.dirname(os.path.abspath(sys.argv[1]))
raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
modelo = os.path.join(raiz, 'modelo')
caminho = lambda p: p if os.path.isabs(p) else os.path.join(d, p)
dur_audio = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', caminho(cfg['narracao'])]))

# 1) alinha o roteiro às palavras da transcrição (difflib); palavras sem par recebem tempo interpolado
norm = lambda w: re.sub(r'[^0-9a-zà-ú]', '', w.lower())
W = json.load(open(caminho(cfg['transcricao'])))['words']
roteiro = cfg['texto'].split()
a = [norm(w) for w in roteiro]
b = [norm(w['word']) for w in W]
tempos = [None] * len(roteiro)
for bloco in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
    for k in range(bloco.size):
        tempos[bloco.a + k] = (W[bloco.b + k]['start'], W[bloco.b + k]['end'])
fim_fala = dur_audio - 0.3
ancoras = [(-1, (0.0, 0.0))] + [(i, t) for i, t in enumerate(tempos) if t] + [(len(roteiro), (fim_fala, fim_fala))]
for (i0, t0), (i1, t1) in zip(ancoras, ancoras[1:]):
    vazios = i1 - i0 - 1
    if vazios <= 0:
        continue
    ini, fim = t0[1], t1[0]
    passo = max(fim - ini, 0.2 * vazios) / vazios
    for k in range(vazios):
        tempos[i0 + 1 + k] = (ini + k * passo, ini + (k + 1) * passo)
palavras = [{'texto': w, 'inicio': round(t[0], 2), 'fim': round(t[1], 2)} for w, t in zip(roteiro, tempos)]

# 2) cartões ancorados em palavras do roteiro
cartoes = []
for c in cfg.get('cartoes', []):
    i = next(k for k, w in enumerate(roteiro) if norm(w) == norm(c['em']) and (not cartoes or palavras[k]['inicio'] >= cartoes[-1]['inicio']))
    cartoes.append({'inicio': palavras[i]['inicio'], 'fim': 0, 'grande': c['grande'], 'pequeno': c['pequeno'], 'dur': c.get('dur', 3.5)})
for k, c in enumerate(cartoes):
    prox = cartoes[k + 1]['inicio'] if k + 1 < len(cartoes) else 1e9
    c['fim'] = round(min(c['inicio'] + c.pop('dur'), prox - 0.1), 2)

# 3) fundo: trechos do trailer em 9:16 cheio, escurecido, sem o áudio original + narração
dur = dur_audio + 2.8
publico = os.path.join(modelo, 'public')
video = f"{cfg['nome']}.mp4"
n = len(cfg['trechos'])
cada = dur / n
entradas, filtros = [], []
for i, (ini, _) in enumerate(cfg['trechos']):
    entradas += ['-ss', str(ini), '-t', str(cada + 0.1), '-i', cfg['fonte']]
    filtros.append(f"[{i}:v]crop=1920:816:0:198,crop=459:816:730:0,scale=1080:1920,setsar=1,eq=brightness=-0.12,trim=0:{cada:.3f},setpts=PTS-STARTPTS[v{i}]")
filtros.append(''.join(f'[v{i}]' for i in range(n)) + f'concat=n={n}:v=1:a=0,format=yuv420p[v]')
subprocess.run(['ffmpeg', '-y', '-v', 'error', *entradas, '-i', caminho(cfg['narracao']),
    '-filter_complex', ';'.join(filtros), '-map', '[v]', '-map', f'{n}:a', '-af', 'apad', '-t', f'{dur:.2f}',
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-c:a', 'aac', '-b:a', '192k', os.path.join(publico, video)], check=True)

props = {'dados': {
    'video': video, 'duracao': round(dur - 0.05, 2), 'gancho': cfg['gancho'], 'destaque': cfg['destaque'],
    'cabecalho': cfg['cabecalho'], 'selo': cfg.get('selo', 'LANÇA 19/11'), 'credito': cfg['credito'], 'canal': cfg['canal'],
    'chamadaFinal': cfg.get('chamadaFinal', 'Segue pra não perder nada de GTA 6'), 'inicioFinal': round(dur_audio + 0.1, 2),
    'legendas': [], 'destaques': cfg['destaques'], 'palavras': palavras, 'cartoes': cartoes}}
saida = os.path.join(modelo, 'cortes', f"{cfg['nome']}.json")
json.dump(props, open(saida, 'w'), ensure_ascii=False, indent=1)
print(saida, round(dur, 1), 's', len(palavras), 'palavras', len(cartoes), 'cartões')
print([(c['grande'], c['inicio'], c['fim']) for c in cartoes])
