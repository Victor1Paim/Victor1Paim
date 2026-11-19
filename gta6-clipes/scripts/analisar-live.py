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
linhas = []
for b in range(0, int(dur), 10):
    fala = ' '.join(s['x'] for s in segs if b <= s['t'] < b + 10)
    msgs = [c['m'] for c in chat if b <= c['t'] - t0 < b + 10]
    if fala or len(msgs) > 5:
        linhas.append(f'[{mmss(b)}] chat={len(msgs)} | {fala} ' + (f'|| chat: {" / ".join(msgs[:6])}' if msgs else ''))
open('roteiro.txt', 'w').write('\n'.join(linhas))

prompt = f"""Você escolhe cortes virais (50 s a 1 min 30) de uma live de GTA 6 para TikTok/Reels/Shorts. Contexto: {contexto}
Abaixo, o roteiro da live em blocos de 10 s: [mm:ss] chat=mensagens no bloco | fala do streamer || amostra do chat.
Escolha os {n} melhores momentos: que se entendam sozinhos, com reação forte, humor, susto, novidade do jogo ou pico de chat. Não sobreponha cortes. Comece um pouco antes do gatilho e termine logo após o desfecho.
Responda JSON: {{"cortes":[{{"inicio":"mm:ss","fim":"mm:ss","titulo":"...","por_que":"...","nota":0-10}}]}} ordenado da maior nota para a menor.

{open('roteiro.txt').read()}"""
r = urllib.request.Request('https://api.openai.com/v1/chat/completions', json.dumps({'model': 'gpt-5.4', 'response_format': {'type': 'json_object'}, 'messages': [{'role': 'user', 'content': prompt}]}).encode(), {'Content-Type': 'application/json', 'Authorization': 'Bearer sk-proxy'})
cand = json.loads(json.load(urllib.request.urlopen(r, timeout=600))['choices'][0]['message']['content'])
json.dump(cand, open('candidatos.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(cand, ensure_ascii=False, indent=1))
