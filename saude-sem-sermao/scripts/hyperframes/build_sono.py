#!/usr/bin/env python3
"""Gera o projeto HyperFrames do vídeo "Precisa dormir 8 horas?" (Saúde sem Sermão)."""
import json, re
from pathlib import Path

V = Path("/home/user/Victor1Paim/saude-sem-sermao/producoes/sono-8-horas/video")
(V / "compositions").mkdir(parents=True, exist_ok=True)
W, H = 1080, 1920
TOTAL = 37.5

sed = "sed"
for p, s in [("package.json", '"hfblank"'), ("meta.json", '"hfblank"')]:
    f = V / p
    f.write_text(f.read_text().replace(s, '"saude-sem-sermao-sono-8-horas"'))

words = json.loads((V.parent / "conferencia/dialogo-a.palavras.json").read_text())

# ---------- paleta e base ----------
BASE_CSS = """
  :root{--verde:#2F483A;--laranja:#D45F2B;--terracota:#CE6840;--creme:#FDF3ED;--creme2:#F2ECE2;
        --pessego:#F7E5DD;--salvia:#95A185;--cinza:#8C8580;--tinta:#2B2B2B;--mostarda:#E2B04A;}
  #root{position:absolute;inset:0;overflow:hidden;font-family:'Nunito',sans-serif;color:var(--tinta);}
  .bg{position:absolute;inset:0;}
  .titulo{position:absolute;left:80px;top:230px;width:920px;font-family:'Playfair Display',serif;
          font-weight:700;font-size:96px;line-height:1.04;letter-spacing:-0.01em;}
  .titulo em{font-style:italic;color:var(--laranja);}
  .tag{position:absolute;left:80px;top:180px;display:inline-flex;gap:8px;align-items:center;padding:6px 18px;
       border-radius:999px;font-weight:900;font-size:28px;letter-spacing:.06em;}
  .fonte{position:absolute;left:80px;font-size:28px;color:#8a837d;font-weight:700;}
  .tito-mini{position:absolute;right:40px;top:1330px;width:300px;height:330px;}
  .tito-grande{position:absolute;left:190px;top:640px;width:700px;height:770px;}
  .balao{position:absolute;left:80px;top:230px;width:920px;background:#fff;border-radius:36px;
         box-shadow:0 18px 50px rgba(120,60,30,.12);padding:40px 48px 48px;}
  .balao .rot{font-weight:900;font-size:28px;letter-spacing:.12em;color:var(--laranja);margin-bottom:18px;}
  .balao .txt{font-weight:800;font-size:60px;line-height:1.18;}
  .balao .rabo{position:absolute;left:420px;bottom:-26px;width:52px;height:52px;background:#fff;
               transform:rotate(45deg);border-radius:6px;}
  .w{display:inline-block;opacity:0;}
"""

FONT_HEAD = ""  # Playfair Display e Nunito estão no pacote do HyperFrames


