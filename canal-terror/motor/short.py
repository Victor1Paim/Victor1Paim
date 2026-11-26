#!/usr/bin/env python3
"""Short vertical (1080x1920) para YouTube Shorts e TikTok, com gancho, legenda grande e chamada para o vídeo completo.

Uso: python3 -I motor/short.py PASTA   (PASTA/short.json + PASTA/imagens/ geradas com motor/imagens.py --tamanho 1024x1536)

short.json:
  "segmentos": [{"texto": "..."} (voz nova, Gemini Enceladus) | {"wav": "caminho/pNN.wav"} (narração já gerada)]
  "planos": [{"id": "v1", "seg": 0}, ...]   imagem por segmento (vários por segmento dividem o tempo)
  "gancho_tela": "LINHA|LINHA"   texto grande no topo nos primeiros 3 s
  "cta_tela":    "LINHA|LINHA"   texto no fim, durante o último segmento
Saída: PASTA/final/short.mp4 (−14 LUFS, legenda gravada), PASTA/final/legenda.srt
"""
import json, os, subprocess, sys
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import GEMINI, env_gemini, jload, duracao, parar_se_sem_credito, esperar_se_limite, RAIZ

pasta = sys.argv[1]
P = lambda *x: os.path.join(pasta, *x)
cfg = jload(P('short.json'))
W, H, FPS, D = 1080, 1920, 30, 0.6
VEL, SR = 1.06, 48000
fin = P('final'); os.makedirs(P('voz'), exist_ok=True); os.makedirs(os.path.join(fin, 'clipes'), exist_ok=True)

# ---------- voz: segmentos novos (Gemini) + narração existente ----------
wavs = []
for i, sg in enumerate(cfg['segmentos']):
    if 'wav' in sg:
        wavs.append(os.path.normpath(os.path.join(pasta, sg['wav']))); continue
    wav = P('voz', f'seg{i:02d}.wav')
    if not os.path.exists(wav):
        txt = P('voz', f'seg{i:02d}.txt'); open(txt, 'w').write(sg['texto'])
        for tent in range(6):
            r = subprocess.run(['node', GEMINI, 'tts', '--text-file', txt, '--out', wav, '--voice', 'Enceladus',
                                '--model', 'gemini-3.8-flash-tts', '--go'], capture_output=True, text=True, env=env_gemini(), cwd=RAIZ)
            if r.returncode == 0 and os.path.exists(wav): break
            parar_se_sem_credito('Gemini (voz)', r.stdout + r.stderr); esperar_se_limite(r.stdout + r.stderr, tent)
        subprocess.run([sys.executable, '-I', os.path.join(RAIZ, 'ferramentas/limpar-fim-audio.py'), wav, wav + '.mp3'], capture_output=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', wav + '.mp3', '-af', 'afade=t=in:st=0.004:d=0.010,areverse,afade=t=in:d=0.015,areverse',
                        '-ar', '24000', '-ac', '1', wav], check=True); os.remove(wav + '.mp3')
    wavs.append(wav)
PAUSA = 0.55
voz, tempos, t = [], [], 0.0
for w in wavs:
    x, sr = sf.read(w); x = x if x.ndim == 1 else x.mean(1)
    y = subprocess.run(['ffmpeg', '-v', 'error', '-i', w, '-af', f'atempo={VEL},afade=t=in:st=0.004:d=0.010,areverse,afade=t=in:d=0.015,areverse', '-ar', str(SR), '-ac', '1', '-f', 'f32le', '-'],
                       capture_output=True, check=True).stdout
    y = np.frombuffer(y, np.float32).astype(float)
    tempos.append((t, t + len(y) / SR)); voz += [y, np.zeros(int(PAUSA * SR))]; t += len(y) / SR + PAUSA
voz = np.concatenate(voz)
INI = 0.25                                         # quase sem respiro: o gancho é a primeira coisa
total = INI + len(voz) / SR + 1.2
sf.write(P('voz', 'voz.wav'), voz.astype(np.float32), SR)

# ---------- legenda palavra a palavra (Whisper) ----------
mp3 = P('voz', 'voz.mp3')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', P('voz', 'voz.wav'), '-b:a', '48k', mp3], check=True)
r = subprocess.run(['curl', '-sS', 'https://api.openai.com/v1/audio/transcriptions', '-H',
                    f"Authorization: Bearer {os.environ.get('OPENAI_API_KEY', 'sk-proxy')}", '-F', 'model=whisper-1',
                    '-F', f'file=@{mp3}', '-F', 'language=en', '-F', 'response_format=verbose_json',
                    '-F', 'timestamp_granularities[]=word'], capture_output=True, text=True)
