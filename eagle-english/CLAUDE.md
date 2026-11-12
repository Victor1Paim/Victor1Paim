# Eagle English BR – Produção de vídeos

Você produz vídeos curtos (Reels/TikTok) para @eagle.english.br. Regras de conteúdo,
identidade, pronúncia e CTA de produto: `docs/EAGLE_ENGLISH_PROJETO_COMPLETO.md`
(PARTE 4, seções 2, 6 e 12). Estado atual da fila: `docs/estado.md`.
Passo a passo do projeto (quem faz o quê): `docs/PASSO_A_PASSO_EAGLE_ENGLISH.md` (seção 2).

Idioma de trabalho com o usuário: português do Brasil, direto e curto.

## DIREÇÃO EDITORIAL V3 (09/11/2026) — `docs/PROMPT_MESTRE_V3.md`

70% A1 / 25% A2 / 5% B1; temas do dia a dia (rotina, casa, lazer, comida, sentimentos, vocabulário fácil);
evitar burocracia/bancos/reclamação formal. Legendas no formato V3 (5 hashtags, sem #eagleenglish).
**Vídeo sempre abre em PORTUGUÊS com o mascote GRANDE no centro falando com quem assiste** (gancho/convite
para se testar); o inglês vem nas frases, e toda frase/resposta em inglês ganha a tradução falada em português.

Ganchos, re-ganchos, CTAs e legendas: escolher da biblioteca adaptada `docs/GANCHOS_E_COPY.md`
(uma ação de engajamento por vídeo; pausa para repetir com `"pausa_repetir": 1.2`).

## RETENÇÃO (10/11/2026) — `docs/RETENCAO.md` (manda sobre os outros guias de roteiro)

Todo vídeo: UMA estrutura declarada (Contradição, Problema, Escolha, Evolução ou Jornada — sem misturar), uma
PERGUNTA ABERTA em até 3 s que só o final responde, virada perto de 70%, o melhor por último, fecho que ecoa a 1ª
frase, CTA só depois da entrega, progresso visível ("3/6"). Antes de produzir, escrever `posts/<post>/roteiro.md`
no formato do guia e passar o checklist. Contradições têm que ser verdadeiras.

## PADRÃO VISUAL (manda sobre o resto deste arquivo)

Todo vídeo segue `docs/PADRAO_VIDEO.md` (medido nos Reels publicados): foto do cenário em cor cheia,
mascote OFICIAL grande falando (`assets/mascote/oficial/`), legendas Poppins com contorno (inglês amarelo,
pronúncia branca, tradução verde), cartão de ponte, telas do ebook e a oferta fixa
(`assets/marca/fechamento_oferta.mp4`). Montagem: `scripts/montar_padrao.py`. Os templates `quiz.html`,
`card_*.html` e os mascotes `assets/mascote/pensando.png`/`positivo.png` são do visual antigo: não usar.

## CAPA (10/11/2026)

Capa produzida: `posts/<post>/capa.json` → `python3 scripts/capa.py posts/<post>` (template `templates/capa.html`): foto do
cenário, selo vermelho ("6 frases"/"Teste rápido"/"5 rodadas"), título Poppins com contorno (palavra-chave em amarelo),
pílula marinho, balão com uma frase em inglês + pronúncia (Repita) ou 4 figuras com "?" (Flashcard/Qual você usa?), mascote
oficial com contorno branco e brilho. Tudo importante entre y 260 e 1640 (recorte 3:4 da grade). `montar_padrao.py` usa
a capa produzida sempre que existir `capa.json`. Não revelar respostas de teste na capa.
**Abertura animada (motion graphics, 10/11):** mesma linguagem da capa, em movimento (selo cai, título pula, figuras voam
pra dentro e flutuam, faixa amarela do DESAFIO pulsa, mascote sobe e fala; nos últimos 0,6 s tudo voa pra fora + whoosh).
`templates/abertura.html` + `scripts/abertura.py` (quadro a quadro, 30 fps, ~2,5 min de render). No `flash.json`, a chave
`"abertura"` substitui a `"intro"` parada (exemplo: `posts/2026-11-12_flashcard-frutas/`). Gancho falado em tom de desafio.

## TESTE: ANÚNCIO UGC DE AFILIADO (10/11/2026)

Bloco de 10–13 s logo depois da abertura, ligado ao tema do vídeo (molde de Natal → "Natal em inglês"). `posts/ugc-molde-natal/`:
fotos do produto geradas no gpt-image-2 COM as fotos da loja como referência (`imagem_gemini.py --ref a.jpg,b.jpg`), animadas
por `scripts/montar_ugc.py` (zoom/deslize, tremido de celular, xfade, camada `templates/ugc.html` com PUBLI + aviso de IA).
Regras: selo PUBLI e #publi, rótulo de conteúdo comercial e de IA no TikTok, nunca "eu comprei/testei", sem medidas/capacidade
(a página do vendedor se contradiz). Nesse teste o vídeo NÃO leva o CTA do Eagle 350 (CTA = link do produto).
Veo/Sora: nenhuma das chaves libera modelo de vídeo (10/11); se liberar, trocar o zoom das fotos por clipes animados.
Pesquisa: `docs/PROMPT_MANUS_UGC_MOLDE.md` → resultado `docs/pesquisas/manus-ugc-molde-natal-2026-11-10.pdf`:
ângulo família > lembrancinhas > versatilidade (sem "renda extra"/"parece de confeitaria"); publi de 8–10 s dentro da aula;
volta: "Agora, vamos descobrir essas formas em inglês!"; CTA "Toque no produto vinculado ao vídeo"; legenda com #publi +
comissão + "Algumas imagens deste vídeo foram geradas por IA". TikTok Shop BR proíbe demonstração falsa: molde idêntico ao
real em toda cena sintética e resultado final com as fotos reais da loja. Roteiros: `posts/2026-11-14_natal-p1/` e `-15_natal-p2/`.
Vídeo (Veo): pelo Flow (`docs/FLOW_PROMPTS_MOLDE.md`) ou API quando a chave liberar.

## Sempre

- Formato 1080x1920 (9:16), 30 fps, H.264 + AAC. **Duração padrão: 40 s a 1 min 10 s** (a partir das
  próximas produções; o D10 Salão segue o modelo antigo). Estrutura, ganchos, re-gancho aos 25–30 s e
  o CTA final novo: `docs/HOOKS_E_CTA_VIDEO.md` (manda sobre a seção 2.6 do passo a passo).
- Gancho nos 2 primeiros segundos (falado + texto na tela).
- Textos na tela renderizados a partir de templates HTML (`templates/`, via
  `scripts/render_cartoes.py`): texto exato, acentos certos, nunca escritos por gerador de imagem.
- Área segura: nada importante nos 250 px de cima, nos 400 px de baixo
  nem nos 150 px da direita (interface do TikTok/Reels).
- Narração em pt-BR; frases em inglês com voz americana (arquivo separado).
- Música a 10–15% do volume da voz; loudness final perto de -14 LUFS.
- Final obrigatório (seção 12.3 + `docs/HOOKS_E_CTA_VIDEO.md` seção 4): CTA falado de 6 a 9 s
  (ponte com o tema → o que recebe → "link na bio" + "manda pra quem…"/"comenta") + texto na tela de
  no máximo 2 linhas ("Eagle 350: 350 mapas + 4 bônus" / "Link na bio 👆").
- Entregar junto: `roteiro.md`, `legenda.md` (legenda terminando no bloco de CTA),
  comentário fixado e resposta curta para "eu quero".
- Fechar a entrega com "CTA incluído: sim" + checklist 12.7.
- Nunca: áudio do ebook, "grátis", preço sem pedido, urgência falsa, promessa de fluência,
  marcas reais, link escrito (sempre "link na bio").

## Frases

As frases vêm do ChatGPT (chat central) em `posts/AAAA-MM-DD_tema/frases.json`.
Não invente frases novas: só produza o vídeo das frases aprovadas. Pronúncia na convenção
da seção 6 (tônica em MAIÚSCULA, sem IPA).

## Ciclo de um vídeo (seção 2.5 do passo a passo)

1. `roteiro.md` com tempos e fala por cena (incluindo o CTA final).
2. Vozes com o **Gemini TTS**: `python3 scripts/vozes.py montar <post>` (cria `falas.json`;
   revisar gancho e CTA) e `python3 scripts/vozes.py gerar <post>`: um `.wav` por fala em `audio/`,
   narração pt-BR (voz Achird) e frases em inglês em arquivo separado (voz Kore), conferidas
   pelo Whisper (skill `whisper-legendas`).
3. Medir durações (`silencedetect`) e montar a linha do tempo (`adelay` + `amix`).
4. Renderizar os cartões HTML em PNG (`scripts/render_cartoes.py`).
5. Montar o vídeo com ffmpeg: fundo, cartões, mascote discreto, música baixa e efeitos.
6. Gerar `.srt` com o texto do roteiro e o tempo do Whisper (skill `whisper-legendas`;
   queimar na tela, se pedido).
7. Tela final de produto + CTA falado.
8. Exportar `video/final.mp4` + folha de contato (1 quadro por cena).
9. `legenda.md`: legenda + bloco de CTA + comentário fixado + resposta curta.
10. "CTA incluído: sim" + checklist.
11. Custo: `python3 ../scripts/custos.py relatorio <post>` e mostrar a tabela (US$ e R$) no fim.

## Quiz (formato B) – já automatizado

`posts/<post>/quiz.json` (perguntas, textos, ids das falas) + `falas.json` → `python3 scripts/vozes.py gerar <post>`
→ imagens (`scripts/imagem_gemini.py`: fundo 9:16 + mascote recortado; padrão OpenAI gpt-image-2) →
`python3 scripts/montar_quiz.py <post>` (cartões `templates/quiz.html`, tique/ding/whoosh, loudness, capa,
folha de contato). Primeiro exemplo: `posts/2026-11-10_quiz-pedir-de-novo/`.
Pronúncia: `pronuncia.json` → `python3 scripts/montar_pronuncia.py <post>` (grupo → "Sua vez!" → ouvir de novo → teste).
Escada de velocidade: `escada.json` → `python3 scripts/montar_escada.py <post>` (lenta/normal/nativo por atempo).
Flashcard "What is this called?" (ref. R1): `flash.json` → `python3 scripts/montar_flash.py <post>` (template `flash.html`;
as respostas podem vir numa fala só, cortada nas pausas; figuras numa grade 2x4 gerada de uma vez e recortada).
"Qual você usa?" (A×B, estrutura Escolha): beat `"escolha"` no `roteiro.json` do `montar_padrao.py` (img branca da cena num cartão,
opções A/B só em inglês, contagem 3-2-1 com tique, revela com ding, frase en + tradução; mascote médio embaixo). Exemplo:
`posts/2026-11-13_quente-ou-frio/`. Cabe em 70 s com 5 rodadas se as perguntas faladas forem curtas.
"Em inglês, como se diz…?" (ref. 12/11, `docs/REF_COMO_SE_DIZ.md`): beat `"comosediz"` no `montar_padrao.py` — começa direto na
1ª pergunta, 3 rodadas A/B/C, contagem 5→1, certa em verde + pronúncia, resposta falada 2x; fim com CTA curto (~30 s no total).
FUNDO EM VÍDEO (12/11): `"fundo_video": "maldivas"` no roteiro.json → quadros transparentes por cima de uma cena diferente por trecho
(biblioteca `assets/fundos/maldivas/` gerada por `scripts/fundos_maldivas.py` a partir do vídeo do Drive do usuário; os .mp4 ficam
fora do git). `"fundo_inicio": N` muda a primeira cena para não repetir entre vídeos. Capa: um quadro das Maldivas em `capa.json`.
MASCOTE ANIMADO (12/11): `assets/mascote/oficial/poses/{a,b,c}_{fechada,aberta}.png` (a = normal, b = asa acenando, c = asa baixa;
asas geradas por edição com máscara e coladas no desenho oficial). O `montar_padrao.py` balança o tronco com pivô nos pés e troca
a pose da asa a cada 0,6 s enquanto ele fala (não sobe e desce mais).
REAÇÕES (12/11): d = apontando para cima (início da pergunta), e = pensando, asa no queixo (contagem), f = joinha + olhos
felizes (revelação). O montar_padrao usa sozinho nos beats "comosediz" e "escolha"; nos outros, o "apontando" entra no ciclo.
Fundo Maldivas: 47 cenas (44 usáveis) — dá ~10 vídeos sem repetir cena; variar "fundo_inicio" a cada vídeo (ex.: +5).
ÁUDIO LIMPO (12/11): `vozes.py` apara cada fala pelo Whisper (silêncio antes da 1ª e depois da última palavra) + corta rajada final:
sem chiado/estalo entre as falas. Para falas antigas: `aparar_com_whisper(arq, lingua)`.
Falas sem áudio viram silêncio estimado (prévia). Mascote reutilizável em `assets/mascote/`.

## Vozes e cotas

**09/11 (tarde): o usuário passou uma chave do Gemini com créditos (plano pago): sem limite diário; imagem no Gemini liberada.**
(Histórico: antes disso, plano gratuito com 10 falas/dia por modelo.)

- Voz aprovada: Gemini **Achird nas DUAS línguas** (o usuário não quer voz feminina no inglês junto da masculina).
  pt no `gemini-3.8-flash-tts`, en no `gemini-3.8-flash-lite-tts` (ou `gemini-2.5-flash-preview-tts`). `velocidade_pt` 1.0 (não acelerar).
  Gancho: pergunta que cria situação e dúvida ("Se o telefone tocar em inglês… você sabe o que dizer?").
  A voz da OpenAI foi reprovada.
- Cota por dia (zera 05h em Brasília): 10 falas pt + 10 falas en → ~1 vídeo por dia. Reaproveitar o áudio
  do CTA quando o texto for idêntico. Planejar: prévia e parte das falas num dia, o resto no dia seguinte.

## Limites das APIs (plano gratuito do Gemini)

- TTS: 3 pedidos/min e 10 por dia POR MODELO (`gemini-3.8-flash-tts`, `-lite-tts`, `2.5-flash-preview-tts`).
  `vozes.py` espera o limite por minuto; no diário, use `--modelo gemini-3.8-flash-lite-tts --pular-existentes`.
- Imagem no Gemini gratuito: bloqueada (limite 0) → usar OpenAI (`gpt-image-2`, qualidade medium; high dá 502).
- Modelos 2.5 de TTS: frase curta vira "instrução" (erro 400); `vozes.py` prefixa "Say…" só nesses.
  Letras soltas na voz pt: escrever "tê", "dê".
- Nome do produto na voz pt: escrever "Ígol trezentos e cinquenta" para sair "Eagle 350".

## Lições técnicas (seção 6 do passo a passo)

- Rodar ffmpeg com `-nostdin` em loops e arredondar os tempos ("Invalid duration").
- Congelar 0,7 s antes de cada transição para evitar quadro preto.
- Voz pt-BR lê inglês errado: frases em inglês sempre em arquivo separado, voz americana.

## Ambiente

- Ferramentas: ffmpeg, Python (Pillow, pydub/numpy), Playwright/Chromium.
- Preparar no notebook: `bash scripts/preparar.sh`.
- Chave do Gemini: no notebook em `.env` (`GEMINI_API_KEY`); na nuvem como network secret
  (host `generativelanguage.googleapis.com`, header `x-goog-api-key`) com `GEMINI_API_KEY=proxy-injected`.
  Nunca no chat nem no git.

## Skills (pasta `.claude/skills` da raiz, as mesmas do branch `claude/awesome-cannon-sxprt5`)

- Vídeo: `hyperframes*`, `bang-motion`, `motion-doctrine`, `cut-the-curve`, `captions-overlay`,
  `remotion-*`, `ffmpeg`, `media-use`.
- Áudio/legenda: `whisper-legendas`, `speech-to-text`, `sound-effects`, `music`.
- Instagram/TikTok: `ig-reel` (gancho e roteiro), `ig-caption`, `ig-carousel`, `ig-story`, `ig-plan`,
  `ig-audit` (métricas), `ig-reply`/`ig-comment`/`ig-dm`, `ig-human` (tirar cara de IA do texto).
  As regras do projeto (seções 7 e 12) mandam sobre as das skills: 5 hashtags fixas, CTA Eagle 350,
  pronúncia na convenção. As `ig-*` guardam voz/plano em `~/.claude/instagram/`, que some na nuvem:
  copiar para `eagle-english/instagram/` o que valer guardar.
- Processo: `brainstorming`, `writing-plans`, `systematic-debugging`, `verification-before-completion`.
- Não usar Higgsfield.
