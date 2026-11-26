#!/usr/bin/env python3
"""Monta o vídeo final (16:9, 1080p30): história única ou coletânea, com legenda gravada e partes para envio.

Uso:
  python3 -I motor/montar.py PASTA [--rascunho] [--sem-legenda] [--partes-mb 180] [--mbps 6]

PASTA tem planos.json (história única: voz/, imagens/ e planos.json na própria pasta)
ou coletanea.json (várias histórias, cada uma numa subpasta com voz/, imagens/ e planos.json):
  {"titulo": "...", "estilo": "...", "vinheta": {"id": "v00", "prompt": "..."},
   "historias": [{"pasta": "s1", "cartela": ["Story 1", "By: ..."]}, ...]}
A imagem da vinheta fica em PASTA/imagens/v00.png.

Linha do tempo (medida nas referências): 0–7 s vinheta com título · por história: cartela de 5 s com sting
(o drone baixa nas trocas) → narração → 3 s no último plano · fim: 20 s de tela escura (end screen).
Legenda: blocos do Whisper (motor/legendas.py --deslocar 0 em cada história), Inter, embaixo, contorno.
Partes: cortes exatos (quadro-chave forçado) em pausas da narração; juntar na ordem, sem sobreposição.
Saída em PASTA/final/: video.mp4, parte01.mp4…, legenda.srt (para o YouTube), audio.wav, linha-do-tempo.json
"""
import argparse, json, math, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import jload, jsave, duracao, RAIZ

ap = argparse.ArgumentParser()
ap.add_argument('pasta'); ap.add_argument('--rascunho', action='store_true')
ap.add_argument('--sem-legenda', action='store_true'); ap.add_argument('--lufs', type=float, default=-20)
ap.add_argument('--mbps', type=float, default=6.0, help='teto de bitrate do vídeo final')
ap.add_argument('--partes-mb', type=float, default=180, help='tamanho máximo de cada parte (0 = não dividir)')
ap.add_argument('--so-audio', action='store_true', help='refaz só o áudio e troca no video.mp4 existente (sem renderizar a imagem)')
a = ap.parse_args()
P = lambda *x: os.path.join(a.pasta, *x)

# ---------- configuração: coletânea ou história única ----------
if os.path.exists(P('coletanea.json')):
    col = jload(P('coletanea.json'))
    hist = [dict(h, dir=P(h['pasta'])) for h in col['historias']]
    vinheta_img = P('imagens', col['vinheta']['id'] + '.png')
    titulo = col['titulo']
    trilha_cfg = col.get('trilha')
else:
    pl = jload(P('planos.json'))
    hist = [{'dir': a.pasta, 'cartela': pl.get('cartela', ['Story 1', ''])}]
    vinheta_img = P('imagens', pl['vinheta']['id'] + '.png')
    titulo = pl.get('titulo', '')
    trilha_cfg = pl.get('trilha')
for h in hist:
    h['planos'] = jload(os.path.join(h['dir'], 'planos.json'))['planos']
    h['tempos'] = jload(os.path.join(h['dir'], 'voz', 'tempos.json'))
    h['blocos'] = jload(os.path.join(h['dir'], 'voz', 'blocos.json'), [])

W, H = (960, 540) if a.rascunho else (1920, 1080)
FPS, D = 30, 1.0
T_VIN, T_CART, FIM_HOLD, END_SCREEN = 7.0, 5.0, 3.0, 20.0
FONTE_TITULO = os.path.join(RAIZ, 'marca/fontes/CormorantGaramond-Medium.ttf')
FONTE_TEXTO = '/usr/share/fonts/opentype/inter/Inter-Light.otf'
FONTE_MONO = subprocess.run(['fc-match', '-f', '%{file}', 'JetBrains Mono'], capture_output=True, text=True).stdout
fin = P('final'); tmp = os.path.join(fin, f'clipes-{H}p'); os.makedirs(tmp, exist_ok=True)   # cache por resolução
esc = lambda s: s.replace('\\', '\\\\').replace(':', '\\:').replace("'", "’")
s = H / 1080

