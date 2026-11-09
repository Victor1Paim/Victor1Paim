#!/usr/bin/env python3
"""Vídeo 03 do cronograma: "Postura perfeita existe?" (Costas na Cadeira)."""
import json, math, re, shutil
from pathlib import Path

SCR = Path("/tmp/claude-0/-home-user-Victor1Paim/bc508778-dc0e-5c3d-a4a6-a9dce8035bd2/scratchpad")
POST = Path("/home/user/Victor1Paim/saude-sem-sermao/producoes/03-postura-perfeita")
V = POST / "video"
(V / "compositions").mkdir(parents=True, exist_ok=True)
(V / "assets").mkdir(exist_ok=True)
for f in ["hyperframes.json", "package.json", "meta.json"]:
    (V / f).write_text((SCR / "hfblank" / f).read_text().replace('"hfblank"', '"saude-sem-sermao-03-postura"'))
shutil.copy(POST / "dialogo.mp3", V / "assets/voz.mp3")
shutil.copy(POST / "imagens/tito-cadeira.png", V / "assets/tito-cadeira.png")

W, H = 1080, 1920
TOTAL = 62.4
AZUL = "#CE6840"  # destaque deste vídeo: terracota
words = json.loads((POST / "conferencia/dialogo.palavras.json").read_text())
CENAS = []
src = (SCR / "build_sono.py").read_text()
exec(src[src.index("# ---------- paleta e base"):src.index("# ---------- 1. capa")])
exec(src[src.index("def cena_tito"):src.index("# ---------- 2. Tito: culpa")])
src2 = (SCR / "build_alongar.py").read_text()
exec(src2[src2.index("BASE_CSS += "):src2.index("VERDE, CREME, BRANCO")])
VERDE, CREME, BRANCO, LARANJA, PESSEGO = "#2F483A", "#FDF3ED", "#FFFFFF", "#D45F2B", "#F7E5DD"

src3 = (SCR / "build_passos.py").read_text()
exec(src3[src3.index("def tito_fala"):src3.index("# ---------- gráfico de risco")])
BASE_CSS += f"""
  .card2{{position:absolute;left:80px;width:920px;background:#fff;border-radius:30px;box-shadow:0 14px 40px rgba(40,60,40,.12);
         padding:30px 38px;font-weight:900;font-size:40px;line-height:1.25;}}
  .card2 .q{{font-size:30px;letter-spacing:.08em;color:{AZUL};margin-bottom:10px;}}
  .selo{{position:absolute;padding:10px 26px;border:6px solid;border-radius:16px;font-weight:900;font-size:56px;letter-spacing:.08em;background:rgba(255,255,255,.85);}}
"""


BASE_CSS += """
  .chip{position:absolute;left:80px;width:920px;padding:22px 34px;border-radius:26px;background:#fff;box-shadow:0 12px 34px rgba(80,40,20,.12);
        font-weight:900;font-size:46px;display:flex;align-items:center;gap:24px;}
  .chip .i{font-size:66px;line-height:1;}
"""
TERRA = "#CE6840"

# 1. capa (0 – 4.3)
d = add("capa", 0, 4.3)
cena("capa", d, f"""
  .bg{{background:{TERRA};}}
  .titulo{{color:var(--creme2);top:230px;font-size:120px;}}
  .titulo em{{color:#1F3328;}}
  #capa-c{{position:absolute;left:150px;top:560px;width:780px;height:780px;border-radius:50%;background:var(--creme);}}
  #capa-img{{left:280px;top:660px;width:520px;height:640px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="capa-t">Postura <em>perfeita</em> existe?</h1>
  <div id="capa-c"></div>
  <div class="img" id="capa-img"><img src="assets/tito-cadeira.png"></div>
""", f"""
  tl.fromTo("#capa-c",{{scale:0.6,opacity:0}},{{scale:1,opacity:1,duration:0.5,ease:"back.out(1.6)"}},0.1);
  tl.fromTo("#capa-img",{{rotation:0}},{{rotation:-4,duration:0.6,ease:"sine.inOut",yoyo:true,repeat:5,transformOrigin:"50% 100%"}},0.3);
""")

# 2. Tito: sentar reto (4.3 – 7.4)
tito_fala("t1", 4.3, 7.4, "Como assim? A vida inteira me mandaram sentar reto!", 4.64, 7.3, destaque=(7, 8), olhos="duvida", cor_ant=TERRA, tam=64)

