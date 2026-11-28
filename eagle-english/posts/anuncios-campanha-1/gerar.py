#!/usr/bin/env python3
"""Criativos da 1ª campanha (Meta Ads, feed 4:5 = 1080x1350), formatos das referências do usuário (28/11):
  1) notas.png   — print do app Notas (checklist) + foto do material na mesa
  2) lousa.png   — lousa branca: bonequinho empurrando a pedra (cursinho) × de bicicleta (frase pronta) + "Faça o teste"
  3) quadro.png  — quadro-negro educativo: "Por que o inglês não sai na hora?" (iceberg) + "Faça o teste"
Texto sempre nosso (HTML, fonte de mão); a IA só fez os desenhos/fotos SEM texto (img/pedra, bike, mesa, lousa).
Uso (em eagle-english/): CHROMIUM_PATH=/opt/pw-browsers/chromium python3 posts/anuncios-campanha-1/gerar.py
"""
import base64, os
from pathlib import Path
from playwright.sync_api import sync_playwright

P = Path(__file__).resolve().parent
I = P / "img"
(P / "criativos").mkdir(exist_ok=True)
d = lambda n: "data:image/png;base64," + base64.b64encode((I / n).read_bytes()).decode()
FONTES = ('<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Kalam:wght@400;700'
          '&family=Patrick+Hand&family=Caveat:wght@600;700&display=swap" rel="stylesheet">')
BASE = "*{margin:0;padding:0;box-sizing:border-box}html,body{width:1080px;height:1350px;overflow:hidden}"

# ---------- 1) NOTAS ----------
itens = ["parar de decorar regra", "frase pronta do dia a dia", "pronúncia escrita do jeito que se lê",
         "aula curtinha: 15 min por dia", "áudio pra repetir em voz alta", "sem mensalidade (dá pra parcelar)",
         "fazer o teste de 1 minuto 👇"]
notas = f"""<html><head>{FONTES}<style>{BASE}
body{{background:#f2f2f2;font-family:-apple-system,'Inter',sans-serif;display:flex;align-items:center;justify-content:center}}
.tel{{width:960px;height:1250px;background:#fff;border-radius:46px;box-shadow:0 20px 60px rgba(0,0,0,.12);padding:34px 54px;position:relative}}
.status{{display:flex;justify-content:space-between;font-weight:600;font-size:30px;color:#111}}
.bar{{display:flex;justify-content:space-between;align-items:center;margin-top:34px;color:#e0a800;font-size:36px}}
.bar .ic{{display:flex;gap:30px;font-size:34px}} .bar .ic span{{width:50px;height:50px;border:3px solid #e0a800;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:700}}
.data{{text-align:center;color:#9a9a9a;font-size:24px;margin:22px 0 22px}}
h1{{font-size:34px;font-weight:700;color:#111;margin-bottom:14px}}
.it{{display:flex;align-items:center;gap:22px;font-size:31px;color:#222;padding:9px 0}}
.it i{{width:38px;height:38px;border:3px solid #c7c7c7;border-radius:50%;flex:none}}
.foto{{margin-top:26px;height:470px;border-radius:18px;overflow:hidden;position:relative;background:url('{d("mesa.png")}') center/cover}}
.foto img{{position:absolute;box-shadow:0 14px 30px rgba(0,0,0,.35);border-radius:6px}}
</style></head><body><div class=tel>
<div class=status><span>11:43</span><span>●●● 📶 🔋</span></div>
<div class=bar><span>‹ Notas</span><div class=ic><span>↶</span><span>↷</span><span>⇪</span><span>⋯</span></div></div>
<div class=data>28 de novembro de 2026 às 11:43</div>
<h1>o que eu precisava pra finalmente falar inglês:</h1>
{''.join(f'<div class=it><i></i>{t}</div>' for t in itens)}
<div class=foto>
 <img src="{d('capa-ebook.png')}" style="left:150px;top:60px;width:250px;transform:rotate(-8deg)">
 <img src="{d('capa-guia.png')}" style="left:360px;top:40px;width:250px;transform:rotate(4deg)">
 <img src="{d('capa-cards.png')}" style="left:560px;top:80px;width:240px;transform:rotate(10deg)">
</div></div></body></html>"""

