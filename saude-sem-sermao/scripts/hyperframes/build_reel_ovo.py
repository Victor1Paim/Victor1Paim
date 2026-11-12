#!/usr/bin/env python3
"""Reel animado de receita com fotos realistas: "Ovo aumenta o colesterol? + omelete de forno"."""
import json, math, re, shutil
from pathlib import Path

SCR = Path("/tmp/claude-0/-home-user-Victor1Paim/bc508778-dc0e-5c3d-a4a6-a9dce8035bd2/scratchpad")
POST = Path("/home/user/Victor1Paim/saude-sem-sermao/producoes/reels-receitas/ovo")
V = POST / "video"
(V / "compositions").mkdir(parents=True, exist_ok=True)
for f in ["hyperframes.json", "package.json", "meta.json"]:
    (V / f).write_text((SCR / "hfblank" / f).read_text().replace('"hfblank"', '"saude-sem-sermao-reel-ovo"'))
shutil.copy(POST / "dialogo.mp3", V / "assets/voz.mp3")

W, H = 1080, 1920
TOTAL = 57.0
words = json.loads((POST / "conferencia/dialogo.palavras.json").read_text())
CENAS = []
src = (SCR / "build_sono.py").read_text()
exec(src[src.index("# ---------- paleta e base"):src.index("# ---------- 1. capa")])
src2 = (SCR / "build_alongar.py").read_text()
exec(src2[src2.index("BASE_CSS += "):src2.index("VERDE, CREME, BRANCO")])
BASE_CSS += """
  .foto{position:absolute;inset:0;overflow:hidden;}
  .foto img{position:absolute;left:-100px;top:0;width:1280px;height:1920px;object-fit:cover;}
  .sombra-top{position:absolute;left:0;right:0;top:0;height:900px;background:linear-gradient(rgba(18,22,18,.78),rgba(18,22,18,0));}
  .sombra-base{position:absolute;left:0;right:0;bottom:0;height:900px;background:linear-gradient(rgba(18,22,18,0),rgba(18,22,18,.6));}
  .chip{position:absolute;padding:12px 28px;border-radius:999px;font-weight:900;font-size:44px;color:#fff;box-shadow:0 10px 30px rgba(0,0,0,.25);}
  .passo{position:absolute;left:80px;top:250px;width:120px;height:120px;border-radius:50%;background:var(--laranja);color:#fff;
         font-family:'Playfair Display',serif;font-weight:700;font-size:80px;display:flex;align-items:center;justify-content:center;box-shadow:0 10px 30px rgba(0,0,0,.3);}
  .tit-foto{position:absolute;left:80px;width:920px;font-family:'Playfair Display',serif;font-weight:800;font-size:100px;line-height:1.02;color:#fff;text-shadow:0 4px 24px rgba(0,0,0,.4);}
  .tit-foto em{font-style:italic;color:#F2C46A;}
"""
LARANJA, CREME = "#D45F2B", "#FDF3ED"


def foto_html(cid, nome, extra=""):
    return f'<div class="foto"><img id="{cid}-img" src="assets/{nome}.jpg"></div>{extra}'


def kb_js(cid, d, de=1.0, ate=1.12, x=0):
    return f'tl.fromTo("#{cid}-img",{{scale:{de},x:0,transformOrigin:"50% 50%"}},{{scale:{ate},x:{x},duration:{d:.2f},ease:"none"}},0);'


