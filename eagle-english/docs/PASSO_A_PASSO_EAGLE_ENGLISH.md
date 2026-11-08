# EAGLE ENGLISH BR – PASSO A PASSO COMPLETO DO PROJETO 

(versão de 08/11/2026: o projeto dividido entre ChatGPT, para carrosséis e legendas, e Claude Code, para vídeos) 

Este documento descreve como o projeto funciona do começo ao fim e como recriá-lo nas duas ferramentas. As regras de conteúdo (identidade, estilos, pronúncia, CTA de produto, fila) estão no arquivo **`EAGLE_ENGLISH_PROJETO_COMPLETO.md`** . Este passo a passo diz quem faz o quê, em que ordem e com quais arquivos. 

## 0. VISÃO GERAL 

### 0.1 Fluxo de ponta a ponta 

```
PESQUISA (Manus, a cada 3–4 semanas)
   ↓ relatório
FILTRO (ChatGPT central): corrige frases e pronúncia, descarta repetidos, encaixa na fila
   ↓ fila + banco de frases atualizados
CARROSSEL (ChatGPT central → ChatGPT arte): pacote de prompts → imagens → checklist → legenda
   ↓ slides finais + frases do post
VÍDEO (Claude Code): roteiro → narração → montagem → legendas → CTA → exportação
   ↓
POSTAGEM (Instagram + TikTok) → comentário fixado → stories
   ↓
MÉTRICAS (a cada 3 posts) → ajuste da fila → volta ao início
```

### 0.2 Quem faz o quê 

|Etapa|Ferramenta|Entrada|Saída|
|---|---|---|---|
|Pesquisa de temas e<br>ganchos|Manus|`PROMPT_PESQUISA_MANUS.md`|relatório em<br>PDF|
|Filtro da pesquisa, fila,<br>frases|ChatGPT –<br>chat central|relatório + arquivo completo|fila e banco<br>de frases<br>atualizados|



|Pacote do carrossel<br>(prompts + legenda)|ChatGPT –<br>chat central|"próximo post"|prompts de<br>cada slide +<br>legenda +<br>CTA|
|---|---|---|---|
|Imagens dos slides|ChatGPT –<br>chat de arte|prompts colados um a um|PNGs<br>1080x1440|
|Revisão das imagens|ChatGPT –<br>chat central|imagens anexadas +<br>"checklist"|lista de<br>correções<br>prontas|
|Vídeos (Reels/TikTok)|Claude Code|frases do post + slides +<br>áudio|MP4 9:16 +<br>legenda +<br>comentário<br>fixado|
|Postagem|você|arquivos finais|post no ar|
|Métricas|ChatGPT –<br>chat central|números de 3 posts|ajuste da fila|



### 0.3 A regra que vale para tudo 

Todo conteúdo termina com o CTA do produto "Eagle 350 – Inglês por Situação" + "link na bio" (seção 12 das instruções). Isso inclui carrossel, vídeo, story e legenda. Toda entrega fecha com "CTA incluído: sim" e o checklist. 

## 1. MONTAGEM NO CHATGPT (carrosséis e legendas) 

### 1.1 Criar o Projeto 

1. No ChatGPT, crie um Projeto chamado "Eagle English – Produção". 

2. Em Instruções do projeto, cole a PARTE 2 do `EAGLE_ENGLISH_PROJETO_COMPLETO.md` (o prompt do chat central). 

3. Em Arquivos do projeto, suba: 

   - `EAGLE_ENGLISH_PROJETO_COMPLETO.md` (regras + banco + fila + pacotes prontos); 



   - `PASSO_A_PASSO_EAGLE_ENGLISH.md` (este arquivo); 

   - os relatórios do Manus, quando houver. 

4. Se puder, ative a memória do projeto, para que as decisões fiquem salvas entre as 

conversas. 

### 1.2 Os dois chats 

- Chat central (dentro do Projeto): é onde você conversa e pede tudo. Pode ter um chat por série (ex.: "D8 Tempo livre") para não ficar longo demais. 

- Chat de arte (uma conversa separada, de preferência fora do Projeto, para não misturar instruções): 

1. Abra uma conversa nova. 

2. Cole a PARTE 3 (prompt do chat de arte) como primeira mensagem. 

3. Use uma conversa de arte por post (ou por série). O mascote fica mais consistente quando todas as imagens do post nascem na mesma conversa. 

### 1.3 Ciclo de UM carrossel (passo a passo) 

