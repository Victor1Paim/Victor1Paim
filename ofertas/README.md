# Estúdio de Ofertas

Vertente de **criação de ofertas e páginas de vendas**: infoprodutos, serviços,
produtos físicos, lançamentos e campanhas sazonais. Branch: `estudio-ofertas`.

Herdado do `estudio-dev`: skills (`.claude/skills/`), memória (`estudio-dev/memoria/`)
e o projeto de referência do Barra Deck (`estudio-dev/projetos/barra-deck-natal/`).

## Como pedir
- "Cria uma oferta para o meu curso de X, público Y, preço Z."
- "Monta a página de vendas da oferta X."
- "Revisa a oferta e a página do projeto X."

O Claude segue a skill `criar-oferta`, nesta ordem:

| Etapa | O que sai | Arquivo |
|---|---|---|
| 1. Briefing | produto, público, preço, provas, prazo | `projetos/<slug>/briefing.md` |
| 2. Pesquisa | dores, desejos, objeções, vocabulário, concorrentes | `projetos/<slug>/pesquisa.md` |
| 3. Oferta | promessa, mecanismo, entregáveis, bônus, garantia, preço e ancoragem | `projetos/<slug>/oferta.md` |
| 4. Copy | headline, seções, FAQ, CTAs, microcopy | `projetos/<slug>/copy.md` |
| 5. Página | site no ar (Vercel) | `projetos/<slug>/pagina/` |
| 6. Divulgação | QR code, legendas, roteiro de reel | `projetos/<slug>/divulgacao/` |

## Modelos
| Modelo | Para quê |
|---|---|
| `modelos/briefing.md` | perguntas do primeiro contato |
| `modelos/oferta.md` | canvas da oferta |
| `modelos/copy-pagina.md` | estrutura da página de vendas |
| `modelos/checklist-lancamento.md` | o que conferir antes de publicar |

## Regras da casa
- Nada de prova, número, depoimento ou escassez inventados. O que faltar fica `[PREENCHER]`.
- Pesquisa de Reddit, X e redes: prompts prontos (skill `prompt-de-pesquisa`).
- Visual premium com as cores do cliente; copy passa pela skill `humanizer`.
- Mobile primeiro; site com proteção contra modo escuro forçado e cache versionado (ver `estudio-dev/memoria/aprendizados.md`).
