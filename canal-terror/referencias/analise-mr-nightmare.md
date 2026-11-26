# Análise das referências (Mr. Nightmare) — 26/11/2026

Três vídeos da pasta do Drive do usuário, medidos com `ferramentas/analisar-referencia.py` (Whisper da OpenAI + ffmpeg).
Números medidos, não estimados. Ninguém ouviu os áudios inteiros: as conclusões sobre o som vêm de nível e espectro.

| | Vídeo 1 | Vídeo 2 | Vídeo 3 |
|---|---|---|---|
| Tema (título na abertura) | 3 Home Alone Stories | Halloween (4 histórias) | Road trip / motel (5 histórias) |
| Duração | 24,1 min | 36,5 min | 26,9 min |
| Histórias | 3 (≈ 7 min cada) | 4 (7 a 10 min) | 5 (3,7 a 7 min) |
| Palavras por história | 1.200–1.500 | 1.300–1.950 | 780–1.470 |
| Ritmo da voz (falando) | 195 palavras/min | 200 | 210 |
| Primeira palavra | 13 s | 10 s | 14 s |
| Duração mediana de um plano | 25 s | 38 s | 13,5 s |
| Loudness integrado | −27,6 LUFS | −28,4 | −28,3 |

## 1. Estrutura

1. **0–6 s: vinheta.** Plano escuro com silhueta (vidro fosco), título em serifa branca centralizado: "3 HOME ALONE STORIES". Sem voz.
2. **6–12 s: cartela "Story 1 / By: J.K."** em fundo preto, fonte fina; a trilha entra.
3. **Narração começa direto na história**, sem "olá", sem apresentação do canal, sem pedido de inscrição. A primeira frase já situa: quem, onde, idade.
   - "My name is Jake and I bought my first house when I was 26…"
   - "My brother Adam and I were driving home from our cousin's wedding in Colorado when this happened."
   - "My dad died of cancer in August and by October I needed something to do…"
4. **Entre histórias (7–14 s):** a voz para, a trilha cai a −50/−60 dB, entra um *sting* de ~4 s (−28 dB, tão alto quanto a voz) junto com a cartela "Story N / By: autor", e a próxima história começa.
5. **Fim:** última frase de fecho, trilha em fade de ~15 s e cerca de 30 s de tela de encerramento muda (end screen do YouTube).

## 2. Roteiro (o que as histórias têm em comum)

- **Primeira pessoa, "real", cotidiano.** Nada de monstro: estranhos, perseguição, invasão, algo errado num lugar comum. Um ou outro toque inexplicável (a voz do irmão vindo do galpão).
- **Assinatura do autor** ("By: J.K.", "By: 6o4dingo", "By: Joe"): são relatos enviados por inscritos. Isso dá a sensação de verdade e resolve o direito de uso.
- **Abertura em 1–2 frases** com contexto concreto (idade, cidade, situação). O medo vem devagar: 1 a 2 minutos de normalidade antes do primeiro sinal.
- **Detalhes físicos e precisos** (horário, distância, o que dava para ver pela janela). Pouco adjetivo de medo.
- **Fecho de 1 frase** que olha para trás: "To this day I'm just grateful he didn't." / "It was the scariest night of my life." / "It's as if nobody even lives there."

## 3. Voz

- Ritmo **rápido e constante**: 195–210 palavras/min falando. Não há pausas dramáticas: 98% das pausas ficam entre 0,3 e 1,2 s (fim de frase); só 1 a 27 pausas de 1,2–2 s por vídeo inteiro.
- Tom baixo, uniforme, de quem conta, não de quem interpreta. O suspense vem do texto e da trilha, não da atuação.
- Referência para a nossa voz: **~190 palavras/min**, entrega calma e grave. Uma história de 1.400 palavras ≈ 7,5 min.

## 4. Som

- **Trilha contínua** sob toda a narração, ~9 dB abaixo da voz, concentrada nos graves (energia em 20–120 Hz ≫ 2–8 kHz): drone/ambiente escuro, sem melodia que dispute com a voz.
- **Sting** nas viradas de história (ver item 1.4).
- **Mix bem baixo (−28 LUFS)**: nada estoura, pensado para ouvir no escuro ou para dormir. O YouTube não aumenta volume baixo, então é escolha de estilo. Para nós: começar em −20 a −24 LUFS (um pouco mais alto que eles, ainda confortável) e testar.
- Efeitos sonoros pontuais quase não aparecem no nível medido; a atmosfera é a trilha.

## 5. Imagem

- **Vídeo de banco de imagens, não ilustração**: drone de bairro, casas, corredores escuros, posto de gasolina à noite, placa de motel, estrada vazia, neve pela janela.
- **Literal ao texto**: o roteiro fala "canal, seawall, deck do vizinho" e a tela mostra exatamente isso. Placa "NEBRASKA" quando a história passa por Nebraska.
- **Planos longos** (mediana 13–38 s, ≈ 1 por parágrafo), câmera quase parada, trocas por **dissolve** lento. Detecção de corte simples quase não acha nada: tudo é fusão.
- **Lua** é o plano coringa: aparece sempre que o texto não tem lugar concreto (dezenas de vezes por vídeo).
- Cor **dessaturada e escura** (brilho médio 51–63 de 255), contraste baixo, leve vinheta. Mesmo as cenas de dia parecem frias.
- Marca d'água "Mr. Nightmare" discreta no canto inferior direito. **Sem legenda queimada.**

## 6. O que levar para o nosso canal

| Deles | Nós (proposta) |
|---|---|
| Coletânea de 3–5 histórias por tema | Igual. 20–35 min, temas que viram título: "3 Disturbing Road Trip Stories" |
| Vinheta 6 s + cartela por história | Igual, com identidade própria (fonte, textura, sting próprio) |
| Narração começa sem apresentação | Igual. CTA só no fim, curto |
| Vídeo de banco literal ao texto | Imagens Gemini **com movimento** (Ken Burns lento, partículas, grão) + vídeo de banco onde houver (Pexels/Pixabay) para não parecer slideshow |
| Lua como coringa | Ter um conjunto fixo de planos coringa nossos (lua, estrada, janela, corredor) para reaproveitar |
| Trilha grave contínua + sting | Igual; trilha de biblioteca livre ou gerada; sting próprio |
| Sem legenda | Longos sem legenda queimada (enviar .srt do Whisper ao YouTube). Cortes verticais (Shorts) com legenda |

## 7. Reprodução

```bash
python3 -I canal-terror/ferramentas/analisar-referencia.py VIDEO.mp4 --saida canal-terror/referencias/videos
```
Os vídeos e as transcrições completas ficam fora do git (texto e imagem de terceiros).
