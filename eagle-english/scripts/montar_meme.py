#!/usr/bin/env python3
"""Post "MEME" (ref. do usuário 25/11, estilo de perfil de inglês viral): fundo preto, cabeçalho do perfil, frase de gancho,
trecho curto de vídeo (16:9) no meio, legenda opcional e faixa do Eagle Primeira Classe entrando no meio do vídeo.

  python3 scripts/montar_meme.py posts/<post>      (lê posts/<post>/meme.json)
meme.json: {"clipe": "brutos/x.mp4", "ini": 12.0, "fim": 23.5, "gancho": "POV: você e seu amigo falando inglês",
            "faixa": "Inglês do jeito fácil: 10 aulas + 2.100 frases com pronúncia escrita", "faixa_em": 0.45,
            "legendas": [[0.0, 1.2, "Really?", "Sério?"], ...]   (opcional: tempo relativo ao corte, en, pt)
            "crop": "iw:iw*9/16"  (opcional: recorte do clipe antes de escalar; padrão = centro 16:9) }
Saída: video/final.mp4 + video/capa.png. Crédito do vídeo original vai na LEGENDA do post (legenda.md).
"""
import json, os, subprocess, sys
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]

def medidas(post, c):
    """Recorte (w,h,x,y) do clipe e o tamanho/posição dele na tela: 16:9 ocupa 1080 de largura; 4:3 ou mais alto, 960."""
    if c.get("crop"):
        cw, ch, cx, cy = [int(v) for v in c["crop"].split(":")]
    else:
        out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-of", "csv=p=0",
                              str(post / c["clipe"])], capture_output=True, text=True).stdout.strip().split(",")
        cw, ch, cx, cy = int(out[0]), int(out[1]), 0, 0
    r = cw / ch
    W = 1080 if r >= 1.5 else 960
    H = int(round(W / r / 2) * 2)
    Y = 640 if H <= 700 else 600
    return (cw, ch, cx, cy), W, H, Y


def sh(*a):
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", *a], check=True)


def png(dados, saida):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        cam = os.environ.get("CHROMIUM_PATH", "/opt/pw-browsers/chromium")
        nav = pw.chromium.launch(executable_path=cam) if os.path.isfile(cam) else pw.chromium.launch()
        pg = nav.new_page(viewport={"width": 1080, "height": 1920})
        pg.add_init_script(f"window.DADOS = {json.dumps(dados, ensure_ascii=False)};")
        pg.goto((PROJ / "templates" / "meme.html").as_uri()); pg.wait_for_selector("body[data-pronto='1']")
        pg.wait_for_load_state("networkidle"); pg.screenshot(path=str(saida), omit_background=True); nav.close()


def main(pasta):
    post = Path(pasta).resolve(); c = json.loads((post / "meme.json").read_text()); v = post / "video"; v.mkdir(exist_ok=True)
    tmp = post / "_tmp"; tmp.mkdir(exist_ok=True)
    (cw, ch, cx, cy), W, H, Y = medidas(post, c); Y_FAIXA = Y + H + 40; X = (1080 - W) // 2
    png({"modo": "base", "gancho": c["gancho"], "y": Y, "h": H, "x": X, "w": W, "logo": (PROJ / "assets/marca/logo_eagle.png").as_uri()}, tmp / "base.png")
    png({"modo": "faixa", "texto": c.get("faixa", "Inglês do jeito fácil: 10 aulas + 2.100 frases com pronúncia escrita"),
         "y_faixa": Y_FAIXA, "produto": (PROJ / "assets/meme/produto.png").as_uri()}, tmp / "faixa.png")
    ini, fim = float(c["ini"]), float(c["fim"]); dur = fim - ini; tf = dur * float(c.get("faixa_em", 0.45))
    # legendas (opcional) como drawtext não: renderiza cada uma em PNG pelo mesmo template seria pesado; usamos ASS simples
    filtros = [f"[0:v]crop={cw}:{ch}:{cx}:{cy},scale={W}:{H},setsar=1,fps=30[clip]",
               "color=black:s=1080x1920:r=30[bg]", f"[bg][clip]overlay={X}:{Y}:shortest=1[a]",
               "[a][1:v]overlay=0:0[b]",
               f"[2:v]format=rgba,fade=t=in:st={tf:.2f}:d=0.35:alpha=1[fx]", f"[b][fx]overlay=0:0:enable='gte(t,{tf:.2f})'[c]"]
    ultimo = "c"
    if c.get("legendas"):
        ass = tmp / "leg.ass"
        linhas = ["[Script Info]", "PlayResX: 1080", "PlayResY: 1920", "", "[V4+ Styles]",
                  "Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, BorderStyle, Outline, Shadow, Alignment, MarginV",
                  "Style: en,Inter,72,&H0000D2FF,&H00000000,&H64000000,1,1,6,0,2,0", "Style: pt,Inter,52,&H00FFFFFF,&H00000000,&H64000000,1,1,5,0,2,0",
                  "", "[Events]", "Format: Layer, Start, End, Style, Text"]
        t = lambda s: f"{int(s // 3600)}:{int(s % 3600 // 60):02d}:{s % 60:05.2f}"
        for a, b, en, pt in c["legendas"]:
            # inglês em cima (se quebrar linha, cresce para cima) e tradução embaixo, sem encavalar
            linhas.append(f"Dialogue: 0,{t(a)},{t(b)},en,{{\\pos(540,{Y + H - (95 if pt else 40)})}}{en}")
            if pt:
                linhas.append(f"Dialogue: 0,{t(a)},{t(b)},pt,{{\\pos(540,{Y + H - 30})}}{pt}")
        ass.write_text("\n".join(linhas))
        filtros.append(f"[c]ass={ass}[d]"); ultimo = "d"
    sh("-ss", f"{ini:.2f}", "-t", f"{dur:.2f}", "-i", str(post / c["clipe"]), "-loop", "1", "-i", str(tmp / "base.png"),
       "-loop", "1", "-i", str(tmp / "faixa.png"), "-filter_complex", ";".join(filtros), "-map", f"[{ultimo}]", "-map", "0:a?",
       "-t", f"{dur:.2f}", "-c:v", "libx264", "-crf", "19", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
       "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-movflags", "+faststart", str(v / "final.mp4"))
    sh("-ss", f"{min(dur - 0.1, tf + 1):.2f}", "-i", str(v / "final.mp4"), "-frames:v", "1", str(v / "capa.png"))
    sh("-i", str(v / "final.mp4"), "-vf", f"fps=6/{dur:.2f},scale=270:480,tile=6x1", "-frames:v", "1", str(v / "contato.jpg"))
    for x in tmp.iterdir():
        x.unlink()
    tmp.rmdir()
    print(f"ok -> {(v / 'final.mp4').relative_to(PROJ)} ({dur:.1f} s)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
