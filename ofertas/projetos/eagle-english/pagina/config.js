/* ============================================================
   CONFIGURAÇÃO — edite SÓ este arquivo para fechar a página.
   Campos "" aparecem como pendentes (abra com ?dev=1 para ver a lista).
   ============================================================ */
window.EAGLE = {
  // Nomes dos planos (provisórios — trocar quando o usuário escolher)
  nomeSimples: "Eagle Bagagem de Mão",
  nomeAvancado: "Eagle Primeira Classe",

  // Checkouts da Kiwify (2 produtos separados)
  checkoutSimples: "",   // [PREENCHER] ex.: "https://pay.kiwify.com.br/XXXX"
  checkoutAvancado: "",  // [PREENCHER]

  // Preços
  precoSimples: "14,90",
  precoAvancadoCheio: "37",
  precoAvancado: "29,90",
  // Lançamento: preço promocional vale para as 100 primeiras vendas (o usuário troca na Kiwify ao bater 100).
  // Para encerrar a promoção: lancamento: false  (a página passa a mostrar só R$ 37).
  lancamento: true,
  textoLancamento: "Preço de lançamento para as 100 primeiras vendas",

  // Aulas gravadas do plano avançado: "" = já disponíveis; ou a data de liberação, ex.: "15/12"
  aulasLiberadasEm: "", // [PREENCHER se ainda não estiverem prontas]

  garantiaDias: 7,
  email: "",            // [PREENCHER] e-mail de contato
  instagram: "https://www.instagram.com/eagle.english.br/",
};
