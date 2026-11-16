# Banco de ideias — Direito Tributário para quem não é da área

Formato de cada ideia (seção 8 do Prompt Mestre): gancho · público · estrutura · pergunta → resposta prometida ·
por que assistir até o fim · motion (formato no kit) · fonte/status · duração/esforço.

> **Status jurídico:** nada aqui foi conferido na fonte para publicação. Cada ideia aponta a fonte primária a
> checar. Datas e valores (tetos, alíquotas, prazos) mudam: confirmar no ano da postagem.
> Roteiros completos e já marcados para o kit estão nesta pasta (`*.txt`).

| # | Gancho (0–3 s) | Público | Estrutura | Resposta prometida | Motion (kit) | Fonte a conferir | Duração · esforço |
|---|---|---|---|---|---|---|---|
| 1 | "Você paga imposto até no cafezinho." | geral | Contradição | tributo sobre consumo vem embutido no preço; a nota mostra o valor aproximado | ela + dividida lista + motion passos + motion mito | Lei 12.741/2012 | 30 s · baixo — **roteiro pronto** |
| 2 | "Fazer Pix gera imposto?" | geral | Contradição | não; tributa-se a renda, não o meio de pagamento | motion mito + dividida comparação | CTN art. 43; Lei 7.713/1988; Res. BCB 1/2020 | 30 s · baixo — **roteiro pronto** |
| 3 | "IPTU, IPVA e ITBI: quem cobra cada um?" | geral, quem vai comprar imóvel | Escolha | IPTU e ITBI municipais; IPVA estadual | motion lista com ícones | CF art. 155, III; art. 156, I e II | 30 s · baixo — **roteiro pronto** |
| 4 | "Saúde ou escola: qual abate mais no IR?" | assalariado | Escolha | saúde sem limite; educação com teto; só na completa | dividida comparação + motion lista | Lei 9.250/1995, art. 8º | 32 s · baixo — **roteiro pronto** |
| 5 | "Por que uns recebem restituição e outros pagam?" | assalariado | Evolução | retido na fonte x devido no ajuste anual | motion passos (12 meses) + mito | Lei 9.250/1995; RIR/2018 | 30 s · baixo (já tem teste 02) |
| 6 | "Taxa e imposto não são a mesma coisa." | geral | Contradição | imposto não tem contraprestação; taxa é por serviço/fiscalização | motion comparação | CTN arts. 16 e 77 | 35 s · baixo (já tem teste 01) |
| 7 | "Caí na malha fina. E agora?" | quem declara IR | Problema | o que é o cruzamento, como consultar e corrigir (retificadora) | motion definição + passos | Receita Federal (orientações e-CAC); IN RFB vigente | 45 s · médio |
| 8 | "MEI paga imposto?" | MEI | Contradição | o DAS mensal reúne contribuição e tributos fixos; a declaração anual é outra | motion lista + numero (se citar valor, conferir) | LC 123/2006; Portal do Empreendedor | 40 s · médio |
| 9 | "Herança paga imposto?" | famílias | Problema | ITCMD é estadual; regras variam por estado | ela + motion definição + alerta | CF art. 155, I; EC 132/2023 (progressividade); lei do estado | 40 s · médio |
| 10 | "O que muda pra você com a reforma tributária?" | geral | Evolução | IBS e CBS substituem tributos sobre consumo aos poucos; cronograma até 2033 | motion passos (linha do tempo) | EC 132/2023; LC 214/2025 | 45–60 s · alto (exige atualização) |
| 11 | "Colocar dependente no IR sempre vale a pena?" | família | Escolha | depende: soma rendas do dependente; comparar as duas simulações | dividida comparação | Lei 9.250/1995; regras do programa do ano | 40 s · médio |
| 12 | "Alugou um imóvel? A renda do aluguel tem regra própria." | quem aluga | Problema | aluguel recebido de pessoa física → carnê-leão mensal | motion passos | Lei 7.713/1988; IN RFB do carnê-leão | 40 s · médio |

## Calendário sugerido (piloto de 2 semanas, 3 vídeos/semana)
- Semana 1: #1 cafezinho · #2 Pix · #6 taxa x imposto (conceitos, alto potencial de compartilhamento)
- Semana 2: #3 IPTU/IPVA/ITBI · #4 saúde x escola · #5 restituição (começa a puxar o tema IR)
- Perto de fev–mai: concentrar em IR (#4, #5, #7, #11, #12). Início do ano: IPVA/IPTU (#3).

## Como transformar uma ideia em roteiro marcado
1. Escreva a fala corrida (≈ 75 palavras para 30 s, uma ideia por frase).
2. Divida em blocos com `# ela`, `# dividida <modelo> | título`, `# motion <modelo> | título`.
   Regra de bolso: ~70% do tempo em `ela`; use `motion` quando houver lista, comparação, número ou passo a passo.
3. Antes da palavra-chave, coloque o elemento: `[icone casa]`, `[etiqueta IPTU | amarelo]`, `[item ...]`.
4. `python scripts/kit.py ler <nome>` gera o texto limpo para gravar.
