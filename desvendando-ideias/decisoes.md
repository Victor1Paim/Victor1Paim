# Desvendando Ideias — Decisões (28/10/2026)

Resultado da rodada de perguntas ("grill me"). **Onde houver conflito, este arquivo vale mais que o `plano-do-canal.md`**, que foi escrito antes.

| # | Decisão | Origem |
|---|---|---|
| 1 | Objetivo dos primeiros 6–12 meses: crescer audiência e **monetizar no TikTok**. Depois, tráfego para o Instagram (link na bio) e produtos de ensino | Resposta do usuário |
| 2 | **Vídeos de 60–90 s** no dia a dia (monetização no TikTok exige 1 min ou mais). Vídeos longos do YouTube ficam para depois; YouTube entra com Shorts reaproveitados | Resposta do usuário |
| 3 | Requisitos de monetização (informados pelo usuário, **a confirmar com fonte oficial**): 10 mil seguidores, vídeos de 1 min ou mais, 100 mil views nos últimos 30 dias | Resposta do usuário |
| 4 | Infoproduto: **produtos de ensino**, tema a definir; o plano anterior de "ensinar a criar canais" foi descartado por ora | Resposta do usuário |
| 5 | Cadência: **1 vídeo por dia (7 por semana)** nos primeiros 90 dias | Resposta do usuário |
| 6 | Gasto: **o mínimo possível**, apoiado nas skills (visual por código, voz no modelo mais barato ou local). Sem teto fixo em reais; acompanhar com `gemini-midia usage` | Resposta do usuário |
| 7 | Visual padrão: **tipografia animada + infográficos em código** (Remotion/mg-styles), sem rosto, sem stock | Resposta do usuário |
| 8 | Temas: engenharia, saúde, curiosidades de finanças/economia/construção e outros a definir por pesquisa. **O diferencial é o hook**, e cada hook e cada tema terão uma ficha de comportamento | Resposta do usuário |
| 9 | Pesquisa em `pesquisa/prompt-pesquisa-temas-hooks.md` rodada no Grok em 28/10/2026 (resultado abaixo) | Resposta do usuário |

## Resultado da pesquisa (Grok, 28/10/2026)

Texto completo em [`pesquisa/resultado-grok-2026-10-28.md`](pesquisa/resultado-grok-2026-10-28.md). As marcações de "confirmado" são do Grok;
nós não conseguimos abrir as fontes. **Tratar como pendente de conferência no app/TikTok Studio** o que vira regra.

