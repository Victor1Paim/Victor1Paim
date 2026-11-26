# Canal de terror faceless (inglês) — plano inicial

Status: 26/11/2026 — piloto produzido (`producoes/piloto/`). Formatos em [`formatos.md`](formatos.md), passo a passo em [`motor/README.md`](motor/README.md). Nome do canal ainda não definido. Pasta provisória: `canal-terror/`.

## Ideia

Canal faceless no YouTube com **coletâneas de histórias de terror narradas em inglês** (3 a 5 histórias ligadas por um tema:
road trip, home alone, college, camping, Halloween, motel, night shift…). Referência: Mr. Nightmare
(análise em [`referencias/analise-mr-nightmare.md`](referencias/analise-mr-nightmare.md)). Inglês para pegar público de CPM mais alto
(EUA, Reino Unido, Canadá, Austrália).

## Pilha de produção

| Etapa | Ferramenta | Situação nesta sessão |
|---|---|---|
| Roteiro (adaptar/escrever) | Claude + skill `humanizer` (tira cara de texto de IA) | ok |
| Voz | **Gemini TTS, voz Enceladus** (decidido 26/11) | ok |
| Imagens | **OpenAI `gpt-image-2` medium** (decidido 26/11: mais barato e mais fotográfico que o Gemini no teste) | ok |
| Transcrição e legendas | Whisper da OpenAI (API) ou Whisper local (skill `whisper-legendas`) | ok (API testada hoje) |
| Trilha e efeitos | biblioteca livre (skill `media-use`) ou geração | a escolher |
| Montagem | FFmpeg, pelo motor em `motor/` (tudo aqui, sem CapCut) | ok |
| Publicação | YouTube (título, descrição com capítulos, miniatura, .srt) | a definir como subir |

## Formato de cada vídeo (a partir das referências)

- 20–35 min, 3–5 histórias de 800–1.900 palavras; narração a ~190 palavras/min.
- 0–6 s vinheta com título do tema → cartela "Story 1 / By: …" → história direto, sem saudação.
- Trilha grave contínua ~9 dB abaixo da voz; sting de ~4 s nas viradas; fim com fade e 20 s de end screen.
- 1 imagem por parágrafo (~15–30 s), sempre com movimento lento e dissolve; planos coringa reaproveitáveis.
- Capítulos na descrição (um por história). Legenda .srt enviada, não queimada.
- Shorts/TikTok: o trecho mais tenso de cada história (45–90 s, vertical, legenda queimada) puxando para o longo.

## Decisões em aberto (próximos portões)

1. **De onde vêm as histórias** — a mais importante, por direitos e por monetização:
   - (a) **Envio de inscritos** com autorização (como o Mr. Nightmare): formulário próprio; exige audiência, então não serve no começo.
   - (b) **Reddit** (r/LetsNotMeet, r/nosleep, r/Thetruthishere…): o texto é do autor; ler sem permissão expõe a strike de direitos autorais. Dá para pedir permissão por mensagem; r/nosleep tem regras próprias de narração.
   - (c) **Domínio público** (Poe, Lovecraft, M. R. James, contos antigos): livre, mas outro clima (clássico, não "true story").
   - (d) **Histórias próprias**, escritas por nós no estilo "true story", inspiradas em padrões (não copiadas). Sem risco de direitos; precisa de cuidado para soar humano.
   - Provável combinação: (d) + (c) no início, (b) com permissão, (a) quando o canal crescer.
2. **Nome, identidade e miniatura** do canal.
3. ~~Voz~~ — decidido: Gemini Enceladus.
4. **Visual**: só Gemini com movimento, ou Gemini + vídeo de banco gratuito.
5. **Onde guardar as referências baixadas**: o usuário pediu a pasta do OneDrive (link em `README.md`).

## Riscos a cuidar desde o primeiro vídeo

- **Monetização do YouTube** (política de conteúdo *inautêntico* / produzido em massa): voz sintética + imagens geradas em série é o perfil mais revisado. Proteção: roteiro próprio e editado, curadoria de tema, montagem com intenção, identidade consistente, nada de vídeos quase iguais.
- **Divulgação de conteúdo alterado/sintético** no upload quando houver imagem realista gerada.
- **Direitos autorais das histórias** (ver decisão 1) e das trilhas (só licença comercial clara).
- **Não imitar a marca do Mr. Nightmare** (nome, vinheta, cartelas idênticas); usar o formato, com identidade nossa.

## Fluxo por vídeo (rascunho, adaptado do Desvendando Ideias)

| # | Etapa | Claude traz | Você decide |
|---|---|---|---|
| 1 | Tema | 3 temas de coletânea com título provisório | o tema |
| 2 | Histórias | 4–6 candidatas (fonte + resumo + direito de uso) | quais 3–5 e a ordem |
| 3 | Roteiro | texto final de cada história, contagem de palavras e tempo | aprovar |
| 4 | Voz | 1 parágrafo de teste, depois o lote | aprovar a voz |
| 5 | Imagens | lista de planos por parágrafo + coringas; geração em lote | trocar o que não serviu |
| 6 | Montagem | rascunho em baixa resolução | ajustes |
| 7 | Publicação | 3 títulos, 2 miniaturas, descrição com capítulos, .srt | as escolhas |
| 8 | Resultado | retenção, CTR, de onde veio o público | o que mudar |
