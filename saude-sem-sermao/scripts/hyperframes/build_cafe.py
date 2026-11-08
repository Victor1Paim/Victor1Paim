#!/usr/bin/env python3
"""Projeto HyperFrames: "Café faz mal pro coração?" (Saúde sem Sermão). CTA novo: enviar + curte/comenta/segue."""
import json, math, re, shutil
from pathlib import Path

SCR = Path("/tmp/claude-0/-home-user-Victor1Paim/bc508778-dc0e-5c3d-a4a6-a9dce8035bd2/scratchpad")
POST = Path("/home/user/Victor1Paim/saude-sem-sermao/producoes/cafe-faz-mal")
V = POST / "video"
(V / "compositions").mkdir(parents=True, exist_ok=True)
(V / "assets").mkdir(exist_ok=True)
for f in ["hyperframes.json", "package.json", "meta.json"]:
    (V / f).write_text((SCR / "hfblank" / f).read_text().replace('"hfblank"', '"saude-sem-sermao-cafe"'))
shutil.copy(POST / "dialogo.mp3", V / "assets/voz.mp3")
for n in ["tito-cafe", "tito-palpitacao"]:
    shutil.copy(POST / "imagens" / f"{n}.png", V / "assets" / f"{n}.png")

W, H = 1080, 1920
TOTAL = 60.8
words = json.loads((POST / "conferencia/dialogo.palavras.json").read_text())
CENAS = []
src = (SCR / "build_sono.py").read_text()
exec(src[src.index("# ---------- paleta e base"):src.index("# ---------- 1. capa")])
exec(src[src.index("def cena_tito"):src.index("# ---------- 2. Tito: culpa")])
src2 = (SCR / "build_alongar.py").read_text()
exec(src2[src2.index("BASE_CSS += "):src2.index("VERDE, CREME, BRANCO")])
src3 = (SCR / "build_passos.py").read_text()
VERDE, CREME, BRANCO, LARANJA, PESSEGO, MOSTARDA = "#2F483A", "#FDF3ED", "#FFFFFF", "#D45F2B", "#F7E5DD", "#E2B04A"
exec(src3[src3.index("def tito_fala"):src3.index("# ---------- gráfico de risco")])


def xicaras(pref, n, x0, y0, tam=90, gap=24, cor="#95A185"):
    out = []
    for i in range(n):
        out.append(f'<svg class="xic" id="{pref}-x{i}" style="left:{x0+i*(tam+gap)}px;top:{y0}px;width:{tam}px;height:{tam}px" viewBox="0 0 100 100">'
                   f'<path d="M14 30 H74 V70 Q74 88 56 88 H32 Q14 88 14 70 Z" fill="{cor}" stroke="#2F483A" stroke-width="5"/>'
                   f'<path d="M74 40 Q92 40 92 54 Q92 68 74 66" fill="none" stroke="#2F483A" stroke-width="6"/>'
                   f'<rect x="20" y="34" width="48" height="8" rx="4" fill="#5A3A22"/></svg>')
    return "".join(out)


# ---------- 1. capa (0 – 3.9) ----------
ini, fim = 0, 3.9
d = add("capa", ini, fim)
cena("capa", d, """
  .bg{background:var(--mostarda);}
  .titulo{color:var(--verde);top:240px;font-size:128px;}
  .titulo em{color:#8E3412;}
  #capa-circ{position:absolute;left:240px;top:520px;width:600px;height:600px;border-radius:50%;background:var(--creme2);}
  #capa-img{left:300px;top:500px;width:480px;height:570px;}
  #capa-pill{position:absolute;left:80px;top:1110px;padding:10px 26px;border-radius:999px;background:var(--verde);color:#fff;font-weight:900;font-size:40px;}
  .vapor{position:absolute;width:14px;height:70px;border-radius:7px;background:rgba(255,255,255,.75);}
""", """
  <div class="bg"></div>
  <div id="capa-circ"></div>
  <h1 class="titulo">Café <em>faz mal?</em></h1>
  <div class="img" id="capa-img"><img src="assets/tito-cafe.png"></div>
""", f"""
  tl.fromTo("#capa-img",{{y:0,rotation:0,transformOrigin:"50% 100%"}},{{y:-10,rotation:2,duration:0.6,ease:"sine.inOut",yoyo:true,repeat:5}},0);
""".replace("repeat:2}},0.1)", "repeat:2}},0.1)"))

