#!/usr/bin/env python3
"""Monta o vídeo final (16:9, 1080p30) a partir de planos.json, voz/ e trilha/.

Uso: python3 -I motor/montar.py PASTA_PRODUCAO [--rascunho]   (--rascunho: 540p, rápido, para conferir)

Linha do tempo (medida nas referências):
  0–7 s vinheta (imagem + título) · 7–12 s cartela "Story N / By" com sting · 12 s narração ·
  1 plano por parágrafo (ou mais), dissolve de 1 s, movimento lento alternado ·
  fim: 4 s no último plano + 20 s de tela final escura (end screen do YouTube).
Áudio: narração + drone ~13 dB abaixo da voz + impacto da vinheta + sting; normalizado a -20 LUFS.
Saída: PASTA/final/video.mp4, PASTA/final/audio.wav (mix), PASTA/final/linha-do-tempo.json
"""
import argparse, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import jload, jsave, duracao, RAIZ

ap = argparse.ArgumentParser()
ap.add_argument('pasta'); ap.add_argument('--rascunho', action='store_true')
ap.add_argument('--lufs', type=float, default=-20)
a = ap.parse_args()
P = lambda *x: os.path.join(a.pasta, *x)
cfg = jload(P('planos.json')); tempos = jload(P('voz', 'tempos.json'))
W, H = (960, 540) if a.rascunho else (1920, 1080)
FPS = 30
T_VIN, T_CART = 7.0, 5.0
T0 = T_VIN + T_CART
D = 1.0                       # dissolve
FIM_HOLD, END_SCREEN = 4.0, 20.0
FONTE_TITULO = os.path.join(RAIZ, 'marca/fontes/CormorantGaramond-Medium.ttf')
FONTE_TEXTO = '/usr/share/fonts/opentype/inter/Inter-Light.otf'
FONTE_MONO = subprocess.run(['fc-match', '-f', '%{file}', 'JetBrains Mono'], capture_output=True, text=True).stdout
tmp = P('final', 'clipes'); os.makedirs(tmp, exist_ok=True)
esc = lambda s: s.replace('\\', '\\\\').replace(':', '\\:').replace("'", "’")

# ---------- tempos dos planos ----------
narr_fim = T0 + tempos[-1]['fim']
inicio_par = [T0 + t['inicio'] for t in tempos] + [narr_fim + FIM_HOLD]
por_par = {}
for pl in cfg['planos']:
    por_par.setdefault(pl['p'], []).append(pl)
segs = []                                   # (plano, inicio, fim)
for p in range(len(tempos)):
    ini, fim = inicio_par[p], inicio_par[p + 1]
    if p == 0: ini = T0
    pls = por_par.get(p, [])
    if not pls:
        segs[-1] = (segs[-1][0], segs[-1][1], fim); continue
    passo = (fim - ini) / len(pls)
    for k, pl in enumerate(pls):
        segs.append((pl, ini + k * passo, ini + (k + 1) * passo))
total = segs[-1][2] + END_SCREEN


def img_de(pl):
    return P('imagens', (pl.get('reusar') or pl['id']) + '.png')


MOVS = ['in', 'right', 'out', 'left']


def render(job):
    nome, img, dur, mov, extra = job
    out = os.path.join(tmp, nome + '.mp4')
    if os.path.exists(out) and abs(duracao(out) - dur) < 0.05:
        return out
    n = int(round(dur * FPS)); Z = 0.07
    z = {'in': f'1+{Z}*on/{n}', 'out': f'1+{Z}-{Z}*on/{n}', 'left': f'1+{Z}', 'right': f'1+{Z}', 'still': '1'}[mov]
    x = {'left': f'(iw-iw/zoom)*(1-on/{n})', 'right': f'(iw-iw/zoom)*on/{n}'}.get(mov, 'iw/2-iw/zoom/2')
    big = 3840 if not a.rascunho else 1920
    vf = (f"scale={big}:-2,crop={big}:{big*9//16},"
          f"zoompan=z='{z}':x='{x}':y='ih/2-ih/zoom/2':d={n}:s={W}x{H}:fps={FPS},setsar=1")
    if extra: vf += ',' + extra
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', img, '-vf', vf, '-frames:v', str(n),
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '14', '-pix_fmt', 'yuv420p', out], check=True)
    return out


