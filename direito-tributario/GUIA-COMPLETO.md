# Guia completo — perfil de Direito Tributário (Isabela)

**Versão 1.0 · 17/11/2026.** Este guia reúne tudo: o posicionamento do perfil, as regras de conteúdo, a estratégia
tirada da pesquisa (Manus, corte de 16/11/2026), o fluxo de produção e o uso do kit de vídeo que roda no seu
computador. As instruções passo a passo de cada etapa (com os prompts prontos) estão em **`SKILLS-E-PROMPTS.md`**.

> Tudo aqui é ponto de partida, não regra fixa. Você tem autonomia para mudar formato, ritmo, cores, ferramentas e
> processos. Quando mudar algo que deu certo, anote na seção 11 (registro de versões) para não perder o histórico.

---

## 0. A pasta

| Pasta / arquivo | Para que serve |
|---|---|
| `GUIA-COMPLETO.md` | este guia (estratégia + uso) |
| `SKILLS-E-PROMPTS.md` | cada etapa do trabalho como "skill", com prompt pronto para colar no Claude/ChatGPT/Manus |
| `CLAUDE.md` | instruções automáticas para o Claude Code, se você abrir esta pasta nele |
| `LEIA-ME.md` | o mínimo para instalar e rodar |
| `pesquisa/manus-2026-11-16/` | relatório completo, planilha e tabelas CSV da pesquisa |
| `pesquisa/prompt-manus.md` | prompt para refazer/atualizar a pesquisa |
| `roteiros/` | banco de ideias e roteiros já marcados para o kit |
| `videos/<nome>/` | um vídeo por pasta: roteiro, gravação, resultado final |
| `scripts/kit.py` | o motor do kit (comandos `novo`, `ler`, `preparar`, `render`, `tudo`) |
| `dicionario-elementos.json` | palavras que viram elementos automaticamente quando não há roteiro marcado |
| `video/` | projeto de animação (Remotion). Só mexa se quiser mudar o visual |

---

## 1. O perfil

**Frase-guia:** *a fala conduz, o movimento explica.* Uma dúvida central por vídeo, resposta honesta, visual a
serviço da compreensão.

- **Público principal:** contribuintes em geral e MEI. **Secundário:** assalariados e pequenos negócios.
- **Território:** Brasil — sempre dizendo se a regra é **federal, estadual ou municipal**.
- **Objetivo (90 dias):** educação pública e crescimento de audiência, sem substituir consulta individual.
- **Formato:** vertical 9:16, 30–60 s (cortes de vídeos longos quando fizer sentido).
  - ~70% do tempo **você na tela** (cheia ou dividida), com elementos ilustrados flutuando nas palavras-chave;
  - **tela dividida** (você em cima, cartão em motion embaixo) para listas curtas;
  - **motion em tela cheia** para comparação, passo a passo, número, definição e mito/verdade.
- **Estilo visual:** cartum em papel creme, traço de nanquim "vivo", cores apagadas (teal, mostarda, laranja, sálvia),
  letra manuscrita, legenda com palavra-chave em vermelho.
- **Tom:** conversa acessível e segura; humor leve só quando não atrapalha a precisão.

**Diferencial (lacuna encontrada na pesquisa):** quase ninguém faz com consistência:
1. separar **federal / estadual / municipal**;
2. separar **regra vigente / aprovada com efeito futuro / proposta / boato**;
3. mostrar **a fonte e a data na tela**;
4. dizer claramente **quando a resposta depende do caso** e do local.

---

## 2. Regras de conteúdo (ler antes de gravar)

1. **Correção antes de alcance.** Toda afirmação jurídica tem fonte primária (Planalto, Receita, SEFAZ, prefeitura,
   STF/STJ, Diário Oficial). Blog e notícia só como pista.
2. **Data e status.** Prazos, limites, alíquotas e telas mudam: reconfira na semana da postagem. Em IRPF, diferencie
   *exercício* de *ano-calendário*.
3. **Local.** IPTU, ITBI e ISS são municipais; IPVA, ICMS e ITCMD são estaduais. Nunca generalize regra de uma cidade/UF.
4. **Sem conselho individual.** Explicar a regra geral, não avaliar o caso de alguém (nem nos comentários e DMs).
5. **Sem promessa.** Evite "reduza seu imposto", "recupere X", "economia garantida".
6. **Boato:** diga o que circulou, o que é verdade, a fonte oficial e a data. Não banalize deveres reais.
7. **Exemplos** hipotéticos são identificados como tal; números exatos são conferidos e diagramados, nunca inventados.

