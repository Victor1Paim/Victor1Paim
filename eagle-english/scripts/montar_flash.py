#!/usr/bin/env python3
"""Monta o vídeo FLASHCARD "What is this called?" (referência R1) a partir de posts/<post>/flash.json.

Uso:  python3 scripts/montar_flash.py posts/<post>
flash.json: {"itens": [{"img": "img/x.png", "en": "...", "pron": "/.../", "pt": "..."}],
             "audio_pergunta": "q_en", "audio_respostas": "respostas_en" (todas numa fala, separadas por pausa)
             ou "audio_resposta" por item, "cta": {"audio": "cta", "telas": [...telas do montar_padrao...]},
             "fundo_cta": "img/fundo_cta.png", "segundos_contagem": 0.8}
A fala com todas as respostas é cortada nas pausas (silencedetect); tem que dar exatamente 1 trecho por item.
"""
import json, re, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from montar_quiz import SR, sh, dur, sfx, preparar_vozes, finalizar  # noqa: E402
import montar_padrao  # noqa: E402

PROJ = Path(__file__).resolve().parents[1]
MASC = PROJ / "assets" / "mascote" / "oficial"


def cortar_respostas(arq, n, pasta, prefixo="resp"):
    r = subprocess.run(["ffmpeg", "-nostdin", "-i", str(arq), "-af", "silencedetect=noise=-40dB:d=0.3", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    ini = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", r)]
    fim = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", r)]
    pausas = [(a + b) / 2 for a, b in zip(ini, fim) if a > 0.05]
    total = dur(arq)
    pausas = [p for p in pausas if p < total - 0.2]
    if len(pausas) != n - 1 and not (pasta.parent / arq.name).exists():   # prévia sem áudio: divide igual
        pausas = [total * (i + 1) / n for i in range(n - 1)]
    if len(pausas) != n - 1:
        sys.exit(f"esperava {n - 1} pausas em {arq.name}, achei {len(pausas)}: regrave a fala com pausas maiores")
    cortes = [0.0] + pausas + [total]
    saidas = []
    for i in range(n):
        out = pasta / f"_{prefixo}_{i + 1}.wav"
        # (o fade de saída é feito com areverse: um afade=out com st=0 zeraria o trecho inteiro)
        sh("-i", str(arq), "-af", f"atrim={cortes[i]:.3f}:{cortes[i + 1]:.3f},asetpts=PTS-STARTPTS,"
           "silenceremove=start_periods=1:start_threshold=-45dB,afade=t=in:d=0.01,"
           "areverse,silenceremove=start_periods=1:start_threshold=-45dB,afade=t=in:d=0.03,areverse,apad=pad_dur=0.1",
           "-ar", str(SR), str(out))
        saidas.append((out, dur(out)))
    return saidas


def main(pasta):
    post = Path(pasta).resolve()
    c = json.loads((post / "flash.json").read_text())
    fx = sfx()
    vozes = preparar_vozes(post, c, 1.0)
    itens = c["itens"]
    if c.get("audio_respostas"):
        resps = cortar_respostas(vozes[c["audio_respostas"]][0], len(itens), post / "audio" / "_mix")
    else:
        resps = [vozes[i["audio_resposta"]] for i in itens]
    aberta, fechada = (MASC / "boca_aberta.png").as_uri(), (MASC / "boca_fechada.png").as_uri()
    conta = c.get("segundos_contagem", 0.8)
    especs, cenas, sons, t = [], [], [], 0.0
    q_arq, q_d = vozes[c["audio_pergunta"]]

    if c.get("audio_traducoes"):
        trads = cortar_respostas(vozes[c["audio_traducoes"]][0], len(itens), post / "audio" / "_mix", "trad")
    else:
        trads = [None] * len(itens)

    # ABERTURA em português: mascote grande no centro, bico abrindo com a voz
    it0 = c.get("intro")
    if it0:
        base = {"tipo": "intro", "selo": it0["selo"], "titulo": it0["titulo"], "sub": it0["sub"],
                "previa": [(post / x).as_uri() for x in it0.get("previa", [])]}
        especs.append(("00_intro_f", {**base, "mascote": fechada}))
        especs.append(("00_intro_a", {**base, "mascote": aberta}))
        a_arq, a_d = vozes[it0["audio"]]
        sons.append((a_arq, 0.15, 1.0))
        total = a_d + 0.5
        abertos = montar_padrao.boca_aberta([(a_arq, 0.15, 1.0)], total)
        cur = 0.0
        for a, b in abertos:
            if a > cur:
                cenas.append(("00_intro_f", a - cur))
            cenas.append(("00_intro_a", b - a)); cur = b
        cenas.append(("00_intro_f", total - cur))
        t = total

    for n, it in enumerate(itens, 1):
        base = {"tipo": "pergunta", "n": n, "total": len(itens), "img": (post / it["img"]).as_uri(), "selo": c.get("selo"),
                "en": it["en"], "pron": it["pron"], "pt": it["pt"]}
        especs.append((f"{n:02d}_q", {**base, "mascote": aberta}))
        sons.append((fx["whoosh"], t, 0.5)); sons.append((q_arq, t + 0.15, 1.0))
        d = q_d + 0.35; cenas.append((f"{n:02d}_q", d)); t += d
        for s in (3, 2, 1):
            especs.append((f"{n:02d}_t{s}", {**base, "timer": s, "mascote": fechada}))
            sons.append((fx["tique"], t, 0.8)); cenas.append((f"{n:02d}_t{s}", conta)); t += conta
        especs.append((f"{n:02d}_r", {**base, "revelar": True, "mascote": aberta}))
        r_arq, r_d = resps[n - 1]
        sons.append((fx["ding"], t, 0.6)); sons.append((r_arq, t + 0.3, 1.0))
        d = 0.3 + r_d + 0.25
        if trads[n - 1]:
            tr_arq, tr_d = trads[n - 1]
            sons.append((tr_arq, t + d, 1.0)); d += tr_d
        d += 0.6
        cenas.append((f"{n:02d}_r", d)); t += d

    # placar + CTA (telas do padrão, renderizadas antes e coladas como imagem)
    k = c["cta"]; arq, d_cta = vozes[k["audio"]]
    especs.append(("90_placar", {"tipo": "placar", "itens": [[i["en"], i["pt"]] for i in itens], "mascote": aberta,
                                 "selo": "PLACAR 🏆", "sub": k.get("sub_placar", "Salva pra praticar depois 📌")}))
    sons.append((fx["whoosh"], t, 0.5)); sons.append((arq, t + 0.2, 1.0))
    seg_placar = k.get("segundos_placar", 3.2)
    cenas.append(("90_placar", seg_placar))
    fundo_cta = (post / c.get("fundo_cta", "img/fundo_cta.png")).as_uri()
    telas = []
    for j, tela in enumerate(k["telas"]):
        if isinstance(tela, dict):
            dd = dict(tela)
            if "capas" in dd:
                dd["capas"] = [montar_padrao.pagina(post, x).as_uri() for x in dd["capas"]]
        else:
            dd = {"tipo": "produto", "tag": tela[0], "pagina": montar_padrao.pagina(post, tela[1]).as_uri()}
        telas.append((f"cta_{j}", dd))
    q = montar_padrao.render(post, telas, fundo_cta)
    from PIL import Image
    mf = Image.open(MASC / "boca_fechada.png"); m = mf.resize((int(mf.width * 400 / mf.height), 400))
    resto = d_cta + 0.2 - seg_placar + 0.8
    for nome, _ in telas:
        im = Image.open(q / f"{nome}.png").convert("RGBA"); im.alpha_composite(m, (20, 1560 - 400))
        im.convert("RGB").save(q / f"{nome}_m.png")
        especs.append((f"{nome}_m", {"tipo": "imagem", "src": (q / f"{nome}_m.png").as_uri()}))
        cenas.append((f"{nome}_m", resto / len(telas)))
    t += seg_placar + resto
    finalizar(post, especs, cenas, sons, t, fundo_cta, template="flash.html", capa=("00_intro_f" if it0 else "01_q"))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
