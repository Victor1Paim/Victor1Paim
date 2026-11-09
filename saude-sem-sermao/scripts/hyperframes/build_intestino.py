#!/usr/bin/env python3
"""Vídeo 05 do cronograma: "Intestino preso: o que ajuda de verdade" (Intestino sem Drama)."""
import json, math, re, shutil
from pathlib import Path

SCR = Path("/tmp/claude-0/-home-user-Victor1Paim/bc508778-dc0e-5c3d-a4a6-a9dce8035bd2/scratchpad")
POST = Path("/home/user/Victor1Paim/saude-sem-sermao/producoes/05-intestino-preso")
V = POST / "video"
(V / "compositions").mkdir(parents=True, exist_ok=True)
(V / "assets").mkdir(exist_ok=True)
for f in ["hyperframes.json", "package.json", "meta.json"]:
    (V / f).write_text((SCR / "hfblank" / f).read_text().replace('"hfblank"', '"saude-sem-sermao-05-intestino"'))
shutil.copy(POST / "dialogo.mp3", V / "assets/voz.mp3")
shutil.copy(POST / "imagens/tito-banquinho.png", V / "assets/tito-banquinho.png")

W, H = 1080, 1920
TOTAL = 68.3
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
CREMEC = "#F2ECE2"

# 1. capa (0 – 5.4)
d = add("capa", 0, 5.4)
cena("capa", d, f"""
  .bg{{background:{CREMEC};}}
  .titulo{{color:var(--verde);top:230px;font-size:112px;}}
  .titulo em{{color:var(--laranja);}}
  #capa-img{{left:250px;top:640px;width:580px;height:650px;}}
  #capa-selo{{left:80px;top:500px;color:var(--verde);border-color:var(--verde);font-size:40px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="capa-t">Intestino preso:<br><em>o que ajuda?</em></h1>
  <div class="selo" id="capa-selo">✕ remédio todo dia</div>
  <div class="img" id="capa-img"><img src="assets/tito-banquinho.png"></div>
""", f"""
  tl.fromTo("#capa-img",{{y:0}},{{y:-10,duration:0.6,ease:"sine.inOut",yoyo:true,repeat:7}},0.1);
  tl.fromTo("#capa-selo",{{opacity:0,scale:2.2,rotation:-12}},{{opacity:1,scale:1,rotation:-4,duration:0.22,ease:"power4.in"}},{t(8)-0.1:.2f});
""")

# 2. Tito (5.4 – 9.65)
tito_fala("t1", 5.4, 9.65, "Mas eu não vou ao banheiro todo dia. Tem algo errado comigo?", 5.5, 9.5, destaque=(6, 7, 10), olhos="duvida", cor_ant=CREMEC, tam=58)

# 3. normal é uma faixa (9.65 – 17.2)
ini, fim = 9.65, 17.2
d = add("normal", ini, fim)
wh, wj = wipe("normal", CREME)
cena("normal", d, f"""
  .bg{{background:#fff;}}
  #normal-barra{{position:absolute;left:80px;top:560px;width:920px;height:60px;border-radius:30px;background:#F2ECE2;}}
  #normal-faixa{{position:absolute;left:80px;top:560px;width:920px;height:60px;border-radius:30px;background:linear-gradient(90deg,#95A185,#2F483A);transform-origin:0 50%;}}
  .ext{{position:absolute;top:650px;width:420px;font-weight:900;font-size:44px;}}
  .ext b{{display:block;white-space:nowrap;font-family:'Playfair Display',serif;font-size:68px;color:var(--verde);}}
  #normal-ok{{position:absolute;left:80px;top:860px;width:920px;padding:24px 34px;border-radius:26px;background:var(--verde);color:#fff;font-weight:900;font-size:46px;}}
  .fonte{{top:1060px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="normal-t">O normal é uma <em>faixa</em></h1>
  <div id="normal-barra"></div><div id="normal-faixa"></div>
  <div class="ext" id="normal-a" style="left:80px"><b>3× por dia</b></div>
  <div class="ext" id="normal-b" style="left:500px;width:500px;text-align:right"><b>3× por semana</b></div>
  <div id="normal-ok">✓ o que conta: sai fácil, sem esforço</div>
  <div class="fonte" id="normal-f">Referência: critérios de Roma IV (2016) e literatura de gastroenterologia</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#normal-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{max(t(27)-ini,0.2):.2f});
  tl.fromTo("#normal-barra",{{opacity:0}},{{opacity:1,duration:0.3}},{t(29)-ini:.2f});
  tl.fromTo("#normal-a",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3}},{t(31)-ini:.2f});
  tl.fromTo("#normal-faixa",{{scaleX:0}},{{scaleX:1,duration:1.4,ease:"power2.inOut"}},{t(31)-ini:.2f});
  tl.fromTo("#normal-b",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3}},{t(36)-ini:.2f});
  tl.fromTo("#normal-f",{{opacity:0}},{{opacity:1,duration:0.3}},{t(29)-ini:.2f});
  tl.fromTo("#normal-ok",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.35,ease:"back.out(1.6)"}},{t(40)-ini:.2f});
""")

