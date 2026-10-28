# Regra de ritmo visual: uma mudança a cada 2 s, no máximo

**Regra:** nenhum plano dura mais de **2,0 s** sem uma mudança visível. A mudança pode ser troca de cenário, aproximação ou mudança de ângulo,
em estilo **2D, 2,5D ou 3D**. Um vídeo de 70–85 s tem, portanto, **cerca de 38 a 45 planos**.

Por que: segura a retenção (o olho sempre recebe novidade) e, na hipótese de revisão da plataforma, reforça que o vídeo é uma animação
original e trabalhada, e não "texto sobre fundo" (risco 1 em `../decisoes.md`; ainda é hipótese a testar).

## O que conta como mudança

| Tipo | O que acontece | Exemplos |
|---|---|---|
| **Troca de cenário** | Outro fundo/cena (corte, wipe, mask reveal, match cut) | Do Sol para a pilha de bolas |
| **Aproximação** | Mudança de escala da câmera | Push-in, pull-out, punch zoom |
| **Mudança de ângulo** | A câmera muda de posição ou inclinação sem trocar a cena | Pan, tilt, giro de 10–20°, órbita |

Não conta como mudança: só o texto trocar, só um elemento pequeno piscar, ou só o fundo se mexer sem a câmera.
Um movimento lento contínuo (drift) pode **acompanhar** o plano, mas o plano ainda precisa começar com uma das mudanças acima.

## Os três estilos

| Estilo | O que é | Como fazemos (Remotion) | Custo | Quando usar |
|---|---|---|---|---|
| **2D** | Plano chapado: formas, gráficos, texto | SVG/CSS; câmera = `scale`, `translate`, `rotate` no contêiner | Mínimo | Dados, números, barras, textos-chave |
| **2,5D** | Camadas em profundidade com paralaxe | Camadas 2D com `perspective` e `translateZ` (CSS 3D); câmera desliza e gira poucos graus | Baixo | Comparações de escala, cenários, "profundidade" barata |
| **3D** | Objetos com volume e câmera real | `@remotion/three` (React Three Fiber): esferas, cubos, órbita da câmera | **Maior**: precisa de WebGL; sem GPU renderiza em software e fica lento (usar a opção `--gl` do Remotion adequada; conferir) | Só em objetos-herói (Sol, cubo, pilha de esferas), poucos planos por vídeo |

Recomendação de custo: **base em 2D e 2,5D, com 3D em 20–30% dos planos** e só nos objetos que ganham com volume.

## Biblioteca de câmera (presets reutilizáveis)

| Preset | Efeito | Duração típica | Curva |
|---|---|---|---|
| `pushIn` | Escala 1 → 1,12 | 1,2–2,0 s | ease in-out |
| `punchZoom` | Escala 1 → 1,18 rápido | 0,15–0,25 s | ease out |
| `pullOut` | Escala 1,15 → 1 | 1,2–2,0 s | ease in-out |
| `panLeft/Right` | Desliza 6–10% da largura | 1,5–2,0 s | ease in-out |
| `tilt` | Gira 4–8° no eixo vertical (2,5D) | 1,2–2,0 s | ease in-out |
| `orbit` | Câmera 3D contorna o objeto, 20–40° | 1,5–2,0 s | ease in-out |
| `cut` | Corte seco para nova cena | 0 | — |
| `wipe` / `maskReveal` | Transição de cena | 0,15–0,3 s | ease out |

## Como organizar para ficar barato (um arquivo por vídeo)

O vídeo é **dados**, não código novo: uma lista de planos (`shots`) lida pelo template do Remotion.

```json
{ "id": 13, "inicio": 21.2, "dur": 1.8, "estilo": "3d", "cena": "cubo", "camera": "orbit",
  "tela": ["109"], "movimento": "draw-on", "fala": "Cento e nove vezes mais largo," }
```

O template renderiza cada plano com o preset de câmera, o estilo e a cena. Trocar um vídeo é trocar o arquivo; custo por vídeo = voz + tempo de render.

## Regras para o ritmo não atrapalhar

1. **Plano de 1,2 a 2,0 s.** Mais curto que 1,0 s só como efeito (punch zoom); mais longo que 2,0 s, não.
2. **Uma ideia por plano e no máximo 4 palavras de texto na tela.** O olho lê ~3 palavras por segundo; cortar mais rápido que isso perde a leitura.
3. **O dado fica, a câmera se move.** Quando um número importa, ele continua visível por 2 planos enquanto a câmera muda em volta.
4. **Cortar na palavra ou na batida da fala**, não no meio da palavra. Cada plano = uma frase curta (até ~6 palavras).
5. **Variar:** nunca 3 planos seguidos do mesmo tipo de mudança (ex.: três push-ins). Alternar troca de cenário e movimento de câmera.
6. **Sem enjoo:** nada de giro rápido, nem tremor; curvas suaves; no máximo 20° por plano.
7. **Um estilo-base por vídeo** (2D, 2,5D ou 3D como "casca") para manter coerência; misturar com intenção, no máximo por beat. Decisão pendente: ver abaixo.
8. **A cadeia problema → solução continua valendo:** o objeto que se transforma (morph) atravessa os planos; a câmera é que varia.

## Medição

O script de checagem (a criar) deve falhar se algum plano tiver `dur > 2.0` ou se houver 3 planos seguidos com a mesma mudança. Registrar também a **quantidade de planos por vídeo** na ficha, para relacionar com retenção.

## Decisão pendente

Um estilo-base por vídeo (mais coerente e barato) ou liberdade para misturar 2D, 2,5D e 3D no mesmo vídeo (mais variado, mais caro e mais difícil de manter bonito).
