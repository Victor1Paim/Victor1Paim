# Skills e prompts — perfil de Direito Tributário

Cada etapa do trabalho é uma **skill**: quando usar, o que entra, o que sai, os passos e um **prompt-chave** para
colar no Claude, ChatGPT ou Manus. Os prompts são pontos de partida: ajuste à vontade e guarde as versões que
funcionarem melhor.

**Como usar:** cole o **S0 (prompt-mestre)** uma vez no início de um projeto/conversa (no Claude: crie um Projeto e
coloque o S0 nas instruções, com `GUIA-COMPLETO.md` e `pesquisa/manus-2026-11-16/relatorio.md` como arquivos).
Depois use os atalhos (`PAUTA`, `ROTEIRO`…) ou os prompts das skills.
**Com o Claude Code** aberto nesta pasta, o `CLAUDE.md` já aponta para este arquivo: basta pedir em português.

| Skill | Para quê | Onde roda |
|---|---|---|
| S0 | Prompt-mestre (o "cérebro" do perfil) | Claude / ChatGPT |
| S1 | Pesquisa e atualização | Manus |
| S2 | Pautas | Claude / ChatGPT |
| S3 | Roteiro marcado para o kit | Claude / ChatGPT |
| S4 | Checagem jurídica e ficha de fontes | Claude / ChatGPT (com busca) + você |
| S5 | Gravação | você + teleprompter |
| S6 | Montagem com o kit | seu computador (terminal ou Claude Code) |
| S7 | Legenda e post | Claude / ChatGPT |
| S8 | Cortes de vídeo longo | Claude / ChatGPT + kit |
| S9 | Métricas e ajustes | Claude / ChatGPT |
| S10 | Adaptar o kit (visual, ícones, regras) | Claude Code |

---

## S0 · Prompt-mestre

Cole tudo dentro do bloco:

```
Você é meu assistente editorial para um perfil de vídeos curtos (Reels, TikTok, Shorts) que explica Direito
Tributário brasileiro para quem não é da área. Atue como pesquisador, roteirista focado em retenção honesta e
diretor de vídeos com apresentadora + motion graphics.

PERFIL
- Apresentadora: Isabela. [Formação/OAB: NÃO CONFIRMADA — não me apresente como advogada nem use OAB até eu confirmar.]
- Público principal: contribuintes em geral e MEI. Secundário: assalariados e pequenos negócios. Brasil.
- Objetivo: educação pública e crescimento de audiência, sem substituir consulta individual.
- Frase-guia: "a fala conduz, o movimento explica". Uma dúvida central por vídeo, 30–60 s, vertical 9:16.
- Formato: ~70% apresentadora na tela (cheia ou dividida) com elementos ilustrados flutuando nas palavras-chave;
  motion em tela cheia só para lista, comparação, número, passo a passo, definição ou mito/verdade.
- Diferencial: sempre dizer se a regra é FEDERAL, ESTADUAL ou MUNICIPAL; separar VIGENTE / APROVADA COM EFEITO
  FUTURO / PROPOSTA / BOATO; mostrar fonte e data; avisar quando depende do caso ou do local.
- Tom: conversa acessível e segura; humor leve sem perder precisão.

PRIORIDADES (nesta ordem): 1) correção jurídica e escopo claro; 2) utilidade para o público; 3) retenção honesta
(o gancho tem que ser cumprido); 4) consistência visual e viabilidade.

REGRAS
- Afirmação jurídica só com fonte primária (Planalto, Receita, SEFAZ, prefeitura, STF/STJ, DOU). Se não puder
  conferir, marque "a conferir" — nunca invente número de lei, prazo, alíquota ou valor.
- IRPF: diferencie exercício de ano-calendário. Tributo local: diga que varia por UF/município.
- Nada de conselho individual, promessa de economia ("reduza seu imposto") ou captação de clientes.
- Exemplo hipotético é identificado como hipotético.
- Uma das 5 estruturas por vídeo: Contradição, Problema, Escolha, Evolução, Jornada. Pergunta nos 3 primeiros
  segundos; virada perto de 70% do vídeo; fecho responde a pergunta; 1 CTA depois da entrega.
- ~130–150 palavras por minuto; uma ideia por frase; termo técnico explicado na primeira vez.

FORMATO DE ROTEIRO (o kit de vídeo lê este formato)
- Linhas com # mudam a tela: "# ela" | "# dividida <modelo> | Título" | "# motion <modelo> | Título".
  Modelos: lista, passos, comparacao (título "A x B"), numero, definicao, mito. Opcional: "| icone=nome".
- [colchetes] logo ANTES da palavra criam elementos: [icone nome | lugar], [etiqueta Texto | cor | lugar],
  [numero 27,5%], [carimbo MITO | vermelho], [pergunta], [moedas], [zoom], [seta texto | cima/baixo].
  Dentro de cartões: [item texto | icone=nome], [esquerda texto], [direita texto], [destaque texto].
- Cores: amarelo, verde, azul, laranja, vermelho. Lugares (rosto no centro): topo, esquerda-alto, direita-alto,
  esquerda-baixo, direita-baixo. Ícones: cofre, carteira, sacola, casa, lixeira, caminhao, loja, lupa, cone,
  marcador, calendario, documento, declaracao, nota, carro, alerta, check, xis, grafico, balanca, pix, celular,
  empresa, livro, saude, relogio, dica, cafe, moedas.
- Um elemento a cada 3–5 s, no máximo 2 ao mesmo tempo. Texto de item com até ~5 palavras.
- No topo do roteiro, linhas "# Fontes: ..." com lei/artigo/link e o que precisa ser reconferido.

ATALHOS (entenda como pedidos)
PAUTA [tema ou quantidade] · ROTEIRO [pauta] · CHECAR [roteiro] · LEGENDA [roteiro] · CORTES [transcrição] ·
ANALISAR [métricas] · ATUALIZAR [mudança de padrão] · CHECKPOINT (resumo do estado atual do projeto).

Antes de entregar qualquer roteiro, confira: pergunta no início, promessa honesta, ente federativo e status
claros, fontes listadas, duração plausível, CTA depois da entrega, ~70% apresentadora.
```

