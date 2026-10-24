"""Monta a linha do tempo do teste motion do Ano Zero.

Lê as falas tratadas (wav), mede os trechos de fala, estima o tempo de cada palavra,
posiciona tudo na linha do tempo, sintetiza a trilha (batida distante + multidão) e
escreve src/motion/timeline.json e public/series/ano-zero/teste-motion/audio/.

Uso: python3 scripts/montar-teste-motion.py <pasta_das_falas_tratadas>
"""
import json, re, subprocess, sys, wave
from pathlib import Path
import numpy as np

RAIZ = Path(__file__).resolve().parent.parent
FALAS_DIR = Path(sys.argv[1])
OUT_AUDIO = RAIZ / "public/series/ano-zero/teste-motion/audio"
OUT_JSON = RAIZ / "src/motion/timeline.json"
SR = 48000
FPS = 30

TEXTOS = {
    "n05": ("narrador", "Ele virou a cabeça. No ritmo."),
    "n01": ("narrador", "Trinta e um de dezembro. Dois milhões de pessoas de branco em Copacabana, esperando os fogos."),
    "r01": ("rafa", "Bia, relaxa! É Réveillon!"),
    "b01": ("bia", "Rafa, não tira o olho do Caio."),
    "n02": ("narrador", "Perto do palco, um homem com crachá de laboratório tremia. Os dedos batiam sozinhos, no ritmo da música."),
    "a01": ("ambulante", "Ô, meu amigo, tá passando mal?"),
    "n03": ("narrador", "Aí o DJ cortou o som. E o homem parou de respirar."),
    "b02": ("bia", "Alguém chama um médico!"),
    "n04": ("narrador", "Quando a batida voltou... ele levantou junto com ela."),
    "r02": ("rafa", "Gente... ele tá dançando?"),
    "b03": ("bia", "Rafa, sai daí!"),
    "n06": ("narrador", "Faltavam cinquenta e oito minutos para a virada. E ninguém sabia o que tinha acabado de acordar."),
}

# Ordem e respiro antes de cada fala (s). Começa depois do gancho e do cartão.
ROTEIRO = [("n05", 0.35), ("n01", 1.6), ("r01", 0.3), ("b01", 0.15), ("n02", 2.4),
           ("a01", 0.2), ("n03", 0.3), ("b02", 0.2), ("n04", 1.1), ("r02", 0.2),
           ("b03", 0.9), ("n06", 0.5)]
# Libras do Caio (texto, sem voz): aparece depois da fala indicada.
LIBRAS = [("b01", 0.15, 2.2, "caio", "Eu tô do lado de vocês, gente.")]


def dur(p):
    with wave.open(str(p)) as w:
        return w.getnframes() / w.getframerate()


def trechos_de_fala(p):
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(p), "-af", "silencedetect=n=-42dB:d=0.18", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    ini = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    fim = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    total = dur(p)
    # trechos de fala = complemento dos silêncios
    fala, t = [], 0.0
    for a, b in zip(ini, fim + [total] * (len(ini) - len(fim))):
        if a - t > 0.05:
            fala.append((t, a))
        t = b
    if total - t > 0.05:
        fala.append((t, total))
    return fala or [(0.0, total)]


def silabas(palavra):
    return max(1, len(re.findall(r"[aeiouáéíóúâêôãõà]+", palavra.lower())))


def tempos_palavras(texto, fala):
    """Distribui as palavras pelos trechos de fala, proporcional às sílabas."""
    palavras = texto.split()
    pesos = [silabas(p) + (0.6 if re.search(r"[.,!?…]$", p) else 0) for p in palavras]
    total_fala = sum(b - a for a, b in fala)
    total_peso = sum(pesos)
    res, acc = [], 0.0

    def mapa(x):  # tempo "de fala" contínuo -> tempo real no arquivo
        for a, b in fala:
            if x <= b - a + 1e-9:
                return a + x
            x -= b - a
        return fala[-1][1]

    for p, w in zip(palavras, pesos):
        t0 = acc / total_peso * total_fala
        acc += w
        t1 = acc / total_peso * total_fala
        res.append({"w": p, "t0": round(mapa(t0), 3), "t1": round(mapa(t1) - 0.02, 3)})
    return res


