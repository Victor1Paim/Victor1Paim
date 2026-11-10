#!/usr/bin/env python3
"""Vídeo 10 do cronograma: "Ronco: só barulho ou sinal de alerta?" (estrutura Jornada)."""
import json, math, re, shutil
from pathlib import Path

SCR = Path("/tmp/claude-0/-home-user-Victor1Paim/bc508778-dc0e-5c3d-a4a6-a9dce8035bd2/scratchpad")
POST = Path("/home/user/Victor1Paim/saude-sem-sermao/producoes/10-ronco")
V = POST / "video"
(V / "compositions").mkdir(parents=True, exist_ok=True)
(V / "assets").mkdir(exist_ok=True)
for f in ["hyperframes.json", "package.json", "meta.json"]:
    (V / f).write_text((SCR / "hfblank" / f).read_text().replace('"hfblank"', '"saude-sem-sermao-10-ronco"'))
shutil.copy(POST / "dialogo.mp3", V / "assets/voz.mp3")
shutil.copy(POST / "imagens/tito-ronco.png", V / "assets/tito-ronco.png")

W, H = 1080, 1920
TOTAL = 64.8
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
  .meta{position:absolute;left:80px;top:180px;width:920px;padding:16px 26px;border-radius:24px;background:rgba(31,51,40,.92);color:#fff;font-weight:900;font-size:30px;letter-spacing:.05em;}
  .meta .tr{position:relative;height:26px;border-radius:13px;background:rgba(255,255,255,.18);margin-top:10px;overflow:hidden;}
  .meta .fi{position:absolute;left:0;top:0;bottom:0;width:100%;border-radius:13px;background:linear-gradient(90deg,#E2B04A,#95A185);transform-origin:0 50%;}
  .meta .pc{position:absolute;right:26px;top:14px;font-size:34px;}
"""
PESS = "#F7E5DD"

def meta(cid, de, anim=False):
    return (f'<div class="meta" id="{cid}-meta">🎯 META DO TITO: PARAR DE RONCAR<span class="pc" id="{cid}-pc">{de}%</span>'
            f'<div class="tr"><div class="fi" id="{cid}-fi"' + ('' if anim else f' style="transform:scaleX({de/100})"') + '></div></div></div>')

def meta_js(cid, de, ate, t_rel, dur=0.6):
    return (f'tl.fromTo("#{cid}-fi",{{scaleX:{de/100}}},{{scaleX:{ate/100},duration:{dur},ease:"power2.inOut"}},{t_rel:.2f});'
            f'(function(){{const o={{v:{de}}};const el=document.querySelector("#{cid}-pc");'
            f'tl.fromTo(o,{{v:{de}}},{{v:{ate},duration:{dur},ease:"power2.inOut",onUpdate:()=>{{el.textContent=Math.round(o.v)+"%";}}}},{t_rel:.2f});}})();')

# 1. capa (0 – 3.75)
d = add("capa", 0, 3.75)
cena("capa", d, f"""
  .bg{{background:{PESS};}}
  .titulo{{color:var(--verde);top:330px;font-size:124px;}}
  .titulo em{{color:var(--laranja);}}
  #capa-img{{left:200px;top:650px;width:680px;height:700px;}}
""", f"""
  <div class="bg"></div>
  {meta("capa", 0)}
  <h1 class="titulo" id="capa-t">Ronco: <em>só barulho?</em></h1>
  <div class="img" id="capa-img"><img src="assets/tito-ronco.png"></div>
""", f"""
  tl.fromTo("#capa-meta",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:0.35,ease:"back.out(1.6)"}},{t(5)-0.1:.2f});
  tl.fromTo("#capa-img",{{scale:1}},{{scale:1.03,duration:0.45,ease:"sine.inOut",yoyo:true,repeat:7,transformOrigin:"50% 80%"}},0);
""")

# 2. Tito (3.75 – 6.0)
tito_fala("t1", 3.75, 6.0, "Fácil! Ronco é só barulho, né?", 3.84, 5.95, destaque=(3, 4), olhos="normal", cor_ant=PESS, tam=72)

# 3. estatística (6.0 – 12.8)
ini, fim = 6.0, 12.8
d = add("stat", ini, fim)
wh, wj = wipe("stat", CREME)
cena("stat", d, f"""
  .bg{{background:#fff;}}
  .titulo{{top:330px;}}
  .pessoa{{position:absolute;top:560px;width:240px;height:400px;}}
  #stat-l{{position:absolute;left:80px;top:990px;width:920px;text-align:center;font-weight:900;font-size:48px;}}
  .fonte{{top:1100px;}}
""", f"""
  <div class="bg"></div>
  {meta("stat", 0)}
  <h1 class="titulo" id="stat-t">Nem sempre: pode ser <em>apneia</em></h1>
  {''.join(f'<svg class="pessoa" id="stat-p{i}" style="left:{150+i*280}px" viewBox="0 0 60 100"><circle cx="30" cy="18" r="14" fill="{"#D45F2B" if i==1 else "#C9C3BA"}"/><rect x="10" y="36" width="40" height="60" rx="18" fill="{"#D45F2B" if i==1 else "#C9C3BA"}"/></svg>' for i in range(3))}
  <div id="stat-l">quase <span style="color:var(--laranja)">1 em cada 3</span> adultos</div>
  <div class="fonte" id="stat-f">Fonte: Tufik et al., Sleep Med 2010 (EPISONO, São Paulo)</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#stat-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.2);
  tl.fromTo("#stat-meta .fi",{{x:0}},{{x:6,duration:0.05,yoyo:true,repeat:5}},0.25);
  tl.fromTo(["#stat-f"],{{opacity:0}},{{opacity:1,duration:0.3}},{t(22)-ini:.2f});
  {' '.join(f'tl.fromTo("#stat-p{i}",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.3,ease:"back.out(1.8)"}},{t(28)-ini+i*0.15:.2f});' for i in range(3))}
  tl.fromTo("#stat-p1",{{scale:1}},{{scale:1.15,duration:0.2,yoyo:true,repeat:1,transformOrigin:"50% 100%"}},{t(32)-ini:.2f});
  tl.fromTo("#stat-l",{{opacity:0}},{{opacity:1,duration:0.3}},{t(29)-ini:.2f});
""")

# 4. mecanismo (12.8 – 19.1)
ini, fim = 12.8, 19.1
d = add("mec", ini, fim)
wh, wj = wipe("mec", BRANCO)
cena("mec", d, f"""
  .bg{{background:#EEF0EA;}}
  .titulo{{top:330px;}}
  #mec-via{{position:absolute;left:140px;top:560px;width:800px;height:200px;}}
  #mec-resp{{position:absolute;left:80px;top:820px;width:920px;height:200px;}}
  #mec-l{{position:absolute;left:80px;top:1040px;width:920px;text-align:center;font-weight:900;font-size:40px;color:#5b524c;}}
""", f"""
  <div class="bg"></div>
  {meta("mec", 0)}
  <h1 class="titulo" id="mec-t">Na apneia, a garganta <em>fecha</em></h1>
  <svg id="mec-via" viewBox="0 0 400 100">
    <rect x="0" y="10" width="400" height="22" rx="10" fill="#D45F2B" id="mec-cima"/>
    <rect x="0" y="68" width="400" height="22" rx="10" fill="#D45F2B" id="mec-baixo"/>
    <text x="200" y="58" text-anchor="middle" font-size="16" font-weight="900" fill="#2F483A" font-family="Nunito" id="mec-ar">ar →</text></svg>
  <svg id="mec-resp" viewBox="0 0 460 100"><path d="M0 50 Q15 10 30 50 T60 50 T90 50 T120 50 L210 50 Q225 10 240 50 T270 50 T300 50 L390 50 Q405 10 420 50 T450 50" fill="none" stroke="#2F483A" stroke-width="5" stroke-linecap="round" id="mec-linha" stroke-dasharray="1000" stroke-dashoffset="1000"/>
    <text x="165" y="85" text-anchor="middle" font-size="16" font-weight="900" fill="#9E3D16" font-family="Nunito">pausa</text>
    <text x="345" y="85" text-anchor="middle" font-size="16" font-weight="900" fill="#9E3D16" font-family="Nunito">pausa</text></svg>
  <div id="mec-l">a respiração para por segundos, várias vezes por noite</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#mec-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.2);
  tl.fromTo("#mec-via",{{opacity:0}},{{opacity:1,duration:0.3}},0.4);
  tl.to("#mec-cima",{{y:22,duration:0.5,ease:"power2.in"}},{t(41)-ini:.2f});
  tl.to("#mec-baixo",{{y:-22,duration:0.5,ease:"power2.in"}},{t(41)-ini:.2f});
  tl.to("#mec-ar",{{opacity:0,duration:0.2}},{t(41)-ini+0.3:.2f});
  tl.to("#mec-linha",{{strokeDashoffset:0,duration:2.4,ease:"none"}},{t(45)-ini:.2f});
  tl.fromTo("#mec-l",{{opacity:0}},{{opacity:1,duration:0.3}},{t(48)-ini:.2f});
""")

# 5. Tito: truque (19.1 – 21.95)
tito_fala("t2", 19.1, 21.95, "Então eu compro um truque da internet e pronto?", 19.2, 21.8, destaque=(4, 5, 6), olhos="duvida", cor_ant="#EEF0EA", tam=62)

# 6. atalho que engana (21.95 – 30.5)
ini, fim = 21.95, 30.5
d = add("atalho", ini, fim)
wh, wj = wipe("atalho", CREME)
cena("atalho", d, f"""
  .bg{{background:{PESS};}}
  .titulo{{top:330px;}}
  #atalho-x{{position:absolute;left:80px;top:840px;width:920px;padding:22px 34px;border-radius:26px;background:var(--verde);color:#fff;font-weight:900;font-size:42px;}}
""", f"""
  <div class="bg"></div>
  {meta("atalho", 0, True)}
  <h1 class="titulo" id="atalho-t">O atalho que <em>engana</em></h1>
  <div class="chip" id="atalho-a" style="top:540px"><span class="i">🛏️</span>dormir de lado</div>
  <div class="chip" id="atalho-b" style="top:680px"><span class="i">🍺</span>evitar álcool à noite</div>
  <div id="atalho-x">⚠️ se for apneia, só o truque não resolve</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#atalho-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(65)-ini:.2f});
  tl.fromTo("#atalho-a",{{opacity:0,x:-100}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(71)-ini:.2f});
  tl.fromTo("#atalho-b",{{opacity:0,x:-100}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(75)-ini:.2f});
  {meta_js("atalho", 0, 45, t(79)-ini)}
  tl.fromTo("#atalho-x",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.35,ease:"back.out(1.6)"}},{t(84)-ini:.2f});
  tl.to("#atalho-fi",{{scaleX:0.10,duration:0.5,ease:"power2.inOut"}},{t(89)-ini:.2f});
  (function(){{const o={{v:45}};const el=document.querySelector("#atalho-pc");tl.to(o,{{v:10,duration:0.5,ease:"power2.inOut",onUpdate:()=>{{el.textContent=Math.round(o.v)+"%";}}}},{t(89)-ini:.2f});}})();
""")

# 7. VIRADA: os sinais (30.5 – 45.95)
ini, fim = 30.5, 45.95
d = add("sinais", ini, fim)
wh, wj = wipe("sinais", PESS)
SIN = [("😮‍💨", "ronco alto quase toda noite", 99), ("⏸️", "pausas na respiração que alguém percebe", 104), ("😵", "acordar engasgado", 110), ("🥱", "sono demais durante o dia", 113)]
cena("sinais", d, f"""
  .bg{{background:#fff;}}
  .titulo{{top:330px;}}
  .sin{{position:absolute;left:80px;width:920px;padding:16px 28px;border-radius:22px;background:#F2ECE2;font-weight:900;font-size:38px;display:flex;align-items:center;gap:20px;color:#8a837d;}}
  .sin .i{{font-size:54px;}}
  #sinais-med{{position:absolute;left:80px;top:1000px;width:920px;padding:20px 30px;border-radius:24px;background:var(--verde);color:#fff;font-weight:900;font-size:40px;}}
  #sinais-trat{{position:absolute;left:80px;top:1110px;font-weight:900;font-size:38px;color:var(--verde);}}
""", f"""
  <div class="bg"></div>
  {meta("sinais", 10, True)}
  <h1 class="titulo" id="sinais-t">O que destrava: <em>os sinais</em></h1>
  {''.join(f'<div class="sin" id="sinais-s{i}" style="top:{530+i*110}px"><span class="i">{e}</span>{n}</div>' for i,(e,n,_) in enumerate(SIN))}
  <div id="sinais-med">🩺 médico + exame do sono</div>
  <div id="sinais-trat">✓ apneia tem tratamento</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#sinais-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{max(t(92)-ini,0.15):.2f});
  {' '.join(f'tl.fromTo("#sinais-s{i}",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:0.3,ease:"back.out(1.6)"}},{t(k)-ini-0.1:.2f});tl.to("#sinais-s{i}",{{background:"#D45F2B",color:"#fff",duration:0.25}},{t(k)-ini+0.35:.2f});' for i,(_,_,k) in enumerate(SIN))}
  tl.fromTo("#sinais-med",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.35,ease:"back.out(1.6)"}},{t(121)-ini:.2f});
  {meta_js("sinais", 10, 100, t(125)-ini, 0.9)}
  tl.fromTo("#sinais-trat",{{opacity:0}},{{opacity:1,duration:0.3}},{t(131)-ini:.2f});
""")

# 8. resumo (45.95 – 53.25)
ini, fim = 45.95, 53.25
d = add("resumo", ini, fim)
wh, wj = wipe("resumo", BRANCO)
txt = "Entendi! Ronco de vez em quando é barulho. Com pausa, engasgo e cansaço, é sinal de alerta: hora do médico."
cena("resumo", d, """
  .bg{background:var(--creme);}
  .balao .txt{font-size:52px;}
""", f"""
  <div class="bg"></div>
  <div class="balao" id="resumo-balao"><div class="rot">💡 O QUE O TITO ENTENDEU</div>
    <div class="txt">{palavras_html("resumo", txt, 0, (9, 10, 12, 14, 15, 16, 17, 18, 19))}</div><div class="rabo"></div></div>
  <div class="tito-grande" id="resumo-tito">{tito_svg("resumo", bracos="acena")}</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#resumo-balao",{{opacity:0,y:30,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"back.out(1.6)"}},0.12);
  tl.fromTo("#resumo-tito",{{opacity:0,y:120}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.4)"}},0.05);
  {palavras_js("resumo", txt, ini, 46.12, 52.95)}
  {fala_js("resumo", round(46.12 - ini, 2), round(52.95 - ini, 2))}
""")

# 9. resposta + eco (53.25 – 55.8)
ini, fim = 53.25, 55.8
d = add("resposta", ini, fim)
wh, wj = wipe("resposta", CREME)
cena("resposta", d, f"""
  .bg{{background:{PESS};}}
  .titulo{{color:var(--verde);top:240px;font-size:104px;}}
  .titulo em{{color:var(--laranja);}}
  #resposta-img{{left:240px;top:640px;width:600px;height:620px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="resposta-t">Ronco é só barulho? <em>Às vezes, não.</em></h1>
  <div class="img" id="resposta-img"><img src="assets/tito-ronco.png"></div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#resposta-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.12);
  tl.fromTo("#resposta-t em",{{scale:1}},{{scale:1.06,duration:0.18,yoyo:true,repeat:1}},{t(161)-ini:.2f});
  tl.fromTo("#resposta-img",{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.4,ease:"back.out(1.6)"}},0.2);
""")

# 10. CTA (55.8 – fim)
ini, fim = 55.8, TOTAL
d = add("cta", ini, fim)
wh, wj = wipe("cta", CREME)
src4 = (SCR / "build_cafe.py").read_text()
cta_src = src4[src4.index('cena("cta", d, """'):src4.index("# ---------- legendas do narrador")]
cta_src = (cta_src
    .replace(".bg{background:var(--laranja);}", ".bg{background:var(--verde);}\n  #cta-tito{filter:drop-shadow(0 0 2px #FDF3ED) drop-shadow(0 0 2px #FDF3ED);}")  # Tito não some no fundo
    .replace("Manda pra quem diz que <em>café faz mal</em>", "Manda pra quem ronca <em>e jura que não</em>")
    .replace('"☕ 3 xícaras!"', "😴 RONCO")
    .replace("#cta-eco{position:absolute;inset:0;background:var(--mostarda);}", "#cta-eco{position:absolute;inset:0;background:#F7E5DD;}")
    .replace("#cta-eco .titulo{color:var(--verde);top:240px;font-size:128px;}", "#cta-eco .titulo{color:var(--verde);top:330px;font-size:124px;}")
    .replace("#cta-eco .titulo em{color:#8E3412;}", "#cta-eco .titulo em{color:var(--laranja);}")
    .replace('<div id="cta-eco-c"></div><h1 class="titulo">Café <em>faz mal?</em></h1>', '<h1 class="titulo">Ronco: <em>só barulho?</em></h1>')
    .replace("assets/tito-cafe.png", "assets/tito-ronco.png")
    .replace("#cta-eco-img{left:300px;top:500px;width:480px;height:570px;}", "#cta-eco-img{left:200px;top:650px;width:680px;height:700px;}")
    .replace("t(165)-ini-0.05", "t(182)-ini-0.1").replace("t(165)-ini+0.45", "t(183)-ini+0.15")
    .replace("TOTAL-ini-2.1", "TOTAL-ini-2.3")
    .replace("t(165)", "t(183)").replace("t(159)", "t(176)").replace("t(158)", "t(175)")
    .replace("t(148)", "t(166)").replace("t(149)", "t(167)").replace("t(152)", "t(171)"))
exec(cta_src)

GRUPOS = [
    ("O Tito tem uma *meta*:", 0, 5), ("*parar de roncar* em uma semana.", 5, 6),
    ("*Nem sempre.*", 17, 2), ("Em São Paulo, um estudo com *exame do sono*", 19, 9), ("encontrou *apneia*", 28, 2), ("em *quase 1 em cada 3 adultos*.", 30, 7),
    ("Na apneia, *a garganta fecha* durante o sono", 37, 8), ("e *a respiração para* por alguns segundos,", 45, 7), ("*várias vezes* por noite.", 52, 4),
    ("Esse é o *atalho que engana*.", 65, 6), ("*Dormir de lado* e *evitar álcool* à noite", 71, 8), ("*podem diminuir* o ronco.", 79, 4),
    ("Mas, *se for apneia*,", 83, 4), ("*só o truque não resolve*.", 87, 5),
    ("O que destrava é *olhar os sinais*:", 92, 7), ("*ronco alto* quase toda noite,", 99, 5), ("*pausas na respiração*", 104, 3), ("que alguém percebe,", 107, 3),
    ("acordar *engasgado*", 110, 2), ("e *sono demais* durante o dia.", 112, 6),
    ("Com esses sinais, o caminho é", 118, 6), ("*o médico e o exame do sono*.", 124, 7), ("E a apneia *tem tratamento*.", 131, 5),
    ("Então, *ronco é só barulho?*", 156, 5), ("*Às vezes, não.*", 161, 3),
    ("*Isso aí.*", 164, 2), ("Manda pra quem ronca *e jura que não*.", 166, 8), ("E *curte*,", 174, 2),
    ("*comenta RONCO* se alguém aí ronca", 176, 6), ("e *segue pra mais!*", 182, 4),
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
