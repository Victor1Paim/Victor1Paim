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
    ? `<div class="de">De R$ ${C.precoAvancadoCheio}</div><div class="por"><small>R$</small> ${C.precoAvancado}</div><div class="unico">pagamento único ou <b>em até 3x no cartão</b></div><span class="promo">🔥 ${C.textoLancamento}</span>`
    : `<div class="por"><small>R$</small> ${C.precoAvancadoCheio}</div><div class="unico">pagamento único ou <b>em até 3x no cartão</b></div>`;
  if (C.aulasLiberadasEm) document.getElementById("aulas-nota").textContent = "pronúncia e fala, com exercícios · liberadas a partir de " + C.aulasLiberadasEm;

  // preço por dia nos 21 dias do guia (conta real, muda sozinha com o preço)
  const pd = document.getElementById("por-dia");
  if (pd) { const v = parseFloat(String(C.lancamento ? C.precoAvancado : C.precoAvancadoCheio).replace(",", ".")) / 21;
    pd.innerHTML = "Menos de <b>R$ " + (Math.ceil(v * 10) / 10).toFixed(2).replace(".", ",") + " por dia</b> nos 21 dias do guia, e o material é seu pra sempre."; }
  // resultado do quiz (localStorage) no topo dos planos
  try {
    const rq = JSON.parse(localStorage.getItem("eagle_quiz") || "null"), rb = document.getElementById("res-quiz");
    const TV = { frase: "NA HORA H (a frase não vem)", vergonha: "NA PRONÚNCIA (medo de errar)", decoreba: "NA DECOREBA (regra demais, frase de menos)", tempo: "NA CONSTÂNCIA (a rotina aperta)" };
    if (rq && rb && TV[rq.trava]) { rb.innerHTML = "🎯 <b>Seu resultado:</b> você trava " + TV[rq.trava] + ". O <b>" + (C.nomeAvancado || "") + "</b> foi feito pra destravar exatamente isso."; rb.hidden = false; }
  } catch (e) {}

  // comparação com o combo de lanche (R$ 40 a 50; sem citar marca: anúncio da Meta): vale com R$ 29,90 e com R$ 37
  const gp = document.getElementById("g-preco");
  if (gp) gp.textContent = "R$ " + (C.lancamento ? C.precoAvancado : C.precoAvancadoCheio);
  const vend = document.getElementById("vendedor");
  if (vend) { const d = (window.EAGLE_PRIV || {}).documento; vend.textContent = d ? "Eagle English BR · " + d : ""; if (!d) pend.push("documento (config.privado.js)"); }
  // personaliza pelo quiz
  const q = new URLSearchParams(location.search);
  // frase do topo e card em destaque conforme a resposta do quiz (?obj=)
  const OBJ = { viagem: "Pra sua próxima viagem pra fora do Brasil.", filho: "Pro seu filho aprender de verdade nas férias.",
    curso: "Pra quem já fez curso e não aprendeu.", carreira: "Pra criar base pra prova, concurso e trabalho.", vida: "Pra entender e falar no dia a dia." };
  const ob = q.get("obj"); const dt = document.getElementById("destino-txt");
  if (dt) dt.textContent = OBJ[ob] || "";
  const pc = document.getElementById("pub-" + ob); if (pc) { pc.classList.add("foco"); pc.parentNode.prepend(pc); }

  // trecho real da aula: toca só quando aparece na tela e sem "reduzir movimento"
  const vid = document.getElementById("previa");
  if (vid && !matchMedia("(prefers-reduced-motion: reduce)").matches && "IntersectionObserver" in window) {
    new IntersectionObserver(([e]) => { if (e.isIntersecting) vid.play().catch(() => {}); else vid.pause(); }, { threshold: .4 }).observe(vid);
  }

  // Pixel da Meta (preencha pixelMeta no config.js): ViewContent na página, InitiateCheckout no clique do checkout
  if (C.pixelMeta) {
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version="2.0";n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,"script","https://connect.facebook.net/en_US/fbevents.js");
    fbq("init", C.pixelMeta); fbq("track", "PageView"); fbq("track", "ViewContent");
  }
  document.querySelectorAll("[data-checkout]").forEach(a => a.addEventListener("click", () => {
    const av = a.dataset.checkout === "checkoutAvancado";
    if (window.fbq) fbq("track", "InitiateCheckout", { value: parseFloat((av ? (C.lancamento ? C.precoAvancado : C.precoAvancadoCheio) : C.precoSimples).replace(",", ".")), currency: "BRL", content_name: av ? C.nomeAvancado : C.nomeSimples });
  }));

  // barra fixa no celular
  document.getElementById("barra-nome").textContent = C.nomeAvancado || "";
  document.getElementById("barra-preco").textContent = "R$ " + (C.lancamento ? C.precoAvancado : C.precoAvancadoCheio) + " ou até 3x";
  const barra = document.getElementById("barra"), planos = document.getElementById("planos");
  // botão flutuante desde o início (quem já quer comprar vai direto); some enquanto os planos estão na tela
  new IntersectionObserver(([e]) => barra.classList.toggle("on", !e.isIntersecting), { threshold: .15 }).observe(planos);

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
