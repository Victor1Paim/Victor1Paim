#!/usr/bin/env python3
"""Vídeo 06: "Grão-de-bico: salada de fibra em 10 minutos" (Reel de receita, estrutura Evolução)."""
import json, re, shutil, sys
from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance

NOME = "grao-de-bico"
SCR = Path("/tmp/claude-0/-home-user-Victor1Paim/bc508778-dc0e-5c3d-a4a6-a9dce8035bd2/scratchpad")
ROOT = Path("/home/user/Victor1Paim/saude-sem-sermao/producoes")
POST = ROOT / "06-grao-de-bico"
V = POST / "video"
(V / "compositions").mkdir(parents=True, exist_ok=True)
(V / "assets").mkdir(exist_ok=True)
for f in ["hyperframes.json", "package.json", "meta.json"]:
    (V / f).write_text((SCR / "hfblank" / f).read_text().replace('"hfblank"', '"saude-sem-sermao-06-grao"'))
shutil.copy(POST / "dialogo.mp3", V / "assets/voz.mp3")

# fotos: as do carrossel + as novas do reel -> 1280x1920 e versão desfocada
fontes_fotos = list((POST / "fotos").glob("*.png"))
for p in fontes_fotos:
    dst = V / "assets" / f"{p.stem}.jpg"
    if dst.exists():
        continue
    im = Image.open(p).convert("RGB").resize((1280, 1920), Image.LANCZOS)
    im.save(dst, quality=90)
    ImageEnhance.Brightness(im.filter(ImageFilter.GaussianBlur(28))).enhance(0.62).save(V / "assets" / f"{p.stem}-desfoque.jpg", quality=85)

W, H = 1080, 1920
words = json.loads((POST / "conferencia/dialogo.palavras.json").read_text())
CENAS = []
src = (SCR / "build_sono.py").read_text()
exec(src[src.index("# ---------- paleta e base"):src.index("# ---------- 1. capa")])
src2 = (SCR / "build_alongar.py").read_text()
exec(src2[src2.index("BASE_CSS += "):src2.index("VERDE, CREME, BRANCO")])
src3 = (SCR / "build_reel_ovo.py").read_text()
exec(src3[src3.index('BASE_CSS += """\n  .foto{'):src3.index("# 1. capa")])
BASE_CSS += """
  .card2{position:absolute;left:80px;width:920px;background:#fff;border-radius:30px;box-shadow:0 14px 40px rgba(40,60,40,.12);
         display:flex;align-items:center;gap:26px;padding:30px 38px;font-weight:900;font-size:44px;line-height:1.2;}
  .card2 .e{font-size:76px;}
"""


def capa(ini, fim, foto, titulo, tag, pill, t_pill, cor_tag="#D45F2B"):
    d = add("capa", ini, fim)
    cena("capa", d, f"""
  #capa-tag{{position:absolute;left:80px;top:220px;padding:8px 24px;border-radius:999px;background:{cor_tag};color:#fff;font-weight:900;font-size:34px;letter-spacing:.06em;}}
  #capa-pill{{left:80px;top:640px;background:var(--verde);}}
""", f"""
  {foto_html("capa", foto, '<div class="sombra-top"></div>')}
  <div id="capa-tag">{tag}</div>
  <h1 class="tit-foto" style="top:290px">{titulo}</h1>
  <div class="chip" id="capa-pill">{pill}</div>
""", f"""
  {kb_js("capa", d, 1.0, 1.14, -30)}
  tl.fromTo("#capa-pill",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.2)"}},{t_pill:.2f});
""")


