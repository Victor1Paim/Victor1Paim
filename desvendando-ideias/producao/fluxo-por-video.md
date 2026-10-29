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

## Portões de decisão (nada avança sem a sua escolha)

Lição do vídeo 001 (29/10/2026): o Claude escolheu sozinho o hook, a ordem das cenas, o CTA, a mensagem final e a próxima ideia, e só depois mostrou. Daqui para a frente
**cada portão abaixo é uma pergunta com 3 a 4 opções, e a produção só segue depois da resposta**. Sem resposta, o Claude para; não escolhe por padrão.

| Portão | Antes de | Opções que o Claude traz | Você decide |
|---|---|---|---|
| 1. Tema e ângulo | Roteiro | 3 temas ou 3 ângulos do mesmo tema | O tema e a "pegadinha" do vídeo |
| 2. Hook | Roteiro | 3 a 5 aberturas de tipos diferentes | O hook (ou uma mistura) |
| 3. Ordem das cenas | Roteiro completo | 2 a 3 ordens (ex.: pegadinha cedo ou tarde; escala primeiro ou conta primeiro), cada uma em uma linha de storyboard | A ordem |
| 4. CTA | Roteiro completo | 3 opções (seguir, comentar uma pergunta, salvar/compartilhar) | O CTA |
| 5. Mensagem final e gancho | Roteiro completo | 3 fechos (pergunta aberta, próxima parte, desafio) | O fecho e **qual será o próximo vídeo** |
| 6. Roteiro aprovado | Voz | Roteiro final em texto corrido, com a contagem de palavras | "Aprovado" ou o que mudar |
| 7. Corte de teste | Render final | Vídeo rascunho (baixa qualidade) e lista do que o Claude mudaria | O que ajustar |
| 8. Publicação | Postar | Legenda, capa, hashtags, horário (2 opções de cada) | As escolhas |

Regras: a pergunta traz o texto exato (não resumo); uma pergunta por portão; o Claude registra a escolha na ficha do roteiro (`roteiros/NNN-tema.md`, seção "Decisões") com data.
O rascunho renderizado antes de uma decisão é só para você ver e **não vale como aprovação**.

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
