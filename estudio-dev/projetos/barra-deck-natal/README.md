# Barra Deck · Ceia de Natal 2026 (pré-pedido)

Site estático de pré-pedido. O cliente monta o carrinho e o pedido é enviado
**organizado para o WhatsApp (21) 98171-6022**. Não há pagamento no site.

## Editar
- **Cardápio, preços e prazo**: `assets/js/app.js` (topo do arquivo: `WHATSAPP`, `DEADLINE`, `MENU`).
- **Textos e avisos**: `index.html`.
- **Cores e fontes**: `assets/css/style.css` (variáveis em `:root`).
- **Datas de retirada/entrega** (23/12 e 24/12): `index.html`, campo "Data".

Depois de 10/12/2026 23:59 o site mostra "Encomendas encerradas" e esconde os botões.

## Rodar local
```bash
npx serve .
```

## Publicar na Vercel
No ar: **https://barra-deck-natal.vercel.app** (projeto `barra-deck-natal`, conta Vercel do Victor).

Para atualizar depois de editar (dentro desta pasta):
```bash
npx vercel login
```
```bash
npx vercel deploy --prod --yes
```
O login é por link de autorização (device code) e se perde quando a sessão na nuvem acaba.
`.vercelignore` impede que `.env*` e `.vercel` sejam publicados.
