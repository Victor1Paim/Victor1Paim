#!/usr/bin/env python3
"""Monta o vídeo de QUIZ (formato B) a partir de posts/<post>/quiz.json + audio/ + img/.

Uso:  python3 scripts/montar_quiz.py posts/2026-11-10_quiz-pedir-de-novo
Saída: video/final.mp4 (1080x1920, 30 fps, H.264 + AAC, ~-14 LUFS), video/contato.jpg, video/linha_do_tempo.json
       e video/capa.png (mesmo quadro da intro, para usar como capa do Reel/TikTok)

Cada pergunta: voz pt lê → contagem 3-2-1 com tique-taque → "ding" + revelação → voz americana diz a
resposta → voz pt traduz. Textos na tela vêm do template HTML (texto exato). Efeitos sonoros gerados
aqui mesmo (assets/sfx). CHROMIUM_PATH opcional, como no render_cartoes.py.
"""
import json, os, subprocess, sys, wave
from pathlib import Path

import numpy as np
from playwright.sync_api import sync_playwright

PROJ = Path(__file__).resolve().parents[1]
SR = 48000
FPS = 30


def sh(*a):
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", *a], check=True)


def dur(arq):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(arq)],
                                capture_output=True, text=True).stdout)


def gravar_wav(arq, x):
    x = np.clip(x, -1, 1)
    with wave.open(str(arq), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


def sfx():
    pasta = PROJ / "assets" / "sfx"; pasta.mkdir(parents=True, exist_ok=True)
    t = np.arange(int(SR * 0.09)) / SR
    tique = 0.5 * np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 70)
    t2 = np.arange(int(SR * 0.9)) / SR
    ding = (0.45 * np.sin(2 * np.pi * 1318.5 * t2) + 0.25 * np.sin(2 * np.pi * 1975.5 * t2)) * np.exp(-t2 * 5)
    ding[:240] *= np.linspace(0, 1, 240)
    t3 = np.arange(int(SR * 0.35)) / SR
    whoosh = np.random.default_rng(1).normal(0, 1, len(t3)) * np.sin(np.pi * t3 / t3[-1]) ** 2 * 0.12
    for nome, x in [("tique", tique), ("ding", ding), ("whoosh", whoosh)]:
        if not (pasta / f"{nome}.wav").exists():
            gravar_wav(pasta / f"{nome}.wav", x)
    return {n: pasta / f"{n}.wav" for n in ("tique", "ding", "whoosh")}


def preparar_vozes(post, cfg, vel):
    """Acelera levemente só a voz pt (a americana fica natural, para o aluno ouvir bem)."""
    falas = {f["id"]: f for f in json.loads((post / "falas.json").read_text())["falas"]}
    out = post / "audio" / "_mix"; out.mkdir(exist_ok=True)
    res = {}
    for i, f in falas.items():
        src, dst = post / "audio" / f"{i}.wav", out / f"{i}.wav"
        if not src.exists():  # prévia: silêncio do tamanho estimado da fala (~13 caracteres/s)
            est = max(1.0, len(f["texto"]) / 13 / (vel if f["lingua"] == "pt" else 1))
            print(f"  AVISO: falta audio/{i}.wav — usando {est:.1f} s de silêncio (prévia)")
            sh("-f", "lavfi", "-i", f"anullsrc=r={SR}:cl=mono", "-t", f"{est:.2f}", str(dst))
            res[i] = (dst, est); continue
        filtro = f"atempo={vel}" if f["lingua"] == "pt" and vel != 1 else "anull"
        sh("-i", str(src), "-af", filtro, "-ar", str(SR), "-ac", "1", str(dst))
        res[i] = (dst, dur(dst))
    return res