# ---------- linha do tempo ----------
t = T_VIN
blocos_video = []       # ('cartela', ini, fim, h) | ('plano', ini, fim, h, plano)
for h in hist:
    blocos_video.append(('cartela', t, t + T_CART, h)); t += T_CART
    h['T0'] = t
    tempos = h['tempos']
    inicio_par = [t + x['inicio'] for x in tempos] + [t + tempos[-1]['fim'] + FIM_HOLD]
    por_par = {}
    for pl in h['planos']:
        por_par.setdefault(pl['p'], []).append(pl)
    segs = []
    for p in range(len(tempos)):
        ini, fim = inicio_par[p], inicio_par[p + 1]
        pls = por_par.get(p, [])
        if not pls:
            segs[-1] = (segs[-1][0], segs[-1][1], fim); continue
        passo = (fim - ini) / len(pls)
        for k, pl in enumerate(pls):
            segs.append((pl, ini + k * passo, ini + (k + 1) * passo))
    segs[0] = (segs[0][0], h['T0'], segs[0][2])
    for pl, ini, fim in segs:
        blocos_video.append(('plano', ini, fim, h, pl))
    t = segs[-1][2]
    h['fim'] = t
total = t + END_SCREEN
MOVS = ['in', 'right', 'out', 'left']


def render(job):
    nome, img, dur, mov, extra = job
    out = os.path.join(tmp, nome + '.mp4')
    if os.path.exists(out) and abs(duracao(out) - dur) < 0.05:
        return out
    n = int(round(dur * FPS)); Z = 0.07
    z = {'in': f'1+{Z}*on/{n}', 'out': f'1+{Z}-{Z}*on/{n}', 'left': f'1+{Z}', 'right': f'1+{Z}'}[mov]
    x = {'left': f'(iw-iw/zoom)*(1-on/{n})', 'right': f'(iw-iw/zoom)*on/{n}'}.get(mov, 'iw/2-iw/zoom/2')
    big = 3840 if not a.rascunho else 1920
    vf = (f"scale={big}:-2,crop={big}:{big*9//16},"
          f"zoompan=z='{z}':x='{x}':y='ih/2-ih/zoom/2':d={n}:s={W}x{H}:fps={FPS},setsar=1")
    if extra: vf += ',' + extra
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', img, '-vf', vf, '-frames:v', str(n),
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '14', '-pix_fmt', 'yuv420p', out], check=True)
    return out


al = lambda a0, a1, b0, b1: f"alpha='if(lt(t,{a0}),0,if(lt(t,{a1}),(t-{a0})/({a1}-{a0}),if(lt(t,{b0}),1,max(0,1-(t-{b0})/({b1}-{b0})))))'"


def cartela(job):
    nome, linhas = job
    out = os.path.join(tmp, nome + '.mp4')
    if os.path.exists(out): return out
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'color=c=0x0b0b0d:s={W}x{H}:r={FPS}:d={T_CART + D}', '-vf',
                    f"drawtext=fontfile={FONTE_TEXTO}:text='{esc(linhas[0])}':fontsize={int(58*s)}:fontcolor=white@0.9:x=(w-tw)/2:y=h/2-{int(52*s)}:{al(0.4,1.2,4.6,5.4)},"
                    f"drawtext=fontfile={FONTE_TEXTO}:text='{esc(linhas[1])}':fontsize={int(28*s)}:fontcolor=white@0.7:x=(w-tw)/2:y=h/2+{int(18*s)}:{al(0.6,1.4,4.6,5.4)}",
                    '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', out], check=True)
    return out


jobs, linha, ordem = [], [], []
linhas_tit = [x.strip() for x in titulo.split('|')]          # "|" quebra a linha do título
tam_tit = int((104 if len(linhas_tit) == 1 else 88) * s)
alfa_tit = "alpha='if(lt(t,1.3),0,if(lt(t,2.4),(t-1.3)/1.1,if(lt(t,5.6),1,max(0,1-(t-5.6)/0.9))))'"
txt_tit = ','.join(f"drawtext=fontfile={FONTE_TITULO}:text='{esc(l)}':fontsize={tam_tit}:fontcolor=white@0.92:x=(w-tw)/2:"
                   f"y=h/2-{int(tam_tit * 1.15 * len(linhas_tit) / 2)}+{int(tam_tit * 1.15 * i)}:{alfa_tit}"
                   for i, l in enumerate(linhas_tit))
