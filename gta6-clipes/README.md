# Canal de clipes de GTA 6

Canal de cortes de streamers jogando e reagindo — começando por GTA 6 (TikTok, Reels, Shorts), com compilados longos no YouTube.
Nome: **Modo Replay** · @modoreplay_10 (Instagram, YouTube) · @modoreplay.10 (TikTok). Kit da marca e dos perfis: [`marca/perfis.md`](marca/perfis.md). Independente do Halftone e do Desvendando Ideias.

Plano completo: [`plano-do-canal.md`](plano-do-canal.md).

Pastas (criadas conforme o uso): `gravacoes/` (brutos, fora do git), `pautas/`, `cortes/`, `producoes/`.

## Fluxo de trabalho

1. **Você (PowerShell, na pasta `Videos\gta6-clipes`)** baixa o vídeo do YouTube:
   ```powershell
   yt-dlp -f "bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[height<=1080]" --merge-output-format mp4 -o nome.mp4 <link>
   ```
2. **Você** sobe o arquivo na pasta `gta6-clipes` do Google Drive (compartilhada como "qualquer pessoa com o link").
3. **Claude** baixa com `scripts/baixar-drive.sh <id> nome.mp4`, transcreve (OpenAI), escolhe os trechos (SupoClip, para vídeos longos com fala), monta e renderiza no `modelo/` (Remotion) e envia o corte no chat.

## Modelo de corte (`modelo/`)

Remotion, 1080×1920, 30 fps. O conteúdo de cada corte fica em `modelo/src/corte.json` (gancho, legendas, crédito, @ do canal); o vídeo base 9:16 vai em `modelo/public/base.mp4`.

```bash
cd gta6-clipes/modelo && npm install && npm run render
```
