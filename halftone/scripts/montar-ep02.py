"""Monta a linha do tempo do Ep. 2 "O toque" (versão motion).

Encadeia planos, falas, legendas de Libras e blocos sem fala; estima o tempo de cada palavra
dentro dos trechos de fala medidos; sintetiza a trilha (batida de festa, multidão, mar e toque
de celular) e escreve src/ep02/timeline.json e public/series/ano-zero/t1/ep02/audio/.

Uso: python3 scripts/montar-ep02.py <pasta_das_falas_tratadas>
"""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from importlib import import_module

base = import_module("montar-teste-motion")  # reaproveita medição de fala e tempo das palavras

RAIZ = Path(__file__).resolve().parent.parent
FALAS = Path(sys.argv[1])
OUT_AUDIO = RAIZ / "public/series/ano-zero/t1/ep02/audio"
OUT_JSON = RAIZ / "src/ep02/timeline.json"
SR, FPS = 48000, 30

TEXTO = {
    "b1": ("bia", "Eu conheço esse toque."),
    "b2": ("bia", "Caio? Me mostra onde você tá."),
    "x1": ("multidao", "Moça, desliga isso! Tá todo mundo olhando pra cá."),
    "e1": ("narrador", "Ela viu o nome na tela. O resto, eu não podia saber."),
    "e2": ("narrador", "Quando o toque parou, o mar cobriu tudo de novo. Por uns segundos, ninguém olhava pra ela."),
    "bp1": ("bia_pensa", "Se eu atender, ele me encontra. Se eu não atender... talvez eu nunca mais encontre ele."),
    "a1": ("ambulante", "Moça... aquele cara ali tá te encarando desde que tocou."),
    "b3": ("bia", "Desculpa, Caio."),
    "e3": ("narrador", "Naquela noite, desculpa não era uma rota."),
    "bp2": ("bia_pensa", "Três piscadas. Luz não faz barulho. Ele sabe o que significa."),
    "e4": ("narrador", "Nessa situação... o que você faria?"),
}

# Planos: (id, [itens]); item = ("fala", id, respiro) | ("libras", quem, texto, dur, respiro) | ("pausa", s)
PLANOS = [
    ("toque", [("pausa", 0.5), ("fala", "b1", 0), ("pausa", 0.6)]),
    ("praia", [("fala", "b2", 0.1), ("fala", "x1", 0.3), ("pausa", 0.4)]),
    ("ecos", [("pausa", 3.0)]),
    ("barreira", [("fala", "e1", 0.3), ("fala", "e2", 0.3), ("pausa", 0.5)]),
    ("tela", [("pausa", 0.8), ("fala", "bp1", 0), ("pausa", 0.4)]),
    ("ambulante", [("fala", "a1", 0.1), ("pausa", 0.4)]),
    ("encarando", [("pausa", 2.2)]),
    ("split", [("fala", "b3", 0.3), ("libras", "caio", "Ela recusou.", 2.4, 0.3), ("pausa", 0.3)]),
    ("fluxo", [("fala", "e3", 0.3), ("pausa", 1.0)]),
    ("lanterna", [("fala", "bp2", 0.3), ("pausa", 0.5)]),
    ("decisao", [("fala", "e4", 0.2), ("pausa", 1.0)]),
    ("cartao", [("pausa", 4.2)]),
]


def dur(p):
    with wave.open(str(p)) as w:
        return w.getnframes() / w.getframerate()


