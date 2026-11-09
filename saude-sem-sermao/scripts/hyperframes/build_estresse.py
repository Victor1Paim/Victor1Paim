#!/usr/bin/env python3
"""Vídeo 02 do cronograma: "Estresse engorda?" (Mente sem Nó)."""
import json, math, re, shutil
from pathlib import Path

SCR = Path("/tmp/claude-0/-home-user-Victor1Paim/bc508778-dc0e-5c3d-a4a6-a9dce8035bd2/scratchpad")
POST = Path("/home/user/Victor1Paim/saude-sem-sermao/producoes/02-estresse-engorda")
V = POST / "video"
(V / "compositions").mkdir(parents=True, exist_ok=True)
(V / "assets").mkdir(exist_ok=True)
for f in ["hyperframes.json", "package.json", "meta.json"]:
    (V / f).write_text((SCR / "hfblank" / f).read_text().replace('"hfblank"', '"saude-sem-sermao-02-estresse"'))
shutil.copy(POST / "dialogo.mp3", V / "assets/voz.mp3")
shutil.copy(POST / "imagens/tito-estresse.png", V / "assets/tito-estresse.png")

W, H = 1080, 1920
TOTAL = 68.6
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
  .chip{position:absolute;left:80px;width:920px;padding:24px 34px;border-radius:26px;background:#fff;box-shadow:0 12px 34px rgba(80,40,20,.12);
        font-weight:900;font-size:46px;display:flex;align-items:center;gap:24px;}
  .chip .i{font-size:70px;line-height:1;}
"""

# 1. capa (0 – 4.5)
d = add("capa", 0, 4.5)
cena("capa", d, f"""
  .bg{{background:var(--pessego);}}
  .titulo{{color:var(--verde);top:230px;font-size:128px;}}
  .titulo em{{color:var(--laranja);}}
  #capa-img{{left:270px;top:640px;width:540px;height:680px;}}
  #capa-sub{{position:absolute;left:80px;top:560px;font-weight:900;font-size:46px;color:#5b524c;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="capa-t">Estresse <em>engorda?</em></h1>
  <div id="capa-sub">pode… mas não do jeito que você pensa</div>
  <div class="img" id="capa-img"><img src="assets/tito-estresse.png"></div>
""", f"""
  tl.fromTo("#capa-img",{{rotation:-2}},{{rotation:2,duration:0.12,ease:"sine.inOut",yoyo:true,repeat:9,transformOrigin:"50% 100%"}},0);
  tl.fromTo("#capa-sub",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35,ease:"power3.out"}},{t(2)-0.05:.2f});
  tl.fromTo("#capa-img",{{y:0}},{{y:-12,duration:0.5,ease:"sine.inOut",yoyo:true,repeat:3}},1.3);
