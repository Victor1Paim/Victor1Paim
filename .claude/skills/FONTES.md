# Origem das skills instaladas

Copiadas dos repositórios abaixo em 24/10/2026 (linhas novas: 28/10 e 08/11/2026, importadas de outros branches em 20/11/2026). Cada pasta traz a licença de origem em `LICENSE.origem`.
Para atualizar, clone o repositório de novo e copie a pasta da skill por cima.

| Repositório (commit) | Skills |
|---|---|
| heygen-com/hyperframes (`89081b9`) | hyperframes, hyperframes-cli, hyperframes-registry, media-use, remotion-to-hyperframes, motion-doctrine, captions-overlay, cut-the-curve, seam-craft |
| remotion-dev/remotion (`a64a027`) | remotion-best-practices, remotion-create, remotion-render, remotion-studio, remotion-captions, remotion-multimedia, remotion-docs, remotion-upgrade, remotion-markup, remotion-interactivity |
| calesthio/OpenMontage (`e01dbf4`) | openmontage (ponte para o submódulo `ferramentas/OpenMontage`), elevenlabs, text-to-speech, sound-effects, music, speech-to-text, ffmpeg, flux-best-practices |
| browser-use/browser-use (`3df5806`) | browser-use, open-source, qa |
| JuliusBrussee/caveman (`1f951fb`) | caveman, ultracave, caveman-commit, caveman-review, caveman-help, investigate-first, lean-build, surgical-patch, safe-refactor, verify-and-stop, migration |
| RobMitt/grill-me-skill (`31d61d6`) | grill-me |
| bangtutorial/bang-motion (`c1aa65e`) — 08/11/2026 | bang-motion (sem a ponte After Effects/Higgsfield: removidos `references/ae-bridge-higgsfield.md` e `scripts/ae/`) |
| Jakeschincariol/instagram-agent-skill (`d03c56b`) — 08/11/2026 | ig-reel, ig-caption, ig-carousel, ig-story, ig-plan, ig-viral, ig-audit, ig-profile, ig-human, ig-comment, ig-reply, ig-dm, ig-repurpose |
| openai/whisper (`8609812`) — 08/11/2026 | whisper-legendas (skill própria; o Whisper é instalado como pacote `openai-whisper` pelo `scripts/preparar-sessao.sh`) |
| lemomo-ai/lemo-opuscar (`413a6bd`) — 28/10/2026 | lemo-opuscar (`SKILL.md` e `scripts/setup.sh` do plugin; a biblioteca de 59 estilos é baixada por `setup.sh` em `~/lemo-opuscar`) |
| Vincentwei1021/mg-styles-15 (`49052d8`) — 28/10/2026 | mg-styles-15 (`SKILL.md` escrito aqui; prompts, rubrica, template e `harness/` copiados; demos de ~1 GB ficam de fora) |
| JohnHeibel/ClaudeAnimationBase (`0ac8bf2`) — 28/10/2026 | claude-animation-base (`SKILL.md` escrito aqui; guia, `src/`, `render.mjs` e fichas de modelo copiados) |
| debpalash/VoiceStudio (`ac821cb`) — 28/10/2026 | voicestudio (SKILL.md do repositório + "Notes for this repo"; licença AGPL-3.0; o app roda no computador do usuário) |
| cheaper-inference/OmniRoute (`a2b7934c`) — 28/10/2026 | omniroute (`SKILL.md` escrito aqui; 10 skills do repositório como referências em `references/`; o servidor não é copiado) |
| — (própria) — 29/10/2026 | gemini-midia (narração Gemini TTS e imagens Gemini; precisa de chave do Gemini) |

Deixadas de fora: skills internas de desenvolvimento de cada repositório, as que dependem de contas
de nuvem (Caveman Cloud, Browser Use Cloud, x402) e `remotion-saas`/`remotion-maps`.
O repositório `higgsfield-ai/higgsfield` não tem skills (é um framework de treino de LLM em GPU) e
o projeto não usa Higgsfield.

As skills `ig-*` guardam voz/plano/log em `~/.claude/instagram/`, que some na nuvem: copiar para o
repositório (pasta do canal/projeto) o que valer guardar.
