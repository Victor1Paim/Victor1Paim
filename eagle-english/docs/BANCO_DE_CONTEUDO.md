# Banco de conteúdo — o que alterna com a série diária (20/11/2026)

**Fixo:** 12h = "1 verbo por dia · 100 dias" (docs/SERIE_VERBO_DO_DIA.md).
**Alterna (19h + carrossel):** os formatos abaixo, sem repetir o mesmo formato dois dias seguidos e sem repetir tema.
**Duração: 30 s a 1 min 20 s CONTANDO O CTA.** Tema grande → Parte 1, Parte 2… (cada parte com gancho e CTA próprios).
Vídeos sem mascote da águia (personagem próprio onde houver personagem), pronúncia no estilo simples, CTA de seguir + comentar;
o Eagle 350 só na legenda.

## Formatos e tempo de cada um (medido)
| Formato | Script | Tempo por item | Cabe em 80 s (com CTA ~6 s) |
|---|---|---|---|
| **Quiz "O que é isso?"** (figura → contagem → nome em inglês + pronúncia) | `montar_flash.py` (Flashcard) | ~6 s | 8 itens + abertura + CTA ≈ 60–70 s |
| **ABC** (como se diz…? A/B/C, personagem) | `montar_abc.py` | ~8 s por rodada | 3–5 rodadas (3 ≈ 32 s · 5 ≈ 50 s) |
| **Lista 12** (lista 1…12 que se completa, **SEM personagem** — é o que mais rendeu) | `montar_lista12.py` | ~6 s (contagem 2,0 s) | 12 itens + 3 re-ganchos + CTA ≈ 78–80 s (limite!) · temas maiores → Lista 8/10 |
| **Prova de inglês** (lista com emoji + contagem) | `montar_padrao.py` beat "prova" | ~6 s | 8 itens ≈ 55–65 s |
| **Qual você usa? (A×B)** | `montar_padrao.py` beat "escolha" | ~9 s | 5 rodadas ≈ 55–65 s |
| **Jornada / Repita** (situação com frases) | `montar_padrao.py` | ~9 s por frase | 5–6 frases ≈ 60–75 s |
(Formatos de `montar_padrao.py` e o Flashcard (`montar_flash.py`) ainda usam a águia: adaptar para o personagem próprio antes de usar
de novo — o Quiz "O que é isso?" é o próximo a adaptar.)
Carrosséis (sem limite de tempo): **Caderno** ↔ **Repita até aprender**, em dias alternados.

## Temas prontos
### Quiz "O que é isso?" (vocabulário com figura — o mais fácil de engajar: "quantas você acertou?")
- 🐾 **Animais** — Parte 1: fazenda (cow, horse, pig, sheep, goat, chicken, duck, rabbit) · Parte 2: selvagens (lion, elephant, giraffe,
  monkey, zebra, bear, snake, tiger) · Parte 3: no mar (fish, shark, whale, dolphin, octopus, crab, turtle, jellyfish)
- 🏫 **Sala de aula** — pencil, eraser, ruler, notebook, backpack, scissors, glue, pen, sharpener, whiteboard (2 partes de 5–6 se passar)
- 🛁 **Banheiro** — toothbrush, toothpaste, towel, soap, shampoo, mirror, comb, toilet paper
- 🍳 **Cozinha** — fork, knife, spoon, plate, cup, pan, fridge, stove
- 🛋️ **Sala de estar** — sofa, TV, remote control, lamp, pillow, carpet, curtain, shelf
- 👕 **Roupas** (as que ainda não saíram: hat, scarf, gloves, boots, dress, belt, shorts, sweater)
- 🍎 **Frutas** Parte 2 / 🥦 **Legumes e verduras** — carrot, potato, tomato, onion, lettuce, broccoli, corn, cucumber
- 🚗 **Transportes** — car, bus, bike, train, plane, boat, motorcycle, taxi
- 🧑‍⚕️ **Profissões** — doctor, teacher, nurse, cook, driver, police officer, firefighter, dentist
- 🌦️ **Clima** — sunny, rainy, cloudy, windy, snowy, hot, cold, stormy
- 🏥 **Corpo** — head, eyes, nose, mouth, hands, feet, knees, shoulders
- 🎄 **Natal** (dezembro) — tree, gift, star, candle, Santa, reindeer, snowman, cookies
### ABC (frases que brasileiro traduz ao pé da letra)
sentimentos · gratidão e comida · Thanksgiving (26/11) · na rua · no trabalho · no telefone · gírias leves · no restaurante ·
no mercado · no médico · no aeroporto · elogios · desculpas · convites · Natal e Ano Novo
### Lista 12 (1 tema por vídeo)
comandos ✅ · no restaurante · perguntas do dia a dia · Black Friday/compras (27/11) · rotina da manhã · emoções · na viagem ·
na academia · no salão/barbearia · respostas curtas ("Sure!", "No way!") · frases de mãe · Natal
### Prova de inglês / Qual você usa? (quando adaptados para o personagem)
cores · números de 10 em 10 · dias da semana · meses · hot×cold, big×small, early×late, borrow×lend, say×tell, make×do
### Carrosséis
Caderno: frases curtas do dia a dia (6 por post) · Repita até aprender: dia a dia, hotel, aeroporto, cafeteria, supermercado, academia

## Rodízio sugerido das 19h (depois do calendário atual)
Quiz → ABC → Lista 12 → Quiz → ABC → Prova/Qual você usa? → Lista 12 … (Quiz 2×/semana; nada repete em dias seguidos)
