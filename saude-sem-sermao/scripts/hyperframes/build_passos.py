#!/usr/bin/env python3
"""Projeto HyperFrames: "10 mil passos por dia é regra?" (Saúde sem Sermão).
Base reaproveitada de build_sono.py (paleta, Tito SVG, balões, legendas) e build_alongar.py (wipe, contador)."""
import json, math, re, shutil
from pathlib import Path

SCR = Path("/tmp/claude-0/-home-user-Victor1Paim/bc508778-dc0e-5c3d-a4a6-a9dce8035bd2/scratchpad")
POST = Path("/home/user/Victor1Paim/saude-sem-sermao/producoes/10-mil-passos")
V = POST / "video"
(V / "compositions").mkdir(parents=True, exist_ok=True)
(V / "assets").mkdir(exist_ok=True)
for f in ["hyperframes.json", "package.json", "meta.json"]:
    (V / f).write_text((SCR / "hfblank" / f).read_text().replace('"hfblank"', '"saude-sem-sermao-10-mil-passos"'))
shutil.copy(POST / "dialogo.mp3", V / "assets/voz.mp3")
for n in ["tito-caminhando", "tito-celular"]:
    shutil.copy(POST / "imagens" / f"{n}.png", V / "assets" / f"{n}.png")

W, H = 1080, 1920
TOTAL = 55.3
words = json.loads((POST / "conferencia/dialogo.palavras.json").read_text())
CENAS = []

src = (SCR / "build_sono.py").read_text()
exec(src[src.index("# ---------- paleta e base"):src.index("# ---------- 1. capa")])
exec(src[src.index("def cena_tito"):src.index("# ---------- 2. Tito: culpa")])
src2 = (SCR / "build_alongar.py").read_text()
exec(src2[src2.index("BASE_CSS += "):src2.index("VERDE, CREME, BRANCO")])
VERDE, CREME, BRANCO, LARANJA, PESSEGO = "#2F483A", "#FDF3ED", "#FFFFFF", "#D45F2B", "#F7E5DD"


def tito_fala(cid, ini, fim, txt, fala_ini, fala_fim, destaque=(), olhos="normal", cor_ant=CREME, tam=60, extra_html="", extra_js=""):
    d = add(cid, ini, fim)
    wh, wj = wipe(cid, cor_ant)
    cena(cid, d, f"""
  .bg{{background:var(--creme);}}
  .balao .txt{{font-size:{tam}px;}}
""", f"""
  <div class="bg"></div>
  <div class="balao" id="{cid}-balao"><div class="rot">💬 PERGUNTA DO TITO</div>
    <div class="txt">{palavras_html(cid, txt, 0, destaque)}</div><div class="rabo"></div></div>
  <div class="tito-grande" id="{cid}-tito">{tito_svg(cid, olhos=olhos)}</div>
  {extra_html}
  {wh}
""", f"""
  {wj}
  tl.fromTo("#{cid}-balao",{{opacity:0,y:30,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.3,ease:"back.out(1.6)"}},0.12);
  tl.fromTo("#{cid}-tito",{{opacity:0,y:120}},{{opacity:1,y:0,duration:0.4,ease:"back.out(1.4)"}},0.05);
  {palavras_js(cid, txt, ini, fala_ini, fala_fim)}
  {fala_js(cid, round(fala_ini - ini, 2), round(fala_fim - ini, 2))}
  {extra_js}
""")