1. No chat central, peça "próximo post". 

O chat pega o próximo item da fila e devolve: 

- a ideia (série, estilo, tema, gancho); 

- um prompt por slide, em inglês, cada um em bloco de código, na ordem; 

- os dois slides finais: CTA de engajamento (comenta, seguir, salva e teaser) e slide de produto Eagle 350; 

- a legenda completa, terminando no bloco de CTA do Eagle 350; 

- os pontos de atenção; 

"CTA incluído: sim" + checklist; 

   - bloco ESTADO ATUALIZADO. 

2. Revise rápido: frases naturais? Teaser certo, anunciando o próximo post real? Ambiente do estilo D sem repetir? 

3. No chat de arte, cole o prompt do slide 1. Espere a imagem e baixe. 

4. Cole o slide 2, depois o 3 e assim por diante, um por vez. Não cole dois prompts na mesma mensagem. 

Se o rosto do mascote mudar: "keep the eagle identical to the one in slide 1". 

5. De volta ao chat central, anexe as imagens e escreva "checklist". 

O chat confere os 12 itens (acentos, pronúncia, tônica, mascote, ambiente, CTA, slide de produto) e devolve as frases de correção prontas. 

6. Corrija no chat de arte, colando a frase de correção na conversa do slide. Exemplo: "Edit only the line '…', keep everything else identical". 

7. Organize os arquivos com numeração de ordem: `01_capa.png` , `02.png` … `09_produto.png` . 

8. Leve as frases do post para o Claude Code (seção 2.5) para gerar o vídeo do mesmo tema. 

9. Poste (seção 3). 

10. Copie o bloco ESTADO ATUALIZADO e guarde, para colar se abrir outro chat. 

### 1.4 Story, quiz e post avulso 

- Story: peça "story de [tema]". Vem o prompt 9:16 com espaço para o sticker e a linha de CTA ("[1 item do kit] | Link na bio"). 

- Quiz em carrossel (pausado): quando voltar, o último quadro é o CTA ligado ao tema do quiz. 

- Sazonal: o chat central já encaixa sozinho, de 1 a 3 dias antes da data, e ajusta o teaser do post anterior. 

### 1.5 Pesquisa no ChatGPT (filtro do Manus) 

1. Anexe o PDF do Manus no chat central e peça: "filtrar pesquisa". 

2. O chat deve: 

   - separar o que é fato e o que é hipótese; 



- descartar temas repetidos ou de nicho; 

- reescrever as frases em inglês americano natural e converter a pronúncia (o Manus costuma usar IPA "ǝ", "ráu" para how e "rév" para have, e tônica em minúsculo); 



encaixar os temas aprovados na fila, respeitando o rodízio D → outro estilo → D. 

3. Peça "fila" para conferir a nova ordem. 

### 1.6 Métricas (a cada 3 posts) 

1. Mande os números de cada post (Instagram: alcance, curtidas, comentários, salvamentos, compartilhamentos, cliques no link da bio; TikTok: views, curtidas, salvamentos, compartilhamentos). 

2. Peça "métricas". O chat compara com os posts anteriores e propõe um ajuste concreto na fila. 

3. Compare sempre carrossel × vídeo do mesmo tema: isso diz onde vale investir. 

## 2. MONTAGEM NO CLAUDE CODE (vídeos) 

### 2.1 Pasta do projeto 

Crie uma pasta (pode ser um repositório git) com esta estrutura: 

```
eagle-english/
```

```
├─ CLAUDE.md                     ← instruções do agente (modelo na seção 2.2)
├─ docs/
│  ├─ EAGLE_ENGLISH_PROJETO_COMPLETO.md
```

- `│  ├─ PASSO_A_PASSO_EAGLE_ENGLISH.md` 

- `│  └─ estado.md                  ← último bloco ESTADO ATUALIZADO colado do ChatG ├─ assets/` 

- `│  ├─ mascote/                   ← PNGs do mascote sem fundo (várias poses) │  ├─ fontes/                    ← Bebas Neue + uma sans (ex.: Montserrat) │  ├─ musica/                    ← trilhas livres de direitos │  ├─ sfx/                       ← tique-taque, ding, whoosh │  └─ marca/                     ← cores, logo/slide de produto em PNG ├─ templates/` 

- `│  ├─ card_frase.html            ← cartão de frase ( / / ) para renderizar │  ├─ card_produto.html          ← tela final do Eagle 350` 

- `│  └─ card_capa.html` 

