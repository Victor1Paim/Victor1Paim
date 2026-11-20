---
name: omniroute
description: >
  Use an OmniRoute gateway (OpenAI-compatible endpoint that routes chat, images, TTS/STT and embeddings across
  many providers with fallback, free-tier pools, cache, prompt compression and spending limits). Use when the user
  has an OmniRoute server running and wants cheaper or routed model calls, a budget cap, usage and cost logs, or
  to configure providers and routing combos. Needs a running server; does nothing without one.
---

# OmniRoute (gateway de modelos para gastar menos)

OmniRoute é um **servidor** (github.com/diegosouzapw/OmniRoute, MIT) que fica entre os apps e os provedores de IA:
um endpoint compatível com OpenAI, roteamento com fallback, cache, compressão de prompt, limites de gasto e logs de uso.
Esta skill só ensina a usar um servidor que já esteja rodando. Os detalhes ficam em `references/` e são lidos sob demanda
(não estão na lista de skills, para não gastar contexto).

## Antes de usar

Precisa de:
- `OMNIROUTE_URL` (padrão do servidor local: `http://localhost:20128`) e `OMNIROUTE_KEY` (chave criada no painel do
  OmniRoute, em API Keys), como **variáveis de ambiente**. Nunca pedir nem aceitar chaves no chat, nunca gravá-las em
  arquivo do repositório.
- Verificar: `curl $OMNIROUTE_URL/api/health` deve responder `{"ok":true}`. Se não responder, **parar** e avisar que não há
  servidor: não inventar resultado e não instalar um segundo servidor.
- Uma sessão na nuvem não alcança o `localhost` do usuário; o servidor precisa estar num endereço acessível (com
  autenticação ligada) ou a sessão precisa ser local.

## Uso básico

```sh
curl $OMNIROUTE_URL/v1/models            # chat; também /v1/models/image, /tts, /stt, /embedding
curl $OMNIROUTE_URL/v1/chat/completions -H "Authorization: Bearer $OMNIROUTE_KEY" -H 'Content-Type: application/json' \
  -d '{"model":"<id de /v1/models>","messages":[{"role":"user","content":"..."}]}'
```

Usar sempre um `model` que apareça em `/v1/models*` (combos aparecem com `owned_by: "combo"`). Erros: `401` chave;
`400 Invalid model format` modelo inexistente; `503` provedor fora (respeitar `Retry-After`); `429` limite (idem).

## Referências (ler só a que a tarefa pede)

| Tarefa | Arquivo |
|---|---|
| Chat, imagens, TTS/STT, embeddings, Responses API | `references/omni-inference/INDEX.md` (+ `references/endpoints.md`, grande) |
| Modelos e apelidos disponíveis | `references/omni-models/INDEX.md` |
| Provedores e chaves deles | `references/omni-providers/INDEX.md` |
| Limite de gasto e de taxa | `references/omni-budget/INDEX.md` |
| Cache de respostas | `references/omni-cache/INDEX.md` |
| Compressão de prompt (RTK, Caveman) | `references/omni-compression/INDEX.md` |
| Combos de roteamento e fallback | `references/omni-combos-routing/INDEX.md` |
| Custo, tokens e logs de chamadas | `references/omni-usage-logs/INDEX.md` |
| Saúde, circuit breaker, latência | `references/omni-resilience/INDEX.md` |
| Autenticação e sessão | `references/omni-auth/INDEX.md` |

O repositório original tem mais 37 skills (CLI, túneis, backup, webhooks, MCP, A2A, avaliações). Não foram copiadas;
pedir ao usuário se alguma for necessária.

## Regras de custo e risco neste projeto

- **Ligar antes de rodar em lote:** limite de gasto por chave (`omni-budget`), cache (`omni-cache`) e conferir `omni-usage-logs`.
- **Provedores gratuitos são de terceiros.** Cada um tem seus limites e termos. O catálogo do OmniRoute marca alguns como
  `tos: avoid` (risco de violar termos); mantê-los desligados. Não ligar contas de assinatura pessoal (login OAuth de
  ferramentas de código) sem o usuário entender o risco para a conta.
- **Chaves:** quem guarda chaves de provedores no OmniRoute (por exemplo a do Gemini) torna o servidor um ponto sensível:
  autenticação ligada, painel fora da internet aberta.
- Para voz e imagem do canal, a skill `gemini-midia` (direta, com cache e simulação) é o caminho mais simples. O OmniRoute
  vale a pena para roteiro, pesquisa e revisão em texto com economia de tokens, ou se o usuário quiser um endpoint único.
- Licença MIT, copyright diegosouzapw (`LICENSE.origem`).
