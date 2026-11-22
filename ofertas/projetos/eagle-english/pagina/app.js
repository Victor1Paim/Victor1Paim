(function () {
  const C = window.EAGLE || {};
  const pend = [];

  // textos vindos do config
  document.querySelectorAll("[data-c]").forEach(el => {
    const v = C[el.dataset.c];
    if (v === "" || v == null) { pend.push(el.dataset.c); el.textContent = "[PREENCHER]"; }
    else el.textContent = v;
  });
  // links
  document.querySelectorAll('[data-href="instagram"]').forEach(a => a.href = C.instagram || "#");
  document.querySelectorAll('[data-href="mailto"]').forEach(a => { if (C.email) a.href = "mailto:" + C.email; });
  if (!C.email) document.getElementById("faq-contato").querySelector("p").innerHTML =
    'Pelo Instagram <a href="' + (C.instagram || "#") + '" target="_blank" rel="noopener">@eagle.english.br</a>.';

  // checkouts (repassa UTMs da URL para a Kiwify)
  const utm = new URLSearchParams(location.search);
  [...utm.keys()].forEach(k => { if (!k.startsWith("utm_") && k !== "src") utm.delete(k); });
  document.querySelectorAll("[data-checkout]").forEach(a => {
    const url = C[a.dataset.checkout];
    if (!url) { a.href = "#planos"; a.setAttribute("aria-disabled", "true"); pend.push(a.dataset.checkout); return; }
    const u = new URL(url); utm.forEach((v, k) => u.searchParams.set(k, v)); a.href = u.toString();
  });

  // preço do avançado (lançamento só enquanto lancamento: true)
  const pa = document.getElementById("preco-avancado");
  pa.innerHTML = C.lancamento
    ? `<div class="de">De R$ ${C.precoAvancadoCheio}</div><div class="por"><small>R$</small> ${C.precoAvancado}</div><div class="unico">pagamento único</div><span class="promo">🔥 ${C.textoLancamento}</span>`
    : `<div class="por"><small>R$</small> ${C.precoAvancadoCheio}</div><div class="unico">pagamento único</div>`;
  if (C.aulasLiberadasEm) document.getElementById("aulas-nota").textContent = "pronúncia e fala, com exercícios · liberadas a partir de " + C.aulasLiberadasEm;

  // comparação com o combo Big Mac no iFood (R$ 46,90): vale com R$ 29,90 e com R$ 37
  const gp = document.getElementById("g-preco");
  if (gp) gp.textContent = "R$ " + (C.lancamento ? C.precoAvancado : C.precoAvancadoCheio);
  // personaliza pelo quiz
  const q = new URLSearchParams(location.search);
  const D = { eua: "🗽 Pra sua viagem aos Estados Unidos", europa: "🇪🇺 Pra sua viagem à Europa", paraiso: "🏝️ Pra sua viagem dos sonhos", trabalho: "💼 Pra sua viagem a trabalho" };
  if (D[q.get("destino")]) document.getElementById("selo-destino").textContent = D[q.get("destino")];

  // barra fixa no celular
  document.getElementById("barra-nome").textContent = C.nomeAvancado || "";
  document.getElementById("barra-preco").textContent = "R$ " + (C.lancamento ? C.precoAvancado : C.precoAvancadoCheio);
  const barra = document.getElementById("barra"), planos = document.getElementById("planos");
  const io = new IntersectionObserver(([e]) => barra.classList.toggle("on", !e.isIntersecting && scrollY > 500));
  io.observe(planos);
  addEventListener("scroll", () => { if (scrollY < 500) barra.classList.remove("on"); }, { passive: true });

  // painel de pendências
  if (q.has("dev") || /localhost|127\.0\.0\.1/.test(location.hostname)) {
    const lista = [...new Set(pend)];
    if (lista.length) {
      const d = document.createElement("div"); d.className = "dev";
      d.innerHTML = "<b>Pendente no config.js:</b><ul>" + lista.map(x => "<li>" + x + "</li>").join("") + "</ul>";
      document.body.appendChild(d);
    }
  }
})();
