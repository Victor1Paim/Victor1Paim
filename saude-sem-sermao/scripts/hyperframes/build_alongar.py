#!/usr/bin/env python3
"""Projeto HyperFrames: "Alongar antes do treino evita lesão?" (Saúde sem Sermão).
Reaproveita a base (paleta, Tito em SVG, balões, legendas) do build do vídeo do sono."""
import json, math, re, shutil
from pathlib import Path

SCR = Path("/tmp/claude-0/-home-user-Victor1Paim/bc508778-dc0e-5c3d-a4a6-a9dce8035bd2/scratchpad")
POST = Path("/home/user/Victor1Paim/saude-sem-sermao/producoes/alongar-antes-do-treino")
V = POST / "video"
(V / "compositions").mkdir(parents=True, exist_ok=True)
(V / "assets").mkdir(exist_ok=True)
for f in ["hyperframes.json", "package.json", "meta.json"]:
    t = (SCR / "hfblank" / f).read_text().replace('"hfblank"', '"saude-sem-sermao-alongar"')
    (V / f).write_text(t)
shutil.copy(POST / "dialogo-a.mp3", V / "assets/voz.mp3")
for n in ["tito-alongando", "tito-agachamento", "tito-equilibrio"]:
    shutil.copy(POST / "imagens" / f"{n}.png", V / "assets" / f"{n}.png")

W, H = 1080, 1920
TOTAL = 40.6
words = json.loads((POST / "conferencia/dialogo-a.palavras.json").read_text())
CENAS = []

# base comum (BASE_CSS, tito_svg, fala_js, palavras_html, tempos_palavras, palavras_js, cena, add, cena_tito)
src = (SCR / "build_sono.py").read_text()
exec(src[src.index("# ---------- paleta e base"):src.index("# ---------- 1. capa")])
exec(src[src.index("def cena_tito"):src.index("# ---------- 2. Tito: culpa")])
BASE_CSS += """
  .wipe{position:absolute;inset:0;z-index:50;}
  .img{position:absolute;}
  .img img{width:100%;height:100%;object-fit:contain;display:block;}
  .card{position:absolute;background:#fff;border-radius:28px;box-shadow:0 14px 40px rgba(80,40,20,.12);}
"""


def t(i):
    return words[i]["inicio"]


def wipe(cid, cor):
    """Transição: a cor da cena anterior sai empurrada para a esquerda (mesma direção em todo o vídeo)."""
    return (f'<div class="wipe" id="{cid}-wipe" style="background:{cor}"></div>',
            f'tl.fromTo("#{cid}-wipe",{{xPercent:0}},{{xPercent:-100,duration:0.38,ease:"power3.inOut"}},0);')


def contador(sel, de, ate, ini, dur, fmt="int"):
    f = "Math.round(o.v).toLocaleString('pt-BR')" if fmt == "milhar" else "Math.round(o.v)"
    return (f'(function(){{const o={{v:{de}}};const el=document.querySelector("{sel}");'
            f'tl.fromTo(o,{{v:{de}}},{{v:{ate},duration:{dur},ease:"power2.out",onUpdate:()=>{{el.textContent={f};}}}},{ini:.2f});}})();')


VERDE, CREME, BRANCO, LARANJA, PESSEGO = "#2F483A", "#FDF3ED", "#FFFFFF", "#D45F2B", "#F7E5DD"

