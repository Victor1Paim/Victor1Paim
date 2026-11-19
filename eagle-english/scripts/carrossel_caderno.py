#!/usr/bin/env python3
"""Carrossel "CADERNO" (realismo, ref. do usuário 19/11): foto realista de folha pautada (gerada UMA vez, sem texto) +
frase "escrita à mão" por cima, seguindo a inclinação e o espaçamento das pautas detectados na foto.
Texto exato (fonte manuscrita, nunca escrito pelo gerador de imagem). Cores de caneta: rótulo azul, frase preta, pronúncia vermelha.

Uso: python3 scripts/carrossel_caderno.py posts/<post>
posts/<post>/caderno.json:
{ "pagina": "img/pagina.png", "zoom": 1.6, "marca": "@eagle.english.br",
  "frases": [{"pt": "Tô morrendo de fome!", "en": "I'm starving!", "pron": "áim STÁR-vin!"}, …],
  "cta": {"perfil": "img/perfil.png", "texto": "…"} }      # opcional: último slide = CTA do perfil (carrossel_tt)
Saída: posts/<post>/slides/01.png … (1080x1440).
"""
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

import numpy as np
from PIL import Image

PROJ = Path(__file__).resolve().parents[1]
W, H = 1080, 1440


def preparar_pagina(src, zoom, saida):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    cw = w / zoom; ch = cw * H / W
    if ch > h:
        ch = h; cw = ch * W / H
    l, t = (w - cw) / 2, (h - ch) / 2
    im.crop((int(l), int(t), int(l + cw), int(t + ch))).resize((W, H), Image.LANCZOS).save(saida, quality=95)
    return saida


def pautas(arq):
    """Ângulo (graus, + = sobe para a direita) e posições das pautas: y(x) = rho - x*tan(a)."""
    x = np.asarray(Image.open(arq).convert("RGB")).astype(float)
    azul = (x[..., 2] - x[..., 0]) > 18
    ys, xs = np.nonzero(azul)
    melhor = None
    for a in np.arange(-15, 15.01, 0.1):
        rho = ys + xs * np.tan(np.radians(a))
        hist, _ = np.histogram(rho, bins=np.arange(-400, H + 400, 2))
        nota = (hist.astype(float) ** 2).sum()
        if melhor is None or nota > melhor[0]:
            melhor = (nota, a, hist)
    _, a, hist = melhor
    # picos do histograma = pautas
    lim = hist.max() * 0.35; picos = []
    for i in range(1, len(hist) - 1):
        if hist[i] >= lim and hist[i] >= hist[i - 1] and hist[i] >= hist[i + 1]:
            r = -400 + i * 2 + 1
            if not picos or r - picos[-1] > 20:
                picos.append(r)
    return float(a), picos


def main(pasta):
    post = (PROJ / pasta).resolve()
    cfg = json.loads((post / "caderno.json").read_text())
    out = post / "slides"; out.mkdir(exist_ok=True)
    pag = preparar_pagina(post / cfg["pagina"], cfg.get("zoom", 1.6), post / "img" / "_pagina_1080.jpg")
    ang, rhos = pautas(pag)
    esp = float(np.median(np.diff(rhos)))
    print(f"  pautas: ângulo {ang:.1f}°, espaçamento {esp:.0f} px, {len(rhos)} linhas")
    tg = np.tan(np.radians(ang))
    # 3 linhas de texto em pautas consecutivas, um pouco acima do meio da página (como na referência)
    alvo = H * 0.47 + 540 * tg   # y da pauta no meio da largura
    k = int(np.argmin([abs(r - 540 * tg - alvo) for r in rhos]))
    base = rhos[k - 1:k + 2]
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        cam = os.environ.get("CHROMIUM_PATH")
        nav = pw.chromium.launch(executable_path=cam) if cam else pw.chromium.launch()
        for i, f in enumerate(cfg["frases"], 1):
            d = {"fundo": pag.as_uri(), "ang": ang, "x0": 62, "linhas": [
                    {"rot": "Português:", "txt": f["pt"], "y": base[0] - 62 * tg, "cor": "#111"},
                    {"rot": "Inglês:", "txt": f["en"], "y": base[1] - 62 * tg, "cor": "#111"},
                    {"rot": "Pronúncia:", "txt": f["pron"], "y": base[2] - 62 * tg, "cor": "#C8143C", "cor_rot": "#C8143C"}],
                 "marca": cfg.get("marca", "@eagle.english.br"), "esp": esp, "semente": i}
            pg = nav.new_page(viewport={"width": W, "height": H})
            pg.add_init_script(f"window.DADOS = {json.dumps(d, ensure_ascii=False)};")
            pg.goto((PROJ / "templates" / "caderno.html").as_uri())
            pg.wait_for_selector("body[data-pronto='1']")
            pg.screenshot(path=str(out / f"{i:02d}.png")); pg.close()
        nav.close()
    n = len(cfg["frases"])
    if cfg.get("cta"):   # slide de CTA igual ao dos outros carrosséis (perfil com moldura vermelha)
        tmp = Path(tempfile.mkdtemp(dir=post))
        (tmp / "img").mkdir()
        shutil.copy(post / cfg["cta"]["perfil"], tmp / "img" / Path(cfg["cta"]["perfil"]).name)
        (tmp / "carrossel.json").write_text(json.dumps({"capa": {"foto": "img/_nao_existe.png", "texto": ""}, "frases": [], "cta": cfg["cta"]}, ensure_ascii=False))
        subprocess.run([sys.executable, str(PROJ / "scripts" / "carrossel_tt.py"), str(tmp)], check=True,
                       capture_output=True)
        ult = sorted((tmp / "slides").glob("*.png"))[-1]
        shutil.copy(ult, out / f"{n + 1:02d}.png"); shutil.rmtree(tmp)
    pag.unlink()
    print(f"ok -> {len(list(out.glob('*.png')))} slides em {out.relative_to(PROJ)}")


if __name__ == "__main__":
    main(sys.argv[1])
