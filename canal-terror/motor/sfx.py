#!/usr/bin/env python3
"""Biblioteca de efeitos sonoros do canal (só ElevenLabs Sound Effects).

  python3 -I motor/sfx.py gerar [--prioridade 1] [--so id1,id2]   gera o que falta no catálogo (já existente = pula)
  python3 -I motor/sfx.py listar [palavra]                         lista o que existe (busca por id ou tag)
  python3 -I motor/sfx.py verificar [--so id1,id2]                 um modelo que escuta (OpenAI gpt-audio) diz o que ouviu
                                                                   em cada som; grava em sfx/verificacao.json

Catálogo: sfx/catalogo.json (id, categoria, prompt, duracao, loop, tags, prioridade). Arquivos: sfx/<categoria>/<id>.mp3.
Para um efeito novo: acrescentar no catálogo e rodar `gerar --so id`. Registro de geração: sfx/gerados.jsonl.
Chave: ~/.config/canal-terror/elevenlabs.key ou ELEVENLABS_API_KEY. Sem crédito → para e avisa.
Licença: gerado em plano PAGO = uso comercial para sempre; gerado no plano grátis = nunca comercial.
"""
import argparse, datetime, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import RAIZ, parar_se_sem_credito, esperar_se_limite

BIB = os.path.join(RAIZ, 'sfx')
CAT = os.path.join(BIB, 'catalogo.json')


def chave():
    k = os.environ.get('ELEVENLABS_API_KEY')
    p = os.path.expanduser('~/.config/canal-terror/elevenlabs.key')
    return k or (open(p).read().strip() if os.path.exists(p) else None)


def caminho(ef):
    return os.path.join(BIB, ef['categoria'], ef['id'] + '.mp3')


def catalogo():
    return json.load(open(CAT, encoding='utf-8'))['efeitos']


def gerar(ef):
    dest = caminho(ef); os.makedirs(os.path.dirname(dest), exist_ok=True)
    body = {'text': ef['prompt'], 'prompt_influence': ef.get('influencia', 0.5), 'loop': bool(ef.get('loop'))}
    if ef.get('duracao'): body['duration_seconds'] = ef['duracao']
    if ef.get('modelo'): body['model_id'] = ef['modelo']
    for t in range(6):
        r = subprocess.run(['curl', '-sS', '-o', dest + '.tmp', '-w', '%{http_code}', '-D', dest + '.hdr',
                            'https://api.elevenlabs.io/v1/sound-generation?output_format=mp3_44100_128',
                            '-H', f'xi-api-key: {chave()}', '-H', 'Content-Type: application/json', '-d', json.dumps(body)],
                           capture_output=True, text=True)
        cod = r.stdout.strip()
        if cod == '200':
            os.replace(dest + '.tmp', dest); break
        erro = open(dest + '.tmp', errors='replace').read()[:500] if os.path.exists(dest + '.tmp') else r.stderr
        if cod in ('401', '402') or 'quota' in erro.lower() or 'credit' in erro.lower():
            parar_se_sem_credito('ElevenLabs (efeitos)', 'insufficient_quota ' + erro)
        if not esperar_se_limite(f'{cod} {erro}' if cod == '429' else '', t):
            sys.exit(f"{ef['id']}: HTTP {cod} {erro}")
    hdr = open(dest + '.hdr').read() if os.path.exists(dest + '.hdr') else ''
    custo = [l.split(':', 1)[1].strip() for l in hdr.splitlines() if l.lower().startswith(('character-cost', 'x-character-count'))]
    for f in (dest + '.hdr', dest + '.tmp'):
        if os.path.exists(f): os.remove(f)
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', dest],
                               capture_output=True, text=True).stdout or 0)
    with open(os.path.join(BIB, 'gerados.jsonl'), 'a') as f:
        f.write(json.dumps({'id': ef['id'], 'em': datetime.datetime.now().isoformat(timespec='seconds'),
                            'duracao': round(dur, 2), 'creditos': custo[0] if custo else None, 'modelo': ef.get('modelo', 'eleven_text_to_sound_v2')}) + '\n')
    print(f"  {ef['id']} ok ({dur:.1f} s{', créditos ' + custo[0] if custo else ''})")
    return dur


ap = argparse.ArgumentParser()
ap.add_argument('acao', choices=['gerar', 'listar', 'verificar']); ap.add_argument('busca', nargs='?', default='')
ap.add_argument('--prioridade', type=int, default=9); ap.add_argument('--so', default='')
a = ap.parse_args()
efs = catalogo()
if a.acao == 'listar':
    for ef in efs:
        if a.busca in ef['id'] or a.busca in ','.join(ef['tags']):
            print(f"{'✓' if os.path.exists(caminho(ef)) else '·'} {ef['id']:26s} {ef['categoria']:9s} {ef.get('duracao') or '':>5} {'loop' if ef.get('loop') else '    '} {','.join(ef['tags'])}")
    sys.exit(0)
so = set(filter(None, a.so.split(',')))
if a.acao == 'verificar':
    import base64, tempfile
    ver_p = os.path.join(BIB, 'verificacao.json')
    ver = json.load(open(ver_p)) if os.path.exists(ver_p) else {}
    for ef in efs:
        if (so and ef['id'] not in so) or not os.path.exists(caminho(ef)): continue
        wav = tempfile.mktemp(suffix='.wav')
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', caminho(ef), '-t', '12', '-af', 'apad=pad_dur=0.5', '-ac', '1', '-ar', '24000', wav], check=True)
        pedido = ('You will hear a short sound effect. In at most 8 words, say what the sound is (e.g. "car horn honk", '
                  '"knocking on glass"). Do not guess a story; describe only what you hear.')
        body = {'model': 'gpt-audio', 'modalities': ['text'], 'messages': [{'role': 'user', 'content': [
            {'type': 'text', 'text': pedido},
            {'type': 'input_audio', 'input_audio': {'data': base64.b64encode(open(wav, 'rb').read()).decode(), 'format': 'wav'}}]}]}
        req = wav + '.json'; open(req, 'w').write(json.dumps(body))
        r = subprocess.run(['curl', '-sS', 'https://api.openai.com/v1/chat/completions', '-H', 'Authorization: Bearer sk-proxy',
                            '-H', 'Content-Type: application/json', '-d', '@' + req], capture_output=True, text=True)
        os.remove(wav); os.remove(req)
        d = json.loads(r.stdout)
        ouviu = d['error']['message'] if 'error' in d else d['choices'][0]['message']['content'].strip()
        ver[ef['id']] = {'ouviu': ouviu, 'pedido': ef['prompt']}
        print(f"{ef['id']:24s} → {ouviu}")
    json.dump(ver, open(ver_p, 'w'), ensure_ascii=False, indent=1)
    sys.exit(0)
fila = [ef for ef in efs if not os.path.exists(caminho(ef)) and (ef['id'] in so if so else ef.get('prioridade', 1) <= a.prioridade)]
print(f'{len(fila)} efeito(s) para gerar · ~{sum(ef.get("duracao") or 5 for ef in fila):.0f} s de som')
total = sum(gerar(ef) for ef in fila)
print(f'gerado agora: {total:.0f} s')
