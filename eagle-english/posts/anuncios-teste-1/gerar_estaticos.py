#!/usr/bin/env python3
"""Telas e anúncios ESTÁTICOS do teste #1 (Meta Ads).
Uso (na pasta eagle-english/): CHROMIUM_PATH=/opt/pw-browsers/chromium python3 posts/anuncios-teste-1/gerar_estaticos.py
Gera: img/tela.png (celular com a oferta), img/quiz.png (celular com o quiz), img/fim.png, img/fim_quiz.png (cartões finais 9:16)
e estaticos/*.png (1080x1350, 4:5): quiz_estatico, remk_faq, remk_pra_quem, remk_dentro_01..07 (carrossel).
"""
import base64, os
from pathlib import Path
from playwright.sync_api import sync_playwright

P = Path(__file__).resolve().parent
R = P.parents[1]
(P / "estaticos").mkdir(exist_ok=True)
d = lambda f: "data:image/png;base64," + base64.b64encode(open(f, "rb").read()).decode()
FONTE = '<link rel=stylesheet href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800;900&display=swap">'
BASE = ("*{margin:0;box-sizing:border-box}body{font-family:Poppins;overflow:hidden;color:#fff;"
        "background:radial-gradient(circle at 50% 30%,#1d4fa8,#0b1f4b 70%)} .am{color:#FDDF33}")


def celular(img, top=660):
    return (f"<html><head>{FONTE}<style>{BASE}body{{width:1080px;height:1920px}}"
            f".ph{{position:absolute;left:50%;top:{top}px;transform:translateX(-50%) rotate(-4deg);width:560px;height:1180px;"
            f"border-radius:70px;background:#111;padding:22px;box-shadow:0 40px 90px rgba(0,0,0,.55)}}"
            f".ph img{{width:100%;height:100%;object-fit:cover;object-position:top;border-radius:50px}}</style></head>"
            f"<body><div class=ph><img src='{img}'></div></body></html>")


def cartao_fim(titulo, sub, botao):
    return (f"<html><head>{FONTE}<style>{BASE}body{{width:1080px;height:1920px}}.c{{position:absolute;left:0;right:0;top:470px;text-align:center}}"
            f"img{{width:300px;height:300px}}h1{{font-weight:900;font-size:92px;line-height:1.02;margin-top:30px}}"
            f"p{{font-weight:700;font-size:44px;margin-top:34px}}.bt{{display:inline-block;margin-top:70px;background:#FDDF33;color:#0b1f4b;"
            f"font-weight:900;font-size:58px;padding:22px 60px;border-radius:999px}}</style></head><body><div class=c>"
            f"<img src='{d(R / 'assets/marca/logo_eagle.png')}'><h1>{titulo}</h1><p>{sub}</p><div class=bt>{botao}</div></div></body></html>")


def quadro(corpo, foto=None):
    """Anúncio 4:5 (1080x1350). foto = imagem de fundo (escurecida embaixo)."""
    fundo = (f"background:linear-gradient(180deg,rgba(11,31,75,0) 45%,rgba(11,31,75,.94) 72%),url('{d(foto)}') center 100%/cover;"
             if foto else "")
    return (f"<html><head>{FONTE}<style>{BASE}body{{width:1080px;height:1350px;{fundo}}}"
            f".topo{{position:absolute;top:44px;left:0;right:0;text-align:center;font-weight:800;font-size:30px;opacity:.95}}"
            f".bx{{position:absolute;left:70px;right:70px}} h1{{font-weight:900;font-size:76px;line-height:1.05;letter-spacing:-.02em}}"
            f"h2{{font-weight:800;font-size:46px;line-height:1.15}} p{{font-weight:600;font-size:38px;line-height:1.3;margin-top:18px}}"
            f".bt{{display:inline-block;background:#FDDF33;color:#0b1f4b;font-weight:900;font-size:46px;padding:16px 46px;border-radius:999px}}"
            f".card{{background:rgba(255,255,255,.08);border:3px solid rgba(255,255,255,.18);border-radius:34px;padding:34px 40px;margin-top:26px}}"
            f".num{{font-size:150px;font-weight:900;line-height:1;color:#FDDF33}} .faq b{{color:#FDDF33}}"
            f".faq div{{font-size:40px;font-weight:600;margin-top:30px;line-height:1.25}}</style></head>"
            f"<body><div class=topo>🦅 Eagle English BR</div>{corpo}</body></html>")


DENTRO = [
    ("🎬", "10 aulas gravadas", "pronúncia e fala, com caderno de exercícios e gabarito"),
    ("🗺️", "2.100 frases", "350 mapas visuais em 35 situações do dia a dia"),
    ("📅", "Guia de 21 dias", "treino de 15 minutos por dia"),
    ("🧠", "Cards de gramática + mapas mentais", "do to be ao present perfect, em 1 página"),
    ("🎧", "100 áudios das frases", "ouça, repita na pausa e confira"),
]

