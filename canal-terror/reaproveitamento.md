# O que veio de outros branches e repositórios (26/11/2026)

Busca feita em todos os 15 branches de `Victor1Paim/Victor1Paim` e no repositório `Barra-Deck---Bot-1-` (bot e site da Barra Deck, nada útil aqui).

## Trazido para este branch

| O quê | De onde | Para que serve aqui |
|---|---|---|
| Skill `whisper-legendas` | `claude/modest-allen-izwbz7` | legendas .srt e tempo por palavra; conferir a voz contra o roteiro (trocar `--idioma pt` por `en`) |
| Skill `gemini-midia` | `claude/modest-allen-izwbz7` | imagens (e voz alternativa) pelo Gemini com simulação, cache e log de custo |
| Skill `prompt-de-pesquisa` | `claude/modest-allen-izwbz7` | Reddit não é acessível daqui: gera o prompt para pesquisar creepypastas/relatos no Grok/Perplexity |
| Skill `humanizer` | `claude/modest-allen-izwbz7` | tirar marcas de texto de IA dos roteiros em inglês |
| `ferramentas/limpar-fim-audio.py` | `claude/wonderful-babbage-737sjf` (gta6-clipes) | corta o estalo que TTS deixa no fim do áudio |
| `ferramentas/baixar-drive.sh` | `claude/wonderful-babbage-737sjf` | baixar vídeo de pasta pública do Drive |

## Fica onde está, mas vale consultar

| O quê | Onde | Por quê |
|---|---|---|
| Plano de som por tipo de cena (`producao/som.md`, `motor/sfx.py`) | `claude/desvendando-ideias` | método de efeitos sonoros e medição de loudness (−14 LUFS) |
| Fluxo com portões de decisão (`producao/fluxo-por-video.md`) | `claude/desvendando-ideias` | base do fluxo em `plano-do-canal.md` |
| Corte automático de pausas (Whisper + ffmpeg) | `claude/loving-ritchie-7ld3r4` (kit da apresentadora) | se um dia houver voz gravada |
| `corte-gringo.py`, `narrar-gemini.py`, `analisar-live.py` | `claude/wonderful-babbage-737sjf` | cortes de vídeo em inglês e narração pelo Gemini |
| Skill `last30days` | `claude/modest-allen-izwbz7` | pesquisa de tendências; pesada (158 arquivos), trazer só se for usar |
| Skills `ig-*`, `bang-motion`, `mg-styles-15` | `claude/modest-allen-izwbz7` | redes sociais e motion; pouco a ver com terror longo |
| Projeto Remotion e `checar-ep.mjs` | `halftone/` (este branch) | base para o template de montagem e o checador de entrega |

## Chaves e acessos

- OpenAI: conectada pelo proxy da sessão (voz, Whisper). Testada.
- Gemini: **não há `GEMINI_API_KEY`** nesta sessão; adicionar nas variáveis do ambiente para gerar imagens.
- YouTube: sem conector; publicar exige a API do YouTube (OAuth) ou subir à mão.
