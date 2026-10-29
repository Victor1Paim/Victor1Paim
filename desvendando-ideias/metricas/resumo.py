#!/usr/bin/env python3
"""Resume metricas/videos.csv: medianas por pilar, tipo de hook e pele (só vídeos com a métrica preenchida).
Regras do plano de 30 dias: comparar vídeos de IDADE parecida (24 h com 24 h, 7 d com 7 d), usar mediana (não média), não decidir com poucos vídeos.
Uso: python3 -I desvendando-ideias/metricas/resumo.py [arquivo.csv]
"""
import csv, os, statistics, sys

path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'videos.csv')
rows = list(csv.DictReader(open(path, encoding='utf-8')))
METR = ['views_24h', 'views_7d', 'retencao_3s_pct', 'assistido_pct', 'assistido_medio_s', 'comentarios_7d', 'compartilhamentos_7d', 'seguidores_7d']

def num(v):
    try: return float(str(v).replace(',', '.'))
    except Exception: return None

def med(vals):
    vals = [v for v in vals if v is not None]
    return statistics.median(vals) if vals else None

def fmt(v): return '—' if v is None else (f'{v:.0f}' if abs(v) >= 100 else f'{v:.1f}')

print(f'{len(rows)} vídeos no arquivo; com views_7d: {sum(1 for r in rows if num(r["views_7d"]) is not None)}')
base = {m: med([num(r[m]) for r in rows]) for m in METR}
print('\nMediana do canal:', ' · '.join(f'{m} {fmt(base[m])}' for m in METR))
for chave in ('pilar', 'hook_tipo', 'pele'):
    grupos = {}
    for r in rows: grupos.setdefault(r[chave] or '(vazio)', []).append(r)
    print(f'\n== por {chave}')
    print(f'{"grupo":34} {"n":>3} ' + ' '.join(f'{m[:12]:>12}' for m in METR) + '  leitura')
    for g, rs in sorted(grupos.items()):
        vals = {m: med([num(r[m]) for r in rs]) for m in METR}
        n_med = sum(1 for r in rs if num(r['views_7d']) is not None)
        acima = sum(1 for m in METR if vals[m] is not None and base[m] is not None and vals[m] > base[m])
        com = sum(1 for m in METR if vals[m] is not None)
        leitura = 'amostra pequena (< 5 com 7 dias)' if n_med < 5 else (f'acima da mediana em {acima}/{com} métricas')
        print(f'{g[:34]:34} {len(rs):>3} ' + ' '.join(f'{fmt(vals[m]):>12}' for m in METR) + f'  {leitura}')
print('\nLembrete: um pilar só "ganha" se ficar acima da mediana do canal em várias publicações e em mais de uma métrica; com amostra pequena, continuar o teste.')
