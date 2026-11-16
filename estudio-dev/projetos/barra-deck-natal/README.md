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
1. vercel.com → Add New → Project → importar o repositório `Victor1Paim/Victor1Paim`.
2. **Root Directory**: `estudio-dev/projetos/barra-deck-natal` · Framework: **Other** · sem build.
3. Production Branch: `estudio-dev` (Settings → Git) ou fazer merge na branch principal.