jobs, linha = [], []
s = H / 1080
# vinheta com título
tit = esc(cfg.get('titulo', ''))
jobs.append(('00-vinheta', P('imagens', cfg['vinheta']['id'] + '.png'), T_VIN + D, 'in',
             f"drawtext=fontfile={FONTE_TITULO}:text='{tit}':fontsize={int(118*s)}:fontcolor=white@0.92:x=(w-tw)/2:y=(h-th)/2:"
             f"alpha='if(lt(t,1.3),0,if(lt(t,2.4),(t-1.3)/1.1,if(lt(t,5.6),1,max(0,1-(t-5.6)/0.9))))',"
             f"fade=t=in:st=0:d=1.2"))
for i, (pl, ini, fim) in enumerate(segs):
    extra = ''
    if pl.get('carimbo'):
        c = pl['carimbo']; base, seg_ = c[:-2], int(c[-2:])
        extra = (f"drawtext=fontfile={FONTE_MONO}:text='{esc(base)}%{{eif\\:mod({seg_}+t\\,60)\\:d\\:2}}':"
                 f"fontsize={int(34*s)}:fontcolor=white@0.85:x=w-tw-{int(60*s)}:y=h-th-{int(50*s)}")
    dur = fim - ini + D
    jobs.append((f'{i+1:02d}-{pl["id"]}', img_de(pl), dur, MOVS[i % 4], extra))
    linha.append({'plano': pl['id'], 'inicio': round(ini, 2), 'fim': round(fim, 2)})
# tela final: lua bem escura, quase parada
lua = next((pl for pl in cfg['planos'] if 'moon' in pl.get('prompt', '').lower()), segs[-1][0])
jobs.append(('99-fim', img_de(lua), END_SCREEN, 'in', 'eq=brightness=-0.06,fade=t=out:st=%.2f:d=3' % (END_SCREEN - 3)))

print(f'{len(jobs)} clipes · vídeo de {total/60:.2f} min · renderizando {W}x{H}…')
with ThreadPoolExecutor(os.cpu_count() or 4) as ex:
    arqs = list(ex.map(render, jobs))

# cartela (preto + texto), gerada direto
cart = cfg.get('cartela', ['Story 1', ''])
cart_out = os.path.join(tmp, '00-cartela.mp4')
al = lambda a0, a1, b0, b1: f"alpha='if(lt(t,{a0}),0,if(lt(t,{a1}),(t-{a0})/({a1}-{a0}),if(lt(t,{b0}),1,max(0,1-(t-{b0})/({b1}-{b0})))))'"
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'color=c=0x0b0b0d:s={W}x{H}:r={FPS}:d={T_CART + D}', '-vf',
                f"drawtext=fontfile={FONTE_TEXTO}:text='{esc(cart[0])}':fontsize={int(58*s)}:fontcolor=white@0.9:x=(w-tw)/2:y=h/2-{int(52*s)}:{al(0.4,1.2,4.6,5.4)},"
                f"drawtext=fontfile={FONTE_TEXTO}:text='{esc(cart[1])}':fontsize={int(28*s)}:fontcolor=white@0.7:x=(w-tw)/2:y=h/2+{int(18*s)}:{al(0.6,1.4,4.6,5.4)}",
                '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', cart_out], check=True)

# ---------- áudio ----------
SR = 48000
mix = np.zeros((int((total + 1) * SR), 2))
def colocar(arq, t, ganho_db=0.0):
    x, sr = sf.read(arq, always_2d=True)
    assert sr == SR, (arq, sr)
    if x.shape[1] == 1: x = np.repeat(x, 2, 1)
    i = int(t * SR); x = x[:len(mix) - i] * 10 ** (ganho_db / 20)
    mix[i:i + len(x)] += x
    return x
