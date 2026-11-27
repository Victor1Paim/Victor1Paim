#!/usr/bin/env python3
"""Vozes dos ANÚNCIOS com o ElevenLabs (locutor natural, só nos anúncios; a produção diária segue no Gemini Achird).
Uso (em eagle-english/): ELEVENLABS_KEY_FILE=<scratchpad>/elevenlabs.key python3 posts/anuncios-teste-1/gerar_vozes_11.py [ids...]
Lê falas.json, grava audio/<id>.wav (PCM 24 kHz mono) e apara o silêncio pelo Whisper.
"""
import json, os, sys, urllib.request
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from vozes import _gravar, tirar_estalo, aparar_com_whisper, registrar  # noqa: E402

P = Path(__file__).resolve().parent
VOZ = {"voice_id": "7lu3ze7orhWaNeSPowWx", "nome": "Lucas", "modelo": "eleven_multilingual_v2",
       "voice_settings": {"stability": 0.45, "similarity_boost": 0.8, "style": 0.3, "use_speaker_boost": True, "speed": 1.08}}
k = Path(os.environ["ELEVENLABS_KEY_FILE"]).read_text().strip()
so = set(sys.argv[1:])
(P / "audio").mkdir(exist_ok=True)
for f in json.loads((P / "falas.json").read_text())["falas"]:
    if so and f["id"] not in so:
        continue
    body = {"text": f["texto"], "model_id": VOZ["modelo"], "language_code": "pt", "voice_settings": VOZ["voice_settings"]}
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ['voice_id']}?output_format=pcm_24000",
                                 data=json.dumps(body).encode(), headers={"xi-api-key": k, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        pcm = r.read()
    registrar(P, "elevenlabs-" + VOZ["modelo"], "voz", caracteres=len(f["texto"]))
    saida = P / "audio" / f"{f['id']}.wav"
    _gravar(tirar_estalo(pcm), saida)
    aparar_com_whisper(saida, "pt")
    print("ok", f["id"])