def tito_foto(cid, ini, fim, txt, fala_ini, fala_fim, foto, rot="💬 PERGUNTA DO TITO", destaque=(), olhos="normal", bracos="baixo", tam=60):
    d = add(cid, ini, fim)
    wh, wj = wipe(cid, "#1c211c")
    cena(cid, d, f"""
  .balao .txt{{font-size:{tam}px;}}
""", f"""
  <div class="foto"><img id="{cid}-img" src="assets/{foto}-desfoque.jpg"></div>
  <div class="balao" id="{cid}-balao"><div class="rot">{rot}</div>
    <div class="txt">{palavras_html(cid, txt, 0, destaque)}</div><div class="rabo"></div></div>
  <div class="tito-grande" id="{cid}-tito">{tito_svg(cid, olhos=olhos, bracos=bracos)}</div>
  {wh}
""", f"""
  {wj}
  {kb_js(cid, d, 1.05, 1.12)}
  tl.fromTo("#{cid}-balao",{{opacity:0,y:30,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.3,ease:"back.out(1.6)"}},0.12);
  tl.fromTo("#{cid}-tito",{{opacity:0,y:120}},{{opacity:1,y:0,duration:0.4,ease:"back.out(1.4)"}},0.05);
  {palavras_js(cid, txt, ini, fala_ini, fala_fim)}
  {fala_js(cid, round(fala_ini - ini, 2), round(fala_fim - ini, 2))}
""")


# 1. capa (0 – 5.2)
ini, fim = 0, 5.2
d = add("capa", ini, fim)
cena("capa", d, """
  #capa-tag{position:absolute;left:80px;top:220px;padding:8px 24px;border-radius:999px;background:var(--laranja);color:#fff;font-weight:900;font-size:34px;letter-spacing:.06em;}
  #capa-nao{left:80px;top:640px;background:var(--verde);}
""", f"""
  {foto_html("capa", "capa", '<div class="sombra-top"></div>')}
  <div id="capa-tag">MITO OU VERDADE?</div>
  <h1 class="tit-foto" style="top:290px">Ovo aumenta o <em>colesterol?</em></h1>
  <div class="chip" id="capa-nao">não do jeito que te contaram</div>
""", f"""
  {kb_js("capa", d, 1.0, 1.14, -30)}
  tl.fromTo("#capa-nao",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.2)"}},{t(9):.2f});
""")

# 2. Tito: cheio de colesterol? (5.2 – 7.35)
tito_foto("t1", 5.2, 7.35, "Mas ovo não é cheio de colesterol?", 5.44, 7.2, "capa", destaque=(5,), olhos="duvida")

# 3. ciência (7.35 – 16.45)
ini, fim = 7.35, 16.45
d = add("ciencia", ini, fim)
wh, wj = wipe("ciencia", "#1c211c")
dias = "STQQSSD"
ovos = "".join(f'<div class="dia" id="ciencia-d{i}" style="left:{80+i*132}px"><div class="ovo"></div><div class="l">{c}</div></div>' for i, c in enumerate(dias))
cena("ciencia", d, """
  .bg{background:#fff;}
  .tag{background:#5F6E52;color:#fff;}
  #ciencia-n{position:absolute;left:80px;top:470px;font-family:'Playfair Display',serif;font-weight:700;font-size:120px;color:var(--laranja);line-height:1;}
  #ciencia-nl{position:absolute;left:84px;top:595px;font-weight:900;font-size:38px;color:#6b6460;}
  .dia{position:absolute;top:670px;width:110px;text-align:center;}
  .dia .ovo{width:84px;height:104px;margin:0 auto;border-radius:50% 50% 46% 46%/60% 60% 40% 40%;background:#F6EBDD;border:5px solid #E2C9A6;}
  .dia .l{font-weight:900;font-size:34px;color:#6b6460;margin-top:8px;}
  .rot{position:absolute;left:80px;font-weight:900;font-size:36px;}
  .barra{position:absolute;left:80px;width:760px;height:66px;border-radius:18px;transform-origin:0% 50%;}
  .pct{position:absolute;left:870px;font-weight:900;font-size:42px;}
  #ciencia-igual{position:absolute;left:600px;top:845px;padding:10px 26px;border-radius:999px;background:var(--verde);color:#fff;font-weight:900;font-size:40px;}
  .fonte{top:1120px;}
""", f"""
  <div class="bg"></div>
  <div class="tag" id="ciencia-tag">✓ CIÊNCIA</div>
  <h1 class="titulo" id="ciencia-t">1 ovo por dia: <em>sem aumento</em> de risco</h1>
  <div id="ciencia-n">0</div><div id="ciencia-nl">pessoas analisadas</div>
  {ovos}
  <div class="rot" style="top:860px">sem ovo</div><div class="barra" id="ciencia-b0" style="top:905px;background:#8C8580"></div><div class="pct" style="top:913px">100</div>
  <div class="rot" style="top:985px">até 1 ovo/dia</div><div class="barra" id="ciencia-b1" style="top:1030px;background:var(--laranja)"></div><div class="pct" style="top:1038px;color:var(--laranja)">98</div>
  <div id="ciencia-igual">≈ igual</div>
  <div class="fonte" id="ciencia-fonte">Fonte: Drouin-Chartier et al., BMJ, 2020</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#ciencia-tag",{{opacity:0,y:-10}},{{opacity:1,y:0,duration:0.3}},0.3);
  tl.fromTo("#ciencia-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.3);
  tl.fromTo("#ciencia-n",{{opacity:0}},{{opacity:1,duration:0.2}},{t(29)-ini:.2f});
  {contador("#ciencia-n", 0, 1720108, t(29)-ini, 1.4, "milhar")}
  tl.fromTo("#ciencia-nl",{{opacity:0}},{{opacity:1,duration:0.3}},{t(33)-ini:.2f});
  tl.fromTo("#ciencia-fonte",{{opacity:0}},{{opacity:1,duration:0.4}},{t(29)-ini:.2f});
  {' '.join(f'tl.fromTo("#ciencia-d{i}",{{opacity:0,y:30,scale:0.6}},{{opacity:1,y:0,scale:1,duration:0.25,ease:"back.out(2.4)"}},{t(39)-ini+i*0.09:.2f});' for i in range(7))}
  tl.fromTo("#ciencia-b0",{{scaleX:0}},{{scaleX:1,duration:0.5,ease:"power2.out"}},{t(45)-ini-0.2:.2f});
  tl.fromTo("#ciencia-b1",{{scaleX:0}},{{scaleX:0.98,duration:0.6,ease:"power2.out"}},{t(45)-ini:.2f});
  tl.fromTo("#ciencia-igual",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.4)"}},{t(47)-ini:.2f});
""")

