# Dicionário de movimento (Desvendando Ideias)

Base: carrossel salvo de @omatheusdaia, "Motion Dictionary" (14/10), com 18 movimentos em 6 grupos. Usamos **o vocabulário**
(termos gerais de animação), não a identidade visual dele (fundo creme, laranja queimado, fonte condensada preta). A identidade do
canal ainda será definida.

**Regra do canal:** cada movimento precisa **mostrar um dado ou uma ideia** (número que cresce, barra que sobe, forma que vira outra).
Movimento só decorativo em cima de texto cai no risco de "só texto/slideshow" apontado na pesquisa (`../decisoes.md`, risco 1).

Receitas em Remotion 4 (`spring`, `interpolate`, `Easing`; o projeto `halftone/` já usa Remotion 4.0.538 e tem
`src/motion/LegendaKaraoke.tsx` para legenda palavra a palavra, a ser reaproveitada). `f` = frame atual, `fps` = 30.

## 1. Entradas suaves (introduzem contexto, sem chamar atenção)

| Movimento | O que é | Receita | Uso nos nossos vídeos |
|---|---|---|---|
| Fade in | Aparece aos poucos | `interpolate(f,[0,10],[0,1],{extrapolateRight:'clamp'})` em `opacity` | Fonte na tela, rodapé, elementos de apoio |
| Slide in | Entra deslizando | `translateX` ou `translateY` de 40–80 px a 0 com `Easing.out(Easing.cubic)`, 10–14 frames | Cartões de comparação, itens de lista |
| Blur in | Do borrado ao nítido | `filter: blur(12px→0px)` + fade, 12–16 frames | Revelar a resposta depois do hook |

## 2. Entradas com impacto (chamam atenção)

| Movimento | O que é | Receita | Uso |
|---|---|---|---|
| Pop in | Surge com pequeno salto de escala | `scale` de 0.6 a 1 com `spring({config:{damping:12,stiffness:180}})` | Número-hook, palavra-chave |
| Scale up | Cresce até o tamanho final | `scale` 0→1 ou largura crescente com `Easing.out(Easing.exp)` | **Comparação de escala** (formiga vs. prédio) |
| Stagger | Elementos entram um depois do outro | Atraso `i * 4` a `i * 6` frames entre itens | Listas, "3 fatos", barras lado a lado |

## 3. Ritmo do movimento (curva, o que dá sensação de qualidade)

| Movimento | O que é | Receita | Uso |
|---|---|---|---|
| Ease in-out | Começa devagar, acelera, freia | `Easing.inOut(Easing.cubic)` | Padrão para tudo que se move de A a B |
| Overshoot | Passa do destino e volta | `Easing.out(Easing.back(1.6))` ou `spring` com `damping` baixo | Número que "bate" no valor final |
| Bounce | Quica antes de parar | `Easing.bounce` ou `spring` com `damping:8` | Só em momentos leves ou de humor; evitar em saúde e finanças |

## 4. Texto em movimento

| Movimento | O que é | Receita | Uso |
|---|---|---|---|
| Typewriter | Letras uma a uma | `texto.slice(0, Math.floor(f * 1.5))` + cursor piscando | Pergunta do hook |
| Word reveal | Palavras em sequência | Opacidade por palavra com atraso = tempo da fala | **Legenda palavra a palavra** (reaproveitar `LegendaKaraoke`) |
| Text swap | Uma palavra troca por outra | Palavra antiga sobe e some, nova entra por baixo (`translateY` + opacidade) | **Hook "você aprendeu errado"**: "MITO → VERDADE" |

## 5. Formas que mudam (as que mais carregam dado)

| Movimento | O que é | Receita | Uso |
|---|---|---|---|
| Draw-on | O traço se desenha | SVG com `strokeDasharray`/`strokeDashoffset` (ou `evolvePath` do `@remotion/paths`) | Linha de gráfico, seta, esquema de uma estrutura |
| Morph | Uma forma vira outra | Interpolar pontos de dois caminhos SVG (conferir se `@remotion/paths` traz `interpolatePath`; se não, `flubber`) | Transformação de processo (ex.: tijolo → parede) |
| Bar grow | Barra cresce até o valor | Largura/altura = `valor * progress`, com overshoot leve, número contando junto | **Quanto o governo cobra de R$ 100**, comparações de preço |

## 6. Transições de cena

