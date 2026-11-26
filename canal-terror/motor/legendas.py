#!/usr/bin/env python3
"""Legenda .srt da narração (Whisper da OpenAI, tempo por palavra), já deslocada para o tempo do vídeo.

Uso: python3 -I motor/legendas.py PASTA_PRODUCAO [--deslocar 12]
Saída: PASTA/final/legenda.srt e PASTA/voz/palavras.json (também serve para os Shorts com legenda queimada).
Custo: US$ 0,006 por minuto.
"""
import argparse, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import jsave, parar_se_sem_credito

ap = argparse.ArgumentParser()
ap.add_argument('pasta'); ap.add_argument('--deslocar', type=float, default=12.0)
ap.add_argument('--max', type=int, default=84, help='caracteres por legenda (2 linhas de ~42)')
a = ap.parse_args()
P = lambda *x: os.path.join(a.pasta, *x)

mp3 = P('voz', 'narracao.mp3')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', P('voz', 'narracao.wav'), '-ac', '1', '-ar', '16000', '-b:a', '32k', mp3], check=True)
r = subprocess.run(['curl', '-sS', 'https://api.openai.com/v1/audio/transcriptions',
                    '-H', f"Authorization: Bearer {os.environ.get('OPENAI_API_KEY', 'sk-proxy')}",
                    '-F', 'model=whisper-1', '-F', f'file=@{mp3}', '-F', 'language=en', '-F', 'response_format=verbose_json',
                    '-F', 'timestamp_granularities[]=word', '-F', 'timestamp_granularities[]=segment'], capture_output=True, text=True)
d = json.loads(r.stdout)
if 'error' in d:
    parar_se_sem_credito('OpenAI (Whisper)', json.dumps(d['error'])); sys.exit(d['error'])
jsave(P('voz', 'palavras.json'), d['words'])

# blocos: segue os segmentos do Whisper (frases), quebrando os longos
blocos = []
for sgm in d['segments']:
    ws = [w for w in d['words'] if w['start'] >= sgm['start'] - 0.05 and w['end'] <= sgm['end'] + 0.05]
    texto = sgm['text'].strip().split()
    n = -(-len(sgm['text'].strip()) // a.max)            # partes iguais, sem palavra órfã
    alvo = len(sgm['text'].strip()) / n
    grupos, atual = [], []
    for palavra in texto:
        atual.append(palavra)
        if len(' '.join(atual)) >= alvo and len(grupos) < n - 1:
            grupos.append(atual); atual = []
    if atual: grupos.append(atual)
    k = 0
    for g in grupos:
        w0 = ws[min(k, len(ws) - 1)] if ws else None; k += len(g)
        w1 = ws[min(k - 1, len(ws) - 1)] if ws else None
        ini = w0['start'] if w0 else sgm['start']; fim = w1['end'] if w1 else sgm['end']
        blocos.append((ini, max(fim, ini + 0.8), ' '.join(g)))

def quebra(t):
    if len(t) <= 42: return t
    meio = len(t) // 2; esq = t.rfind(' ', 0, meio); dir_ = t.find(' ', meio)
    corte = esq if dir_ < 0 or (esq >= 0 and meio - esq <= dir_ - meio) else dir_
    return t[:corte] + '\n' + t[corte + 1:]


ts = lambda s: f'{int(s//3600):02d}:{int(s%3600//60):02d}:{int(s%60):02d},{int(round(s%1*1000))%1000:03d}'
os.makedirs(P('final'), exist_ok=True)
with open(P('final', 'legenda.srt'), 'w', encoding='utf-8') as f:
    for n, (i, e, t) in enumerate(blocos, 1):
        f.write(f'{n}\n{ts(i + a.deslocar)} --> {ts(e + a.deslocar)}\n{quebra(t)}\n\n')
print(f'{len(blocos)} legendas · {P("final", "legenda.srt")}')
