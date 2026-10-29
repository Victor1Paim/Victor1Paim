# Direção de arte do Desvendando Ideias (adaptada do relatório "Halftone: estilos de motion design", 26/10/2026)

Fonte: relatório do Manus AI sobre 9 estilos para vídeos explicativos verticais, escrito para o canal **Halftone** (séries). Aqui ele é lido
criticamente e adaptado ao **Desvendando Ideias**. Status: **portão 0 respondido em 29/10/2026** (ver seção 9). Nada abaixo fixa um estilo único.

## 1. O que o relatório diz, em uma página

- Recomenda **fixar uma gramática visual e variar a "pele" conforme o assunto**, em vez de adotar nove estéticas ao mesmo tempo.
- Base sugerida: **blueprint editorial + tipografia cinética + geometria Bauhaus** ("Halftone Lab"). Variações ocasionais: quadrinhos, isométrico 2.5D, neo-brutalismo.
- Split-flap, pixel art e Art Déco: **acentos temáticos**, não base (split-flap para números/datas, pixel para temas digitais, Art Déco para arquitetura/história).
- Princípios: objeto reconhecível **antes** do close; **uma ação principal por beat**; diagramas ligados por transformações; texto testado no celular; contraste (WCAG 4,5:1 texto normal, 3:1 grande); margens de segurança; conclusão que recompõe o gancho.
- Plano de teste: o **mesmo trecho de 10 s** nas linguagens candidatas, comparado em quadros e em vídeo, por quem não fez.

## 2. Leitura crítica (o que dá para confiar e o que não)

| Ponto | Avaliação |
|---|---|
| Princípios de produção (gramática fixa, uma ação por beat, contraste, objeto antes do close) | **Sólidos e aproveitáveis.** São juízo de produção, não dado de audiência, e o próprio relatório diz isso |
| Notas da matriz comparativa (1–10) | **Opinião editorial do relatório.** Servem de ponto de partida, não de prova. As notas não consideram o seu nicho nem 1 vídeo por dia |
| Fatos históricos (Bauhaus 1919–1933, Exposição de Paris 1925, Saul Bass 1959, cianotipia de Herschel em 1842, WCAG) | Batem com o que eu conheço, mas **não consegui abrir as fontes** (domínios fora da rede da sessão) |
| **Numeração das citações** | **Não bate.** No corpo, [8] é citado para o "fechamento" dos quadrinhos, mas na lista [8] é um vídeo explicativo isométrico; [10] (neo-brutalismo no texto) é uma curadoria isométrica na lista; a lista tem 62 itens e o corpo usa só 28. Não dá para saber qual fonte sustenta qual frase. Tratar como lista de leitura, não como prova |
| Referências audiovisuais | O relatório admite que várias são vitrines comerciais ou tutoriais ("referência de craft") e que não achou um explainer vertical com split-flap |
| Prompts de imagem (seção 9) | **Não adotamos.** O nosso visual é código (custo ~zero); os prompts pedem imagens de IA. Servem, no máximo, como briefing de composição |
| Duração do exemplo (40 s) | **Não monetiza no TikTok** (precisa passar de 61 s, `../decisoes.md`). Adaptar para 70–85 s |
| Explicação da geladeira | O ciclo está certo (evaporador absorve calor, compressor pressuriza, condensador libera calor, capilar reduz a pressão). A **ordem narrada** (evaporador, compressor, condensador, capilar) é a do ciclo repetido, mas ganha força na ordem "problema → solução" (seção 5) |

## 3. Onde o relatório se alinha e onde diverge das nossas decisões

| Tema | Relatório | Nossa decisão | Resolução |
|---|---|---|---|
| Ritmo | Uma mudança visual por frase; pausas para ler; "movimento constante não é simultâneo em tudo" | Plano de no máximo 2,0 s (`regra-troca-a-cada-2s.md`) | Compatíveis: o **dado fica** e a câmera/ângulo muda (regra 3). Adotar a ideia de um único elemento em ação por vez |
| Legenda | Tipografia cinética "sem legendar palavra por palavra" | Legenda palavra a palavra sempre ligada | **Manter** a legenda da fala (padrão de retenção em vertical). O texto na tela fica em até 4 palavras e **nunca repete** a legenda |
| Estilo único | Recomenda uma base, com peles | "Não defina um estilo único no momento" | Adotar a **estrutura** (gramática fixa + pele variável) e **testar** peles antes de fixar qualquer uma |
| 3D | Acento, custo alto | 3D só em CSS (sem WebGL aqui), ~30% dos planos | Reduzir para 20–30% e só em objetos-herói, como já recomendamos |
| Texto em imagem de IA | Inserir texto em SVG/HTML | Tudo é HTML | Já cumprimos |
| Safe area | 8–10% laterais, folga no topo e na base; validar no preview de cada plataforma | Conteúdo entre y 168 e 1330, texto a ≥ 90 px das bordas | Já compatível; falta **validar nos previews reais** das três plataformas |

