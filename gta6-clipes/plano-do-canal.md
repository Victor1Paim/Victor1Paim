# Canal de clipes de GTA 6 — Plano do canal

Cortes de **streamers e criadores reagindo / jogando** — começando por GTA 6 (lançamento em 19/11) e depois outros jogos. Os melhores momentos de cada live ou react, em 50s a 1m30.

| Plataforma | Formato principal |
|---|---|
| TikTok | Curto, 50s a 1m30 |
| Instagram | Reels, 50s a 1m30 |
| YouTube | Shorts + compilados de 8 a 12 min |

Nome: **Modo Replay** (@modoreplay_10). Kit dos perfis em `marca/perfis.md`.

---

## 1. Posicionamento

**Promessa:** os melhores momentos de GTA 6 em poucos segundos, sem enrolação.

**Diferencial a escolher:** clipes de jogo são um nicho lotado. Sugestões de assinatura:
- **"Detalhe que ninguém viu"**: easter eggs e detalhes de Leonida explicados em 30s.
- **Desafios recorrentes** (ex.: "atravessar Vice City sem ser pego", "1 estrela por minuto").
- **Série de personagem**: um personagem/carro fixo com mini-histórias em capítulos.
- Um bordão ou vinheta de 1s no início/fim de todo corte.

## 2. Pilares de conteúdo

1. **Caos e física** — acidentes, ragdoll, perseguições que dão errado.
2. **Detalhes e segredos** — easter eggs, NPCs com rotina, coisas escondidas no mapa.
3. **Desafios** — regras próprias, com placar/contador na tela.
4. **Dicas rápidas** — dinheiro, carros raros, missões (pico de busca logo após o lançamento).
5. **Comparações** — GTA 6 x GTA 5, antes/depois, realismo x vida real.

Regra de equilíbrio: nenhum pilar passa de 40% do mês.

## 3. Formatos

### Curtos (50s a 1m30)
1. **0–2s:** o momento mais forte primeiro (o acidente, o susto, o segredo). Sem introdução.
2. **Texto de gancho** na tela no primeiro frame ("ninguém percebeu isso no GTA 6").
3. **Meio:** o clipe com cortes secos, zoom nos detalhes, slow-motion no pico.
4. **Fim:** loop (o último frame encaixa no primeiro) ou pergunta para comentar.

### Compilados no YouTube (8 a 12 min)
- Tema único ("20 detalhes insanos de Vice City", "top 15 acidentes da semana").
- Os melhores curtos da semana viram o compilado; o compilado aponta para os curtos e vice-versa.
- Capítulos na descrição, miniatura planejada junto.

## 4. Fluxo de produção

1. **Fonte**: live ou react de um criador (de preferência que autorize cortes — ver seção 7), ou trailer oficial.
2. **Transcrever e escolher**: SupoClip (`scripts/supoclip.sh`) transcreve com Whisper local e usa a OpenAI para escolher e pontuar os trechos (gancho, engajamento, valor, compartilhamento). Duração `medium`/`long` para 50s–1m30.
3. **Reenquadrar**: 9:16 com o rosto do criador centralizado (`vertical`), tela dividida rosto + jogo (`vertical_split`) ou quadro inteiro com fundo (`vertical_fit`).
4. **Acabamento com a marca do canal**: Remotion/HyperFrames para gancho, legenda, vinheta e **crédito fixo do criador** na tela.
5. **Publicar**: mesmo corte nas três plataformas, título e legenda adaptados, @ do criador na descrição.

Vídeos brutos ficam fora do git (`gravacoes/` no `.gitignore`).

## 5. Cadência sugerida

- **Curtos:** 1 a 2 por dia (o nicho premia volume, principalmente nas semanas de lançamento).
- **Compilado:** 1 por semana.
- Meta inicial realista: **1 curto/dia + 1 compilado a cada 15 dias**, subir depois.

## 6. Regras técnicas

- Curtos: **9:16, 1080×1920**, 30 ou 60 fps. Texto e legenda longe das bordas e do rodapé.
- Compilados: **16:9, 1920×1080** (ou 4K se a gravação permitir).
- Áudio do jogo baixo sob a narração (se houver); música própria ou livre de direitos — trilha licenciada das rádios do jogo pode gerar reivindicação de direitos autorais.

## 7. Direitos e regras (importante neste nicho)

Canal de cortes vive ou morre pela relação com os criadores. Regras:

- **Decisão do canal: postar cortes de grandes criadores sem pedir autorização antes**, assumindo o risco de reivindicação/derrubada. Para reduzir o risco: prefira criadores que liberam cortes publicamente. Muitos streamers liberam cortes (às vezes com programa de clipadores e divisão de receita). Peça autorização por escrito quando não houver regra pública e guarde em `pautas/autorizacoes.md`.
- **Crédito sempre**: @ do criador na tela durante todo o corte e na descrição, com link para a live/vídeo original.
- **Transformar, não só recortar**: gancho próprio, legenda, edição, contexto. Corte cru sem edição cai na regra de "conteúdo reutilizado" do YouTube e é derrubado com facilidade.
- Se o criador pedir para remover, remover na hora.
- **Músicas**: trilhas licenciadas (rádio do jogo, música da live, música dos trailers) geram reivindicação de direitos autorais. Cortar ou abaixar o trecho de música.
- **Trailers oficiais**: usar com crédito à Rockstar, sempre com reação/comentário por cima; nada de vazamentos.
- Não usar logo ou marca da Rockstar como se o canal fosse oficial.
- Spoilers da história: avisar no título/texto nas primeiras semanas após o lançamento.

## 8. Próximos passos

1. Definir nome, @ e identidade visual (logo, cores, vinheta).
2. Montar o template de corte vertical (Remotion ou HyperFrames): gancho, legenda, contador, vinheta.
3. Primeira sessão de gravação e lista de 10 momentos.
4. Publicar os 7 primeiros curtos e ler a retenção para ajustar os pilares.
