#!/usr/bin/env python3
"""Vozes do Eagle English com o Gemini TTS: narração pt-BR e frases em inglês (voz americana),
um arquivo por fala, conferidas pelo Whisper e com custo registrado no post.

1) Montar as falas do formato A a partir do frases.json (gancho, 7 frases, CTA):
     python3 scripts/vozes.py montar posts/2026-11-10_salao
   -> cria posts/<post>/falas.json (revise o texto do gancho e do CTA antes de gerar)

2) Gerar os áudios:
     python3 scripts/vozes.py gerar posts/2026-11-10_salao [--so 03_en] [--sem-conferir]
   -> posts/<post>/audio/<id>.wav + audio/conferencia/  + custos.jsonl

3) Custo do post:  python3 ../scripts/custos.py relatorio posts/2026-11-10_salao

Chave: GEMINI_API_KEY (ou GEMINI_KEY_FILE). Na nuvem, com a chave salva como network secret
(host generativelanguage.googleapis.com, header x-goog-api-key), use GEMINI_API_KEY=proxy-injected.
No notebook, coloque GEMINI_API_KEY no eagle-english/.env. Nunca grave a chave no git.

Regras (aprendidas no Saúde sem Sermão em 08/11/2026): não colocar instrução de tom no texto
("Say warmly: ..."): o gemini-3.8-flash-tts às vezes lê a instrução em voz alta.
Voz pt-BR lê inglês errado: frase em inglês SEMPRE em arquivo separado, com a voz americana.
"""
import argparse, base64, json, os, subprocess, sys, tempfile, urllib.request
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
RAIZ = PROJ.parent
sys.path.insert(0, str(RAIZ / "scripts"))
from custos import registrar  # noqa: E402

CONFERIR = RAIZ / ".claude/skills/whisper-legendas/scripts/whisper_legendas.py"
VOZ = {"pt": "Achird", "en": "Kore"}
MODELO = "gemini-3.8-flash-tts"


def carregar_env():
    env = PROJ / ".env"
    if env.exists():
        for l in env.read_text().splitlines():
            if "=" in l and not l.lstrip().startswith("#"):
                k, v = l.split("=", 1)
                if v.strip():
                    os.environ.setdefault(k.strip(), v.strip())


def chave():
    if os.environ.get("GEMINI_KEY_FILE"):
        return Path(os.environ["GEMINI_KEY_FILE"]).read_text().strip()
    if os.environ.get("GEMINI_API_KEY"):
        return os.environ["GEMINI_API_KEY"]
    sys.exit("defina GEMINI_API_KEY (no .env) ou GEMINI_KEY_FILE")


def montar(post):
    d = json.loads((post / "frases.json").read_text(encoding="utf-8"))
    falas = [{"id": "00_gancho", "lingua": "pt",
              "texto": f"Repita comigo: inglês do {d['tema']}! {d.get('gancho', '')}".strip()}]
    for i, f in enumerate(d["frases"], 1):
        falas.append({"id": f"{i:02d}_en", "lingua": "en", "texto": f["en"]})
    falas.append({"id": "99_cta", "lingua": "pt", "texto":
                  f"Essas foram {len(d['frases'])}. No Eagle 350 tem mapas de 35 situações do dia a dia, "
                  "com tradução e pronúncia escrita, e mais 4 bônus. Link na bio. E manda pra quem vai viajar!"})
    arq = post / "falas.json"
    if arq.exists():
        sys.exit(f"{arq} já existe; apague para remontar")
    arq.write_text(json.dumps({"vozes": VOZ, "modelo": MODELO, "falas": falas}, ensure_ascii=False, indent=2) + "\n")
    print(f"criado {arq.relative_to(PROJ)} com {len(falas)} falas: revise gancho e CTA (seção 12) antes de gerar")


