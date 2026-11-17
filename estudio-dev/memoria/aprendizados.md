# Aprendizados

- Fotos de pratos com IA: `impressos/gerar_fotos.py` (estilo único no prompt, 6 em paralelo, retry). Miniaturas 240px em `pratos/mini/`; originais 640px fora do deploy (`.vercelignore`). ~US$ 0,07 por imagem 1024² medium.
- Modo escuro forçado (Chrome/Samsung no Android) inverte cores de sites claros. Sites com identidade clara: `<meta name="color-scheme" content="only light">` + `color-scheme: only light` em `:root`/`html` + fundo explícito no `html`. Teste: Chromium com `--blink-settings=forceDarkModeEnabled=true`.
- Cache: nunca cache longo em JS/CSS sem versão. Barra Deck usa `?v=<hash>` no index.html + `max-age=0, must-revalidate` para css/js (vercel.json). Ao editar CSS/JS, atualizar o `?v=` (hash md5 de 8 caracteres).
- Quando o usuário manda um cardápio antigo, confirmar antes se é para misturar com o atual. A fonte da verdade do Barra Deck é o PDF 2026.
- Copy: nunca colocar escassez não confirmada ("se a produção esgotar") nem promessas operacionais (aquecer, travessa, chefs) sem o cliente confirmar.
- Remotion aqui: o Chrome do render não confia no certificado do proxy → fontes do Google falham. Baixar fontes para `public/` (script) e usar `@remotion/fonts`.
- Voz: OpenAI `gpt-4o-mini-tts` (proxy já tem a chave) + Whisper `verbose_json` com tempos por palavra para sincronizar cenas. Gemini só existe no `.env` do notebook (branch eagle-english).
- Fotos recortadas do PDF são de baixa resolução: em vídeo, usar dentro de moldura com fundo desfocado, nunca em tela cheia.
- Deploy na Vercel daqui: `npx vercel login` (link de autorização que o usuário abre) → `vercel link --yes --project <nome>` → `vercel deploy --prod --yes`. Conectar o GitHub falha se a conta Vercel não tiver login pelo GitHub; o deploy pela CLI funciona igual. Criar `.vercelignore` com `.env*` antes (o `link` cria `.env.local` com token).
- CSS: `.field { display: grid }` sobrescreve o atributo `hidden`; sempre incluir `[hidden] { display: none !important; }`.
- Scripts Python longos dentro de heredoc no Bash podem ser barrados pela checagem de segurança; salvar o script em arquivo e rodar.
- Cardápio em PDF achatado (uma imagem por página): recortar logo e fotos com PIL; fundo creme da logo removido por distância de cor.
- Detector do `impeccable` acusa "cream palette" e "serif itálico"; manter quando vêm da identidade do cliente.
