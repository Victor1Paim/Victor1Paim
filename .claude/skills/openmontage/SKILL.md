---
name: openmontage
description: Produce Halftone assets with OpenMontage (agentic video production system, vendored as a git submodule in ferramentas/OpenMontage) - illustrated plates (placas), character reference sheets, covers, narration/TTS, music and sound effects, style tests. Use when the user asks to generate images, plates, voices, music or a style test for the Halftone / Ano Zero project, or mentions OpenMontage / "Open Montage".
---

# OpenMontage no projeto Halftone

OpenMontage está em `ferramentas/OpenMontage` (submódulo, AGPLv3). Ele gera e organiza mídia;
a montagem final dos episódios continua no Remotion em `halftone/` (ou HyperFrames, se o usuário pedir).

## Antes de qualquer coisa

1. Leia `ferramentas/OpenMontage/AGENT_GUIDE.md` (regras do OpenMontage: todo trabalho passa por um pipeline,
   leia o "stage director" de cada etapa, anuncie ferramenta/provedor/modelo/custo antes de gerar).
2. Se a pasta estiver vazia: `git submodule update --init --depth 1 ferramentas/OpenMontage`.
3. Dependências: `scripts/preparar-sessao.sh` (submódulo, `npm ci` do Remotion, `pip install` do OpenMontage).
4. Chaves de provedor vêm de variáveis de ambiente (veja `ferramentas/OpenMontage/docs/PROVIDERS.md`).
   Nunca peça para colar chave no chat; peça para cadastrar nas configurações do ambiente.
   **Não use Higgsfield** neste projeto (decisão do usuário).

## Fonte da verdade criativa

- Bíblia: `halftone/series/ano-zero/biblia.md` — fichas visuais em inglês (seção 4), cenários (seção 5),
  trecho fixo de estilo (seção 9.5), paleta (9.2). Use os trechos fixos **literalmente** em todo prompt.
- Plano-mestre: `halftone/docs/plano-mestre-novela-tiktok.md` — capas (seção 8), pipeline (seção 9).
- Regras: sem texto/letras/logos na arte, sem gore, sem fotorrealismo, nada de emissora/marca real,
  Libras nunca desenhada (mãos fora do quadro, de costas ou desfocadas).

## Onde salvar o que for gerado

O Remotion só lê arquivos de `halftone/public/`. Os nomes seguem o `ep.json` (campo `placas`):

| Tipo | Caminho |
|---|---|
| Personagem / pose | `halftone/public/series/ano-zero/personagens/<personagem>/<pose>.png` |
| Cenário (fundo, meio) | `halftone/public/series/ano-zero/cenarios/<cenario>/<camada>.png` |
| Arte de capa | `halftone/public/series/ano-zero/t1/epNN/capa-arte.png` |
| Narração / falas | `halftone/public/series/ano-zero/t1/epNN/audio/*.mp3` (referenciar em `narracao[]` do ep.json) |

Placas são 1080×1920 (9:16). Camadas de personagem/primeiro plano em PNG com fundo transparente.
Guarde o prompt usado ao lado (`<nome>.prompt.txt`) para o arquivo do episódio (checklist de conformidade).

Depois de salvar: `cd halftone && npm run placas` (atualiza o manifesto) e renderize um quadro para conferir:
`npx remotion still src/index.ts <Composição> out/x.png --frame=N`.

## Teste de estilo (bíblia 9.5)

3 quadros: Bia na multidão · Caio sem som · um eco no calçadão. Gere como amostra (sample), mostre ao
usuário e só depois faça lote.
