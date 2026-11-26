# Custos por produção (Gemini + OpenAI)

Preços da página oficial (aistudio.google.com/docs/pricing), lidos em 26/11/2026, em dólar, plano pago "Standard".
**Atenção:** os modelos de voz 3.8 dobram de preço em 01/01/2027.
O gasto real de cada vídeo sai do log da skill: `node .claude/skills/gemini-midia/scripts/gemini.mjs usage`.

## Preços usados

| Item | Modelo | Preço |
|---|---|---|
| Voz | `gemini-3.8-flash-tts` | US$ 9 por 1 milhão de tokens de áudio (25 tokens = 1 s) → **US$ 0,0135 por minuto** (US$ 0,027 a partir de 2027) |
| Voz (mais barata) | `gemini-3.8-flash-lite-tts` | US$ 0,009/min (0,018 em 2027) |
| Imagem barata | `gemini-3.1-flash-lite-image` (Nano Banana 2 Lite) | US$ 0,034 por imagem 1K |
| Imagem padrão | `gemini-3.1-flash-image` (Nano Banana 2) | US$ 0,067 (1K) · US$ 0,101 (2K) |
| Imagem top | `gemini-3-pro-image` (Nano Banana Pro) | US$ 0,134 (1K/2K) |
| Legenda | OpenAI `whisper-1` | US$ 0,006 por minuto |
| Trilha, sting, efeitos | biblioteca livre | US$ 0 |

**Medido no teste de voz (26/11):** 3 vozes × 28 s = 2.070 tokens de áudio = **US$ 0,019**. Bate com a conta (25 tokens/s).

## Premissas

- Uma imagem a cada ~20 s de narração (as referências trocam a cada 13–38 s), mais 30% de margem para refazer.
- Voz: uma passada completa e mais 30% de margem para refazer trechos.
- Planos coringa (lua, estrada, janela) e a vinheta são gerados uma vez e reaproveitados nos vídeos seguintes.

## Estimativa por produção (US$)

| | Piloto: 1 história, ~7 min | Coletânea: 3–4 histórias, ~25 min | Short vertical (corte de 60 s) |
|---|---|---|---|
| Voz (3.8 Flash, com margem) | 0,12 | 0,44 | 0 (reaproveita a voz do longo) |
| Imagens: quantidade | ~28 | ~95 | ~3 novas em 9:16 |
| — com Nano Banana 2 Lite | 0,95 | 3,20 | 0,10 |
| — com Nano Banana 2, 1K | 1,90 | 6,40 | 0,20 |
| — com Nano Banana 2, 2K | 2,85 | 9,60 | 0,30 |
| — com Nano Banana Pro | 3,75 | 12,75 | 0,40 |
| Miniatura (3 opções, Nano Banana 2 em 2K) | 0,30 | 0,30 | — |
| Legenda (Whisper) | 0,05 | 0,15 | 0,01 |
| **Total, opção recomendada (Nano Banana 2 em 1K + ampliação local)** | **≈ US$ 2,40** | **≈ US$ 7,30** | **≈ US$ 0,20** |
| Total mínimo (Lite) | ≈ US$ 1,40 | ≈ US$ 4,10 | ≈ US$ 0,10 |
| Total máximo (Pro) | ≈ US$ 4,20 | ≈ US$ 13,60 | ≈ US$ 0,40 |

## Imagens pela OpenAI (chave já conectada)

Preço oficial do `gpt-image-2`: US$ 30 por 1 milhão de tokens de imagem gerada (developers.openai.com/api/docs/pricing).
**Medido em 26/11:** 1 imagem 1536×1024, qualidade *medium* = 1.372 tokens = **US$ 0,042**. A mesma cena no Gemini Nano Banana 2
(1376×768) deu 1.639 tokens de saída ≈ **US$ 0,07–0,10** (o log não separa imagem de "raciocínio").
Comparação lado a lado: `producoes/piloto/teste-imagem/comparacao.jpg` (esquerda OpenAI, direita Gemini).

