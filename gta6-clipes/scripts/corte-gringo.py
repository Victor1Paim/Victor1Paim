#!/usr/bin/env python3
"""Corte de live/VOD gringo (Twitch) com legenda TRADUZIDA para português, no layout do Modo Replay.

Uso: corte-gringo.py <url_vod> <inicio H:MM:SS> <fim H:MM:SS> <nome> "<o que acontece (pt)>" <canal>
Saída: gta6-clipes/pacote-postagens/gringos/<nome>/ com video.mp4, capa.jpg, legendas.txt, decisao.json

Passos: baixa só o trecho (yt-dlp) → Whisper (inglês, tempo por frase) → gpt-5.4 traduz cada frase (censura palavrões,
remove insultos) e escreve gancho + legendas das redes → base 9:16 com reflexo → Remotion (modelo/) → capa (vigia/capa.js).
"""
import json, os, subprocess, sys, urllib.request

url, ini_h, fim_h, nome, contexto, canal = sys.argv[1:7]
LONGA = sys.argv[7] if len(sys.argv) > 7 else None   # transcrição longa do VOD (json com t, f, x em segundos do VOD)
RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MODELO = os.path.join(RAIZ, 'modelo')
PASTA = os.path.join(RAIZ, 'pacote-postagens', 'gringos', nome)
os.makedirs(PASTA, exist_ok=True)
seg = lambda h: sum(int(x) * m for x, m in zip(h.split(':'), [3600, 60, 1]))
ini, fim = seg(ini_h), seg(fim_h)
dur_fala = fim - ini


def log(*a):
    print(f'[{nome}]', *a, flush=True)


def openai_json(prompt, modelo='gpt-5.4'):
    req = urllib.request.Request('https://api.openai.com/v1/chat/completions',
        data=json.dumps({'model': modelo, 'messages': [{'role': 'user', 'content': prompt}], 'response_format': {'type': 'json_object'}}).encode(),
        headers={'Content-Type': 'application/json', 'Authorization': 'Bearer sk-proxy'})
    return json.loads(json.load(urllib.request.urlopen(req, timeout=300))['choices'][0]['message']['content'])


# 1) trecho do VOD (com 3 s de margem para a tela final)
bruto = os.path.join(PASTA, 'bruto.mp4')
if not os.path.exists(bruto) and os.path.exists(url):   # gravação local (streamlink): recorta direto
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(ini), '-t', str(fim - ini + 3), '-i', url, '-c:v', 'libx264', '-preset', 'veryfast',
                    '-crf', '18', '-c:a', 'aac', '-b:a', '192k', bruto], check=True)
if not os.path.exists(bruto):
    subprocess.run(['yt-dlp', '-q', '--no-warnings', '-f', '720p60/720p/best[height<=720]', '--download-sections',
                    f'*{ini}-{fim + 3}', '--force-keyframes-at-cuts', '-o', bruto, url], check=True)
log('trecho baixado')

# 2) transcrição (frases com tempo)
audio = os.path.join(PASTA, 'audio.mp3')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', bruto, '-vn', '-ac', '1', '-ar', '16000', '-b:a', '64k', audio], check=True)
r = subprocess.run(['curl', '-s', '-m', '300', 'https://api.openai.com/v1/audio/transcriptions', '-H', 'Authorization: Bearer sk-proxy',
                    '-F', f'file=@{audio}', '-F', 'model=whisper-1', '-F', 'language=en', '-F', 'response_format=verbose_json',
                    '-F', f'prompt={canal} streaming GTA 6: Lucia, Jason, Vice City, Leonida.'], capture_output=True, text=True)
tr = json.loads(r.stdout)
frases, ant = [], None
for s in tr['segments']:
    x = s['text'].strip()
    if s['start'] >= dur_fala or s.get('no_speech_prob', 0) > 0.6 or s.get('compression_ratio', 0) > 2.4 or x == ant:
        ant = x; continue
    ant = x
    frases.append({'i': round(s['start'], 2), 'f': round(min(s['end'], dur_fala), 2), 'en': x})
