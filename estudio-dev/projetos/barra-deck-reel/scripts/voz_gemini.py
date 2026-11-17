"""Gera narração com o Gemini TTS (voz Fenrir por padrão).

Uso:
  python3 scripts/voz_gemini.py "texto da narração" [saida.mp3] [--voz Fenrir] [--estilo "instrução de tom"]
  python3 scripts/voz_gemini.py --arquivo roteiro.txt saida.mp3

A chave vem de GEMINI_API_KEY (variável do ambiente) ou é injetada pelo proxy no cabeçalho
x-goog-api-key quando cadastrada como Network secret do host generativelanguage.googleapis.com.
Modelo: GEMINI_TTS_MODEL (padrão gemini-2.5-flash-preview-tts). Áudio: PCM 24 kHz mono -> mp3.
"""
import argparse
import base64
import json
import os
import subprocess
import tempfile
import time
import urllib.request

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELO = os.environ.get('GEMINI_TTS_MODEL', 'gemini-2.5-flash-preview-tts')
KEY = os.environ.get('GEMINI_API_KEY', 'proxy')

ESTILO_PADRAO = (
    'Leia em português do Brasil, sotaque carioca natural, voz masculina de apresentador: calorosa, confiante e '
    'elegante, ritmo de Reels sem pressa. Dê ênfase às datas e horários.'
)


def gerar(texto, saida, voz='Fenrir', estilo=ESTILO_PADRAO):
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{MODELO}:generateContent'
    corpo = {
        'contents': [{'parts': [{'text': f'{estilo}\n\n{texto}'}]}],
        'generationConfig': {
            'responseModalities': ['AUDIO'],
            'speechConfig': {'voiceConfig': {'prebuiltVoiceConfig': {'voiceName': voz}}},
        },
    }
    req = urllib.request.Request(url, data=json.dumps(corpo).encode(),
                                 headers={'x-goog-api-key': KEY, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=300) as r:
        d = json.loads(r.read())
    parte = d['candidates'][0]['content']['parts'][0]['inlineData']
    pcm = base64.b64decode(parte['data'])
    with tempfile.NamedTemporaryFile(suffix='.pcm', delete=False) as f:
        f.write(pcm)
        bruto = f.name
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 's16le', '-ar', '24000', '-ac', '1', '-i', bruto,
                    '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-b:a', '192k', saida], check=True)
    os.unlink(bruto)
    with open(os.path.join(AQUI, 'custos.jsonl'), 'a') as f:
        f.write(json.dumps({'quando': time.strftime('%Y-%m-%d %H:%M'), 'api': 'gemini', 'modelo': MODELO,
                            'voz': voz, 'item': os.path.basename(saida), 'uso': d.get('usageMetadata')}) + '\n')
    return saida


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('texto', nargs='?')
    ap.add_argument('saida', nargs='?', default=os.path.join(AQUI, 'public', 'audio', 'narracao-fenrir.mp3'))
    ap.add_argument('--arquivo')
    ap.add_argument('--voz', default='Fenrir')
    ap.add_argument('--estilo', default=ESTILO_PADRAO)
    a = ap.parse_args()
    texto = open(a.arquivo).read().strip() if a.arquivo else a.texto
    if not texto:
        ap.error('informe o texto ou --arquivo')
    print(gerar(texto, a.saida, a.voz, a.estilo))
