#!/usr/bin/env python3
"""Vídeo 08 do cronograma: "Respiração 4-7-8 funciona?" (estrutura Evolução)."""
import json, math, re, shutil
from pathlib import Path

SCR = Path("/tmp/claude-0/-home-user-Victor1Paim/bc508778-dc0e-5c3d-a4a6-a9dce8035bd2/scratchpad")
POST = Path("/home/user/Victor1Paim/saude-sem-sermao/producoes/08-respiracao-478")
V = POST / "video"
(V / "compositions").mkdir(parents=True, exist_ok=True)
(V / "assets").mkdir(exist_ok=True)
for f in ["hyperframes.json", "package.json", "meta.json"]:
    (V / f).write_text((SCR / "hfblank" / f).read_text().replace('"hfblank"', '"saude-sem-sermao-08-respiracao"'))
shutil.copy(POST / "dialogo.mp3", V / "assets/voz.mp3")
shutil.copy(POST / "imagens/tito-respira.png", V / "assets/tito-respira.png")

W, H = 1080, 1920
TOTAL = 59.6
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
  .num{position:absolute;width:190px;height:190px;border-radius:50%;display:flex;align-items:center;justify-content:center;
       font-family:'Playfair Display',serif;font-weight:800;font-size:130px;color:#fff;box-shadow:0 12px 34px rgba(0,0,0,.25);}
  .relo{position:absolute;left:730px;top:190px;width:270px;padding:12px 0;border-radius:999px;background:rgba(18,22,18,.85);color:#fff;
        text-align:center;font-weight:900;font-size:52px;font-variant-numeric:tabular-nums;}
"""
CORES = ["#95A185", "#E2B04A", "#D45F2B"]

# 1. capa (0 – 4.5)
d = add("capa", 0, 4.5)
cena("capa", d, f"""
  .bg{{background:var(--verde);}}
  .titulo{{color:var(--creme2);top:230px;font-size:110px;}}
  .titulo em{{color:var(--mostarda);}}
  #capa-img{{left:300px;top:820px;width:480px;height:520px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="capa-t">Respiração <em>4-7-8</em> funciona?</h1>
  {''.join(f'<div class="num" id="capa-n{i}" style="left:{110+i*300}px;top:560px;background:{c};color:{"#fff" if i==2 else "#1F3328"}">{n}</div>' for i,(n,c) in enumerate(zip("478",CORES)))}
  <div class="img" id="capa-img"><img src="assets/tito-respira.png"></div>
""", f"""
  {' '.join(f'tl.fromTo("#capa-n{i}",{{scale:0.6,opacity:0.3}},{{scale:1,opacity:1,duration:0.3,ease:"back.out(2.4)"}},{t(1+i)-0.05:.2f});' for i in range(3))}
  tl.fromTo("#capa-img",{{scale:1}},{{scale:1.05,duration:1.0,ease:"sine.inOut",yoyo:true,repeat:3,transformOrigin:"50% 100%"}},0);
""")

# 2. Tito (4.5 – 7.45)
tito_fala("t1", 4.5, 7.45, "Respirar contando? Parece coisa de coach.", 4.58, 7.2, destaque=(5,), olhos="duvida", cor_ant=VERDE, tam=68)

# 3. o ciclo (7.45 – 20.2)
ini, fim = 7.45, 20.2
d = add("ciclo", ini, fim)
wh, wj = wipe("ciclo", CREME)
cena("ciclo", d, f"""
  .bg{{background:#fff;}}
  #ciclo-fase{{position:absolute;left:80px;top:200px;padding:12px 30px;border-radius:999px;background:var(--verde);color:#fff;font-weight:900;font-size:46px;letter-spacing:.06em;}}
  #ciclo-pulm{{position:absolute;left:180px;top:380px;width:480px;height:560px;transform-origin:50% 60%;}}
  #ciclo-cor{{position:absolute;left:720px;top:520px;font-size:150px;}}
  #ciclo-bpm{{position:absolute;left:680px;top:720px;width:300px;text-align:center;font-weight:900;font-size:40px;}}
  #ciclo-l{{position:absolute;left:80px;top:1000px;width:920px;text-align:center;font-weight:900;font-size:42px;color:#5b524c;}}
""", f"""
  <div class="bg"></div>
  <div class="relo" id="ciclo-rel">0 s</div>
  <div id="ciclo-fase">INSPIRA · 4</div>
  <svg id="ciclo-pulm" viewBox="0 0 240 280"><path d="M120 20 L120 110" stroke="#2F483A" stroke-width="14" stroke-linecap="round"/>
    <path d="M112 100 C70 70 20 110 20 180 C20 240 60 262 100 250 C112 246 116 230 116 210 L116 120 Z" fill="#E8907A" stroke="#C2563A" stroke-width="6"/>
    <path d="M128 100 C170 70 220 110 220 180 C220 240 180 262 140 250 C128 246 124 230 124 210 L124 120 Z" fill="#E8907A" stroke="#C2563A" stroke-width="6"/></svg>
  <div id="ciclo-cor">❤️</div>
  <div id="ciclo-bpm">coração <span id="ciclo-seta" style="color:var(--laranja)">▲</span></div>
  <div id="ciclo-l">pelo nariz</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#ciclo-pulm",{{scale:0.72}},{{scale:1.0,duration:{t(31)-t(22):.2f},ease:"sine.inOut"}},{t(22)-ini:.2f});
  tl.to("#ciclo-cor",{{scale:1.18,duration:0.22,yoyo:true,repeat:{int((t(32)-t(26))/0.44)*2+1},ease:"sine.inOut"}},{t(26)-ini:.2f});
  tl.fromTo("#ciclo-rel",{{opacity:0.5}},{{opacity:1,duration:0.2}},{t(20)-ini:.2f});
  tl.set("#ciclo-rel",{{textContent:"4 s"}},{t(32)-ini:.2f});
  tl.set("#ciclo-fase",{{textContent:"SEGURA · 7",background:"#E2B04A",color:"#1F3328"}},{t(32)-ini:.2f});
  tl.set("#ciclo-l",{{textContent:"segura o ar"}},{t(32)-ini:.2f});
  tl.set("#ciclo-seta",{{textContent:"="}},{t(32)-ini:.2f});
  tl.set("#ciclo-rel",{{textContent:"11 s"}},{t(37)-ini:.2f});
  tl.set("#ciclo-fase",{{textContent:"SOLTA · 8",background:"#D45F2B",color:"#fff"}},{t(37)-ini:.2f});
  tl.set("#ciclo-l",{{textContent:"pela boca, devagar"}},{t(37)-ini:.2f});
  tl.to("#ciclo-pulm",{{scale:0.7,duration:{t(49)-t(39):.2f},ease:"sine.inOut"}},{t(39)-ini:.2f});
  tl.set("#ciclo-seta",{{textContent:"▼"}},{t(47)-ini:.2f});
  tl.to("#ciclo-cor",{{scale:1.1,duration:0.5,yoyo:true,repeat:3,ease:"sine.inOut"}},{t(47)-ini:.2f});
  tl.set("#ciclo-rel",{{textContent:"19 s"}},{t(49)-ini+0.3:.2f});
""")

# 4. Tito (20.2 – 21.75)
tito_fala("t2", 20.2, 21.95, "E depois de um minuto?", 20.32, 21.6, destaque=(3, 4), olhos="duvida", cor_ant=BRANCO, tam=74)

# 5. freio (21.75 – 28.8)
ini, fim = 21.95, 28.8
d = add("freio", ini, fim)
wh, wj = wipe("freio", CREME)
cena("freio", d, f"""
  .bg{{background:#EEF0EA;}}
  .titulo{{top:300px;}}
  .ci{{position:absolute;top:520px;width:200px;height:120px;border-radius:24px;background:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:40px;color:#c9c3ba;}}
  #freio-vfc{{position:absolute;left:80px;top:700px;width:920px;padding:24px 34px;border-radius:26px;background:#fff;font-weight:900;font-size:40px;}}
  #freio-vfc .tr{{position:relative;height:30px;border-radius:15px;background:#F2ECE2;margin-top:14px;overflow:hidden;}}
  #freio-fi{{position:absolute;left:0;top:0;bottom:0;width:100%;border-radius:15px;background:linear-gradient(90deg,#95A185,#2F483A);transform-origin:0 50%;}}
  #freio-p{{position:absolute;left:80px;top:900px;font-weight:900;font-size:34px;color:#8a837d;}}
  .fonte{{top:1110px;}}
""", f"""
  <div class="bg"></div>
  <div class="relo" id="freio-rel">~1 min</div>
  <h1 class="titulo" id="freio-t">Entra o <em>freio do corpo</em> 🛑</h1>
  {''.join(f'<div class="ci" id="freio-c{i}" style="left:{80+i*240}px">{i+1}/4</div>' for i in range(4))}
  <div id="freio-vfc">💓 sinal de relaxamento do coração (VFC)<div class="tr"><div id="freio-fi"></div></div></div>
  <div id="freio-p">estudo pequeno, efeito logo depois</div>
  <div class="fonte" id="freio-f">Fonte: Vierra et al., Physiological Reports, 2022</div>
  {wh}
""", f"""
  {wj}
  {' '.join(f'tl.to("#freio-c{i}",{{background:"#2F483A",color:"#fff",duration:0.15}},{t(56)-ini+i*0.25:.2f});' for i in range(4))}
  tl.fromTo("#freio-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(60)-ini:.2f});
  tl.fromTo(["#freio-vfc","#freio-p","#freio-f"],{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.35,ease:"back.out(1.6)"}},{t(65)-ini:.2f});
  tl.fromTo("#freio-fi",{{scaleX:0.35}},{{scaleX:0.75,duration:1.0,ease:"power2.out"}},{t(74)-ini:.2f});
""")

# 6. VIRADA (28.8 – 38.15)
ini, fim = 28.8, 38.15
d = add("virada", ini, fim)
wh, wj = wipe("virada", "#EEF0EA")
cena("virada", d, f"""
  .bg{{background:var(--verde);}}
  .titulo{{color:var(--creme2);top:230px;}}
  .titulo em{{color:var(--mostarda);}}
  #virada-exp{{position:absolute;left:80px;top:600px;width:920px;padding:24px 34px;border-radius:26px;background:rgba(255,255,255,.1);color:#fff;font-weight:900;font-size:40px;}}
  #virada-exp .tr{{position:relative;height:30px;border-radius:15px;background:rgba(255,255,255,.15);margin-top:14px;overflow:hidden;}}
  #virada-in{{position:absolute;left:0;top:0;bottom:0;width:33%;background:#95A185;}}
  #virada-out{{position:absolute;left:33%;top:0;bottom:0;width:67%;background:#E2B04A;transform-origin:0 50%;}}
  #virada-meta{{position:absolute;left:80px;top:830px;width:920px;padding:24px 34px;border-radius:26px;background:#fff;font-weight:900;font-size:40px;}}
  #virada-meta .q{{font-size:28px;letter-spacing:.06em;color:var(--laranja);margin-bottom:6px;}}
""", f"""
  <div class="bg"></div>
  {''.join(f'<div class="num" id="virada-n{i}" style="left:{110+i*300}px;top:560px;background:{c};color:{"#fff" if i==2 else "#1F3328"}">{n}</div>' for i,(n,c) in enumerate(zip("478",CORES)))}
  <h1 class="titulo" id="virada-t">O segredo: <em>soltar o ar devagar</em></h1>
  <div id="virada-exp">🌬️ inspira curto · solta longo<div class="tr"><div id="virada-in"></div><div id="virada-out"></div></div></div>
  <div id="virada-meta"><div class="q">META-ANÁLISE · Fincham et al., Sci Rep 2023</div>técnicas de respiração: <span style="color:var(--laranja)">↓ um pouco o estresse</span></div>
  {wh}
""", f"""
  {wj}
  {' '.join(f'tl.to("#virada-n{i}",{{y:1400,rotation:{(i-1)*40},duration:0.8,ease:"power2.in"}},{t(81)-ini+i*0.1:.2f});' for i in range(3))}
  tl.fromTo("#virada-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(84)-ini:.2f});
  tl.fromTo("#virada-exp",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.35,ease:"back.out(1.6)"}},{t(85)-ini:.2f});
  tl.fromTo("#virada-out",{{scaleX:0}},{{scaleX:1,duration:1.6,ease:"none"}},{t(87)-ini:.2f});
  tl.fromTo("#virada-meta",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.35,ease:"back.out(1.6)"}},{t(92)-ini:.2f});
""")

# 7. ressalva (38.15 – 42.75)
ini, fim = 38.15, 42.75
d = add("ressalva", ini, fim)
wh, wj = wipe("ressalva", VERDE)
cena("ressalva", d, f"""
  .bg{{background:var(--pessego);}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="ressalva-t">Com <em>cuidado</em></h1>
  <div class="chip" id="ressalva-a" style="top:520px"><span class="i">😵‍💫</span>ficou tonto? volta ao normal</div>
  <div class="chip" id="ressalva-b" style="top:660px"><span class="i">💬</span>ansiedade frequente? procure ajuda</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#ressalva-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.15);
  tl.fromTo("#ressalva-a",{{opacity:0,x:-100}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{max(t(105)-ini,0.25):.2f});
  tl.fromTo("#ressalva-b",{{opacity:0,x:-100}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(110)-ini:.2f});
""")

# 8. resumo (42.75 – 48.2)
ini, fim = 42.75, 48.2
d = add("resumo", ini, fim)
wh, wj = wipe("resumo", PESSEGO)
txt = "Entendi! Não é mágica dos números: é expirar devagar que puxa o freio do corpo."
cena("resumo", d, """
  .bg{background:var(--creme);}
  .balao .txt{font-size:56px;}
""", f"""
  <div class="bg"></div>
  <div class="balao" id="resumo-balao"><div class="rot">💡 O QUE O TITO ENTENDEU</div>
    <div class="txt">{palavras_html("resumo", txt, 0, (7, 8, 10, 11, 12, 13, 14))}</div><div class="rabo"></div></div>
  <div class="tito-grande" id="resumo-tito">{tito_svg("resumo", bracos="acena")}</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#resumo-balao",{{opacity:0,y:30,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"back.out(1.6)"}},0.12);
  tl.fromTo("#resumo-tito",{{opacity:0,y:120}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.4)"}},0.05);
  {palavras_js("resumo", txt, ini, 42.88, 48.0)}
  {fala_js("resumo", round(42.88 - ini, 2), round(48.0 - ini, 2))}
""")

# 9. resposta + eco (48.2 – 51.85)
ini, fim = 48.2, 51.85
d = add("resposta", ini, fim)
wh, wj = wipe("resposta", CREME)
cena("resposta", d, f"""
  .bg{{background:var(--verde);}}
  .titulo{{color:var(--creme2);top:250px;font-size:96px;}}
  .titulo em{{color:var(--mostarda);}}
  #resposta-img{{left:280px;top:700px;width:520px;height:570px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="resposta-t">4-7-8 funciona? <em>Como respiração lenta, sim.</em></h1>
  <div class="img" id="resposta-img"><img src="assets/tito-respira.png"></div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#resposta-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.12);
  tl.fromTo("#resposta-t em",{{scale:1}},{{scale:1.05,duration:0.18,yoyo:true,repeat:1}},{t(134)-ini:.2f});
  tl.fromTo("#resposta-img",{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.4,ease:"back.out(1.6)"}},0.2);
""")

# 10. CTA (51.85 – fim)
ini, fim = 51.85, TOTAL
d = add("cta", ini, fim)
wh, wj = wipe("cta", CREME)
src4 = (SCR / "build_cafe.py").read_text()
cta_src = src4[src4.index('cena("cta", d, """'):src4.index("# ---------- legendas do narrador")]
cta_src = (cta_src
    .replace(".bg{background:var(--laranja);}", ".bg{background:var(--verde);}\n  #cta-tito{filter:drop-shadow(0 0 2px #FDF3ED) drop-shadow(0 0 2px #FDF3ED);}")  # Tito não some no fundo
    .replace("Manda pra quem diz que <em>café faz mal</em>", "Manda pra quem vive <em>acelerado</em>")
    .replace('"☕ 3 xícaras!"', "🌬️ RESPIRA")
    .replace("#cta-eco{position:absolute;inset:0;background:var(--mostarda);}", "#cta-eco{position:absolute;inset:0;background:#2F483A;}")
    .replace("#cta-eco .titulo{color:var(--verde);top:240px;font-size:128px;}", "#cta-eco .titulo{color:#FDF3ED;top:230px;font-size:110px;}")
    .replace("#cta-eco .titulo em{color:#8E3412;}", "#cta-eco .titulo em{color:#E2B04A;}")
    .replace('<div id="cta-eco-c"></div><h1 class="titulo">Café <em>faz mal?</em></h1>', '<h1 class="titulo">Respiração <em>4-7-8</em> funciona?</h1>')
    .replace("assets/tito-cafe.png", "assets/tito-respira.png")
    .replace("#cta-eco-img{left:300px;top:500px;width:480px;height:570px;}", "#cta-eco-img{left:260px;top:620px;width:560px;height:620px;}")
    .replace("t(165)-ini-0.05", "t(153)-ini-0.6").replace("t(165)-ini+0.45", "t(153)-ini+0.15")
    .replace("TOTAL-ini-2.1", "TOTAL-ini-2.3")
    .replace("t(165)", "t(153)").replace("t(159)", "t(147)").replace("t(158)", "t(146)")
    .replace("t(148)", "t(140)").replace("t(149)", "t(141)").replace("t(152)", "t(144)"))
exec(cta_src)

GRUPOS = [
    ("Respiração *4, 7, 8*:", 0, 4), ("o que ela faz *no seu corpo* em 1 minuto?", 4, 10),
    ("*Segundo 0*: inspira pelo nariz até 4.", 20, 7), ("O coração *acelera um pouquinho*.", 27, 5),
    ("*Segundo 4*: segura até 7.", 32, 5), ("*Segundo 11*: solta pela boca até 8.", 37, 7),
    ("Na *expiração longa*,", 44, 3), ("o coração *desacelera*.", 47, 3),
    ("Depois de *uns 4 ciclos*,", 55, 5), ("entra *o freio do corpo*.", 60, 5),
    ("Num *estudo pequeno*,", 65, 3), ("um *sinal de relaxamento* do coração", 68, 6), ("*subiu* logo depois.", 74, 3),
    ("Mas o segredo *não são os números*.", 77, 7), ("É *respirar devagar*,", 84, 3), ("*soltando o ar bem devagar*.", 87, 5),
    ("Uma *meta-análise* viu que", 92, 5), ("técnicas de respiração", 97, 3), ("*reduzem um pouco o estresse*.", 100, 5),
    ("Ficou tonto? *Volta ao normal.*", 105, 5), ("Ansiedade frequente? *Procure ajuda.*", 110, 4),
    ("Então, *4, 7, 8 funciona?*", 129, 5), ("*Como respiração lenta, sim.*", 134, 4),
    ("*Isso aí.*", 138, 2), ("Manda pra quem vive *acelerado*.", 140, 5), ("E *curte*,", 145, 2),
    ("*comenta RESPIRA* se vai testar", 147, 5), ("e *segue pra mais!*", 152, 4),
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
