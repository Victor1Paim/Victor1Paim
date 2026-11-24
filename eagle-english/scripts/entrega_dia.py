#!/usr/bin/env python3
"""Pacote de postagem do dia, em ordem de horário (pedido do usuário, 24/11):

  python3 scripts/entrega_dia.py 2026-11-25
    -> entregas/2026-11-25/  arquivos numerados na ordem de postar (01_09h_story1.png, 05_12h_reels_aula.mp4 ...; hardlinks, fora do git)
    -> entregas/2026-11-25.md roteiro "POSTAR" (horário, onde, arquivos, legenda, comentário fixado, recomendações) — vai pro git
Lê posts/<data>_stories, posts/<data>_verbo-*, posts/<data>_carrossel-*, e o vídeo das 19h (lista/abc/caderno-falado/...).
Sem arquivo pronto = aparece como PENDENTE no roteiro.
"""
import os, re, shutil, sys
from pathlib import Path

PROJ = Path(__file__).resolve().parents[1]
DIAS = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]


def blocos(md):
    """{'Legenda': '...', 'Comentário fixado': '...', 'Prompt da capa (só o cenário)': '...'} a partir do legenda.md."""
    out, titulo = {}, None
    for parte in re.split(r"^## ", md, flags=re.M)[1:]:
        titulo, _, resto = parte.partition("\n")
        m = re.search(r"```\n(.*?)```", resto, re.S)
        if m:
            out[titulo.strip()] = m.group(1).strip()
    return out


def main(data):
    import datetime
    dia = datetime.date.fromisoformat(data); rot = f"{DIAS[dia.weekday()]} {dia.day:02d}/{dia.month:02d}"
    posts = sorted(p for p in (PROJ / "posts").glob(f"{data}_*") if p.is_dir())
    st = next((p for p in posts if p.name.endswith("_stories")), None)
    aula = next((p for p in posts if "_verbo-" in p.name), None)
    carr = next((p for p in posts if "_carrossel-" in p.name), None)
    noite = next((p for p in posts if p not in (st, aula, carr) and (p / "legenda.md").exists()), None)
    pasta = PROJ / "entregas" / data
    if pasta.exists():
        shutil.rmtree(pasta)
    pasta.mkdir(parents=True)
    n = [0]; md = [f"# POSTAR · {rot}\n", "Arquivos na pasta `entregas/" + data + "/`, numerados na ordem. Avisos chegam 10 min antes de cada horário.\n"]

    def pegar(src, nome):
        if not src or not Path(src).exists():
            return None
        dst = pasta / nome
        try:
            os.link(src, dst)
        except OSError:
            shutil.copy(src, dst)
        return dst.name

    def num():
        n[0] += 1; return f"{n[0]:02d}"

    instr = (st / "instrucoes.md").read_text() if st and (st / "instrucoes.md").exists() else ""
    linhas = {int(m.group(1)): m.group(0) for m in re.finditer(r"^(\d)\. story_\d.*?(?=^\d\. |\Z)", instr, re.S | re.M)}
    link = re.search(r"```\n(https://\S+)\n```", instr)

    def story(k, hora, rec):
        f = pegar(st / f"story_{k}.png", f"{num()}_{hora}_story{k}.png") if st else None
        txt = linhas.get(k, "").split("·", 1)[-1].strip() if linhas.get(k) else ""
        md.append(f"### {hora} · Story {k}\n- Arquivo: `{f or 'PENDENTE'}`\n- {txt.splitlines()[0].rstrip(":") if txt else 'sem adesivo'}\n- {rec}\n")
        if k == 4 and link:
            t = re.search(r'texto do adesivo: "([^"]+)"', instr)
            md.append(f"Link do adesivo (texto do adesivo: **{t.group(1) if t else 'Saiba mais'}**):\n```\n{link.group(1)}\n```\n")

    md.append("## 09h · Stories da manhã\n")
    story(1, "09h", "Música calma (lo-fi/acústica) com o adesivo da música escondido.")
    story(2, "09h", "Música opcional. É a frase do dia: nada de adesivo por cima do texto.")
    story(3, "09h", "Adesivo QUIZ no espaço vazio do meio; pergunta do adesivo: \"Qual é?\". Música baixa ou nenhuma.")

    if carr:
        b = blocos((carr / "legenda.md").read_text()); sl = sorted((carr / "slides").glob("*.png"))
        nomes = [pegar(s, f"{num()}_09h_carrossel_{s.stem}.png") for s in sl]
        md.append(f"## 09h · Carrossel no feed ({carr.name.split('_', 1)[1]})\n- Arquivos: `{nomes[0]}` … `{nomes[-1]}` ({len(nomes)} fotos, nessa ordem)")
        if not (carr / "slides" / "01.png").exists():
            md.append("- **Capa (01) é sua:** gere o cenário com o prompt abaixo e poste como 1ª foto (o texto da capa vai pelo nosso template; se preferir, me mande a imagem que eu monto).")
            if "Prompt da capa (só o cenário)" in b:
                md.append(f"```\n{b['Prompt da capa (só o cenário)']}\n```")
        md.append("- Instagram: post com várias fotos + música calma. TikTok: modo Foto, mesma legenda.\n- Fixe o comentário logo depois de postar.\n")
        md.append(f"Legenda:\n```\n{b.get('Legenda', 'PENDENTE')}\n```\nComentário fixado:\n```\n{b.get('Comentário fixado', 'PENDENTE')}\n```\n")

    def reels(p, hora, rotulo):
        if not p:
            md.append(f"## {hora} · Reels/TikTok ({rotulo})\n- PENDENTE\n"); return
        b = blocos((p / "legenda.md").read_text()); k = num()
        v = pegar(p / "video" / "final.mp4", f"{k}_{hora}_reels_{rotulo}.mp4")
        c = pegar(p / "video" / "capa.png", f"{k}_{hora}_reels_{rotulo}_CAPA.png")
        md.append(f"## {hora} · Reels + TikTok ({p.name.split('_', 1)[1]})\n- Vídeo: `{v or 'PENDENTE'}`\n- Capa: `{c or 'sem capa'}` → Reels: \"Editar capa\" → \"Adicionar da galeria\"; TikTok: \"Selecionar capa\" (ou o 1º quadro).")
        md.append("- Sem música extra (o vídeo já tem a voz e os efeitos). Deixe \"Compartilhar no feed\" ligado. Fixe o comentário logo depois de postar.\n")
        md.append(f"Legenda:\n```\n{b.get('Legenda', 'PENDENTE')}\n```\nComentário fixado:\n```\n{b.get('Comentário fixado', 'PENDENTE')}\n```\n")

    reels(aula, "12h", "aula")
    md.append("## 12h · Story do pedido\n"); story(4, "12h", "Adesivo LINK no espaço vazio, com o texto personalizado (veja abaixo). Música baixa ou nenhuma.")
    md.append("## 18h · Story da resposta\n"); story(5, "18h", "Música opcional. Depois veja quem respondeu o quiz e responda no direct quem errou.")
    reels(noite, "19h", "noite")
    (PROJ / "entregas" / f"{data}.md").write_text("\n".join(md))
    print(f"ok -> entregas/{data}/ ({n[0]} itens) + entregas/{data}.md")
    for f in sorted(pasta.iterdir()):
        print("  ", f.name, flush=True)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
