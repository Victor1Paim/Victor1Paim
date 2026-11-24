#!/usr/bin/env python3
"""CTA do produto (pedido 22/11): clipe vertical de ~14 s no estilo das aulas (sala, lousa, personagem, voz Achird)
para colar no FIM dos vídeos diários. Falas em assets/cta_produto/falas.json (gerar com vozes.py).

  python3 scripts/montar_cta_produto.py <variante>                 -> assets/cta_produto/cta_<variante>.mp4
  python3 scripts/montar_cta_produto.py anexar posts/<post> [variante]
      -> acrescenta o clipe ao final.mp4 (guarda final_sem_cta.mp4). Sem variante: roda entre as variantes ROTACAO pela data do post.
Variantes em assets/cta_produto/variantes/<nome>/ (falas.json + lousa.json; áudio com vozes.py gerar <pasta>).
"""
import json, math, os, shutil, subprocess, sys, wave
from pathlib import Path

import numpy as np

PROJ = Path(__file__).resolve().parents[1]
BASE = PROJ / "assets" / "cta_produto"
ROTACAO = ["pc_mae", "pc_nao_so_prova", "pc_ja_tentou", "pc_viagem"]   # 24/11: CTA vende o Eagle Primeira Classe
FPS = 15


def sh(*a):
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", *a], check=True)


def dur(a):
    with wave.open(str(a)) as w:
        return w.getnframes() / w.getframerate()


