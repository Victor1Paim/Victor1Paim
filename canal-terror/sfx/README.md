# Biblioteca de efeitos sonoros do canal

Todos os sons foram gerados no **ElevenLabs Sound Effects** (decisão do usuário: efeitos só do ElevenLabs).
Ficam no repositório para não depender da assinatura: o que foi gerado em plano **pago** pode ser usado comercialmente
para sempre, mesmo depois de cancelar (help center do ElevenLabs). O que for gerado no plano grátis **não** pode.

- `catalogo.json` — id, categoria, prompt usado, duração, loop, tags. `gerados.jsonl` — quando, duração e créditos de cada um.
- `trilha/` drones em loop (30 s), stings, vinheta, riser, whoosh · `ambiente/` loops de 30 s · `efeito/` sons pontuais.
- 26/11/2026: 48 sons, ~9 min, 6.639 créditos.

Uso:
```bash
python3 -I motor/sfx.py listar porta        # procura por id ou tag
python3 -I motor/sfx.py gerar --so novo-id  # depois de acrescentar o novo efeito no catalogo.json
```
Numa produção: `sfx.json` na pasta de cada história (ambientes por parágrafo e efeitos presos a uma frase da narração,
ganhos em dB relativos à voz) e `"trilha": {"drone", "sting", "vinheta"}` no `coletanea.json` / `planos.json` / `short.json`.
Formato em `motor/sfxmix.py`.