- `├─ scripts/                      ← scripts Python/ffmpeg que o Claude Code vai cr └─ posts/ └─ 2026-11-10_salao/` 

- `├─ frases.json             ← as 7 frases (en, pt, pronúncia) ├─ slides/                 ← PNGs do carrossel vindos do ChatGPT ├─ audio/                  ← narração (por cena) e áudio final ├─ roteiro.md              ← roteiro com tempos ├─ legenda.md              ← legenda + comentário fixado + resposta curta └─ video/                  ← MP4 final 1080x1920` 

### 2.2 O CLAUDE.md (cole e adapte) 

```
# Eagle English BR – Produção de vídeos
```

```
Você produz vídeos curtos (Reels/TikTok) para @eagle.english.br. Regras de conteúdo,
identidade, pronúncia e CTA de produto: docs/EAGLE_ENGLISH_PROJETO_COMPLETO.md
(PARTE 4, seções 2, 6 e 12). Estado atual da fila: docs/estado.md.
```

```
Sempre:
```

- `Formato 1080x1920 (9:16), 30 fps, H.264 + AAC, até 60 s (ideal 20–45 s).` 

- `Gancho nos 2 primeiros segundos (falado + texto na tela).` 

- `Textos na tela renderizados a partir de templates HTML (texto exato, acentos ce nunca escritos por gerador de imagem.` 

- `Área segura: nada importante nos 250 px de cima, nos 400 px de baixo nem nos 150 px da direita (interface do TikTok/Reels).` 

- `Narração em pt-BR; frases em inglês com voz americana (arquivo separado).` 

- `Música a 10–15% do volume da voz; loudness final perto de -14 LUFS.` 

- `Final obrigatório (seção 12.3): CTA falado de 5 a 8 s + texto na tela de no máx` 

```
  ("Eagle 350: 350 mapas + 4 bônus | Link na bio").
```

- `Entregar junto: roteiro.md, legenda.md (legenda terminando no bloco de CTA), comentário fixado e resposta curta para "eu quero".` 

- `Fechar a entrega com "CTA incluído: sim" + checklist 12.7.` 

- `Nunca: áudio do ebook, "grátis", preço sem pedido, urgência falsa, promessa de` 

### 2.3 Ferramentas que o Claude Code vai usar 

- ffmpeg: cortar, juntar, sobrepor, mixar áudio, exportar. 

- Python (Pillow, pydub ou numpy): medir silêncios e tempos, gerar a linha do tempo. Playwright/Chromium: renderizar os templates HTML em PNG, com texto exato (resolve os erros de acento do gerador de imagem). 

- Voz: 

   - Fish Audio: o mesmo que já usamos. Pela API, com a sua chave no arquivo `.env` , 

   - sem colar a chave no chat. Se não tiver API, gere no site e solte os arquivos em `audio/` . 

   - Use uma voz pt-BR para a narração e uma voz americana só para as frases em inglês. 

- Legendas automáticas: o Claude Code gera um `.srt` a partir do roteiro (o texto já é conhecido, então não depende de transcrição). 

### 2.4 Os formatos de vídeo 

A) "Repita até aprender" em vídeo (versão em vídeo de todo post D) 

|Tempo|Cena|
|---|---|
|0–2 s|Gancho falado + capa: "Repita comigo: inglês do [tema]!"|
|~4 s<br>por<br>frase|Cartão da frase. Para cada uma das 7 frases: voz americana diz a frase → 1,2 s de<br>pausa para o espectador repetir → voz americana repete → a tradução aparece.|
|final,<br>5–8 s|CTA falado + tela final de produto|



Duração total: de 35 a 45 s. Fundo: o mesmo ambiente do carrossel, com véu, ou o próprio slide do carrossel com um leve zoom (Ken Burns). 

B) Quiz com contagem (como o "Traduza pro inglês") 

Estrutura: 

1. Gancho: "Teste rápido! X palavras em 4 segundos cada". 

2. Para cada pergunta: pergunta falada → 4 s de pensar, com tique-taque e contagem na tela → "ding" + resposta + pronúncia. 

3. Placar: "Quantas você acertou?". 

4. CTA final ligado ao tema. 

Passos técnicos que já usamos e funcionaram: 

1. Medir a narração: detectar silêncios ( `silencedetect` ) para achar o começo e o fim de cada fala. 

2. Montar a linha do tempo: cada fala é posicionada no instante exato da revelação na tela ( `adelay` + `amix` ), com 4,0 a 4,3 s de pensar entre a pergunta e a resposta. 

