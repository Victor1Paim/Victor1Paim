#!/usr/bin/env python3
"""Anima uma imagem em vídeo com o Gemini Omni (Interactions API) e registra o custo.

Uso: python3 scripts/video_omni.py IMAGEM "PROMPT" SAIDA.mp4 --post posts/<post> [--modelo gemini-omni-1.2-flash]
Chave: OMNI_KEY_FILE (arquivo) ou GEMINI_KEY_FILE/GEMINI_API_KEY. Sai ~4 s, 720x1280, 24 fps, com som ambiente.
Preço (10/11/2026): US$ 12 por 1M tokens de vídeo, 5.792 tokens/s em 720p (~US$ 0,07/s). O fim do clipe às vezes deforma:
usar os 2–3 s iniciais.
"""
import argparse, base64, io, json, os, sys, time, urllib.request, urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from custos import registrar  # noqa: E402


def chave():
    for v in ("OMNI_KEY_FILE", "GEMINI_KEY_FILE"):
        if os.environ.get(v) and Path(os.environ[v]).exists():
            return Path(os.environ[v]).read_text().strip()
    return os.environ.get("GEMINI_API_KEY", "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("imagem"); ap.add_argument("prompt"); ap.add_argument("saida")
    ap.add_argument("--post", required=True); ap.add_argument("--modelo", default="gemini-omni-1.2-flash")
    a = ap.parse_args()
    from PIL import Image
    im = Image.open(a.imagem).convert("RGB"); im.thumbnail((768, 1152))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=90)
    body = {"model": a.modelo, "response_modalities": ["video"],
            "input": [{"type": "text", "text": a.prompt},
                      {"type": "image", "data": base64.b64encode(buf.getvalue()).decode(), "mime_type": "image/jpeg"}]}
    req = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/interactions", data=json.dumps(body).encode(),
                                 headers={"x-goog-api-key": chave(), "Content-Type": "application/json"})
    for tentativa in range(3):
        try:
            d = json.load(urllib.request.urlopen(req, timeout=900)); break
        except urllib.error.HTTPError as e:
            msg = e.read()[:300].decode(errors="ignore")
            if e.code not in (429, 500, 502, 503, 504) or tentativa == 2:
                sys.exit(f"erro {e.code}: {msg}")
            print(f"  erro {e.code}; tentando de novo...", flush=True); time.sleep(20)
    u = d.get("usage", {})
    ent = {m["modality"]: m["tokens"] for m in u.get("input_tokens_by_modality", [])}
    sai = {m["modality"]: m["tokens"] for m in u.get("output_tokens_by_modality", [])}
    usd = registrar(a.post, a.modelo, "video", entrada_texto=ent.get("text", 0), entrada_imagem=ent.get("image", 0),
                    saida_texto=u.get("total_thought_tokens", 0) + sai.get("text", 0), saida_video=sai.get("video", 0))
    for s in d.get("steps", []):
        for c in s.get("content", []) or []:
            if c.get("type") == "video":
                Path(a.saida).parent.mkdir(parents=True, exist_ok=True)
                Path(a.saida).write_bytes(base64.b64decode(c["data"]))
                print(f"ok {a.saida} (US$ {usd:.3f})"); return
    sys.exit("sem vídeo na resposta: " + json.dumps(d)[:400])


if __name__ == "__main__":
    main()