def tito_svg(pref, olhos="normal", bracos="baixo"):
    """Tito em vetor plano: coração terracota com estetoscópio verde-escuro."""
    if olhos == "piscando":
        olho_esq = f'<ellipse cx="76" cy="92" rx="8" ry="11" fill="#2B2B2B"/><circle cx="79" cy="88" r="3" fill="#fff"/>'
        olho_dir = '<path d="M112 94 q12 -10 24 0" stroke="#2B2B2B" stroke-width="5" fill="none" stroke-linecap="round"/>'
    else:
        olho_esq = '<ellipse cx="78" cy="92" rx="8" ry="11" fill="#2B2B2B"/><circle cx="81" cy="88" r="3" fill="#fff"/>'
        olho_dir = '<ellipse cx="122" cy="92" rx="8" ry="11" fill="#2B2B2B"/><circle cx="125" cy="88" r="3" fill="#fff"/>'
    if olhos == "duvida":
        sobr = ('<path d="M64 72 q14 -6 26 2" stroke="#2B2B2B" stroke-width="5" fill="none" stroke-linecap="round"/>'
                '<path d="M110 66 q14 -12 28 -2" stroke="#2B2B2B" stroke-width="5" fill="none" stroke-linecap="round"/>')
    else:
        sobr = ('<path d="M64 72 q14 -10 28 -2" stroke="#2B2B2B" stroke-width="5" fill="none" stroke-linecap="round"/>'
                '<path d="M108 70 q14 -8 28 2" stroke="#2B2B2B" stroke-width="5" fill="none" stroke-linecap="round"/>')
    braco_dir = ('<g id="%s-braco"><path d="M168 102 q26 -8 30 -38" stroke="#C75A34" stroke-width="15" fill="none" stroke-linecap="round"/>'
                 '<circle cx="198" cy="60" r="11" fill="#C75A34"/></g>' % pref) if bracos == "acena" else \
                ('<g id="%s-braco"><path d="M168 104 q22 10 22 34" stroke="#C75A34" stroke-width="15" fill="none" stroke-linecap="round"/>'
                 '<circle cx="190" cy="142" r="11" fill="#C75A34"/></g>' % pref)
    return f'''<svg viewBox="-10 0 220 240" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="100" cy="226" rx="62" ry="8" fill="rgba(90,50,30,.12)"/>
  <rect x="74" y="166" width="17" height="48" rx="8" fill="#C75A34"/><rect x="109" y="166" width="17" height="48" rx="8" fill="#C75A34"/>
  <ellipse cx="80" cy="216" rx="19" ry="9" fill="#C75A34"/><ellipse cx="120" cy="216" rx="19" ry="9" fill="#C75A34"/>
  <path d="M32 104 q-22 10 -22 34" stroke="#C75A34" stroke-width="15" fill="none" stroke-linecap="round"/><circle cx="10" cy="142" r="11" fill="#C75A34"/>
  {braco_dir}
  <path d="M100 188 C 40 142, 10 106, 18 66 C 25 30, 70 22, 100 56 C 130 22, 175 30, 182 66 C 190 106, 160 142, 100 188 Z" fill="#CE6840"/>
  <ellipse cx="56" cy="58" rx="17" ry="10" fill="#E08A63" opacity=".75" transform="rotate(-25 56 58)"/>
  {sobr}{olho_esq}{olho_dir}
  <ellipse cx="60" cy="112" rx="10" ry="6" fill="#EE8F78" opacity=".75"/><ellipse cx="140" cy="112" rx="10" ry="6" fill="#EE8F78" opacity=".75"/>
  <path id="{pref}-sorriso" d="M86 116 q14 14 28 0" stroke="#2B2B2B" stroke-width="5" fill="none" stroke-linecap="round"/>
  <ellipse id="{pref}-boca" cx="100" cy="121" rx="10" ry="8" fill="#5A1E14" opacity="0"/>
  <path d="M42 126 q58 42 116 0" stroke="#2F483A" stroke-width="8" fill="none" stroke-linecap="round"/>
  <path d="M152 130 q14 26 -4 44" stroke="#2F483A" stroke-width="7" fill="none" stroke-linecap="round"/>
  <circle cx="146" cy="176" r="11" fill="#F2ECE2" stroke="#2F483A" stroke-width="6"/>
</svg>'''


def fala_js(pref, inicio, fim):
    """Boca abre e fecha enquanto o Tito fala (sílabas a ~7 por segundo)."""
    return f"""
  (function(){{
    const a={inicio}, b={fim};
    tl.set("#{pref}-sorriso",{{opacity:0}},a); tl.set("#{pref}-boca",{{opacity:1}},a);
    for(let t=a;t<b-0.08;t+=0.14){{ tl.fromTo("#{pref}-boca",{{scaleY:0.35,transformOrigin:"50% 50%"}},{{scaleY:1,duration:0.07,ease:"sine.out"}},t);
      tl.to("#{pref}-boca",{{scaleY:0.35,duration:0.07,ease:"sine.in"}},t+0.07); }}
    tl.set("#{pref}-boca",{{opacity:0}},b); tl.set("#{pref}-sorriso",{{opacity:1}},b);
  }})();"""


