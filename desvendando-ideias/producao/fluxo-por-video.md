# Fluxo de produção por vídeo (rascunho para refinar juntos)

Em cada etapa o Claude traz **opções** e você escolhe; o que for escolhido fica registrado na ficha do vídeo
(`roteiros/NNN-tema.md`). Rascunho: ajustar depois da pesquisa dos hooks e do primeiro vídeo-piloto.

| # | Etapa | Claude propõe | Você decide | Skill / ferramenta | Custo |
|---|---|---|---|---|---|
| 1 | **Tema e fontes** | 3 temas do calendário com fontes oficiais já achadas e o risco de cada | Qual tema | pesquisa na web; `deep-research` só em tema difícil | texto |
| 2 | **Hooks** | 3 a 5 aberturas (tipo do catálogo, primeira frase, o que aparece na tela, por que retém) | Qual hook (ou mistura) | catálogo de hooks | texto |
| 3 | **Roteiro 70–85 s** | Roteiro por beat com marcação de movimento do dicionário, números e a fonte de cada um | Aprovar ou pedir ajustes | `dicionario-de-movimento.md` | texto |
| 4 | **Checagem de fatos** | Lista de afirmações com 2 fontes (saúde/finanças) e o que ficou sem fonte | Remover ou aprovar o que falta | regra 12 de `decisoes.md` | texto |
| 5 | **Voz** | Texto dividido por cena, teste de 1–2 frases, depois lote | Aprovar a voz do teste | `gemini-midia` (simulação, depois `--go`) ou VoiceStudio | centavos; cache evita repetir |
| 6 | **Montagem** | Composição Remotion do template com os movimentos do roteiro; 3 frames-chave para conferir | Aprovar o visual ou pedir troca de transição | Remotion (`remotion-*`), `ffmpeg` | zero (código) |
| 7 | **Revisão final** | Conferência: duração ≥ 61 s, legenda, fonte na tela, hook nos 3 s, sem marca d'água | Aprovar | script de checagem (a criar) | zero |
| 8 | **Publicação** | Legenda do post, capa, 3–5 hashtags, comentário fixado, horário; versão para Reels e Shorts | Escolher a legenda | modelo de legenda | texto |
| 9 | **Resultado** | Leitura das métricas (saída em 3 s, retenção, compartilhamentos, seguidores por vídeo) e o que mudar no próximo | Decisões de manter/trocar hook ou tema | plano de teste de `decisoes.md` | texto |

## Opções que o Claude sempre apresenta

- **Hooks:** 3 a 5 por vídeo, de tipos diferentes, para testar.
- **Transições:** 2 combinações do dicionário para o beat da virada.
- **Variações A/B:** mesmo roteiro com hook ou capa diferente, quando valer o teste.
- **Melhorias após o 1º corte:** onde cortar 2–3 s, onde a retenção deve cair, o que simplificar.

## Para refinar depois

1. Template Remotion vertical (1080×1920) com legenda, fonte na tela e os movimentos do dicionário.
2. Script de checagem automática (duração, legenda, resolução, áudio) como o `checar` do Halftone.
3. Modelo de roteiro e de legenda do post.
4. Uso das skills por etapa com custo (próximo passo combinado).