# 4. conjunto (16.45 – 21.05)
ini, fim = 16.45, 21.05
d = add("conjunto", ini, fim)
wh, wj = wipe("conjunto", "#FFFFFF")
cena("conjunto", d, """
  .bg{background:var(--pessego);}
  #conjunto-prato{position:absolute;left:290px;top:520px;width:500px;height:500px;border-radius:50%;background:#fff;border:14px solid #EADFD4;}
  .fatia{position:absolute;border-radius:50%;}
  #conjunto-ovo{position:absolute;left:470px;top:700px;width:140px;height:170px;border-radius:50% 50% 46% 46%/60% 60% 40% 40%;background:#F6EBDD;border:6px solid #E2C9A6;}
  .item{position:absolute;padding:10px 24px;border-radius:999px;background:#fff;font-weight:900;font-size:34px;box-shadow:0 8px 24px rgba(80,40,20,.12);}
  #conjunto-rot{position:absolute;left:80px;top:1060px;width:920px;text-align:center;font-weight:900;font-size:40px;color:var(--verde);}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="conjunto-t">Conta mais o <em>conjunto</em></h1>
  <div id="conjunto-prato"></div>
  <div id="conjunto-ovo"></div>
  <div class="item" id="conjunto-i0" style="left:90px;top:540px">🥩 gordura saturada</div>
  <div class="item" id="conjunto-i1" style="left:640px;top:560px">🍟 ultraprocessados</div>
  <div class="item" id="conjunto-i2" style="left:110px;top:900px">🥗 fibras</div>
  <div class="item" id="conjunto-i3" style="left:700px;top:930px">🏃 seu corpo</div>
  <div id="conjunto-rot">o ovo é só uma parte do prato</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#conjunto-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.3);
  tl.fromTo("#conjunto-prato",{{scale:0}},{{scale:1,duration:0.45,ease:"back.out(1.6)"}},0.4);
  tl.fromTo("#conjunto-ovo",{{scale:0}},{{scale:1,duration:0.35,ease:"back.out(2.4)"}},0.7);
  {' '.join(f'tl.fromTo("#conjunto-i{i}",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2.2)"}},{t(55)-ini+i*0.25:.2f});' for i in range(4))}
  tl.to("#conjunto-ovo",{{scale:0.7,duration:0.5,ease:"power2.inOut"}},{t(60)-ini:.2f});
  tl.fromTo("#conjunto-rot",{{opacity:0}},{{opacity:1,duration:0.3}},{t(52)-ini:.2f});
""")