# ---------- gráfico de risco (reutilizado nas cenas 4 e 6) ----------
GX0, GX1, GY0, GY1 = 140, 980, 520, 1000   # área do gráfico (px)
PASSOS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
RISCO = [100, 85, 73, 64, 58, 53, 50, 49, 48, 47, 46.5]   # forma aproximada da curva (HR 0,53 em 7 mil; ~10% a menos em 10 mil)
gx = lambda p: GX0 + (p - 2) / 10 * (GX1 - GX0)
gy = lambda r: GY1 - (r - 40) / 60 * (GY1 - GY0)
pts = [(gx(p), gy(r)) for p, r in zip(PASSOS, RISCO)]
path = "M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts)
def grafico_svg(pref):
    eixo_x = "".join(f'<text x="{gx(p):.0f}" y="{GY1+48}" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="30" fill="#6b6460">{p}k</text>' for p in [2, 4, 6, 8, 10, 12])
    return f'''<svg class="graf" viewBox="0 0 {W} 1100" width="{W}" height="1100">
  <line x1="{GX0}" y1="{GY1}" x2="{GX1}" y2="{GY1}" stroke="#2B2B2B" stroke-width="5" stroke-linecap="round"/>
  <line x1="{GX0}" y1="{GY0-20}" x2="{GX0}" y2="{GY1}" stroke="#2B2B2B" stroke-width="5" stroke-linecap="round"/>
  <text x="{GX0-14}" y="{GY0-34}" font-family="Nunito" font-weight="900" font-size="28" fill="#8a837d">risco de morte</text>
  <text x="{GX1}" y="{GY1+92}" text-anchor="end" font-family="Nunito" font-weight="900" font-size="28" fill="#8a837d">passos por dia</text>
  {eixo_x}
  <path id="{pref}-curva" d="{path}" fill="none" stroke="#D45F2B" stroke-width="12" stroke-linecap="butt" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
</svg>'''


# ---------- 1. capa (0 – 3.95) ----------
ini, fim = 0, 3.95
d = add("capa", ini, fim)
cena("capa", d, """
  .bg{background:var(--verde);}
  .titulo{color:var(--creme2);top:230px;font-size:104px;}
  .titulo em{color:var(--mostarda);}
  #capa-cont{position:absolute;left:80px;top:470px;font-family:'Playfair Display',serif;font-weight:700;font-size:170px;color:var(--creme2);line-height:1;}
  #capa-risco{position:absolute;left:70px;top:555px;width:620px;height:16px;border-radius:8px;background:var(--laranja);transform-origin:0% 50%;}
  #capa-nao{position:absolute;left:84px;top:670px;font-weight:900;font-size:44px;color:var(--mostarda);}
  #capa-img{left:360px;top:690px;width:500px;height:470px;}
  .pe{position:absolute;width:46px;height:70px;border-radius:50%;background:rgba(242,236,226,.35);}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo">10 mil passos <em>é regra?</em></h1>
  <div id="capa-cont">10.000</div><div id="capa-risco"></div>
  <div id="capa-nao">não veio da ciência</div>
  {''.join(f'<div class="pe" id="capa-pe{i}" style="left:{90+i*130}px;top:{1180 + (i%2)*60}px;transform:rotate(80deg)"></div>' for i in range(7))}
  <div class="img" id="capa-img"><img src="assets/tito-caminhando.png"></div>
""", f"""
  tl.fromTo("#capa-img",{{y:0}},{{y:-18,duration:0.25,ease:"sine.inOut",yoyo:true,repeat:13}},0);
  {' '.join(f'tl.fromTo("#capa-pe{i}",{{opacity:0}},{{opacity:1,duration:0.15}},{0.2+i*0.35:.2f});' for i in range(7))}
  tl.fromTo("#capa-risco",{{scaleX:0}},{{scaleX:1,duration:0.35,ease:"power3.out"}},{t(7):.2f});
  tl.fromTo("#capa-nao",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3}},{t(7)+0.1:.2f});
""".replace('style="left:{90','style="left:{90'))
# a rotação dos pés fica em CSS estático (não animado), sem conflito com GSAP (só opacidade é animada)

