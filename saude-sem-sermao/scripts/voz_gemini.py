#!/usr/bin/env python3
"""Gera narração com o Gemini TTS e confere com o Whisper (regera se não bater).

Uso: python3 saude-sem-sermao/scripts/voz_gemini.py ROTEIRO.txt SAIDA.mp3 [--voz Achird] [--minimo 97]

Chave: variável GEMINI_API_KEY (ou arquivo indicado em GEMINI_KEY_FILE). Se a chave estiver salva
no ambiente como network secret (header x-goog-api-key), use GEMINI_API_KEY=proxy-injected.
Nunca grave a chave no repositório.

Regra aprendida em 08/11/2026: NÃO colocar instrução de tom no texto ("Say warmly: ...").
O modelo gemini-3.8-flash-tts às vezes lê a instrução em voz alta, e não aceita systemInstruction.
Sem instrução, a leitura natural já sai calorosa e bate 99% com o roteiro.
"""
import argparse, base64, json, os, subprocess, sys, tempfile, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
CONFERIR = RAIZ / ".claude/skills/whisper-legendas/scripts/whisper_legendas.py"


def chave():
    if os.environ.get("GEMINI_KEY_FILE"):
        return Path(os.environ["GEMINI_KEY_FILE"]).read_text().strip()
    if os.environ.get("GEMINI_API_KEY"):
        return os.environ["GEMINI_API_KEY"]
    sys.exit("defina GEMINI_API_KEY ou GEMINI_KEY_FILE")


def gerar(texto, voz, modelo, saida):
    body = {"contents": [{"parts": [{"text": texto}]}],
            "generationConfig": {"responseModalities": ["AUDIO"],
                                 "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voz}}}}}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent",
        data=json.dumps(body).encode(), headers={"x-goog-api-key": chave(), "Content-Type": "application/json"})
    d = json.load(urllib.request.urlopen(req, timeout=180))
    pcm = base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
    with tempfile.NamedTemporaryFile(suffix=".pcm") as f:
        f.write(pcm); f.flush()
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", "24000", "-ac", "1",
                        "-i", f.name, "-b:a", "128k", str(saida)], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roteiro"); ap.add_argument("saida")
    ap.add_argument("--voz", default="Achird")
    ap.add_argument("--modelo", default="gemini-3.8-flash-tts")
    ap.add_argument("--minimo", type=float, default=97.0)
    ap.add_argument("--tentativas", type=int, default=3)
    a = ap.parse_args()
    texto = Path(a.roteiro).read_text().strip()
    saida = Path(a.saida); saida.parent.mkdir(parents=True, exist_ok=True)
    conf = saida.parent / "conferencia"
    for i in range(1, a.tentativas + 1):
        gerar(texto, a.voz, a.modelo, saida)
        r = subprocess.run([sys.executable, str(CONFERIR), str(saida), "--saida", str(conf), "--roteiro", a.roteiro],
                           capture_output=True, text=True).stdout
        linhas = [l for l in r.splitlines() if l.startswith(("semelhança", "insert", "replace", "delete"))]
        pct = float(linhas[0].split()[1].rstrip("%")) if linhas else 0.0
        print(f"tentativa {i}: {pct}%")
        if pct >= a.minimo:
            print("\n".join(linhas[1:]) or "sem diferenças")
            print(f"ok -> {saida} (legendas em {conf}/)")
            return 0
    print("REPROVADA: revise o roteiro ou troque a voz"); return 1


if __name__ == "__main__":
    sys.exit(main())
