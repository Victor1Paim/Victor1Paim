---
name: gemini-midia
description: >
  Generate narration audio (Gemini TTS) and, only when no other skill can, images (Gemini image models)
  through the user's Gemini API key, with a cost guard: dry run by default, cache by content, size limit per call
  and a usage log. Use for the voice of Desvendando Ideias videos (short and long) and for images that code-rendered
  or free skills cannot make. Not for music or sound effects.
---

# Gemini mídia (voz e imagem, com controle de custo)

Script único, sem dependências: `scripts/gemini.mjs` (Node 20+). A chave vem **só** da variável de ambiente
`GEMINI_API_KEY`.

## Chave (regras)

- Nunca pedir nem aceitar a chave no chat, nunca escrevê-la em arquivo do repositório, log, commit ou comando
  visível. O script envia a chave no cabeçalho `x-goog-api-key` e nunca a imprime.
- Se `GEMINI_API_KEY` não existir, parar e dizer ao usuário para adicioná-la nas configurações do ambiente
  (menu do ambiente na barra de título da sessão, depois Edit, em variáveis/segredos). Sessões novas a recebem.
- Domínio necessário: `generativelanguage.googleapis.com`.

## Comandos

```sh
node .claude/skills/gemini-midia/scripts/gemini.mjs models            # modelos de voz/imagem que a conta enxerga
node .claude/skills/gemini-midia/scripts/gemini.mjs tts --text-file roteiro.txt --out voz.wav --voice Kore --style "Fale em português do Brasil, tom curioso e claro"
node .claude/skills/gemini-midia/scripts/gemini.mjs tts ... --go      # chama de verdade
node .claude/skills/gemini-midia/scripts/gemini.mjs image --prompt-file p.txt --out img.png --aspect 9:16 --go
node .claude/skills/gemini-midia/scripts/gemini.mjs usage             # soma das chamadas feitas
```

Modelos padrão: `gemini-2.5-flash-preview-tts` (voz) e `gemini-2.5-flash-image` (imagem), trocáveis com `--model` ou
`GEMINI_TTS_MODEL` / `GEMINI_IMAGE_MODEL`. Esses nomes mudam: na primeira vez, rodar `models` e usar um que apareça.

Vistos na conta do usuário em 28/10/2026 (`models`): voz `gemini-3.8-flash-lite-tts`, `gemini-3.8-flash-tts`,
`gemini-3.1-flash-tts-preview`, `gemini-2.5-flash-preview-tts`, `gemini-2.5-pro-preview-tts`; imagem
`gemini-3.1-flash-lite-image`, `gemini-3.1-flash-image`, `gemini-3-pro-image`, `gemini-2.5-flash-image`.
Os "Lite" são a primeira tentativa para gastar menos: comparar com uma frase de teste e subir de modelo só se a
qualidade (pronúncia em pt-BR, ritmo) não servir. Teste de 41 caracteres com `gemini-3.8-flash-lite-tts`: 22 tokens de
entrada, 213 de saída, 8,6 s de áudio WAV 24 kHz mono. A estimativa de duração do modo simulação é grosseira.
A saída de voz é WAV mono (o Gemini devolve PCM 16 bits, normalmente 24 kHz).

## Como gastar o mínimo

1. **Ordem de preferência para voz:** VoiceStudio local (grátis, se estiver acessível) → Gemini → ElevenLabs.
2. **Ordem de preferência para imagem:** código (Remotion, SVG, `mg-styles-15`, `claude-animation-base`) e material
   próprio → Gemini imagem, só quando nenhuma skill resolve. Imagem de vídeo longo: gerar só as que carregam a
   explicação; reutilizar entre cenas.
3. **Sempre simulação primeiro.** Sem `--go` o script mostra modelo, tamanho e se há cache, sem chamar a API.
4. **Cache por conteúdo** (`producoes/.cache-gemini/`, fora do git). Mesmo texto, voz, estilo e modelo = zero custo.
   Por isso, dividir o roteiro **por cena** (um arquivo por trecho): ao corrigir uma frase, só aquela cena é regenerada.
5. **Teste curto antes do lote:** gerar 1–2 frases com a voz e o estilo escolhidos, aprovar, depois o resto.
6. **Limite por chamada:** 4000 caracteres (`--max-chars`). Textos maiores são recusados; dividir.
7. **Revisar o texto antes de gerar** (fatos, números, pontuação para o ritmo). Corrigir depois custa uma nova geração.
8. **Registrar:** `usage` mostra chamadas, caracteres e tokens por modelo. Conferir o preço vigente na página de preços
   do Gemini API e pedir ao usuário para configurar alerta de orçamento/cota no projeto da chave.
9. Usar uma voz e um estilo fixos para o canal (ver `desvendando-ideias/preparacao.md`) para nunca regenerar por inconsistência.

## Divulgação

Voz sintética e imagem gerada por IA podem exigir rótulo de conteúdo gerado/alterado por IA nas plataformas
(ver `desvendando-ideias/plano-do-canal.md`, seção 6). Imagens do Gemini levam marca d'água invisível (SynthID).