def palavras_html(pref, texto, t0, destaque=()):
    """Separa o texto em <span class=w> com ids; destaque = índices em laranja."""
    out = []
    for i, w in enumerate(texto.split()):
        cor = ' style="color:var(--laranja)"' if i in destaque else ""
        out.append(f'<span class="w" id="{pref}-w{i}"{cor}>{w}</span>')
    return " ".join(out)


def tempos_palavras(ini_abs, fim_abs):
    return [w for w in words if w["inicio"] >= ini_abs - 0.05 and w["fim"] <= fim_abs + 0.05]


def palavras_js(pref, texto, t_cena, ini_abs, fim_abs):
    ws = tempos_palavras(ini_abs, fim_abs)
    n = len(texto.split())
    js = []
    for i in range(n):
        t = (ws[i]["inicio"] if i < len(ws) else ws[-1]["fim"]) - t_cena
        js.append(f'tl.fromTo("#{pref}-w{i}",{{opacity:0,y:14}},{{opacity:1,y:0,duration:0.16,ease:"power2.out"}},{max(t,0.05):.2f});')
    return "\n  ".join(js)


def cena(cid, dur, css, html, js):
    (V / "compositions" / f"{cid}.html").write_text(f"""<template>
<style>{BASE_CSS}{css}</style>
<div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}">
{html}
</div>
<script>
  const tl = gsap.timeline({{ paused: true }});
  {js}
  window.__timelines["{cid}"] = tl;
</script>
</template>
""")


CENAS = []


def add(cid, ini, fim):
    CENAS.append((cid, ini, fim))
    return fim - ini


# ---------- 1. capa ----------
d = add("capa", 0, 3.0)
cena("capa", d, """
  .bg{background:var(--verde);}
  .titulo{color:var(--creme2);top:250px;}
  .titulo em{color:var(--mostarda);}
  #capa-lua{position:absolute;left:300px;top:600px;width:420px;height:420px;}
  #capa-selo{position:absolute;left:650px;top:560px;width:190px;height:190px;border-radius:50%;background:var(--laranja);
     color:#fff;font-family:'Playfair Display',serif;font-style:italic;font-weight:700;font-size:78px;display:flex;align-items:center;justify-content:center;}
  #capa-q{position:absolute;left:830px;top:520px;font-family:'Playfair Display',serif;font-weight:700;font-size:80px;color:var(--mostarda);}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo"><span id="capa-t1" style="display:inline-block">Precisa dormir</span><br><em id="capa-t2" style="display:inline-block">8 horas?</em></h1>
  <svg id="capa-lua" viewBox="0 0 200 200"><path d="M130 20 A80 80 0 1 0 180 140 A64 64 0 1 1 130 20 Z" fill="#F2ECE2"/>
    <circle cx="160" cy="40" r="5" fill="#E2B04A"/><circle cx="40" cy="30" r="4" fill="#E2B04A"/><circle cx="185" cy="90" r="3" fill="#F2ECE2"/></svg>
  <div id="capa-selo">8h</div><div id="capa-q">?</div>
  <div class="tito-mini" id="capa-tito">{tito_svg("capa", olhos="piscando", bracos="acena")}</div>
""", """
  tl.fromTo("#capa-t2",{scale:1,transformOrigin:"0% 50%"},{scale:1.08,duration:0.25,ease:"power2.out",yoyo:true,repeat:1},1.5);
  tl.fromTo("#capa-lua",{rotation:-6},{rotation:0,duration:1.2,ease:"power2.out"},0.0);
  tl.fromTo("#capa-selo",{scale:0},{scale:1,duration:0.4,ease:"back.out(2.2)"},0.25);
  tl.fromTo("#capa-q",{opacity:0,y:-20},{opacity:1,y:0,duration:0.3,ease:"power2.out"},0.5);
  tl.fromTo("#capa-tito",{opacity:0,y:80},{opacity:1,y:0,duration:0.5,ease:"back.out(1.5)"},0.6);
  tl.fromTo("#capa-braco",{rotation:-12,transformOrigin:"170px 100px"},{rotation:12,duration:0.3,ease:"sine.inOut",yoyo:true,repeat:3},1.1);
""")