**OAB (aplicação condicional).** A pesquisa não confirmou formação/inscrição. Enquanto não houver confirmação: não se
apresentar como advogada, não usar número de OAB, limitar-se a explicação geral de informação pública, sem parecer
nem captação de clientes (Lei 8.906/1994, art. 1º). Se a inscrição for confirmada, seguir o Provimento OAB 205/2021,
o Código de Ética e a cartilha de publicidade: conteúdo informativo, verdadeiro, discreto e sóbrio; sem mercantilizar,
captar clientela, induzir litígio, prometer resultado ou usar caso de cliente. A revisão do Provimento estava em
consolidação em 12/2025 — conferir se mudou antes de campanhas.

**Aviso educativo (bio, descrição ou destaque fixo):**
> Conteúdo educativo e geral; não constitui consulta, parecer ou recomendação jurídica ou tributária individual. A
> aplicação das regras depende dos fatos, documentos e legislação vigente. Nenhuma redução de tributo ou outro
> resultado é garantido. Para avaliar um caso concreto, procure profissional legalmente habilitado.

---

## 3. Estratégia (da pesquisa)

### 3.1 Dez temas prioritários
1. **MEI: obrigações recorrentes** — DAS, DASN-SIMEI, nota, registros, regularidade.
2. **IRPF do assalariado e do MEI** — obrigatoriedade anual, exercício x ano-calendário, renda paralela.
3. **Pix e boatos** — movimentação ≠ renda; desmentir sem banalizar deveres.
4. **Reforma tributária do consumo** — cronograma 2026–2033 com status, sem antecipar alíquotas individuais.
5. **Tributos locais** — IPTU, IPVA, ISS, ITCMD, sempre com aviso de que depende do município/UF.
6. **Nota fiscal e documentação** — recibo x nota, regras do MEI, canais de emissão.
7. **Restituição e malha fiscal** — consulta oficial, pendências, prevenção de golpes.
8. **Renda do trabalho** — contracheque, FGTS, 13º e IRPF (sem virar parecer trabalhista).
9. **Compras, doações e transferências** — consumidor, comprovação, natureza do fato.
10. **Segurança e regularização** — cobranças falsas, dívida ativa, portais oficiais.

As **40 pautas** completas (gancho, promessa, pergunta, fonte, prioridade, risco, estrutura, visuais) estão em
`pesquisa/manus-2026-11-16/relatorio.md` (seção 7) e na planilha. As **60 dúvidas reais** estão na seção 2.

### 3.2 Calendário editorial (sazonalidade inferida dos prazos)
| Período | Foco |
|---|---|
| jan–fev | IPVA e IPTU (sempre "depende da sua UF/cidade"), organização de documentos |
| mar–mai | IRPF (obrigatoriedade, pré-preenchida, deduções) e DASN-SIMEI (até 31/05, em regra) |
| mai–ago | restituição (lotes), malha fiscal, golpes |
| set–out | obrigações do MEI e reforma tributária |
| nov–dez | 13º (1ª parcela até 30/11, 2ª até 20/12), fechamento de registros, consumo e golpes |
| ano todo | boatos de Pix, DAS mensal (dia 20, conferir agenda) |

### 3.3 Reforma: o que dizer com segurança
2026 ano de teste (CBS 0,9% e IBS 0,1%, com compensação/dispensa nas hipóteses legais) · 2027 começa a CBS e o
Imposto Seletivo; PIS/Cofins saem; IPI a zero (ressalva ZFM) · 2029–2032 ICMS/ISS caem para 90%, 80%, 70%, 60% ·
2033 modelo completo. Fontes: EC 132/2023, LC 214/2025, página da Receita. "Aprovado" ≠ "operacionalizado": cite o
status e a data.

### 3.4 Boatos já checados (bons ganchos)
Pix acima de R$ 5 mil tributado (falso) · multa de 150% por Pix (falso) · Receita rastreando cada Pix / "Harpia" e
"T-Rex" (falso) · cadastro de imóveis aumentaria IPTU automaticamente (falso) · salário/doação contam no limite do MEI
(falso) · "taxa das blusinhas" volta em 2027 (falso até o corte). Links e datas: relatório, seção 5.

### 3.5 Referências e padrões
Perfis analisados: Nath Finanças, Me Poupe!, Serasa Ensina, Receita Federal, Sebrae, Contabilizei, Primo Pobre,
EconoMirna, Contabilidade Facilitada, Alexandre Silva (tributarista), AEXO. Padrões que funcionam: gancho em pergunta,
problema do dia a dia, contraste ("MEI ou CLT", "Pix ou imposto"), alerta de prazo/golpe, caso hipotético.

---

## 4. Fluxo de produção (do tema ao post)

