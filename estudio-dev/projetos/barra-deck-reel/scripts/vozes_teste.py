"""Gera amostras da narração em vozes masculinas (OpenAI TTS) para escolher a melhor."""
import json
import os
import sys
import urllib.request

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = os.environ.get('OPENAI_API_KEY', 'proxy')

TEXTO = (
    'Olha só: a sua ceia de Natal já tem endereço. '
    'O Barra Deck prepara tudo pra você: entradas, quiches, pratos principais, acompanhamentos e sobremesas. '
    'Anota aí: encomendas até dez de dezembro. '
    'Retirada no dia vinte e quatro, das dez às quinze horas. '
    'É só montar o seu pré-pedido no link da bio.'
)
INSTRUCOES = (
    'Fale em português do Brasil, com sotaque carioca natural. Voz masculina de apresentador e instrutor: '
    'confiante, próximo, animado na medida certa, como quem explica algo a um amigo olhando para a câmera. '
    'Entonação viva e variada, nada monótono nem robótico. Dê ênfase às datas e horários. '
    'Ritmo dinâmico de Reels, com micro-pausas naturais depois de "Olha só" e "Anota aí".'
)


def tts(voz, destino):
    req = urllib.request.Request('https://api.openai.com/v1/audio/speech', data=json.dumps({
        'model': 'gpt-4o-mini-tts', 'voice': voz, 'input': TEXTO, 'instructions': INSTRUCOES,
        'response_format': 'mp3'}).encode(), headers={'Authorization': f'Bearer {KEY}', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=120) as r:
        open(destino, 'wb').write(r.read())


if __name__ == '__main__':
    vozes = sys.argv[1:] or ['ash', 'onyx', 'echo']
    os.makedirs(os.path.join(AQUI, 'amostras'), exist_ok=True)
    for v in vozes:
        tts(v, os.path.join(AQUI, 'amostras', f'voz-{v}.mp3'))
        print('ok', v)