def cena_tito(cid, ini, fim, rotulo, icone, texto, fala_ini, fala_fim, destaque=(), olhos="normal", bracos="baixo", tamanho=60):
    d = add(cid, ini, fim)
    cena(cid, d, f"""
  .bg{{background:var(--creme);}}
  .balao .txt{{font-size:{tamanho}px;}}
""", f"""
  <div class="bg"></div>
  <div class="balao" id="{cid}-balao"><div class="rot">{icone} {rotulo}</div>
    <div class="txt">{palavras_html(cid, texto, 0, destaque)}</div><div class="rabo"></div></div>
  <div class="tito-grande" id="{cid}-tito">{tito_svg(cid, olhos=olhos, bracos=bracos)}</div>
""", f"""
  tl.fromTo("#{cid}-balao",{{opacity:0,y:30,scale:0.96}},{{opacity:1,y:0,scale:1,duration:0.35,ease:"back.out(1.6)"}},0.0);
  tl.fromTo("#{cid}-tito",{{opacity:0,y:120}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.4)"}},0.0);
  {palavras_js(cid, texto, ini, fala_ini, fala_fim)}
  {fala_js(cid, round(fala_ini - ini, 2), round(fala_fim - ini, 2))}
""")


# ---------- 2. Tito: culpa ----------
cena_tito("culpa", 3.0, 6.4, "PERGUNTA DO TITO", "💬", "Eu durmo 7 e ainda acordo com culpa.",
          3.04, 5.8, destaque=(2, 6))

# ---------- 3. faixa 7 a 9 ----------
ini, fim = 6.4, 15.6
d = add("faixa", ini, fim)
x = lambda h: 120 + (h - 5) * 140
ticks = "".join(
    f'<div style="position:absolute;left:{x(h)-40}px;top:900px;width:80px;text-align:center;font-weight:900;font-size:40px;color:#6b6460">{h}h</div>'
    f'<div style="position:absolute;left:{x(h)-2}px;top:858px;width:4px;height:26px;background:#2B2B2B;border-radius:2px"></div>'
    for h in range(5, 12))
