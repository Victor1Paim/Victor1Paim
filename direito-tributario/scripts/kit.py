#!/usr/bin/env python3
"""Kit de vídeo: gravação da apresentadora + elementos flutuantes + cartões em motion, tudo pelo roteiro.

Uso (na pasta direito-tributario/):
    python scripts/kit.py novo    <nome>   cria videos/<nome>/roteiro.txt (modelo com marcações)
    python scripts/kit.py ler     <nome>   gera videos/<nome>/texto-para-gravar.txt (sem marcações)
    python scripts/kit.py preparar <nome>  converte a gravação, transcreve (Whisper, grátis) e monta os dados
    python scripts/kit.py render  <nome>   gera videos/<nome>/final.mp4
    python scripts/kit.py tudo    <nome>   preparar + render

Coloque a gravação em videos/<nome>/gravacao.mp4 (ou .mov/.m4v/.webm). Vídeo vertical, de preferência.
Marcações do roteiro: veja LEIA-ME.md ("Como marcar o roteiro").
"""
import argparse, difflib, json, re, shutil, subprocess, sys, unicodedata
from pathlib import Path

for _s in (sys.stdout, sys.stderr):  # console do Windows não é UTF-8
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PROJ = Path(__file__).resolve().parents[1]
VIDEOS = PROJ / "videos"
PUBLIC = PROJ / "video" / "public" / "videos"
FPS = 30

CORES = {"amarelo": "mostarda", "mostarda": "mostarda", "verde": "salvia", "salvia": "salvia", "azul": "tealClaro",
         "teal": "teal", "laranja": "laranja", "vermelho": "vermelho", "jeans": "jeans", "branco": "papel"}
LUGARES = ["direita-alto", "esquerda", "direita", "esquerda-alto", "topo", "esquerda-baixo", "direita-baixo"]
TIPOS_FLUTUANTES = {"icone", "etiqueta", "numero", "carimbo", "pergunta", "moedas", "zoom", "seta"}
TIPOS_CARTAO = {"item", "esquerda", "direita", "destaque"}
MODELOS = {"lista", "comparacao", "numero", "passos", "definicao", "mito"}
DUR = {"icone": 2.6, "etiqueta": 2.6, "numero": 2.4, "carimbo": 2.2, "pergunta": 1.8, "moedas": 1.6, "zoom": 1.6, "seta": 2.2}

MODELO_ROTEIRO = """# Roteiro: escreva a fala normalmente. Linhas com # mudam o modo; [colchetes] criam elementos.
# Na gravação, leia o arquivo texto-para-gravar.txt (python scripts/kit.py ler {nome}).

# ela
Você sabia que paga [icone cafe] imposto até no cafezinho? [pergunta] Pois é.

# dividida lista | Onde o imposto aparece
Ele vem [item embutido no preço] embutido no preço, e a nota mostra o [item valor aproximado] valor aproximado.

# motion numero | Exemplo fictício
Num café de dez reais, [destaque parte vai pra tributos] uma parte vai pra tributos.

# ela
Salva esse vídeo [etiqueta salva! | vermelho] e manda pra alguém.
"""


# ---------------------------------------------------------------- utilidades
def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def norm(t):
    t = re.sub(r"[^\w%]", "", sem_acento(t.lower()))
    return {"pra": "para", "pro": "para", "ta": "esta", "to": "estou", "ce": "voce", "vc": "voce"}.get(t, t)


def rodar(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"erro ao rodar {cmd[0]}:\n{r.stderr[-1500:]}")
    return r.stdout


def achar_gravacao(pasta):
    for ext in ("mp4", "mov", "m4v", "webm", "mkv"):
        for nome in ("gravacao", "gravação"):
            p = pasta / f"{nome}.{ext}"
            if p.exists():
                return p
    vids = [p for p in pasta.iterdir() if p.suffix.lower() in (".mp4", ".mov", ".m4v", ".webm", ".mkv") and p.stem != "final"]
    if len(vids) == 1:
        return vids[0]
    sys.exit(f"não achei a gravação em {pasta} (coloque como gravacao.mp4)")