# ---------- 2. Tito: cinco mil (3.95 – 8.0) ----------
ini, fim = 3.95, 8.0
d = add("cinco", ini, fim)
wh, wj = wipe("cinco", VERDE)
txt = "Ué! Eu mal chego a 5 mil. Então nem adianta?"
cena("cinco", d, """
  .bg{background:var(--creme);}
  #cinco-img{left:60px;top:640px;width:560px;height:680px;}
  #cinco-anel{position:absolute;left:640px;top:700px;width:360px;height:360px;}
  #cinco-num{position:absolute;left:640px;top:820px;width:360px;text-align:center;font-family:'Playfair Display',serif;font-weight:700;font-size:72px;color:#2B2B2B;}
  #cinco-meta{position:absolute;left:640px;top:910px;width:360px;text-align:center;font-weight:900;font-size:30px;color:#8a837d;}
""", f"""
  <div class="bg"></div>
  <div class="balao" id="cinco-balao"><div class="rot">💬 PERGUNTA DO TITO</div>
    <div class="txt">{palavras_html("cinco", txt, 0, (5, 6, 8, 9))}</div><div class="rabo"></div></div>
  <div class="img" id="cinco-img"><img src="assets/tito-celular.png"></div>
  <svg id="cinco-anel" viewBox="0 0 100 100"><circle cx="50" cy="50" r="42" fill="none" stroke="#F2ECE2" stroke-width="10"/>
    <circle id="cinco-arco" cx="50" cy="50" r="42" fill="none" stroke="#D45F2B" stroke-width="10" stroke-linecap="butt"
      pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" transform="rotate(-90 50 50)"/></svg>
  <div id="cinco-num">0</div><div id="cinco-meta">de 10.000</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#cinco-balao",{{opacity:0,y:30,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.3,ease:"back.out(1.6)"}},0.12);
  tl.fromTo("#cinco-img",{{opacity:0,y:100}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.4)"}},0.05);
  {palavras_js("cinco", txt, ini, 4.04, 7.6)}
  tl.fromTo("#cinco-anel",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(1.8)"}},0.5);
  tl.fromTo("#cinco-arco",{{attr:{{"stroke-dashoffset":1}}}},{{attr:{{"stroke-dashoffset":0.5}},duration:1.0,ease:"power2.out"}},{t(14)-ini:.2f});
  {contador("#cinco-num", 0, 5000, t(14)-ini, 1.0, "milhar")}
  tl.fromTo("#cinco-img",{{rotation:0,transformOrigin:"50% 100%"}},{{rotation:-4,duration:0.3,yoyo:true,repeat:1,ease:"sine.inOut"}},{t(18)-ini:.2f});
""")

# ---------- 3. origem (8.0 – 14.0) ----------
ini, fim = 8.0, 14.0
d = add("origem", ini, fim)
wh, wj = wipe("origem", CREME)
cena("origem", d, """
  .bg{background:var(--pessego);}
  #origem-ped{position:absolute;left:150px;top:520px;width:400px;height:520px;}
  #origem-kanji{position:absolute;left:620px;top:540px;width:340px;text-align:center;font-family:'Noto Sans JP',sans-serif;font-weight:900;font-size:260px;line-height:1;color:var(--verde);}
  #origem-k2{position:absolute;left:620px;top:830px;width:340px;text-align:center;font-weight:900;font-size:40px;color:#2B2B2B;}
  #origem-k3{position:absolute;left:620px;top:885px;width:340px;text-align:center;font-weight:800;font-size:30px;color:#8a837d;}
  #origem-ano{position:absolute;left:150px;top:1060px;width:400px;text-align:center;font-weight:900;font-size:38px;color:#6b6460;}
  #origem-selo{position:absolute;left:520px;top:960px;padding:10px 26px;border:6px solid var(--laranja);border-radius:16px;color:var(--laranja);
               font-weight:900;font-size:58px;letter-spacing:.08em;background:rgba(247,229,221,.9);}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="origem-t">De onde veio o <em>10 mil</em>?</h1>
  <svg id="origem-ped" viewBox="0 0 100 130">
    <rect x="12" y="10" width="76" height="110" rx="28" fill="#F2ECE2" stroke="#2F483A" stroke-width="5"/>
    <rect x="44" y="0" width="12" height="14" rx="4" fill="#2F483A"/>
    <circle cx="50" cy="58" r="28" fill="#fff" stroke="#2F483A" stroke-width="4"/>
    <text x="50" y="68" text-anchor="middle" font-family="Noto Sans JP" font-weight="900" font-size="28" fill="#D45F2B">万</text>
    <line id="origem-pont" x1="50" y1="58" x2="50" y2="36" stroke="#2B2B2B" stroke-width="3" stroke-linecap="round"/>
    <rect x="32" y="95" width="36" height="12" rx="6" fill="#95A185"/></svg>
  <div id="origem-kanji">万</div>
  <div id="origem-k2">"man" = 10 mil</div>
  <div id="origem-k3">manpo-kei: "medidor de 10 mil passos"</div>
  <div id="origem-ano">Japão · anos 60</div>
  <div id="origem-selo">MARKETING</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#origem-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.3);
  tl.fromTo("#origem-ped",{{opacity:0,rotation:-15,scale:0.7}},{{opacity:1,rotation:0,scale:1,duration:0.5,ease:"back.out(1.6)"}},{t(29)-ini:.2f});
  tl.fromTo("#origem-pont",{{rotation:0,svgOrigin:"50 58"}},{{rotation:720,duration:3.0,ease:"power1.inOut"}},{t(29)-ini:.2f});
  tl.fromTo("#origem-ano",{{opacity:0}},{{opacity:1,duration:0.3}},{t(31)-ini:.2f});
  tl.fromTo("#origem-kanji",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.4,ease:"back.out(2)"}},{t(30)-ini:.2f});
  tl.fromTo("#origem-k2",{{opacity:0}},{{opacity:1,duration:0.3}},{t(31)-ini:.2f});
  tl.fromTo("#origem-k3",{{opacity:0}},{{opacity:1,duration:0.3}},{t(30)-ini+0.3:.2f});
  tl.fromTo("#origem-selo",{{opacity:0,scale:2.4,rotation:-16}},{{opacity:1,scale:1,rotation:-8,duration:0.22,ease:"power4.in"}},{t(35)-ini:.2f});
  tl.fromTo("#root",{{x:0}},{{x:10,duration:0.04,yoyo:true,repeat:5,ease:"none"}},{t(35)-ini+0.22:.2f});
""")

