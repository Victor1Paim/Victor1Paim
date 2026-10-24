"""Monta a linha do tempo do Ep. 1 "A mão" (versão motion).

Encadeia planos, falas, legendas de Libras e blocos sem fala; estima o tempo de cada palavra
dentro dos trechos de fala medidos; sintetiza a trilha (batida de festa, multidão, mar e toque
de celular) e escreve src/ep01/timeline.json e public/series/ano-zero/t1/ep01/audio/.

Uso: python3 scripts/montar-ep01.py <pasta_das_falas_tratadas>
"""
import json, subprocess, sys, wave
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from importlib import import_module

base = import_module("montar-teste-motion")  # reaproveita medição de fala e tempo das palavras

RAIZ = Path(__file__).resolve().parent.parent
FALAS = Path(sys.argv[1])
OUT_AUDIO = RAIZ / "public/series/ano-zero/t1/ep01/audio"
OUT_JSON = RAIZ / "src/ep01/timeline.json"
SR, FPS = 48000, 30

TEXTO = {
    "bp1": ("bia_pensa", "Eu soltei primeiro. Não ele."),
    "e1": ("narrador", "Eu passei anos dizendo que a multidão separou os dois. É uma versão limpa."),
    "e2": ("narrador", "A câmera não gravou o que a Bia pensava. Só o segundo em que ela escolheu pra onde olhar."),
    "b1": ("bia", "Vocês dois ficam do meu lado. A avenida tá fechada."),
    "r1": ("rafa", "Eu sei. Por isso tô te pedindo, não te puxando."),
    "b2": ("bia", "Caio, se a gente se perder?"),
    "b3": ("bia", "Eu também lembro. Só não some sem me avisar."),
    "r2": ("rafa", "Bia, olha. O segurança caiu. Vou chamar alguém."),
    "x1": ("multidao", "Dá espaço! Ele tá respirando?"),
    "e3": ("narrador", "A gravação ficou muda por dois minutos. Eu achei que tinha acabado."),
    "b4": ("bia", "Ninguém encosta nele."),
    "r3": ("rafa", "Então por que a cabeça dele ainda marca a batida?"),
    "bp2": ("bia_pensa", "Eu chamei aquilo de cuidado. Era raiva, porque ele decidiu sem mim."),
}

