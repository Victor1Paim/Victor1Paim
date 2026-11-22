#!/usr/bin/env python3
"""10 aulas gravadas do plano avançado (1920×1080): personagem próprio numa sala de aula com lousa (templates/aula.html).
Roteiro em produtos/fonte/aulas.json; frases e pronúncia do Eagle 350 (pronúncia no estilo simples: minúsculas, sem hífen).

  python3 scripts/produto_aulas.py vozes produtos 1 2 3     # gera as falas (pt: 1 arquivo por fala; en: 1 pedido cortado pelo Whisper)
  python3 scripts/produto_aulas.py montar produtos 1 2 3    # monta o vídeo (15 fps, quadros repetidos deduplicados)

Saída: produtos/avancado/aulas/Aula_NN_<titulo>.mp4 · trabalho em produtos/_tmp/aulaNN · custos em produtos/custos.jsonl
Vozes: Achird (pt gemini-3.8-flash-tts; en gemini-3.8-flash-lite-tts). Nunca Kore/OpenAI no Eagle.
"""
import json, math, os, re, subprocess, sys, unicodedata, wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import vozes  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
FPS = 15
SR = 48000


def slug(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def pron_simples(p):
    return re.sub(r"\s+", " ", p.lower().replace("-", "")).strip()


def dur(arq):
    with wave.open(str(arq)) as w:
        return w.getnframes() / w.getframerate()


def sh(*a):
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", *a], check=True)


def roteiro(base, n):
    A = next(a for a in json.load(open(base / "fonte" / "aulas.json")) if a["n"] == n)
    M = {m["mapa"]: m for m in json.load(open(base / "fonte" / "eagle350.json"))}
    F = lambda r: dict(M[r[0]]["frases"][r[1]], pron=pron_simples(M[r[0]]["frases"][r[1]]["pron"]))
    pt = {"intro": A["intro"], "metodo": A["metodo"]["fala"], "dica": A["dica"]["fala"], "fim": A["fim"]["fala"],
          "sua_vez": ("Agora é sua vez. Eu falo em português e você responde em inglês na pausa, antes de mim."
                      if A["frases"] else "Vamos começar. Primeira parada: o aeroporto.")}
    frases = []
    for k, f in enumerate(A["frases"]):
        pt[f"cue{k}"] = f["cue"]; frases.append(F(f["ref"]))
    ex = [F(r) for r in A["exercicios"]]
    for k, e in enumerate(ex):
        pt[f"ex{k}"] = "Como você diz: " + e["pt"].rstrip(".!") + "?" if not e["pt"].endswith("?") else "Como você diz: " + e["pt"]
    en = []
    for f in frases + ex:
        if f["en"] not in en:
            en.append(f["en"])
    return A, pt, frases, ex, en


_MOD = {}


def modelos():
    if not _MOD:
        import whisper
        _MOD["t"] = whisper.load_model("small"); _MOD["c"] = whisper.load_model("base.en")
    return _MOD["t"], _MOD["c"]


def gerar_vozes(base, n):
    A, pt, frases, ex, en = roteiro(base, n)
    d = base / "_tmp" / f"aula{n:02d}" / "audio"; d.mkdir(parents=True, exist_ok=True)
    for k, txt in pt.items():
        saida = d / f"{k}.wav"
        if saida.exists():
            continue
        for t in range(3):
            vozes.tts(txt, "Achird", "gemini-3.8-flash-tts", saida, base, "pt")
            pct = vozes.conferir(saida, txt, "pt")
            print(f"  aula {n} {k}: {pct}%", flush=True)
            if pct >= 90:
                break
    # inglês: 1 pedido com todas as frases da aula, cortado nas palavras do Whisper
    if not all((d / f"en{k}.wav").exists() for k in range(len(en))):
        from recortar_whisper import recortar, gravar
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from produto_audio import nota
        mw, cw = modelos()
        for t in range(3):
            bruto = d / "_en_bruto.wav"
            vozes.tts("\n\n".join(en), "Achird", "gemini-3.8-flash-lite-tts", bruto, base, "en")
            pecas, sr, _ = recortar(bruto, "en", en, mw)
            notas = []
            for k, (y, f) in enumerate(zip(pecas, en)):
                gravar(d / f"en{k}.wav", y, sr)
                notas.append(nota(f, cw.transcribe(str(d / f"en{k}.wav"), language="en", fp16=False)["text"]))
            print(f"  aula {n} inglês: {[round(x, 2) for x in notas]}", flush=True)
            if min(notas) >= 0.7:
                break
        bruto.unlink(missing_ok=True)
    (d.parent / "vozes_ok").touch()
    print(f"ok vozes aula {n}")


def envelope(sons, total):
    passo = 1 / FPS; nq = int(total * FPS) + 2; env = np.zeros(nq)
    for arq, ini in sons:
        with wave.open(str(arq)) as w:
            x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768; sr = w.getframerate()
        k = int(sr * passo)
        for j in range(len(x) // k):
            i = int(round(ini / passo)) + j
            if i < nq:
                env[i] = max(env[i], math.sqrt((x[j * k:(j + 1) * k] ** 2).mean()))
    return env


def montar(base, n):
    A, pt, frases, ex, en = roteiro(base, n)
    tmp = base / "_tmp" / f"aula{n:02d}"; d = tmp / "audio"
    aud = lambda k: d / f"{k}.wav"
    eni = lambda s: aud(f"en{en.index(s)}")
    import whisper
    from montar_lista12 import palavras
    mw = whisper.load_model("base.en")
    pal = {s: palavras(mw, eni(s), s, "en") for s in en}
    cab = {"aula": f"AULA {n}", "tema": A["titulo"].upper()}
    sons, cenas, t = [], [], 0.5

    def fala(k, estado, pos=0.35):
        nonlocal t
        a = t; dd = dur(aud(k)); sons.append((aud(k), t)); t += dd + pos
        cenas.append((a, t, estado, None)); return a, a + dd

    def ingles(s, estado, falas):
        nonlocal t
        a = t; dd = dur(eni(s)); sons.append((eni(s), t)); falas.append((t, s)); t += dd
        return a, t

    # abertura
    fala("intro", {"fase": "titulo", "titulo": A["titulo"], "sub": A["tema"]}, 0.5)
    m = A["metodo"]; a0 = t
    fala("metodo", {"fase": "lista", "titulo": "Hoje" if n > 1 else "Como funciona", "linhas": m["linhas"], "progressivo": True}, 0.6)
    # frases: cue → inglês → pausa para repetir → inglês de novo
    for k, f in enumerate(frases):
        base_st = {"fase": "frase", "en": f["en"], "pron": f["pron"], "pt": f["pt"], "cue": A["frases"][k]["cue"], "selo": f"{k + 1}/{len(frases)}"}
        a = t; dd = dur(aud(f"cue{k}")); sons.append((aud(f"cue{k}"), t)); t += dd + 0.25
        cenas.append((a, t, dict(base_st, falando="pt"), None))
        falas = []
        a, b = ingles(f["en"], base_st, falas); cenas.append((a, b, dict(base_st, falando="en"), falas[-1])); t += 0.15
        pausa = max(2.2, dur(eni(f["en"])) * 1.5 + 0.8)
        cenas.append((t, t + pausa, dict(base_st, selo="REPITA EM VOZ ALTA", barra=True), None)); t += pausa
        a, b = ingles(f["en"], base_st, falas); cenas.append((a, b, dict(base_st, falando="en"), falas[-1])); t += 0.9
        cenas.append((b, t, base_st, None))
    # dica de pronúncia
    fala("dica", {"fase": "lista", "titulo": "Dica de pronúncia" if n != 10 else "Dica", "linhas": A["dica"]["linhas"]}, 0.6)
    # exercícios / simulação
    fala("sua_vez", {"fase": "titulo", "titulo": "Sua vez!" if n != 10 else "Simulação", "sub": "responda em inglês na pausa"}, 0.4)
    for k, e in enumerate(ex):
        st = {"fase": "pergunta", "pt": e["pt"], "en": e["en"], "pron": e["pron"], "selo": f"{k + 1}/{len(ex)}"}
        fala(f"ex{k}", dict(st, falando="pt"), 0.1)
        espera = max(3.5, dur(eni(e["en"])) * 1.6 + 1.5)
        cenas.append((t, t + espera, dict(st, selo="SUA VEZ", barra=True, pensa=True), None)); t += espera
        falas = []
        a, b = ingles(e["en"], st, falas); cenas.append((a, b, dict(st, revela=True, falando="en"), falas[-1])); t += 1.0
        cenas.append((b, t, dict(st, revela=True, feliz=True), None))
    fala("fim", {"fase": "lista", "titulo": "Para revisar", "linhas": A["fim"]["linhas"]}, 1.2)
    total = t
    print(f"  aula {n}: {total / 60:.1f} min")
    env = envelope(sons, total)

    def estado(k):
        x = k / FPS
        c = next((c for c in cenas if c[0] <= x < c[1]), cenas[-1])
        st = dict(cab, **c[2])
        e = env[k] if k < len(env) else 0
        falando = e > 0.02
        st["boca"] = 0 if e < 0.03 else (1 if (e > 0.09 and k % 4 < 2) else 2 if k % 4 < 3 else 1)
        st["piscar"] = (x % 3.7) < 0.14
        if st["fase"] == "lista" and st.get("progressivo"):
            st["ate"] = 1 + int((x - c[0]) / max(0.1, (c[1] - c[0]) / len(st["linhas"])))
        # destaque da palavra falada
        if c[3]:
            a, s = c[3]; ws = pal[s]
            for j, (w, s0, e0) in enumerate(ws):
                fim = ws[j + 1][1] if j + 1 < len(ws) else e0 + 0.3
                if a + s0 <= x < a + fim:
                    npr = len(st["pron"].split(" "))
                    st["hl"] = j; st["hl_pr"] = j if npr == len(ws) else min(npr - 1, int(j * npr / len(ws)))
                    st["aponta"] = 0.1
        if st.get("barra"):
            st["barra"] = round(1 - (x - c[0]) / (c[1] - c[0]), 2)
        # pose
        if st.get("pensa"):
            pose = "pensando"
        elif st.get("feliz"):
            pose = "feliz"
        elif c[3] and falando:
            pose = "aponta"
        elif falando:
            pose = ["fala1", "fala3", "fala2", "fala4"][int(x / 0.9) % 4]
        else:
            pose = "neutro"
        st["pose"] = pose
        for kk in ("falando", "pensa", "feliz", "progressivo"):
            st.pop(kk, None)
        return st

    nq = int(total * FPS)
    sts = [estado(k) for k in range(nq)]
    # transição suave entre poses (0,4 s)
    ant, atual, ini = "neutro", None, 0
    for k, st in enumerate(sts):
        if st["pose"] != atual:
            ant = atual or "neutro"; atual = st["pose"]; ini = k
        kk = min(1.0, (k - ini) / (0.4 * FPS)); st["pose_ant"] = ant; st["k"] = round(kk * kk * (3 - 2 * kk), 2)
        if st["k"] >= 1:
            st["pose_ant"] = st["pose"]
    segs = []
    for st in sts:
        key = json.dumps(st, sort_keys=True, ensure_ascii=False)
        if segs and segs[-1][0] == key:
            segs[-1][1] += 1
        else:
            segs.append([key, 1])
    unicos = {}
    for key, _ in segs:
        unicos.setdefault(key, len(unicos))
    print(f"  {nq} quadros → {len(unicos)} únicos", flush=True)
    q = tmp / "quadros"; q.mkdir(exist_ok=True)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        cam = os.environ.get("CHROMIUM_PATH", "/opt/pw-browsers/chromium")
        nav = pw.chromium.launch(executable_path=cam) if os.path.isfile(cam) else pw.chromium.launch()
        pg = nav.new_page(viewport={"width": 1920, "height": 1080})
        pg.goto((PROJ / "templates" / "aula.html").as_uri()); pg.wait_for_function("window.fontesOk === true")
        for key, i in unicos.items():
            arq = q / f"{i:05d}.jpg"
            if not arq.exists():
                pg.evaluate("s => window.render(s)", json.loads(key)); pg.screenshot(path=str(arq), type="jpeg", quality=88)
            if i % 300 == 0:
                print(f"    quadro {i}/{len(unicos)}", flush=True)
        # capa da aula
        pg.evaluate("s => window.render(s)", dict(cab, fase="titulo", titulo=A["titulo"], sub=A["tema"], pose="feliz", pose_ant="feliz", k=1, boca=1))
        pg.screenshot(path=str(tmp / "capa.jpg"), type="jpeg", quality=92)
        nav.close()
    lista = tmp / "cenas.txt"
    with open(lista, "w") as f:
        for key, nfr in segs:
            f.write(f"file '{q / f'{unicos[key]:05d}.jpg'}'\nduration {nfr / FPS:.4f}\n")
        f.write(f"file '{q / f'{unicos[segs[-1][0]]:05d}.jpg'}'\n")
    mudo = tmp / "_mudo.mp4"
    sh("-f", "concat", "-safe", "0", "-i", str(lista), "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-crf", "20",
       "-preset", "medium", "-tune", "animation", str(mudo))
    ent, fil = [], []
    for k, (arq, ini) in enumerate(sons):
        ent += ["-i", str(arq)]; ms = int(round(ini * 1000))
        fil.append(f"[{k}:a]aresample={SR},aformat=channel_layouts=mono,adelay={ms}|{ms}[s{k}]")
    fil.append("".join(f"[s{k}]" for k in range(len(sons))) + f"amix=inputs={len(sons)}:normalize=0,apad=whole_dur={total:.3f},atrim=0:{total:.3f}[a]")
    bruto = tmp / "_bruto.wav"
    sh(*ent, "-filter_complex", ";".join(fil), "-map", "[a]", "-ar", str(SR), str(bruto))
    saida_dir = base / "avancado" / "aulas"; saida_dir.mkdir(parents=True, exist_ok=True)
    final = saida_dir / f"Aula_{n:02d}_{slug(A['titulo'])}.mp4"
    sh("-i", str(mudo), "-i", str(bruto), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
       "-ar", "48000", "-ac", "2", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(final))
    sh("-i", str(final), "-vf", f"fps=1/{max(1, total / 24):.3f},scale=320:180,tile=6x4", "-frames:v", "1", str(tmp / "contato.jpg"))
    for x in q.glob("*.jpg"):
        x.unlink()
    for x in (mudo, bruto, lista):
        x.unlink(missing_ok=True)
    print(f"ok -> {final.relative_to(base)} ({total / 60:.1f} min)")


def main():
    vozes.carregar_env()
    acao, base, ns = sys.argv[1], Path(sys.argv[2]).resolve(), [int(x) for x in sys.argv[3:]] or list(range(1, 11))
    for n in ns:
        (gerar_vozes if acao == "vozes" else montar)(base, n)


if __name__ == "__main__":
    main()