""")

# 2. Tito: sem caloria (4.5 – 7.6)
tito_fala("t1", 4.5, 7.6, "Ué, mas esse estresse não tem caloria nenhuma!", 4.82, 7.4, destaque=(6, 7), olhos="duvida", cor_ant=PESSEGO, tam=66)

# 3. verdade + dominós (7.6 – 13.4)
ini, fim = 7.6, 13.4
d = add("verdade", ini, fim)
wh, wj = wipe("verdade", CREME)
DOM = [("cortisol", "#CE6840"), ("fome", "#E2B04A"), ("sono ruim", "#2F483A")]
cena("verdade", d, f"""
  .bg{{background:#EEF0EA;}}
  #verdade-selo{{left:80px;top:200px;color:var(--verde);border-color:var(--verde);font-size:44px;}}
  .titulo{{top:330px;}}
  .dom{{position:absolute;top:620px;width:200px;height:400px;border-radius:26px;border:8px solid #2B2B2B;display:flex;align-items:flex-end;justify-content:center;
        padding-bottom:26px;font-weight:900;font-size:36px;color:#fff;text-align:center;transform-origin:50% 100%;}}
  .dom::before{{content:"";position:absolute;left:24px;right:24px;top:180px;height:8px;background:rgba(255,255,255,.7);border-radius:4px;}}
  #verdade-r{{position:absolute;left:80px;top:1070px;width:920px;text-align:center;font-weight:900;font-size:46px;color:var(--verde);}}
""", f"""
  <div class="bg"></div>
  <div class="selo" id="verdade-selo">✓ VERDADE</div>
  <h1 class="titulo" id="verdade-t">O estresse <em>em si</em> não engorda</h1>
  {''.join(f'<div class="dom" id="verdade-d{i}" style="left:{170+i*270}px;background:{c}">{n}</div>' for i,(n,c) in enumerate(DOM))}
  <div id="verdade-r">o que pesa é o efeito em cadeia</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#verdade-selo",{{opacity:0,scale:2.2,rotation:-12}},{{opacity:1,scale:1,rotation:-5,duration:0.22,ease:"power4.in"}},{t(18)-ini:.2f});
  tl.fromTo("#verdade-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(19)-ini:.2f});
  {' '.join(f'tl.fromTo("#verdade-d{i}",{{opacity:0,y:-160}},{{opacity:1,y:0,duration:0.4,ease:"bounce.out"}},{t(25)-ini+i*0.25:.2f});' for i in range(3))}
  tl.fromTo("#verdade-r",{{opacity:0}},{{opacity:1,duration:0.3}},{t(26)-ini:.2f});
  tl.fromTo("#verdade-d0",{{rotation:0}},{{rotation:-6,duration:0.15,yoyo:true,repeat:3,ease:"sine.inOut"}},{t(33)-ini:.2f});
""")

# 4. cortisol e fome (13.4 – 21.8)
ini, fim = 13.4, 21.8
d = add("cortisol", ini, fim)
wh, wj = wipe("cortisol", "#EEF0EA")
cena("cortisol", d, f"""
  .bg{{background:#fff;}}
  #cortisol-trilho{{position:absolute;left:140px;top:430px;width:100px;height:560px;border-radius:50px;background:#F2ECE2;overflow:hidden;}}
  #cortisol-nivel{{position:absolute;left:0;bottom:0;width:100px;height:560px;border-radius:50px;background:linear-gradient(#CE6840,#E2B04A);transform-origin:50% 100%;}}
  #cortisol-rot{{position:absolute;left:90px;top:1010px;width:200px;text-align:center;font-weight:900;font-size:38px;}}
  #cortisol-seta{{position:absolute;left:300px;top:440px;font-weight:900;font-size:44px;color:var(--laranja);}}
  #cortisol-fome{{position:absolute;left:330px;top:540px;width:670px;font-weight:900;font-size:50px;}}
  .comida{{position:absolute;top:680px;width:200px;height:200px;border-radius:50%;background:#F7E5DD;display:flex;align-items:center;justify-content:center;font-size:110px;}}
  #cortisol-cal{{position:absolute;left:330px;top:920px;width:670px;font-weight:900;font-size:40px;color:#8a837d;}}
  .fonte{{top:1080px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="cortisol-t">Estresse <em>de rotina</em></h1>
  <div id="cortisol-trilho"><div id="cortisol-nivel"></div></div><div id="cortisol-rot">cortisol</div>
  <div id="cortisol-seta">▲ fica alto</div>
  <div id="cortisol-fome">→ mais <span style="color:var(--laranja)">fome</span></div>
  {''.join(f'<div class="comida" id="cortisol-c{i}" style="left:{330+i*230}px">{e}</div>' for i,e in enumerate(["🍫","🍕","🍟"]))}
  <div id="cortisol-cal">principalmente por comida calórica</div>
  <div class="fonte" id="cortisol-f">Fonte: van der Valk et al., Curr Obes Rep, 2018</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#cortisol-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.25);
  tl.fromTo("#cortisol-nivel",{{scaleY:0.15}},{{scaleY:0.88,duration:1.3,ease:"power2.out"}},{t(43)-ini:.2f});
  tl.fromTo("#cortisol-seta",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.3}},{t(46)-ini:.2f});
  tl.fromTo("#cortisol-fome",{{opacity:0,x:60}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(50)-ini:.2f});
  {' '.join(f'tl.fromTo("#cortisol-c{i}",{{scale:0}},{{scale:1,duration:0.3,ease:"back.out(2.6)"}},{t(55)-ini+i*0.2:.2f});' for i in range(3))}
  tl.fromTo("#cortisol-f",{{opacity:0}},{{opacity:1,duration:0.3}},{t(44)-ini:.2f});
  tl.fromTo("#cortisol-cal",{{opacity:0}},{{opacity:1,duration:0.3}},{t(53)-ini:.2f});
""")

# 5. Tito: chocolate (21.8 – 25.1)
tito_fala("t2", 21.8, 25.1, "Por isso que eu ataco o chocolate depois de um dia daqueles?", 21.96, 25.0, destaque=(4, 6), olhos="duvida", cor_ant=BRANCO, tam=58)

# 6. nem todo mundo (25.1 – 31.5)
ini, fim = 25.1, 31.5
d = add("todos", ini, fim)
wh, wj = wipe("todos", CREME)
cena("todos", d, f"""
  .bg{{background:var(--pessego);}}
  .lado{{position:absolute;top:470px;width:430px;height:520px;border-radius:34px;background:#fff;box-shadow:0 14px 40px rgba(80,40,20,.12);
         display:flex;flex-direction:column;align-items:center;justify-content:center;gap:22px;text-align:center;font-weight:900;font-size:44px;}}
  .lado .i{{font-size:150px;line-height:1;}}
  .lado .s{{font-size:80px;}}
  #todos-vs{{position:absolute;left:470px;top:680px;width:140px;height:140px;border-radius:50%;background:var(--verde);color:#fff;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:44px;}}
  .fonte{{top:1060px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="todos-t">Não é com <em>todo mundo</em></h1>
  <div class="lado" id="todos-a" style="left:60px"><span class="i">🍔</span>come mais<span class="s" style="color:var(--laranja)">▲</span></div>
  <div class="lado" id="todos-b" style="left:590px"><span class="i">🍽️</span>perde a fome<span class="s" style="color:var(--verde)">▼</span></div>
  <div id="todos-vs">ou</div>
  <div class="fonte" id="todos-f">Fonte: Oliver &amp; Wardle, Physiol Behav, 1999</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#todos-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(72)-ini:.2f});
  tl.fromTo("#todos-a",{{opacity:0,x:-120}},{{opacity:1,x:0,duration:0.4,ease:"back.out(1.6)"}},{t(78)-ini:.2f});
  tl.fromTo("#todos-vs",{{scale:0}},{{scale:1,duration:0.3,ease:"back.out(2.6)"}},{t(85)-ini:.2f});
  tl.fromTo("#todos-b",{{opacity:0,x:120}},{{opacity:1,x:0,duration:0.4,ease:"back.out(1.6)"}},{t(86)-ini:.2f});
  tl.fromTo("#todos-f",{{opacity:0}},{{opacity:1,duration:0.3}},{t(78)-ini:.2f});
""")

# 7. sono (31.5 – 39.8)
ini, fim = 31.5, 39.8
d = add("sono", ini, fim)
wh, wj = wipe("sono", PESSEGO)
cena("sono", d, f"""
  .bg{{background:var(--verde);}}
  .titulo{{color:var(--creme2);}}
  .titulo em{{color:var(--mostarda);}}
  #sono-lua{{position:absolute;left:760px;top:180px;font-size:150px;}}
  #sono-cad{{position:absolute;left:80px;top:470px;width:920px;font-weight:900;font-size:44px;color:var(--creme2);}}
  #sono-n{{position:absolute;left:80px;top:600px;font-family:'Playfair Display',serif;font-weight:700;font-size:210px;color:var(--mostarda);line-height:1;}}
  #sono-l{{position:absolute;left:86px;top:840px;width:900px;font-weight:900;font-size:46px;color:var(--creme2);}}
  .fonte{{top:1060px;color:#c9d3c6;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="sono-t">E tem o <em>sono</em></h1>
  <div id="sono-lua">🌙</div>
  <div id="sono-cad">estresse → dorme pouco →</div>
  <div id="sono-n">+0</div>
  <div id="sono-l">kcal a mais no dia seguinte (média)</div>
  <div class="fonte" id="sono-f">Fonte: Al Khatib et al., Eur J Clin Nutr, 2017 (meta-análise)</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#sono-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.2);
  tl.fromTo("#sono-lua",{{opacity:0,rotation:-30,scale:0.4}},{{opacity:1,rotation:0,scale:1,duration:0.5,ease:"back.out(2)"}},0.35);
  tl.fromTo("#sono-cad",{{opacity:0,x:-40}},{{opacity:1,x:0,duration:0.35}},{t(97)-ini:.2f});
  tl.fromTo(["#sono-n","#sono-l"],{{opacity:0}},{{opacity:1,duration:0.3}},{t(104)-ini:.2f});
  (function(){{const o={{v:0}};const el=document.querySelector("#sono-n");
    tl.fromTo(o,{{v:0}},{{v:385,duration:1.4,ease:"power2.out",onUpdate:()=>{{el.textContent="+"+Math.round(o.v);}}}},{t(109)-ini:.2f});}})();
  tl.fromTo("#sono-n",{{scale:1}},{{scale:1.08,duration:0.18,yoyo:true,repeat:1}},{t(109)-ini+1.4:.2f});
  tl.fromTo("#sono-f",{{opacity:0}},{{opacity:1,duration:0.3}},{t(102)-ini:.2f});
""")

# 8. Tito: cortar o estresse? (39.8 – 41.85)
tito_fala("t3", 39.8, 41.85, "Então é só cortar o estresse?", 40.0, 41.7, destaque=(3, 4, 5), olhos="duvida", cor_ant=VERDE, tam=70)

# 9. baixar o volume (41.85 – 50.9)
ini, fim = 41.85, 50.9
d = add("volume", ini, fim)
wh, wj = wipe("volume", CREME)
cena("volume", d, f"""
  .bg{{background:#fff;}}
  .titulo{{top:270px;}}
  #volume-qd{{position:absolute;left:80px;top:180px;font-weight:900;font-size:44px;color:#8a837d;}}
  #volume-barra{{position:absolute;left:80px;top:540px;width:920px;height:24px;border-radius:12px;background:#F2ECE2;}}
  #volume-fill{{position:absolute;left:0;top:0;height:24px;width:920px;border-radius:12px;background:linear-gradient(90deg,#95A185,#CE6840);transform-origin:0 50%;}}
  #volume-knob{{position:absolute;left:830px;top:515px;width:74px;height:74px;border-radius:50%;background:var(--verde);box-shadow:0 6px 16px rgba(0,0,0,.25);}}
  #volume-ic{{position:absolute;left:80px;top:390px;font-size:56px;}}
  #volume-ajuda{{position:absolute;left:80px;top:1045px;width:920px;padding:24px 34px;border-radius:26px;background:var(--verde);color:#fff;font-weight:900;font-size:42px;}}
""", f"""
  <div class="bg"></div>
  <div id="volume-qd">Quem dera, né? 😅</div>
  <h1 class="titulo" id="volume-t">Dá pra <em>baixar o volume</em></h1>
  <div id="volume-barra"><div id="volume-fill"></div></div><div id="volume-knob"></div>
  <div class="chip" id="volume-c0" style="top:640px"><span class="i">😴</span>dormir melhor</div>
  <div class="chip" id="volume-c1" style="top:770px"><span class="i">🚶</span>se mexer</div>
  <div class="chip" id="volume-c2" style="top:900px"><span class="i">🤝</span>não brigar com a fome</div>
  <div id="volume-ajuda">💬 Não passa? Procure ajuda</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#volume-qd",{{opacity:0}},{{opacity:1,duration:0.3}},0.2);
  tl.fromTo("#volume-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(126)-ini:.2f});
  tl.fromTo(["#volume-barra","#volume-knob"],{{opacity:0}},{{opacity:1,duration:0.3}},{t(126)-ini:.2f});
  tl.fromTo("#volume-knob",{{x:0}},{{x:-500,duration:1.0,ease:"power2.inOut"}},{t(129)-ini:.2f});
  tl.fromTo("#volume-fill",{{scaleX:1}},{{scaleX:0.42,duration:1.0,ease:"power2.inOut"}},{t(129)-ini:.2f});
  tl.fromTo("#volume-c0",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(132)-ini:.2f});
  tl.fromTo("#volume-c1",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(134)-ini:.2f});
  tl.fromTo("#volume-c2",{{opacity:0,x:-80}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(137)-ini:.2f});
  tl.fromTo("#volume-ajuda",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"back.out(1.6)"}},{t(142)-ini:.2f});
""")

# 10. resumo (50.9 – 58.0)
ini, fim = 50.9, 58.0
d = add("resumo", ini, fim)
wh, wj = wipe("resumo", BRANCO)
txt = "Entendi! Não é o estresse que engorda, é o efeito dominó: cortisol, fome e sono ruim."
cena("resumo", d, """
  .bg{background:var(--creme);}
  .balao .txt{font-size:56px;}
""", f"""
  <div class="bg"></div>
  <div class="balao" id="resumo-balao"><div class="rot">💡 O QUE O TITO ENTENDEU</div>
    <div class="txt">{palavras_html("resumo", txt, 0, (8, 9, 10, 11, 12, 13, 14, 15))}</div><div class="rabo"></div></div>
  <div class="tito-grande" id="resumo-tito">{tito_svg("resumo", bracos="acena")}</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#resumo-balao",{{opacity:0,y:30,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"back.out(1.6)"}},0.12);
  tl.fromTo("#resumo-tito",{{opacity:0,y:120}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.4)"}},0.05);
  {palavras_js("resumo", txt, ini, 51.2, 57.8)}
  {fala_js("resumo", round(51.2 - ini, 2), round(57.8 - ini, 2))}
""")

# 11. CTA (58.0 – fim): reaproveita o CTA do vídeo do café, trocando textos e o eco final
ini, fim = 58.0, TOTAL
d = add("cta", ini, fim)
wh, wj = wipe("cta", CREME)
src4 = (SCR / "build_cafe.py").read_text()
cta_src = src4[src4.index('cena("cta", d, """'):src4.index("# ---------- legendas do narrador")]
cta_src = (cta_src
    .replace(".bg{background:var(--laranja);}", ".bg{background:var(--verde);}\n  #cta-tito{filter:drop-shadow(0 0 2px #FDF3ED) drop-shadow(0 0 2px #FDF3ED);}")  # Tito não some no fundo
    .replace("Manda pra quem diz que <em>café faz mal</em>", "Manda pra quem vive <em>estressado</em>")
    .replace('"☕ 3 xícaras!"', "😌 CALMA")
    .replace("#cta-eco{position:absolute;inset:0;background:var(--mostarda);}", "#cta-eco{position:absolute;inset:0;background:var(--pessego);}")
    .replace("#cta-eco .titulo{color:var(--verde);top:240px;font-size:128px;}", "#cta-eco .titulo{color:var(--verde);top:230px;font-size:128px;}")
    .replace("#cta-eco .titulo em{color:#8E3412;}", "#cta-eco .titulo em{color:var(--laranja);}")
    .replace('<div id="cta-eco-c"></div><h1 class="titulo">Café <em>faz mal?</em></h1>', '<h1 class="titulo">Estresse <em>engorda?</em></h1>')
    .replace("assets/tito-cafe.png", "assets/tito-estresse.png")
    .replace("t(148)", "t(168)").replace("t(149)", "t(169)").replace("t(152)", "t(172)")
    .replace("t(158)", "t(176)").replace("t(159)", "t(177)").replace("t(165)", "t(185)"))
cta_src = cta_src.replace("TOTAL-ini-2.1", "TOTAL-ini-2.3").replace("t(185)-ini-0.05", "t(184)-ini-0.1").replace("t(185)-ini+0.45", "t(185)-ini+0.15")
exec(cta_src)

GRUPOS = [
    ("Estresse *engorda?*", 0, 2), ("Pode, mas *não do jeito* que você pensa.", 2, 8),
    ("*Verdade.*", 18, 1), ("O estresse *em si* não engorda.", 19, 6), ("O que pesa é o que ele *faz com a gente*.", 25, 11),
    ("Quando o estresse *vira rotina*,", 36, 5), ("o corpo mantém o *cortisol alto*.", 41, 6), ("E o cortisol *aumenta a fome*,", 47, 6),
    ("principalmente por *comida bem calórica*.", 53, 5),
    ("*Pode ser.*", 70, 2), ("Mas não é com *todo mundo*:", 72, 6), ("tem gente que *come mais* no estresse", 78, 7), ("e tem gente que *perde a fome*.", 85, 7),
    ("E tem o *sono*.", 92, 4), ("O estresse costuma *piorar o sono*,", 96, 6), ("e quem *dorme pouco* come, em média,", 102, 7),
    ("*quase 400 calorias a mais*", 109, 5), ("no dia seguinte.", 114, 3),
    ("*Quem dera, né?*", 123, 3), ("Mas dá pra *baixar o volume*:", 126, 6), ("*dormir melhor*, *se mexer*", 132, 4), ("e *não brigar com a fome*.", 136, 6),
    ("Se o estresse não passa,", 142, 5), ("vale *procurar ajuda*.", 147, 3),
    ("*Isso aí.*", 166, 2), ("Manda pra quem vive *estressado* no trabalho.", 168, 7), ("E *curte*,", 175, 2),
    ("*comenta CALMA* se você come no estresse", 177, 7), ("e *segue pra mais!*", 184, 4),
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
