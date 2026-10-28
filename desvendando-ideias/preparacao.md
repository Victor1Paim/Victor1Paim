# Desvendando Ideias — Preparação (uma vez só)

Passos que dependem do seu computador. Marque cada um quando terminar.

## 1. Instalar o VoiceStudio (voz do canal)

- [ ] Baixar o app em <https://github.com/debpalash/VoiceStudio/releases/latest> (Mac Apple Silicon, Windows ou Linux). Guias por sistema: `docs/install/` no repositório.
- [ ] Abrir o app e instalar **um** modelo de voz pelo gerenciador de modelos (comece pelo padrão, VoiceStudio/OmniVoice). Os modelos são baixados pelo app e podem ser grandes.
- [ ] Conferir que o servidor responde: abra `http://localhost:3900/health` no navegador. Deve retornar OK.

## 2. Criar a voz do canal

- [ ] Escolher entre **criar uma voz por descrição** (sem precisar de gravação de ninguém) ou **clonar a sua** (só voz que você tem direito de usar).
- [ ] Gravar 3 amostras do mesmo texto (um trecho de roteiro de 30s) com opções diferentes e escolher uma.
- [ ] Salvar como perfil com o nome `desvendando-ideias` e anotar abaixo o nome e o ID do perfil.

| Item | Valor |
|---|---|
| Nome do perfil | `desvendando-ideias` |
| ID do perfil | _(preencher)_ |
| Idioma | pt-BR |
| Descrição (tom, ritmo) | _(preencher)_ |

Regra: toda narração do canal usa **este perfil**. Nunca os nomes de voz de compatibilidade (alloy etc.).

## 3. Como o áudio chega ao projeto

A sessão do Claude na nuvem não alcança o `localhost` do seu computador. Escolha um caminho:

- **A. Você gera no app (mais simples):** cola o texto do roteiro, gera `.wav` e coloca em `desvendando-ideias/producoes/<video>/voz.wav` (commit/push ou envio na conversa). Eu faço o resto (legenda, montagem).
- **B. Endereço acessível:** se você expuser o servidor por um endereço que a sessão alcance, eu chamo a API direto. Só faça isso com autenticação ligada; não exponha o servidor aberto na internet.
- **D. Gemini (configurado):** a voz é gerada pela API do Gemini com a skill `gemini-midia`, direto da sessão na nuvem, sem depender do seu computador. A chave fica só em variável de ambiente (`GEMINI_API_KEY`). Mantém o VoiceStudio como opção grátis e local quando você instalar.
- **C. Sessão local:** usar o Claude Code instalado no seu computador, onde `localhost:3900` existe.

Caminho escolhido: _(preencher)_

**Tentativa de instalar na nuvem (28/10/2026):** o backend (`node scripts/setup-api.mjs`, versão CPU) parou porque a rede
do ambiente bloqueou `download-r2.pytorch.org`. `huggingface.co`, de onde vêm os pesos das vozes, também está bloqueado.
Para instalar no ambiente da nuvem, é preciso liberar esses domínios em *Network access* (Allowed domains) e depois
repetir. Mesmo liberado, o servidor some quando a sessão termina e roda só em CPU, então o app no seu computador
continua sendo o caminho principal.

## 4. Teste final (5 min)

- [ ] Gerar 20s de narração com o perfil do canal.
- [ ] Transcrever o próprio áudio e conferir se o texto bate (valida o modelo de transcrição para as legendas).
- [ ] Anexar o `.wav` ao projeto e confirmar que a duração e o formato estão corretos.

## Próximo passo

Definir o **processo de uso das skills com o menor gasto possível**: quais skills ficam fora do caminho padrão, o que roda local e grátis (VoiceStudio, Kokoro, ffmpeg, Remotion), o que só entra quando necessário (ElevenLabs, geração de imagem) e um passo a passo por tipo de vídeo (curto e longo).
