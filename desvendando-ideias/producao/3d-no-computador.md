# 3D no computador do usuário (próxima produção)

Decisão do usuário (29/10/2026): o 004 ficou bom, mas a próxima produção em 3D roda no computador dele, com placa de vídeo, para render mais rápido e melhor. Também vamos testar outros jeitos de gerar o 3D.

## Antes da sessão (checklist do usuário)

1. Instalar: Git, Node 20+, Python 3.11+, ffmpeg, **Blender 4.x** (grátis) e o driver mais novo da placa de vídeo.
2. Clonar o repositório e abrir o branch `claude/desvendando-ideias`.
3. Criar uma chave nova do Gemini e guardar como variável de ambiente `GEMINI_API_KEY` no computador (não colar no chat).
4. Abrir o Claude Code **no próprio computador**, na pasta do repositório (app Claude no desktop → Claude Code → escolher a pasta). Funciona em Windows, Mac e Linux.
   - Alternativa: compartilhar a pasta por Remote Control (app → Settings → Claude Code → Remote Control) para uma sessão na nuvem usá-la. Só vale para **Mac ou Linux**, e a pasta precisa ser a raiz de um repositório git.

## Teste comparativo (mesma cena do 004, 10 s)

| Opção | O que muda | Esperado |
|---|---|---|
| A. Three.js atual com GPU | `npx hyperframes render --browser-gpu` (o padrão já tenta a placa) | Mesmo visual, render muito mais rápido; dá para ligar sombras suaves, oclusão de ambiente (SSAO), bloom e mais geometria |
| B. Blender Eevee (script Python `bpy`) | Cena montada por código no Blender, render Eevee | Luz e sombras bonitas, materiais melhores, rápido com GPU |
| C. Blender Cycles | Mesmo script, render Cycles com poucas amostras + denoise | Visual mais realista (luz rebatida), mais lento |

Medir em cada uma: segundos de render por segundo de vídeo, qualidade (quadros lado a lado) e esforço para manter. A legenda, os títulos e o som continuam no HyperFrames; o 3D entra como vídeo de fundo quando vier do Blender.

## Melhorias de visual a testar junto

- Personagem com mais detalhe (mãos, expressões trocando por fala, piscar), mesmo estilo de cabeça quadrada e moletom de nuvens.
- Materiais com textura (telha, madeira, reboco), céu com nuvens, chuva com respingos.
- Câmera com movimento contínuo entre cenas (sem corte seco) e desfoque de movimento.
- Transições mais longas, mantendo a média de ~3,5 s por plano do 004.