# o Whisper às vezes pula 30-60 s com música alta: usa a transcrição longa do VOD e completa os buracos com a do recorte
if LONGA:
    longa = [{'i': round(x['t'] - ini, 2), 'f': round(min(x['f'], fim) - ini, 2), 'en': x['x']} for x in json.load(open(LONGA)) if ini - 1 <= x['t'] < fim]
    cobre = lambda t: any(l['i'] - 1 <= t <= l['f'] + 1 for l in longa)
    frases = sorted(longa + [f for f in frases if not cobre((f['i'] + f['f']) / 2)], key=lambda f: f['i'])
    frases = [f for f in frases if f['f'] > max(f['i'], 0)]
    norm = lambda x: ''.join(c for c in x.lower() if c.isalnum())
    unicas = []
    for f in frases:   # a mesma fala nas duas transcrições, com horário um pouco diferente
        if any(abs(u['i'] - f['i']) < 8 and (norm(u['en']) in norm(f['en']) or norm(f['en']) in norm(u['en'])) for u in unicas):
            continue
        unicas.append(f)
    frases = unicas
log(len(frases), 'frases')

# 3) tradução + gancho + legendas
pedido = {
    'contexto': contexto, 'canal': canal,
    'frases': [{'n': k, 'en': f['en']} for k, f in enumerate(frases)],
}
dec = openai_json(f"""Você legenda cortes do streamer {canal} jogando GTA 6 para o canal brasileiro "Modo Replay".
Contexto do corte: {contexto}
Traduza CADA frase para português do Brasil falado, curta e natural (gírias ok). Regras: palavrões viram versão censurada
com asterisco (ex.: "p*rra", "c*ralho", "f*da"); insultos raciais/homofóbicos são REMOVIDOS ou trocados por "mano"/"cara";
falas do jogo (personagens) também são traduzidas. Não junte nem omita frases: uma tradução por "n".
Também escreva:
- "gancho": 2 linhas em MAIÚSCULAS de até 16 letras cada, chamativas, sem copiar a fala (ex.: ["GTA 6 TEM", "BEBÊ?!"]);
- "destaque": UMA palavra do gancho para ir em amarelo;
- "titulo_faixa": UMA frase em MAIÚSCULAS de 25 a 45 caracteres que conta o que acontece, estilo manchete de corte (ex.: "SPEED VIU O BEBÊ E ENTROU EM PÂNICO");
- "destaques": 4 a 6 palavras-chave das traduções;
- "tiktok": legenda TikTok/Reels em pt com 1-2 emojis, pergunta para comentar, e hashtags #gta6 #{canal.lower()} #gta6brasil #cortes;
- "shorts_titulo": até 60 caracteres com #gta6 #shorts;
- "instagram": 2-3 linhas em pt + hashtags (#gta6 #{canal.lower()} #gta6brasil #cortes).
Responda SOMENTE JSON: {{"traducoes":[{{"n":0,"pt":"..."}}], "gancho":[...], "destaque":"...", "destaques":[...], "tiktok":"...", "shorts_titulo":"...", "instagram":"..."}}

FRASES: {json.dumps(pedido['frases'], ensure_ascii=False)}""")
pt = {t['n']: t['pt'] for t in dec['traducoes']}
legendas = [{'inicio': f['i'], 'fim': f['f'], 'texto': pt.get(k, '').strip()} for k, f in enumerate(frases) if pt.get(k, '').strip()]
json.dump({'frases': frases, **dec}, open(os.path.join(PASTA, 'decisao.json'), 'w'), ensure_ascii=False, indent=1)
log('traduzido; gancho:', dec['gancho'])

# 4) base 9:16: estilo "faixa" (FAIXA=camx,camy,camw,camh,gx,gy,gw,gh na resolução da fonte) ou reflexo
FAIXA = os.environ.get('FAIXA')
dur = dur_fala + 2.6
base_nome = f'gringo-{nome}.mp4'
base = os.path.join(MODELO, 'public', base_nome)
reflexo = ('split=3[c][a][b];[a]vflip,scale=270:-2,boxblur=8:2,scale=1080:656,eq=brightness=-0.28:saturation=1.1[t];'
           '[b]vflip,scale=270:-2,boxblur=8:2,scale=1080:656,eq=brightness=-0.28:saturation=1.1[bo];[t][c][bo]vstack=3,format=yuv420p[v]')