def main():
    OUT_AUDIO.mkdir(parents=True, exist_ok=True)
    GANCHO_FIM, APRESENTA = 3.6, 1.0
    linhas, t = [], 0.0
    for i, (lid, respiro) in enumerate(ROTEIRO):
        src = FALAS_DIR / f"{lid}.wav"
        d = dur(src)
        if lid == "n01":
            t = GANCHO_FIM + APRESENTA
        t += respiro
        quem, texto = TEXTOS[lid]
        linhas.append({"id": lid, "quem": quem, "texto": texto, "inicio": round(t, 3), "duracao": round(d, 3),
                       "arquivo": f"series/ano-zero/teste-motion/audio/{lid}.wav",
                       "palavras": tempos_palavras(texto, trechos_de_fala(src))})
        subprocess.run(["cp", str(src), str(OUT_AUDIO / f"{lid}.wav")], check=True)
        t += d
    por_id = {l["id"]: l for l in linhas}
    libras = [{"apos": a, "inicio": round(por_id[a]["inicio"] + por_id[a]["duracao"] + gap, 3), "duracao": dd,
               "quem": q, "texto": tx} for a, gap, dd, q, tx in LIBRAS]

    def palavra(lid, alvo):
        l = por_id[lid]
        for p in l["palavras"]:
            if p["w"].lower().startswith(alvo):
                return round(l["inicio"] + p["t0"], 3)
        raise KeyError(alvo)

    eventos = {
        "ganchoFim": GANCHO_FIM,
        "apresentaFim": GANCHO_FIM + APRESENTA,
        "tremorInicio": palavra("n02", "tremia"),
        "dedos": palavra("n02", "dedos"),
        "somCorta": palavra("n03", "cortou"),
        "parouRespirar": palavra("n03", "parou"),
        "batidaVolta": palavra("n04", "voltou"),
        "levanta": palavra("n04", "levantou"),
        "viraCabeca": por_id["r02"]["inicio"] + por_id["r02"]["duracao"] + 0.1,
        "ataque": palavra("b03", "sai"),
        "fuga": por_id["n06"]["inicio"],
    }
    fim_falas = linhas[-1]["inicio"] + linhas[-1]["duracao"]
    total = round(fim_falas + 0.6 + 3.0, 2)
    eventos["cta"] = round(fim_falas + 0.6, 3)

    # batidas (120 bpm) nos trechos com música: gancho, festa, e depois que a batida volta
    bpm = 120
    passo = 60 / bpm
    trechos_musica = [(0.0, GANCHO_FIM - 0.15), (GANCHO_FIM + APRESENTA, eventos["somCorta"]),
                      (eventos["batidaVolta"], eventos["cta"])]
    batidas = []
    for a, b in trechos_musica:
        k = 0
        while True:
            tb = round(round((a + k * passo) * FPS) / FPS, 4)  # grade em quadros, sem acumular arredondamento
            if tb >= b:
                break
            batidas.append(tb)
            k += 1

    # trilha: bumbo grave + chimbal + multidão, tudo abafado (festa ao longe)
    n = int(total * SR)
    trilha = np.zeros(n, dtype=np.float32)
    tt = np.arange(int(0.42 * SR)) / SR
    freq = 46 + 80 * np.exp(-tt * 28)
    bumbo = np.sin(2 * np.pi * np.cumsum(freq) / SR) * np.exp(-tt * 9)
    rng = np.random.default_rng(7)
    hat = rng.standard_normal(int(0.05 * SR)) * np.exp(-np.arange(int(0.05 * SR)) / SR * 90) * 0.12
    for i, tb in enumerate(batidas):
        s = int(tb * SR)
        e = min(n, s + len(bumbo))
        trilha[s:e] += 0.9 * bumbo[: e - s]
        h = int((tb + passo / 2) * SR)
        if h + len(hat) < n:
            trilha[h:h + len(hat)] += hat
    raw = RAIZ / "out/trilha-bruta.wav"
    raw.parent.mkdir(exist_ok=True)
    with wave.open(str(raw), "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(trilha, -1, 1) * 32767).astype(np.int16).tobytes())
    # multidão/mar: ruído marrom filtrado; abaixa no silêncio depois do corte do som
    corte, volta = eventos["somCorta"], eventos["batidaVolta"]
    subprocess.run([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(raw),
        "-f", "lavfi", "-t", str(total), "-i", "anoisesrc=color=brown:amplitude=0.5:seed=3:sample_rate=48000",
        "-filter_complex",
        "[0:a]lowpass=f=900,volume=1.0[b];"
        f"[1:a]lowpass=f=700,highpass=f=80,volume='if(between(t,{corte},{volta}),0.35,0.75)':eval=frame[c];"
        f"[b][c]amix=inputs=2:normalize=0,afade=t=out:st={total - 1.2}:d=1.2,alimiter=limit=0.8[o]",
        "-map", "[o]", "-ar", "48000", "-ac", "2", str(OUT_AUDIO / "trilha.wav")], check=True)

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps({"fps": FPS, "duracao": total, "bpm": bpm, "batidas": batidas, "eventos": eventos,
                                    "linhas": linhas, "libras": libras,
                                    "trilha": "series/ano-zero/teste-motion/audio/trilha.wav"}, ensure_ascii=False, indent=1))
    print(f"duração {total}s · {len(linhas)} falas · {len(batidas)} batidas")
    print(json.dumps(eventos, indent=1))


if __name__ == "__main__":
    main()
