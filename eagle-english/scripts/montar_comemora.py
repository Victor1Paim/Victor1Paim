#!/usr/bin/env python3
"""Reel curto de comemoração (marcos de seguidores, ~12 s): contador 0→1.000, confete, fogos, textos e personagem falando.
Uso: python3 scripts/montar_comemora.py posts/<post>   (áudio da fala em audio/fala.wav; fundo Maldivas)"""
import json, math, os, subprocess, sys, wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from montar_quiz import SR, FPS, sh, dur, sfx, gravar_wav  # noqa: E402
from montar_padrao import trilha_fundo  # noqa: E402
from montar_abc import envelope  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]


def main(pasta):
    post = (PROJ / pasta).resolve(); v = post / "video"; q = v / "quadros"; q.mkdir(parents=True, exist_ok=True)
    for x in q.glob("*.png"):
        x.unlink()
    fala = post / "audio" / "fala.wav"; ini_fala = 0.6
    total = round(ini_fala + dur(fala) + 2.6, 2)
    fx = sfx()
    pop = PROJ / "assets" / "sfx" / "pop.wav"
    if not pop.exists():   # "pop" de confete: ruído curto com ataque rápido
        tt = np.arange(int(SR * 0.12)) / SR
        gravar_wav(pop, np.random.default_rng(3).normal(0, 1, len(tt)) * np.exp(-tt * 45) * 0.5)
    sons = [(fx["whoosh"], 0.15, 0.7, False), (fala, ini_fala, 1.0, True), (fx["ding"], 2.2, 0.5, False)]
    sons += [(pop, t, 0.6, False) for t in (2.2, 2.3, 2.7, 3.3, 5.2, 6.4)]
    env = envelope(sons, total)
    nq = int(total * FPS)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        cam = os.environ.get("CHROMIUM_PATH")
        nav = pw.chromium.launch(executable_path=cam) if cam else pw.chromium.launch()
        pg = nav.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto((PROJ / "templates" / "comemora.html").as_uri()); pg.wait_for_function("window.fontesOk === true")
        for k in range(nq):
            t = k / FPS; e = env[k] if k < len(env) else 0
            falando = env[max(0, k - 4):k + 4].max() > 0.02
            pose = (["fala3", "feliz"][int(t / 0.9) % 2]) if falando else "feliz"
            boca = 0 if e < 0.03 else (1 if (e > 0.09 and k % 4 < 2) else 2 if k % 4 < 3 else 1)
            st = {"t": t, "pose": pose, "pose_ant": pose, "k": 1, "boca": boca, "piscar": (t % 3.3) < 0.12,
                  "balanco": 2.0 * math.sin(t * 2.4)}
            pg.evaluate("s => window.render(s)", st)
            pg.screenshot(path=str(q / f"{k:05d}.png"), omit_background=True)
        nav.close()
    ov = v / "_camada.mov"
    sh("-framerate", str(FPS), "-i", str(q / "%05d.png"), "-c:v", "qtrle", "-pix_fmt", "argb", str(ov))
    for _x in q.glob("*.png"):   # libera disco: os quadros já viraram a camada .mov
        _x.unlink()
    bg = trilha_fundo(post, {"fundo_video": "maldivas", "fundo_inicio": 14}, [(0, total / 2), (total / 2, total)], total)
    ent, fil = [], []
    for k, (arq, ini, vol, _) in enumerate(sons):
        ent += ["-i", str(arq)]; ms = int(round(ini * 1000))
        fil.append(f"[{k}:a]aresample={SR},aformat=channel_layouts=mono,volume={vol},adelay={ms}|{ms}[s{k}]")
    fil.append("".join(f"[s{k}]" for k in range(len(sons))) + f"amix=inputs={len(sons)}:normalize=0,apad=whole_dur={total:.3f},atrim=0:{total:.3f}[a]")
    bruto, audio = v / "_bruto.wav", v / "_audio.wav"
    sh(*ent, "-filter_complex", ";".join(fil), "-map", "[a]", "-ar", str(SR), str(bruto))
    alvo = "I=-14:TP=-1.5:LRA=11"
    r = subprocess.run(["ffmpeg", "-nostdin", "-i", str(bruto), "-af", f"loudnorm={alvo}:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    sh("-i", str(bruto), "-af", f"loudnorm={alvo}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
       f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,alimiter=limit=0.84:level=false", "-ar", "48000", "-ac", "2", str(audio))
    final = v / "final.mp4"
    sh("-i", str(bg), "-i", str(ov), "-i", str(audio), "-filter_complex", "[0:v]eq=brightness=-0.06[b];[b][1:v]overlay=0:0:shortest=1,format=yuv420p[v]",
       "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "-t", f"{total:.3f}", "-movflags", "+faststart", str(final))
    sh("-ss", "8.5", "-i", str(final), "-frames:v", "1", str(v / "capa.png"))
    sh("-i", str(final), "-vf", f"fps=2,scale=270:480,tile=6x4", "-frames:v", "1", str(v / "contato.jpg"))
    for x in (bruto, audio, ov, bg):
        x.unlink(missing_ok=True)
    print(f"ok -> {final.relative_to(PROJ)} ({total:.1f} s)")


if __name__ == "__main__":
    main(sys.argv[1])
