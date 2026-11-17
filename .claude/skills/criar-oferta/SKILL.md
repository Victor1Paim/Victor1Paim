---
name: criar-oferta
description: Criar, estruturar ou revisar uma oferta comercial e sua página de vendas (infoproduto, serviço, produto físico, cardápio, campanha sazonal, lançamento). Conduz briefing → pesquisa → oferta → copy → página → divulgação em ofertas/projetos/<slug>/. Use quando o usuário pedir "oferta", "página de vendas", "landing", "lançamento", "funil" ou "campanha".
---

# Criar oferta

Trabalhe em `ofertas/projetos/<slug>/` (branch `estudio-ofertas`). Leia antes a memória
(`estudio-dev/memoria/`, skill `memoria`) e o `ofertas/README.md`.

## Fluxo
1. **Briefing** — copie `ofertas/modelos/briefing.md` para `briefing.md` e preencha com o
   que o usuário já disse. Pergunte no máximo 5 coisas que mudem o resultado.
2. **Pesquisa** — web aberta primeiro (cite fontes). Reddit, X e redes: entregue prompts
   prontos com a skill `prompt-de-pesquisa` e espere o usuário colar a resposta.
   Resumo em `pesquisa.md`: dores, desejos, objeções, vocabulário, concorrentes.
3. **Oferta** — preencha `oferta.md` a partir de `ofertas/modelos/oferta.md`.
   Mostre ao usuário a promessa, o preço/ancoragem e a garantia antes de escrever a página.
4. **Copy** — `copy.md` a partir de `ofertas/modelos/copy-pagina.md`, com 3 opções de
   headline por ângulo e uma recomendada. Passe pela skill `humanizer`.
5. **Página** — siga `pagina-de-vendas` + `dev-senior` (+ `ui-ux-pro-max`, `impeccable`).
   Projeto estático em `pagina/`, deploy com `deploy-web`. Reaproveite padrões do
   Barra Deck (`estudio-dev/projetos/barra-deck-natal/`): carrinho → WhatsApp,
   pop-up de PDF, QR code, textura, cache com `?v=`, proteção de modo escuro.
6. **Divulgação** (se pedido) — QR code, legendas, roteiro de reel.
7. **Checklist** — `ofertas/modelos/checklist-lancamento.md` antes de dizer "pronto".

## Regras
- Nunca inventar depoimento, número, prêmio, "chef", ingrediente premium, escassez ou
  garantia. O que faltar vira `[PREENCHER]` e entra na lista de perguntas.
- Urgência só se for real (prazo, capacidade, estoque).
- Quando o cliente manda material antigo e novo, confirme qual é a fonte da verdade.
- Registre decisões e aprendizados na memória ao final.
