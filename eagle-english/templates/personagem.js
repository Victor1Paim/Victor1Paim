// Personagem próprio do Eagle English (traço simples, SVG) — usado pelos formatos ABC e Verbo do dia.
// personagem(st): st.pose (neutro, fala1..4, pensando, feliz), st.pose_ant + st.k (transição), st.boca (0 fechada, 1 aberta, 2 'o'), st.piscar.
const C = { pele:"#F4C7A1", cabelo:"#3A2416", camisa:"#1F3F8F", tenis:"#ffffff", traco:"#151515", estrela:"#FFD21F" };
// mãos-alvo relativas ao ombro (x para fora = negativo na esquerda)
const POSES = {
  neutro:   { L:[-38, 228], R:[38, 228] },
  fala1:    { L:[-128, 70], R:[36, 226] },
  fala2:    { L:[-36, 226], R:[128, 70] },
  fala3:    { L:[-150, 120], R:[150, 120] },
  fala4:    { L:[-110, 150], R:[60, 200] },
  pensando: { L:[100, 170], R:[-62, -26], olhar:[6, -8] },
  feliz:    { L:[-36, 226], R:[118, -50], joinha:true, sorriso:true, dobraR:1 },
};
const SH = { L:[125, 292], R:[275, 292] }, A = 118, B = 112;
function ik(s, t, lado, dobra) {               // braço de 2 segmentos (ombro→cotovelo→mão), cotovelo para fora/baixo
  const dx = t[0], dy = t[1]; let d = Math.hypot(dx, dy); d = Math.min(d, A + B - 1);
  const base = Math.atan2(dy, dx), cos = (A * A + d * d - B * B) / (2 * A * d), al = Math.acos(Math.max(-1, Math.min(1, cos)));
  const sg = dobra ?? (lado === "L" ? 1 : -1), ang = base + sg * al;
  const e = [s[0] + A * Math.cos(ang), s[1] + A * Math.sin(ang)];
  const h = [s[0] + dx * d / Math.hypot(dx, dy || 1e-6), s[1] + dy * d / Math.hypot(dx, dy || 1e-6)];
  return [e, h];
}

