#!/usr/bin/env python3
"""Vídeo 13 do cronograma: "Por que não consigo parar de rolar o feed?" (estrutura Contradição)."""
import json, math, re, shutil
from pathlib import Path

SCR = Path("/tmp/claude-0/-home-user-Victor1Paim/bc508778-dc0e-5c3d-a4a6-a9dce8035bd2/scratchpad")
POST = Path("/home/user/Victor1Paim/saude-sem-sermao/producoes/13-rolar-o-feed")
V = POST / "video"
(V / "compositions").mkdir(parents=True, exist_ok=True)
(V / "assets").mkdir(exist_ok=True)
for f in ["hyperframes.json", "package.json", "meta.json"]:
    (V / f).write_text((SCR / "hfblank" / f).read_text().replace('"hfblank"', '"saude-sem-sermao-13-feed"'))
shutil.copy(POST / "dialogo.mp3", V / "assets/voz.mp3")
shutil.copy(POST / "imagens/tito-feed.png", V / "assets/tito-feed.png")

W, H = 1080, 1920
TOTAL = 69.6
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
TERRA = "#CE6840"

# 1. capa (0 – 5.6)
d = add("capa", 0, 5.6)
cena("capa", d, f"""
  .bg{{background:{TERRA};}}
  .titulo{{color:var(--creme2);top:230px;font-size:104px;}}
  .titulo em{{color:#1F3328;}}
  #capa-c{{position:absolute;left:170px;top:760px;width:740px;height:740px;border-radius:50%;background:var(--creme);}}
  #capa-img{{left:220px;top:860px;width:640px;height:580px;}}
  #capa-rel{{position:absolute;left:80px;top:620px;padding:10px 28px;border-radius:999px;background:rgba(18,22,18,.85);color:#fff;font-weight:900;font-size:50px;font-variant-numeric:tabular-nums;}}
  #capa-selo{{left:620px;top:630px;color:#fff;border-color:#fff;background:transparent;font-size:40px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="capa-t">Por que não consigo <em>parar de rolar?</em></h1>
  <div id="capa-c"></div>
  <div class="img" id="capa-img"><img src="assets/tito-feed.png"></div>
  <div id="capa-rel">📱 21:00</div>
  <div class="selo" id="capa-selo">FRAQUEZA?</div>
""", f"""
  (function(){{const o={{v:0}};const el=document.querySelector("#capa-rel");
    tl.fromTo(o,{{v:0}},{{v:64,duration:1.0,ease:"power2.in",onUpdate:()=>{{const m=Math.round(o.v);el.textContent="📱 "+String(21+Math.floor(m/60))+":"+String(m%60).padStart(2,"0");}}}},{t(11)-0.1:.2f});}})();
  tl.fromTo("#capa-selo",{{opacity:0,scale:2.2,rotation:-12}},{{opacity:1,scale:1,rotation:-5,duration:0.22,ease:"power4.in"}},{t(14)-0.05:.2f});
  tl.fromTo("#capa-img",{{y:0}},{{y:-8,duration:0.5,ease:"sine.inOut",yoyo:true,repeat:9}},0);
""")

# 2. Tito (5.6 – 7.9)
tito_fala("t1", 5.6, 7.9, "Claro! Eu é que sou fraco pra celular.", 5.68, 7.7, destaque=(5,), olhos="normal", cor_ant=TERRA, tam=66)

# 3. tempo (7.9 – 15.75)
ini, fim = 7.9, 15.75
d = add("tempo", ini, fim)
wh, wj = wipe("tempo", CREME)
cena("tempo", d, f"""
  .bg{{background:#fff;}}
  .titulo{{top:250px;}}
  .barra{{position:absolute;left:80px;height:110px;border-radius:24px;display:flex;align-items:center;padding:0 30px;font-weight:900;font-size:42px;color:#fff;transform-origin:0 50%;}}
  #tempo-r{{position:absolute;left:80px;top:900px;width:920px;font-weight:900;font-size:44px;color:var(--verde);}}
  .fonte{{top:1060px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="tempo-t">Quase <em>4 h por dia</em> nas redes</h1>
  <div class="barra" id="tempo-b1" style="top:520px;width:920px;background:{TERRA}">🇧🇷 Brasil · 3h49</div>
  <div class="barra" id="tempo-b2" style="top:660px;width:567px;background:#95A185">🌍 mundo · 2h21</div>
  <div id="tempo-r">Não dá pra ser só fraqueza de todo mundo.</div>
  <div class="fonte" id="tempo-f">Fonte: DataReportal/We Are Social via Statista, fev. 2025</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#tempo-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{max(t(28)-ini,0.15):.2f});
  tl.fromTo("#tempo-b1",{{scaleX:0}},{{scaleX:1,duration:0.8,ease:"power2.out"}},{t(32)-ini:.2f});
  tl.fromTo(["#tempo-b2","#tempo-f"],{{scaleX:0,opacity:0}},{{scaleX:1,opacity:1,duration:0.6,ease:"power2.out"}},{t(39)-ini:.2f});
  tl.fromTo("#tempo-r",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.35}},{t(45)-ini-0.3:.2f});
""")

