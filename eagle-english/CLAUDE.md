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
"Lista com emoji" (12/11): beats `"item"` (emoji, en, pron, pt, audio_en, audio_pt) + `"lista_fim"` no `montar_padrao.py` — a lista inteira
aparece desde o início com "?" e vai se completando (ideia da ref. "Prova de inglês"); item atual grande embaixo; mascote médio.
Exemplo: `posts/2026-11-15_objetos-do-quarto/`. TRADUÇÕES CURTAS (1–2 palavras): gerar TODAS numa fala só com pausas e cortar
(`cortar_respostas`), senão a voz escorrega para o espanhol. Pico > -1 dB é limitado sozinho no fim do montar_padrao.
"Prova de inglês" (15/11): beat `"prova"` (emoji, en, pron, pt, audio_q, audio_r) + `"lista_fim"` no `montar_padrao.py` — lista 1…N
vazia que se completa; "Como se diz X?" na tela + contagem 3-2-1 → resposta entra na lista. Perguntas e respostas: UMA fala
cada (todas juntas) cortada com `cortar_respostas`. Exemplo: `posts/2026-11-18_prova-roupas/`.
PRODUÇÃO NA MÁQUINA DA NUVEM (4 núcleos): rodar geração/conferência/montagem EM FILA (um script bash em segundo plano),
nunca em paralelo — o Whisper satura a CPU e os comandos estouram o tempo.
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

## PADRÃO NOVO (19/11/2026): "LISTA 12", SEM MASCOTE E SEM CTA DE PRODUTO

Pedido do usuário: copiar o estilo da referência do Drive (lista "Como se diz…?" de 12 itens com fundo de mar) para ver se o
engajamento sobe. `posts/<post>/lista.json` + `falas.json` → `python3 scripts/montar_lista12.py posts/<post>` (template
`templates/lista12.html`): selo do perfil vermelho no topo, palavra falada da vez em verde gigante (legenda palavra por palavra pelo
Whisper), lista 1)…12) que se completa (resposta nova em amarelo), cronômetro vertical na contagem, fundo Maldivas (uma cena por item).
Sequência: "Como se diz X?" → cronômetro 2,5 s com tique → resposta em inglês falada uma vez; re-ganchos depois dos itens 3 (curtir),
6 (seguir) e 11 (comentar com emoji). **Sem mascote e SEM CTA do Eagle 350 / de produto** (o vídeo termina na última resposta).
Perguntas e respostas: UMA fala cada, cortadas com **`scripts/recortar_whisper.py`** (19/11: o `cortar_respostas` deixava pedaço da
frase vizinha e pausas longas no meio = "travadas"; o novo corta no vale de energia entre as palavras do Whisper, apara a -50 dB com
margem e encurta pausa interna > 0,35 s). Uso: `python3 scripts/recortar_whisper.py audio/perguntas_pt.wav pt audio/q "frase 1" …`.
Exemplo: `posts/2026-11-20_lista12-comandos/`.
**Regra do usuário (19/11): VÍDEOS sem mascote e sem CTA de oferta (ele vai trocar a oferta depois). CTA e mascote ficam SÓ nos
CARROSSÉIS** (`scripts/carrossel_tt.py`, slide final de CTA continua como está). Legenda dos vídeos: sem bloco de CTA do Eagle 350.

## CARROSSEL "CADERNO" (realismo, 19/11/2026)
Ref. do usuário (perfil que bateu 10,9 mil curtidas): folha de caderno pautada, "Português: / Inglês: / Pronúncia:" escritos à mão.
`posts/<post>/caderno.json` → `python3 scripts/carrossel_caderno.py posts/<post>` (template `templates/caderno.html`). A folha é UMA foto
realista sem texto (gpt-image-2; o Gemini recusou) reaproveitável; o texto é nosso (fonte manuscrita), girado no ângulo das pautas
detectado na foto, cada linha no maior tamanho que cabe. Último slide = CTA do perfil (carrossel_tt). Exemplo: `posts/2026-11-19_carrossel-caderno-1/`.

## PERSONAGEM PRÓPRIO (20/11/2026)
Personagem em SVG (`templates/personagem.js`), usado no ABC e no Verbo do dia. **Roupa padrão escolhida pelo usuário: opção 6,
"jeans" (jaqueta jeans aberta + camiseta branca + calça escura).** Outras roupas prontas (`st.roupa`): estrela, moletom, praia, xadrez,
esporte, professor, natal, verao, viajante, chef — prévias em `assets/personagem/`. Só trocar se o usuário pedir.

