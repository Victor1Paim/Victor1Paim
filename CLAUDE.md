# Halftone

Canal de séries em capítulos (@halftone.tv1). Série atual: **Ano Zero · T1 A Virada**.

- Projeto de vídeo (Remotion): `halftone/` — leia `halftone/README.md`.
- Bíblia: `halftone/series/ano-zero/biblia.md` · Plano-mestre: `halftone/docs/plano-mestre-novela-tiktok.md`.
- Geração de mídia (placas, vozes, música): skill `openmontage` → submódulo `ferramentas/OpenMontage`.
- Montagem: Remotion em `halftone/`; HyperFrames (skills `hyperframes*`) quando pedido.
- Não usar Higgsfield.
- Sessão nova: rodar `scripts/preparar-sessao.sh` (submódulo + npm ci + pip).
- Antes de entregar um episódio: `cd halftone && npm run checar -- series/ano-zero/t1/epNN/ep.json`.
- Segundo canal: **Desvendando Ideias** (@desvendandoideias.ofc) — curiosidades/ciência/mistérios, curtos e longos. Pasta `desvendando-ideias/` — leia `desvendando-ideias/plano-do-canal.md`. Independente do Halftone.
- Terceiro projeto: **Eagle English BR** (@eagle.english.br) — vídeos de inglês para brasileiros (carrosséis no ChatGPT). Pasta `eagle-english/` — leia `eagle-english/README.md` e `eagle-english/CLAUDE.md`. Independente do Halftone.
- Quarto projeto (teste): **Direito Tributário** — tela dividida + motion em estilo cartum. Pasta `direito-tributario/` — leia `direito-tributario/README.md`. Independente do Halftone.
- **Custo de API em todo post:** toda geração com chave de API (Gemini, OpenAI, xAI…) registra tokens e custo em `<pasta do post>/custos.jsonl` via `scripts/custos.py` (preços em `scripts/precos-api.json`). Ao terminar a criação de cada post, SEMPRE rodar `python3 scripts/custos.py relatorio <pasta do post>` e mostrar a tabela de custo estimado (US$ e R$) ao usuário no fim da resposta. Whisper, ffmpeg e render local são grátis.
- Idioma de trabalho com o usuário: português do Brasil.
