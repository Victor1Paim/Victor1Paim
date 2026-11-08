#!/usr/bin/env python3
"""Gera os 3 carrosséis de receitas (1080x1350) do Saúde sem Sermão como HTML e exporta cada lâmina em JPG."""
import json, re, subprocess
from pathlib import Path

SCR = Path("/tmp/claude-0/-home-user-Victor1Paim/bc508778-dc0e-5c3d-a4a6-a9dce8035bd2/scratchpad")
BASE = Path("/home/user/Victor1Paim/saude-sem-sermao/producoes/carrosseis")
src = (SCR / "build_sono.py").read_text()
ns = {}
exec(src[src.index("def tito_svg"):src.index("def fala_js")], ns)
tito = ns["tito_svg"]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,800;1,700;1,800&family=Nunito:wght@700;800;900&display=block');
*{box-sizing:border-box;margin:0;padding:0}
body{background:#ddd}
.s{position:relative;width:1080px;height:1350px;overflow:hidden;font-family:Nunito,sans-serif;color:#2B2B2B;margin-bottom:20px}
.foto{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.grad{position:absolute;left:0;right:0;bottom:0;height:62%;background:linear-gradient(rgba(0,0,0,0),rgba(20,24,20,.82))}
.gradtop{position:absolute;left:0;right:0;top:0;height:46%;background:linear-gradient(rgba(20,24,20,.72),rgba(0,0,0,0))}
.num{position:absolute;right:56px;top:52px;font-weight:900;font-size:32px;padding:6px 18px;border-radius:999px;background:rgba(255,255,255,.88);color:#2B2B2B}
.handle{position:absolute;left:60px;bottom:44px;font-weight:900;font-size:32px;opacity:.9}
.h1{font-family:'Playfair Display',serif;font-weight:800;line-height:1.02;letter-spacing:-.01em}
.h1 em{font-style:italic}
.tag{display:inline-block;padding:8px 22px;border-radius:999px;font-weight:900;font-size:32px;letter-spacing:.06em}
.body{font-weight:800;font-size:42px;line-height:1.3}
.fonte{font-weight:800;font-size:28px;opacity:.75}
.lista li{list-style:none;font-weight:800;font-size:40px;line-height:1.25;margin:0 0 22px;padding-left:54px;position:relative}
.lista li:before{content:"";position:absolute;left:0;top:12px;width:28px;height:28px;border-radius:50%;background:var(--ac)}
.tito{position:absolute;width:300px;height:330px}
.balao{background:#fff;border-radius:34px;padding:34px 40px;box-shadow:0 16px 40px rgba(80,40,20,.14);font-weight:900;font-size:42px;line-height:1.2;position:relative}
.balao .rot{font-size:28px;letter-spacing:.12em;color:var(--ac);margin-bottom:12px}
.aviso{background:rgba(255,255,255,.7);border-left:10px solid var(--ac);border-radius:18px;padding:24px 30px;font-weight:800;font-size:34px;line-height:1.3}
.cta-i{display:flex;gap:22px;justify-content:center}
.cta-i div{background:#fff;border-radius:28px;width:290px;height:200px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;font-weight:900;font-size:32px;color:#2B2B2B;box-shadow:0 14px 34px rgba(0,0,0,.18)}
.cta-i span{font-size:70px;line-height:1}
"""

H = "@saudesemsermao"


def slide_foto_capa(c, n, tot):
    return f'''<section class="s"><img class="foto" src="fotos/capa.png"><div class="gradtop"></div>
<div class="num">1/{tot}</div>
<div style="position:absolute;left:64px;top:110px;width:950px">
  <div class="tag" style="background:{c['ac']};color:#fff">MITO OU VERDADE?</div>
  <div class="h1" style="font-size:110px;color:#fff;margin-top:22px;text-shadow:0 4px 24px rgba(0,0,0,.35)">{c['titulo']}</div>
  <div style="margin-top:22px;font-weight:900;font-size:44px;color:#fff;text-shadow:0 2px 14px rgba(0,0,0,.5)">{c['sub']}</div>
</div>
<div class="handle" style="color:#fff">{H}</div></section>'''


def slide_texto(c, n, tot, selo, titulo, corpo, fonte, bg, cor):
    return f'''<section class="s" style="background:{bg};color:{cor}"><div class="num">{n}/{tot}</div>
<div style="position:absolute;left:72px;top:150px;width:936px">
  <div class="tag" style="background:{'#fff' if bg!='#fff' else c['ac']};color:{c['ac'] if bg!='#fff' else '#fff'}">{selo}</div>
  <div class="h1" style="font-size:84px;margin-top:34px">{titulo}</div>
  <div class="body" style="margin-top:40px">{corpo}</div>
  <div class="fonte" style="margin-top:44px">Fonte: {fonte}</div>
</div>
<div class="tito" style="right:30px;bottom:40px;width:270px;height:300px">{tito('s'+str(n), olhos='piscando')}</div>
<div class="handle">{H}</div></section>'''


def slide_tito(c, n, tot, pergunta, resposta, aviso):
    return f'''<section class="s" style="background:#FDF3ED"><div class="num">{n}/{tot}</div>
<div style="position:absolute;left:64px;top:140px;width:952px">
  <div class="balao"><div class="rot">💬 PERGUNTA DO TITO</div>{pergunta}</div>
  <div class="body" style="margin-top:56px;width:640px">{resposta}</div>
</div>
<div class="tito" style="right:20px;top:470px;width:360px;height:400px">{tito('t'+str(n), olhos='duvida')}</div>
{f'<div class="aviso" style="position:absolute;left:64px;right:64px;bottom:120px">{aviso}</div>' if aviso else ''}
<div class="handle">{H}</div></section>'''


def slide_foto(c, n, tot, foto, titulo, corpo):
    return f'''<section class="s"><img class="foto" src="fotos/{foto}.png"><div class="grad"></div><div class="num">{n}/{tot}</div>
<div style="position:absolute;left:64px;bottom:120px;width:952px;color:#fff">
  <div class="h1" style="font-size:84px;text-shadow:0 3px 18px rgba(0,0,0,.4)">{titulo}</div>
  <div class="body" style="margin-top:20px;text-shadow:0 2px 12px rgba(0,0,0,.5)">{corpo}</div>
</div>
<div class="handle" style="color:#fff">{H}</div></section>'''


def slide_ingredientes(c, n, tot, cab, itens):
    lis = "".join(f"<li>{i}</li>" for i in itens)
    return f'''<section class="s"><img class="foto" src="fotos/ingredientes.png" style="height:56%;object-position:center"><div class="num">{n}/{tot}</div>
<div style="position:absolute;left:0;right:0;bottom:0;height:47%;background:#FDF3ED;border-radius:44px 44px 0 0;padding:44px 64px 0">
  <div style="display:flex;justify-content:space-between;align-items:baseline"><div class="h1" style="font-size:70px">Ingredientes</div>
  <div style="font-weight:900;font-size:32px;color:{c['ac']}">{cab}</div></div>
  <ul class="lista" style="margin-top:26px;columns:1">{lis}</ul>
</div>
<div class="handle" style="left:auto;right:60px">{H}</div></section>'''


def slide_html(c, n, tot, html, bg="#FDF3ED"):
    return f'''<section class="s" style="background:{bg}"><div class="num">{n}/{tot}</div>{html}<div class="handle">{H}</div></section>'''


def slide_resumo(c, n, tot, itens):
    lis = "".join(f"<li>{i}</li>" for i in itens)
    return f'''<section class="s" style="background:#fff"><div class="num">{n}/{tot}</div>
<div style="position:absolute;left:72px;top:140px;width:936px">
  <div class="tag" style="background:{c['ac']};color:#fff">📌 SALVA ESSE RESUMO</div>
  <div class="h1" style="font-size:80px;margin:30px 0 44px">{c['resumo_t']}</div>
  <ul class="lista">{lis}</ul>
</div>
<div class="handle">{H}</div></section>'''


def slide_cta(c, n, tot):
    return f'''<section class="s" style="background:{c['ac']};color:#fff"><div class="num">{n}/{tot}</div>
<div style="position:absolute;left:72px;top:150px;width:936px">
  <div class="h1" style="font-size:96px">{c['cta']}</div>
</div>
<div class="cta-i" style="position:absolute;left:0;right:0;top:560px">
  <div><span>❤️</span>curte</div><div><span>💬</span>comenta "{c['palavra']}"</div><div><span>🧡</span>segue</div></div>
<div style="position:absolute;left:72px;right:72px;top:830px;font-weight:900;font-size:40px;text-align:center">{c['cta_sub']}</div>
<div style="position:absolute;left:72px;right:330px;bottom:120px;font-weight:800;font-size:30px;text-align:left;opacity:.92">Conteúdo educativo, não substitui orientação profissional.<br>Imagens ilustrativas geradas com IA.</div>
<div class="tito" style="right:50px;top:1000px;width:230px;height:260px">{tito('c'+str(n), olhos='piscando', bracos='acena')}</div>
<div class="handle">{H}</div></section>'''


def prato_svg(ac):
    return f'''<svg viewBox="0 0 400 400" width="520" height="520" style="position:absolute;left:280px;top:400px">
<circle cx="200" cy="200" r="190" fill="#fff" stroke="#E8E1D8" stroke-width="10"/>
<path d="M200 200 L200 18 A182 182 0 0 0 200 382 Z" fill="#95A185"/>
<path d="M200 200 L200 18 A182 182 0 0 1 382 200 Z" fill="#E2B04A"/>
<path d="M200 200 L382 200 A182 182 0 0 1 200 382 Z" fill="{ac}"/>
<text x="105" y="205" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="26" fill="#fff">½ vegetais</text>
<text x="285" y="125" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="22" fill="#2B2B2B">¼ arroz</text>
<text x="285" y="152" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="22" fill="#2B2B2B">+ feijão</text>
<text x="285" y="290" text-anchor="middle" font-family="Nunito" font-weight="900" font-size="22" fill="#fff">¼ proteína</text></svg>'''


CARROSSEIS = {
    "ovo": dict(ac="#D45F2B", titulo="Ovo aumenta o <em>colesterol?</em>", sub="+ omelete de forno pra semana toda",
                palavra="OVO", cta="Manda pra quem tem medo de ovo 🥚", cta_sub="E comenta OVO se vai fazer a receita!",
                resumo_t="Ovo sem sermão"),
    "arroz-feijao": dict(ac="#2F483A", titulo="Arroz com feijão <em>engorda?</em>", sub="+ como montar o prato feito equilibrado",
                palavra="PF", cta="Manda pra quem acha que arroz com feijão engorda 🍛", cta_sub="E comenta PF se esse é o seu almoço!",
                resumo_t="O PF sem sermão"),
    "lanche": dict(ac="#C2563A", titulo="Lanche da tarde em <em>5 minutos</em>", sub="a troca do biscoito recheado",
                palavra="LANCHE", cta="Manda pra quem vive de biscoito recheado 🍪", cta_sub="E comenta LANCHE se vai testar amanhã!",
                resumo_t="O lanche sem sermão"),
}

def montar(nome):
    c = CARROSSEIS[nome]; T = 10; s = []
    s.append(slide_foto_capa(c, 1, T))
    if nome == "ovo":
        s.append(slide_texto(c, 2, T, "✓ CIÊNCIA", "1 ovo por dia <em>não</em> aumentou o risco do coração",
            "Uma análise com 1,7 milhão de pessoas não viu ligação entre comer até 1 ovo por dia e doença cardiovascular.",
            "Drouin-Chartier et al., BMJ, 2020", "#2F483A", "#fff"))
        s.append(slide_tito(c, 3, T, "Ué, mas ovo não tem colesterol?",
            "Tem. Mas, pra maioria das pessoas, o colesterol do sangue depende mais do conjunto da alimentação do que do ovo sozinho.",
            "Tem diabetes ou colesterol alto? Combine a quantidade de ovos com seu médico ou nutricionista."))
        s.append(slide_ingredientes(c, 4, T, "4 porções · 30 min", ["4 ovos", "1 tomate picado", "½ cebola picada",
            "1 xícara de espinafre ou couve", "2 colheres (sopa) de queijo ralado", "sal, pimenta e orégano"]))
        s.append(slide_foto(c, 5, T, "batendo", "1. Bata e misture", "Bata os ovos com sal, pimenta e orégano. Junte o tomate, a cebola e o espinafre."))
        s.append(slide_foto(c, 6, T, "forma", "2. Forno", "Despeje numa forma untada, cubra com o queijo e asse a 180 °C por 20 a 25 minutos."))
        s.append(slide_foto(c, 7, T, "capa", "3. Ponto certo", "Pronto quando o centro fica firme. Espere 5 minutos e corte em quadrados."))
        s.append(slide_html(c, 8, T, f'''<div style="position:absolute;left:64px;top:150px;width:952px">
  <div class="balao"><div class="rot">💡 DICA DO TITO</div>Sobrou? Guarda na geladeira por até 3 dias: vira café da manhã, marmita ou recheio de sanduíche.</div>
  <div class="body" style="margin-top:50px;width:600px">Troque o espinafre por qualquer legume que tiver em casa: abobrinha, cenoura ralada, brócolis.</div></div>
  <div class="tito" style="right:30px;top:560px;width:380px;height:420px">{tito('d8', bracos='acena')}</div>'''))
        s.append(slide_resumo(c, 9, T, ["Até 1 ovo/dia não aumentou o risco do coração (maioria das pessoas)",
            "Colesterol do sangue: conta mais o conjunto da alimentação", "Omelete de forno: 4 ovos + legumes + 25 min a 180 °C",
            "Diabetes ou colesterol alto: combine com seu médico"]))
    elif nome == "arroz-feijao":
        s.append(slide_texto(c, 2, T, "✓ CIÊNCIA", "Arroz com feijão andou junto com <em>menos</em> sobrepeso",
            "Em estudos no Rio de Janeiro, o padrão tradicional de arroz com feijão esteve ligado a menos sobrepeso do que o padrão com mais gordura e açúcar.",
            "Sichieri, Obes Res, 2002 · Cunha et al., Br J Nutr, 2010 (estudos observacionais)", "#95A185", "#fff"))
        s.append(slide_tito(c, 3, T, "Mas arroz não é carboidrato demais?",
            "O que pesa é o prato todo e a quantidade. Arroz e feijão juntos se completam em proteína, e o feijão traz fibra, que ajuda a dar saciedade.",
            "O Guia Alimentar do Ministério da Saúde usa o arroz com feijão como base de refeições saudáveis."))
        s.append(slide_ingredientes(c, 4, T, "1 prato · exemplo", ["4 colheres (sopa) de arroz", "1 concha de feijão",
            "1 filé de frango (ou ovo, carne, peixe)", "salada à vontade", "legumes refogados"]))
        s.append(slide_foto(c, 5, T, "montagem", "1. Metade: vegetais", "Salada e legumes ocupam metade do prato. Quanto mais cor, melhor."))
        s.append(slide_html(c, 6, T, f'''<div style="position:absolute;left:64px;top:150px;width:952px">
  <div class="h1" style="font-size:84px">O método do <em style="color:{c['ac']}">prato</em></div>
  <div class="body" style="margin-top:18px">Ajuste a quantidade à sua fome.</div></div>{prato_svg(c['ac'])}''', bg="#F7E5DD"))
        s.append(slide_foto(c, 7, T, "capa", "2. O PF pronto", "Arroz e feijão num quarto, proteína no outro. Simples, barato e completo."))
        s.append(slide_html(c, 8, T, f'''<div style="position:absolute;left:64px;top:150px;width:952px">
  <div class="balao"><div class="rot">💡 DICA DO TITO</div>Faz feijão no fim de semana e congela em porções. Dura até 3 meses no freezer.</div>
  <div class="body" style="margin-top:50px;width:600px">Na correria, é só descongelar uma porção e montar o prato em 10 minutos.</div></div>
  <div class="tito" style="right:30px;top:560px;width:380px;height:420px">{tito('d8', bracos='acena')}</div>'''))
        s.append(slide_resumo(c, 9, T, ["Arroz com feijão andou junto com menos sobrepeso", "A dupla se completa em proteína; o feijão traz fibra",
            "Prato: ½ vegetais · ¼ arroz + feijão · ¼ proteína", "Feijão congelado em porções salva a semana"]))
    else:
        s.append(slide_texto(c, 2, T, "✓ GUIA ALIMENTAR", "Biscoito recheado é <em>ultraprocessado</em>",
            "O Guia Alimentar do Ministério da Saúde recomenda evitar ultraprocessados e preferir fruta e preparações feitas em casa.",
            "Guia Alimentar para a População Brasileira, 2014", "#F7E5DD", "#2B2B2B"))
        s.append(slide_tito(c, 3, T, "Mas biscoito é tão prático…",
            "Esse lanche também é: 5 minutos e 4 ingredientes. Tem fruta, a fibra da aveia e a proteína do iogurte.", ""))
        s.append(slide_ingredientes(c, 4, T, "1 porção · 5 min", ["1 pote de iogurte natural (170 g)", "1 banana",
            "3 morangos (ou outra fruta)", "2 colheres (sopa) de aveia", "mel: opcional, só um fio"]))
        s.append(slide_foto(c, 5, T, "camadas", "1. Faça camadas", "Aveia e banana no fundo do copo, iogurte natural por cima."))
        s.append(slide_foto(c, 6, T, "capa", "2. Finalize", "Morango e mais aveia por cima. Se quiser, um fio de mel."))
        s.append(slide_html(c, 7, T, f'''<div style="position:absolute;left:64px;top:150px;width:952px">
  <div class="h1" style="font-size:84px">A <em style="color:{c['ac']}">troca</em></div></div>
  <div style="position:absolute;left:64px;top:330px;width:440px;height:560px;background:#fff;border-radius:34px;padding:40px;box-shadow:0 14px 34px rgba(0,0,0,.08)">
    <div style="font-size:80px">🍪</div><div class="h1" style="font-size:52px;margin:16px 0 24px">Biscoito recheado</div>
    <div class="body" style="font-size:36px;color:#6b6460">ultraprocessado<br>açúcar e gordura<br>pouca fibra</div></div>
  <div style="position:absolute;right:64px;top:330px;width:440px;height:560px;background:{c['ac']};color:#fff;border-radius:34px;padding:40px">
    <div style="font-size:80px">🥣</div><div class="h1" style="font-size:52px;margin:16px 0 24px">Copo do Tito</div>
    <div class="body" style="font-size:36px">comida de verdade<br>fruta + aveia + iogurte<br>fibra e proteína</div></div>
  <div class="tito" style="left:400px;top:930px;width:260px;height:290px">{tito('d7', olhos='piscando')}</div>''', bg="#FDF3ED"))
        s.append(slide_html(c, 8, T, f'''<div style="position:absolute;left:64px;top:150px;width:952px">
  <div class="balao"><div class="rot">💡 DICA DO TITO</div>Monta 3 copos à noite, sem a fruta, e guarda na geladeira.</div>
  <div class="body" style="margin-top:50px;width:600px">De manhã é só pôr a fruta e levar. A aveia fica macia e o lanche já está pronto.</div></div>
  <div class="tito" style="right:30px;top:560px;width:380px;height:420px">{tito('d8', bracos='acena')}</div>'''))
        s.append(slide_resumo(c, 9, T, ["Biscoito recheado é ultraprocessado (Guia Alimentar)", "Troca: iogurte natural + fruta + aveia",
            "5 minutos, 4 ingredientes, sem fogão", "Dá pra deixar 3 copos prontos na geladeira"]))
    s.append(slide_cta(c, 10, T))
    html = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS.replace('var(--ac)', c['ac'])}</style></head><body>{''.join(s)}</body></html>"
    (BASE / nome / "carrossel.html").write_text(html)
    print(nome, len(s), "lâminas")


for nome in CARROSSEIS:
    montar(nome)