jobs.append(('000-vinheta', vinheta_img, T_VIN + D, 'in', txt_tit + ',fade=t=in:st=0:d=1.2'))
ordem.append(('r', 0, 0.0))
cartelas, k = [], 0
for b in blocos_video:
    if b[0] == 'cartela':
        nome = f'{len(ordem):03d}-cartela'; cartelas.append((nome, b[3]['cartela'])); ordem.append(('c', nome, b[1]))
        linha.append({'cartela': b[3]['cartela'][0], 'inicio': round(b[1], 2)})
        continue
    _, ini, fim, h, pl = b
    extra = ''
    if pl.get('carimbo'):
        c = pl['carimbo']; base, sg = c[:-2], int(c[-2:])
        extra = (f"drawtext=fontfile={FONTE_MONO}:text='{esc(base)}%{{eif\\:mod({sg}+t\\,60)\\:d\\:2}}':"
                 f"fontsize={int(34*s)}:fontcolor=white@0.85:x=w-tw-{int(60*s)}:y=h-th-{int(50*s)}")
    img = os.path.join(h['dir'], 'imagens', (pl.get('reusar') or pl['id']) + '.png')
    nome = f'{len(ordem):03d}-{os.path.basename(h["dir"].rstrip("/"))}-{pl["id"]}'
    jobs.append((nome, img, fim - ini + D, MOVS[k % 4], extra)); k += 1
    ordem.append(('r', len(jobs) - 1, ini))
    linha.append({'plano': pl['id'], 'inicio': round(ini, 2), 'fim': round(fim, 2)})
ultimo = hist[-1]
lua = next((pl for pl in ultimo['planos'] if 'moon' in pl.get('prompt', '').lower()), ultimo['planos'][-1])
jobs.append(('999-fim', os.path.join(ultimo['dir'], 'imagens', (lua.get('reusar') or lua['id']) + '.png'), END_SCREEN, 'in',
             'eq=brightness=-0.06,fade=t=out:st=%.2f:d=3' % (END_SCREEN - 3)))
ordem.append(('r', len(jobs) - 1, ultimo['fim']))

print(f'{len(hist)} história(s) · {len(jobs)} clipes · {total/60:.2f} min · {W}x{H}')
with ThreadPoolExecutor(os.cpu_count() or 4) as ex:
    arqs = list(ex.map(render, jobs))
    arq_c = dict(zip([c[0] for c in cartelas], ex.map(cartela, cartelas)))
entradas = [arqs[o[1]] if o[0] == 'r' else arq_c[o[1]] for o in ordem]
starts = [o[2] for o in ordem]

# ---------- áudio ----------
SR = 48000
N = int((total + 1) * SR)
voz_fx, drone = np.zeros((N, 2)), np.zeros((N, 2))


def colocar(trilha, arq, t0, db=0.0):
    x, sr = sf.read(arq, always_2d=True)
    assert sr == SR, (arq, sr)
    if x.shape[1] == 1: x = np.repeat(x, 2, 1)
    i = int(t0 * SR); x = x[:N - i] * 10 ** (db / 20)
    trilha[i:i + len(x)] += x


rms = lambda v: 20 * np.log10(np.sqrt(np.mean(v ** 2)) + 1e-9)
niveis = []
for h in hist:
    colocar(voz_fx, os.path.join(h['dir'], 'voz', 'narracao.wav'), h['T0'])
    v, _ = sf.read(os.path.join(h['dir'], 'voz', 'narracao.wav')); niveis.append(rms(v[v != 0]))
voz_db = float(np.mean(niveis))
if trilha_cfg:                               # trilha da biblioteca (ElevenLabs): {"drone", "sting", "vinheta", "drone_db"}
    import sfxmix
    sfxmix.colocar(voz_fx, sfxmix.carregar(trilha_cfg['vinheta']), 0.0, voz_db + trilha_cfg.get('vinheta_db', -1))
    st = sfxmix.carregar(trilha_cfg['sting'])
    for b in blocos_video:
        if b[0] == 'cartela':
            sfxmix.colocar(voz_fx, st, b[1] - 1.2, voz_db + trilha_cfg.get('sting_db', -3))
    x = sfxmix.em_loop(sfxmix.carregar(trilha_cfg['drone']), N - int((T_VIN - 0.5) * SR))
    f = int(2.5 * SR); x[:f] *= np.linspace(0, 1, f)[:, None]
    sfxmix.colocar(drone, x, T_VIN - 0.5, voz_db + trilha_cfg.get('drone_db', -11))
    avisos = []
    for h in hist:
        q = sfxmix.aplicar_historia(voz_fx, h['dir'], h['T0'], h['tempos'], voz_db, avisos)
        print(f"  efeitos de {os.path.basename(h['dir'].rstrip('/'))}: {q}")
    for av in avisos: print('  AVISO', av)