cena("faixa", d, f"""
  .bg{{background:#fff;}}
  .tag{{background:#5F6E52;color:#fff;}}
  #faixa-reg{{position:absolute;left:100px;top:868px;width:880px;height:8px;background:#2B2B2B;border-radius:4px;}}
  #faixa-banda{{position:absolute;left:{x(7)}px;top:780px;width:{x(9)-x(7)}px;height:90px;background:var(--laranja);border-radius:18px;}}
  #faixa-rotbanda{{position:absolute;left:{x(7)}px;top:700px;width:{x(9)-x(7)}px;text-align:center;}}
  #faixa-rotbanda span{{display:inline-block;background:var(--salvia);color:#fff;font-weight:900;font-size:30px;padding:6px 18px;border-radius:999px;}}
  #faixa-pino8{{position:absolute;left:{x(8)-70}px;top:560px;width:140px;text-align:center;}}
  #faixa-pino8 .b{{display:inline-block;background:#8C8580;color:#fff;font-weight:900;font-size:40px;padding:8px 20px;border-radius:16px;}}
  #faixa-pino8 .l{{width:4px;height:150px;background:#8C8580;margin:0 auto;}}
  #faixa-magico{{position:absolute;left:{x(8)-200}px;top:990px;width:400px;text-align:center;font-weight:900;font-size:40px;color:#8C8580;}}
  #faixa-sete{{position:absolute;left:{x(7)-120}px;top:990px;width:240px;text-align:center;}}
  #faixa-sete span{{display:inline-block;background:var(--verde);color:#fff;font-weight:900;font-size:40px;padding:8px 22px;border-radius:999px;}}
  .fonte{{top:1090px;}}
""", f"""
  <div class="bg"></div>
  <div class="tag" id="faixa-tag">✓ CIÊNCIA</div>
  <h1 class="titulo" id="faixa-t1">8 horas <em>não é mágico</em></h1>
  <h1 class="titulo" id="faixa-t2" style="opacity:0"><em>7 a 9 horas</em> por noite</h1>
  <div id="faixa-reg"></div>{ticks}
  <div id="faixa-banda"></div>
  <div id="faixa-rotbanda"><span>recomendado</span></div>
  <div id="faixa-pino8"><div class="b">8h</div><div class="l"></div></div>
  <div id="faixa-magico">só um ponto da faixa</div>
  <div id="faixa-sete"><span>7h ✓</span></div>
  <div class="fonte" id="faixa-fonte">Fonte: Hirshkowitz et al., Sleep Health, 2015</div>
  <div class="tito-mini" id="faixa-tito">{tito_svg("faixa")}</div>
""", f"""
  tl.fromTo("#faixa-tag",{{opacity:0,y:-10}},{{opacity:1,y:0,duration:0.3}},0.05);
  tl.fromTo("#faixa-t1",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.1);
  tl.fromTo("#faixa-reg",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:0.6,ease:"power2.inOut"}},0.2);
  tl.fromTo("#faixa-pino8",{{opacity:0,y:-60}},{{opacity:1,y:0,duration:0.45,ease:"bounce.out"}},{7.3-ini:.2f});
  tl.fromTo("#faixa-magico",{{opacity:0}},{{opacity:1,duration:0.3}},{8.3-ini:.2f});
  tl.to("#faixa-t1",{{opacity:0,y:-20,duration:0.25}},{9.3-ini:.2f});
  tl.fromTo("#faixa-t2",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{9.45-ini:.2f});
  tl.fromTo("#faixa-banda",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:0.7,ease:"power3.out"}},{10.92-ini:.2f});
  tl.fromTo("#faixa-rotbanda",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3}},{11.5-ini:.2f});
  tl.to("#faixa-pino8",{{opacity:0.35,duration:0.3}},{11.0-ini:.2f});
  tl.to("#faixa-magico",{{opacity:0,duration:0.25}},{12.6-ini:.2f});
  tl.fromTo("#faixa-sete",{{opacity:0,scale:0.5}},{{opacity:1,scale:1,duration:0.4,ease:"back.out(2)"}},{13.52-ini:.2f});
  tl.fromTo("#faixa-fonte",{{opacity:0}},{{opacity:1,duration:0.4}},{11.2-ini:.2f});
  tl.fromTo("#faixa-tito",{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.5)"}},0.3);
""")

# ---------- 4. Tito: cansado ----------
cena_tito("cansado", 15.6, 18.0, "PERGUNTA DO TITO", "💬", "Ué, então por que eu acordo cansado?",
          15.78, 17.86, destaque=(6,), olhos="duvida")

# ---------- 5. horário regular ----------
ini, fim = 18.0, 25.3
d = add("horario", ini, fim)
X0, PX = 230, 78  # 22h no x=230; 78 px por hora
dias = ["S", "T", "Q", "Q", "S", "S", "D"]
bagunca = [(1.0, 8.0), (2.5, 6.5), (0.5, 7.5), (3.0, 7.0), (1.5, 9.0), (3.5, 9.5), (2.5, 10.0)]
certo = (1.0, 9.0)
linhas = []
for i, (dia, (a, b)) in enumerate(zip(dias, bagunca)):
    y = 500 + i * 76
    fds = i >= 5
    linhas.append(f'<div style="position:absolute;left:110px;top:{y}px;width:60px;text-align:center;font-weight:900;font-size:40px;color:{"var(--laranja)" if fds else "#6b6460"}">{dia}</div>')
    linhas.append(f'<div class="barra" id="horario-b{i}" style="top:{y+8}px"></div>')
