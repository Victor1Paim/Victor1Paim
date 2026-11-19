(() => {
  'use strict';

  const WHATSAPP = '5521981716022';
  // Fim do prazo: 10/12/2026 23:59:59 (horário de Brasília)
  // Ocasiões: cada uma tem data de retirada e prazo próprio de encomenda (horário de Brasília)
  const OCASIOES = [
    { id: 'natal', nome: 'Natal', dia: '24/12', semana: 'quinta', prazo: new Date('2026-12-10T23:59:59-03:00'), prazoTxt: '10/12' },
    { id: 'reveillon', nome: 'Réveillon', dia: '31/12', semana: 'quinta', prazo: new Date('2026-12-20T23:59:59-03:00'), prazoTxt: '20/12' },
  ];
  const aberta = (o) => Date.now() <= o.prazo.getTime();
  const DEADLINE = new Date(Math.max(...OCASIOES.map((o) => o.prazo.getTime())));
  const STORAGE_KEY = 'barradeck-natal-2026';

  const MENU = [
    {
      id: 'entradas', title: 'Entradas', img: 'categorias/entradas.webp', alt: 'Entradas de Natal: bolinhos de bacalhau, coxinhas, kibes e camarão empanado',
      items: [
        ['bolinho-bacalhau', 'Bolinho de bacalhau', '50 unid.', 150],
        ['empanado-camarao', 'Empanado de camarão', '50 unid.', 150],
        ['croquete-alemao', 'Croquete do Alemão', '100 unid.', 100],
        ['coxinha', 'Coxinha', '100 unid.', 100],
        ['kibe-queijo', 'Kibe com queijo', '100 unid.', 100],
      ],
    },
    {
      id: 'quiches', title: 'Quiches', note: 'Aro 24', img: 'categorias/quiches.webp', alt: 'Quiches douradas, uma fatiada',
      items: [
        ['quiche-alho-poro', 'Quiche de alho-poró', '', 130],
        ['quiche-minas-tomate', 'Quiche de queijo minas com tomate seco', '', 130],
        ['quiche-presunto', 'Quiche de queijo, presunto e orégano', '', 130],
        ['quiche-brie', 'Quiche de queijo brie com damasco', '', 180],
        ['quiche-gorgonzola', 'Quiche de gorgonzola com pera e mel', '', 180],
        ['quiche-camarao', 'Quiche de camarão', '', 200],
        ['quiche-bacalhau', 'Quiche de bacalhau', '', 200],
      ],
    },
    {
      id: 'principais', title: 'Principais', note: 'Sem acompanhamento', img: 'categorias/principais.webp', alt: 'Mesa de Natal com chester, tender, lombo e bacalhau',
      items: [
        ['lombo', 'Lombo suíno', '1 kg', 125],
        ['maminha', 'Maminha recheada', '1 kg', 150],
        ['tender', 'Tender bolinha', 'unidade', 190],
        ['escondidinho-carne-seca', 'Escondidinho de carne-seca', '', 240],
        ['escondidinho-camarao', 'Escondidinho de camarão', '', 300],
        ['bacalhau-desfiado', 'Bacalhau desfiado à portuguesa', '1,3 kg', 275],
        ['postas-bacalhau', 'Postas de bacalhau dessalgado', '1,3 kg', 300],
        ['chester', 'Chester', 'unidade', 275],
        ['pernil', 'Pernil sem osso', '3 kg', 300],
        ['arroz-polvo', 'Arroz de polvo', 'serve 3 pessoas', 280],
        ['arroz-frutos-mar', 'Arroz de frutos do mar', 'serve 3 pessoas', 320],
        ['arroz-camarao', 'Arroz de camarão', 'serve 3 pessoas', 280],
      ],
    },
    {
      id: 'acompanhamentos', title: 'Acompanhamentos', img: 'categorias/acompanhamentos.webp', alt: 'Arroz natalino, farofa, cuscuz e salpicão',
      items: [
        ['arroz-branco', 'Arroz branco', '1 kg', 50],
        ['arroz-natalino', 'Arroz natalino', '1,3 kg · passas, lascas de castanha, nozes, milho, bacon, azeitonas, ovos e presunto', 150],
        ['arroz-bacalhau', 'Arroz de bacalhau', '1,3 kg', 180],
        ['farofa-tradicional', 'Farofa tradicional', '1 kg', 50],
        ['farofa-ameixa', 'Farofa de ameixa', '1 kg', 75],
        ['farofa-ovos', 'Farofa de ovos', '1 kg', 75],
        ['cuscuz', 'Cuscuz marroquino', '1 kg', 100],
        ['salada-aipo', 'Salada de aipo', '1 kg', 100],
        ['salpicao', 'Salpicão de frango', '1 kg', 120],
        ['empadao-frango', 'Empadão de frango', '', 180],
        ['empadao-camarao', 'Empadão de camarão', '', 280],
      ],
    },
    {
      id: 'sobremesas-menu', title: 'Sobremesas', img: 'categorias/sobremesas.webp', alt: 'Sobremesas de Natal: rabanadas, torta de limão, pavê e cheesecake',
      items: [
        ['rabanada', 'Rabanada tradicional', 'unidade', 8],
        ['rabanada-panetone', 'Rabanada de panetone', 'unidade', 8],
        ['pudim-medio', 'Pudim médio', 'unidade', 130, 'pudim'],
        ['pudim-grande', 'Pudim grande', 'unidade', 150, 'pudim'],
        ['torta-limao', 'Torta de limão', '', 150],
        ['cheesecake-damasco', 'Cheesecake de damasco', 'unidade', 175],
        ['cheesecake-frutas', 'Cheesecake de frutas vermelhas', 'unidade', 175, 'cheesecake'],
        ['pave-chocolate', 'Pavê de chocolate', 'unidade', 175],
        ['pave-pacoca', 'Pavê de paçoca', 'unidade', 175],
        ['pave-oreo', 'Pavê de Oreo', 'unidade', 175, 'pave-oreo'],
      ],
    },
  ];

  const ITEMS = new Map();
  MENU.forEach((cat) => cat.items.forEach(([id, name, detail, price, photo]) => {
    ITEMS.set(id, { id, name, detail, price, photo, cat: cat.title });
  }));

  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const brl = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });
  const money = (v) => brl.format(v).replace(/ /g, ' ');
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  const isClosed = () => Date.now() > DEADLINE.getTime();

  /* ---------- estado ---------- */
  let cart = {};
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
    for (const [id, q] of Object.entries(saved)) if (ITEMS.has(id) && q > 0) cart[id] = Math.min(99, q | 0);
  } catch (_) { /* sem storage: segue com pedido vazio */ }

  const save = () => { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(cart)); } catch (_) {} };
  const count = () => Object.values(cart).reduce((a, b) => a + b, 0);
  const total = () => Object.entries(cart).reduce((a, [id, q]) => a + ITEMS.get(id).price * q, 0);

  function setQty(id, q) {
    q = Math.max(0, Math.min(99, q));
    if (q === 0) delete cart[id]; else cart[id] = q;
    save();
    render();
  }

  /* ---------- cardápio ---------- */
  function buildMenu() {
    $('[data-cats]').innerHTML = MENU.map((c) => `<a href="#${c.id}" data-cat-link="${c.id}">${c.title}</a>`).join('');
    $('[data-menu]').innerHTML = MENU.map((c) => `
      <section class="cat" id="${c.id}" aria-labelledby="${c.id}-t">
        <div class="cat__head reveal">
          <div class="cat__title">
            <h3 id="${c.id}-t">${c.title}</h3>
            ${c.note ? `<p class="cat__note">${c.note}</p>` : ''}
          </div>
          <figure class="cat__img"><img src="/assets/img/${c.img}" alt="${esc(c.alt)}" loading="lazy" decoding="async"></figure>
        </div>
        <ul class="items">
          ${c.items.map(([id, name, detail, price, photo]) => `
            <li class="item" data-item="${id}">
              <img class="item__ph" src="/assets/img/${photo ? `${photo}-240` : `pratos/mini/${id}`}.webp" alt="" width="640" height="640" loading="lazy" decoding="async">
              <div class="item__txt">
                <p class="item__name">${esc(name)}</p>
                ${detail ? `<p class="item__detail">${esc(detail)}</p>` : ''}
              </div>
              <p class="item__price">${money(price)}</p>
              <div class="item__ctl" data-ctl="${id}"></div>
            </li>`).join('')}
        </ul>
      </section>`).join('');
  }

  function ctlHTML(id, name) {
    const q = cart[id] || 0;
    if (isClosed()) return '';
    if (!q) return `<button class="add" type="button" data-add="${id}" aria-label="Adicionar ${esc(name)}">Adicionar</button>`;
    return `<div class="stepper" role="group" aria-label="Quantidade de ${esc(name)}">
      <button type="button" data-dec="${id}" aria-label="Diminuir">−</button>
      <output aria-live="polite">${q}</output>
      <button type="button" data-inc="${id}" aria-label="Aumentar">+</button>
    </div>`;
  }

  /* ---------- render ---------- */
  function render() {
    const n = count(), t = total();
    $$('[data-ctl]').forEach((el) => {
      const id = el.dataset.ctl;
      const html = ctlHTML(id, ITEMS.get(id).name);
      if (el.innerHTML !== html) el.innerHTML = html;
      el.closest('.item').classList.toggle('is-in', !!cart[id]);
    });

    $$('[data-cart-count]').forEach((el) => { el.textContent = n; el.hidden = !n; });
    if (window.BDMotion) window.BDMotion.total(t, money); else $$('[data-cart-total]').forEach((el) => { el.textContent = money(t); });
    $$('[data-cart-items]').forEach((el) => { el.textContent = `${n} ${n === 1 ? 'item' : 'itens'}`; });
    $('[data-cartbar]').hidden = !n;
    document.body.classList.toggle('has-cart', !!n);

    const ids = Object.keys(cart);
    $('[data-empty]').hidden = !!ids.length;
    $('[data-total-box]').hidden = !ids.length;
    $('[data-form]').hidden = !ids.length || isClosed();
    $('[data-closed]').hidden = !isClosed();
    $('[data-lines]').innerHTML = ids.map((id) => {
      const it = ITEMS.get(id), q = cart[id];
      return `<li class="line">
        <div><p class="line__name">${esc(it.name)}</p><p class="line__meta">${it.detail ? esc(it.detail.split(' · ')[0]) + ' · ' : ''}${money(it.price)}</p></div>
        <div class="line__end">
          ${ctlHTML(id, it.name)}
          <p class="line__sum">${money(it.price * q)}</p>
        </div>
      </li>`;
    }).join('');
  }

  /* ---------- prazo ---------- */
  function renderDeadline() {
    const el = $('[data-deadline]');
    if (isClosed()) { el.textContent = 'Encomendas encerradas'; document.body.classList.add('is-closed'); return; }
    const prox = OCASIOES.find(aberta);
    const days = Math.ceil((prox.prazo - Date.now()) / 86400000);
    el.innerHTML = `<span class="fl">${days <= 1 ? 'Último dia' : `Faltam ${days} dias`}</span><span class="fl fl--sub">para o ${prox.nome}</span>`;
    // ocasião com prazo vencido fica indisponível no pedido
    OCASIOES.forEach((o) => {
      const inp = $(`input[name="ocasiao"][value="${o.id}"]`);
      if (inp && !aberta(o)) { inp.disabled = true; inp.closest('label').classList.add('is-off'); inp.closest('label').title = 'Encomendas encerradas'; }
    });
  }

  /* ---------- gaveta ---------- */
  const drawer = $('[data-drawer]');
  function openCart() {
    if (typeof drawer.showModal === 'function') drawer.showModal(); else drawer.setAttribute('open', '');
    document.body.classList.add('lock');
  }
  function closeCart() {
    if (drawer.open && typeof drawer.close === 'function') drawer.close(); else drawer.removeAttribute('open');
  }
  drawer.addEventListener('close', () => document.body.classList.remove('lock'));
  drawer.addEventListener('click', (e) => { if (e.target === drawer) closeCart(); });

  /* ---------- pop-up do cardápio em PDF ---------- */
  function promo() {
    const dlg = $('[data-promo]');
    const KEY = 'barradeck-promo-pdf';
    if (!dlg || typeof dlg.showModal !== 'function') return;
    try { if (localStorage.getItem(KEY)) return; } catch (_) { /* sem storage: mostra mesmo assim */ }
    const fechar = () => {
      try { localStorage.setItem(KEY, '1'); } catch (_) {}
      if (dlg.open) dlg.close();
    };
    dlg.addEventListener('click', (e) => {
      if (e.target === dlg || e.target.closest('[data-promo-close]')) fechar();
      if (e.target.closest('[data-promo-dl]')) setTimeout(fechar, 300);
    });
    dlg.addEventListener('cancel', () => { try { localStorage.setItem(KEY, '1'); } catch (_) {} });
    setTimeout(() => {
      if (!$('[data-drawer]').open) dlg.showModal();
    }, 1500);
  }

  /* ---------- toast ---------- */
  let toastT;
  function toast(msg) {
    const t = $('[data-toast]');
    t.textContent = msg;
    t.classList.add('show');
    clearTimeout(toastT);
    toastT = setTimeout(() => t.classList.remove('show'), 2200);
  }

  /* ---------- eventos ---------- */
  document.addEventListener('click', (e) => {
    const b = e.target.closest('button, a');
    if (!b) return;
    if (b.matches('[data-open-cart]')) return openCart();
    if (b.matches('[data-close-cart]')) return closeCart();
    const { add, inc, dec } = b.dataset;
    if (add) { setQty(add, 1); if (window.BDMotion) window.BDMotion.fly(add); toast(`${ITEMS.get(add).name} adicionado`); focusCtl(add, '[data-inc]'); }
    if (inc) setQty(inc, (cart[inc] || 0) + 1);
    if (dec) { setQty(dec, (cart[dec] || 0) - 1); if (!cart[dec]) focusCtl(dec, '[data-add]'); }
  });
  function focusCtl(id, sel) {
    const inMenu = document.activeElement && document.activeElement.closest('[data-menu]');
    if (inMenu) { const el = $(`[data-ctl="${id}"] ${sel}`); if (el) el.focus(); }
  }

  /* ---------- formulário ---------- */
  const form = $('[data-form]');
  const endereco = $('[data-endereco]');
  const ocasiaoSel = () => OCASIOES.find((o) => o.id === (form.elements.ocasiao && form.elements.ocasiao.value));
  function renderOcasiao() {
    const o = ocasiaoSel();
    const conf = $('[data-ocasiao-ok]');
    if (!o) { conf.hidden = true; return; }
    conf.hidden = false;
    conf.innerHTML = `<strong>Pedido para o ${o.nome}</strong> · retirada ou entrega em ${o.dia} (${o.semana}-feira).`;
    form.elements.data.value = `${o.dia} (${o.semana}) – ${o.nome}`;
  }
  form.addEventListener('change', (e) => {
    if (e.target.name === 'ocasiao') { renderOcasiao(); $('[data-err="ocasiao"]').classList.remove('on'); }
    if (e.target.name === 'recebimento') {
      const ent = e.target.value === 'Entrega';
      endereco.hidden = !ent;
      $('[data-horario]').hidden = ent;
      $('[data-entrega-aviso]').hidden = !ent;
    }
  });
  const tel = form.elements.telefone;
  tel.addEventListener('input', () => {
    const d = tel.value.replace(/\D/g, '').slice(0, 11);
    let v = d;
    if (d.length > 2) v = `(${d.slice(0, 2)}) ${d.slice(2)}`;
    if (d.length > 7) v = `(${d.slice(0, 2)}) ${d.slice(2, d.length - 4)}-${d.slice(-4)}`;
    tel.value = v;
  });

  function validate() {
    const f = form.elements;
    const errs = {
      nome: f.nome.value.trim().length < 3,
      telefone: f.telefone.value.replace(/\D/g, '').length < 10,
      ocasiao: !f.ocasiao.value,
    };
    let first = null;
    for (const [k, bad] of Object.entries(errs)) {
      const field = f[k];
      const el = field instanceof RadioNodeList ? field[0] : field;
      if (!(field instanceof RadioNodeList)) field.setAttribute('aria-invalid', bad);
      $(`[data-err="${k}"]`).classList.toggle('on', bad);
      if (bad && !first) first = el;
    }
    if (first) first.focus();
    return !first;
  }

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (isClosed() || !count() || !validate()) return;
    const f = form.elements;
    const lines = [];
    MENU.forEach((cat) => {
      const its = cat.items.filter(([id]) => cart[id]);
      if (!its.length) return;
      lines.push(`_${cat.title}_`);
      its.forEach(([id]) => {
        const it = ITEMS.get(id), q = cart[id];
        const det = it.detail ? ` (${it.detail.split(' · ')[0]})` : '';
        lines.push(`• ${q}x ${it.name}${det} — ${money(it.price * q)}`);
      });
      lines.push('');
    });
    const oc = ocasiaoSel();
    const d = new Date();
    // BD-DDMM-HHMM-XX: dia/mês e hora do envio + 2 dígitos aleatórios
    const p2 = (n) => String(n).padStart(2, '0');
    const code = `BD-${p2(d.getDate())}${p2(d.getMonth() + 1)}-${p2(d.getHours())}${p2(d.getMinutes())}-${p2(Math.floor(Math.random() * 100))} – ${oc.nome}`;
    const entrega = f.recebimento.value === 'Entrega';
    const v = (n) => (f[n] && f[n].value ? f[n].value.trim() : '');
    // mesma ordem da comanda de papel: cliente, telefone, recebimento, data, horário, endereço, pedido
    const cliente = [
      `*Cliente:* ${v('nome')}`,
      `*Telefone:* ${v('telefone')}`,
      `*Recebimento:* ${entrega ? 'Entrega' : 'Retirada'}`,
      `*Ocasião:* ${oc.nome}`,
      `*Data:* ${oc.dia} (${oc.semana})`,
    ];
    if (!entrega) {
      cliente.push(`*Horário:* ${v('horario') || 'a combinar (entre 10h e 15h)'}`);
      cliente.push('*Local:* Clube da Aeronáutica da Barra da Tijuca – Av. Rachel de Queiroz, s/n');
    } else {
      const rua = v('rua'), num = v('numero');
      const linhaRua = [rua, num && `nº ${num}`].filter(Boolean).join(', ');
      cliente.push(`*Endereço:* ${linhaRua || 'a informar'}`);
      if (v('complemento')) cliente.push(`*Complemento:* ${v('complemento')}`);
      if (v('bairro')) cliente.push(`*Bairro:* ${v('bairro')}`);
      if (v('referencia')) cliente.push(`*Ponto de referência:* ${v('referencia')}`);
      cliente.push('_Por favor, confirmem se entregam neste endereço e o valor da taxa._');
    }
    const msg = [
      `Olá, Barra Deck! Segue meu *pré-pedido de ${oc.nome} 2026* (nº ${code}).`,
      '',
      ...cliente,
      '',
      '*Descrição do pedido*',
      ...lines,
      `*Total estimado:* ${money(total())}${entrega ? ' + taxa de entrega' : ''}`,
      ...(v('obs') ? ['', `*Observações:* ${v('obs')}`] : []),
      '',
      'Aguardo a confirmação da disponibilidade, do valor final e da forma de pagamento. Obrigado!',
    ].join('\n');
    window.open(`https://wa.me/${WHATSAPP}?text=${encodeURIComponent(msg)}`, '_blank', 'noopener');
  });

  /* ---------- categoria ativa + revelar ---------- */
  function observe() {
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if ('IntersectionObserver' in window && !reduce) {
      const io = new IntersectionObserver((ents) => ents.forEach((en) => {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      }), { rootMargin: '0px 0px -8% 0px' });
      $$('.reveal').forEach((el) => io.observe(el));
    } else {
      $$('.reveal').forEach((el) => el.classList.add('in'));
    }

  }

  /* categoria ativa conforme a rolagem */
  let current = null;
  function spy() {
    const line = window.innerHeight * 0.4;
    let id = null;
    $$('.cat').forEach((sec) => { if (sec.getBoundingClientRect().top <= line) id = sec.id; });
    if (id === current) return;
    current = id;
    $$('[data-cat-link]').forEach((a) => {
      if (a.dataset.catLink === id) {
        a.setAttribute('aria-current', 'true');
        const bar = a.parentElement;
        bar.scrollTo({ left: a.offsetLeft - (bar.clientWidth - a.offsetWidth) / 2 });
      } else a.removeAttribute('aria-current');
    });
  }

  // cabeçalho com sombra ao rolar
  const top = $('.topbar');
  let ticking = false;
  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(() => { top.classList.toggle('scrolled', window.scrollY > 8); spy(); ticking = false; });
  };
  window.addEventListener('scroll', onScroll, { passive: true });

  document.documentElement.classList.add('js');
  buildMenu();
  renderDeadline();
  promo();
  render();
  observe();
  onScroll();
})();