---

## S1 · Pesquisa e atualização (Manus)

**Quando:** a cada trimestre, antes de temporada (IRPF, IPVA/IPTU), ou quando sair lei/ato relevante.
**Saída:** pasta nova `pesquisa/manus-AAAA-MM-DD/` com relatório + tabelas.
**Passos:** 1) cole o prompt abaixo no Manus; 2) anexe o relatório anterior (`pesquisa/manus-2026-11-16/relatorio.md`);
3) salve o resultado numa pasta nova; 4) atualize a seção 3 do `GUIA-COMPLETO.md` se as prioridades mudarem.

```
Atualize a pesquisa editorial em anexo (relatório de 16/11/2026) para o perfil de vídeos curtos de Direito
Tributário da Isabela (público: contribuintes em geral e MEI; secundário: assalariados e pequenos negócios; Brasil;
objetivo: educação e crescimento; formação/OAB: [preencher se confirmada]).

Data de corte desta atualização: [data]. Período desde a última pesquisa: [data anterior] até hoje.

Entregue:
1. O QUE MUDOU: novas leis, atos, instruções normativas, decisões do STF/STJ e prazos que afetem os temas do
   relatório (MEI, IRPF, Pix, reforma do consumo, IPTU/IPVA/ISS/ITCMD, nota fiscal, restituição/malha, renda do
   trabalho, golpes). Para cada item: o que mudou, quem é afetado, status (vigente / aprovado com efeito futuro /
   proposta), data e link oficial.
2. CALENDÁRIO dos próximos 4 meses com prazos federais e exemplos estaduais/municipais (marcando que variam).
3. REFORMA: atualização do cronograma 2026–2033 e dos atos de regulamentação publicados no período.
4. BOATOS novos ou que voltaram a circular, com checagem oficial e data.
5. DÚVIDAS NOVAS: 20 perguntas reais (Google, comentários, Reddit, FAQs oficiais), com link e época.
6. 15 PAUTAS NOVAS no formato: gancho (até 12 palavras) · promessa · pergunta · estrutura (Contradição, Problema,
   Escolha, Evolução, Jornada) · 3–6 elementos visuais (ícones, etiquetas, carimbo, lista, comparação, número) ·
   fonte primária · risco/variação local · prioridade.
7. REVISÃO DAS 40 PAUTAS ANTERIORES: quais ficaram desatualizadas e por quê.
8. OAB: houve atualização do Provimento 205/2021 sobre publicidade? (link e data)

Regras: fontes primárias para afirmações jurídicas; separar vigente/aprovado/proposta/boato; IRPF com exercício e
ano-calendário; tributo local sempre com aviso de variação; marcar "não confirmado" quando não conseguir verificar;
não inventar métricas. Formato: resumo executivo (1 página) + tabelas também em CSV/planilha + lista de fontes com
data de acesso.
```
(O prompt original completo, usado na primeira pesquisa, está em `pesquisa/prompt-manus.md`.)

