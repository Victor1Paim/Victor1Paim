// Receitas de plano para vídeos de dinheiro/economia (002 · inflação em diante): carteira, nota, etiqueta de preço,
// cesta de compras, custo subindo, balança procura × oferta, linha do tempo, carrinhos, manchete, gráfico de inclinação e lanche.
// Tudo desenhado em SVG/CSS; as cores vêm da pele (COL) para funcionar em Cosmos, Neo-brutalismo e Blueprint.
export default function receitasDinheiro({ COL, r3, px, fit }) {
  const ink = COL.ink;
  const S = (n) => `stroke="${ink}" stroke-width="${n}" stroke-linejoin="round" stroke-linecap="round"`;
  const money = (v) => 'R$ ' + v.toFixed(2).replace('.', ',');
  const noteSVG = (gid, w, h, label = '100') => `<defs><linearGradient id="${gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7CC8FF"/><stop offset="1" stop-color="#2E6BD9"/></linearGradient></defs>
<rect x="4" y="4" width="${w - 8}" height="${h - 8}" rx="${h * 0.07}" fill="url(#${gid})" ${S(7)}/>
<rect x="${w * 0.05}" y="${h * 0.1}" width="${w * 0.9}" height="${h * 0.8}" rx="${h * 0.05}" fill="none" stroke="rgba(255,255,255,.55)" stroke-width="3"/>
<circle cx="${w * 0.24}" cy="${h * 0.5}" r="${h * 0.29}" fill="rgba(255,255,255,.35)" ${S(5)}/>
<text x="${w * 0.7}" y="${h * 0.62}" text-anchor="middle" font-family="Archivo Black" font-size="${h * 0.42}" fill="#fff" stroke="${ink}" stroke-width="${h * 0.012}" paint-order="stroke">${label}</text>
<text x="${w * 0.7}" y="${h * 0.84}" text-anchor="middle" font-family="Archivo Black" font-size="${h * 0.12}" fill="#fff">REAIS</text>`;
  const tagPath = (w, h) => `M${h * 0.32} 4 H${w - 4} V${h - 4} H${h * 0.32} L4 ${h / 2} Z`;
  const icons = {
    comida: `<path d="M75 40 C70 20 85 10 95 8" fill="none" ${S(6)}/><ellipse cx="96" cy="30" rx="22" ry="11" transform="rotate(-25 96 30)" fill="#2BB673" ${S(5)}/><circle cx="75" cy="88" r="50" fill="#E63946" ${S(6)}/>`,
    aluguel: `<rect x="30" y="68" width="90" height="70" fill="#FFF3D6" ${S(6)}/><path d="M14 74 L75 16 L136 74 Z" fill="#FF8C1A" ${S(6)}/><rect x="62" y="96" width="26" height="42" fill="#7A4422" ${S(5)}/>`,
    transporte: `<rect x="14" y="28" width="122" height="88" rx="16" fill="#FFD60A" ${S(6)}/><rect x="26" y="40" width="44" height="32" rx="6" fill="#BEE3FF" ${S(4)}/><rect x="80" y="40" width="44" height="32" rx="6" fill="#BEE3FF" ${S(4)}/><circle cx="42" cy="118" r="14" fill="#333" ${S(5)}/><circle cx="108" cy="118" r="14" fill="#333" ${S(5)}/>`,
    luz: `<circle cx="75" cy="62" r="44" fill="#FFE66D" ${S(6)}/><rect x="55" y="104" width="40" height="30" rx="5" fill="#9AA0A6" ${S(5)}/><path d="M60 64 L70 76 L80 64 L90 76" fill="none" ${S(4)}/>`,
    combustivel: `<rect x="20" y="30" width="80" height="110" rx="10" fill="${COL.coral}" ${S(6)}/><rect x="34" y="44" width="52" height="34" rx="5" fill="#fff" ${S(4)}/><path d="M100 50 H120 V110 a10 10 0 0 0 20 0 V60" fill="none" ${S(6)}/>`,
    energia: `<path d="M88 10 L36 82 H70 L58 140 L114 62 H80 Z" fill="#FFD60A" ${S(6)}/>`,
    fabrica: `<path d="M10 140 V70 L50 90 V70 L90 90 V70 L130 90 V140 Z" fill="#B0B7C3" ${S(6)}/><rect x="104" y="22" width="22" height="58" fill="#8A93A3" ${S(5)}/><rect x="28" y="108" width="22" height="20" fill="#FFE66D" ${S(4)}/><rect x="66" y="108" width="22" height="20" fill="#FFE66D" ${S(4)}/>`,
  };
  const icon = (id, k, x, y, size, cls = '') => `<svg id="${id}" class="abs obj ${cls}" style="left:${px(x)}px;top:${px(y)}px" width="${size}" height="${size}" viewBox="0 0 150 150">${icons[k]}</svg>`;
  const arrowUp = (id, x, y, w, h, color) => `<svg id="${id}" class="abs obj" style="left:${x}px;top:${y}px;transform-origin:50% 100%" width="${w}" height="${h}" viewBox="0 0 100 200"><path d="M50 4 L96 70 H68 V196 H32 V70 H4 Z" fill="${color}" ${S(6)}/></svg>`;
  const lbl = (id, text, x, y, w, size, color = ink) => `<div id="${id}" class="abs" style="left:${x}px;top:${y}px;width:${w}px;text-align:center;font-family:'Archivo Black',sans-serif;font-size:${size}px;line-height:1;color:${color};white-space:nowrap">${text}</div>`;
  const pop = (sel, t, extra = '') => `tl.fromTo('${sel}',{opacity:0,scale:0.4},{opacity:1,scale:1,duration:0.3,ease:'back.out(1.8)'${extra}},${r3(t)});`;

  return {
    // Carteira com notas; o.fade: as notas ficam transparentes ("sumiu")
    wallet(P, T0, D, o) {
      const notes = [-12, -2, 9].map((a, i) => `<g transform="translate(${130 + i * 40} ${40 + i * 18}) rotate(${a} 210 100)"><svg width="420" height="200" viewBox="0 0 420 200">${noteSVG(`${P}-g${i}`, 420, 200)}</svg></g>`).join('');
      const html = `<svg id="${P}-w" class="abs obj" style="left:190px;top:330px" width="700" height="640" viewBox="0 0 700 640"><g id="${P}-notes">${notes}</g>
<rect x="40" y="250" width="620" height="370" rx="44" fill="#9A5B2E" ${S(8)}/><rect x="70" y="280" width="560" height="310" rx="30" fill="none" stroke="rgba(0,0,0,.35)" stroke-width="4" stroke-dasharray="16 12"/>
<rect x="380" y="350" width="280" height="150" rx="34" fill="#7A4422" ${S(8)}/><circle cx="600" cy="425" r="24" fill="${COL.amber}" ${S(6)}/></svg>`;
      let js = `tl.fromTo('#${P}-w',{opacity:0,y:80},{opacity:1,y:0,duration:0.35,ease:'back.out(1.4)'},${r3(T0)});`;
      if (o.fade) js += `tl.fromTo('#${P}-notes',{opacity:1,y:0},{opacity:0.08,y:-30,duration:${r3(Math.min(1.4, D * 0.6))},ease:'power2.in'},${r3(T0 + 0.3)});`;
      return { html, js };
    },
    // Nota de R$ 100 grande; o.shrink: encolhe até o.to (escala)
    note(P, T0, D, o) {
      const html = `<svg id="${P}-n" class="abs obj" style="left:140px;top:450px;transform-origin:50% 50%" width="800" height="380" viewBox="0 0 800 380">${noteSVG(`${P}-g`, 800, 380, o.value || '100')}</svg>`;
      let js = pop(`#${P}-n`, T0);
      if (o.shrink) js += `tl.to('#${P}-n',{scale:${o.to || 0.45},duration:${r3(Math.min(1.6, D * 0.7))},ease:'power2.inOut'},${r3(T0 + 0.35)});`;
      return { html, js };
    },
    // Etiqueta de preço que sobe de o.from para o.to (reais), com seta
    priceTag(P, T0, D, o) {
      const w = 660, h = 300, d = r3(Math.min(1.4, D * 0.7));
      const html = `<svg id="${P}-tag" class="abs obj" style="left:90px;top:470px;transform:rotate(-6deg)" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><path d="${tagPath(w, h)}" fill="#FFD60A" ${S(8)}/><circle cx="${h * 0.3}" cy="${h / 2}" r="20" fill="#fff" ${S(6)}/></svg>
<div id="${P}-pr" class="abs" style="left:230px;top:${470 + h / 2 - 52}px;width:${w - 160}px;text-align:center;font-family:'Archivo Black',sans-serif;font-size:${Math.min(96, Math.floor(480 / (money(o.to).length * 0.7)))}px;line-height:1.1;color:#111;white-space:nowrap;transform:rotate(-6deg)">${money(o.from)}</div>
${arrowUp(`${P}-ar`, 800, 390, 170, 340, COL.coral)}`;
      const js = `tl.fromTo('#${P}-tag',{opacity:0,x:-120},{opacity:1,x:0,duration:0.3,ease:'power3.out'},${r3(T0)});tl.fromTo('#${P}-pr',{opacity:0},{opacity:1,duration:0.2},${r3(T0 + 0.05)});`
        + `{const E=document.getElementById('${P}-pr');const S={v:${o.from}};tl.fromTo(S,{v:${o.from}},{v:${o.to},duration:${d},ease:'power2.out',onUpdate:()=>{E.textContent='R$ '+S.v.toFixed(2).replace('.',',')}},${r3(T0 + 0.25)});}`
        + `tl.fromTo('#${P}-ar',{scaleY:0},{scaleY:1,duration:${d},ease:'power2.out'},${r3(T0 + 0.25)});`;
      return { html, js };
    },
    // Cesta de compras; o.items: ícones que entram em sequência com rótulo
    basket(P, T0, D, o) {
      const items = o.items || [];
      const n = items.length, slot = 240, x0 = 540 - (n * slot) / 2;
      const seg = n ? Math.min(0.7, (D - 0.3) / n) : 0;
      const ic = items.map((k, i) => icon(`${P}-i${i}`, k, x0 + i * slot + (slot - 170) / 2, 330, 170) + lbl(`${P}-l${i}`, (o.labels || [])[i] || k.toUpperCase(), x0 + i * slot, 515, slot, 30)).join('');
      const html = ic + `<svg id="${P}-b" class="abs obj" style="left:170px;top:600px" width="740" height="460" viewBox="0 0 740 460"><path d="M150 150 C150 20 590 20 590 150" fill="none" ${S(14)}/>
<path d="M20 150 H720 L640 440 H100 Z" fill="#C98A3E" ${S(8)}/><path d="M60 230 H680 M85 320 H655 M200 150 L215 440 M370 150 V440 M540 150 L525 440" fill="none" stroke="rgba(0,0,0,.35)" stroke-width="6"/></svg>`;
      const js = pop(`#${P}-b`, T0) + items.map((_, i) => pop(`#${P}-i${i}`, T0 + 0.2 + i * seg) + `tl.fromTo('#${P}-l${i}',{opacity:0,y:20},{opacity:1,y:0,duration:0.2},${r3(T0 + 0.3 + i * seg)});`).join('');
      return { html, js };
    },
    // Custo subindo: o.mode 'factory' (fábrica + seta CUSTO) ou 'inputs' (combustível e energia com setas)
    costUp(P, T0, D, o) {
      if (o.mode === 'inputs') {
        const html = icon(`${P}-a`, 'combustivel', 90, 430, 330) + arrowUp(`${P}-aa`, 400, 430, 110, 260, COL.coral) + lbl(`${P}-la`, 'COMBUSTÍVEL', 40, 790, 480, 50)
          + icon(`${P}-b`, 'energia', 560, 430, 330) + arrowUp(`${P}-ab`, 880, 430, 110, 260, COL.coral) + lbl(`${P}-lb`, 'ENERGIA', 560, 790, 440, 50);
        const js = pop(`#${P}-a`, T0) + `tl.fromTo('#${P}-aa',{scaleY:0},{scaleY:1,duration:0.5,ease:'power2.out'},${r3(T0 + 0.2)});tl.fromTo('#${P}-la',{opacity:0},{opacity:1,duration:0.2},${r3(T0 + 0.2)});`
          + pop(`#${P}-b`, T0 + 0.6) + `tl.fromTo('#${P}-ab',{scaleY:0},{scaleY:1,duration:0.5,ease:'power2.out'},${r3(T0 + 0.8)});tl.fromTo('#${P}-lb',{opacity:0},{opacity:1,duration:0.2},${r3(T0 + 0.8)});`;
        return { html, js };
      }
      const html = icon(`${P}-f`, 'fabrica', 90, 400, 520) + arrowUp(`${P}-ar`, 690, 380, 220, 440, COL.coral) + lbl(`${P}-l`, 'CUSTO', 620, 850, 360, 72, COL.coral);
      const js = pop(`#${P}-f`, T0) + `tl.fromTo('#${P}-ar',{scaleY:0},{scaleY:1,duration:0.7,ease:'power2.out'},${r3(T0 + 0.3)});tl.fromTo('#${P}-l',{opacity:0,y:30},{opacity:1,y:0,duration:0.25},${r3(T0 + 0.6)});`;
      return { html, js };
    },
    // Balança procura × oferta; o.tilt: o lado da procura desce
    balanca(P, T0, D, o) {
      const beamY = 520, L = 290, ang = 12, dy = r3(L * Math.sin((ang * Math.PI) / 180));
      const pan = (id, cx, label, nBox, color) => `<div id="${id}" class="abs" style="left:${cx - 140}px;top:${beamY}px;width:280px;height:420px">
<svg class="abs obj" style="left:0;top:0" width="280" height="300" viewBox="0 0 280 300"><path d="M140 6 L30 200 M140 6 L250 200" fill="none" ${S(5)}/>${Array.from({ length: nBox }, (_, i) => `<rect x="${140 - (nBox * 46) / 2 + i * 46 + 3}" y="${158 - (i % 2) * 6}" width="40" height="40" rx="6" fill="${color}" ${S(4)}/>`).join('')}<path d="M14 200 H266 C250 270 30 270 14 200 Z" fill="#B0B7C3" ${S(7)}/></svg>
${lbl(`${id}-t`, label, -40, 300, 360, 46)}</div>`;
      const html = `<svg class="abs obj" style="left:390px;top:${beamY - 40}px" width="300" height="560" viewBox="0 0 300 560"><rect x="138" y="20" width="24" height="470" fill="#8A93A3" ${S(6)}/><path d="M40 540 L150 470 L260 540 Z" fill="#8A93A3" ${S(6)}/><circle cx="150" cy="40" r="26" fill="${COL.amber}" ${S(6)}/></svg>
<div id="${P}-beam" class="abs" style="left:${540 - L - 20}px;top:${beamY - 12}px;width:${2 * L + 40}px;height:24px;border-radius:12px;background:#8A93A3;border:6px solid ${ink};box-sizing:border-box"></div>
${pan(`${P}-pl`, 540 - L, 'PROCURA', 5, COL.amber)}${pan(`${P}-pr`, 540 + L, 'OFERTA', 2, COL.blue)}`;
      let js = `tl.fromTo('#${P}-beam,#${P}-pl,#${P}-pr',{opacity:0,y:-40},{opacity:1,y:0,duration:0.3,ease:'power3.out'},${r3(T0)});`;
      if (o.tilt) js += `tl.fromTo('#${P}-beam',{rotation:0},{rotation:${-ang},duration:0.6,ease:'back.out(1.6)'},${r3(T0 + 0.35)});tl.fromTo('#${P}-pl',{y:0},{y:${dy},duration:0.6,ease:'back.out(1.6)'},${r3(T0 + 0.35)});tl.fromTo('#${P}-pr',{y:0},{y:${-dy},duration:0.6,ease:'back.out(1.6)'},${r3(T0 + 0.35)});`;
      return { html, js };
    },
    // Linha do tempo de o.from até o.to (anos), com marcador andando e o ano grande contando
    timeline(P, T0, D, o) {
      const y0 = o.from || 2010, y1 = o.to || 2026, x0 = 210, x1 = 870, d = r3(Math.min(2.2, D * 0.8));
      const ticks = (o.ticks || [2010, 2014, 2018, 2022, y1]).map((y, i, a) => { const x = x0 + ((y - y0) / (y1 - y0)) * (x1 - x0); return `<div class="abs" style="left:${px(x - 4)}px;top:690px;width:8px;height:40px;background:${ink}"></div>${lbl(`${P}-t${i}`, i === a.length - 1 && o.lastLabel ? o.lastLabel : y, x - 100, 750, 200, 44)}`; }).join('');
      const html = `<div class="abs" style="left:${x0}px;top:700px;width:${x1 - x0}px;height:20px;border-radius:10px;background:${COL.soft};opacity:.45"></div><div id="${P}-bar" class="abs" style="left:${x0}px;top:700px;width:${x1 - x0}px;height:20px;border-radius:10px;background:${COL.amber};transform-origin:0 50%"></div>${ticks}
<div id="${P}-dot" class="abs" style="left:${x0 - 30}px;top:680px;width:60px;height:60px;border-radius:50%;background:${COL.amber};border:8px solid ${ink};box-sizing:border-box"></div>
<div id="${P}-yr" class="t" style="top:400px;font-size:210px;color:${ink}">${y0}</div>`;
      const js = `tl.fromTo('#${P}-bar',{scaleX:0},{scaleX:1,duration:${d},ease:'power1.inOut'},${r3(T0 + 0.15)});tl.fromTo('#${P}-dot',{x:0},{x:${x1 - x0},duration:${d},ease:'power1.inOut'},${r3(T0 + 0.15)});`
        + `{const E=document.getElementById('${P}-yr');const S={v:${y0}};tl.fromTo(S,{v:${y0}},{v:${y1},duration:${d},ease:'power1.inOut',onUpdate:()=>{E.textContent=Math.round(S.v)}},${r3(T0 + 0.15)});}`;
      return { html, js };
    },
    // Dois carrinhos com o mesmo dinheiro: o de hoje perde caixas até sobrar o.keep de 10
    carts(P, T0, D, o) {
      const keep = o.keep ?? 4, colors = [COL.amber, COL.blue, COL.mint, COL.coral, '#FFD60A'];
      const cart = (id, x, label, lose) => {
        const boxes = Array.from({ length: 10 }, (_, i) => { const c = i % 5, r = Math.floor(i / 5); const gone = lose && i >= keep; return `<rect ${gone ? `class="${P}-gone"` : ''} x="${70 + c * 58}" y="${150 - r * 58}" width="52" height="52" rx="6" fill="${colors[(i + r) % 5]}" ${S(4)}/>`; }).join('');
        return `${lbl(`${id}-t`, label, x, 360, 440, 72)}<svg id="${id}" class="abs obj" style="left:${x}px;top:450px" width="440" height="420" viewBox="0 0 440 420">${boxes}<path d="M10 40 H60 L90 300 H380 L410 110 H70" fill="none" ${S(10)}/><path d="M64 110 H410" ${S(10)}/><circle cx="120" cy="350" r="30" fill="#fff" ${S(8)}/><circle cx="350" cy="350" r="30" fill="#fff" ${S(8)}/></svg>${lbl(`${id}-v`, 'R$ 100', x, 890, 440, 60, COL.amber)}`;
      };
      const html = cart(`${P}-a`, 60, '2010', false) + cart(`${P}-b`, 580, 'HOJE', true);
      const js = pop(`#${P}-a`, T0) + pop(`#${P}-b`, T0 + 0.1) + `tl.to('.${P}-gone',{opacity:0,y:-160,rotation:25,duration:0.5,ease:'power2.in',stagger:0.08},${r3(T0 + 0.6)});`;
      return { html, js };
    },
    // Manchete de jornal (o.lines: linhas do título)
    headline(P, T0, D, o) {
      const lines = o.lines || ['INFLAÇÃO', 'CAIU'];
      const size = Math.min(130, Math.floor(740 / (Math.max(...lines.map((l) => l.length)) * 0.88)));
      const html = `<div id="${P}-pp" class="abs" style="left:110px;top:330px;width:860px;height:720px;background:#FFFDF5;border:8px solid #111;box-shadow:16px 16px 0 rgba(0,0,0,.55);box-sizing:border-box;padding:40px 50px;transform-origin:50% 50%">
<div style="font-family:'Archivo Black';font-size:52px;color:#111;text-align:center;letter-spacing:6px">O DIÁRIO</div><div style="height:8px;background:#111;margin:14px 0 6px"></div><div style="height:3px;background:#111;margin-bottom:36px"></div>
${lines.map((l) => `<div style="font-family:'Archivo Black';font-size:${size}px;line-height:1.05;color:#111;text-align:center">${l}</div>`).join('')}
<div style="margin-top:40px">${[1, 0.92, 0.97, 0.7].map((w) => `<div style="height:18px;width:${w * 100}%;background:#C9C9C9;margin:16px 0"></div>`).join('')}</div></div>`;
      const js = `tl.fromTo('#${P}-pp',{opacity:0,x:700,rotation:10},{opacity:1,x:0,rotation:-3,duration:0.45,ease:'power3.out'},${r3(T0)});`;
      return { html, js };
    },
    // Gráfico de preço: sobe rápido e depois sobe mais devagar (não cai)
    slope(P, T0, D, o) {
      const html = `<svg class="abs obj" style="left:140px;top:360px" width="800" height="700" viewBox="0 0 800 700"><path d="M40 20 V640 H780" fill="none" ${S(8)}/>
<path id="${P}-p1" d="M60 600 L380 300" fill="none" stroke="${COL.coral}" stroke-width="18" stroke-linecap="round" stroke-dasharray="440" stroke-dashoffset="440"/>
<path id="${P}-p2" d="M380 300 L760 190" fill="none" stroke="${COL.amber}" stroke-width="18" stroke-linecap="round" stroke-dasharray="400" stroke-dashoffset="400"/>
<circle id="${P}-c" cx="380" cy="300" r="20" fill="#fff" ${S(6)}/></svg>
${lbl(`${P}-l1`, o.l1 || '+10%', 400, 860, 320, 80, COL.coral)}${lbl(`${P}-l2`, o.l2 || '+4%', 560, 450, 320, 80, COL.amber)}<div id="${P}-ly" class="abs" style="left:205px;top:385px;font-family:'Archivo Black',sans-serif;font-size:40px;color:${ink}">PREÇO ↑</div>${lbl(`${P}-lx`, 'TEMPO →', 660, 1030, 300, 40)}`;
      const js = `tl.fromTo('#${P}-p1',{strokeDashoffset:440},{strokeDashoffset:0,duration:0.6,ease:'power2.out'},${r3(T0 + 0.1)});tl.fromTo('#${P}-l1',{opacity:0},{opacity:1,duration:0.2},${r3(T0 + 0.4)});`
        + `tl.fromTo('#${P}-c',{scale:0},{scale:1,duration:0.2,ease:'back.out(2)'},${r3(T0 + 0.7)});tl.fromTo('#${P}-p2',{strokeDashoffset:400},{strokeDashoffset:0,duration:0.8,ease:'power2.out'},${r3(T0 + 0.8)});tl.fromTo('#${P}-l2',{opacity:0},{opacity:1,duration:0.2},${r3(T0 + 1.3)});`;
      return { html, js };
    },
    // Lanche com etiqueta de preço balançando (o.tag)
    lunch(P, T0, D, o) {
      const html = `<svg id="${P}-bg" class="abs obj" style="left:70px;top:520px" width="560" height="480" viewBox="0 0 560 480">
<path d="M40 210 C40 60 520 60 520 210 Z" fill="#E9A23B" ${S(8)}/>${[[160, 120], [250, 95], [340, 115], [210, 165], [310, 160], [420, 150]].map(([x, y]) => `<ellipse cx="${x}" cy="${y}" rx="14" ry="8" fill="#FFF3D6" ${S(3)}/>`).join('')}
<path d="M30 230 Q80 200 130 232 T230 232 T330 232 T430 232 T530 230 L520 260 H40 Z" fill="#2BB673" ${S(6)}/><path d="M60 255 H500 L470 300 L430 262 Z" fill="#FFD60A" ${S(6)}/>
<rect x="40" y="262" width="480" height="80" rx="34" fill="#6B3A1E" ${S(8)}/><path d="M40 352 H520 C520 440 40 440 40 352 Z" fill="#E9A23B" ${S(8)}/></svg>
<div id="${P}-tg" class="abs" style="left:545px;top:400px;width:400px;height:420px;transform-origin:200px 0"><div class="abs" style="left:196px;top:0;width:8px;height:120px;background:${ink}"></div>
<svg class="abs obj" style="left:0;top:110px" width="400" height="200" viewBox="0 0 400 200"><path d="${tagPath(400, 200)}" fill="#FFD60A" ${S(8)}/><circle cx="62" cy="100" r="14" fill="#fff" ${S(5)}/></svg>
<div class="abs" style="left:70px;top:160px;width:330px;text-align:center;font-family:'Archivo Black';font-size:50px;line-height:1.1;color:#111;white-space:nowrap">${o.tag || '2010: R$ ?'}</div></div>`;
      const js = pop(`#${P}-bg`, T0) + `tl.fromTo('#${P}-tg',{rotation:-60,opacity:0},{rotation:-6,opacity:1,duration:0.8,ease:'elastic.out(1,0.45)'},${r3(T0 + 0.35)});`;
      return { html, js };
    },
  };
}