# Planos: (id, [itens]); item = ("fala", id, respiro) | ("libras", quem, texto, dur, respiro) | ("pausa", s)
PLANOS = [
    ("mao", [("pausa", 0.4), ("fala", "bp1", 0), ("pausa", 0.7)]),
    ("rebobina", [("pausa", 0.9), ("fala", "e1", 0), ("pausa", 0.4)]),
    ("calcadao", [("libras", "caio", "O palco menor tá livre. Vou com o Rafa.", 2.9, 0.1)]),
    ("closeBia", [("fala", "e2", 0.2), ("pausa", 0.3)]),
    ("caminho", [("fala", "b1", 0.1), ("fala", "r1", 0.15), ("pausa", 0.2)]),
    ("beiramar", [("fala", "b2", 0.1), ("libras", "caio", "Prédio da Dinda. Eu lembro.", 2.3, 0.1), ("pausa", 0.1)]),
    ("palcoAlto", [("fala", "b3", 0.1), ("pausa", 0.8)]),
    ("cracha", [("fala", "r2", 0.1), ("fala", "x1", 0.1), ("pausa", 0.3)]),
    ("imovel", [("pausa", 0.6), ("fala", "e3", 0), ("pausa", 0.6)]),
    ("levanta", [("pausa", 2.4), ("fala", "b4", 0), ("pausa", 0.4)]),
    ("camadas", [("fala", "r3", 0.1), ("pausa", 0.8)]),
    ("barreira", [("fala", "bp2", 0.2), ("pausa", 0.4)]),
    ("lanterna", [("pausa", 2.4)]),
    ("celular", [("pausa", 2.6)]),
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
                               "arquivo": f"series/ano-zero/t1/ep01/audio/{lid}.wav",
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
        "queda": palavra("r2", "caiu"),
        "pulo23_02": P["imovel"]["inicio"] + 0.6,
        "batidaVolta": P["levanta"]["inicio"],
        "batidaPara": P["camadas"]["fim"] - 0.6,
        "toque1": P["celular"]["inicio"] + 0.35,
        "toque2": P["celular"]["inicio"] + 1.75,
    }

    # batida 124 bpm nas janelas de festa
    passo = 60 / 124
    janelas = [(0.0, P["mao"]["fim"]), (P["rebobina"]["inicio"] + 0.9, P["imovel"]["inicio"]),
               (ev["batidaVolta"], ev["batidaPara"])]
    buraco = (1.0, 1.5)  # o grave some por meio segundo no gancho
    batidas = []
    for a, b in janelas:
        k = 0
        while True:
            tb = round(round((a + k * passo) * FPS) / FPS, 4)
            if tb >= b:
                break
            if not (buraco[0] <= tb < buraco[1]):
                batidas.append(tb)
            k += 1

    n = int(total * SR)
    tr = np.zeros(n, dtype=np.float32)
    tt = np.arange(int(0.42 * SR)) / SR
    bumbo = np.sin(2 * np.pi * np.cumsum(46 + 80 * np.exp(-tt * 28)) / SR) * np.exp(-tt * 9)
    rng = np.random.default_rng(11)
    hat = rng.standard_normal(int(0.05 * SR)) * np.exp(-np.arange(int(0.05 * SR)) / SR * 90) * 0.12
    for tb in batidas:
        s = int(tb * SR)
        e = min(n, s + len(bumbo))
        # na volta da batida (o eco), mais seca e mais alta
        g = 1.15 if tb >= ev["batidaVolta"] else 0.85
        tr[s:e] += g * bumbo[: e - s]
        h = int((tb + passo / 2) * SR)
        if h + len(hat) < n and tb < ev["batidaVolta"]:
            tr[h:h + len(hat)] += hat
    # toque de celular: dois tons alternados em ciclo; o segundo é cortado
    tt2 = np.arange(int(0.9 * SR)) / SR
    toque = (np.sin(2 * np.pi * 880 * tt2) * (np.floor(tt2 * 16) % 2 == 0) + np.sin(2 * np.pi * 660 * tt2) * (np.floor(tt2 * 16) % 2 == 1)) * 0.22
    toque *= np.minimum(1, (0.9 - tt2) * 30)
    for k, tc in enumerate([ev["toque1"], ev["toque2"]]):
        s = int(tc * SR)
        cut = int((P["celular"]["fim"] - tc) * SR) if k == 1 else len(toque)
        seg = toque[: max(0, min(len(toque), cut, n - s))]
        tr[s:s + len(seg)] += seg
    raw = RAIZ / "out/ep01-trilha-bruta.wav"
    raw.parent.mkdir(exist_ok=True)
    with wave.open(str(raw), "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(tr, -1, 1) * 32767).astype(np.int16).tobytes())

    mudo_a, mudo_b = P["imovel"]["inicio"], P["imovel"]["fim"]
    mar_a, mar_b = P["beiramar"]["inicio"], P["beiramar"]["fim"]
    fim_cena = P["cartao"]["inicio"]
    vol_multidao = (f"if(between(t,{mudo_a},{mudo_b}),0.12,if(gte(t,{fim_cena}),0.15,"
                    f"if(between(t,{P['barreira']['inicio']},{P['celular']['fim']}),0.45,0.8)))")
    vol_mar = f"if(between(t,{mar_a},{mar_b})+between(t,{ev['batidaPara']},{fim_cena}),0.9,0.35)"
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(raw),
        "-f", "lavfi", "-t", str(total), "-i", "anoisesrc=color=brown:amplitude=0.5:seed=5:sample_rate=48000",
        "-f", "lavfi", "-t", str(total), "-i", "anoisesrc=color=pink:amplitude=0.25:seed=8:sample_rate=48000",
        "-filter_complex",
        "[0:a]lowpass=f=1400,volume=1.0[b];"
        f"[1:a]lowpass=f=700,highpass=f=90,volume='{vol_multidao}':eval=frame[c];"
        f"[2:a]lowpass=f=1200,highpass=f=200,volume='{vol_mar}*(0.6+0.4*sin(2*PI*t/7))':eval=frame[m];"
        f"[b][c][m]amix=inputs=3:normalize=0,afade=t=out:st={total - 1.5}:d=1.5,alimiter=limit=0.8[o]",
        "-map", "[o]", "-ar", "48000", "-ac", "2", str(OUT_AUDIO / "trilha.wav")], check=True)

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps({"fps": FPS, "duracao": total, "batidas": batidas, "eventos": ev, "planos": planos,
                                    "linhas": linhas, "libras": libras,
                                    "trilha": "series/ano-zero/t1/ep01/audio/trilha.wav"}, ensure_ascii=False, indent=1))
    print(f"duração {total}s · {len(planos)} planos · {len(linhas)} falas · {len(batidas)} batidas")
    for p in planos:
        print(f"  {p['id']:10} {p['inicio']:6.2f} → {p['fim']:6.2f}")
    print(json.dumps(ev))


if __name__ == "__main__":
    main()