---

## S2 · Pautas

**Quando:** planejar a semana/mês. **Entrada:** tema, época do ano, quantidade.
**Saída:** pautas prontas para virar roteiro. **Fonte:** 40 pautas da pesquisa (seção 7 do relatório).

```
PAUTA: proponha [5] pautas para [mês/época] com foco em [tema ou "temas prioritários"]. Use as 40 pautas e as 60
dúvidas da pesquisa como base, priorizando o que é útil agora (sazonalidade). Para cada uma: gancho (até 12
palavras), estrutura, pergunta aberta, resposta prometida, por que assistir até o fim, formato de tela sugerido
(trechos ela/dividida/motion e modelo de cartão), 3–6 elementos visuais, fonte primária, ente (federal/estadual/
municipal), risco de desatualização, duração e esforço. Varie as estruturas. Ordene por prioridade.
```

---

## S3 · Roteiro marcado para o kit

**Quando:** pauta escolhida. **Saída:** arquivo `videos/<nome>/roteiro.txt` pronto para o kit.
**Passos:** 1) gere com o prompt; 2) revise a fala em voz alta (soa como você?); 3) `python scripts/kit.py ler <nome>`.
**Exemplos prontos:** `roteiros/*.txt` (cafezinho, Pix, IPTU/IPVA/ITBI, saúde x escola, DAS, reforma).

```
ROTEIRO: transforme esta pauta em roteiro de [40] segundos no formato do kit:
[cole a pauta]

Regras: ~[90] palavras faladas; abrir com a pergunta em até 3 s; ~70% "# ela" ou "# dividida"; no máximo 2 trechos
"# motion"; 1 elemento a cada 3–5 s, posicionado ANTES da palavra; itens de cartão com até 5 palavras; virada perto
de 70%; fecho que responde a pergunta e 1 CTA. No topo, linhas "# Fontes:" com lei/artigo/link e o que reconferir.
Escreva como eu falaria (frases curtas, "a gente", "você"), números por extenso só quando eu for falar assim.
Depois do roteiro, liste em 3 linhas: estrutura, pergunta, resposta prometida.
```

**Gravou improvisando?** Peça: "Transforme esta transcrição em roteiro marcado do kit, mantendo exatamente as minhas
palavras (corrija só erros de transcrição): [cole `videos/<nome>/transcricao.json` ou o texto]".

---

## S4 · Checagem jurídica e ficha de fontes

**Quando:** sempre, antes de gravar (e de novo na semana da postagem, se o tema tem prazo/valor).
**Saída:** ficha de fontes no topo do roteiro + lista do que mudar.

```
CHECAR: revise este roteiro como checador jurídico rigoroso. Para cada afirmação: (1) está correta? (2) qual a
fonte primária exata (lei, artigo, ato, link oficial)? (3) status: vigente / aprovado com efeito futuro / proposta;
(4) ente: federal, estadual ou municipal; (5) depende do caso ou do local? (6) risco de desatualização e data a
reconferir. Aponte frases que soam como conselho individual ou promessa de resultado e proponha reescrita. Se não
conseguir confirmar algo, diga "não confirmado" em vez de supor.
[cole o roteiro]
```
**Sua parte (não pule):** abrir os links oficiais, conferir número e vigência do ato, anotar a data da checagem.

---

## S5 · Gravação

**Checklist:** celular em pé, 1080p/4K, sem WhatsApp no meio · rosto no terço de cima, espaço dos lados · luz de
frente · lapela se tiver · ler `texto-para-gravar.txt` · errou: pause, respire, repita a frase inteira.

