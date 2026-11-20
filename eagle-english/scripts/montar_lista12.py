#!/usr/bin/env python3
"""Formato "LISTA 12" (ref. do usuário 19/11, padrão novo SEM mascote): fundo do mar em vídeo, selo do perfil, palavra falada
da vez em verde gigante (legenda palavra por palavra), lista 1)…12) que se completa e cronômetro vertical na contagem.

Sequência por item: "Como se diz X?" → cronômetro (contagem) → resposta em inglês entra na lista (falada uma vez).
Re-ganchos falados depois de alguns itens (curtir / seguir / comentar com emoji) e CTA no fim.

Uso: python3 scripts/montar_lista12.py posts/<post>

posts/<post>/lista.json:
{ "selo": "@eagle.english.br", "fundo_video": "maldivas", "fundo_inicio": 25, "contagem": 2.5,
  "capa": "Como se diz…\\nem inglês? 🤔",
  "itens": [{"en": "Sit down", "q": "q1", "r": "r1"}, …],          # q/r = ids em falas.json (áudio em audio/<id>.wav)
  "reganchos": {"3": "rg1", "6": "rg2", "11": "rg3"},             # fala tocada DEPOIS do item N
  "cta": "cta" }
"""
import json, os, re, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from montar_quiz import SR, FPS, sh, dur, sfx  # noqa: E402
from montar_padrao import trilha_fundo, clipes_fundo  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]


def palavras(modelo, arq, texto, lingua):
    """Tempo de cada palavra (Whisper); se a contagem bater com o texto do roteiro, usa a grafia do roteiro."""
    r = modelo.transcribe(str(arq), language=lingua, word_timestamps=True)
    ws = []
    for w in (w for s in r["segments"] for w in s.get("words", [])):
        if ws and w["word"].strip().startswith("-"):      # "sente" + "-se" → uma palavra só
            ws[-1] = {**ws[-1], "end": w["end"]}
        else:
            ws.append(dict(w))
    tx = [w for w in re.findall(r"[\wÀ-ÿ'’-]+", texto) if w.strip("-")]
    if len(ws) == len(tx):
        return [(t, w["start"], w["end"]) for t, w in zip(tx, ws)]
    print(f"  aviso: {arq.name}: whisper {len(ws)} palavras x roteiro {len(tx)} — distribuindo pelo tempo")
    d = dur(arq); n = max(1, len(tx))
    return [(t, d * i / n, d * (i + 1) / n) for i, t in enumerate(tx)]


