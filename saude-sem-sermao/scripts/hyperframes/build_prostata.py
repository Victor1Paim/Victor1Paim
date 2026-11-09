#!/usr/bin/env python3
"""Vídeo 01 do cronograma: "Exame de próstata: mitos e verdades" (Novembro Azul)."""
import json, math, re, shutil
from pathlib import Path

SCR = Path("/tmp/claude-0/-home-user-Victor1Paim/bc508778-dc0e-5c3d-a4a6-a9dce8035bd2/scratchpad")
POST = Path("/home/user/Victor1Paim/saude-sem-sermao/producoes/01-exame-prostata")
V = POST / "video"
(V / "compositions").mkdir(parents=True, exist_ok=True)
(V / "assets").mkdir(exist_ok=True)
for f in ["hyperframes.json", "package.json", "meta.json"]:
    (V / f).write_text((SCR / "hfblank" / f).read_text().replace('"hfblank"', '"saude-sem-sermao-01-prostata"'))
shutil.copy(POST / "dialogo.mp3", V / "assets/voz.mp3")
shutil.copy(POST / "imagens/tito-bigode.png", V / "assets/tito-bigode.png")

W, H = 1080, 1920
TOTAL = 63.6
AZUL = "#3B6EA5"
words = json.loads((POST / "conferencia/dialogo.palavras.json").read_text())
CENAS = []
src = (SCR / "build_sono.py").read_text()
exec(src[src.index("# ---------- paleta e base"):src.index("# ---------- 1. capa")])
exec(src[src.index("def cena_tito"):src.index("# ---------- 2. Tito: culpa")])
src2 = (SCR / "build_alongar.py").read_text()
exec(src2[src2.index("BASE_CSS += "):src2.index("VERDE, CREME, BRANCO")])
VERDE, CREME, BRANCO, LARANJA, PESSEGO = "#2F483A", "#FDF3ED", "#FFFFFF", "#D45F2B", "#F7E5DD"

_tito_orig = tito_svg
BIGODE = f'<path d="M78 111 q11 -9 22 -1 q11 -8 22 1 q-3 9 -22 5 q-19 4 -22 -5z" fill="{AZUL}"/>'
def tito_svg(pref, **kw):  # Tito de bigode azul em todo o vídeo
    return _tito_orig(pref, **kw).replace(f'<path id="{pref}-sorriso"', BIGODE + f'<path id="{pref}-sorriso"')

src3 = (SCR / "build_passos.py").read_text()
exec(src3[src3.index("def tito_fala"):src3.index("# ---------- gráfico de risco")])
BASE_CSS += f"""
  .card2{{position:absolute;left:80px;width:920px;background:#fff;border-radius:30px;box-shadow:0 14px 40px rgba(40,60,40,.12);
         padding:30px 38px;font-weight:900;font-size:40px;line-height:1.25;}}
  .card2 .q{{font-size:30px;letter-spacing:.08em;color:{AZUL};margin-bottom:10px;}}
  .selo{{position:absolute;padding:10px 26px;border:6px solid;border-radius:16px;font-weight:900;font-size:56px;letter-spacing:.08em;background:rgba(255,255,255,.85);}}
"""

# 1. capa (0 – 3.2)
d = add("capa", 0, 3.2)
cena("capa", d, f"""
  .bg{{background:var(--verde);}}
  .titulo{{color:var(--creme2);top:230px;font-size:104px;}}
  .titulo em{{color:#8FB7E6;}}
  #capa-img{{left:250px;top:620px;width:580px;height:560px;}}
  #capa-laco{{position:absolute;left:800px;top:560px;width:180px;height:240px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo">Exame de próstata: <em>mito ou verdade?</em></h1>
  <div class="img" id="capa-img"><img src="assets/tito-bigode.png"></div>
  <svg id="capa-laco" viewBox="0 0 100 130"><path d="M50 40 C20 0 80 0 50 40 L20 125 L38 125 L50 70 L62 125 L80 125 Z" fill="{AZUL}" stroke="#fff" stroke-width="4" stroke-linejoin="round"/></svg>
""", f"""
  tl.fromTo("#capa-img",{{y:0}},{{y:-14,duration:0.5,ease:"sine.inOut",yoyo:true,repeat:5}},0);
  tl.fromTo("#capa-laco",{{scale:0,rotation:-20}},{{scale:1,rotation:0,duration:0.4,ease:"back.out(2.4)"}},0.3);
""")

