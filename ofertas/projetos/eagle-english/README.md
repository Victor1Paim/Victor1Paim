# Eagle English — site novo (quiz + 2 planos)

- `pagina/index.html` — quiz de 6 perguntas (link da bio). Resultado → `oferta.html?perfil=&destino=&medo=` (UTMs repassados).
- `pagina/oferta.html` — página com os 2 planos. Tudo que muda (nomes, preços, checkouts, e-mail, promoção) fica em `pagina/config.js`.
- Ver pendências: abrir `oferta.html?dev=1`.
- `copy.md` (quiz + copy + decisões) e `criativos.md` (3 criativos de teste) — cópias de `eagle-english/docs/` (branch eagle-english).

## Decisões (22/11)
- 2 infoprodutos separados na Kiwify: Simples (Eagle 350 + 500 Frases, R$ 14,90) e Avançado (10 itens, R$ 37; R$ 29,90 nas 100 primeiras vendas).
- Ao bater 100 vendas: preço R$ 37 na Kiwify + `lancamento: false` no config.js.
- Sem contador de tempo; sem depoimento ou número inventado.

## Pendente
- Nomes dos planos (provisórios: Eagle Bagagem de Mão × Eagle Primeira Classe).
- Links de checkout, e-mail, bloco "Quem criou".
- Produzir antes de vender o Avançado: 10 aulas (ou `aulasLiberadasEm`), Mapas Mentais, áudio, cola de viagem, checklist.
- NO AR (22/11): https://eagle-viagem.vercel.app (quiz, link da bio) · https://eagle-viagem.vercel.app/oferta (vendas). Redeploy: `vercel deploy --prod --yes` dentro de pagina/ (config.privado.js precisa existir localmente).
