# Análise do "Plano de ação: primeiros 30 dias de um canal de Shorts de curiosidades" (PDF, 9 páginas)

O PDF é um plano de **método** para um canal de Shorts de curiosidades (YouTube): 20 vídeos em 30 dias, 3 pilares, 30–40 s, testes comparáveis, medianas e regras de decisão.
Não traz fontes nem números de desempenho: o que ele vale é o **desenho de experimento** e a **disciplina editorial**. Esta página separa o que adotamos, o que mudamos e o que não serve.

## 1. O que o PDF tem de melhor (adotado)

| Ideia do PDF | Por que importa para nós | Onde entrou |
|---|---|---|
| **Um vídeo isolado não prova nada**; o mês 1 serve para aprender | Evita decidir cedo com 1 vídeo viral ou ruim | `plano-30-dias.md`, seção 1 |
| **Não mudar tema, duração, estilo visual e horário ao mesmo tempo** | Sem isso, não se sabe o que causou o resultado. Nós estávamos prestes a variar pilar, hook, pele e duração juntos | Seção 2: fixos = duração, voz, estrutura, horário e **pele**; variam só pilar e hook |
| Distribuição **balanceada** entre pilares + vídeos finais de **confirmação** | Dá amostra comparável e testa se o resultado se repete | Quadrado latino 5×5 (25 vídeos) + 5 de confirmação |
| **Comparar vídeos de idade semelhante** (24 h com 24 h, 7 dias com 7 dias) | Vídeo velho sempre parece melhor | `videos.csv` tem colunas separadas de 24 h e 7 dias |
| **Mediana**, não média; nada de limite universal de sucesso | Um viral distorce a média; os limites absolutos que o Grok sugeriu eram palpite | `metricas/resumo.py` usa a mediana do próprio canal |
| **Revisão semanal com uma única correção** para a semana seguinte | Mantém o experimento interpretável | Dias 7, 14, 21 |
| "Separar **tema promissor** de **execução promissora**" | Um bom tema pode ter perdido por áudio, hook ou edição | Regra de leitura no plano e no `resumo.py` |
| **Planilha com colunas definidas** antes de começar | Evita lembrar dados depois | `metricas/videos.csv` |
| **Banco de pelo menos 30 ideias**, fontes guardadas e checagem de nomes, datas, números | Sem estoque de pautas a cadência de 1 por dia quebra | `pautas/banco.md` |
| **2 ou 3 opções de hook** para a mesma história | É o que já fazemos no portão 2 | Mantido |
| **Revisar sem som e sem imagem** | Cobre quem assiste mudo e quem só ouve | Checklist do `roteiro-modelo.md` |
| Limites editoriais: não apresentar lenda como fato, não chamar de "segredo" o que é conhecido, não aconselhar saúde, não reciclar roteiro trocando só imagens | Credibilidade e risco de conteúdo repetitivo na monetização | `roteiro-modelo.md` |
| **Regras de decisão** do fim do mês (repetir, ajustar, reeditar o processo, suspender, não escalar) | Decisão antes dos dados, não depois | Seção 8 do plano |
| **Mês 2: um teste principal por vez** | Continuidade do método | Seção 8 do plano |

## 2. O que mudamos (e por quê)

| PDF | Nosso plano | Motivo |
|---|---|---|
| 20 vídeos, **5 por semana** | **30 vídeos, 7 por semana** (sua decisão) | Meta de ser monetizado no TikTok. Mas o PDF avisa que isso exige rotina: ver seção 6 do plano (sessão de pauta em lote); se faltar tempo, cai para 5 |
| 30–40 s | **70–85 s** | O TikTok só monetiza vídeos acima de 1 min (seu requisito); 30–40 s não monetiza |
| 3 pilares: mistérios/lugares, história bizarra, "e se…?"/ciência | **5 pilares** (conjunto A) ou o conjunto B com "mistérios/história" | Você pediu engenharia, saúde, finanças/economia, construção e curiosidades; o conjunto B traz também os pilares do PDF |
| "E se…?" como **pilar** | "E se…?" como **tipo de hook** (candidato à lista de 5) | Funciona em qualquer pilar (ex.: "e se a Terra fosse um cubo?" fecha o vídeo 001) |
| Voz gravada ou gerada, **música discreta**, imagens que ilustram | Voz Gemini, **sem música por enquanto**, visual todo em código, **efeitos sonoros por cena** | Gasto mínimo; música é um portão à parte |
| Métricas do **YouTube Studio** | Métricas do **TikTok Studio** (principal), Shorts e Reels (secundários) | Nosso objetivo é o TikTok; os nomes exatos das métricas dependem da conta |
| Estrutura de roteiro em 5 trechos de 0–35 s | Mesma lógica, esticada para 70–85 s, com **elos problema → solução** na revelação | Padrão do canal |
| Uma única "pele" implícita (um estilo de edição) | **Pele fixa no mês 1**, peles testadas uma por vez no mês 2 | Resolve o conflito entre "pele por tema" e "não mudar tudo ao mesmo tempo" |

## 3. O que não adotamos

- **Hashtags e título** só descritos de forma geral: o PDF não traz regra aproveitável; fica para o portão 8.
- **Gravar narração em ambiente silencioso**: usamos TTS. A decisão da voz do canal continua pendente.
- **Imagens que ilustram a história** (banco de imagens, cenas): nosso visual é código; imagem gerada só se nenhuma skill resolver.
- **Exemplos de pauta** (ilha proibida, a Terra parar de girar, buraco negro, falta de sono): ficam só como inspiração de formato; não entram no banco como decididos.

## 4. Riscos do plano do PDF que levamos a sério

1. **Amostra pequena:** 1 vídeo por combinação não prova nada; o plano admite isso e repete no mês 2.
2. **Mudança de variável sem registro:** toda mudança entre vídeos (hook, pele, duração) tem coluna própria na planilha.
3. **Dados sem idade:** sempre anotar a idade do vídeo no registro.
4. **Fatos:** a maior ameaça de um canal de curiosidades é publicar erro com cara de certeza. `checar.mjs` avisa quando a fonte ainda está pendente.
5. **Gargalo humano:** a produção é rápida; as decisões e as checagens não. Daí a rotina em lote.

## 5. O que o PDF não resolve (fica com a gente)

- Como **produzir 7 vídeos por semana com qualidade**: resolvido com o motor (`motor/novo.mjs`, `build.mjs`, `checar.mjs`).
- Como **medir a retenção de um vídeo longo de 70–85 s** contra o de 30–40 s: o PDF só compara vídeos de duração parecida, e nós mantemos a faixa.
- **Monetização no TikTok** (requisitos, originalidade, rótulo de IA): fica no `decisoes.md`; o PDF é de YouTube.
