# Anúncios de teste #1 — vender o SENTIMENTO e levar pro QUIZ (Meta Ads, 27/11/2026)

**Direção do usuário (27/11):** vender o sentimento (presente pro filho sem cursinho caro · "paguei cursinho e só gastei dinheiro,
acho que não consigo aprender" · medo de travar na viagem) → virada **"o problema não foi você, nem o inglês: foi o MÉTODO"** →
CTA SEMPRE para o **quiz** ("faz o teste de 1 minuto e descobre onde você trava"). O quiz leva à oferta.

Destino de TODOS os anúncios (trocar só o utm_campaign/utm_content):
```
https://eagle-viagem.vercel.app/?utm_source=meta&utm_medium=ads&utm_campaign=<campanha>&utm_content=<criativo>
```
Botão: **Saiba mais** (ou "Começar" se aparecer). Marcar conteúdo de IA se o Gerenciador pedir.
Otimização: no começo **Lead** (evento no fim do quiz, quando o Pixel estiver instalado) ou **Visualização da página de destino**;
trocar para **Compra** quando passar de ~20 compras/semana (ver docs/META_ADS.md).

## CAMPANHA 1 — "Sentimento" (vídeos narrados, voz de locutor ElevenLabs) · utm_campaign=sentimento · R$ 30–50/dia
Mesmo conjunto, 4 anúncios (público aberto Brasil 18–55):

**video/mae.mp4** (utm_content=mae) — presente pro filho
```
Sabe aquele presente que não quebra, não sai de moda e fica com o seu filho pra vida toda? 🎁

Inglês. Mas sem cursinho caro e mensalidade todo mês. Se ele estuda e não sai do lugar, o problema não é ele: é o método.

Faz o teste rápido de 1 minuto e descobre onde ele trava e o jeito mais fácil pra ele aprender 👇
```
Título: `Onde o seu filho trava no inglês?` · Descrição: `Teste rápido · 1 minuto`

**video/jatentou.mp4** (utm_content=jatentou) — já pagou e não aprendeu
```
Pagou cursinho, comprou apostila… e sentiu que só jogou dinheiro fora? 💸

Se bateu aquele pensamento de "eu não nasci pra aprender inglês": o problema nunca foi você, nem o inglês. Foi o método.

Faz o teste de 1 minuto e descobre exatamente onde você trava 👇
```
Título: `O problema foi o método` · Descrição: `Descubra onde você trava`

**video/viagem.mp4** (utm_content=viagem) — medo de travar
```
E se você travar no aeroporto? 😰

Ficar só apontando e sorrindo, com vergonha de falar… não precisa ser assim. Você não tem problema com inglês: falta o treino certo.

Faz o teste de 1 minuto e descobre onde você trava antes de embarcar ✈️
```
Título: `Vai viajar? Descubra onde você trava` · Descrição: `Teste rápido · 1 minuto`

**video/dedo.mp4** (utm_content=dedo) — "levanta um dedo"
```
☝️ Levanta um dedo se você já sentiu que inglês não é pra você.
…se já fez curso e sentiu que só gastou dinheiro,
…se quer dar pro seu filho o inglês que você não teve, sem cursinho caro,
…ou se tem medo de travar na viagem.

O problema nunca foi o inglês. Foi o método. Faz o teste de 1 minuto e descobre onde você trava 👇
```
Título: `Inglês não é pra você? Será?` · Descrição: `Teste rápido · 1 minuto`

## CAMPANHA 2 — "Quiz direto" (sem voz + imagens) · utm_campaign=quiz · R$ 20–30/dia
- **video/quiz_mudo.mp4** (14 s, só texto; ativar "Música" no Gerenciador) · utm_content=quiz_video
- **estaticos/quiz_estatico.png** "Por que o seu inglês ainda não pegou?" · utm_content=quiz_img
- **estaticos/sent_ja_tentou.png** "Pagou cursinho e sentiu que jogou dinheiro fora?" · utm_content=img_jatentou
- **estaticos/sent_presente.png** "O presente que fica com seu filho pra vida toda" · utm_content=img_presente
Texto principal (todos):
```
Estudou inglês e ainda não pegou? O problema não foi você: foi o método.
Faz o teste rápido (6 perguntas, 1 minuto) e descobre onde você trava e o jeito mais fácil de aprender, pra você ou pro seu filho 👇
```
Título: `Por que o seu inglês não pegou?` · Descrição: `Teste rápido · 1 minuto`

## CAMPANHA 3 — Remarketing (entra em 1–2 semanas) · utm_campaign=remarketing · R$ 10–15/dia
Público: interagiu com @eagle.english.br (30 dias) + visitou o site. Criativos:
- **estaticos/remk_dentro_01…07.png** (carrossel "O que tem dentro") · utm_content=carrossel
- **estaticos/remk_faq.png** ("Ainda com dúvida?") · utm_content=faq
- **estaticos/remk_pra_quem.png** ("Pra quem é") · utm_content=pra_quem
```
Ainda pensando? Sem mensalidade: pagamento único ou até 3x no cartão, acesso no e-mail na hora e 7 dias de garantia.
Faz o teste de 1 minuto e vê o jeito mais fácil pra você 👇
```

## CAMPANHA 4 — Impulsionar Reels orgânicos que forem bem (opcional, R$ 10–20/dia, 3–5 dias)
Sem material novo: escolher no Instagram o Reels com mais salvamentos da semana e impulsionar (objetivo: visitas ao perfil).

## Regras usadas (para não reprovar)
Sem promessa de fluência, sem "você é burro/ruim", sem marca de terceiros (página /oferta já sem "Big Mac"), sem depoimento,
sem preço fixo, pessoas por IA SEM aviso no vídeo: o usuário marca "conteúdo de IA" direto no Gerenciador de Anúncios.
