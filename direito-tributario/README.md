# Direito Tributário · tela dividida + motion (projeto em teste)

Perfil de vídeos verticais (9:16) sobre Direito Tributário brasileiro. Base editorial: o PDF
"Prompt Mestre — Direito Tributário com movimento" (v1.0, 10/11/2026). Independente do Halftone.

**Formato:** tela dividida (apresentador em cima, 40% da altura; explicação embaixo, 60%). Nos trechos
que pedem explicação, a explicação "sobe" e toma a tela inteira em motion; no fecho a tela volta a dividir.

**Estilo visual:** cartum em papel creme, traço de nanquim que "ferve" (redesenho a ~8 quadros/s),
cores apagadas (teal e laranja da identidade do PDF + mostarda, sálvia, jeans), letra manuscrita em caixa alta
(Patrick Hand), legenda queimada com palavra-chave em vermelho. Inspirado na *estética* das referências
(animações de @rafaellatuma) — sem copiar personagens, cenários ou assinatura dela.

## Fluxo de um vídeo
1. `testes/<id>/falas.json` — roteiro dividido em falas, cada uma com `modo` = `dividida` ou `motion`.
2. Voz: `python3 scripts/vozes_openai.py testes/<id>` (gpt-4o-mini-tts; custo vai para `custos.jsonl`).
   Quando houver gravação real do apresentador, ela substitui a voz e o boneco do painel de cima.
3. Tempos: `python3 scripts/preparar_dados.py testes/<id>` (Whisper local, grátis) → `video/src/dados-<id>.json`.
4. Cenas em `video/src/Cenas.tsx` (uma por fala, sincronizadas por palavra com `quando(fala, 'palavra')`).
5. Render: `cd video && npx remotion render src/index.ts <id> ../testes/<id>/<id>.mp4`
   (conferir quadros: `node scripts/quadros.mjs <id> <pasta> 120 400 ...`).
6. Custo: `python3 ../scripts/custos.py relatorio direito-tributario/testes/<id>`.
