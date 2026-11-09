# Assistente pessoal no WhatsApp

Bot que conversa com você pelo WhatsApp, usa a OpenAI e acessa seu **Google Agenda** e **Gmail**.
Projeto independente do Halftone e do Desvendando Ideias.

**O que ele faz**
- Agenda: "o que tenho amanhã?", "marca dentista sexta 15h".
- Gmail: "tem e-mail novo importante?", "resume o último e-mail do banco", "responde o João dizendo que topo".
  E-mail **nunca sai direto**: ele cria um rascunho, mostra e só envia depois que você confirmar numa próxima mensagem
  (essa trava está no código, não só no prompt).
- Conversa geral: perguntas, resumos, traduções. Entende **áudio** (transcreve com a OpenAI).
- Comandos: `/ajuda`, `/limpar` (apaga a memória da conversa).
- Só responde aos números listados em `NUMEROS_PERMITIDOS` — mais ninguém consegue ler seus e-mails.

## Como funciona

```
WhatsApp ──► Meta (Cloud API) ──webhook──► app/main.py ──► app/agente.py ──► OpenAI
                                                │                  │
                                                │                  └─► app/ferramentas.py ──► Google Agenda / Gmail
                                                └─ memória da conversa: dados/assistente.db (SQLite)
```

| Arquivo | Papel |
|---|---|
| `app/main.py` | Servidor FastAPI: verifica o webhook, confere a assinatura da Meta, filtra números, evita duplicadas |
| `app/agente.py` | Prompt, memória, laço de chamadas de ferramenta, transcrição de áudio |
| `app/ferramentas.py` | Ferramentas que o modelo pode usar (+ trava de envio de e-mail) |
| `app/google_servicos.py` | Chamadas ao Google Agenda e Gmail |
| `app/whatsapp.py` | Enviar mensagem, baixar áudio, validar assinatura |
| `scripts/autorizar_google.py` | Autoriza sua conta Google uma vez e gera `token.json` |

## Configuração (uma vez)

### 1. Instalar

```bash
cd assistente
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
```

### 2. OpenAI
Crie uma chave em platform.openai.com → *API keys* e coloque em `OPENAI_API_KEY`.
O modelo padrão é `gpt-5.4-mini` (barato e bom com ferramentas); troque em `OPENAI_MODELO` se quiser.

### 3. WhatsApp (Meta for Developers)
1. Em developers.facebook.com crie um app do tipo **Business** e adicione o produto **WhatsApp**.
2. Em *WhatsApp → Configuração da API*: copie o **Phone number ID** (`WHATSAPP_PHONE_NUMBER_ID`)
   e adicione o seu celular como número de teste (destinatário).
3. Token: o temporário dura 24 h. Para um permanente, crie um **usuário do sistema** no Business Manager
   com permissão `whatsapp_business_messaging` e gere o token (`WHATSAPP_TOKEN`).
4. *Configurações do app → Básico*: copie a **Chave secreta do app** (`WHATSAPP_APP_SECRET`).
5. Invente uma frase para `WHATSAPP_VERIFY_TOKEN`.
6. Coloque seu número em `NUMEROS_PERMITIDOS` (ex.: `5511999999999`).

### 4. Google (Agenda + Gmail)
1. Em console.cloud.google.com crie um projeto e ative **Google Calendar API** e **Gmail API**.
2. *Tela de consentimento OAuth*: tipo **Externo**, adicione seu e-mail como usuário de teste.
   Depois, em *Público-alvo*, clique em **Publicar app** — no modo "Teste" o token expira em 7 dias.
3. *Credenciais → Criar → ID do cliente OAuth → App para computador*. Baixe o JSON como `assistente/credentials.json`.
4. No seu computador: `python scripts/autorizar_google.py` → entra na conta → cria `token.json`.

### 5. Rodar e ligar o webhook

```bash
uvicorn app.main:criar_app --factory --host 0.0.0.0 --port 8000
```

A Meta precisa de um endereço **HTTPS público**. Para testar no seu PC, use um túnel
(ex.: `cloudflared tunnel --url http://localhost:8000` ou `ngrok http 8000`).
Em *WhatsApp → Configuração → Webhook*: URL `https://SEU-ENDERECO/webhook`, token de verificação = `WHATSAPP_VERIFY_TOKEN`,
e assine o campo **messages**. Mande "oi" pro número do bot. 🎉

### 6. Deixar no ar 24 h
Qualquer serviço que rode Python serve (Render, Railway, Fly.io, uma VPS). Configure as mesmas variáveis do `.env`
e, em vez do arquivo, cole o conteúdo de `token.json` em `GOOGLE_TOKEN_JSON`. Comando de início:
`uvicorn app.main:criar_app --factory --host 0.0.0.0 --port $PORT`.
A memória fica em `dados/` — use um disco persistente se quiser que ela sobreviva a reinícios.

## Testes

```bash
python -m pytest -q
```

Os testes usam versões falsas da OpenAI, do WhatsApp e do Google (não gastam nada nem precisam de chave).

## Limites conhecidos / próximos passos
- O WhatsApp só deixa o bot **iniciar** conversa com modelos aprovados (fora da janela de 24 h).
  Por isso ainda não há lembretes proativos ("me avisa às 9h") — dá para adicionar com um modelo de mensagem aprovado.
- Imagens e documentos ainda não são lidos (só texto e áudio).
- A memória guarda as últimas `MEMORIA_MENSAGENS` mensagens de texto; resultados de ferramentas não ficam no histórico.