# ---------- 2. Tito: tomo 3 (3.9 – 7.0) ----------
tito_fala("tres", 3.9, 7.0, "Mas eu tomo 3 por dia, e todo mundo diz que é demais!", 3.96, 6.75, destaque=(3, 4, 5, 12),
          cor_ant=MOSTARDA, extra_html=f'<div style="position:absolute;left:700px;top:640px">{xicaras("tres", 3, 0, 0, 90, 10)}</div>'
          '<style>.xic{position:absolute;}</style>',
          extra_js=" ".join(f'tl.fromTo("#tres-x{i}",{{scale:0}},{{scale:1,duration:0.25,ease:"back.out(2.4)"}},{t(13)-3.9+i*0.12:.2f});' for i in range(3)))

# ---------- 3. a revisão (7.0 – 18.7) ----------
ini, fim = 7.0, 18.7
d = add("revisao", ini, fim)
wh, wj = wipe("revisao", CREME)
cena("revisao", d, """
  .bg{background:#fff;}
  .tag{background:#5F6E52;color:#fff;}
  .xic{position:absolute;}
  #revisao-n{position:absolute;left:80px;top:410px;font-family:'Playfair Display',serif;font-weight:700;font-size:110px;color:var(--laranja);line-height:1;}
  #revisao-nl{position:absolute;left:84px;top:528px;font-weight:900;font-size:38px;color:#6b6460;}
  #revisao-faixa{position:absolute;left:316px;top:620px;width:232px;height:130px;border-radius:24px;background:rgba(226,176,74,.35);transform-origin:50% 50%;}
  #revisao-fl{position:absolute;left:316px;top:760px;width:232px;text-align:center;font-weight:900;font-size:32px;color:#8a6a1f;}
  .rot{position:absolute;left:80px;font-weight:900;font-size:34px;}
  .trilho{position:absolute;left:80px;width:800px;height:64px;border-radius:18px;background:#F2ECE2;}
  .barra{position:absolute;left:80px;width:800px;height:64px;border-radius:18px;transform-origin:0% 50%;}
  .pct{position:absolute;left:900px;font-weight:900;font-size:44px;}
  #revisao-menor{position:absolute;left:560px;top:420px;padding:12px 28px;border-radius:999px;background:var(--verde);color:#fff;font-weight:900;font-size:46px;}
  .fonte{top:1120px;}
""", f"""
  <div class="bg"></div>
  <div class="tag" id="revisao-tag">✓ CIÊNCIA</div>
  <h1 class="titulo" id="revisao-t">O que a <em>ciência</em> diz</h1>
  <div id="revisao-n">0</div><div id="revisao-nl">análises</div>
  <div id="revisao-faixa"></div>
  {xicaras("revisao", 5, 90, 640, 96, 20)}
  <div id="revisao-fl">3 a 4 por dia</div>
  <div class="rot" style="top:830px">sem café</div>
  <div class="trilho" style="top:875px"></div><div class="barra" id="revisao-b0" style="top:875px;background:#8C8580"></div>
  <div class="pct" style="top:880px">100</div>
  <div class="rot" style="top:965px">3 a 4 xícaras/dia</div>
  <div class="trilho" style="top:1010px"></div><div class="barra" id="revisao-b1" style="top:1010px;background:var(--laranja)"></div>
  <div class="pct" id="revisao-p1" style="top:1015px;color:var(--laranja)">100</div>
  <div id="revisao-menor">menor ↓</div>
  <div class="fonte" id="revisao-fonte">Fonte: Poole et al., BMJ, 2017 (estudos observacionais)</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#revisao-tag",{{opacity:0,y:-10}},{{opacity:1,y:0,duration:0.3}},0.3);
  tl.fromTo("#revisao-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.3);
  tl.fromTo("#revisao-n",{{opacity:0}},{{opacity:1,duration:0.2}},{t(26)-ini:.2f});
  {contador("#revisao-n", 0, 201, t(26)-ini, 1.0)}
  tl.fromTo("#revisao-nl",{{opacity:0}},{{opacity:1,duration:0.2}},{t(29)-ini:.2f});
  tl.fromTo("#revisao-fonte",{{opacity:0}},{{opacity:1,duration:0.4}},{t(29)-ini:.2f});
  {' '.join(f'tl.fromTo("#revisao-x{i}",{{scale:0}},{{scale:1,duration:0.25,ease:"back.out(2.4)"}},{t(34)-ini+i*0.1:.2f});' for i in range(5))}
  tl.fromTo("#revisao-faixa",{{scale:0}},{{scale:1,duration:0.35,ease:"back.out(1.8)"}},{t(37)-ini:.2f});
  tl.fromTo("#revisao-fl",{{opacity:0}},{{opacity:1,duration:0.3}},{t(39)-ini:.2f});
  tl.fromTo("#revisao-b0",{{scaleX:0}},{{scaleX:1,duration:0.5,ease:"power2.out"}},{t(43)-ini-0.6:.2f});
  tl.fromTo("#revisao-b1",{{scaleX:0}},{{scaleX:1,duration:0.5,ease:"power2.out"}},{t(43)-ini-0.4:.2f});
  tl.to("#revisao-b1",{{scaleX:0.83,duration:0.7,ease:"power2.inOut"}},{t(44)-ini:.2f});
  {contador("#revisao-p1", 100, 83, t(44)-ini, 0.7)}
  tl.fromTo("#revisao-menor",{{opacity:0,scale:2,rotation:-10}},{{opacity:1,scale:1,rotation:-4,duration:0.25,ease:"power4.in"}},{t(53)-ini:.2f});
  tl.to(["#revisao-n","#revisao-nl"],{{opacity:0,duration:0.2}},{t(53)-ini-0.2:.2f});
""")

