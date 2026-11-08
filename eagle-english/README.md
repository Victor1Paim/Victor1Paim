# Eagle English BR (@eagle.english.br)

Perfil de TikTok + Instagram que ensina inglês a brasileiros. Projeto dividido em duas ferramentas:

- **ChatGPT**: carrosséis e legendas (chat central + chat de arte). A fila e o banco de frases moram lá.
- **Claude Code (esta pasta)**: vídeos (Reels/TikTok) dos mesmos temas.

Todo conteúdo termina com o CTA do produto **Eagle 350 – Inglês por Situação** + "link na bio".

## Onde está cada coisa

| Caminho | O quê |
|---|---|
| `CLAUDE.md` | instruções do agente de vídeo (lido automaticamente pelo Claude Code) |
| `docs/EAGLE_ENGLISH_PROJETO_COMPLETO.md` | regras completas: estado, prompts do ChatGPT, identidade, estilos, pronúncia, fila, CTA, banco de frases, pacotes prontos |
| `docs/PASSO_A_PASSO_EAGLE_ENGLISH.md` | quem faz o quê, em que ordem |
| `docs/estado.md` | último bloco ESTADO ATUALIZADO do ChatGPT |
| `docs/HOOKS_E_CTA_VIDEO.md` | duração padrão (40 s–1 min 10 s), ganchos, retenção e o CTA final novo |
| `docs/PROMPT_PESQUISA_MANUS_VIDEO.md` | prompt de pesquisa no Manus para os vídeos (quiz, pronúncia, estilos) |
| `docs/originais/` | os PDFs originais (fonte da conversão) |
| `templates/` | cartões HTML (capa, frase, produto) para texto exato na tela |
| `scripts/` | `preparar.sh`, `novo_post.sh`, `render_cartoes.py`, `vozes.py` (Gemini TTS + Whisper) |
| `assets/` | mascote (PNGs sem fundo), fontes, música, sfx, marca |
| `posts/AAAA-MM-DD_tema/` | um post por pasta: `frases.json`, `slides/`, `audio/`, `roteiro.md`, `legenda.md`, `video/` |

> Os `.md` em `docs/` foram convertidos dos PDFs. Linhas muito longas dentro de blocos de
> código (alguns prompts de imagem) vieram cortadas no próprio PDF. Se você tiver os `.md`
> originais no notebook, substitua os arquivos de `docs/` por eles.

## Continuar no notebook

```bash
git clone https://github.com/Victor1Paim/Victor1Paim.git
cd Victor1Paim
git checkout claude/eagle-english
cd eagle-english
bash scripts/preparar.sh          # ffmpeg à parte; cria .venv, instala Playwright e cria o .env
# coloque sua GEMINI_API_KEY no .env (nunca no chat)
cd ..                             # volte para a raiz do repositório
claude                            # abra o Claude Code NA RAIZ: é lá que estão as skills (.claude/skills)
```

Se o repositório já estiver clonado: `git fetch origin && git checkout claude/eagle-english && git pull`.

## Ciclo de um vídeo

1. `bash scripts/novo_post.sh 2026-11-17 lavanderia` e cole as frases do ChatGPT em `frases.json`.
2. (Opcional) coloque os PNGs do carrossel em `slides/`.
3. `python3 scripts/render_cartoes.py posts/2026-11-17_lavanderia` → cartões em `cartoes/`.
4. `python3 scripts/vozes.py montar posts/...` → revise `falas.json` → `python3 scripts/vozes.py gerar posts/...`.
5. Peça ao Claude Code: "Gere o vídeo do formato A para o post de lavanderia".
6. Assista com e sem som; peça ajustes pontuais.

Primeiro post já preparado: `posts/2026-11-10_salao/` (D10 Salão, 7 frases da pesquisa do Manus de 07/11).

## Custo de API

Toda chamada ao Gemini é registrada em `posts/<post>/custos.jsonl`.
Relatório: `python3 ../scripts/custos.py relatorio posts/<post>` (preços em `../scripts/precos-api.json`).

## Skills

O Claude Code usa as skills de `../.claude/skills` (as mesmas do branch `claude/awesome-cannon-sxprt5`):
vídeo (HyperFrames, bang-motion, Remotion, ffmpeg), Whisper, e as `ig-*` para Reels, legendas,
stories e métricas. Lista e origem em `../.claude/skills/FONTES.md`.
