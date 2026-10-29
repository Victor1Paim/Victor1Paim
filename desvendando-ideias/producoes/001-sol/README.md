# 001 · Quantas Terras cabem no Sol (HyperFrames, 1080×1920)

Roteiro, decisões e fatos: `../../roteiros/001-quantas-terras-cabem-no-sol.md`.

## Como reconstruir

```sh
scripts/voz-proc.sh        # normaliza a voz de cada beat para assets/voz/proc/ (ffmpeg)
node scripts/build.mjs     # gera index.html, compositions/*.html, PLANOS.md, build-out.json e o som do cronômetro (scripts/sfx.py)
npx hyperframes check      # lint + runtime + layout + contraste
npx hyperframes snapshot --at 3.4,34.6   # quadros para olhar
npx hyperframes render --quality draft -o renders/001-sol-rascunho.mp4   # ~2,5 min nesta máquina (sem GPU)
```

## O que é dado e o que é código

| Arquivo | Papel |
|---|---|
| `shots.json` | **Os planos**: fala, tipo de plano, câmera, fundo e estilo (2D, 2,5D, 3D). Para mudar o vídeo, edite isto |
| `scripts/build.mjs` | Receitas visuais por tipo de plano, tempos dos planos a partir da voz, legendas palavra a palavra, `index.html` |
| `scripts/sfx.py` | Tique-taque de cronômetro, bipe e sino (síntese, sem arquivos externos) |
| `assets/voz/beat*.wav` | Voz crua (Gemini TTS, um arquivo por beat); `assets/voz/proc/` é a versão normalizada que toca no vídeo |
| `assets/vendor/gsap.min.js` | GSAP local (o ambiente bloqueia CDNs) |
| `assets/sfx/`, `renders/`, `.hyperframes/` | Gerados; fora do git (os renders de marco entram com `git add -f`) |

## Limites conhecidos

- Sem WebGL neste ambiente: o "3D" é CSS 3D (cubo) e esferas sombreadas; sem Three.js.
- Tempos dos planos dentro de cada beat são estimados pela fala (pausas reais da voz + proporção de caracteres). Quando houver whisper, trocar por palavras com tempo exato.
- "Fonte: NASA" aparece no plano do 1,3 milhão e **precisa ser conferida** antes de publicar.
- Sem música. O áudio do cronômetro e o sino foram pedidos/derivados do roteiro; outros efeitos (whoosh, impacto) ficam para um portão futuro.
