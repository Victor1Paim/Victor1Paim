#!/usr/bin/env python3
"""Narração com o Gemini TTS (voz padrão do canal: Fenrir).

Uso: narrar-gemini.py "<texto>" saida.mp3 [voz] [modelo]
Chave: variável GEMINI_API_KEY, ou cabeçalho injetado pelo proxy do ambiente (Network secret para
generativelanguage.googleapis.com). NUNCA commitar a chave.
Obs.: mandar só o texto. O modelo lê em voz alta qualquer instrução de estilo colocada no texto e não aceita systemInstruction.
"""
import base64, json, os, subprocess, sys, urllib.request

texto, saida = sys.argv[1], sys.argv[2]
voz = sys.argv[3] if len(sys.argv) > 3 else 'Fenrir'
modelo = sys.argv[4] if len(sys.argv) > 4 else 'gemini-3.8-flash-tts'
cab = {'Content-Type': 'application/json'}
if os.environ.get('GEMINI_API_KEY'):
    cab['x-goog-api-key'] = os.environ['GEMINI_API_KEY']
corpo = {'contents': [{'parts': [{'text': texto}]}],
         'generationConfig': {'responseModalities': ['AUDIO'], 'speechConfig': {'voiceConfig': {'prebuiltVoiceConfig': {'voiceName': voz}}}}}
req = urllib.request.Request(f'https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent', data=json.dumps(corpo).encode(), headers=cab)
d = json.load(urllib.request.urlopen(req, timeout=300))
pcm = base64.b64decode(d['candidates'][0]['content']['parts'][0]['inlineData']['data'])
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 's16le', '-ar', '24000', '-ac', '1', '-i', '-', '-b:a', '128k', saida], input=pcm, check=True)
# o Gemini deixa um estalo nos últimos ~150 ms: limpar sempre
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'limpar-fim-audio.py'), saida], check=True)
