#!/usr/bin/env python3
"""Reel animado de receita (fotos realistas + Tito + CTA novo). Uso: python3 build_reel_receita.py arroz-feijao|lanche"""
import json, re, shutil, sys
from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance

NOME = sys.argv[1]
SCR = Path("/tmp/claude-0/-home-user-Victor1Paim/bc508778-dc0e-5c3d-a4a6-a9dce8035bd2/scratchpad")
ROOT = Path("/home/user/Victor1Paim/saude-sem-sermao/producoes")
POST = ROOT / "reels-receitas" / NOME
V = POST / "video"
(V / "compositions").mkdir(parents=True, exist_ok=True)
(V / "assets").mkdir(exist_ok=True)
for f in ["hyperframes.json", "package.json", "meta.json"]:
    (V / f).write_text((SCR / "hfblank" / f).read_text().replace('"hfblank"', f'"saude-sem-sermao-reel-{NOME}"'))
shutil.copy(POST / "dialogo.mp3", V / "assets/voz.mp3")

# fotos: as do carrossel + as novas do reel -> 1280x1920 e versão desfocada
fontes_fotos = list((ROOT / "carrosseis" / NOME / "fotos").glob("*.png")) + list((POST / "fotos").glob("*.png"))
for p in fontes_fotos:
    dst = V / "assets" / f"{p.stem}.jpg"
    if dst.exists():
        continue
    im = Image.open(p).convert("RGB").resize((1280, 1920), Image.LANCZOS)
    im.save(dst, quality=90)
    ImageEnhance.Brightness(im.filter(ImageFilter.GaussianBlur(28))).enhance(0.62).save(V / "assets" / f"{p.stem}-desfoque.jpg", quality=85)

W, H = 1080, 1920
words = json.loads((POST / "conferencia/dialogo.palavras.json").read_text())
CENAS = []
src = (SCR / "build_sono.py").read_text()
exec(src[src.index("# ---------- paleta e base"):src.index("# ---------- 1. capa")])
src2 = (SCR / "build_alongar.py").read_text()
exec(src2[src2.index("BASE_CSS += "):src2.index("VERDE, CREME, BRANCO")])
src3 = (SCR / "build_reel_ovo.py").read_text()
exec(src3[src3.index('BASE_CSS += """\n  .foto{'):src3.index("# 1. capa")])
BASE_CSS += """
  .card2{position:absolute;left:80px;width:920px;background:#fff;border-radius:30px;box-shadow:0 14px 40px rgba(40,60,40,.12);
         display:flex;align-items:center;gap:26px;padding:30px 38px;font-weight:900;font-size:44px;line-height:1.2;}
  .card2 .e{font-size:76px;}
"""


def capa(ini, fim, foto, titulo, tag, pill, t_pill, cor_tag="#D45F2B"):
    d = add("capa", ini, fim)
    cena("capa", d, f"""
  #capa-tag{{position:absolute;left:80px;top:220px;padding:8px 24px;border-radius:999px;background:{cor_tag};color:#fff;font-weight:900;font-size:34px;letter-spacing:.06em;}}
  #capa-pill{{left:80px;top:640px;background:var(--verde);}}
""", f"""
  {foto_html("capa", foto, '<div class="sombra-top"></div>')}
  <div id="capa-tag">{tag}</div>
  <h1 class="tit-foto" style="top:290px">{titulo}</h1>
  <div class="chip" id="capa-pill">{pill}</div>
""", f"""
  {kb_js("capa", d, 1.0, 1.14, -30)}
  tl.fromTo("#capa-pill",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.2)"}},{t_pill:.2f});
""")