# ---------- 4. a curva (14.0 – 25.4) ----------
ini, fim = 14.0, 25.4
d = add("curva", ini, fim)
wh, wj = wipe("curva", PESSEGO)
x2, y2 = pts[0]; x7, y7 = pts[5]
cena("curva", d, f"""
  .bg{{background:#fff;}}
  .tag{{background:#5F6E52;color:#fff;}}
  .graf{{position:absolute;left:0;top:0;}}
  #curva-chip{{position:absolute;left:600px;top:420px;padding:8px 22px;border-radius:999px;background:var(--salvia);color:#fff;font-weight:900;font-size:32px;}}
  .ponto{{position:absolute;width:40px;height:40px;border-radius:50%;border:8px solid #fff;box-shadow:0 4px 14px rgba(0,0,0,.18);}}
  #curva-p2{{left:{x2-20:.0f}px;top:{y2-20:.0f}px;background:#8C8580;}}
  #curva-p7{{left:{x7-20:.0f}px;top:{y7-20:.0f}px;background:var(--laranja);}}
  #curva-l2{{position:absolute;left:{x2+36:.0f}px;top:{y2+8:.0f}px;font-weight:900;font-size:34px;color:#6b6460;}}
  #curva-l7{{position:absolute;left:{x7-60:.0f}px;top:{y7+40:.0f}px;padding:10px 24px;border-radius:999px;background:var(--verde);color:#fff;font-weight:900;font-size:44px;}}
  .cf{{position:absolute;left:{x7-10:.0f}px;top:{y7-10:.0f}px;width:20px;height:30px;border-radius:5px;opacity:0;}}
  .fonte{{top:1110px;}}
""", f"""
  <div class="bg"></div>
  <div class="tag" id="curva-tag">✓ CIÊNCIA</div>
  <h1 class="titulo" id="curva-t1">O que a <em>ciência</em> diz</h1>
  <h1 class="titulo" id="curva-t2" style="opacity:0"><em>7 mil</em>: quase metade do risco</h1>
  {grafico_svg("curva")}
  <div id="curva-chip">57 estudos</div>
  <div class="ponto" id="curva-p2"></div><div id="curva-l2">2 mil passos = 100</div>
  <div class="ponto" id="curva-p7"></div><div id="curva-l7">−47%</div>
  {''.join(f'<div class="cf" id="curva-cf{i}" style="background:{["#E2B04A","#2F483A","#95A185","#D45F2B"][i%4]}"></div>' for i in range(16))}
  <div class="fonte" id="curva-fonte">Fonte: Ding et al., Lancet Public Health, 2025 (estudo observacional)</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#curva-tag",{{opacity:0,y:-10}},{{opacity:1,y:0,duration:0.3}},0.3);
  tl.fromTo("#curva-t1",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.3);
  tl.fromTo(".graf",{{opacity:0}},{{opacity:1,duration:0.4}},{t(39)-ini:.2f});
  tl.fromTo("#curva-chip",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"}},{t(41)-ini:.2f});
  tl.fromTo("#curva-curva",{{attr:{{"stroke-dashoffset":1}}}},{{attr:{{"stroke-dashoffset":0}},duration:2.4,ease:"power2.inOut"}},{t(43)-ini:.2f});
  tl.fromTo("#curva-fonte",{{opacity:0}},{{opacity:1,duration:0.4}},{t(43)-ini:.2f});
  tl.fromTo("#curva-p2",{{scale:0}},{{scale:1,duration:0.3,ease:"back.out(2.4)"}},{t(52)-ini:.2f});
  tl.fromTo("#curva-l2",{{opacity:0,x:-10}},{{opacity:1,x:0,duration:0.3}},{t(53)-ini:.2f});
  tl.to("#curva-t1",{{opacity:0,y:-20,duration:0.25}},{t(59)-ini-0.15:.2f});
  tl.fromTo("#curva-t2",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(59)-ini:.2f});
  tl.to("#curva-chip",{{opacity:0,duration:0.2}},{t(59)-ini-0.15:.2f});
  tl.fromTo("#curva-p7",{{scale:0}},{{scale:1,duration:0.35,ease:"back.out(2.6)"}},{t(59)-ini:.2f});
  tl.fromTo("#curva-l7",{{opacity:0,scale:0.4}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.4)"}},{t(62)-ini:.2f});
  {' '.join(f'tl.fromTo("#curva-cf{i}",{{opacity:1,x:0,y:0,rotation:0}},{{immediateRender:false,opacity:0,x:{math.cos(i*0.39)*(130+(i%3)*45):.0f},y:{math.sin(i*0.39)*(100+(i%4)*30):.0f},rotation:{(i*47)%360},duration:0.9,ease:"power2.out"}},{t(62)-ini:.2f});' for i in range(16))}
""")