# ---------- 4. Tito: acelera? (18.7 – 21.4) ----------
ecg = "M0 50 L60 50 L75 50 L85 20 L95 80 L105 35 L115 50 L180 50 L195 50 L205 20 L215 80 L225 35 L235 50 L300 50"
tito_fala("acelera", 18.7, 21.4, "Ué, mas café não acelera o coração?", 19.02, 21.3, destaque=(4, 5, 6), olhos="duvida", cor_ant=BRANCO,
          extra_html=f'<svg style="position:absolute;left:640px;top:690px;width:380px;height:130px" viewBox="0 0 300 100"><path id="acelera-ecg" d="{ecg}" fill="none" stroke="#D45F2B" stroke-width="7" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg>',
          extra_js=f'tl.fromTo("#acelera-ecg",{{attr:{{"stroke-dashoffset":1}}}},{{attr:{{"stroke-dashoffset":0}},duration:1.2,ease:"none"}},{t(59)-18.7:.2f});')

# ---------- 5. arritmia (21.4 – 28.05) ----------
ini, fim = 21.4, 28.05
d = add("arritmia", ini, fim)
wh, wj = wipe("arritmia", CREME)
ecg2 = " ".join(f"M{k*180} 60 L{k*180+70} 60 L{k*180+85} 20 L{k*180+100} 100 L{k*180+112} 45 L{k*180+125} 60 L{k*180+180} 60" for k in range(5))
cena("arritmia", d, f"""
  .bg{{background:var(--pessego);}}
  .tag{{background:#5F6E52;color:#fff;}}
  #arritmia-n{{position:absolute;left:80px;top:420px;font-family:'Playfair Display',serif;font-weight:700;font-size:110px;color:var(--laranja);line-height:1;}}
  #arritmia-nl{{position:absolute;left:84px;top:540px;font-weight:900;font-size:38px;color:#6b6460;}}
  #arritmia-ecg{{position:absolute;left:40px;top:650px;width:1000px;height:150px;}}
  #arritmia-ok{{position:absolute;left:80px;top:850px;padding:12px 28px;border-radius:999px;background:var(--verde);color:#fff;font-weight:900;font-size:44px;}}
  #arritmia-menor{{position:absolute;left:80px;top:950px;font-weight:900;font-size:42px;color:var(--laranja);}}
  .fonte{{top:1110px;}}
""", f"""
  <div class="bg"></div>
  <div class="tag" id="arritmia-tag">✓ CIÊNCIA</div>
  <h1 class="titulo" id="arritmia-t">E a <em>arritmia</em>?</h1>
  <div id="arritmia-n">0</div><div id="arritmia-nl">pessoas acompanhadas por ~12 anos</div>
  <svg id="arritmia-ecg" viewBox="0 0 900 120"><path id="arritmia-linha" d="{ecg2}" fill="none" stroke="#2F483A" stroke-width="7" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/></svg>
  <div id="arritmia-ok">✓ não aumentou</div>
  <div id="arritmia-menor">o risco foi até um pouco menor</div>
  <div class="fonte" id="arritmia-fonte">Fonte: Chieng et al., Eur J Prev Cardiol, 2022 (UK Biobank)</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#arritmia-tag",{{opacity:0,y:-10}},{{opacity:1,y:0,duration:0.3}},0.3);
  tl.fromTo("#arritmia-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.3);
  tl.fromTo("#arritmia-n",{{opacity:0}},{{opacity:1,duration:0.2}},{t(66)-ini:.2f});
  {contador("#arritmia-n", 0, 449563, t(66)-ini, 1.3, "milhar")}
  tl.fromTo("#arritmia-nl",{{opacity:0}},{{opacity:1,duration:0.3}},{t(70)-ini:.2f});
  tl.fromTo("#arritmia-fonte",{{opacity:0}},{{opacity:1,duration:0.4}},{t(66)-ini:.2f});
  tl.fromTo("#arritmia-linha",{{attr:{{"stroke-dashoffset":1}}}},{{attr:{{"stroke-dashoffset":0}},duration:3.2,ease:"none"}},{t(71)-ini:.2f});
  tl.fromTo("#arritmia-ok",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.4)"}},{t(74)-ini:.2f});
  tl.fromTo("#arritmia-menor",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3}},{t(78)-ini:.2f});
""")