| Movimento | O que é | Receita | Uso |
|---|---|---|---|
| Mask reveal | Uma máscara revela o conteúdo | `clip-path: inset()` animado | Entrada de bloco de informação |
| Wipe | Faixa troca uma cena pela outra | Faixa em `translateX` com `overflow:hidden` | Mudança de beat (número → comparação) |
| Punch zoom | Zoom rápido para dar impacto | `scale` 1→1.15 em 4–6 frames com `Easing.out(Easing.cubic)` | Virada do vídeo (o momento "ahá") |

## Combinações-base por hook (a refinar com a pesquisa)

| Hook | Entrada | Dado | Virada |
|---|---|---|---|
| Número absurdo | Pop in + overshoot | Count-up + Bar grow | Punch zoom |
| Comparação de escala | Scale up lado a lado | Bar grow | Wipe |
| Você aprendeu errado | Text swap (MITO → VERDADE) | Draw-on do esquema | Mask reveal |
| Consequência antes da causa | Blur in do resultado | Morph causa → efeito | Punch zoom |
| Lista ("3 fatos") | Stagger | Slide in por item | Wipe entre itens |

## Limites para manter o custo e a qualidade

- Máximo de **3 tipos de movimento por vídeo** além da legenda, para o modelo continuar reaproveitável.
- Mesma curva padrão (ease in-out) em tudo; overshoot só onde há número ou virada.
- Tempo por tela entre 2 e 4 s (pesquisa); legenda palavra a palavra sempre ligada.
- Tudo é código: nenhum movimento exige imagem gerada nem stock.

## 7. No motor atual (HyperFrames + GSAP) · atualizado em 29/10/2026

Referência: carrossel "Motion Dictionary" de @omatheusdaia (telas 2 a 7, salvas pelo usuário em 29/10/2026). As receitas acima eram para o Remotion; a produção hoje usa `motor/build.mjs` (HyperFrames + GSAP). Esta tabela diz onde cada movimento já existe e como pedir em `shots.json`.

| Movimento | Estado | Como usar / onde está |
|---|---|---|
| Fade in | Pronto | Legenda por palavra; fontes e rótulos (`opacity` 0→1) |
| Slide in | Pronto | Títulos `o.ov` (entrada `slide` em rodízio); etiqueta de preço entra deslizando |
| Blur in | Pronto | Títulos `o.ov` (entrada `blur` em rodízio) |
| Pop in | Pronto | Títulos `o.ov` (entrada `pop`); objetos das receitas (`back.out`) |
| Scale up | Pronto | `note` com `shrink` (inverso), `cube`, `sun`, câmera `pullOut` |
| Stagger | Pronto | `basket` (itens), `spherePile`, `squares`, opções do `quiz`, caixas do `carts` |
| Ease in-out | Pronto | Padrão das câmeras (`power2.inOut`) |
| Overshoot | Pronto | `back.out(1.6–1.8)` em pops, `balanca` inclinando, número batendo no valor |
| Bounce | Pronto (uso raro) | Etiqueta do `lunch` (`elastic.out`); evitar em saúde e finanças |
| Typewriter | **Novo** | `k: "typewriter"`, `o: {text, size, y, cps}` (`motor/receitas-texto.mjs`), com som de digitação |
| Word reveal | Pronto | Legenda palavra a palavra (todas as peles) |
| Text swap | **Novo** | `k: "textSwap"`, `o: {from: "MITO", to: "VERDADE", fromLabel, toLabel, at}`: a palavra velha é riscada, sobe e some; a nova entra por baixo. Base dos vídeos "você aprendeu errado" |
| Draw-on | Pronto | `straightLine`, `slope`, contorno do `box` |
| Morph | Falta | Precisa de interpolação de caminhos SVG (ex.: flubber); fazer quando um roteiro pedir |
| Bar grow | Pronto | `barFill` (`grow`, `pct`, `growPct`, `empty` com `emptyLabel`) |
| Mask reveal | **Novo** | Em qualquer plano: `o.enter: "mask"` (faixa horizontal abre e revela o conteúdo; o fundo já está lá) |
| Wipe | **Novo** | Em qualquer plano: `o.enter: "wipe"`: uma faixa na cor de destaque da pele cobre o fim do plano anterior (mesmo beat) e sai revelando o novo, com som de passagem |
| Punch zoom | Pronto | Câmera `punch`; punch extra no meio dos planos acima de 3 s |

Regras: um movimento de destaque por plano (o resto é apoio); wipe só na mudança de assunto dentro de um beat, no máximo 2 ou 3 por vídeo; text swap no máximo 1 ou 2 por vídeo.