## 4. Gramática visual do Desvendando Ideias (regras fixas, a aprovar)

Estas regras valem para **qualquer pele**. O que já está no vídeo 001 vira regra.

1. **Cor: cada pele tem a sua paleta** (decisão do usuário, 29/10/2026). A cor **não** é regra fixa entre peles. Dentro de uma mesma pele, cada cor mantém um papel (dado, objeto, problema, solução) do começo ao fim do vídeo, para o espectador não ter de reaprender. A paleta do vídeo 001 (âmbar/azul/menta/coral) pertence à pele **Cosmos**.
2. **Tipografia:** uma família de exibição (Archivo Black) para ganchos, números e palavras-chave; uma informativa (Inter 700) para rótulos e fontes. Nada de terceira família.
3. **Uma ação principal por plano**; o objeto aparece inteiro e reconhecível **antes** de qualquer aproximação.
4. **Plano ≤ 2,0 s com mudança visível** (cenário, aproximação ou ângulo); o dado importante fica visível por 2 planos enquanto a câmera muda.
5. **Transição com causa:** o elemento do plano anterior vira o do próximo (a gota vira o líquido; a barra vira eixo), em vez de cortes sem relação.
6. **Fecho que recompõe o gancho** (no 001: o cubo fecha a conta que o hook abriu).
7. **Margens:** conteúdo entre y 168 e 1330 e a ≥ 108 px das laterais; legenda em y ≈ 1130; abaixo de 1330 só textura/decoração.
8. **Contraste mínimo:** 4,5:1 para texto comum e 3:1 para texto grande, conferido no render (o `check` do HyperFrames mede). Problema real que já tivemos: número âmbar sobre o Sol âmbar.
9. **Toda animação é código** (HTML/GSAP). Zero imagem gerada por IA, a não ser quando nenhuma skill resolver (`gemini-midia`).
10. **Rótulo de representação:** quando o desenho é esquemático (esferas, ciclos), a fala ou a tela deve dizer "esquema" ou "exemplo".

## 5. Peles (variáveis) e para que servem aqui

Pele = fundo, paleta secundária, densidade de linha, formas e tipo de movimento. Troca por tema; a gramática da seção 4 não muda.

| Pele | Quando usar | Como fica em código | Custo |
|---|---|---|---|
| **Cosmos** (a do 001): azul-noite, formas chapadas, brilho | Escala, espaço, números grandes, curiosidades gerais | Já existe | Zero |
| **Blueprint** | Engenharia, construção, mecanismos, saúde (cortes de corpo) | Fundo azul cianótipo, traço claro, grade, cotas; SVG com `stroke-dashoffset` | Baixo |
| **Bauhaus claro** | Saúde, mente, conceitos abstratos | Fundo marfim, círculos/barras/retângulos, paleta curta | Baixo |
| **Laboratório de dados** (neo-brutalismo) | Finanças, economia, mitos e comparações | Placas de cor plana, contorno preto e sombra dura, carimbos, barras | Baixo |
| **Split-flap** (acento) | Datas, valores, contadores em finanças/história | Componente de células com meia-aba (CSS) | Baixo-médio |
| **Isométrico 2.5D** | Máquinas, redes, infraestrutura | Camadas com `perspective` e eixos a 30° | Médio |
| **Quadrinhos/painéis** | Histórias, humor, antes/depois | Molduras e balões em SVG | Médio-alto |
| **Art Déco** (acento raro) | Arquitetura e história material (ex.: Panteão) | Molduras radiais e linhas | Médio |
| **Pixel art** | Só temas de jogos/tecnologia | Sprites e `image-rendering: pixelated` | Médio-alto, evitar |

Mapa por pilar (sugestão, não decisão): engenharia/construção → Blueprint (+ isométrico quando houver mecanismo); saúde → Bauhaus claro (+ Blueprint em cortes); finanças/economia → Laboratório de dados (+ split-flap em números); curiosidades/escala → Cosmos.

## 6. As três direções do relatório, como ficam para nós

| Direção | Resumo | Para o Desvendando Ideias |
|---|---|---|
| **Lab** (principal do relatório) | Blueprint + tipografia cinética + Bauhaus | Boa para engenharia/construção/saúde; mais fria para curiosidades gerais. Custo baixo |
| **Panels** (ousada) | Quadrinhos infográficos + acentos neo-brutalistas | Mais memorável, mas exige ilustração: contraria "gasto mínimo" com 1 vídeo por dia |
| **Object Theatre** (equilibrada) | Objeto isométrico 2.5D que vira corte blueprint | Combina com o nosso padrão problema → solução em engenharia. Custo médio |

## 7. Plano de teste adaptado (sem custo de voz nem de roteiro novos)

O relatório testa o mesmo trecho de 10 s em todas as linguagens. Para nós, o trecho **já existe**: o beat da "pegadinha" e do empacotamento do vídeo 001 (≈ 17 s de voz já gerada).

