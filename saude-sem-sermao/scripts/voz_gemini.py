#!/usr/bin/env python3
"""Gera narração com o Gemini TTS e confere com o Whisper (regera se não bater).

Uso: python3 saude-sem-sermao/scripts/voz_gemini.py ROTEIRO.txt SAIDA.mp3 [--voz Achird] [--minimo 97]

Chave: variável GEMINI_API_KEY (ou arquivo indicado em GEMINI_KEY_FILE). Se a chave estiver salva
no ambiente como network secret (header x-goog-api-key), use GEMINI_API_KEY=proxy-injected.
Nunca grave a chave no repositório.
Cada geração registra tokens e custo em PASTA_DO_POST/custos.jsonl (ver scripts/custos.py).

Regra aprendida em 08/11/2026: NÃO colocar instrução de tom no texto ("Say warmly: ...").
O modelo gemini-3.8-flash-tts às vezes lê a instrução em voz alta, e não aceita systemInstruction.
Sem instrução, a leitura natural já sai calorosa e bate 99% com o roteiro.
"""
import argparse, base64, json, os, subprocess, sys, tempfile, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts"))
from custos import registrar  # noqa: E402
CONFERIR = RAIZ / ".claude/skills/whisper-legendas/scripts/whisper_legendas.py"


def chave():
    if os.environ.get("GEMINI_KEY_FILE"):
        return Path(os.environ["GEMINI_KEY_FILE"]).read_text().strip()
    if os.environ.get("GEMINI_API_KEY"):
        return os.environ["GEMINI_API_KEY"]
    sys.exit("defina GEMINI_API_KEY ou GEMINI_KEY_FILE")


def limpar_final(arquivo):
    """Remove o estalo que o Gemini TTS deixa no fim do áudio (silêncio curto + pico alto nos
    últimos ~100 ms), aplica fade-out de 80 ms e deixa 0,4 s de silêncio limpo no final."""
    import numpy as np
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(arquivo), "-ac", "1", "-ar", "24000",
                          "-f", "s16le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768
    sr, jan = 24000, 240  # janelas de 10 ms
    env = np.array([np.sqrt((x[i:i + jan] ** 2).mean()) for i in range(0, len(x) - jan, jan)])
    db = 20 * np.log10(env + 1e-9)
    fim = len(db)
    # procura, no último 1,5 s, um trecho de silêncio (< -45 dB) de pelo menos 120 ms;
    # o que vem depois dele e dura menos de 0,4 s é o estalo
    ini_busca = max(0, len(db) - 150)
    i = len(db) - 1
    while i > ini_busca:
        if db[i] < -45:
            j = i
            while j > ini_busca and db[j - 1] < -45:
                j -= 1
            if i - j + 1 >= 12 and (len(db) - i) <= 40:
                fim = j + 5  # mantém 50 ms do silêncio
                break
            i = j - 1
        else:
            i -= 1
    y = x[: fim * jan].copy()
    f = min(len(y), int(0.08 * sr))
    y[-f:] *= np.linspace(1, 0, f)
    y = np.concatenate([y, np.zeros(int(0.4 * sr), dtype=np.float32)])
    pcm = (np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes()
    tmp = Path(str(arquivo) + ".tmp.mp3")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", "-",
                    "-b:a", "128k", str(tmp)], input=pcm, check=True)
    tmp.replace(arquivo)
    return (len(x) - fim * jan) / sr  # segundos removidos