# ---------- 6. limite (28.05 – 36.35) ----------
ini, fim = 28.05, 36.35
d = add("limite", ini, fim)
wh, wj = wipe("limite", PESSEGO)
cena("limite", d, """
  .bg{background:#fff;}
  .xic{position:absolute;}
  #limite-tag{position:absolute;left:80px;top:180px;padding:6px 18px;border-radius:999px;background:var(--mostarda);color:#2B2B2B;font-weight:900;font-size:28px;letter-spacing:.06em;}
  .med{position:absolute;left:80px;width:920px;height:70px;border-radius:35px;background:#F2ECE2;}
  .medb{position:absolute;left:80px;width:920px;height:70px;border-radius:35px;transform-origin:0% 50%;}
  .medr{position:absolute;left:80px;font-weight:900;font-size:36px;}
  .medv{position:absolute;right:80px;font-family:'Playfair Display',serif;font-weight:700;font-size:56px;}
  #limite-eq{position:absolute;left:80px;top:760px;font-weight:900;font-size:40px;color:#6b6460;}
  .fonte{top:1110px;}
""", f"""
  <div class="bg"></div>
  <div id="limite-tag">⚠ LIMITE</div>
  <h1 class="titulo" id="limite-t">Mas tem <em>limite</em></h1>
  <div class="medr" style="top:440px">adultos</div><div class="medv" id="limite-v1" style="top:425px;color:var(--laranja)">0 mg</div>
  <div class="med" style="top:500px"></div><div class="medb" id="limite-b1" style="top:500px;background:var(--laranja)"></div>
  {xicaras("limite", 4, 110, 610, 120, 40)}
  <div id="limite-eq">≈ 4 xícaras de café coado (≈ 90 mg cada)</div>
  <div class="medr" id="limite-gr" style="top:880px">grávidas</div><div class="medv" id="limite-v2" style="top:865px;color:var(--verde)">200 mg</div>
  <div class="med" id="limite-m2" style="top:940px"></div><div class="medb" id="limite-b2" style="top:940px;background:var(--verde)"></div>
  <div class="fonte" id="limite-fonte">Fonte: EFSA, Scientific Opinion on the safety of caffeine, 2015</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#limite-tag",{{opacity:0,y:-10}},{{opacity:1,y:0,duration:0.3}},0.3);
  tl.fromTo("#limite-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.3);
  tl.fromTo("#limite-fonte",{{opacity:0}},{{opacity:1,duration:0.4}},{t(89)-ini:.2f});
  tl.fromTo("#limite-b1",{{scaleX:0}},{{scaleX:1,duration:1.6,ease:"power1.inOut"}},{t(89)-ini:.2f});
  (function(){{const o={{v:0}};const el=document.querySelector("#limite-v1");
    tl.fromTo(o,{{v:0}},{{v:400,duration:1.6,ease:"power1.inOut",onUpdate:()=>{{el.textContent=Math.round(o.v)+" mg";}}}},{t(89)-ini:.2f});}})();
  {' '.join(f'tl.fromTo("#limite-x{i}",{{scale:0}},{{scale:1,duration:0.25,ease:"back.out(2.4)"}},{t(97)-ini+i*0.15:.2f});' for i in range(4))}
  tl.fromTo("#limite-eq",{{opacity:0}},{{opacity:1,duration:0.3}},{t(98)-ini:.2f});
  tl.fromTo(["#limite-gr","#limite-v2","#limite-m2"],{{opacity:0}},{{opacity:1,duration:0.3}},{t(102)-ini:.2f});
  tl.fromTo("#limite-b2",{{scaleX:0}},{{scaleX:0.5,duration:0.6,ease:"power2.out"}},{t(102)-ini+0.2:.2f});
""")