1. Implementar `tema` no gerador (`motor/build.mjs`): paleta, fundo, forma das placas e tipo de entrada, sem mexer em `shots.json`.
2. Renderizar o mesmo trecho em 2 ou 3 peles (2,5 min por render, custo zero).
3. Comparar lado a lado: quadro 0, plano de maior densidade, quadro final; e o trecho em velocidade normal, **com e sem som**.
4. Dois ou três observadores que não participaram respondem: "o que aconteceu?", "o que é o objeto?", "o que você lembra?". Pontuar de 1 a 5: reconhecimento, legibilidade, clareza, tempo de produção. Para fixar uma pele como base: ≥ 4/5 em reconhecimento e legibilidade.
5. Só depois definir a pele-base de cada pilar.

## 8. Pauta candidata vinda do relatório (**não decidida**)

"Como uma geladeira funciona?" é um bom teste de pele para engenharia, e encaixa no padrão problema → solução: tirar calor de dentro → evaporar um líquido absorve calor (evaporador) → o vapor se acumula, então comprime (compressor) → fica quente demais, então libera o calor para fora (condensador) → ainda está sob pressão, então estreita (capilar) → volta ao início. Precisa de 70–85 s para monetizar e de 2 fontes oficiais para os fatos. Fica no banco de pautas até você escolher o próximo vídeo.

## 9. Portão 0 · decisões do usuário (29/10/2026)

| Pergunta | Resposta |
|---|---|
| Estrutura | **Regras fixas + pele por tema.** Sem estilo único por enquanto |
| Peles a testar no trecho do vídeo 001 | **Neo-brutalismo (laboratório de dados), Blueprint e Isométrico 2.5D**; Cosmos (atual) como referência |
| Cores semânticas como regra do canal | **Não.** Cada pele tem a sua paleta (regra 1 acima) |
| Validação nos previews de TikTok, Reels e Shorts | Pendente (só o usuário consegue abrir os apps) |

Próximo passo: gerar o mesmo trecho nas três peles (e no Cosmos), comparar e só então escolher a pele-base de cada pilar. Código: `motor/build.mjs --tema`.

## 10. Resultado do teste de peles (29/10/2026)

Trecho: beats 3 e 4 do vídeo 001 (a pegadinha e o empacotamento, 17,4 s, 12 planos), mesma voz, mesmos planos, mesmo roteiro; só a pele muda
(`node ../../motor/build.mjs --tema <cosmos|brutal|blueprint|iso> --beats 3,4 --out ../001-sol-teste-<pele>` (na pasta do vídeo)). Quadros lado a lado: `../producoes/comparacao-peles/comparacao-peles.png`.
Cada render levou 30–40 s e custo zero de API.

| Pele | O que se vê | Pontos fortes | Pontos fracos | Custo de implementar |
|---|---|---|---|---|
| **Cosmos** (referência) | Fundo escuro, esferas com brilho | Já pronto; leitura boa de números e rótulos | Parece "tema espacial" mesmo em assuntos sem relação | Zero |
| **Neo-brutalismo** | Fundo claro chapado (creme, amarelo, rosa, menta), contorno preto, sombra dura | **Maior impacto e maior contraste**; números e formas lidos de longe; legenda em caixa branca nítida | Cores muito vivas cansam em 70+ s; cada tema pede uma troca de cor de fundo para não repetir; o vermelho sobre rosa falhou no contraste (2,5:1) e foi corrigido | Baixo: só CSS e paleta |
| **Blueprint** | Campo azul com grade, traço claro, hachura | Visual "técnico" coerente para engenharia; ótimo para cortes e esquemas | Elementos pequenos (a pilha de esferas) **perdem peso**: azul sobre azul, preenchimento com hachura leve; o `check` não acusou, mas no celular exige conferência | Baixo: só CSS e paleta |
| **Isométrico 2.5D** | Piso em losango, esferas em camadas | **A pilha 3D conta a ideia melhor que as outras** (empacotamento visível como volume) | Só 2 dos 12 planos foram redesenhados; barras e textos seguem iguais ao Cosmos. Para valer em todo o vídeo, cada tipo de plano precisa de versão isométrica | Médio: receita nova por tipo de plano |

Leitura honesta: são **peles de CSS** (brutal, blueprint) contra uma pele que exige **redesenho por plano** (isométrico). Isto é análise minha dos quadros; a avaliação que conta é a sua e a de quem não fez o vídeo (seção 7, passos 3 e 4).

### Pendente (portão 0, parte 2)
1. Qual(is) pele(s) seguem para a segunda rodada (mais planos e outro assunto)?
2. Avaliar com 2 ou 3 pessoas que não participaram, com e sem som (perguntas da seção 7).
3. Escolher a pele-base provisória de cada pilar (seção 5, sugestão de mapa).
