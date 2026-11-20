#!/usr/bin/env python3
"""Série "1 verbo por dia · 100 dias seguidos" (docs/SERIE_VERBO_DO_DIA.md). Personagem próprio (templates/personagem.js),
fundo Maldivas (cena nova por bloco), legenda falada em blocos de 3 palavras (Whisper) e caixas amarela/branca/vermelha.

Uso: python3 scripts/montar_verbo.py posts/<post>
verbo.json: {"aula": 1, "fundo_inicio": 5, "passos": [
   {"pt": "pt1", "caixas": [["1 verbo por dia", "am", "min"], ["100 dias seguidos", "vm"]], "bloco": 1},
   {"en": "en1", "caixas": [["GET", "am", "g"]], "vezes": 1, "pausa": 1.2}, …,
   {"pt": "pt9", "fim": "COMENTA\\n“APRENDER”"} ]}
Cada "pt"/"en" é o id de um áudio em audio/<id>.wav (cortados de UMA fala pt e UMA en com recortar_whisper.py).
"caixas" ficam na tela durante o passo (sem caixas = legenda falada). "bloco": troca a cena do fundo a partir desse passo.
"""
import json, math, os, re, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from montar_quiz import SR, FPS, sh, dur  # noqa: E402
from montar_padrao import trilha_fundo, clipes_fundo  # noqa: E402
from montar_abc import envelope  # noqa: E402
from montar_lista12 import palavras  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]


def main(pasta):
    post = (PROJ / pasta).resolve()
    cfg = json.loads((post / "verbo.json").read_text()); cfg.setdefault("fundo_video", "maldivas")
    falas = {f["id"]: f for f in json.loads((post / "falas.json").read_text())["falas"]}
    aud = lambda i: post / "audio" / f"{i}.wav"
    import whisper
    modelo = whisper.load_model("turbo")
    sons, segs, legs, cortes = [], [], [], [0.0]
    t = 0.15
    for p in cfg["passos"]:
        if p.get("bloco") and t > 0.2:
            cortes.append(t)
        ini = t
        if "pt" in p:
            a = aud(p["pt"]); d = dur(a); sons.append((a, t, 1.0, True))
            ws = palavras(modelo, a, falas[p["pt"]]["texto"], "pt")
            for k in range(0, len(ws), 3):          # blocos de 3 palavras; a atual em amarelo
                bloco = ws[k:k + 3]
                for j, (w, s, e) in enumerate(bloco):
                    fim = bloco[j + 1][1] if j + 1 < len(bloco) else (ws[k + 3][1] if k + 3 < len(ws) else e + 0.25)
                    legs.append((t + s, t + fim, [x[0] for x in bloco], j))
            t += d + p.get("depois", 0.25)
        else:
            a = aud(p["en"]); d = dur(a)
            for v in range(p.get("vezes", 1)):
                sons.append((a, t, 1.0, True)); t += d + (0.55 if v + 1 < p.get("vezes", 1) else 0)
            t += p.get("pausa", 0.35)
        segs.append((ini, t, p))
    total = t + 0.4
    cortes.append(total)
    trechos = list(zip(cortes[:-1], cortes[1:]))
    print(f"  duração: {total:.1f} s · {len(trechos)} cenas")
    env = envelope(sons, total)
    nq = int(total * FPS)

    def passo_em(x):
        for a, b, p in segs:
            if a <= x < b:
                return p
        return segs[-1][2]
    poses, atual, ant, ini_k = [], None, "neutro", 0
    for k in range(nq):
        x = k / FPS; i = k
        falando = env[max(0, i - 4):i + 4].max() > 0.02
        p = passo_em(x)
        pose = ("feliz" if p.get("fim") else ["fala1", "fala3", "fala2", "fala4"][int(x / 0.5) % 4]) if falando else \
               ("fala3" if "en" in p and p.get("pausa", 0) >= 1 else "neutro")
        if pose != atual:
            ant, atual, ini_k = (atual or "neutro"), pose, k
        poses.append((pose, ant, ini_k))

    v = post / "video"; q = v / "quadros"; q.mkdir(parents=True, exist_ok=True)
    for x in q.glob("*.png"):
        x.unlink()
    aula = f"AULA {cfg['aula']}"
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        cam = os.environ.get("CHROMIUM_PATH")
        nav = pw.chromium.launch(executable_path=cam) if cam else pw.chromium.launch()
        pg = nav.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto((PROJ / "templates" / "verbo.html").as_uri()); pg.wait_for_function("window.fontesOk === true")
        def estado(k):
            x = k / FPS; p = passo_em(x); pose, ant, ik = poses[k]
            kk = min(1.0, (k - ik) / (0.18 * FPS)); kk = kk * kk * (3 - 2 * kk)
            e = env[k] if k < len(env) else 0
            boca = 0 if e < 0.03 else (1 if (e > 0.09 and k % 4 < 2) else 2 if k % 4 < 3 else 1)
            st = {"aula": aula, "caixas": [{"t": c[0], "cor": c[1], "g": "g" in c[2:], "min": "min" in c[2:]} for c in p.get("caixas", [])],
                  "fim": p.get("fim"), "pose": pose, "pose_ant": ant, "k": kk, "boca": boca,
                  "piscar": (x % 3.3) < 0.12, "balanco": 1.3 * math.sin(x * 1.7)}
            lg = next((l for l in legs if l[0] <= x < l[1]), None)
            if lg:
                st["legenda"], st["atual"] = lg[2], lg[3]
            return st
        for k in range(nq):
            pg.evaluate("s => window.render(s)", estado(k))
            pg.screenshot(path=str(q / f"{k:05d}.png"), omit_background=True)
            if k % 300 == 0:
                print(f"  quadro {k}/{nq}", flush=True)
        # capa: "AULA N" + verbo grande + "1 verbo por dia / 100 dias seguidos"
        cap = v / "_capa_fundo.jpg"
        sh("-ss", "3", "-i", str(clipes_fundo(cfg)[0]), "-frames:v", "1", "-vf", "scale=1080:1920", str(cap))
        st = estado(int(0.5 * FPS)); st.update(fundo=cap.as_uri(), legenda=[], pose="fala3", pose_ant="fala3", boca=0,
                                               caixas=[{"t": cfg["verbo"], "cor": "am", "g": True},
                                                       {"t": cfg["significado"], "cor": "br"},
                                                       {"t": "1 verbo por dia · 100 dias", "cor": "vm"}])
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
