#!/usr/bin/env python3
"""Capa PRODUZIDA do Reel/TikTok (templates/capa.html) a partir de posts/<post>/capa.json.

Uso:  python3 scripts/capa.py posts/<post> [posts/<outro> ...]   -> video/capa.png (1080x1920)
capa.json:
{"fundo": "img/cama.png", "selo": "6 frases", "titulo": "Inglês antes de *dormir* 🌙",
 "sub": "Repete comigo · <b>A1</b>", "balao": {"en": "Sweet dreams!", "pron": "/SUÍIT DRÍIMZ/", "lado": "dir"},
 "figuras": [{"img": "img/apple.png", "txt": "?"}]}       # figuras opcionais (até 4), em volta do mascote
Título: *palavra* = amarelo, _palavra_ = verde, \\n = quebra. Mascote oficial (boca fechada) grande no centro.
"""
import json, os, sys
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]


def capas(pastas):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        cam = os.environ.get("CHROMIUM_PATH")
        nav = pw.chromium.launch(executable_path=cam) if cam else pw.chromium.launch()
        for pasta in pastas:
            post = Path(pasta).resolve()
            c = json.loads((post / "capa.json").read_text())
            c["fundo"] = (post / c["fundo"]).as_uri()
            c["mascote"] = (PROJ / "assets/mascote/oficial/boca_fechada.png").as_uri()
            for f in c.get("figuras", []):
                f["img"] = (post / f["img"]).as_uri()
            pg = nav.new_page(viewport={"width": 1080, "height": 1920})
            pg.add_init_script(f"window.DADOS = {json.dumps(c, ensure_ascii=False)};")
            pg.goto((PROJ / "templates" / "capa.html").as_uri())
            pg.wait_for_selector("body[data-pronto='1']"); pg.wait_for_load_state("networkidle")
            (post / "video").mkdir(exist_ok=True)
            pg.screenshot(path=str(post / "video" / "capa.png")); pg.close()
            print("ok ->", (post / "video" / "capa.png").relative_to(PROJ))
        nav.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    capas(sys.argv[1:])
