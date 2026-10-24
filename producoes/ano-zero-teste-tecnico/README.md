# Ano Zero — teste técnico (produção OpenMontage)

Produzido 100% pelo OpenMontage, pipeline `animation`, modo atelier, montagem HyperFrames.

- Vídeo: `ano-zero-teste-tecnico.mp4` (1080×1920, 30 fps, H.264/AAC, 17 s)
- Artefatos do pipeline (pesquisa, proposta, decisões, roteiro, cenas, assets, edição, render): `artifacts/`
- Composição editável: `hyperframes/` (`npx hyperframes@0.8.193 preview` dentro da pasta)
- Prompts de cada imagem: `prompts/`

| Item | Ferramenta | Custo estimado [E] |
|---|---|---|
| 11 imagens (6 placas + 3 camadas refeitas + 2 edições sem fogos) | google_imagen · gemini-3-pro-image 2K | ~US$ 1,47 |
| Narração do Edson | gemini_tts · gemini-3.8-flash-tts, voz Algenib | ~US$ 0,01 |
| Ambiente | google_music · Lyria 3.5 | ~US$ 0,04 |
| Recorte, mixagem, render | ffmpeg + HyperFrames local | US$ 0 |
| **Total** | | **~US$ 1,52** |

O Gemini não devolve o valor cobrado (`cost_status: unquoted`): conferir no faturamento do Google AI Studio.

Para refazer o render a partir do OpenMontage: copie `hyperframes/` e `artifacts/` para
`ferramentas/OpenMontage/projects/ano-zero-teste-tecnico/` e rode `hyperframes_compose` com
`operation: render_existing`.
