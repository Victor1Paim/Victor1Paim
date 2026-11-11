#!/usr/bin/env python3
"""Imagens com o gpt-image-2 (OpenAI), custo registrado no post.

    python3 scripts/imagem_openai.py gerar  <post> <saida.png> "<prompt>" [--tam 1024x1536]
    python3 scripts/imagem_openai.py editar <post> <entrada.png> <saida.png> "<prompt>"

Na nuvem o proxy injeta a chave; no notebook, defina OPENAI_API_KEY. Nunca grave a chave no git.
"""
import base64, json, os, subprocess, sys, uuid
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "scripts"))
from custos import registrar  # noqa: E402

MODELO = "gpt-image-2"
QUAL = os.environ.get("QUALIDADE_IMAGEM", "medium")  # "high" pode passar de 30 s e o proxy corta (502)
CHAVE = os.environ.get("OPENAI_API_KEY", "proxy-injected")


def chamar(args):
    tmp = Path(f"/tmp/img-{uuid.uuid4().hex}.json")
    cod = subprocess.run(["curl", "-sS", "-m", "900", "-o", str(tmp), "-w", "%{http_code}", *args],
                         capture_output=True, text=True)
    txt = tmp.read_text() if tmp.exists() else ""
    tmp.unlink(missing_ok=True)
    try:
        return json.loads(txt)
    except json.JSONDecodeError:
        sys.exit(f"falhou (HTTP {cod.stdout}) {cod.stderr[:300]} {txt[:300]}")


def custo(post, etapa, r):
    u = r.get("usage") or {}
    det = u.get("input_tokens_details") or {}
    registrar(post, MODELO, etapa, entrada_texto=det.get("text_tokens", u.get("input_tokens", 0)),
              entrada_imagem=det.get("image_tokens", 0), saida_imagem=u.get("output_tokens", 0))


def salvar(r, saida):
    Path(saida).write_bytes(base64.b64decode(r["data"][0]["b64_json"]))
    print("ok", saida, r.get("usage"))


def gerar(post, saida, prompt, tam="1024x1536"):
    corpo = json.dumps({"model": MODELO, "prompt": prompt, "size": tam, "quality": QUAL})
    r = chamar(["https://api.openai.com/v1/images/generations", "-H", f"Authorization: Bearer {CHAVE}",
                "-H", "Content-Type: application/json", "-d", corpo])
    if "data" not in r: sys.exit(str(r)[:800])
    custo(post, f"imagem {Path(saida).stem}", r); salvar(r, saida)


def editar(post, entrada, saida, prompt):
    r = chamar(["https://api.openai.com/v1/images/edits", "-H", f"Authorization: Bearer {CHAVE}",
                "-F", f"model={MODELO}", "-F", f"image[]=@{entrada}", "-F", f"prompt={prompt}",
                "-F", f"quality={QUAL}", "-F", "size=1024x1536"])
    if "data" not in r: sys.exit(str(r)[:800])
    custo(post, f"edição {Path(saida).stem}", r); salvar(r, saida)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "gerar": gerar(Path(a[1]), a[2], a[3], *(a[5:6] if "--tam" in a else []))
    else: editar(Path(a[1]), a[2], a[3], a[4])
