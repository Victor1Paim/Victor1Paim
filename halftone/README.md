# Halftone · Séries em capítulos

Projeto Remotion do canal **Halftone** (@halftone.tv1). Primeira série: **Ano Zero · T1 A Virada**.
Documentos de referência: [`docs/plano-mestre-novela-tiktok.md`](docs/plano-mestre-novela-tiktok.md) e [`series/ano-zero/biblia.md`](series/ano-zero/biblia.md).

## Rodar

```bash
npm install
npm run dev                     # Remotion Studio (atualiza o manifesto de placas antes)
npm run checar -- series/ano-zero/t1/ep01/ep.json   # checklist automático do episódio
npm run render:ep -- src/index.ts AnoZero-T1-Ep01 out/ep01.mp4
npm run still -- src/index.ts AnoZero-T1-Ep01-Capa out/ep01-capa.png
npm run svg:marca               # regenera marca/avatar.svg e marca/logo.svg
```

Saída: 1080×1920, 30 fps, H.264. Fontes locais em `public/fonts` (OFL), então o render não depende de rede.

## Estrutura

```
marca/            marca.ts (nome, handle, cores, fontes) · simbolo.ts (geometria do avatar) · logo.svg · avatar.svg
series/ano-zero/  biblia.md · paleta.ts · t1/epNN/{roteiro.md, ep.json, audio/} · t1/teste-tecnico/ep.json
public/           marca/ (PNGs do pacote de marca) · fonts/ · series/ano-zero/{personagens,cenarios}/ (placas)
src/components/   Placa, Cena, LuzCena, Nevoa, Particulas, Reticula, AneisSom, TiqueEco, Relogio,
                  CartaoSessao, Rebobina, TelaCelular, Legenda, LegendaLibras, MomentoDecisao,
                  HalftoneApresenta, SeloFiccao, CTAFinal, SimboloHalftone, Logotipo
src/compositions/ Episodio (lê ep.json), Capa, Trailer, Avatar, DestaqueIG
scripts/          manifesto-placas.mjs · checar-ep.mjs · gerar-svg-marca.mjs
```

> As imagens ficam em `public/` porque o Remotion só serve arquivos de lá. Os dados (`roteiro.md`, `ep.json`) ficam em `series/`, como no plano-mestre.

## Composições

| ID | O que é |
|---|---|
| `AnoZero-T1-TesteTecnico` | Trecho técnico de 15 s: Libras, celular, anéis, sessão do Caio, Momento Decisão |
| `AnoZero-T1-Ep01` / `-Capa` | Ep. 1 "A mão" (rascunho) e sua capa |
| `AnoZero-Trailer` | Trailer de 25 s (bíblia, seção 13) |
| `Avatar`, `Avatar-Simplificado` | Avatar 1080×1080 gerado por código |
| `Destaque-*` | Capas de destaque do Instagram |

Episódio novo: criar `series/ano-zero/t1/epNN/ep.json` e adicionar uma linha em `src/Root.tsx`.

## ep.json

Formato em [`src/tipos.ts`](src/tipos.ts). Tempos em segundos do vídeo.

- `placas`: do fundo ao primeiro plano. `"rafa/pose-ombro"` → `public/series/ano-zero/personagens/rafa/pose-ombro.png`; nomes que não são personagem vão para `cenarios/`. **Placa que ainda não existe aparece como rascunho** (silhueta + nome), então dá para montar e cronometrar antes da arte.
- `legendas[].tipo`: `narrador`, `dialogo`, `pensamento`, `libras`, `som`. `inicio`/`fim` relativos à cena.
- `som[]` com `aneis: true` desenha anéis vermelhos em `x`,`y` (0–1) no ritmo de `bpm`. `tiqueEco` aplica o tique seco a uma camada.
- `celular`: `chamada`, `videochamada`, `mensagem`, `alerta`, `chamada-recusada` — sempre fictícios.
- `momentoDecisao`: congela a imagem (`<Freeze>`) por 1,5–2 s com A/B. Deixe a cena seguir por baixo; a parte congelada não aparece.
- `cartaoSessao`, `rebobina`, `apresentaEm` (padrão 3 s, sempre depois do gancho).
- Áudio: `narracao[]` e `som[].arquivo` apontam para arquivos em `public/`.

O `npm run checar` confere duração (1:05–1:20), palavras por camada (125–160 no total), gancho, legendas sobrepostas ou rápidas demais (> 3,2 palavras/s) e o tempo do Momento Decisão.

## Pendências (plano-mestre, seção 15)

1. **Teste de estilo** (3 quadros) com Open Montage / Hyper Frames — as skills não estão instaladas nesta sessão.
2. Vozes no ElevenLabs (bíblia, seção 6.3).
3. Custo de imagem das skills.
4. Banco de trilha e efeitos.
5. Revisão das falas em Libras por pessoa surda.