# ---------- 1. capa (0 – 2.2) ----------
ini, fim = 0, 2.2
d = add("capa", ini, fim)
cena("capa", d, """
  .bg{background:var(--verde);}
  .titulo{color:var(--creme2);top:230px;font-size:100px;}
  .titulo em{color:var(--mostarda);}
  #capa-img{left:270px;top:540px;width:540px;height:620px;}
  #capa-selo{position:absolute;left:790px;top:520px;width:170px;height:170px;border-radius:50%;background:var(--laranja);
     color:#fff;font-family:'Playfair Display',serif;font-weight:700;font-size:80px;display:flex;align-items:center;justify-content:center;}
""", """
  <div class="bg"></div>
  <h1 class="titulo">Alongar antes do treino <em id="capa-em" style="display:inline-block">evita lesão?</em></h1>
  <div class="img" id="capa-img"><img src="assets/tito-alongando.png"></div>
  <div id="capa-selo">?!</div>
""", f"""
  tl.fromTo("#capa-img",{{rotation:-4,transformOrigin:"50% 95%"}},{{rotation:4,duration:0.55,ease:"sine.inOut",yoyo:true,repeat:3}},0);
  tl.fromTo("#capa-selo",{{scale:0,rotation:-30}},{{scale:1,rotation:0,duration:0.4,ease:"back.out(2.4)"}},{t(4):.2f});
  tl.fromTo("#capa-em",{{scale:1,transformOrigin:"0% 50%"}},{{scale:1.07,duration:0.2,yoyo:true,repeat:1,ease:"power2.out"}},{t(4):.2f});
""")

# ---------- 2. Tito: dúvida (2.2 – 5.55) ----------
ini, fim = 2.2, 5.55
d = add("duvida", ini, fim)
txt = "Eu sempre alongo 10 minutos antes. Tô perdendo tempo?"
wh, wj = wipe("duvida", VERDE)
cena("duvida", d, """
  .bg{background:var(--creme);}
  #duvida-rel{position:absolute;left:760px;top:600px;width:240px;height:240px;}
  #duvida-num{position:absolute;left:760px;top:845px;width:240px;text-align:center;font-weight:900;font-size:44px;color:var(--laranja);}
""", f"""
  <div class="bg"></div>
  <div class="balao" id="duvida-balao"><div class="rot">💬 PERGUNTA DO TITO</div>
    <div class="txt">{palavras_html("duvida", txt, 0, (3, 4, 8))}</div><div class="rabo"></div></div>
  <div class="tito-grande" id="duvida-tito" style="left:120px">{tito_svg("duvida")}</div>
  <svg id="duvida-rel" viewBox="0 0 100 100"><circle cx="50" cy="54" r="40" fill="#fff" stroke="#2F483A" stroke-width="6"/>
    <rect x="44" y="4" width="12" height="10" rx="3" fill="#2F483A"/>
    <path id="duvida-arco" d="M50 54 L50 18 A36 36 0 0 1 86 54 Z" fill="#D45F2B" opacity=".9"/>
    <line id="duvida-pont" x1="50" y1="54" x2="50" y2="22" stroke="#2B2B2B" stroke-width="5" stroke-linecap="round"/></svg>
  <div id="duvida-num">10 min</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#duvida-balao",{{opacity:0,y:30,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"back.out(1.6)"}},0.15);
  tl.fromTo("#duvida-tito",{{opacity:0,y:120}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.4)"}},0.1);
  {palavras_js("duvida", txt, ini, 2.26, 5.32)}
  {fala_js("duvida", round(2.26 - ini, 2), round(5.32 - ini, 2))}
  tl.fromTo("#duvida-rel",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"}},{t(10)-ini:.2f});
  tl.fromTo("#duvida-pont",{{rotation:0,svgOrigin:"50 54"}},{{rotation:360,duration:1.6,ease:"power1.inOut"}},{t(10)-ini:.2f});
  tl.fromTo("#duvida-num",{{opacity:0}},{{opacity:1,duration:0.2}},{t(11)-ini:.2f});
""")

# ---------- 3. o estudo (5.55 – 12.2) ----------
ini, fim = 5.55, 12.2
d = add("estudo", ini, fim)
wh, wj = wipe("estudo", CREME)
pontos = []
for k in range(60):
    r, c = divmod(k, 12)
    pontos.append(f'<div class="pt" id="estudo-p{k}" style="left:{100 + c*74}px;top:{650 + r*58}px"></div>')
