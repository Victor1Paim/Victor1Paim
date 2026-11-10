#!/usr/bin/env python3
"""Vídeo 09 do cronograma: "Comer à noite engorda?" (estrutura Contradição)."""
import json, math, re, shutil
from pathlib import Path

SCR = Path("/tmp/claude-0/-home-user-Victor1Paim/bc508778-dc0e-5c3d-a4a6-a9dce8035bd2/scratchpad")
POST = Path("/home/user/Victor1Paim/saude-sem-sermao/producoes/09-comer-a-noite")
V = POST / "video"
(V / "compositions").mkdir(parents=True, exist_ok=True)
(V / "assets").mkdir(exist_ok=True)
for f in ["hyperframes.json", "package.json", "meta.json"]:
    (V / f).write_text((SCR / "hfblank" / f).read_text().replace('"hfblank"', '"saude-sem-sermao-09-noite"'))
shutil.copy(POST / "dialogo.mp3", V / "assets/voz.mp3")
shutil.copy(POST / "imagens/tito-jantar.png", V / "assets/tito-jantar.png")

W, H = 1080, 1920
TOTAL = 56.9
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
        font-weight:900;font-size:44px;display:flex;align-items:center;gap:24px;}
  .chip .i{font-size:66px;line-height:1;}
"""
SALVIA = "#95A185"

# 1. capa (0 – 3.2)
d = add("capa", 0, 3.2)
cena("capa", d, f"""
  .bg{{background:{SALVIA};}}
  .titulo{{color:#1F3328;top:300px;font-size:120px;}}
  .titulo em{{color:#7A2E10;}}
  #capa-selo{{left:80px;top:190px;color:#1F3328;border-color:#1F3328;background:rgba(255,255,255,.6);font-size:38px;}}
  #capa-img{{left:200px;top:640px;width:680px;height:780px;}}
""", f"""
  <div class="bg"></div>
  <div class="selo" id="capa-selo">TODO MUNDO DIZ</div>
  <h1 class="titulo" id="capa-t">Comer à noite <em>engorda?</em></h1>
  <div class="img" id="capa-img"><img src="assets/tito-jantar.png"></div>
""", f"""
  tl.fromTo("#capa-selo",{{opacity:0,scale:2,rotation:-10}},{{opacity:1,scale:1,rotation:-4,duration:0.22,ease:"power4.in"}},0.15);
  tl.fromTo("#capa-img",{{y:0}},{{y:-10,duration:0.5,ease:"sine.inOut",yoyo:true,repeat:5}},0.2);
""")

# 2. Tito (3.2 – 6.3)
tito_fala("t1", 3.2, 6.3, "Por isso eu janto às sete e vou dormir com fome!", 3.32, 6.1, destaque=(3, 4, 5, 9, 10), olhos="duvida", cor_ant=SALVIA, tam=60)

# 3. estudo 1 (6.3 – 18.6)
ini, fim = 6.3, 18.6
d = add("estudo", ini, fim)
wh, wj = wipe("estudo", CREME)
cena("estudo", d, f"""
  .bg{{background:#fff;}}
  #estudo-c{{position:absolute;left:80px;top:440px;width:920px;padding:24px 34px;border-radius:26px;background:#EEF0EA;font-weight:900;font-size:40px;}}
  #estudo-c .q{{font-size:30px;letter-spacing:.06em;color:var(--laranja);margin-bottom:6px;}}
  .mes{{position:absolute;top:650px;width:430px;height:360px;border-radius:30px;background:#fff;box-shadow:0 14px 40px rgba(40,60,40,.14);
        display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;text-align:center;font-weight:900;font-size:38px;}}
  .mes .i{{font-size:110px;line-height:1;}}
  .mes .m{{font-size:28px;color:#8a837d;letter-spacing:.06em;}}
  #estudo-r{{position:absolute;left:190px;top:1020px;width:700px;white-space:nowrap;padding:18px 0;text-align:center;border-radius:999px;background:var(--verde);color:#fff;font-weight:900;font-size:46px;}}
  .fonte{{top:1130px;}}
  #estudo-c{{top:470px !important;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="estudo-t">Essa regra tem <em>um problema</em></h1>
  <div id="estudo-c"><div class="q">ESTUDO (2022)</div>30 pessoas · as mesmas calorias</div>
  <div class="mes" id="estudo-a" style="left:80px"><span class="m">MÊS 1</span><span class="i">☀️</span>café da manhã reforçado</div>
  <div class="mes" id="estudo-b" style="left:570px"><span class="m">MÊS 2</span><span class="i">🌙</span>jantar reforçado</div>
  <div id="estudo-r">= mesmo peso perdido</div>
  <div class="fonte" id="estudo-f">Fonte: Ruddick-Collins et al., Cell Metabolism, 2022</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#estudo-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.2);
  tl.fromTo(["#estudo-c","#estudo-f"],{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.35,ease:"back.out(1.6)"}},{t(27)-ini:.2f});
  tl.fromTo("#estudo-a",{{opacity:0,x:-100}},{{opacity:1,x:0,duration:0.4,ease:"back.out(1.6)"}},{t(35)-ini:.2f});
  tl.fromTo("#estudo-b",{{opacity:0,x:100}},{{opacity:1,x:0,duration:0.4,ease:"back.out(1.6)"}},{t(41)-ini:.2f});
  tl.fromTo("#estudo-r",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.4)"}},{t(46)-ini:.2f});
  tl.fromTo([".mes"],{{y:0}},{{y:-14,duration:0.18,yoyo:true,repeat:1,stagger:0.08}},{t(48)-ini:.2f});
""")

# 4. Tito (18.6 – 20.8)
tito_fala("t2", 18.6, 20.8, "Então comer à noite não engorda nada?", 18.68, 20.6, destaque=(5, 6), olhos="duvida", cor_ant=BRANCO, tam=66)

# 5. fome (20.8 – 25.55)
ini, fim = 20.8, 25.55
d = add("fome", ini, fim)
wh, wj = wipe("fome", CREME)
cena("fome", d, f"""
  .bg{{background:var(--pessego);}}
  #fome-calma{{position:absolute;left:80px;top:190px;font-weight:900;font-size:44px;color:#8a837d;}}
  .titulo{{top:270px;}}
  #fome-trilho{{position:absolute;left:140px;top:480px;width:100px;height:540px;border-radius:50px;background:#fff;overflow:hidden;}}
  #fome-nivel{{position:absolute;left:0;bottom:0;width:100px;height:540px;border-radius:50px;background:linear-gradient(#D45F2B,#E2B04A);transform-origin:50% 100%;}}
  #fome-rot{{position:absolute;left:100px;top:1035px;width:180px;text-align:center;font-weight:900;font-size:38px;}}
  #fome-a{{position:absolute;left:320px;top:520px;width:680px;font-weight:900;font-size:46px;}}
  #fome-b{{position:absolute;left:320px;top:700px;width:680px;font-weight:900;font-size:36px;color:#8a837d;}}
  .fonte{{top:1110px;}}
""", f"""
  <div class="bg"></div>
  <div id="fome-calma">Calma. ✋</div>
  <h1 class="titulo" id="fome-t">Mas o horário mexe com a <em>fome</em></h1>
  <div id="fome-trilho"><div id="fome-nivel"></div></div><div id="fome-rot">fome</div>
  <div id="fome-a">🌙 comer mais tarde → <span style="color:var(--laranja)">mais fome</span></div>
  <div id="fome-b">estudo pequeno: 16 pessoas</div>
  <div class="fonte" id="fome-f">Fonte: Vujović et al., Cell Metabolism, 2022</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#fome-calma",{{opacity:0}},{{opacity:1,duration:0.3}},0.1);
  tl.fromTo("#fome-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(61)-ini:.2f});
  tl.fromTo(["#fome-trilho","#fome-rot","#fome-f"],{{opacity:0}},{{opacity:1,duration:0.3}},{t(61)-ini:.2f});
  tl.fromTo("#fome-b",{{opacity:0}},{{opacity:1,duration:0.3}},{t(62)-ini:.2f});
  tl.fromTo("#fome-a",{{opacity:0,x:60}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(66)-ini:.2f});
  tl.fromTo("#fome-nivel",{{scaleY:0.2}},{{scaleY:0.9,duration:1.2,ease:"power2.out"}},{t(69)-ini:.2f});
""")

# 6. VIRADA: o porquê (25.55 – 38.45)
ini, fim = 25.55, 38.45
d = add("virada", ini, fim)
wh, wj = wipe("virada", PESSEGO)
BLOCOS = [("☀️ café", "#E2B04A", 95), ("🍽️ almoço", "#95A185", 96), ("🌙 jantar", "#2F483A", 97), ("🍪 belisco", "#D45F2B", 116), ("🍫 belisco", "#D45F2B", 117), ("🥨 belisco", "#D45F2B", 119)]
cena("virada", d, f"""
  .bg{{background:#fff;}}
  #virada-rel{{position:absolute;left:330px;top:300px;width:420px;height:420px;}}
  #virada-selo{{left:290px;top:420px;color:var(--laranja);border-color:var(--laranja);font-size:84px;}}
  #virada-t2{{position:absolute;left:80px;top:220px;width:920px;font-family:'Playfair Display',serif;font-weight:700;font-size:84px;line-height:1.05;}}
  #virada-t2 em{{color:var(--laranja);}}
  #virada-pilha{{position:absolute;left:80px;top:440px;width:920px;display:flex;flex-direction:column;gap:12px;}}
  .bloco{{height:88px;border-radius:20px;display:flex;align-items:center;padding:0 30px;font-weight:900;font-size:40px;color:#fff;}}
""", f"""
  <div class="bg"></div>
  <svg id="virada-rel" viewBox="0 0 100 100"><circle cx="50" cy="50" r="44" fill="#FDF3ED" stroke="#2F483A" stroke-width="6"/>
    <line x1="50" y1="50" x2="50" y2="20" stroke="#2B2B2B" stroke-width="5" stroke-linecap="round"/>
    <line x1="50" y1="50" x2="30" y2="62" stroke="#2B2B2B" stroke-width="5" stroke-linecap="round"/></svg>
  <div class="selo" id="virada-selo">✕ MITO</div>
  <h1 id="virada-t2">O que pesa: <em>o total do dia</em></h1>
  <div id="virada-pilha">{''.join(f'<div class="bloco" id="virada-b{i}" style="background:{c}">{n}</div>' for i,(n,c,_) in enumerate(BLOCOS))}</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#virada-rel",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.4,ease:"back.out(1.8)"}},0.2);
  tl.fromTo("#virada-selo",{{opacity:0,scale:2.6,rotation:-16}},{{opacity:1,scale:1,rotation:-8,duration:0.22,ease:"power4.in"}},{t(85)-ini:.2f});
  tl.fromTo("#root",{{x:0}},{{x:10,duration:0.04,yoyo:true,repeat:5,ease:"none"}},{t(85)-ini+0.22:.2f});
  tl.to(["#virada-rel","#virada-selo"],{{opacity:0,y:-40,duration:0.3}},{t(95)-ini-0.35:.2f});
  tl.fromTo("#virada-t2",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(95)-ini-0.1:.2f});
  {' '.join(f'tl.fromTo("#virada-b{i}",{{opacity:0,x:-120}},{{opacity:1,x:0,duration:0.3,ease:"back.out(1.6)"}},{t(k)-ini:.2f});' for i,(_,_,k) in enumerate(BLOCOS))}
  tl.fromTo(["#virada-b3","#virada-b4","#virada-b5"],{{scale:1}},{{scale:1.04,duration:0.15,yoyo:true,repeat:1,stagger:0.08}},{t(119)-ini+0.3:.2f});
""")

# 7. resumo (38.45 – 44.55)
ini, fim = 38.45, 44.55
d = add("resumo", ini, fim)
wh, wj = wipe("resumo", BRANCO)
txt = "Entendi! Não é o relógio, é o total do dia. Jantar, tudo bem. O que pesa é o belisco sem fim."
cena("resumo", d, """
  .bg{background:var(--creme);}
  .balao .txt{font-size:54px;}
""", f"""
  <div class="bg"></div>
  <div class="balao" id="resumo-balao"><div class="rot">💡 O QUE O TITO ENTENDEU</div>
    <div class="txt">{palavras_html("resumo", txt, 0, (5, 6, 7, 8, 9, 18, 19, 20))}</div><div class="rabo"></div></div>
  <div class="tito-grande" id="resumo-tito">{tito_svg("resumo", bracos="acena")}</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#resumo-balao",{{opacity:0,y:30,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"back.out(1.6)"}},0.12);
  tl.fromTo("#resumo-tito",{{opacity:0,y:120}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.4)"}},0.05);
  {palavras_js("resumo", txt, ini, 38.52, 44.3)}
  {fala_js("resumo", round(38.52 - ini, 2), round(44.3 - ini, 2))}
""")

# 8. resposta + eco do gancho (44.55 – 47.65)
ini, fim = 44.55, 47.65
d = add("resposta", ini, fim)
wh, wj = wipe("resposta", CREME)
cena("resposta", d, f"""
  .bg{{background:{SALVIA};}}
  .titulo{{color:#1F3328;top:240px;font-size:96px;}}
  .titulo em{{color:#7A2E10;}}
  #resposta-img{{left:240px;top:640px;width:600px;height:690px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="resposta-t">Comer à noite engorda? <em>Não por ser à noite.</em></h1>
  <div class="img" id="resposta-img"><img src="assets/tito-jantar.png"></div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#resposta-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.15);
  tl.fromTo("#resposta-t em",{{scale:1}},{{scale:1.06,duration:0.18,yoyo:true,repeat:1}},{t(146)-ini:.2f});
  tl.fromTo("#resposta-img",{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.4,ease:"back.out(1.6)"}},0.25);
""")

# 9. CTA (47.65 – fim)
ini, fim = 47.65, TOTAL
d = add("cta", ini, fim)
wh, wj = wipe("cta", CREME)
src4 = (SCR / "build_cafe.py").read_text()
cta_src = src4[src4.index('cena("cta", d, """'):src4.index("# ---------- legendas do narrador")]
cta_src = (cta_src
    .replace(".bg{background:var(--laranja);}", ".bg{background:var(--verde);}\n  #cta-tito{filter:drop-shadow(0 0 2px #FDF3ED) drop-shadow(0 0 2px #FDF3ED);}")  # Tito não some no fundo
    .replace("Manda pra quem diz que <em>café faz mal</em>", "Manda pra quem <em>janta às seis</em>")
    .replace('"☕ 3 xícaras!"', "🕗 OITO")
    .replace("#cta-eco{position:absolute;inset:0;background:var(--mostarda);}", "#cta-eco{position:absolute;inset:0;background:#95A185;}")
    .replace("#cta-eco .titulo{color:var(--verde);top:240px;font-size:128px;}", "#cta-eco .titulo{color:#1F3328;top:300px;font-size:120px;}")
    .replace("#cta-eco .titulo em{color:#8E3412;}", "#cta-eco .titulo em{color:#7A2E10;}")
    .replace('<div id="cta-eco-c"></div><h1 class="titulo">Café <em>faz mal?</em></h1>', '<h1 class="titulo">Comer à noite <em>engorda?</em></h1>')
    .replace("assets/tito-cafe.png", "assets/tito-jantar.png")
    .replace("#cta-eco-img{left:300px;top:500px;width:480px;height:570px;}", "#cta-eco-img{left:200px;top:640px;width:680px;height:780px;}")
    .replace("t(165)-ini-0.05", "t(173)-ini-0.1").replace("t(165)-ini+0.45", "t(174)-ini+0.15")
    .replace("TOTAL-ini-2.1", "TOTAL-ini-2.3")
    .replace("t(165)", "t(174)").replace("t(159)", "t(165)").replace("t(158)", "t(164)")
    .replace("t(148)", "t(153)").replace("t(149)", "t(154)").replace("t(152)", "t(158)"))
exec(cta_src)

GRUPOS = [
    ("Todo mundo diz:", 0, 3), ("comeu *depois das oito*,", 3, 4), ("*vira gordura*.", 7, 2),
    ("Só que essa regra *tem um problema*.", 20, 7), ("Num estudo, *30 pessoas*", 27, 4), ("comeram *as mesmas calorias*:", 31, 4),
    ("num mês, *café da manhã reforçado*;", 35, 6), ("no outro, *jantar reforçado*.", 41, 4),
    ("Resultado: perderam *o mesmo peso*", 45, 5), ("nas duas fases.", 50, 3),
    ("*Calma.*", 60, 1), ("Outro estudo, *pequeno*,", 61, 3), ("mostrou que *comer mais tarde*", 64, 5), ("deixou as pessoas com *mais fome*.", 69, 6),
    ("E aqui está *o porquê*:", 75, 5), ("o corpo *não tem um relógio*", 80, 6), ("que transforma a comida em gordura", 86, 6), ("depois das oito.", 92, 3),
    ("O que pesa é *quanto você come*", 95, 7), ("*no dia todo*.", 102, 3),
    ("E à noite, *cansado e com fome*,", 105, 7), ("é mais fácil *o belisco não ter fim*.", 112, 8),
    ("Então, *comer à noite engorda?*", 141, 5), ("*Não por ser à noite.*", 146, 5),
    ("*Isso aí.*", 151, 2), ("Manda pra quem janta às seis *com medo da balança*.", 153, 10), ("E *curte*,", 163, 2),
    ("*comenta OITO* se você já ouviu essa regra", 165, 8), ("e *segue pra mais!*", 173, 4),
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
