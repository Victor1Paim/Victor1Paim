/* Barra Deck · animações com GSAP (assets/vendor/gsap-3.15.1.min.js)
 * 1. item "voa" até o carrinho  2. total do pedido conta até o valor
 * 3. abertura do topo em sequência  5. pratos do cardápio entram em cascata
 * Tudo desligado com "reduzir movimento" ou se o GSAP não carregar.
 */
(() => {
  'use strict';
  const doc = document.documentElement;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const g = window.gsap;
  const ativo = !!g && !reduce;
  const liberar = () => doc.classList.remove('gsap-pending');
  if (!ativo) { liberar(); }

  let ultimoTotal = null;
  let tweenTotal = null;

  window.BDMotion = {
    /* 2. total animado */
    total(valor, formatar) {
      const els = document.querySelectorAll('[data-cart-total]');
      const pinta = (v) => els.forEach((el) => { el.textContent = formatar(v); });
      if (!ativo || ultimoTotal === null || ultimoTotal === valor) {
        ultimoTotal = valor; pinta(valor); return;
      }
      if (tweenTotal) tweenTotal.kill();
      const obj = { v: ultimoTotal };
      ultimoTotal = valor;
      tweenTotal = g.to(obj, {
        v: valor, duration: 0.6, ease: 'power2.out',
        onUpdate: () => pinta(Math.round(obj.v)), onComplete: () => pinta(valor),
      });
    },

    /* 1. foto do prato voa até o carrinho */
    fly(id) {
      if (!ativo) return;
      const img = document.querySelector(`[data-item="${id}"] .item__ph`);
      const alvos = [document.querySelector('.cartbar:not([hidden]) .btn'), document.querySelector('.topbar__cart')];
      const alvo = alvos.find((el) => el && el.getBoundingClientRect().width > 0 && el.getBoundingClientRect().top < innerHeight);
      const pulso = () => {
        g.fromTo('[data-cart-count]', { scale: 1.7 }, { scale: 1, duration: 0.5, ease: 'back.out(3)' });
        if (alvo) g.fromTo(alvo, { scale: 1.06 }, { scale: 1, duration: 0.45, ease: 'back.out(2.5)', clearProps: 'transform' });
      };
      if (!img || !alvo) { pulso(); return; }
      const a = img.getBoundingClientRect();
      const b = alvo.getBoundingClientRect();
      const clone = img.cloneNode();
      clone.removeAttribute('loading');
      Object.assign(clone.style, {
        position: 'fixed', left: `${a.left}px`, top: `${a.top}px`, width: `${a.width}px`, height: `${a.height}px`,
        margin: 0, zIndex: 80, pointerEvents: 'none', borderRadius: '16px', objectFit: 'cover',
        boxShadow: '0 18px 30px -12px rgba(42,20,9,.55)',
      });
      document.body.appendChild(clone);
      const dx = b.left + b.width / 2 - (a.left + a.width / 2);
      const dy = b.top + b.height / 2 - (a.top + a.height / 2);
      const dur = 0.75;
      g.timeline({ onComplete: () => { clone.remove(); pulso(); } })
        .to(clone, { x: dx, duration: dur, ease: 'power1.inOut' }, 0)
        .to(clone, { y: dy, duration: dur, ease: 'back.in(1.6)' }, 0)
        .to(clone, { scale: 0.22, rotation: 12, borderRadius: '50%', duration: dur, ease: 'power2.in' }, 0)
        .to(clone, { autoAlpha: 0, duration: 0.15 }, dur - 0.12);
    },
  };

  if (!ativo) return;

  document.addEventListener('DOMContentLoaded', () => {
    /* 3. abertura do topo em sequência */
    const t = '.hero__text';
    const tl = g.timeline({ defaults: { ease: 'power3.out', duration: 0.8 } });
    tl.from(`${t} .eyebrow`, { y: 16, autoAlpha: 0 })
      .from(`${t} h1`, { y: 34, autoAlpha: 0, duration: 0.9 }, '-=0.5')
      .from(`${t} h1 em`, { y: 18, autoAlpha: 0 }, '-=0.55')
      .from(`${t} .lead`, { y: 18, autoAlpha: 0 }, '-=0.5')
      .from(`${t} .hero__cta > *`, { y: 16, autoAlpha: 0, stagger: 0.1 }, '-=0.5')
      .from(`${t} .hero__facts > div`, { y: 14, autoAlpha: 0, stagger: 0.1 }, '-=0.5')
      .from('.hero__art .arch', { y: 40, autoAlpha: 0, scale: 0.97, duration: 1.1 }, 0.15)
      .from('.hero__art .orb', { scale: 0.6, autoAlpha: 0, duration: 0.8, ease: 'back.out(1.7)' }, 0.75)
      .from('.hero__art .seal', { scale: 0.5, rotation: -40, autoAlpha: 0, duration: 0.8, ease: 'back.out(2)' }, 0.95);
    liberar();

    /* 5. pratos do cardápio em cascata */
    const listas = document.querySelectorAll('.items');
    if (!('IntersectionObserver' in window)) return;
    listas.forEach((ul) => g.set(ul.children, { autoAlpha: 0, y: 26 }));
    const io = new IntersectionObserver((ents) => ents.forEach((en) => {
      if (!en.isIntersecting) return;
      io.unobserve(en.target);
      g.to(en.target.children, { autoAlpha: 1, y: 0, duration: 0.55, ease: 'power2.out', stagger: 0.06, clearProps: 'transform,opacity,visibility' });
    }), { rootMargin: '0px 0px -6% 0px' });
    listas.forEach((ul) => io.observe(ul));
  });

  // segurança: nunca deixar o topo invisível
  setTimeout(liberar, 2500);
})();