# ---------- 5. Tito: e de 7 pra 10? (25.4 – 28.15) ----------
tito_fala("dez", 25.4, 28.15, "E de 7 pra 10 mil, muda muito?", 25.46, 28.1, destaque=(2, 4, 5), olhos="duvida", cor_ant=BRANCO)

# ---------- 6. platô + cada mil conta (28.15 – 34.25) ----------
ini, fim = 28.15, 34.25
d = add("plato", ini, fim)
wh, wj = wipe("plato", CREME)
x10, y10 = pts[8]
cena("plato", d, f"""
  .bg{{background:#fff;}}
  .graf{{position:absolute;left:0;top:-40px;}}
  #plato-faixa{{position:absolute;left:{x7:.0f}px;top:{GY0-40:.0f}px;width:{x10-x7:.0f}px;height:{GY1-GY0:.0f}px;background:rgba(149,161,133,.22);border-radius:14px;transform-origin:0% 50%;}}
  #plato-rot{{position:absolute;left:{x7-40:.0f}px;top:{y7-150:.0f}px;padding:8px 20px;border-radius:999px;background:var(--salvia);color:#fff;font-weight:900;font-size:32px;}}
  #plato-salto{{position:absolute;left:{GX0+30}px;top:{GY0-10}px;padding:8px 20px;border-radius:999px;background:var(--laranja);color:#fff;font-weight:900;font-size:32px;}}
  .pe{{position:absolute;width:40px;height:62px;border-radius:50%;background:var(--terracota);opacity:0;}}
  #plato-cont{{position:absolute;left:80px;top:1085px;font-family:'Playfair Display',serif;font-weight:700;font-size:60px;color:var(--laranja);}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="plato-t">O salto vem <em>antes</em></h1>
  <div id="plato-faixa"></div>
  {grafico_svg("plato")}
  <div id="plato-salto">maior salto ↓</div>
  <div id="plato-rot">7k → 10k: só ~10%</div>
  {''.join(f'<div class="pe" id="plato-pe{i}" style="left:{380+i*90}px;top:{1090 + (i%2)*40}px;transform:rotate(80deg)"></div>' for i in range(7))}
  <div id="plato-cont">+0</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#plato-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.3);
  tl.fromTo("#plato-curva",{{attr:{{"stroke-dashoffset":1}}}},{{attr:{{"stroke-dashoffset":0}},duration:0.9,ease:"power2.out"}},0.35);
  tl.fromTo("#plato-salto",{{opacity:0,y:-10}},{{opacity:1,y:0,duration:0.3,ease:"back.out(2)"}},{t(78)-ini:.2f});
  tl.fromTo("#plato-faixa",{{scaleX:0}},{{scaleX:1,duration:0.5,ease:"power2.out"}},{t(81)-ini:.2f});
  tl.fromTo("#plato-rot",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.2)"}},{t(82)-ini:.2f});
  tl.fromTo("#plato-cont",{{opacity:0}},{{opacity:1,duration:0.2}},{t(86)-ini:.2f});
  {' '.join(f'tl.fromTo("#plato-pe{i}",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.15}},{t(86)-ini+i*0.24:.2f});' for i in range(7))}
  (function(){{const o={{v:0}};const el=document.querySelector("#plato-cont");
    tl.fromTo(o,{{v:0}},{{v:7,duration:1.68,ease:"none",onUpdate:()=>{{el.textContent="+"+(Math.round(o.v)*1000).toLocaleString('pt-BR');}}}},{t(86)-ini:.2f});}})();
""")