# 4. preso (17.2 – 23.25)
ini, fim = 17.2, 23.25
d = add("preso", ini, fim)
wh, wj = wipe("preso", BRANCO)
cena("preso", d, f"""
  .bg{{background:var(--pessego);}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="preso-t">Aí pode ser <em>intestino preso</em></h1>
  <div class="chip" id="preso-a" style="top:520px"><span class="i">📅</span>menos de 3× por semana</div>
  <div class="chip" id="preso-b" style="top:660px"><span class="i">🪨</span>fezes duras</div>
  <div class="chip" id="preso-c" style="top:800px"><span class="i">😣</span>muito esforço</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#preso-a",{{opacity:0,x:-100}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{max(t(45)-ini,0.25):.2f});
  tl.fromTo("#preso-b",{{opacity:0,x:-100}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(52)-ini:.2f});
  tl.fromTo("#preso-c",{{opacity:0,x:-100}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(54)-ini:.2f});
  tl.fromTo("#preso-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(56)-ini:.2f});
""")

# 5. Tito (23.25 – 25.0)
tito_fala("t2", 23.25, 25.3, "E o que ajuda de verdade?", 23.44, 24.8, destaque=(3, 4, 5), olhos="duvida", cor_ant=PESSEGO, tam=72)

# 6. fibra + água (25.3 – 31.2)
ini, fim = 25.3, 31.2
d = add("fibra", ini, fim)
wh, wj = wipe("fibra", CREME)
COM = [("🫘", "feijão", 68), ("🍎", "fruta", 69), ("🥬", "verdura", 70), ("🥣", "aveia", 71)]
cena("fibra", d, f"""
  .bg{{background:#fff;}}
  .al{{position:absolute;top:480px;width:210px;text-align:center;font-weight:900;font-size:36px;}}
  .al .c{{width:190px;height:190px;margin:0 auto 12px;border-radius:50%;background:#EEF0EA;display:flex;align-items:center;justify-content:center;font-size:110px;}}
  #fibra-agua{{position:absolute;left:80px;top:790px;width:920px;padding:24px 34px;border-radius:26px;background:#DCEAF2;font-weight:900;font-size:46px;color:#22445E;}}
  #fibra-emp{{position:absolute;left:80px;top:950px;font-weight:900;font-size:40px;color:var(--laranja);}}
  .fonte{{top:1060px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="fibra-t"><em>Fibra</em> + água</h1>
  {''.join(f'<div class="al" id="fibra-c{i}" style="left:{80+i*235}px"><div class="c">{e}</div>{n}</div>' for i,(e,n,_) in enumerate(COM))}
  <div id="fibra-agua">💧 com bastante água</div>
  <div id="fibra-emp">senão a fibra empaca</div>
  <div class="fonte" id="fibra-f">Fonte: Guia Alimentar para a População Brasileira (MS, 2014)</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#fibra-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.15);
  {' '.join(f'tl.fromTo("#fibra-c{i}",{{opacity:0,scale:0.3}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2.4)"}},{t(k)-ini-0.05:.2f});' for i,(_,_,k) in enumerate(COM))}
  tl.fromTo("#fibra-f",{{opacity:0}},{{opacity:1,duration:0.3}},0.3);
  tl.fromTo("#fibra-agua",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.35,ease:"back.out(1.6)"}},{t(72)-ini:.2f});
  tl.fromTo("#fibra-emp",{{opacity:0}},{{opacity:1,duration:0.3}},{t(74)-ini:.2f});
""")

# 7. movimento e sem segurar (31.2 – 34.9)
ini, fim = 31.2, 34.9
d = add("habito", ini, fim)
wh, wj = wipe("habito", BRANCO)
cena("habito", d, f"""
  .bg{{background:#EEF0EA;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="habito-t">Movimento e <em>sem segurar</em></h1>
  <div class="chip" id="habito-a" style="top:520px"><span class="i">🚶</span>se mexer</div>
  <div class="chip" id="habito-b" style="top:660px"><span class="i">🔔</span>deu sinal? vai!</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#habito-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.15);
  tl.fromTo("#habito-a",{{opacity:0,x:-100}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{max(t(78)-ini,0.3):.2f});
  tl.fromTo("#habito-b",{{opacity:0,x:-100}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(81)-ini:.2f});
  tl.fromTo("#habito-b .i",{{rotation:-18}},{{rotation:18,duration:0.08,yoyo:true,repeat:7,ease:"none"}},{t(85)-ini:.2f});
""")