def seq_fotos(cid, ini, fim, fotos, chips, titulo=None, passo=None):
    """fotos: [(nome, t_abs)], troca com crossfade; chips: [(texto, t_abs, cor)] empilhados à esquerda no topo."""
    d = add(cid, ini, fim)
    wh, wj = wipe(cid, "#1c211c")
    camadas, js = [], []
    for k, (nome, tt) in enumerate(fotos):
        camadas.append(f'<div class="foto" id="{cid}-f{k}" style="opacity:{1 if k == 0 else 0}"><img id="{cid}-i{k}" src="assets/{nome}.jpg"></div>')
        a = 0 if k == 0 else max(tt - ini - 0.25, 0)
        if k > 0:
            js.append(f'tl.to("#{cid}-f{k}",{{opacity:1,duration:0.45,ease:"power2.inOut"}},{a:.2f});')
        js.append(f'tl.fromTo("#{cid}-i{k}",{{scale:1.03}},{{scale:1.13,duration:{max(d - a, 0.5):.2f},ease:"none"}},{a:.2f});')
    topo = 250 if not titulo else 420
    chips_html = "".join(f'<div class="chip" id="{cid}-c{i}" style="left:{80 if i % 2 == 0 else 160}px;top:{topo + 90*i}px;background:{c}">{txt}</div>'
                         for i, (txt, _, c) in enumerate(chips))
    js += [f'tl.fromTo("#{cid}-c{i}",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.3,ease:"back.out(1.8)"}},{max(tt - ini, 0.1):.2f});' for i, (_, tt, _) in enumerate(chips)]
    tit = f'<h1 class="tit-foto" id="{cid}-t" style="top:240px;font-size:88px">{titulo}</h1>' if titulo else ""
    if titulo:
        js.append(f'tl.fromTo("#{cid}-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.15);')
    cena(cid, d, "", f"""
  {''.join(camadas)}
  <div class="sombra-top"></div>
  {tit}
  {chips_html}
  {wh}
""", f"""
  {wj}
  {' '.join(js)}
""")


def grafico(cid, ini, fim, bg, html, js, css=""):
    d = add(cid, ini, fim)
    wh, wj = wipe(cid, "#1c211c")
    cena(cid, d, f".bg{{background:{bg};}}\n  .tag{{background:#5F6E52;color:#fff;}}\n{css}", f'<div class="bg"></div>\n{html}\n{wh}', f"{wj}\n{js}")


def cta(ini, fim, titulo, comenta, eco_foto, eco_tit, i_manda, i_aviao, i_curte, i_comenta, i_segue, total):
    d = add("cta", ini, fim)
    wh, wj = wipe("cta", "#1c211c")
    cta_ovo = src3[src3.index('cena("cta", d, """'):src3.index("GRUPOS = [")]
    loc = dict(globals()); loc.update(d=d, ini=ini, TOTAL=total, wh=wh, wj=wj)
    cta_ovo = (cta_ovo.replace('Manda pra quem tem <em>medo de ovo</em>', titulo)
               .replace('"🥕 cenoura!"', comenta)
               .replace('assets/capa.jpg', f'assets/{eco_foto}.jpg')
               .replace('Ovo aumenta o <em>colesterol?</em>', eco_tit)
               .replace("t(133)", f"t({i_manda})").replace("t(134)", f"t({i_manda+1})").replace("t(137)", f"t({i_aviao})")
               .replace("t(141)", f"t({i_curte})").replace("t(142)", f"t({i_comenta})").replace("t(148)", f"t({i_segue})"))
    exec(cta_ovo, loc)