# ---------- 7. Tito: e devagar? (34.25 – 36.6) ----------
tito_fala("devagar", 34.25, 36.6, "E se eu andar devagar, conta também?", 34.32, 36.5, destaque=(4,), olhos="duvida", cor_ant=BRANCO)

# ---------- 8. o total pesa (36.6 – 41.05) ----------
ini, fim = 36.6, 41.05
d = add("total", ini, fim)
wh, wj = wipe("total", CREME)
dia = [("☕", "padaria", 1200), ("🚌", "ponto de ônibus", 900), ("🏢", "escada", 600), ("🛒", "mercado", 1800), ("🐕", "passeio", 2500)]
itens = "".join(f'<div class="card it" id="total-i{i}" style="top:{500+i*104}px"><span class="e">{e}</span><span class="n">{n}</span><span class="v">+{v:,}</span></div>'.replace(",", ".")
                for i, (e, n, v) in enumerate(dia))
cena("total", d, """
  .bg{background:var(--pessego);}
  .it{left:80px;width:560px;height:84px;display:flex;align-items:center;gap:18px;padding:0 26px;font-weight:900;font-size:36px;}
  .it .e{font-size:44px;} .it .v{margin-left:auto;color:var(--laranja);}
  #total-anel{position:absolute;left:680px;top:540px;width:340px;height:340px;}
  #total-num{position:absolute;left:680px;top:650px;width:340px;text-align:center;font-family:'Playfair Display',serif;font-weight:700;font-size:66px;}
  #total-ok{position:absolute;left:680px;top:740px;width:340px;text-align:center;font-weight:900;font-size:32px;color:var(--verde);}
  .fonte{top:1060px;}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="total-t">O <em>total</em> pesa mais</h1>
  {itens}
  <svg id="total-anel" viewBox="0 0 100 100"><circle cx="50" cy="50" r="42" fill="none" stroke="#fff" stroke-width="10"/>
    <circle id="total-arco" cx="50" cy="50" r="42" fill="none" stroke="#2F483A" stroke-width="10" stroke-linecap="butt"
      pathLength="1" stroke-dasharray="1" stroke-dashoffset="1" transform="rotate(-90 50 50)"/></svg>
  <div id="total-num">0</div><div id="total-ok">passos no dia</div>
  <div class="fonte" id="total-fonte">Fonte: Saint-Maurice et al., JAMA, 2020</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#total-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.3);
  tl.fromTo("#total-anel",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(1.8)"}},0.4);
  {' '.join(f'tl.fromTo("#total-i{i}",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.3,ease:"back.out(1.6)"}},{0.7+i*0.45:.2f});' for i in range(5))}
  tl.fromTo("#total-arco",{{attr:{{"stroke-dashoffset":1}}}},{{attr:{{"stroke-dashoffset":0}},duration:2.4,ease:"power1.inOut"}},0.7);
  {contador("#total-num", 0, 7000, 0.7, 2.4, "milhar")}
  tl.to("#total-ok",{{color:"#D45F2B",duration:0.2}},3.1);
  tl.set("#total-ok",{{textContent:"7 mil ✓"}},3.1);
  tl.fromTo("#total-fonte",{{opacity:0}},{{opacity:1,duration:0.4}},0.5);
""")

