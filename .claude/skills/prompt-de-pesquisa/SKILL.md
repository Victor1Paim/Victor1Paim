---
name: prompt-de-pesquisa
description: Gerar prompts de pesquisa prontos para o usuário colar em outra ferramenta (Grok, ChatGPT, Perplexity, Gemini, busca do Google) quando a fonte necessária não é acessível daqui — Reddit, X/Twitter, Instagram, TikTok, grupos, sites com login. Use sempre que uma pesquisa precisar dessas fontes ou quando o usuário pedir "prompt de pesquisa".
---

# Prompt de pesquisa

## O que dá para acessar daqui
- **Web aberta**: busca na web (WebSearch) e leitura de páginas — usar primeiro.
- **Google Drive/Gmail/Agenda do usuário**: via conectores, quando ele pedir.
- **Não acessível**: Reddit (bloqueado para a busca e para este servidor), X/Twitter,
  Instagram, TikTok, Facebook, conteúdo com login. Para isso → gerar prompt.

## Fluxo
1. Pesquisar o que der na web aberta e citar fontes.
2. Para o que faltar, entregar **1 prompt por ferramenta**, em bloco de código, pronto para colar:
   - **Grok** (melhor para X/Twitter), **Perplexity** ou **ChatGPT com busca** (Reddit, fóruns),
   - **Google**: lista de buscas com operadores (`site:reddit.com`, `"frase exata"`, `after:2026-10-01`).
3. Pedir que o usuário cole a resposta aqui; então sintetizar e aplicar no projeto.

## Modelo de prompt
```
Você é um pesquisador de mercado. Pesquise em <FONTE> o que as pessoas disseram nos
últimos <N> dias sobre <TEMA/NICHO>, em português e inglês.
Quero:
1. As 10 dores/reclamações mais repetidas, com frases literais e link do post.
2. Desejos e objeções de compra (o que fariam alguém comprar ou desistir).
3. Palavras e expressões que o público usa (vocabulário para copy).
4. Concorrentes/produtos citados e o que elogiam ou criticam.
5. Tendências ou assuntos em alta.
Responda em português, em tópicos, com links. Não invente: se não achar, diga.
```
Adaptar: para página de vendas, foco em dores/objeções/vocabulário; para app, foco em
funcionalidades pedidas e reclamações de concorrentes.