3. Ajustar o vídeo à voz: se o vídeo for de quadros fixos, estender cada quadro até o fim da fala ( `tpad` com valores arredondados). Congelar 0,7 s antes de cada transição evita quadros pretos. 

4. Rodar ffmpeg com **`-nostdin`** em loops; sem isso aparece o erro "Invalid duration". 

#### C) Microdiálogo de situação (novo, vindo da pesquisa) 

|Tempo|Cena|
|---|---|
|0–2 s|Gancho: "No salão, explique seu corte"|
|2–25 s|3 a 4 cenas de pergunta → resposta (cliente × atendente), cada fala com cartão<br>EN + PT + pronúncia|
|final|CTA falado + tela do Eagle 350|



Duração: de 25 a 35 s. Visual: os slides do carrossel do mesmo tema, ou ilustrações em aquarela + cartões renderizados. 

D) "Qual você usa?" / "Não confunda" (formatos B do carrossel em vídeo) 

Duas opções lado a lado → 3 s para o espectador escolher → revelação com explicação de 1 linha → CTA. 

### 2.5 Ciclo de UM vídeo (passo a passo) 

1. Crie a pasta do post: `posts/AAAA-MM-DD_tema/` . 

2. Coloque os insumos: 



`frases.json` , com as frases que o ChatGPT gerou para o carrossel; 

os PNGs do carrossel em `slides/` , se for aproveitá-los. 

#### Exemplo de `frases.json` : 

```
{"tema":"salão","gancho":"No salão, explique seu corte",
```

```
 "situacao_ebook":"cuidados pessoais",
```

- `"frases":[{"en":"Just a trim, please.","pt":"Só aparar, por favor.","pron":"/DJÂ` 

3. Peça ao Claude Code: "Gere o vídeo do formato A (ou B, C ou D) para o post de [tema]". 

4. O Claude Code deve, nesta ordem: 

1. escrever o `roteiro.md` com tempos e fala por cena (incluindo o CTA final); 

2. gerar ou receber a narração (pt-BR) e as frases em inglês (voz americana), um arquivo por cena; 

3. medir as durações e montar a linha do tempo; 

4. renderizar os cartões HTML em PNG (texto exato); 

5. montar o vídeo 1080x1920 com ffmpeg: fundo, cartões, mascote discreto, música baixa e efeitos; 

6. gerar o `.srt` e "queimar" as legendas na tela, se quiser; 

7. inserir a tela final de produto + CTA falado; 

8. exportar `video/final.mp4` e uma prévia de quadros: uma folha de contato com 1 quadro por cena, para você conferir rápido no celular; 

9. escrever o `legenda.md` : legenda + bloco de CTA + comentário fixado + resposta curta para quem pedir o link; 

10. fechar com "CTA incluído: sim" + checklist. 

5. Confira: assista uma vez com som e uma vez sem som. Sem som, a legenda e os cartões precisam contar a história sozinhos. 

6. Peça ajustes pontuais ("aumenta a pausa da frase 3", "baixa a música"). O Claude Code refaz só o trecho. 

### 2.6 Modelo de CTA para vídeo (seção 12.3) 

- CTA falado (5 a 8 s): "Quer as frases certas pra cada situação? No Eagle 350 você tem 350 mapas visuais com tradução e pronúncia, e mais 4 bônus. Link na bio!" 

- Texto na tela (2 linhas): "Eagle 350: 350 mapas + 4 bônus" / "Link na bio " Comentário fixado: " Eagle 350 – Inglês por Situação: 350 mapas visuais em 35 situações do dia a dia, com frases, tradução e pronúncia escrita + Guia de 21 Dias, 20 Cards de Gramática, 500 Frases para o Dia a Dia e 100 Combinações de Verbos. Link na bio " 

Resposta para "eu quero": "Oi! O Eagle 350 tá no link da bio Qualquer dúvida, me chama!" 

Varie o início do CTA a cada vídeo, ligando ao tema. Fixos: só o nome do produto, os fatos e "link na bio". 

## 3. POSTAGEM 

### 3.1 Instagram 

1. Carrossel: suba os slides na ordem, em 3:4 (1080x1440), sem cortar. 

2. Cole a legenda (termina no bloco de CTA do Eagle 350). 

3. Reel: suba o MP4. A capa do Reel é o quadro do gancho. Cole a legenda e fixe o comentário do CTA. 

