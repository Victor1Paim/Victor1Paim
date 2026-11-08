#!/usr/bin/env python3
"""Monta o vídeo ESCADA DE VELOCIDADE: cada frase em inglês dita lenta → normal → nativo,
com "Sua vez! Repete" depois de cada velocidade. Uma gravação por frase; as velocidades saem
do ffmpeg (atempo, que muda a velocidade sem mudar o tom da voz).

Uso:  python3 scripts/montar_escada.py posts/2026-11-14_telefone-velocidades
"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from montar_quiz import SR, sfx, preparar_vozes, finalizar, sh, dur  # noqa: E402


def main(pasta):
    post = Path(pasta).resolve()
    c = json.loads((post / "escada.json").read_text())
    fx = sfx()
    vozes = preparar_vozes(post, c, c.get("velocidade_pt", 1.0))
    fundo = (post / "img" / "fundo.png").as_uri()
    m_tel = (post / "img" / "mascote_telefone.png").as_uri()
    m_ok = (Path(__file__).resolve().parents[1] / "assets" / "mascote" / "positivo.png").as_uri()
    nomes_vel = [v[0] for v in c["velocidades"]]
    especs, cenas, sons = [], [], []

    def falar(ids, inicio, gap=0.25):
        for i in ids:
            arq, d = vozes[i]; sons.append((arq, inicio, 1.0)); inicio += d + gap
        return inicio - gap

    def veloc(i, fator):
        arq, d = vozes[i]
        if fator == 1.0:
            return arq, d
        out = arq.with_name(f"{i}_x{fator}.wav")
        sh("-i", str(arq), "-af", f"atempo={fator}", "-ar", str(SR), str(out))
        return out, dur(out)

    it = c["intro"]
    especs.append(("00_intro", {"tipo": "intro", "selo": it["selo"], "hook": it["hook"], "sub": it["sub"], "mascote": m_tel}))
    fim = falar(it["audio"], 0.15, gap=0.3); cenas.append(("00_intro", fim + 0.3)); t = fim + 0.3

    rep = c.get("segundos_repetir", 2.2)
    for n, f in enumerate(c["frases"], 1):
        base = {"tipo": "escada", "selo": f"📞 FRASE {n}/{len(c['frases'])}", "titulo": f["titulo"], "en": f["en"],
                "pron": f["pron"], "traducao": f["traducao"], "velocidades": nomes_vel, "mascote": m_tel}
        especs.append((f"f{n}_0", {**base, "atual": -1}))
        sons.append((fx["whoosh"], t, 0.6))
        fim = falar([f["audio_titulo"]], t + 0.15); cenas.append((f"f{n}_0", fim - t + 0.2)); t = fim + 0.2
        for k, (_, fator) in enumerate(c["velocidades"]):
            especs.append((f"f{n}_v{k}", {**base, "atual": k}))
            arq, d = veloc(f["audio"], fator)
            sons.append((arq, t + 0.15, 1.0))
            cenas.append((f"f{n}_v{k}", d + 0.35)); t += d + 0.35
            especs.append((f"f{n}_v{k}_vez", {**base, "atual": k, "suavez": True}))
            sons.append((fx["tique"], t, 0.5))
            cenas.append((f"f{n}_v{k}_vez", rep)); t += rep

    k = c["cta"]
    especs.append(("99_cta", {"tipo": "cta", "titulo": k["titulo"], "comenta": k["comenta"], "itens": k["itens"], "mascote": m_ok}))
    sons.append((fx["whoosh"], t, 0.6))
    fim = falar(k["audio"], t + 0.2); cenas.append(("99_cta", fim - t + 0.8)); t = fim + 0.8
    cenas.append(("00_intro", 0.3)); t += 0.3
    finalizar(post, especs, cenas, sons, t, fundo)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
