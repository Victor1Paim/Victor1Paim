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

A partir de 2027 a voz soma uns US$ 0,10 (piloto) a US$ 0,40 (coletânea). O que pesa no custo são as imagens.

## Como gastar menos

- Gerar a imagem em 1K e ampliar para 1920×1080 no computador (o grão e o desfoque do estilo escondem a perda).
- Um banco de planos coringa reaproveitável, que cresce a cada vídeo.
- Misturar com vídeo gratuito de banco (Pexels/Pixabay) nos planos de lugar comum (estrada, posto, céu).
- Sempre rodar em simulação antes (o script mostra o tamanho e se já tem cache) e testar 1 imagem antes do lote.