4. Stories do dia: repost do post + sticker de link apontando para o mesmo link da bio + 1 linha de CTA. 

### 3.2 TikTok 

1. O carrossel vira modo foto (mesmos slides) e o vídeo vai normal. 

2. Marque sempre "conteúdo gerado por IA". 

3. Use a mesma legenda e fixe o comentário do CTA. 

4. Se o link da bio não aparecer no TikTok, troque "link na bio" por "link no Instagram" só no TikTok. 

### 3.3 Depois de postar 

- Responda os comentários nas primeiras horas. Para quem pedir o link, use a resposta curta. 

Anote os números depois de 48 h (para a etapa de métricas). 

## 4. ROTINA SEMANAL SUGERIDA 

|Quando|O quê|Onde|
|---|---|---|
|Início da semana|"fila" → confirmar os próximos 3 posts|ChatGPT central|
|Na mesma sessão|Pacotes dos 3 posts ("próximo post" × 3)|ChatGPT central|



|Em seguida|Gerar as imagens + checklist|ChatGPT arte +<br>central|
|---|---|---|
|Depois|Vídeos dos mesmos 3 temas|Claude Code|
|Durante a semana|Postar (carrossel e vídeo em dias<br>alternados)|Instagram + TikTok|
|A cada 3 posts|"métricas"|ChatGPT central|
|A cada 3–4<br>semanas|Nova pesquisa no Manus → "filtrar<br>pesquisa"|Manus + ChatGPT|



## 5. COMO MANTER AS DUAS FERRAMENTAS SINCRONIZADAS 

1. A fila mora no ChatGPT. O chat central é a fonte da verdade da fila e do banco de frases. 

2. Toda vez que o ChatGPT devolver o bloco ESTADO ATUALIZADO, cole-o em `docs/estado.md` no Claude Code. 

3. As frases de cada post passam do ChatGPT para o Claude Code em `frases.json` . Não peça para o Claude Code inventar frases novas: ele só produz o vídeo das frases aprovadas. 

4. Quando mudar uma regra (ex.: o CTA de produto), atualize o `EAGLE_ENGLISH_PROJETO_COMPLETO.md` nos dois lugares: nos arquivos do Projeto do 

ChatGPT e em `docs/` do Claude Code. 

## 6. ERROS QUE JÁ APARECERAM (e a solução) 

|Problema|Solução|
|---|---|
|ChatGPT erra acento, til ou letras<br>("PREPOSIÇAO", "perğunta")|"Edit only the line '…', keep everything else identical".<br>Nos vídeos, use cartões HTML renderizados.|
|Capa do D sai em CAIXA ALTA|"change the two hook lines to mixed case and keep<br>the fixed layout"|
|Mascote grande, com bandeira ou|"make the eagle smaller, about 10% of the image|
|com outro rosto|width" / "keep the eagle identical to the one in slide 1"|
|Fundo do D forte demais|"make the veil stronger"|



|Texto em placas, telas ou<br>embalagens|Pedir "no readable text" no prompt|
|---|---|
|"2,000" em vez de "2.000"|Escrever o formato brasileiro no prompt|
|Pesquisa externa com IPA, "ráu",<br>"rév", "NIÚ", "Á" em stop|Converter para a convenção (seção 6 das instruções)<br>antes de usar|
|Canva com fonte só maiúscula<br>(some a tônica) ou tamanho<br>816x1056|Trocar a fonte e redimensionar para 1080x1440|
|Vídeo com quadro preto na<br>transição|Congelar 0,7 s antes da troca|
|ffmpeg com "Invalid duration" em<br>loop|Usar<br>`-nostdin`e arredondar os tempos|
|Voz pt-BR lendo inglês errado|Gerar as frases em inglês com voz americana, em<br>arquivo separado|



## 7. ESTADO DA FILA E O QUE VEIO DA PESQUISA DE 07/11 

Veja a PARTE 1 e a seção 11 do arquivo completo (atualizadas em 08/11). 

Resumo do que entrou na fila: 

- D10: salão → lavanderia → correios. 

- D11: veterinário → museu → a definir. 

- B3: o "não confunda" passou a ser dead/died/death/deaf (dúvida real nos comentários). Também entrou "uma palavra, vários sentidos" (fan, nail, light…). 

- H2: ganhou "EUA × Reino Unido: qual você usa?". 

- B4: "SOME na pergunta: pode?". 

- Todo post D ganha versão em vídeo (formato A), porque os Reels dominaram a amostra da pesquisa. 

