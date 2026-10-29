# Tarefa: produzir o vídeo 005 · Estalar os dedos dá artrite? (rodar no computador do usuário)

Fale com o usuário em português do Brasil (pronomes neutros). Esta sessão roda no computador dele (Windows, PowerShell, sem placa de vídeo dedicada: Intel UHD + Core Ultra), no clone local do repositório.

## Antes de tudo
1. Branch `claude/desvendando-ideias`, atualizado (`git pull`).
2. Leia: `CLAUDE.md`, `desvendando-ideias/decisoes.md` (29, 33 e 34), `desvendando-ideias/producao/padrao-cadeia-problema-solucao.md`, `desvendando-ideias/producao/3d-no-computador.md`, `desvendando-ideias/producao/tarefa-teste-blender.md` e **o roteiro `desvendando-ideias/roteiros/005-estalar-dedos.md`** (texto, planos, fatos, legendas).
3. Se o teste Eevee × Cycles da tarefa anterior ainda não terminou, termine-o primeiro e registre em `producao/3d-no-computador.md` os segundos por quadro (sem contar o 1º quadro do processo) de cada motor.

## Portões com o usuário (perguntar antes de gastar voz ou render)
1. **Hook** e **CTA**: o roteiro tem 5 opções de cada (recomendados: hook 1 e CTA 1). Pergunte qual usar, registre no roteiro (tabela de portões) e monte os beats 0 e 8.
2. **Motor 3D**: com os tempos do teste, recomende e pergunte.
   - Cycles na CPU se ficar ≤ 20 s por quadro em 1080×1920 (com denoise; ~2.700 quadros ≈ 15 h).
   - Senão, Eevee com 64 amostras, sombras e AO ligados (decisão 34 pede qualidade, mas a máquina não tem GPU).
   - Informe a estimativa total em horas antes de renderizar o vídeo inteiro.
3. **Corte de teste**: mostre 3 planos prontos (1, 13 e 20 do roteiro) com legenda e som antes do render completo.

## Etapas
1. **Projeto:** `node desvendando-ideias/motor/novo.mjs 005 estalar-dedos "Estalar os dedos dá artrite?"`.
2. **Voz:** `GEMINI_API_KEY` precisa estar no ambiente do Windows (o usuário roda `setx GEMINI_API_KEY "<chave>"` e reabre o PowerShell; nunca peça a chave no chat nem a grave em arquivo). Skill `gemini-midia`: modelo `gemini-3.8-flash-lite-tts`, voz Kore, sem `--style`, um arquivo por beat (`assets/voz/beat0.wav` … `beat8.wav`), cache em `producoes/.cache-gemini`. Rode `usage` antes e depois e anote o custo. Acelere 1,2× (`ffmpeg -af atempo=1.2`) e depois rode `motor/voz-proc.sh` (no Git Bash) ou o mesmo `loudnorm` −13 LUFS direto no ffmpeg.
3. **Tempos:** `shots.json` com `"legenda": "palavra"`, os `destaques` do roteiro e os 28 planos (frases com `cont: true` quando um plano visual cobre duas frases; planos de 2 a 4 s). `node ../../motor/build.mjs` gera `build-out.json` com o início e a duração de cada plano.
4. **Cena no Blender:** `desvendando-ideias/motor/blender/cena_dedo.py` (bpy), lendo os planos de `build-out.json` (exportar para `producoes/005-estalar-dedos/blender/planos.json`) e animando por quadro a 30 fps.
   - Visual da referência: fundo azul-petróleo em degradê com vinheta (e marrom-escuro nas cenas de pele, vinho no fim); osso marfim fosco; raio-X = osso azul translúcido com Fresnel brilhando; cartilagem azul-clara brilhante; cápsula translúcida; líquido sinovial amarelado; músculos vermelho-salmão; bolha de gás com reflexo; profundidade de campo leve; desfoque de movimento.
   - Personagem do canal recriado em bpy pela especificação de `motor/3d/cena.js` (cabeça cúbica com rosto, cabelo castanho espetado, moletom preto com nuvens vermelhas de borda branca, calça jeans), com mãos de 5 dedos articuladas (3 falanges por dedo, 2 no polegar) para estalar, mexer os dedos e comemorar.
   - Uma câmera por plano (os movimentos estão na tabela do roteiro); cortes secos, sem transição.
   - Quadros PNG em `producoes/005-estalar-dedos/blender/frames/` (fora do git) → `blender/fundo.mp4` com ffmpeg.
5. **Camada de cima (HyperFrames, fundo transparente):** legenda palavra a palavra (top 1250, 104 px, destaques amarelos), pílulas, títulos, medidor de pressão, relógio de 20 min, cartão dos 215 pontinhos com carimbo, contador "60 ANOS", cartão do perfil com "Seguir → Seguindo". Use as receitas existentes (`ovHTML` pill/tag, `stopwatch`, `vsBars`) e crie no `build.mjs` um `modo: "blender"` que omite o canvas 3D e põe `blender/fundo.mp4` como `<video muted>` de fundo, ou renderize a camada em `--format mov` e sobreponha com ffmpeg. Prefira o primeiro (um só render).
6. **Som:** `motor/sfx.py` com os sons de objeto da tabela (estalo, vidro, madeira, raspar, gota, carimbo, festa, pop); **sem som de troca de cena** (decisão 34). Mix final em −14 LUFS.
7. **Checagem:** `node ../../motor/checar.mjs --full`; `npx hyperframes check`; olhar quadros de todos os planos (`npx hyperframes snapshot`) antes de entregar.
8. **Capas:** 3 opções 1080×1920 com o conteúdo entre y 340–1580 e x 90–990 (zona segura do feed): A "Estalar os dedos dá artrite?" com o personagem e a mão em raio-X; B "CREC! O que é esse barulho?" com a bolha; C "Montei um dedo do zero" com o dedo montado. `capa/` do projeto.
9. **Entrega:** `renders/005-estalar-dedos.mp4` (1080×1920, 30 fps, H.264 + AAC), as 3 capas e as legendas do roteiro. Atualize o status no roteiro, commite o código e os PNG das capas e dê push (vídeo e quadros fora do git). Avise o usuário para me mandar o vídeo pelo chat da nuvem se quiser revisão.

## Regras do canal
- Planos de 2 a 4 s; legenda e títulos dentro da zona segura; nada de "cura", "garantido" ou "faz bem".
- Na tela, o aviso "Se doer ou inchar, procure um médico" no plano 26.
- Nunca gravar chave de API em arquivo, log ou commit. Não usar Higgsfield.

## Pronto quando
O usuário aprovou o corte de teste e recebeu o vídeo final, as capas e as legendas, tudo commitado e com push.
