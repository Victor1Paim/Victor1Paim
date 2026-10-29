// Cena 3D low-poly (Three.js) para vídeos de construção em formato cadeia (004 · telhado em diante).
// Um único mundo; cada plano de shots.json descreve o estado (o.st) e a câmera (o.cam). Tudo é função do tempo:
// renderAt(t) zera o estado, aplica o plano corrente e desenha. Valores [a, b] em o.st são interpolados ao longo do plano.
import * as THREE from './three.module.js';

const ease = (x) => (x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2);
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, k) => a + (b - a) * k;
const V = (a) => new THREE.Vector3(a[0], a[1], a[2]);
function prng(seed) { let s = seed; return () => ((s = (s * 16807) % 2147483647) / 2147483647); }

// câmeras prontas (posição inicial a, final b, alvo l). Planos podem passar {a,b,l} próprios.
export const CAMS = {
  geral: { a: [11, 6.5, 13], b: [8.5, 6, 14.5], l: [0, 2.4, 0] },
  geralEsq: { a: [-12, 6.5, 11], b: [-9, 6, 13.5], l: [0, 2.4, 0] },
  topo: { a: [5, 10.5, 9], b: [3, 10, 10], l: [0, 3.4, 0] },
  topoPerto: { a: [2.5, 7.2, 6], b: [1.5, 6.8, 6.4], l: [0, 3.6, 1.2] },
  telhaPerto: { a: [1.6, 5.2, 4.6], b: [0.6, 5.0, 4.9], l: [0, 3.9, 1.6] },
  telhaMuitoPerto: { a: [0.9, 4.6, 3.6], b: [0.4, 4.5, 3.7], l: [0, 4.0, 2.0] },
  lado: { a: [14, 5.2, 2.5], b: [14.5, 5, 0.5], l: [0, 3.2, 0] },
  frente: { a: [0.5, 3.4, 11], b: [-0.5, 3.2, 12], l: [0, 2.6, 0] },
  beiral: { a: [2.5, 2.2, 7.5], b: [1.5, 2.1, 7.8], l: [0.5, 2.6, 2.5] },
  calha: { a: [5.5, 2.4, 6.5], b: [6.2, 2.2, 5.8], l: [2.6, 2.4, 2.8] },
  rufo: { a: [1.0, 7.5, 5.5], b: [0.2, 7.2, 6.2], l: [3.2, 4.2, 0.8] },
  dentro: { a: [0.6, 1.7, 7.6], b: [-0.2, 1.6, 8.0], l: [0, 1.7, 0], fov: 50 },
  estrutura: { a: [8, 7.5, 9], b: [6.5, 7, 10], l: [0, 3.6, 0] },
  heroi: { a: [-2.2, 2.0, 7.2], b: [-2.6, 1.9, 7.6], l: [-2.6, 1.3, 4.2] },
  final: { a: [9, 4.5, 12], b: [-9, 4.5, 12], l: [0, 2.4, 0] },
};