def gerar(texto, voz, modelo, saida, pasta_post=None, vozes=None):
    if vozes:  # diálogo: {"Narrador": "Charon", "Tito": "Puck"}; roteiro com linhas "Nome: fala"
        fala = {"multiSpeakerVoiceConfig": {"speakerVoiceConfigs": [
            {"speaker": n, "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": v}}} for n, v in vozes.items()]}}
    else:
        fala = {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voz}}}
    if vozes:  # gemini-3.8 exige cada fala numa parte, marcada com speechMetadata.speaker
        partes = []
        for linha in texto.splitlines():
            if ":" in linha and linha.split(":", 1)[0].strip() in vozes:
                quem, frase = linha.split(":", 1)
                partes.append({"text": frase.strip(), "speechMetadata": {"speaker": quem.strip()}})
    else:
        partes = [{"text": texto}]
    body = {"contents": [{"parts": partes}],
            "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": fala}}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent",
        data=json.dumps(body).encode(), headers={"x-goog-api-key": chave(), "Content-Type": "application/json"})
    d = json.load(urllib.request.urlopen(req, timeout=180))
    u = d.get("usageMetadata", {})
    usd = registrar(pasta_post or Path(saida).parent, modelo, "voz",
                    entrada_texto=u.get("promptTokenCount", 0), saida_audio=u.get("candidatesTokenCount", 0))
    if usd is not None:
        print(f"  custo desta geração: US$ {usd:.4f}")
    pcm = base64.b64decode(d["candidates"][0]["content"]["parts"][0]["inlineData"]["data"])
    with tempfile.NamedTemporaryFile(suffix=".pcm") as f:
        f.write(pcm); f.flush()
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "s16le", "-ar", "24000", "-ac", "1",
                        "-i", f.name, "-b:a", "128k", str(saida)], check=True)
    cortado = limpar_final(saida)
    if cortado > 0.02:
        print(f"  estalo final removido ({cortado*1000:.0f} ms)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roteiro"); ap.add_argument("saida")
    ap.add_argument("--voz", default="Achird")
    ap.add_argument("--vozes", help='diálogo: "Narrador=Charon,Tito=Puck" (roteiro com linhas "Nome: fala")')
    ap.add_argument("--modelo", default="gemini-3.8-flash-tts")
    ap.add_argument("--minimo", type=float, default=97.0)
    ap.add_argument("--tentativas", type=int, default=3)
    ap.add_argument("--post", help="pasta do post onde registrar custos.jsonl (padrão: pasta da saída)")
    a = ap.parse_args()
    texto = Path(a.roteiro).read_text().strip()
    vozes = dict(p.split("=") for p in a.vozes.split(",")) if a.vozes else None
    roteiro_conf = a.roteiro
    if vozes:  # para conferir, tira o "Nome:" do começo das linhas
        import re
        limpo = "\n".join(re.sub(r"^\s*[^:]{1,20}:\s*", "", l) for l in texto.splitlines())
        roteiro_conf = str(Path(tempfile.gettempdir()) / "roteiro_sem_nomes.txt"); Path(roteiro_conf).write_text(limpo)
    saida = Path(a.saida); saida.parent.mkdir(parents=True, exist_ok=True)
    conf = saida.parent / "conferencia"
    for i in range(1, a.tentativas + 1):
        gerar(texto, a.voz, a.modelo, saida, a.post, vozes)
        r = subprocess.run([sys.executable, str(CONFERIR), str(saida), "--saida", str(conf), "--roteiro", roteiro_conf],
                           capture_output=True, text=True).stdout
        linhas = [l for l in r.splitlines() if l.startswith(("semelhança", "insert", "replace", "delete"))]
        pct = float(linhas[0].split()[1].rstrip("%")) if linhas else 0.0
        # erro nas primeiras 8 palavras (o gancho) reprova, mesmo com semelhança alta
        erro_gancho = [l for l in linhas[1:] if " pos=" in l and int(l.rsplit("pos=", 1)[1]) < 8]
        print(f"tentativa {i}: {pct}%" + ("  [ERRO NO GANCHO: " + "; ".join(erro_gancho) + "]" if erro_gancho else ""))
        if pct >= a.minimo and not erro_gancho:
            print("\n".join(linhas[1:]) or "sem diferenças")
            print(f"ok -> {saida} (legendas em {conf}/)")
            return 0
    print("REPROVADA: revise o roteiro ou troque a voz"); return 1


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "limpar":  # corrige áudios já gerados
        for arq in sys.argv[2:]:
            print(arq, f"{limpar_final(arq)*1000:.0f} ms removidos")
        sys.exit(0)
    sys.exit(main())