pontos_js = " ".join(f'tl.fromTo("#estudo-p{k}",{{scale:0}},{{scale:1,duration:0.25,ease:"back.out(2)"}},{t(24)-ini + (k%12)*0.025 + (k//12)*0.05:.2f});' for k in range(60))
cards = [("alongamento", "🧘", "Alongamento"), ("forca", "🏋️", "Força"), ("equil", "🦩", "Equilíbrio")]
cards_html = "".join(f'<div class="card est-c" id="estudo-{c}" style="left:{80 + i*318}px;top:960px;width:290px;height:90px">'
                     f'<span>{e}</span> {n}</div>' for i, (c, e, n) in enumerate(cards))
cena("estudo", d, """
  .bg{background:#fff;}
  .tag{background:#5F6E52;color:#fff;}
  .num{position:absolute;font-family:'Playfair Display',serif;font-weight:700;font-size:120px;color:var(--laranja);line-height:1;}
  .numl{position:absolute;font-weight:900;font-size:40px;color:#6b6460;}
  .pt{position:absolute;width:44px;height:44px;border-radius:50%;background:#95A185;}
  .est-c{display:flex;align-items:center;justify-content:center;gap:10px;font-weight:900;font-size:36px;}
  .fonte{top:1075px;}
""", f"""
  <div class="bg"></div>
  <div class="tag" id="estudo-tag">✓ CIÊNCIA</div>
  <h1 class="titulo" id="estudo-t">O que <em>previne</em> lesão?</h1>
  <div class="num" id="estudo-n1" style="left:80px;top:410px">0</div><div class="numl" id="estudo-l1" style="left:84px;top:540px">estudos</div>
  <div class="num" id="estudo-n2" style="left:480px;top:410px">0</div><div class="numl" id="estudo-l2" style="left:484px;top:540px">pessoas</div>
  {''.join(pontos)}
  {cards_html}
  <div class="fonte" id="estudo-fonte">Fonte: Lauersen et al., Br J Sports Med, 2014</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#estudo-tag",{{opacity:0,y:-10}},{{opacity:1,y:0,duration:0.3}},0.3);
  tl.fromTo("#estudo-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.3);
  tl.fromTo("#estudo-n1",{{opacity:0}},{{opacity:1,duration:0.2}},{t(19)-ini-0.1:.2f});
  tl.fromTo("#estudo-l1",{{opacity:0}},{{opacity:1,duration:0.2}},{t(20)-ini:.2f});
  {contador("#estudo-n1", 0, 25, t(19)-ini-0.1, 0.9)}
  tl.fromTo("#estudo-n2",{{opacity:0}},{{opacity:1,duration:0.2}},{t(24)-ini-0.1:.2f});
  tl.fromTo("#estudo-l2",{{opacity:0}},{{opacity:1,duration:0.2}},{t(26)-ini:.2f});
  {contador("#estudo-n2", 0, 26610, t(24)-ini-0.1, 1.2, "milhar")}
  {pontos_js}
  {' '.join(f'tl.fromTo("#estudo-{c}",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.35,ease:"back.out(1.6)"}},{t(27)-ini + i*0.18:.2f});' for i,(c,_,_) in enumerate(cards))}
  tl.fromTo("#estudo-fonte",{{opacity:0}},{{opacity:1,duration:0.4}},{t(19)-ini:.2f});
""")

