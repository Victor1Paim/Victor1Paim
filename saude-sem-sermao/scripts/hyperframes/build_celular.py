#!/usr/bin/env python3
"""Vídeo 04 do cronograma: "Celular antes de dormir faz mal?" (Tela na Mão)."""
import json, math, re, shutil
from pathlib import Path

SCR = Path("/tmp/claude-0/-home-user-Victor1Paim/bc508778-dc0e-5c3d-a4a6-a9dce8035bd2/scratchpad")
POST = Path("/home/user/Victor1Paim/saude-sem-sermao/producoes/04-celular-antes-de-dormir")
V = POST / "video"
(V / "compositions").mkdir(parents=True, exist_ok=True)
(V / "assets").mkdir(exist_ok=True)
for f in ["hyperframes.json", "package.json", "meta.json"]:
    (V / f).write_text((SCR / "hfblank" / f).read_text().replace('"hfblank"', '"saude-sem-sermao-04-celular"'))
shutil.copy(POST / "dialogo.mp3", V / "assets/voz.mp3")
shutil.copy(POST / "imagens/tito-cama.png", V / "assets/tito-cama.png")

W, H = 1080, 1920
TOTAL = 61.0
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
NOITE = "#22362A"

# 1. capa (0 – 5.1)
d = add("capa", 0, 5.1)
cena("capa", d, f"""
  .bg{{background:var(--verde);}}
  .titulo{{color:var(--creme2);top:230px;font-size:112px;}}
  .titulo em{{color:var(--mostarda);}}
  #capa-img{{left:300px;top:600px;width:480px;height:690px;}}
  #capa-brilho{{position:absolute;left:440px;top:820px;width:200px;height:200px;border-radius:50%;background:radial-gradient(rgba(190,225,255,.55),rgba(190,225,255,0) 70%);}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="capa-t">Celular antes de dormir <em>faz mal?</em></h1>
  <div class="img" id="capa-img"><img src="assets/tito-cama.png"></div>
  <div id="capa-brilho"></div>
""", f"""
  tl.fromTo("#capa-brilho",{{opacity:0.3,scale:0.8}},{{opacity:1,scale:1.15,duration:0.4,ease:"sine.inOut",yoyo:true,repeat:11}},0);
  tl.fromTo("#capa-img",{{y:0}},{{y:-10,duration:0.6,ease:"sine.inOut",yoyo:true,repeat:7}},0.2);
""")

# 2. Tito: luz azul (5.1 – 7.5)
tito_fala("t1", 5.1, 8.1, "Mas não é a luz azul que estraga o sono?", 5.42, 7.4, destaque=(4, 5), olhos="duvida", cor_ant=VERDE, tam=64)

# 3. luz pesa pouco (7.9 – 17.5)
ini, fim = 8.1, 17.5
d = add("luz", ini, fim)
wh, wj = wipe("luz", CREME)
cena("luz", d, f"""
  .bg{{background:#fff;}}
  .card2 .q{{color:var(--laranja);}}
  #luz-n{{position:absolute;left:630px;top:478px;white-space:nowrap;font-family:'Playfair Display',serif;font-weight:700;font-size:84px;color:var(--laranja);line-height:1;}}
  #luz-f1{{top:720px;}} #luz-f2{{top:1060px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="luz-t">A luz <em>pesa pouco</em></h1>
  <div class="card2" id="luz-a" style="top:420px;padding-right:330px"><div class="q">ESTUDO (PNAS, 2015)</div>4 h lendo no tablet: demorou mais pra dormir</div>
  <div id="luz-n">+0 min</div>
  <div class="fonte" id="luz-f1">Fonte: Chang et al., PNAS, 2015</div>
  <div class="card2" id="luz-b" style="top:800px"><div class="q">REVISÃO (2024)</div>a luz da tela atrasa o sono só por <span style="color:var(--laranja)">poucos minutos</span></div>
  <div class="fonte" id="luz-f2">Fonte: Bauducco et al., Sleep Med Rev, 2024</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#luz-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.2);
  tl.fromTo("#luz-a",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:0.4,ease:"back.out(1.6)"}},{max(t(28)-ini,0.3):.2f});
  tl.fromTo(["#luz-n","#luz-f1"],{{opacity:0}},{{opacity:1,duration:0.3}},{t(35)-ini:.2f});
  (function(){{const o={{v:0}};const el=document.querySelector("#luz-n");
    tl.fromTo(o,{{v:0}},{{v:10,duration:0.8,ease:"power2.out",onUpdate:()=>{{el.textContent="+"+Math.round(o.v)+" min";}}}},{t(39)-ini:.2f});}})();
  tl.fromTo("#luz-b",{{opacity:0,x:80}},{{opacity:1,x:0,duration:0.4,ease:"back.out(1.6)"}},{t(43)-ini:.2f});
  tl.fromTo("#luz-f2",{{opacity:0}},{{opacity:1,duration:0.3}},{t(43)-ini:.2f});
""")

