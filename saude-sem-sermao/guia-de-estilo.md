# Guia de estilo — Saúde sem Sermão

Extraído em 08/11/2026 dos vídeos publicados **002 "Treinar 2× por semana adianta?"** (52s) e **004 "Musculação deixa a mulher grande demais?"** (60s). Todo vídeo novo segue este guia; o que mudar aqui muda em todos.

## 1. Os dois personagens

| | Narrador | Tico |
|---|---|---|
| Quem é | O locutor que explica a ciência | O telespectador: tem as dúvidas que o público tem |
| Aparece? | Só a voz | Coração ilustrado com estetoscópio (mascote do canal), em quase toda cena |
| Voz | Masculina, grave, calma (tom médio ~100 Hz) | Mais aguda e leve (~155–180 Hz), curiosa, um pouco ingênua |
| Fala | Frases curtas, uma informação por frase, com número e fonte | Frases de 2 a 6 segundos, coloquiais ("Ué, mas…", "Minha tia…", "Só uma horinha?") |
| Na tela | Legenda em caixa branca no meio da tela, palavra-chave em laranja | Balão "PERGUNTA DO TICO"; no fim, "O QUE O TICO ENTENDEU" |

**Papel do Tico (regra):**
1. **Logo após o gancho**, traz o problema para a vida real, com a objeção do público ("Eu só consigo ir duas vezes… nem adianta?", "Minha tia não pega peso com medo de ficar grandona").
2. **No meio**, faz 1 pergunta de dúvida ou surpresa que puxa o próximo bloco ("Ué, mas osso não fica frágil?", "Só uma horinha por semana?").
3. **No fim**, faz o **resumo** em 1 frase, com as palavras dele ("Entendi! Peso não deixa grandona, fortalece o osso e ainda cuida do coração. O bíceps é só o brinde!"). O narrador confirma com 2–3 palavras ("Resumiu bem.").
4. O Tico nunca dá informação técnica nova, nunca está "certo" no lugar do narrador e nunca é ridicularizado. Ele é o público.

## 2. Estrutura do vídeo (45–60s)

| Tempo | Bloco | Quem | Tela |
|---|---|---|---|
| 0–3s | **Gancho**: a pergunta do título | Narrador | Capa verde-escura, título serifado com palavra em itálico mostarda, ícone grande, selo laranja (`2×`, `?!`) |
| 3–8s | **Objeção da vida real** | Tico | Fundo creme, Tico grande, balão "PERGUNTA DO TICO" |
| 8–40s | **2 a 4 blocos de informação** (ou "Mito 1/3, 2/3, 3/3") | Narrador; Tico entra 1× no meio | Título do bloco + infográfico simples + fonte em letra pequena + legenda; Tico pequeno no canto inferior direito reagindo |
| 40–50s | **Resumo do Tico** + confirmação do narrador | Tico → Narrador | Balão "O QUE O TICO ENTENDEU", texto aparecendo palavra por palavra |
| últimos 4–5s | **CTA**: "Curtiu? Então segue a gente pra ver mais." | Narrador | Fundo laranja, card do perfil @saudesemsermao com botão "Seguir → Seguindo ✓" e cursor, confete; aviso "Conteúdo educativo, não substitui orientação profissional." |

Formato de mitos: rótulo **✕ MITO** + contador **1/3**, fundo laranja, e o desmentido em fundo claro. Formato de evidência: rótulo **✓ CIÊNCIA**.

## 3. Identidade visual

- **Vertical 1080×1920, 30 fps.**
- **Paleta** (amostrada dos vídeos):
  - Verde-escuro `#2F483A` (capa e botão "Seguindo")
  - Laranja terracota `#D45F2B` / `#CE6840` (destaque, mitos, CTA, Tico)
  - Creme `#FDF3ED` / `#F2ECE2` (fundo das cenas do Tico)
  - Branco `#FFFFFF` (fundo dos infográficos)
  - Verde-sálvia `#95A185` (selos "mesmo %", "↑ coluna", "30–60 min/semana")
  - Cinza quente `#8C8580` (barra de comparação)
  - Mostarda (palavra em itálico na capa)
- **Tipografia:** título em **serifada** com 1–2 palavras em *itálico laranja* ("Osso *mais denso*", "Séries > *dias*"); legenda e rótulos em **sem serifa arredondada, negrito**.
- **Legenda:** caixa branca de cantos arredondados, à esquerda, no terço inferior; 1–2 linhas; palavras-chave em laranja.
- **Infográficos:** formas planas, poucas cores, um conceito por tela (barras, relógio, calendário S-T-Q-Q-S-S-D, prancheta com checks, osso, espelho). Animação de construção (barra sobe, ponteiro gira, check aparece).
- **Fonte científica sempre na tela**, abaixo do gráfico, em cinza pequeno: "Fonte: Autor et al., Revista, Ano".
- **Tico:** 2 tamanhos (grande nas falas dele, pequeno no canto nas falas do narrador), com expressão que reage ao conteúdo (surpreso, pensativo, acenando, punho para cima).

## 4. Som

- Música de fundo contínua, baixa, do começo ao fim (não há silêncio absoluto em nenhum ponto).
- Narrador e Tico nunca falam por cima um do outro; ~0,5s de respiro entre as falas.

## 5. Texto do roteiro

- Linguagem falada: "pra", "tá valendo", "grandona", "Ué".
- Uma ideia por frase. Número sempre com unidade e contexto ("30 a 60 minutos de força por semana").
- Sem bronca: a conclusão é sempre o "mínimo possível" ("Qualquer treino ganha de nenhum treino", "Então terça e sexta tá valendo").
- Ressalva quando couber ("Exemplo geral, não é prescrição").

## 6. Pontos a corrigir nos próximos vídeos

Achados na transcrição com o Whisper e na análise quadro a quadro:

1. **Pronúncia:** no 004, a voz soou como **"Penso** não deixa grandona" (era "Peso"). Uma palavra trocada num canal de saúde tira credibilidade. Passar toda narração pelo `scripts/voz_gemini.py`, que confere com o Whisper.
2. **Final do 004:** o Whisper ouviu **"Chico, curtiu?"**. Conferir se a fala é "Tico, curtiu?" e se está clara.
3. **Rótulo inconsistente:** no 002, o resumo final do Tico ("Então…") aparece como "PERGUNTA DO TICO"; no 004 está certo ("O QUE O TICO ENTENDEU"). Usar sempre "O QUE O TICO ENTENDEU" no resumo.
4. **Resumo do 002 curto demais:** "Então terça e sexta tá valendo" não resume o vídeo. O padrão do 004 (3 ideias em 1 frase + piada leve) é o modelo.
5. **Aviso legal:** o 004 tem "Conteúdo educativo, não substitui orientação profissional" no CTA e o 002 não tem. Pôr em todos.
6. **Fonte "ACSM, 2026":** conferir a referência exata (título do documento e ano) antes de reutilizar; anotar no roteiro.

## 7. Voz no Gemini (para os próximos)

- **Narrador:** voz masculina grave e calma. Dos testes de 08/11, **Achird** e **Puck** são masculinas; testar também vozes mais graves (ex.: **Charon**, **Orus**, **Algenib**).
- **Tico:** voz mais aguda e leve, diferente o bastante do narrador para o público distinguir de olhos fechados (ex.: **Puck**, **Leda**, **Zephyr**). Gerar as falas do Tico separadas das do narrador e montar na linha do tempo.
- Gemini TTS aceita **2 vozes no mesmo pedido** (multi-speaker), útil para diálogos narrador ↔ Tico.
