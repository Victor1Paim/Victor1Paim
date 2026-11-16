"""Gera a narração do reel com a API da OpenAI (TTS) e as marcações de tempo por palavra.

Uso: python3 scripts/narracao.py
A chave é injetada pelo proxy do ambiente; localmente, defina OPENAI_API_KEY.
"""
import json
import os
import urllib.request
import uuid

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(AQUI, 'public', 'audio')
KEY = os.environ.get('OPENAI_API_KEY', 'proxy')

TEXTO = (
    'Sua ceia de Natal, pronta, do jeito do Barra Deck. '
    'Entradas, quiches, pratos principais, acompanhamentos e sobremesas, tudo feito na casa. '
    'Encomendas até dez de dezembro. '
    'Retirada no dia vinte e quatro, das dez às quinze horas. '
    'Monte seu pré-pedido pelo link na bio.'
)
INSTRUCOES = (
    'Português do Brasil, sotaque carioca leve. Voz feminina calorosa e elegante, '
    'tom acolhedor de Natal, ritmo calmo mas sem arrastar, sorriso na voz. '
    'Pausas curtas entre as frases.'
)


def post_json(url, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers={
        'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def transcrever(caminho):
    b = uuid.uuid4().hex
    partes = []
    for k, v in (('model', 'whisper-1'), ('language', 'pt'), ('response_format', 'verbose_json'),
                 ('timestamp_granularities[]', 'word')):
        partes.append(f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    with open(caminho, 'rb') as f:
        dados = f.read()
    partes.append(f'--{b}\r\nContent-Disposition: form-data; name="file"; filename="narracao.mp3"\r\n'
                  f'Content-Type: audio/mpeg\r\n\r\n'.encode() + dados + b'\r\n')
    partes.append(f'--{b}--\r\n'.encode())
    req = urllib.request.Request('https://api.openai.com/v1/audio/transcriptions', data=b''.join(partes), headers={
        'Authorization': f'Bearer {KEY}', 'Content-Type': f'multipart/form-data; boundary={b}'})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read())


if __name__ == '__main__':
    os.makedirs(SAIDA, exist_ok=True)
    mp3 = os.path.join(SAIDA, 'narracao.mp3')
    audio = post_json('https://api.openai.com/v1/audio/speech', {
        'model': 'gpt-4o-mini-tts', 'voice': 'coral', 'input': TEXTO,
        'instructions': INSTRUCOES, 'response_format': 'mp3'})
    open(mp3, 'wb').write(audio)
    t = transcrever(mp3)
    json.dump({'texto': TEXTO, 'duracao': t.get('duration'), 'palavras': t.get('words', [])},
              open(os.path.join(SAIDA, 'narracao.json'), 'w'), ensure_ascii=False, indent=1)
    print('duração:', t.get('duration'))
    print(t.get('text'))
