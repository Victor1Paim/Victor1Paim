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
