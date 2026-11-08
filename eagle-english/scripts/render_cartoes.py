#!/usr/bin/env python3
"""Renderiza os cartões de um post (capa, frases, produto) em PNG 1080x1920 com texto exato.

Uso:  python3 scripts/render_cartoes.py posts/2026-11-10_salao
Saída: posts/<post>/cartoes/00_capa.png, 01_frase.png ... 99_produto.png
       (frases com e sem tradução: NN_frase.png e NN_frase_sem_traducao.png)
Requer: pip install playwright && python3 -m playwright install chromium
"""
import json, os, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

RAIZ = Path(__file__).resolve().parent.parent
TPL = RAIZ / "templates"


def render(page, template, dados, saida):
    page.add_init_script(f"window.DADOS = {json.dumps(dados, ensure_ascii=False)};")
    page.goto((TPL / template).as_uri())
    page.wait_for_load_state("networkidle")
    page.evaluate("document.fonts.ready")
    page.screenshot(path=str(saida), omit_background=True)
    print("ok", saida.relative_to(RAIZ))


def main(pasta_post):
    post = Path(pasta_post).resolve()
    dados = json.loads((post / "frases.json").read_text(encoding="utf-8"))
    frases = dados["frases"]
    out = post / "cartoes"
    out.mkdir(exist_ok=True)
    total = len(frases)
    with sync_playwright() as p:
        # CHROMIUM_PATH opcional: usar um Chromium já instalado em vez do baixado pelo Playwright
        caminho = os.environ.get("CHROMIUM_PATH")
        nav = p.chromium.launch(executable_path=caminho) if caminho else p.chromium.launch()

        def nova():
            return nav.new_page(viewport={"width": 1080, "height": 1920})

        f0 = frases[0]
        render(nova(), "card_capa.html", {"versao": dados.get("versao", dados["tema"]), **f0}, out / "00_capa.png")
        for i, f in enumerate(frases, 1):
            base = {**f, "num": f"FRASE {i} DE {total}"}
            render(nova(), "card_frase.html", base, out / f"{i:02d}_frase.png")
            render(nova(), "card_frase.html", {**base, "revelar": False}, out / f"{i:02d}_frase_sem_traducao.png")
        titulo = dados.get("titulo_produto", f"Frases de *{dados['tema']}* e muito mais")
        render(nova(), "card_produto.html", {"titulo": titulo}, out / "99_produto.png")
        nav.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