export function criarCena(canvas, shots) {
  const R = new THREE.WebGLRenderer({ canvas, antialias: true, preserveDrawingBuffer: true });
  R.setSize(1080, 1920, false); R.shadowMap.enabled = true; R.shadowMap.type = THREE.PCFSoftShadowMap;
  const S = new THREE.Scene();
  const SKY_DAY = new THREE.Color(0x8fd0ff), SKY_NIGHT = new THREE.Color(0x1c2a4a);
  S.fog = new THREE.Fog(0x8fd0ff, 34, 80);
  const cam = new THREE.PerspectiveCamera(42, 1080 / 1920, 0.1, 300);
  const hemi = new THREE.HemisphereLight(0xffffff, 0x6a8f5a, 1.1); S.add(hemi);
  const sun = new THREE.DirectionalLight(0xffffff, 1.7); sun.position.set(9, 15, 7); sun.castShadow = true;
  sun.shadow.mapSize.set(1024, 1024); Object.assign(sun.shadow.camera, { left: -12, right: 12, top: 12, bottom: -12 }); sun.shadow.bias = -0.0015; S.add(sun);
  const M = (c, extra = {}) => new THREE.MeshStandardMaterial({ color: c, flatShading: true, roughness: 0.85, ...extra });
  const box = (w, h, d, mat) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat); m.castShadow = m.receiveShadow = true; return m; };
  const rnd = prng(20261029);

  // ---------- chão, árvores, casas ao fundo ----------
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(160, 160), M(0x6cc04a)); ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; S.add(ground);
  const walk = box(2.2, 0.04, 6, M(0xbfc4c9)); walk.position.set(-1, 0.02, 5.6); S.add(walk);
  for (let i = 0; i < 18; i++) {
    const a = rnd() * Math.PI * 2, d = 14 + rnd() * 22;
    const tr = new THREE.Mesh(new THREE.IcosahedronGeometry(1.1 + rnd() * 0.9, 0), M(0x3e9f3a)); tr.position.set(Math.cos(a) * d, 2.4, Math.sin(a) * d); tr.castShadow = true; S.add(tr);
    const tk = box(0.3, 1.6, 0.3, M(0x7a4a22)); tk.position.set(tr.position.x, 0.8, tr.position.z); S.add(tk);
  }
  for (let i = 0; i < 7; i++) { const h = box(4, 3, 4, M(0xe8e2d6)); h.position.set(-24 + i * 8, 1.5, -26 - rnd() * 6); S.add(h); const rf = new THREE.Mesh(new THREE.ConeGeometry(3.3, 1.6, 4), M(0xc8613a)); rf.position.set(h.position.x, 3.8, h.position.z); rf.rotation.y = Math.PI / 4; S.add(rf); }
  const bushes = []; for (let i = 0; i < 9; i++) { const b = new THREE.Mesh(new THREE.IcosahedronGeometry(0.55, 0), M(0x2f8f35)); b.position.set(-3.6 + i * 0.85, 0.4, 3.2); b.castShadow = true; S.add(b); bushes.push(b); }

  // ---------- casa: 4 paredes (frente e fundo com pivô no pé, para "abrir") ----------
  const wallM = M(0xe9edf1), W = 6, D = 5, H = 3;
  const mkWall = (w, d) => { const g = new THREE.Group(); const m = box(w, H, d, wallM); m.position.y = H / 2; g.add(m); S.add(g); return g; };
  const wFront = mkWall(W, 0.2); wFront.position.z = D / 2;
  const wBack = mkWall(W, 0.2); wBack.position.z = -D / 2;
  const wLeft = mkWall(0.2, D); wLeft.position.x = -W / 2;
  const wRight = mkWall(0.2, D); wRight.position.x = W / 2;
  const door = box(1, 2, 0.08, M(0x7a4422)); door.position.set(-1, 1, 0.12); wFront.add(door);
  const win1 = box(1.3, 1, 0.08, M(0x9fd3ff, { metalness: 0.2 })); win1.position.set(1.4, 1.7, 0.12); wFront.add(win1);
  const wet = new THREE.Mesh(new THREE.PlaneGeometry(W, H), new THREE.MeshBasicMaterial({ color: 0x5a6a7a, transparent: true, opacity: 0 })); wet.position.set(0, H / 2, 0.111); wFront.add(wet);
  // interior (aparece no corte)
  const inside = new THREE.Group(); S.add(inside);
  const floor = box(W - 0.2, 0.05, D - 0.2, M(0xcdb38f)); floor.position.y = 0.03; inside.add(floor);
  const sofa = new THREE.Group(); const sa = box(2.2, 0.5, 0.9, M(0x2f56c8)); sa.position.set(0, 0.45, 0); const sb = box(2.2, 0.8, 0.25, M(0x2a4db3)); sb.position.set(0, 0.8, -0.35); sofa.add(sa); sofa.add(sb); sofa.position.set(0.8, 0, -1.3); inside.add(sofa);
  const tv = box(1.4, 0.8, 0.08, M(0x111111)); tv.position.set(-2.75, 1.3, -0.6); tv.rotation.y = Math.PI / 2; inside.add(tv);
  const lamp = box(0.08, 1.6, 0.08, M(0xd9c9a3)); lamp.position.set(2.4, 0.8, -1.8); inside.add(lamp);

  // ---------- laje ----------
  const slabG = new THREE.Group(); slabG.position.set(0, H, 0); S.add(slabG);
  const slab = box(W + 0.4, 0.3, D + 0.4, M(0xd4d7da)); slab.position.y = 0.15; slabG.add(slab);
  const puddles = [[-1.2, 0.6, 0.9], [1.3, -0.4, 0.7], [0.2, -1.4, 0.55], [-2, -1, 0.45], [2.2, 1.3, 0.5]].map(([x, z, r]) => { const p = new THREE.Mesh(new THREE.CylinderGeometry(r, r, 0.02, 14), new THREE.MeshStandardMaterial({ color: 0x3d7fd6, roughness: 0.2, metalness: 0.1 })); p.position.set(x, 0.31, z); slabG.add(p); return p; });
  const crackM = new THREE.MeshBasicMaterial({ color: 0x333333 });
  const cracks = [[0.2, 0.5, 0.9, 0.6], [0.9, 0.6, 1.3, 1.2], [0.9, 0.6, 1.5, 0.2], [-0.4, 0.2, 0.2, 0.5]].map(([x1, z1, x2, z2]) => { const len = Math.hypot(x2 - x1, z2 - z1); const m = new THREE.Mesh(new THREE.BoxGeometry(len, 0.02, 0.05), crackM); m.position.set((x1 + x2) / 2, 0.315, (z1 + z2) / 2); m.rotation.y = -Math.atan2(z2 - z1, x2 - x1); slabG.add(m); return m; });

  // ---------- telhado (duas águas, cumeeira no eixo x) ----------
  const roof = new THREE.Group(); S.add(roof);
  const sides = [1, -1].map((s) => { const g = new THREE.Group(); g.userData.s = s; roof.add(g); return g; });
  const RS = 0.42, COLS = 19, ROWS = 9, X0 = -(COLS - 1) * RS / 2;
  const tileGeo = new THREE.CylinderGeometry(0.2, 0.2, 1, 8, 1, true, -Math.PI / 2, Math.PI); tileGeo.rotateX(Math.PI / 2);
  const tileMat = new THREE.MeshStandardMaterial({ color: 0xffffff, flatShading: true, roughness: 0.8, side: THREE.DoubleSide, emissive: 0xff3300, emissiveIntensity: 0 });
  const tiles = sides.map((g) => { const im = new THREE.InstancedMesh(tileGeo, tileMat, COLS * ROWS); im.castShadow = im.receiveShadow = true; const c = new THREE.Color(); for (let i = 0; i < COLS * ROWS; i++) { c.setHSL(0.045 + rnd() * 0.012, 0.62, 0.48 + rnd() * 0.06); im.setColorAt(i, c); } g.add(im); return im; });
  const ripaGeo = new THREE.BoxGeometry(1, 0.06, 0.1);
  const ripas = sides.map((g) => { const im = new THREE.InstancedMesh(ripaGeo, M(0xc9955a), ROWS); im.castShadow = true; g.add(im); return im; });
  const NC = 11, caibroGeo = new THREE.BoxGeometry(0.14, 0.14, 1);
  const caibros = sides.map((g) => { const im = new THREE.InstancedMesh(caibroGeo, M(0x9c6a3a), NC); im.castShadow = true; g.add(im); return im; });
  const manta = sides.map((g) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshStandardMaterial({ color: 0xe6ebf0, metalness: 0.3, roughness: 0.35, side: THREE.DoubleSide, emissive: 0x9aa4ae, emissiveIntensity: 0.25 })); m.rotation.x = -Math.PI / 2; g.add(m); return m; });
  const rufoM = M(0x9aa3ad, { metalness: 0.6, roughness: 0.4 });
  const rufo = sides.map((g) => { const a = box(0.4, 0.03, 1, rufoM), b = box(0.03, 0.45, 1, rufoM); g.add(a); g.add(b); return [a, b]; });
  const cumGeo = new THREE.CylinderGeometry(0.24, 0.24, 0.5, 8, 1, true, -Math.PI / 2, Math.PI); cumGeo.rotateZ(Math.PI / 2);
  const cume = new THREE.InstancedMesh(cumGeo, new THREE.MeshStandardMaterial({ color: 0xc4522e, flatShading: true, side: THREE.DoubleSide }), COLS); cume.castShadow = true; S.add(cume);
  const calhaM = M(0xb9c0c8, { metalness: 0.5 });
  const calha = new THREE.Group(); S.add(calha);
  const calhaBar = box(1, 0.18, 0.22, calhaM); calha.add(calhaBar);
  const cano = box(0.16, 1, 0.16, calhaM); calha.add(cano);
  // tesouras (4), cada uma com 5 barras recalculadas por quadro
  const trussM = M(0xa36d39);
  const trusses = [-2.7, -0.9, 0.9, 2.7].map((x) => { const bars = Array.from({ length: 5 }, () => { const b = box(0.16, 0.16, 1, trussM); S.add(b); return b; }); return { x, bars }; });
  const beam = (m, p1, p2) => { const d = p2.clone().sub(p1); m.position.copy(p1).add(p2).multiplyScalar(0.5); m.scale.set(1, 1, d.length()); m.lookAt(p2); };
  const forro = box(W - 0.2, 0.05, D - 0.2, M(0xf3f1ec)); forro.position.y = H - 0.05; S.add(forro);
  const gGeo = new THREE.BufferGeometry(); { const d = D / 2, t = 0.1; const v = [-d, 0, -t, d, 0, -t, 0, 1, -t, -d, 0, t, d, 0, t, 0, 1, t]; const idx = [0, 2, 1, 3, 4, 5, 0, 3, 5, 0, 5, 2, 1, 2, 5, 1, 5, 4, 0, 1, 4, 0, 4, 3]; gGeo.setAttribute('position', new THREE.Float32BufferAttribute(v, 3)); gGeo.setIndex(idx); gGeo.computeVertexNormals(); }
  const gables = [-W / 2, W / 2].map((x) => { const m = new THREE.Mesh(gGeo, wallM); m.position.set(x, H, 0); m.rotation.y = Math.PI / 2; m.castShadow = m.receiveShadow = true; S.add(m); return m; });
  const viz = box(4, 6.2, 7, M(0xd9cfc0)); viz.position.set(W / 2 + 2.25, 3.1, 0); S.add(viz);
  const arrows = Array.from({ length: 6 }, (_, i) => { const g = new THREE.Group(); const c = new THREE.Mesh(new THREE.ConeGeometry(0.28, 0.6, 10), M(0xe53935)); c.rotation.x = Math.PI; c.position.y = 0; const st = box(0.12, 0.9, 0.12, M(0xe53935)); st.position.y = 0.75; g.add(c); g.add(st); g.position.set(-2.5 + i, 0, (i % 2 ? 1 : -1) * 0.9); S.add(g); return g; });
  const wire = sides.map((g) => { const m = new THREE.Mesh(new THREE.TorusGeometry(0.16, 0.02, 6, 16), M(0x222222, { metalness: 0.6 })); g.add(m); return m; });

  // ---------- água: chuva e gotas ----------
  const NR = 520, rain = new THREE.InstancedMesh(new THREE.BoxGeometry(0.025, 0.45, 0.025), new THREE.MeshBasicMaterial({ color: 0xdcefff, transparent: true, opacity: 0.75 }), NR); rain.frustumCulled = false; S.add(rain);
  const rainSeed = Array.from({ length: NR }, () => [rnd() * 30 - 15, rnd() * 16, rnd() * 30 - 15]);
  const ND = 90, drops = new THREE.InstancedMesh(new THREE.SphereGeometry(0.07, 8, 6), new THREE.MeshStandardMaterial({ color: 0x3f8fe6, roughness: 0.15 }), ND); drops.frustumCulled = false; S.add(drops);
  const NH = 70, heat = new THREE.InstancedMesh(new THREE.SphereGeometry(0.1, 8, 6), new THREE.MeshBasicMaterial({ color: 0xff7a2f, transparent: true, opacity: 0.85 }), NH); heat.frustumCulled = false; S.add(heat);
  const seeds = Array.from({ length: Math.max(ND, NH) }, () => [rnd(), rnd(), rnd()]);

  // ---------- personagem (avatar do canal: cabeça quadrada, moletom preto com nuvens vermelhas) ----------
  const tex = (w, h, draw) => { const c = document.createElement('canvas'); c.width = w; c.height = h; draw(c.getContext('2d')); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; };
  const cloud = (g, x, y, s) => { g.save(); g.translate(x, y); g.scale(s, s); g.beginPath(); g.arc(-18, 4, 14, Math.PI * 0.5, Math.PI * 1.6); g.arc(0, -8, 16, Math.PI * 1.1, Math.PI * 1.95); g.arc(20, 2, 13, Math.PI * 1.4, Math.PI * 0.6); g.closePath(); g.fillStyle = '#d0191e'; g.fill(); g.lineWidth = 3.5; g.strokeStyle = '#ffffff'; g.stroke(); g.restore(); };
  const hoodTex = tex(256, 256, (g) => { g.fillStyle = '#141414'; g.fillRect(0, 0, 256, 256); [[50, 60, 1], [170, 50, 0.9], [110, 140, 1.1], [40, 200, 0.9], [200, 190, 1]].forEach(([x, y, s]) => cloud(g, x, y, s)); });
  const faceTex = tex(256, 256, (g) => { g.fillStyle = '#f2c7a0'; g.fillRect(0, 0, 256, 256); g.fillStyle = '#141414'; g.beginPath(); g.ellipse(88, 120, 13, 20, 0, 0, 7); g.ellipse(168, 120, 13, 20, 0, 0, 7); g.fill(); g.lineWidth = 7; g.lineCap = 'round'; g.strokeStyle = '#3a2316'; g.beginPath(); g.moveTo(66, 84); g.quadraticCurveTo(88, 72, 110, 86); g.moveTo(146, 80); g.quadraticCurveTo(168, 72, 190, 82); g.stroke(); g.strokeStyle = '#141414'; g.lineWidth = 6; g.beginPath(); g.moveTo(104, 182); g.quadraticCurveTo(140, 196, 170, 176); g.stroke(); });
  const skin = M(0xf2c7a0), hoodM = new THREE.MeshStandardMaterial({ map: hoodTex, roughness: 0.9 }), jeans = M(0x2a3550), hairM = M(0x3d2416);
  const hero = new THREE.Group(); S.add(hero);
  const torso = box(1.0, 1.0, 0.55, hoodM); torso.position.y = 1.55; hero.add(torso);
  const headMats = [skin, skin, skin, skin, new THREE.MeshStandardMaterial({ map: faceTex, roughness: 0.9 }), skin];
  const head = new THREE.Mesh(new THREE.BoxGeometry(0.78, 0.78, 0.78), headMats); head.position.y = 2.45; head.castShadow = true; hero.add(head);
  const hair = new THREE.Group(); head.add(hair);
  for (let i = 0; i < 16; i++) { const c = new THREE.Mesh(new THREE.ConeGeometry(0.16, 0.42, 5), hairM); const a = (i / 16) * Math.PI * 2; c.position.set(Math.cos(a) * 0.3, 0.42 + rnd() * 0.08, Math.sin(a) * 0.3 - 0.04); c.rotation.set(Math.sin(a) * 0.9, 0, -Math.cos(a) * 0.9); hair.add(c); }
  const cap = box(0.82, 0.16, 0.82, hairM); cap.position.y = 0.38; hair.add(cap);
  const hood = box(0.9, 0.3, 0.3, hoodM); hood.position.set(0, 2.05, -0.28); hero.add(hood);
  const mkLimb = (x, y, mat, len, w = 0.32) => { const g = new THREE.Group(); g.position.set(x, y, 0); const m = box(w, len, w, mat); m.position.y = -len / 2; g.add(m); hero.add(g); return g; };
  const armL = mkLimb(-0.67, 2.0, hoodM, 0.95), armR = mkLimb(0.67, 2.0, hoodM, 0.95);
  [armL, armR].forEach((a) => { const h = box(0.3, 0.2, 0.3, skin); h.position.y = -1.02; a.add(h); });
  const legL = mkLimb(-0.25, 1.05, jeans, 1.05, 0.38), legR = mkLimb(0.25, 1.05, jeans, 1.05, 0.38);
  const umb = new THREE.Group(); const umbTop = new THREE.Mesh(new THREE.ConeGeometry(1.0, 0.45, 12, 1, true), new THREE.MeshStandardMaterial({ map: tex(256, 64, (g) => { for (let i = 0; i < 12; i++) { g.fillStyle = i % 2 ? '#ffffff' : '#e53935'; g.fillRect(i * 256 / 12, 0, 256 / 12 + 1, 64); } }), side: THREE.DoubleSide, flatShading: true })); umbTop.position.y = 1.3; const stick = box(0.05, 1.3, 0.05, M(0x333333)); stick.position.y = 0.65; umb.add(umbTop); umb.add(stick); umb.position.y = -1.05; armR.add(umb);
  const sweat = Array.from({ length: 4 }, (_, i) => { const d = new THREE.Mesh(new THREE.SphereGeometry(0.06, 6, 5), M(0x8fd3ff)); head.add(d); d.userData.i = i; return d; });

  // ---------- estado ----------
  const DEF = { rain: 0, wind: 0, night: 0, slab: 0, slabTilt: 0, slabExpand: 0, puddles: 0, crack: 0, drip: 0,
    roof: 0, build: 1, overlap: 1, angle: 17, eave: 0.55, gapDrops: 0, flowDrops: 0, pool: 0,
    ripas: 0, caibros: 0, tesouras: 0, sag: 0, weight: 0, cumeeira: 0, ridgeGap: 0,
    wallWet: 0, wallRun: 0, eaveDrops: 0, calha: 0, vizinho: 0, rufo: 0, neighborRun: 0,
    heat: 0, manta: 0, mantaDrops: 0, windRain: 0, cut: 0, hotAir: 0, forro: 0, arame: 0, tileLift: 0, cutRoof: 0,
    hero: 1, heroX: -2.6, heroZ: 4.4, heroRot: 0.35, pose: 'idle' };
  const shotAt = (t) => { let s = shots[0]; for (const x of shots) if (t >= x.start - 1e-6) s = x; return s; };

  function setTiles(st, sideIdx, a, L, t) {
    const im = tiles[sideIdx], s = sides[sideIdx].userData.s, m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), p = new THREE.Vector3(), sc = new THREE.Vector3();
    const len = RS * lerp(0.82, 1.32, st.overlap), u0 = st.ridgeGap ? 0.32 : 0.14;
    let k = 0;
    for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) {
      const u = u0 + RS * (r + 0.5) * lerp(1, 0.98, st.overlap);
      const on = st.roof && u < L && Math.abs(X0 + c * RS) <= W / 2 + st.eave + 0.05 && (!st.vizinho || X0 + c * RS < W / 2 + 0.2);
      const order = (r * 0.09 + c * 0.012) / 1.0, kb = clamp((st.build - order) * 6);
      const lift = st.tileLift && r === ROWS - 1 && c === COLS - 2 && s === 1 ? st.tileLift : 0;
      const cutHide = st.cutRoof && s === 1 && Math.abs(X0 + c * RS) < 1.5 && r > 1;
      p.set(X0 + c * RS, 0.16 + (r % 2) * 0.002 + st.overlap * 0.04 * (ROWS - r) / ROWS + lift * 0.6, s * u);
      q.setFromEuler(new THREE.Euler(-s * lift * 0.9, 0, 0));
      const vis = on && !cutHide ? Math.max(0.001, ease(kb)) : 0.001;
      sc.set(vis, vis, len * vis); m4.compose(p, q, sc); im.setMatrixAt(k++, m4);
    }
    im.instanceMatrix.needsUpdate = true;
  }

  function apply(st, t, p) {
    S.background = SKY_DAY.clone().lerp(SKY_NIGHT, st.night); S.fog.color.copy(S.background);
    sun.intensity = lerp(1.7, 0.15, st.night); hemi.intensity = lerp(1.1, 0.35, st.night);
    // paredes (abrem para fora com o peso)
    wFront.rotation.x = st.sag * 0.14; wBack.rotation.x = -st.sag * 0.14; wFront.visible = !st.cut; wet.material.opacity = st.wallWet * 0.55;
    inside.visible = true; tv.visible = sofa.visible = lamp.visible = !!st.cut;
    bushes.forEach((b) => (b.visible = !st.cut));
    // laje
    slabG.visible = !!st.slab; slabG.rotation.x = st.slabTilt * 0.24; slab.scale.x = 1 + st.slabExpand * 0.05; slabG.position.y = H + st.slabTilt * 0.2;
    puddles.forEach((m, i) => { const k = clamp(st.puddles * 1.4 - i * 0.12); m.scale.set(k || 0.001, 1, k || 0.001); m.visible = k > 0.01; });
    cracks.forEach((m, i) => { m.visible = st.crack > i * 0.22; m.scale.x = clamp(st.crack * 3 - i * 0.6, 0.001, 1); });
    // telhado
    const a = THREE.MathUtils.degToRad(st.angle), hR = (D / 2) * Math.tan(a) * (1 - st.sag * 0.35), L = (D / 2 + st.eave) / Math.cos(a);
    sides.forEach((g, i) => { const s = g.userData.s; g.position.set(0, H + hR + 0.05, 0); g.rotation.x = s * a; setTiles(st, i, a, L, t); });
    const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), pv = new THREE.Vector3(), sc = new THREE.Vector3();
    sides.forEach((g, i) => {
      const s = g.userData.s, len = W + 2 * st.eave + 0.2;
      for (let r = 0; r < ROWS; r++) { const u = 0.14 + RS * (r + 0.5), kb = clamp((st.ripas - r / ROWS) * 4); pv.set(0, 0.0, s * (u - RS * 0.3)); sc.set(len * Math.max(0.001, kb), 1, 1); m4.compose(pv, q, sc); ripas[i].setMatrixAt(r, m4); }
      ripas[i].visible = st.ripas > 0; ripas[i].instanceMatrix.needsUpdate = true;
      for (let c = 0; c < NC; c++) { const x = -W / 2 - st.eave + 0.1 + c * (W + 2 * st.eave - 0.2) / (NC - 1), kb = clamp((st.caibros - c / NC) * 4); pv.set(x, -0.12, s * L * kb / 2); sc.set(1, 1, Math.max(0.001, L * kb)); m4.compose(pv, q, sc); caibros[i].setMatrixAt(c, m4); }
      caibros[i].visible = st.caibros > 0; caibros[i].instanceMatrix.needsUpdate = true;
      manta[i].visible = st.manta > 0; manta[i].scale.set(len, L * st.manta || 0.001, 1); manta[i].position.set(0, 0.07, s * L * st.manta / 2);
      rufo[i].forEach((m, j) => { m.visible = st.rufo > 0 && st.vizinho > 0; m.scale.z = L * clamp(st.rufo); m.position.set(W / 2 + (j ? 0.38 : 0.2), j ? 0.32 : 0.2, s * L * clamp(st.rufo) / 2); });
      wire[i].visible = st.arame > 0 && s === 1; wire[i].position.set(X0 + (COLS - 2) * RS, 0.2, s * (L - 0.25)); wire[i].rotation.y = 0; wire[i].scale.setScalar(Math.max(0.001, st.arame));
    });
    tileMat.emissiveIntensity = st.heat * 0.55;
    // cumeeira
    for (let c = 0; c < COLS; c++) { const kb = clamp((st.cumeeira - c / COLS) * 3); pv.set(X0 + c * RS, H + hR + 0.2, 0); sc.setScalar(Math.max(0.001, kb)); m4.compose(pv, q, sc); cume.setMatrixAt(c, m4); }
    cume.visible = st.cumeeira > 0; cume.instanceMatrix.needsUpdate = true;
    // calha e cano (na beirada da frente)
    const eY = H + hR + 0.05 - L * Math.sin(a), eZ = L * Math.cos(a);
    calha.visible = st.calha > 0; calhaBar.scale.set((W + 2 * st.eave) * clamp(st.calha), 1, 1); calhaBar.position.set(0, eY - 0.12, eZ + 0.08); cano.scale.y = Math.max(0.001, eY * clamp(st.calha * 2 - 1)); cano.position.set(W / 2 + st.eave - 0.15, eY - eY * clamp(st.calha * 2 - 1) / 2 - 0.1, eZ + 0.08);
    // tesouras
    trusses.forEach((tr, j) => { const vis = st.tesouras > j * 0.2; tr.bars.forEach((b) => (b.visible = vis)); if (!vis) return;
      const top = new THREE.Vector3(tr.x, H + hR, 0), l = new THREE.Vector3(tr.x, H, -D / 2), r = new THREE.Vector3(tr.x, H, D / 2), mid = new THREE.Vector3(tr.x, H, 0);
      beam(tr.bars[0], l, top); beam(tr.bars[1], r, top); beam(tr.bars[2], l, r); beam(tr.bars[3], mid, top);
      beam(tr.bars[4], mid, new THREE.Vector3(tr.x, H + hR / 2, D / 4)); });
    gables.forEach((g) => { g.visible = (st.roof > 0 || st.ripas > 0 || st.caibros > 0) && !(st.tesouras > 0 && !st.roof); g.scale.y = Math.max(0.001, hR); });
    forro.visible = st.forro > 0; forro.scale.set(clamp(st.forro, 0.001, 1), 1, 1);
    viz.visible = !!st.vizinho;
    arrows.forEach((g, i) => { g.visible = st.weight > 0; g.position.y = H + hR + 1.2 + Math.max(0, 1 - st.weight * 1.5 + i * 0.05) * 3 - (Math.sin(t * 8 + i) * 0.05); });
    // chuva
    for (let i = 0; i < NR; i++) { const [x, y0, z] = rainSeed[i]; const y = ((y0 - t * 11) % 16 + 16) % 16; pv.set(x + (st.wind ? -(16 - y) * 0.45 * st.wind : 0), y, z); q.setFromEuler(new THREE.Euler(0, 0, st.wind * 0.45)); sc.setScalar(st.rain ? 1 : 0.001); m4.compose(pv, q, sc); rain.setMatrixAt(i, m4); }
    rain.instanceMatrix.needsUpdate = true;
    // gotas: cada modo usa uma faixa das 90 instâncias
    let k = 0; const put = (x, y, z) => { pv.set(x, y, z); sc.setScalar(1); m4.compose(pv, q, sc); drops.setMatrixAt(k++, m4); };
    const roofPt = (x, u, s) => { const sg = sides[s === 1 ? 0 : 1]; return new THREE.Vector3(x, 0.32, s * u).applyEuler(new THREE.Euler(s * a, 0, 0)).add(sg.position); };
    if (st.drip) for (let i = 0; i < 12; i++) { const ph = ((t * 0.9 + seeds[i][0]) % 1); put(0.6 + seeds[i][1] * 0.6, H - 0.05 - ph * (H - 0.1), 0.5 + seeds[i][2] * 0.5); }
    if (st.gapDrops || st.flowDrops || st.pool) for (let i = 0; i < 40; i++) { const [r1, r2] = seeds[i]; const ph = ((t * 0.5 + r1) % 1); const x = X0 + Math.floor(r2 * COLS) * RS + (st.gapDrops ? RS / 2 : 0); const u = st.pool ? 0.6 + r1 * (L - 0.8) : ph * L; const v = roofPt(x, u, 1); if (st.gapDrops && ph > 0.8) v.y -= (ph - 0.8) * 2; put(v.x, v.y, v.z); }
    if (st.eaveDrops || st.wallRun) for (let i = 0; i < 24; i++) { const ph = ((t * 0.8 + seeds[i][0]) % 1), x = -W / 2 + seeds[i][1] * W; if (st.wallRun) put(x, eY - ph * eY, D / 2 + 0.14); else put(x, eY - ph * eY, eZ + 0.15 + ph * 0.25); }
    if (st.calha > 0.9 && st.rain) for (let i = 0; i < 10; i++) { const ph = ((t * 1.1 + seeds[i][2]) % 1); put(W / 2 + st.eave - 0.15, eY - ph * eY, eZ + 0.08); }
    if (st.neighborRun) for (let i = 0; i < 16; i++) { const ph = ((t * 0.7 + seeds[i][1]) % 1), z = -2 + seeds[i][0] * 4; put(W / 2 + 0.06, 6 - ph * 2.6, z); }
    if (st.mantaDrops) for (let i = 0; i < 16; i++) { const ph = ((t * 0.6 + seeds[i][0]) % 1); const v = roofPt(-2 + seeds[i][1] * 4, ph * L, 1); v.y -= 0.18; put(v.x, v.y, v.z); }
    if (st.windRain) for (let i = 0; i < 14; i++) { const ph = ((t * 0.9 + seeds[i][2]) % 1); const v = roofPt(-2.5 + seeds[i][0] * 5, L - ph * 1.6, 1); v.y -= 0.12; put(v.x + 0.3, v.y, v.z); }
    for (; k < ND; k++) { pv.set(0, -50, 0); sc.setScalar(0.001); m4.compose(pv, q, sc); drops.setMatrixAt(k, m4); }
    drops.instanceMatrix.needsUpdate = true;
    // ar quente (no corte): desce até a sala, ou fica preso acima do forro
    for (let i = 0; i < NH; i++) { const [r1, r2, r3] = seeds[i]; let y = H + hR * 0.6 - ((t * 0.35 + r1) % 1) * (st.forro > 0.9 ? hR * 0.55 : H + hR * 0.4); if (st.forro > 0.9) y = Math.max(y, H + 0.1); pv.set(-2.6 + r2 * 5.2, y, -2 + r3 * 4); sc.setScalar(st.hotAir ? 1 : 0.001); m4.compose(pv, q, sc); heat.setMatrixAt(i, m4); }
    heat.instanceMatrix.needsUpdate = true;
    // personagem
    hero.visible = !!st.hero; hero.position.set(st.heroX, st.pose === 'sit' ? -0.45 : 0, st.heroZ); hero.rotation.y = st.heroRot; hero.scale.setScalar(0.62);
    const sw = Math.sin(t * 6);
    armL.rotation.set(0, 0, 0.12); armR.rotation.set(0, 0, -0.12); legL.rotation.set(0, 0, 0); legR.rotation.set(0, 0, 0); umb.visible = false; head.rotation.set(0, 0, 0);
    sweat.forEach((d) => (d.visible = false));
    if (st.pose === 'umbrella') { armR.rotation.set(-1.0, 0, -0.25); umb.visible = true; umb.rotation.x = 1.0; head.rotation.y = Math.sin(t * 2) * 0.15; }
    if (st.pose === 'celebrate') { armL.rotation.z = 2.6 + sw * 0.15; armR.rotation.z = -2.6 - sw * 0.15; hero.position.y = Math.abs(Math.sin(t * 6)) * 0.25; }
    if (st.pose === 'think') { armR.rotation.set(-1.9, 0, 0.5); head.rotation.z = 0.12; }
    if (st.pose === 'worried') { armL.rotation.set(-0.6, 0, 1.1); armR.rotation.set(-0.6, 0, -1.1); head.rotation.x = Math.sin(t * 3) * 0.1; }
    if (st.pose === 'sweat' || st.pose === 'sit') { if (st.pose === 'sit') { legL.rotation.x = legR.rotation.x = -1.5; } armR.rotation.set(-1.2 + sw * 0.5, 0, -0.6); sweat.forEach((d, i) => { d.visible = st.pose === 'sweat' || st.heat > 0 || st.hotAir > 0; const ph = (t * 0.8 + i * 0.25) % 1; d.position.set(-0.35 + i * 0.23, 0.3 - ph * 0.6, 0.42); }); }
    // câmera
    return { a, hR, L };
  }

  function renderAt(t) {
    const s = shotAt(t), o = s.o || {}, p = clamp((t - s.start) / Math.max(0.01, s.dur)), e = ease(p);
    const st = { ...DEF };
    for (const [k, v] of Object.entries(o.st || {})) st[k] = Array.isArray(v) && typeof v[0] === 'number' ? lerp(v[0], v[1], v[2] === 'lin' ? p : e) : v;
    apply(st, t, p);
    const c = typeof o.cam === 'string' ? CAMS[o.cam] : (o.cam || CAMS.geral);
    const ec = s.camDur ? ease(clamp((t - s.camStart) / Math.max(0.01, s.camDur))) : e;   // câmera anda ao longo do plano visual inteiro
    cam.position.copy(V(c.a).lerp(V(c.b || c.a), ec)); cam.fov = c.fov || 42; cam.updateProjectionMatrix(); cam.lookAt(V(c.l).lerp(V(c.lb || c.l), ec));
    R.render(S, cam);
  }
  return { renderAt };
}