| # | Etapa | Skill (em `SKILLS-E-PROMPTS.md`) | Saída |
|---|---|---|---|
| 1 | Escolher pauta | S2 · Pautas | 1 pauta com gancho, pergunta e fonte |
| 2 | Conferir a fonte | S4 · Checagem jurídica | ficha de fontes com status e data |
| 3 | Escrever o roteiro marcado | S3 · Roteiro para o kit | `videos/<nome>/roteiro.txt` |
| 4 | Gravar | S5 · Gravação | `videos/<nome>/gravacao.mp4` |
| 5 | Montar | S6 · Kit | `videos/<nome>/final.mp4` |
| 6 | Publicar | S7 · Legenda e post | legenda, capa, aviso |
| 7 | Cortes de vídeo longo | S8 · Cortes | 2–3 vídeos curtos |
| 8 | Medir e ajustar | S9 · Métricas | próxima hipótese de teste |

Atalho: com o **prompt-mestre** (S0) colado num projeto do Claude/ChatGPT, basta pedir "PAUTA", "ROTEIRO [tema]",
"CHECAR [roteiro]", "LEGENDA [roteiro]", "CORTES [transcrição]", "ANALISAR [métricas]".

---

## 5. Instalar (uma vez)

**Windows** — no Prompt de Comando:
```
winget install OpenJS.NodeJS.LTS
winget install Python.Python.3.12
winget install Gyan.FFmpeg
```
Feche e abra o Prompt de novo; dê dois cliques em **`instalar.bat`**.

