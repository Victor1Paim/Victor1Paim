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
def _ler(l):
    try: return json.loads(l)
    except Exception: return None  # linha cortada (ex.: disco cheio) não derruba a análise
chat = [c for c in map(_ler, open('chat.jsonl')) if c]
mmss = lambda s: f'{int(s // 60)}:{int(s % 60):02d}'

# --- métricas de fala por bloco de 10 s (para escolher e para buscar depois) ---
import re, numpy as np
pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', 'live.mp4', '-vn', '-ac', '1', '-ar', '8000', '-f', 's16le', '-'], capture_output=True).stdout
amost = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
rms = lambda a, b: float(np.sqrt(np.mean(amost[int(a * 8000):int(b * 8000)] ** 2) + 1e-12))
base = np.median([rms(b, b + 10) for b in range(0, int(dur), 10)]) or 1e-6
# Gatilhos revisados pela pesquisa (Manus, 2026). Termos ambíguos sozinhos ("no way", "what", "novo", "GG", "F",
# "meta", "safe", "chat") ficam de fora: palavra-gatilho é sinal fraco e só conta junto com outro indício.
GATILHOS = {
    'ensinamento': r'\b(dica|macete|o segredo é|faz assim|presta atenção|tutorial|como (que )?(faz|se faz|eu faço)|truque|aprend|ensin|pro tip|here\'?s how|the trick is|let me explain|you (gotta|have to))\b',
    'curiosidade': r'\b(sabia que|você sabia|olha isso|detalhe|easter ?egg|lore|segredo|nunca vi|reparou|percebeu|referência|did you know|look at this|fun fact|i just found out|wait,? what)\b',
    'novidade': r'\b(descobri|primeira vez|não sabia|nao sabia|dá pra|da pra|tem como|chegou|lançou|atualização|skin nova|just dropped|brand new|first time|you can)\b',
    'humor': r'(k{3,}|ha(ha)+|rs(rs)+|\blol\b|lmao|\bkekw\b|não tankei|nao tankei|tá de sacanagem|ta de sacanagem|trollou|that\'?s hilarious|i\'?m dead|bruh)',
    'susto': r'\b(meu deus|caraca|eita|que susto|do nada|não esperava|nao esperava|mano do céu|jump ?scare|i didn\'?t expect|oh my god|holy)\b',
    'polemica': r'\b(discordo|nada a ver|polêmic|treta|opinião impopular|isso é roubado|quebrado|tiltou|hot take|bad take|controversial|that\'?s not true|cooked|crash(ed)? out)\b',
    'opiniao': r'\b(achei|acho que|horrível|incrível|absurdo|gráfico|grafico|best|worst|insane|graphics)\b',
}
PERGUNTA_CHAT = r'\b(chat|vocês|voces|o que (vocês )?acham|y\'?all|what do you think)\b'
EMOTES = r'(kekw|omegalul|\blul\b|lulw|pog(champ|gers|u)?|monkas|pepelaugh|kappa|icant|aware|k{4,}|😂|🤣|💀)'

pal_s = []  # palavras por minuto de cada bloco, para comparar com a linha de base do próprio streamer
blocos = []
for b in range(0, int(dur), 10):
    fala = ' '.join(s['x'] for s in segs if b <= s['t'] < b + 10)
    msgs = [c['m'] for c in chat if b <= c['t'] - t0 < b + 10]
    baixo = [m.lower() for m in msgs]
    pal = len(fala.split())
    # silêncio/baixa energia nos 3 s antes de um pico (suspense → explosão)
    antes = rms(max(0, b - 3), b) / base if b >= 3 else 1
    blocos.append({'t': b, 'tempo': mmss(b), 'fala': fala, 'palavras_min': pal * 6, 'exclamacoes': fala.count('!') + fala.count('?'),
                   'volume': round(rms(b, b + 10) / base, 2), 'silencio_antes': bool(antes < .5), 'chat': len(msgs),
                   'emotes': sum(len(re.findall(EMOTES, m)) for m in baixo),
                   'repeticao': round(1 - len(set(baixo)) / len(baixo), 2) if len(baixo) > 3 else 0,
                   'pergunta_chat': bool(re.search(PERGUNTA_CHAT, fala.lower())),
                   'gatilhos': [k for k, rx in GATILHOS.items() if re.search(rx, fala.lower())], 'amostra_chat': msgs[:6]})

# nota de sinais 0-100 por bloco, normalizada por percentis (p5-p95) da própria live, pesos iniciais da pesquisa:
# volume 12, chat/s 20, emotes 10, repetição 7, velocidade 7, silêncio antes de pico 5, gatilhos 5, pergunta ao chat 3.
def pct(chave):
    v = np.array([x[chave] for x in blocos], float)
    lo, hi = np.percentile(v, 5), np.percentile(v, 95)
    return np.clip((v - lo) / (hi - lo + 1e-9), 0, 1)
ppm = np.array([x['palavras_min'] for x in blocos], float)
vel = np.clip(np.abs(ppm - np.median(ppm)) / (np.percentile(ppm, 95) - np.median(ppm) + 1e-9), 0, 1)
comp = {'volume': (12, pct('volume')), 'chat': (20, pct('chat')), 'emotes': (10, pct('emotes')), 'repeticao': (7, pct('repeticao')),
        'velocidade': (7, vel)}
