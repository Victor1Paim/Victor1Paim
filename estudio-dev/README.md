# Estúdio Dev

Área de criação de **páginas de vendas, sites e apps**. Independente do Halftone
e do Desvendando Ideias. Branch de trabalho: `estudio-dev`.

## Como pedir
Escreva no chat algo como:
- "Cria uma página de vendas para meu curso X, preço R$ 197, checkout na Kiwify."
- "Quero um site para uma clínica, 5 páginas, com WhatsApp."
- "Faz um app de agendamento com login e painel do dono."

O Claude segue a skill `dev-senior`: briefing curto → plano → build → QA → deploy.

## Skills
| Skill | Para quê |
|---|---|
| `dev-senior` | Fluxo, stack padrão e régua de qualidade |
| `pagina-de-vendas` | Estrutura, copy e conversão de landing/vendas |
| `site-e-app` | Sites (Astro), web apps (Next.js + Supabase), mobile (Expo) |
| `deploy-web` | Preview, Vercel/Netlify, domínio, checklist |
| `qa` | Nota de qualidade 1–5 testando no navegador |

## Estrutura
```
estudio-dev/
  README.md
  projetos/
    <slug-do-projeto>/   ← um projeto por pasta, cada um com seu README
```