# 5. Tito: me ensina uma receita (21.05 – 23.3)
tito_foto("t2", 21.05, 23.3, "Então me ensina uma receita!", 21.22, 22.9, "ingredientes", destaque=(4,), bracos="acena", tam=66)

# 6. ingredientes + passo 1 (23.3 – 30.6)
ini, fim = 23.3, 30.6
d = add("passo1", ini, fim)
wh, wj = wipe("passo1", "#1c211c")
chips = [("4 ovos", 72, "#D45F2B", 400), ("sal · pimenta · orégano", 75, "#5F6E52", 490), ("tomate", 80, "#C2563A", 580), ("cebola", 81, "#8A6A1F", 670), ("espinafre", 83, "#2F483A", 760)]
cena("passo1", d, """
  #passo1-b{opacity:0;}
""", f"""
  <div class="foto"><img id="passo1-img" src="assets/ingredientes.jpg"></div>
  <div class="foto" id="passo1-b"><img id="passo1-img2" src="assets/batendo.jpg"></div>
  <div class="sombra-top"></div>
  <h1 class="tit-foto" id="passo1-t" style="top:230px;font-size:96px">Omelete <em>de forno</em></h1>
  <div class="passo" id="passo1-n" style="top:240px;opacity:0">1</div>
  {''.join(f'<div class="chip" id="passo1-c{i}" style="left:{80 if i%2==0 else 200}px;top:{y}px;background:{c}">{txt}</div>' for i,(txt,_,c,y) in enumerate(chips))}
  {wh}
""", f"""
  {wj}
  {kb_js("passo1", 2.0, 1.02, 1.1)}
  tl.fromTo("#passo1-img2",{{scale:1.05}},{{scale:1.14,duration:{d-1.2:.2f},ease:"none"}},1.2);
  tl.fromTo("#passo1-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.1);
  tl.to("#passo1-b",{{opacity:1,duration:0.5,ease:"power2.inOut"}},{t(71)-ini-0.3:.2f});
  tl.to("#passo1-t",{{opacity:0,duration:0.3}},{t(71)-ini-0.3:.2f});
  tl.fromTo("#passo1-n",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.4)"}},{t(71)-ini:.2f});
  {' '.join(f'tl.fromTo("#passo1-c{i}",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.3,ease:"back.out(1.8)"}},{t(k)-ini:.2f});' for i,(_,k,_,_) in enumerate(chips))}
""".replace('top:{y}px', 'top:{y}px'))

