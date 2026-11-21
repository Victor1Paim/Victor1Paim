#!/usr/bin/env python3
"""Vídeo "CADERNO FALADO" (ref. do usuário 21/11): lista de expressões escrita à mão na folha pautada realista; a voz lê
pt → en e o marca-texto amarelo varre a linha lida; ✓ verde nas já lidas; CTA no fim. Sem personagem.

Uso: python3 scripts/montar_caderno_video.py posts/<post>
caderno_video.json: {"pagina": "img/pagina.png", "titulo": "Inglês do dia a dia", "fala_titulo": "titulo", "cta": "cta",
  "itens": [{"pt": "Com certeza", "en": "For sure", "pron": "fór xúr", "a_pt": "p1", "a_en": "e1"}, …]}
"""
import json, os, subprocess, sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from montar_quiz import SR, FPS, sh, dur  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
W, H = 1080, 1920


def pagina_916(src, saida):
    im = Image.open(src).convert("RGB"); w, h = im.size
    cw = h * W / H
    if cw > w:
        cw = w; ch = w * H / W
    else:
        ch = h
    l, t = (w - cw) / 2, (h - ch) / 2
    im.crop((int(l), int(t), int(l + cw), int(t + ch))).resize((W, H), Image.LANCZOS).save(saida, quality=95)


def pautas(arq):
    x = np.asarray(Image.open(arq).convert("RGB")).astype(float)
    ys, xs = np.nonzero((x[..., 2] - x[..., 0]) > 18)
    melhor = None
    for a in np.arange(-15, 15.01, 0.1):
        hist, _ = np.histogram(ys + xs * np.tan(np.radians(a)), bins=np.arange(-500, H + 500, 2))
        nota = (hist.astype(float) ** 2).sum()
        if melhor is None or nota > melhor[0]:
            melhor = (nota, a, hist)
    _, a, hist = melhor
    lim = hist.max() * 0.35; rh = []
    for i in range(1, len(hist) - 1):
        if hist[i] >= lim and hist[i] >= hist[i - 1] and hist[i] >= hist[i + 1]:
            r = -500 + i * 2 + 1
            if not rh or r - rh[-1] > 20:
                rh.append(r)
    return float(a), rh