# ---------- 4. alongamento: quase nada (12.2 – 15.5) ----------
ini, fim = 12.2, 15.5
d = add("mito", ini, fim)
wh, wj = wipe("mito", BRANCO)
cena("mito", d, """
  .bg{background:var(--laranja);}
  .titulo{color:#fff;top:300px;}
  .titulo em{color:var(--creme2);}
  #mito-selo{position:absolute;left:80px;top:200px;padding:8px 22px;border:5px solid #fff;border-radius:14px;color:#fff;
             font-weight:900;font-size:40px;letter-spacing:.1em;}
  .rot{position:absolute;left:80px;font-weight:900;font-size:36px;color:#fff;}
  .trilho{position:absolute;left:80px;width:920px;height:80px;border-radius:20px;background:rgba(255,255,255,.18);}
  .barra{position:absolute;left:80px;width:920px;height:80px;border-radius:20px;transform-origin:0% 50%;}
  .pct{position:absolute;font-weight:900;font-size:48px;color:#fff;}
  #mito-img{right:30px;top:1290px;width:330px;height:390px;}
  #mito-quase{position:absolute;left:80px;top:990px;font-weight:900;font-size:44px;color:var(--creme2);}
""", f"""
  <div class="bg"></div>
  <div id="mito-selo">✕ MITO</div>
  <h1 class="titulo" id="mito-t">Alongar <em>sozinho</em>?</h1>
  <div class="rot" style="top:530px">sem prevenção</div>
  <div class="trilho" style="top:585px"></div><div class="barra" id="mito-b0" style="top:585px;background:#8C8580"></div>
  <div class="pct" style="left:870px;top:595px">100</div>
  <div class="rot" style="top:740px">com alongamento</div>
  <div class="trilho" style="top:795px"></div><div class="barra" id="mito-b1" style="top:795px;background:#fff"></div>
  <div class="pct" id="mito-p1" style="left:870px;top:805px;color:var(--laranja)">100</div>
  <div id="mito-quase">−4%: quase nada</div>
  <div class="img" id="mito-img"><img src="assets/tito-alongando.png"></div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#mito-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.25);
  tl.fromTo("#mito-b0",{{scaleX:0}},{{scaleX:1,duration:0.5,ease:"power2.out"}},0.4);
  tl.fromTo("#mito-b1",{{scaleX:0}},{{scaleX:1,duration:0.5,ease:"power2.out"}},0.6);
  tl.to("#mito-b1",{{scaleX:0.96,duration:0.6,ease:"power2.inOut"}},1.15);
  {contador("#mito-p1", 100, 96, 1.15, 0.6)}
  tl.fromTo("#mito-selo",{{opacity:0,scale:2.4,rotation:-14}},{{opacity:1,scale:1,rotation:-6,duration:0.22,ease:"power4.in"}},{t(37)-ini:.2f});
  tl.fromTo("#mito-shake",{{x:0}},{{x:0,duration:0.01}},0);
  tl.fromTo("#root",{{x:0}},{{x:10,duration:0.04,yoyo:true,repeat:5,ease:"none"}},{t(37)-ini+0.22:.2f});
  tl.fromTo("#mito-quase",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3}},1.8);
  tl.fromTo("#mito-img",{{opacity:0,y:80}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.5)"}},0.5);
  tl.to("#mito-img",{{rotation:-5,transformOrigin:"50% 95%",duration:0.5,yoyo:true,repeat:3,ease:"sine.inOut"}},1.0);
""".replace('tl.fromTo("#mito-shake",{x:0},{x:0,duration:0.01},0);\n', ''))

# ---------- 5. Tito: e o que fez? (15.5 – 17.3) ----------
ini, fim = 15.5, 17.3
d = add("oque", ini, fim)
txt = "Ué, e o que fez?"
wh, wj = wipe("oque", LARANJA)
cena("oque", d, """
  .bg{background:var(--creme);}
  .balao .txt{font-size:72px;}
""", f"""
  <div class="bg"></div>
  <div class="balao" id="oque-balao"><div class="rot">💬 PERGUNTA DO TITO</div>
    <div class="txt">{palavras_html("oque", txt, 0, (4,))}</div><div class="rabo"></div></div>
  <div class="tito-grande" id="oque-tito">{tito_svg("oque", olhos="duvida")}</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#oque-balao",{{opacity:0,y:30,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.3,ease:"back.out(1.6)"}},0.12);
  tl.fromTo("#oque-tito",{{opacity:0,y:120}},{{opacity:1,y:0,duration:0.4,ease:"back.out(1.4)"}},0.05);
  {palavras_js("oque", txt, ini, 15.7, 17.0)}
  {fala_js("oque", round(15.7 - ini, 2), round(17.0 - ini, 2))}
  tl.fromTo("#oque-tito",{{rotation:0,transformOrigin:"50% 90%"}},{{rotation:-6,duration:0.25,yoyo:true,repeat:1,ease:"sine.inOut"}},{16.3-ini:.2f});
""")

