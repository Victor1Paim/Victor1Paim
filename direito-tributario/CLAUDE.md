# Perfil de Direito Tributário (Isabela) — instruções para o Claude Code

Idioma: português do Brasil. Pasta local da Isabela; tudo roda aqui (sem servidor).

- Estratégia, regras de conteúdo e uso do kit: `GUIA-COMPLETO.md`. Processos e prompts: `SKILLS-E-PROMPTS.md`
  (S0 a S10) — siga a skill que corresponder ao pedido.
- Pesquisa base: `pesquisa/manus-2026-11-16/relatorio.md` (40 pautas, 60 dúvidas, calendário, reforma, boatos, OAB).
- Kit de vídeo: `python scripts/kit.py <novo|ler|preparar|render|tudo> <nome>` (no Mac/Linux: `python3`).
  Roteiro marcado em `videos/<nome>/roteiro.txt`; ajustes em `videos/<nome>/ajustes.json`.
  Antes de renderizar um vídeo novo, gere quadros de conferência: `cd video && node scripts/quadros.mjs kit <pasta> <quadros...>`
  e confira se nada cobre o rosto e nenhum cartão estoura.
- Regras que não mudam: afirmação jurídica só com fonte primária e data; dizer se é federal/estadual/municipal e se
  é vigente/aprovado/proposta; nada de conselho individual nem promessa de resultado; não apresentar a Isabela como
  advogada enquanto a inscrição na OAB não estiver confirmada no guia.
- A Isabela pode mudar processos: quando ela mudar um padrão, registre na seção 11 do `GUIA-COMPLETO.md`.
- Custos: o kit não usa API (Whisper e render locais). Se usar API paga (voz/imagem), registre com `scripts/custos.py`.
