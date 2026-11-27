# Meta Ads — estudo e plano para o Eagle Primeira Classe (27/11/2026)

## 1. Os 2 vídeos de referência (enviados pelo usuário 27/11)

| | Ref A (32 s, app de inglês) | Ref B (56 s, preparatório de residência) |
|---|---|---|
| Voz | Nenhuma: música + texto grande na tela | Narração em 1ª pessoa → fala direta com quem assiste |
| Imagem | Pessoa gerada por IA (moletom amarelo, lago ao pôr do sol), cenas paradas com leve movimento | Ator gerado por IA, várias cenas (plantão, celular, mesa de estudo, corredor), close de tela do app |
| Roteiro | dor ("Cansado de travar no inglês?") → passo 1 (teste grátis de 10 questões) → passo 2 (plano de 5–15 min/dia) → passo 3 (prática com correção) → preço + garantia de 7 dias → "Toque no botão. Leia a legenda" | rotina/dor ("todo dia a mesma coisa… preso nas redes") → "Levanta um dedo se você quer…" → 4× "se você…" (cada um uma dor/desejo) → prova (maior taxa de aprovação) → nome do produto → "Clique no link" |
| O que copiar | Promessa em PASSOS simples; o teste grátis como porta de entrada; preço e garantia escritos; mandar ler a legenda | Identificação ("é comigo"); lista de "se você…" que cobre vários públicos num vídeo só; mostrar o produto por dentro no celular |
| Cuidado | Sem voz, depende 100% de texto: precisa ser lido em 2 s por cena | "Maior taxa de aprovação" é alegação que exige prova; nós NÃO temos número assim (não inventar) |

Os dois: vertical 9:16, gancho de dor nos 2–3 primeiros segundos, legenda grande, uma pessoa "comum" com quem o público se identifica,
produto aparecendo no celular, CTA único. Feitos com IA (pessoa e cenas) — dá para fazer o mesmo aqui.

## 2. Como a Meta funciona hoje (resumo do estudo)
- **Objetivo da campanha:** para vender, objetivo **Vendas** otimizando para **Compra**. A Meta procura quem compra, não quem clica.
  Para isso precisa do **Pixel** (no site e no checkout da Kiwify) e de preferência a **API de Conversões**.
- **Advantage+ (automação):** público aberto (Brasil, 18–55, sem interesses) + posicionamentos automáticos. Em 2026 o público vem
  dos CRIATIVOS: cada vídeo "chama" um público (mãe, quem já tentou, viagem). O criativo é a segmentação.
- **Teste x escala:** testar com orçamento por conjunto (ABO) e poucos conjuntos; o que vender vai para uma campanha de escala (CBO).
- **Criativos:** variedade de ÂNGULO vale mais que produção caprichada. Uma campanha bem alimentada tem de 4 a 10 anúncios diferentes,
  trocando 2–3 por semana quando cansar. Vídeo vertical com legenda (a maioria assiste sem som).
- **Fase de aprendizado:** ~50 compras/semana por conjunto para "sair do aprendizado". Com ticket baixo e pouco orçamento não vamos
  chegar nisso no começo; então: não mexer em orçamento/anúncio todo dia, esperar 3–7 dias antes de julgar.
