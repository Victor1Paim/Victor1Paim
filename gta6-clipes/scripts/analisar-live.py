#!/usr/bin/env python3
"""Analisa uma gravação de live: remux, transcrição (Whisper em partes), roteiro com chat a cada 10 s e candidatos a corte (gpt-5.4).
Uso: analisar-live.py <pasta com live.ts, chat.jsonl, inicio.txt> <n_cortes> "<contexto>" [idioma=pt]
Gera na pasta: live.mp4, transcricao.json [{t,f,x}], roteiro.txt, candidatos.json."""
import sys, os, json, subprocess, glob, urllib.request

pasta, n, contexto = sys.argv[1], int(sys.argv[2]), sys.argv[3]
idioma = sys.argv[4] if len(sys.argv) > 4 else 'pt'
os.chdir(pasta)
run = lambda *a: subprocess.run(a, check=True, capture_output=True)

if not os.path.exists('live.mp4'):
    run('ffmpeg', '-y', '-fflags', '+genpts+igndts', '-i', 'live.ts', '-c', 'copy', '-avoid_negative_ts', 'make_zero', 'live.mp4')
dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', 'live.mp4']))

os.makedirs('partes', exist_ok=True)
PARTE = 300
def whisper(mp3):
    bound = 'xBoundx'
    corpo = b''
    for k, v in [('model', 'whisper-1'), ('response_format', 'verbose_json'), ('language', idioma), ('timestamp_granularities[]', 'segment')]:
        corpo += f'--{bound}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
    corpo += f'--{bound}\r\nContent-Disposition: form-data; name="file"; filename="a.mp3"\r\nContent-Type: audio/mpeg\r\n\r\n'.encode() + open(mp3, 'rb').read() + f'\r\n--{bound}--\r\n'.encode()
    r = urllib.request.Request('https://api.openai.com/v1/audio/transcriptions', corpo, {'Content-Type': f'multipart/form-data; boundary={bound}', 'Authorization': 'Bearer sk-proxy'})
    return json.load(urllib.request.urlopen(r, timeout=600))