else:                                        # trilha sintetizada (antiga)
    tr = P('trilha')
    if not os.path.exists(os.path.join(tr, 'drone.wav')) or duracao(os.path.join(tr, 'drone.wav')) < total:
        subprocess.run([sys.executable, '-I', os.path.join(RAIZ, 'motor/trilha.py'), tr, '--duracao', f'{total + 2:.0f}'], check=True)
    colocar(voz_fx, os.path.join(tr, 'vinheta.wav'), 0.0, -2)
    for b in blocos_video:
        if b[0] == 'cartela':
            colocar(voz_fx, os.path.join(tr, 'sting.wav'), b[1] - 1.4, -4)
    dr, _ = sf.read(os.path.join(tr, 'drone.wav'))
    colocar(drone, os.path.join(tr, 'drone.wav'), T_VIN - 0.5, voz_db - 7 - rms(dr))
env = np.ones(N)
for b in blocos_video[1:]:                   # o drone baixa nas trocas de história (como nas referências)
    if b[0] == 'cartela':
        i0, i1 = int((b[1] - 1.5) * SR), int((b[1] + T_CART) * SR)
        env[i0:i1] = np.minimum(env[i0:i1], np.interp(np.arange(i0, i1), [i0, i0 + SR, i1 - SR * 1.5, i1], [1, .15, .15, 1]))
i0, i1 = int((ultimo['fim'] + 1) * SR), int((total - 1) * SR)
env[i0:i1] *= np.linspace(1, 0.3, i1 - i0); env[i1:] *= 0.3
mix = voz_fx + drone * env[:, None]
sf.write(os.path.join(fin, 'mix-bruto.wav'), mix.astype(np.float32), SR)
med = subprocess.run(['ffmpeg', '-v', 'info', '-i', os.path.join(fin, 'mix-bruto.wav'), '-af',
                      f'highpass=f=28,alimiter=limit=0.5:attack=2:release=60:level=false,loudnorm=I={a.lufs}:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'],
                     capture_output=True, text=True).stderr
j = json.loads(med[med.rindex('{'):med.rindex('}') + 1])
audio = os.path.join(fin, 'audio.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(fin, 'mix-bruto.wav'), '-af',
                f"highpass=f=28,alimiter=limit=0.5:attack=2:release=60:level=false,loudnorm=I={a.lufs}:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
                f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,"
                f"afade=t=out:st={total-3:.2f}:d=3", '-ar', '48000', '-t', f'{total:.3f}', audio], check=True)
os.remove(os.path.join(fin, 'mix-bruto.wav'))

# ---------- legenda (.srt para o YouTube e .ass gravada no vídeo) ----------
leg = [(b['inicio'] + h['T0'], b['fim'] + h['T0'], b['texto']) for h in hist for b in h['blocos']]


def quebra(t, n=42):
    if len(t) <= n: return [t]
    meio = len(t) // 2; e = t.rfind(' ', 0, meio); d = t.find(' ', meio)
    c = e if d < 0 or (e >= 0 and meio - e <= d - meio) else d
    return [t[:c], t[c + 1:]]


ts = lambda x: f'{int(x//3600):02d}:{int(x%3600//60):02d}:{int(x%60):02d},{int(round(x%1*1000))%1000:03d}'
ta = lambda x: f'{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}'
with open(os.path.join(fin, 'legenda.srt'), 'w', encoding='utf-8') as f:
    for n, (i, e, txt) in enumerate(leg, 1):
        f.write(f'{n}\n{ts(i)} --> {ts(e)}\n' + '\n'.join(quebra(txt)) + '\n\n')