# ---------- 9. resumo do Tito (41.05 – 49.3) ----------
ini, fim = 41.05, 49.3
d = add("resumo", ini, fim)
wh, wj = wipe("resumo", PESSEGO)
txt = "Entendi! 10 mil não é regra. 7 mil já é ótimo, e cada passinho a mais conta. Vou descer do ônibus um ponto antes!"
cena("resumo", d, """
  .bg{background:var(--creme);}
  .balao .txt{font-size:54px;}
  #resumo-anda{left:260px;top:760px;width:600px;height:580px;opacity:0;}
""", f"""
  <div class="bg"></div>
  <div class="balao" id="resumo-balao"><div class="rot">💡 O QUE O TITO ENTENDEU</div>
    <div class="txt">{palavras_html("resumo", txt, 0, (1, 2, 5, 6, 8, 12, 13, 18, 19))}</div><div class="rabo"></div></div>
  <div class="tito-grande" id="resumo-tito">{tito_svg("resumo", bracos="acena")}</div>
  <div class="img" id="resumo-anda"><img src="assets/tito-caminhando.png"></div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#resumo-balao",{{opacity:0,y:30,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"back.out(1.6)"}},0.12);
  tl.fromTo("#resumo-tito",{{opacity:0,y:120}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.4)"}},0.05);
  {palavras_js("resumo", txt, ini, 41.16, 48.9)}
  {fala_js("resumo", round(41.16 - ini, 2), round(t(131) - ini - 0.05, 2))}
  tl.to("#resumo-tito",{{opacity:0,scale:0.9,duration:0.2}},{t(131)-ini:.2f});
  tl.fromTo("#resumo-anda",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:0.3,ease:"back.out(1.4)"}},{t(131)-ini+0.05:.2f});
  tl.fromTo("#resumo-anda",{{y:0}},{{y:-16,duration:0.22,ease:"sine.inOut",yoyo:true,repeat:7}},{t(131)-ini+0.35:.2f});
  tl.to("#resumo-anda",{{x:420,duration:1.4,ease:"power1.in"}},{t(134)-ini:.2f});
""")