# 8. banquinho (34.9 – 40.2)
ini, fim = 34.9, 40.2
d = add("banq", ini, fim)
wh, wj = wipe("banq", "#EEF0EA")
cena("banq", d, f"""
  .bg{{background:var(--creme);}}
  #banq-img{{left:80px;top:470px;width:520px;height:580px;}}
  #banq-n{{position:absolute;left:620px;top:560px;width:400px;font-weight:900;font-size:40px;}}
  #banq-n b{{display:block;font-family:'Playfair Display',serif;font-size:110px;color:var(--laranja);line-height:1;}}
  .fonte{{top:1080px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="banq-t">O truque do <em>banquinho</em></h1>
  <div class="img" id="banq-img"><img src="assets/tito-banquinho.png"></div>
  <div id="banq-n"><b>9 em 10</b>relataram menos esforço</div>
  <div class="fonte" id="banq-f">Fonte: Modi et al., J Clin Gastroenterol, 2019 (52 adultos saudáveis)</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#banq-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.15);
  tl.fromTo("#banq-img",{{opacity:0,scale:0.8}},{{opacity:1,scale:1,duration:0.4,ease:"back.out(1.6)"}},{t(93)-ini:.2f});
  tl.fromTo("#banq-f",{{opacity:0}},{{opacity:1,duration:0.3}},{t(93)-ini:.2f});
  tl.fromTo("#banq-n",{{opacity:0,x:60}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(99)-ini:.2f});
""")

# 9. Tito (40.2 – 41.95)
tito_fala("t3", 40.2, 41.95, "E se nada disso resolver?", 40.26, 41.8, destaque=(2, 3, 4), olhos="duvida", cor_ant=CREME, tam=72)

# 10. médico (41.95 – 52.2)
ini, fim = 41.95, 52.2
d = add("medico", ini, fim)
wh, wj = wipe("medico", CREME)
cena("medico", d, f"""
  .bg{{background:#fff;}}
  #medico-card{{position:absolute;left:80px;top:460px;width:920px;padding:30px 36px;border-radius:30px;background:var(--pessego);}}
  #medico-card .q{{font-weight:900;font-size:34px;letter-spacing:.06em;color:var(--laranja);margin-bottom:14px;}}
  .sinal{{font-weight:900;font-size:46px;margin:10px 0;}}
  #medico-lax{{position:absolute;left:80px;top:900px;width:920px;padding:22px 34px;border-radius:26px;background:var(--verde);color:#fff;font-weight:900;font-size:44px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="medico-t">Hora do <em>médico</em></h1>
  <div id="medico-card"><div class="q">⚠️ AINDA MAIS SE TIVER…</div>
    <div class="sinal" id="medico-s0">• sangue nas fezes</div><div class="sinal" id="medico-s1">• perda de peso sem explicação</div><div class="sinal" id="medico-s2">• mudança do ritmo do nada</div></div>
  <div id="medico-lax">🚫 nada de laxante por conta própria</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#medico-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{max(t(112)-ini,0.2):.2f});
  tl.fromTo("#medico-card",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.35,ease:"back.out(1.6)"}},{t(115)-ini:.2f});
  tl.fromTo("#medico-s0",{{opacity:0,x:40}},{{opacity:1,x:0,duration:0.3}},{t(119)-ini:.2f});
  tl.fromTo("#medico-s1",{{opacity:0,x:40}},{{opacity:1,x:0,duration:0.3}},{t(122)-ini:.2f});
  tl.fromTo("#medico-s2",{{opacity:0,x:40}},{{opacity:1,x:0,duration:0.3}},{t(130)-ini:.2f});
  tl.fromTo("#medico-lax",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.35,ease:"back.out(1.6)"}},{t(135)-ini:.2f});
""")

