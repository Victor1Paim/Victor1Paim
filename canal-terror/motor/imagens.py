#!/usr/bin/env python3
"""Imagens dos planos (OpenAI gpt-image-2), com cache, paralelismo e aviso de crédito.

Uso: python3 -I motor/imagens.py PASTA_PRODUCAO [--qualidade medium] [--simular] [--so s05,s12]

Lê PASTA/planos.json. Cada plano tem "prompt" (gera), "arquivo" (usa uma imagem pronta) ou "reusar" (id de outro plano).
Saída: PASTA/imagens/<id>.png. Já existente = não gera de novo (apague para refazer).
Custo medido: medium 1536x1024 ≈ US$ 0,042 por imagem. Log em PASTA/imagens/custos.jsonl.
"""
import argparse, base64, json, os, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import jload, parar_se_sem_credito, esperar_se_limite

ap = argparse.ArgumentParser()
ap.add_argument('pasta'); ap.add_argument('--qualidade', default='medium')
ap.add_argument('--tamanho', default='1536x1024'); ap.add_argument('--modelo', default='gpt-image-2')
ap.add_argument('--simular', action='store_true'); ap.add_argument('--so', default='')
a = ap.parse_args()

cfg = jload(os.path.join(a.pasta, 'planos.json'))
out = os.path.join(a.pasta, 'imagens'); os.makedirs(out, exist_ok=True)
so = set(filter(None, a.so.split(',')))
planos = ([cfg['vinheta']] if cfg.get('vinheta') else []) + cfg['planos']
PRECO_SAIDA, PRECO_TXT = 30e-6, 5e-6


def gerar(pl):
    dest = os.path.join(out, pl['id'] + '.png')
    if (so and pl['id'] not in so) or os.path.exists(dest) or 'reusar' in pl:
        return 0.0
    if 'arquivo' in pl:
        shutil.copy(os.path.join(a.pasta, pl['arquivo']), dest); return 0.0
    prompt = f"{cfg['estilo']} {pl['prompt']}"
    if a.simular:
        print(f"  {pl['id']}: {len(prompt)} caracteres (simulação)"); return 0.042
    body = {'model': a.modelo, 'prompt': prompt, 'size': a.tamanho, 'quality': a.qualidade, 'n': 1}
    for t in range(8):
        r = subprocess.run(['curl', '-sS', 'https://api.openai.com/v1/images/generations',
                            '-H', f"Authorization: Bearer {os.environ.get('OPENAI_API_KEY', 'sk-proxy')}",
                            '-H', 'Content-Type: application/json', '-d', json.dumps(body)], capture_output=True, text=True)
        try:
            d = json.loads(r.stdout)
        except json.JSONDecodeError:
            d = {'error': {'message': r.stdout[-300:] + r.stderr[-300:]}}
        if 'data' in d:
            break
        msg = json.dumps(d.get('error', d))
        parar_se_sem_credito('OpenAI (imagens)', msg)
        if 'safety' in msg or 'moderation' in msg:
            print(f"  {pl['id']}: recusada pela moderação; reescrever o prompt. {msg[:200]}"); return 0.0
        if not esperar_se_limite(msg, t) and t >= 2:
            sys.exit(f"{pl['id']}: {msg[:400]}")
    open(dest, 'wb').write(base64.b64decode(d['data'][0]['b64_json']))
    u = d.get('usage', {}); custo = u.get('output_tokens', 0) * PRECO_SAIDA + u.get('input_tokens', 0) * PRECO_TXT
    with open(os.path.join(out, 'custos.jsonl'), 'a') as f:
        f.write(json.dumps({'id': pl['id'], 'modelo': a.modelo, 'qualidade': a.qualidade, 'usage': u, 'usd': round(custo, 4)}) + '\n')
    print(f"  {pl['id']} ok (US$ {custo:.3f})")
    return custo


with ThreadPoolExecutor(4) as ex:
    total = sum(ex.map(gerar, planos))
print(f'{"estimado" if a.simular else "gasto agora"}: US$ {total:.2f}')