def tirar_estalo(pcm, sr=24000):
    """O Gemini TTS às vezes devolve um ruído curto e forte DEPOIS do fim da fala (estalo no final).
    Remove blocos finais curtos (< 0,4 s) que venham depois de >= 80 ms de quase-silêncio."""
    import numpy as np
    a = np.frombuffer(pcm, np.int16)
    w = sr // 100  # janelas de 10 ms
    for _ in range(3):
        n = len(a) // w
        if n < 20:
            break
        rms = np.sqrt((a[:n * w].astype(float).reshape(n, w) ** 2).mean(axis=1))
        som = np.nonzero(rms > 60)[0]
        if not len(som):
            break
        fim = som[-1]
        ini = fim
        while ini > 0 and rms[ini - 1] > 60:
            ini -= 1
        silencio = 0
        j = ini - 1
        while j >= 0 and rms[j] <= 60:
            silencio += 1; j -= 1
        if fim - ini + 1 < 40 and silencio >= 8 and j > 0:
            a = a[:(ini - silencio // 2) * w]  # corta o ruído, mantém metade do silêncio antes dele
        else:
            break
    return a.tobytes()


def pedir(req, tentativas=8):
    """Chama a API; no plano gratuito (3 pedidos/min) espera e tenta de novo. Limite diário: para com aviso."""
    import re, time, urllib.error
    for i in range(tentativas):
        try:
            return json.load(urllib.request.urlopen(req, timeout=180))
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            msg = e.read().decode(errors="ignore")
            if "per day" in msg or "PerDay" in msg:
                sys.exit("Limite DIÁRIO do Gemini gratuito atingido: tente amanhã ou ative o faturamento no AI Studio.")
            m = re.search(r"retry in ([0-9.]+)s", msg)
            espera = max(float(m.group(1)) if m else 20.0, 5.0) + 1
            print(f"  limite por minuto do Gemini; esperando {espera:.0f} s...", flush=True)
            time.sleep(espera)
    sys.exit("Gemini continua recusando (429).")


INSTRUCOES = {  # só OpenAI (gpt-4o-mini-tts): tom de locutor, mesma voz nas duas línguas
    "pt": "Locutor brasileiro de rádio e comerciais: voz grave, firme, animada e clara, ritmo dinâmico, "
          "sotaque de português do Brasil, sem exagero.",
    "en": "Same announcer voice and energy, now speaking clear, natural American English, at a slightly "
          "slower pace so a learner can repeat it.",
}


def tts_openai(texto, voz, modelo, lingua, instrucoes, post):
    import time, urllib.error
    body = {"model": modelo, "voice": voz, "input": texto, "response_format": "pcm",
            "instructions": (instrucoes or INSTRUCOES)[lingua]}
    req = urllib.request.Request("https://api.openai.com/v1/audio/speech", data=json.dumps(body).encode(),
                                 headers={"Authorization": "Bearer " + os.environ.get("OPENAI_API_KEY", "proxy-injected"),
                                          "Content-Type": "application/json"})
    for i in range(3):
        try:
            pcm = urllib.request.urlopen(req, timeout=180).read(); break
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503) or i == 2:
                raise
            time.sleep(8)
    # custo estimado pela duração (24 kHz, 16 bits): a rota /audio/speech não devolve tokens
    registrar(post, modelo, "voz", minuto_audio=len(pcm) / 2 / 24000 / 60)
    return pcm


def tts(texto, voz, modelo, saida, post, lingua="pt", instrucoes=None):
    if modelo.startswith("gpt-"):
        pcm = tirar_estalo(tts_openai(texto, voz, modelo, lingua, instrucoes, post))
        return _gravar(pcm, saida)
    # Modelos 2.5 tratam frase curta como instrução (erro 400 "tried to generate text"): prefixar "Say".
    # Os 3.x NÃO podem ter prefixo (às vezes leem a instrução em voz alta).
    if "2.5" in modelo:
        texto = ("Say in Brazilian Portuguese: " if lingua == "pt" else "Say in American English: ") + texto
    body = {"contents": [{"parts": [{"text": texto}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voz}}}}}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent",
        data=json.dumps(body).encode(), headers={"x-goog-api-key": chave(), "Content-Type": "application/json"})
    d = pedir(req)
    u = d.get("usageMetadata", {})
    registrar(post, modelo, "voz", entrada_texto=u.get("promptTokenCount", 0),
              saida_audio=u.get("candidatesTokenCount", 0))
    pcm = tirar_estalo(base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]))
    return _gravar(pcm, saida)