# ---------- 6. força e equilíbrio (17.3 – 24.6) ----------
ini, fim = 17.3, 24.6
d = add("forca", ini, fim)
wh, wj = wipe("forca", CREME)
linhas = [("f0", "Alongamento", 0.96, "#B9B0A9", "96"), ("f1", "Força", 0.32, "#D45F2B", "32"), ("f2", "Equilíbrio", 0.55, "#2F483A", "55")]
barras_html = ""
for i, (k, nome, v, cor, p) in enumerate(linhas):
    y = 500 + i * 170
    barras_html += (f'<div class="rot2" style="top:{y}px">{nome}</div>'
                    f'<div class="trilho2" style="top:{y+50}px"></div>'
                    f'<div class="barra2" id="forca-{k}" style="top:{y+50}px;background:{cor}"></div>'
                    f'<div class="pct2" id="forca-p{k}" style="top:{y+56}px">100</div>')
confete = []
cores = ["#E2B04A", "#2F483A", "#95A185", "#D45F2B", "#F2ECE2"]
for i in range(18):
    ang = i * 360 / 18
    confete.append((i, cores[i % 5], math.cos(math.radians(ang)) * (120 + (i % 3) * 50), math.sin(math.radians(ang)) * (100 + (i % 4) * 30)))
cena("forca", d, f"""
  .bg{{background:#fff;}}
  .rot2{{position:absolute;left:80px;font-weight:900;font-size:40px;}}
  .trilho2{{position:absolute;left:80px;width:760px;height:76px;border-radius:20px;background:#F2ECE2;}}
  .barra2{{position:absolute;left:80px;width:760px;height:76px;border-radius:20px;transform-origin:0% 50%;}}
  .pct2{{position:absolute;left:860px;font-weight:900;font-size:52px;color:#2B2B2B;}}
  .leg2{{position:absolute;left:80px;top:445px;font-weight:800;font-size:30px;color:#8a837d;}}
  #forca-terco{{position:absolute;left:400px;top:700px;padding:8px 22px;border-radius:999px;background:var(--verde);color:#fff;font-weight:900;font-size:38px;}}
  #forca-metade{{position:absolute;left:520px;top:870px;padding:8px 22px;border-radius:999px;background:#5F6E52;color:#fff;font-weight:900;font-size:38px;}}
  .cf{{position:absolute;left:330px;top:720px;width:20px;height:30px;border-radius:5px;opacity:0;}}
  #forca-agach{{right:20px;top:1300px;width:360px;height:420px;}}
  #forca-equil{{right:0px;top:1310px;width:420px;height:380px;opacity:0;}}
  .fonte{{top:1050px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="forca-t1">Treino de <em>força</em></h1>
  <h1 class="titulo" id="forca-t2" style="opacity:0">Força e <em>equilíbrio</em></h1>
  <div class="leg2" id="forca-leg">lesões a cada 100 (sem prevenção = 100)</div>
  {barras_html}
  <div id="forca-terco">≈ 1/3</div>
  <div id="forca-metade">quase metade</div>
  {''.join(f'<div class="cf" id="forca-cf{i}" style="background:{c}"></div>' for i, c, _, _ in confete)}
  <div class="fonte" id="forca-fonte">Fonte: Lauersen et al., Br J Sports Med, 2014</div>
  <div class="img" id="forca-agach"><img src="assets/tito-agachamento.png"></div>
  <div class="img" id="forca-equil"><img src="assets/tito-equilibrio.png"></div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#forca-t1",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(47)-ini:.2f});
  tl.fromTo("#forca-leg",{{opacity:0}},{{opacity:1,duration:0.3}},0.5);
  {' '.join(f'tl.fromTo("#forca-{k}",{{scaleX:0}},{{scaleX:1,duration:0.45,ease:"power2.out"}},{0.3+i*0.1:.2f});' for i,(k,_,_,_,_) in enumerate(linhas))}
  tl.set("#forca-f0",{{scaleX:0.96}},0.9); tl.set("#forca-pf0",{{textContent:"96"}},0.9);
  tl.to("#forca-f1",{{scaleX:0.32,duration:0.9,ease:"power3.inOut"}},{t(52)-ini:.2f});
  {contador("#forca-pf1", 100, 32, t(52)-ini, 0.9)}
  tl.fromTo("#forca-terco",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.4)"}},{t(56)-ini:.2f});
  {' '.join(f'tl.fromTo("#forca-cf{i}",{{opacity:1,x:0,y:0,rotation:0}},{{immediateRender:false,opacity:0,x:{dx:.0f},y:{dy:.0f},rotation:{(i*53)%360},duration:0.9,ease:"power2.out"}},{t(56)-ini:.2f});' for i,_,dx,dy in confete)}
  tl.fromTo("#forca-agach",{{opacity:0,x:120}},{{opacity:1,x:0,duration:0.45,ease:"back.out(1.4)"}},{t(47)-ini:.2f});
  tl.fromTo("#forca-agach",{{y:0,scaleY:1,transformOrigin:"50% 100%"}},{{y:30,scaleY:0.9,duration:0.42,ease:"sine.inOut",yoyo:true,repeat:5}},{t(49)-ini:.2f});
  tl.to("#forca-t1",{{opacity:0,y:-20,duration:0.25}},{t(58)-ini-0.15:.2f});
  tl.fromTo("#forca-t2",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(58)-ini:.2f});
  tl.to("#forca-agach",{{opacity:0,x:-60,duration:0.3}},{t(60)-ini-0.1:.2f});
  tl.fromTo("#forca-equil",{{opacity:0,x:120}},{{opacity:1,x:0,duration:0.4,ease:"back.out(1.4)"}},{t(60)-ini:.2f});
  tl.fromTo("#forca-equil",{{rotation:-5,transformOrigin:"55% 100%"}},{{rotation:5,duration:0.5,ease:"sine.inOut",yoyo:true,repeat:3}},{t(60)-ini+0.4:.2f});
  tl.to("#forca-f2",{{scaleX:0.55,duration:0.8,ease:"power3.inOut"}},{t(63)-ini:.2f});
  {contador("#forca-pf2", 100, 55, t(63)-ini, 0.8)}
  tl.fromTo("#forca-metade",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.4)"}},{t(65)-ini:.2f});
  tl.fromTo("#forca-fonte",{{opacity:0}},{{opacity:1,duration:0.4}},{t(58)-ini:.2f});
""")

