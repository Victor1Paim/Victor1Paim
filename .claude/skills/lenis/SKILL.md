---
name: lenis
description: Smooth scroll com Lenis (darkroomengineering/lenis) em páginas de vendas, landings e sites — instalação (npm ou CDN), opções, scrollTo, âncoras, modais e scroll aninhado, integração com GSAP ScrollTrigger, React/Vue, snap e acessibilidade. Use quando o usuário pedir "scroll suave", "smooth scroll", "Lenis", rolagem estilo site premium/Awwwards, ou parallax/animação de scroll que precise ficar fluida.
license: MIT (documentação de origem)
---

# Lenis — scroll suave

Escrita a partir do README oficial (Lenis 1.3.27). Lenis roda **sobre o scroll nativo**:
`position: sticky`, âncoras e acessibilidade continuam funcionando. Não tem dependências.

## Quando usar (e quando não)
- Use em páginas "premium" com animação de scroll (parallax, reveals, ScrollTrigger).
- Não use por padrão em páginas simples de conversão: só adiciona JS e muda a sensação do
  scroll. Pergunte/justifique se a página não tiver animação ligada ao scroll.
- Sempre respeite `prefers-reduced-motion` (Lenis já faz: `respectReducedMotion: true` por padrão).

## Instalação
```bash
npm i lenis
```
```js
import Lenis from 'lenis'
import 'lenis/dist/lenis.css'   // CSS recomendado — sempre incluir
```
Site estático sem build (fixe a versão):
```html
<link rel="stylesheet" href="https://unpkg.com/lenis@1.3.27/dist/lenis.css">
<script src="https://unpkg.com/lenis@1.3.27/dist/lenis.min.js"></script>
<script>
  const lenis = new Lenis({ autoRaf: true, anchors: true, allowNestedScroll: true, stopInertiaOnNavigate: true })
</script>
```

## Setup
```js
const lenis = new Lenis({ autoRaf: true })   // loop próprio
lenis.on('scroll', (e) => { /* e.scroll, e.velocity, e.direction, e.progress */ })
```
Loop manual (se já existe um rAF): `function raf(t){ lenis.raf(t); requestAnimationFrame(raf) } requestAnimationFrame(raf)`.
Sem `autoRaf` nem `raf()` o scroll trava — é o erro mais comum.

## Com GSAP ScrollTrigger (padrão do estúdio)
Use **um só loop** (o ticker do GSAP) — não ligue `autoRaf` junto:
```js
gsap.registerPlugin(ScrollTrigger)
const lenis = new Lenis()
lenis.on('scroll', ScrollTrigger.update)
gsap.ticker.add((time) => lenis.raf(time * 1000))   // segundos → ms
gsap.ticker.lagSmoothing(0)
```
Depois disso, ScrollTrigger funciona normal (ver skill `gsap-scrolltrigger`).

## Opções mais usadas
| Opção | Padrão | Para quê |
|---|---|---|
| `lerp` | `0.1` | suavidade (menor = mais "macio"); se definido, ignora `duration` |
| `duration` / `easing` | `1.2` / expo | alternativa ao `lerp` |
| `anchors` | `false` | `true` ou `{ offset: 80 }` para links `#secao` com header fixo |
| `allowNestedScroll` | `false` | deixa áreas roláveis internas rolarem nativo (custa performance) |
| `autoToggle` | `false` | para/retoma sozinho conforme `overflow` do wrapper (modais) |
| `stopInertiaOnNavigate` | `false` | corta a inércia ao clicar link interno |
| `syncTouch` | `false` | suaviza também no touch (instável em iOS < 16) — evite em mobile |
| `orientation` | `vertical` | `horizontal` para scroll lateral |
| `infinite` | `false` | scroll infinito (precisa `syncTouch` no touch) |
| `wrapper` / `content` | `window` / `<html>` | container próprio de scroll |
| `prevent` | — | `(node) => node.id === 'modal'` para não suavizar certos elementos |

## Métodos e propriedades
- `lenis.scrollTo(alvo, { offset, duration, easing, immediate, lock, onComplete })` —
  alvo: número (px), seletor (`'#oferta'`), elemento, ou `'top'`/`'bottom'`.
- `lenis.stop()` / `lenis.start()` — pause ao abrir modal/menu; retome ao fechar.
- `lenis.resize()` (só com `autoResize: false`), `lenis.destroy()` (SPA ao desmontar).
- Leitura: `scroll`, `progress` (0–1), `velocity`, `direction`, `isScrolling`, `isStopped`, `limit`.

## Modais, menus e áreas roláveis
- Atributo no elemento: `data-lenis-prevent` (ou `-wheel`, `-touch`, `-vertical`, `-horizontal`).
- Ao abrir modal: `lenis.stop()`; ao fechar: `lenis.start()` (ou `autoToggle: true`).
- O CSS oficial já põe `overscroll-behavior: contain` nesses elementos e
  `pointer-events: none` em iframes durante o scroll suave.

## React / Vue
```jsx
import { ReactLenis, useLenis } from 'lenis/react'
<ReactLenis root options={{ lerp: 0.1, anchors: true }} />
const lenis = useLenis(({ scroll }) => { /* a cada scroll */ })
```
Vue: `import { VueLenis, useLenis } from 'lenis/vue'` com `<VueLenis root />`.
Com GSAP em React: `options={{ autoRaf: false }}` e ligue `lenis.raf` no `gsap.ticker`.

## Snap
CSS scroll-snap **não funciona** com Lenis. Use `lenis/snap`:
```js
import Snap from 'lenis/snap'
const snap = new Snap(lenis, { type: 'mandatory' })
snap.addElements(document.querySelectorAll('section'), { align: 'start' })
```

## Limitações conhecidas
- Safari: máx. 60fps (30fps em modo economia). `position: fixed` pode tremer em Macs pré-M1.
- Wheel não atravessa iframes (vídeos embutidos param o scroll suave sobre eles).
- Sem suporte a CSS scroll-snap (use `lenis/snap`).

## Checklist antes de entregar
- [ ] CSS do Lenis incluído e versão fixada (CDN com `@1.3.27`, ou npm).
- [ ] Um único loop (`autoRaf` **ou** `gsap.ticker`, nunca os dois).
- [ ] Âncoras do menu funcionam com o offset do header fixo.
- [ ] Modal/carrinho/menu rolam por dentro e travam o fundo.
- [ ] Testado no celular (touch nativo) e com "reduzir movimento" ligado.
- [ ] Sem Lenis a página continua rolável (teste desligando).