def _gravar(pcm, saida):
    with tempfile.NamedTemporaryFile(suffix=".pcm") as f:
        f.write(pcm); f.flush()
        # wav 48 kHz para montar no ffmpeg sem perda. Apara o silêncio das pontas deixando 80 ms de folga,
        # faz fade de 60 ms no fim e 10 ms no começo e soma 150 ms de silêncio: sem estalo de corte no final.
        apara = "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.08"
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-f", "s16le", "-ar", "24000", "-ac", "1",
                        "-i", f.name, "-af",
                        f"{apara},areverse,{apara},afade=t=in:d=0.06,areverse,afade=t=in:d=0.01,apad=pad_dur=0.15",
                        "-ar", "48000", str(saida)], check=True)
    limpar_estalo_wav(saida)


def limpar_estalo_wav(arq):
    """Rede de segurança no .wav final: o TTS às vezes termina com uma rajada de ruído alta e chapada (~0,1–0,3 s) depois
    de um respiro curto. Se o último trecho com som for curto (< 0,35 s), bem alto (mediana > 0,3) e vier depois de >= 30 ms
    de quase-silêncio, corta a partir do respiro e refaz o fade + 150 ms de silêncio. Devolve True se cortou."""
    import numpy as np, wave
    with wave.open(str(arq)) as w:
        sr, ch, sw = w.getframerate(), w.getnchannels(), w.getsampwidth(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16)
    if ch != 1 or sw != 2:
        return False
    k = sr // 100; n = len(x) // k
    rms = np.sqrt((x[:n * k].astype(float).reshape(n, k) / 32768) ** 2).mean(axis=1) if False else \
        np.sqrt(((x[:n * k].astype(float) / 32768).reshape(n, k) ** 2).mean(axis=1))
    som = np.nonzero(rms > 0.01)[0]
    if not len(som):
        return False
    fim = som[-1]; ini = fim
    while ini > 0 and rms[ini - 1] > 0.01:
        ini -= 1
    gap = 0; j = ini - 1
    while j >= 0 and rms[j] <= 0.01:
        gap += 1; j -= 1
    if not (fim - ini + 1 < 35 and np.median(rms[ini:fim + 1]) > 0.3 and gap >= 3 and j > 0):
        return False
    corte = (ini - gap // 2) * k
    y = x[:corte].astype(float)
    f = min(len(y), int(sr * 0.06)); y[-f:] *= np.linspace(1, 0, f)
    y = np.concatenate([y, np.zeros(int(sr * 0.15))]).astype(np.int16)
    with wave.open(str(arq), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(y.tobytes())
    return True


def aparar_com_whisper(arq, lingua, palavras=None):
    """Silencia tudo antes da 1ª palavra e depois da última (marcadas pelo Whisper), com folga de 0,12 s antes e 0,28 s depois
    + fades: some qualquer estalo/chiado que o TTS solta fora da fala. Devolve (início, fim) mantidos."""
    import numpy as np, wave
    global _WHISPER
    if palavras is None:
        import whisper
        if _WHISPER is None:
            _WHISPER = whisper.load_model(os.environ.get("WHISPER_MODELO", "turbo"))
        r = _WHISPER.transcribe(str(arq), language=lingua, fp16=False, word_timestamps=True)
        palavras = [(w["start"], w["end"]) for sg in r["segments"] for w in sg.get("words", [])]
    if not palavras:
        return None
    with wave.open(str(arq)) as w:
        sr = w.getframerate(); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float)
    a = max(0, int((palavras[0][0] - 0.12) * sr)); b = min(len(x), int((palavras[-1][1] + 0.28) * sr))
    y = np.zeros_like(x); y[a:b] = x[a:b]
    fi, fo = int(sr * 0.02), int(sr * 0.08)
    y[a:a + fi] *= np.linspace(0, 1, len(y[a:a + fi])); y[max(a, b - fo):b] *= np.linspace(1, 0, len(y[max(a, b - fo):b]))
    with wave.open(str(arq), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(y.astype(np.int16).tobytes())
    return a / sr, b / sr


_WHISPER = None


def conferir(saida, texto, lingua):
    """Transcreve com o Whisper (modelo carregado uma vez) e devolve a semelhança com o texto (%)."""
    global _WHISPER
    import difflib, re
    import whisper
    if _WHISPER is None:
        _WHISPER = whisper.load_model(os.environ.get("WHISPER_MODELO", "turbo"))
    res = _WHISPER.transcribe(str(saida), language=lingua, fp16=False, word_timestamps=True)
    ouvido = res["text"].strip()
    aparar_com_whisper(saida, lingua, [(w["start"], w["end"]) for sg in res["segments"] for w in sg.get("words", [])])
    # o TTS às vezes "escorrega" de idioma em fala curta (ex.: "Un sino" em espanhol): detecta a língua e reprova
    audio = whisper.pad_or_trim(whisper.load_audio(str(saida)))
    mel = whisper.log_mel_spectrogram(audio, n_mels=_WHISPER.dims.n_mels).to(_WHISPER.device)
    _, probs = _WHISPER.detect_language(mel)
    rival = {"pt": "es", "en": "pt"}.get(lingua)
    if rival and probs.get(rival, 0) > probs.get(lingua, 0):
        print(f"    whisper: {ouvido}  [IDIOMA ERRADO: soa {rival} ({probs[rival]:.0%}) em vez de {lingua}]")
        return 0.0
    norm = lambda t: re.sub(r"[^\wáéíóúâêôãõçà' ]", " ", t.lower()).split()
    pct = round(difflib.SequenceMatcher(None, norm(texto), norm(ouvido)).ratio() * 100, 1)
    print(f"    whisper: {ouvido}")
    return pct


def conferir_antigo(saida, texto, lingua):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as r:
        r.write(texto)
    out = subprocess.run([sys.executable, str(CONFERIR), str(saida), "--saida", str(saida.parent / "conferencia"),
                          "--roteiro", r.name, "--idioma", lingua], capture_output=True, text=True).stdout
    os.unlink(r.name)
    linhas = [l for l in out.splitlines() if l.startswith("semelhança")]
    return float(linhas[0].split()[1].rstrip("%")) if linhas else 0.0


def gerar(post, so, sem_conferir, minimo, tentativas, pular=False, modelo_forcado=None):
    cfg = json.loads((post / "falas.json").read_text(encoding="utf-8"))
    vozes, modelo = {**VOZ, **cfg.get("vozes", {})}, modelo_forcado or cfg.get("modelo", MODELO)
    (post / "audio").mkdir(exist_ok=True)
    falhas = []
    for f in cfg["falas"]:
        if so and f["id"] not in so:
            continue
        if pular and (post / "audio" / f"{f['id']}.wav").exists():
            continue
        saida = post / "audio" / f"{f['id']}.wav"
        for t in range(1, tentativas + 1):
            tts(f["texto"], vozes[f["lingua"]], f.get("modelo", modelo), saida, post, f["lingua"], cfg.get("instrucoes"))
            if sem_conferir:
                print(f"{f['id']}: gerado"); break
            pct = conferir(saida, f["texto"], f["lingua"])
            print(f"{f['id']}: tentativa {t}, {pct}%")
            if pct >= minimo:
                break
        else:
            falhas.append(f["id"])
    if falhas:
        print("REPROVADAS (ouça e ajuste o texto ou a voz):", ", ".join(falhas)); return 1
    print(f"ok -> {post.relative_to(PROJ)}/audio/")
    return 0


def main():
    carregar_env()
    ap = argparse.ArgumentParser()
    ap.add_argument("acao", choices=["montar", "gerar"]); ap.add_argument("post")
    ap.add_argument("--so", nargs="*", help="gerar só estes ids")
    ap.add_argument("--sem-conferir", action="store_true", help="pular a conferência do Whisper")
    ap.add_argument("--modelo", help="outro modelo de TTS (ex.: gemini-3.8-flash-lite-tts quando o limite diário acabar)")
    ap.add_argument("--pular-existentes", action="store_true", help="não regerar falas que já têm áudio")
    ap.add_argument("--minimo", type=float, default=95.0)
    ap.add_argument("--tentativas", type=int, default=3)
    a = ap.parse_args()
    post = Path(a.post).resolve()
    if a.acao == "montar":
        return montar(post)
    return gerar(post, a.so, a.sem_conferir, a.minimo, a.tentativas, a.pular_existentes, a.modelo)


if __name__ == "__main__":
    sys.exit(main())