# 4. revista x feed (15.75 – 22.55)
ini, fim = 15.75, 22.55
d = add("revista", ini, fim)
wh, wj = wipe("revista", BRANCO)
cena("revista", d, f"""
  .bg{{background:#EEF0EA;}}
  .lado{{position:absolute;top:300px;width:440px;height:760px;border-radius:30px;background:#fff;box-shadow:0 14px 40px rgba(40,60,40,.12);overflow:hidden;}}
  .rot{{position:absolute;left:0;right:0;top:26px;text-align:center;font-weight:900;font-size:40px;}}
  #revista-pg{{position:absolute;left:70px;top:150px;width:300px;height:400px;border-radius:12px;background:#F7E5DD;border:6px solid #2B2B2B;display:flex;align-items:center;justify-content:center;
              font-family:'Playfair Display',serif;font-weight:800;font-size:90px;color:{TERRA};transform-origin:0 50%;}}
  #revista-pp{{position:absolute;left:30px;top:600px;width:380px;text-align:center;font-weight:900;font-size:36px;color:var(--verde);}}
  #revista-tela{{position:absolute;left:90px;top:130px;width:260px;height:470px;border-radius:30px;background:#1E1E1E;padding:12px;}}
  #revista-scroll{{position:relative;width:100%;height:100%;border-radius:20px;background:#fff;overflow:hidden;}}
  #revista-lista{{position:absolute;left:10px;top:10px;width:216px;}}
  .post{{width:216px;height:110px;border-radius:14px;margin-bottom:10px;}}
  #revista-inf{{position:absolute;left:30px;top:620px;width:380px;text-align:center;font-weight:900;font-size:64px;color:{TERRA};}}
""", f"""
  <div class="bg"></div>
  <div class="lado" id="revista-a" style="left:80px"><div class="rot">📖 revista</div><div id="revista-pg">FIM</div><div id="revista-pp">✋ ponto de parada</div></div>
  <div class="lado" id="revista-b" style="left:560px"><div class="rot">📱 feed</div>
    <div id="revista-tela"><div id="revista-scroll"><div id="revista-lista">{''.join(f'<div class="post" style="background:{c}"></div>' for c in ["#CE6840","#E2B04A","#95A185","#F7E5DD"]*4)}</div></div></div>
    <div id="revista-inf">∞</div></div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#revista-a",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.35,ease:"back.out(1.6)"}},{max(t(55)-ini,0.15):.2f});
  tl.fromTo("#revista-pg",{{rotationY:-70,opacity:0.3}},{{rotationY:0,opacity:1,duration:0.6,ease:"power2.out"}},{t(59)-ini:.2f});
  tl.fromTo("#revista-pp",{{opacity:0}},{{opacity:1,duration:0.3}},{t(65)-ini:.2f});
  tl.fromTo("#revista-b",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.35,ease:"back.out(1.6)"}},{t(68)-ini:.2f});
  tl.fromTo("#revista-lista",{{y:0}},{{y:-900,duration:{fim-t(68)+0.3:.2f},ease:"none"}},{t(68)-ini:.2f});
  tl.fromTo("#revista-inf",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2)"}},{t(71)-ini:.2f});
""")

# 5. Tito (22.55 – 24.9)
tito_fala("t2", 22.55, 24.9, "Mas eu podia simplesmente parar, né?", 22.6, 24.8, destaque=(4,), olhos="duvida", cor_ant="#EEF0EA", tam=66)