segs = []
for k in range(int(dur // PARTE) + 1):
    ini = k * PARTE
    if dur - ini < 3: break
    mp3, js = f'partes/p{k:02d}.mp3', f'partes/p{k:02d}.json'
    if not os.path.exists(js):
        run('ffmpeg', '-y', '-ss', str(ini), '-t', str(PARTE), '-i', 'live.mp4', '-vn', '-ac', '1', '-ar', '16000', '-b:a', '64k', mp3)
        json.dump(whisper(mp3), open(js, 'w'), ensure_ascii=False)
    ant = None
    for s in json.load(open(js)).get('segments', []):
        x = s['text'].strip()
        if not x or s.get('no_speech_prob', 0) > .6 or s.get('avg_logprob', 0) < -1 or s.get('compression_ratio', 0) > 2.4 or x == ant: continue
        ant = x
        segs.append({'t': round(ini + s['start'], 2), 'f': round(ini + s['end'], 2), 'x': x})
json.dump(segs, open('transcricao.json', 'w'), ensure_ascii=False, indent=0)

t0 = float(open('inicio.txt').read())
chat = [json.loads(l) for l in open('chat.jsonl') if l.strip()]
mmss = lambda s: f'{int(s // 60)}:{int(s % 60):02d}'

# --- métricas de fala por bloco de 10 s (para escolher e para buscar depois) ---
import re, numpy as np
pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', 'live.mp4', '-vn', '-ac', '1', '-ar', '8000', '-f', 's16le', '-'], capture_output=True).stdout
amost = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
rms = lambda a, b: float(np.sqrt(np.mean(amost[int(a * 8000):int(b * 8000)] ** 2) + 1e-12))
base = np.median([rms(b, b + 10) for b in range(0, int(dur), 10)]) or 1e-6
GATILHOS = {
    'ensinamento': r'\b(dica|tutorial|como (que )?(faz|se faz|eu faço)|tem que|aprend|ensin|truque|macete|segredo|tip|how to|you gotta|you have to|trick)\b',
    'curiosidade': r'\b(sabia|curios|detalhe|reparou|percebeu|olha isso|easter|referência|referencia|did you know|look at this|detail|notice)\b',
    'novidade': r'\b(descobri|novo|nova|primeira vez|não sabia|nao sabia|dá pra|da pra|tem como|new|first time|you can)\b',
    'humor': r'(k{3,}|ha(ha)+|rs(rs)+|lol|lmao|\bri(r|s)o\b|engraçad|funny)',
    'susto': r'\b(meu deus|caralho|puta|nossa|mano do céu|what the|oh my god|bro what|no way|what)\b',
    'opiniao': r'\b(achei|acho que|melhor|pior|horrível|incrível|lindo|absurdo|gráfico|grafico|best|worst|crazy|insane|graphics)\b',
}
blocos = []
for b in range(0, int(dur), 10):
    fala = ' '.join(s['x'] for s in segs if b <= s['t'] < b + 10)
    msgs = [c['m'] for c in chat if b <= c['t'] - t0 < b + 10]
    pal = len(fala.split())
    blocos.append({'t': b, 'tempo': mmss(b), 'fala': fala, 'palavras_min': pal * 6, 'exclamacoes': fala.count('!') + fala.count('?'),
                   'volume': round(rms(b, b + 10) / base, 2), 'chat': len(msgs),
                   'gatilhos': [k for k, rx in GATILHOS.items() if re.search(rx, fala.lower())], 'amostra_chat': msgs[:6]})
linhas = [f"[{x['tempo']}] chat={x['chat']} vol={x['volume']} ppm={x['palavras_min']} tags={','.join(x['gatilhos']) or '-'} | {x['fala']} " + (f"|| chat: {' / '.join(x['amostra_chat'])}" if x['amostra_chat'] else '')
          for x in blocos if x['fala'] or x['chat'] > 5]
open('roteiro.txt', 'w').write('\n'.join(linhas))

def gpt(prompt):
    r = urllib.request.Request('https://api.openai.com/v1/chat/completions', json.dumps({'model': 'gpt-5.4', 'response_format': {'type': 'json_object'}, 'messages': [{'role': 'user', 'content': prompt}]}).encode(), {'Content-Type': 'application/json', 'Authorization': 'Bearer sk-proxy'})
    return json.loads(json.load(urllib.request.urlopen(r, timeout=900))['choices'][0]['message']['content'])

# --- índice pesquisável: um resumo por minuto com categoria e tags ---
indice = gpt(f"""Abaixo, o roteiro de uma live de GTA 6 em blocos de 10 s ([mm:ss] chat, vol = volume relativo à mediana, ppm = palavras por minuto, tags = gatilhos detectados | fala). Contexto: {contexto}
Divida a live em trechos de ~1 min (ajuste aos assuntos) e, para cada trecho, devolva: inicio, fim (mm:ss), resumo (1 frase em pt), categoria (uma de: reacao, humor, ensinamento, curiosidade, novidade_do_jogo, historia, opiniao, gameplay_comum), tags (3-6 palavras-chave em pt para busca: missões, personagens, lugares, mecânicas, veículos, emoções), forca (0-10, quanto renderia um corte).
Responda JSON: {{"trechos":[...]}}

{open('roteiro.txt').read()}""")
meta = {'pasta': os.getcwd(), 'contexto': contexto, 'idioma': idioma, 'duracao_s': round(dur), 'offset_vod_s': float(open('offset.txt').read()) if os.path.exists('offset.txt') else 0}
json.dump({'meta': meta, 'trechos': indice.get('trechos', []), 'blocos': blocos}, open('indice.json', 'w'), ensure_ascii=False, indent=1)

cand = gpt(f"""Você escolhe cortes (50 s a 1 min 30) de uma live de GTA 6 para TikTok/Reels/Shorts. Contexto: {contexto}
Não escolha só por volume ou pico de chat. Vale tanto quanto uma reação forte:
- ENSINAMENTO: dica, macete, como fazer algo no jogo que o público vai querer saber;
- CURIOSIDADE: detalhe escondido, referência, easter egg, coisa que surpreende quem não jogou;
- NOVIDADE DO JOGO: mecânica, sistema, recurso que o streamer descobre ao vivo;
- HUMOR / REAÇÃO / HISTÓRIA: momento que se entende sozinho e tem desfecho.
Use as métricas (vol, ppm, chat, tags) só como pistas. O corte precisa se entender sem o resto da live; comece um pouco antes do gatilho e termine logo após o desfecho; não sobreponha cortes; equilibre os tipos quando houver opção.
Índice da live por minuto: {json.dumps(indice.get('trechos', []), ensure_ascii=False)}
Escolha os {n} melhores. Responda JSON: {{"cortes":[{{"inicio":"mm:ss","fim":"mm:ss","tipo":"ensinamento|curiosidade|novidade_do_jogo|humor|reacao|historia","titulo":"...","por_que":"...","nota":0-10}}]}} ordenado da maior nota para a menor.

{open('roteiro.txt').read()}""")
json.dump(cand, open('candidatos.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(cand, ensure_ascii=False, indent=1))
