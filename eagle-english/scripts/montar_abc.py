#!/usr/bin/env python3
"""Formato "ABC" (ref. do usuário 20/11): 3 rodadas curtas (~20 s no total), personagem próprio animado em SVG no centro.

Rodada: pergunta falada em pt ("Em inglês, como se diz…?") com título + opções A/B/C → contagem 5→1 (anel, tique, personagem
pensando) → ding: só a certa em verde + pronúncia, personagem feliz (joinha), resposta falada 2x. Fundo Maldivas (cena por rodada).
Sem CTA de produto (regra 19/11). Boca pelo volume da voz, braços gesticulando enquanto fala, piscadas, balanço leve.

Uso: python3 scripts/montar_abc.py posts/<post>
abc.json: {"fundo_video": "maldivas", "fundo_inicio": 30, "repetir": 2, "contagem": 2.5,
           "rodadas": [{"titulo": "Estou atrasado", "opcoes": ["A) …", "B) …", "C) …"], "certa": 1, "pron": "áim LÊIT", "q": "q1", "r": "r1"}]}
"""
import json, math, os, subprocess, sys, wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from montar_quiz import SR, FPS, sh, dur, sfx  # noqa: E402
from montar_padrao import trilha_fundo, clipes_fundo  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]


def envelope(sons, total, passo=1 / FPS):
    n = int(total / passo) + 2; env = np.zeros(n)
    for arq, ini, vol, voz in sons:
        if not voz:
            continue
        with wave.open(str(arq)) as w:
            x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
            if w.getnchannels() > 1:
                x = x.reshape(-1, w.getnchannels()).mean(1)
            sr = w.getframerate()
        k = int(sr * passo)
        for j in range(len(x) // k):
            i = int(round(ini / passo)) + j
            if i < n:
                env[i] = max(env[i], math.sqrt((x[j * k:(j + 1) * k] ** 2).mean()))
    return env


def main(pasta):
    post = (PROJ / pasta).resolve()
    cfg = json.loads((post / "abc.json").read_text())
    aud = lambda i: post / "audio" / f"{i}.wav"
    fx = sfx(); cont = cfg.get("contagem", 2.5); rep = cfg.get("repetir", 2)
    rods = cfg["rodadas"]; n = len(rods)
    sons, eventos, trechos = [], [], []
    t = 0.1
    for i, r in enumerate(rods):
        t0 = t
        dq = dur(aud(r["q"])); sons.append((aud(r["q"]), t, 1.0, True)); qa, qb = t, t + dq
        t += dq + 0.2
        cs = t
        for k in range(5):
            sons.append((fx["tique"], cs + k * cont / 5, 0.5, False))
        t += cont
        rv = t; sons.append((fx["ding"], rv, 0.45, False)); t += 0.15
        falas_r = []
        for _ in range(rep):
            d = dur(aud(r["r"])); sons.append((aud(r["r"]), t, 1.0, True)); falas_r.append((t, t + d)); t += d + 0.35
        t += 0.35
        eventos.append({"i": i, "ini": t0, "q": (qa, qb), "cont": (cs, rv), "rev": rv, "fim": t})
        trechos.append((t0, t))
    total = t
    print(f"  duração: {total:.1f} s")
    env = envelope(sons, total)

    # POSES ao longo do tempo (com transição de 0,18 s)
    def pose_base(x):
        ev = next((e for e in eventos if e["ini"] <= x < e["fim"]), eventos[-1])
        if x >= ev["rev"]:
            return "feliz", ev
        if ev["cont"][0] <= x < ev["cont"][1]:
            return "pensando", ev
        i = int(x / (1 / FPS)); falando = env[max(0, i - 4):i + 4].max() > 0.02
        if falando:
            return ["fala1", "fala3", "fala2", "fala4"][int((x - ev["ini"]) / 0.45) % 4], ev
        return "neutro", ev
    nq = int(total * FPS)
    poses = [pose_base(k / FPS) for k in range(nq)]
    ini_pose, ant, atual = [], "neutro", None
    for k, (p, _) in enumerate(poses):
        if p != atual:
            ant = atual or "neutro"; atual = p; ini = k
        ini_pose.append((ant, ini))

    v = post / "video"; q = v / "quadros"; q.mkdir(parents=True, exist_ok=True)
    for x in q.glob("*.png"):
        x.unlink()
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        cam = os.environ.get("CHROMIUM_PATH")
        nav = pw.chromium.launch(executable_path=cam) if cam else pw.chromium.launch()
        pg = nav.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto((PROJ / "templates" / "abc.html").as_uri()); pg.wait_for_function("window.fontesOk === true")
        def estado(k):
            x = k / FPS; p, ev = poses[k]; r = rods[ev["i"]]; ant, ini = ini_pose[k]
            kk = min(1.0, (k - ini) / (0.18 * FPS)); kk = kk * kk * (3 - 2 * kk)
            e = env[k] if k < len(env) else 0
            boca = 0 if e < 0.03 else (1 if (e > 0.09 and k % 4 < 2) else 2 if k % 4 < 3 else 1)
            st = {"rodada": f"{ev['i'] + 1}/{n}", "titulo": r["titulo"], "opcoes": r["opcoes"], "certa": r["certa"],
                  "pron": r["pron"], "pose": p, "pose_ant": ant, "k": kk, "boca": boca,
                  "piscar": (x % 3.3) < 0.12 and p != "feliz", "balanco": 1.3 * math.sin(x * 1.7)}
            if x >= ev["rev"]:
                st["fase"] = "revela"
            elif ev["cont"][0] <= x < ev["cont"][1]:
                f = (x - ev["cont"][0]) / cont
                st.update(fase="contagem", num=5 - min(4, int(f * 5)), anel=1 - (f * 5 % 1))
            else:
                st["fase"] = "pergunta"
            return st
        for k in range(nq):
            pg.evaluate("s => window.render(s)", estado(k))
            pg.screenshot(path=str(q / f"{k:05d}.png"), omit_background=True)
            if k % 150 == 0:
                print(f"  quadro {k}/{nq}", flush=True)
        # capa: rodada 1 na contagem (sem revelar), com o fundo
        cap = v / "_capa_fundo.jpg"
        sh("-ss", "4", "-i", str(clipes_fundo(cfg)[0]), "-frames:v", "1", "-vf", "scale=1080:1920", str(cap))
        k1 = int((eventos[0]["cont"][0] + 0.1) * FPS); st = estado(k1); st["fundo"] = cap.as_uri(); st["pose"] = st["pose_ant"] = "pensando"
        pg.evaluate("s => window.render(s)", st); pg.wait_for_timeout(300); pg.screenshot(path=str(v / "capa.png")); cap.unlink()
        nav.close()

    ov = v / "_camada.mov"
    sh("-framerate", str(FPS), "-i", str(q / "%05d.png"), "-c:v", "qtrle", "-pix_fmt", "argb", str(ov))
    bg = trilha_fundo(post, cfg, trechos, total)
    ent, fil = [], []
    for k, (arq, ini, vol, _) in enumerate(sons):
        ent += ["-i", str(arq)]; ms = int(round(ini * 1000))
        fil.append(f"[{k}:a]aresample={SR},aformat=channel_layouts=mono,volume={vol},adelay={ms}|{ms}[s{k}]")
    fil.append("".join(f"[s{k}]" for k in range(len(sons))) +
               f"amix=inputs={len(sons)}:normalize=0,apad=whole_dur={total:.3f},atrim=0:{total:.3f}[a]")
    bruto, audio = v / "_bruto.wav", v / "_audio.wav"
    sh(*ent, "-filter_complex", ";".join(fil), "-map", "[a]", "-ar", str(SR), str(bruto))
    alvo = "I=-14:TP=-1.5:LRA=11"
    r = subprocess.run(["ffmpeg", "-nostdin", "-i", str(bruto), "-af", f"loudnorm={alvo}:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    m = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    sh("-i", str(bruto), "-af", f"loudnorm={alvo}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
       f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,"
       "alimiter=limit=0.84:level=false", "-ar", "48000", "-ac", "2", str(audio))
    final = v / "final.mp4"
    sh("-i", str(bg), "-i", str(ov), "-i", str(audio), "-filter_complex",
       "[0:v]eq=brightness=-0.03[b];[b][1:v]overlay=0:0:shortest=1,format=yuv420p[v]",
       "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "aac", "-b:a", "192k",
       "-t", f"{total:.3f}", "-movflags", "+faststart", str(final))
    for x in (bruto, audio, ov, bg):
        x.unlink(missing_ok=True)
    def lufs():
        r = subprocess.run(["ffmpeg", "-nostdin", "-i", str(final), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
        return float(r[r.rindex("I:"):].split()[1])
    l = lufs()
    if abs(l + 14) > 0.5:
        tmp = final.with_name("_ganho.mp4")
        sh("-i", str(final), "-c:v", "copy", "-af", f"volume={-14 - l:.2f}dB,alimiter=limit=0.89:level=false",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(tmp))
        tmp.replace(final); l = lufs()
    sh("-i", str(final), "-vf", f"fps=1/{max(0.5, total / 24):.3f},scale=270:480,tile=6x4", "-frames:v", "1", str(v / "contato.jpg"))
    print(f"ok -> {final.relative_to(PROJ)}  ({total:.1f} s, {l:.1f} LUFS)")


if __name__ == "__main__":
    main(sys.argv[1])
