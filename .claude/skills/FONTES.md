# Origem das skills instaladas

Copiadas dos repositórios abaixo em 24/10/2026. Cada pasta traz a licença de origem em `LICENSE.origem`.
Para atualizar, clone o repositório de novo e copie a pasta da skill por cima.

| Repositório (commit) | Skills |
|---|---|
| heygen-com/hyperframes (`89081b9`) | hyperframes, hyperframes-cli, hyperframes-registry, media-use, remotion-to-hyperframes, motion-doctrine, captions-overlay, cut-the-curve, seam-craft |
| remotion-dev/remotion (`a64a027`) | remotion-best-practices, remotion-create, remotion-render, remotion-studio, remotion-captions, remotion-multimedia, remotion-docs, remotion-upgrade, remotion-markup, remotion-interactivity |
| calesthio/OpenMontage (`e01dbf4`) | openmontage (ponte para o submódulo `ferramentas/OpenMontage`), elevenlabs, text-to-speech, sound-effects, music, speech-to-text, ffmpeg, flux-best-practices |
| browser-use/browser-use (`3df5806`) | browser-use, open-source, qa |
| JuliusBrussee/caveman (`1f951fb`) | caveman, ultracave, caveman-commit, caveman-review, caveman-help, investigate-first, lean-build, surgical-patch, safe-refactor, verify-and-stop, migration |
| obra/superpowers (`22f0b46`) — 08/11/2026 | brainstorming, writing-plans, executing-plans, subagent-driven-development, dispatching-parallel-agents, systematic-debugging, test-driven-development, verification-before-completion, requesting-code-review, receiving-code-review, using-git-worktrees, finishing-a-development-branch, writing-skills |
| bangtutorial/bang-motion (`c1aa65e`) — 08/11/2026 | bang-motion (sem a ponte After Effects/Higgsfield: removidos `references/ae-bridge-higgsfield.md` e `scripts/ae/`) |
| Jakeschincariol/instagram-agent-skill (`d03c56b`) — 08/11/2026 | ig-reel, ig-caption, ig-carousel, ig-story, ig-plan, ig-viral, ig-audit, ig-profile, ig-human, ig-comment, ig-reply, ig-dm, ig-repurpose |
| RobMitt/grill-me-skill (`31d61d6`) | grill-me |

Deixadas de fora: skills internas de desenvolvimento de cada repositório, as que dependem de contas
de nuvem (Caveman Cloud, Browser Use Cloud, x402) e `remotion-saas`/`remotion-maps`.
O repositório `higgsfield-ai/higgsfield` não tem skills (é um framework de treino de LLM em GPU) e
o projeto não usa Higgsfield.

Em 08/11/2026 também ficaram de fora: `using-superpowers` (força carregar skills antes de toda resposta) e
`diagnosing-superpowers` (diagnóstico interno do próprio superpowers); e o `thedotmack/claude-mem` inteiro
(é um plugin com serviço rodando em segundo plano e banco de memória local, que se perde quando o
contêiner da nuvem é reciclado; a memória do projeto fica nos arquivos do repositório).
As skills `ig-*` guardam voz/plano/log em `~/.claude/instagram/`, que some na nuvem: copiar para
`saude-sem-sermao/instagram/` o que valer guardar.
