# Direção de arte do Desvendando Ideias (adaptada do relatório "Halftone: estilos de motion design", 26/10/2026)

Fonte: relatório do Manus AI sobre 9 estilos para vídeos explicativos verticais, escrito para o canal **Halftone** (séries). Aqui ele é lido
criticamente e adaptado ao **Desvendando Ideias**. Status: **proposta, aguardando suas escolhas** (portão 0, no fim). Nada abaixo fixa um estilo único.

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

1. **Cor semântica (constante):** âmbar `#FFB300` = número/dado/destaque; azul `#2E8BFF` = objeto/sistema; **menta** `#3DDC97` = correto/solução/resposta; **coral** `#FF4D5E` = problema/pegadinha/alerta/vazio; branco = texto. Calor ou energia, quando for o tema, usa laranja `#FF6A00` só no objeto, nunca como cor de dado.
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

1. Implementar `tema` no gerador (`scripts/build.mjs`): paleta, fundo, forma das placas e tipo de entrada, sem mexer em `shots.json`.
2. Renderizar o mesmo trecho em 2 ou 3 peles (2,5 min por render, custo zero).
3. Comparar lado a lado: quadro 0, plano de maior densidade, quadro final; e o trecho em velocidade normal, **com e sem som**.
4. Dois ou três observadores que não participaram respondem: "o que aconteceu?", "o que é o objeto?", "o que você lembra?". Pontuar de 1 a 5: reconhecimento, legibilidade, clareza, tempo de produção. Para fixar uma pele como base: ≥ 4/5 em reconhecimento e legibilidade.
5. Só depois definir a pele-base de cada pilar.

## 8. Pauta candidata vinda do relatório (**não decidida**)

"Como uma geladeira funciona?" é um bom teste de pele para engenharia, e encaixa no padrão problema → solução: tirar calor de dentro → evaporar um líquido absorve calor (evaporador) → o vapor se acumula, então comprime (compressor) → fica quente demais, então libera o calor para fora (condensador) → ainda está sob pressão, então estreita (capilar) → volta ao início. Precisa de 70–85 s para monetizar e de 2 fontes oficiais para os fatos. Fica no banco de pautas até você escolher o próximo vídeo.

## 9. Decisões pendentes (portão 0 · direção de arte)

1. Adotar a **gramática da seção 4** (regras fixas) como padrão do canal? Quais regras mudar?
2. Quais **peles testar** no trecho do vídeo 001?
3. Cores semânticas: manter âmbar = dado, coral = problema, menta = solução, azul = objeto?
4. Validar nos previews reais de TikTok, Reels e Shorts (só você consegue abrir): quando?
