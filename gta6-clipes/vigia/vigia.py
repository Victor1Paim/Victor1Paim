#!/usr/bin/env python3
"""Vigia de live (Twitch) do Modo Replay: grava a live e o chat, detecta momentos fortes e entrega cortes prontos.

Uso: python3 vigia.py <canal> [--teste]
  --teste   limiares mais baixos (para testar em qualquer live)

Para cada momento detectado gera em gta6-clipes/vigia/saida/<canal>/<AAAAMMDD-HHMMSS>/:
  video.mp4 (1080x1920, legenda, logo, reflexo) · capa.jpg · legendas.txt · decisao.json
e escreve no log a linha  NOVO_CORTE <pasta>  (é o que acorda o Claude para enviar no chat).

Peças: streamlink (vídeo) · WebSocket do chat da Twitch (porta 443) · Whisper (OpenAI) · gpt-5.4-mini (decisão)
· Remotion (modelo/) · Playwright (capa). As chaves de API vêm do proxy do ambiente.
"""
import asyncio, collections, glob, json, os, re, shutil, ssl, statistics, subprocess, sys, threading, time, urllib.request, queue
from datetime import datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
MODELO = os.path.join(RAIZ, 'modelo')
CANAL = sys.argv[1].lower()
TESTE = '--teste' in sys.argv
TRAB = os.path.join(AQUI, 'trabalho', CANAL)
SEG = os.path.join(TRAB, 'segmentos')
SAIDA = os.path.join(AQUI, 'saida', CANAL)
for d in (SEG, SAIDA):
    os.makedirs(d, exist_ok=True)

# ---------- ajustes ----------
SEG_DUR = 20                 # segundos por segmento gravado
GUARDAR_MIN = 25             # minutos de gravação mantidos
ANTES, DEPOIS = 100, 35      # janela em volta do pico (s)
ESPERA_CAPTURA = DEPOIS + 15 # espera após o pico antes de cortar
RECARGA = 120 if TESTE else 180   # intervalo mínimo entre momentos (s)
AQUECIMENTO = 180 if TESTE else 300
MULT, MIN_ABS = (1.8, 3) if TESTE else (2.6, 10)
NOTA_MIN = 5 if TESTE else 7
REACOES = re.compile(r'(k{4,}|kek|lul|omegalul|pog|wtf|caralho|mds|meu deus|clipa|clip|socorro|kkkk|😂|🤣|😱|💀|omg|monka)', re.I)
CENSURA = {'porra': 'p*rra', 'caralho': 'c*ralho', 'merda': 'm*rda', 'foda': 'f*da', 'fodase': 'f*dase', 'puta': 'p*ta', 'cu': 'c*'}


def log(*a):
    print(datetime.now().strftime('%H:%M:%S'), f'[{CANAL}]', *a, flush=True)


# ---------- 1) gravação contínua ----------
def gravar():
    while True:
        log('gravação: conectando')
        sl = subprocess.Popen(['streamlink', '--twitch-disable-ads', '--twitch-low-latency', '-O',
                               f'https://www.twitch.tv/{CANAL}', '720p60,720p,best'],
                              stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        ff = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', 'pipe:0', '-map', '0:v:0', '-map', '0:a:0', '-c', 'copy',
                               '-f', 'segment', '-segment_time', str(SEG_DUR), '-reset_timestamps', '1', '-strftime', '1',
                               os.path.join(SEG, '%s.ts')], stdin=sl.stdout)
        ff.wait(); sl.kill()
        log('gravação: live encerrada ou caiu; tentando de novo em 30 s')
        time.sleep(30)


def limpar_segmentos():
    limite = time.time() - GUARDAR_MIN * 60
    for f in glob.glob(os.path.join(SEG, '*.ts')):
        if int(os.path.basename(f)[:-3]) < limite:
            os.remove(f)


# ---------- 2) chat ao vivo ----------
chat = collections.deque(maxlen=200000)   # (epoch, autor, texto)


async def ler_chat():
    import websockets
    ctx = ssl.create_default_context(cafile=os.environ.get('SSL_CERT_FILE', '/root/.ccr/ca-bundle.crt'))
    while True:
        try:
            async with websockets.connect('wss://irc-ws.chat.twitch.tv:443', ssl=ctx, ping_interval=60) as ws:
                for c in ['CAP REQ :twitch.tv/tags', 'PASS SCHMOOPIIE', f'NICK justinfan{int(time.time()) % 90000 + 1000}', f'JOIN #{CANAL}']:
                    await ws.send(c)
                log('chat: conectado')
                async for raw in ws:
                    for linha in raw.split('\r\n'):
                        if linha.startswith('PING'):
                            await ws.send('PONG :tmi.twitch.tv'); continue
                        m = re.search(r'display-name=([^;]*).* PRIVMSG #\w+ :(.*)', linha)
                        if m:
                            chat.append((time.time(), m.group(1), m.group(2)))
        except Exception as e:
            log('chat: caiu', e); await asyncio.sleep(10)