# 3. revisão (7.4 – 16.0)
ini, fim = 7.4, 16.0
d = add("revisao", ini, fim)
wh, wj = wipe("revisao", CREME)
cena("revisao", d, f"""
  .bg{{background:#fff;}}
  #revisao-n{{position:absolute;left:80px;top:470px;font-family:'Playfair Display',serif;font-weight:700;font-size:230px;color:{TERRA};line-height:1;}}
  #revisao-l{{position:absolute;left:86px;top:730px;width:900px;font-weight:900;font-size:46px;}}
  #revisao-q{{position:absolute;left:80px;top:860px;width:920px;font-weight:900;font-size:44px;color:#5b524c;}}
  #revisao-selo{{left:560px;top:520px;color:var(--verde);border-color:var(--verde);font-size:46px;}}
  .fonte{{top:1060px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="revisao-t">Uma <em>grande</em> revisão</h1>
  <div id="revisao-n">0</div>
  <div id="revisao-l">revisões sistemáticas analisadas</div>
  <div id="revisao-q">“postura causa dor nas costas?”</div>
  <div class="selo" id="revisao-selo">SEM CONSENSO</div>
  <div class="fonte" id="revisao-f">Fonte: Swain et al., J Biomech, 2020</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#revisao-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(24)-ini:.2f});
  tl.fromTo("#revisao-f",{{opacity:0}},{{opacity:1,duration:0.3}},{t(26)-ini:.2f});
  tl.fromTo(["#revisao-n","#revisao-l"],{{opacity:0}},{{opacity:1,duration:0.3}},{t(28)-ini:.2f});
  {contador("#revisao-n", 0, 41, t(29)-ini, 1.0)}
  tl.fromTo("#revisao-q",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35}},{t(37)-ini:.2f});
  tl.fromTo("#revisao-selo",{{opacity:0,scale:2.4,rotation:-14}},{{opacity:1,scale:1,rotation:-6,duration:0.22,ease:"power4.in"}},{t(34)-ini:.2f});
  tl.fromTo("#root",{{x:0}},{{x:10,duration:0.04,yoyo:true,repeat:5,ease:"none"}},{t(34)-ini+0.22:.2f});
""")

# 4. curvas (16.0 – 21.0)
ini, fim = 16.0, 21.0
d = add("curvas", ini, fim)
wh, wj = wipe("curvas", BRANCO)
def coluna(i, curva, cor):
    pts = []
    for k in range(11):
        y = 30 + k * 34
        x = 60 + curva * math.sin((k / 10) * math.pi * 1.6 - 0.4)
        pts.append((x, y))
    path = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    dots = "".join(f'<rect x="{x-22:.1f}" y="{y-11:.1f}" width="44" height="22" rx="9" fill="{cor}"/>' for x, y in pts)
    return f'<svg class="col" id="curvas-c{i}" viewBox="0 0 120 400" style="left:{150+i*290}px"><path d="{path}" stroke="#2B2B2B" stroke-width="6" fill="none"/>{dots}</svg>'
cena("curvas", d, f"""
  .bg{{background:var(--pessego);}}
  .col{{position:absolute;top:470px;width:180px;height:600px;}}
  .fonte{{top:1090px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="curvas-t">Não existe <em>uma única</em> postura correta</h1>
  {coluna(0, 10, TERRA)}{coluna(1, 22, "#E2B04A")}{coluna(2, 34, "#2F483A")}
  <div class="fonte" id="curvas-f">Fonte: Slater et al., JOSPT, 2019</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#curvas-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.25);
  {' '.join(f'tl.fromTo("#curvas-c{i}",{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.4,ease:"back.out(1.6)"}},{t(51)-ini+i*0.3:.2f});' for i in range(3))}
  tl.fromTo("#curvas-f",{{opacity:0}},{{opacity:1,duration:0.3}},{t(51)-ini:.2f});
  tl.fromTo(".col",{{scaleX:1}},{{scaleX:1.12,duration:0.25,yoyo:true,repeat:1,stagger:0.12}},{t(56)-ini:.2f});
""")

# 5. Tito: torto (21.0 – 23.6)
tito_fala("t2", 21.0, 23.6, "Então eu posso ficar torto o dia inteiro?", 21.26, 23.4, destaque=(4,), olhos="duvida", cor_ant=PESSEGO, tam=66)