def seq_fotos(cid, ini, fim, fotos, chips, titulo=None, passo=None):
    """fotos: [(nome, t_abs)], troca com crossfade; chips: [(texto, t_abs, cor)] empilhados à esquerda no topo."""
    d = add(cid, ini, fim)
    wh, wj = wipe(cid, "#1c211c")
    camadas, js = [], []
    for k, (nome, tt) in enumerate(fotos):
        camadas.append(f'<div class="foto" id="{cid}-f{k}" style="opacity:{1 if k == 0 else 0}"><img id="{cid}-i{k}" src="assets/{nome}.jpg"></div>')
        a = 0 if k == 0 else max(tt - ini - 0.25, 0)
        if k > 0:
            js.append(f'tl.to("#{cid}-f{k}",{{opacity:1,duration:0.45,ease:"power2.inOut"}},{a:.2f});')
        js.append(f'tl.fromTo("#{cid}-i{k}",{{scale:1.03}},{{scale:1.13,duration:{max(d - a, 0.5):.2f},ease:"none"}},{a:.2f});')
    topo = 250 if not titulo else 420
    chips_html = "".join(f'<div class="chip" id="{cid}-c{i}" style="left:{80 if i % 2 == 0 else 160}px;top:{topo + 90*i}px;background:{c}">{txt}</div>'
                         for i, (txt, _, c) in enumerate(chips))
    js += [f'tl.fromTo("#{cid}-c{i}",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.3,ease:"back.out(1.8)"}},{max(tt - ini, 0.1):.2f});' for i, (_, tt, _) in enumerate(chips)]
    tit = f'<h1 class="tit-foto" id="{cid}-t" style="top:240px;font-size:88px">{titulo}</h1>' if titulo else ""
    if titulo:
        js.append(f'tl.fromTo("#{cid}-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.15);')
    cena(cid, d, "", f"""
  {''.join(camadas)}
  <div class="sombra-top"></div>
  {tit}
  {chips_html}
  {wh}
""", f"""
  {wj}
  {' '.join(js)}
""")


def grafico(cid, ini, fim, bg, html, js, css=""):
    d = add(cid, ini, fim)
    wh, wj = wipe(cid, "#1c211c")
    cena(cid, d, f".bg{{background:{bg};}}\n  .tag{{background:#5F6E52;color:#fff;}}\n{css}", f'<div class="bg"></div>\n{html}\n{wh}', f"{wj}\n{js}")


def cta(ini, fim, titulo, comenta, eco_foto, eco_tit, i_manda, i_aviao, i_curte, i_comenta, i_segue, total):
    d = add("cta", ini, fim)
    wh, wj = wipe("cta", "#1c211c")
    cta_ovo = src3[src3.index('cena("cta", d, """'):src3.index("GRUPOS = [")]
    loc = dict(globals()); loc.update(d=d, ini=ini, TOTAL=total, wh=wh, wj=wj)
    cta_ovo = (cta_ovo.replace(".bg{background:var(--laranja);}", ".bg{background:var(--verde);}\n  #cta-tito{filter:drop-shadow(0 0 2px #FDF3ED) drop-shadow(0 0 2px #FDF3ED);}")
               .replace("t(148)-ini-0.05", f"t({i_segue-1})-ini-0.1").replace("t(148)-ini+0.45", f"t({i_segue})-ini+0.15").replace("TOTAL-ini-2.1", "TOTAL-ini-2.3")
               .replace('Manda pra quem tem <em>medo de ovo</em>', titulo)
               .replace('"🥕 cenoura!"', comenta)
               .replace('assets/capa.jpg', f'assets/{eco_foto}.jpg')
               .replace('Ovo aumenta o <em>colesterol?</em>', eco_tit)
               .replace("t(133)", f"t({i_manda})").replace("t(134)", f"t({i_manda+1})").replace("t(137)", f"t({i_aviao})")
               .replace("t(141)", f"t({i_curte})").replace("t(142)", f"t({i_comenta})").replace("t(148)", f"t({i_segue})"))
    exec(cta_ovo, loc)