# ---------- 7. Tito: e se disparar? (36.35 – 39.2) — com a pose da palpitação ----------
ini, fim = 36.35, 39.2
d = add("dispara", ini, fim)
wh, wj = wipe("dispara", BRANCO)
txt = "E se o meu coração disparar depois do café?"
cena("dispara", d, """
  .bg{background:var(--creme);}
  #dispara-img{left:170px;top:650px;width:740px;height:700px;}
""", f"""
  <div class="bg"></div>
  <div class="balao" id="dispara-balao"><div class="rot">💬 PERGUNTA DO TITO</div>
    <div class="txt">{palavras_html("dispara", txt, 0, (3, 4, 7))}</div><div class="rabo"></div></div>
  <div class="img" id="dispara-img"><img src="assets/tito-palpitacao.png"></div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#dispara-balao",{{opacity:0,y:30,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.3,ease:"back.out(1.6)"}},0.12);
  tl.fromTo("#dispara-img",{{opacity:0,y:100}},{{opacity:1,y:0,duration:0.4,ease:"back.out(1.4)"}},0.05);
  {palavras_js("dispara", txt, ini, 36.5, 39.0)}
  tl.fromTo("#dispara-img",{{scale:1,transformOrigin:"50% 60%"}},{{scale:1.05,duration:0.12,yoyo:true,repeat:9,ease:"power1.inOut"}},{t(110)-ini:.2f});
""")