if FAIXA:
    cx, cy, cw, ch, gx, gy, gw, gh = FAIXA.split(',')
    filtro = (f'[0:v]split[a][b];[a]crop={cw}:{ch}:{cx}:{cy},scale=1080:660,setsar=1[cam];[b]crop={gw}:{gh}:{gx}:{gy},scale=1080:972,setsar=1[jogo];'
              'color=black:s=1080x288:r=60[preto];[cam][preto][jogo]vstack=3:shortest=1,format=yuv420p[v]')
else:
    filtro = '[0:v]scale=1080:608,setsar=1,' + reflexo
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', bruto, '-t', f'{dur:.2f}', '-filter_complex', filtro,
                '-map', '[v]', '-map', '0:a', '-af', 'apad', '-t', f'{dur:.2f}', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18',
                '-c:a', 'aac', '-b:a', '192k', base], check=True)

# 5) render
props = {'dados': {'video': base_nome, 'duracao': round(dur - 0.05, 2), 'gancho': dec['gancho'], 'destaque': dec.get('destaque', ''),
                   'cabecalho': f'GTA 6 · {canal}', 'selo': 'DIA 1', 'credito': f'{canal} (Twitch) · tradução Modo Replay', 'canal': 'Modo Replay',
                   'chamadaFinal': 'Segue pra ver o GTA 6 legendado', 'inicioFinal': round(dur_fala + 0.2, 2), 'legendas': legendas,
                   'destaques': dec.get('destaques', []), 'layout': {'topo': 656, 'altura': 608}}}
if FAIXA:
    props['dados'].update({'estilo': 'faixa', 'faixa': {'topo': 610, 'titulo': dec.get('titulo_faixa') or ' '.join(dec['gancho'])}})
arq = os.path.join(PASTA, 'props.json')
json.dump(props, open(arq, 'w'), ensure_ascii=False)
tmp = os.path.join(PASTA, 'render.mp4')
subprocess.run(['npx', 'remotion', 'render', 'src/index.ts', 'Corte', tmp, f'--props={arq}', '--concurrency=4', '--log=error'], cwd=MODELO, check=True)
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', tmp, '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', '-c:a', 'aac', '-b:a', '160k',
                '-movflags', '+faststart', os.path.join(PASTA, 'video.mp4')], check=True)
os.remove(tmp)
if FAIXA:   # capa no mesmo estilo: quadro do próprio vídeo, manchete maior
    props['dados']['capa'] = True
    json.dump(props, open(arq, 'w'), ensure_ascii=False)
    subprocess.run(['npx', 'remotion', 'still', 'src/index.ts', 'Corte', os.path.join(PASTA, 'capa.jpg'), f'--props={arq}',
                    f'--frame={int(dur_fala * 0.4 * 30)}', '--jpeg-quality=92', '--log=error'], cwd=MODELO, check=True)
os.remove(base)

# 6) capa + legendas das redes
quadro = os.path.join(PASTA, 'quadro.jpg')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', f'{dur_fala * 0.5:.2f}', '-i', bruto, '-frames:v', '1',
                '-vf', 'crop=ih*9/16:ih,scale=1080:1920:flags=lanczos', quadro], check=True)
if not FAIXA:
  subprocess.run(['node', os.path.join(RAIZ, 'vigia', 'capa.js'), quadro, json.dumps(dec['gancho']), dec.get('destaque', ''),
                f'🎮 {canal.upper()} · GTA 6', os.path.join(PASTA, 'capa.jpg')], check=True)
credito = f'📺 Créditos: {canal} (Twitch) — https://www.twitch.tv/{canal.lower()}'
open(os.path.join(PASTA, 'legendas.txt'), 'w').write(
    f"=== TIKTOK / REELS ===\n{dec['tiktok']}\n{credito}\n\n=== SHORTS ===\nTítulo: {dec['shorts_titulo']}\nDescrição: {contexto}\n{credito}\n\n"
    f"=== INSTAGRAM ===\n{dec['instagram']}\n{credito}\n")
for f in (audio, quadro):
    os.remove(f)
log('PRONTO', PASTA)
