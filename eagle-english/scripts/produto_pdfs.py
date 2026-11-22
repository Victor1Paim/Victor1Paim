#!/usr/bin/env python3
"""PDFs novos do plano avançado, no mesmo formato dos ebooks (1080×1440, DejaVu Condensed, marinho/vermelho):
  06_Mapas_Mentais_Eagle.pdf · 07_Cola_de_Viagem.pdf · 08_Checklist_Antes_de_Embarcar.pdf
Frases tiradas do Eagle 350 (produtos/fonte/eagle350.json). Grátis (render local).
Uso: python3 scripts/produto_pdfs.py produtos [mapas|cola|checklist ...]
"""
import json, os, sys
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]


def carregar(base):
    m = json.load(open(base / "fonte" / "eagle350.json"))
    return {x["mapa"]: x for x in m}


def F(M, mapa, i):
    f = M[mapa]["frases"][i]
    return {"en": f["en"], "pt": f["pt"], "pron": f["pron"]}


def doc_mapas(M, base):
    mm = json.load(open(base / "fonte" / "mapas_mentais.json"))
    pags = [{"tipo": "capa", "pill": "RESUMOS DE 1 PÁGINA", "titulo": "MAPAS MENTAIS", "destaque": "MENTAIS",
             "desc": "15 mapas para revisar o inglês da viagem e a gramática que mais trava a fala",
             "forte": "Um tema por página. Olhe, leia em voz alta, revise antes de dormir."},
            None,
            {"tipo": "texto", "titulo": "COMO USAR", "destaque": "USAR", "rodape": "Como usar",
             "intro": "Cada mapa resume um tema em uma página: o centro é o assunto, cada ramo é uma regra com exemplos.",
             "caixas": [{"t": "OLHE O CENTRO", "p": "1 min: entenda o tema antes dos detalhes."},
                        {"t": "LEIA CADA RAMO EM VOZ ALTA", "p": "3 min: um ramo por vez, sempre com os exemplos."},
                        {"t": "TAMPE E LEMBRE", "p": "2 min: cubra um ramo e tente dizer os exemplos sem olhar."},
                        {"t": "USE NA VIAGEM", "p": "Mapas 11 a 15 são de viagem: salve no celular antes de embarcar."}]}]
    itens = []
    for k, m in enumerate(mm, 1):
        ramos = []
        for r in m["ramos"]:
            if "ref" in r:
                its = [f'{F(M, a, b)["en"]}<small>{F(M, a, b)["pt"]}</small><em>/{F(M, a, b)["pron"]}/</em>' for a, b in r["ref"]]
            else:
                its = [x.replace("(", "<small>").replace(")", "</small>") if "(" in x else x for x in r["i"]]
            ramos.append({"t": r["t"], "i": its})
        pid = f"m{k}"
        pags.append({"tipo": "mapa", "id": pid, "titulo": m["titulo"], "destaque": m["destaque"], "sub": f"Mapa {k} · {m['sub']}",
                     "centro": m["centro"], "ramos": ramos, "rodape": f"Mapa mental {k}"})
        itens.append({"id": pid, "n": f"{k:02d}", "t": m["titulo"], "pag": len(pags)})
    pags[1] = {"tipo": "sumario", "itens": itens}
    return pags


SITUACOES = [("Aeroporto", "NO AEROPORTO", "AEROPORTO"), ("Hotel", "NO HOTEL", "HOTEL"), ("Restaurante", "NO RESTAURANTE", "RESTAURANTE"),
             ("Transporte", "TRANSPORTE", "TRANSPORTE"), ("Compras", "COMPRAS", "COMPRAS"), ("Saúde", "SAÚDE", "SAÚDE"),
             ("Banco e dinheiro", "DINHEIRO", "DINHEIRO"), ("Cidade e passeios", "PASSEIOS", "PASSEIOS"),
             ("Emergências e problemas", "EMERGÊNCIA", "EMERGÊNCIA"), ("Entender e ser entendido", "NÃO ENTENDI", "ENTENDI")]


