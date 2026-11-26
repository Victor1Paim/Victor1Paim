# Motor de produção — passo a passo

Rodar de dentro de `canal-terror/`. Cada etapa guarda o que já fez: refazer uma parte é apagar o arquivo dela e rodar de novo.

```bash
P=producoes/NOME
```

1. **História** em `historias/NOME.md` (texto depois da linha `---`, um parágrafo por bloco).
2. **Voz** (Gemini, Enceladus) → `$P/voz/narracao.wav` e `tempos.json`:
   ```bash
   python3 -I motor/voz.py historias/NOME.md $P
   ```
3. **Planos**: escrever `$P/planos.json` (título, cartela, estilo, vinheta e 1–2 planos por parágrafo; `"reusar"`, `"arquivo"` e `"carimbo"` disponíveis). Modelo: `producoes/piloto/planos.json`.
4. **Imagens** (OpenAI `gpt-image-2`, medium, US$ 0,042 cada) → `$P/imagens/`:
   ```bash
   python3 -I motor/imagens.py $P --simular   # conta e custo antes
   python3 -I motor/imagens.py $P
   ```
5. **Trilha** (sintetizada aqui, sem custo):
   ```bash
   python3 -I motor/trilha.py $P/trilha --duracao SEGUNDOS_DO_VIDEO
   ```
6. **Montagem** (rascunho 540p em ~3 min; final 1080p em ~10 min):
   ```bash
   python3 -I motor/montar.py $P --rascunho
   python3 -I motor/montar.py $P
   ```
7. **Legenda** (.srt, Whisper, US$ 0,006/min): `python3 -I motor/legendas.py $P`
8. **Miniatura**: imagem base em qualidade *high* + `python3 -I motor/miniatura.py BASE.png $P/final/miniatura.jpg "LINHA 1" "LINHA 2" --destaque 2`

## Créditos

Se a OpenAI ou o Gemini recusarem por falta de crédito ou cota diária, o script **para** e imprime
`*** … a API recusou por COTA/CRÉDITO …`. Limite por minuto (429 comum) não para: o script espera e tenta de novo.
Chave do Gemini: `~/.config/canal-terror/gemini.key` (fora do repositório) ou `GEMINI_API_KEY`. OpenAI: proxy da sessão.

## Gasto real

- Voz: `node ../.claude/skills/gemini-midia/scripts/gemini.mjs usage` (rodar em `canal-terror/`), US$ 9 por 1 milhão de tokens de saída.
- Imagens: `$P/imagens/custos.jsonl`.
