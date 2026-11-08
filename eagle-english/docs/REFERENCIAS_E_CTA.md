# Referências de estilo, voz e CTA novo (08/11/2026)

## 1. As 4 referências e como adaptar ao nosso mascote

| # | Formato | Ritmo medido | Visual | Adaptação Eagle |
|---|---|---|---|---|
| R1 (72 s) | **Flashcard "What is this called?"**: imagem → contagem 3-2-1 → palavra + pronúncia | ~6 s/item (4 s pergunta+contagem, 2 s resposta), 12 itens; fecha "Let me know in the comments" | fundo lilás claro, cartão branco central, ilustração em aquarela, círculo de contagem, bandeira no topo | Cartão com ilustração do objeto/situação, pergunta falada em inglês, contagem, resposta amarela + pronúncia na nossa convenção (sem IPA) + tradução verde. Mascote pequeno ao lado do cartão "perguntando". Temas: objetos de uma situação do ebook (aeroporto, cozinha, farmácia…). |
| R2 (104 s → nosso 60–70 s) | **"Prova de Inglês" 1 a 10**: "Como se diz trabalho em inglês?" → pausa → a resposta entra na lista | ~6–9 s/item; frases de engajamento nos itens 3, 5 e 7 ("Se achou fácil…", "Compartilha com…", "Diz sua nota nos comentários") | céu noturno/estrada escura, etiqueta vermelha "Prova de Inglês", lista numerada branca, personagem à direita falando | Igual, com o mascote no lugar do boneco; lista com 8–10 itens; nossa pausa de 3 s; engajamento nos itens 3/5/7; nota final "Quantas você acertou?". Encurtar para caber em 70 s (8 itens). |
| R3 (16 s) | **Lista com emoji**: palavra em português → o inglês aparece embaixo | ~2 s/palavra, 8 palavras | pessoa falando + lista de emojis à esquerda | Lista com emoji à esquerda, mascote grande à direita falando; inglês aparece sob cada palavra; versão de 20–30 s (perfeita para teste de alcance). |
| R4 (36 s) | **"O que significa *I go*?"**: verbo amarelo + tradução verde | ~2,2 s/par, 9 pares; CTA "R$ 19,90 LINK NA BIO" | paisagem escura/dramática, personagem central | É o nosso padrão atual (`PADRAO_VIDEO.md`) — manter, com fundo mais "cinematográfico". |

Regras herdadas: mudança de cena a cada fala (corte seco), legenda curta e grande, nada de texto parado por mais de 3 s.
Para variar as poses do mascote (apontar, pensar, comemorar), gerar novas poses por edição a partir de
`assets/mascote/oficial/boca_fechada.png` (mesmo método do bico, `docs/PADRAO_VIDEO.md`).

## 2. Voz "mais locutora" e inglês no mesmo tom

**Em uso desde 08/11:** OpenAI `gpt-4o-mini-tts`, voz **onyx** nas duas línguas, com instrução de tom
(`INSTRUCOES` em `scripts/vozes.py`): locutor brasileiro grave e animado; em inglês, mesma voz, americano
claro e um pouco mais devagar. Sem limite diário (o Gemini gratuito só dá 10 falas/dia por modelo).
No `falas.json`: `"modelo": "gpt-4o-mini-tts", "vozes": {"pt": "onyx", "en": "onyx"}`. Produto: "Eagle trezentos e cinquenta".
Conferir no Whisper que a última fala do CTA termina em "Link na bio" (a voz às vezes corta o final).

(Plano anterior com o Gemini, mantido como alternativa:)

- Usar **a mesma voz do Gemini nas duas línguas** (arquivos separados): o inglês sai com o mesmo timbre do
  narrador, em vez de outra pessoa. Candidatas de locutor: **Charon** (informativa), **Orus** (firme),
  **Sadaltager** (de quem sabe) e **Alnilam** (firme). Teste: 1 frase pt + 1 frase en de cada, escolher de ouvido.
- Nos modelos 2.5 dá para pedir o tom ("Say like an energetic radio announcer: …"); nos 3.x não (leem a instrução).
- **Whisper em todo vídeo:** `vozes.py gerar` sem `--sem-conferir` (confere cada fala, regenera se < 95%)
  + transcrição do `final.mp4` antes de entregar. O nome do produto se escreve "Ígol trezentos e cinquenta".
- Quando estiver pronto, a oferta antiga com a voz original (`fechamento_oferta.mp4`) sai de uso: o fechamento
  passa a ser narrado com a mesma voz do vídeo (seção 3).

## 3. CTA novo (fatos da página de vendas — eagle-pagina.vercel.app, config de 08/11)

Fatos confirmados: "Ache a frase certa em inglês para cada situação — sem travar na hora." · 35 situações,
350 mapas, 2.100 frases, cada uma com tradução e pronúncia escrita · sumário clicável · celular, tablet,
computador ou impresso · **Ebook + 4 bônus**: Guia de 21 Dias (15 min/dia), 20 Cards de Gramática
(120 frases), 500 Frases para o Dia a Dia (seleção do ebook), 100 Combinações de Verbos (40 exercícios com
gabarito) · valores individuais 37 + 27 + 19,90 + 19,90 + 19,90 = **R$ 123,70** · **R$ 19,90, pagamento único** ·
PDFs por e-mail após a confirmação · **garantia incondicional de 7 dias** · oferta com prazo real **até 25/12/2026**.
Não citar: áudio, aulas, professor, fluência garantida, depoimentos (a página ainda não tem).

O que estava "perdido" no fechamento antigo: não dizia a promessa, não ligava as frases do vídeo ao produto,
falava "Guia" + "3 bônus" (a página fala "4 bônus") e a voz mudava no fim.

**Estrutura nova (12–15 s, mesma voz do vídeo, mascote pequeno no canto):**

| Tela | Texto na tela | Fala |
|---|---|---|
| Mapa real do tema | "Essas frases estão **aqui** 👇" + página do mapa | "Essas frases estão num mapa do Eagle 350." |
| Sumário | "**35 situações** no sumário" + sumário | "São 35 situações e 2.100 frases, com tradução e pronúncia escrita: você acha a situação e já fala." |
| Kit | "Ebook + **4 bônus**" + 5 capas + lista | "E vem com 4 bônus, como o Guia de 21 dias, de 15 minutos por dia." |
| Preço | "Separado: ~~R$ 123,70~~" · "**R$ 19,90**" · PDF no e-mail · Garantia de 7 dias · Oferta até 25/12 · "Link na bio 👆" | "Separado, daria 123 e 70. Hoje, o kit completo sai por 19 e 90, pagamento único, com 7 dias de garantia. Link na bio!" |

- O vídeo passa a ensinar **frases de um mapa real** do ebook (temos em alta: aeroporto, saúde, trabalho,
  namoro, emergências, telefone, phrasal verbs, contrações e pronúncia difícil — `assets/marca/paginas/site/`),
  então "essas frases estão aqui" é verdade e funciona como prova.
- Legenda e comentário fixado seguem o mesmo texto (seção 12 das instruções + preço da página).
- Depois de 25/12, trocar o prazo (ou tirar a linha "Oferta até 25/12").

## 4. Ordem para recriar (um por vez)

Cada vídeo: ideia → gancho → roteiro com tempos → imagem de fundo → estilo (R1–R4) → vozes conferidas → montagem → capa → legenda.
Sugestão de início: **R4 com o mapa "Atender o telefone"** (frases reais do mapa, fecha com o CTA novo).