ass = os.path.join(fin, 'legenda.ass')
with open(ass, 'w', encoding='utf-8') as f:
    f.write(f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: L,Inter Medium,{int(44*s)},&H00EDF0F2,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,0.3,0,1,{2.2*s:.1f},{1.2*s:.1f},2,{int(160*s)},{int(160*s)},{int(72*s)},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""")
    for i, e, txt in leg:
        f.write(f"Dialogue: 0,{ta(i)},{ta(e)},L,,0,0,0,,{{\\fad(120,120)}}" + '\\N'.join(quebra(txt)) + '\n')

# ---------- cortes das partes: em pausas entre parágrafos, perto de tamanhos iguais ----------
cortes = []
if a.partes_mb and not a.rascunho:
    tam_mb = (a.mbps + 0.2) * total / 8
    n_partes = max(1, math.ceil(tam_mb / a.partes_mb))
    pausas = []
    for h in hist:
        tp = h['tempos']
        pausas += [h['T0'] + (tp[i]['fim'] + tp[i + 1]['inicio']) / 2 for i in range(len(tp) - 1)]
    pausas += [b[1] + 2.5 for b in blocos_video if b[0] == 'cartela'][1:]
    for q in range(1, n_partes):
        alvo = total * q / n_partes
        c = min(pausas, key=lambda x: abs(x - alvo))
        cortes.append(round(round(c * FPS) / FPS, 3))      # exatamente num quadro

# ---------- vídeo ----------
fc = [f"[{k}:v]fps={FPS},settb=1/{FPS},setpts=PTS-STARTPTS,format=yuv420p[n{k}]" for k in range(len(entradas))]
prev = '[n0]'
for k in range(1, len(entradas)):
    fc.append(f"{prev}[n{k}]xfade=transition=fade:duration={D}:offset={starts[k]:.3f}[x{k}]"); prev = f'[x{k}]'
grade = ("eq=saturation=0.72:contrast=0.94:brightness=-0.035:gamma=0.97,colorbalance=bs=0.04:bm=0.02:rh=-0.02,"
         f"vignette=angle=PI/4.5,noise=alls={4 if a.rascunho else 5}:allf=t")
if not a.sem_legenda and leg:
    grade += f",subtitles={ass}:fontsdir=/usr/share/fonts/opentype/inter"
MARCA = os.path.join(RAIZ, 'marca/marca-dagua.png')
if os.path.exists(MARCA):                    # marca d'água do canal: canto superior direito (embaixo fica a legenda), 35%, depois da vinheta
    fc.append(f"movie={MARCA},format=rgba,scale=-1:{int(46*s)},colorchannelmixer=aa=0.35[wm]")
    fc.append(f"{prev}{grade}[g];[g][wm]overlay=W-w-{int(48*s)}:{int(40*s)}:enable='gte(t,{T_VIN + T_CART})',format=yuv420p[v]")
else:
    fc.append(f"{prev}{grade},format=yuv420p[v]")
saida = os.path.join(fin, 'video-rascunho.mp4' if a.rascunho else 'video.mp4')
cmd = ['ffmpeg', '-v', 'error', '-stats', '-y']
for e in entradas: cmd += ['-i', e]
cmd += ['-i', audio, '-filter_complex', ';'.join(fc), '-map', '[v]', '-map', f'{len(entradas)}:a',
        '-c:v', 'libx264', '-preset', 'veryfast' if a.rascunho else 'medium', '-crf', '21',
        '-maxrate', f'{a.mbps}M', '-bufsize', f'{2*a.mbps}M', '-r', str(FPS), '-c:a', 'aac', '-b:a', '192k']
if cortes:
    cmd += ['-force_key_frames', ','.join(f'{c:.3f}' for c in cortes)]
cmd += ['-t', f'{total:.3f}', '-movflags', '+faststart', saida]
if a.so_audio:
    novo = saida + '.novo.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', saida, '-i', audio, '-map', '0:v', '-map', '1:a', '-c:v', 'copy',
                    '-c:a', 'aac', '-b:a', '192k', '-t', f'{total:.3f}', '-movflags', '+faststart', novo], check=True)
    os.replace(novo, saida)
else:
    r = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
    if r.returncode:
        sys.exit('ffmpeg falhou:\n' + r.stderr[-1500:])
if cortes:
    for f in os.listdir(fin):
        if f.startswith('parte') and f.endswith('.mp4'): os.remove(os.path.join(fin, f))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', saida, '-map', '0', '-c', 'copy', '-f', 'segment',
                    '-segment_times', ','.join(f'{c:.3f}' for c in cortes), '-reset_timestamps', '1',
                    '-segment_start_number', '1', os.path.join(fin, 'parte%02d.mp4')], check=True)
jsave(os.path.join(fin, 'linha-do-tempo.json'), {'total': round(total, 2), 'cortes_das_partes': cortes,
      'historias': [{'cartela': h['cartela'][0], 'narracao_comeca': round(h['T0'], 2), 'termina': round(h['fim'], 2)} for h in hist],
      'blocos': linha})
print('ok', saida, 'partes nos tempos:', cortes)