def legendas(grupos, total):
    for txt_, i0, n in grupos:
        print(f"{txt_!r:50} <- {' '.join(w['palavra'] for w in words[i0:i0+n])!r}")
    leg_html, leg_js = [], []
    for k, (txt_, i0, n) in enumerate(grupos):
        a = max(words[i0]["inicio"] - 0.08, 0.15)
        b = words[i0 + n - 1]["fim"] + 0.18
        if k + 1 < len(grupos) and grupos[k + 1][1] == i0 + n:
            b = min(b, words[grupos[k + 1][1]]["inicio"] - 0.1)
        leg_html.append(f'<div class="leg" id="leg-{k}">{re.sub(r"[*](.+?)[*]", r"<b>\1</b>", txt_)}</div>')
        leg_js.append(f'tl.fromTo("#leg-{k}",{{opacity:0,y:16,visibility:"visible"}},{{opacity:1,y:0,duration:0.14,ease:"power2.out"}},{a:.2f});'
                      f'tl.to("#leg-{k}",{{opacity:0,duration:0.1,ease:"power2.in"}},{b-0.1:.2f});'
                      f'tl.set("#leg-{k}",{{opacity:0,visibility:"hidden"}},{b:.2f});')
    (V / "compositions/legendas.html").write_text(f"""<template>
<style>
  #root{{position:absolute;inset:0;font-family:'Nunito',sans-serif;pointer-events:none;}}
  .leg{{position:absolute;left:80px;top:1180px;max-width:640px;background:#fff;border-radius:24px;padding:18px 30px;
        font-weight:900;font-size:50px;line-height:1.15;color:#2B2B2B;box-shadow:0 12px 34px rgba(0,0,0,.25);
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
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #1c211c; }}
      #main {{ position: relative; width: 100%; height: 100%; }}
    </style>
  </head>
  <body>
    <div id="main" data-composition-id="main" data-start="0" data-duration="{total}" data-width="{W}" data-height="{H}">
{chr(10).join(hosts)}
      <div id="legendas" data-composition-id="legendas" data-composition-src="compositions/legendas.html"
        data-start="0" data-duration="{total}" data-track-index="2" data-track-kind="captions"
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


VERDE_ = "#2F483A"; SAL = "#5F6E52"; TER = "#C2563A"; MOS = "#8A6A1F"; LAR = "#D45F2B"
TOTAL = 58.3
BASE_CSS += """
  .relogio{position:absolute;left:730px;top:190px;width:270px;padding:12px 0;border-radius:999px;background:rgba(18,22,18,.82);color:#fff;
           text-align:center;font-weight:900;font-size:56px;letter-spacing:.04em;box-shadow:0 10px 30px rgba(0,0,0,.3);font-variant-numeric:tabular-nums;}
  .minuto{position:absolute;left:80px;top:190px;padding:10px 26px;border-radius:999px;background:var(--laranja);color:#fff;font-weight:900;font-size:40px;letter-spacing:.06em;}
"""

def relogio(cid, de, ate, t_rel, dur=0.9):
    html = f'<div class="relogio" id="{cid}-rel">⏱ {de:02d}:00</div>'
    js = (f'(function(){{const o={{v:{de*60}}};const el=document.querySelector("#{cid}-rel");'
          f'tl.fromTo(o,{{v:{de*60}}},{{v:{ate*60},duration:{dur},ease:"power1.inOut",onUpdate:()=>{{const s=Math.round(o.v);'
          f'el.textContent="⏱ "+String(Math.floor(s/60)).padStart(2,"0")+":"+String(s%60).padStart(2,"0");}}}},{max(t_rel,0.05):.2f});}})();'
          f'tl.fromTo("#{cid}-rel",{{scale:1}},{{scale:1.12,duration:0.15,yoyo:true,repeat:1}},{max(t_rel,0.05)+dur:.2f});')
    return html, js

def passo(cid, ini, fim, foto, minuto, de, ate, t_min, chips, extra_html="", extra_js=""):
    d = add(cid, ini, fim)
    wh, wj = wipe(cid, "#1c211c")
    rh, rj = relogio(cid, de, ate, t_min - ini)
    chips_html = "".join(f'<div class="chip" id="{cid}-c{i}" style="left:80px;top:{300 + 96*i}px;background:{c}">{txt}</div>' for i, (txt, _, c) in enumerate(chips))
    cjs = " ".join(f'tl.fromTo("#{cid}-c{i}",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:0.3,ease:"back.out(1.8)"}},{max(tt - ini, 0.1):.2f});' for i, (_, tt, _) in enumerate(chips))
    cena(cid, d, "", f"""
  {foto_html(cid, foto, '<div class="sombra-top"></div>')}
  <div class="minuto" id="{cid}-m">MINUTO {minuto}</div>
  {rh}
  {chips_html}
  {extra_html}
  {wh}
""", f"""
  {wj}
  {kb_js(cid, d, 1.02, 1.12, -20)}
  tl.fromTo("#{cid}-m",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.3,ease:"back.out(2.2)"}},{max(t_min - ini - 0.1, 0.1):.2f});
  {rj}
  {cjs}
  {extra_js}
