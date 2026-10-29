# 003 · O lagarto por trás do Ozempic

Pilar: Saúde · Hook (tipo): história/consequência (escolha do usuário; o plano pedia "você aprendeu errado" no dia 3, a mudança fica anotada para o quadrado latino) · Pele: _(a decidir: plano diz Isométrico 2.5D, que ainda não cobre todos os planos)_ · Duração-alvo: 70–85 s · Criado em 2026-10-29
Status: **rascunho** · Projeto: `../producoes/003-lagarto-ozempic/`

## Decisões (portões do fluxo)

| Portão | Escolha do usuário | Alternativas que ficaram de fora |
|---|---|---|
| 1. Tema e ângulo | **P29 · O remédio da moda veio do veneno de um lagarto** (29/10/2026; usuário respondeu "Tem 1") | Mito "queima gordura" (P31), injeção semanal (P32), Ozempic × Mounjaro (P33) e outros 6 temas de GLP-1; estalar dedos e demais mitos de saúde |
| 2. Hook | **3 · "Em 1992, um médico foi estudar veneno de lagarto. E acabou mudando o tratamento do diabetes."** Primeiro quadro: "1992" digitado (typewriter) com o lagarto (29/10/2026) | 1 "lagarto ajudou a criar", 2 "veneno na história", 4 mito VENENO → INSPIRAÇÃO, 5 "meses sem comer" |
| 3. Ordem das cenas | _(pendente)_ | |
| 4. CTA | **2 · "Comenta: de qual outro remédio você quer saber a origem? Deixa o like e segue pra mais curiosidades."** + aviso fixo "Não use sem prescrição. Converse com seu médico." (29/10/2026) | 1 dúvida + like + seguir, 3 "conhecia essa história?", 4 "qual animal vai virar remédio", 5 dúvida sobre remédios |
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
| Exendina-4 foi achada no veneno do monstro-de-gila por John Eng (VA do Bronx) em 1992 | 1992 | 1 fonte boa (Golden Goose Award) + Nautilus | Fonte científica primária (artigo de 1992) ou revisão |
| Eng escolheu o lagarto porque a mordida causava pancreatite | — | Golden Goose Award + Biotech Academy | Ok com 2 fontes; conferir texto |
| Exenatida (Byetta) aprovada pela FDA em abril de 2005, para diabetes tipo 2 | abr/2005 | RAPS + UNC Endeavors | Ok com 2 fontes |
| O GLP-1 humano dura cerca de 2 minutos no sangue (enzima DPP-4) | ~2 min | 1 fonte (Nautilus) | **Segunda fonte** (revisão médica) |
| A exendina-4 resiste à DPP-4 e dura bem mais | "horas" (fontes divergem nos números) | Biotech Academy + Nautilus | Não citar número exato |
| A semaglutida (Ozempic) **não** é feita de veneno: é sintética, desenhada a partir do GLP-1 humano | — | Nautilus + InfoMoney | Bula/Novo Nordisk |
| A semaglutida dura cerca de 1 semana no corpo (dose semanal) | ~1 semana | — | Bula (ANVISA/EMA) + 1 fonte |
| O monstro-de-gila passa longos períodos sem comer | — | — | 2 fontes de biologia, **só usar se confirmar** |

Regras de remédio: ver `../pautas/banco.md` ("Regras extras para remédios"). Na tela e na legenda: "Não use sem prescrição. Converse com seu médico."

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