def legendas(grupos, total):
    for txt_, i0, n in grupos:
        print(f"{txt_!r:50} <- {' '.join(w['palavra'] for w in words[i0:i0+n])!r}")
    leg_html, leg_js = [], []
    for k, (txt_, i0, n) in enumerate(grupos):
        a = max(words[i0]["inicio"] - 0.08, 0.15)
        b = words[i0 + n - 1]["fim"] + 0.18
        if k + 1 < len(grupos) and grupos[k + 1][1] == i0 + n:
            b = min(b, words[grupos[k + 1][1]]["inicio"] - 0.1)
        leg_html.append(f'<div class="leg" id="leg-{k}">{re.sub(r"[*](.+?)[*]", r"<b>\1</b>", txt_)}</div>')
        leg_js.append(f'tl.fromTo("#leg-{k}",{{opacity:0,y:16,visibility:"visible"}},{{opacity:1,y:0,duration:0.14,ease:"power2.out"}},{a:.2f});'
                      f'tl.to("#leg-{k}",{{opacity:0,duration:0.1,ease:"power2.in"}},{b-0.1:.2f});'
                      f'tl.set("#leg-{k}",{{opacity:0,visibility:"hidden"}},{b:.2f});')
    (V / "compositions/legendas.html").write_text(f"""<template>
<style>
  #root{{position:absolute;inset:0;font-family:'Nunito',sans-serif;pointer-events:none;}}
  .leg{{position:absolute;left:80px;top:1180px;max-width:640px;background:#fff;border-radius:24px;padding:18px 30px;
        font-weight:900;font-size:50px;line-height:1.15;color:#2B2B2B;box-shadow:0 12px 34px rgba(0,0,0,.25);
        opacity:0;visibility:hidden;}}
  .leg b{{color:#D45F2B;font-weight:900;}}
</style>
<div id="root" data-composition-id="legendas" data-width="{W}" data-height="{H}" data-layout-allow-caption-zone>
{chr(10).join(leg_html)}
</div>
<script>
  const tl = gsap.timeline({{ paused: true }});
  {chr(10).join('  ' + j for j in leg_js)}
  window.__timelines["legendas"] = tl;
</script>
</template>
""")
    hosts = [f'''      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html"
        data-start="{a}" data-duration="{round(b - a, 2)}" data-track-index="1" data-track-kind="graphics"
        data-width="{W}" data-height="{H}" style="z-index:1"></div>''' for cid, a, b in CENAS]
    (V / "index.html").write_text(f"""<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #1c211c; }}
      #main {{ position: relative; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="main" data-composition-id="main" data-start="0" data-duration="{total}" data-width="{W}" data-height="{H}">
{chr(10).join(hosts)}
      <div id="legendas" data-composition-id="legendas" data-composition-src="compositions/legendas.html"
        data-start="0" data-duration="{total}" data-track-index="2" data-track-kind="captions"
        data-width="{W}" data-height="{H}" style="z-index:5"></div>
      <audio id="voz" class="clip" src="assets/voz.mp3" data-start="0" data-track-index="3" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
    print("ok", [c[0] for c in CENAS])


VERDE_ = "#2F483A"; SAL = "#5F6E52"; TER = "#C2563A"; MOS = "#8A6A1F"; LAR = "#D45F2B"

if NOME == "arroz-feijao":
    TOTAL = 48.3
    capa(0, 4.1, "capa", "Arroz com feijão <em>engorda?</em>", "MITO OU VERDADE?", "a dupla pode até ajudar", t(6))
    tito_foto("t1", 4.1, 6.75, "Mas arroz não é carboidrato demais?", 4.22, 6.6, "ingredientes", destaque=(4,), olhos="duvida")
    ini = 6.75
    grafico("ciencia", 6.75, 14.05, "#fff", f"""
  <div class="tag" id="ciencia-tag">✓ CIÊNCIA</div>
  <h1 class="titulo" id="ciencia-t">Arroz com feijão: <em>menos</em> sobrepeso</h1>
  <div class="card2" id="ciencia-c0" style="top:470px"><span class="e">🍛</span>padrão tradicional<br>arroz com feijão</div>
  <div class="card2" id="ciencia-c1" style="top:680px"><span class="e">🍔</span>padrão com mais<br>gordura e açúcar</div>
  <div id="ciencia-menos" style="position:absolute;left:600px;top:540px;padding:12px 26px;border-radius:999px;background:var(--verde);color:#fff;font-weight:900;font-size:40px">menos sobrepeso ✓</div>
  <div class="fonte" id="ciencia-fonte" style="top:900px">Fonte: Sichieri, Obes Res, 2002 · Cunha et al., Br J Nutr, 2010 (observacionais)</div>""",
        f"""tl.fromTo("#ciencia-tag",{{opacity:0,y:-10}},{{opacity:1,y:0,duration:0.3}},0.3);
  tl.fromTo("#ciencia-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.3);
  tl.fromTo("#ciencia-c0",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:0.4,ease:"back.out(1.6)"}},{t(26)-ini:.2f});
  tl.fromTo("#ciencia-menos",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.4)"}},{t(31)-ini:.2f});
  tl.fromTo("#ciencia-c1",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:0.4,ease:"back.out(1.6)"}},{t(33)-ini:.2f});
  tl.fromTo("#ciencia-fonte",{{opacity:0}},{{opacity:1,duration:0.4}},{t(18)-ini:.2f});""")
    ini = 14.05
    grafico("dupla", 14.05, 18.75, "var(--pessego)", """
  <h1 class="titulo" id="dupla-t">A dupla se <em>completa</em></h1>
  <div id="dupla-a" style="position:absolute;left:150px;top:500px;width:360px;height:360px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;font-size:150px;box-shadow:0 14px 40px rgba(80,40,20,.12)">🍚</div>
  <div id="dupla-b" style="position:absolute;left:570px;top:500px;width:360px;height:360px;border-radius:50%;background:#7A4A2E;display:flex;align-items:center;justify-content:center;font-size:150px;box-shadow:0 14px 40px rgba(80,40,20,.12)">🫘</div>
  <div id="dupla-mais" style="position:absolute;left:500px;top:610px;font-weight:900;font-size:110px;color:var(--laranja)">+</div>
  <div id="dupla-prot" style="position:absolute;left:80px;top:900px;width:920px;text-align:center;font-weight:900;font-size:44px;color:var(--verde)">proteína completa</div>
  <div class="chip" id="dupla-fibra" style="left:330px;top:990px;background:#5F6E52">🌾 fibra = saciedade</div>""",
        f"""tl.fromTo("#dupla-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.3);
  tl.fromTo("#dupla-a",{{x:-260,opacity:0}},{{x:0,opacity:1,duration:0.5,ease:"power3.out"}},0.4);
  tl.fromTo("#dupla-b",{{x:260,opacity:0}},{{x:0,opacity:1,duration:0.5,ease:"power3.out"}},0.4);
  tl.fromTo("#dupla-mais",{{scale:0}},{{scale:1,duration:0.3,ease:"back.out(2.6)"}},{t(44)-ini:.2f});
  tl.fromTo("#dupla-prot",{{opacity:0}},{{opacity:1,duration:0.3}},{t(46)-ini:.2f});
  tl.fromTo("#dupla-fibra",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.2)"}},{t(51)-ini:.2f});""")
    tito_foto("t2", 18.75, 20.95, "Então como eu monto o prato?", 18.82, 20.6, "montagem", destaque=(3, 4, 5), bracos="acena", tam=64)
    seq_fotos("prato", 20.95, 28.8, [("montagem", 21.04), ("servindo", t(69)), ("capa", t(75))],
              [("½ salada e legumes", t(62), SAL), ("¼ arroz + feijão", t(69), MOS), ("¼ proteína", t(75), LAR),
               ("frango · ovo · carne · peixe", t(80), VERDE_)])
    tito_foto("t3", 28.8, 30.35, "E na correria?", 28.9, 29.9, "feijao-panela", destaque=(2,), olhos="duvida", tam=72)
    seq_fotos("congelar", 30.35, 35.0, [("feijao-panela", 30.42), ("congelado", t(94))],
              [("feijão no fim de semana", t(89), MOS), ("congela em porções", t(94), VERDE_), ("❄️ até 3 meses", t(99), SAL)])
    tito_foto("resumo", 35.0, 39.15, "Entendi! Arroz com feijão não é vilão. O segredo é o prato todo.", 35.06, 38.6, "capa",
              rot="💡 O QUE O TITO ENTENDEU", destaque=(1, 2, 3, 4, 5, 6, 9, 10, 11, 12), bracos="acena", tam=58)
    cta(39.15, TOTAL, "Manda pra quem acha que <em>arroz com feijão engorda</em>", '"🍗 frango!"', "capa",
        "Arroz com feijão <em>engorda?</em>", 119, 123, 128, 130, 139, TOTAL)
    legendas([
        ("Arroz com feijão *engorda?*", 0, 4), ("Na verdade, a dupla *pode até ajudar*.", 4, 7),
        ("Em estudos no Rio de Janeiro,", 17, 6), ("quem comia o *tradicional arroz com feijão*", 23, 7), ("tinha *menos sobrepeso*", 30, 3),
        ("do que quem comia *mais gordura e açúcar*.", 33, 8), ("A dupla *se completa em proteína*,", 41, 6), ("e o feijão traz *fibra*,", 47, 5),
        ("que *segura a fome*.", 52, 4), ("*Metade do prato*", 62, 3), ("com salada e legumes.", 65, 4), ("*Um quarto* com arroz e feijão.", 69, 6),
        ("E um quarto com *proteína*:", 75, 5), ("frango, ovo, carne ou peixe.", 80, 5), ("Faça feijão *no fim de semana*", 88, 6),
        ("e *congele em porções*.", 94, 4), ("Dura até *três meses* no freezer.", 98, 6),
        ("*Isso aí.*", 117, 2), ("Manda pra quem acha que", 119, 5), ("*arroz com feijão engorda*.", 124, 4), ("E *curte*,", 128, 2),
        ("*comenta* qual é a proteína do seu PF", 130, 8), ("e *segue pra mais!*", 138, 4)], TOTAL)

