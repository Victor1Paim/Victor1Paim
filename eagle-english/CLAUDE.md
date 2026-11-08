# Eagle English BR – Produção de vídeos

Você produz vídeos curtos (Reels/TikTok) para @eagle.english.br. Regras de conteúdo,
identidade, pronúncia e CTA de produto: `docs/EAGLE_ENGLISH_PROJETO_COMPLETO.md`
(PARTE 4, seções 2, 6 e 12). Estado atual da fila: `docs/estado.md`.
Passo a passo do projeto (quem faz o quê): `docs/PASSO_A_PASSO_EAGLE_ENGLISH.md` (seção 2).

Idioma de trabalho com o usuário: português do Brasil, direto e curto.

## Sempre

- Formato 1080x1920 (9:16), 30 fps, H.264 + AAC, até 60 s (ideal 20–45 s).
- Gancho nos 2 primeiros segundos (falado + texto na tela).
- Textos na tela renderizados a partir de templates HTML (`templates/`, via
  `scripts/render_cartoes.py`): texto exato, acentos certos, nunca escritos por gerador de imagem.
- Área segura: nada importante nos 250 px de cima, nos 400 px de baixo
  nem nos 150 px da direita (interface do TikTok/Reels).
- Narração em pt-BR; frases em inglês com voz americana (arquivo separado).
- Música a 10–15% do volume da voz; loudness final perto de -14 LUFS.
- Final obrigatório (seção 12.3): CTA falado de 5 a 8 s + texto na tela de no máximo 2 linhas
  ("Eagle 350: 350 mapas + 4 bônus | Link na bio").
- Entregar junto: `roteiro.md`, `legenda.md` (legenda terminando no bloco de CTA),
  comentário fixado e resposta curta para "eu quero".
- Fechar a entrega com "CTA incluído: sim" + checklist 12.7.
- Nunca: áudio do ebook, "grátis", preço sem pedido, urgência falsa, promessa de fluência,
  marcas reais, link escrito (sempre "link na bio").

## Frases

As frases vêm do ChatGPT (chat central) em `posts/AAAA-MM-DD_tema/frases.json`.
Não invente frases novas: só produza o vídeo das frases aprovadas. Pronúncia na convenção
da seção 6 (tônica em MAIÚSCULA, sem IPA).

## Ciclo de um vídeo (seção 2.5 do passo a passo)

1. `roteiro.md` com tempos e fala por cena (incluindo o CTA final).
2. Narração pt-BR + frases em inglês (voz americana), um arquivo por cena em `audio/`
   (Fish Audio pela API com a chave em `.env`, ou arquivos soltos pelo usuário).
3. Medir durações (`silencedetect`) e montar a linha do tempo (`adelay` + `amix`).
4. Renderizar os cartões HTML em PNG (`scripts/render_cartoes.py`).
5. Montar o vídeo com ffmpeg: fundo, cartões, mascote discreto, música baixa e efeitos.
6. Gerar `.srt` a partir do roteiro (e queimar na tela, se pedido).
7. Tela final de produto + CTA falado.
8. Exportar `video/final.mp4` + folha de contato (1 quadro por cena).
9. `legenda.md`: legenda + bloco de CTA + comentário fixado + resposta curta.
10. "CTA incluído: sim" + checklist.

## Lições técnicas (seção 6 do passo a passo)

- Rodar ffmpeg com `-nostdin` em loops e arredondar os tempos ("Invalid duration").
- Congelar 0,7 s antes de cada transição para evitar quadro preto.
- Voz pt-BR lê inglês errado: frases em inglês sempre em arquivo separado, voz americana.

## Ambiente

- Ferramentas: ffmpeg, Python (Pillow, pydub/numpy), Playwright/Chromium.
- Preparar no notebook: `bash scripts/preparar.sh`.
- A chave do Fish Audio fica em `.env` (`FISH_AUDIO_API_KEY`), nunca no chat nem no git.