# 6. caça-níquel (24.9 – 33.6)
ini, fim = 24.9, 33.6
d = add("slot", ini, fim)
wh, wj = wipe("slot", CREME)
cena("slot", d, f"""
  .bg{{background:var(--pessego);}}
  #slot-pod{{position:absolute;left:80px;top:190px;font-weight:900;font-size:44px;color:#8a837d;}}
  #slot-maq{{position:absolute;left:150px;top:330px;width:780px;height:330px;border-radius:40px;background:#2F483A;box-shadow:0 18px 44px rgba(0,0,0,.2);display:flex;gap:30px;align-items:center;justify-content:center;}}
  .rolo{{width:200px;height:220px;border-radius:24px;background:#fff;display:flex;align-items:center;justify-content:center;font-size:130px;}}
  .tag{{position:absolute;top:700px;padding:12px 26px;border-radius:999px;background:#fff;font-weight:900;font-size:38px;}}
  #slot-r{{position:absolute;left:80px;top:840px;width:920px;padding:24px 34px;border-radius:26px;background:#fff;font-weight:900;font-size:42px;}}
  #slot-p{{position:absolute;left:80px;top:1010px;width:920px;font-weight:900;font-size:44px;color:var(--verde);}}
""", f"""
  <div class="bg"></div>
  <div id="slot-pod">Podia. Mas repara… 👀</div>
  <div id="slot-maq"><div class="rolo" id="slot-r0">😐</div><div class="rolo" id="slot-r1">😐</div><div class="rolo" id="slot-r2">😐</div></div>
  <div class="tag" id="slot-a" style="left:150px">chato</div><div class="tag" id="slot-b" style="left:430px">chato</div><div class="tag" id="slot-c" style="left:710px;background:{TERRA};color:#fff">ótimo! 😍</div>
  <div id="slot-r">🎁 recompensa que você não sabe quando vem</div>
  <div id="slot-p">= o mesmo princípio do caça-níquel 🎰</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#slot-pod",{{opacity:0}},{{opacity:1,duration:0.3}},0.1);
  tl.fromTo("#slot-maq",{{opacity:0,scale:0.9}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(1.6)"}},0.3);
  {' '.join(f'tl.fromTo(".rolo",{{y:-20}},{{y:0,duration:0.1,stagger:0.05,ease:"none"}},{x:.2f});' for x in [t(83)-ini, t(85)-ini, t(88)-ini])}
  tl.fromTo("#slot-a",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.25}},{t(84)-ini:.2f});
  tl.fromTo("#slot-b",{{opacity:0,y:20}},{{opacity:1,y:0,duration:0.25}},{t(85)-ini:.2f});
  tl.set("#slot-r1",{{textContent:"😍"}},{t(90)-ini:.2f});
  tl.fromTo("#slot-r1",{{scale:1}},{{scale:1.25,duration:0.18,yoyo:true,repeat:3}},{t(90)-ini:.2f});
  tl.fromTo("#slot-c",{{opacity:0,y:20,scale:0.6}},{{opacity:1,y:0,scale:1,duration:0.3,ease:"back.out(2.2)"}},{t(90)-ini:.2f});
  tl.fromTo("#slot-r",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.35,ease:"back.out(1.6)"}},{t(91)-ini:.2f});
  tl.fromTo("#slot-p",{{opacity:0}},{{opacity:1,duration:0.3}},{t(98)-ini:.2f});
""")