""")

# 1. capa (0 – 4.4)
d = add("capa", 0, 4.4)
rh, rj = relogio("capa", 0, 0, 99)
cena("capa", d, """
  #capa-tag{position:absolute;left:80px;top:300px;padding:8px 24px;border-radius:999px;background:#2F483A;color:#fff;font-weight:900;font-size:34px;letter-spacing:.06em;}
  #capa-q{left:80px;top:700px;background:var(--laranja);}
""", f"""
  {foto_html("capa", "lata", '<div class="sombra-top" style="height:1100px"></div>')}
  {rh}
  <div id="capa-tag">RECEITA SEM MORAL</div>
  <h1 class="tit-foto" style="top:370px">Lata vira almoço em <em>10 minutos?</em></h1>
  <div class="chip" id="capa-q">vira almoço de verdade?</div>
""", f"""
  {kb_js("capa", d, 1.0, 1.12, -20)}
  tl.fromTo("#capa-q",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.2)"}},{t(9)-0.05:.2f});
  tl.fromTo("#capa-rel",{{opacity:0.4}},{{opacity:1,duration:0.4,yoyo:true,repeat:4}},0.2);
""")

# 2. Tito: fome de novo (4.4 – 7.65)
tito_foto("t1", 4.4, 7.65, "Salada? Daqui a uma hora eu tô com fome de novo.", 4.66, 7.4, "lata", destaque=(0, 8, 9, 10), olhos="duvida", tam=62)

# 3. minuto 1 (7.65 – 10.65)
passo("p1", 7.65, 10.65, "escorredor", 1, 0, 1, t(24), [("💧 escorre e lava", t(26), SAL)])

# 4. minuto 3 (10.65 – 14.15)
passo("p3", 10.65, 14.15, "tabua", 3, 1, 3, t(31), [("🍅 tomate", t(33), TER), ("🥒 pepino", t(34), SAL), ("🧅 cebola", t(36), MOS)])

# 5. Tito: sem graça? (14.15 – 16.25)
tito_foto("t2", 14.15, 16.25, "E o tempero, vai ser sem graça?", 14.26, 16.1, "tabua", destaque=(5, 6), olhos="duvida", tam=66)

# 6. minuto 6 (16.25 – 21.35)
passo("p6", 16.25, 21.35, "tempero", 6, 3, 6, t(46), [("🍋 limão", t(48), MOS), ("🫒 azeite", t(49), SAL), ("🧂 sal", t(50), TER), ("🌿 salsinha", t(52), VERDE_)])

# 7. minuto 8 (21.35 – 25.65)
passo("p8", 21.35, 25.65, "ovo", 8, 6, 8, t(55), [("🥚 ovo ou queijo branco", t(57), MOS), ("+ proteína (opcional)", t(65), SAL)])

# 8. minuto 10: pronto (25.65 – 27.7)
d = add("pronto", 25.65, 27.7)
wh, wj = wipe("pronto", "#1c211c")
rh, rj = relogio("pronto", 8, 10, t(67) - 25.65, 0.7)
cena("pronto", d, """
  #pronto-ok{position:absolute;left:240px;top:760px;width:600px;text-align:center;font-family:'Playfair Display',serif;font-weight:800;font-size:150px;color:#fff;text-shadow:0 6px 30px rgba(0,0,0,.5);}
  #pronto-img{filter:blur(10px) brightness(.7);}
""", f"""
  {foto_html("pronto", "prato")}
  <div class="minuto" id="pronto-m">MINUTO 10</div>
  {rh}
  <div id="pronto-ok">Pronto.</div>
  {wh}
""", f"""
  {wj}
  {kb_js("pronto", d, 1.08, 1.12)}
  {rj}
  tl.fromTo("#pronto-ok",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.4)"}},{t(69) - 25.65 - 0.05:.2f});