# ---------- 8. reduzir + médico + cada corpo (39.2 – 43.9) ----------
ini, fim = 39.2, 43.9
d = add("medico", ini, fim)
wh, wj = wipe("medico", CREME)
cena("medico", d, f"""
  .bg{{background:#EEF0EA;}}
  .card2{{position:absolute;left:80px;width:920px;height:120px;background:#fff;border-radius:28px;box-shadow:0 14px 40px rgba(40,60,40,.12);
          display:flex;align-items:center;gap:24px;padding:0 34px;font-weight:900;font-size:42px;}}
  .card2 .e{{font-size:56px;}}
  .cor{{position:absolute;top:840px;width:150px;height:140px;}}
  #medico-cr{{position:absolute;left:80px;top:1010px;width:920px;text-align:center;font-weight:900;font-size:38px;color:#6b6460;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="medico-t">Aí vale <em>reduzir</em></h1>
  <div class="card2" id="medico-c1" style="top:430px"><span class="e">☕↓</span> diminuir a quantidade</div>
  <div class="card2" id="medico-c2" style="top:580px"><span class="e">🩺</span> conversar com um médico</div>
  {''.join(f'<svg class="cor" id="medico-h{i}" style="left:{200+i*250}px" viewBox="0 0 100 92"><path d="M50 88 C20 66 4 50 6 30 C8 12 30 4 50 22 C70 4 92 12 94 30 C96 50 80 66 50 88 Z" fill="{c}"/></svg>' for i, c in enumerate(["#D45F2B", "#CE6840", "#B5481F"]))}
  <div id="medico-cr">cada corpo reage de um jeito</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#medico-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.3);
  tl.fromTo("#medico-c1",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(116)-ini:.2f});
  tl.fromTo("#medico-c2",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(118)-ini:.2f});
  {' '.join(f'tl.fromTo("#medico-h{i}",{{scale:0}},{{scale:1,duration:0.3,ease:"back.out(2)"}},{t(122)-ini+i*0.1:.2f});' for i in range(3))}
  {' '.join(f'tl.fromTo("#medico-h{i}",{{scale:1,transformOrigin:"50% 55%"}},{{scale:1.15,duration:{d_:.2f},yoyo:true,repeat:{r},ease:"power1.inOut",immediateRender:false}},{t(122)-ini+0.6:.2f});' for i,(d_,r) in enumerate([(0.35,3),(0.18,7),(0.5,1)]))}
  tl.fromTo("#medico-cr",{{opacity:0}},{{opacity:1,duration:0.3}},{t(122)-ini-0.3:.2f});
""")

# ---------- 9. resumo do Tito (43.9 – 50.7) ----------
ini, fim = 43.9, 50.7
d = add("resumo", ini, fim)
wh, wj = wipe("resumo", "#EEF0EA")
txt = "Entendi! Café não é vilão. Até umas 4 xícaras tá tranquilo, e se o coração disparar, eu diminuo."
cena("resumo", d, """
  .bg{background:var(--creme);}
  .balao .txt{font-size:56px;}
  #resumo-cafe{left:250px;top:720px;width:580px;height:690px;opacity:0;}
""", f"""
  <div class="bg"></div>
  <div class="balao" id="resumo-balao"><div class="rot">💡 O QUE O TITO ENTENDEU</div>
    <div class="txt">{palavras_html("resumo", txt, 0, (1, 2, 3, 4, 7, 8, 16))}</div><div class="rabo"></div></div>
  <div class="tito-grande" id="resumo-tito">{tito_svg("resumo", bracos="acena")}</div>
  <div class="img" id="resumo-cafe"><img src="assets/tito-cafe.png"></div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#resumo-balao",{{opacity:0,y:30,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"back.out(1.6)"}},0.12);
  tl.fromTo("#resumo-tito",{{opacity:0,y:120}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.4)"}},0.05);
  {palavras_js("resumo", txt, ini, 43.98, 50.4)}
  {fala_js("resumo", round(43.98 - ini, 2), round(t(137) - ini, 2))}
  tl.to("#resumo-tito",{{opacity:0,scale:0.9,duration:0.2}},{t(137)-ini:.2f});
  tl.fromTo("#resumo-cafe",{{opacity:0,scale:0.9}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(1.6)"}},{t(137)-ini+0.05:.2f});
  tl.fromTo("#resumo-cafe",{{rotation:0,transformOrigin:"50% 100%"}},{{rotation:3,duration:0.5,yoyo:true,repeat:3,ease:"sine.inOut"}},{t(137)-ini+0.4:.2f});
""")