voz, _ = sf.read(P('voz', 'narracao.wav'))
rms = lambda v: 20 * np.log10(np.sqrt(np.mean(v ** 2)) + 1e-9)
dr, _ = sf.read(P('trilha', 'drone.wav'))
g_drone = rms(voz[voz != 0]) - 7 - rms(dr)   # medido: fica ~11 dB abaixo da voz depois do highpass
colocar(P('voz', 'narracao.wav'), T0)
colocar(P('trilha', 'vinheta.wav'), 0.0, -2)
colocar(P('trilha', 'sting.wav'), T_VIN - 1.4, -4)
# drone em faixa própria: baixa devagar durante a tela final
voz_fx = mix.copy(); mix[:] = 0
colocar(P('trilha', 'drone.wav'), T_VIN - 0.5, g_drone)
ini_f, fim_i = int((segs[-1][2] + 1) * SR), int((total - 1) * SR)
env = np.ones(len(mix)); env[ini_f:fim_i] = np.linspace(1, 0.3, fim_i - ini_f); env[fim_i:] = 0.3
mix = voz_fx + mix * env[:, None]
final_dir = P('final')
sf.write(os.path.join(final_dir, 'mix-bruto.wav'), mix.astype(np.float32), SR)
# loudness: 2 passadas
med = subprocess.run(['ffmpeg', '-v', 'info', '-i', os.path.join(final_dir, 'mix-bruto.wav'), '-af',
                      f'highpass=f=28,loudnorm=I={a.lufs}:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'],
                     capture_output=True, text=True).stderr
j = json.loads(med[med.rindex('{'):med.rindex('}') + 1])
af = (f"highpass=f=28,loudnorm=I={a.lufs}:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
      f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,"
      f"afade=t=out:st={total-3:.2f}:d=3")
audio = os.path.join(final_dir, 'audio.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(final_dir, 'mix-bruto.wav'), '-af', af, '-ar', '48000',
                '-t', f'{total:.3f}', audio], check=True)

# ---------- vídeo: dissolves + cor ----------
entradas = [arqs[0], cart_out] + arqs[1:]
starts = [0.0, T_VIN] + [ini for _, ini, _ in segs] + [segs[-1][2]]
fc = [f"[{k}:v]fps={FPS},settb=1/{FPS},setpts=PTS-STARTPTS,format=yuv420p[n{k}]" for k in range(len(entradas))]
prev = '[n0]'
for k in range(1, len(entradas)):
    lab = f'[x{k}]'
    fc.append(f"{prev}[n{k}]xfade=transition=fade:duration={D}:offset={starts[k]:.3f}{lab}")
    prev = lab
grade = ("eq=saturation=0.72:contrast=0.94:brightness=-0.035:gamma=0.97,"
         "colorbalance=bs=0.04:bm=0.02:rh=-0.02,"
         f"vignette=angle=PI/4.5,noise=alls={4 if a.rascunho else 7}:allf=t,format=yuv420p")
fc.append(f"{prev}{grade}[v]")
cmd = ['ffmpeg', '-v', 'error', '-stats', '-y']
for e in entradas: cmd += ['-i', e]
cmd += ['-i', audio, '-filter_complex', ';'.join(fc), '-map', '[v]', '-map', f'{len(entradas)}:a',
        '-c:v', 'libx264', '-preset', 'medium' if not a.rascunho else 'veryfast', '-crf', '20', '-r', str(FPS),
        '-c:a', 'aac', '-b:a', '192k', '-t', f'{total:.3f}', '-movflags', '+faststart',
        os.path.join(final_dir, 'video-rascunho.mp4' if a.rascunho else 'video.mp4')]
r = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
if r.returncode:
    sys.exit('ffmpeg falhou:\n' + r.stderr[-1500:])
jsave(os.path.join(final_dir, 'linha-do-tempo.json'), {'T0_narracao': T0, 'total': round(total, 2), 'planos': linha})
print('ok')