# 6. parado (23.6 – 28.95)
ini, fim = 23.6, 28.95
d = add("parado", ini, fim)
wh, wj = wipe("parado", CREME)
cena("parado", d, f"""
  .bg{{background:#EEF0EA;}}
  #parado-a{{top:500px;color:#8a837d;}}
  #parado-risco{{position:absolute;left:70px;top:556px;width:0;height:8px;background:{TERRA};border-radius:4px;}}
  #parado-b{{top:680px;background:var(--verde);color:#fff;}}
  #parado-rel{{position:absolute;left:390px;top:860px;width:300px;height:300px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="parado-t">O problema é ficar <em>parado</em></h1>
  <div class="chip" id="parado-a"><span class="i">🪑</span>a posição</div><div id="parado-risco"></div>
  <div class="chip" id="parado-b"><span class="i">⏳</span>parado muito tempo</div>
  <svg id="parado-rel" viewBox="0 0 100 100"><circle cx="50" cy="54" r="40" fill="#fff" stroke="#2F483A" stroke-width="6"/>
    <rect x="44" y="4" width="12" height="10" rx="3" fill="#2F483A"/>
    <line id="parado-pont" x1="50" y1="54" x2="50" y2="22" stroke="#2B2B2B" stroke-width="5" stroke-linecap="round"/></svg>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#parado-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.25);
  tl.fromTo("#parado-a",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(70)-ini:.2f});
  tl.fromTo("#parado-risco",{{width:0}},{{width:500,duration:0.35,ease:"power2.out"}},{t(72)-ini:.2f});
  tl.fromTo("#parado-b",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(77)-ini:.2f});
  tl.fromTo("#parado-rel",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"}},{t(78)-ini:.2f});
  tl.fromTo("#parado-pont",{{rotation:0,svgOrigin:"50 54"}},{{rotation:300,duration:1.4,ease:"power1.inOut"}},{t(80)-ini:.2f});
""")

# 7. próxima (28.95 – 36.55)
ini, fim = 28.95, 36.55
d = add("proxima", ini, fim)
wh, wj = wipe("proxima", "#EEF0EA")
ITENS = [("🔄", "muda de posição", 94), ("🧍", "levanta", 97), ("🙆", "se espreguiça", 98), ("🚶", "anda um pouco", 99)]
cena("proxima", d, f"""
  .bg{{background:var(--verde);}}
  .titulo{{color:var(--creme2);}}
  .titulo em{{color:var(--mostarda);}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="proxima-t">A melhor postura é a <em>próxima</em></h1>
  {''.join(f'<div class="chip" id="proxima-c{i}" style="top:{500+i*140}px"><span class="i">{e}</span>{n}</div>' for i,(e,n,_) in enumerate(ITENS))}
  {wh}
""", f"""
  {wj}
  tl.fromTo("#proxima-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(87)-ini:.2f});
  tl.fromTo("#proxima-t em",{{color:"#E2B04A"}},{{scale:1.1,duration:0.2,yoyo:true,repeat:1}},{t(93)-ini:.2f});
  {' '.join(f'tl.fromTo("#proxima-c{i}",{{opacity:0,x:-100}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(k)-ini-0.05:.2f});' for i,(_,_,k) in enumerate(ITENS))}
  {' '.join(f'tl.fromTo("#proxima-c{i} .i",{{rotation:0}},{{rotation:20,duration:0.15,yoyo:true,repeat:1}},{t(k)-ini+0.3:.2f});' for i,(_,_,k) in enumerate(ITENS))}
""")

# 8. Tito: doendo? (36.5 – 38.4)
tito_fala("t3", 36.55, 38.9, "E se as costas já estiverem doendo?", 36.6, 38.3, destaque=(3, 6), olhos="duvida", cor_ant=VERDE, tam=68)

