# Padrão oficial dos vídeos (medido nos Reels publicados — 08/11/2026)

Referências analisadas: "I eat / I drink…" (48 s), "Say, tell ou speak" (47 s) e "Paquera Copa" (65 s).
Este padrão **substitui** o visual dos primeiros vídeos feitos aqui (fundo com véu creme, cartões brancos,
mascote pequeno, contagem com tique-taque). Tudo que for recriado segue este documento.

## 1. Estrutura (45–65 s)

| Bloco | Tempo | O que aparece | Fala |
|---|---|---|---|
| Gancho | 0–4 s | legenda branca grande no topo + mascote grande falando | pergunta/afirmação do tema ("O que significa *I eat*?", "Say, tell ou speak? Cada um tem o seu lugar.") |
| (contexto opcional) | 3–10 s | legenda branca | "Ano que vem, a Copa do Mundo feminina é aqui no Brasil. … Então repete comigo." |
| Frases | ~2,3–3 s cada, 6 a 9 frases | inglês AMARELO + pronúncia BRANCA pequena; a tradução VERDE entra quando a voz pt fala | voz americana diz a frase → voz pt diz a tradução. Sem pausa de "sua vez" |
| Ponte | ~4–5 s | cartão creme com borda marinho: "Não sei se você **ficou sabendo**, mas … **frases prontas** pro dia a dia" (palavras-chave em vermelho) | lê o cartão |
| Produto | ~9–10 s | etiqueta + página do ebook, mascote pequeno no canto inferior esquerdo: "O Eagle 350" (capa) → "350 mapas · 35 situações" (mapa ligado ao tema) → "Com pronúncia escrita" (zoom num card) → "Guia de 21 dias" (capa) → "15 minutos por dia" (Dia 5) → selo "vendido separado R$ 27 · BÔNUS" | "O Eagle 350 tem mapas para 35 situações, com pronúncia escrita. E o Guia de 21 dias mostra o que estudar, 15 minutos por dia." |
| Oferta (fixa) | últimos ~11 s | céu ilustrado com avião, bônus no topo, "+ 3 bônus", tabela "Comprando separado" (R$ 123,70 riscado), "Valor final da promoção R$ 19,90", "Oferta por tempo limitado até 25/12", "pagamento único · direto no seu e-mail", "Link na bio", "@eagle.english.br · garantia de 7 dias" | "E mais três bônus. Separado, daria R$ 123,70. Na promoção, sai por R$ 19,90 até 25 de dezembro. Link na bio." |

A oferta é igual em todos os vídeos: está pronta em `assets/marca/fechamento_oferta.mp4` (11,1 s, recortada
do vídeo "Say, tell ou speak", com a narração original). **Atenção:** ela diz "até 25/12" — depois dessa data
precisa de uma versão nova.

## 2. Visual

- **Fundo:** foto fotorrealista do cenário do tema, **em cor cheia, sem véu** (sala de estar, escritório,
  quiosque de praia ao pôr do sol, restaurante à noite). Deixar chão livre no centro-baixo para o mascote.
  Só um leve escurecido no topo (gradiente), para a legenda.
- **Mascote oficial:** `assets/mascote/oficial/boca_fechada.png` e `boca_aberta.png` (mesmo enquadramento):
  águia com capelo e tassel vermelho, óculos redondos, livro vermelho na asa esquerda, acenando com a direita,
  estilo ilustração infantil pintada. **Grande** (~860 px de altura, centro, pés em y≈1730) nas legendas;
  **pequeno** (~400 px, canto inferior esquerdo) nas telas do produto. O bico abre e fecha com a voz
  (~8 vezes por segundo) e o corpo balança de leve.
  - Os mascotes gerados antes (`assets/mascote/pensando.png`, `positivo.png`) são de outro traço: não usar mais.
- **Legendas:** Poppins Black, letras levemente juntas (-0,03em), contorno preto grosso.
  - Inglês: amarelo `#FDDF33`, ~86 px · Pronúncia: branca, ~40 px, entre barras · Tradução: verde `#7CFD4E`, ~64 px
  - Gancho/contexto: branco, ~78 px. Bloco começa em y≈260 e encolhe sozinho se a frase for longa.
- **Cartões (ponte e etiquetas):** fundo creme `#F7F3EA`, borda marinho `#0B1F4B`, cantos arredondados,
  Oswald, texto marinho com palavras-chave em vermelho `#E63946`.
- **Páginas do ebook:** `assets/marca/paginas/` (capa do ebook, capa e Dia 5 do Guia de 21 dias, exemplo de
  mapa "Say, tell e speak"). O **mapa do tema** precisa ser uma página real do ebook ligada ao assunto do vídeo.

## 3. Voz

- Narração pt-BR + frases em inglês com voz americana (arquivos separados), ritmo rápido.
- A oferta fixa tem a voz original dos vídeos publicados. Para não trocar de voz no fim, ou se usa a mesma
  voz no vídeo todo, ou se renarra a oferta (opção `"oferta": {"audio": "<id da fala>"}` no roteiro).

## 4. Como montar

`posts/<post>/roteiro.json` + `falas.json` + `img/fundo.png` →
`python3 scripts/montar_padrao.py posts/<post>` (ou `--previa` para só os quadros).
Modelo comentado no topo do script. Template: `templates/padrao.html`.

## 5. Adaptação dos formatos novos (quiz, pronúncia, velocidades) a este padrão

- **Quiz:** mesma linguagem visual — pergunta em legenda branca, alternativas A/B em amarelo, revelação
  com a certa em verde; sem cartões brancos nem cronômetro vermelho (no máximo um "3, 2, 1" na própria legenda).
- **Pronúncia (-ed):** palavra em amarelo com o "ed" destacado, pronúncia em branco, explicação curta em verde.
- **Velocidades:** a mesma frase em amarelo, com "🐢 / 🚶 / 🚀" na legenda branca indicando a velocidade.
- Todos fecham com ponte → produto → oferta, como acima.