with sync_playwright() as pw:
    nav = pw.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH") or None)

    def site(url, nome):
        pg = nav.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=3)
        pg.goto(url, wait_until="networkidle"); pg.wait_for_timeout(1500)
        pg.screenshot(path=str(P / "img" / nome)); pg.close()

    def foto(html, saida, w=1080, h=1920):
        pg = nav.new_page(viewport={"width": w, "height": h}); pg.set_content(html); pg.wait_for_timeout(1500)
        pg.screenshot(path=str(saida)); pg.close()

    site("https://eagle-viagem.vercel.app/oferta", "_site.png")
    site("https://eagle-viagem.vercel.app/", "_quiz.png")
    foto(celular(d(P / "img/_site.png")), P / "img/tela.png")
    foto(celular(d(P / "img/_quiz.png")), P / "img/quiz.png")
    foto(cartao_fim("Eagle<br><span class=am>Primeira Classe</span>", "Pagamento único ou até 3x no cartão", "Toque em Saiba mais 👇"),
         P / "img/fim.png")
    foto(cartao_fim("Teste rápido<br><span class=am>1 minuto</span>", "Descubra o jeito mais fácil pra você", "Fazer o teste 👇"),
         P / "img/fim_quiz.png")

    E = P / "estaticos"
    if (P / "img/q1.png").exists():
        foto(quadro("<div class=bx style='top:900px'><h1>Por que o seu inglês<br>ainda <span class=am>não pegou</span>? 🤔</h1>"
                    "<p>Teste rápido: 6 perguntas, 1 minuto.</p><div class=bt style='margin-top:34px'>Fazer o teste 👇</div></div>",
                    P / "img/q1.png"), E / "quiz_estatico.png", 1080, 1350)
    for nome, img, h1, p in (
            ("sent_ja_tentou", "jt1.png", "Pagou cursinho e sentiu<br>que <span class=am>jogou dinheiro fora?</span> 💸",
             "O problema não foi você. Foi o método."),
            ("sent_presente", "mae3.png", "O presente que fica com<br>seu filho <span class=am>pra vida toda</span> 🎁",
             "Inglês de verdade, sem cursinho caro.")):
        foto(quadro(f"<div class=bx style='top:880px'><h1 style='font-size:68px'>{h1}</h1><p>{p}</p>"
                    "<div class=bt style='margin-top:30px'>Fazer o teste de 1 minuto 👇</div></div>", P / "img" / img),
             E / f"{nome}.png", 1080, 1350)
    foto(quadro("<div class=bx style='top:150px'><h1>Ainda com<br><span class=am>dúvida?</span></h1><div class='faq'>"
                "<div>💳 <b>Dá pra parcelar?</b><br>Sim, em até 3x no cartão.</div>"
                "<div>🔁 <b>Tem mensalidade?</b><br>Não. Pagamento único.</div>"
                "<div>📩 <b>Como eu recebo?</b><br>No seu e-mail, logo após a compra.</div>"
                "<div>🛡️ <b>E se eu não gostar?</b><br>7 dias de garantia.</div></div>"
                "<div class=bt style='margin-top:44px'>Fazer o teste rápido 👇</div></div>"), E / "remk_faq.png", 1080, 1350)
    pub = [("👩‍👦", "Pro seu filho", "aprender sem mensalidade cara"), ("😶", "Pra quem já fez curso", "e na hora de falar, travou"),
           ("✈️", "Pra quem vai viajar", "e tem medo de travar"), ("💼", "Pra prova e trabalho", "um pouco por dia, sem decoreba")]
    foto(quadro("<div class=bx style='top:130px'><h1>Pra quem é o<br><span class=am>Eagle Primeira Classe?</span></h1>"
                + "".join(f"<div class=card><h2>{e} {t}</h2><p style='margin-top:6px'>{s}</p></div>" for e, t, s in pub)
                + "</div>"), E / "remk_pra_quem.png", 1080, 1350)
    # carrossel "o que tem dentro": capa + 5 itens + fechamento
    foto(quadro("<div class=bx style='top:300px;text-align:center'><div style='font-size:170px'>🎒</div><h1>O que tem dentro do<br>"
                "<span class=am>Eagle Primeira Classe</span></h1><p>arrasta pro lado 👉</p></div>"), E / "remk_dentro_01.png", 1080, 1350)
    for i, (e, t, s) in enumerate(DENTRO, 2):
        foto(quadro(f"<div class=bx style='top:330px;text-align:center'><div style='font-size:200px'>{e}</div>"
                    f"<h1 style='margin-top:20px'>{t}</h1><p>{s}</p><p style='opacity:.6;margin-top:60px'>{i - 1}/5</p></div>"),
             E / f"remk_dentro_{i:02d}.png", 1080, 1350)
    foto(quadro("<div class=bx style='top:330px;text-align:center'><h1>Sem mensalidade.<br><span class=am>Pagamento único</span><br>"
                "ou até 3x no cartão.</h1><p>Acesso no e-mail na hora · 7 dias de garantia</p>"
                "<div class=bt style='margin-top:50px'>Descubra onde você trava 👇</div></div>"), E / "remk_dentro_07.png", 1080, 1350)
    nav.close()
print("ok")
