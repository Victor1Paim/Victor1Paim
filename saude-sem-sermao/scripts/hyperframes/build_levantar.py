#!/usr/bin/env python3
"""Vídeo 07 do cronograma: "Levantar a cada 30 minutos funciona?" (estrutura Escolha)."""
import json, math, re, shutil
from pathlib import Path

SCR = Path("/tmp/claude-0/-home-user-Victor1Paim/bc508778-dc0e-5c3d-a4a6-a9dce8035bd2/scratchpad")
POST = Path("/home/user/Victor1Paim/saude-sem-sermao/producoes/07-levantar-30-min")
V = POST / "video"
(V / "compositions").mkdir(parents=True, exist_ok=True)
(V / "assets").mkdir(exist_ok=True)
for f in ["hyperframes.json", "package.json", "meta.json"]:
    (V / f).write_text((SCR / "hfblank" / f).read_text().replace('"hfblank"', '"saude-sem-sermao-07-levantar"'))
shutil.copy(POST / "dialogo.mp3", V / "assets/voz.mp3")
shutil.copy(POST / "imagens/tito-levanta.png", V / "assets/tito-levanta.png")

W, H = 1080, 1920
TOTAL = 68.7
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
  .op{position:absolute;top:470px;width:440px;height:520px;border-radius:34px;background:#fff;box-shadow:0 16px 44px rgba(40,60,40,.14);
      display:flex;flex-direction:column;align-items:center;justify-content:flex-start;padding-top:24px;text-align:center;font-weight:900;font-size:36px;line-height:1.25;}
  .op .L{width:110px;height:110px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#fff;
         font-family:'Playfair Display',serif;font-weight:800;font-size:76px;margin-bottom:18px;}
  .op .i{font-size:70px;line-height:1.2;}
  .op small{font-size:30px;color:#8a837d;}
  .placar{position:absolute;left:80px;top:180px;width:920px;padding:14px 26px;border-radius:22px;background:rgba(31,51,40,.92);color:#fff;font-weight:900;font-size:30px;letter-spacing:.05em;display:flex;justify-content:space-between;}
"""
MOST = "#E2B04A"; AZA = "#3B6EA5"; VB = "#2F483A"

def opcoes(cid, top=470):
    return (f'<div class="op" id="{cid}-a" style="left:80px;top:{top}px"><div class="L" style="background:{AZA}">A</div><span class="i">🚶‍♂️</span>30 min de caminhada<br><small>e depois</small><span class="i">🪑</span>9 h sentado</div>'
            f'<div class="op" id="{cid}-b" style="left:560px;top:{top}px"><div class="L" style="background:{VB}">B</div><span class="i">⏱️🚶</span>2 min de caminhada<br><small>a cada</small><span class="i" style="font-size:60px;font-weight:900;color:{VB}">30 min</span></div>')

# 1. gancho: duas opções (0 – 8.7)
d = add("capa", 0, 8.7)
cena("capa", d, f"""
  .bg{{background:{MOST};}}
  .titulo{{color:#1F3328;top:230px;font-size:104px;}}
  .titulo em{{color:#7A2E10;}}
  #capa-img{{left:320px;top:1040px;width:440px;height:300px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="capa-t">Duas opções. <em>Qual é melhor?</em></h1>
  {opcoes("capa")}
  <div class="img" id="capa-img"><img src="assets/tito-levanta.png"></div>
""", f"""
  tl.fromTo("#capa-t",{{scale:0.96}},{{scale:1,duration:0.4,ease:"power3.out"}},0);
  tl.fromTo("#capa-a",{{opacity:0,x:-120}},{{opacity:1,x:0,duration:0.4,ease:"back.out(1.6)"}},{t(8)-0.1:.2f});
  tl.fromTo("#capa-b",{{opacity:0,x:120}},{{opacity:1,x:0,duration:0.4,ease:"back.out(1.6)"}},{t(18)-0.1:.2f});
  tl.fromTo("#capa-img",{{x:-30}},{{x:30,duration:1.2,ease:"sine.inOut",yoyo:true,repeat:5}},0);
""")

# 2. Tito escolhe A (8.7 – 12.6)
tito_fala("t1", 8.7, 12.6, "Fácil! A! Meia hora seguida é exercício de verdade.", 8.84, 12.4, destaque=(1,), olhos="normal", cor_ant=MOST, tam=62,
          extra_html=f'<div id="t1-voto" style="position:absolute;left:760px;top:900px;width:200px;height:200px;border-radius:50%;background:{AZA};color:#fff;display:flex;align-items:center;justify-content:center;font-family:Playfair Display,serif;font-weight:800;font-size:130px;box-shadow:0 14px 40px rgba(0,0,0,.2);">A</div>',
          extra_js=f'tl.fromTo("#t1-voto",{{scale:0,rotation:-20}},{{scale:1,rotation:0,duration:0.35,ease:"back.out(2.4)"}},{t(28)-8.7:.2f});')

# 3. você escolhe (12.6 – 18.95)
ini, fim = 12.6, 18.95
d = add("voto", ini, fim)
wh, wj = wipe("voto", CREME)
cena("voto", d, f"""
  .bg{{background:#fff;}}
  .titulo{{top:200px;font-size:84px;}}
  .op{{height:440px;}}
  #voto-cont{{position:absolute;left:390px;top:960px;width:300px;height:300px;border-radius:50%;background:var(--laranja);color:#fff;display:flex;align-items:center;justify-content:center;
             font-family:'Playfair Display',serif;font-weight:800;font-size:200px;box-shadow:0 14px 40px rgba(0,0,0,.2);}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="voto-t">Qual segura melhor o <em>açúcar no sangue</em> depois de comer?</h1>
  {opcoes("voto", 520)}
  <div id="voto-cont">3</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#voto-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(38)-ini:.2f});
  tl.fromTo(["#voto-a","#voto-b"],{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.35,stagger:0.12,ease:"back.out(1.6)"}},0.3);
  tl.fromTo("#voto-cont",{{scale:0}},{{scale:1,duration:0.3,ease:"back.out(2.4)"}},{t(48)-ini:.2f});
  tl.set("#voto-cont",{{textContent:"2"}},{t(48)-ini+0.6:.2f});
  tl.set("#voto-cont",{{textContent:"1"}},{t(48)-ini+1.2:.2f});
  tl.set("#voto-cont",{{textContent:"?"}},{t(48)-ini+1.8:.2f});
  tl.to("#voto-cont",{{scale:1.12,duration:0.12,yoyo:true,repeat:5}},{t(48)-ini+0.5:.2f});
""")

# 4. pistas (18.95 – 28.6)
ini, fim = 18.95, 28.6
d = add("pistas", ini, fim)
wh, wj = wipe("pistas", BRANCO)
cena("pistas", d, f"""
  .bg{{background:#EEF0EA;}}
  .titulo{{top:300px;}}
  #pistas-1{{position:absolute;left:80px;top:500px;width:920px;padding:26px 34px;border-radius:28px;background:#fff;font-weight:900;font-size:44px;display:flex;align-items:center;justify-content:space-between;}}
  #pistas-1 b{{font-family:'Playfair Display',serif;font-size:66px;}}
  #pistas-2{{position:absolute;left:80px;top:700px;width:920px;padding:26px 34px;border-radius:28px;background:#fff;font-weight:900;font-size:40px;}}
  #pistas-musc{{position:absolute;left:420px;top:860px;font-size:150px;}}
  .gota{{position:absolute;top:900px;font-size:60px;}}
""", f"""
  <div class="bg"></div>
  <div class="placar" id="pistas-pl"><span>🔎 PISTAS</span><span id="pistas-n">0/2</span></div>
  <h1 class="titulo" id="pistas-t">As <em>pistas</em></h1>
  <div id="pistas-1"><span style="color:{AZA}">A: <b>30 min</b></span><span>=</span><span style="color:{VB}">B: <b>30 min</b></span></div>
  <div id="pistas-2">💪 depois de comer, o músculo puxa açúcar do sangue… <span style="color:var(--laranja)">só enquanto se mexe</span></div>
  <div id="pistas-musc">💪</div>
  {''.join(f'<div class="gota" id="pistas-g{i}" style="left:{140+i*130}px">🩸</div>' for i in range(3))}
  {wh}
""", f"""
  {wj}
  tl.fromTo("#pistas-pl",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:0.3}},0.1);
  tl.fromTo("#pistas-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.2);
  tl.fromTo("#pistas-1",{{opacity:0,x:-100}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(55)-ini:.2f});
  tl.set("#pistas-n",{{textContent:"1/2"}},{t(55)-ini:.2f});
  tl.fromTo("#pistas-2",{{opacity:0,x:-100}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(68)-ini:.2f});
  tl.set("#pistas-n",{{textContent:"2/2"}},{t(68)-ini:.2f});
  tl.fromTo("#pistas-musc",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2)"}},{t(72)-ini:.2f});
  {' '.join(f'tl.fromTo("#pistas-g{i}",{{opacity:0,x:0}},{{opacity:1,x:{300-i*130},scale:0.4,duration:0.8,ease:"power2.in"}},{t(73)-ini+i*0.3:.2f});tl.to("#pistas-g{i}",{{opacity:0,duration:0.1}},{t(73)-ini+i*0.3+0.8:.2f});' for i in range(3))}
  tl.fromTo("#pistas-musc",{{rotation:-8}},{{rotation:8,duration:0.15,yoyo:true,repeat:5}},{t(80)-ini:.2f});
""")

# 5. VIRADA: resposta B (28.6 – 44.15)
ini, fim = 28.6, 44.15
d = add("virada", ini, fim)
wh, wj = wipe("virada", "#EEF0EA")
cena("virada", d, f"""
  .bg{{background:#fff;}}
  .op{{height:300px;padding-top:16px;font-size:30px;}}
  .op .i{{font-size:50px;}}
  .op .L{{width:90px;height:90px;font-size:60px;margin-bottom:8px;}}
  #virada-selo{{left:640px;top:200px;color:{VB};border-color:{VB};font-size:60px;}}
  .est{{position:absolute;left:80px;width:920px;padding:22px 32px;border-radius:26px;background:#EEF0EA;font-weight:900;font-size:38px;}}
  .est .q{{font-size:28px;letter-spacing:.06em;color:var(--laranja);margin-bottom:6px;}}
  .est b{{font-family:'Playfair Display',serif;font-size:64px;color:{VB};}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="virada-t" style="top:200px">Resposta: <em>B</em></h1>
  <div class="selo" id="virada-selo">✓ B</div>
  <div class="op" id="virada-a" style="left:80px;top:400px"><div class="L" style="background:{AZA}">A</div><span class="i">🚶‍♂️🪑</span>tudo de uma vez</div>
  <div class="op" id="virada-b" style="left:560px;top:400px"><div class="L" style="background:{VB}">B</div><span class="i">⏱️🚶</span>a cada 30 min</div>
  <div class="est" id="virada-e1" style="top:740px"><div class="q">ESTUDO 1 · 70 ADULTOS (Peddie et al., AJCN 2013)</div>pausas baixaram mais o açúcar e a insulina que a caminhada de uma vez</div>
  <div class="est" id="virada-e2" style="top:740px"><div class="q">ESTUDO 2 · Duran et al., Med Sci Sports Exerc 2023</div>5 min andando a cada 30 min: pico de açúcar <b>−<span id="virada-pc">0</span>%</b></div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#virada-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(84)-ini:.2f});
  tl.fromTo(["#virada-a","#virada-b"],{{opacity:0}},{{opacity:1,duration:0.3}},0.1);
  tl.to("#virada-a",{{opacity:0.35,scale:0.92,duration:0.4}},{t(85)-ini:.2f});
  tl.to("#virada-b",{{scale:1.06,boxShadow:"0 0 0 8px #2F483A",duration:0.4,ease:"back.out(2)"}},{t(85)-ini:.2f});
  tl.fromTo("#virada-selo",{{opacity:0,scale:2.4,rotation:-14}},{{opacity:1,scale:1,rotation:-6,duration:0.22,ease:"power4.in"}},{t(85)-ini+0.1:.2f});
  tl.fromTo("#root",{{x:0}},{{x:10,duration:0.04,yoyo:true,repeat:5,ease:"none"}},{t(85)-ini+0.32:.2f});
  tl.fromTo("#virada-e1",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.35,ease:"back.out(1.6)"}},{t(87)-ini:.2f});
  tl.to("#virada-e1",{{opacity:0,y:-30,duration:0.3}},{t(114)-ini-0.2:.2f});
  tl.fromTo("#virada-e2",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.35,ease:"back.out(1.6)"}},{t(114)-ini+0.1:.2f});
  {contador("#virada-pc", 0, 58, t(125)-ini, 1.0)}
""")

# 6. ressalva (44.15 – 49.3)
ini, fim = 44.15, 49.3
d = add("ressalva", ini, fim)
wh, wj = wipe("ressalva", BRANCO)
cena("ressalva", d, f"""
  .bg{{background:var(--pessego);}}
  #ressalva-r{{position:absolute;left:80px;top:880px;width:920px;text-align:center;font-weight:900;font-size:46px;color:{VB};}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="ressalva-t">Mas treinar <em>continua valendo</em></h1>
  <div class="chip" id="ressalva-a" style="top:520px"><span class="i">❤️</span>coração</div>
  <div class="chip" id="ressalva-b" style="top:660px"><span class="i">💪</span>músculos</div>
  <div id="ressalva-r">A + B: uma coisa não substitui a outra 🤝</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#ressalva-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.15);
  tl.fromTo("#ressalva-a",{{opacity:0,x:-100}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(140)-ini:.2f});
  tl.fromTo("#ressalva-b",{{opacity:0,x:-100}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(143)-ini:.2f});
  tl.fromTo("#ressalva-r",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35}},{t(143)-ini+0.3:.2f});
""")

# 7. resumo (49.3 – 56.15)
ini, fim = 49.3, 56.15
d = add("resumo", ini, fim)
wh, wj = wipe("resumo", PESSEGO)
txt = "Errei! Treino é ótimo, mas não compensa nove horas sentado. O segredo é levantar de meia em meia hora."
cena("resumo", d, """
  .bg{background:var(--creme);}
  .balao .txt{font-size:54px;}
""", f"""
  <div class="bg"></div>
  <div class="balao" id="resumo-balao"><div class="rot">💡 O QUE O TITO ENTENDEU</div>
    <div class="txt">{palavras_html("resumo", txt, 0, (13, 14, 15, 16, 17, 18))}</div><div class="rabo"></div></div>
  <div class="tito-grande" id="resumo-tito">{tito_svg("resumo", bracos="acena")}</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#resumo-balao",{{opacity:0,y:30,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"back.out(1.6)"}},0.12);
  tl.fromTo("#resumo-tito",{{opacity:0,y:120}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.4)"}},0.05);
  {palavras_js("resumo", txt, ini, 49.48, 55.9)}
  {fala_js("resumo", round(49.48 - ini, 2), round(55.9 - ini, 2))}
""")

# 8. resposta + eco (56.15 – 60.25)
ini, fim = 56.15, 60.25
d = add("resposta", ini, fim)
wh, wj = wipe("resposta", CREME)
cena("resposta", d, f"""
  .bg{{background:{MOST};}}
  .titulo{{color:#1F3328;top:260px;font-size:96px;}}
  #resposta-B{{position:absolute;left:390px;top:620px;width:300px;height:300px;border-radius:50%;background:{VB};color:#fff;display:flex;align-items:center;justify-content:center;
               font-family:'Playfair Display',serif;font-weight:800;font-size:200px;box-shadow:0 14px 40px rgba(0,0,0,.2);}}
  #resposta-img{{left:300px;top:960px;width:480px;height:330px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="resposta-t">A ou B? Pro açúcar depois das refeições:</h1>
  <div id="resposta-B">B</div>
  <div class="img" id="resposta-img"><img src="assets/tito-levanta.png"></div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#resposta-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.12);
  tl.fromTo("#resposta-B",{{scale:0,rotation:-30}},{{scale:1,rotation:0,duration:0.4,ease:"back.out(2.4)"}},{t(180)-ini-0.05:.2f});
  tl.fromTo("#resposta-img",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:0.4}},0.3);
""")

# 9. CTA (60.25 – fim)
ini, fim = 60.25, TOTAL
d = add("cta", ini, fim)
wh, wj = wipe("cta", CREME)
src4 = (SCR / "build_cafe.py").read_text()
cta_src = src4[src4.index('cena("cta", d, """'):src4.index("# ---------- legendas do narrador")]
cta_src = (cta_src
    .replace(".bg{background:var(--laranja);}", ".bg{background:var(--verde);}\n  #cta-tito{filter:drop-shadow(0 0 2px #FDF3ED) drop-shadow(0 0 2px #FDF3ED);}")  # Tito não some no fundo
    .replace("Manda pra quem diz que <em>café faz mal</em>", "Manda pra quem vive <em>na cadeira</em>")
    .replace('"☕ 3 xícaras!"', "acertou? A ou B")
    .replace("#cta-eco{position:absolute;inset:0;background:var(--mostarda);}", "#cta-eco{position:absolute;inset:0;background:#E2B04A;}")
    .replace("#cta-eco .titulo{color:var(--verde);top:240px;font-size:128px;}", "#cta-eco .titulo{color:#1F3328;top:300px;font-size:110px;}")
    .replace("#cta-eco .titulo em{color:#8E3412;}", "#cta-eco .titulo em{color:#7A2E10;}")
    .replace('<div id="cta-eco-c"></div><h1 class="titulo">Café <em>faz mal?</em></h1>', '<h1 class="titulo">Levantar a cada 30 min <em>funciona?</em></h1>')
    .replace("assets/tito-cafe.png", "assets/tito-levanta.png")
    .replace("#cta-eco-img{left:300px;top:500px;width:480px;height:570px;}", "#cta-eco-img{left:140px;top:820px;width:800px;height:560px;}")
    .replace("t(165)-ini-0.05", "t(198)-ini-0.1").replace("t(165)-ini+0.45", "t(199)-ini+0.15")
    .replace("TOTAL-ini-2.1", "TOTAL-ini-2.3")
    .replace("t(165)", "t(199)").replace("t(159)", "t(194)").replace("t(158)", "t(193)")
    .replace("t(148)", "t(183)").replace("t(149)", "t(184)").replace("t(152)", "t(188)"))
exec(cta_src)

GRUPOS = [
    ("Duas opções pro seu *dia de trabalho*.", 0, 8), ("*A*: meia hora de caminhada", 8, 5), ("e depois *9 horas sentado*.", 13, 5),
    ("*B*: dois minutinhos de caminhada", 18, 5), ("*a cada meia hora*.", 23, 4),
    ("E você? Qual segura melhor", 36, 5), ("o *açúcar no sangue*", 41, 4), ("depois das refeições?", 45, 3), ("*Escolhe agora: A ou B.*", 48, 5),
    ("*Pista 1*: nas duas,", 53, 4), ("o total de caminhada é *o mesmo*, meia hora.", 57, 9),
    ("*Pista 2*: depois de comer,", 66, 5), ("os músculos *puxam o açúcar* do sangue,", 71, 7), ("mas *só enquanto estão se mexendo*.", 78, 6),
    ("*Resposta: B.*", 84, 2), ("Num estudo com *70 adultos*,", 86, 5), ("as *pausas a cada meia hora*", 91, 6), ("baixaram *mais o açúcar e a insulina*", 97, 7),
    ("depois das refeições", 104, 3), ("do que a caminhada *de uma vez*.", 107, 7),
    ("E outro estudo viu:", 114, 4), ("*5 minutos andando* a cada meia hora", 118, 7), ("cortaram o pico de açúcar *em mais da metade*.", 125, 9),
    ("Mas *treinar continua valendo*", 134, 4), ("pro coração e pros músculos.", 138, 7), ("Uma coisa *não substitui a outra*.", 145, 6),
    ("Então, *A ou B?*", 170, 4), ("Pro açúcar depois das refeições, *B*.", 174, 7),
    ("*Isso aí.*", 181, 2), ("Manda pra quem passa o dia *grudado na cadeira*.", 183, 9), ("E *curte*,", 192, 2),
    ("*comenta se você acertou*", 194, 4), ("e *segue pra mais!*", 198, 4),
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