## PRONÚNCIA ESCRITA (20/11/2026, escolha do usuário — manda sobre a convenção antiga da seção 6)
Estilo SIMPLES da referência: tudo minúsculo, sem hífen e sem maiúsculas de tônica, acento só para guiar a leitura em português:
"mêibi nékst táim", "ái guét áp ét séven", "ái gárit!", "áim lêit". Vale para vídeos (caixa verde do Verbo/ABC), Caderno e Repita.
Gestos do personagem: suaves (ciclo de 0,9 s, transição de 0,4 s). APONTAR para o texto só na 1ª fala do vídeo e na última fixação
em inglês (pedido 20/11); no resto, gestos suaves. Destaque da palavra atual continua em todas as falas.

## CTA DE ENGAJAMENTO NOS VÍDEOS (20/11/2026, pedido do usuário)
Todo vídeo termina com um CTA falado + texto grande pedindo para SEGUIR e COMENTAR algo do vídeo (sem produto):
Verbo do dia → "Segue o perfil pra não perder a próxima aula, e comenta aprender!" (tela "SEGUE ✅ E COMENTA “APRENDER”");
ABC → `"cta": {"fala": "cta", "texto": "Quantas você\nacertou? 👇\n*SEGUE* pra mais!"}` no abc.json ("Quantas você acertou? Comenta aí
embaixo! E segue o perfil pra mais desafios como esse."); Lista 12 → `"cta": "cta"` no lista.json ("Quantas das doze você acertou?
Comenta o número! E segue o perfil pra treinar todo dia."). Variar a pergunta do comentário conforme o tema.

## CORTES/ESTALOS NO ÁUDIO (20/11/2026)
O gerador de voz às vezes solta um estouro curto isolado no começo/fim da fala (soa como "corte"). `recortar_whisper.remover_blips`
tira estouros ≤ 80 ms separados da fala por ≥ 120 ms de silêncio; roda sozinho no `vozes.py` (toda fala gerada) e no
`recortar_whisper.py` (todo pedaço). Para arquivos antigos: `python3 scripts/recortar_whisper.py --limpar audio/*.wav`.
Conferência do vídeo final: envelope de energia em janelas de 20 ms procurando um quadro isolado de som entre silêncios.

## LEGENDA DOS VÍDEOS (20/11/2026, pedido do usuário — manda sobre "sem bloco do Eagle 350" acima)
Simples: 1 linha do tema + 1 pedido de comentário/seguir + 1 linha do infoproduto na bio
("📘 Quer 2.100 frases prontas com tradução e pronúncia? Conheça o Eagle 350, link na bio!") + 5 hashtags.
O VÍDEO continua sem CTA de produto; a chamada do produto fica só na legenda.

## DURAÇÃO (20/11/2026, regra do usuário — manda sobre "40 s a 1 min 10 s")
Todo vídeo entre **30 s e 1 min 20 s CONTANDO O CTA**. Se o tema não couber, dividir em Parte 1, Parte 2… (cada parte com gancho e CTA
próprios). Lista 12 cabe com `"contagem": 2.0, "respiro": 0.4`; se passar, virar Lista 8/10 ou 2 partes. Banco de temas:
`docs/BANCO_DE_CONTEUDO.md` (só o "1 verbo por dia" é fixo; o resto alterna pelo banco).

**Lista 12 = SEMPRE SEM PERSONAGEM (20/11, decisão do usuário: o 1º Lista 12 sem personagem rendeu muitas visualizações).** Só fundo
de mar, selo, palavra falada em verde, lista e cronômetro — não adicionar o personagem nesse formato.

## CADERNO FALADO (vídeo, 21/11/2026 — ref. do usuário "Inglês para iniciantes")
`posts/<post>/caderno_video.json` → `python3 scripts/montar_caderno_video.py posts/<post>` (template `templates/caderno_video.html`):
folha pautada realista (mesma do Caderno), título vermelho, 14 linhas "pt – en (pronúncia)" (preto/azul/vermelho), a voz lê pt → en,
marca-texto amarelo varre a linha lida, ✓ verde nas lidas, CTA de salvar/comentar/seguir. Sem personagem. ~40 s.
Falas: pt todas numa fala, en todas numa fala, cortadas com recortar_whisper.py. Exemplo: `posts/2026-11-24_caderno-falado-1/`.

## VOZ ÚNICA DO PERSONAGEM (22/11 — regra fixa)
Sempre a MESMA voz em tudo (vídeos, aulas, áudios do produto): **Achird** — pt no `gemini-3.8-flash-tts`, en no `gemini-3.8-flash-lite-tts`.
Trocar de chave do Gemini NÃO muda a voz; nunca trocar de voz/modelo para fugir de limite (se travar, esperar ou usar outra chave).

## CTA DO PRODUTO EM VÍDEO (22/11; REFEITO 24/11 pelo usuário — manda sobre "vídeos sem CTA de produto")
Todo vídeo diário termina com um clipe de CTA (sala de aula + lousa + personagem + voz Achird), colado DEPOIS do CTA de engajamento.
**Produto do CTA = EAGLE PRIMEIRA CLASSE (produto principal).** O CTA varia por PÚBLICO (não só quem vai viajar):
`pc_mae` (mãe que quer curso fácil pro filho, sem mensalidade cara), `pc_nao_so_prova` (aprender de verdade, não só pra nota e esquecer),
`pc_ja_tentou` (já fez cursinho e não aprendeu: o problema é o método), `pc_viagem` (vai viajar e tem medo de travar).
Pastas em `assets/cta_produto/variantes/<nome>/` → clipes `assets/cta_produto/cta_<nome>.mp4`. Nunca citar marca de concorrente
(nada de "Wizard" etc.: dizer "mensalidade cara", "cursinho"). Sem preço no vídeo ("pagamento único", "sem mensalidade" pode).
Anexar: `python3 scripts/montar_cta_produto.py anexar posts/<post> [variante]` (sem variante = rodízio entre as 4 `pc_*`; guarda
video/final_sem_cta.mp4). Variantes DIFERENTES nos 2 vídeos do dia. (As antigas facil_*/imigracao ficam fora do rodízio.)
**DURAÇÃO (24/11, manda sobre a regra de 22/11):** o limite de 30 s–1 min 20 s vale para o vídeo SEM o CTA do produto; o CTA é tempo
EXTRA. Lista volta a ter 12 itens (reganchos 3, 6, 11).
**LEGENDA (24/11):** a linha do produto passa a ser do Eagle Primeira Classe, combinando com o CTA do vídeo:
- pc_mae: "👩‍👦 Inglês de verdade pro seu filho, sem mensalidade cara: conheça o Eagle Primeira Classe, link na bio!"
- pc_nao_so_prova: "📘 Inglês pra usar na vida, não só pra prova: conheça o Eagle Primeira Classe, link na bio!"
- pc_ja_tentou: "💡 Já fez cursinho e não aprendeu? Conheça o Eagle Primeira Classe, o jeito fácil. Link na bio!"
- pc_viagem: "✈️ Vai viajar? Eagle Primeira Classe: 10 aulas + 2.100 frases com pronúncia. Link na bio!"

## NÍVEL DO INGLÊS NOS POSTS (22/11/2026, pedido do usuário — regra fixa)
Manter o inglês BÁSICO (A1), onde está o engajamento: frases de 1 a 4 palavras, vocabulário do dia a dia, estruturas que se
repetem ("No ice, please." / "Just water." / "More bread, please."). Nada de frases longas ou elaboradas nos vídeos e carrosséis
("What do you recommend?", "Can we split the bill?" = avançado demais para o feed). Frases mais longas ficam para as aulas do produto.

## CARROSSEL REPITA: 12 FRASES + PRINT NOVO DO PERFIL (24/11/2026, pedido do usuário)
Repita até aprender = capa (cenário do usuário) + **12 frases A1** (slides 02–13) + slide 14 com o **print do perfil**
`assets/marca/perfil_instagram.jpg` (modo escuro): `"cta": {"perfil": "img/perfil.jpg", "fundo": "#0c0f14", "texto": "..."}`
(copiar o print para img/perfil.jpg do post). Texto do slide final vende a SOLUÇÃO, não só viagem
("Inglês do jeito fácil, sem decoreba: aula curtinha e pronúncia escrita 🇺🇸 Link no perfil!"). Quando o usuário mandar print
novo do perfil, trocar o arquivo em assets/marca/. Legenda do carrossel = uma das linhas do Eagle Primeira Classe (seção CTA).
Exemplo: `posts/2026-11-27_carrossel-repita-5/`. Vídeos: Lista sempre com 12 itens, e o CTA do produto é tempo EXTRA.

## LISTA "COMO SE DIZ" = SEMPRE 12 ITENS, SEM SE PRENDER AO TEMPO (24/11/2026, pedido do usuário — manda sobre as regras de DURAÇÃO)
A Lista tem SEMPRE 12 itens (nunca 8/10 nem "Parte 1/2" por causa de tempo). O tamanho do vídeo NÃO é mais critério: use
"contagem": 2.0 e "respiro": 0.4 (padrão) e re-ganchos depois dos itens 3, 6 e 11, mesmo que passe de 1 min 20 s. O CTA do produto
continua como tempo extra no fim. Nos outros formatos, a duração é só uma referência, não um limite rígido.

## STORIES DIÁRIOS (24/11/2026, pedido do usuário) — `docs/ROTINA_STORIES.md`
5 stories por dia (abertura · frase do dia · quiz · CTA · resposta), adesivo de pedido no story 4, rodízio CTA do quiz (seg/qua/sex)
x CTA do produto por público (ter mãe, qui já tentou, sáb viagem, dom caixinha + não só prova). `scripts/montar_stories.py`.

## CHAMADA LEVE NO MEIO + "ATÉ 3X" (24/11/2026, pedido do usuário — manda sobre "CTA DO PRODUTO EM VÍDEO")
Todo vídeo diário leva DUAS chamadas do Eagle Primeira Classe: (1) chamada curta (~6 s, `assets/cta_produto/cta_pc_meio.mp4`:
"Tá curtindo a aula? No Eagle Primeira Classe tem muito mais. Link na bio. Bora continuar!") colada no ponto mais silencioso entre
60% e 70% do vídeo; (2) o CTA completo da variante pc_* no fim. Um só comando faz as duas:
`python3 scripts/montar_cta_produto.py anexar posts/<post> <variante>` (`--sem-meio` desliga a do meio).
Parcelamento: o Eagle Primeira Classe sai "em até 3x no cartão" (falado no fim dos 4 CTAs e escrito na lousa). NÃO dizer se tem
ou não juros. O Bagagem de Mão NÃO parcela: nunca falar de 3x para ele.

## ENTREGA ORGANIZADA POR DIA (24/11/2026, pedido do usuário — manda sobre a forma de entregar)
Depois de produzir o dia: `python3 scripts/entrega_dia.py <AAAA-MM-DD>` → `entregas/<data>/` com os arquivos numerados NA ORDEM DE
POSTAR e com o horário no nome (01_09h_story1.png … 11_12h_reels_aula.mp4 + _CAPA.png … 14_19h_reels_noite.mp4) e o roteiro
`entregas/<data>.md` (horário, onde, arquivo, adesivo, música, capa, legenda e comentário fixado em blocos de código).
Envio: uma mensagem por dia, com os arquivos de `entregas/<data>/` em ordem e o roteiro (resumido) no texto.
Horários: 09h stories 1–3 + carrossel · 12h aula + story 4 · 18h story 5 · 19h vídeo da noite.
**Capa do Repita: gerar EU MESMO** (não pedir ao usuário): prompt do cenário no legenda.md →
`GEMINI_KEY_FILE=<scratchpad>/gemini_paga.key python3 scripts/imagem_gemini.py "<prompt>" posts/<post>/img/capa.png --post posts/<post> --proporcao 3:4 --modelo gemini-2.5-flash-image`
e rodar o carrossel_tt de novo (o slide 01 sai com o texto da capa).

## AGENDAMENTO NO METRICOOL (25/11/2026, pedido do usuário — "agende tudo, só os stories ficam comigo")
Conector Metricool ligado: marca blogId **8348919** (@eagle.english.br, fuso America/Sao_Paulo; só Instagram por enquanto).
Depois da produção e do push (a mídia precisa estar no GitHub), agendar com `createScheduledPost`:
- 09h carrossel (instagramData.type "POST", media = URLs dos slides na ordem) · 12h Reels da aula · 19h Reels da noite
  (type "REEL", showReelOnFeed true, videoThumbnailUrl = capa.png).
- text = legenda do legenda.md; firstCommentText = comentário fixado (o usuário só fixa o comentário).
- Mídia: `https://raw.githubusercontent.com/Victor1Paim/Victor1Paim/claude/charming-cerf-y3w346/eagle-english/posts/<post>/...`
  (conferir com curl -I = 200 antes). Depois, `getScheduledPosts` para confirmar e não duplicar (não agendar o que já está lá).
- **STORIES NUNCA são agendados**: ficam com o usuário (avisos 8h50, 11h50, 17h50).
**Onde a chamada do meio NÃO pode cair (25/11):** entre uma pergunta e a resposta, ou depois de "esse verbo vira:". Sempre conferir no
Whisper e, se cair errado, refazer com `--meio-em=SEGUNDOS` (o script acha o silêncio a até 0,6 s): Verbo → antes de "Agora presta
atenção" (pt8); ABC → depois da resposta da rodada 2; Lista → depois da resposta do item 8.

## POST "MEME" (25/11/2026, pedido do usuário — ref. de perfil de inglês viral) — `scripts/montar_meme.py` + `templates/meme.html`
Fundo preto, cabeçalho do perfil (logo + Eagle English BR + @, SEM selo de verificado), gancho em cima, trecho viral curto no meio
(16:9 em 1080 de largura; 4:3 em 960), legenda original mantida, faixa do Eagle Primeira Classe entrando aos 45% (texto por público).
`posts/<data>_meme-NN-<tema>/meme.json` (clipe, ini, fim, gancho com *negrito*, faixa, crop "w:h:x:y" se o vídeo veio editado por
outra página) → video/final.mp4 + capa. Legenda com CRÉDITO ao autor original + linha do Primeira Classe + #memesdeingles.
Fluxo: usuário baixa com yt-dlp (`C:\Users\victo\Videos\Aulas Eagle`) e sobe na pasta do Drive 1bDdwI7LxWN0vpy09SYi7ZbdvAW43dMlL;
eu acho pelo conector do Google Drive e baixo com curl em `https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t`.
Brutos fora do git. **Dias: 15h nos dias SEM carrossel** (calendário). Nunca reaproveitar o texto/cabeçalho de outra página (recortar só
a cena). Quando o estoque de memes prontos acabar, pedir 2 a 4 links novos ao usuário com os comandos do yt-dlp prontos.

## GRADE NOVA A PARTIR DE 28/11/2026 (3 posts/dia, pedido do usuário) — manda sobre horários anteriores
09h carrossel (rotação de 25/11): seg **Caderno** ↔ **Vocabulário com emoji** (semana sim, semana não) · ter/sáb **INICIANTE × NATIVO** · qua **NÃO CONFUNDA** · qui **PRONÚNCIA ✗/✓** · sex **A PRONÚNCIA É IGUAL** · dom **Repita** · 12h **Aula do verbo** (fixo) ·
19h rodízio: seg/sex **Lista 12** · qua/dom **ABC** · ter/sáb **MEME** · qui **CENA DE FILME**. Stories continuam (5/dia).
**Iniciante × Nativo** (ref. "A1 × C1"): `posts/<data>_carrossel-nativo-N/nativo.json` → `python3 scripts/carrossel_nativo.py posts/<post>`
(template `templates/nativo.html`): capa + 5 pares (frase de iniciante × jeito natural, ATÉ 5 palavras, com pronúncia escrita e
tradução; personagem próprio com poses neutro/pensando/feliz/triste/confiante + emoji de apoio no quadro) + print do perfil.
Exemplo: `posts/2026-11-28_carrossel-nativo-1/`. Frases nunca repetidas (grep nos JSON). Meme e cena de filme dependem de vídeo do
usuário (Drive): se faltar, pedir com antecedência (2 dias antes). CENA DE FILME: formato ainda a montar quando chegar o 1º vídeo
(tela dividida: cena em cima com a fala em inglês, personagem/lousa embaixo repetindo com pronúncia escrita e tradução, voz Achird).

**Carrosséis variados (25/11):** `posts/<data>_carrossel-<tipo>-N/variado.json` → `python3 scripts/carrossel_variado.py posts/<post>` (template
`templates/variado.html`, fundo claro): "confunda" (5 pares de falsos cognatos + nota "*X* não é Y!"; ex. posts/2026-12-02_carrossel-confunda-1),
"pronuncia" (6 palavras com ✗ como o brasileiro fala / ✓ como é; ex. posts/2026-12-03_carrossel-pronuncia-1), "igual" (5 pares de
homófonos + som comum; ex. posts/2026-12-04_carrossel-igual-1), "vocab" (tema com 12 itens emoji/palavra/tradução/pronúncia, 6 por
slide). Um emoji por quadro (dois emojis estouram a coluna). Todos terminam com o print do perfil. Sem custo de API.