""")

# 9. VIRADA: o segredo é a fibra (27.7 – 39.0)
ini, fim = 27.7, 39.0
d = add("virada", ini, fim)
wh, wj = wipe("virada", "#1c211c")
cena("virada", d, f"""
  #virada-img{{filter:blur(10px) brightness(.7);}}
  #virada-card{{position:absolute;left:80px;top:470px;width:920px;padding:34px 40px;border-radius:32px;background:#fff;box-shadow:0 20px 50px rgba(0,0,0,.3);}}
  #virada-card .q{{font-weight:900;font-size:32px;letter-spacing:.06em;color:{LAR};}}
  #virada-n{{font-family:'Playfair Display',serif;font-weight:800;font-size:120px;color:#2F483A;line-height:1.05;}}
  #virada-n small{{font-size:52px;color:#8a837d;}}
  #virada-barra{{position:relative;height:40px;border-radius:20px;background:#EEF0EA;margin:16px 0 10px;overflow:hidden;}}
  #virada-fill{{position:absolute;left:0;top:0;bottom:0;width:100%;border-radius:20px;background:linear-gradient(90deg,#95A185,#2F483A);transform-origin:0 50%;}}
  #virada-meta{{font-weight:900;font-size:40px;}}
  #virada-sac{{left:80px;top:930px;background:{VERDE_};}}
  #virada-f{{position:absolute;left:80px;top:1040px;width:920px;padding:12px 22px;border-radius:18px;background:rgba(18,22,18,.78);font-weight:800;font-size:28px;color:#fff;}}