# 9. dor (38.9 – 46.6)
ini, fim = 38.9, 46.6
d = add("dor", ini, fim)
wh, wj = wipe("dor", CREME)
cena("dor", d, f"""
  .bg{{background:#fff;}}
  #dor-sub{{position:absolute;left:80px;top:440px;font-weight:900;font-size:42px;color:#8a837d;}}
  #dor-card{{position:absolute;left:80px;top:540px;width:920px;padding:30px 36px;border-radius:30px;background:var(--pessego);}}
  #dor-card .q{{font-weight:900;font-size:34px;letter-spacing:.06em;color:{TERRA};margin-bottom:14px;}}
  .sinal{{font-weight:900;font-size:46px;margin:10px 0;}}
  #dor-pro{{position:absolute;left:80px;top:960px;width:920px;padding:22px 34px;border-radius:26px;background:var(--verde);color:#fff;font-weight:900;font-size:44px;}}
  .fonte{{top:1100px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="dor-t">Se mexer <em>costuma ajudar</em></h1>
  <div id="dor-sub">mais do que ficar travado</div>
  <div id="dor-card"><div class="q">⚠️ PROCURE AVALIAÇÃO SE A DOR…</div>
    <div class="sinal" id="dor-s0">• for forte</div><div class="sinal" id="dor-s1">• durar semanas</div><div class="sinal" id="dor-s2">• vier com formigamento</div></div>
  <div id="dor-pro">👩‍⚕️ procura um profissional</div>
  <div class="fonte" id="dor-f">Fonte: OMS, diretriz de dor lombar crônica, 2023</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#dor-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.2);
  tl.fromTo(["#dor-sub","#dor-f"],{{opacity:0}},{{opacity:1,duration:0.3}},{t(115)-ini:.2f});
  tl.fromTo("#dor-card",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.35,ease:"back.out(1.6)"}},{t(119)-ini:.2f});
  tl.fromTo("#dor-s0",{{opacity:0,x:40}},{{opacity:1,x:0,duration:0.3}},{t(124)-ini:.2f});
  tl.fromTo("#dor-s1",{{opacity:0,x:40}},{{opacity:1,x:0,duration:0.3}},{t(125)-ini:.2f});
  tl.fromTo("#dor-s2",{{opacity:0,x:40}},{{opacity:1,x:0,duration:0.3}},{t(128)-ini:.2f});
  tl.fromTo("#dor-pro",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.35,ease:"back.out(1.6)"}},{t(130)-ini:.2f});
""")

# 10. resumo (46.6 – 52.0)
ini, fim = 46.6, 52.0
d = add("resumo", ini, fim)
wh, wj = wipe("resumo", BRANCO)
txt = "Entendi! Postura perfeita não existe. A melhor é a próxima: o segredo é variar."
cena("resumo", d, """
  .bg{background:var(--creme);}
  .balao .txt{font-size:58px;}
""", f"""
  <div class="bg"></div>
  <div class="balao" id="resumo-balao"><div class="rot">💡 O QUE O TITO ENTENDEU</div>
    <div class="txt">{palavras_html("resumo", txt, 0, (6, 7, 8, 9, 13))}</div><div class="rabo"></div></div>
  <div class="tito-grande" id="resumo-tito">{tito_svg("resumo", bracos="acena")}</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#resumo-balao",{{opacity:0,y:30,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"back.out(1.6)"}},0.12);
  tl.fromTo("#resumo-tito",{{opacity:0,y:120}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.4)"}},0.05);
  {palavras_js("resumo", txt, ini, 46.7, 51.95)}
  {fala_js("resumo", round(46.7 - ini, 2), round(51.95 - ini, 2))}
""")


# 11. CTA (52.0 – fim): reaproveita o CTA do vídeo do café, trocando textos e o eco final
ini, fim = 52.0, TOTAL
d = add("cta", ini, fim)
wh, wj = wipe("cta", CREME)
src4 = (SCR / "build_cafe.py").read_text()
cta_src = src4[src4.index('cena("cta", d, """'):src4.index("# ---------- legendas do narrador")]
cta_src = (cta_src
    .replace("Manda pra quem diz que <em>café faz mal</em>", "Manda pra quem <em>corrige sua postura</em>")
    .replace('"☕ 3 xícaras!"', "🔄 PRÓXIMA")
    .replace("#cta-eco{position:absolute;inset:0;background:var(--mostarda);}", "#cta-eco{position:absolute;inset:0;background:#CE6840;}")
    .replace("#cta-eco .titulo{color:var(--verde);top:240px;font-size:128px;}", "#cta-eco .titulo{color:var(--creme2);top:230px;font-size:120px;}\n  #cta-eco-c2{position:absolute;left:150px;top:560px;width:780px;height:780px;border-radius:50%;background:var(--creme);}")
    .replace("#cta-eco .titulo em{color:#8E3412;}", "#cta-eco .titulo em{color:#1F3328;}")
    .replace('<div id="cta-eco-c"></div><h1 class="titulo">Café <em>faz mal?</em></h1>', '<div id="cta-eco-c2"></div><h1 class="titulo">Postura <em>perfeita</em> existe?</h1>')
    .replace("assets/tito-cafe.png", "assets/tito-cadeira.png")
    .replace("t(148)", "t(150)").replace("t(149)", "t(151)").replace("t(152)", "t(154)")
    .replace("t(159)", "t(160)").replace("t(158)", "t(159)").replace("t(165)", "t(169)"))
