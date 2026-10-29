# 001 · Quantas Terras cabem no Sol

Tema: curiosidades (escala) · Duração: ~73 s (voz 66 s + 1,4 s de pausa final + planos sem fala) · Planos ≤ 2,0 s (`../producao/regra-troca-a-cada-2s.md`)
Status: **rascunho 2, aguardando seu "aprovado" no corte de teste (portão 7)** · Projeto: `../producoes/001-sol/` (HyperFrames, 1080×1920)

## Decisões (portões do fluxo, 29/10/2026)

| Portão | Escolha do usuário | Alternativas que ficaram de fora |
|---|---|---|
| 2. Hook | **A · Desafio de adivinhar:** "Quantas Terras cabem dentro do Sol? Pensa num número antes que eu fale." | B contradição ("tem uma pegadinha"), C basquete/alfinete, D número absurdo (reservados para outros vídeos) |
| 3. Ordem das cenas | **3 · Escala primeiro:** basquete e alfinete → 109× → volume ao cubo → pegadinha → resposta | Tamanho/volume (antiga), pegadinha cedo, resposta primeiro |
| 4. CTA | **Seguir:** "Segue para descobrir mais curiosidades." | Comentar, compartilhar, sem CTA |
| 5. Fecho | **Pergunta com cubos:** "E se a Terra fosse um cubo? Sem vãos, cabem quase um milhão e trezentas mil." | Síntese, humor, texto próprio |
| Próximo vídeo | **Não definido.** O rascunho anterior prometia "as gigantes" sem a sua escolha; foi removido. Escolher junto, em outro portão | — |

Pendentes: portão 6 (aprovar o texto abaixo), portão 7 (corte de teste), portão 8 (legenda, capa, hashtags).

## Texto falado (por beat, como vai para a voz)

1. **Hook.** Quantas Terras cabem dentro do Sol? Pensa num número antes que eu fale. *(+1,8 s de contagem 3-2-1 sem fala)*
2. **Escala.** Primeiro, o tamanho. Se o Sol fosse uma bola de basquete, a Terra seria do tamanho da cabeça de um alfinete. Na vida real, o Sol é cerca de cento e nove vezes mais largo que a Terra.
3. **Volume.** Mas volume não cresce em linha reta, cresce ao cubo. Cento e nove vezes mais largo, mais alto e mais fundo dá cerca de um milhão e trezentas mil Terras. Se você chutou por aí, acertou. Mas tem uma pegadinha.
4. **Pegadinha.** Essa conta vale se você derretesse as Terras e enchesse o Sol como água. Mas a Terra é uma bola. E bola não encaixa sem deixar vãos.
5. **Empacotamento.** Empilhando esferas do jeito mais eficiente que existe, só setenta e quatro por cento do espaço é ocupado.
6. **Resposta.** Então, com Terras inteiras, cabem no máximo cerca de novecentas e sessenta mil.
7. **Fecho e CTA.** E se a Terra fosse um cubo? Sem vãos, cabem quase um milhão e trezentas mil. Segue para descobrir mais curiosidades.

Os 45 planos (estilo 2D, 2,5D ou 3D por plano, início e duração) saem de `../producoes/001-sol/shots.json` e ficam listados em `../producoes/001-sol/PLANOS.md`.

## Conferência de fatos

| Afirmação | Valor usado | Estado | O que falta |
|---|---|---|---|
| Diâmetro do Sol ÷ diâmetro da Terra | ~109 | Conta com 1.392.700 km e 12.742 km: 109,3 | **Ficha do Sol da NASA** (domínio fora da rede da sessão); o vídeo mostra "Fonte: NASA" no plano do 1,3 milhão: **só publicar depois de conferir** |
| Volume do Sol ÷ volume da Terra | ~1,3 milhão | Fontes secundárias (1,41×10¹⁸ km³ ÷ 1,08×10¹² km³) e 109,3³ ≈ 1,306 milhão | NASA |
| Bola de basquete → Terra | ~2 mm | Conta própria: 24 cm ÷ 109,3 = 2,2 mm | Aceitável |
| Empacotamento de esferas iguais | 74% (π/√18 ≈ 0,7405) | Resultado matemático (conjectura de Kepler) | 1 fonte de matemática |
| ~960 mil Terras | 1,3 milhão × 0,7405 ≈ 962,6 mil | Conta própria; dentro de uma esfera há perda a mais nas bordas, por isso "no máximo" | Dizer "no máximo cerca de" (já está) |
| Cubos | "quase 1,3 milhão" | Cubos de mesmo volume encaixam sem vãos entre si; na borda curva do Sol sobra uma perda pequena, por isso "quase" | Confirmar com conta de borda se quiser dar número exato |

Antes de publicar: 2 fontes para o 109 e o 1,3 milhão e 1 para o 74%.

## Ficha de produção

- Voz: Gemini TTS, modelo Lite, voz Kore, **sem** instrução de estilo (ela é lida em voz alta); um arquivo por beat. Voz do canal ainda é decisão sua (ouvir amostras).
- Visual: paleta provisória (azul-noite, âmbar, azul-Terra); estilo único **não** definido, cada plano usa 2D, 2,5D ou 3D (CSS 3D, sem WebGL).
- Sem música e sem efeitos sonoros por enquanto.
- Rótulo de conteúdo gerado por IA ligado na publicação.
