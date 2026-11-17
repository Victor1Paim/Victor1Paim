# Decisões

| Data | Decisão | Motivo |
|---|---|---|
| 2026-11-17 | Criado o branch `estudio-ofertas` (a partir do `estudio-dev`) para ofertas e páginas de vendas; pasta `ofertas/`, skill `criar-oferta` | Pedido do usuário |
| 2026-11-16 | Barra Deck: formulário espelha a comanda de papel (cliente, telefone, recebimento, data, horário, endereço em campos, ponto de referência); só nome e telefone obrigatórios; botão de envio verde WhatsApp #1A9E57 | Pedido do usuário (foto da comanda) |
| 2026-11-16 | Barra Deck: **seguir exatamente o PDF 2026** (`Ceia_de_Natal_2026_Barra_Deck.pdf`); principais SEM acompanhamento. Revertido o acréscimo do cardápio antigo | Usuário pediu explicitamente |
| 2026-11-16 | Barra Deck: nova copy ("O fogão é nosso. A noite é sua.", CTA "Montar minha ceia", fechamento "Sabor de casa, capricho de restaurante") + seção Dúvidas | Pesquisa de copy do usuário; só fatos confirmados (sem chefs, kits por pessoa, aquecimento) |
| 2026-11-16 | Barra Deck: acompanhamentos dos principais vindos do cardápio anterior (lombo, maminha, tender, bacalhaus, chester, pernil); preços/pesos/itens de 2026 mantidos | Pedido do usuário; o PDF 2026 dizia "sem acompanhamento" |
| 2026-11-16 | Barra Deck publicado via Vercel CLI (sem integração GitHub) | Conta Vercel sem conexão GitHub; login por autorização do usuário |
| 2026-11-16 | Barra Deck: site estático (HTML/CSS/JS, sem build) na Vercel | Página única; deploy e manutenção mais simples |
| 2026-11-16 | Barra Deck: pedido → WhatsApp (21) 98171-6022, sem pagamento; entrega/taxa sob consulta | Pedido do cliente |
| 2026-11-16 | Memória em `estudio-dev/memoria/` em vez do claude-mem | claude-mem guarda em `~/.claude-mem`, apagado ao fim da sessão na nuvem; exige conta |
| 2026-11-13 | Pesquisa de Reddit/X via prompts para o usuário colar fora | Reddit bloqueia o servidor (403) e a busca; chaves não cadastradas |
| 2026-11-13 | Skills de terceiros instaladas (ver `.claude/skills/TERCEIROS.md`) | Pedido do usuário |
| 2026-11-13 | Stack padrão: Astro (páginas/sites), Next.js + Supabase (apps), Expo (mobile) | Rápido, barato de hospedar, ecossistema maduro |
| 2026-11-13 | Estúdio Dev em branch separado `estudio-dev` | Pedido do usuário |
