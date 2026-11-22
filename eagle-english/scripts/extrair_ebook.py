#!/usr/bin/env python3
"""Extrai os 350 mapas do Eagle 350 (PDF) para JSON: [{mapa, pag, situacao, titulo, sub, frases:[{ramo,en,pt,pron}]}]."""
import json, re, sys
import pymupdf

def main(pdf, saida):
    d = pymupdf.open(pdf); mapas = []
    for i, p in enumerate(d):
        t = [l.strip() for l in p.get_text().split("\n") if l.strip()]
        m = next((l for l in t if re.search(r"· mapa \d+", l)), None)
        if not m:
            continue
        situacao, num = re.match(r"(.+?) · mapa (\d+)", m).groups()
        titulo, sub = t[0], t[1]
        corpo0 = t[2:t.index("@eagle.english.br")]
        corpo, j = [], 0
        while j < len(corpo0):          # pronúncia quebrada em várias linhas: junta até fechar a barra
            l = corpo0[j]
            if l.startswith("/") and not (l.endswith("/") and len(l) > 1):
                while j + 1 < len(corpo0) and not l.endswith("/"):
                    j += 1; l += " " + corpo0[j]
            corpo.append(l); j += 1
        frases, ramo, buf = [], None, []
        k = 0
        while k < len(corpo):
            l = corpo[k]
            if l.startswith("/") and l.endswith("/") and buf:
                # buf = [ramo?, en..., pt...]: pt é a última linha que não é inglês; heurística: en termina com ? . !
                en_lin, pt_lin, fase = [], [], "en"
                for x in buf:
                    if fase == "en":
                        en_lin.append(x)
                        if re.search(r"[.?!]$", x): fase = "pt"
                    else:
                        pt_lin.append(x)
                frases.append({"ramo": ramo, "en": " ".join(en_lin), "pt": " ".join(pt_lin), "pron": l.strip("/")})
                buf = []
            elif l.isupper() and not buf and len(l) < 30 and not re.search(r"[.?!]$", l):
                ramo = l
            else:
                buf.append(l)
            k += 1
        mapas.append({"mapa": int(num), "pag": i + 1, "situacao": situacao, "titulo": titulo, "sub": sub, "frases": frases})
    json.dump(mapas, open(saida, "w"), ensure_ascii=False, indent=1)
    ruins = [m["mapa"] for m in mapas if len(m["frases"]) != 6]
    print(len(mapas), "mapas;", sum(len(m["frases"]) for m in mapas), "frases; mapas com != 6:", ruins[:20])

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
