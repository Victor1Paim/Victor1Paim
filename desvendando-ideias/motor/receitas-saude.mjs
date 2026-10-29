// Receitas de plano para vídeos de saúde (003 · lagarto e Ozempic em diante): lagarto, intestino com GLP-1, efeito
// (açúcar/saciedade), cronômetro, enzima cortando ou batendo na molécula, barras minutos × horas, caneta e calendário.
// Objetos ficam sobre um ladrilho isométrico (isoTile), o que dá o ar 2,5D da pele Isométrico em qualquer pele.
export default function receitasSaude({ COL, r3, px }) {
  const ink = COL.ink, dark = '#1B1B1B';
  const S = (n, c = dark) => `stroke="${c}" stroke-width="${n}" stroke-linejoin="round" stroke-linecap="round"`;
  const lbl = (id, text, x, y, w, size, color = ink) => `<div id="${id}" class="abs" style="left:${x}px;top:${y}px;width:${w}px;text-align:center;font-family:'Archivo Black',sans-serif;font-size:${size}px;line-height:1.05;color:${color};white-space:nowrap">${text}</div>`;
  const pop = (sel, t) => `tl.fromTo('${sel}',{opacity:0,scale:0.4},{opacity:1,scale:1,duration:0.3,ease:'back.out(1.8)'},${r3(t)});`;
  // ladrilho isométrico: losango de largura w com espessura d, centro do topo em (cx, cy)
  const isoTile = (id, cx, cy, w, d = 34) => {
    const h = w / 2, x0 = cx - w / 2;
    return `<svg id="${id}" class="abs" style="left:${px(x0)}px;top:${px(cy - h / 2)}px" width="${w}" height="${h + d + 4}" viewBox="0 0 ${w} ${h + d + 4}">
<path d="M0 ${h / 2} L${w / 2} ${h} V${h + d} L0 ${h / 2 + d} Z" fill="rgba(0,0,0,.38)"/><path d="M${w} ${h / 2} L${w / 2} ${h} V${h + d} L${w} ${h / 2 + d} Z" fill="rgba(0,0,0,.22)"/>
<path d="M${w / 2} 0 L${w} ${h / 2} L${w / 2} ${h} L0 ${h / 2} Z" fill="rgba(255,255,255,.14)" stroke="rgba(255,255,255,.45)" stroke-width="3"/></svg>`;
  };
  const tileJS = (id, t) => `tl.fromTo('#${id}',{opacity:0,y:40},{opacity:1,y:0,duration:0.3,ease:'power3.out'},${r3(t)});`;

  const lizardSVG = (id) => `<svg id="${id}" class="abs obj" style="left:120px;top:500px" width="840" height="360" viewBox="0 0 840 360">
<path d="M20 230 C120 250 200 215 270 200 L300 250 C220 265 120 268 20 230 Z" fill="${dark}" ${S(5)}/>
<path d="M250 190 C330 120 520 110 640 150 C700 165 760 170 812 190 C790 222 730 236 660 232 C560 262 360 268 260 240 Z" fill="#2A2A2A" ${S(6)}/>
${[[330, 175, 34, 18], [410, 160, 30, 16], [480, 170, 36, 18], [560, 165, 30, 16], [390, 215, 34, 16], [470, 220, 30, 15], [550, 215, 32, 16], [620, 200, 26, 13], [300, 225, 22, 12]].map(([x, y, rx, ry], i) => `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="${i % 2 ? '#F4A7B9' : '#F28C28'}"/>`).join('')}
<path d="M330 245 L300 300 H340 M450 255 L440 312 H482 M560 250 L585 305 H625 M650 228 L690 280 H730" fill="none" ${S(14, '#2A2A2A')}/>
<circle cx="745" cy="178" r="9" fill="#fff"/><circle cx="747" cy="179" r="4" fill="${dark}"/><path d="M790 200 L812 196" ${S(4, '#F4A7B9')}/></svg>`;

  return {
    // Lagarto (monstro-de-gila) num ladrilho; o.venom: gota caindo da boca; o.cross: ✕ vermelho sobre a gota; o.badge: selo embaixo
    lizard(P, T0, D, o) {
      const drop = `<svg id="${P}-drop" class="abs obj" style="left:875px;top:690px" width="70" height="100" viewBox="0 0 70 100"><path d="M35 4 C55 40 66 58 66 70 A31 31 0 0 1 4 70 C4 58 15 40 35 4 Z" fill="${COL.mint}" ${S(5)}/></svg>`;
      const cross = o.cross ? `<svg id="${P}-x" class="abs" style="left:800px;top:640px" width="220" height="220" viewBox="0 0 220 220"><path d="M30 30 L190 190 M190 30 L30 190" ${S(30, COL.coral)}/></svg>` : '';
      const html = isoTile(`${P}-tile`, 540, 860, 860) + lizardSVG(`${P}-lz`) + (o.venom || o.cross ? drop : '') + cross + (o.badge ? lbl(`${P}-bd`, o.badge, 90, 1010, 900, 56, COL.amber) : '');
      let js = tileJS(`${P}-tile`, T0) + `tl.fromTo('#${P}-lz',{opacity:0,x:-140},{opacity:1,x:0,duration:0.45,ease:'power3.out'},${r3(T0 + 0.05)});`;
      if (o.venom || o.cross) js += `tl.fromTo('#${P}-drop',{opacity:0,y:-60,scale:0.4},{opacity:1,y:0,scale:1,duration:0.4,ease:'bounce.out'},${r3(T0 + 0.5)});`;
      if (o.cross) js += `tl.fromTo('#${P}-x',{opacity:0,scale:1.8},{opacity:1,scale:1,duration:0.25,ease:'power4.out'},${r3(T0 + 0.9)});`;
      if (o.badge) js += `tl.fromTo('#${P}-bd',{opacity:0,y:30},{opacity:1,y:0,duration:0.3},${r3(T0 + 0.6)});`;
      return { html, js };
    },
    // Prato e intestino; o.glp: partículas "GLP-1" saindo do intestino
    gut(P, T0, D, o) {
      const plate = `<svg id="${P}-pl" class="abs obj" style="left:120px;top:330px" width="300" height="190" viewBox="0 0 300 190"><ellipse cx="150" cy="110" rx="140" ry="70" fill="#F2F2F2" ${S(6)}/><ellipse cx="150" cy="104" rx="96" ry="44" fill="none" stroke="#C9C9C9" stroke-width="4"/><circle cx="118" cy="96" r="26" fill="#E9A23B" ${S(4)}/><circle cx="170" cy="92" r="20" fill="#2BB673" ${S(4)}/><circle cx="188" cy="118" r="16" fill="#E63946" ${S(4)}/></svg>`;
      const gutSVG = `<svg id="${P}-gt" class="abs obj" style="left:330px;top:500px" width="560" height="460" viewBox="0 0 560 460"><path d="M80 80 H470 C520 80 520 160 470 160 H100 C50 160 50 240 100 240 H460 C510 240 510 320 460 320 H110 C60 320 60 400 110 400 H480" fill="none" ${S(66)}/><path d="M80 80 H470 C520 80 520 160 470 160 H100 C50 160 50 240 100 240 H460 C510 240 510 320 460 320 H110 C60 320 60 400 110 400 H480" fill="none" stroke="#F4A7B9" stroke-width="54" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
      const parts = o.glp ? [[420, 640], [560, 600], [700, 660], [480, 760], [640, 780]].map(([x, y], i) => `<svg id="${P}-p${i}" class="abs obj ${P}-pp" style="left:${x}px;top:${y}px" width="120" height="104" viewBox="0 0 120 104"><path d="M30 4 H90 L116 52 L90 100 H30 L4 52 Z" fill="${COL.blue}" ${S(5)}/><text x="60" y="64" text-anchor="middle" font-family="Archivo Black" font-size="30" fill="#fff">GLP-1</text></svg>`).join('') : '';
      const html = isoTile(`${P}-tile`, 610, 900, 700) + plate + gutSVG + parts;
      let js = tileJS(`${P}-tile`, T0) + pop(`#${P}-pl`, T0) + `tl.fromTo('#${P}-gt',{opacity:0,y:60},{opacity:1,y:0,duration:0.4,ease:'power3.out'},${r3(T0 + 0.15)});`;
      if (o.glp) js += `tl.fromTo('.${P}-pp',{opacity:0,scale:0.3,y:60},{opacity:1,scale:1,y:-210,duration:0.9,ease:'power2.out',stagger:0.12},${r3(T0 + 0.35)});`;
      return { html, js };
    },
    // Um efeito do hormônio: o.kind 'acucar' (gota de sangue com seta para baixo) ou 'saciedade' (estômago cheio com ✓)
    effect(P, T0, D, o) {
      const sugar = o.kind === 'acucar';
      const icon = sugar
        ? `<path d="M150 20 C210 110 240 160 240 200 A90 90 0 0 1 60 200 C60 160 90 110 150 20 Z" fill="#E63946" ${S(8)}/><path d="M150 150 V240 M115 205 L150 240 L185 205" fill="none" ${S(12, '#fff')}/>`
        : `<path d="M90 60 C40 70 30 150 70 200 C110 250 200 260 240 210 C270 170 250 120 210 120 C180 120 170 90 160 60 C150 30 120 50 90 60 Z" fill="#F4A7B9" ${S(8)}/><path d="M105 170 L140 205 L210 130" fill="none" ${S(16, COL.mint)}/>`;
      const html = isoTile(`${P}-tile`, 540, 880, 640) + `<svg id="${P}-ic" class="abs obj" style="left:390px;top:470px" width="300" height="300" viewBox="0 0 300 300">${icon}</svg>` + lbl(`${P}-l`, o.label || (sugar ? 'AÇÚCAR NO SANGUE' : 'SACIEDADE'), 90, 330, 900, 72);
      const js = tileJS(`${P}-tile`, T0) + pop(`#${P}-ic`, T0 + 0.05) + `tl.fromTo('#${P}-l',{opacity:0,y:-30},{opacity:1,y:0,duration:0.3},${r3(T0 + 0.15)});`;
      return { html, js };
    },
    // Cronômetro contando de o.secs até 0 (anel esvaziando); o.label embaixo
    stopwatch(P, T0, D, o) {
      const secs = o.secs || 120, d = r3(Math.min(3.0, D * 0.7)), C = 2 * Math.PI * 200;
      const html = `<svg id="${P}-sw" class="abs obj" style="left:290px;top:380px" width="500" height="560" viewBox="0 0 500 560"><rect x="210" y="10" width="80" height="50" rx="10" fill="${COL.soft}" ${S(6)}/><circle cx="250" cy="310" r="230" fill="#F2FBFF" ${S(10)}/>
<circle id="${P}-ring" cx="250" cy="310" r="200" fill="none" stroke="${COL.coral}" stroke-width="34" stroke-dasharray="${r3(C)}" stroke-dashoffset="0" transform="rotate(-90 250 310)"/></svg>
<div id="${P}-tm" class="abs" style="left:290px;top:610px;width:500px;text-align:center;font-family:'Archivo Black',sans-serif;font-size:120px;line-height:1;color:${dark}">${Math.floor(secs / 60)}:${String(secs % 60).padStart(2, '0')}</div>${lbl(`${P}-l`, o.label || 'NO SANGUE', 90, 1000, 900, 60)}`;
      const js = pop(`#${P}-sw`, T0) + `tl.fromTo('#${P}-ring',{strokeDashoffset:0},{strokeDashoffset:${r3(C)},duration:${d},ease:'none'},${r3(T0 + 0.3)});`
        + `{const E=document.getElementById('${P}-tm');const S={v:${secs}};tl.fromTo(S,{v:${secs}},{v:0,duration:${d},ease:'none',onUpdate:()=>{const v=Math.ceil(S.v);E.textContent=Math.floor(v/60)+':'+String(v%60).padStart(2,'0')}},${r3(T0 + 0.3)});}`
        + `tl.fromTo('#${P}-l',{opacity:0},{opacity:1,duration:0.2},${r3(T0 + 0.2)});`;
      return { html, js };
    },
    // Molécula (corrente de contas) e a enzima-tesoura: o.mode 'cut' (corta e as contas se espalham) ou 'resist' (bate e volta)
    enzyme(P, T0, D, o) {
      const resist = o.mode === 'resist', at = o.at ?? 0.4, n = 8, beadC = o.beadColor || (resist ? '#F28C28' : COL.blue);
      const beads = Array.from({ length: n }, (_, i) => `<circle class="${P}-${i < n / 2 ? 'a' : 'b'}" cx="${190 + i * 100}" cy="680" r="40" fill="${beadC}" ${S(6)}/>`).join('');
      const link = `<path id="${P}-lk" d="M190 680 H${190 + (n - 1) * 100}" ${S(14)}/>`;
      const shield = resist ? ` <rect id="${P}-sh" x="130" y="610" width="${(n - 1) * 100 + 120}" height="140" rx="70" fill="none" stroke="${COL.mint}" stroke-width="10" stroke-dasharray="24 16"/>` : '';
      const html = `<svg class="abs" style="left:0;top:0" width="1080" height="1100" viewBox="0 0 1080 1100">${shield}${link}${beads}</svg>
<svg id="${P}-sc" class="abs obj" style="left:700px;top:300px" width="300" height="260" viewBox="0 0 300 260"><circle cx="70" cy="70" r="46" fill="none" ${S(16, COL.coral)}/><circle cx="70" cy="190" r="46" fill="none" ${S(16, COL.coral)}/><path d="M105 95 L290 160 M105 165 L290 100" ${S(18, COL.coral)}/></svg>
${lbl(`${P}-sl`, o.enzymeLabel || 'ENZIMA', 90, 330, 900, 64, COL.coral)}${lbl(`${P}-ml`, o.label || (resist ? 'MOLÉCULA DO LAGARTO' : 'GLP-1'), 90, 800, 900, 60, beadC)}`;
      let js = `tl.fromTo('.${P}-a,.${P}-b,#${P}-lk',{opacity:0,scale:0.4},{opacity:1,scale:1,duration:0.3,ease:'back.out(1.8)',stagger:0.03,transformOrigin:'50% 50%'},${r3(T0)});tl.fromTo('#${P}-ml',{opacity:0},{opacity:1,duration:0.2},${r3(T0 + 0.2)});`
        + `tl.fromTo('#${P}-sl',{opacity:0},{opacity:1,duration:0.2},${r3(T0 + at)});tl.fromTo('#${P}-sc',{x:300,y:-60,opacity:0},{x:-230,y:170,opacity:1,duration:0.5,ease:'power2.in'},${r3(T0 + at)});`;
      if (resist) js += `tl.fromTo('#${P}-sh',{opacity:0},{opacity:1,duration:0.15},${r3(T0 + at + 0.45)});tl.to('#${P}-sc',{x:150,y:-40,rotation:30,duration:0.5,ease:'back.out(2)'},${r3(T0 + at + 0.5)});`;
      else js += `tl.to('#${P}-lk',{opacity:0,duration:0.1},${r3(T0 + at + 0.5)});tl.to('.${P}-a',{x:-160,y:120,opacity:0.25,duration:0.6,ease:'power2.out',stagger:0.04},${r3(T0 + at + 0.5)});tl.to('.${P}-b',{x:160,y:150,opacity:0.25,duration:0.6,ease:'power2.out',stagger:0.04},${r3(T0 + at + 0.5)});`;
      return { html, js };
    },
    // Duas barras: curta (o.a) e longa (o.b), crescendo uma depois da outra
    vsBars(P, T0, D, o) {
      const a = o.a || ['GLP-1 HUMANO', '~2 MIN', 0.1], b = o.b || ['MOLÉCULA DO LAGARTO', 'HORAS', 1];
      const bar = (id, y, [name, val, f], color) => `${lbl(`${id}-n`, name, 90, y, 900, 50)}<div class="abs" style="left:120px;top:${y + 70}px;width:840px;height:110px;border-radius:24px;background:rgba(255,255,255,.12);border:5px solid ${ink};box-sizing:border-box"></div><div id="${id}-f" class="abs" style="left:126px;top:${y + 76}px;width:${828 * f}px;height:98px;border-radius:20px;background:${color};transform-origin:0 50%"></div>${lbl(`${id}-v`, val, 90, y + 200, 900, 64, color)}`;
      const html = bar(`${P}-a`, 360, a, COL.blue) + bar(`${P}-b`, 700, b, '#F28C28');
      const js = `tl.fromTo('#${P}-a-f',{scaleX:0},{scaleX:1,duration:0.35,ease:'power3.out'},${r3(T0 + 0.1)});tl.fromTo('#${P}-a-v',{opacity:0},{opacity:1,duration:0.2},${r3(T0 + 0.4)});`
        + `tl.fromTo('#${P}-b-f',{scaleX:0},{scaleX:1,duration:0.9,ease:'power2.out'},${r3(T0 + 0.6)});tl.fromTo('#${P}-b-v',{opacity:0,scale:0.6},{opacity:1,scale:1,duration:0.3,ease:'back.out(1.8)'},${r3(T0 + 1.4)});`;
      return { html, js };
    },
    // Caneta de injeção num ladrilho; o.label embaixo
    pen(P, T0, D, o) {
      const html = isoTile(`${P}-tile`, 540, 880, 760) + `<svg id="${P}-pn" class="abs obj" style="left:160px;top:520px;transform:rotate(-14deg)" width="760" height="200" viewBox="0 0 760 200"><rect x="40" y="60" width="520" height="90" rx="40" fill="#F2FBFF" ${S(7)}/><rect x="380" y="60" width="200" height="90" rx="30" fill="${COL.blue}" ${S(7)}/><rect x="150" y="80" width="120" height="50" rx="10" fill="#C9F2EC" ${S(5)}/><rect x="580" y="88" width="70" height="34" rx="8" fill="#9AA0A6" ${S(5)}/><path d="M650 105 H735" ${S(5)}/><rect x="10" y="78" width="40" height="54" rx="10" fill="${COL.amber}" ${S(6)}/></svg>` + (o.label ? lbl(`${P}-l`, o.label, 90, 1000, 900, 64, COL.amber) : '');
      const js = tileJS(`${P}-tile`, T0) + `tl.fromTo('#${P}-pn',{opacity:0,x:-200,rotation:-40},{opacity:1,x:0,rotation:-14,duration:0.45,ease:'back.out(1.4)'},${r3(T0 + 0.05)});` + (o.label ? `tl.fromTo('#${P}-l',{opacity:0,y:30},{opacity:1,y:0,duration:0.3},${r3(T0 + 0.4)});` : '');
      return { html, js };
    },
    // Semana de 7 dias: o.mode 'week' (barra percorre a semana) ou 'once' (uma injeção no primeiro dia)
    calendar(P, T0, D, o) {
      const days = ['D', 'S', 'T', 'Q', 'Q', 'S', 'S'], w = 124, x0 = 540 - (7 * w) / 2, once = o.mode === 'once';
      const boxes = days.map((d, i) => `<div class="abs ${P}-d" style="left:${px(x0 + i * w + 6)}px;top:520px;width:${w - 12}px;height:150px;border-radius:18px;background:${once && i === 0 ? COL.amber : 'rgba(255,255,255,.12)'};border:5px solid ${ink};box-sizing:border-box;text-align:center;font-family:'Archivo Black';font-size:56px;line-height:140px;color:${once && i === 0 ? dark : ink}">${d}</div>`).join('');
      const bar = once ? '' : `<div class="abs" style="left:${x0 + 6}px;top:700px;width:${7 * w - 12}px;height:26px;border-radius:13px;background:rgba(255,255,255,.15)"></div><div id="${P}-bar" class="abs" style="left:${x0 + 6}px;top:700px;width:${7 * w - 12}px;height:26px;border-radius:13px;background:${COL.mint};transform-origin:0 50%"></div>`;
      const mark = once ? `<svg id="${P}-pn" class="abs obj" style="left:${x0 - 20}px;top:390px;transform:rotate(-30deg)" width="260" height="80" viewBox="0 0 260 80"><rect x="10" y="20" width="170" height="40" rx="18" fill="#F2FBFF" ${S(5)}/><rect x="120" y="20" width="70" height="40" rx="14" fill="${COL.blue}" ${S(5)}/><path d="M190 40 H250" ${S(5)}/></svg>` : '';
      const html = boxes + bar + mark + lbl(`${P}-l`, o.label || (once ? '1 INJEÇÃO POR SEMANA' : 'CERCA DE 1 SEMANA'), 90, 790, 900, 64, once ? COL.amber : COL.mint);
      let js = `tl.fromTo('.${P}-d',{opacity:0,y:40},{opacity:1,y:0,duration:0.25,ease:'back.out(1.6)',stagger:0.05},${r3(T0)});tl.fromTo('#${P}-l',{opacity:0},{opacity:1,duration:0.25},${r3(T0 + 0.5)});`;
      if (once) js += `tl.fromTo('#${P}-pn',{opacity:0,y:-120},{opacity:1,y:0,duration:0.4,ease:'bounce.out'},${r3(T0 + 0.4)});`;
      else js += `tl.fromTo('#${P}-bar',{scaleX:0},{scaleX:1,duration:${r3(Math.min(1.6, D * 0.7))},ease:'power1.inOut'},${r3(T0 + 0.4)});`;
      return { html, js };
    },
  };
}