# 4. feed (17.5 – 26.5)
ini, fim = 17.5, 26.5
d = add("feed", ini, fim)
wh, wj = wipe("feed", BRANCO)
POSTS = ["#CE6840", "#E2B04A", "#95A185", "#F7E5DD", "#CE6840", "#E2B04A", "#95A185", "#F7E5DD"]
cena("feed", d, f"""
  .bg{{background:var(--verde);}}
  .titulo{{color:var(--creme2);font-size:84px;}}
  .titulo em{{color:var(--mostarda);}}
  #feed-cel{{position:absolute;left:80px;top:440px;width:330px;height:620px;border-radius:44px;background:#1E1E1E;padding:18px;}}
  #feed-tela{{position:relative;width:100%;height:100%;border-radius:30px;background:#fff;overflow:hidden;}}
  #feed-lista{{position:absolute;left:14px;top:14px;width:266px;}}
  .post{{width:266px;height:150px;border-radius:18px;margin-bottom:14px;}}
  #feed-n1{{position:absolute;left:470px;top:460px;width:530px;font-weight:900;font-size:40px;color:var(--creme2);}}
  #feed-n1 b{{font-family:'Playfair Display',serif;font-size:90px;color:var(--mostarda);display:block;line-height:1.05;}}
  #feed-n2{{position:absolute;left:470px;top:720px;width:530px;font-weight:900;font-size:40px;color:var(--creme2);}}
  #feed-n2 b{{font-family:'Playfair Display',serif;font-size:110px;color:var(--mostarda);display:block;line-height:1.05;}}
  .fonte{{top:1090px;color:#c9d3c6;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="feed-t">O que pesa: <em>"só mais um vídeo"</em></h1>
  <div id="feed-cel"><div id="feed-tela"><div id="feed-lista">{''.join(f'<div class="post" style="background:{c}"></div>' for c in POSTS)}</div></div></div>
  <div id="feed-n1"><b>548 mil</b>pessoas acompanhadas</div>
  <div id="feed-n2"><b id="feed-min">+0 min</b>pra dormir, por hora de tela</div>
  <div class="fonte" id="feed-f">Fonte: meta-análise de 21 coortes, Frontiers in Psychiatry, 2025</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#feed-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.2);
  tl.fromTo("#feed-cel",{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.4,ease:"back.out(1.6)"}},{t(64)-ini:.2f});
  tl.fromTo("#feed-lista",{{y:0}},{{y:-660,duration:{fim-ini-1.6:.2f},ease:"none"}},{t(64)-ini+0.3:.2f});
  tl.fromTo(["#feed-n1","#feed-f"],{{opacity:0,x:40}},{{opacity:1,x:0,duration:0.35}},{t(72)-ini:.2f});
  tl.fromTo("#feed-n2",{{opacity:0,x:40}},{{opacity:1,x:0,duration:0.35}},{t(78)-ini:.2f});
  (function(){{const o={{v:0}};const el=document.querySelector("#feed-min");
    tl.fromTo(o,{{v:0}},{{v:13,duration:0.9,ease:"power2.out",onUpdate:()=>{{el.textContent="+"+Math.round(o.v)+" min";}}}},{t(84)-ini:.2f});}})();
""")

# 5. Tito: perco a hora (26.5 – 29.8)
tito_fala("t2", 26.5, 30.05, "Então o problema é que eu perco a hora rolando o feed?", 26.78, 29.6, destaque=(6, 7, 8, 9, 10, 11), olhos="duvida", cor_ant=VERDE, tam=58)

