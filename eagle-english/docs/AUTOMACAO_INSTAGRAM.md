# Automação do Instagram · Eagle English (25/11/2026)

Base: playbook "Instagram + Claude" (Metricool · Minter.io · Meta API + n8n). Escolha para o Eagle:

| Tarefa | Ferramenta | Por quê |
|---|---|---|
| Agendar Reels, carrosséis e stories (Instagram **e TikTok**) | **Metricool** + conector do Claude | Eu agendo direto daqui, toda manhã, depois da produção. Sem código. |
| Comentário → resposta pública + DM com o link | **ManyChat** (parceiro oficial da Meta) | Funciona com qualquer pessoa desde o 1º dia, sem revisão de app da Meta. |
| Métricas / relatório semanal | Metricool (o mesmo conector) | `getAnalyticsDataByMetrics`, `getBestTimeToPostByNetwork`. |

Por que NÃO Meta API + n8n agora: para mandar DM a pessoas que não têm papel no app, a Meta exige App Review
(permissão de mensagens em acesso avançado) + servidor n8n sempre ligado. Fica para quando o volume justificar.

## O que NÃO dá para automatizar
- **Adesivos de story** (quiz, link, enquete, caixinha) não podem ser colocados por API/agendador. Os stories 3 (quiz) e 4 (link)
  continuam manuais, com o aviso no celular. Os stories 1, 2 e 5 (sem adesivo) podem ser agendados.
- O TikTok não tem DM automática por comentário: lá, responder o comentário à mão ("te mandei no direct do Insta 📩").

## 1) Metricool (agendamento) — o que o usuário faz uma vez
1. Criar conta em metricool.com e conectar o Instagram profissional (@eagle.english.br) e o TikTok.
2. Em claude.ai → Configurações → Conectores → procurar **Metricool** → Conectar → autorizar a marca.
3. Me avisar. Eu testo listando a marca e agendando 1 post de teste para você conferir no planejador.
Plano: o grátis tem limite de posts agendados por mês; com ~4 a 6 por dia (Reels x2, carrossel, stories), confira o plano pago.
Depois disso a produção das 5h17 agenda: 09h stories 1-2 + carrossel · 12h Reels da aula · 18h story 5 · 19h Reels da noite
(Instagram e TikTok, com legenda e capa). Mídia vai por link público (os arquivos já ficam no GitHub público do projeto).

## 2) ManyChat (comentário → DM) — o que o usuário faz uma vez
1. manychat.com → entrar com o Instagram (@eagle.english.br) → permitir acesso a mensagens.
   No app do Instagram: Configurações → Mensagens → **Permitir acesso a mensagens** (ligado).
2. Automação → Novo → modelo **"Responder comentários com DM"** (Comment Growth Tool / Auto-DM from comments).
3. Gatilho: **Qualquer publicação ou Reel** · palavra-chave contém: `APRENDER`, `QUERO`, `CURSO`, `LINK`, `EAGLE`
   (maiúsculas/minúsculas tanto faz).
4. Resposta pública no comentário: ativar e colar as 4 variações abaixo (o ManyChat sorteia).
5. DM: colar a mensagem padrão abaixo com um **botão** "Fazer o teste" → link do teste.
6. Testar: comentar APRENDER com outra conta e conferir a resposta + a DM. Ligar.
Plano grátis: até 1.000 contatos (depois, plano Pro).

### Respostas públicas (sorteio)
1. Boa! 🔥 Te mandei no direct o próximo passo pra aprender do jeito fácil 📩
2. Mandei no seu direct! Abre lá que é rapidinho 😉
3. Aí sim! 🇺🇸 Olha seu direct: tem um teste de 1 minuto te esperando
4. Anotado ✅ Te chamei na DM, depois me conta o resultado 👇

### DM padrão (com botão)
Oi! Vi que você comentou aqui 🙌
Aqui o inglês é do jeito fácil: frase de verdade, pronúncia escrita do jeito que se lê e aula curtinha. Sem decoreba.
Fiz um teste de 1 minuto que mostra o melhor caminho pra você (pra você, pro seu filho, pra viagem ou pra quem já fez curso e não aprendeu) 👇
[Botão: Fazer o teste] → https://eagle-viagem.vercel.app/?utm_source=instagram&utm_medium=dm&utm_campaign=comentario

### Se a pessoa responder na DM (respostas rápidas salvas no ManyChat ou no Instagram)
- **"Quanto custa?"** → Tem 2 opções: Bagagem de Mão R$ 14,90 (ebook com as 2.100 frases) e Primeira Classe R$ 29,90 no
  lançamento (tudo + 10 aulas gravadas e áudios), que dá pra parcelar em até 3x no cartão. Os dois com 7 dias de garantia:
  https://eagle-viagem.vercel.app/oferta?utm_source=instagram&utm_medium=dm
- **"É pro meu filho"** → Serve sim, pra quem já lê bem: aula curtinha e frase do dia a dia, sem pagar cursinho caro. No começo vale
  um adulto acompanhar. Dá uma olhada: (link da oferta)
- **"Já fiz curso e não aprendi"** → Normal, a maioria aprende pra prova e esquece. Aqui é uma frase de verdade por vez, falada em voz
  alta, com a pronúncia escrita. Faz o teste que ele te mostra por onde começar: (link do teste)
- **"Depois eu vejo"** → Tranquilo! O link fica aqui salvo pra quando quiser 😉
Regras: sem promessa de fluência, sem "vagas acabando" inventado, preço só se perguntarem, 1 DM por comentário, nunca DM em massa.

## Resposta rápida para quem comenta "APRENDER" (manual, mandando pra bio) — 25/11
1. Boa! 🔥 O link tá na bio: faz o teste de 1 minuto e vê o jeito mais fácil pra você 🦅
2. Aí sim! 🇺🇸 Corre no link da bio que tem o próximo passo 👆
3. Anotado ✅ Toca no link da bio, o teste é rapidinho e já te mostra por onde começar
4. Bora! 💪 Tá tudo no link da bio: aula curtinha e pronúncia escrita, sem decoreba
5. Isso! 👏 Dá uma olhada no link da bio, vai te ajudar muito 😉
6. Que bom! 🙌 O link tá no perfil: começa pelo teste de 1 minuto
Atalho no Instagram: Configurações → Ferramentas para criadores/empresas → Respostas salvas → atalho "apr".
