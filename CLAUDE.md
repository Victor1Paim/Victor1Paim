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
- Idioma de trabalho com o usuário: português do Brasil.
