# Ganchos, re-ganchos e copys — biblioteca adaptada (pesquisa Manus de 09/11/2026)

Fonte: `docs/pesquisas/manus-ganchos-copy-2026-11-09.jsonl` (168 peças: 60 ganchos, 30 re-ganchos, 20 CTAs de
engajamento, 20 pontes para o Eagle 350, 20 primeiras linhas de legenda, 18 comentários fixados).
**Limite da pesquisa:** o Manus não conseguiu métricas comparáveis (só 8 vídeos localizados, sem views/retenção).
Tudo aqui é HIPÓTESE editorial para testar com os nossos números, não "o que viraliza".

## O que adotamos (e como)

1. **Abrir pela situação ou tarefa, nunca por apresentação.** Nada de "Oi, gente" / "Hoje vou te ensinar".
   Gancho falado ≤ 12 palavras, texto na tela ≤ 8 palavras + 1 emoji, com funções diferentes:
   a fala convida ("Vai dormir? Vamos falar isso em inglês."), a tela nomeia a situação ("Inglês antes de dormir 🌙").
2. **Mascote grande no centro já com o contexto**: o cenário (ou uma prévia dos itens) mostra o assunto desde o
   1º quadro. Na abertura, NÃO mostrar frase em inglês/pronúncia/tradução — só o gancho.
3. **Primeira frase útil até ~5 s.** Abertura curta (3–4 s de fala).
4. **Participação de verdade:** 6 frases com pausa para repetir (`"pausa_repetir": 1.2` no roteiro.json) valem mais
   que 7 apressadas. No flashcard, a contagem já é a pausa.
5. **Re-gancho funcional** depois da 3ª frase: "Agora, tente antes de mim." / "Repete olhando só o inglês." /
   "Pode errar. Vamos tentar juntos." (evitar "espera até o final", "a última é a melhor").
6. **Uma ação de engajamento por vídeo**, escolhida pelo formato: Flashcard/Prova → "comenta seu placar";
   Repita → "salva pra repetir amanhã"; Qual você usa? → "comenta A ou B"; passeios/amigos → "envia pra quem…".
   O resto (seguir, outras perguntas) vai para a legenda e o comentário fixado.
7. **Ponte para o produto: consulta por situação, 5–12 s**, só com fatos da página. Frase-âncora:
   "Ache a frase certa em inglês para cada situação, sem travar na hora. Eagle 350: link na bio."
   "Essas frases estão num mapa do Eagle 350" SÓ quando as frases vierem de um mapa real (imagens em
   `assets/marca/paginas/site/`).
8. **Legenda (V3)**: 1ª linha com a situação/tarefa (≤ 90 caracteres) → salvar → seguir → Eagle 350 → as 5 hashtags do V3.

## O que NÃO adotamos

- Hashtags sugeridas pelo Manus (#InglesAmericano etc.): mantemos as 4 fixas do V3 + 1 do tema.
- Comentários com ressalva ("a pronúncia é só aproximação", "o guia não é promessa de prazo"): a regra de venda é
  só benefícios; esses avisos ficam fora.
- "Comenta que eu envio o link" (automação de DM): não temos entrega configurada.

## Plano de teste (4 semanas, uma variável por vez; anotar em 24 h, 72 h e 7 dias)

| Semana | Variável | A × B | Métrica |
|---|---|---|---|
| 1 | Gancho falado | pergunta ("Você sabe falar da sua manhã em inglês?" — já no ar) × situação ("Vai dormir? Vamos falar isso em inglês.") | retenção aos 3 s, % até o fim |
| 2 | Texto inicial | nome da situação × convite ("Repita estas frases comigo") | retenção aos 3 s, tempo médio |
| 3 | Re-gancho | transição neutra × "Agora, tente antes de mim." | % de conclusão |
| 4 | Ponte do produto | consulta por situação × mapas visuais | visitas ao perfil, cliques no link |

Manter iguais entre A e B: formato, dificuldade, duração aproximada, voz, posição do mascote, estilo visual.
Registrar: retenção 3 s, % conclusão, comentários/envios/salvamentos por alcance, visitas ao perfil, cliques no link.