# ---------- 10. CTA: enviar + curte/comenta/segue (50.7 – fim) ----------
ini, fim = 50.7, TOTAL
d = add("cta", ini, fim)
wh, wj = wipe("cta", CREME)
cena("cta", d, """
  .bg{background:var(--laranja);}
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
  #cta-eco{position:absolute;inset:0;background:var(--mostarda);}
  #cta-eco .titulo{color:var(--verde);top:240px;font-size:128px;}
  #cta-eco .titulo em{color:#8E3412;}
  #cta-eco-c{position:absolute;left:240px;top:520px;width:600px;height:600px;border-radius:50%;background:var(--creme2);}
  #cta-eco-img{left:300px;top:500px;width:480px;height:570px;}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="cta-t">Manda pra quem diz que <em>café faz mal</em></h1>
  <div id="cta-card" data-layout-allow-overlap><div id="cta-rot">Enviar para…</div>
    <div class="av" id="cta-av0" style="left:30px"><div class="c">A</div>amiga</div>
    <div class="av" id="cta-av1" style="left:215px"><div class="c">M</div>mãe</div>
    <div class="av" id="cta-av2" style="left:400px"><div class="c">J</div>João</div>
    <div class="av" id="cta-av3" style="left:585px"><div class="c">+</div>grupo</div>
    <div id="cta-check">✓</div></div>
  <div class="acao" id="cta-a1" style="left:60px"><span class="i">❤️</span>curte</div>
  <div class="acao" id="cta-a2" style="left:395px"><span class="i">💬</span>"☕ 3 xícaras!"</div>
  <div class="acao" id="cta-a3" style="left:730px" data-layout-allow-overlap><span class="i">🧡</span><div id="cta-seg"><div id="cta-seg1">Seguir</div><div id="cta-seg2">Seguindo ✓</div></div></div>
  <svg id="cta-aviao" viewBox="0 0 100 100"><path d="M6 46 L94 8 L66 92 L48 60 Z" fill="#fff" stroke="#2B2B2B" stroke-width="5" stroke-linejoin="round"/>
    <path d="M48 60 L94 8" stroke="#2B2B2B" stroke-width="4"/></svg>
  <div id="cta-aviso">Conteúdo educativo, não substitui orientação profissional.</div>
  <div class="tito-mini" id="cta-tito" style="top:1360px">{tito_svg("cta", olhos="piscando", bracos="acena")}</div>
  <div id="cta-eco" style="opacity:0"><div id="cta-eco-c"></div><h1 class="titulo">Café <em>faz mal?</em></h1>
    <div class="img" id="cta-eco-img"><img src="assets/tito-cafe.png"></div></div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#cta-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(148)-ini-0.2:.2f});
  tl.fromTo("#cta-card",{{opacity:0,y:60,scale:0.95}},{{opacity:1,y:0,scale:1,duration:0.45,ease:"back.out(1.5)"}},{t(148)-ini:.2f});
  {' '.join(f'tl.fromTo("#cta-av{i}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.25,ease:"back.out(2)"}},{t(149)-ini+i*0.1:.2f});' for i in range(4))}
  tl.to("#cta-aviao",{{x:-500,y:-500,rotation:-25,scale:0.6,duration:0.8,ease:"power2.in"}},{t(152)-ini:.2f});
  tl.to("#cta-aviao",{{opacity:0,duration:0.1}},{t(152)-ini+0.75:.2f});
  tl.fromTo("#cta-check",{{scale:0}},{{scale:1,duration:0.3,ease:"back.out(2.4)"}},{t(152)-ini+0.8:.2f});
  tl.fromTo("#cta-a1",{{opacity:0,scale:0.4,y:40}},{{opacity:1,scale:1,y:0,duration:0.35,ease:"back.out(2.2)"}},{t(158)-ini-0.05:.2f});
  tl.fromTo("#cta-a1 .i",{{scale:1}},{{scale:1.35,duration:0.15,yoyo:true,repeat:1}},{t(158)-ini+0.3:.2f});
  tl.fromTo("#cta-a2",{{opacity:0,scale:0.4,y:40}},{{opacity:1,scale:1,y:0,duration:0.35,ease:"back.out(2.2)"}},{t(159)-ini-0.05:.2f});
  tl.fromTo("#cta-a3",{{opacity:0,scale:0.4,y:40}},{{opacity:1,scale:1,y:0,duration:0.35,ease:"back.out(2.2)"}},{t(165)-ini-0.05:.2f});
  tl.to("#cta-seg1",{{opacity:0,duration:0.15}},{t(165)-ini+0.45:.2f});
  tl.to("#cta-seg2",{{opacity:1,duration:0.15}},{t(165)-ini+0.45:.2f});
  tl.fromTo("#cta-aviso",{{opacity:0}},{{opacity:1,duration:0.4}},0.6);
  tl.fromTo("#cta-tito",{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.5)"}},0.4);
  tl.fromTo("#cta-braco",{{rotation:-12,transformOrigin:"170px 100px"}},{{rotation:12,duration:0.3,ease:"sine.inOut",yoyo:true,repeat:7}},0.9);
  tl.to(["#cta-t","#cta-card","#cta-a1","#cta-a2","#cta-a3","#cta-aviso","#cta-tito"],{{opacity:0,duration:0.3}},{TOTAL-ini-2.1:.2f});
  tl.fromTo("#cta-eco",{{opacity:0}},{{opacity:1,duration:0.35,ease:"power2.inOut"}},{TOTAL-ini-2.1:.2f});
""")

