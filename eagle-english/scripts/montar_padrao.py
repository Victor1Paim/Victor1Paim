#!/usr/bin/env python3
"""Monta um Reel no PADRÃO OFICIAL do perfil (docs/PADRAO_VIDEO.md) a partir de posts/<post>/roteiro.json.

Uso:  python3 scripts/montar_padrao.py posts/<post> [--previa]
  --previa: só renderiza os quadros e a folha de contato (sem vídeo).

roteiro.json:
{
  "fundo": "img/fundo.png",                    # foto do cenário (cor cheia, sem texto)
  "velocidade_pt": 1.0,
  "beats": [
    {"tipo": "abertura", "texto": "…", "audio": ["00_gancho"]},
    {"tipo": "frase", "en": "…", "pron": "/…/", "pt": "…", "audio_en": "f1_en", "audio_pt": "f1_pt"},
    {"tipo": "ponte", "texto": "Não sei se você *ficou sabendo*,\\nmas …", "audio": ["ponte"]},
    {"tipo": "produto", "audio": ["produto"], "telas": [["O *Eagle 350*", "ebook_capa"], ["350 mapas · *35 situações*", "mapa_x"]]},
    {"tipo": "escolha", "img": "img/cafe.png", "a": "hot", "b": "cold", "certa": "a", "audio_q": "q1",
     "en": "The coffee is hot.", "pron": "/…/", "pt": "…", "audio_en": "r1_en", "audio_pt": "r1_pt"},   # "Qual você usa?"
    {"tipo": "oferta", "audio": "original"}   # ou o id de uma fala nossa (o vídeo da oferta fica mudo)
  ]
}
Páginas: nome de arquivo em assets/marca/paginas/ (sem .png) ou caminho relativo ao post.
Mascote: assets/mascote/oficial/boca_fechada.png e boca_aberta.png (mesmo enquadramento),
grande no centro nas legendas e pequeno no canto nas telas do produto; o bico abre com a voz.
"""
import json, subprocess, sys, wave
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from montar_quiz import SR, FPS, sh, dur, preparar_vozes  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
MASC = PROJ / "assets" / "mascote" / "oficial"
OFERTA = PROJ / "assets" / "marca" / "fechamento_oferta.mp4"
GRANDE = (860, 1730)   # altura do mascote, linha do chão (y) — centro da tela
PEQUENO = (400, 1560)  # altura, chão — canto inferior esquerdo
MEDIO = (380, 1640)    # altura, chão — centro, abaixo da legenda (formato "Qual você usa?")


def pagina(post, nome):
    for p in (PROJ / "assets/marca/paginas" / f"{nome}.png", PROJ / "assets/marca/paginas/site" / f"{nome}.webp"):
        if p.exists():
            return p
    return post / nome


def render(post, especs, fundo):
    import os
    from playwright.sync_api import sync_playwright
    q = post / "video" / "quadros"; q.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        cam = os.environ.get("CHROMIUM_PATH")
        nav = pw.chromium.launch(executable_path=cam) if cam else pw.chromium.launch()
        for nome, dados in especs:
            pg = nav.new_page(viewport={"width": 1080, "height": 1920})
            pg.add_init_script(f"window.DADOS = {json.dumps({'fundo': fundo, **dados}, ensure_ascii=False)};")
            pg.goto((PROJ / "templates" / "padrao.html").as_uri())
            pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready")
            pg.screenshot(path=str(q / f"{nome}.png")); pg.close()
        nav.close()
    return q