def doc_cola(M, base):
    pags = [{"tipo": "capa", "pill": "SALVE NO CELULAR", "titulo": "COLA DE VIAGEM", "destaque": "VIAGEM",
             "desc": "10 situações, 1 página cada: a primeira frase de cada mapa do Eagle 350, pronta para usar",
             "forte": "Tire print da página da situação e use na hora, mesmo sem internet."}, None]
    itens = []
    for k, (sit, tit, dest) in enumerate(SITUACOES, 1):
        mapas = [m for m in M.values() if m["situacao"] == sit]
        fr = [F(M, m["mapa"], 0) for m in mapas][:10]
        pid = f"c{k}"
        pags.append({"tipo": "frases", "classe": "cola", "id": pid, "titulo": tit, "destaque": dest,
                     "sub": f"Situação {k} · as 10 frases que resolvem", "grupos": [{"f": fr}], "rodape": f"Cola · {sit}"})
        itens.append({"id": pid, "n": f"{k:02d}", "t": sit, "pag": len(pags)})
    pags[1] = {"tipo": "sumario", "itens": itens}
    return pags


CHECK = [("AEROPORTO E IMIGRAÇÃO", [(2, 0), (3, 2), (3, 3), (3, 4), (1, 5)]),
         ("HOTEL", [(11, 0), (15, 0), (13, 0), (18, 0), (14, 0)]),
         ("RESTAURANTE", [(21, 0), (23, 0), (25, 0), (24, 0), (27, 0)]),
         ("TRANSPORTE E CIDADE", [(32, 0), (33, 0), (71, 0), (72, 0), (44, 0)]),
         ("SAÚDE E EMERGÊNCIA", [(51, 0), (53, 0), (171, 0), (176, 0), (56, 0)]),
         ("QUANDO NÃO ENTENDER", [(191, 0), (192, 0), (194, 0), (199, 0), (200, 0)])]


def doc_checklist(M, base):
    pags = [{"tipo": "capa", "pill": "SEMANA DA VIAGEM", "titulo": "ANTES DE EMBARCAR", "destaque": "EMBARCAR",
             "desc": "As 30 frases para treinar nos 7 dias antes da viagem",
             "forte": "Marque cada frase quando conseguir dizer sem olhar."},
            {"tipo": "texto", "titulo": "PLANO DOS 7 DIAS", "destaque": "7 DIAS", "rodape": "Plano dos 7 dias",
             "intro": "10 minutos por dia. Leia em voz alta, tampe o inglês, fale pela tradução e marque o quadrado.",
             "caixas": [{"n": "7", "t": "7 DIAS ANTES", "p": "Aeroporto e imigração (frases 1 a 5)."},
                        {"n": "6", "t": "6 DIAS ANTES", "p": "Hotel (frases 6 a 10)."},
                        {"n": "5", "t": "5 DIAS ANTES", "p": "Restaurante (frases 11 a 15)."},
                        {"n": "4", "t": "4 DIAS ANTES", "p": "Transporte e cidade (frases 16 a 20)."},
                        {"n": "3", "t": "3 DIAS ANTES", "p": "Saúde e emergência (frases 21 a 25)."},
                        {"n": "2", "t": "2 DIAS ANTES", "p": "Quando não entender (frases 26 a 30)."},
                        {"n": "1", "t": "VÉSPERA E NO AVIÃO", "p": "Revise as 30. As que ainda travam: repita 3 vezes cada."}]}]
    for i, (t, refs) in enumerate(CHECK):
        pags.append({"tipo": "frases", "ck": True, "titulo": t, "destaque": t.split()[-1],
                     "sub": f"{7 - i} dias antes · frases {i * 5 + 1} a {i * 5 + 5} · marque quando disser sem olhar",
                     "grupos": [{"f": [F(M, a, b) for a, b in refs]}], "rodape": f"Checklist · {t.title()}"})
    return pags