# 7. passo 2: forno (30.6 – 36.75)
ini, fim = 30.6, 36.75
d = add("forno", ini, fim)
wh, wj = wipe("forno", "#1c211c")
cena("forno", d, """
  #forno-temp{left:80px;top:420px;background:var(--laranja);font-size:64px;}
  #forno-rel{position:absolute;left:640px;top:380px;width:240px;height:240px;}
  #forno-min{position:absolute;left:640px;top:470px;width:240px;text-align:center;font-family:'Playfair Display',serif;font-weight:700;font-size:64px;color:#fff;}
  #forno-c1{left:200px;top:250px;background:#5F6E52;}
  #forno-c2{left:200px;top:330px;background:#8A6A1F;}
""", f"""
  {foto_html("forno", "forma", '<div class="sombra-top"></div>')}
  <div class="passo" id="forno-n">2</div>
  <div class="chip" id="forno-c1">forma untada</div>
  <div class="chip" id="forno-c2">+ queijo por cima</div>
  <div class="chip" id="forno-temp">🔥 180 °C</div>
  <svg id="forno-rel" viewBox="0 0 100 100"><circle cx="50" cy="50" r="42" fill="rgba(0,0,0,.35)" stroke="rgba(255,255,255,.35)" stroke-width="8"/>
    <circle id="forno-arco" cx="50" cy="50" r="42" fill="none" stroke="#F2C46A" stroke-width="8" stroke-linecap="butt" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" transform="rotate(-90 50 50)"/></svg>
  <div id="forno-min">0 min</div>
  {wh}
""", f"""
  {wj}
  {kb_js("forno", d, 1.0, 1.12, 20)}
  tl.fromTo("#forno-n",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.4)"}},0.3);
  tl.fromTo("#forno-c1",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.3,ease:"back.out(1.8)"}},{t(86)-ini:.2f});
  tl.fromTo("#forno-c2",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.3,ease:"back.out(1.8)"}},{t(90)-ini:.2f});
  tl.fromTo("#forno-temp",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.4)"}},{t(94)-ini:.2f});
  tl.fromTo(["#forno-rel","#forno-min"],{{opacity:0}},{{opacity:1,duration:0.3}},{t(98)-ini-0.2:.2f});
  tl.fromTo("#forno-arco",{{attr:{{"stroke-dashoffset":1}}}},{{attr:{{"stroke-dashoffset":0}},duration:1.0,ease:"power2.out"}},{t(98)-ini:.2f});
  (function(){{const o={{v:0}};const el=document.querySelector("#forno-min");
    tl.fromTo(o,{{v:0}},{{v:20,duration:1.0,ease:"power2.out",onUpdate:()=>{{el.textContent=Math.round(o.v)+" min";}}}},{t(98)-ini:.2f});}})();
""")

# 8. Tito: colesterol alto? (36.75 – 38.7)
tito_foto("t3", 36.75, 38.7, "E se eu tiver colesterol alto?", 36.78, 38.6, "forma", destaque=(4, 5), olhos="duvida", tam=66)

# 9. médico (38.7 – 42.25)
ini, fim = 38.7, 42.25
d = add("medico", ini, fim)
wh, wj = wipe("medico", "#1c211c")
cena("medico", d, """
  .bg{background:#EEF0EA;}
  .card2{position:absolute;left:80px;width:920px;background:#fff;border-radius:30px;box-shadow:0 14px 40px rgba(40,60,40,.12);
         display:flex;align-items:center;gap:26px;padding:34px 40px;font-weight:900;font-size:46px;line-height:1.2;}
  .card2 .e{font-size:80px;}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="medico-t">Colesterol <em>alto</em>?</h1>
  <div class="card2" id="medico-c" style="top:470px"><span class="e">🩺</span>combine a quantidade de ovos com seu médico ou nutricionista</div>
  <div class="tito-mini" id="medico-tito" style="top:900px;right:120px;width:340px;height:380px">{tito_svg("medico", bracos="acena")}</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#medico-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.3);
  tl.fromTo("#medico-c",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:0.4,ease:"back.out(1.6)"}},{t(107)-ini:.2f});
  tl.fromTo("#medico-tito",{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.4,ease:"back.out(1.5)"}},0.5);
""")

# 10. resumo (42.25 – 47.4)
tito_foto("resumo", 42.25, 47.4, "Entendi! Ovo não é vilão, e essa omelete rende o café da manhã da semana.", 42.36, 47.2, "capa",
          rot="💡 O QUE O TITO ENTENDEU", destaque=(1, 2, 3, 4, 7, 8, 13), bracos="acena", tam=56)