# ---------- 2) LOUSA BRANCA ----------
lousa = f"""<html><head>{FONTES}<style>{BASE}
body{{background:#f4f1ea;display:flex;align-items:center;justify-content:center;font-family:'Kalam',cursive}}
.qb{{width:980px;height:1250px;background:#fff;border:16px solid #b9bcc2;border-radius:14px;box-shadow:0 18px 40px rgba(0,0,0,.18),inset 0 0 40px rgba(0,0,0,.04);position:relative}}
.meia{{position:absolute;left:0;right:0;height:540px}} .meia img{{position:absolute;left:-10px;width:540px;mix-blend-mode:multiply}}
.t{{position:absolute;right:40px;width:470px;text-align:center}}
.t b{{display:block;font-weight:700;font-size:92px;line-height:1;color:#1d2f9e}}
.t span{{display:block;font-size:54px;line-height:1.08;margin-top:16px}}
.linha{{position:absolute;left:30px;right:30px;top:560px;border-top:5px solid #1d2f9e;transform:rotate(-.6deg)}}
.bt{{position:absolute;left:50%;transform:translateX(-50%);bottom:60px;border:5px solid #1d2f9e;border-radius:60px;padding:6px 44px 10px;font-size:64px;color:#1d2f9e;font-weight:700;white-space:nowrap}}
.marca{{position:absolute;right:30px;bottom:14px;font-family:Inter;font-size:20px;color:#9aa0aa}}
</style></head><body><div class=qb>
<div class=meia style="top:20px"><img src="{d('pedra.png')}" style="top:20px">
 <div class=t style="top:70px"><b>Cursinho<br>3 anos</b><span style="color:#c4161c">Na hora de falar,<br>a frase não saiu</span></div></div>
<div class=linha></div>
<div class=meia style="top:575px"><img src="{d('bike.png')}" style="top:10px">
 <div class=t style="top:40px"><b>Frase<br>pronta</b><span style="color:#11804a">15 min por dia,<br>em voz alta,<br>sem decoreba</span></div></div>
<div class=bt>Faça o teste 👇</div>
<div class=marca>Eagle Primeira Classe</div>
</div></body></html>"""

# ---------- 3) QUADRO-NEGRO ----------
giz = "fill:none;stroke:#f4f1e6;stroke-width:5;stroke-linecap:round;stroke-linejoin:round;filter:url(#giz)"
quadro = f"""<html><head>{FONTES}<style>{BASE}
body{{background:url('{d("lousa.png")}') center/100% 100%;font-family:'Patrick Hand',cursive;color:#f4f1e6;position:relative}}
.giz{{text-shadow:0 0 2px rgba(255,255,255,.35)}}
h1{{position:absolute;top:120px;left:110px;right:110px;text-align:center;font-weight:400;font-size:76px;line-height:1.05;letter-spacing:1px}}
.sub{{position:absolute;top:70px;left:0;right:0;text-align:center;font-size:32px;color:#d8d3c2}}
svg{{position:absolute;left:100px;top:330px}}
.r{{position:absolute;font-size:34px;line-height:1.15}}
.lista{{position:absolute;left:600px;top:360px;width:380px;font-size:37px;line-height:1.2}}
.lista p{{margin-bottom:14px}}
.fim{{position:absolute;left:110px;bottom:150px;font-size:52px}}
.box{{position:absolute;right:110px;bottom:130px;border:4px solid #f4f1e6;padding:8px 26px;font-size:48px;letter-spacing:1px}}
.am{{color:#ffe27a}}
</style></head><body class=giz>
<div class=sub>Eagle Primeira Classe explica</div>
<h1>POR QUE O INGLÊS<br>NÃO SAI NA HORA?</h1>
<svg width="480" height="560" viewBox="0 0 480 560"><defs><filter id="giz"><feTurbulence baseFrequency="0.9" numOctaves="2" result="n"/>
<feDisplacementMap in="SourceGraphic" in2="n" scale="3"/></filter></defs>
<path d="M10 190 Q 120 175 240 192 T 470 190" style="{giz};stroke-dasharray:14 10"/>
<path d="M150 190 L205 95 L232 120 L262 70 L320 190" style="{giz}"/>
<path d="M150 190 L95 300 L120 410 L200 520 L300 500 L380 400 L360 280 L320 190" style="{giz};stroke-dasharray:22 9"/>
<path d="M160 250 L330 250 M140 320 L350 320 M150 390 L345 390 M190 455 L300 455" style="{giz};stroke-width:3;opacity:.55"/>
</svg>
<div class=r style="left:560px;top:420px;width:420px">← <span class=am>regra decorada</span><br>é aqui que o cursinho para</div>
<div class=r style="left:560px;top:640px;width:420px">← <span class=am>frase pronta, pronúncia<br>e treino em voz alta</span><br>é o que a conversa precisa</div>
<div class=lista style="left:110px;top:930px;width:860px">
<p>– não é falta de esforço: regra decorada não vira fala</p><p>– a frase certa precisa estar pronta e treinada em voz alta</p><p>– 15 minutos por dia já fazem diferença</p>
</div>
<div class=fim>Essa trava <span class=am>pode se soltar.</span></div>
<div class=box>FAÇA O TESTE →</div>
</body></html>"""

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH") or None)
    for nome, html in (("notas", notas), ("lousa", lousa), ("quadro", quadro)):
        pg = nav.new_page(viewport={"width": 1080, "height": 1350})
        pg.set_content(html); pg.wait_for_timeout(2000)
        pg.screenshot(path=str(P / "criativos" / f"{nome}.png")); pg.close()
    nav.close()
print("ok")