| | Piloto (~28 imagens) | Coletânea (~95) | Short (~3) |
|---|---|---|---|
| gpt-image-2 *low* (≈ US$ 0,005/imagem, não testado) | 0,15 | 0,50 | 0,02 |
| gpt-image-2 *medium* (US$ 0,042, medido) | 1,20 | 4,00 | 0,13 |
| gpt-image-2 *high* (≈ US$ 0,165, não testado) | 4,60 | 15,70 | 0,50 |

**Total com OpenAI medium nas imagens + voz Gemini + Whisper + 3 miniaturas em high:**
**piloto ≈ US$ 1,90 · coletânea ≈ US$ 5,10 · short ≈ US$ 0,15.** É a opção mais barata com qualidade boa.
O formato 1536×1024 é 3:2: corta-se para 16:9 e amplia-se para 1920×1080 localmente.

A partir de 2027 a voz soma uns US$ 0,10 (piloto) a US$ 0,40 (coletânea). O que pesa no custo são as imagens.

## Como gastar menos

- Gerar a imagem em 1K e ampliar para 1920×1080 no computador (o grão e o desfoque do estilo escondem a perda).
- Um banco de planos coringa reaproveitável, que cresce a cada vídeo.
- Misturar com vídeo gratuito de banco (Pexels/Pixabay) nos planos de lugar comum (estrada, posto, céu).
- Sempre rodar em simulação antes (o script mostra o tamanho e se já tem cache) e testar 1 imagem antes do lote.

## Gasto real do piloto "The Detour" (26/11/2026)

| Item | Quantidade | US$ |
|---|---|---|
| Voz Gemini 3.8 Flash TTS (Enceladus) | 22 parágrafos, 9.967 tokens de áudio, 6,6 min | 0,09 |
| Imagens OpenAI gpt-image-2 medium | 30 (inclui 1 refeita) | 1,25 |
| Miniatura OpenAI gpt-image-2 high | 1 | 0,17 |
| Legenda Whisper | 6,6 min | 0,04 |
| Trilha e efeitos | sintetizados aqui | 0 |
| **Total do piloto** | | **≈ US$ 1,55** |
| Testes antes do piloto (3 vozes, 2 imagens de comparação) | | ≈ 0,15 |
| Análise das 3 referências (Whisper, 87 min) | uma vez | ≈ 0,52 |

Ficou abaixo da estimativa (US$ 1,90): a história rendeu 30 imagens em vez das 28 + margem, e quase nada precisou ser refeito.

## Gasto real — Coletânea 01 e Short 01 (26/11/2026)

### Coletânea 01 "3 Disturbing Road Trip Stories" (19 min 12 s)

| Onde | Detalhe | US$ |
|---|---|---|
| Voz — Gemini 3.8 Flash TTS | Story 1 (reaproveitada do piloto) 0,09 + Story 2 0,09 + Story 3 0,08 | 0,26 |
| Imagens — OpenAI gpt-image-2 medium | Story 1: 30 (do piloto) 1,25 · Story 2: 23 = 0,96 · Story 3: 21 = 0,87 · vinheta 0,04 | 3,12 |
| Miniatura — OpenAI gpt-image-2 high | 1 imagem | 0,17 |
| Legenda — OpenAI Whisper | 18,4 min de narração (mais refações) | 0,15 |
| Trilha, sting, cartelas, montagem | feitos aqui | 0 |
| **Total da coletânea** | | **≈ US$ 3,70** |
| Só o que foi novo (Story 1 já estava paga no piloto) | | ≈ US$ 2,25 |

### Short 01 (1 min 39 s)

| Onde | Detalhe | US$ |
|---|---|---|
| Voz nova (gancho + chamada) — Gemini | 2 trechos, ~12 s | 0,003 |
| Narração do meio | reaproveitada da Story 2 | 0 |
| Imagens verticais — OpenAI medium | 8 | 0,33 |
| Legenda — Whisper | 3 passadas de 1,7 min | 0,03 |
| Capa | feita aqui a partir de uma imagem do Short | 0 |
| **Total do Short** | | **≈ US$ 0,37** |

Obs.: as chaves do Gemini usadas parecem ser do nível gratuito (limite de 100 pedidos/dia por modelo). Se forem, a voz
saiu de graça e os valores de voz acima são o que custaria no nível pago. Teste do ElevenLabs (1 efeito de 1,5 s): créditos mínimos.
