#!/usr/bin/env python3
"""Stories do dia (1080x1920) no padrão dos stories do Eagle: fundo Maldivas escurecido + textos grandes + personagem.

  python3 scripts/montar_stories.py posts/<data>_stories   -> story_1.png, story_2.png...
stories.json: {"fundo_inicio": 5, "frames": [{"html": "<div class='t' ...>", "personagem": {"pose": "feliz", "pes": 1560}}, ...]}
Rotina e regras: docs/ROTINA_STORIES.md. Área segura: nada acima de y=250 nem abaixo de y=1600; ".vazio" marca onde
o usuário cola o adesivo (quiz, link, enquete, caixinha).
"""
import json, os, subprocess, sys
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]


def main(pasta):
    post = Path(pasta).resolve(); c = json.loads((post / "stories.json").read_text())
    fundos = json.loads((PROJ / "assets/fundos/maldivas.json").read_text())
    fundos = [f for i, f in enumerate(fundos) if i not in (12, 29)]   # m13/m30 têm faixa preta em cima no segundo 4
    tmp = post / "_fundos"; tmp.mkdir(exist_ok=True)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        cam = os.environ.get("CHROMIUM_PATH", "/opt/pw-browsers/chromium")
        nav = pw.chromium.launch(executable_path=cam) if os.path.isfile(cam) else pw.chromium.launch()
        for i, f in enumerate(c["frames"], 1):
            arq = PROJ / fundos[(c.get("fundo_inicio", 0) + i - 1) % len(fundos)]["arquivo"]
            jpg = tmp / f"f{i}.jpg"
            subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-ss", "4", "-i", str(arq), "-frames:v", "1", "-q:v", "2", str(jpg)], check=True)
            per = f.get("personagem")
            if per:
                per = {"pose": "feliz", "roupa": "jeans", "boca": 0, "piscar": False, "aponta": 0.15, "k": 1, **per}
            dados = {"fundo": jpg.as_uri(), "html": f["html"], "personagem": per}
            pg = nav.new_page(viewport={"width": 1080, "height": 1920})
            pg.add_init_script(f"window.DADOS = {json.dumps(dados, ensure_ascii=False)};")
            pg.goto((PROJ / "templates" / "story.html").as_uri()); pg.wait_for_selector("body[data-pronto='1']")
            pg.wait_for_load_state("networkidle"); pg.screenshot(path=str(post / f"story_{i}.png")); pg.close()
        nav.close()
    for x in tmp.glob("*"):
        x.unlink()
    tmp.rmdir()
    print(f"ok -> {len(c['frames'])} stories em {post.relative_to(PROJ)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
