#!/usr/bin/env python3
"""Carrossel "INICIANTE × NATIVO" (ref. do usuário 25/11, estilo "A1 × C1" com o personagem próprio).

  python3 scripts/carrossel_nativo.py posts/<post>      (lê posts/<post>/nativo.json)
nativo.json: {"capa": {"sub": "...", "prop": "🇺🇸"},
              "pares": [{"ini": {"en": "It's very easy.", "pron": "its véri ízi", "pt": "É muito fácil.", "pose": "pensando", "prop": "📚"},
                         "nat": {"en": "It's a piece of cake!", "pron": "...", "pt": "É moleza!", "pose": "feliz", "prop": "🍰"}}, ...],
              "cta": {"perfil": "img/perfil.jpg", "fundo": "#0c0f14", "texto": "..."}}
Poses: neutro, pensando, feliz, triste, confiante, fala1..4. Saída: slides/01.png (capa) … pares … último = print do perfil.
"""
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]


def main(pasta):
    post = Path(pasta).resolve(); c = json.loads((post / "nativo.json").read_text())
    out = post / "slides"; out.mkdir(exist_ok=True)
    for x in out.glob("*.png"):
        x.unlink()
    total = len(c["pares"]) + 2
    slides = [{"tipo": "capa", **c.get("capa", {})}] + [{"tipo": "par", "n": f"{i + 2}/{total}", **p} for i, p in enumerate(c["pares"])]
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        cam = os.environ.get("CHROMIUM_PATH", "/opt/pw-browsers/chromium")
        nav = pw.chromium.launch(executable_path=cam) if os.path.isfile(cam) else pw.chromium.launch()
        for i, s in enumerate(slides, 1):
            pg = nav.new_page(viewport={"width": 1080, "height": 1440})
            pg.add_init_script(f"window.DADOS = {json.dumps(s, ensure_ascii=False)};")
            pg.goto((PROJ / "templates" / "nativo.html").as_uri()); pg.wait_for_selector("body[data-pronto='1']")
            pg.wait_for_load_state("networkidle"); pg.screenshot(path=str(out / f"{i:02d}.png")); pg.close()
        nav.close()
    if c.get("cta"):   # último slide = print do perfil (mesmo dos outros carrosséis)
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