def doc_caderno(M, base):
    aulas = json.load(open(base / "fonte" / "aulas.json"))
    simp = lambda f: dict(f, pron=f["pron"].lower().replace("-", ""))
    pags = [{"tipo": "capa", "pill": "ACOMPANHA AS 10 AULAS", "titulo": "CADERNO DE EXERCÍCIOS", "destaque": "EXERCÍCIOS",
             "desc": "Uma página por aula: as frases para marcar e os exercícios para escrever",
             "forte": "Assista à aula, faça a página e confira no gabarito."}, None]
    itens, gab = [], []
    for a in aulas:
        fr = [simp(F(M, *f["ref"])) for f in a["frases"]][:6] or [simp(F(M, *r)) for r in a["exercicios"][:6]]
        ex = [F(M, *r) for r in a["exercicios"]][:4] if a["frases"] else [F(M, *r) for r in a["exercicios"][6:10]]
        pid = f"a{a['n']}"
        pags.append({"tipo": "aula", "id": pid, "titulo": f"AULA {a['n']} · {a['titulo'].upper()}", "destaque": a["titulo"].upper(),
                     "sub": a["tema"], "frases": fr, "ex": ex, "rodape": f"Aula {a['n']}"})
        itens.append({"id": pid, "n": f"{a['n']:02d}", "t": a["titulo"], "pag": len(pags)})
        gab.append({"t": f"Aula {a['n']}:", "r": [e["en"] for e in ex]})
    pags.append({"tipo": "gabarito", "id": "gab", "itens": gab})
    itens.append({"id": "gab", "n": "✓", "t": "Gabarito", "pag": len(pags)})
    pags[1] = {"tipo": "sumario", "itens": itens}
    return pags


DOCS = {"caderno": ("09_Caderno_de_Exercicios_das_Aulas.pdf", doc_caderno), "mapas": ("06_Mapas_Mentais_Eagle.pdf", doc_mapas), "cola": ("07_Cola_de_Viagem.pdf", doc_cola),
        "checklist": ("08_Checklist_Antes_de_Embarcar.pdf", doc_checklist)}


def main():
    base = Path(sys.argv[1]).resolve(); quais = sys.argv[2:] or list(DOCS)
    M = carregar(base)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        nav = pw.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH", "/opt/pw-browsers/chromium")) if os.path.exists(os.environ.get("CHROMIUM_PATH", "/opt/pw-browsers/chromium")) and os.path.isfile(os.environ.get("CHROMIUM_PATH", "/opt/pw-browsers/chromium")) else pw.chromium.launch()
        for q in quais:
            nome, fn = DOCS[q]
            pags = fn(M, base)
            if not any(p["tipo"] == "sumario" for p in pags):
                pass
            pg = nav.new_page(viewport={"width": 1080, "height": 1440})
            pg.add_init_script(f"window.DOC = {json.dumps({'paginas': pags}, ensure_ascii=False)};")
            pg.goto((PROJ / "templates" / "produto_pdf.html").as_uri()); pg.wait_for_function("window.pronto === true")
            pg.wait_for_timeout(300)
            saida = base / "avancado" / nome
            pg.pdf(path=str(saida), width="1080px", height="1440px", print_background=True)
            # prévia: miniaturas
            prev = base / "_previas"; prev.mkdir(exist_ok=True)
            for k in range(len(pags)):
                pg.set_viewport_size({"width": 1080, "height": 1440})
                pg.evaluate(f"window.scrollTo(0, {k * 1440})")
                pg.screenshot(path=str(prev / f"{q}_{k + 1:02d}.png"), clip={"x": 0, "y": k * 1440, "width": 1080, "height": 1440}, full_page=True)
            pg.close()
            print(f"ok {saida.name}: {len(pags)} páginas")
        nav.close()


if __name__ == "__main__":
    main()
