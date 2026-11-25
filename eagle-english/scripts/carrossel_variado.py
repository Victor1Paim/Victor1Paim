#!/usr/bin/env python3
"""Carrosséis variados (25/11): "igual" (A pronúncia é igual!), "confunda" (Não confunda! falsos cognatos),
"pronuncia" (Pronúncia certa ✗/✓) e "vocab" (Vocabulário com emoji, 6 por slide).

  python3 scripts/carrossel_variado.py posts/<post>     (lê posts/<post>/variado.json)
variado.json: {"tipo": "igual|confunda|pronuncia|vocab", "capa": {"titulo": "A PRONÚNCIA\n*É IGUAL!*", "sub": "...", "emojis": "8️⃣🍽️"},
  igual:     "pares": [{"a": {"emoji","en","pt"}, "b": {...}, "som": "êit"}]
  confunda:  "pares": [{"a": {"emoji","en","pt","pron"}, "b": {...}, "nota": "*Push* não é puxar!"}]
  pronuncia: "palavras": [{"emoji","en","pt","errado","certo"}]
  vocab:     "titulo": "A COZINHA *EM INGLÊS*", "itens": [{"emoji","en","pt","pron"}] (6 por slide)
  "cta": {"perfil": "img/perfil.jpg", "fundo": "#0c0f14", "texto": "..."}}
Saída: slides/01.png (capa) … último = print do perfil. Template: templates/variado.html.
"""
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
TITULO = {"igual": "A pronúncia *é igual!*", "confunda": "Não *confunda!*", "pronuncia": "Pare de falar *errado!*"}


def main(pasta):
    post = Path(pasta).resolve(); c = json.loads((post / "variado.json").read_text()); t = c["tipo"]
    if t in ("igual", "confunda"):
        corpo = [{"tipo": "par", "titulo": TITULO[t], **p} for p in c["pares"]]
    elif t == "pronuncia":
        corpo = [{"tipo": "pron", "titulo": TITULO[t], **p} for p in c["palavras"]]
    else:
        it = c["itens"]; corpo = [{"tipo": "vocab", "titulo": c["titulo"], "itens": it[i:i + 6]} for i in range(0, len(it), 6)]
    total = len(corpo) + 2
    slides = [{"tipo": "capa", **c["capa"]}] + [{**s, "n": f"{i + 2}/{total}"} for i, s in enumerate(corpo)]
    out = post / "slides"; out.mkdir(exist_ok=True)
    for x in out.glob("*.png"):
        x.unlink()
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        cam = os.environ.get("CHROMIUM_PATH", "/opt/pw-browsers/chromium")
        nav = pw.chromium.launch(executable_path=cam) if os.path.isfile(cam) else pw.chromium.launch()
        for i, s in enumerate(slides, 1):
            pg = nav.new_page(viewport={"width": 1080, "height": 1440})
            pg.add_init_script(f"window.DADOS = {json.dumps(s, ensure_ascii=False)};")
            pg.goto((PROJ / "templates" / "variado.html").as_uri()); pg.wait_for_selector("body[data-pronto='1']")
            pg.wait_for_load_state("networkidle"); pg.screenshot(path=str(out / f"{i:02d}.png")); pg.close()
        nav.close()
    if c.get("cta"):
        tmp = Path(tempfile.mkdtemp(dir=post)); (tmp / "img").mkdir()
        shutil.copy(post / c["cta"]["perfil"], tmp / "img" / Path(c["cta"]["perfil"]).name)
        (tmp / "carrossel.json").write_text(json.dumps({"capa": {"foto": "img/_nao_existe.png", "texto": ""}, "frases": [], "cta": c["cta"]}, ensure_ascii=False))
        subprocess.run([sys.executable, str(PROJ / "scripts" / "carrossel_tt.py"), str(tmp)], check=True, capture_output=True)
        shutil.copy(sorted((tmp / "slides").glob("*.png"))[-1], out / f"{total:02d}.png"); shutil.rmtree(tmp)
    print(f"ok -> {len(list(out.glob('*.png')))} slides em {out.relative_to(PROJ)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
