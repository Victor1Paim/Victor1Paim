# Barra Deck · Reel Ceia de Natal 2026

Vídeo vertical 1080×1920, 24 s, 30 fps, narração em pt-BR. Cores e fontes da marca.

| Arquivo | O quê |
|---|---|
| `src/Reel.tsx` | cenas, tempos e textos (tempos amarrados à narração em `t()`) |
| `scripts/narracao.py` | gera a voz (OpenAI `gpt-4o-mini-tts`, voz *coral*) e os tempos por palavra (Whisper) |
| `scripts/baixar_fontes.py` | baixa Cormorant Garamond e Karla para `public/fontes` |
| `legenda.md` | legenda e hashtags para o post |

## Renderizar
```bash
npm ci
```
```bash
npm run render
```
Depois, normalizar o volume para Reels:
```bash
ffmpeg -i out/barra-deck-natal-reel.mp4 -c:v copy -af loudnorm=I=-14:TP=-1.5:LRA=11 -c:a aac -b:a 192k out/final.mp4
```

Música: adicionar pelo próprio Instagram (biblioteca licenciada), volume baixo sob a narração.

Custo de API desta versão (estimado): TTS ~US$ 0,005 + Whisper ~US$ 0,002 ≈ **US$ 0,01 (≈ R$ 0,06)**.
