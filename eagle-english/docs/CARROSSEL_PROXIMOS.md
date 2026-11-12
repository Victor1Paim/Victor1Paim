> **13/11: análise das capas de referência em `docs/REF_CAPAS_CARROSSEL.md` — capa = PAISAGEM NATURAL ÉPICA (não precisa
> combinar com o tema) + 🇺🇸 "Repita até aprender o inglês do dia a dia". Manda sobre as ideias de capa abaixo.**

# Próximos carrosséis "Repita até aprender…" (capa realista + slides 🇧🇷/🇺🇸/🗣️ + CTA do perfil)

Por que a capa do restaurante funcionou: foto natural com cara de foto de viagem (não ilustração), luz de pôr do sol,
cena desejável ligada ao tema, terço de baixo calmo para o texto branco. Repetir a fórmula.

**Fluxo combinado (12/11):** o usuário gera a CAPA (foto realista com o texto) pelo prompt; nós geramos os slides 02–08
(sem `img/capa.png`, o script começa no 02). Entregar: slides 02–08 + prompt da capa + legenda + comentário fixado. **Enviar CADA slide num envio separado** (um arquivo por envio, na ordem).

Produção: `posts/<data>_carrossel-<tema>/carrossel.json` → `python3 scripts/carrossel_tt.py posts/<post>` (8 slides 1080x1440).
Capa: `python3 scripts/imagem_gemini.py "<PROMPT>" posts/<post>/img/capa.png --post posts/<post> --proporcao 3:4 --modelo gemini-2.5-flash-image`
(~R$ 0,21). CTA: `{"perfil": "img/perfil.png", "texto": "..."}` (copiar o perfil.png do carrossel do restaurante).

**Regra do usuário (12/11): VARIAR SEMPRE o cenário da capa** — nunca repetir o tipo de lugar/luz/enquadramento do carrossel
anterior (ex.: restaurante ao pôr do sol → bangalô nas Maldivas → janela de avião ao amanhecer → café em NY no outono…).

Final comum de todos os prompts de capa (já incluído abaixo):
"…cinematic, rich natural colors, shallow depth of field, vertical 3:4, the lower third slightly darker and calm (space for
text), no people faces, no text, no letters, no signs, no logos."

---

## ⭐ Ideia 1 (recomendada): "Repita até aprender o inglês do HOTEL" 🏨
Por quê: continua a "viagem" do restaurante (quem salvou um, salva o outro) e conversa com o fundo das Maldivas dos vídeos.

**Prompt da capa**
```
Breathtaking natural travel photograph at golden hour: the private wooden deck of an overwater villa in the Maldives,
two lounge chairs and a small table with fresh juice facing a calm turquoise lagoon, the sun setting on the horizon with
warm orange and pink sky reflected on the water, cinematic, rich natural colors, shallow depth of field, vertical 3:4,
the lower third slightly darker and calm (space for text), no people faces, no text, no letters, no signs, no logos.
```
Texto da capa: "Repita até aprender\no inglês do hotel"

**Frases (pt-BR · inglês · pronúncia)**
1. Tenho uma reserva no meu nome. · I have a reservation under my name. · ái HÉV a ré-zer-VÊI-xân ÂN-der mái NÊIM
2. Que horas é o check-out? · What time is check-out? · UÓT TÁIM iz TCHÉK-áut?
3. O café da manhã está incluído? · Is breakfast included? · iz BRÉK-fâst in-KLÚ-did?
4. Qual é a senha do Wi-Fi? · What's the Wi-Fi password? · UÓTS the UÁI-fái PÉS-uârd?
5. Posso deixar minhas malas aqui? · Can I leave my bags here? · kén ái LÍIV mái BÉGZ RÍER?
6. Pode me chamar um táxi? · Could you call me a taxi? · kud iú KÓL mi a TÉK-si?

Legenda: "Repita até aprender o inglês do hotel 🇺🇸🏨 / Salva pra sua próxima viagem 📌" + bloco V3 + hashtags
#inglesparabrasileiros #inglesdodiaadia #frasesemingles #inglesparaviagem #inglesnohotel

---

## Ideia 2: "Repita até aprender o inglês do AEROPORTO" ✈️
**Prompt da capa**
```
Breathtaking natural travel photograph at sunrise: the view through an airplane window seat, the wing glowing in golden
light above a sea of soft pink and orange clouds, a passport and a boarding pass resting on the tray table in the
foreground, cinematic, rich natural colors, shallow depth of field, vertical 3:4, the lower third slightly darker and calm
(space for text), no people faces, no text, no letters, no signs, no logos.
```
Frases: Where is gate 12? · Could I have a window seat? · Is this flight on time? · Where is baggage claim? ·
I have a connecting flight. · How long is the delay?

---

## Ideia 3: "Repita até aprender o inglês da CAFETERIA" ☕
**Prompt da capa**
```
Breathtaking natural photograph on a cozy autumn afternoon: a latte with heart latte art and a croissant on a wooden table
by the big window of a charming coffee shop in New York, warm golden light, a blurred brownstone street with orange
autumn trees outside, cinematic, rich natural colors, shallow depth of field, vertical 3:4, the lower third slightly
darker and calm (space for text), no people faces, no text, no letters, no signs, no logos.
```
Frases: Can I get a latte, please? · For here or to go? · Can I have it with oat milk? · How much is it? ·
Can I pay by card? · Do you have Wi-Fi?

---

Ordem sugerida: Hotel → Aeroporto → Cafeteria (série "viagem" primeiro, que é o que salvou mais).