def main():
    OUT_AUDIO.mkdir(parents=True, exist_ok=True)
    t = 0.0
    planos, linhas, libras = [], [], []
    for pid, itens in PLANOS:
        ini = t
        for it in itens:
            if it[0] == "pausa":
                t += it[1]
            elif it[0] == "fala":
                _, lid, resp = it
                t += resp
                src = FALAS / f"{lid}.wav"
                d = dur(src)
                quem, texto = TEXTO[lid]
                linhas.append({"id": lid, "quem": quem, "texto": texto, "inicio": round(t, 3), "duracao": round(d, 3),
                               "arquivo": f"series/ano-zero/t1/ep02/audio/{lid}.wav",
                               "palavras": base.tempos_palavras(texto, base.trechos_de_fala(src))})
                subprocess.run(["cp", str(src), str(OUT_AUDIO / f"{lid}.wav")], check=True)
                t += d
            elif it[0] == "libras":
                _, quem, texto, d, resp = it
                t += resp
                libras.append({"quem": quem, "texto": texto, "inicio": round(t, 3), "duracao": d})
                t += d
        planos.append({"id": pid, "inicio": round(ini, 3), "fim": round(t, 3)})
    total = round(t, 2)
    P = {p["id"]: p for p in planos}
    L = {l["id"]: l for l in linhas}

    def palavra(lid, alvo):
        for w in L[lid]["palavras"]:
            if w["w"].lower().startswith(alvo):
                return round(L[lid]["inicio"] + w["t0"], 3)
        raise KeyError(alvo)

    ev = {
    "toqueA": P["toque"]["inicio"] + 0.05,
    "toqueAfim": P["ecos"]["fim"],
    "regra2": palavra("e2", "cobriu"),
    "toqueB": P["tela"]["inicio"] + 0.1,
    "recusa": L["b3"]["inicio"] + L["b3"]["duracao"] + 0.05,
    "freeze": P["decisao"]["inicio"],
}
    # toque em ciclos: rajada de 0,9 s a cada 1,4 s, enquanto ninguém atende
    ciclo = 1.4
    toques = []
    for a, b in [(ev["toqueA"], ev["toqueAfim"]), (ev["toqueB"], ev["recusa"])]:
        k = 0
        while a + k * ciclo < b - 0.15:
            toques.append(round(round((a + k * ciclo) * FPS) / FPS, 4))
            k += 1
    ev["toques"] = toques

    # batida da festa ao longe (sem anéis: é longe e contínua) até o congelamento
    passo = 60 / 124
    batidas = []
    k = 0
    while k * passo < ev["freeze"]:
        batidas.append(round(round(k * passo * FPS) / FPS, 4))
        k += 1

    n = int(total * SR)
    tr = np.zeros(n, dtype=np.float32)
    tt = np.arange(int(0.42 * SR)) / SR
    bumbo = np.sin(2 * np.pi * np.cumsum(46 + 80 * np.exp(-tt * 28)) / SR) * np.exp(-tt * 9)
    for tb in batidas:
        s0 = int(tb * SR)
        e0 = min(n, s0 + len(bumbo))
        tr[s0:e0] += 0.45 * bumbo[: e0 - s0]
    tt2 = np.arange(int(0.9 * SR)) / SR
    toque = (np.sin(2 * np.pi * 880 * tt2) * (np.floor(tt2 * 16) % 2 == 0) + np.sin(2 * np.pi * 660 * tt2) * (np.floor(tt2 * 16) % 2 == 1)) * 0.24
    toque *= np.minimum(1, (0.9 - tt2) * 30)
    for tc in toques:
        s0 = int(tc * SR)
        fim = ev["recusa"] if tc >= ev["toqueB"] else ev["toqueAfim"]
        cut = int((fim - tc) * SR)
        seg = toque[: max(0, min(len(toque), cut, n - s0))]
        tr[s0:s0 + len(seg)] += seg
    raw = RAIZ / "out/ep02-trilha-bruta.wav"
    raw.parent.mkdir(exist_ok=True)
    with wave.open(str(raw), "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(tr, -1, 1) * 32767).astype(np.int16).tobytes())

    fim_cena = P["cartao"]["inicio"]
    fz = ev["freeze"]
    vol_multidao = f"if(gte(t,{fz}),0.0,if(between(t,{P['barreira']['inicio']},{P['barreira']['fim']}),0.5,0.75))"
    vol_mar = f"if(gte(t,{fz}),0.0,if(between(t,{P['barreira']['inicio']},{P['barreira']['fim']})+gte(t,{P['fluxo']['inicio']}),1.0,0.4))"
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(raw),
        "-f", "lavfi", "-t", str(total), "-i", "anoisesrc=color=brown:amplitude=0.5:seed=21:sample_rate=48000",
        "-f", "lavfi", "-t", str(total), "-i", "anoisesrc=color=pink:amplitude=0.25:seed=22:sample_rate=48000",
        "-filter_complex",
        "[0:a]lowpass=f=1600,volume=1.0[b];"
        f"[1:a]lowpass=f=700,highpass=f=90,volume='{vol_multidao}':eval=frame[c];"
        f"[2:a]lowpass=f=1200,highpass=f=200,volume='{vol_mar}*(0.6+0.4*sin(2*PI*t/7))':eval=frame[m];"
        f"[b][c][m]amix=inputs=3:normalize=0,alimiter=limit=0.8[o]",
        "-map", "[o]", "-ar", "48000", "-ac", "2", str(OUT_AUDIO / "trilha.wav")], check=True)

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps({"fps": FPS, "duracao": total, "batidas": batidas, "eventos": ev, "planos": planos,
                                    "linhas": linhas, "libras": libras,
                                    "trilha": "series/ano-zero/t1/ep02/audio/trilha.wav"}, ensure_ascii=False, indent=1))
    print(f"duração {total}s · {len(planos)} planos · {len(linhas)} falas · {len(batidas)} batidas")
    for p in planos:
        print(f"  {p['id']:10} {p['inicio']:6.2f} → {p['fim']:6.2f}")
    print(json.dumps(ev))


if __name__ == "__main__":
    main()
