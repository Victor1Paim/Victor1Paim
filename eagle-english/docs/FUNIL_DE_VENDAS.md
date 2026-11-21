# Funil de vendas — Eagle English BR (rascunho 21/11/2026)

Site e páginas: desenvolver no branch **`estudio-ofertas`** (skill `criar-oferta`, pasta `ofertas/projetos/eagle-english/`:
briefing → pesquisa → oferta → copy → página → divulgação; modelos em `ofertas/modelos/`). Página atual: https://eagle-pagina.vercel.app/
(o link da bio https://kiwify.app/KQ1i4Ps redireciona para ela; checkout na Kiwify).

## Produtos que já existem (PDFs do usuário)
| Produto | O que é | Tamanho |
|---|---|---|
| **Eagle 350 Mapas Visuais** | 35 situações × 10 mapas × 6 frases = 2.100 frases, tradução + pronúncia escrita, sumário clicável, 9 partes | 389 págs |
| **500 Frases para o Dia a Dia** | seleção de 500 frases do ebook, reorganizadas em 25 situações (não são frases novas) | 104 págs |
| **Guia de 21 Dias** | rotina de 15 min/dia: 3 mapas por dia, frase em voz alta, missão, revisões, progresso | 27 págs |
| **100 Combinações de Verbos** | 60 combinações (make/do/take/have/get…) + 40 phrasal verbs, 40 exercícios + gabarito | 62 págs |
| **Cards de Gramática** | 20 cards, 120 frases, do to be ao present perfect | 24 págs |

## Funil proposto
```
Conteúdo diário (1 verbo por dia + Lista 12 + ABC + Caderno…) → link na bio
        ↓
[PÁGINA] Eagle 350 + bônus  ............................ FRONT  R$ 19,00
        ↓ (no checkout)
[ORDER BUMP] opcional — ver nota  ....................... R$ 9,90–14,90
        ↓ (pós-compra, 1 clique)
[UPSELL] Método Fluência Eagle (aulas em vídeo + pronúncia + exercícios) + 100 Combinações de Verbos  ... R$ 47–67
        ↓ (se recusar)
[DOWNSELL] Cards de Gramática  .......................... R$ 9,90
        ↓
Área de membros / e-mail: Guia de 21 Dias puxa o uso diário → prova social (prints de progresso) → volta para o conteúdo
```

### 1) Front — Eagle 350 (R$ 19,00)
- Entrega: ebook + **500 Frases** (bônus, como o usuário pediu) + **Guia de 21 Dias** (recomendo manter no front: é o que faz a pessoa
  USAR o ebook e voltar satisfeita; sem ele o reembolso tende a subir).
- Por que o bônus 500 Frases precisa ser apresentado com cuidado: a própria página diz que é seleção do ebook → vender como
  "versão de bolso / consulta rápida", não como "500 frases novas".

### 2) Upsell — "Método Fluência Eagle" (nome provisório)
Aulas guiadas **no mesmo formato dos nossos vídeos** (personagem, caixa amarela inglês / verde pronúncia / branca tradução, palavra
falada destacada, "repita comigo" com pausa), mais exercícios. Proposta de estrutura (30 aulas curtas, 3–5 min):
| Módulo | Aulas | O que treina |
|---|---|---|
| 1. Os sons que travam o brasileiro | 8 | TH, R americano, vogais longas × curtas, -ED, -S final, consoante final, "schwa", ritmo |
| 2. Os verbos que destravam a fala | 10 | make/do/take/have/get/go… em blocos (usa as 100 Combinações) — conversa com a série "1 verbo por dia" |
| 3. Frases em voz alta (shadowing) | 8 | situações do Eagle 350 em ritmo lento → normal → nativo, com pausa para repetir |
| 4. Conversas simuladas | 4 | "Se um gringo te disser…": responder rápido, com roteiro |
+ exercícios por aula (escute e repita, complete, ditado, "grave e compare"), folha de pronúncia em PDF, **100 Combinações de Verbos** junto.
Produção: o nosso pipeline (Achird, Whisper, personagem SVG) já faz isso — custo de voz baixo por aula.
**Cuidado com o nome:** "Fluência" vira promessa. Ou mantemos o nome e a copy diz claramente o que entrega (pronúncia e fala do
dia a dia, sem prometer fluência), ou trocamos: "Método Eagle de Fala", "Eagle Destrava", "Método Voo Eagle".
Preço sugerido: R$ 47 (lançamento R$ 37). Testar.

### 3) Downsell — Cards de Gramática (R$ 9,90)
Aparece só para quem recusou o upsell. Ângulo: "a base que falta para montar suas próprias frases".

### 4) Order bump (opcional, decidir)
Hoje nenhum produto sobra para bump sem canibalizar o upsell/downsell. Opções: (a) não usar bump no começo; (b) bump de um
"Pack de áudio das 100 frases mais usadas" (não existe ainda — a página atual diz "não tem áudio", e é a objeção mais comum);
(c) bump = Cards de Gramática (aí o downsell vira outra coisa). Recomendo (b) quando tivermos o áudio — gerado pelo nosso pipeline.

## Problemas encontrados na página atual (eagle-pagina.vercel.app — leitura do HTML)
1. Preço aparece como o marcador "⟦preço⟧" em todos os blocos e "Soma dos valores individuais R$ 0,00" (pode ser preenchido por
   JavaScript — conferir no celular; se aparecer assim, a página não vende).
2. Contador "termina em" sem data/tempo (urgência falsa/vazia — tirar ou usar prazo real).
3. "Quem já usa, conta" sem nenhum depoimento — preencher com depoimentos REAIS (prints de DM/comentários) ou tirar a seção.
4. E-mail de contato vazio; título "Quem criou" trocado com o da garantia.
5. Página conta "5 materiais"/"4 bônus" de jeitos diferentes; reorganizar quando os produtos forem redistribuídos no funil
   (Cards e 100 Combinações saem do pacote e viram upsell/downsell).
6. Nenhuma demonstração em vídeo — usar um dos nossos vídeos (ex.: Caderno falado) como "veja por dentro".

## Próximos passos
1. Usuário confirma: nome do upsell, preços, se o Guia de 21 Dias fica no front, e o order bump.
2. Briefing + oferta em `ofertas/projetos/eagle-english/` (branch `estudio-ofertas`) — precisa de autorização para trabalhar nesse branch.
3. Ajustar a página atual (preço, provas, bônus) e criar as páginas de upsell/downsell (1 clique na Kiwify).
4. Produzir a aula 1 do upsell como amostra (vídeo + exercício) para validar o formato.
5. Divulgação: CTA do produto só na legenda dos vídeos (regra atual) + stories com o link + carrosséis com CTA do perfil.
