#!/usr/bin/env python3
"""Narração: um áudio por parágrafo (Gemini TTS), limpeza do fim, pausas e junção.

Uso: python3 -I motor/voz.py HISTORIA.md PASTA_PRODUCAO [--voz Enceladus] [--modelo gemini-3.8-flash-tts]
       [--velocidade 1.06] [--simular]

Saída em PASTA/voz/: pNN.wav (cache: só gera o que falta), narracao.wav e tempos.json
(início e fim de cada parágrafo na narração final, em segundos).
Para refazer um parágrafo: apague voz/pNN.wav e rode de novo.
"""
import argparse, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comum import GEMINI, env_gemini, ler_historia, duracao, jsave, parar_se_sem_credito, esperar_se_limite, RAIZ

ap = argparse.ArgumentParser()
ap.add_argument('historia'); ap.add_argument('pasta')
ap.add_argument('--voz', default='Enceladus'); ap.add_argument('--modelo', default='gemini-3.8-flash-tts')
ap.add_argument('--velocidade', type=float, default=1.06, help='atempo (1.06 ≈ 190 palavras/min com a Enceladus)')
ap.add_argument('--pausa', type=float, default=0.85, help='silêncio entre parágrafos, em s')
ap.add_argument('--simular', action='store_true')
a = ap.parse_args()
# começo de cada trecho: 4 ms mudos + fade de 10 ms; fim: fade de 15 ms (sem estalo nas emendas)
ANTI_ESTALO = 'afade=t=in:st=0.004:d=0.010,areverse,afade=t=in:d=0.015,areverse'

pasta = os.path.join(a.pasta, 'voz'); os.makedirs(pasta, exist_ok=True)
pars = ler_historia(a.historia)
print(f'{len(pars)} parágrafos, {sum(len(p.split()) for p in pars)} palavras')


def gerar(i_p):
    i, p = i_p
    wav = os.path.join(pasta, f'p{i:02d}.wav')
    txt = os.path.join(pasta, f'p{i:02d}.txt')
    # reaproveita só se o áudio é DESTE texto (parágrafos inseridos mudam a numeração)
    if os.path.exists(wav) and os.path.exists(txt) and open(txt).read() == p:
        return wav
    if os.path.exists(wav): os.remove(wav)
    open(txt, 'w').write(p)
    cmd = ['node', GEMINI, 'tts', '--text-file', txt, '--out', wav, '--voice', a.voz, '--model', a.modelo]
    if not a.simular: cmd.append('--go')
    for tentativa in range(8):
        r = subprocess.run(cmd, capture_output=True, text=True, env=env_gemini(), cwd=RAIZ)
        saida = r.stdout + r.stderr
        if r.returncode == 0 and (a.simular or os.path.exists(wav)):
            break
        parar_se_sem_credito('Gemini (voz)', saida)
        if not esperar_se_limite(saida, tentativa) and tentativa >= 2:
            sys.exit(f'falhou p{i:02d}: {saida[-500:]}')
    else:
        parar_se_sem_credito('Gemini (voz)', 'PerDay: limite não liberou depois de 8 tentativas. ' + saida)
    if not a.simular:
        subprocess.run([sys.executable, '-I', os.path.join(RAIZ, 'ferramentas/limpar-fim-audio.py'), wav, wav + '.mp3'],
                       capture_output=True)
        # volta para wav 24 kHz já limpo
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', wav + '.mp3', '-af', ANTI_ESTALO, '-ar', '24000', '-ac', '1', wav], check=True)
        os.remove(wav + '.mp3')
    print(f'  p{i:02d} ok')
    return wav


with ThreadPoolExecutor(3) as ex:
    wavs = list(ex.map(gerar, enumerate(pars)))
if a.simular:
    sys.exit(0)

# junção: parágrafo + pausa, com acelerador leve
silencio = os.path.join(pasta, 'silencio.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'anullsrc=r=24000:cl=mono', '-t', str(a.pausa), silencio], check=True)
lista = os.path.join(pasta, 'lista.txt')
with open(lista, 'w') as f:
    for w in wavs:
        f.write(f"file '{os.path.abspath(w)}'\nfile '{os.path.abspath(silencio)}'\n")
saida = os.path.join(pasta, 'narracao.wav')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lista,
                '-af', f'atempo={a.velocidade},highpass=f=60,acompressor=threshold=-20dB:ratio=2.5:attack=10:release=200',
                '-ar', '48000', '-ac', '1', saida], check=True)

t = 0.0; tempos = []
for i, w in enumerate(wavs):
    d = duracao(w) / a.velocidade
    tempos.append({'paragrafo': i, 'inicio': round(t, 3), 'fim': round(t + d, 3), 'palavras': len(pars[i].split())})
    t += d + a.pausa / a.velocidade
jsave(os.path.join(pasta, 'tempos.json'), tempos)
tot = duracao(saida)
print(f'narração: {tot/60:.2f} min · {sum(x["palavras"] for x in tempos)/(tot/60):.0f} palavras/min · {saida}')