def main(pasta):
    post = (PROJ / pasta).resolve(); cfg = json.loads((post / "caderno_video.json").read_text())
    v = post / "video"; v.mkdir(exist_ok=True); q = v / "quadros"; q.mkdir(exist_ok=True)
    pag = v / "_pagina.jpg"; pagina_916(post / cfg["pagina"], pag)
    ang, rh = pautas(pag); esp = float(np.median(np.diff(rh))); tg = np.tan(np.radians(ang)); x0 = 70
    n = len(cfg["itens"])
    # título na 1ª pauta com y(meio) ≥ 330; itens nas pautas seguintes (precisa caber antes de y ≈ 1560)
    ys = [r - 540 * tg for r in rh]
    k0 = next(i for i, y in enumerate(ys) if y >= 330)
    if k0 + n >= len(rh) or ys[k0 + n] > 1600:
        sys.exit(f"não cabe: {n} itens com espaçamento {esp:.0f} px — use menos itens")
    linhas = [{**it, "y": rh[k0 + 1 + i] - x0 * tg} for i, it in enumerate(cfg["itens"])]
    dados = {"fundo": pag.as_uri(), "ang": ang, "x0": x0, "esp": esp, "titulo": cfg["titulo"], "titulo_y": rh[k0] - x0 * tg, "linhas": linhas}
    aud = lambda i: post / "audio" / f"{i}.wav"
    sons, marcas, t = [], [], 0.3
    d = dur(aud(cfg["fala_titulo"])); sons.append((aud(cfg["fala_titulo"]), t)); t += d + 0.35
    for i, it in enumerate(cfg["itens"]):
        a = t
        d = dur(aud(it["a_pt"])); sons.append((aud(it["a_pt"]), t)); t += d + 0.12
        d = dur(aud(it["a_en"])); sons.append((aud(it["a_en"]), t)); t += d + cfg.get("respiro", 0.3)
        marcas.append((a, t))
    d = dur(aud(cfg["cta"])); sons.append((aud(cfg["cta"]), t + 0.2)); total = t + 0.2 + d + 0.6
    print(f"  duração: {total:.1f} s · espaçamento {esp:.0f} px · ângulo {ang:.1f}°")

    def estado(x):
        for i, (a, b) in enumerate(marcas):
            if a <= x < b:
                return {"atual": i, "varre": round(min(1, (x - a) / 0.35) * 8) / 8, "feitas": i}
        return {"atual": -1, "feitas": sum(1 for a, b in marcas if b <= x)}
    passo = 1 / 15; segs = []
    for k in range(int(total / passo) + 1):
        e = estado(k * passo); key = json.dumps(e, sort_keys=True)
        if segs and segs[-1][0] == key:
            segs[-1][2] += passo
        else:
            segs.append([key, e, passo])
    unicos = {}
    for key, _, _ in segs:
        unicos.setdefault(key, f"c{len(unicos):04d}")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        cam = os.environ.get("CHROMIUM_PATH")
        nav = pw.chromium.launch(executable_path=cam) if cam else pw.chromium.launch()
        pg = nav.new_page(viewport={"width": W, "height": H})
        pg.add_init_script(f"window.DADOS = {json.dumps(dados, ensure_ascii=False)};")
        pg.goto((PROJ / "templates" / "caderno_video.html").as_uri()); pg.wait_for_function("window.fontesOk === true")
        for key, nome in unicos.items():
            pg.evaluate("s => window.render(s)", json.loads(key)); pg.screenshot(path=str(q / f"{nome}.png"))
        pg.evaluate("s => window.render(s)", {"atual": -1, "feitas": 0}); pg.screenshot(path=str(v / "capa.png"))
        nav.close()
    lista = v / "cenas.txt"
    with open(lista, "w") as f:
        for key, _, d in segs:
            f.write(f"file '{q / (unicos[key] + '.png')}'\nduration {d:.4f}\n")
        f.write(f"file '{q / (unicos[segs[-1][0]] + '.png')}'\n")
    mudo = v / "_mudo.mp4"
    sh("-f", "concat", "-safe", "0", "-i", str(lista), "-vf", f"fps={FPS},format=yuv420p", "-c:v", "libx264", "-crf", "18", str(mudo))
    for x in q.glob("*.png"):
        x.unlink()
    ent, fil = [], []
    for k, (arq, ini) in enumerate(sons):
        ent += ["-i", str(arq)]; ms = int(round(ini * 1000))
        fil.append(f"[{k}:a]aresample={SR},aformat=channel_layouts=mono,adelay={ms}|{ms}[s{k}]")
    fil.append("".join(f"[s{k}]" for k in range(len(sons))) + f"amix=inputs={len(sons)}:normalize=0,apad=whole_dur={total:.3f},atrim=0:{total:.3f}[a]")
    bruto, audio = v / "_bruto.wav", v / "_audio.wav"
    sh(*ent, "-filter_complex", ";".join(fil), "-map", "[a]", "-ar", str(SR), str(bruto))
    alvo = "I=-14:TP=-1.5:LRA=11"
    r = subprocess.run(["ffmpeg", "-nostdin", "-i", str(bruto), "-af", f"loudnorm={alvo}:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    sh("-i", str(bruto), "-af", f"loudnorm={alvo}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
       f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,alimiter=limit=0.84:level=false", "-ar", "48000", "-ac", "2", str(audio))
    final = v / "final.mp4"
    sh("-i", str(mudo), "-i", str(audio), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(final))
    r = subprocess.run(["ffmpeg", "-nostdin", "-i", str(final), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    lufs = float(r[r.rindex("I:"):].split()[1])
    if abs(lufs + 14) > 0.5:   # o AAC/limitador deixa abaixo da meta: corrige o ganho
        tmp = final.with_name("_ganho.mp4")
        sh("-i", str(final), "-c:v", "copy", "-af", f"volume={-14 - lufs:.2f}dB,alimiter=limit=0.89:level=false",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(tmp))
        tmp.replace(final)
    sh("-i", str(final), "-vf", "fps=1/2,scale=270:480,tile=6x4", "-frames:v", "1", str(v / "contato.jpg"))
    for x in (bruto, audio, mudo, lista, pag):
        x.unlink(missing_ok=True)
    print(f"ok -> {final.relative_to(PROJ)} ({total:.1f} s)")


if __name__ == "__main__":
    main(sys.argv[1])
