---
name: pagina-de-vendas
description: Criar ou revisar página de vendas, landing page, página de captura, VSL, página de obrigado ou de lançamento (infoproduto, serviço, produto físico). Cobre copy (estrutura e gatilhos), seções, design de conversão, pixels e checkout. Use junto com dev-senior.
---

# Página de vendas

## 1. Antes de escrever
Colete: produto/oferta, preço e condições, público e dor principal, promessa,
provas (depoimentos, números, prints), bônus, garantia, link de checkout,
pixel (Meta/Google/TikTok). Faltou prova? Marque `[PREENCHER]` — **nunca invente
depoimento, número ou resultado**.

## 2. Estrutura padrão (ordem)
1. **Hero**: headline (promessa + prazo/mecanismo), subheadline, CTA, prova rápida
   (nota, nº de alunos) e imagem/vídeo do produto. Tudo visível sem rolar no celular.
2. **Dor / problema** (PAS: problema → agitação → solução).
3. **Apresentação da solução** e o mecanismo único.
4. **O que você recebe** (módulos/entregáveis em cards).
5. **Para quem é / para quem não é**.
6. **Prova social** (depoimentos reais, prints, logos).
7. **Quem é o autor/marca**.
8. **Bônus** com valor percebido.
9. **Oferta**: ancoragem de preço, parcelamento, CTA forte.
10. **Garantia** (selo + texto).
11. **FAQ** (5–8 objeções reais).
12. **CTA final** + rodapé (CNPJ/contato, termos, privacidade).

CTA a cada 2–3 seções. Em celular, botão fixo no rodapé após o hero.

## 3. Copy
- Fale com "você", frases curtas, benefício antes de característica.
- Headline: teste 3 variações e mostre ao usuário.
- Gatilhos com honestidade: escassez/urgência só se forem reais.
- Evite promessas proibidas (saúde, renda garantida) — regras de anúncio Meta/Google.

## 4. Design de conversão
- Uma ação por página. Sem menu que tire o usuário da página.
- Cor do CTA exclusiva (não usada em outro elemento).
- Seções alternando fundo; largura de texto ≤ 70 caracteres.
- Vídeo (VSL): embed leve (facade/thumbnail que carrega o player no clique).

## 5. Técnico
- Arquivo único estático (HTML + Tailwind) ou Astro; peso alvo < 1 MB acima da dobra.
- Pixels/analytics num só lugar (`<head>`), eventos `ViewContent` e `InitiateCheckout` no CTA.
- UTMs repassadas ao link de checkout (script simples copiando `location.search`).
- Página de obrigado separada (evento `Lead`/`Purchase` quando aplicável).
- Checar em 390px e 1440px antes de entregar.
