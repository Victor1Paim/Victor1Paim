# Formato "Em inglês, como se diz…?" (referência enviada em 12/11/2026)

## O que as referências fazem (2 vídeos, 18–24 s, 720x1280)
- Começa DIRETO na 1ª pergunta, sem apresentação: "Em inglês, como se diz não sei?" (0–2 s).
- 3 rodadas, selo vermelho "1/3 · 2/3 · 3/3". Cada rodada ~7 s:
  pergunta falada em pt + tarja amarela com a frase em pt (MAIÚSCULAS) → 3 opções A/B/C em caixas escuras (erros típicos de
  brasileiro: "I know not", "You ready?", "Say me") → contagem 5→1 (~0,5 s por número) → só a certa numa caixa VERDE +
  pronúncia em outra caixa verde → resposta falada em inglês (às vezes 3x seguidas).
- Personagem simples grande no centro, falando. Fundo = vídeo REAL de viagem que muda a cada rodada.
- Acaba seco, sem CTA (favorece replay).

## Nossa adaptação
- Mascote oficial grande no centro (bico mexe com a voz), cores do perfil, Poppins.
- Beat `"comosediz"` no `montar_padrao.py` (pergunta, opcoes, certa, pron, audio_q, audio_r, repetir 2). Contagem 5→1 com tique,
  ding na revelação. Exemplo: `posts/como-se-diz-01/`.
- Erros das opções sempre de verdade (não marcar como errada uma forma correta).
- Fim: "Quantas você acertou? Comenta!" + CTA curto do Eagle 350 (~8 s) → vídeo de ~30 s (exceção à regra dos 40–70 s:
  o formato é curto de propósito).
- Fundo: o usuário vai mandar o estilo de fundo (provavelmente vídeo de viagem); até lá, fotos de cenário.