| # | Decisão adotada a partir da pesquisa |
|---|---|
| 10 | Duração-alvo **70–85 s** (nunca abaixo de 61 s). Os termos dizem "pelo menos 1 minuto" e outras páginas "mais de 1 minuto"; 61 s atende às duas leituras |
| 11 | Rótulo de conteúdo gerado por IA **sempre ligado** (voz sintética) |
| 12 | Saúde e finanças: **2 fontes primárias oficiais** por afirmação (OMS, Ministério da Saúde, Anvisa, Banco Central, IBGE, Receita), fonte na tela por 2–3 s, linguagem "segundo X". Proibido: "cura", "garantido", "enriqueça rápido", "ninguém te conta o segredo" |
| 13 | Catálogo de 12 hooks do Grok adotado como ponto de partida; a ficha de comportamento de cada um precisa ser completada |
| 14 | Calendário inicial: engenharia (dias 1–5), finanças (6–10), saúde (11–15), construção (16–20), depois misto pelo que reteve. Não matar um tema antes de 5–7 vídeos |
| 15 | Regras de teste do Grok como ponto de partida: trocar hook se saída em 3 s < 30% em 5 vídeos; focar tema se shares > 2% e > 0,5 seguidor por vídeo em 7 vídeos |
| 17 | **Troca visual a cada 2 s, no máximo** (cenário, aproximação ou ângulo; 2D, 2,5D ou 3D): ~38–45 planos por vídeo de 70–85 s. Detalhes em `producao/regra-troca-a-cada-2s.md` | Resposta do usuário |
| 18 | Padrão de explicação "problema → solução → novo problema" (exemplo do telhado) para vídeos de engenharia e construção. `producao/padrao-cadeia-problema-solucao.md` | Resposta do usuário |
| 19 | Piloto: vídeo 001 "Quantas Terras cabem no Sol" (`roteiros/001-quantas-terras-cabem-no-sol.md`) | Resposta do usuário |
| 20 | **Portões de decisão:** hook, ordem das cenas, CTA, mensagem final e tema do próximo vídeo são escolhas do usuário, uma pergunta por portão; o Claude não segue sem resposta (`producao/fluxo-por-video.md`) | Resposta do usuário (29/10) |
| 21 | Vídeo 001: hook A (adivinhar), ordem "escala primeiro", CTA "Seguir", fecho "pergunta com cubos". **Próximo tema em aberto** | Resposta do usuário (29/10) |
| 22 | Produção em **HyperFrames** (HTML + GSAP), vertical 1080×1920, estilo não fixado (mistura 2D, 2,5D e 3D por plano); 3D só em CSS porque o ambiente não tem WebGL | Resposta do usuário (28/10) |
| 16 | Postar o mesmo arquivo limpo (sem marca d'água) em TikTok, Reels e Shorts, com legenda e capa nativas |

### Riscos e lacunas da pesquisa

1. **Risco principal: nosso visual pode ser lido como "só texto".** A lista de conteúdo que não conta inclui "slideshows" e "só texto overlays".
   Tipografia animada sem movimento real de infográfico, diagrama e transformação de números cairia nisso. O modelo de vídeo precisa ter
   **animação de dados e diagramas de verdade** e narração com roteiro próprio; teste com os primeiros 10 vídeos e ver se entram em "For You".
   O próprio Grok listou isso como não confirmado.
2. **Tabela de 60 temas incompleta:** vieram 5 linhas e um "...". Falta pedir de novo.
3. **Contas de referência sem verificação** (sem links, sem métricas). Conferir no app.
4. **Hooks sem exemplos reais com link e sem dados de retenção**, que o prompt pedia. As aberturas prontas em português só aparecem para um dos 12.
5. **Contradições leves:** "pelo menos 1 minuto" vs "mais de 1 minuto" (resolvido usando 61 s); limites de upload citados (TikTok 60 min, Reels 20 min, Shorts 3 min) não foram confirmados e não afetam o plano.
6. **RPM Brasil** (US$ 0,15–0,50 por mil views) é relato, não dado oficial. Em 100 mil views seriam algo entre US$ 15 e US$ 50. Para planejar, tratar a receita inicial como baixa.
7. O Grok chamou de "dado oficial" a regra de que a conta precisa ter 1.000 views no For You por vídeo; conferir.

## Consequências para o trabalho

- Um vídeo por dia com pouco gasto exige **modelo de composição fixo** (template Remotion) em que só mudam roteiro, números e voz.
- Saúde e finanças pedem checagem de fontes e linguagem cuidadosa; a pesquisa inclui as regras das plataformas.
- Até chegar aos requisitos de monetização tudo é custo sem receita: medir custo por vídeo desde o primeiro.
- Conteúdo em massa, repetitivo e voz sintética sem valor agregado é risco de elegibilidade; ver tópico 1 da pesquisa.

## Ainda em aberto

1. Voz do canal (modelo do Gemini ou outra) e o teste pendente do `voz-teste.wav`.
2. Regras exatas de monetização e de rótulo de IA (a pesquisa responde).
3. Nome e identidade visual do modelo de vídeo (paleta, fonte, animação padrão de hook).
4. Processo de uso das skills com gasto mínimo, por etapa do vídeo.
5. Quem revisa fatos de saúde e finanças e como.
