# Barra Deck · Reel Ceia de Natal 2026

Vídeo vertical 1080×1920, 26,5 s, 30 fps. Motion graphics (sem fotos de produto), fundos gerados por IA,
narração masculina estilo apresentador (OpenAI `gpt-4o-mini-tts`, voz *ash*, acelerada 1,1×). Cores e fontes da marca.

| Arquivo | O quê |
|---|---|
| `src/Reel.tsx` | cenas, tempos e textos (tempos amarrados à narração em `t()`) |
| `scripts/vozes_teste.py` | gera a narração em vozes masculinas (ash, onyx, echo) para escolher |
| `scripts/narracao.py` | função de transcrição (Whisper) com tempos por palavra |
| `scripts/gerar_fundos.py` | gera os 5 fundos de motion graphics (OpenAI `gpt-image-2`) |
| `custos.jsonl` | registro de uso das gerações de imagem |
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

Custo de API (estimado): v1 ≈ US$ 0,01 · v2: 5 fundos ≈ US$ 0,27 + 3 vozes ≈ US$ 0,02 + Whisper ≈ US$ 0,003 → **≈ US$ 0,30 (≈ R$ 1,70)**.

## Vídeo de divulgação (composição `Divulgacao`)
30 s, 1080×1920, sem narração (música entra pelo Instagram). Fundo: os dois criativos do cliente
(`public/criativos/fundo1.mp4` e `fundo2.mp4`) desfocados e escurecidos, com textura de feltro.
Cenas: logo → "O fogão é nosso. A noite é sua." → cardápio (5 categorias, 3 pratos com foto e preço 2026)
→ prazos e local → QR code + site + WhatsApp. Pratos e preços em `src/Divulgacao.tsx` (`CARDAPIO`).
```bash
npx remotion render Divulgacao out/divulgacao.mp4 --codec h264 --crf 18
```