""", f"""
  {foto_html("virada", "prato", '<div class="sombra-top"></div>')}
  <h1 class="tit-foto" id="virada-t" style="top:220px;font-size:96px">O segredo: <em>fibra</em></h1>
  <div id="virada-card"><div class="q">FIBRA NESTE PRATO (MEIA LATA)</div>
    <div id="virada-n">~<span id="virada-g">0</span> g <small>de 25 g por dia</small></div>
    <div id="virada-barra"><div id="virada-fill"></div></div>
    <div id="virada-meta">≈ <span style="color:{LAR}">metade</span> do que a OMS recomenda</div></div>
  <div class="chip" id="virada-sac">fibra + proteína = fome demora a voltar</div>
  <div id="virada-f">Fontes: OMS, diretriz de carboidratos (2023) · USDA/TACO (fibra do grão; estimativa por porção)</div>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#virada-img",{{scale:1.12,filter:"blur(10px) brightness(.7)"}},{{scale:1.0,filter:"blur(0px) brightness(.85)",duration:1.0,ease:"power2.out"}},0);
  tl.fromTo("#virada-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(72)-ini:.2f});
  tl.fromTo("#virada-card",{{opacity:0,y:60,scale:0.95}},{{opacity:1,y:0,scale:1,duration:0.45,ease:"back.out(1.5)"}},{t(75)-ini:.2f});
  {contador("#virada-g", 0, 10, t(78)-ini, 1.0)}
  tl.fromTo("#virada-fill",{{scaleX:0}},{{scaleX:0.42,duration:1.2,ease:"power2.out"}},{t(79)-ini:.2f});
  tl.fromTo("#virada-meta",{{opacity:0}},{{opacity:1,duration:0.3}},{t(84)-ini:.2f});
  tl.fromTo("#virada-f",{{opacity:0}},{{opacity:1,duration:0.3}},{t(75)-ini:.2f});
  tl.fromTo("#virada-sac",{{opacity:0,scale:0.6}},{{opacity:1,scale:1,duration:0.35,ease:"back.out(2.2)"}},{t(95)-ini:.2f});
""")

# 10. resumo do Tito (39.0 – 45.85)
tito_foto("resumo", 39.0, 45.85, "Entendi! Uma lata, dez minutos e quase metade da fibra do dia. Assim a fome demora pra voltar.", 39.14, 45.6, "prato",
          rot="💡 O QUE O TITO ENTENDEU", destaque=(6, 7, 8, 9, 10, 11), bracos="acena", tam=52)

# 11. resposta + eco do gancho (45.85 – 49.0)
ini, fim = 45.85, 49.0
d = add("resposta", ini, fim)
wh, wj = wipe("resposta", "#1c211c")
cena("resposta", d, """
  .metade{position:absolute;top:0;bottom:0;width:540px;overflow:hidden;}
  .metade img{position:absolute;top:0;height:1920px;width:1280px;object-fit:cover;}
  .rot2{position:absolute;top:1020px;padding:10px 26px;border-radius:999px;background:rgba(18,22,18,.85);color:#fff;font-weight:900;font-size:44px;}
  #resposta-sim{position:absolute;left:80px;top:300px;width:920px;font-family:'Playfair Display',serif;font-weight:800;font-size:100px;line-height:1.02;color:#fff;text-shadow:0 4px 24px rgba(0,0,0,.5);}
  #resposta-sim em{font-style:italic;color:#F2C46A;}
  #resposta-seta{position:absolute;left:470px;top:880px;width:140px;height:140px;border-radius:50%;background:#D45F2B;color:#fff;font-size:80px;font-weight:900;display:flex;align-items:center;justify-content:center;}
""", f"""
  <div class="metade" style="left:0"><img id="resposta-a" src="assets/lata.jpg" style="left:-420px"></div>
  <div class="metade" style="left:540px"><img id="resposta-b" src="assets/prato.jpg" style="left:-370px"></div>
  <div class="sombra-top"></div>
  <div class="rot2" style="left:80px">⏱ 00:00</div><div class="rot2" style="left:640px">⏱ 10:00</div>
  <div id="resposta-seta">→</div>
  <h1 id="resposta-sim">Vira almoço de verdade? <em>Sim.</em></h1>
  {wh}
""", f"""
  {wj}
  tl.fromTo("#resposta-a",{{x:-200}},{{x:0,duration:0.5,ease:"power3.out"}},0.05);
  tl.fromTo("#resposta-b",{{x:200}},{{x:0,duration:0.5,ease:"power3.out"}},0.05);
  tl.fromTo("#resposta-seta",{{scale:0}},{{scale:1,duration:0.3,ease:"back.out(2.4)"}},0.5);
  tl.fromTo("#resposta-sim",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{t(129)-ini:.2f});
  tl.fromTo("#resposta-sim em",{{scale:1}},{{scale:1.15,duration:0.18,yoyo:true,repeat:1}},{t(133)-ini:.2f});
""")

# 12. CTA (49.0 – fim)
cta(49.0, TOTAL, '<span style="font-size:84px">Manda pra quem diz que <em>salada não sustenta</em></span>', "🫘 GRÃO", "lata", "Lata vira almoço em <em>10 minutos?</em>",
    136, 141, 145, 146, 153, TOTAL)

legendas([
    ("Uma lata de *grão-de-bico* e *10 minutos*.", 0, 9), ("*Vira almoço* de verdade?", 9, 4),
    ("*Minuto 1*: escorre e lava o grão.", 24, 7), ("*Minuto 3*: tomate, pepino", 31, 4), ("e cebola em cubinhos.", 35, 4),
    ("*Minuto 6*: limão, azeite,", 46, 4), ("sal e salsinha. *Mexe bem.*", 50, 5),
    ("*Minuto 8*: um ovo cozido", 55, 5), ("ou *queijo branco*,", 60, 3), ("se quiser *mais proteína*.", 63, 4),
    ("*Minuto 10.* Pronto.", 67, 3),
    ("E aqui vem *o segredo*:", 70, 5), ("esse prato tem *uns 10 gramas de fibra*.", 75, 8),
    ("É *perto de metade*", 83, 4), ("do que a OMS recomenda pro dia inteiro.", 87, 8),
    ("*Fibra e proteína* do grão:", 95, 5), ("é isso que *segura a fome*.", 100, 6),
    ("Uma lata e 10 minutos:", 124, 5), ("vira almoço de verdade, *sim*.", 129, 5),
    ("*Isso aí.*", 134, 2), ("Manda pra quem diz que *salada não sustenta*.", 136, 8), ("E *curte*,", 144, 2),
    ("*comenta GRÃO* se você vai fazer", 146, 6), ("e *segue pra mais!*", 152, 4),
], TOTAL)
