---
name: deploy-web
description: Publicar e colocar no ar páginas, sites e apps do Estúdio Dev — preview rápido, Vercel, Netlify, GitHub Pages, domínio próprio, variáveis de ambiente e checklist pré-lançamento.
---

# Deploy

## Preview rápido (dentro do chat)
- Página estática única → publicar como **Artifact** (link privado para o usuário ver/compartilhar).
- Projeto com servidor → `npm run dev` / `npm run preview` e informar a porta com `report_preview_port`.

## Produção (recomendação)
| Projeto | Onde |
|---|---|
| Landing/site estático | Vercel, Netlify ou GitHub Pages |
| Next.js | Vercel |
| App Expo | EAS (lojas) ou PWA na Vercel |

Fluxo: o usuário conecta o repositório GitHub na Vercel/Netlify (uma vez),
define **Root Directory** = `estudio-dev/projetos/<slug>` e as variáveis de
ambiente no painel. Cada push no branch gera deploy. Não peça tokens no chat.

## Domínio
Registro.br (.com.br) ou outro registrador → apontar DNS conforme o painel da
hospedagem (CNAME `www` + registro A/ALIAS na raiz).

## Checklist pré-lançamento
- [ ] Build sem erro, sem `console.error` na página
- [ ] Celular 390px e desktop OK, links e CTAs testados
- [ ] Pixels disparando (Meta Pixel Helper / Tag Assistant)
- [ ] SEO/OG (testar preview do link no WhatsApp)
- [ ] Favicon, 404, política de privacidade
- [ ] Segredos fora do repositório