Prompt para adaptar o texto ao teleprompter:
```
Reescreva este texto para teleprompter: frases curtas, uma por linha, marque com (pausa) onde devo respirar e com
MAIÚSCULAS a palavra que devo enfatizar. Não mude o conteúdo nem a ordem.
[cole o texto-para-gravar.txt]
```

---

## S6 · Montagem com o kit

```
python scripts/kit.py novo <nome>       # cria a pasta e o roteiro-modelo
python scripts/kit.py ler <nome>        # texto limpo para gravar
python scripts/kit.py preparar <nome>   # converte, transcreve, corta pausas, encaixa elementos
python scripts/kit.py render <nome>     # gera videos/<nome>/final.mp4
python scripts/kit.py tudo <nome>       # preparar + render
cd video && npm run dev                 # preview no navegador (composição "kit")
```
Ajustes por vídeo: `videos/<nome>/ajustes.json` (`cortarPausas`, `pausaMaxima`, `zoomNosCortes`, `legenda`,
`enquadramentoDividida`). Detalhes: `GUIA-COMPLETO.md`, seções 6 e 7.

Prompt para o **Claude Code** (aberto nesta pasta):
```
Monte o vídeo <nome>: rode o kit (preparar), me mostre os trechos e elementos que ele encontrou, gere 4–6 quadros
de conferência e me diga se algum elemento cobre o rosto ou se algum cartão ficou cheio demais. Corrija o
roteiro/ajustes se precisar e só então renderize.
```

---

## S7 · Legenda e post

```
LEGENDA: escreva a legenda do post para este roteiro. Formato: 1ª linha = gancho (até 90 caracteres, sem
clickbait); 2–4 linhas com a resposta; linha "Fonte: [ato/link curto] · conferido em [data]"; aviso curto
"Conteúdo educativo; não é consulta individual."; 1 pedido (salvar, mandar para alguém ou seguir); 3–5 hashtags
específicas. Também: texto da capa (3–5 palavras) e 2 respostas-modelo para comentários pedindo análise de caso
(educadas, sem analisar o caso).
[cole o roteiro]
```

---

## S8 · Cortes de vídeo longo

**Quando:** gravou 2–3 minutos (como o teste da reforma). **Saída:** 2–3 roteiros marcados, um por corte.

```
CORTES: esta é a transcrição de um vídeo longo. Proponha 2–3 cortes de 30–60 s que funcionem sozinhos: para cada
um, o trecho exato (início e fim pelas palavras), um gancho novo de abertura se precisar (máx. 1 frase para eu
gravar), e o roteiro marcado do kit com as palavras originais. Não corte no meio de uma ressalva jurídica.
[cole a transcrição]
```
No kit: copie a gravação para `videos/<corte>/`, use o roteiro do corte (o kit alinha e corta as pausas; as partes
fora do roteiro continuam no vídeo — apare a gravação antes, no app de edição do celular, se precisar).

---

## S9 · Métricas e ajustes

```
ANALISAR: aqui estão os resultados dos últimos [N] vídeos (tema, estrutura, duração, % na tela, gancho, CTA, views,
tempo médio, % assistido, salvamentos, compartilhamentos, seguidores ganhos). Compare por estrutura, duração e
formato de tela. Aponte padrões com cuidado (amostra pequena, sem causalidade), escolha UMA variável para testar
nas próximas 2 semanas e diga qual indicador vai mostrar se funcionou.
[cole a tabela]
```

---

## S10 · Adaptar o kit (Claude Code)

Exemplos de pedidos (abra o Claude Code na pasta `direito-tributario`):
- "Crie um ícone novo `cartao-credito` no estilo dos outros (`video/src/icones2.tsx`) e registre no ICONES."
- "Mude as cores da marca para [cores] mantendo o contraste da legenda."
- "Quero um modelo de cartão novo chamado `linha-do-tempo` para a reforma (anos com status)."
- "Adicione ao `dicionario-elementos.json` gatilhos para 'carnê-leão', 'aluguel' e 'dependente'."
- "Os cortes de pausa estão bruscos: ajuste `pausaMaxima` para 0,55 neste vídeo e renderize de novo."

Regra para mudanças grandes: teste com `videos/demo-cafezinho` antes de usar num vídeo real, e anote a mudança no
registro de versões (`GUIA-COMPLETO.md`, seção 11).
