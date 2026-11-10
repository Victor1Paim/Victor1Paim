#!/usr/bin/env python3
"""Bloco de anúncio UGC (afiliado) animado a partir de fotos: posts/<post>/ugc.json -> video/ugc.mp4.

ugc.json: {"cenas": [{"img": "img/1.png", "fala": "u1", "texto": "As formas vieram *daqui* 👀", "mov": "in"|"out"|"esq"|"dir",
                      "link": "Link no vídeo 👇" (opcional)}]}
Cada cena dura a fala + 0,25 s; movimento de câmera (zoom/deslize) + tremido leve de celular; corte com transição rápida
(xfade 0,2 s); camada templates/ugc.html (PUBLI, texto, aviso de IA). Voz pelas falas do falas.json (vozes.py gerar).
"""
import json, os, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from montar_quiz import SR, FPS, sh, dur, preparar_vozes  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
TRANS = ["slideleft", "smoothup", "slideright", "circleopen", "smoothleft"]


def camadas(post, cenas):
    from playwright.sync_api import sync_playwright
    out = post / "video" / "ugc_camadas"; out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        cam = os.environ.get("CHROMIUM_PATH")
        nav = pw.chromium.launch(executable_path=cam) if cam else pw.chromium.launch()
        for i, c in enumerate(cenas):
            pg = nav.new_page(viewport={"width": 1080, "height": 1920})
            pg.add_init_script(f"window.DADOS = {json.dumps(c, ensure_ascii=False)};")
            pg.goto((PROJ / "templates" / "ugc.html").as_uri()); pg.wait_for_selector("body[data-pronto='1']")
            pg.screenshot(path=str(out / f"c{i}.png"), omit_background=True); pg.close()
        nav.close()
    return out


def main(pasta):
    post = Path(pasta).resolve()
    u = json.loads((post / "ugc.json").read_text()); cenas = u["cenas"]
    vozes = preparar_vozes(post, u, 1.0)
    cam = camadas(post, cenas)
    v = post / "video"; X = 0.2
    durs = [vozes[c["fala"]][1] - 0.2 + (X if i < len(cenas) - 1 else 0.4) for i, c in enumerate(cenas)]   # fala já tem ~0,25 s de respiro nas pontas
    clipes = []
    for i, (c, d) in enumerate(zip(cenas, durs)):
        n = int(round(d * FPS)); mov = c.get("mov", "in")
        z = {"in": f"1.0+0.14*on/{n}", "out": f"1.14-0.14*on/{n}"}.get(mov, "1.12")
        x = {"esq": f"(iw-iw/zoom)*(1-on/{n})", "dir": f"(iw-iw/zoom)*on/{n}"}.get(mov, "(iw-iw/zoom)/2")
        saida = v / f"_ugc{i}.mp4"; clipes.append(saida)
        # 1024x1536 -> preenche 9:16 em 2x (zoompan suave), tremido leve de celular com crop variável
        sh("-i", str(post / c["img"]), "-loop", "1", "-i", str(cam / f"c{i}.png"), "-filter_complex",
           f"[0:v]scale=-2:3840,crop=2160:3840,zoompan=z='{z}':x='{x}':y='(ih-ih/zoom)/2':d={n}:s=1188x2112:fps={FPS},"
           f"crop=1080:1920:'54+20*sin(2*PI*t*0.7)':'96+14*sin(2*PI*t*0.9+1)',setsar=1[b];"
           f"[b][1:v]overlay=0:0,format=yuv420p[v]", "-map", "[v]", "-frames:v", str(n), "-c:v", "libx264", "-crf", "17", str(saida))
    # junta com xfade
    ent = sum((["-i", str(c)] for c in clipes), [])
    fc, ult, t = [], "[0:v]", durs[0]
    for i in range(1, len(clipes)):
        off = t - X
        fc.append(f"{ult}[{i}:v]xfade=transition={TRANS[(i - 1) % len(TRANS)]}:duration={X}:offset={off:.3f}[x{i}]")
        ult = f"[x{i}]"; t = off + durs[i]
    mudo = v / "_ugc_mudo.mp4"
    sh(*ent, "-filter_complex", ";".join(fc), "-map", ult, "-c:v", "libx264", "-crf", "17", str(mudo))
    # áudio: cada fala no começo da sua cena
    ent, fil, ini = [], [], 0.0
    for i, c in enumerate(cenas):
        arq, _ = vozes[c["fala"]]; ent += ["-i", str(arq)]; ms = int(round(max(0, ini - 0.15) * 1000))
        fil.append(f"[{i}:a]aresample={SR},aformat=channel_layouts=mono,adelay={ms}|{ms}[s{i}]"); ini += durs[i] - X
    fil.append("".join(f"[s{i}]" for i in range(len(cenas))) + f"amix=inputs={len(cenas)}:normalize=0,apad=whole_dur={t:.3f},"
               f"atrim=0:{t:.3f},loudnorm=I=-14:TP=-1.5:LRA=11,aformat=channel_layouts=stereo[a]")
    final = v / "ugc.mp4"
    sh("-i", str(mudo), *ent, "-filter_complex", ";".join(f.replace(f"[{i}:a]", f"[{i + 1}:a]") for i, f in enumerate(fil[:-1]))
       + ";" + fil[-1], "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
       "-movflags", "+faststart", str(final))
    for c in clipes + [mudo]:
        c.unlink()
    r = subprocess.run(["ffmpeg", "-nostdin", "-i", str(final), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    lufs = float(r[r.rindex("I:"):].split()[1])
    if abs(lufs + 14) > 0.5:   # loudnorm de uma passada fica abaixo da meta em trechos curtos
        tmp = final.with_name("_g.mp4")
        sh("-i", str(final), "-c:v", "copy", "-af", f"volume={-14 - lufs:.2f}dB,alimiter=limit=0.89:level=false", "-c:a", "aac",
           "-b:a", "192k", "-movflags", "+faststart", str(tmp)); tmp.replace(final)
    print(f"ok -> {final.relative_to(PROJ)}  ({dur(final):.1f} s)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