elif NOME == "lanche":
    TOTAL = 47.0
    capa(0, 3.75, "capa", "Lanche da tarde em <em>5 minutos</em>", "TROCA SEM SERMÃO", "sem biscoito recheado", t(6), cor_tag="#C2563A")
    tito_foto("t1", 3.75, 5.75, "Mas biscoito é tão prático...", 3.84, 5.4, "biscoito", destaque=(3, 4), olhos="duvida", tam=66)
    ini = 5.75
    d_ = add("guia", 5.75, 12.85); wh, wj = wipe("guia", "#1c211c")
    cena("guia", d_, """
  #guia-tag{position:absolute;left:80px;top:220px;padding:8px 24px;border-radius:999px;background:#fff;color:#5F6E52;font-weight:900;font-size:32px;letter-spacing:.06em;}
  #guia-selo{position:absolute;left:560px;top:640px;padding:10px 26px;border:7px solid #fff;border-radius:16px;color:#fff;font-weight:900;font-size:62px;letter-spacing:.08em;}
  .fonte{top:1100px;color:#fff;opacity:.85;}
""", f"""
  <div class="foto"><img id="guia-img" src="assets/biscoito.jpg"></div><div class="sombra-top" style="height:1300px"></div>
  <div id="guia-tag">✓ GUIA ALIMENTAR</div>
  <h1 class="tit-foto" style="top:290px;font-size:90px">Biscoito recheado é <em>ultraprocessado</em></h1>
  <div id="guia-selo">EVITAR</div>
  <div class="chip" id="guia-c0" style="left:80px;top:800px;background:#5F6E52">🍎 fruta</div>
  <div class="chip" id="guia-c1" style="left:330px;top:800px;background:#2F483A">🍳 comida feita em casa</div>
  <div class="fonte" id="guia-fonte">Fonte: Guia Alimentar para a População Brasileira, Ministério da Saúde, 2014</div>
  {wh}
""", f"""
  {wj}
  {kb_js("guia", d_, 1.0, 1.12)}
  tl.fromTo("#guia-selo",{{opacity:0,scale:2.4,rotation:-14}},{{opacity:1,scale:1,rotation:-8,duration:0.22,ease:"power4.in"}},{t(22)-ini:.2f});
  tl.fromTo("#root",{{x:0}},{{x:10,duration:0.04,yoyo:true,repeat:5,ease:"none"}},{t(22)-ini+0.22:.2f});
  tl.fromTo("#guia-c0",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.3,ease:"back.out(1.8)"}},{t(29)-ini:.2f});
  tl.fromTo("#guia-c1",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.3,ease:"back.out(1.8)"}},{t(30)-ini:.2f});
  tl.fromTo("#guia-fonte",{{opacity:0}},{{opacity:1,duration:0.4}},{t(15)-ini:.2f});
""")
    tito_foto("t2", 12.85, 14.65, "E o que eu como no lugar?", 12.9, 14.4, "capa", destaque=(5, 6), olhos="duvida", tam=66)
    seq_fotos("copo", 14.65, 21.95, [("banana", 14.72), ("camadas", t(46)), ("capa", t(55))],
              [("1 copo em camadas", t(43), LAR), ("aveia + banana", t(48), MOS), ("iogurte natural", t(53), SAL), ("morango + aveia", t(57), TER)])
    ini = 21.95
    grafico("quatro", 21.95, 24.75, "var(--creme)", """
  <h1 class="titulo" id="quatro-t"><em>4</em> ingredientes, <em>zero</em> fogão</h1>
  <div id="quatro-i" style="position:absolute;left:80px;top:520px;width:920px;display:flex;justify-content:space-between">
    <div class="q" id="quatro-q0">🥣</div><div class="q" id="quatro-q1">🍌</div><div class="q" id="quatro-q2">🍓</div><div class="q" id="quatro-q3">🌾</div></div>
  <div id="quatro-fogao" style="position:absolute;left:390px;top:800px;width:300px;height:300px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;font-size:160px">🔥</div>
  <svg id="quatro-x" style="position:absolute;left:390px;top:800px;width:300px;height:300px" viewBox="0 0 100 100"><path d="M18 18 L82 82 M82 18 L18 82" stroke="#D45F2B" stroke-width="12" stroke-linecap="round"/></svg>""",
        f"""tl.fromTo("#quatro-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.25);
  {' '.join(f'tl.fromTo("#quatro-q{i}",{{scale:0}},{{scale:1,duration:0.3,ease:"back.out(2.4)"}},{t(61)-ini+i*0.12:.2f});' for i in range(4))}
  tl.fromTo("#quatro-fogao",{{scale:0}},{{scale:1,duration:0.3,ease:"back.out(2)"}},{t(63)-ini-0.1:.2f});
  tl.fromTo("#quatro-x",{{scale:0,opacity:0}},{{scale:1,opacity:1,duration:0.2,ease:"power3.out"}},{t(64)-ini:.2f});""",
        css=".q{width:200px;height:200px;border-radius:40px;background:#fff;display:flex;align-items:center;justify-content:center;font-size:120px;box-shadow:0 14px 40px rgba(80,40,20,.12);}")
    seq_fotos("geladeira", 24.75, 27.55, [("geladeira", 24.78)], [("3 copos prontos", t(69), SAL), ("❄️ na geladeira", t(70), VERDE_)])
    tito_foto("t3", 27.55, 30.4, "Sem a fruta, né? Senão ela escurece.", 27.58, 30.2, "geladeira", destaque=(1, 2, 6), tam=64)
    seq_fotos("fruta", 30.4, 32.95, [("banana", 30.42)], [("🍓 fruta na hora", t(85), TER)])
    tito_foto("resumo", 32.95, 37.7, "Entendi! Trocar o biscoito pelo copo é fácil e leva cinco minutos.", 32.98, 37.3, "capa",
              rot="💡 O QUE O TITO ENTENDEU", destaque=(1, 3, 6, 7, 10, 11), bracos="acena", tam=58)
    cta(37.7, TOTAL, "Manda pra quem vive de <em>biscoito recheado</em>", '"🍓 morango!"', "capa",
        "Lanche da tarde em <em>5 minutos</em>", 105, 111, 112, 114, 120, TOTAL)
    legendas([
        ("Lanche da tarde em *5 minutos*,", 0, 6), ("*sem biscoito recheado*.", 6, 3), ("O Guia Alimentar do Ministério da Saúde", 14, 7),
        ("recomenda *evitar ultraprocessados*,", 21, 3), ("como biscoito recheado,", 24, 3), ("e preferir *fruta e comida feita em casa*.", 27, 8),
        ("Um *copo em camadas*.", 42, 4), ("No fundo, *aveia e banana*.", 46, 5), ("Por cima, *iogurte natural*.", 51, 4),
        ("Finalize com *morango e mais aveia*.", 55, 6), ("*Quatro ingredientes*,", 61, 2), ("*nenhum fogão*.", 63, 2),
        ("E dá pra montar *três copos* de noite", 65, 8), ("e deixar na geladeira.", 73, 4), ("*Isso.*", 84, 1), ("A fruta você coloca *na hora*.", 85, 6),
        ("*Isso aí.*", 103, 2), ("Manda pra quem vive de *biscoito recheado*.", 105, 7), ("E *curte*,", 112, 2),
        ("*comenta* qual fruta você colocaria", 114, 5), ("e *segue pra mais!*", 119, 4)], TOTAL)