# ---------------------------------------------------------------- roteiro
def ler_roteiro(arq):
    """Devolve (palavras, marcas, modos). palavras = lista de str; marcas/modos apontam para o índice da palavra."""
    palavras, marcas, modos = [], [], []
    for linha in arq.read_text(encoding="utf-8").splitlines():
        s = linha.strip()
        if not s:
            continue
        if s.startswith("#"):
            d = s.lstrip("#").strip()
            cab = d.split("|")
            p0 = cab[0].split()
            if p0 and p0[0].lower() in ("ela", "dividida", "motion"):
                modo = {"modo": p0[0].lower(), "modelo": None if p0[0].lower() == "ela" else (p0[1].lower() if len(p0) > 1 else "lista"),
                        "titulo": cab[1].strip() if len(cab) > 1 else "", "icone": None}
                for extra in cab[2:]:
                    if extra.strip().startswith("icone="):
                        modo["icone"] = extra.split("=", 1)[1].strip()
                if modo["modo"] != "ela" and modo["modelo"] not in MODELOS:
                    sys.exit(f"modelo '{modo['modelo']}' não existe. Use: {', '.join(sorted(MODELOS))}")
                modos.append((len(palavras), modo))
            continue  # demais linhas com # são comentário
        for parte in re.split(r"(\[[^\]]*\])", s):
            if parte.startswith("["):
                marcas.append((len(palavras), parte[1:-1].strip()))
            else:
                palavras.extend(parte.split())
    return palavras, marcas, modos


def texto_limpo(arq):
    linhas = []
    for linha in arq.read_text(encoding="utf-8").splitlines():
        if linha.strip().startswith("#"):
            continue
        t = re.sub(r"\s+", " ", re.sub(r"\[[^\]]*\]", "", linha)).strip()
        if t:
            linhas.append(t)
    return "\n\n".join(linhas) + "\n"


def interpretar_marca(txt):
    partes = [p.strip() for p in txt.split("|")]
    cab = partes[0].split(None, 1)
    tipo = sem_acento(cab[0].lower()) if cab else ""
    resto = cab[1] if len(cab) > 1 else ""
    el = {"tipo": tipo}
    if tipo == "icone":
        el["icone"] = sem_acento(resto.lower()).replace(" ", "")
    elif resto:
        el["texto"] = resto
    for op in partes[1:]:
        o = sem_acento(op.lower())
        if o in CORES:
            el["cor"] = CORES[o]
        elif o in LUGARES:
            el["lugar"] = o
        elif re.fullmatch(r"\d+([.,]\d+)?s", o):
            el["dur"] = float(o[:-1].replace(",", "."))
        elif o in ("cima", "baixo"):
            el["direcao"] = o
        elif o.startswith("icone="):
            el["icone"] = o.split("=", 1)[1]
        elif op:
            print(f"  aviso: opção '{op}' em [{txt}] ignorada")
    if tipo not in TIPOS_FLUTUANTES | TIPOS_CARTAO:
        sys.exit(f"marcação desconhecida: [{txt}]. Tipos: {', '.join(sorted(TIPOS_FLUTUANTES | TIPOS_CARTAO))}")
    return el


# ---------------------------------------------------------------- alinhamento
def alinhar(roteiro, ws):
    """Tempo (ini, fim) de cada palavra do roteiro a partir das palavras do Whisper."""
    a = [norm(w) for w in roteiro]
    b = [norm(w["t"]) for w in ws]
    tempos = [None] * len(roteiro)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
            for k in range(i1, i2):
                tempos[k] = (ws[j1 + k - i1]["ini"], ws[j1 + k - i1]["fim"])
        elif tag == "replace":
            ini, fim = ws[j1]["ini"], ws[j2 - 1]["fim"]
            for k in range(i1, i2):
                tempos[k] = (ini + (fim - ini) * (k - i1) / (i2 - i1), ini + (fim - ini) * (k - i1 + 1) / (i2 - i1))
    for k in range(len(tempos)):
        if tempos[k] is None:
            prev = tempos[k - 1][1] if k else (ws[0]["ini"] if ws else 0)
            tempos[k] = (prev, prev + 0.2)
    return tempos, sm.ratio()


# ---------------------------------------------------------------- dicionário automático
def elementos_automaticos(palavras):
    dic = json.loads((PROJ / "dicionario-elementos.json").read_text(encoding="utf-8"))["regras"]
    els, usados = [], set()
    ns = [norm(p["t"]) for p in palavras]
    for i, n in enumerate(ns):
        for r in dic:
            gat = [norm(g) for g in r["gatilhos"]]
            for g in gat:
                gs = g.split() if " " in g else [g]
                alvo = ns[i:i + len(gs)]
                if len(alvo) == len(gs) and all(x.startswith(y) for x, y in zip(alvo, gs)):
                    chave = json.dumps(r["elemento"], sort_keys=True)
                    if chave in usados:
                        break
                    usados.add(chave)
                    els.append({**r["elemento"], "_i": i})
                    break
    k = next((i for i, p in enumerate(palavras[:16]) if "?" in p["t"]), None)
    if k is not None:  # pergunta no gancho
        els.append({"tipo": "pergunta", "_i": k})
    return els