# 7. VIRADA (33.6 – 40.95)
ini, fim = 33.6, 40.95
d = add("virada", ini, fim)
wh, wj = wipe("virada", PESSEGO)
cena("virada", d, f"""
  .bg{{background:var(--verde);}}
  .titulo{{color:var(--creme2);top:250px;}}
  .titulo em{{color:var(--mostarda);}}
  #virada-q{{position:absolute;left:80px;top:500px;width:920px;padding:30px 36px;border-radius:30px;background:#fff;font-weight:900;font-size:42px;line-height:1.3;}}
  #virada-q .a{{display:block;margin-top:12px;font-size:30px;color:#8a837d;}}
  #virada-selo{{left:300px;top:840px;color:var(--mostarda);border-color:var(--mostarda);background:transparent;font-size:52px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="virada-t">Feito pra <em>não ter fim</em></h1>
  <div id="virada-q">🎙️ O criador da rolagem infinita disse publicamente que <span style="color:var(--laranja)">se arrepende</span>.<span class="a">Aza Raskin, em entrevistas (opinião dele)</span></div>
  <div class="selo" id="virada-selo">✕ SÓ FRAQUEZA</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#virada-q",{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.4,ease:"back.out(1.6)"}},{t(111)-ini:.2f});
  tl.fromTo("#virada-selo",{{opacity:0,scale:2.4,rotation:-14}},{{opacity:1,scale:1,rotation:-6,duration:0.22,ease:"power4.in"}},{t(106)-ini:.2f});
  tl.fromTo("#root",{{x:0}},{{x:10,duration:0.04,yoyo:true,repeat:5,ease:"none"}},{t(106)-ini+0.22:.2f});
  tl.fromTo("#virada-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(121)-ini:.2f});
""")

# 8. saída (40.95 – 48.7)
ini, fim = 40.95, 48.7
d = add("saida", ini, fim)
wh, wj = wipe("saida", VERDE)
cena("saida", d, f"""
  .bg{{background:#fff;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="saida-t">Devolva os <em>pontos de parada</em></h1>
  <div class="chip" id="saida-a" style="top:520px"><span class="i">⏲️</span>limite de tempo no app</div>
  <div class="chip" id="saida-b" style="top:660px"><span class="i">📲</span>app fora da tela inicial</div>
  <div class="chip" id="saida-c" style="top:800px"><span class="i">🛏️</span>celular longe na hora de dormir</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#saida-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{max(t(129)-ini,0.15):.2f});
  tl.fromTo("#saida-a",{{opacity:0,x:-100}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(136)-ini:.2f});
  tl.fromTo("#saida-b",{{opacity:0,x:-100}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(141)-ini:.2f});
  tl.fromTo("#saida-c",{{opacity:0,x:-100}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(147)-ini:.2f});
""")

# 9. resumo (48.7 – 54.95)
ini, fim = 48.7, 54.95
d = add("resumo", ini, fim)
wh, wj = wipe("resumo", BRANCO)
txt = "Entendi! Não é só fraqueza: o feed não tem fim de propósito. Então eu crio o meu fim."
cena("resumo", d, """
  .bg{background:var(--creme);}
  .balao .txt{font-size:56px;}
""", f"""
  <div class="bg"></div>
  <div class="balao" id="resumo-balao"><div class="rot">💡 O QUE O TITO ENTENDEU</div>
    <div class="txt">{palavras_html("resumo", txt, 0, (7, 8, 9, 10, 11, 14, 15, 16, 17))}</div><div class="rabo"></div></div>
  <div class="tito-grande" id="resumo-tito">{tito_svg("resumo", bracos="acena")}</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#resumo-balao",{{opacity:0,y:30,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"back.out(1.6)"}},0.06);
  tl.fromTo("#resumo-tito",{{opacity:0,y:120}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.4)"}},0.05);
  {palavras_js("resumo", txt, ini, 48.78, 54.7)}
  {fala_js("resumo", round(48.78 - ini, 2), round(54.7 - ini, 2))}
""")

# 10. resposta + eco (54.95 – 58.1)
ini, fim = 54.95, 58.1
d = add("resposta", ini, fim)
wh, wj = wipe("resposta", CREME)
cena("resposta", d, f"""
  .bg{{background:{TERRA};}}
  .titulo{{color:var(--creme2);top:250px;font-size:96px;}}
  .titulo em{{color:#1F3328;}}
  #resposta-c{{position:absolute;left:230px;top:700px;width:620px;height:620px;border-radius:50%;background:var(--creme);}}
  #resposta-img{{left:270px;top:780px;width:540px;height:490px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="resposta-t">Falta de força de vontade? <em>Não só.</em></h1>
  <div id="resposta-c"></div>
  <div class="img" id="resposta-img"><img src="assets/tito-feed.png"></div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#resposta-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.12);
  tl.fromTo("#resposta-t em",{{scale:1}},{{scale:1.08,duration:0.18,yoyo:true,repeat:1}},{t(179)-ini:.2f});
  tl.fromTo(["#resposta-c","#resposta-img"],{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.4,ease:"back.out(1.6)"}},0.2);
""")

