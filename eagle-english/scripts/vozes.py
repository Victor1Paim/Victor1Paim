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


def tts(texto, voz, modelo, saida, post):
    body = {"contents": [{"parts": [{"text": texto}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voz}}}}}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent",
        data=json.dumps(body).encode(), headers={"x-goog-api-key": chave(), "Content-Type": "application/json"})
    d = json.load(urllib.request.urlopen(req, timeout=180))
    u = d.get("usageMetadata", {})
    registrar(post, modelo, "voz", entrada_texto=u.get("promptTokenCount", 0),
              saida_audio=u.get("candidatesTokenCount", 0))
    pcm = tirar_estalo(base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]))
    with tempfile.NamedTemporaryFile(suffix=".pcm") as f:
        f.write(pcm); f.flush()
        # wav 48 kHz para montar no ffmpeg sem perda. Apara o silêncio das pontas deixando 80 ms de folga,
        # faz fade de 60 ms no fim e 10 ms no começo e soma 150 ms de silêncio: sem estalo de corte no final.
        apara = "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.08"
        subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-f", "s16le", "-ar", "24000", "-ac", "1",
                        "-i", f.name, "-af",
                        f"{apara},areverse,{apara},afade=t=in:d=0.06,areverse,afade=t=in:d=0.01,apad=pad_dur=0.15",
                        "-ar", "48000", str(saida)], check=True)


def conferir(saida, texto, lingua):
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as r:
        r.write(texto)
    out = subprocess.run([sys.executable, str(CONFERIR), str(saida), "--saida", str(saida.parent / "conferencia"),
                          "--roteiro", r.name, "--idioma", lingua], capture_output=True, text=True).stdout
    os.unlink(r.name)
    linhas = [l for l in out.splitlines() if l.startswith("semelhança")]
    return float(linhas[0].split()[1].rstrip("%")) if linhas else 0.0


def gerar(post, so, sem_conferir, minimo, tentativas):
    cfg = json.loads((post / "falas.json").read_text(encoding="utf-8"))
    vozes, modelo = {**VOZ, **cfg.get("vozes", {})}, cfg.get("modelo", MODELO)
    (post / "audio").mkdir(exist_ok=True)
    falhas = []
    for f in cfg["falas"]:
        if so and f["id"] not in so:
            continue
        saida = post / "audio" / f"{f['id']}.wav"
        for t in range(1, tentativas + 1):
            tts(f["texto"], vozes[f["lingua"]], modelo, saida, post)
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
    ap.add_argument("--minimo", type=float, default=95.0)
    ap.add_argument("--tentativas", type=int, default=3)
    a = ap.parse_args()
    post = Path(a.post).resolve()
    if a.acao == "montar":
        return montar(post)
    return gerar(post, a.so, a.sem_conferir, a.minimo, a.tentativas)


if __name__ == "__main__":
    sys.exit(main())
