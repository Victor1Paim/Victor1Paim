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
- Terceiro canal: **Saúde sem Sermão** (@saudesemsermao) — saúde e hábitos explicados sem bronca, com fonte. Pasta `saude-sem-sermao/` — leia `saude-sem-sermao/plano-do-canal.md`. Independente dos outros canais.
- **Custo de API em todo post:** toda geração com chave de API (Gemini, OpenAI, xAI…) registra tokens e custo em `<pasta do post>/custos.jsonl` via `scripts/custos.py` (preços em `scripts/precos-api.json`). Ao terminar a criação de cada post, SEMPRE rodar `python3 scripts/custos.py relatorio <pasta do post>` e mostrar a tabela de custo estimado (US$ e R$) ao usuário no fim da resposta. Chamadas feitas fora dos scripts também entram no relatório (registrar com `registrar(...)`). Whisper, ffmpeg e render local são grátis.
- **Cronograma do Saúde sem Sermão** (`saude-sem-sermao/pautas/cronograma-producao.md`): sempre que o usuário pedir o cronograma atual, mostrar a cor de risco (🟢 🟡 🔴) ao lado de cada tema, e marcar o que já foi produzido.
- Idioma de trabalho com o usuário: português do Brasil.