# ---------- 10. CTA novo: enviar (49.3 – 55.0) ----------
ini, fim = 49.3, TOTAL
d = add("cta", ini, fim)
wh, wj = wipe("cta", CREME)
cena("cta", d, """
  .bg{background:var(--laranja);}
  .titulo{color:#fff;top:230px;}
  .titulo em{color:var(--creme2);}
  #cta-card{position:absolute;left:150px;top:600px;width:780px;height:330px;background:#fff;border-radius:36px;box-shadow:0 24px 60px rgba(80,30,10,.25);}
  #cta-rot{position:absolute;left:40px;top:30px;font-weight:900;font-size:34px;color:#8a837d;}
  .av{position:absolute;top:96px;width:150px;text-align:center;font-weight:900;font-size:30px;color:#4a4440;}
  .av .c{width:110px;height:110px;margin:0 auto 10px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:46px;color:#fff;}
  #cta-av0 .c{background:#5F6E52;} #cta-av1 .c{background:var(--verde);} #cta-av2 .c{background:var(--mostarda);color:#2B2B2B;} #cta-av3 .c{background:#B5481F;}
  #cta-check{position:absolute;left:60px;top:90px;width:130px;height:130px;border-radius:50%;background:rgba(47,72,58,.92);color:#fff;
             font-size:70px;font-weight:900;display:flex;align-items:center;justify-content:center;}
  #cta-aviao{position:absolute;left:800px;top:1120px;width:150px;height:150px;}
  #cta-aviso{position:absolute;left:80px;top:990px;width:920px;text-align:center;font-weight:800;font-size:30px;color:#FDF3ED;}
  #cta-eco{position:absolute;inset:0;background:var(--verde);}
  #cta-eco .titulo{color:var(--creme2);top:230px;font-size:104px;}
  #cta-eco .titulo em{color:var(--mostarda);}
  #cta-eco-num{position:absolute;left:80px;top:470px;font-family:'Playfair Display',serif;font-weight:700;font-size:170px;color:var(--creme2);line-height:1;}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="cta-t">Manda pra quem <em>se culpa</em></h1>
  <div id="cta-card" data-layout-allow-overlap><div id="cta-rot">Enviar para…</div>
    <div class="av" id="cta-av0" style="left:40px"><div class="c">A</div>amiga</div>
    <div class="av" id="cta-av1" style="left:230px"><div class="c">M</div>mãe</div>
    <div class="av" id="cta-av2" style="left:420px"><div class="c">J</div>João</div>
    <div class="av" id="cta-av3" style="left:610px"><div class="c">+</div>grupo</div>
    <div id="cta-check">✓</div></div>
  <svg id="cta-aviao" viewBox="0 0 100 100"><path d="M6 46 L94 8 L66 92 L48 60 Z" fill="#fff" stroke="#2B2B2B" stroke-width="5" stroke-linejoin="round"/>
    <path d="M48 60 L94 8" stroke="#2B2B2B" stroke-width="4"/></svg>
  <div id="cta-aviso">Conteúdo educativo, não substitui orientação profissional.</div>
  <div class="tito-mini" id="cta-tito" style="top:1360px">{tito_svg("cta", olhos="piscando", bracos="acena")}</div>
  <div id="cta-eco" style="opacity:0"><h1 class="titulo">10 mil passos <em>é regra?</em></h1><div id="cta-eco-num">10.000</div></div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#cta-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(140)-ini-0.1:.2f});
  tl.fromTo("#cta-card",{{opacity:0,y:60,scale:0.95}},{{opacity:1,y:0,scale:1,duration:0.45,ease:"back.out(1.5)"}},{t(140)-ini:.2f});
  {' '.join(f'tl.fromTo("#cta-av{i}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.25,ease:"back.out(2)"}},{t(141)-ini+i*0.1:.2f});' for i in range(4))}
  tl.fromTo("#cta-aviao",{{x:0,y:0,rotation:0,opacity:1}},{{x:0,y:0,rotation:0,opacity:1,duration:0.01}},0);
  tl.to("#cta-aviao",{{x:-260,y:-400,rotation:-25,scale:0.6,duration:0.8,ease:"power2.in"}},{t(144)-ini:.2f});
  tl.to("#cta-aviao",{{opacity:0,duration:0.1}},{t(144)-ini+0.75:.2f});
  tl.fromTo("#cta-check",{{scale:0}},{{scale:1,duration:0.3,ease:"back.out(2.4)"}},{t(144)-ini+0.8:.2f});
  tl.fromTo("#cta-aviso",{{opacity:0}},{{opacity:1,duration:0.4}},0.6);
  tl.fromTo("#cta-tito",{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.5)"}},0.4);
  tl.fromTo("#cta-braco",{{rotation:-12,transformOrigin:"170px 100px"}},{{rotation:12,duration:0.3,ease:"sine.inOut",yoyo:true,repeat:5}},0.9);
  tl.to(["#cta-t","#cta-card","#cta-aviso","#cta-tito"],{{opacity:0,duration:0.3}},{TOTAL-ini-2.05:.2f});
  tl.fromTo("#cta-eco",{{opacity:0}},{{opacity:1,duration:0.35,ease:"power2.inOut"}},{TOTAL-ini-2.05:.2f});
""".replace('tl.fromTo("#cta-aviao",{x:0,y:0,rotation:0,opacity:1},{x:0,y:0,rotation:0,opacity:1,duration:0.01},0);\n', ''))

# ---------- legendas do narrador ----------
GRUPOS = [
    ("*10 mil passos* por dia?", 0, 5), ("Esse número nem nasceu *na ciência*.", 5, 6),
    ("*Adianta, sim.*", 21, 2), ("Os 10 mil vieram de um *pedômetro japonês*", 23, 8), ("dos *anos 60*.", 31, 3), ("Era *marketing*.", 34, 2),
    ("Em 2025, uma *revisão*", 36, 4), ("juntou *dezenas de estudos*", 40, 4), ("sobre passos e saúde.", 44, 4),
    ("Comparado com quem dava *2 mil* passos por dia,", 48, 9), ("quem dava *7 mil*", 57, 4), ("tinha *quase metade* do risco de morte.", 61, 7),
    ("*Pouco.*", 76, 1), ("O maior salto vem *antes dos 7 mil*.", 77, 8), ("E *cada mil passos* a mais", 85, 6), ("*já conta*.", 91, 2),
    ("*Conta.*", 100, 1), ("Nos estudos, o que *mais pesou*", 101, 6), ("foi o *total de passos* do dia.", 107, 7),
    ("*Isso aí.*", 138, 2), ("Manda pra quem *se culpa*", 140, 5), ("por não bater *10 mil*.", 145, 5),
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
