# Kit de vídeos — Direito Tributário (Isabela)

> **RASCUNHO.** A versão final deste guia (com pautas e briefing) sai depois do resultado da pesquisa
> (`pesquisa/prompt-manus.md`). Os comandos e as marcações abaixo já funcionam.

Você grava o vídeo falando para a câmera. O kit coloca **elementos desenhados flutuando** ao seu redor na hora
certa da fala (ícones, etiquetas, carimbos, moedas, zoom), troca para **tela dividida** ou **motion em tela cheia**
quando o roteiro pede, e põe **legenda**. Tudo roda no seu computador, de graça (sem chave de API).

Exemplo pronto: `videos/demo-cafezinho/` (a "gravação" do demo é uma apresentadora ilustrada só para teste).

---

## 1. Instalar (uma vez só)

**Windows** — abra o *Prompt de Comando* e rode, um por vez:
```
winget install OpenJS.NodeJS.LTS
winget install Python.Python.3.12
winget install Gyan.FFmpeg
```
Feche e abra o Prompt de novo. Depois dê dois cliques em **`instalar.bat`** (nesta pasta).

**Mac** — instale o Homebrew (https://brew.sh), depois no Terminal:
```
brew install node python@3.12 ffmpeg
cd caminho/da/pasta/direito-tributario
./instalar.sh
```

Teste: `python scripts/kit.py tudo demo-cafezinho` (no Mac: `python3`). O primeiro uso baixa o Whisper
(~500 MB) e o navegador do render — precisa de internet só dessa vez. Resultado: `videos/demo-cafezinho/final.mp4`.

> Se você usa o Claude Code no computador: abra esta pasta nele e peça "me ajuda a rodar o kit do LEIA-ME".

---

## 2. Fazer um vídeo (o dia a dia)

Todos os comandos são rodados **dentro da pasta `direito-tributario`**. No Mac troque `python` por `python3`.

1. **Roteiro.** Escolha um em `roteiros/` ou crie um novo:
   `python scripts/kit.py novo pix-01` → abre `videos/pix-01/roteiro.txt` e escreva (ou cole um de `roteiros/`).
2. **Texto para gravar.** `python scripts/kit.py ler pix-01` → `videos/pix-01/texto-para-gravar.txt`
   (só a fala, sem marcações — bom para teleprompter).
3. **Gravar** no celular, **em pé (vertical)**:
   - rosto no terço de cima da tela, com **espaço livre dos dois lados** (é onde os elementos aparecem);
   - luz de frente, fundo simples, celular na altura dos olhos;
   - pode errar e repetir a frase — só corte o começo e o fim. Pode improvisar um pouco: o kit acompanha.
4. **Copiar** o vídeo para `videos/pix-01/` com o nome `gravacao.mp4` (ou `.mov`).
5. **Gerar:** `python scripts/kit.py tudo pix-01` → `videos/pix-01/final.mp4`.
6. Quer ver antes / ajustar? `cd video` e `npm run dev` (abre no navegador; escolha **kit**). Mexeu no
   roteiro? Rode `python scripts/kit.py preparar pix-01` de novo (é rápido: não transcreve outra vez).

**Sem roteiro marcado?** Se a pasta não tiver `roteiro.txt`, o kit escolhe elementos sozinho pelas palavras que
você falou (lista em `dicionario-elementos.json`). Bom para vídeos improvisados.

---

## 3. Como marcar o roteiro

O roteiro é texto normal. Duas coisas extras:

**Linhas com `#` mudam o modo da tela** (valem até o próximo `#`):

| Linha | O que acontece |
|---|---|
| `# ela` | você em tela cheia, elementos flutuando (use em ~70% do vídeo) |
| `# dividida lista \| Título` | você em cima, cartão em motion embaixo |
| `# motion lista \| Título` | tela cheia só de informação (sua voz continua) |

Modelos de cartão: `lista` · `passos` (numerado) · `comparacao` (título "A x B") · `numero` · `definicao` · `mito`.
Opcional: `# motion definicao | Malha fina | icone=lupa`.

**`[colchetes]` criam elementos** — coloque **logo antes da palavra** em que ele deve aparecer:

| Marcação | Exemplo |
|---|---|
| ícone flutuante | `[icone casa]` |
| etiqueta | `[etiqueta IPTU \| amarelo]` · com ícone: `[etiqueta MEI \| azul \| icone=empresa]` |
| número grande | `[numero 27,5%]` |
| carimbo | `[carimbo MITO \| vermelho]` |
| interrogação | `[pergunta]` |
| chuva de moedas | `[moedas]` |
| zoom de câmera | `[zoom]` |
| seta | `[seta aumenta \| cima]` · `[seta cai \| baixo]` |
| **dentro de cartão** | `[item texto]` (lista/passos) · `[esquerda texto]` `[direita texto]` (comparação) · `[destaque texto]` (número, definição, mito) — aceitam `\| icone=nome` |

Opções depois de `|`: cor (`amarelo`, `verde`, `azul`, `laranja`, `vermelho`), lugar (`topo`, `esquerda-alto`,
`direita-alto`, `esquerda`, `direita`, `esquerda-baixo`, `direita-baixo`), duração (`3s`).
Sem lugar, o kit distribui sozinho sem tampar o rosto.

**Ícones disponíveis:** cofre, carteira, sacola, casa, lixeira, caminhao, loja, lupa, cone, marcador, calendario,
documento, declaracao, nota, carro, alerta, check, xis, grafico, balanca, pix, celular, empresa, livro, saude,
relogio, dica, cafe, moedas.

Exemplo completo: `roteiros/imposto-no-cafezinho.txt`.

---

## 4. Ajustes finos (opcional)
Crie `videos/<nome>/ajustes.json`:
```json
{ "legenda": true, "enquadramentoDividida": -170 }
```
`enquadramentoDividida` sobe/desce seu rosto na tela dividida (mais negativo = sobe). Depois rode `preparar` de novo.

## 5. Problemas comuns
| Mensagem | Solução |
|---|---|
| `não achei a gravação` | o vídeo precisa estar em `videos/<nome>/` como `gravacao.mp4` ou `.mov` |
| `ffmpeg` não encontrado | instale o FFmpeg (passo 1) e abra o terminal de novo |
| `roteiro x gravação: 40%` | a fala ficou muito diferente do roteiro: ajuste o roteiro ao que foi dito |
| elemento aparece cedo/tarde | mude a marcação de lugar no roteiro (antes de outra palavra) |
| render lento | normal: ~1 a 3 min para 30 s. Feche outros programas |
| transcrição errada | `python scripts/kit.py preparar <nome> --modelo medium --refazer` (mais lento, mais preciso) |

**Antes de postar:** confira as fontes jurídicas indicadas no topo de cada roteiro (`#` comentários).
