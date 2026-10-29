# Tarefa: teste de render 3D do telhado no Blender Cycles (rodar no computador do usuário)

Fale com o usuário em português do Brasil. Esta sessão roda no computador dele (Windows, PowerShell), com placa de vídeo, no clone local do repositório.

## Objetivo
Recriar os primeiros ~10 s do vídeo **004 · Como se constrói um telhado** em **Blender Cycles** (decisão 34: qualidade acima de tempo), compor por cima a legenda, os títulos e o áudio que já existem, e mostrar a comparação com a versão atual (Three.js) antes de renderizar o vídeo inteiro.

## Antes de tudo
1. Confirme que está no branch `claude/desvendando-ideias` e atualizado (`git pull`).
2. Leia: `CLAUDE.md`, `desvendando-ideias/decisoes.md` (decisões 33 e 34), `desvendando-ideias/producao/3d-no-computador.md`, `desvendando-ideias/roteiros/004-telhado.md`.
3. Confira e informe: `blender --version` (no Windows pode estar em `C:\Program Files\Blender Foundation\Blender 4.x\blender.exe`), a placa (`nvidia-smi` ou equivalente), se o Cycles enxerga a GPU (OPTIX/CUDA/HIP), `ffmpeg -version`, `node -v`. Se faltar algo, diga o comando `winget` para instalar e pare.

## Referência da cena (não reinventar)
- `desvendando-ideias/motor/3d/cena.js`: mundo atual em Three.js, usado como especificação. Casa W=6 (x), D=5 (z), H=3; telhado de duas águas com cumeeira no eixo x; telhas meia-cana em fileiras (19 colunas × 9 linhas por lado, passo 0,42); laje com poças e trinca; chuva; gotas; personagem (cabeça cúbica com rosto, cabelo castanho espetado, moletom preto com nuvens vermelhas de borda branca, calça jeans; poses idle, umbrella, worried, celebrate, think, sit); câmeras em `CAMS`; estado por trecho com as chaves de `DEF`, e valores `[a, b]` interpolados ao longo do trecho.
- Tempos e estados: rode `node ../../motor/build.mjs --tema cosmos` dentro de `desvendando-ideias/producoes/004-telhado`; o array `shots` embutido no `index.html` (função `shots3d()` em `motor/build.mjs`) tem os trechos com estado por frase e câmera por plano (`camStart`/`camDur`).

## O que fazer
1. Criar `desvendando-ideias/motor/blender/cena_telhado.py` (bpy) com o mesmo mundo e visual melhor: céu Nishita, sol suave, materiais PBR simples (telha cerâmica, reboco, madeira, grama), bevel leve, chuva fina, desfoque de movimento. Estilo low-poly/cartoon com luz de verdade.
2. O script lê os trechos (exportar do index.html para `producoes/004-telhado/blender/trechos.json`) e anima por quadro, a 30 fps, os mesmos estados e câmeras. Para o teste, só t = 0 a 10 s.
3. Cycles na GPU: 1080×1920, ~128 amostras + denoise, PNG em `producoes/004-telhado/blender/frames/` (pôr no .gitignore). Medir segundos por quadro.
4. Camada de cima: gerar legenda/títulos do HyperFrames com fundo transparente para os mesmos 10 s (criar no `build.mjs` um modo que omite o canvas 3D; `npx hyperframes render --format webm` ou `mov`), sobrepor com ffmpeg aos quadros do Blender e pôr o áudio do trecho (voz em `assets/voz/proc/` + `assets/sfx/sfx-mix.wav`, nos tempos de `build-out.json`; −14 LUFS).
5. Entregar: o clipe de 10 s, uma imagem com 3 quadros lado a lado (atual × Cycles; se o vídeo atual não existir localmente, use `npx hyperframes snapshot` nos mesmos instantes) e o tempo de render por segundo de vídeo, com a estimativa para os 2:37.
6. Commitar o código no branch (renders e quadros fora do git). Nunca gravar chave de API em arquivo.

## Regras do canal
- Planos de 2 a 4 s; sem som de troca de cena (decisão 34).
- Não renderizar o vídeo inteiro sem o "ok" do usuário.

## Pronto quando
O usuário viu o clipe de 10 s em Cycles, a comparação e a estimativa, e respondeu se seguimos com o vídeo inteiro.