# 2. Tito: tenho 45 (3.2 – 6.15)
tito_fala("t1", 3.2, 6.15, "Eu tenho 45 anos. Já tenho que fazer?", 3.32, 5.9, destaque=(2, 3), olhos="duvida", cor_ant=VERDE)

# 3. número (6.15 – 10.7)
ini, fim = 6.15, 10.7
d = add("numero", ini, fim)
wh, wj = wipe("numero", CREME)
cena("numero", d, f"""
  .bg{{background:#fff;}}
  #numero-n{{position:absolute;left:80px;top:560px;font-family:'Playfair Display',serif;font-weight:700;font-size:200px;color:{AZUL};line-height:1;}}
  #numero-l{{position:absolute;left:86px;top:790px;font-weight:900;font-size:48px;}}
  #numero-o{{position:absolute;left:86px;top:860px;font-weight:800;font-size:32px;color:#8a837d;}}
  .fonte{{top:1060px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="numero-t">O câncer <em>mais comum</em> entre os homens</h1>
  <div id="numero-n">0</div><div id="numero-l">casos novos por ano no Brasil</div>
  <div id="numero-o">(sem contar o câncer de pele não melanoma)</div>
  <div class="fonte" id="numero-f">Fonte: INCA, Estimativa 2023 (triênio 2023-2025)</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#numero-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.25);
  tl.fromTo(["#numero-n","#numero-l"],{{opacity:0}},{{opacity:1,duration:0.3}},{t(31)-ini:.2f});
  {contador("#numero-n", 0, 72000, t(31)-ini, 1.3, "milhar")}
  tl.fromTo(["#numero-o","#numero-f"],{{opacity:0}},{{opacity:1,duration:0.3}},{t(31)-ini:.2f});
""")

# 4. depende: MS x SBU (10.7 – 24.3)
ini, fim = 10.7, 24.3
d = add("depende", ini, fim)
wh, wj = wipe("depende", BRANCO)
cena("depende", d, f"""
  .bg{{background:var(--pessego);}}
  #depende-t{{transform-origin:0% 50%;}}
  .idade{{position:absolute;width:150px;height:150px;border-radius:50%;background:{AZUL};color:#fff;display:flex;align-items:center;justify-content:center;
          font-family:'Playfair Display',serif;font-weight:700;font-size:72px;box-shadow:0 10px 30px rgba(0,0,0,.18);}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="depende-t">Resposta: <em>depende</em></h1>
  <div class="card2" id="depende-ms" style="top:420px"><div class="q">MINISTÉRIO DA SAÚDE / INCA</div>não recomenda exame em massa para quem não tem sintomas</div>
  <div class="card2" id="depende-sbu" style="top:680px"><div class="q">SOCIEDADE BRASILEIRA DE UROLOGIA</div>conversar com o urologista a partir dos 50<br>(45 se negro ou com caso na família)</div>
  <div class="idade" id="depende-50" style="left:640px;top:910px">50</div>
  <div class="idade" id="depende-45" style="left:820px;top:910px;background:var(--laranja)">45</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#depende-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(38)-ini:.2f});
  tl.fromTo("#depende-t",{{scale:1}},{{scale:1.06,duration:0.2,yoyo:true,repeat:1}},{t(42)-ini:.2f});
  tl.fromTo("#depende-ms",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:0.4,ease:"back.out(1.6)"}},{t(43)-ini:.2f});
  tl.fromTo("#depende-sbu",{{opacity:0,x:80}},{{opacity:1,x:0,duration:0.4,ease:"back.out(1.6)"}},{t(57)-ini:.2f});
  tl.fromTo("#depende-50",{{scale:0}},{{scale:1,duration:0.3,ease:"back.out(2.6)"}},{t(72)-ini:.2f});
  tl.fromTo("#depende-45",{{scale:0}},{{scale:1,duration:0.3,ease:"back.out(2.6)"}},{t(75)-ini:.2f});
""")

