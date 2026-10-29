# 002 · A nota de R$ 100 encolheu

Pilar: Finanças/Economia · Hook (tipo): Contradição (dia 2 do plano) · Pele: _(a decidir: plano diz Neo-brutalismo; 001 usou Cosmos)_ · Duração-alvo: 70–85 s · Criado em 2026-10-29
Status: **portão 1 decidido; aguardando hook e CTA** · Projeto: `../producoes/002-inflacao/`

## Decisões (portões do fluxo)

| Portão | Escolha do usuário | Alternativas que ficaram de fora |
|---|---|---|
| 1. Tema e ângulo | **Inflação: a nota de R$ 100 encolheu** (29/10/2026) | Imposto na nota fiscal, R$ 200/mês por 20 anos, 10 temas de engenharia (P15–P23) |
| 2. Hook | _(pendente: 5 opções enviadas)_ | |
| 3. Ordem das cenas | _(pendente)_ | |
| 4. CTA | _(pendente: 5 opções enviadas)_ | |
| 5. Fecho e próximo vídeo | _(pendente)_ | |
| 6. Roteiro aprovado | _(pendente)_ | |
| 7. Corte de teste | _(pendente)_ | |
| 8. Publicação (legenda, capa, hashtags, horário) | _(pendente)_ | |

## Texto falado (por beat, como vai para a voz)

1. **Hook.** …
2. **Contexto.** …
3. **Revelação (elos).** …
4. **Payoff.** …
5. **Fecho e CTA.** …

## Conferência de fatos

| Afirmação | Valor usado | Estado | O que falta |
|---|---|---|---|
| R$ 100 de jan/2010 equivalem a cerca de R$ 250 hoje (IPCA) | ≈ R$ 245 até dez/2025; ≈ R$ 254 até jun/2026 (conta com o IPCA anual do IBGE: 2010–2024 conhecidos, 2025 = 4,26%, 2026 até jun = 3,36% segundo investidor10) | **A conferir** | Rodar a Calculadora do Cidadão (Banco Central) com IPCA, 01/2010 → mês atual; segunda fonte: IBGE (série do IPCA). Hosts do BCB/IBGE bloqueados nesta sessão |
| R$ 100 de hoje compram o que ~R$ 40 compravam em 2010 | 100 / 2,5 ≈ 40 | **A conferir** | Sai da mesma conta acima |

Regras: 2 fontes primárias para saúde e finanças; fonte na tela por 2–3 s; nada de "cura", "garantido", "segredo" para fato conhecido; lenda nunca como fato.

## Checklist do roteiro (antes de gerar a voz)

- [ ] O hook deixa claro o assunto e abre uma pergunta que **será respondida**?
- [ ] A resposta prometida aparece antes do fim?
- [ ] Cada afirmação factual foi conferida? (tabela acima)
- [ ] Há **uma** ideia principal, e não vários fatos soltos?
- [ ] O texto funciona em voz alta e cabe em 70–85 s (≈ 2,4 palavras por segundo)?
- [ ] O título e a legenda do post descrevem o vídeo sem prometer o que ele não entrega?
- [ ] Revisado **sem som** (a legenda e a imagem bastam?) e **sem imagem** (a história se entende só pela voz)?
- [ ] Não reaproveita o roteiro de outro vídeo trocando só as imagens?

## Ficha de produção

- Voz: Gemini TTS, modelo Lite, sem instrução de estilo; um arquivo por beat. Custo registrado: _(preencher)_
- Planos e som: `shots.json` e `motor/sfx.py`. Rodar `node ../../motor/checar.mjs --full` antes de entregar.
- Rótulo de conteúdo gerado por IA ligado na publicação.
- Métricas: registrar em `../metricas/videos.csv` após 24 h e 7 dias, sempre anotando a idade do vídeo.
