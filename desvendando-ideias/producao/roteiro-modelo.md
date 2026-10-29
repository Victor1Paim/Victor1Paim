# Modelo de roteiro (70–85 s)

Adaptado do "modelo de roteiro para cada Short" do plano de 30 dias do PDF (30–40 s) para a nossa faixa de 70–85 s e para as regras do canal.
O arquivo abaixo da linha `MODELO:INICIO` é copiado por `motor/novo.mjs` para `roteiros/NNN-slug.md`.

## Estrutura de tempo

| Trecho | Tempo | Função | Regra |
|---|---|---|---|
| Hook | 0–3 s | Promessa concreta, pergunta ou contraste verificável | Sem "Você sabia que…" genérico; o primeiro quadro já mostra o assunto |
| Contexto mínimo | 3–10 s | Nomear o objeto, lugar ou fenômeno e por que importa | Uma frase |
| Revelação em etapas | 10–55 s | 3 ou 4 elos "problema → solução → novo problema" (`../producao/padrao-cadeia-problema-solucao.md`) | Cada frase avança; cada plano muda algo (≤ 2,0 s) |
| Payoff | 55–70 s | Responde ao hook ou entrega a reviravolta | A resposta prometida aparece antes do fim |
| Fecho e CTA | 70–80 s | Retoma o gancho; CTA escolhido no portão 4 | Não sacrificar a conclusão para forçar loop |

Duração-alvo: **70–85 s** em todos os vídeos do teste de 30 dias (mesma faixa para comparar; nunca abaixo de 61 s).

<!-- MODELO:INICIO -->
# NNN · __TITULO__

Pilar: _(preencher)_ · Hook (tipo): _(preencher)_ · Pele: _(preencher)_ · Duração-alvo: 70–85 s · Criado em __DATA__
Status: **rascunho** · Projeto: `../producoes/NNN-__SLUG__/`

## Decisões (portões do fluxo)

| Portão | Escolha do usuário | Alternativas que ficaram de fora |
|---|---|---|
| 1. Tema e ângulo | _(pendente)_ | |
| 2. Hook | _(pendente)_ | |
| 3. Ordem das cenas | _(pendente)_ | |
| 4. CTA | _(pendente)_ | |
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
| | | | |

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