eixo = "".join(f'<div style="position:absolute;left:{X0 + k*2*PX - 40}px;top:1040px;width:80px;text-align:center;font-weight:800;font-size:32px;color:#8a837d">{(22 + k*2) % 24}h</div>' for k in range(6))
mover = []
for i, (a, b) in enumerate(bagunca):
    mover.append(f'tl.fromTo("#horario-b{i}",{{x:{a*PX:.0f},scaleX:{(b-a)/8:.3f}}},{{x:{a*PX:.0f},scaleX:{(b-a)/8:.3f},duration:0.01}},0.0);')
    mover.append(f'tl.fromTo("#horario-b{i}",{{opacity:0}},{{opacity:1,duration:0.25}},{0.25 + i*0.08:.2f});')
    mover.append(f'tl.to("#horario-b{i}",{{x:{certo[0]*PX:.0f},scaleX:1,backgroundColor:"#D45F2B",duration:0.7,ease:"power3.inOut"}},{20.3-ini + i*0.06:.2f});')
cena("horario", d, f"""
  .bg{{background:var(--pessego);}}
  .barra{{position:absolute;left:{X0}px;width:{8*PX}px;height:48px;border-radius:24px;background:#B9B0A9;transform-origin:0% 50%;}}
  #horario-fds{{position:absolute;left:80px;top:400px;}}
  #horario-fds span{{display:inline-block;background:var(--salvia);color:#fff;font-weight:900;font-size:32px;padding:8px 20px;border-radius:999px;}}
  .fonte{{top:1240px;}}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="horario-t1">Não é só <em>quantidade</em></h1>
  <h1 class="titulo" id="horario-t2" style="opacity:0">Horário <em>regular</em></h1>
  {''.join(linhas)}{eixo}
  <div id="horario-fds"><span>fim de semana também</span></div>
  <div class="fonte" id="horario-fonte" style="top:1110px">Fonte: AASM; National Sleep Foundation</div>
  <div class="tito-mini" id="horario-tito" style="top:1380px">{tito_svg("horario")}</div>
""", f"""
  tl.fromTo("#horario-t1",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.1);
  {' '.join(mover)}
  tl.to("#horario-t1",{{opacity:0,y:-20,duration:0.25}},{20.1-ini:.2f});
  tl.fromTo("#horario-t2",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},{20.25-ini:.2f});
  tl.fromTo("#horario-fds",{{opacity:0,y:10}},{{opacity:1,y:0,duration:0.3,ease:"back.out(2)"}},{22.1-ini:.2f});
  tl.fromTo("#horario-fonte",{{opacity:0}},{{opacity:1,duration:0.4}},{23.2-ini:.2f});
  tl.fromTo("#horario-tito",{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.5)"}},0.4);
""")

# ---------- 6. resumo do Tito ----------
cena_tito("resumo", 25.3, 32.6, "O QUE O TITO ENTENDEU", "💡",
          "Entendi! 8 horas não é regra. De 7 a 9 está ótimo, e horário certinho ajuda mais do que contar minuto.",
          25.44, 32.06, destaque=(1, 6, 7, 8, 13, 14), bracos="acena", tamanho=54)

# ---------- 7. CTA ----------
ini, fim = 32.6, TOTAL
d = add("cta", ini, fim)
confete = []
cores = ["#E2B04A", "#2F483A", "#FDF3ED", "#95A185", "#D45F2B"]
for i in range(14):
    ang = i * 360 / 14
    import math
    dx, dy = math.cos(math.radians(ang)) * (140 + (i % 3) * 40), math.sin(math.radians(ang)) * (90 + (i % 4) * 25)
    confete.append((i, cores[i % 5], dx, dy))
