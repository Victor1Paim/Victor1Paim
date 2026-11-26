# Formatos do canal (definidos em 26/11/2026)

Tudo é gerado e montado aqui, sem passar pelo CapCut. Entrega: vídeo final pronto para subir, miniatura, legenda .srt e texto de publicação.

| Formato | O que é | Duração | Tela | Legenda | Custo estimado |
|---|---|---|---|---|---|
| **Coletânea** (principal) | 3–5 histórias com um tema ("3 Disturbing Road Trip Stories") | 20–35 min | 16:9, 1080p | **gravada no vídeo** + .srt enviada ao YouTube | ≈ US$ 5 |
| **História única** | 1 história longa, como o piloto | 6–10 min | 16:9, 1080p | gravada + .srt | ≈ US$ 1,50–2 |
| **Short — história curta** | história completa e original, com virada no fim | 45–90 s | 9:16, 1080×1920 | queimada, palavra a palavra | ≈ US$ 0,20–0,35 |
| **Short — corte** | o trecho mais tenso de uma história do longo, chamando para o vídeo completo | 45–90 s | 9:16 | queimada | ≈ US$ 0,10 (reaproveita voz e imagens) |

## Padrão de todo vídeo longo (das referências)

- 0–7 s vinheta com o título; 7–12 s cartela "Story N / By: …" com sting; a narração começa sem saudação.
- Voz Gemini **Enceladus**, ~190–197 palavras/min, 0,85 s entre parágrafos.
- 1 imagem por parágrafo (~15–25 s), movimento lento alternado, dissolve de 1 s, cor escura e dessaturada, grão.
- Drone grave próprio ~11 dB abaixo da voz; mix a −20 LUFS.
- Final: 4 s no último plano + 20 s de tela escura para os elementos de fim do YouTube.
- Coletânea: sting e cartela nova em cada troca de história; capítulos na descrição.

## Shorts

- Gancho na primeira frase (sem vinheta). Texto curto e legível no celular, 2–4 palavras por vez, no terço de baixo da área segura.
- 3–6 imagens geradas já em vertical (1024×1536).
- História curta: 120–250 palavras. Corte: termina num momento de suspense e manda para o vídeo completo.

## Custos

Detalhes e valores medidos em [`custos.md`](custos.md).

## Regras de texto

- Histórias são **originais** (inspiradas em relatos, com nomes, lugares e finais nossos): **não** chamar de "True" no título nem na miniatura.
- Cartela "By: Anonymous" até haver histórias enviadas por inscritos com autorização.

## Entrega

- `final/video.mp4` (1080p, teto de 6 Mbps) e `final/parteNN.mp4`: partes de até ~180 MB cortadas em pausas da narração,
  em quadro-chave exato. Juntar em ordem, uma colada na outra (fim de uma = começo da próxima), sem transição.
- `entrega/miniatura.jpg`, `final/legenda.srt`, `publicacao.md` (títulos, descrição com capítulos, configurações).