# 11. CTA (58.1 – fim)
ini, fim = 58.1, TOTAL
d = add("cta", ini, fim)
wh, wj = wipe("cta", CREME)
src4 = (SCR / "build_cafe.py").read_text()
cta_src = src4[src4.index('cena("cta", d, """'):src4.index("# ---------- legendas do narrador")]
cta_src = (cta_src
    .replace(".bg{background:var(--laranja);}", ".bg{background:var(--verde);}\n  #cta-tito{filter:drop-shadow(0 0 2px #FDF3ED) drop-shadow(0 0 2px #FDF3ED);}")  # Tito não some no fundo
    .replace("Manda pra quem diz que <em>café faz mal</em>", "Manda pra quem vive no <em>“só mais um”</em>")
    .replace('"☕ 3 xícaras!"', "⏹️ FIM")
    .replace("#cta-eco{position:absolute;inset:0;background:var(--mostarda);}", "#cta-eco{position:absolute;inset:0;background:#CE6840;}")
    .replace("#cta-eco .titulo{color:var(--verde);top:240px;font-size:128px;}", "#cta-eco .titulo{color:#FDF3ED;top:230px;font-size:104px;}\n  #cta-eco-c2{position:absolute;left:170px;top:760px;width:740px;height:740px;border-radius:50%;background:var(--creme);}")
    .replace("#cta-eco .titulo em{color:#8E3412;}", "#cta-eco .titulo em{color:#1F3328;}")
    .replace('<div id="cta-eco-c"></div><h1 class="titulo">Café <em>faz mal?</em></h1>', '<div id="cta-eco-c2"></div><h1 class="titulo">Por que não consigo <em>parar de rolar?</em></h1>')
    .replace("assets/tito-cafe.png", "assets/tito-feed.png")
    .replace("#cta-eco-img{left:300px;top:500px;width:480px;height:570px;}", "#cta-eco-img{left:220px;top:860px;width:640px;height:580px;}")
    .replace("t(165)-ini-0.05", "t(207)-ini-0.6").replace("t(165)-ini+0.45", "t(207)-ini+0.15")
    .replace("TOTAL-ini-2.1", "TOTAL-ini-2.3")
    .replace("t(165)", "t(207)").replace("t(159)", "t(194)").replace("t(158)", "t(193)")
    .replace("t(152)", "t(188)").replace("t(148)", "t(183)").replace("t(149)", "t(184)"))
exec(cta_src)

GRUPOS = [
    ("Você abre o app pra ver *uma coisinha*", 0, 8), ("e, quando vê, *passou uma hora*.", 8, 6), ("*Falta de força de vontade?*", 14, 5),
    ("O brasileiro passa, em média,", 27, 5), ("*quase 4 horas por dia* nas redes.", 32, 7), ("É *um dos maiores tempos* do mundo.", 39, 7),
    ("Não dá pra ser *só fraqueza* de todo mundo.", 46, 9),
    ("Pensa numa revista: *ela acaba*.", 55, 5), ("A última página é *um ponto de parada*.", 60, 8), ("O feed *não tem última página*.", 68, 6),
    ("*Podia.* Mas repara:", 80, 3), ("vídeo chato, chato,", 83, 3), ("e, de repente, *um ótimo*.", 86, 5),
    ("*Recompensa que você não sabe quando vem*:", 91, 7), ("é o mesmo princípio *do caça-níquel*.", 98, 7),
    ("Isso *não é teoria da conspiração*:", 105, 6), ("o criador da *rolagem infinita*", 111, 5), ("disse publicamente que *se arrepende*.", 116, 5),
    ("Ela foi feita *pra não ter fim*.", 121, 7),
    ("A saída é *devolver os pontos de parada*:", 128, 8), ("*limite de tempo* no app,", 136, 5), ("*tirar o app* da tela inicial", 141, 6), ("e *celular longe* na hora de dormir.", 147, 7),
    ("Então, é *falta de força de vontade?*", 172, 7), ("*Não só.*", 179, 2),
    ("*Isso aí.*", 181, 2), ("Manda pra quem vive no *“só mais um vídeo”*.", 183, 9), ("E *curte*,", 192, 2),
    ("*comenta FIM* se você vai criar", 194, 7), ("o seu *ponto de parada*", 201, 5), ("e *segue pra mais!*", 206, 4),
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