# 11. CTA (47.4 – fim)
ini, fim = 47.4, TOTAL
d = add("cta", ini, fim)
wh, wj = wipe("cta", "#1c211c")
cena("cta", d, """
  .bg{background:var(--verde);}
  #cta-tito{filter:drop-shadow(0 0 2px #FDF3ED) drop-shadow(0 0 2px #FDF3ED);}
  .titulo{color:#fff;top:220px;}
  .titulo em{color:var(--creme2);}
  #cta-card{position:absolute;left:150px;top:470px;width:780px;height:300px;background:#fff;border-radius:36px;box-shadow:0 24px 60px rgba(80,30,10,.25);}
  #cta-rot{position:absolute;left:40px;top:26px;font-weight:900;font-size:34px;color:#6b6460;}
  .av{position:absolute;top:90px;width:150px;text-align:center;font-weight:900;font-size:30px;color:#4a4440;}
  .av .c{width:104px;height:104px;margin:0 auto 10px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:44px;color:#fff;}
  #cta-av0 .c{background:#5F6E52;} #cta-av1 .c{background:var(--verde);} #cta-av2 .c{background:var(--mostarda);color:#2B2B2B;} #cta-av3 .c{background:#B5481F;}
  #cta-check{position:absolute;left:62px;top:84px;width:120px;height:120px;border-radius:50%;background:rgba(47,72,58,.92);color:#fff;font-size:64px;font-weight:900;display:flex;align-items:center;justify-content:center;}
  #cta-aviao{position:absolute;left:820px;top:1080px;width:140px;height:140px;}
  .acao{position:absolute;top:820px;width:290px;height:200px;background:#fff;border-radius:30px;box-shadow:0 18px 44px rgba(80,30,10,.22);
        display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;font-weight:900;font-size:34px;color:#2B2B2B;}
  .acao .i{font-size:72px;line-height:1;}
  #cta-seg{position:relative;width:220px;height:62px;}
  #cta-seg1,#cta-seg2{position:absolute;inset:0;border-radius:16px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:32px;color:#fff;}
  #cta-seg1{background:var(--laranja);} #cta-seg2{background:var(--verde);opacity:0;}
  #cta-aviso{position:absolute;left:80px;top:1060px;width:920px;text-align:center;font-weight:800;font-size:28px;color:#FDF3ED;}
  #cta-eco{position:absolute;inset:0;}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="cta-t">Manda pra quem tem <em>medo de ovo</em></h1>
  <div id="cta-card" data-layout-allow-overlap><div id="cta-rot">Enviar para…</div>
    <div class="av" id="cta-av0" style="left:30px"><div class="c">A</div>amiga</div>
    <div class="av" id="cta-av1" style="left:215px"><div class="c">M</div>mãe</div>
    <div class="av" id="cta-av2" style="left:400px"><div class="c">J</div>João</div>
    <div class="av" id="cta-av3" style="left:585px"><div class="c">+</div>grupo</div>
    <div id="cta-check">✓</div></div>
  <div class="acao" id="cta-a1" style="left:60px"><span class="i">❤️</span>curte</div>
  <div class="acao" id="cta-a2" style="left:395px"><span class="i">💬</span>"🥕 cenoura!"</div>
  <div class="acao" id="cta-a3" style="left:730px" data-layout-allow-overlap><span class="i">🧡</span><div id="cta-seg"><div id="cta-seg1">Seguir</div><div id="cta-seg2">Seguindo ✓</div></div></div>
  <svg id="cta-aviao" viewBox="0 0 100 100"><path d="M6 46 L94 8 L66 92 L48 60 Z" fill="#fff" stroke="#2B2B2B" stroke-width="5" stroke-linejoin="round"/>
    <path d="M48 60 L94 8" stroke="#2B2B2B" stroke-width="4"/></svg>
  <div id="cta-aviso">Conteúdo educativo, não substitui orientação profissional. Imagens geradas com IA.</div>
  <div class="tito-mini" id="cta-tito" style="top:1360px">{tito_svg("cta", olhos="piscando", bracos="acena")}</div>
  <div id="cta-eco" style="opacity:0"><div class="foto"><img id="cta-eco-img" src="assets/capa.jpg"></div><div class="sombra-top"></div>
    <h1 class="tit-foto" style="top:290px">Ovo aumenta o <em>colesterol?</em></h1></div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#cta-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(133)-ini-0.2:.2f});
  tl.fromTo("#cta-card",{{opacity:0,y:60,scale:0.95}},{{opacity:1,y:0,scale:1,duration:0.45,ease:"back.out(1.5)"}},{t(133)-ini:.2f});
  {' '.join(f'tl.fromTo("#cta-av{i}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.25,ease:"back.out(2)"}},{t(134)-ini+i*0.1:.2f});' for i in range(4))}
  tl.to("#cta-aviao",{{x:-500,y:-500,rotation:-25,scale:0.6,duration:0.8,ease:"power2.in"}},{t(137)-ini:.2f});
  tl.to("#cta-aviao",{{opacity:0,duration:0.1}},{t(137)-ini+0.75:.2f});
  tl.fromTo("#cta-check",{{scale:0}},{{scale:1,duration:0.3,ease:"back.out(2.4)"}},{t(137)-ini+0.8:.2f});
  tl.fromTo("#cta-a1",{{opacity:0,scale:0.4,y:40}},{{opacity:1,scale:1,y:0,duration:0.35,ease:"back.out(2.2)"}},{t(141)-ini-0.05:.2f});
  tl.fromTo("#cta-a2",{{opacity:0,scale:0.4,y:40}},{{opacity:1,scale:1,y:0,duration:0.35,ease:"back.out(2.2)"}},{t(142)-ini-0.05:.2f});
  tl.fromTo("#cta-a3",{{opacity:0,scale:0.4,y:40}},{{opacity:1,scale:1,y:0,duration:0.35,ease:"back.out(2.2)"}},{t(148)-ini-0.05:.2f});
  tl.to("#cta-seg1",{{opacity:0,duration:0.15}},{t(148)-ini+0.45:.2f});
  tl.to("#cta-seg2",{{opacity:1,duration:0.15}},{t(148)-ini+0.45:.2f});
  tl.fromTo("#cta-aviso",{{opacity:0}},{{opacity:1,duration:0.4}},0.6);
  tl.fromTo("#cta-tito",{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.5)"}},0.4);
  tl.fromTo("#cta-braco",{{rotation:-12,transformOrigin:"170px 100px"}},{{rotation:12,duration:0.3,ease:"sine.inOut",yoyo:true,repeat:7}},0.9);
  tl.to(["#cta-t","#cta-card","#cta-a1","#cta-a2","#cta-a3","#cta-aviso","#cta-tito"],{{opacity:0,duration:0.3}},{TOTAL-ini-2.1:.2f});
  tl.fromTo("#cta-eco",{{opacity:0}},{{opacity:1,duration:0.35,ease:"power2.inOut"}},{TOTAL-ini-2.1:.2f});
  tl.fromTo("#cta-eco-img",{{scale:1.0}},{{scale:1.06,duration:2.1,ease:"none"}},{TOTAL-ini-2.1:.2f});
""")