# 5. ponto em comum (24.3 – 27.85)
ini, fim = 24.3, 27.85
d = add("comum", ini, fim)
wh, wj = wipe("comum", PESSEGO)
cena("comum", d, f"""
  .bg{{background:#EEF0EA;}}
  .bola{{position:absolute;top:560px;width:300px;height:300px;border-radius:50%;display:flex;align-items:center;justify-content:center;text-align:center;
         font-weight:900;font-size:40px;color:#fff;}}
  #comum-mao{{position:absolute;left:390px;top:600px;width:300px;text-align:center;font-size:200px;opacity:0;}}
  #comum-r{{position:absolute;left:80px;top:950px;width:920px;text-align:center;font-weight:900;font-size:52px;color:var(--verde);}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="comum-t">O ponto em <em>comum</em></h1>
  <div class="bola" id="comum-a" style="left:150px;background:{AZUL}">você</div>
  <div class="bola" id="comum-b" style="left:630px;background:var(--verde)">o médico</div>
  <div id="comum-mao">🤝</div>
  <div id="comum-r">a decisão é tomada junto</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#comum-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.25);
  tl.fromTo("#comum-a",{{x:-200,opacity:0}},{{x:0,opacity:1,duration:0.4,ease:"power3.out"}},0.35);
  tl.fromTo("#comum-b",{{x:200,opacity:0}},{{x:0,opacity:1,duration:0.4,ease:"power3.out"}},0.35);
  tl.to("#comum-a",{{x:90,scale:0.6,opacity:0,duration:0.45,ease:"power2.inOut"}},{t(88)-ini:.2f});
  tl.to("#comum-b",{{x:-90,scale:0.6,opacity:0,duration:0.45,ease:"power2.inOut"}},{t(88)-ini:.2f});
  tl.fromTo("#comum-mao",{{opacity:0,scale:0.3}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.4)"}},{t(88)-ini+0.45:.2f});
  tl.fromTo("#comum-r",{{opacity:0}},{{opacity:1,duration:0.3}},{t(89)-ini:.2f});
""")

# 6. Tito: e o toque? (27.85 – 29.05)
tito_fala("t2", 27.85, 29.05, "E o exame de toque, hein?", 27.88, 29.0, destaque=(4,), olhos="duvida", cor_ant="#EEF0EA", tam=68)

# 7. toque: mito (29.05 – 33.9)
ini, fim = 29.05, 33.9
d = add("toque", ini, fim)
wh, wj = wipe("toque", CREME)
cena("toque", d, f"""
  .bg{{background:var(--laranja);}}
  .titulo{{color:#fff;top:330px;}}
  .titulo em{{color:var(--creme2);}}
  #toque-selo{{left:80px;top:200px;color:#fff;border-color:#fff;background:transparent;font-size:44px;}}
  #toque-rel{{position:absolute;left:330px;top:640px;width:420px;height:420px;}}
  #toque-seg{{position:absolute;left:330px;top:1070px;width:420px;text-align:center;font-weight:900;font-size:48px;color:#fff;}}
""", f"""
  <div class="bg"></div>
  <div class="selo" id="toque-selo">✕ MITO</div>
  <h1 class="titulo" id="toque-t">"Toque tira a <em>masculinidade</em>"</h1>
  <svg id="toque-rel" viewBox="0 0 100 100"><circle cx="50" cy="54" r="40" fill="#fff" stroke="#2F483A" stroke-width="6"/>
    <rect x="44" y="4" width="12" height="10" rx="3" fill="#2F483A"/>
    <line id="toque-pont" x1="50" y1="54" x2="50" y2="22" stroke="#2B2B2B" stroke-width="5" stroke-linecap="round"/></svg>
  <div id="toque-seg">poucos segundos</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#toque-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.25);
  tl.fromTo("#toque-selo",{{opacity:0,scale:2.4,rotation:-14}},{{opacity:1,scale:1,rotation:-6,duration:0.22,ease:"power4.in"}},{t(104)-ini:.2f});
  tl.fromTo("#root",{{x:0}},{{x:10,duration:0.04,yoyo:true,repeat:5,ease:"none"}},{t(104)-ini+0.22:.2f});
  tl.fromTo("#toque-rel",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"}},{t(111)-ini:.2f});
  tl.fromTo("#toque-pont",{{rotation:0,svgOrigin:"50 54"}},{{rotation:60,duration:1.2,ease:"power1.inOut"}},{t(113)-ini:.2f});
  tl.fromTo("#toque-seg",{{opacity:0}},{{opacity:1,duration:0.3}},{t(114)-ini:.2f});
""")

# 8. Tito: PSA alto? (33.9 – 36.3)
tito_fala("t3", 33.9, 36.3, "E se o PSA der alto, é câncer?", 33.96, 36.0, destaque=(3, 5, 7), olhos="duvida", cor_ant=LARANJA, tam=66)