**Mac** — com Homebrew (https://brew.sh): `brew install node python@3.12 ffmpeg`, depois `./instalar.sh` nesta pasta.

**Teste:** `python scripts/kit.py tudo demo-cafezinho` (Mac: `python3`). A primeira vez baixa o Whisper (~500 MB) e o
navegador do render. Depois tudo funciona offline. Resultado em `videos/demo-cafezinho/final.mp4`.

---

## 6. Fazer um vídeo com o kit

Rodar dentro da pasta `direito-tributario` (Mac: `python3`):

1. `python scripts/kit.py novo pix-01` → cria `videos/pix-01/roteiro.txt` (ou copie um de `roteiros/`).
2. `python scripts/kit.py ler pix-01` → `texto-para-gravar.txt` (fala limpa, para teleprompter).
3. Grave e salve como `videos/pix-01/gravacao.mp4` (ou `.mov`).
4. `python scripts/kit.py tudo pix-01` → `videos/pix-01/final.mp4`.
5. Ver/ajustar antes: `cd video` e `npm run dev` (abre no navegador, composição **kit**). Mudou o roteiro? Rode
   `python scripts/kit.py preparar pix-01` de novo (rápido: não transcreve outra vez).

**O que o kit faz sozinho:**
- converte a gravação (1080×1920, 30 fps, volume normalizado);
- transcreve com o Whisper (grátis, no seu computador) e acha o tempo de cada palavra;
- **corta as pausas** de respiração/hesitação e o silêncio do começo e do fim, alternando um leve zoom a cada corte
  para disfarçar o salto;
- encaixa os elementos, os cartões e a legenda nas palavras marcadas;
- sem roteiro marcado, escolhe elementos pelo `dicionario-elementos.json`.

**Ajustes por vídeo** — `videos/<nome>/ajustes.json` (depois rode `preparar` de novo):
```json
{
  "cortarPausas": true,
  "pausaMaxima": 0.4,
  "zoomNosCortes": true,
  "legenda": true,
  "enquadramentoDividida": -300
}
```
`pausaMaxima`: pausas maiores que isso (segundos) são cortadas — suba para 0.6 se ficar corrido demais.
`enquadramentoDividida`: posição do rosto na tela dividida (mais negativo = rosto sobe).

---

## 7. Como marcar o roteiro

**Linhas com `#` mudam a tela** (até o próximo `#`):

| Linha | O que acontece |
|---|---|
| `# ela` | você em tela cheia, elementos flutuando |
| `# dividida lista \| Título` | você em cima, cartão embaixo |
| `# motion passos \| Título` | só informação em tela cheia (a voz continua) |

Modelos de cartão: `lista` · `passos` · `comparacao` (título "A x B") · `numero` · `definicao` · `mito`.
Ícone no título: `# motion definicao | Malha fina | icone=lupa`.

**`[colchetes]` criam elementos** — logo **antes** da palavra em que aparecem:

| Elemento | Exemplo |
|---|---|
| ícone | `[icone casa]` |
| etiqueta | `[etiqueta IPTU \| amarelo]` · com ícone: `[etiqueta MEI \| azul \| icone=empresa]` |
| número | `[numero 27,5%]` |
| carimbo | `[carimbo MITO \| vermelho]` |
| interrogação | `[pergunta]` |
| moedas | `[moedas]` |
| zoom | `[zoom]` |
| seta | `[seta aumenta \| cima]` · `[seta cai \| baixo]` |
| dentro do cartão | `[item texto]` · `[esquerda texto]` `[direita texto]` · `[destaque texto]` (aceitam `\| icone=nome`) |

Opções após `|`: cor (`amarelo`, `verde`, `azul`, `laranja`, `vermelho`), lugar (`topo`, `esquerda-alto`,
`direita-alto`, `esquerda`, `direita`, `esquerda-baixo`, `direita-baixo`), duração (`3s`).
**Dica:** com o rosto no centro, prefira `topo`, `*-alto` e `*-baixo` (as posições `esquerda`/`direita` ficam na
altura das bochechas).

**Ícones:** cofre, carteira, sacola, casa, lixeira, caminhao, loja, lupa, cone, marcador, calendario, documento,
declaracao, nota, carro, alerta, check, xis, grafico, balanca, pix, celular, empresa, livro, saude, relogio, dica,
cafe, moedas.

**Regra de bolso:** ~70% `ela`/`dividida`; `motion` só quando há lista, comparação, número ou passo a passo; 1
elemento a cada 3–5 s; não mais que 2 ao mesmo tempo.

---

## 8. Gravação
- Celular **em pé**, câmera traseira ou frontal em 1080p/4K, **sem passar pelo WhatsApp** (perde qualidade).
- Rosto no terço de cima, com **espaço dos dois lados** (é onde os elementos entram).
- Luz de frente (janela ou ring light), fundo simples, celular na altura dos olhos, microfone de lapela se tiver.
- Leia o `texto-para-gravar.txt` (teleprompter ajuda). Errou? Pare, respire e repita a frase: o kit corta a pausa,
  mas a frase errada continua — corte o trecho errado ou ajuste o roteiro ao que foi dito.
- Grave vídeos curtos (30–60 s). Vídeo longo: grave e depois use a skill S8 para virar 2–3 cortes.

## 9. Publicação
- Legenda do post: gancho na 1ª linha, resposta em 2–3 linhas, **fonte e data**, aviso educativo curto, 1 pedido
  (salvar / mandar para alguém / seguir), 3–5 hashtags. Skill S7.
- Capa: pergunta do vídeo em 3–5 palavras.
- Comentários: responder com a regra geral e "depende do seu caso/cidade"; não analisar caso individual.

## 10. Métricas e ciclo de revisão
Registrar por vídeo: data, tema, estrutura, duração, % em `ela`/`motion`, gancho, CTA, views, tempo médio,
% assistido, salvamentos, compartilhamentos, seguidores. A cada 2 semanas: observação → hipótese → mudança (uma
variável por vez) → próximo teste. Mudança de lei exige correção imediata do conteúdo, sem esperar métrica. Skill S9.

## 11. Autonomia: como adaptar
- **Roteiro e ritmo:** mude à vontade; o kit só precisa das marcações.
- **Elementos automáticos:** edite `dicionario-elementos.json` (gatilho → elemento).
- **Corte de pausas:** `ajustes.json` por vídeo.
- **Cores, fontes, ícones novos, novos modelos de cartão:** arquivos em `video/src/` (`estilo.tsx`, `icones2.tsx`,
  `kit/Cartoes.tsx`). Com o Claude Code aberto na pasta, peça em português (skill S10).
- **Pesquisa nova:** `pesquisa/prompt-manus.md` (S1) a cada trimestre ou quando a lei mudar.

**Registro de versões** (preencha quando mudar o padrão):
| Versão | Data | O que mudou | Por quê (evidência) |
|---|---|---|---|
| 1.0 | 17/11/2026 | padrão inicial: 70% ela, cartum, cortes automáticos | pesquisa Manus + testes |

## 12. Problemas comuns
| Sintoma | Solução |
|---|---|
| `não achei a gravação` | arquivo em `videos/<nome>/` como `gravacao.mp4` ou `.mov` |
| `ffmpeg`/`npx` não encontrado | instale (seção 5) e abra o terminal de novo |
| `roteiro x gravação: 40%` | a fala ficou diferente do roteiro: ajuste o roteiro ao que foi dito |
| elemento cedo/tarde | mova a marcação para antes de outra palavra |
| cortes bruscos demais | `"pausaMaxima": 0.6` ou `"cortarPausas": false` |
| transcrição errada | `python scripts/kit.py preparar <nome> --modelo medium --refazer` |
| render lento | normal: ~3–5 min por minuto de vídeo; feche outros programas |
