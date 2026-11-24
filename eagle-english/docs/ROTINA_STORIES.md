# Rotina de stories · Eagle English (24/11/2026)

Stories são para quem JÁ segue: aprofundar, conversar e vender. 5 stories por dia, pedido (adesivo) no story 4.
Gerar: `posts/<data>_stories/stories.json` → `python3 scripts/montar_stories.py posts/<data>_stories` (story_1…5.png).
Modelos: `posts/2026-11-26_stories/` (CTA de produto) e `posts/2026-11-27_stories/` (CTA do quiz).

## A sequência do dia
| # | O que é | Adesivo (o usuário coloca no app) | Quando postar |
|---|---|---|---|
| 1 | Abertura com o personagem: "Bom dia! Sua dose de inglês de hoje 👇" (ou gancho da data) | — | manhã (8h–10h) |
| 2 | Frase do dia: situação → inglês (amarelo) → pronúncia (verde) → português (branco) → "fala em voz alta 3x" | — | manhã |
| 3 | Quiz: "Como se diz…?" com 3 opções | **QUIZ** (opções no stories.json) | manhã |
| 4 | O pedido: CTA do quiz OU CTA do produto (rodízio abaixo) | **LINK** | meio-dia |
| 5 | Resposta do quiz + o que sai hoje no feed (12h aula / 19h vídeo) | — | fim da tarde (antes das 19h) |

## Rodízio da semana (story 4)
| Dia | Story 4 | Link (adesivo) |
|---|---|---|
| seg | Quiz: "Por que o inglês ainda não pegou? Faz o teste de 1 minuto" | QUIZ |
| ter | Produto · mãe/pai: "Inglês de verdade pro seu filho nas férias, sem mensalidade cara" | OFERTA |
| qua | Quiz | QUIZ |
| qui | Produto · já tentou: "Já fez cursinho e não aprendeu? O problema foi o método" | OFERTA |
| sex | Quiz | QUIZ |
| sáb | Produto · viagem: "Vai viajar? Treine antes de ir: 10 aulas + 2.100 frases" | OFERTA |
| dom | Caixinha de perguntas: "Qual frase você quer aprender?" + produto · não só prova | CAIXINHA + OFERTA |

Links (com UTM para saber o que veio dos stories):
- QUIZ: `https://eagle-viagem.vercel.app/?utm_source=instagram&utm_medium=stories&utm_campaign=quiz`
- OFERTA: `https://eagle-viagem.vercel.app/oferta?utm_source=instagram&utm_medium=stories&utm_campaign=produto`
Texto do adesivo de link: "Fazer o teste 👇" (quiz) / "Ver o Eagle Primeira Classe" (oferta).

## Regras
- Inglês A1 (1 a 4 palavras), pronúncia no estilo simples, frases que não saíram no feed (ficam no "frases" do stories.json).
- Nada acima de y=250 nem abaixo de y=1600 de texto; o espaço do adesivo fica livre (div .vazio transparente).
- Sem preço, sem número inventado, sem marca de concorrente. "Pagamento único / sem mensalidade" pode.
- Respostas da caixinha e da enquete viram pauta (ganchos de vídeo e frases do Repita); quem responde no direct recebe resposta.
- Datas especiais mandam no story 1 (Thanksgiving, Black Friday, Natal, férias escolares → público mãe/pai).
