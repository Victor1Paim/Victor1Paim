---
name: site-e-app
description: Criar site institucional, portfólio, blog, web app, SaaS, painel administrativo, PWA ou app mobile (Expo). Define arquitetura, scaffolding, estrutura de pastas, auth e banco. Use junto com dev-senior.
---

# Sites e apps

## Site (Astro + Tailwind)
```bash
npm create astro@latest <slug> -- --template minimal --typescript strict --no-git --install
npx astro add tailwind --yes
```
- `src/layouts/Base.astro` com SEO (title, description, OG) e `lang="pt-BR"`.
- Páginas em `src/pages/`, componentes em `src/components/`, conteúdo em `src/content/`.
- Formulário de contato: Formspree/Web3Forms ou link de WhatsApp (`wa.me`).

## Web app (Next.js + Supabase)
```bash
npx create-next-app@latest <slug> --ts --tailwind --eslint --app --src-dir --use-npm --no-git
npx shadcn@latest init -d
```
- Estrutura: `src/app/(publico)`, `src/app/(app)` protegido por middleware,
  `src/lib/supabase/{client,server}.ts`, `src/components/ui` (shadcn).
- Banco: migrações SQL versionadas em `supabase/migrations/`, **RLS ligado em toda tabela**.
- Server Actions/Route Handlers para escrita; validar entrada com `zod`.
- Estados de carregando, vazio e erro em toda tela.
- Sem chave Supabase? Rode com dados mock e deixe `.env.example` pronto.

## App mobile (Expo)
```bash
npx create-expo-app@latest <slug> --template tabs
```
- Expo Router, TypeScript, navegação por abas; testar no Expo Go do celular.
- Publicação nas lojas via EAS Build (exige contas Apple/Google — avisar custos).
- Se não precisa de loja nem recurso nativo: prefira **PWA** no Next.js.

## Sempre
- Rodar `npm run build` e `npm run lint` antes de dizer que está pronto.
- Screenshot em celular e desktop (Playwright já instalado no ambiente).
- `README.md` do projeto: rodar, variáveis, deploy.
