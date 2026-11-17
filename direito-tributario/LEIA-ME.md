# Comece aqui

1. **Leia** `GUIA-COMPLETO.md` (o perfil, as regras, a estratégia e o kit) e `SKILLS-E-PROMPTS.md` (cada etapa com
   prompt pronto).
2. **Instale** (uma vez):
   - Windows: `winget install OpenJS.NodeJS.LTS`, `winget install Python.Python.3.12`, `winget install Gyan.FFmpeg`,
     feche e abra o terminal, dê dois cliques em `instalar.bat`.
   - Mac: `brew install node python@3.12 ffmpeg` e rode `./instalar.sh`.
3. **Teste:** `python scripts/kit.py tudo demo-cafezinho` (Mac: `python3`) → `videos/demo-cafezinho/final.mp4`.
4. **Seu primeiro vídeo:**
   ```
   python scripts/kit.py novo meu-video        # ou copie um roteiro de roteiros/ para videos/meu-video/roteiro.txt
   python scripts/kit.py ler meu-video         # texto para gravar
   (grave e salve como videos/meu-video/gravacao.mp4)
   python scripts/kit.py tudo meu-video        # resultado: videos/meu-video/final.mp4
   ```
5. **Usa o Claude Code?** Abra esta pasta nele e peça em português — o `CLAUDE.md` já explica tudo para ele.

Tudo roda no seu computador, sem custo (o Whisper transcreve localmente; o render também é local).