# ---------------------------------------------------------------- comandos
def cmd_novo(nome):
    pasta = VIDEOS / nome
    pasta.mkdir(parents=True, exist_ok=True)
    arq = pasta / "roteiro.txt"
    if arq.exists():
        sys.exit(f"{arq} já existe")
    arq.write_text(MODELO_ROTEIRO.format(nome=nome), encoding="utf-8")
    print(f"criado {arq.relative_to(PROJ)} — escreva o roteiro, depois: python scripts/kit.py ler {nome}")


def cmd_ler(nome):
    pasta = VIDEOS / nome
    out = pasta / "texto-para-gravar.txt"
    out.write_text(texto_limpo(pasta / "roteiro.txt"), encoding="utf-8")
    print(out.read_text(encoding="utf-8"))
    print(f"(salvo em {out.relative_to(PROJ)})")


def converter(grav, destino):
    """H.264 1080×1920 30 fps + áudio normalizado (o navegador do render não lê HEVC do iPhone)."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    print("convertendo a gravação (1080×1920, 30 fps)...")
    rodar(["ffmpeg", "-v", "error", "-y", "-i", str(grav),
           "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(destino)])


def transcrever(video, modelo):
    import whisper
    print(f"transcrevendo com o Whisper ({modelo}) — na primeira vez ele baixa o modelo...")
    m = whisper.load_model(modelo)
    r = m.transcribe(str(video), language="pt", word_timestamps=True, fp16=False)
    return [{"t": w["word"].strip(), "ini": round(w["start"], 3), "fim": round(w["end"], 3)}
            for s in r["segments"] for w in s["words"] if w["word"].strip()]


PAUSA_MAX = 0.4    # pausa entre palavras acima disso é cortada (s)
FOLGA_ANTES = 0.08  # mantém antes da 1ª palavra de cada trecho (s)
FOLGA_DEPOIS = 0.16 # mantém depois da última palavra (o Whisper costuma marcar o fim cedo) (s)


def duracao(arq):
    return float(rodar(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(arq)]).strip())


def segmentos_de_fala(ws, dur, pausa_max=PAUSA_MAX):
    """Trechos (ini, fim) a manter: fala + folgas; pausas maiores que pausa_max saem."""
    segs = []
    a = max(0.0, ws[0]["ini"] - FOLGA_ANTES)
    for w, prox in zip(ws, ws[1:] + [None]):
        if prox is None:
            segs.append((a, min(dur, w["fim"] + FOLGA_DEPOIS + 0.25)))
        elif prox["ini"] - w["fim"] > pausa_max:
            fim = w["fim"] + FOLGA_DEPOIS
            ini = prox["ini"] - FOLGA_ANTES
            if ini - fim > 0.05:
                segs.append((a, fim))
                a = ini
    return [(round(x, 3), round(y, 3)) for x, y in segs if y - x > 0.05]


def cortar(original, destino, segs):
    """Recorta cada trecho num arquivo (com microfade no áudio, sem estalo) e junta tudo.
    Um trecho por vez: pouca memória, funciona em qualquer computador."""
    if len(segs) == 1 and segs[0][0] < 0.01:
        shutil.copy(original, destino)
        return
    print(f"cortando pausas ({len(segs)} trechos)...")
    tmp = destino.parent / "_trechos"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir()
    lista = []
    for i, (a, b) in enumerate(segs):
        d = b - a
        arq = tmp / f"t{i:04d}.mp4"
        rodar(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-i", str(original), "-t", f"{d:.3f}",
               "-af", f"afade=t=in:d=0.012,afade=t=out:st={max(0, d - 0.012):.3f}:d=0.012",
               "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-r", "30", "-pix_fmt", "yuv420p",
               "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(arq)])
        lista.append(f"file '{arq.name}'")
    (tmp / "lista.txt").write_text("\n".join(lista) + "\n", encoding="utf-8")
    rodar(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(tmp / "lista.txt"),
           "-c", "copy", "-movflags", "+faststart", str(destino)])
    shutil.rmtree(tmp, ignore_errors=True)


def remapear(ws, segs):
    """Leva os tempos das palavras para a linha do tempo já cortada."""
    out, base = [], []
    acc = 0.0
    for a, b in segs:
        base.append((a, b, acc))
        acc += b - a

    def novo(t):
        for a, b, off in base:
            if t <= b:
                return off + max(0.0, t - a)
        a, b, off = base[-1]
        return off + (b - a)

    for w in ws:
        out.append({**w, "ini": round(novo(w["ini"]), 3), "fim": round(novo(w["fim"]), 3)})
    return out


def cmd_preparar(nome, modelo="small", refazer=False):
    pasta = VIDEOS / nome
    if not pasta.exists():
        sys.exit(f"pasta {pasta} não existe (python scripts/kit.py novo {nome})")
    grav = achar_gravacao(pasta)
    pub = PUBLIC / nome
    cfg_arq = pasta / "ajustes.json"
    cfg = json.loads(cfg_arq.read_text(encoding="utf-8")) if cfg_arq.exists() else {}
    original = pub / "original.mp4"  # gravação convertida, sem cortes
    if refazer or not original.exists() or original.stat().st_mtime < grav.stat().st_mtime:
        converter(grav, original)

    cache = pasta / "transcricao.json"
    if refazer or not cache.exists() or cache.stat().st_mtime < original.stat().st_mtime:
        ws = transcrever(original, modelo)
        cache.write_text(json.dumps(ws, ensure_ascii=False, indent=0), encoding="utf-8")
    ws = json.loads(cache.read_text(encoding="utf-8"))
    if not ws:
        sys.exit("o Whisper não ouviu fala nenhuma na gravação")

    # corte automático das pausas (respiração, hesitação, silêncio no começo/fim)
    dur_orig = duracao(original)
    video = pub / "gravacao.mp4"
    if cfg.get("cortarPausas", True):
        segs = segmentos_de_fala(ws, dur_orig, cfg.get("pausaMaxima", PAUSA_MAX))
    else:
        segs = [(0.0, dur_orig)]
    chave = json.dumps([[round(a, 3), round(b, 3)] for a, b in segs])
    marca = pub / "cortes.json"
    if refazer or not video.exists() or not marca.exists() or marca.read_text() != chave or video.stat().st_mtime < original.stat().st_mtime:
        cortar(original, video, segs)
        marca.write_text(chave)
    ws = remapear(ws, segs)
    cortes = []
    acc = 0.0
    for a, b in segs[:-1]:
        acc += b - a
        cortes.append(round(acc, 3))
    if len(segs) > 1:
        print(f"pausas cortadas: {len(segs) - 1} cortes, {dur_orig - sum(b - a for a, b in segs):.1f}s a menos "
              f"({dur_orig:.1f}s -> {sum(b - a for a, b in segs):.1f}s)")
    dur = duracao(video)

    rot = pasta / "roteiro.txt"
    trechos, elementos, itens_cartao = [], [], []
    if rot.exists():
        rpal, marcas, modos = ler_roteiro(rot)
        tempos, ratio = alinhar(rpal, ws)
        print(f"roteiro x gravação: {ratio:.0%} das palavras batem")
        if ratio < 0.6:
            print("  aviso: a fala ficou bem diferente do roteiro — confira os tempos no preview")
        palavras = [{"t": w, "ini": round(t[0], 3), "fim": round(t[1], 3)} for w, t in zip(rpal, tempos)] if ratio >= 0.75 else ws
        t_de = lambda i: tempos[min(i, len(tempos) - 1)][0]
        for i, m in modos:
            trechos.append({**m, "ini": round(max(0, t_de(i) - 0.25), 3)})
        for i, txt in marcas:
            el = interpretar_marca(txt)
            el["ini"] = round(max(0, t_de(i) - 0.12), 3)
            (itens_cartao if el["tipo"] in TIPOS_CARTAO else elementos).append(el)
    else:
        print("sem roteiro.txt: usando o dicionário automático (dicionario-elementos.json)")
        palavras = ws
        for el in elementos_automaticos(ws):
            el["ini"] = round(max(0, ws[el.pop("_i")]["ini"] - 0.12), 3)
            elementos.append(el)
    if not trechos or trechos[0]["ini"] > 0.01:
        trechos.insert(0, {"modo": "ela", "modelo": None, "titulo": "", "icone": None, "ini": 0})
    trechos.sort(key=lambda t: t["ini"])
    for k, t in enumerate(trechos):
        t["fim"] = trechos[k + 1]["ini"] if k + 1 < len(trechos) else dur
        t["itens"] = [i for i in itens_cartao if t["ini"] - 0.3 <= i["ini"] < t["fim"]]
        for i in t["itens"]:
            i["ini"] = max(i["ini"], t["ini"])
        if t["modo"] == "ela" and t["itens"]:
            print(f"  aviso: [item]/[destaque] fora de um trecho dividida/motion (em {t['ini']:.1f}s) — ignorado")

    # elementos: duração, lugar automático sem sobreposição, só onde a apresentadora aparece
    elementos.sort(key=lambda e: e["ini"])
    ocupado = {l: -1.0 for l in LUGARES}
    finais, k = [], 0
    for e in elementos:
        tr = next(t for t in trechos if t["ini"] <= e["ini"] + 0.01 < t["fim"] + 0.01)
        if tr["modo"] == "motion" and e["tipo"] != "zoom":
            print(f"  aviso: [{e['tipo']}] em {e['ini']:.1f}s cai num trecho motion (tela cheia de informação) — ignorado")
            continue
        e.setdefault("dur", DUR.get(e["tipo"], 2.4))
        e["dur"] = min(e["dur"], tr["fim"] - e["ini"])
        if e["tipo"] not in ("zoom", "moedas") and "lugar" not in e:
            livres = [l for l in LUGARES[k:] + LUGARES[:k] if ocupado[l] <= e["ini"]]
            if tr["modo"] == "dividida":
                livres = [l for l in livres if l in ("esquerda-alto", "direita-alto", "topo")] or ["direita-alto"]
            e["lugar"] = livres[0] if livres else LUGARES[k % len(LUGARES)]
            k = (LUGARES.index(e["lugar"]) + 1) % len(LUGARES)
        if "lugar" in e:
            ocupado[e["lugar"]] = e["ini"] + e["dur"]
        finais.append(e)

    dados = {"nome": nome, "duracao": round(dur, 3), "video": f"videos/{nome}/gravacao.mp4",
             "palavras": palavras, "trechos": trechos, "elementos": finais, "legenda": True}
    dados["cortes"] = cortes
    dados.update({k: v for k, v in cfg.items() if k not in ("cortarPausas", "pausaMaxima")})
    (pub / "dados.json").write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
    (PUBLIC / "ultimo.json").write_text(json.dumps({"nome": nome}), encoding="utf-8")
    print(f"ok: {len(trechos)} trechos, {len(finais)} elementos flutuantes, {dur:.1f}s")
    for t in trechos:
        print(f"   {t['ini']:6.1f}s  {t['modo']:<9} {t.get('modelo') or '':<11} {t.get('titulo') or ''}")
    print(f"preview: cd video && npm run dev   |   render: python scripts/kit.py render {nome}")


def cmd_render(nome):
    if not (PUBLIC / nome / "dados.json").exists():
        sys.exit(f"rode antes: python scripts/kit.py preparar {nome}")
    saida = VIDEOS / nome / "final.mp4"
    npx = shutil.which("npx") or shutil.which("npx.cmd")
    if not npx:
        sys.exit("não achei o npx: instale o Node.js (veja LEIA-ME.md)")
    print("renderizando (pode levar alguns minutos)...")
    props = PUBLIC / nome / "props.json"  # arquivo, não JSON na linha de comando (o cmd do Windows estraga aspas)
    props.write_text(json.dumps({"nome": nome}), encoding="utf-8")
    r = subprocess.run([npx, "remotion", "render", "src/index.ts", "kit", str(saida),
                        f"--props={props}", "--log=error"], cwd=PROJ / "video")
    if r.returncode != 0:
        sys.exit("o render falhou (veja a mensagem acima)")
    print(f"pronto: {saida.relative_to(PROJ)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("comando", choices=["novo", "ler", "preparar", "render", "tudo"])
    ap.add_argument("nome")
    ap.add_argument("--modelo", default="small", help="modelo do Whisper: base (rápido), small (padrão), medium (melhor)")
    ap.add_argument("--refazer", action="store_true", help="refaz conversão e transcrição")
    a = ap.parse_args()
    if not re.fullmatch(r"[a-z0-9-]+", a.nome):
        sys.exit("use só letras minúsculas, números e hífen no nome (ex.: cafezinho-01)")
    if a.comando == "novo":
        cmd_novo(a.nome)
    elif a.comando == "ler":
        cmd_ler(a.nome)
    elif a.comando == "preparar":
        cmd_preparar(a.nome, a.modelo, a.refazer)
    elif a.comando == "render":
        cmd_render(a.nome)
    else:
        cmd_preparar(a.nome, a.modelo, a.refazer)
        cmd_render(a.nome)
