#!/usr/bin/env python3
"""Baixa só um trecho de um VOD da Twitch, em vídeo, pelos segmentos HLS (evita o travamento do ffmpeg com fMP4).
Uso: trecho-vod.py <id_vod> <ini_s> <fim_s> <saida.mp4> [formato=1080p60] [transcricao.json da análise] [offset_da_analise_s]
Se receber a transcrição da análise, grava <saida>.json com os tempos deslocados para o trecho (para usar como LONGA no corte-gringo)."""
import sys, subprocess, os, re, json, tempfile, urllib.request, concurrent.futures as cf

vid, ini, fim, saida = sys.argv[1].lstrip('v'), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
fmt = sys.argv[5] if len(sys.argv) > 5 else '1080p60'
m3u8 = subprocess.check_output(['yt-dlp', '-f', fmt, '-g', f'https://www.twitch.tv/videos/{vid}'], text=True).strip()
base = m3u8.rsplit('/', 1)[0]
pl = urllib.request.urlopen(m3u8).read().decode()
mapa = re.search(r'#EXT-X-MAP:URI="([^"]+)"', pl)
segs, t = [], 0.0
for dur, nome in re.findall(r'#EXTINF:([\d.]+),\s*\n([^\n#]+)', pl):
    d = float(dur)
    if t + d > ini - 2 and t < fim + 2: segs.append((t, nome.strip()))
    t += d
if not segs: sys.exit('trecho fora do VOD')
t0 = segs[0][0]
tmp = tempfile.mkdtemp()
baixa = lambda n: urllib.request.urlopen(f'{base}/{n}').read()
with cf.ThreadPoolExecutor(16) as ex: partes = list(ex.map(baixa, [n for _, n in segs]))
cru = os.path.join(tmp, 'cru' + ('.mp4' if mapa else '.ts'))
with open(cru, 'wb') as f:
    if mapa: f.write(baixa(mapa.group(1)))
    for p in partes: f.write(p)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-fflags', '+genpts', '-ss', str(ini - t0), '-i', cru, '-t', str(fim - ini),
                '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '16', '-c:a', 'aac', '-b:a', '192k', saida], check=True)
if len(sys.argv) > 7:
    off = float(sys.argv[7])
    tr = [{'t': round(s['t'] + off - ini, 2), 'f': round(s['f'] + off - ini, 2), 'x': s['x']} for s in json.load(open(sys.argv[6])) if ini - 1 <= s['t'] + off < fim]
    json.dump(tr, open(saida.rsplit('.', 1)[0] + '.json', 'w'), ensure_ascii=False)
print('ok', saida, f'{fim - ini:.0f}s')
