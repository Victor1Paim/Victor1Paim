#!/usr/bin/env python3
"""Busca momentos em todas as lives já analisadas (gravacoes/**/indice.json).
Uso: buscar-momentos.py "<termos>" [--categoria ensinamento] [--min-forca 7]
Exemplos: buscar-momentos.py "farol"  ·  buscar-momentos.py "" --categoria curiosidade --min-forca 8"""
import sys, json, glob, os, argparse

ap = argparse.ArgumentParser()
ap.add_argument('termos', nargs='?', default='')
ap.add_argument('--categoria')
ap.add_argument('--min-forca', type=float, default=0)
a = ap.parse_args()
raiz = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'gravacoes')
termos = [t.lower() for t in a.termos.split() if t]
achados = []
for f in glob.glob(os.path.join(raiz, '**', 'indice.json'), recursive=True):
    d = json.load(open(f))
    for t in d['trechos']:
        texto = ' '.join([t.get('resumo', ''), ' '.join(t.get('tags', [])), t.get('categoria', '')]).lower()
        # inclui a fala dos blocos do trecho na busca
        mm = lambda s: int(s.split(':')[0]) * 60 + int(s.split(':')[1])
        try: ini, fim = mm(t['inicio']), mm(t['fim'])
        except Exception: continue
        texto += ' ' + ' '.join(b['fala'] for b in d['blocos'] if ini <= b['t'] < fim).lower()
        if termos and not all(x in texto for x in termos): continue
        if a.categoria and t.get('categoria') != a.categoria: continue
        if t.get('forca', 0) < a.min_forca: continue
        achados.append((t.get('forca', 0), os.path.relpath(os.path.dirname(f), raiz), d['meta'].get('offset_vod_s', 0), t))
for forca, pasta, off, t in sorted(achados, key=lambda x: -x[0]):
    extra = f" (no VOD: +{int(off)} s)" if off else ''
    print(f"[{forca}] {pasta} {t['inicio']}-{t['fim']}{extra} · {t.get('categoria')} · {t.get('resumo')} · tags: {', '.join(t.get('tags', []))}")
print(f'{len(achados)} trecho(s).')