# ---------- legendas do narrador ----------
GRUPOS = [
    ("*Café*... faz mal pro coração?", 0, 5), ("Talvez você *não precise cortar*.", 5, 5),
    ("Uma revisão juntou", 23, 3), ("mais de *200 análises*", 26, 4), ("sobre café e saúde.", 30, 4),
    ("Quem tomava *de 3 a 4 xícaras* por dia", 34, 9), ("tinha *risco menor*", 43, 3), ("de morte e de *doença do coração*.", 46, 7),
    ("*Menor, não maior.*", 53, 3),
    ("Num estudo com *quase meio milhão* de pessoas,", 63, 8), ("quem tomava café", 71, 3), ("*não teve mais arritmia*.", 74, 4),
    ("O risco foi até *um pouco menor*.", 78, 7),
    ("Mas tem *limite*.", 85, 3), ("Até *400 miligramas* de cafeína por dia.", 88, 7), ("Algo como *4 xícaras* de café coado.", 95, 7),
    ("*Grávidas*, até 200.", 102, 3),
    ("Aí vale *reduzir*", 114, 3), ("e conversar com *um médico*.", 117, 5), ("*Cada corpo* reage de um jeito.", 122, 6),
    ("*Isso aí.*", 146, 2), ("Manda pra quem vive dizendo", 148, 5), ("que *café faz mal*.", 153, 4),
    ("E *curte*,", 157, 2), ("*comenta* quantas xícaras você toma", 159, 5), ("e *segue pra mais!*", 164, 4),
]
for txt_, i0, n in GRUPOS:
    print(f"{txt_!r:52} <- {' '.join(w['palavra'] for w in words[i0:i0+n])!r}")
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
