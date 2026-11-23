#!/usr/bin/env python3
"""Carrossel "PERGAMINHO" (pedido 23/11): foto realista de pergaminho (gerada uma vez, sem texto) + texto manuscrito nosso.
posts/<post>/pergaminho.json: {"fundo": "img/pergaminho.png", "titulo": "...", "sub": "...", "frases": [{"pt","en","pron"}],
  "por_slide": 2, "cta": {"perfil": "img/perfil.png", "titulo": "...", "sub": "..."}}
Saída: slides/01.png… (1080x1440). Uso: python3 scripts/carrossel_pergaminho.py posts/<post>
"""
import json, os, sys
from pathlib import Path
PROJ = Path(__file__).resolve().parents[1]

def main(pasta):
    post = (PROJ / pasta).resolve(); c = json.load(open(post / "pergaminho.json"))
    fundo = (post / c["fundo"]).as_uri(); n = c.get("por_slide", 2)
    slides = [{"tipo": "capa", "titulo": c["titulo"], "sub": c["sub"]}]
    fr = [dict(f, n=f"{i + 1}/{len(c['frases'])}") for i, f in enumerate(c["frases"])]
    for i in range(0, len(fr), n):
        slides.append({"tipo": "frases", "frases": fr[i:i + n]})
    if c.get("cta"):
        slides.append({"tipo": "cta", "perfil": (post / c["cta"]["perfil"]).as_uri(), "titulo": c["cta"]["titulo"], "sub": c["cta"]["sub"]})
    out = post / "slides"; out.mkdir(exist_ok=True)
    for x in out.glob("*.png"): x.unlink()
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        cam = os.environ.get("CHROMIUM_PATH", "/opt/pw-browsers/chromium")
        nav = pw.chromium.launch(executable_path=cam) if os.path.isfile(cam) else pw.chromium.launch()
        pg = nav.new_page(viewport={"width": 1080, "height": 1440})
        pg.goto((PROJ / "templates" / "pergaminho.html").as_uri())
        for k, s in enumerate(slides, 1):
            pg.evaluate("window.pronto=false"); pg.evaluate("d => window.render(d)", dict(s, fundo=fundo))
            pg.wait_for_function("window.pronto === true"); pg.wait_for_timeout(250)
            pg.screenshot(path=str(out / f"{k:02d}.png"))
        nav.close()
    print(f"ok -> {len(slides)} slides em {(out).relative_to(PROJ)}")

if __name__ == "__main__":
    main(sys.argv[1])