# ---------- 7. não é escudo (24.6 – 29.65) ----------
ini, fim = 24.6, 29.65
d = add("escudo", ini, fim)
wh, wj = wipe("escudo", BRANCO)
cena("escudo", d, """
  .bg{background:var(--pessego);}
  #escudo-img{left:120px;top:560px;width:420px;height:500px;}
  #escudo-flex{position:absolute;left:150px;top:1070px;padding:8px 22px;border-radius:999px;background:#5F6E52;color:#fff;font-weight:900;font-size:36px;}
  #escudo-sh{position:absolute;left:600px;top:560px;width:380px;height:440px;}
  #escudo-x{position:absolute;left:600px;top:560px;width:380px;height:440px;}
  #escudo-rot{position:absolute;left:560px;top:1020px;width:460px;text-align:center;font-weight:900;font-size:36px;color:var(--laranja);}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="escudo-t1">Alongar <em>não faz mal</em></h1>
  <h1 class="titulo" id="escudo-t2" style="opacity:0">Só não é <em>escudo</em></h1>
  <div class="img" id="escudo-img"><img src="assets/tito-alongando.png"></div>
  <div id="escudo-flex">flexibilidade ✓</div>
  <svg id="escudo-sh" viewBox="0 0 100 116"><path d="M50 4 L92 20 L92 56 C92 84 72 104 50 112 C28 104 8 84 8 56 L8 20 Z" fill="#95A185" stroke="#2F483A" stroke-width="5"/>
    <path d="M50 22 L76 32 L76 58 C76 76 64 90 50 95 C36 90 24 76 24 58 L24 32 Z" fill="#F2ECE2"/></svg>
  <svg id="escudo-x" viewBox="0 0 100 116"><path id="escudo-x1" d="M18 26 L82 96" stroke="#D45F2B" stroke-width="12" stroke-linecap="round"/>
    <path id="escudo-x2" d="M82 26 L18 96" stroke="#D45F2B" stroke-width="12" stroke-linecap="round"/></svg>
  <div id="escudo-rot">contra lesão</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#escudo-t1",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(67)-ini:.2f});
  tl.fromTo("#escudo-img",{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.5)"}},0.35);
  tl.fromTo("#escudo-img",{{rotation:-5,transformOrigin:"50% 95%"}},{{rotation:5,duration:0.6,ease:"sine.inOut",yoyo:true,repeat:3}},0.8);
  tl.fromTo("#escudo-flex",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.2)"}},{t(74)-ini:.2f});
  tl.to("#escudo-t1",{{opacity:0,y:-20,duration:0.25}},{t(75)-ini-0.15:.2f});
  tl.fromTo("#escudo-t2",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(75)-ini:.2f});
  tl.fromTo("#escudo-sh",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.4,ease:"back.out(1.8)"}},{t(79)-ini-0.1:.2f});
  tl.fromTo("#escudo-x1",{{drawSVG:0,opacity:0}},{{opacity:1,duration:0.01}},{t(80)-ini:.2f});
  tl.fromTo("#escudo-x1",{{scale:0,svgOrigin:"50 61"}},{{scale:1,duration:0.18,ease:"power3.out"}},{t(80)-ini:.2f});
  tl.fromTo("#escudo-x2",{{scale:0,svgOrigin:"50 61",opacity:0}},{{scale:1,opacity:1,duration:0.18,ease:"power3.out"}},{t(80)-ini+0.12:.2f});
  tl.fromTo("#escudo-sh",{{rotation:0,transformOrigin:"50% 50%"}},{{rotation:4,duration:0.05,yoyo:true,repeat:5}},{t(80)-ini+0.3:.2f});
  tl.fromTo("#escudo-rot",{{opacity:0}},{{opacity:1,duration:0.3}},{t(81)-ini:.2f});
""".replace('tl.fromTo("#escudo-x1",{drawSVG:0,opacity:0},{opacity:1,duration:0.01},', 'tl.fromTo("#escudo-x1",{opacity:0},{opacity:1,duration:0.01},'))

