# Saúde sem Sermão — Plano do canal

Versão 2 (08/11/2026). O que ainda está **a definir** depende de decisão sua.

| Plataforma | Perfil | Formato principal |
|---|---|---|
| TikTok | @saudesemsermao | Curto, 30s a 1m30 |
| Instagram | @saudesemsermao | Reels, 30s a 1m30 |
| YouTube | @saudesemsermao | Shorts, 30s a 1m30 |

---

## 1. Posicionamento

**Promessa:** o que a ciência diz sobre hábitos e saúde do dia a dia, explicado sem bronca, sem culpa e sem milagre.

**Tom:** amigo bem informado, não professor nem médico dando sermão. Humor leve, zero terrorismo ("isso vai te matar"), zero vergonha do corpo ou do hábito de quem assiste. Mostra o custo-benefício real e deixa a pessoa decidir.

**Assinatura (em desenvolvimento — opções e roteiros de exemplo em `assinatura.md`):**
- Fechar cada vídeo com "o mínimo que já ajuda" (o passo menor e realista, não o ideal).
- Um selo de força da evidência: **Forte · Moderada · Fraca · Mito**.
- Quadro "Sermão x Realidade": o conselho exagerado que todo mundo ouve versus o que os estudos mostram.

## 2. Pilares de conteúdo

1. **Mito x verdade** — ovo, café, glúten, 8 copos de água, "detox". Maior potencial de comentário.
2. **Sono, energia e cabeça** — sono, estresse, foco, cansaço.
3. **Comida sem culpa** — rótulos, ultraprocessados, dietas da moda, sem demonizar alimento.
4. **Movimento possível** — exercício para quem odeia exercício, o mínimo que funciona.
5. **Corpo explicado** — por que dá soluço, cãibra, ressaca, ronco. Curiosidade com utilidade.

Regra de equilíbrio: nenhum pilar passa de 40% do calendário do mês.

## 3. Formatos

Duração: **30s a 1m30**. Temas que pedem mais detalhe viram **Parte 1 / Parte 2** (a Parte 1 termina com um gancho real para a Parte 2, e a Parte 2 abre com 3s de recapitulação).

| Formato | Duração | Uso |
|---|---|---|
| Relâmpago | 30–45s | 1 mito derrubado ou 1 dica com motivo |
| Explicado | 60–90s | Hábito + o que os estudos dizem + o mínimo que ajuda |
| Sermão x Realidade | 60–90s | Conselho exagerado comparado com a evidência |
| Série em partes | 2 × 60–90s | Tema grande dividido em Parte 1 e Parte 2 |

Estrutura base:
1. **0–3s:** gancho (o conselho que todo mundo ouve, ou uma contradição). Sem "olá".
2. **3–10s:** a dúvida que o vídeo resolve.
3. **Meio:** 2–4 beats, cada um com uma informação nova.
4. **Virada:** "na verdade…" perto de 70% do vídeo.
5. **Fim:** o mínimo que já ajuda, e a ressalva quando houver ("se tem X, fale com seu médico").

## 4. Rigor e segurança (inegociável em saúde)

- Toda afirmação tem fonte anotada no roteiro. Preferir revisões sistemáticas, diretrizes (OMS, Ministério da Saúde, sociedades médicas) e artigos revisados por pares. Um estudo isolado nunca vira regra.
- Dizer a força da evidência. Correlação não é narrada como causa.
- **Não** prescrever remédio, dose, suplemento ou tratamento, e não sugerir parar tratamento. Informar, não substituir consulta.
- Temas sensíveis (transtornos alimentares, saúde mental, gravidez, doenças graves) só com cuidado extra no tom e indicação de onde buscar ajuda (ex.: CVV 188).
- Sem antes/depois de corpo, sem promessa de emagrecimento, sem venda de produto milagroso.
- Conferir as políticas das plataformas para **informação médica** e para **conteúdo gerado por IA**. Saúde é a categoria em que desinformação mais derruba alcance e monetização.
- **Revisão por profissional de saúde:** todo roteiro passa por um profissional antes da gravação. Registrar no roteiro quem revisou e quando. Nome e registro profissional a definir.
- Erro corrigido em comentário fixado e, se grave, no vídeo.

## 5. Cadência sugerida

Começar com **3 a 5 curtos por semana**, constante, e subir depois. Produção em lote: um dia para pesquisa e roteiros, um para voz e imagens, um para montagem e agendamento.

## 6. Regras técnicas

- Vertical **9:16, 1080×1920**, 30 fps, margens de segurança para a interface.
- Legendas queimadas no vídeo, grandes, com palavras-chave destacadas.
- Fontes na descrição ou no comentário fixado.

## 7. Identidade visual e sonora (a definir)

- **Nome:** Saúde sem Sermão · **@saudesemsermao** nas três plataformas.
- **Paleta e tipografia:** cores claras e acolhedoras, longe do visual "hospital" e do visual "alerta vermelho". Uma fonte só para título e legenda.
- **Voz:** sintética, via **API do Gemini** (`gemini_tts` do OpenMontage). Uma voz fixa, calorosa e informal; testar 3 opções e fixar uma.
- **Imagem:** ilustração e motion graphics próprios; sem imagens de doença chocantes.

## 8. Produção (reaproveitando o que já existe no repo)

- **Montagem:** Remotion, como no Halftone (`halftone/`).
- **Mídia:** via skill `openmontage`. Voz no **Gemini**, imagens na **OpenAI** (GPT Image). Sem Higgsfield (regra do projeto).
- **Pesquisa de pauta:** **Grok** para assuntos da atualidade (o que está em alta em saúde). O Grok só sugere o tema; a checagem é feita nas fontes primárias (seção 4). Prompt pronto em `pautas/pesquisa-grok.md`.
- **Skills de apoio:** `ig-reel`, `ig-caption`, `ig-plan`, `ig-human` (roteiro, legenda, semana, tirar cara de IA); `bang-motion` e `hyperframes` (motion); `brainstorming` e `writing-plans` (planejar).
- **Pastas:** `pautas/` (banco de ideias com gancho, pilar, formato e fontes), `roteiros/` (um arquivo por vídeo), `producoes/` (finalizados e apoio).
- **Fluxo:** pesquisa no Grok → pauta → checagem nas fontes → roteiro → revisão do profissional de saúde → voz (Gemini) → imagens (OpenAI)/motion → montagem → checagem → publicação.

## 9. Fases

| Fase | Entrega | Critério para avançar |
|---|---|---|
| 0. Setup | @, identidade (paleta, fonte, voz), modelo de vídeo | Um vídeo-teste aprovado por você |
| 1. Piloto | 10 curtos variando pilares e formatos | Ver quais retêm mais |
| 2. Ritmo | Cadência estável, calendário mensal | 30 dias sem atrasar |
| 3. Ajuste | Dobrar nos pilares e formatos que funcionaram | Métricas abaixo |

## 10. Métricas

Retenção média e % que assiste até o fim, compartilhamentos e salvamentos (forte sinal em conteúdo útil), seguidores por vídeo. Decidir pelo conjunto de 10 vídeos, não por um isolado.

## 11. Decisões

Já decididas (08/11/2026): @saudesemsermao; voz sintética no Gemini; imagens na OpenAI; revisão por profissional de saúde; curtos de 30s a 1m30 com Parte 2 quando preciso; pesquisa de atualidade no Grok.

Em aberto:
1. Assinatura do canal (em desenvolvimento).
2. Rosto aparece ou não?
3. Quem é o profissional de saúde revisor.
4. Paleta, fonte e a voz escolhida entre as 3 do teste.
5. Primeiros 10 temas do piloto.
