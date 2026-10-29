# Som dos vídeos: efeitos por cena

Feedback do usuário (29/10/2026) no vídeo 001: faltaram efeitos sonoros adaptados a cada cena: som de contagem nos números, cronômetro no quiz, som de objetos passando.
O som agora é planejado **por tipo de plano**, automaticamente, a partir de `shots.json` (`producoes/001-sol/scripts/sfx.py`).

## Ferramentas

| Fonte | Uso | Licença |
|---|---|---|
| Biblioteca offline da skill `media-use` (21 efeitos, copiados para `assets/sfx-lib/`) | whoosh, pop, impacto, ping, erro, sparkle, cliques | Pixabay Content License (uso comercial livre, sem atribuição obrigatória) |
| Síntese em Python (sem dependências, semente fixa) | cronômetro, contagem de números, zíper de traço, líquido, plips, baque, subida/queda | Própria (código do projeto) |
| Openverse (busca na skill `media-use`) | **não alcançável daqui** (rede bloqueada); fica como opção se o domínio for liberado | CC0 / CC BY (exige crédito) |
| Skills extras (catálogo do usuário) | Procuradas em 29/10/2026: nada encontrado | — |

Regra do HyperFrames: cada efeito tem uma causa visível; o pico cai cerca de 1 quadro depois da imagem; variar o som repetido (tom e canal).

## O que toca em cada cena

| Cena (tipo de plano) | Efeito |
|---|---|
| Quiz entra (A–D) | Passe rápido + 4 pops subindo de tom, um por opção |
| **Cronômetro** | Tique-taque do quiz até o fim da contagem: 2 por segundo, **4 por segundo** durante o 3-2-1, e bipe de fim de tempo |
| Contagem 3-2-1 | Clique + ping a cada número |
| Resposta do quiz (C acende) | Ping, sino e sparkle |
| **Número contando** (109×, 1,3 milhão, 74%, ~960 mil) | Roleta de cliques que acompanha a curva do número (rápida no começo, lenta no fim), tom subindo, e ping ao pousar |
| Número fixo | Pop curto |
| **Objeto passando** (panorâmicas) | Whoosh que atravessa o estéreo no sentido do movimento (esquerda para direita ou o contrário) |
| Órbita e inclinação de câmera | Whoosh grave e discreto, com movimento no estéreo |
| Soco de zoom (punch) e carimbo (PEGADINHA) | Baque grave; carimbo soma um aviso de "erro" suave |
| Zoom até o alfinete | Whoosh cinematográfico crescente e pop no fim |
| Traço se desenhando (régua, linha, caixa) | Zíper + clique ao fechar |
| Barra crescendo | Subida de tom |
| Esferas empilhando, vãos, quadrados | Plips rápidos subindo de tom |
| Terra derretendo, Sol enchendo de água | Bolha, queda, respingo, água enchendo |
| Textos que entram "estourando" | Pop curto; os que deslizam, passe curto |
| Troca entre beats | Whoosh de transição |
| Fecho (SEGUE e @) | Pop e sparkle |

## Níveis e verificação (medido, não ouvido)

Mix final do rascunho 4: **−14,2 LUFS**, pico **−1,7 dBFS**. Os tique-taques da contagem batem em **−5,9 dBFS** de pico (voz em ≈ −1,5).
Foi medido com `ffmpeg ebur128`; ninguém ouviu o resultado ainda. O ajuste fino de volume deve ser feito com o ouvido do usuário.

## Para ajustar

Ganhos por evento: `scripts/sfx.py` (campo `g=`). Rodar `python3 -I scripts/sfx.py` e `node scripts/build.mjs` e renderizar de novo.
Sem música por enquanto: a música é um portão à parte.