# ---------- 8. resumo do Tito (29.65 – 36.15) ----------
ini, fim = 29.65, 36.15
d = add("resumo", ini, fim)
txt = "Entendi! Alongar pode, mas quem protege mesmo é músculo forte. Vou incluir uns agachamentos no treino!"
wh, wj = wipe("resumo", PESSEGO)
cena("resumo", d, """
  .bg{background:var(--creme);}
  .balao .txt{font-size:54px;}
  #resumo-agach{left:250px;top:780px;width:560px;height:650px;opacity:0;}
""", f"""
  <div class="bg"></div>
  <div class="balao" id="resumo-balao"><div class="rot">💡 O QUE O TITO ENTENDEU</div>
    <div class="txt">{palavras_html("resumo", txt, 0, (1, 2, 8, 9, 13))}</div><div class="rabo"></div></div>
  <div class="tito-grande" id="resumo-tito">{tito_svg("resumo", bracos="acena")}</div>
  <div class="img" id="resumo-agach"><img src="assets/tito-agachamento.png"></div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#resumo-balao",{{opacity:0,y:30,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"back.out(1.6)"}},0.12);
  tl.fromTo("#resumo-tito",{{opacity:0,y:120}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.4)"}},0.05);
  {palavras_js("resumo", txt, ini, 29.84, 35.94)}
  {fala_js("resumo", round(29.84 - ini, 2), round(34.1 - ini, 2))}
  tl.to("#resumo-tito",{{opacity:0,scale:0.9,duration:0.2}},{t(96)-ini-0.1:.2f});
  tl.fromTo("#resumo-agach",{{opacity:0,scale:0.9}},{{opacity:1,scale:1,duration:0.25,ease:"back.out(1.6)"}},{t(96)-ini:.2f});
  tl.fromTo("#resumo-agach",{{y:0,scaleY:1,transformOrigin:"50% 100%"}},{{y:40,scaleY:0.9,duration:0.4,ease:"sine.inOut",yoyo:true,repeat:1}},{t(96)-ini+0.3:.2f});
""")

