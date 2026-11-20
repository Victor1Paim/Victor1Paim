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
function mistura(a, b, k) { return [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k]; }
function personagem(st) {
  const P = POSES[st.pose] || POSES.neutro, Q = POSES[st.pose_ant] || P, k = st.k ?? 1;
  const alvo = l => mistura(Q[l], P[l], k);
  let g = "";
  // pernas e tênis
  g += `<path d="M170 560 L162 770 M230 560 L240 770" stroke="${C.traco}" stroke-width="10" stroke-linecap="round" fill="none"/>`;
  g += `<path d="M128 772 q34 -26 56 0 z M218 772 q34 -26 60 2 z" fill="${C.tenis}" stroke="${C.traco}" stroke-width="7" stroke-linejoin="round"/>`;
  // camiseta (tronco) com estrela
  g += `<path d="M128 282 Q200 262 272 282 L282 560 Q200 574 118 560 Z" fill="${C.camisa}" stroke="${C.traco}" stroke-width="8" stroke-linejoin="round"/>`;
  g += `<path d="M200 352 l9 20 22 2 -17 14 6 22 -20 -12 -20 12 6 -22 -17 -14 22 -2 z" fill="${C.estrela}" stroke="${C.traco}" stroke-width="4" stroke-linejoin="round"/>`;
  // cabeça
  g += `<circle cx="96" cy="160" r="20" fill="${C.pele}" stroke="${C.traco}" stroke-width="7"/><circle cx="304" cy="160" r="20" fill="${C.pele}" stroke="${C.traco}" stroke-width="7"/>`;
  g += `<circle cx="200" cy="155" r="112" fill="${C.pele}" stroke="${C.traco}" stroke-width="8"/>`;
  g += `<path d="M96 120 Q104 40 196 38 Q292 34 306 118 Q280 84 246 92 Q232 62 200 80 Q168 58 150 92 Q118 84 96 120 Z" fill="${C.cabelo}" stroke="${C.traco}" stroke-width="7" stroke-linejoin="round"/>`;
  // olhos, sobrancelhas, boca
  const ol = P.olhar || [0, 0];
  if (st.piscar) g += `<path d="M150 150 h26 M224 150 h26" stroke="${C.traco}" stroke-width="7" stroke-linecap="round"/>`;
  else g += `<ellipse cx="${163 + ol[0]}" cy="${150 + ol[1]}" rx="11" ry="16" fill="${C.traco}"/><ellipse cx="${237 + ol[0]}" cy="${150 + ol[1]}" rx="11" ry="16" fill="${C.traco}"/>`;
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
    g += `<circle cx="${h[0]}" cy="${h[1]}" r="19" fill="${C.pele}" stroke="${C.traco}" stroke-width="6"/>`;
    if (P.joinha && l === "R" && k > 0.6) g += `<path d="M${h[0]} ${h[1] - 14} l0 -24" stroke="${C.traco}" stroke-width="9" stroke-linecap="round"/>`;
  }
  return g;
}