# 6. emoção (30.05 – 36.3)
ini, fim = 30.05, 36.3
d = add("emocao", ini, fim)
wh, wj = wipe("emocao", CREME)
cena("emocao", d, f"""
  .bg{{background:var(--pessego);}}
  #emocao-selo{{left:80px;top:200px;color:var(--verde);border-color:var(--verde);font-size:44px;}}
  .titulo{{top:330px;}}
  #emocao-c{{position:absolute;left:390px;top:840px;width:300px;height:300px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;font-size:170px;box-shadow:0 14px 40px rgba(80,40,20,.14);}}
  #emocao-r{{position:absolute;left:80px;top:1150px;width:920px;text-align:center;font-weight:900;font-size:44px;color:var(--verde);}}
""", f"""
  <div class="bg"></div>
  <div class="selo" id="emocao-selo">✓ EXATO</div>
  <h1 class="titulo" id="emocao-t">Conteúdo que <em>mexe com a emoção</em></h1>
  <div class="chip" id="emocao-a" style="top:560px"><span class="i">💢</span>briga nos comentários</div>
  <div class="chip" id="emocao-b" style="top:690px"><span class="i">📰</span>notícia tensa</div>
  <div id="emocao-c">🧠</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#emocao-selo",{{opacity:0,scale:2.2,rotation:-12}},{{opacity:1,scale:1,rotation:-5,duration:0.22,ease:"power4.in"}},{max(t(101)-ini,0.1):.2f});
  tl.fromTo("#emocao-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(102)-ini:.2f});
  tl.fromTo("#emocao-a",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(110)-ini:.2f});
  tl.fromTo("#emocao-b",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(114)-ini:.2f});
  tl.fromTo("#emocao-c",{{scale:0}},{{scale:1,duration:0.35,ease:"back.out(2.2)"}},{t(116)-ini:.2f});
  tl.fromTo("#emocao-c",{{boxShadow:"0 0 0 0 rgba(212,95,43,.6)"}},{{boxShadow:"0 0 0 40px rgba(212,95,43,0)",duration:0.6,repeat:1,ease:"power1.out"}},{t(118)-ini:.2f});
""")

# 7. Tito: jogo fora? (36.3 – 38.1)
tito_fala("t3", 36.3, 38.6, "E aí? Joga o celular fora?", 36.54, 37.95, destaque=(4, 5), olhos="duvida", cor_ant=PESSEGO, tam=72)

# 8. dicas (38.6 – 46.9)
ini, fim = 38.6, 46.9
d = add("dicas", ini, fim)
wh, wj = wipe("dicas", CREME)
cena("dicas", d, f"""
  .bg{{background:#EEF0EA;}}
  #dicas-np{{position:absolute;left:80px;top:180px;font-weight:900;font-size:44px;color:#8a837d;}}
  .titulo{{top:270px;}}
""", f"""
  <div class="bg"></div>
  <div id="dicas-np">Não precisa. 😌</div>
  <h1 class="titulo" id="dicas-t">3 ajustes <em>possíveis</em></h1>
  <div class="chip" id="dicas-a" style="top:520px"><span class="i">⏰</span>alarme pra hora de largar</div>
  <div class="chip" id="dicas-b" style="top:660px"><span class="i">🛏️</span>celular longe da cama</div>
  <div class="chip" id="dicas-c" style="top:800px"><span class="i">🎧</span>música ou podcast no lugar do feed</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#dicas-np",{{opacity:0}},{{opacity:1,duration:0.3}},0.1);
  tl.fromTo("#dicas-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{max(t(127)-ini,0.2):.2f});
  tl.fromTo("#dicas-a",{{opacity:0,x:-100}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(128)-ini:.2f});
  tl.fromTo("#dicas-a .i",{{rotation:-15}},{{rotation:15,duration:0.08,yoyo:true,repeat:9,ease:"none"}},{t(130)-ini:.2f});
  tl.fromTo("#dicas-b",{{opacity:0,x:-100}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(135)-ini:.2f});
  tl.fromTo("#dicas-c",{{opacity:0,x:-100}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(142)-ini:.2f});
""")

# 9. resumo (46.9 – 51.9)
ini, fim = 46.9, 51.9
d = add("resumo", ini, fim)
wh, wj = wipe("resumo", "#EEF0EA")
txt = "Entendi! Não é só a luz, é o tempo: o feed rouba o sono. Bora de alarme!"
cena("resumo", d, """
  .bg{background:var(--creme);}
  .balao .txt{font-size:56px;}
""", f"""
  <div class="bg"></div>
  <div class="balao" id="resumo-balao"><div class="rot">💡 O QUE O TITO ENTENDEU</div>
    <div class="txt">{palavras_html("resumo", txt, 0, (6, 7, 8, 10, 11, 12, 13))}</div><div class="rabo"></div></div>
  <div class="tito-grande" id="resumo-tito">{tito_svg("resumo", bracos="acena")}</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#resumo-balao",{{opacity:0,y:30,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"back.out(1.6)"}},0.12);
  tl.fromTo("#resumo-tito",{{opacity:0,y:120}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.4)"}},0.05);
  {palavras_js("resumo", txt, ini, 47.1, 51.8)}
  {fala_js("resumo", round(47.1 - ini, 2), round(51.8 - ini, 2))}
""")

