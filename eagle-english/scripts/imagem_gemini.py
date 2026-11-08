#!/usr/bin/env python3
"""Gera uma imagem (fundo de cena, mascote) com a OpenAI (padrão, gpt-image-2) ou o Gemini e registra o custo.

O Gemini no plano gratuito não libera imagem (erro 429, limite 0); por isso o padrão é a OpenAI,
cuja chave é injetada pelo proxy do ambiente (no notebook: OPENAI_API_KEY no .env).

Uso:
  python3 scripts/imagem_gemini.py "PROMPT" SAIDA.png --post posts/<post> [--proporcao 9:16] [--ref ref.png]
  --verde: personagem recortado (PNG com transparência), para o mascote.
--modelo gemini-2.5-flash-image: usa o Gemini (precisa de plano pago).

Texto em imagem: NÃO pedir texto ao gerador; o texto entra depois pelos templates HTML.
Chave: GEMINI_API_KEY / GEMINI_KEY_FILE (ver scripts/vozes.py).
"""
import argparse, base64, json, sys, urllib.request
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJ.parent / "scripts"))
sys.path.insert(0, str(PROJ / "scripts"))
from custos import registrar  # noqa: E402
from vozes import carregar_env, chave  # noqa: E402

MODELO = "gpt-image-2"
QUALIDADE = "medium"  # "high" pode passar do tempo do proxy (erro 502)
TAMANHO = {"9:16": "1024x1536", "1:1": "1024x1024", "3:4": "1024x1536", "16:9": "1536x1024"}


def gerar_openai(prompt, saida, post, proporcao, transparente, modelo):
    import os
    body = {"model": modelo, "prompt": prompt, "size": TAMANHO.get(proporcao, "1024x1536"), "quality": QUALIDADE, "n": 1}
    if transparente:
        body["background"] = "transparent"; body["output_format"] = "png"
    req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=json.dumps(body).encode(),
                                 headers={"Authorization": "Bearer " + os.environ.get("OPENAI_API_KEY", "proxy-injected"),
                                          "Content-Type": "application/json"})
    d = json.load(urllib.request.urlopen(req, timeout=600))
    u = d.get("usage", {})
    det = u.get("input_tokens_details", {})
    registrar(post, modelo, "imagem", entrada_texto=det.get("text_tokens", u.get("input_tokens", 0)),
              entrada_imagem=det.get("image_tokens", 0), saida_imagem=u.get("output_tokens", 0))
    Path(saida).parent.mkdir(parents=True, exist_ok=True)
    Path(saida).write_bytes(base64.b64decode(d["data"][0]["b64_json"]))
    return saida


def gerar(prompt, saida, post, proporcao="9:16", ref=None, modelo=MODELO):
    partes = [{"text": prompt}]
    if ref:
        partes.append({"inlineData": {"mimeType": "image/png", "data": base64.b64encode(Path(ref).read_bytes()).decode()}})
    body = {"contents": [{"parts": partes}],
            "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": proporcao}}}
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent",
        data=json.dumps(body).encode(), headers={"x-goog-api-key": chave(), "Content-Type": "application/json"})
    d = json.load(urllib.request.urlopen(req, timeout=300))
    u = d.get("usageMetadata", {})
    registrar(post, modelo, "imagem", entrada_texto=u.get("promptTokenCount", 0),
              saida_imagem=u.get("candidatesTokenCount", 0))
    for p in d["candidates"][0]["content"]["parts"]:
        if "inlineData" in p:
            Path(saida).parent.mkdir(parents=True, exist_ok=True)
            Path(saida).write_bytes(base64.b64decode(p["inlineData"]["data"]))
            return saida
    sys.exit("o modelo não devolveu imagem: " + json.dumps(d)[:500])


def recortar_verde(arq):
    """Remove o fundo verde (chroma key) e deixa uma borda suave."""
    import numpy as np
    from PIL import Image, ImageFilter
    im = Image.open(arq).convert("RGBA")
    a = np.array(im).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    verde = (g > 120) & (g > r * 1.35) & (g > b * 1.35)
    alfa = np.where(verde, 0, 255).astype("uint8")
    mask = Image.fromarray(alfa).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1))
    # tira o reflexo verde das bordas
    a[..., 1] = np.where(~verde & (g > r) & (g > b), np.maximum(r, b), g)
    out = Image.fromarray(a.astype("uint8"), "RGBA")
    out.putalpha(mask)
    bbox = out.getbbox()
    out.crop(bbox).save(arq)


def main():
    carregar_env()
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt"); ap.add_argument("saida")
    ap.add_argument("--post", required=True)
    ap.add_argument("--proporcao", default="9:16")
    ap.add_argument("--ref")
    ap.add_argument("--verde", action="store_true")
    ap.add_argument("--modelo", default=MODELO)
    a = ap.parse_args()
    prompt = a.prompt
    if a.verde:  # gpt-image-2 não aceita background=transparent: fundo verde + recorte
        prompt += (" Place the character alone on a perfectly flat, solid pure green background (#00FF00), "
                   "no shadow on the background, no floor, no other objects, no text.")
    if a.modelo.startswith("gpt"):
        gerar_openai(prompt, a.saida, a.post, a.proporcao, False, a.modelo)
    else:
        gerar(prompt, a.saida, a.post, a.proporcao, a.ref, a.modelo)
    if a.verde:
        recortar_verde(a.saida)
    print("ok", a.saida)


if __name__ == "__main__":
    main()
