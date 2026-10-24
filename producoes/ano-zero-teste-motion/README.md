# Ano Zero — teste motion (início da infecção)

57,8 s · 1080×1920 · 30 fps · H.264/AAC · −15 LUFS. Tudo animado em código (Remotion), sem imagens de IA.

- Animação: `halftone/src/motion/` (composição `AnoZero-TesteMotion`)
- Linha do tempo (falas, palavras, batidas, eventos): `halftone/src/motion/timeline.json`,
  gerada por `halftone/scripts/montar-teste-motion.py`
- Áudio: `halftone/public/series/ano-zero/teste-motion/audio/`
- Falas e vozes: `falas.json` (Gemini TTS: narrador Algenib, Bia Kore, Rafa Puck, ambulante Charon)

| Item | Custo |
|---|---|
| 12 falas no Gemini TTS | ~US$ 0,02 [E] |
| Animação, trilha (batida + multidão sintetizadas), legendas, render | US$ 0 (local) |

Legenda palavra por palavra com tempo estimado por sílaba dentro de cada trecho de fala medido
(sem Whisper: huggingface.co bloqueado na rede do ambiente).