- **Regras que reprovam anúncio:** prometer fluência/resultado garantido; atacar atributo pessoal ("Você é burro no inglês?" — use
  "Cansado de travar no inglês?"); marca de terceiros (McDonald's, nomes de cursos); antes/depois; depoimento inventado.
  Pessoa gerada por IA: pode, mas a Meta pode exigir o rótulo de conteúdo de IA — marcar quando pedir.

## 3. A conta (números do produto)
- Primeira Classe: **R$ 29,90** (lançamento) → R$ 37 depois das 100 primeiras vendas. Parcela em até 3x. Bagagem de Mão: R$ 14,90.
- Taxa da Kiwify (conferir no painel): sobra ~R$ 24–25 por venda de R$ 29,90. **CPA máximo para não perder dinheiro: ~R$ 24.**
- Referência de mercado (uma fonte, varia muito): CPM de R$ 20–45 para infoproduto barato. Com CPM R$ 30, cada R$ 24 compra ~800
  impressões: precisa vender 1 a cada ~800 pessoas que veem. É apertado → por isso:
  1. **Aumentar o valor por cliente**: order bump da Bagagem de Mão no checkout (ou um bump novo de R$ 9,90–14,90) e upsell depois.
  2. **Página e checkout rápidos** no celular (cada segundo perdido encarece a venda).
  3. **Começar pequeno** e só escalar o que der CPA abaixo de R$ 24.

## 4. Plano de campanhas (proposta)

### Campanha 1 — VENDAS com vídeo (a principal, a que o usuário quer)
- Objetivo Vendas · evento Compra (se o Pixel ainda não tiver compras, começar otimizando para **Iniciar finalização de compra** e
  trocar para Compra quando passar de ~20 compras).
- 1 conjunto Advantage+ (Brasil, público aberto, posicionamentos automáticos), **R$ 30–50/dia**, ABO.
- **4 vídeos, um por público** (mesmo produto, ângulo diferente) — formato misto das 2 referências:
  1. **Mãe/pai:** "Seu filho faz cursinho de inglês há anos e ainda não fala?" → se você… → passos → preço/3x → link.
  2. **Já tentou:** "Já pagou cursinho e não aprendeu? O problema não foi você." → método: uma frase por vez, pronúncia escrita.
  3. **Viagem:** "Vai viajar e tem medo de travar no aeroporto?" → 2.100 frases + 10 aulas → treine antes de ir.
  4. **"Levanta um dedo se…"** (estilo Ref B): 4 "se você…" (mãe, já tentou, viagem, trabalho) → Eagle Primeira Classe.
  Todos: 20–40 s, legenda grande, produto por dentro no celular, "pagamento único ou até 3x", "link abaixo". Destino:
  `https://eagle-viagem.vercel.app/oferta?utm_source=meta&utm_medium=ads&utm_campaign=vendas&utm_content=<angulo>`.
- Julgar depois de 3–4 dias / ~R$ 100 por vídeo: desligar o que tiver CTR de link < 0,8% ou custo por compra > R$ 24.

### Campanha 2 — REMARKETING (barata, entra depois de 1–2 semanas)
- Público: quem interagiu com o @ nos últimos 30 dias + visitou a página e não comprou. R$ 10–15/dia.
- Criativos: carrossel "o que tem dentro", vídeo da aula por dentro, a pergunta frequente (parcela? acesso vitalício? 7 dias de garantia).

### Campanha 3 — ALCANCE/SEGUIDORES impulsionando Reels orgânicos (opcional)
- Impulsionar a Aula/Lista que já foi bem no orgânico (R$ 10–20/dia por 3–5 dias) para crescer seguidores e alimentar o remarketing.
  Não é campanha de venda: é para encher o público da Campanha 2.

### (Depois) Campanha de MENSAGEM "APRENDER" no direct
- Anúncio que leva para o direct com a palavra APRENDER e o ManyChat responde com o link. Só quando o ManyChat estiver configurado.

## 5. O que precisa estar pronto ANTES de ligar (checklist)
- [ ] Gerenciador de Negócios + conta de anúncios + forma de pagamento (usuário).
- [ ] Instagram @eagle.english.br conectado à conta de anúncios (usuário).
- [ ] **Pixel**: criar no Gerenciador de Eventos e mandar o ID (usuário) → eu coloco no site (`/` e `/oferta`, eventos PageView,
      ViewContent, Lead no fim do quiz) e o usuário cola o mesmo ID na Kiwify (Produto → Pixel), que dispara InitiateCheckout e Purchase.
- [ ] Verificar o domínio na Meta (eagle-viagem.vercel.app ou domínio próprio — domínio próprio é melhor para anúncio).
- [ ] Order bump na Kiwify (decisão do usuário: qual produto e preço).
- [ ] 4 vídeos de anúncio (eu produzo: pessoa por IA + nosso personagem/telas do produto, voz Achird, legenda).
- [ ] Planilha de acompanhamento: gasto, impressões, CTR, custo por compra, vendas por UTM.

## 6. Métricas que importam (o que olhar no painel)
| Métrica | O que diz | Meta inicial |
|---|---|---|
| Hook rate (visualizações de 3 s ÷ impressões) | o gancho segura? | > 25% |
| CTR de link | o vídeo faz clicar? | > 1% |
| Custo por visualização da página | tráfego barato? | < R$ 1,50 |
| Taxa de compra (compras ÷ visitas) | a página converte? | > 2% |
| **Custo por compra (CPA)** | dá lucro? | **< R$ 24** |

Fontes do estudo: benly.ai/learn/meta-ads/creative-best-practices · scalewin.ai/blog/meta-advantage-plus ·
1clickreport.com/blog/advantage-plus-shopping-best-practices-2026 · admove.ai/blog/meta-advantage-creative-best-practices-for-2026 ·
keepersdigital.com (facebook-ads-creative-best-practices) · trafius.com.br/blog/cbo-ou-abo-qual-escolher-em-2026 ·
topgrowthmarketing.com/meta-ads-creative-testing-framework (blogs de agência: números são referência, não regra).
