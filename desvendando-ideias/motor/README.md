# Motor de produção (compartilhado por todos os vídeos)

Gera o vídeo a partir de **dados** (`shots.json` + voz) em HTML do HyperFrames, com legendas palavra a palavra, efeitos sonoros por cena e peles. Cada vídeo é uma pasta em `producoes/NNN-slug/`.

| Arquivo | Para que serve |
|---|---|
| `novo.mjs` | Cria `producoes/NNN-slug/` (projeto) e `roteiros/NNN-slug.md` (a partir de `producao/roteiro-modelo.md`) |
| `voz-proc.sh` | Normaliza a voz de cada beat (−13 LUFS, pico −1,5 dBTP) em `assets/voz/proc/` |
| `build.mjs` | Lê `shots.json` e os tempos da voz; escreve `index.html`, `compositions/`, `PLANOS.md`, `build-out.json`; chama `sfx.py`. Opções: `--tema cosmos\|brutal\|blueprint\|iso`, `--beats 3,4`, `--out pasta`, `--dir pasta` |
| `sfx.py` | Efeitos sonoros por tipo de plano (biblioteca `sfx-lib/` + síntese). Ver `producao/som.md` |
| `checar.mjs` | Confere duração, planos, texto na tela, voz, roteiro, fontes pendentes e o render (loudness, pico, resolução). `--full` roda também `hyperframes check` |
| `vendor/gsap.min.js` | GSAP local (o ambiente bloqueia CDNs); `build.mjs` copia para cada vídeo |
| `sfx-lib/` | 11 efeitos reais da skill `media-use` (licença Pixabay) |
| `molde/` | Arquivos-base de projeto copiados por `novo.mjs` |

## Fluxo de um vídeo novo

```sh
node desvendando-ideias/motor/novo.mjs 002 slug "Título"      # cria pasta e roteiro (portões 1 a 5 no roteiro)
# ... escrever shots.json e gerar a voz por beat (gemini-midia)  → assets/voz/beatN.wav
cd desvendando-ideias/producoes/002-slug
../../motor/voz-proc.sh
node ../../motor/build.mjs
node ../../motor/checar.mjs --full
npx hyperframes render --quality draft -o renders/002-slug-rascunho1.mp4
```

Peles: `node ../../motor/build.mjs --tema brutal --beats 3,4 --out ../002-slug-teste-brutal` gera só um trecho em outra pele (reproduz o teste de peles do vídeo 001).

## Limites conhecidos

Sem WebGL no ambiente: 3D é CSS 3D. Tempos dos planos dentro de um beat são estimados pela fala (pausas reais + proporção de caracteres); com whisper seria exato. Os planos novos de cada vídeo ainda são
escritos à mão em `shots.json` (receitas: `build.mjs`, objeto `R`); novos tipos de plano entram no motor para todos os vídeos.
