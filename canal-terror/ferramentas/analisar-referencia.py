#!/usr/bin/env python3
"""Analisa um vídeo de referência de narração (ritmo, pausas, histórias, planos, som).

Uso:  python3 -I analisar-referencia.py VIDEO.mp4 [--saida PASTA]

Gera em PASTA (padrão: ao lado do vídeo):
  NOME.transcricao.json   Whisper da OpenAI (whisper-1, tempo por palavra). Cache: não refaz se existir.
  NOME.folha.jpg          1 quadro a cada 30 s (mosaico 6 colunas)
  NOME.relatorio.txt      métricas abaixo

Precisa: ffmpeg, numpy, soundfile; acesso a api.openai.com (nesta sessão o proxy injeta a chave;
fora dela, OPENAI_API_KEY). Áudio vai a 24 kbps mono para caber no limite de 25 MB do Whisper (~2 h).
Atenção: o Whisper "alucina" em silêncio ("you you you"); trechos de 1 palavra no fim são ruído.
"""
import argparse, json, os, subprocess, sys
import numpy as np, soundfile as sf

ap = argparse.ArgumentParser()
ap.add_argument('video'); ap.add_argument('--saida')
a = ap.parse_args()
base = os.path.splitext(os.path.basename(a.video))[0]
out = a.saida or os.path.dirname(os.path.abspath(a.video)); os.makedirs(out, exist_ok=True)
P = lambda ext: os.path.join(out, f'{base}.{ext}')
run = lambda *c: subprocess.run(c, check=True, capture_output=True)
linhas = []
def log(s=''): print(s); linhas.append(s)

# 1. áudio
if not os.path.exists(P('mp3')):
    run('ffmpeg', '-v', 'error', '-y', '-i', a.video, '-vn', '-ac', '1', '-ar', '16000', '-b:a', '24k', P('mp3'))
if not os.path.exists(P('wav')):
    run('ffmpeg', '-v', 'error', '-y', '-i', a.video, '-vn', '-ac', '1', '-ar', '22050', P('wav'))

# 2. transcrição
if not os.path.exists(P('transcricao.json')):
    key = os.environ.get('OPENAI_API_KEY', 'sk-proxy')
    r = subprocess.run(['curl', '-sS', 'https://api.openai.com/v1/audio/transcriptions',
                        '-H', f'Authorization: Bearer {key}', '-F', 'model=whisper-1', '-F', f'file=@{P("mp3")}',
                        '-F', 'response_format=verbose_json', '-F', 'timestamp_granularities[]=word',
                        '-F', 'timestamp_granularities[]=segment', '-o', P('transcricao.json')], check=True)
tr = json.load(open(P('transcricao.json')))
if 'error' in tr: sys.exit(f'Whisper: {tr["error"]}')
w = tr['words']; dur = tr['duration']

# 3. ritmo e pausas
g = [w[i]['start'] - w[i-1]['end'] for i in range(1, len(w))]
fala = sum(min(x, 0.6) for x in g) + sum(x['end'] - x['start'] for x in w)
log(f'# {base}  ({dur/60:.1f} min)')
log(f'Primeira palavra: {w[0]["start"]:.1f} s · palavras: {len(w)} · ritmo falando: {len(w)/(fala/60):.0f} palavras/min')
for lo, hi in [(0.3, 0.7), (0.7, 1.2), (1.2, 2), (2, 6), (6, 999)]:
    log(f'  pausas {lo}–{hi} s: {sum(lo <= x < hi for x in g)}')

# 4. histórias (separadas por pausa > 6 s)
br = [0] + [i for i in range(1, len(w)) if w[i]['start'] - w[i-1]['end'] > 6]
log('\nHistórias:')
for k, i in enumerate(br):
    j = br[k+1] if k + 1 < len(br) else len(w)
    if j - i < 30: continue  # ruído do Whisper
    log(f'  {k+1}. {w[i]["start"]/60:.1f}–{w[j-1]["end"]/60:.1f} min ({j-i} palavras)')
    log('     abre:  ' + ' '.join(x['word'] for x in w[i:i+16]))
    log('     fecha: ' + ' '.join(x['word'] for x in w[max(i, j-20):j]))

# 5. som
au, sr = sf.read(P('wav'))
db = lambda x: 20 * np.log10(np.sqrt(np.mean(x**2)) + 1e-9)
seg = lambda t0, t1: au[int(t0*sr):int(t1*sr)]
voz = np.concatenate([seg(x['start'], x['end']) for x in w[::5]])
gaps = [(w[i-1]['end'] + .12, w[i]['start'] - .12) for i in range(1, len(w)) if .6 < w[i]['start'] - w[i-1]['end'] < 3]
fundo = np.concatenate([seg(s, e) for s, e in gaps]) if gaps else np.zeros(10)
lufs = subprocess.run(['ffmpeg', '-v', 'info', '-i', P('wav'), '-af', 'ebur128', '-f', 'null', '-'],
                      capture_output=True, text=True).stderr
lufs = [l.strip() for l in lufs.splitlines() if l.strip().startswith('I:')][-1:]
log(f'\nSom: voz {db(voz):.1f} dBFS · fundo entre frases {db(fundo):.1f} dBFS (trilha ≈ {db(voz)-db(fundo):.0f} dB abaixo) · integrado {lufs}')
for i in range(1, len(w)):
    gg = w[i]['start'] - w[i-1]['end']
    if gg > 6:
        s = w[i-1]['end']
        log(f'  virada @{s/60:.1f} min ({gg:.0f} s), dB por segundo: {[round(db(seg(s+k, s+k+1))) for k in range(min(int(gg), 15))]}')

# 6. planos (troca de imagem, inclusive dissolve)
W_, H_ = 64, 36
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', a.video, '-vf', f'fps=2,scale={W_}:{H_},format=gray',
                      '-f', 'rawvideo', '-'], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, H_, W_).astype(float)
d = np.abs(fr[4:] - fr[:-4]).mean(axis=(1, 2)); cortes = []; ult = -99
for i, v in enumerate(d):
    if v > 18 and i - ult > 6: cortes.append((i + 2) / 2); ult = i
L = np.diff([0] + cortes + [len(fr) / 2])
log(f'\nPlanos: {len(L)} · duração mediana {np.median(L):.1f} s (p25 {np.percentile(L,25):.1f}, p75 {np.percentile(L,75):.1f}) · brilho médio {fr.mean():.0f}/255')

run('ffmpeg', '-v', 'error', '-y', '-i', a.video, '-vf', 'fps=1/30,scale=384:-1,tile=6x10', '-frames:v', '1', P('folha.jpg'))
open(P('relatorio.txt'), 'w').write('\n'.join(linhas) + '\n')
print(f'\nok: {P("relatorio.txt")}')
