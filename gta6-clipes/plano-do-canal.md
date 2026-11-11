# Canal de clipes de GTA 6 — Plano do canal

Cortes de gameplay de GTA 6: momentos engraçados, perseguições, física absurda, segredos e detalhes do mapa.

| Plataforma | Formato principal |
|---|---|
| TikTok | Curto, 15s a 60s |
| Instagram | Reels, 15s a 60s |
| YouTube | Shorts + compilados de 8 a 12 min |

Decisões abertas: nome do canal, @, bio, se haverá voz/narração ou só gameplay com legenda.

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

### Curtos (15s a 60s)
1. **0–2s:** o momento mais forte primeiro (o acidente, o susto, o segredo). Sem introdução.
2. **Texto de gancho** na tela no primeiro frame ("ninguém percebeu isso no GTA 6").
3. **Meio:** o clipe com cortes secos, zoom nos detalhes, slow-motion no pico.
4. **Fim:** loop (o último frame encaixa no primeiro) ou pergunta para comentar.

### Compilados no YouTube (8 a 12 min)
- Tema único ("20 detalhes insanos de Vice City", "top 15 acidentes da semana").
- Os melhores curtos da semana viram o compilado; o compilado aponta para os curtos e vice-versa.
- Capítulos na descrição, miniatura planejada junto.

## 4. Fluxo de produção

1. **Gravar**: sessões de jogo com gravação contínua (replay/clip do console ou OBS no PC). Marcar os tempos dos bons momentos na hora.
2. **Selecionar**: lista de momentos em `pautas/` (arquivo, tempo, pilar, gancho).
3. **Cortar**: ffmpeg para extrair trechos; reenquadrar 16:9 → 9:16 (crop no centro de ação, ou blur de fundo).
4. **Montar**: Remotion ou HyperFrames para texto de gancho, legendas, zoom, contador, vinheta.
5. **Publicar**: mesmo corte nas três plataformas, exportado limpo, com título e legenda adaptados.

Arquivos de gravação são grandes: ficam fora do git (`gravacoes/` no `.gitignore`).

## 5. Cadência sugerida

- **Curtos:** 1 a 2 por dia (o nicho premia volume, principalmente nas semanas de lançamento).
- **Compilado:** 1 por semana.
- Meta inicial realista: **1 curto/dia + 1 compilado a cada 15 dias**, subir depois.

## 6. Regras técnicas

- Curtos: **9:16, 1080×1920**, 30 ou 60 fps. Texto e legenda longe das bordas e do rodapé.
- Compilados: **16:9, 1920×1080** (ou 4K se a gravação permitir).
- Áudio do jogo baixo sob a narração (se houver); música própria ou livre de direitos — trilha licenciada das rádios do jogo pode gerar reivindicação de direitos autorais.

## 7. Direitos e regras (importante neste nicho)

- **Só gameplay próprio.** Nada de reupload de clipes de outros criadores sem permissão; é o motivo nº 1 de derrubada e de recusa de monetização.
- **Nada de vazamentos.** A Rockstar/Take-Two derruba conteúdo vazado; usar só material oficial lançado (jogo, trailers oficiais com crédito).
- Conferir a política de vídeos da Rockstar/Take-Two antes de monetizar e as regras de "conteúdo reutilizado" do YouTube: corte cru sem edição corre risco. Edição com intenção (gancho, texto, comentário, montagem) é o que protege o canal.
- Não usar logo ou marca da Rockstar como se o canal fosse oficial. Nome e identidade visual próprios.
- Spoilers da história: avisar no título/texto nas primeiras semanas após o lançamento.

## 8. Próximos passos

1. Definir nome, @ e identidade visual (logo, cores, vinheta).
2. Montar o template de corte vertical (Remotion ou HyperFrames): gancho, legenda, contador, vinheta.
3. Primeira sessão de gravação e lista de 10 momentos.
4. Publicar os 7 primeiros curtos e ler a retenção para ajustar os pilares.