# ---------- 3) detector ----------
def taxa(t_ini, t_fim):
    return sum(1 for t, _, _ in chat if t_ini <= t < t_fim)


def reacoes(t_ini, t_fim):
    return sum(1 for t, _, x in chat if t_ini <= t < t_fim and REACOES.search(x))


fila = queue.Queue()


async def detectar():
    inicio = time.time(); ultimo = 0
    while True:
        await asyncio.sleep(10)
        agora = time.time()
        if agora - inicio < AQUECIMENTO or agora - ultimo < RECARGA:
            continue
        atual = taxa(agora - 15, agora)
        base = [taxa(agora - 15 * (k + 1), agora - 15 * k) for k in range(2, 80)]
        base = [b for b in base if b is not None]
        mediana = statistics.median(base) if base else 0
        reac = reacoes(agora - 15, agora)
        if atual >= max(MULT * mediana, mediana + MIN_ABS) or reac >= max(6, 1.5 * MIN_ABS):
            ultimo = agora
            log(f'PICO: {atual} msgs/15s (normal {mediana:.1f}), {reac} reações → processando')
            fila.put(agora)


# ---------- 4) processamento de um momento ----------
def openai(caminho, dados=None, arquivos=None, timeout=180):
    url = 'https://api.openai.com/v1/' + caminho
    if arquivos:
        r = subprocess.run(['curl', '-s', '-m', str(timeout), url, '-H', 'Authorization: Bearer sk-proxy'] +
                           sum([['-F', f'{k}={v}'] for k, v in arquivos], []), capture_output=True, text=True)
        return json.loads(r.stdout)
    req = urllib.request.Request(url, data=json.dumps(dados).encode(), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer sk-proxy'})
    return json.load(urllib.request.urlopen(req, timeout=timeout))


def recortar_janela(pico, destino):
    ini, fim = pico - ANTES, pico + DEPOIS
    segs = sorted((int(os.path.basename(f)[:-3]), f) for f in glob.glob(os.path.join(SEG, '*.ts')))
    usar = [(t, f) for t, f in segs if t + SEG_DUR > ini and t < fim]
    if not usar:
        return None, 0
    lista = os.path.join(destino, 'lista.txt')
    open(lista, 'w').write(''.join(f"file '{f}'\n" for _, f in usar))
    t0 = max(ini, usar[0][0])
    janela = os.path.join(destino, 'janela.mp4')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', lista, '-ss', f'{t0 - usar[0][0]:.2f}',
                    '-t', f'{fim - t0:.2f}', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-c:a', 'aac', janela], check=True)
    return janela, t0


def processar(pico):
    pasta = os.path.join(SAIDA, datetime.fromtimestamp(pico).strftime('%Y%m%d-%H%M%S'))
    os.makedirs(pasta, exist_ok=True)
    janela, t0 = recortar_janela(pico, pasta)
    if not janela:
        log('sem gravação para esse momento'); return
    audio = os.path.join(pasta, 'audio.mp3')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', janela, '-vn', '-ac', '1', '-ar', '16000', '-b:a', '64k', audio], check=True)
    tr = openai('audio/transcriptions', arquivos=[('file', '@' + audio), ('model', 'whisper-1'), ('language', 'pt'),
                ('response_format', 'verbose_json'), ('timestamp_granularities[]', 'word'), ('timestamp_granularities[]', 'segment'),
                ('prompt', f'Live do streamer {CANAL} na Twitch, em português do Brasil.')])
    if 'error' in tr:
        log('transcrição falhou', tr['error']); return
    # filtro de fala: descarta trechos sem fala/alucinados (Whisper inventa frases repetidas em som ambiente)
    bons, anterior = [], None
    for sg in tr['segments']:
        txt = sg['text'].strip()
        if sg.get('no_speech_prob', 0) > 0.6 or sg.get('avg_logprob', 0) < -1.0 or sg.get('compression_ratio', 0) > 2.4 or txt == anterior:
            anterior = txt; continue
        anterior = txt; bons.append(sg)
    tr['words'] = [w for w in tr.get('words', []) if any(sg['start'] - 0.2 <= w['start'] <= sg['end'] + 0.2 for sg in bons)]
    n_palavras = len(tr['words'])
    falas = '\n'.join(f"[{sg['start']:.1f}-{sg['end']:.1f}] {sg['text'].strip()}" for sg in bons) or '(SEM FALA CLARA NESTE TRECHO)'
    log(f'fala útil: {n_palavras} palavras em {len(bons)}/{len(tr["segments"])} trechos')
    msgs = [(t - t0, a, x) for t, a, x in list(chat) if t0 <= t < t0 + ANTES + DEPOIS]
    por10 = collections.Counter(int(t // 10) * 10 for t, _, _ in msgs)
    resumo_chat = ' '.join(f'{k}s:{v}' for k, v in sorted(por10.items()))
    amostra = '\n'.join(f'[{t:.0f}s] {x[:60]}' for t, _, x in msgs[-60:])
    prompt = f"""Você edita cortes para o canal brasileiro "Modo Replay" (TikTok/Reels/Shorts) a partir de lives de streamers.
Canal da live: {CANAL}. Abaixo, a transcrição de uma janela de {ANTES + DEPOIS:.0f}s (tempos em segundos dentro da janela),
quantas mensagens o chat mandou a cada 10s, e uma amostra do chat. O pico do chat foi por volta de {pico - t0:.0f}s
(o chat reage alguns segundos DEPOIS do que aconteceu na tela).

TRANSCRIÇÃO:
{falas}

CHAT POR 10s: {resumo_chat}
AMOSTRA DO CHAT:
{amostra}

Regras: NÃO invente contexto que não está na transcrição ou no chat. Se não houver fala clara, só aprove se o chat
mostrar claramente uma reação forte a algo visual, e diga isso no motivo. Na dúvida, reprove (vale=false).
GANCHO (texto grande na tela nos 3 primeiros segundos): NÃO copie palavras da fala. Resuma o que acontece de forma
chamativa e curiosa, em MAIÚSCULAS, 2 linhas de até 16 letras cada, usando o nome do streamer quando ajudar.
Exemplos de estilo: ["ALANZOKA NÃO", "ACREDITOU"], ["ELE FOI ATÉ", "O LIMITE"], ["O CHAT", "PERDEU A LINHA"].
"destaque" é UMA palavra do gancho que vai em amarelo.
Decida se vale um corte. Um bom corte tem gancho nos primeiros 3s, se entende sozinho e termina numa reação/fecho.
Escolha início e fim (entre 45 e 90 segundos, dentro da janela) começando um pouco antes do que gerou a reação.
Responda SOMENTE JSON:
{{"vale": true/false, "nota": 0-10, "motivo": "...", "inicio": s, "fim": s,
 "gancho": ["LINHA 1", "LINHA 2"], "destaque": "palavra do gancho em amarelo",
 "titulo": "frase curta do que aconteceu", "destaques": ["5 a 8 palavras-chave faladas"],
 "tiktok": "legenda TikTok/Reels com 1 emoji, pergunta para comentar e 4 hashtags", "shorts_titulo": "até 60 caracteres com #shorts",
 "instagram": "legenda Instagram de 2-3 linhas com hashtags"}}"""
    resp = openai('chat/completions', {'model': 'gpt-5.4-mini', 'messages': [{'role': 'user', 'content': prompt}],
                                       'response_format': {'type': 'json_object'}})
    dec = json.loads(resp['choices'][0]['message']['content'])
    json.dump(dec, open(os.path.join(pasta, 'decisao.json'), 'w'), ensure_ascii=False, indent=1)
    log(f"decisão: vale={dec.get('vale')} nota={dec.get('nota')} · {dec.get('titulo')} · {dec.get('motivo', '')[:80]}")
    if not dec.get('vale') or dec.get('nota', 0) < NOTA_MIN:
        return
    total = ANTES + DEPOIS
    ini, fim = max(0.0, float(dec['inicio'])), min(total, float(dec['fim']))
    if fim - ini < 45:                       # garante 45 s, crescendo para trás (onde está o contexto)
        falta = 45 - (fim - ini)
        ini = max(0.0, ini - falta); fim = min(total, max(fim, ini + 45))
    if fim - ini > 90:
        ini = fim - 90
    montar(pasta, janela, tr, dec, ini, fim)


def montar(pasta, janela, tr, dec, ini, fim):
    nome = 'vigia-' + CANAL + '-' + os.path.basename(pasta)
    palavras = []
    for w in tr.get('words', []):
        if ini - 0.05 <= w['start'] <= fim:
            t = w['word'].strip()
            t = CENSURA.get(t.lower().strip('.,!?'), t)
            palavras.append({'texto': t, 'inicio': round(w['start'] - ini, 2), 'fim': round(w['end'] - ini, 2)})
    dur = fim - ini + 2.6
    base = os.path.join(MODELO, 'public', nome + '.mp4')
    reflexo = ('split=3[c][a][b];[a]vflip,scale=270:-2,boxblur=8:2,scale=1080:656,eq=brightness=-0.28:saturation=1.1[t];'
               '[b]vflip,scale=270:-2,boxblur=8:2,scale=1080:656,eq=brightness=-0.28:saturation=1.1[bo];[t][c][bo]vstack=3,format=yuv420p[v]')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', f'{ini:.2f}', '-t', f'{dur:.2f}', '-i', janela, '-filter_complex',
                    '[0:v]scale=1080:608,setsar=1,' + reflexo, '-map', '[v]', '-map', '0:a', '-af', 'apad', '-t', f'{dur:.2f}',
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-c:a', 'aac', '-b:a', '192k', base], check=True)
    props = {'dados': {'video': nome + '.mp4', 'duracao': round(dur - 0.05, 2), 'gancho': dec['gancho'], 'destaque': dec.get('destaque', ''),
                       'cabecalho': f'AO VIVO · {CANAL}', 'selo': 'AO VIVO', 'credito': f'{CANAL} (Twitch)', 'canal': 'Modo Replay',
                       'chamadaFinal': 'Segue pra ver os cortes primeiro', 'inicioFinal': round(fim - ini + 0.2, 2), 'legendas': [],
                       'destaques': dec.get('destaques', []), 'palavras': palavras, 'layout': {'topo': 656, 'altura': 608}}}
    arq_props = os.path.join(pasta, 'props.json')
    json.dump(props, open(arq_props, 'w'), ensure_ascii=False)
    final = os.path.join(pasta, 'video-render.mp4')
    subprocess.run(['npx', 'remotion', 'render', 'src/index.ts', 'Corte', final, f'--props={arq_props}', '--concurrency=3', '--log=error'],
                   cwd=MODELO, check=True)
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', final, '-c:v', 'libx264', '-crf', '26', '-preset', 'medium', '-c:a', 'aac',
                    '-b:a', '128k', '-movflags', '+faststart', os.path.join(pasta, 'video.mp4')], check=True)
    os.remove(final); os.remove(base)
    # capa: quadro do meio do corte + gancho
    quadro = os.path.join(pasta, 'quadro.jpg')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', f'{ini + (fim - ini) * 0.4:.2f}', '-i', janela, '-frames:v', '1',
                    '-vf', 'crop=ih*9/16:ih,scale=1080:1920:flags=lanczos', quadro], check=True)
    subprocess.run(['node', os.path.join(AQUI, 'capa.js'), quadro, json.dumps(dec['gancho']), dec.get('destaque', ''),
                    f'🔴 {CANAL.upper()}', os.path.join(pasta, 'capa.jpg')], check=True)
    credito = f'📺 Créditos: {CANAL} — live na Twitch: https://www.twitch.tv/{CANAL}'
    open(os.path.join(pasta, 'legendas.txt'), 'w').write(
        f"{dec.get('titulo', '')}\n\n=== TIKTOK / REELS ===\n{dec.get('tiktok', '')}\n{credito}\n\n"
        f"=== SHORTS ===\nTítulo: {dec.get('shorts_titulo', '')}\nDescrição: {dec.get('titulo', '')}\n{credito}\n\n"
        f"=== INSTAGRAM ===\n{dec.get('instagram', '')}\n{credito}\n")
    for f in ('janela.mp4', 'audio.mp3', 'lista.txt', 'quadro.jpg'):
        try: os.remove(os.path.join(pasta, f))
        except FileNotFoundError: pass
    log('NOVO_CORTE', pasta)


def trabalhador():
    while True:
        pico = fila.get()
        time.sleep(max(0, pico + ESPERA_CAPTURA - time.time()))
        try:
            processar(pico)
        except Exception as e:
            log('erro ao processar', repr(e)[:300])
        limpar_segmentos()


async def principal():
    threading.Thread(target=gravar, daemon=True).start()
    threading.Thread(target=trabalhador, daemon=True).start()
    log('vigia iniciado', '(modo teste)' if TESTE else '')
    await asyncio.gather(ler_chat(), detectar())


if __name__ == '__main__':
    asyncio.run(principal())