# 9. PSA (36.3 – 42.95)
ini, fim = 36.3, 42.95
d = add("psa", ini, fim)
wh, wj = wipe("psa", CREME)
cena("psa", d, f"""
  .bg{{background:#fff;}}
  #psa-trilho{{position:absolute;left:140px;top:430px;width:90px;height:560px;border-radius:45px;background:#F2ECE2;overflow:hidden;}}
  #psa-nivel{{position:absolute;left:0;bottom:0;width:90px;height:560px;border-radius:45px;background:linear-gradient(#D45F2B,#E2B04A);transform-origin:50% 100%;}}
  #psa-rot{{position:absolute;left:110px;top:1010px;width:150px;text-align:center;font-weight:900;font-size:40px;}}
  .causa{{position:absolute;left:320px;width:680px;padding:24px 30px;border-radius:24px;font-weight:900;font-size:42px;color:#fff;}}
  #psa-inv{{position:absolute;left:320px;top:900px;font-weight:900;font-size:44px;color:var(--verde);}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="psa-t">PSA alto <em>≠</em> câncer</h1>
  <div id="psa-trilho"><div id="psa-nivel"></div></div><div id="psa-rot">PSA</div>
  <div class="causa" id="psa-c0" style="top:440px;background:#5F6E52">aumento benigno da próstata</div>
  <div class="causa" id="psa-c1" style="top:580px;background:#8A6A1F">inflamação</div>
  <div class="causa" id="psa-c2" style="top:720px;background:#8C8580">câncer (às vezes)</div>
  <div id="psa-inv">🔎 por isso o médico investiga</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#psa-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.2);
  tl.fromTo("#psa-nivel",{{scaleY:0.15}},{{scaleY:0.85,duration:1.2,ease:"power2.out"}},{t(129)-ini:.2f});
  tl.fromTo("#psa-c0",{{opacity:0,x:80}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(132)-ini:.2f});
  tl.fromTo("#psa-c1",{{opacity:0,x:80}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(137)-ini:.2f});
  tl.fromTo("#psa-c2",{{opacity:0,x:80}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(138)-ini:.2f});
  tl.fromTo("#psa-inv",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3}},{t(138)-ini:.2f});
""")

# 10. silencioso: verdade (42.95 – 47.85)
ini, fim = 42.95, 47.85
d = add("silencio", ini, fim)
wh, wj = wipe("silencio", BRANCO)
cena("silencio", d, f"""
  .bg{{background:#EEF0EA;}}
  #silencio-selo{{left:80px;top:200px;color:var(--verde);border-color:var(--verde);font-size:44px;}}
  .titulo{{top:330px;}}
  #silencio-i{{position:absolute;left:340px;top:600px;width:400px;height:400px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;font-size:200px;box-shadow:0 14px 40px rgba(40,60,40,.12);}}
  #silencio-r{{position:absolute;left:80px;top:1040px;width:920px;text-align:center;font-weight:900;font-size:44px;color:var(--verde);}}
""", f"""
  <div class="bg"></div>
  <div class="selo" id="silencio-selo">✓ VERDADE</div>
  <h1 class="titulo" id="silencio-t">Sem sintoma <em>não garante</em> nada</h1>
  <div id="silencio-i">🤫</div>
  <div id="silencio-r">no começo, costuma ser silencioso</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#silencio-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.25);
  tl.fromTo("#silencio-selo",{{opacity:0,scale:2.2,rotation:-12}},{{opacity:1,scale:1,rotation:-5,duration:0.22,ease:"power4.in"}},{t(148)-ini:.2f});
  tl.fromTo("#silencio-i",{{scale:0}},{{scale:1,duration:0.4,ease:"back.out(2)"}},{t(151)-ini:.2f});
  tl.fromTo("#silencio-r",{{opacity:0}},{{opacity:1,duration:0.3}},{t(151)-ini:.2f});
""")

