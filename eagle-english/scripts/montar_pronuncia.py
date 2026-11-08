#!/usr/bin/env python3
"""Monta o vídeo de DICA DE PRONÚNCIA a partir de posts/<post>/pronuncia.json + audio/ + img/.

Uso:  python3 scripts/montar_pronuncia.py posts/2026-11-12_pronuncia-ed
Estrutura: intro → para cada grupo: cartão + voz pt (título) + voz americana (palavras e exemplo)
→ "Sua vez! Repete" (pausa) → voz americana de novo, pra comparar → teste rápido (cartão de pergunta
com contagem) → CTA. Saídas iguais às do montar_quiz.py (final.mp4, capa.png, contato.jpg...).
Falas sem áudio viram silêncio estimado (prévia), com aviso.
"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from montar_quiz import sfx, preparar_vozes, finalizar  # noqa: E402


def main(pasta):
    post = Path(pasta).resolve()
    c = json.loads((post / "pronuncia.json").read_text())
    fx = sfx()
    vozes = preparar_vozes(post, c, c.get("velocidade_pt", 1.0))
    img = post / "img"
    fundo = (img / "fundo.png").as_uri()
    m_fones = (img / "mascote_fones.png").as_uri()
    m_ok = (Path(__file__).resolve().parents[1] / "assets" / "mascote" / "positivo.png").as_uri()
    m_pensa = (Path(__file__).resolve().parents[1] / "assets" / "mascote" / "pensando.png").as_uri()
    especs, cenas, sons = [], [], []

    def falar(ids, inicio, gap=0.25):
        for i in ids:
            arq, d = vozes[i]; sons.append((arq, inicio, 1.0)); inicio += d + gap
        return inicio - gap

    it = c["intro"]
    especs.append(("00_intro", {"tipo": "intro", "selo": it["selo"], "hook": it["hook"], "sub": it["sub"], "mascote": m_fones}))
    fim = falar(it["audio"], 0.15); cenas.append(("00_intro", fim + 0.35)); t = fim + 0.35

    for n, g in enumerate(c["grupos"], 1):
        base = {"tipo": "grupo", "mascote": m_fones, **{k: g[k] for k in ("selo", "regra", "palavras", "exemplo")}}
        especs.append((f"g{n}", base)); especs.append((f"g{n}_vez", {**base, "suavez": True}))
        sons.append((fx["whoosh"], t, 0.6))
        fim = falar(g["audio_titulo"] + g["audio"], t + 0.15, gap=0.35)
        cenas.append((f"g{n}", fim - t + 0.3)); t = fim + 0.3
        sons.append((fx["tique"], t, 0.6))
        rep = c.get("segundos_repetir", 3)
        cenas.append((f"g{n}_vez", rep)); t += rep
        fim = falar(g["audio"], t + 0.1)           # ouve de novo, pra comparar
        cenas.append((f"g{n}", fim - t + 0.45)); t = fim + 0.45

    q = c["teste"]
    base = {"tipo": "pergunta", "n": 1, "total": 1, "mascote": m_pensa,
            **{k: q.get(k) for k in ("selo", "enunciado", "frase", "a", "b", "certa", "pron", "traducao", "nota")}}
    especs.append(("t_0", base))
    sons.append((fx["whoosh"], t, 0.6))
    fim = falar(q["audio_pergunta"], t + 0.15); cenas.append(("t_0", fim - t + 0.15)); t = fim + 0.15
    for s in range(3, 0, -1):
        especs.append((f"t_t{s}", {**base, "timer": s})); sons.append((fx["tique"], t, 0.9))
        cenas.append((f"t_t{s}", 1.0)); t += 1.0
    especs.append(("t_r", {**base, "revelar": True})); sons.append((fx["ding"], t, 0.7))
    fim = falar(q["audio_resposta"], t + 0.35); cenas.append(("t_r", fim - t + 1.2)); t = fim + 1.2

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