def main(pasta):
    post = (PROJ / pasta).resolve() if not Path(pasta).is_absolute() else Path(pasta)
    cfg = json.loads((post / "lista.json").read_text())
    falas = {f["id"]: f for f in json.loads((post / "falas.json").read_text())["falas"]}
    aud = lambda i: post / "audio" / f"{i}.wav"
    import whisper
    modelo = whisper.load_model("turbo")
    fx = sfx()
    itens = cfg["itens"]; n = len(itens); cont = cfg.get("contagem", 2.5)
    sons, falas_t, timers, revela, trechos = [], [], [], [], []

    def falar(fid, t, texto=None):
        a = aud(fid); d = dur(a)
        f = falas[fid]
        sons.append((a, t, 1.0))
        for w, s, e in palavras(modelo, a, texto or f["texto"], f["lingua"]):
            falas_t.append((t + s, t + e, w))
        return d

    t = 0.15
    for i, it in enumerate(itens):
        t0 = t
        t += falar(it["q"], t) + 0.15
        timers.append((t, t + cont))
        for k in range(int(round(cont))):
            sons.append((fx["tique"], t + k * cont / round(cont), 0.45))
        t += cont
        revela.append(t)
        t += falar(it["r"], t, it["en"]) + cfg.get("respiro", 0.55)
        trechos.append((t0, t))
        rg = cfg.get("reganchos", {}).get(str(i + 1))
        if rg:
            t0 = t; t += falar(rg, t) + 0.35; trechos.append((t0, t))
    if cfg.get("cta"):
        t0 = t; t += falar(cfg["cta"], t) + 0.6; trechos.append((t0, t))
    total = t
    print(f"  duração: {total:.1f} s")

    # ESTADOS (o que está na tela em cada instante): palavra da vez, itens revelados, cronômetro
    falas_t.sort()
    def palavra_em(x):
        for k, (s, e, w) in enumerate(falas_t):
            prox = falas_t[k + 1][0] if k + 1 < len(falas_t) else e + 0.3
            fim = prox if prox - e < 0.35 else e + 0.2
            if s <= x < fim:
                return w
        return ""
    def estado(x):
        nrev = sum(1 for r in revela if r <= x + 1e-6)
        tim = None
        for a, b in timers:
            if a <= x < b:
                tim = round((x - a) / (b - a) * 20) / 20
        novo = nrev - 1 if nrev and x - revela[nrev - 1] < 1.2 else -1
        return {"selo": cfg.get("selo", "@eagle.english.br"), "palavra": palavra_em(x),
                "itens": [itens[k]["en"] if k < nrev else "" for k in range(n)], "novo": novo, "timer": tim}
    passo = 1 / 15
    segs = []
    for k in range(int(total / passo) + 1):
        e = estado(k * passo); key = json.dumps(e, ensure_ascii=False, sort_keys=True)
        if segs and segs[-1][0] == key:
            segs[-1][2] += passo
        else:
            segs.append([key, e, passo])
    unicos = {}
    for key, e, _ in segs:
        unicos.setdefault(key, f"e{len(unicos):04d}")
    print(f"  {len(segs)} trechos, {len(unicos)} quadros únicos")

    v = post / "video"; q = v / "quadros"; q.mkdir(parents=True, exist_ok=True)
    for x in q.glob("e*.png"):
        x.unlink()
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        cam = os.environ.get("CHROMIUM_PATH")
        nav = pw.chromium.launch(executable_path=cam) if cam else pw.chromium.launch()
        for key, nome in unicos.items():
            pg = nav.new_page(viewport={"width": 1080, "height": 1920})
            pg.add_init_script(f"window.DADOS = {key};")
            pg.goto((PROJ / "templates" / "lista12.html").as_uri())
            pg.wait_for_selector("body[data-pronto='1']")
            pg.screenshot(path=str(q / f"{nome}.png"), omit_background=True); pg.close()
        # capa: quadro do 1º clipe + título, lista vazia
        cap = v / "_capa_fundo.jpg"
        sh("-ss", "3", "-i", str(clipes_fundo(cfg)[0]), "-frames:v", "1", "-vf", "scale=1080:1920", str(cap))
        dc = {"selo": cfg.get("selo", "@eagle.english.br"), "titulo": cfg.get("capa", "Como se diz…\nem inglês?"),
              "itens": [""] * n, "novo": -1, "timer": None, "fundo": cap.as_uri(), "sub": cfg.get("capa_sub", "")}
        pg2 = nav.new_page(viewport={"width": 1080, "height": 1920})
        pg2.add_init_script(f"window.DADOS = {json.dumps(dc, ensure_ascii=False)};")
        pg2.goto((PROJ / "templates" / "lista12.html").as_uri()); pg2.wait_for_selector("body[data-pronto='1']")
        pg2.screenshot(path=str(v / "capa.png")); cap.unlink()
        nav.close()

    lista = v / "cenas.txt"
    with open(lista, "w") as f:
        for key, _, d in segs:
            f.write(f"file '{q / (unicos[key] + '.png')}'\nduration {d:.4f}\n")
        f.write(f"file '{q / (unicos[segs[-1][0]] + '.png')}'\n")
    ov = v / "_camada.mov"
    sh("-f", "concat", "-safe", "0", "-i", str(lista), "-vf", f"fps={FPS},format=argb", "-c:v", "qtrle", str(ov))
    bg = trilha_fundo(post, cfg, trechos, total)

    # ÁUDIO: falas + tiques, loudness -14 LUFS em duas passadas
    ent, fil = [], []
    for k, (arq, ini, vol) in enumerate(sons):
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
    sh("-i", str(bg), "-i", str(ov), "-i", str(audio), "-filter_complex", "[0:v]eq=brightness=-0.07:saturation=1.08[b];[b][1:v]overlay=0:0:shortest=1,format=yuv420p[v]",
       "-map", "[v]", "-map", "2:a", "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "aac", "-b:a", "192k",
       "-t", f"{total:.3f}", "-movflags", "+faststart", str(final))
    for x in (bruto, audio, ov, bg, lista):
        x.unlink(missing_ok=True)
    sh("-i", str(final), "-vf", f"fps=1/{max(1, total / 24):.3f},scale=270:480,tile=6x4", "-frames:v", "1", str(v / "contato.jpg"))
    r = subprocess.run(["ffmpeg", "-nostdin", "-i", str(final), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    lufs = float(r[r.rindex("I:"):].split()[1])
    if abs(lufs + 14) > 0.5:   # o limitador puxa a fala curta para baixo: corrige o ganho e limita de novo
        tmp = final.with_name("_ganho.mp4")
        sh("-i", str(final), "-c:v", "copy", "-af", f"volume={-14 - lufs:.2f}dB,alimiter=limit=0.89:level=false",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(tmp))
        tmp.replace(final)
        r = subprocess.run(["ffmpeg", "-nostdin", "-i", str(final), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    print(f"ok -> {final.relative_to(PROJ)}  ({total:.1f} s, {r[r.rindex('I:'):].split()[1]} LUFS)")


if __name__ == "__main__":
    main(sys.argv[1])
