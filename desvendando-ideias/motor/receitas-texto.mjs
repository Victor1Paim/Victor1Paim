// Receitas de texto em movimento (dicionário de movimento, seção 4): text swap (MITO → VERDADE) e typewriter.
export default function receitasTexto({ COL, r3, fit }) {
  return {
    // Uma palavra troca por outra: o.from (riscada, sobe e some) → o.to (entra por baixo). o.at: segundos até a troca.
    textSwap(P, T0, D, o) {
      const at = r3(T0 + (o.at ?? Math.min(1.0, D * 0.4))), sz = Math.min(fit(o.from, o.size || 230), fit(o.to, o.size || 230));
      const lab = (txt, top, color) => txt ? `<div class="t ts" style="top:${top}px;font-size:56px;color:${color}">${txt}</div>` : '';
      const html = `<div id="${P}-a" class="t" style="top:560px;font-size:${sz}px;color:${COL[o.fromColor] || COL.coral}">${o.from}<div id="${P}-x" class="abs" style="left:${540 - (String(o.from).length * sz * 0.44)}px;top:${sz * 0.5}px;width:${String(o.from).length * sz * 0.88}px;height:${Math.max(14, sz * 0.09)}px;background:${COL.ink};transform-origin:0 50%"></div></div>
<div id="${P}-b" class="t" style="top:560px;font-size:${sz}px;color:${COL[o.toColor] || COL.mint}">${o.to}</div>${lab(o.fromLabel, 480, COL.soft).replace('class="t ts"', `id="${P}-la" class="t ts"`)}${lab(o.toLabel, 480, COL.soft).replace('class="t ts"', `id="${P}-lb" class="t ts"`)}`;
      const js = `tl.fromTo('#${P}-a',{opacity:0,scale:0.7},{opacity:1,scale:1,duration:0.25,ease:'back.out(1.8)'},${r3(T0)});tl.fromTo('#${P}-x',{scaleX:0},{scaleX:1,duration:0.25,ease:'power2.out'},${r3(at - 0.3)});`
        + `tl.to('#${P}-a',{y:-160,opacity:0,duration:0.3,ease:'power3.in'},${at});tl.fromTo('#${P}-b',{y:160,opacity:0},{y:0,opacity:1,duration:0.35,ease:'back.out(1.6)'},${r3(at + 0.12)});`
        + (o.fromLabel ? `tl.fromTo('#${P}-la',{opacity:0},{opacity:1,duration:0.2},${r3(T0 + 0.1)});tl.to('#${P}-la',{opacity:0,duration:0.2},${at});` : '')
        + (o.toLabel ? `tl.fromTo('#${P}-lb',{opacity:0},{opacity:1,duration:0.2},${r3(at + 0.2)});` : '');
      return { html, js };
    },
    // Letras aparecem uma a uma, com cursor. o.text, o.y, o.size, o.cps (letras por segundo).
    typewriter(P, T0, D, o) {
      const txt = String(o.text), n = txt.length, dur = r3(Math.min(D * 0.75, n / (o.cps || 14))), sz = fit(txt, o.size || 120);
      const html = `<div class="t" style="top:${o.y || 640}px;font-size:${sz}px;color:${COL[o.color] || COL.ink}"><span id="${P}-tx"></span><span id="${P}-cur" style="display:inline-block;width:${Math.round(sz * 0.08)}px;height:${sz}px;margin-left:${Math.round(sz * 0.06)}px;background:${COL.amber};vertical-align:-0.12em"></span></div>`;
      const js = `{const E=document.getElementById('${P}-tx');const T=${JSON.stringify(txt)};const S={v:0};tl.fromTo(S,{v:0},{v:${n},duration:${dur},ease:'none',onUpdate:()=>{E.textContent=T.slice(0,Math.round(S.v))}},${r3(T0 + 0.1)});}`
        + Array.from({ length: Math.max(1, Math.floor(D / 0.5)) }, (_, k) => `tl.set('#${P}-cur',{opacity:${k % 2 ? 1 : 0}},${r3(T0 + 0.25 + k * 0.5)});`).join('');
      return { html, js };
    },
  };
}