GRUPOS = [
    ("Ovo aumenta o *colesterol?*", 0, 4), ("Pra maioria das pessoas,", 4, 5), ("*não do jeito* que te contaram.", 9, 6),
    ("Tem colesterol, *sim*.", 22, 3), ("Mas uma análise com *1,7 milhão* de pessoas", 25, 9), ("*não viu ligação*", 34, 3),
    ("entre comer *até um ovo por dia*", 37, 7), ("e *doença do coração*.", 44, 4),
    ("O colesterol do sangue", 48, 4), ("depende mais do *conjunto da alimentação*", 52, 6), ("do que do ovo sozinho.", 58, 5),
    ("*Omelete de forno.*", 68, 3), ("Bata *4 ovos*", 71, 3), ("com sal, pimenta e orégano.", 74, 5), ("Junte *tomate, cebola e espinafre*.", 79, 5),
    ("Coloque numa *forma untada*,", 84, 4), ("cubra com *queijo*", 88, 3), ("e asse a *180 graus*", 91, 5), ("por uns *20 minutos*.", 96, 4),
    ("Aí *combine a quantidade*", 106, 4), ("com seu *médico ou nutricionista*.", 110, 5),
    ("*Isso aí.*", 131, 2), ("Manda pra quem *tem medo de ovo*.", 133, 7), ("E *curte*,", 140, 2),
    ("*comenta* qual legume você colocaria", 142, 5), ("e *segue pra mais!*", 147, 4),
]
for txt_, i0, n in GRUPOS:
    print(f"{txt_!r:46} <- {' '.join(w['palavra'] for w in words[i0:i0+n])!r}")
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
