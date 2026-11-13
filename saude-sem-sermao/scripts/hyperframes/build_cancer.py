#!/usr/bin/env python3
"""Vídeo 11 do cronograma: "Câncer: o que dá pra mudar no risco" (estrutura Problema)."""
import json, math, re, shutil
from pathlib import Path

SCR = Path("/tmp/claude-0/-home-user-Victor1Paim/bc508778-dc0e-5c3d-a4a6-a9dce8035bd2/scratchpad")
POST = Path("/home/user/Victor1Paim/saude-sem-sermao/producoes/11-cancer-risco")
V = POST / "video"
(V / "compositions").mkdir(parents=True, exist_ok=True)
(V / "assets").mkdir(exist_ok=True)
for f in ["hyperframes.json", "package.json", "meta.json"]:
    (V / f).write_text((SCR / "hfblank" / f).read_text().replace('"hfblank"', '"saude-sem-sermao-11-cancer"'))
shutil.copy(POST / "dialogo.mp3", V / "assets/voz.mp3")
shutil.copy(POST / "imagens/tito-lista.png", V / "assets/tito-lista.png")

W, H = 1080, 1920
TOTAL = 67.0
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
  .cont{position:absolute;left:730px;top:190px;width:270px;padding:12px 0;border-radius:999px;background:var(--verde);color:#fff;text-align:center;font-weight:900;font-size:46px;}
  .item{position:absolute;left:80px;width:920px;padding:18px 28px;border-radius:24px;background:#fff;box-shadow:0 10px 28px rgba(40,60,40,.12);
        font-weight:900;font-size:42px;display:flex;align-items:center;gap:22px;}
  .item .n{width:72px;height:72px;border-radius:50%;background:var(--verde);color:#fff;display:flex;align-items:center;justify-content:center;font-family:'Playfair Display',serif;font-size:48px;flex:none;}
  .item small{display:block;font-size:28px;color:#8a837d;font-weight:800;}
"""
CC = "#F2ECE2"

# 1. capa (0 – 5.0)
d = add("capa", 0, 5.0)
cena("capa", d, f"""
  .bg{{background:{CC};}}
  .titulo{{color:var(--verde);top:230px;font-size:116px;}}
  .titulo em{{color:var(--laranja);}}
  .bola{{position:absolute;top:620px;width:150px;height:150px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'Playfair Display',serif;font-weight:800;font-size:80px;color:#fff;box-shadow:0 10px 26px rgba(0,0,0,.2);}}
  #capa-img{{left:320px;top:830px;width:440px;height:470px;}}
  #capa-selo{{left:80px;top:500px;color:var(--verde);border-color:var(--verde);font-size:40px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="capa-t">Câncer: o que dá pra <em>mudar?</em></h1>
  {''.join(f'<div class="bola" id="capa-b{i}" style="left:{90+i*190}px;background:{c};color:{"#1F3328" if i<2 else "#fff"}">?</div>' for i,c in enumerate(["#95A185","#E2B04A","#D45F2B","#3B6EA5","#2F483A"]))}
  <div class="selo" id="capa-selo">não é só sorte</div>
  <div class="img" id="capa-img"><img src="assets/tito-lista.png"></div>
""", f"""
  {' '.join(f'tl.fromTo("#capa-b{i}",{{rotation:0,y:0}},{{rotation:360,y:-30,duration:0.5,ease:"sine.inOut",yoyo:true,repeat:3}},{i*0.08:.2f});' for i in range(5))}
  tl.fromTo("#capa-selo",{{opacity:0,scale:2.2,rotation:-12}},{{opacity:1,scale:1,rotation:-5,duration:0.22,ease:"power4.in"}},{t(7)-0.05:.2f});
""")

# 2. Tito (5.0 – 7.15)
tito_fala("t1", 5.0, 7.15, "Ué, mas não é tudo genética?", 5.1, 6.95, destaque=(4, 5), olhos="duvida", cor_ant=CC, tam=72)

# 3. dado (7.15 – 15.5)
ini, fim = 7.15, 15.5
d = add("dado", ini, fim)
wh, wj = wipe("dado", CREME)
cena("dado", d, f"""
  .bg{{background:#fff;}}
  .titulo{{top:300px;}}
  .p{{position:absolute;width:150px;height:240px;}}
  #dado-l{{position:absolute;left:80px;top:1010px;font-weight:900;font-size:40px;}}
  .fonte{{top:1080px;}}
""", f"""
  <div class="bg"></div>
  <div class="cont" id="dado-cont">0/5</div>
  <h1 class="titulo" id="dado-t">Genética pesa, mas <em>4 em cada 10</em> casos…</h1>
  {''.join(f'<svg class="p" id="dado-p{i}" style="left:{90+(i%5)*185}px;top:{500+(i//5)*260}px" viewBox="0 0 60 100"><circle cx="30" cy="18" r="14" fill="#C9C3BA" class="pc"/><rect x="10" y="36" width="40" height="60" rx="18" fill="#C9C3BA" class="pc"/></svg>' for i in range(10))}
  <div id="dado-l">…ligados a coisas que <span style="color:var(--laranja)">dá pra mudar</span></div>
  <div class="fonte" id="dado-f">Fonte: Islami et al., CA Cancer J Clin, 2024 (EUA, adultos 30+)</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#dado-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.2);
  {' '.join(f'tl.fromTo("#dado-p{i}",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.25}},{0.4+i*0.06:.2f});' for i in range(10))}
  {' '.join(f'tl.to("#dado-p{i} .pc",{{fill:"#D45F2B",duration:0.2}},{t(27)-ini+i*0.25:.2f});' for i in range(4))}
  tl.fromTo(["#dado-l","#dado-f"],{{opacity:0}},{{opacity:1,duration:0.3}},{t(32)-ini:.2f});
  tl.fromTo("#dado-cont",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2.2)"}},{t(40)-ini:.2f});
""")

# 4. lista 1–4 (15.5 – 33.15)
ini, fim = 15.5, 33.15
d = add("lista", ini, fim)
wh, wj = wipe("lista", BRANCO)
IT = [("🚬", "cigarro", "o maior · parar ajuda em qualquer idade", 44), ("⚖️", "excesso de peso", "", 58),
      ("🍺", "álcool", "pra câncer, não há dose totalmente segura", 62), ("☀️", "sol sem proteção", "câncer de pele", 74)]
cena("lista", d, f"""
  .bg{{background:#EEF0EA;}}
  #lista-t{{position:absolute;left:80px;top:200px;font-family:'Playfair Display',serif;font-weight:700;font-size:66px;}}
  #lista-t em{{color:var(--laranja);font-style:italic;}}
  #lista-tito{{position:absolute;left:640px;top:1000px;width:200px;height:220px;}}
  #lista-bal{{position:absolute;left:640px;top:900px;padding:14px 26px;border-radius:22px;background:#fff;font-weight:900;font-size:38px;box-shadow:0 10px 28px rgba(0,0,0,.12);}}
""", f"""
  <div class="bg"></div>
  <div class="cont" id="lista-cont">0/5</div>
  <h1 id="lista-t">O que <em>dá pra mudar</em></h1>
  {''.join(f'<div class="item" id="lista-i{i}" style="top:{340+i*150}px"><div class="n">{i+1}</div><span style="font-size:56px">{e}</span><div>{n}{f"<small>{s}</small>" if s else ""}</div></div>' for i,(e,n,s,_) in enumerate(IT))}
  <div id="lista-bal">💬 E o quarto?</div>
  <div class="tito-mini" id="lista-tito">{tito_svg("lista", olhos="duvida")}</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#lista-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.15);
  {' '.join(f'tl.fromTo("#lista-i{i}",{{opacity:0,x:-120}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(k)-ini-0.1:.2f});tl.set("#lista-cont",{{textContent:"{i+1}/5"}},{t(k)-ini:.2f});tl.fromTo("#lista-cont",{{scale:1}},{{scale:1.15,duration:0.12,yoyo:true,repeat:1}},{t(k)-ini:.2f});' for i,(_,_,_,k) in enumerate(IT))}
  tl.fromTo(["#lista-bal","#lista-tito"],{{opacity:0,y:40}},{{opacity:1,y:0,duration:0.3,ease:"back.out(1.6)"}},{t(71)-ini-0.15:.2f});
  tl.to(["#lista-bal","#lista-tito"],{{opacity:0,duration:0.25}},{t(75)-ini+0.6:.2f});
""")

# 5. VIRADA: vacina (33.15 – 40.9)
ini, fim = 33.15, 40.9
d = add("vacina", ini, fim)
wh, wj = wipe("vacina", "#EEF0EA")
cena("vacina", d, f"""
  .bg{{background:var(--verde);}}
  .titulo{{color:var(--creme2);top:300px;}}
  .titulo em{{color:var(--mostarda);}}
  #vacina-n{{position:absolute;left:80px;top:500px;width:920px;padding:24px 34px;border-radius:30px;background:#fff;display:flex;align-items:center;gap:26px;font-weight:900;font-size:60px;}}
  #vacina-n .n{{width:110px;height:110px;border-radius:50%;background:var(--laranja);color:#fff;display:flex;align-items:center;justify-content:center;font-family:'Playfair Display',serif;font-size:72px;}}
  .vchip{{position:absolute;padding:14px 30px;border-radius:999px;font-weight:900;font-size:42px;color:#1F3328;background:var(--mostarda);}}
  .fonte{{top:1080px;color:#c9d3c6;}}
""", f"""
  <div class="bg"></div>
  <div class="cont" id="vacina-cont" style="background:var(--laranja)">5/5</div>
  <h1 class="titulo" id="vacina-t">O 5, que <em>pouca gente sabe</em></h1>
  <div id="vacina-n"><div class="n">5</div>💉 vacina</div>
  <div class="vchip" id="vacina-a" style="left:80px;top:720px">HPV</div>
  <div class="vchip" id="vacina-b" style="left:300px;top:720px">hepatite B</div>
  <div class="vchip" id="vacina-c" style="left:80px;top:840px;background:#fff">✓ estão no SUS</div>
  <div class="fonte" id="vacina-f">Fonte: Ministério da Saúde (PNI); INCA</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#vacina-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.15);
  tl.fromTo("#vacina-cont",{{scale:0.5,opacity:0}},{{scale:1,opacity:1,duration:0.3,ease:"back.out(2.4)"}},{t(86)-ini:.2f});
  tl.fromTo("#vacina-n",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.4,ease:"back.out(2)"}},{t(91)-ini-0.1:.2f});
  tl.fromTo("#root",{{x:0}},{{x:10,duration:0.04,yoyo:true,repeat:5,ease:"none"}},{t(91)-ini+0.3:.2f});
  tl.fromTo("#vacina-a",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.3,ease:"back.out(2)"}},{t(94)-ini:.2f});
  tl.fromTo("#vacina-b",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.3,ease:"back.out(2)"}},{t(98)-ini:.2f});
  tl.fromTo("#vacina-f",{{opacity:0}},{{opacity:1,duration:0.3}},{t(91)-ini:.2f});
  tl.fromTo("#vacina-c",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.3,ease:"back.out(2)"}},{t(102)-ini:.2f});
""")

# 6. ressalva (40.9 – 48.4)
ini, fim = 40.9, 48.4
d = add("ressalva", ini, fim)
wh, wj = wipe("ressalva", VERDE)
cena("ressalva", d, f"""
  .bg{{background:var(--pessego);}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="ressalva-t">Diminui o risco, <em>não zera</em></h1>
  <div class="chip" id="ressalva-a" style="top:520px"><span class="i">💛</span>ninguém tem câncer por merecer</div>
  <div class="chip" id="ressalva-b" style="top:660px"><span class="i">🩺</span>rastreamento: combine com o médico</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#ressalva-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{max(t(106)-ini,0.15):.2f});
  tl.fromTo("#ressalva-a",{{opacity:0,x:-100}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(112)-ini:.2f});
  tl.fromTo("#ressalva-b",{{opacity:0,x:-100}},{{opacity:1,x:0,duration:0.35,ease:"back.out(1.6)"}},{t(117)-ini:.2f});
""")

# 7. resumo (48.4 – 54.45)
ini, fim = 48.4, 54.45
d = add("resumo", ini, fim)
wh, wj = wipe("resumo", PESSEGO)
txt = "Entendi! Não é só sorte: cigarro, peso, álcool, sol e vacina estão nas nossas mãos."
cena("resumo", d, """
  .bg{background:var(--creme);}
  .balao .txt{font-size:56px;}
""", f"""
  <div class="bg"></div>
  <div class="balao" id="resumo-balao"><div class="rot">💡 O QUE O TITO ENTENDEU</div>
    <div class="txt">{palavras_html("resumo", txt, 0, (5, 6, 7, 8, 10, 13, 14))}</div><div class="rabo"></div></div>
  <div class="tito-grande" id="resumo-tito">{tito_svg("resumo", bracos="acena")}</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#resumo-balao",{{opacity:0,y:30,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"back.out(1.6)"}},0.08);
  tl.fromTo("#resumo-tito",{{opacity:0,y:120}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.4)"}},0.05);
  {palavras_js("resumo", txt, ini, 48.5, 54.2)}
  {fala_js("resumo", round(48.5 - ini, 2), round(54.2 - ini, 2))}
""")

# 8. resposta + eco (54.45 – 58.05)
ini, fim = 54.45, 58.05
d = add("resposta", ini, fim)
wh, wj = wipe("resposta", CREME)
cena("resposta", d, f"""
  .bg{{background:{CC};}}
  .titulo{{color:var(--verde);top:260px;font-size:104px;}}
  .titulo em{{color:var(--laranja);}}
  #resposta-img{{left:270px;top:680px;width:540px;height:580px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="resposta-t">Câncer é loteria? <em>Não totalmente.</em></h1>
  <div class="img" id="resposta-img"><img src="assets/tito-lista.png"></div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#resposta-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.12);
  tl.fromTo("#resposta-t em",{{scale:1}},{{scale:1.06,duration:0.18,yoyo:true,repeat:1}},{t(147)-ini:.2f});
  tl.fromTo("#resposta-img",{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.4,ease:"back.out(1.6)"}},0.2);
""")

# 9. CTA (58.05 – fim)
ini, fim = 58.05, TOTAL
d = add("cta", ini, fim)
wh, wj = wipe("cta", CREME)
src4 = (SCR / "build_cafe.py").read_text()
cta_src = src4[src4.index('cena("cta", d, """'):src4.index("# ---------- legendas do narrador")]
cta_src = (cta_src
    .replace(".bg{background:var(--laranja);}", ".bg{background:var(--verde);}\n  #cta-tito{filter:drop-shadow(0 0 2px #FDF3ED) drop-shadow(0 0 2px #FDF3ED);}")  # Tito não some no fundo
    .replace("Manda pra quem diz que <em>café faz mal</em>", "Manda pra quem diz <em>“é genética”</em>")
    .replace('"☕ 3 xícaras!"', "qual dos 5?")
    .replace("#cta-eco{position:absolute;inset:0;background:var(--mostarda);}", "#cta-eco{position:absolute;inset:0;background:#F2ECE2;}")
    .replace("#cta-eco .titulo{color:var(--verde);top:240px;font-size:128px;}", "#cta-eco .titulo{color:var(--verde);top:230px;font-size:116px;}")
    .replace("#cta-eco .titulo em{color:#8E3412;}", "#cta-eco .titulo em{color:var(--laranja);}")
    .replace('<div id="cta-eco-c"></div><h1 class="titulo">Café <em>faz mal?</em></h1>', '<h1 class="titulo">Câncer: o que dá pra <em>mudar?</em></h1>')
    .replace("assets/tito-cafe.png", "assets/tito-lista.png")
    .replace("#cta-eco-img{left:300px;top:500px;width:480px;height:570px;}", "#cta-eco-img{left:270px;top:640px;width:540px;height:620px;}")
    .replace("t(165)-ini-0.05", "t(168)-ini-0.6").replace("t(165)-ini+0.45", "t(168)-ini+0.15")
    .replace("TOTAL-ini-2.1", "TOTAL-ini-2.3")
    .replace("t(165)", "t(168)").replace("t(159)", "t(161)").replace("t(158)", "t(160)")
    .replace("t(152)", "t(157)").replace("t(148)", "t(151)").replace("t(149)", "t(152)"))
exec(cta_src)

GRUPOS = [
    ("Câncer parece *loteria*.", 0, 3), ("Mas uma parte grande", 3, 4), ("*não é sorte nem azar*.", 7, 5),
    ("*Genética pesa*, sim.", 18, 3), ("Mas um estudo grande estimou", 21, 5), ("que *4 em cada 10 casos*", 26, 6),
    ("estão ligados a coisas *que dá pra mudar*.", 32, 8), ("Vou te mostrar *5*.", 40, 4),
    ("*1: cigarro.*", 44, 2), ("Sozinho, é *o maior de todos*.", 46, 6), ("E parar ajuda *em qualquer idade*.", 52, 6),
    ("*2: excesso de peso.*", 58, 4), ("*3: álcool.*", 62, 2), ("Pra câncer, não existe", 64, 4), ("*dose totalmente segura*.", 68, 3),
    ("*4: sol sem proteção*,", 74, 4), ("que pesa no *câncer de pele*.", 78, 6),
    ("E o 5, que *pouca gente sabe*:", 84, 7), ("*vacina.*", 91, 1), ("A do *HPV* e a da *hepatite B*", 92, 8),
    ("*previnem câncer*.", 100, 2), ("E estão *no SUS*.", 102, 4),
    ("Isso *diminui o risco, não zera*.", 106, 6), ("*Ninguém tem câncer por merecer.*", 112, 5),
    ("E os exames de rastreamento,", 117, 5), ("a gente *combina com o médico*.", 122, 6),
    ("Então, *câncer é loteria?*", 143, 4), ("*Não totalmente.*", 147, 2),
    ("*Isso aí.*", 149, 2), ("Manda pra quem acha que *é tudo genética*.", 151, 8), ("E *curte*,", 159, 2),
    ("*comenta qual dos 5 te surpreendeu*", 161, 6), ("e *segue pra mais!*", 167, 4),
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
