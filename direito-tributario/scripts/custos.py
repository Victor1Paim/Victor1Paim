#!/usr/bin/env python3
"""Registro e relatório de custo das APIs por post.

Registrar (dentro de outro script):
    from custos import registrar
    registrar(pasta_do_post, modelo, etapa, entrada_texto=..., saida_audio=..., ...)

Relatório (no fim de cada post):
    python3 scripts/custos.py relatorio PASTA_DO_POST

Cada chamada vira uma linha em PASTA_DO_POST/custos.jsonl com os tokens que a própria API devolveu
(usage/usageMetadata). Preços em scripts/precos-api.json.
"""
import json, sys, datetime
from pathlib import Path

PRECOS = Path(__file__).with_name("precos-api.json")


def _precos():
    return json.loads(PRECOS.read_text())


def custo_usd(modelo, **tokens):
    tabela = _precos()["modelos"].get(modelo)
    if not tabela:
        return None
    # preços por 1M de tokens; chaves "minuto_*" são preço por minuto (ex.: TTS da OpenAI)
    return sum(tabela.get(k, 0) * v / (1 if k.startswith("minuto") else 1_000_000) for k, v in tokens.items())


def registrar(pasta, modelo, etapa, **tokens):
    pasta = Path(pasta); pasta.mkdir(parents=True, exist_ok=True)
    usd = custo_usd(modelo, **tokens)
    linha = {"quando": datetime.datetime.now().isoformat(timespec="seconds"), "etapa": etapa,
             "modelo": modelo, "tokens": tokens, "usd": None if usd is None else round(usd, 6)}
    with open(pasta / "custos.jsonl", "a") as f:
        f.write(json.dumps(linha, ensure_ascii=False) + "\n")
    return usd


def relatorio(pasta):
    arq = Path(pasta) / "custos.jsonl"
    if not arq.exists():
        print("Nenhuma chamada de API registrada neste post (custo US$ 0,00)."); return
    p = _precos(); cambio = p["cambio_brl_por_usd"]
    linhas = [json.loads(l) for l in arq.read_text().splitlines() if l.strip()]
    for l in linhas:  # recalcula com a tabela atual (corrige registros antigos)
        u = custo_usd(l["modelo"], **l["tokens"])
        l["usd"] = None if u is None else u
    por = {}
    sem_preco = set()
    for l in linhas:
        k = (l["etapa"], l["modelo"])
        a = por.setdefault(k, {"chamadas": 0, "usd": 0.0})
        a["chamadas"] += 1
        if l["usd"] is None: sem_preco.add(l["modelo"])
        else: a["usd"] += l["usd"]
    total = sum(a["usd"] for a in por.values())
    print(f"| Etapa | Modelo | Chamadas | US$ | R$ |\n|---|---|---|---|---|")
    for (etapa, modelo), a in sorted(por.items()):
        print(f"| {etapa} | {modelo} | {a['chamadas']} | {a['usd']:.4f} | {a['usd']*cambio:.3f} |")
    print(f"| **Total** | | {len(linhas)} | **{total:.4f}** | **{total*cambio:.3f}** |")
    print(f"\nPreços da camada paga conferidos em {p['conferido_em']}; câmbio R$ {cambio:.2f}/US$."
          " Se a chave estiver na camada gratuita do Gemini, a voz sai de graça (dentro dos limites).")
    if sem_preco:
        print("Sem preço na tabela (adicionar em scripts/precos-api.json):", ", ".join(sorted(sem_preco)))


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "relatorio":
        relatorio(sys.argv[2])
    else:
        sys.exit(__doc__)