# 10. CTA (51.9 – fim)
ini, fim = 51.9, TOTAL
d = add("cta", ini, fim)
wh, wj = wipe("cta", CREME)
src4 = (SCR / "build_cafe.py").read_text()
cta_src = src4[src4.index('cena("cta", d, """'):src4.index("# ---------- legendas do narrador")]
cta_src = (cta_src
    .replace(".bg{background:var(--laranja);}", ".bg{background:var(--verde);}\n  #cta-tito{filter:drop-shadow(0 0 2px #FDF3ED) drop-shadow(0 0 2px #FDF3ED);}")  # Tito não some no fundo
    .replace("Manda pra quem diz que <em>café faz mal</em>", "Manda pra quem dorme <em>no celular</em>")
    .replace('"☕ 3 xícaras!"', "⏰ ALARME")
    .replace("#cta-eco{position:absolute;inset:0;background:var(--mostarda);}", "#cta-eco{position:absolute;inset:0;background:var(--verde);}")
    .replace("#cta-eco .titulo{color:var(--verde);top:240px;font-size:128px;}", "#cta-eco .titulo{color:var(--creme2);top:230px;font-size:112px;}")
    .replace("#cta-eco .titulo em{color:#8E3412;}", "#cta-eco .titulo em{color:var(--mostarda);}")
    .replace('<div id="cta-eco-c"></div><h1 class="titulo">Café <em>faz mal?</em></h1>', '<h1 class="titulo">Celular antes de dormir <em>faz mal?</em></h1>')
    .replace("assets/tito-cafe.png", "assets/tito-cama.png")
    .replace("#cta-eco-img{left:300px;top:500px;width:480px;height:570px;}", "#cta-eco-img{left:300px;top:600px;width:480px;height:690px;}")
    .replace("t(165)-ini-0.05", "t(189)-ini-0.1").replace("t(165)-ini+0.45", "t(190)-ini+0.15")
    .replace("TOTAL-ini-2.1", "TOTAL-ini-2.3")
    .replace("t(148)", "t(172)").replace("t(149)", "t(173)").replace("t(152)", "t(178)")
    .replace("t(158)", "t(182)").replace("t(159)", "t(183)").replace("t(165)", "t(190)"))
exec(cta_src)

GRUPOS = [
    ("Celular antes de dormir *faz mal?*", 0, 6), ("*Depende* menos da luz", 6, 4), ("e mais do que *você faz nele*.", 10, 7),
    ("Num *estudo famoso*,", 27, 3), ("ler *4 horas* num tablet", 30, 5), ("atrasou o sono em *uns 10 minutos*.", 35, 7),
    ("E uma *revisão recente* concluiu:", 42, 5), ("a luz da tela atrasou o sono", 47, 7), ("só por *poucos minutos*.", 54, 4),
    ("O que pesa mais é o *“só mais um vídeo”*.", 58, 10), ("Uma *meta-análise*", 68, 3), ("com *mais de 500 mil pessoas*", 71, 6),
    ("ligou cada *hora de tela*", 77, 5), ("a dormir *uns 13 minutos mais tarde*.", 82, 7),
    ("*Exato.*", 101, 1), ("E conteúdo que *mexe com a emoção*,", 102, 7), ("tipo *briga nos comentários*", 109, 4), ("ou *notícia tensa*,", 113, 3),
    ("deixa a *cabeça ligada*.", 116, 4),
    ("*Não precisa.*", 126, 2), ("Coloca um *alarme* pra hora de largar,", 128, 7), ("deixa o celular *longe da cama*", 135, 6),
    ("e troca o *feed infinito*", 141, 5), ("por algo calmo, como *música ou podcast*.", 146, 7),
    ("*Isso aí.*", 170, 2), ("Manda pra quem dorme com o *celular na cara*.", 172, 9), ("E *curte*,", 181, 2),
    ("*comenta ALARME* se você vai testar", 183, 6), ("e *segue pra mais!*", 189, 4),
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