def boca_aberta(sons, total):
    """Intervalos em que o bico fica aberto: voz acima do limiar, abrindo e fechando a cada ~1/8 s."""
    passo = 1 / 8
    n = int(total / passo) + 1
    env = np.zeros(n)
    for arq, ini, _ in sons:
        with wave.open(str(arq)) as w:
            x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float) / 32768
            sr = w.getframerate()
        k = int(sr * passo)
        for j in range(len(x) // k):
            i = int((ini + j * passo) / passo)
            if i < n:
                env[i] = max(env[i], np.sqrt((x[j * k:(j + 1) * k] ** 2).mean()))
    falando = env > 0.03
    abertos, i = [], 0
    while i < n:
        if falando[i] and (i % 2 == 0):
            abertos.append((round(i * passo, 3), round((i + 1) * passo, 3)))
        i += 1
    return abertos


def antes_do_corpo(post, r, vozes, corpo):
    """Junta [abertura animada (scripts/abertura.py)] + [publi (vídeo pronto)] + corpo. Devolve o arquivo juntado (sem loudness)."""
    from montar_quiz import sfx
    v = post / "video"; partes = []
    if r.get("abertura"):
        import abertura
        a = r["abertura"]; arq, d = vozes[a["audio"]]
        qs, dab = abertura.render_abertura(post, a, (arq, d))
        ab = v / "_abertura.mp4"; w = int((dab - 0.55) * 1000)
        sh("-framerate", str(FPS), "-i", str(qs[0].parent / "q%04d.png"), "-i", str(arq), "-i", str(sfx()["whoosh"]),
           "-filter_complex", f"[1:a]adelay=150|150[a1];[2:a]volume=0.6,adelay={w}|{w}[a2];"
           f"[a1][a2]amix=inputs=2:normalize=0,apad=whole_dur={dab:.3f},atrim=0:{dab:.3f}[a]",
           "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "pcm_s16le",
           "-f", "matroska", str(ab))
        partes.append(ab)
    if r.get("publi"):
        partes.append((post / r["publi"]).resolve())
    partes.append(corpo)
    ent = sum((["-i", str(x)] for x in partes), [])
    fc = "".join(f"[{i}:v]fps={FPS},scale=1080:1920,setsar=1,format=yuv420p[v{i}];[{i}:a]aresample=48000,aformat=channel_layouts=stereo[a{i}];"
                 for i in range(len(partes)))
    fc += "".join(f"[v{i}][a{i}]" for i in range(len(partes))) + f"concat=n={len(partes)}:v=1:a=1[v][a]"
    junto = v / "_junto.mkv"
    sh(*ent, "-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "17", "-c:a", "pcm_s16le", str(junto))
    for x in partes:
        if x.name.startswith("_abertura"):
            x.unlink()
    return junto


def main(pasta, previa=False):
    post = Path(pasta).resolve()
    r = json.loads((post / "roteiro.json").read_text())
    vozes = preparar_vozes(post, r, r.get("velocidade_pt", 1.0))
    fundo = (post / r.get("fundo", "img/fundo.png")).as_uri()
    from montar_quiz import sfx
    fx = sfx(); efeitos = []   # tique/ding: entram no áudio, mas não abrem o bico do mascote
    especs, cenas, sons, janelas = [], [], [], []   # janelas do mascote: (inicio, fim, "grande"/"pequeno")
    t, oferta = 0.0, None

    def falar(ids, ini, gap=0.25):
        for i in ids:
            arq, d = vozes[i]; sons.append((arq, ini, 1.0)); ini += d + gap
        return ini - gap

    for n, b in enumerate(r["beats"]):
        k0 = len(especs)
        tp = b["tipo"]
        if tp == "oferta":
            oferta = b; break
        if tp in ("abertura", "ponte"):
            nome = f"{n:02d}_{tp}"
            especs.append((nome, {"tipo": tp, "texto": b["texto"]}))
            fim = falar(b["audio"], t + 0.1); d = fim - t + 0.35
            cenas.append((nome, d)); janelas.append((t, t + d, "grande")); t += d
        elif tp == "frase":
            a, c = f"{n:02d}_frase", f"{n:02d}_frase_pt"
            nfrase = sum(1 for x in r["beats"][:n + 1] if x["tipo"] == "frase")
            tfrase = sum(1 for x in r["beats"] if x["tipo"] == "frase")
            base = {"tipo": "frase", "en": b["en"], "pron": b.get("pron"), "pt": b.get("pt"),
                    "progresso": f"{nfrase}/{tfrase}" if r.get("progresso", True) else ""}
            especs += [(a, base), (c, {**base, "mostrar_pt": True})]
            fim = falar([b["audio_en"]], t + 0.1); d1 = fim - t + 0.2 + r.get("pausa_repetir", 0)   # tempo pra pessoa repetir
            cenas.append((a, d1)); ini_pt = t + d1
            fim = falar([b["audio_pt"]], ini_pt) if b.get("audio_pt") else ini_pt + 1.2
            d2 = fim - ini_pt + 0.3
            cenas.append((c, d2)); janelas.append((t, t + d1 + d2, "grande")); t += d1 + d2
        elif tp == "escolha":   # cena → A×B → contagem 3-2-1 → revela → frase em inglês → tradução
            ne = sum(1 for x in r["beats"][:n + 1] if x["tipo"] == "escolha")
            te = sum(1 for x in r["beats"] if x["tipo"] == "escolha")
            base = {"tipo": "escolha", "img": (post / b["img"]).as_uri(), "a": b["a"], "b": b["b"], "certa": b["certa"],
                    "progresso": f"{ne}/{te}"}
            t0 = t
            fim = falar(b["audio_q"] if isinstance(b["audio_q"], list) else [b["audio_q"]], t + 0.1)
            nome = f"{n:02d}_esc_q"; especs.append((nome, base)); d = fim - t + 0.2; cenas.append((nome, d)); t += d
            for k in (3, 2, 1):
                nome = f"{n:02d}_esc_{k}"; especs.append((nome, {**base, "num": str(k)}))
                efeitos.append((fx["tique"], t, 0.8)); cenas.append((nome, r.get("segundos_contagem", 0.7)))
                t += r.get("segundos_contagem", 0.7)
            rv = {**base, "estado": "revela"}
            nome = f"{n:02d}_esc_rv"; especs.append((nome, rv)); efeitos.append((fx["ding"], t, 0.7))
            cenas.append((nome, 0.5)); t += 0.5
            frase = {**rv, "en": b["en"], "pron": b.get("pron"), "pt": b.get("pt")}
            nome = f"{n:02d}_esc_en"; especs.append((nome, frase))
            fim = falar([b["audio_en"]], t + 0.05); d = fim - t + 0.2 + r.get("pausa_repetir", 0); cenas.append((nome, d)); t += d
            nome = f"{n:02d}_esc_pt"; especs.append((nome, {**frase, "mostrar_pt": True}))
            fim = falar([b["audio_pt"]], t); d = fim - t + 0.3; cenas.append((nome, d)); t += d
            janelas.append((t0, t, "medio"))
        elif tp == "produto":
            fim = falar(b["audio"], t + 0.1); total = fim - t + 0.3
            telas = b["telas"]; cada = total / len(telas)
            for k, tela in enumerate(telas):
                nome = f"{n:02d}_produto_{k}"
                if isinstance(tela, dict):   # telas "kit" e "preco" (fechamento novo)
                    dados = dict(tela)
                    if "capas" in dados:
                        dados["capas"] = [pagina(post, c).as_uri() for c in dados["capas"]]
                    dados.setdefault("tipo", "produto")
                else:
                    tag, pag = tela
                    dados = {"tipo": "produto", "tag": tag, "pagina": pagina(post, pag).as_uri()}
                especs.append((nome, dados))
                cenas.append((nome, tela.get("segundos", cada) if isinstance(tela, dict) else cada))
            janelas.append((t, t + total, "pequeno")); t += total
        if b.get("fundo"):   # cenário próprio deste trecho (regra de cenários do V3)
            for i in range(k0, len(especs)):
                especs[i] = (especs[i][0], {**especs[i][1], "fundo": (post / b["fundo"]).as_uri()})

    q = render(post, especs, fundo)
    # folha de contato (com o mascote por cima, como vai ficar)
    from PIL import Image
    mf = Image.open(MASC / "boca_fechada.png")
    cols = 6; lin = (len(especs) + cols - 1) // cols
    folha = Image.new("RGB", (cols * 270, lin * 480), "white")
    for i, (nm, dados) in enumerate(especs):
        im = Image.open(q / f"{nm}.png").convert("RGBA")
        h, chao = PEQUENO if dados["tipo"] in ("produto", "kit", "preco") else MEDIO if dados["tipo"] == "escolha" else GRANDE
        m = mf.resize((int(mf.width * h / mf.height), h))
        x = 20 if dados["tipo"] in ("produto", "kit", "preco") else (1080 - m.width) // 2
        im.alpha_composite(m, (x, chao - h))
        folha.paste(im.convert("RGB").resize((270, 480)), ((i % cols) * 270, (i // cols) * 480))
    folha.save(post / "video" / "contato.jpg", quality=85)
    capa = Image.open(q / f"{especs[0][0]}.png").convert("RGBA")
    h, chao = GRANDE; m = mf.resize((int(mf.width * h / mf.height), h))
    capa.alpha_composite(m, ((1080 - m.width) // 2, chao - h)); capa.convert("RGB").save(post / "video" / "capa.png")
    if (post / "capa.json").exists():   # capa produzida (templates/capa.html) substitui a simples
        import capa as capa_prod
        capa_prod.capas([post])
    if previa:
        print(f"prévia: {len(especs)} quadros, ~{t:.1f} s + oferta -> video/contato.jpg"); return

    v = post / "video"
    lista = v / "cenas.txt"
    with open(lista, "w") as f:
        for nome, d in cenas:
            f.write(f"file '{q / (nome + '.png')}'\nduration {round(d * FPS) / FPS:.4f}\n")
        f.write(f"file '{q / (cenas[-1][0] + '.png')}'\n")
    base = v / "_base.mp4"
    sh("-f", "concat", "-safe", "0", "-i", str(lista), "-vf", f"fps={FPS},format=yuv420p", "-c:v", "libx264", "-crf", "17", str(base))

    # mascote: fechado sempre (na janela) + aberto por cima nos instantes de fala; balanço leve
    abertos = boca_aberta(sons, t)
    ent = ["-i", str(base)]
    fc, ultimo, k = [], "[0:v]", 1
    for tam in ("grande", "pequeno", "medio"):
        js = [j for j in janelas if j[2] == tam]
        if not js:
            continue
        h, chao = {"grande": GRANDE, "pequeno": PEQUENO, "medio": MEDIO}[tam]
        x = "20" if tam == "pequeno" else "(W-w)/2"
        y = f"{chao}-h+6*sin(2*PI*t*0.9)"
        dentro = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b, _ in js)
        abre = "+".join(f"between(t,{a},{b})" for a, b in abertos
                        if any(ja <= a < jb for ja, jb, _ in js)) or "0"
        for estado, en in (("fechada", dentro), ("aberta", f"({dentro})*({abre})")):
            ent += ["-loop", "1", "-i", str(MASC / f"boca_{estado}.png")]
            fc.append(f"[{k}:v]scale=-1:{h},format=rgba[m{k}]")
            fc.append(f"{ultimo}[m{k}]overlay=x={x}:y='{y}':enable='{en}':shortest=1[v{k}]")
            ultimo, k = f"[v{k}]", k + 1
    com_masc = v / "_masc.mp4"
    sh(*ent, "-filter_complex", ";".join(fc), "-map", ultimo, "-c:v", "libx264", "-crf", "17", "-t", f"{t:.3f}", str(com_masc))

    # áudio das falas
    ent, fil = [], []
    sons = sons + efeitos
    for i, (arq, ini, vol) in enumerate(sons):
        ent += ["-i", str(arq)]; ms = int(round(ini * 1000))
        fil.append(f"[{i}:a]aresample={SR},aformat=channel_layouts=mono,volume={vol},adelay={ms}|{ms}[s{i}]")
    fil.append("".join(f"[s{i}]" for i in range(len(sons))) +
               f"amix=inputs={len(sons)}:normalize=0,apad=whole_dur={t:.3f},atrim=0:{t:.3f},aformat=channel_layouts=stereo[a]")
    voz = v / "_voz.wav"
    sh(*ent, "-filter_complex", ";".join(fil), "-map", "[a]", "-ar", str(SR), str(voz))

    # junta com a oferta (vídeo pronto do perfil)
    final = v / "final.mp4"
    if oferta:
        if oferta.get("audio", "original") == "original":
            fa = "[1:a]aresample=48000,aformat=channel_layouts=stereo[oa]"
            ent2 = ["-i", str(com_masc), "-i", str(OFERTA), "-i", str(voz)]
            fc2 = (f"[0:v]setsar=1[v0];[1:v]scale=1080:1920,fps={FPS},setsar=1[v1];{fa};"
                   "[v0][2:a][v1][oa]concat=n=2:v=1:a=1[v][a0]")
        else:
            arq, d = vozes[oferta["audio"]]
            ent2 = ["-i", str(com_masc), "-i", str(OFERTA), "-i", str(voz), "-i", str(arq)]
            fc2 = (f"[0:v]setsar=1[v0];[1:v]scale=1080:1920,fps={FPS},setsar=1[v1];"
                   f"[3:a]aresample=48000,aformat=channel_layouts=stereo,adelay=300|300,apad,atrim=0:{dur(OFERTA):.3f}[oa];"
                   "[v0][2:a][v1][oa]concat=n=2:v=1:a=1[v][a0]")
        bruto = v / "_bruto.mp4"
        sh(*ent2, "-filter_complex", fc2, "-map", "[v]", "-map", "[a0]", "-c:v", "libx264", "-crf", "17",
           "-c:a", "pcm_s16le", "-f", "matroska", str(bruto))
        fonte = bruto
    else:
        fonte = None
        bruto = v / "_bruto.mp4"
        sh("-i", str(com_masc), "-i", str(voz), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "pcm_s16le",
           "-f", "matroska", str(bruto))
        fonte = bruto
    if r.get("abertura") or r.get("publi"):   # abertura animada + anúncio ANTES das frases (série Natal)
        fonte = antes_do_corpo(post, r, vozes, fonte)
    alvo = "I=-14:TP=-1.5:LRA=11"
    m = subprocess.run(["ffmpeg", "-nostdin", "-i", str(fonte), "-af", f"loudnorm={alvo}:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    m = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
    sh("-i", str(fonte), "-c:v", "copy", "-af",
       f"loudnorm={alvo}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
       f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true",
       "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(final))
    for x in (lista, base, com_masc, voz, bruto, v / "_junto.mkv"):
        x.unlink(missing_ok=True)
    print(f"ok -> {final.relative_to(PROJ)}  ({dur(final):.1f} s)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1], "--previa" in sys.argv)