# 11. resumo (52.2 – 58.65)
ini, fim = 52.2, 58.65
d = add("resumo", ini, fim)
wh, wj = wipe("resumo", BRANCO)
txt = "Entendi! Fibra com água, movimento, banquinho e sem segurar. Não melhorou? Médico."
cena("resumo", d, """
  .bg{background:var(--creme);}
  .balao .txt{font-size:58px;}
""", f"""
  <div class="bg"></div>
  <div class="balao" id="resumo-balao"><div class="rot">💡 O QUE O TITO ENTENDEU</div>
    <div class="txt">{palavras_html("resumo", txt, 0, (1, 2, 3, 4, 5, 7, 8, 11))}</div><div class="rabo"></div></div>
  <div class="tito-grande" id="resumo-tito">{tito_svg("resumo", bracos="acena")}</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#resumo-balao",{{opacity:0,y:30,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"back.out(1.6)"}},0.12);
  tl.fromTo("#resumo-tito",{{opacity:0,y:120}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.4)"}},0.05);
  {palavras_js("resumo", txt, ini, 52.3, 58.4)}
  {fala_js("resumo", round(52.3 - ini, 2), round(58.4 - ini, 2))}
""")

# 12. CTA (58.65 – fim)
ini, fim = 58.65, TOTAL
d = add("cta", ini, fim)
wh, wj = wipe("cta", CREME)
src4 = (SCR / "build_cafe.py").read_text()
cta_src = src4[src4.index('cena("cta", d, """'):src4.index("# ---------- legendas do narrador")]
cta_src = (cta_src
    .replace(".bg{background:var(--laranja);}", ".bg{background:var(--verde);}\n  #cta-tito{filter:drop-shadow(0 0 2px #FDF3ED) drop-shadow(0 0 2px #FDF3ED);}")  # Tito não some no fundo
    .replace("Manda pra quem diz que <em>café faz mal</em>", "Manda pra quem <em>mora no banheiro</em>")
    .replace('"☕ 3 xícaras!"', "🪑 BANQUINHO")
    .replace("#cta-eco{position:absolute;inset:0;background:var(--mostarda);}", "#cta-eco{position:absolute;inset:0;background:#F2ECE2;}")
    .replace("#cta-eco .titulo{color:var(--verde);top:240px;font-size:128px;}", "#cta-eco .titulo{color:var(--verde);top:230px;font-size:112px;}")
    .replace("#cta-eco .titulo em{color:#8E3412;}", "#cta-eco .titulo em{color:var(--laranja);}")
    .replace('<div id="cta-eco-c"></div><h1 class="titulo">Café <em>faz mal?</em></h1>', '<h1 class="titulo">Intestino preso:<br><em>o que ajuda?</em></h1>')
    .replace("assets/tito-cafe.png", "assets/tito-banquinho.png")
    .replace("#cta-eco-img{left:300px;top:500px;width:480px;height:570px;}", "#cta-eco-img{left:250px;top:640px;width:580px;height:650px;}")
    .replace("t(165)-ini-0.05", "t(173)-ini-0.1").replace("t(165)-ini+0.45", "t(174)-ini+0.15")
    .replace("TOTAL-ini-2.1", "TOTAL-ini-2.3")
    .replace("t(148)", "t(156)").replace("t(149)", "t(157)").replace("t(152)", "t(160)")
    .replace("t(165)", "t(174)").replace("t(158)", "t(165)").replace("t(159)", "t(167)"))
exec(cta_src)

GRUPOS = [
    ("Intestino preso:", 0, 2), ("o que ajuda *de verdade*?", 2, 5), ("Spoiler: *não é remédio todo dia*.", 7, 6),
    ("*Não necessariamente.*", 25, 2), ("O normal vai de *3 vezes por dia*", 27, 8), ("a *3 vezes por semana*,", 35, 5), ("se *sai fácil, sem esforço*.", 40, 5),
    ("*Menos de 3 vezes* por semana,", 45, 6), ("com *fezes duras* e esforço?", 51, 5), ("Aí pode ser *intestino preso*.", 56, 5),
    ("*Fibra*:", 67, 1), ("feijão, fruta, verdura, aveia.", 68, 4), ("Com *bastante água*,", 72, 3), ("senão ela *empaca*.", 75, 3),
    ("*Se mexer*,", 78, 2), ("e *não segurar a vontade*:", 80, 5), ("*deu sinal, vai*.", 85, 3),
    ("E um *truque*:", 88, 3), ("num estudo, apoiar os pés *no banquinho*", 91, 7), ("fez a maioria fazer *menos esforço*.", 98, 6),
    ("Aí é a *hora do médico*,", 109, 6), ("ainda mais se tiver *sangue nas fezes*,", 115, 7), ("*perda de peso* sem explicação", 122, 5),
    ("ou se *o ritmo mudou* do nada.", 127, 7), ("E *nada de laxante* por conta própria.", 134, 7),
    ("*Isso aí.*", 154, 2), ("Manda pra quem passa *meia hora no banheiro*.", 156, 8), ("E *curte*,", 164, 2),
    ("*comenta BANQUINHO* se você vai testar", 167, 6), ("e *segue pra mais!*", 173, 4),
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