# 11. resumo (47.85 – 53.7)
ini, fim = 47.85, 53.7
d = add("resumo", ini, fim)
wh, wj = wipe("resumo", "#EEF0EA")
txt = "Entendi! Nem pânico, nem descaso: é conversa com o médico, na idade certa pra mim."
cena("resumo", d, """
  .bg{background:var(--creme);}
  .balao .txt{font-size:58px;}
  #resumo-b{left:270px;top:740px;width:540px;height:620px;opacity:0;}
""", f"""
  <div class="bg"></div>
  <div class="balao" id="resumo-balao"><div class="rot">💡 O QUE O TITO ENTENDEU</div>
    <div class="txt">{palavras_html("resumo", txt, 0, (1, 2, 3, 4, 7, 10, 11, 12))}</div><div class="rabo"></div></div>
  <div class="tito-grande" id="resumo-tito">{tito_svg("resumo", bracos="acena")}</div>
  <div class="img" id="resumo-b"><img src="assets/tito-bigode.png"></div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#resumo-balao",{{opacity:0,y:30,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"back.out(1.6)"}},0.12);
  tl.fromTo("#resumo-tito",{{opacity:0,y:120}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.4)"}},0.05);
  {palavras_js("resumo", txt, ini, 47.9, 53.3)}
  {fala_js("resumo", round(47.9 - ini, 2), round(t(168) - ini, 2))}
  tl.to("#resumo-tito",{{opacity:0,scale:0.9,duration:0.2}},{t(168)-ini:.2f});
  tl.fromTo("#resumo-b",{{opacity:0,scale:0.9}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(1.6)"}},{t(168)-ini+0.05:.2f});
""")

# 12. CTA (53.7 – fim): reaproveita o CTA do vídeo do café, trocando textos e o eco final
ini, fim = 53.7, TOTAL
d = add("cta", ini, fim)
wh, wj = wipe("cta", CREME)
src4 = (SCR / "build_cafe.py").read_text()
cta_src = src4[src4.index('cena("cta", d, """'):src4.index("# ---------- legendas do narrador")]
cta_src = (cta_src
    .replace(".bg{background:var(--laranja);}", ".bg{background:var(--verde);}\n  #cta-tito{filter:drop-shadow(0 0 2px #FDF3ED) drop-shadow(0 0 2px #FDF3ED);}")  # Tito não some no fundo
    .replace("Manda pra quem diz que <em>café faz mal</em>", "Manda pra quem <em>foge do médico</em>")
    .replace('"☕ 3 xícaras!"', "💙 AZUL")
    .replace("#cta-eco{position:absolute;inset:0;background:var(--mostarda);}", "#cta-eco{position:absolute;inset:0;background:var(--verde);}")
    .replace("#cta-eco .titulo{color:var(--verde);top:240px;font-size:128px;}", "#cta-eco .titulo{color:var(--creme2);top:230px;font-size:104px;}")
    .replace("#cta-eco .titulo em{color:#8E3412;}", "#cta-eco .titulo em{color:#8FB7E6;}")
    .replace('<div id="cta-eco-c"></div><h1 class="titulo">Café <em>faz mal?</em></h1>', '<h1 class="titulo">Exame de próstata: <em>mito ou verdade?</em></h1>')
    .replace("assets/tito-cafe.png", "assets/tito-bigode.png")
    .replace("t(148)", "t(175)").replace("t(149)", "t(176)").replace("t(152)", "t(180)")
    .replace("t(158)", "t(184)").replace("t(159)", "t(185)").replace("t(165)", "t(191)"))
exec(cta_src)

GRUPOS = [
    ("Exame de *próstata*:", 0, 3), ("o que é *mito* e o que é *verdade*?", 3, 9),
    ("É o câncer *mais comum* entre os homens", 21, 8), ("no Brasil:", 29, 2), ("cerca de *72 mil casos* por ano.", 31, 7),
    ("Mas a resposta é: *depende*.", 38, 5), ("O *Ministério da Saúde* não recomenda", 43, 6), ("*exame em massa* pra quem não tem sintomas.", 49, 8),
    ("Já a *Sociedade Brasileira de Urologia*", 57, 6), ("orienta conversar com o médico", 63, 6), ("a partir dos *50*,", 69, 4),
    ("ou dos *45* pra homens negros", 73, 6), ("ou com caso na família.", 79, 5),
    ("O *ponto em comum*:", 84, 4), ("a decisão é *sua, junto com o médico*.", 88, 8),
    ("O toque *não tem nada a ver* com masculinidade.", 102, 9), ("É rápido, leva *poucos segundos*.", 111, 5),
    ("*Não necessariamente.*", 124, 2), ("O PSA também sobe com o *aumento benigno* da próstata", 126, 10), ("ou com *inflamação*.", 136, 3),
    ("Por isso o médico *investiga*.", 139, 5), ("E *não ter sintoma* não garante nada:", 144, 7), ("no começo, esse câncer costuma ser *silencioso*.", 151, 7),
    ("*Isso aí.*", 173, 2), ("Manda pra aquele homem *que foge do médico*.", 175, 8), ("E *curte*,", 183, 2),
    ("*comenta AZUL* se aprendeu algo", 185, 5), ("e *segue pra mais!*", 190, 4),
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