d = json.loads(r.stdout)
if 'error' in d: parar_se_sem_credito('OpenAI (Whisper)', json.dumps(d['error'])); sys.exit(d['error'])
palavras = d['words']
blocos, atual = [], []
for w in palavras:
    if atual and w['start'] - atual[-1]['end'] > 0.18:      # pausa = fim de frase: não juntar frases
        blocos.append((atual[0]['start'] + INI, atual[-1]['end'] + INI, ' '.join(x['word'] for x in atual))); atual = []
    atual.append(w)
    txt = ' '.join(x['word'] for x in atual)
    if len(atual) >= 3 or len(txt) >= 16:
        blocos.append((atual[0]['start'] + INI, w['end'] + INI, txt)); atual = []
if atual: blocos.append((atual[0]['start'] + INI, atual[-1]['end'] + INI, ' '.join(x['word'] for x in atual)))
# a legenda some durante o gancho de tela (0–3 s fica só o texto grande? não: os dois convivem, legenda embaixo)
ta = lambda x: f'{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}'
ts = lambda x: f'{int(x//3600):02d}:{int(x%3600//60):02d}:{int(x%60):02d},{int(round(x%1*1000))%1000:03d}'
ass = os.path.join(fin, 'legenda.ass')
g_l = cfg.get('gancho_tela', '').split('|'); c_l = cfg.get('cta_tela', '').split('|')
cta_ini = INI + tempos[-1][0]
with open(ass, 'w', encoding='utf-8') as f:
    f.write(f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Leg,Inter Black,86,&H00FFFFFF,&H00FFFFFF,&H00000000,&HA0000000,0,0,0,0,100,100,0,0,1,6,3,2,90,90,640,1
Style: Gancho,Inter Black,104,&H00FFFFFF,&H00FFFFFF,&H00000000,&HA0000000,0,0,0,0,100,100,0,0,1,7,4,8,70,70,300,1
Style: Cta,Inter Black,96,&H00FFFFFF,&H00FFFFFF,&H00000000,&HA0000000,0,0,0,0,100,100,0,0,1,7,4,5,70,70,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""")
    if g_l[0]:
        f.write(f"Dialogue: 1,{ta(0)},{ta(3.2)},Gancho,,0,0,0,,{{\\fad(0,250)}}{g_l[0]}\\N{{\\c&H1C1CD6&}}{' '.join(g_l[1:])}\n")
    for i, e, txt in blocos:
        if i >= cta_ini and c_l[0]: continue                       # no fim, quem fala é o cartão
        f.write(f"Dialogue: 0,{ta(i)},{ta(max(e, i + 0.35))},Leg,,0,0,0,,{{\\fscx92\\fscy92\\t(0,90,\\fscx100\\fscy100)}}{txt.upper()}\n")
    if c_l[0]:
        f.write(f"Dialogue: 1,{ta(cta_ini)},{ta(total)},Cta,,0,0,0,,{{\\fad(250,0)}}{c_l[0]}\\N{{\\c&H1C1CD6&}}{' '.join(c_l[1:])}\n")
with open(os.path.join(fin, 'legenda.srt'), 'w', encoding='utf-8') as f:
    for n, (i, e, txt) in enumerate(blocos, 1):
        f.write(f'{n}\n{ts(i)} --> {ts(e)}\n{txt}\n\n')

# ---------- imagens por segmento ----------
por_seg = {}
for pl in cfg['planos']: por_seg.setdefault(pl['seg'], []).append(pl)
segs = []
for k, (a0, a1) in enumerate(tempos):
    ini = 0.0 if k == 0 else INI + a0
    fim = total if k == len(tempos) - 1 else INI + tempos[k + 1][0]
    pls = por_seg.get(k)
    if not pls:
        segs[-1] = (segs[-1][0], segs[-1][1], fim); continue
    passo = (fim - ini) / len(pls)
    for j, pl in enumerate(pls): segs.append((pl, ini + j * passo, ini + (j + 1) * passo))
clipes = []
for n, (pl, ini, fim) in enumerate(segs):
    dur = fim - ini + (D if n < len(segs) - 1 else 0)
    fr = int(round(dur * FPS)); Z = 0.10
    z = f'1+{Z}*on/{fr}' if n % 2 == 0 else f'1+{Z}-{Z}*on/{fr}'
    out = os.path.join(fin, 'clipes', f'{n:02d}-{pl["id"]}.mp4')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', P('imagens', pl['id'] + '.png'), '-vf',
                    f"scale=-2:3840,crop=2160:3840,zoompan=z='{z}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d={fr}:s={W}x{H}:fps={FPS},setsar=1",
                    '-frames:v', str(fr), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '14', '-pix_fmt', 'yuv420p', out], check=True)
    clipes.append((out, ini))

# ---------- áudio: voz + drone + sting no "There was a woman…" ----------
N = int((total + 0.5) * SR)
mix = np.zeros((N, 2))
v = np.repeat(voz[:, None], 2, 1); mix[int(INI * SR):int(INI * SR) + len(v)] += v
rms = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
voz_db = rms(voz[voz != 0])
import sfxmix                                    # trilha e efeitos da biblioteca (ElevenLabs)
tc = cfg.get('trilha', {'drone': 'drone-grave-1', 'sting': 'sting-1'})
x = sfxmix.em_loop(sfxmix.carregar(tc['drone']), N); f = int(0.8 * SR); x[:f] *= np.linspace(0, 1, f)[:, None]
sfxmix.colocar(mix, x, 0, voz_db + tc.get('drone_db', -10))
if tc.get('sting'):                              # impacto quando o susto começa (início do 2º segmento)
    sfxmix.colocar(mix, sfxmix.carregar(tc['sting']), INI + tempos[1][0] - 1.2, voz_db + tc.get('sting_db', -4))
sx = cfg.get('sfx', {}); avisos = []
for amb in sx.get('ambientes', []):              # de/ate = segmentos (inclusive)
    a0 = 0.0 if amb['de'] == 0 else INI + tempos[amb['de']][0] - 0.4
    a1 = total if amb['ate'] >= len(tempos) - 1 else INI + tempos[amb['ate'] + 1][0]
    y = sfxmix.em_loop(sfxmix.carregar(amb['id']), int((a1 - a0) * SR)); f = min(int(SR), len(y) // 3)
    y[:f] *= np.linspace(0, 1, f)[:, None]; y[-f:] *= np.linspace(1, 0, f)[:, None]
    sfxmix.colocar(mix, y, a0, voz_db + amb.get('db', -22))
for ef in sx.get('efeitos', []):
    t = sfxmix.tempo_frase(palavras, ef['frase'], ef.get('n', 1), ef.get('fim', False))
    if t is None: avisos.append(ef['frase']); continue
    sfxmix.colocar(mix, sfxmix.carregar(ef['id']), INI + t + ef.get('desloc', 0.0), voz_db + ef.get('db', -10))
if avisos: print('AVISO frases não achadas:', avisos)
sf.write(os.path.join(fin, 'mix.wav'), mix.astype(np.float32), SR)
audio = os.path.join(fin, 'audio.wav')
med = subprocess.run(['ffmpeg', '-v', 'info', '-i', os.path.join(fin, 'mix.wav'), '-af',
                      'highpass=f=30,loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'],
                     capture_output=True, text=True).stderr
j = json.loads(med[med.rindex('{'):med.rindex('}') + 1])
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(fin, 'mix.wav'), '-af',      # 2 passadas, linear: sem "bombear"
                f"highpass=f=30,loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
                f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,"
                f"afade=t=out:st={total-0.8:.2f}:d=0.8", '-ar', '48000', '-t', f'{total:.3f}', audio], check=True)
os.remove(os.path.join(fin, 'mix.wav'))

# ---------- vídeo ----------
fc = [f"[{k}:v]fps={FPS},settb=1/{FPS},setpts=PTS-STARTPTS,format=yuv420p[n{k}]" for k in range(len(clipes))]
prev = '[n0]'
for k in range(1, len(clipes)):
    fc.append(f"{prev}[n{k}]xfade=transition=fade:duration={D}:offset={clipes[k][1]:.3f}[x{k}]"); prev = f'[x{k}]'
fc.append(f"{prev}eq=saturation=0.75:contrast=0.97:brightness=-0.02,colorbalance=bs=0.04:bm=0.02:rh=-0.02,"
          f"vignette=angle=PI/4.5,noise=alls=4:allf=t,subtitles={ass}:fontsdir=/usr/share/fonts/opentype/inter,format=yuv420p[v]")
cmd = ['ffmpeg', '-v', 'error', '-y']
for c, _ in clipes: cmd += ['-i', c]
cmd += ['-i', audio, '-filter_complex', ';'.join(fc), '-map', '[v]', '-map', f'{len(clipes)}:a', '-c:v', 'libx264',
        '-preset', 'medium', '-crf', '20', '-maxrate', '10M', '-bufsize', '20M', '-c:a', 'aac', '-b:a', '192k',
        '-t', f'{total:.3f}', '-movflags', '+faststart', os.path.join(fin, 'short.mp4')]
r = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
if r.returncode: sys.exit(r.stderr[-1500:])
print(f'ok: {os.path.join(fin, "short.mp4")} · {total:.1f} s')