cena("cta", d, """
  .bg{background:var(--laranja);}
  .titulo{color:#fff;}
  .titulo em{color:var(--creme2);}
  #cta-card{position:absolute;left:150px;top:640px;width:780px;background:#fff;border-radius:36px;padding:40px;
            box-shadow:0 24px 60px rgba(80,30,10,.25);}
  #cta-av{position:absolute;left:40px;top:36px;width:110px;height:110px;border-radius:50%;background:var(--salvia);overflow:hidden;}
  #cta-nome{position:absolute;left:175px;top:44px;font-weight:900;font-size:44px;}
  #cta-bio{position:absolute;left:175px;top:102px;font-weight:700;font-size:30px;color:#8a837d;}
  #cta-esp{height:150px;}
  #cta-bt{position:relative;height:96px;border-radius:24px;}
  #cta-bt1,#cta-bt2{position:absolute;inset:0;border-radius:24px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:44px;color:#fff;}
  #cta-bt1{background:var(--laranja);} #cta-bt2{background:var(--verde);opacity:0;}
  #cta-cursor{position:absolute;left:640px;top:880px;width:90px;height:110px;}
  #cta-circ{position:absolute;right:30px;top:1340px;width:320px;height:320px;border-radius:50%;background:var(--salvia);}
  .cf{position:absolute;left:660px;top:880px;width:18px;height:28px;border-radius:4px;opacity:0;}
  #cta-aviso{position:absolute;left:80px;top:1010px;width:920px;text-align:center;font-weight:800;font-size:30px;color:#FDF3ED;}
""", f"""
  <div class="bg"></div>
  <h1 class="titulo" id="cta-t">Curtiu? <em>Segue a gente</em></h1>
  <div id="cta-card"><div id="cta-av">{tito_svg("cta-av")}</div>
    <div id="cta-nome">@saudesemsermao</div><div id="cta-bio">saúde explicada com ciência</div>
    <div id="cta-esp"></div>
    <div id="cta-bt" data-layout-allow-overlap><div id="cta-bt1">Seguir</div><div id="cta-bt2">Seguindo ✓</div></div></div>
  {''.join(f'<div class="cf" id="cta-cf{i}" style="background:{c}"></div>' for i, c, _, _ in confete)}
  <svg id="cta-cursor" viewBox="0 0 60 74"><path d="M6 4 L6 58 L20 46 L30 70 L40 66 L30 42 L48 42 Z" fill="#fff" stroke="#2B2B2B" stroke-width="4" stroke-linejoin="round"/></svg>
  <div id="cta-aviso">Conteúdo educativo, não substitui orientação profissional.</div>
  <div id="cta-circ"></div>
  <div class="tito-mini" id="cta-tito">{tito_svg("cta", olhos="piscando", bracos="acena")}</div>
""", f"""
  tl.fromTo("#cta-t",{{opacity:0,y:30}},{{opacity:1,y:0,duration:0.4,ease:"power3.out"}},0.05);
  tl.fromTo("#cta-card",{{opacity:0,y:60,scale:0.95}},{{opacity:1,y:0,scale:1,duration:0.5,ease:"back.out(1.5)"}},0.3);
  tl.fromTo("#cta-cursor",{{opacity:0,x:200,y:200}},{{opacity:1,x:0,y:0,duration:0.7,ease:"power3.out"}},{34.3-ini:.2f});
  tl.to("#cta-cursor",{{scale:0.85,duration:0.08,yoyo:true,repeat:1,transformOrigin:"10% 10%"}},{35.05-ini:.2f});
  tl.to("#cta-bt1",{{opacity:0,duration:0.15}},{35.12-ini:.2f});
  tl.to("#cta-bt2",{{opacity:1,duration:0.15}},{35.12-ini:.2f});
  {' '.join(f'tl.fromTo("#cta-cf{i}",{{opacity:1,x:0,y:0,rotation:0}},{{immediateRender:false,opacity:0,x:{dx:.0f},y:{dy - 60:.0f},rotation:{(i*47)%360},duration:0.9,ease:"power2.out"}},{35.15-ini:.2f});' for i, _, dx, dy in confete)}
  tl.fromTo("#cta-aviso",{{opacity:0}},{{opacity:1,duration:0.4}},0.8);
  tl.fromTo("#cta-circ",{{scale:0}},{{scale:1,duration:0.4,ease:"back.out(1.6)"}},0.4);
  tl.fromTo("#cta-tito",{{opacity:0,y:60}},{{opacity:1,y:0,duration:0.45,ease:"back.out(1.5)"}},0.5);
  tl.fromTo("#cta-braco",{{rotation:-12,transformOrigin:"170px 100px"}},{{rotation:12,duration:0.3,ease:"sine.inOut",yoyo:true,repeat:5}},1.0);
""")

