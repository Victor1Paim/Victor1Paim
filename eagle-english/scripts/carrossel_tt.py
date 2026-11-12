#!/usr/bin/env python3
"""Carrossel de FOTOS (TikTok modo Foto / Instagram) a partir de posts/<post>/carrossel.json -> slides/01.png, 02.png...

carrossel.json: {"capa": {"foto": "img/capa.png", "texto": "Repita até aprender\\no inglês do dia a dia"},
                 "frases": [{"pt": "...", "en": "...", "pron": "a TÊI-bol..."}],
                 "cta": {"titulo": "Quer *2.100 frases* como essas?", "texto": "...", "botao": "Link na bio 👆"}
                        ou {"imagem": "img/perfil.png"} (print do perfil com a seta)}
1080x1440 (3:4). Pronúncia na convenção do projeto (tônica em MAIÚSCULA), tradução em pt-BR.
"""
import json, os, sys
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]


def main(pasta):
    post = Path(pasta).resolve(); c = json.loads((post / "carrossel.json").read_text())
    # a capa (foto realista com o texto) pode vir pronta do usuário: sem a foto, gera do slide 02 em diante
    foto = post / c["capa"]["foto"]
    slides = [{"tipo": "capa", "foto": foto.as_uri(), "texto": c["capa"]["texto"]}] if foto.exists() else []
    inicio = 1 if foto.exists() else 2
    slides += [{"tipo": "frase", **f} for f in c["frases"]]
    k = c["cta"]
    slides.append({"tipo": "perfil", "src": (post / k["perfil"]).as_uri(), "texto": k.get("texto", "")} if k.get("perfil") else
                  {"tipo": "imagem", "src": (post / k["imagem"]).as_uri()} if k.get("imagem") else
                  {"tipo": "cta", **k, "mascote": (PROJ / "assets/mascote/oficial/boca_fechada.png").as_uri()})
    out = post / "slides"; out.mkdir(exist_ok=True)
    for x in out.glob("*.png"):
        x.unlink()
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        cam = os.environ.get("CHROMIUM_PATH")
        nav = pw.chromium.launch(executable_path=cam) if cam else pw.chromium.launch()
        for i, s in enumerate(slides, inicio):
            pg = nav.new_page(viewport={"width": 1080, "height": 1440})
            pg.add_init_script(f"window.DADOS = {json.dumps(s, ensure_ascii=False)};")
            pg.goto((PROJ / "templates" / "carrossel_tt.html").as_uri()); pg.wait_for_selector("body[data-pronto='1']")
            pg.wait_for_load_state("networkidle"); pg.screenshot(path=str(out / f"{i:02d}.png")); pg.close()
        nav.close()
    print(f"ok -> {len(slides)} slides ({inicio:02d} a {inicio + len(slides) - 1:02d}) em {out.relative_to(PROJ)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