cta_src = cta_src.replace("TOTAL-ini-2.1", "TOTAL-ini-2.3").replace("t(169)-ini-0.05", "t(168)-ini-0.1").replace("t(169)-ini+0.45", "t(169)-ini+0.15").replace("#cta-eco-img{left:300px;top:500px;width:480px;height:570px;}", "#cta-eco-img{left:280px;top:660px;width:520px;height:640px;}")
exec(cta_src)

GRUPOS = [
    ("Postura *perfeita* existe?", 0, 3), ("A ciência diz: *não do jeito* que te ensinaram.", 3, 9),
    ("*Pois é.*", 21, 2), ("Mas uma *grande revisão*,", 23, 4), ("que juntou *41 revisões sistemáticas*,", 27, 5),
    ("*não encontrou consenso*", 32, 3), ("de que alguma postura *cause dor nas costas*.", 35, 8),
    ("E não existe *uma única postura correta*:", 43, 7), ("a coluna de cada pessoa tem *curvas diferentes*.", 50, 8),
    ("*Não é bem isso.*", 66, 4), ("O problema *não é a posição*.", 70, 6), ("É ficar *parado* nela por muito tempo.", 76, 7),
    ("Por isso se diz que", 83, 5), ("a melhor postura é *a próxima*:", 88, 6), ("*muda de posição*, *levanta*,", 94, 4), ("*se espreguiça*, *anda um pouco*.", 98, 5),
    ("*Se mexer* costuma ajudar", 110, 4), ("mais do que *ficar travado*.", 114, 5), ("Mas se a dor *for forte*,", 119, 6), ("*durar semanas*", 125, 2),
    ("ou vier com *formigamento*,", 127, 4), ("procura *um profissional*.", 131, 3),
    ("*Isso aí.*", 148, 2), ("Manda pra quem vive *corrigindo a sua postura*.", 150, 8), ("E *curte*,", 158, 2),
    ("*comenta PRÓXIMA* se você tá torto agora", 160, 8), ("e *segue pra mais!*", 168, 4),
]
for txt_, i0, n in GRUPOS:
    print(f"{txt_!r:56} <- {' '.join(w['palavra'] for w in words[i0:i0+n])!r}")
leg_html, leg_js = [], []
for k, (txt_, i0, n) in enumerate(GRUPOS):
    a = max(words[i0]["inicio"] - 0.08, 0.15)
    b = words[i0 + n - 1]["fim"] + 0.18
    if k + 1 < len(GRUPOS) and GRUPOS[k + 1][1] == i0 + n:
        b = min(b, words[GRUPOS[k + 1][1]]["inicio"] - 0.1)
    leg_html.append(f'<div class="leg" id="leg-{k}">{re.sub(r"[*](.+?)[*]", r"<b>\1</b>", txt_)}</div>')
    leg_js.append(f'tl.fromTo("#leg-{k}",{{opacity:0,y:16,visibility:"visible"}},{{opacity:1,y:0,duration:0.14,ease:"power2.out"}},{a:.2f});'
                  f'tl.to("#leg-{k}",{{opacity:0,duration:0.1,ease:"power2.in"}},{b-0.1:.2f});'
                  f'tl.set("#leg-{k}",{{opacity:0,visibility:"hidden"}},{b:.2f});')
(V / "compositions/legendas.html").write_text(f"""<template>
<style>
  #root{{position:absolute;inset:0;font-family:'Nunito',sans-serif;pointer-events:none;}}
  .leg{{position:absolute;left:80px;top:1180px;max-width:640px;background:#fff;border-radius:24px;padding:18px 30px;
        font-weight:900;font-size:50px;line-height:1.15;color:#2B2B2B;box-shadow:0 12px 34px rgba(80,40,20,.14);
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
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #FDF3ED; }}
      #main {{ position: relative; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="main" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
{chr(10).join(hosts)}
      <div id="legendas" data-composition-id="legendas" data-composition-src="compositions/legendas.html"
        data-start="0" data-duration="{TOTAL}" data-track-index="2" data-track-kind="captions"
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