# ---------- legendas do narrador ----------
GRUPOS = [  # (texto com *destaque*, índice da 1ª palavra no json, nº de palavras)
    ("Precisa mesmo *dormir*", 0, 3), ("*8 horas* por noite?", 3, 4),
    ("*Calma.*", 15, 1), ("8 horas não é *número mágico*.", 16, 6),
    ("A *recomendação* pra adultos", 22, 4), ("é de *7 a 9 horas* por noite.", 26, 8),
    ("Ou seja, *7 horas*", 34, 4), ("já está *dentro da faixa*.", 38, 5),
    ("Porque não é só *quantidade*.", 50, 5), ("Dormir e acordar em *horários parecidos*,", 55, 6),
    ("até no *fim de semana*,", 61, 5), ("ajuda o corpo a *se ajustar*.", 66, 6),
    ("*Resumiu bem.*", 93, 2), ("Curtiu? Então *segue a gente*", 95, 5),
]
# confere o alinhamento com o json (posição, não texto)
for txt, i0, n in GRUPOS:
    a = " ".join(w["palavra"] for w in words[i0:i0 + n])
    print(f"{txt!r:48} <- {a!r}")
leg_html, leg_js = [], []
for k, (txt, i0, n) in enumerate(GRUPOS):
    a = max(words[i0]["inicio"] - 0.08, 0.15)
    b = words[i0 + n - 1]["fim"] + 0.18
    if k + 1 < len(GRUPOS):
        b = min(b, words[GRUPOS[k + 1][1]]["inicio"] - 0.1) if GRUPOS[k + 1][1] == i0 + n else b
    html = re.sub(r"\*(.+?)\*", r'<b>\1</b>', txt)
    leg_html.append(f'<div class="leg" id="leg-{k}">{html}</div>')
    leg_js.append(f'tl.fromTo("#leg-{k}",{{opacity:0,y:16,visibility:"visible"}},{{opacity:1,y:0,duration:0.14,ease:"power2.out"}},{a:.2f});'
                  f'tl.to("#leg-{k}",{{opacity:0,duration:0.1,ease:"power2.in"}},{b-0.1:.2f});'
                  f'tl.set("#leg-{k}",{{opacity:0,visibility:"hidden"}},{b:.2f});')
(V / "compositions/legendas.html").write_text(f"""<template>
<style>
  #root{{position:absolute;inset:0;font-family:'Nunito',sans-serif;pointer-events:none;}}
  .leg{{position:absolute;left:80px;top:1180px;max-width:700px;background:#fff;border-radius:24px;padding:18px 30px;
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

# ---------- index ----------
hosts = []
for i, (cid, a, b) in enumerate(CENAS):
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
      <audio id="voz" class="clip" src="assets/voz.mp3" data-start="0" data-track-index="3" data-volume="1"></audio>
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print("ok", [c[0] for c in CENAS])
