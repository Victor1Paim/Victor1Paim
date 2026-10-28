# Origem das skills instaladas

Copiadas dos repositórios abaixo em 24/10/2026 (as três últimas linhas, em 28/10/2026, na branch `claude/desvendando-ideias`). Cada pasta traz a licença de origem em `LICENSE.origem`.
Para atualizar, clone o repositório de novo e copie a pasta da skill por cima.

| Repositório (commit) | Skills |
|---|---|
| heygen-com/hyperframes (`89081b9`) | hyperframes, hyperframes-cli, hyperframes-registry, media-use, remotion-to-hyperframes, motion-doctrine, captions-overlay, cut-the-curve, seam-craft |
| remotion-dev/remotion (`a64a027`) | remotion-best-practices, remotion-create, remotion-render, remotion-studio, remotion-captions, remotion-multimedia, remotion-docs, remotion-upgrade, remotion-markup, remotion-interactivity |
| calesthio/OpenMontage (`e01dbf4`) | openmontage (ponte para o submódulo `ferramentas/OpenMontage`), elevenlabs, text-to-speech, sound-effects, music, speech-to-text, ffmpeg, flux-best-practices |
| browser-use/browser-use (`3df5806`) | browser-use, open-source, qa |
| JuliusBrussee/caveman (`1f951fb`) | caveman, ultracave, caveman-commit, caveman-review, caveman-help, investigate-first, lean-build, surgical-patch, safe-refactor, verify-and-stop, migration |
| RobMitt/grill-me-skill (`31d61d6`) | grill-me |
| lemomo-ai/lemo-opuscar (`413a6bd`) | lemo-opuscar (`SKILL.md` e `scripts/setup.sh` do plugin; a biblioteca de 59 estilos é baixada por `setup.sh` em `~/lemo-opuscar`, clone esparso da `main`) |
| Vincentwei1021/mg-styles-15 (`49052d8`) | mg-styles-15 (repositório não é skill: `SKILL.md` escrito aqui; prompts, rubrica, template e `harness/` copiados; demos de ~1 GB ficam de fora) |
| JohnHeibel/ClaudeAnimationBase (`0ac8bf2`) | claude-animation-base (repositório não é skill: `SKILL.md` escrito aqui; guia, `src/`, `render.mjs` e fichas de modelo copiados) |
| debpalash/VoiceStudio (`ac821cb`) | voicestudio (`skills/voicestudio/SKILL.md` do repositório, mais uma seção "Notes for this repo" no fim; licença AGPL-3.0, o aplicativo não é copiado: roda no computador do usuário) |

Deixadas de fora: skills internas de desenvolvimento de cada repositório, as que dependem de contas
de nuvem (Caveman Cloud, Browser Use Cloud, x402) e `remotion-saas`/`remotion-maps`.
O repositório `higgsfield-ai/higgsfield` não tem skills (é um framework de treino de LLM em GPU) e
o projeto não usa Higgsfield.