def finalizar(post, especs, cenas, sons, t, fundo, template="quiz.html", capa="00_intro"):
    """Renderiza os quadros (HTML), monta vídeo + áudio, loudness, capa, folha de contato e linha do tempo."""
    quadros = post / "video" / "quadros"; quadros.mkdir(parents=True, exist_ok=True)
    # RENDER DOS QUADROS
    with sync_playwright() as pw:
        cam = os.environ.get("CHROMIUM_PATH")
        nav = pw.chromium.launch(executable_path=cam) if cam else pw.chromium.launch()
        for nome, dados in especs:
            pg = nav.new_page(viewport={"width": 1080, "height": 1920})
            pg.add_init_script(f"window.DADOS = {json.dumps({'fundo': fundo, **dados}, ensure_ascii=False)};")
            pg.goto((PROJ / "templates" / template).as_uri())
            pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready")
            pg.screenshot(path=str(quadros / f"{nome}.png"))
            pg.close()
        nav.close()

    # VÍDEO: quadros fixos com a duração de cada cena (arredondada a quadros inteiros)
    lista = post / "video" / "cenas.txt"
    with open(lista, "w") as f:
        for nome, d in cenas:
            f.write(f"file '{quadros / (nome + '.png')}'\nduration {round(d * FPS) / FPS:.4f}\n")
        f.write(f"file '{quadros / (cenas[-1][0] + '.png')}'\n")
    mudo = post / "video" / "_mudo.mp4"
    sh("-f", "concat", "-safe", "0", "-i", str(lista), "-vf", f"fps={FPS},format=yuv420p",
       "-c:v", "libx264", "-preset", "medium", "-crf", "18", str(mudo))

    # ÁUDIO: cada som no seu instante (adelay) + mix + loudness -14 LUFS
    entradas, filtros = [], []
    for k, (arq, ini, vol) in enumerate(sons):
        entradas += ["-i", str(arq)]
        ms = int(round(ini * 1000))
        filtros.append(f"[{k}:a]aresample={SR},aformat=channel_layouts=mono,volume={vol},adelay={ms}|{ms}[s{k}]")
    mix = "".join(f"[s{k}]" for k in range(len(sons)))
    filtros.append(f"{mix}amix=inputs={len(sons)}:normalize=0,apad=whole_dur={t:.3f},atrim=0:{t:.3f}[a]")
    bruto, audio = post / "video" / "_bruto.wav", post / "video" / "_audio.wav"
    sh(*entradas, "-filter_complex", ";".join(filtros), "-map", "[a]", "-ar", str(SR), str(bruto))
    # loudness em duas passadas (uma passada só deixa ~1,5 dB abaixo da meta em falas curtas)
    alvo = "I=-14:TP=-1.5:LRA=11"
    r = subprocess.run(["ffmpeg", "-nostdin", "-i", str(bruto), "-af", f"loudnorm={alvo}:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    m = json.loads(r[r.rindex("{"):r.rindex("}") + 1])
    sh("-i", str(bruto), "-af", f"loudnorm={alvo}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
       f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true",
       "-ar", str(SR), "-ac", "2", str(audio))
    bruto.unlink()

    final = post / "video" / "final.mp4"
    sh("-i", str(mudo), "-i", str(audio), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
       "-shortest", "-movflags", "+faststart", str(final))
    for x in (mudo, audio, lista):
        x.unlink()

    # capa + folha de contato (1 quadro por cena) + linha do tempo
    import shutil
    from PIL import Image
    shutil.copy(quadros / f"{capa}.png", post / "video" / "capa.png")
    nomes = [n for n, _ in especs]
    cols = 6; lin = (len(nomes) + cols - 1) // cols
    folha = Image.new("RGB", (cols * 270, lin * 480), "white")
    for i, nm in enumerate(nomes):
        im = Image.open(quadros / f"{nm}.png").convert("RGB").resize((270, 480))
        folha.paste(im, ((i % cols) * 270, (i // cols) * 480))
    folha.save(post / "video" / "contato.jpg", quality=85)
    (post / "video" / "linha_do_tempo.json").write_text(json.dumps(
        {"duracao": round(t, 2), "cenas": [[n, round(d, 2)] for n, d in cenas],
         "sons": [[Path(a).name, round(i, 2)] for a, i, _ in sons]}, ensure_ascii=False, indent=1))
    print(f"ok -> {final.relative_to(PROJ)}  ({t:.1f} s)")


def main(pasta):
    post = Path(pasta).resolve()
    q = json.loads((post / "quiz.json").read_text())
    fx = sfx()
    vozes = preparar_vozes(post, q, q.get("velocidade_pt", 1.0))
    fundo = (post / "img" / "fundo.png").as_uri()
    m_pensa = (post / "img" / "mascote_pensando.png").as_uri()
    m_ok = (post / "img" / "mascote_positivo.png").as_uri()
    quadros = post / "video" / "quadros"; quadros.mkdir(parents=True, exist_ok=True)

    cenas, sons = [], []  # cenas: (png, segundos); sons: (wav, inicio, volume)
    t = 0.0

    def falar(ids, inicio, gap=0.22):
        for i in ids:
            arq, d = vozes[i]
            sons.append((arq, inicio, 1.0))
            inicio += d + gap
        return inicio - gap

    especs = []  # (nome_png, dados)
    # INTRO
    especs.append(("00_intro", {"tipo": "intro", "selo": q["intro"]["selo"], "hook": q["intro"]["hook"],
                                "sub": q["intro"]["sub"], "mascote": m_pensa}))
    fim = falar(q["intro"]["audio"], 0.15, gap=0.3)
    cenas.append(("00_intro", fim + 0.3)); t = fim + 0.3

    perguntas = [p for p in q["perguntas"] if "regancho" not in p]
    total, n = len(perguntas), 0
    for p in q["perguntas"]:
        if "regancho" in p:
            nome = "re_gancho"
            especs.append((nome, {"tipo": "regancho", "texto": p["regancho"], "mascote": m_pensa}))
            sons.append((fx["whoosh"], t, 0.8))
            fim = falar(p["audio"], t + 0.15)
            cenas.append((nome, fim - t + 0.3)); t = fim + 0.3
            continue
        n += 1
        base = {"tipo": "pergunta", "n": n, "total": total, "mascote": m_pensa,
                **{k: p.get(k) for k in ("enunciado", "frase", "a", "b", "certa", "pron", "traducao", "nota")}}
        especs.append((f"q{n}_0", base))
        sons.append((fx["whoosh"], t, 0.6))
        fim = falar(p["audio_pergunta"], t + 0.15)
        cenas.append((f"q{n}_0", fim - t + 0.15)); t = fim + 0.15
        for s in range(q.get("segundos_pensar", 3), 0, -1):
            especs.append((f"q{n}_t{s}", {**base, "timer": s}))
            sons.append((fx["tique"], t, 0.9))
            cenas.append((f"q{n}_t{s}", 1.0)); t += 1.0
        especs.append((f"q{n}_r", {**base, "revelar": True}))
        sons.append((fx["ding"], t, 0.7))
        fim = falar(p["audio_resposta"], t + 0.35, gap=0.3)
        cenas.append((f"q{n}_r", fim - t + 0.45)); t = fim + 0.45

    c = q["cta"]
    especs.append(("99_cta", {"tipo": "cta", "titulo": c["titulo"], "comenta": c["comenta"], "itens": c["itens"],
                              "mascote": m_ok}))
    sons.append((fx["whoosh"], t, 0.6))
    fim = falar(c["audio"], t + 0.2)
    cenas.append(("99_cta", fim - t + 0.8)); t = fim + 0.8
    cenas.append(("00_intro", 0.3)); t += 0.3  # volta à capa: o vídeo emenda no começo (loop)

    finalizar(post, especs, cenas, sons, t, fundo)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
