#!/usr/bin/env python3
"""Abertura animada (motion graphics) no estilo da capa: templates/abertura.html renderizado quadro a quadro (30 fps).

Config (em flash.json/roteiro.json, chave "abertura"):
{"audio": "intro", "fundo": "img/fundo_cta.png", "selo": "Desafio 🧠", "titulo": "Frutas em\\n*inglês* 🍎",
 "sub": "<b>8 frutas</b> · 3 segundos cada", "desafio": "Fala antes da resposta! 👇",
 "figuras": [{"img": "img/apple.png", "txt": "?"}, ...]}          # até 6 figuras
Uso direto (prévia):  python3 scripts/abertura.py posts/<post> [flash.json]
"""
import json, os, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
PROJ = Path(__file__).resolve().parents[1]
MASC = PROJ / "assets" / "mascote" / "oficial"
FPS = 30


def render_abertura(post, cfg, voz, ini_voz=0.15, saida=0.6):
    """voz = (arquivo, duração). Devolve (lista de PNGs, duração em s)."""
    import montar_padrao
    from playwright.sync_api import sync_playwright
    dur = round(ini_voz + voz[1] + 0.25 + saida, 2)
    boca = montar_padrao.boca_aberta([(voz[0], ini_voz, 1.0)], dur)
    dados = {**cfg, "fundo": (post / cfg["fundo"]).as_uri(), "duracao": dur, "boca": boca,
             "mascote_f": (MASC / "boca_fechada.png").as_uri(), "mascote_a": (MASC / "boca_aberta.png").as_uri(),
             "figuras": [{**f, "img": (post / f["img"]).as_uri()} for f in cfg.get("figuras", [])]}
    pasta = post / "video" / "abertura"; pasta.mkdir(parents=True, exist_ok=True)
    for x in pasta.glob("*.png"):
        x.unlink()
    n = int(round(dur * FPS)); quadros = []
    with sync_playwright() as pw:
        cam = os.environ.get("CHROMIUM_PATH")
        nav = pw.chromium.launch(executable_path=cam) if cam else pw.chromium.launch()
        pg = nav.new_page(viewport={"width": 1080, "height": 1920})
        pg.add_init_script(f"window.DADOS = {json.dumps(dados, ensure_ascii=False)};")
        pg.goto((PROJ / "templates" / "abertura.html").as_uri())
        pg.wait_for_selector("body[data-pronto='1']"); pg.wait_for_load_state("networkidle")
        for i in range(n):
            pg.evaluate(f"window.quadro({i / FPS:.4f})")
            q = pasta / f"q{i:04d}.png"; pg.screenshot(path=str(q), type="png"); quadros.append(q)
        nav.close()
    return quadros, n / FPS


if __name__ == "__main__":
    from montar_quiz import preparar_vozes
    post = Path(sys.argv[1]).resolve()
    c = json.loads((post / (sys.argv[2] if len(sys.argv) > 2 else "flash.json")).read_text())
    v = preparar_vozes(post, c, 1.0)
    qs, d = render_abertura(post, c["abertura"], v[c["abertura"]["audio"]])
    print(len(qs), "quadros,", d, "s")