def lufs(arq):
    r = subprocess.run(["ffmpeg", "-nostdin", "-i", str(arq), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(r[r.rindex("I:"):].split()[1])


def montar(nome):
    V = BASE / "variantes" / nome
    textos = json.load(open(V / "lousa.json"))
    aud = lambda k: V / "audio" / f"{k}.wav"
    t = 0.2; sons, fases = [], []
    for k, fase in (("c1", 1), ("c2", 2), ("c3", 3)):
        d = dur(aud(k)); sons.append((aud(k), t)); fases.append((t, t + d, fase)); t += d + (0.2 if k != "c3" else 0.6)
    total = t
    # envelope da voz (boca)
    env = np.zeros(int(total * FPS) + 2)
    for arq, ini in sons:
        with wave.open(str(arq)) as w:
            x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768; sr = w.getframerate()
        k = int(sr / FPS)
        for j in range(len(x) // k):
            i = int(round(ini * FPS)) + j
            if i < len(env):
                env[i] = max(env[i], math.sqrt((x[j * k:(j + 1) * k] ** 2).mean()))
    a2, b2 = fases[1][0], fases[1][1]
    sts = []
    for k in range(int(total * FPS)):
        x = k / FPS
        fase = next((f for a, b, f in fases if a - 0.3 <= x < b + 0.3), 3 if x > fases[2][0] else 1)
        e = env[k]; falando = e > 0.02
        st = {"fase": fase, "itens": 0 if x < a2 + (b2 - a2) * 0.30 else 1 if x < a2 + (b2 - a2) * 0.58 else 2 if x < a2 + (b2 - a2) * 0.82 else 3,
              "boca": 0 if e < 0.03 else (1 if (e > 0.09 and k % 4 < 2) else 2 if k % 4 < 3 else 1), "piscar": (x % 3.7) < 0.14,
              "logo": (PROJ / "assets/marca/logo_eagle.png").as_uri(), "aponta": 0.15, "textos": textos}
        if fase == 3:
            st["pose"] = "aponta" if falando else "feliz"
        elif falando:
            st["pose"] = ["fala1", "fala3", "fala2", "fala4"][int(x / 0.9) % 4]
        else:
            st["pose"] = "neutro"
        sts.append(st)
    ant, atual, ini = "neutro", None, 0
    for k, st in enumerate(sts):
        if st["pose"] != atual:
            ant = atual or "neutro"; atual = st["pose"]; ini = k
        kk = min(1.0, (k - ini) / (0.4 * FPS)); st["pose_ant"] = ant; st["k"] = round(kk * kk * (3 - 2 * kk), 2)
    tmp = BASE / f"_tmp_{nome}"; tmp.mkdir(exist_ok=True)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        cam = os.environ.get("CHROMIUM_PATH", "/opt/pw-browsers/chromium")
        nav = pw.chromium.launch(executable_path=cam) if os.path.isfile(cam) else pw.chromium.launch()
        pg = nav.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto((PROJ / "templates" / "cta_produto.html").as_uri()); pg.wait_for_function("window.fontesOk === true")
        cache, lista = {}, []
        for st in sts:
            key = json.dumps(st, sort_keys=True)
            if key not in cache:
                cache[key] = tmp / f"{len(cache):05d}.jpg"
                pg.evaluate("s => window.render(s)", st); pg.wait_for_timeout(15); pg.screenshot(path=str(cache[key]), type="jpeg", quality=90)
            lista.append(cache[key])
        nav.close()
    with open(tmp / "lista.txt", "w") as f:
        for q in lista:
            f.write(f"file '{q}'\nduration {1 / FPS:.5f}\n")
        f.write(f"file '{lista[-1]}'\n")
    ent, fil = [], []
    for k, (arq, ini) in enumerate(sons):
        ent += ["-i", str(arq)]; ms = int(ini * 1000)
        fil.append(f"[{k + 1}:a]aresample=48000,aformat=channel_layouts=mono,adelay={ms}|{ms}[s{k}]")
    fil.append("".join(f"[s{k}]" for k in range(len(sons))) + f"amix=inputs={len(sons)}:normalize=0,apad=whole_dur={total:.3f},atrim=0:{total:.3f},loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    saida = BASE / f"cta_{nome}.mp4"
    sh("-f", "concat", "-safe", "0", "-i", str(tmp / "lista.txt"), *ent, "-filter_complex", ";".join(fil),
       "-map", "0:v", "-map", "[a]", "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "18", "-c:a", "aac", "-b:a", "192k",
       "-ar", "48000", "-ac", "2", "-t", f"{total:.3f}", "-movflags", "+faststart", str(saida))
    l = lufs(saida)
    if abs(l + 14) > 0.5:
        g = saida.with_name("_g.mp4")
        sh("-i", str(saida), "-c:v", "copy", "-af", f"volume={-14 - l:.2f}dB,alimiter=limit=0.89:level=false", "-c:a", "aac", "-b:a", "192k", str(g)); g.replace(saida)
    sh("-i", str(saida), "-vf", f"fps=1/{total / 8:.3f},scale=270:480,tile=4x2", "-frames:v", "1", str(BASE / f"contato_{nome}.jpg"))
    shutil.rmtree(tmp)
    print(f"ok -> {saida.relative_to(PROJ)} ({total:.1f} s, {lufs(saida):.1f} LUFS)")


def ponto_meio(arq, ini=0.60, fim=0.70):
    """Ponto mais silencioso (média de 300 ms) entre 60% e 70% do vídeo: onde a chamada curta entra sem cortar fala."""
    raw = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", str(arq), "-ac", "1", "-ar", "8000", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16).astype(float) / 32768; sr = 8000; j = sr // 20            # janelas de 50 ms
    e = np.sqrt(np.convolve((x[:len(x) // j * j].reshape(-1, j) ** 2).mean(1), np.ones(6) / 6, mode="same"))
    a, b = int(len(e) * ini), int(len(e) * fim)
    return (a + int(np.argmin(e[a:b]))) * 0.05


def anexar(post, nome=None, meio="pc_meio"):
    """final.mp4 = [vídeo até ~65%] + chamada curta (pc_meio, ~6 s) + [resto do vídeo] + CTA final da variante.
    24/11: pedido do usuário (chamada leve no meio + CTA no fim). meio=None desliga a chamada do meio."""
    if not nome:
        import hashlib
        nome = ROTACAO[int(hashlib.md5(Path(post).name.encode()).hexdigest(), 16) % len(ROTACAO)]
    v = (PROJ / post).resolve() / "video"; final = v / "final.mp4"; orig = v / "final_sem_cta.mp4"
    if not orig.exists():
        shutil.copy(final, orig)
    cta = BASE / f"cta_{nome}.mp4"
    norm_v = "fps=30,scale=1080:1920,setsar=1,format=yuv420p"; norm_a = "aresample=48000,aformat=channel_layouts=stereo"
    if meio:
        t = ponto_meio(orig)
        ent = ["-i", str(orig), "-i", str(BASE / f"cta_{meio}.mp4"), "-i", str(cta)]
        fc = (f"[0:v]{norm_v},split[va][vb];[0:a]{norm_a},asplit[aa][ab];"
              f"[va]trim=0:{t:.3f},setpts=PTS-STARTPTS[v0];[aa]atrim=0:{t:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={max(t - 0.08, 0):.3f}:d=0.08[a0];"
              f"[vb]trim=start={t:.3f},setpts=PTS-STARTPTS[v2];[ab]atrim=start={t:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.08[a2];"
              f"[1:v]{norm_v}[v1];[1:a]{norm_a}[a1];[2:v]{norm_v}[v3];[2:a]{norm_a}[a3];"
              "[v0][a0][v1][a1][v2][a2][v3][a3]concat=n=4:v=1:a=1[v][a]")
    else:
        ent = ["-i", str(orig), "-i", str(cta)]
        fc = f"[0:v]{norm_v}[v0];[1:v]{norm_v}[v1];[0:a]{norm_a}[a0];[1:a]{norm_a}[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]"
    sh(*ent, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18", "-c:a", "aac", "-b:a", "192k",
       "-movflags", "+faststart", str(final))
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(final)], capture_output=True, text=True).stdout)
    print(f"ok -> {final.relative_to(PROJ)} com chamada do meio{f' em {t:.1f} s' if meio else ' (sem)'} + CTA '{nome}' ({d:.1f} s)")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "anexar":
        anexar(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None, None if "--sem-meio" in sys.argv else "pc_meio")
    else:
        for n in (sys.argv[1:] or ROTACAO):
            montar(n)