const T = "#151515";
const ROUPAS = {
  estrela: { cor:"#1F3F8F", enfeite: () => `<path d="M200 352 l9 20 22 2 -17 14 6 22 -20 -12 -20 12 6 -22 -17 -14 22 -2 z" fill="#FFD21F" stroke="${T}" stroke-width="4" stroke-linejoin="round"/>` },
  moletom: { cor:"#8D96A3", manga:"longa", calca:"#3B5B92",
    enfeite: () => `<path d="M140 284 Q200 330 260 284" fill="#7A8390" stroke="${T}" stroke-width="7"/>
      <path d="M186 312 l-4 60 M214 312 l4 60" stroke="#fff" stroke-width="6" stroke-linecap="round"/><circle cx="182" cy="374" r="6" fill="#fff" stroke="${T}" stroke-width="3"/><circle cx="218" cy="374" r="6" fill="#fff" stroke="${T}" stroke-width="3"/>
      <path d="M150 470 L250 470 L262 540 L138 540 Z" fill="#7A8390" stroke="${T}" stroke-width="6" stroke-linejoin="round"/>` },
  praia: { cor:"#16A39A", manga:"curta", bermuda:"#E4C38F", tenis:"#FFD21F",
    enfeite: () => { let f = ""; for (const [x, y, c] of [[150,330,"#fff"],[245,320,"#FFD21F"],[175,420,"#FFD21F"],[240,450,"#fff"],[150,510,"#fff"],[215,520,"#FFD21F"],[262,380,"#fff"]])
        f += `<g transform="translate(${x} ${y})"><circle r="11" fill="${c}" stroke="${T}" stroke-width="3"/><circle r="4" fill="#E8574B"/></g>`;
      return f + `<path d="M176 278 L200 330 L224 278" fill="#F4C7A1" stroke="${T}" stroke-width="6" stroke-linejoin="round"/>`; },
    cabeca: () => `<g><rect x="128" y="64" width="62" height="34" rx="14" fill="#111" stroke="${T}" stroke-width="5"/><rect x="210" y="64" width="62" height="34" rx="14" fill="#111" stroke="${T}" stroke-width="5"/><path d="M190 80 h20" stroke="${T}" stroke-width="6"/></g>` },
  xadrez: { cor:"#C8352E", manga:"longa", calca:"#3B5B92",
    enfeite: () => { let f = `<path d="M178 280 L176 562 L224 562 L222 280 Z" fill="#fff" stroke="${T}" stroke-width="6"/>`;
      for (const y of [330, 400, 470, 540]) f += `<path d="M124 ${y} H176 M224 ${y} H280" stroke="#7E1B17" stroke-width="9" opacity=".8"/>`;
      for (const x of [148, 252]) f += `<path d="M${x} 290 V560" stroke="#7E1B17" stroke-width="9" opacity=".8"/>`;
      return f; } },
  esporte: { cor:"#FFD21F", manga:"curta", cor_manga:"#1F3F8F", bermuda:"#1F3F8F",
    enfeite: () => `<text x="200" y="455" text-anchor="middle" font-family="Montserrat,Arial" font-weight="900" font-size="96" fill="#1F3F8F" stroke="${T}" stroke-width="4">EE</text>`,
    cabeca: () => `<path d="M92 112 Q100 30 200 32 Q300 30 308 112 Z" fill="#1F3F8F" stroke="${T}" stroke-width="7" stroke-linejoin="round"/><path d="M300 100 q46 -6 64 12 q-30 14 -70 8 z" fill="#1F3F8F" stroke="${T}" stroke-width="6" stroke-linejoin="round"/><circle cx="200" cy="40" r="8" fill="#FFD21F" stroke="${T}" stroke-width="3"/>` },
  professor: { cor:"#A8CDEE", manga:"longa", calca:"#BFA06A", tenis:"#5A3A22",
    enfeite: () => `<path d="M162 276 L200 312 L238 276 L226 300 L200 318 L174 300 Z" fill="#fff" stroke="${T}" stroke-width="6" stroke-linejoin="round"/>
      <path d="M200 318 V556" stroke="${T}" stroke-width="4"/>${[360, 410, 460, 510].map(y => `<circle cx="200" cy="${y}" r="6" fill="#fff" stroke="${T}" stroke-width="3"/>`).join("")}
      <path d="M150 380 h28 v34 h-28 z" fill="none" stroke="${T}" stroke-width="4"/><path d="M158 372 v26" stroke="#E3262E" stroke-width="5"/>`,
    rosto: () => `<circle cx="163" cy="150" r="30" fill="none" stroke="${T}" stroke-width="7"/><circle cx="237" cy="150" r="30" fill="none" stroke="${T}" stroke-width="7"/><path d="M193 148 h14" stroke="${T}" stroke-width="7"/>` },
};
function mistura(a, b, k) { return [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k]; }
function personagem(st) {
  const P = POSES[st.pose] || POSES.neutro, Q = POSES[st.pose_ant] || P, k = st.k ?? 1;
  const alvo = l => mistura(Q[l], P[l], k);
  let g = "";
  const R = ROUPAS[st.roupa || window.ROUPA || "estrela"] || ROUPAS.estrela;
  // pernas (calça comprida, bermuda ou perna à mostra) e tênis
  g += `<path d="M170 560 L162 770 M230 560 L240 770" stroke="${C.traco}" stroke-width="10" stroke-linecap="round" fill="none"/>`;
  if (R.calca) g += `<path d="M170 556 L163 748 M230 556 L239 748" stroke="${C.traco}" stroke-width="46" stroke-linecap="round" fill="none"/>
                     <path d="M170 556 L163 748 M230 556 L239 748" stroke="${R.calca}" stroke-width="32" stroke-linecap="round" fill="none"/>`;
  if (R.bermuda) g += `<path d="M122 548 L118 640 L192 644 L200 600 L208 644 L282 640 L278 548 Z" fill="${R.bermuda}" stroke="${C.traco}" stroke-width="7" stroke-linejoin="round"/>`;
  g += `<path d="M128 772 q34 -26 56 0 z M218 772 q34 -26 60 2 z" fill="${R.tenis || C.tenis}" stroke="${C.traco}" stroke-width="7" stroke-linejoin="round"/>`;
  // tronco
  g += `<path d="M128 282 Q200 262 272 282 L282 560 Q200 574 118 560 Z" fill="${R.cor}" stroke="${C.traco}" stroke-width="8" stroke-linejoin="round"/>`;
  g += R.enfeite ? R.enfeite() : "";
  // cabeça
  g += `<circle cx="96" cy="160" r="20" fill="${C.pele}" stroke="${C.traco}" stroke-width="7"/><circle cx="304" cy="160" r="20" fill="${C.pele}" stroke="${C.traco}" stroke-width="7"/>`;
  g += `<circle cx="200" cy="155" r="112" fill="${C.pele}" stroke="${C.traco}" stroke-width="8"/>`;
  g += `<path d="M96 120 Q104 40 196 38 Q292 34 306 118 Q280 84 246 92 Q232 62 200 80 Q168 58 150 92 Q118 84 96 120 Z" fill="${C.cabelo}" stroke="${C.traco}" stroke-width="7" stroke-linejoin="round"/>`;
  g += R.cabeca ? R.cabeca() : "";
  // olhos, sobrancelhas, boca
  const ol = P.olhar || [0, 0];
  if (st.piscar) g += `<path d="M150 150 h26 M224 150 h26" stroke="${C.traco}" stroke-width="7" stroke-linecap="round"/>`;
  else g += `<ellipse cx="${163 + ol[0]}" cy="${150 + ol[1]}" rx="11" ry="16" fill="${C.traco}"/><ellipse cx="${237 + ol[0]}" cy="${150 + ol[1]}" rx="11" ry="16" fill="${C.traco}"/>`;
  g += R.rosto ? R.rosto() : "";
  const sob = st.pose === "pensando" ? -10 : (P.sorriso ? -6 : 0);
  g += `<path d="M146 ${118 + sob} q17 -9 32 -2 M222 ${116} q17 -7 32 2" stroke="${C.traco}" stroke-width="6" stroke-linecap="round" fill="none"/>`;
  const b = st.boca || 0;
  if (b === 0) g += P.sorriso ? `<path d="M166 205 q34 30 68 0" stroke="${C.traco}" stroke-width="7" stroke-linecap="round" fill="none"/>`
                 : (st.pose === "pensando" ? `<path d="M182 212 q18 -6 34 4" stroke="${C.traco}" stroke-width="7" stroke-linecap="round" fill="none"/>`
                 : `<path d="M172 207 q28 16 56 0" stroke="${C.traco}" stroke-width="7" stroke-linecap="round" fill="none"/>`);
  else if (b === 1) g += `<path d="M172 200 q28 34 56 0 q-28 6 -56 0 z" fill="#6B1F24" stroke="${C.traco}" stroke-width="6" stroke-linejoin="round"/>`;
  else g += `<ellipse cx="200" cy="212" rx="20" ry="24" fill="#6B1F24" stroke="${C.traco}" stroke-width="6"/><ellipse cx="200" cy="224" rx="11" ry="7" fill="#E46A6A"/>`;
  // braços
  for (const l of ["L", "R"]) {
    const s = SH[l], [e, h] = ik(s, alvo(l), l, l === "R" && k > 0.5 ? P.dobraR : undefined);
    g += `<path d="M${s[0]} ${s[1]} L${e[0]} ${e[1]} L${h[0]} ${h[1]}" stroke="${C.traco}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" fill="none"/>`;
    if (R.manga) { const ponto = (a, b, f) => [a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f];
      const d = R.manga === "longa" ? `M${s[0]} ${s[1]} L${e[0]} ${e[1]} L${ponto(e, h, 0.78).join(" ")}` : `M${s[0]} ${s[1]} L${ponto(s, e, 0.5).join(" ")}`;
      g += `<path d="${d}" stroke="${C.traco}" stroke-width="40" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
            <path d="${d}" stroke="${R.cor_manga || R.cor}" stroke-width="27" stroke-linecap="round" stroke-linejoin="round" fill="none"/>`; }
    g += `<circle cx="${h[0]}" cy="${h[1]}" r="19" fill="${C.pele}" stroke="${C.traco}" stroke-width="6"/>`;
    if (P.joinha && l === "R" && k > 0.6) g += `<path d="M${h[0]} ${h[1] - 14} l0 -24" stroke="${C.traco}" stroke-width="9" stroke-linecap="round"/>`;
  }
  return g;
}