tot = sum(p for p, _ in comp.values()) + 5 + 5 + 3
for i, x in enumerate(blocos):
    n = sum(p * v[i] for p, v in comp.values())
    n += 5 * (x['silencio_antes'] and comp['volume'][1][i] > .7)
    # gatilho só conta junto com outro indício (emoção na voz, chat ou emote)
    n += 5 * (bool(x['gatilhos']) and (comp['volume'][1][i] > .5 or comp['chat'][1][i] > .5 or x['emotes'] > 0))
    n += 3 * x['pergunta_chat']
    x['sinais'] = round(100 * n / tot)

linhas = [f"[{x['tempo']}] sinais={x['sinais']} chat={x['chat']} emotes={x['emotes']} vol={x['volume']} ppm={x['palavras_min']} tags={','.join(x['gatilhos']) or '-'} | {x['fala']} " + (f"|| chat: {' / '.join(x['amostra_chat'])}" if x['amostra_chat'] else '')
          for x in blocos if x['fala'] or x['chat'] > 5]
open('roteiro.txt', 'w').write('\n'.join(linhas))

def gpt(prompt):
    r = urllib.request.Request('https://api.openai.com/v1/chat/completions', json.dumps({'model': 'gpt-5.4', 'response_format': {'type': 'json_object'}, 'messages': [{'role': 'user', 'content': prompt}]}).encode(), {'Content-Type': 'application/json', 'Authorization': 'Bearer sk-proxy'})
    return json.loads(json.load(urllib.request.urlopen(r, timeout=900))['choices'][0]['message']['content'])

# --- índice pesquisável: um resumo por minuto com categoria e tags ---
indice = gpt(f"""Abaixo, o roteiro de uma live de GTA 6 em blocos de 10 s ([mm:ss] sinais = nota 0-100 de áudio+chat, chat = mensagens, emotes, vol = volume relativo à mediana, ppm = palavras por minuto, tags = gatilhos detectados | fala). Contexto: {contexto}
Divida a live em trechos de ~1 min (ajuste aos assuntos) e, para cada trecho, devolva: inicio, fim (mm:ss), resumo (1 frase em pt), categoria (uma de: reacao, humor, susto, fail, ensinamento, curiosidade, novidade_do_jogo, historia, polemica, opiniao, gameplay_comum), tags (3-6 palavras-chave em pt para busca: missões, personagens, lugares, mecânicas, veículos, emoções), forca (0-10, quanto renderia um corte).
Responda JSON: {{"trechos":[...]}}

{open('roteiro.txt').read()}""")
meta = {'pasta': os.getcwd(), 'contexto': contexto, 'idioma': idioma, 'duracao_s': round(dur), 'offset_vod_s': float(open('offset.txt').read()) if os.path.exists('offset.txt') else 0}
json.dump({'meta': meta, 'trechos': indice.get('trechos', []), 'blocos': blocos}, open('indice.json', 'w'), ensure_ascii=False, indent=1)

cand = gpt(f"""Você escolhe cortes (50 s a 1 min 30) de uma live de GTA 6 para TikTok/Reels/Shorts. Contexto: {contexto}
Não escolha só por volume ou pico de chat. Vale tanto quanto uma reação forte:
- ENSINAMENTO: dica, macete, como fazer algo no jogo que o público vai querer saber;
- CURIOSIDADE: detalhe escondido, referência, easter egg, coisa que surpreende quem não jogou;
- NOVIDADE DO JOGO: mecânica, sistema, recurso que o streamer descobre ao vivo;
- HUMOR / SUSTO / FAIL / REAÇÃO / HISTÓRIA: momento que se entende sozinho e tem desfecho.
Pontue cada candidato de 0 a 100 em cada dimensão e calcule
nota = 0,15·P + 0,18·D + 0,10·R + 0,15·N + 0,06·V + 0,12·U + 0,12·C + 0,12·(100 − K), onde
P = picos de áudio/chat ligados ao conteúdo (use a coluna sinais; pico sem relação com a cena não vale);
D = densidade informativa (informação útil por segundo, sem enrolação);
R = reação espontânea e inteligível (riso, surpresa, emoção);
N = estrutura narrativa: contexto mínimo, desenvolvimento e desfecho, entende-se sozinho;
V = novidade em relação ao que o público já viu do jogo;
U = utilidade ou entretenimento claro para quem joga ou vai jogar;
C = clareza: fala inteligível, sem referência a algo fora do trecho;
K = risco: exposição de terceiros, conteúdo sensível, fala tirada de contexto, afirmação falsa.
Abra no acontecimento ou na promessa (sem saudação ou espera), dê só o contexto mínimo e termine logo após o desfecho; não sobreponha cortes; equilibre os tipos quando houver opção. Vete (não escolha) trecho com K > 70.
Índice da live por minuto: {json.dumps(indice.get('trechos', []), ensure_ascii=False)}
Escolha os {n} melhores. Responda JSON: {{"cortes":[{{"inicio":"mm:ss","fim":"mm:ss","tipo":"ensinamento|curiosidade|novidade_do_jogo|humor|susto|fail|reacao|historia","titulo":"até 5 palavras, fiel ao que acontece","gancho":"o que aparece/é dito nos 3 primeiros segundos","dimensoes":{{"P":0,"D":0,"R":0,"N":0,"V":0,"U":0,"C":0,"K":0}},"nota":0-100,"por_que":"..."}}]}} ordenado da maior nota para a menor.

{open('roteiro.txt').read()}""")
json.dump(cand, open('candidatos.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(cand, ensure_ascii=False, indent=1))
