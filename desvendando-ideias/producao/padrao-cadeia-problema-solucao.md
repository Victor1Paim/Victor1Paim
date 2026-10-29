# Padrão de explicação: cadeia problema → solução → novo problema

Comportamento-modelo para vídeos que **explicam por que algo é como é** (engenharia, construção, ciência aplicada). A ideia veio do exemplo do
telhado. Em vez de dar a resposta pronta, o vídeo **reconstrói** o objeto: tenta a solução óbvia, mostra onde ela falha, conserta, e a correção
cria o problema seguinte, até chegar no objeto real que o espectador reconhece.

Por que funciona: cada elo é um mini-hook (o espectador quer saber como se resolve), a retenção se renova a cada ~12–15 s, o resultado final
"faz sentido" porque cada peça nasceu de um problema, e o dado aparece como consequência, não como lista.

## Esqueleto (70–85 s)

| Bloco | Tempo | O que acontece | Fala-modelo |
|---|---|---|---|
| Hook | 0–5 s | Mostra o **objeto final** e faz a pergunta de lacuna | "Por que X é feito de ...?" |
| Ponto de partida | 5–15 s | A solução mais simples, ingênua | "Para ... a ideia mais simples é ..." |
| Elo 1: problema | 15–28 s | **Mostra o problema antes de explicar** (consequência antes da causa) | "Mas aí surge um problema: ..." |
| Elo 1: solução | 28–40 s | A forma muda (morph) para resolver | "A solução é ..." |
| Elo 2: novo problema | 40–55 s | A solução tem um custo que só aparece agora | "Só que isso cria outro problema: ..." |
| Elo 2: solução | 55–68 s | A forma muda de novo e chega perto do objeto real | "Então divide-se ..." |
| Remate | 68–80 s | Volta ao hook: o objeto final, agora explicado. Pergunta aberta que leva ao próximo vídeo | "Por isso X é assim. E por que ...?" |

Regras:
1. **3 a 4 elos no máximo.** Mais que isso vira aula e a retenção cai.
2. **Bordão fixo** entre elos: "Mas aí surge um problema." Repetir exatamente vira assinatura do canal e dá ritmo.
3. **O mesmo objeto atravessa o vídeo e se transforma** (morph); não trocar de cena a cada elo.
4. **Mostrar o problema antes de falar dele** (a água subindo, a rachadura aparecendo) e só então nomear.
5. **Cada elo tem um dado ou uma ideia visual**, nunca só texto (regra do canal, `../decisoes.md`).
6. **Honestidade didática:** é uma reconstrução para explicar, não a história real de quem inventou. Falar "uma das razões", "por isso, em geral", nunca "foi inventado para".
7. **Plano de 2 a 3 s** (revisado, decisão 28) (`regra-troca-a-cada-2s.md`): os blocos das tabelas abaixo são *beats*, e cada beat se divide em planos de 2 a 3 s com mudança de cenário, aproximação ou ângulo (2D, 2,5D ou 3D). Exemplo completo plano a plano em `../roteiros/001-quantas-terras-cabem-no-sol.md`.
8. **Remate com pergunta aberta** que vira o gancho do próximo vídeo (série encadeada, também favorece seguir o perfil).

## Movimentos fixos por papel (do dicionário)

| Papel | Movimento | Observação |
|---|---|---|
| Objeto entra | Slide in ou pop in | Só no começo |
| Problema aparece | Bar grow (água sobe), draw-on (rachadura) + **punch zoom** curto | Sempre com a mesma cor de alerta |
| Solução | **Morph** do objeto para a nova forma | É o movimento-assinatura do padrão |
| Troca de elo | Wipe curto | 4–6 frames |
| Dado | Count-up + overshoot leve | Só em números reais |
| Remate | Mask reveal do objeto final | Volta ao primeiro quadro |

## Exemplo: por que o telhado é feito de telhas

Hook A (pergunta): "Por que o telhado da sua casa é feito de pedacinhos?"

| Tempo | Tela (movimento) | Fala |
|---|---|---|
| 0–5 | Casa com telhado de telhas, zoom nas telhas (punch zoom) | "Por que o telhado da sua casa é feito de pedacinhos?" |
| 5–15 | Casa sem telhado; uma laje reta de concreto desenha por cima (draw-on) | "Para cobrir uma casa, a ideia mais simples é uma laje de concreto, reta e inteira. Forte, barata, fácil de fazer." |
| 15–28 | Chuva cai na laje; a água sobe e fica parada (bar grow azul) | "Mas aí surge um problema: quando chove, a água não tem para onde ir. Ela fica parada em cima da laje." |
| 28–40 | A laje inclina (morph); a água escorre para uma borda | "A solução é inclinar a cobertura. Com a inclinação, a água escorre." |
| 40–55 | Sol forte; setas de expansão na laje; rachadura abre (draw-on) | "Só que isso cria outro problema: uma peça inteira e grande dilata com o calor do sol e encolhe com o frio. E, presa, ela racha." |
| 55–68 | A laje se divide em peças menores que se sobrepõem (morph para telhas); cada telha tem uma pequena folga | "Então divide-se em peças pequenas, as telhas. Cada uma dilata um pouco sem forçar a vizinha, e a sobreposição deixa a água escorrer." |
| 68–80 | Volta à casa com telhado (mask reveal) | "É por isso que o telhado é feito de pedacinhos. E por que a telha tem aquela ondulação?" |

**Fatos a checar antes de produzir** (não afirmar sem fonte):
- Empoçamento de água em laje plana e impermeabilização: norma de impermeabilização (ABNT NBR 9575) e de desempenho de coberturas (NBR 15575-5).
- Dilatação térmica do concreto e uso de juntas de dilatação em lajes de cobertura (manual técnico ou norma).
- Observação: lajes de cobertura reais **também** são feitas com caimento e juntas. O vídeo mostra a reconstrução didática, e a fala precisa
  deixar claro que telha é **uma** solução comum, não a única.
- A função da sobreposição e da ondulação da telha (escoamento e resistência) precisa de fonte técnica.

## Onde aplicar nos nossos temas

| Vídeo | Cadeia |
|---|---|
| #10 Ponte com "buraco" | Ponte inteira → calor dilata → racha → junta de dilatação → junta entope/vaza → vedação |
| #2 Concreto cura | Concreto seca → perde resistência → molha/cobre → cura de 7 dias |
| #1 Taipei 101 | Prédio alto balança → enrijecer? → peso demais → amortecedor de massa |
| Novos | Por que o tijolo tem furos, por que pontes têm arcos, por que trilho tem folga |
