---
name: whisper-legendas
description: Transcrever áudio/vídeo com o Whisper local (openai-whisper, grátis, sem chave) para gerar legendas com tempo por palavra e conferir se a narração bate com o roteiro. Use ao legendar um vídeo dos canais (Saúde sem Sermão, Desvendando Ideias, Halftone), ao checar uma voz gerada contra o roteiro, ou ao transcrever um vídeo de referência.
---

# Whisper: legendas e conferência de narração

Roda na máquina, sem chave e sem enviar o áudio a terceiros. Script: `scripts/whisper_legendas.py`.

## Uso

```bash
python3 .claude/skills/whisper-legendas/scripts/whisper_legendas.py AUDIO --saida PASTA [--roteiro ROTEIRO.txt] [--modelo turbo]
```

Gera em `PASTA/`:
- `NOME.palavras.json` — lista `{palavra, inicio, fim}` em segundos (entrada para legendas no Remotion/HyperFrames).
- `NOME.srt` — legenda por frase.
- `NOME.txt` — texto corrido.
- `NOME.conferencia.txt` (com `--roteiro`) — diferenças entre o roteiro e o que a voz falou.

## Regras

- Modelo padrão `turbo` (~1,5 GB, baixado no primeiro uso para `~/.cache/whisper`). Em CPU leva ~1 min para carregar e ~0,3× a duração do áudio para transcrever. `small` é mais rápido e pior.
- Sempre passar o idioma (`--idioma pt`, padrão).
- A legenda final usa o **texto do roteiro** com o **tempo do Whisper**: o Whisper pode errar grafia de nomes, termos médicos e marcas. Nunca publicar a transcrição crua sem revisar.
- Na conferência, qualquer diferença em número, dose, nome de doença ou de remédio é bloqueante: regerar a voz.
- Precisa do host `openaipublic.azureedge.net` liberado no ambiente para baixar o modelo.