# ---------- 9. CTA (36.15 – fim) ----------
ini, fim = 36.15, TOTAL
d = add("cta", ini, fim)
wh, wj = wipe("cta", CREME)
cta_src = src[src.index('cena("cta", d, """'):src.index("# ---------- legendas do narrador")]
cta_src = cta_src.replace("34.3-ini", f"{t(102)-0.1:.2f}-ini").replace("35.05-ini", f"{t(103)+0.1:.2f}-ini") \
                 .replace("35.12-ini", f"{t(103)+0.17:.2f}-ini").replace("35.15-ini", f"{t(103)+0.2:.2f}-ini")
cta_src = cta_src.replace('<div class="tito-mini" id="cta-tito">', wh + '\n  <div class="tito-mini" id="cta-tito">')
cta_src = cta_src.replace('tl.fromTo("#cta-t",', wj.replace('{','{{').replace('}','}}') + '\n  tl.fromTo("#cta-t",')
confete = []
cores = ["#E2B04A", "#2F483A", "#FDF3ED", "#95A185", "#D45F2B"]
for i in range(14):
    ang = i * 360 / 14
    confete.append((i, cores[i % 5], math.cos(math.radians(ang)) * (140 + (i % 3) * 40), math.sin(math.radians(ang)) * (90 + (i % 4) * 25)))
exec(cta_src)

# ---------- legendas do narrador ----------
GRUPOS = [
    ("Alongar antes do *treino*", 0, 4), ("*evita a lesão?*", 4, 3),
    ("Uma análise de *25 estudos*,", 16, 5), ("com mais de *26 mil pessoas*,", 21, 6),
    ("comparou formas de *prevenir lesão*", 27, 5), ("no esporte.", 32, 2),
    ("O *alongamento*, sozinho,", 34, 3), ("*quase não* fez diferença.", 37, 4),
    ("O treino de *força*.", 46, 4), ("As lesões caíram", 50, 3), ("para cerca de *um terço*.", 53, 5),
    ("Treino de *equilíbrio* também ajudou,", 58, 5), ("cortando *quase pela metade*.", 63, 4),
    ("Alongar *não faz mal*", 67, 4), ("e ajuda na *flexibilidade*.", 71, 4),
    ("Só não é o *escudo*", 75, 5), ("contra a lesão.", 80, 3),
    ("*Resumiu bem.*", 99, 2), ("Curtiu? Então *segue a gente*", 101, 5),
]
for txt_, i0, n in GRUPOS:
    a = " ".join(w["palavra"] for w in words[i0:i0 + n])
    print(f"{txt_!r:44} <- {a!r}")
leg_html, leg_js = [], []
for k, (txt_, i0, n) in enumerate(GRUPOS):
    a = max(words[i0]["inicio"] - 0.08, 0.15)
    b = words[i0 + n - 1]["fim"] + 0.18
    if k + 1 < len(GRUPOS) and GRUPOS[k + 1][1] == i0 + n:
        b = min(b, words[GRUPOS[k + 1][1]]["inicio"] - 0.1)
    html = re.sub(r"\*(.+?)\*", r'<b>\1</b>', txt_)
    leg_html.append(f'<div class="leg" id="leg-{k}">{html}</div>')
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

hosts = []
for cid, a, b in CENAS:
    hosts.append(f'''      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html"
        data-start="{a}" data-duration="{round(b - a, 2)}" data-track-index="1" data-track-kind="graphics"
        data-width="{W}" data-height="{H}" style="z-index:1"></div>''')
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
      <audio id="voz" class="clip" src="assets/voz.mp3" data-start="0" data-track-index="3" data-volume="1" data-fade-out="0.3"></audio>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print("ok", [c[0] for c in CENAS])
