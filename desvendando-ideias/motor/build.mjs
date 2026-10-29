#!/usr/bin/env node
// Gera index.html, compositions/beat*.html e compositions/captions.html a partir de shots.json
// e dos tempos reais da voz (assets/voz/*.wav -> assets/voz/timing.json via ffmpeg silencedetect).
// Uso: node scripts/build.mjs          (da pasta do projeto)
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync, spawnSync } from 'node:child_process';

const MOTOR = path.dirname(new URL(import.meta.url).pathname);            // motor compartilhado (esta pasta)
const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf('--' + k); return i >= 0 ? argv[i + 1] : d; };
const ROOT = path.resolve(arg('dir', process.cwd()));                      // pasta do vídeo (shots.json, assets/voz): padrão = pasta atual
const J = (p) => JSON.parse(fs.readFileSync(path.join(ROOT, p), 'utf8'));
const data = J('shots.json');
const THEME = arg('tema', 'cosmos');                                    // cosmos | brutal | blueprint | iso
const ONLY = arg('beats', null) ? arg('beats').split(',').map(Number) : null;   // só estes beats (teste de pele)
const OUT = arg('out', null) ? path.resolve(ROOT, arg('out')) : ROOT;   // pasta de saída (outro projeto)
const FULL = !ONLY;                                                      // vídeo inteiro (na pasta do vídeo ou em --out): gera PLANOS, build-out e som
const r3 = (n) => Math.round(n * 1000) / 1000;

// ---------- tempos da voz ----------
function probe(file) {
  const out = execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path.join(ROOT, file)]).toString();
  return parseFloat(out);
}
function silences(file) {
  const r = spawnSync('ffmpeg', ['-hide_banner', '-nostats', '-i', path.join(ROOT, file), '-af', 'silencedetect=noise=-38dB:d=0.10', '-f', 'null', '-'], { encoding: 'utf8' });
  const err = r.stderr || '';
  const s = [...err.matchAll(/silence_start: ([\d.]+)/g)].map((m) => parseFloat(m[1]));
  const e = [...err.matchAll(/silence_end: ([\d.]+)/g)].map((m) => parseFloat(m[1]));
  return s.map((a, i) => [a, e[i] ?? Infinity]);
}
const timingPath = path.join(ROOT, 'assets/voz/timing.json');
let timing = fs.existsSync(timingPath) ? JSON.parse(fs.readFileSync(timingPath, 'utf8')) : {};
data.beats.forEach((b) => {
  if (!timing[b.audio]) timing[b.audio] = { dur: probe(b.audio), silences: silences(b.audio) };
});
fs.writeFileSync(timingPath, JSON.stringify(timing, null, 1));

// ---------- mapeia palavras ao tempo de fala ----------
function mapWords(phrases, dur, sil) {
  const segs = []; let cur = 0;
  for (const [s, e] of sil) { if (s > cur + 0.02) segs.push([cur, s]); cur = Math.max(cur, e); }
  if (cur < dur - 0.02) segs.push([cur, dur]);
  const total = segs.reduce((a, [s, e]) => a + (e - s), 0);
  const real = (x, side) => {
    let acc = 0;
    for (const [s, e] of segs) { const L = e - s; if (side === 'start' ? x < acc + L - 1e-9 : x <= acc + L + 1e-9) return s + (x - acc); acc += L; }
    return segs.at(-1)[1];
  };
  const words = [];
  phrases.forEach((p, pi) => p.split(/\s+/).forEach((w) => words.push({ w, pi, wt: w.length + 1 })));
  const W = words.reduce((a, x) => a + x.wt, 0); let acc = 0;
  for (const x of words) { x.s = real(acc / W * total, 'start'); acc += x.wt; x.e = real(acc / W * total, 'end'); }
  return words;
}

// ---------- organiza beats e planos ----------
let G = 0; const beats = [];
data.beats.forEach((b, i) => {
  const all = data.shots.filter((s) => s.b === i);
  const shots = all.filter((s) => !s.silent), silents = all.filter((s) => s.silent);
  const tm = timing[b.audio];
  const speechEnd = r3(tm.dur + b.gap);
  const dur = r3(speechEnd + silents.reduce((a, s) => a + s.dur, 0));
  const words = mapWords(shots.map((s) => s.t), tm.dur, tm.silences);
  // Fronteiras entre planos: ponto médio estimado entre a última palavra de um plano e a primeira do seguinte,
  // puxado para a pausa real mais próxima (até 0,7 s) quando existe; nunca duas fronteiras na mesma pausa.
  const pauses = tm.silences.map(([a, b2]) => (a + Math.min(b2, tm.dur)) / 2).filter((m) => m > 0.5 && m < tm.dur - 0.3);
  const usedPause = new Set(); let lastB = 0;
  const starts = shots.map((s, k) => {
    if (k === 0) return 0;
    const first = words.find((w) => w.pi === k);
    const prev = [...words].filter((w) => w.pi === k - 1).at(-1);
    let bnd = (prev.e + first.s) / 2;
    const cand = pauses.map((m, ix) => ({ m, ix })).filter((c) => !usedPause.has(c.ix) && Math.abs(c.m - bnd) <= 0.7 && c.m > lastB + 0.7).sort((a, b2) => Math.abs(a.m - bnd) - Math.abs(b2.m - bnd))[0];
    if (cand) { bnd = cand.m; usedPause.add(cand.ix); }
    bnd = Math.max(bnd, lastB + 0.7); lastB = bnd;
    return r3(bnd);
  });
  shots.forEach((s, k) => { s.start = starts[k]; s.end = k + 1 < shots.length ? starts[k + 1] : speechEnd; s.dur = r3(s.end - s.start); s.P = `b${i}s${k + 1}`; });
  let at = speechEnd;
  silents.forEach((s, q) => { s.start = r3(at); s.end = r3(at + s.dur); at += s.dur; s.P = `b${i}s${shots.length + q + 1}`; });
  beats.push({ i, G: r3(G), dur, audioDur: tm.dur, shots: [...shots, ...silents], words, audio: b.audio });
  G += dur;
});
if (ONLY) { const keep = beats.filter((B) => ONLY.includes(B.i)); beats.length = 0; let g = 0; keep.forEach((B) => { B.G = r3(g); g += B.dur; beats.push(B); }); G = g; }
const TOTAL = r3(G);

// ---------- relatório ----------
const report = ['| Plano | Início | Dur | Estilo | Fala |', '|---|---|---|---|---|'];
let warn = 0;
beats.forEach((B) => B.shots.forEach((s) => {
  const flag = s.dur > 2.0 ? ' (plano longo: punch extra no meio)' : s.dur < 0.8 ? ' ⚠ <0,8 s' : '';
  if (flag.includes('⚠')) warn++;
  report.push(`| ${s.P} | ${r3(B.G + s.start)} | ${s.dur}${flag} | ${s.st} | ${s.t} |`);
}));
fs.mkdirSync(OUT, { recursive: true });
if (FULL) fs.writeFileSync(path.join(OUT, 'PLANOS.md'), `# Planos (gerado por motor/build.mjs)\n\nTotal: ${TOTAL} s · ${beats.reduce((a, b) => a + b.shots.length, 0)} planos · avisos: ${warn}\n\n${report.join('\n')}\n`);

if (FULL) if (FULL) { const AN = ['pop', 'blur', 'slide', 'rise'];
  fs.writeFileSync(path.join(OUT, 'build-out.json'), JSON.stringify({ total: TOTAL, beats: beats.map((B) => ({ i: B.i, G: B.G, dur: B.dur })), shots: beats.flatMap((B) => B.shots.map((s, idx) => ({ id: s.P, k: s.k, silent: !!s.silent, start: r3(B.G + s.start), dur: s.dur, cam: s.cam || [], o: s.o || {}, anims: ((s.o || {}).ov || []).map((_, i) => AN[(B.i + idx + i) % AN.length]) }))) }, null, 1)); }
if (FULL) spawnSync('python3', ['-I', path.join(MOTOR, 'sfx.py'), OUT], { cwd: OUT, stdio: 'inherit' });

// ---------- visuais ----------
const GRID = 'linear-gradient(rgba(255,255,255,.07) 1px,transparent 1px) 0 0/60px 60px,linear-gradient(90deg,rgba(255,255,255,.07) 1px,transparent 1px) 0 0/60px 60px,';
const THEMES = {
  // Cosmos: pele do vídeo 001 (azul-noite, formas com brilho)
  cosmos: {
    col: { amber: '#FFB300', mint: '#3DDC97', coral: '#FF4D5E', blue: '#2E8BFF', ink: '#F5F7FF', soft: '#9FB0D8' },
    bg: {
      space: 'radial-gradient(ellipse at 50% 30%,#16264F 0%,#080D22 62%,#04060F 100%)',
      warm: 'radial-gradient(ellipse at 50% 35%,#3A1C08 0%,#150A05 65%,#080403 100%)',
      alert: 'radial-gradient(ellipse at 50% 35%,#4A0F1C 0%,#1A060B 65%,#080305 100%)',
      mint: 'radial-gradient(ellipse at 50% 35%,#0C3A33 0%,#061A18 65%,#030C0B 100%)',
    },
    css: '', base: '#FFFFFF',
    cap: ".cg{position:absolute;left:108px;top:1150px;width:864px;text-align:center;font-family:'Archivo Black',sans-serif;font-size:62px;line-height:1.16;color:#fff;text-shadow:0 4px 18px rgba(0,0,0,.85),0 0 4px rgba(0,0,0,.9);opacity:0}",
  },
  // Neo-brutalismo (laboratório de dados): fundo claro chapado, contorno preto, sombra dura, cores saturadas
  brutal: {
    col: { amber: '#D90368', mint: '#007A4D', coral: '#B3001B', blue: '#3A86FF', ink: '#111111', soft: '#444444' },
    bg: { space: '#FFF3D6', warm: '#FFD60A', alert: '#FFB3C1', mint: '#B8F2D9' },
    css: `#root{color:#111}.stars{display:none}.t{text-shadow:none}
.sun{background:#FFD60A;border:8px solid #111;box-shadow:14px 14px 0 #111;box-sizing:border-box}.suntex{display:none}
.earth{background:#3A86FF;border:8px solid #111;box-shadow:12px 12px 0 #111;box-sizing:border-box}
.pile{background:#3A86FF;border:6px solid #111;box-shadow:8px 8px 0 #111;box-sizing:border-box}
[id$="-liq"]{background:#3A86FF!important;opacity:1!important}[id$="-drop"]{background:#3A86FF!important;border:8px solid #111;box-sizing:border-box}
[id$="-splash"]{background:#3A86FF!important;border:6px solid #111;box-sizing:border-box}[id$="-fill"]{background:#3A86FF!important;border:4px solid #111;box-sizing:border-box}
.qrow{background:#fff;border:6px solid #111;box-shadow:10px 10px 0 #111;color:#111}.qlet{background:#FFD60A;color:#111;border:4px solid #111}
.trk{background:#fff;border:4px solid #111;box-sizing:border-box}
.ball{background:#FF8C1A;border:8px solid #111;box-shadow:14px 14px 0 #111;box-sizing:border-box}svg g[stroke="#2a1304"]{stroke:#111}
.sqb{background:#3A86FF;border:8px solid #111;box-shadow:12px 12px 0 #111;box-sizing:border-box}.sqr{background:#3A86FF;border:4px solid #111;box-sizing:border-box}
.cube .face{border:6px solid #111;background:rgba(255,214,10,.55)}.cube.blue .face{border:6px solid #111;background:rgba(58,134,255,.55)}`,
    base: '#111111',
    cap: ".cgh{display:flex;justify-content:center;align-items:flex-start}.cg{position:static;margin-top:1140px;width:auto;max-width:864px;text-align:center;font-family:'Archivo Black',sans-serif;font-size:56px;line-height:1.18;color:#111;background:#fff;border:6px solid #111;box-shadow:10px 10px 0 #111;padding:14px 26px;box-sizing:border-box;opacity:0}",
  },
  // Blueprint: campo azul com grade, traço claro, hachura, rótulos técnicos
  blueprint: {
    col: { amber: '#FFD166', mint: '#8DFFD1', coral: '#FF8FA3', blue: '#9CC9FF', ink: '#EAF2FF', soft: '#9DB8E8' },
    bg: {
      space: GRID + 'radial-gradient(ellipse at 50% 35%,#154799 0%,#0B2E70 62%,#071B45 100%)',
      warm: GRID + 'radial-gradient(ellipse at 50% 35%,#14509E 0%,#0B3374 62%,#071E4A 100%)',
      alert: GRID + 'radial-gradient(ellipse at 50% 35%,#1C3A8A 0%,#0F2461 65%,#081540 100%)',
      mint: GRID + 'radial-gradient(ellipse at 50% 35%,#13589F 0%,#0A3C78 62%,#06254C 100%)',
    },
    css: `.stars{display:none}.t{font-family:'Oswald',sans-serif;font-weight:700;letter-spacing:.03em;text-shadow:none}.ts{font-family:'IBM Plex Mono',monospace}
.sun{background:repeating-linear-gradient(45deg,rgba(234,242,255,.30) 0 3px,transparent 3px 14px);border:6px solid #EAF2FF;box-shadow:none;box-sizing:border-box}.suntex{display:none}
.earth{background:repeating-linear-gradient(45deg,rgba(156,201,255,.32) 0 3px,transparent 3px 12px);border:6px solid #9CC9FF;box-shadow:none;box-sizing:border-box}
.pile{background:repeating-linear-gradient(45deg,rgba(156,201,255,.30) 0 3px,transparent 3px 12px);border:5px solid #9CC9FF;box-sizing:border-box}
[id$="-liq"]{background:repeating-linear-gradient(0deg,rgba(156,201,255,.55) 0 3px,rgba(156,201,255,.2) 3px 10px)!important}
[id$="-drop"]{background:rgba(156,201,255,.35)!important;border:5px solid #9CC9FF;box-sizing:border-box}[id$="-splash"]{background:rgba(156,201,255,.4)!important}
[id$="-fill"]{background:repeating-linear-gradient(45deg,#9CC9FF 0 4px,#6FA8F0 4px 10px)!important}
.qrow{background:rgba(234,242,255,.08);border:4px solid #9CC9FF;color:#EAF2FF;font-family:'Oswald',sans-serif;font-weight:700}.qlet{background:#FFD166;color:#0B2E70}
.trk{background:rgba(234,242,255,.2)}
.ball{background:repeating-linear-gradient(45deg,rgba(255,190,120,.35) 0 3px,transparent 3px 12px);border:6px solid #FFD166;box-sizing:border-box}svg g[stroke="#2a1304"]{stroke:#FFD166}
.sqb{background:repeating-linear-gradient(45deg,rgba(156,201,255,.45) 0 4px,rgba(156,201,255,.15) 4px 10px);border:6px solid #9CC9FF;box-sizing:border-box}
.sqr{background:repeating-linear-gradient(45deg,rgba(156,201,255,.30) 0 3px,transparent 3px 12px);border:4px solid #9CC9FF;box-sizing:border-box}
.cube .face{border-color:#EAF2FF;background:rgba(234,242,255,.10)}.cube.blue .face{border-color:#9CC9FF;background:rgba(156,201,255,.14)}`,
    base: '#EAF2FF',
    cap: ".cg{position:absolute;left:108px;top:1150px;width:864px;text-align:center;font-family:'Oswald',sans-serif;font-weight:700;letter-spacing:.02em;font-size:68px;line-height:1.18;color:#EAF2FF;text-shadow:0 3px 14px rgba(0,0,0,.8);opacity:0}",
  },
  // Isométrico 2.5D: cenário em eixos a 30° com piso em losango, esferas empilhadas em camadas
  iso: {
    col: { amber: '#FFC857', mint: '#7CFFCB', coral: '#FF6B6B', blue: '#2DD4BF', ink: '#F2FBFF', soft: '#9CC9C9' },
    bg: {
      space: 'radial-gradient(ellipse at 50% 30%,#12383F 0%,#0A1F26 62%,#051217 100%)',
      warm: 'radial-gradient(ellipse at 50% 35%,#3B2A14 0%,#150F07 65%,#080503 100%)',
      alert: 'radial-gradient(ellipse at 50% 35%,#3A1420 0%,#1A0A10 65%,#08040A 100%)',
      mint: 'radial-gradient(ellipse at 50% 35%,#0C3A33 0%,#061A18 65%,#030C0B 100%)',
    },
    css: `.stars{opacity:.35}.pile{background:radial-gradient(circle at 36% 30%,#C9FFF3 0%,#2DD4BF 45%,#0B6E6E 100%)}
.floor{position:absolute;border:4px solid rgba(242,251,255,.35);background:repeating-linear-gradient(0deg,rgba(242,251,255,.10) 0 2px,transparent 2px 60px),repeating-linear-gradient(90deg,rgba(242,251,255,.10) 0 2px,transparent 2px 60px),rgba(45,212,191,.10);transform:scaleY(.5) rotate(45deg)}`,
    base: '#FFFFFF',
    cap: null,
  },
};
THEMES.iso.cap = THEMES.cosmos.cap;
const COL = THEMES[THEME].col, BG = THEMES[THEME].bg;
const fit = (text, size) => Math.min(size, Math.floor(864 / (String(text).length * 0.88)));
const px = (n) => Math.round(n * 100) / 100;

function mulberry32(a) { return () => { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
const rnd = mulberry32(20261028);
const stars = Array.from({ length: 70 }, () => `${Math.floor(rnd() * 1080)}px ${Math.floor(rnd() * 1920)}px 0 ${rnd() < 0.2 ? 1 : 0}px rgba(255,255,255,${(0.25 + rnd() * 0.6).toFixed(2)})`).join(',');

const COMMON_CSS = `
#root{position:absolute;inset:0;overflow:hidden;font-family:'Inter',sans-serif;color:#F5F7FF}
.shot{position:absolute;inset:0;overflow:hidden}
.bg{position:absolute;inset:0}
.stars{position:absolute;left:0;top:0;width:1px;height:1px;background:transparent;box-shadow:${stars}}
.cam{position:absolute;inset:0;transform-origin:50% 38%}
.sun{position:absolute;border-radius:50%;background:radial-gradient(circle at 38% 34%,#FFE08A 0%,#FFB300 32%,#FF6A00 72%,#C23B00 100%);box-shadow:0 0 140px 50px rgba(255,140,0,.40)}
.suntex{position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 0deg,rgba(255,255,255,0),rgba(255,240,200,.22) 18%,rgba(255,255,255,0) 36%,rgba(140,30,0,.28) 58%,rgba(255,255,255,0) 80%)}
.earth{position:absolute;border-radius:50%;background:radial-gradient(circle at 62% 56%,#3DDC97 0 12%,transparent 13%),radial-gradient(circle at 30% 66%,#3DDC97 0 9%,transparent 10%),radial-gradient(circle at 36% 30%,#9ADBFF 0%,#2E8BFF 42%,#0A3C95 100%);box-shadow:0 0 60px 10px rgba(46,139,255,.35)}
.t{position:absolute;left:0;width:1080px;text-align:center;font-family:'Archivo Black',sans-serif;line-height:1;color:#F5F7FF;white-space:nowrap;text-shadow:0 6px 28px rgba(0,0,0,.55)}
.ts{font-family:'Inter',sans-serif;font-weight:700}
.abs{position:absolute}
.sqb{background:linear-gradient(180deg,#5AA2FF,#2E8BFF)}
.sqr{background:linear-gradient(135deg,#5AA2FF,#2E8BFF);border:3px solid #7CC8FF;box-sizing:border-box}
.trk{background:rgba(255,255,255,.18)}
.qrow{position:absolute;left:110px;width:860px;height:140px;border-radius:28px;background:rgba(255,255,255,.09);border:4px solid rgba(255,255,255,.35);display:flex;align-items:center;gap:30px;padding:0 36px;box-sizing:border-box;font-family:'Archivo Black',sans-serif;font-size:58px;color:#F5F7FF}
.qlet{width:86px;height:86px;border-radius:50%;background:#FFB300;color:#101426;display:flex;align-items:center;justify-content:center;font-size:54px;flex:none}
.ball{position:absolute;border-radius:50%;background:radial-gradient(circle at 36% 30%,#FFA552 0%,#E8731A 45%,#8A3A07 100%)}
.pile{position:absolute;border-radius:50%;background:radial-gradient(circle at 36% 30%,#9ADBFF 0%,#2E8BFF 45%,#0A3C95 100%)}
.p3d{position:absolute;left:0;top:0;width:1080px;height:1920px;perspective:1600px}
.cube{position:absolute;width:360px;height:360px;left:360px;top:500px;transform-style:preserve-3d}
.face{position:absolute;width:360px;height:360px;border:6px solid #FFB300;background:rgba(255,179,0,.16);box-sizing:border-box;backface-visibility:visible}
.cube.blue .face{border-color:#2E8BFF;background:rgba(46,139,255,.24)}
.f1{transform:rotateY(0deg) translateZ(180px)}.f2{transform:rotateY(90deg) translateZ(180px)}.f3{transform:rotateY(180deg) translateZ(180px)}
.f4{transform:rotateY(-90deg) translateZ(180px)}.f5{transform:rotateX(90deg) translateZ(180px)}.f6{transform:rotateX(-90deg) translateZ(180px)}
`;

const fmtJS = `const F=n=>String(n).replace(/\\B(?=(\\d{3})+(?!\\d))/g,'.');`;
const CAMS = {
  pushIn: { f: { scale: 1 }, t: { scale: 1.12 }, e: 'power2.inOut' },
  pushInBig: { f: { scale: 1 }, t: { scale: 1.3 }, e: 'power2.in' },
  pullOut: { f: { scale: 1.22 }, t: { scale: 1 }, e: 'power2.out' },
  panL: { f: { x: 60 }, t: { x: -60 }, e: 'power1.inOut' },
  panR: { f: { x: -60 }, t: { x: 60 }, e: 'power1.inOut' },
  tilt: { f: { rotateX: 12, transformPerspective: 1400 }, t: { rotateX: -3, transformPerspective: 1400 }, e: 'power2.inOut' },
  orbit: { f: { rotateY: -18, transformPerspective: 1400 }, t: { rotateY: 18, transformPerspective: 1400 }, e: 'power1.inOut' },
  punch: { f: { scale: 1 }, t: { scale: 1.16 }, e: 'power3.out', d: 0.25 },
};
function camJS(P, T0, D, list) {
  if (!list.length) return '';
  let f = {}, t = {}, e = 'power2.inOut', d = null;
  list.forEach((n) => { const c = CAMS[n]; Object.assign(f, c.f); Object.assign(t, c.t); e = c.e; if (c.d) d = c.d; });
  const s = JSON.stringify;
  if (d) return `tl.fromTo('#${P}-cam',${s(f)},{...${s(t)},duration:${d},ease:'${e}'},${T0});tl.to('#${P}-cam',{scale:1.2,duration:${r3(Math.max(0.1, D - d))},ease:'none'},${r3(T0 + d)});`;
  return `tl.fromTo('#${P}-cam',${s(f)},{...${s(t)},duration:${D},ease:'${e}'},${T0});`;
}

const ENTR = ['pop', 'blur', 'slide', 'rise'];
function ovHTML(P, list) {
  return (list || []).map((o, i) => `<div id="${P}-ov${i}" class="t" style="top:${(list.length === 1 && o.y >= 180 && o.y <= 340) ? 230 : o.y}px;font-size:${fit(o.text, o.size)}px;color:${COL[o.color] || COL.ink}">${o.text}</div>`).join('');
}
function ovJS(P, list, T0, idx) {
  return (list || []).map((o, i) => {
    const a = ENTR[(idx + i) % ENTR.length], id = `#${P}-ov${i}`, t = r3(T0 + 0.05 + i * 0.08);
    if (a === 'pop') return `tl.fromTo('${id}',{opacity:0,scale:0.6},{opacity:1,scale:1,duration:0.3,ease:'back.out(1.6)'},${t});`;
    if (a === 'blur') return `tl.fromTo('${id}',{opacity:0,filter:'blur(14px)'},{opacity:1,filter:'blur(0px)',duration:0.25,ease:'power2.out'},${t});`;
    if (a === 'slide') return `tl.fromTo('${id}',{opacity:0,x:-90},{opacity:1,x:0,duration:0.3,ease:'power4.out'},${t});`;
    return `tl.fromTo('${id}',{opacity:0,y:50},{opacity:1,y:0,duration:0.3,ease:'power4.out'},${t});`;
  }).join('');
}
function numHTML(P, n, color) {
  const fmt = (v) => (n.prefix || '') + String(Math.round(v)).replace(/\B(?=(\d{3})+(?!\d))/g, '.') + (n.suffix || '');
  const txt = fmt(n.from);
  return `<div id="${P}-num" class="t" style="top:${n.y}px;font-size:${fit((n.prefix || '') + '1.300.000' + (n.suffix || ''), n.size)}px;color:${color || COL.amber}">${txt}</div>`;
}
function numJS(P, n, T0) {
  return `{const E=document.getElementById('${P}-num');const S={v:${n.from}};tl.fromTo(S,{v:${n.from}},{v:${n.to},duration:${n.dur || 1},ease:'power3.out',onUpdate:()=>{E.textContent='${n.prefix || ''}'+F(Math.round(S.v))+'${n.suffix || ''}'}},${T0});}`;
}
const sunHTML = (id, cx, cy, w) => `<div id="${id}" class="sun" style="left:${px(cx - w / 2)}px;top:${px(cy - w / 2)}px;width:${w}px;height:${w}px"><div id="${id}-tex" class="suntex"></div></div>`;
const earthHTML = (id, cx, cy, w) => `<div id="${id}" class="earth" style="left:${px(cx - w / 2)}px;top:${px(cy - w / 2)}px;width:${w}px;height:${w}px"></div>`;
const rot = (id, T0, D, deg) => `tl.fromTo('#${id}-tex',{rotation:0},{rotation:${deg},duration:${D},ease:'none'},${T0});`;

// ---------- receitas por tipo de plano ----------
const R = {
  sun(P, T0, D, o) {
    const w = o.w || 880, cy = o.cy || 700;
    return { html: sunHTML(`${P}-sun`, 540, cy, w) + (o.num ? numHTML(P, o.num, COL.ink) : ''), js: rot(`${P}-sun`, T0, D, 35) + (o.num ? numJS(P, o.num, T0) : '') };
  },
  earthSun(P, T0, D, o) {
    const flip = !!o.flip;
    return {
      html: sunHTML(`${P}-sun`, flip ? 320 : 780, 640, 1150) + earthHTML(`${P}-earth`, flip ? 820 : 300, 820, 170) + `<div class="abs" style="left:${flip ? 740 : 220}px;top:915px;width:160px;height:26px;border-radius:50%;background:rgba(0,0,0,.45);filter:blur(10px)"></div>`,
      js: `tl.fromTo('#${P}-sun',{x:${flip ? -40 : 40}},{x:${flip ? 40 : -40},duration:${D},ease:'power1.inOut'},${T0});tl.fromTo('#${P}-earth',{x:${flip ? 90 : -90}},{x:${flip ? -90 : 90},duration:${D},ease:'power1.inOut'},${T0});` + rot(`${P}-sun`, T0, D, 20),
    };
  },
  box(P, T0, D) {
    return {
      html: sunHTML(`${P}-sun`, 540, 700, 480) + `<svg class="abs" style="left:180px;top:340px" width="720" height="720" viewBox="0 0 720 720"><rect id="${P}-rect" x="6" y="6" width="708" height="708" rx="26" fill="none" stroke="${COL.ink}" stroke-width="8" stroke-dasharray="2832" stroke-dashoffset="2832"/></svg>`,
      js: `tl.fromTo('#${P}-rect',{strokeDashoffset:2832},{strokeDashoffset:0,duration:0.7,ease:'power2.out'},${T0});` + rot(`${P}-sun`, T0, D, 30),
    };
  },
  flash(P, T0, D, o) {
    return { html: `<div id="${P}-big" class="t" style="top:560px;font-size:${fit(o.text, 330)}px;color:${COL[o.color] || COL.coral}">${o.text}</div>`, js: `tl.fromTo('#${P}-big',{scale:1.5,opacity:0},{scale:1,opacity:1,duration:0.22,ease:'expo.out'},${T0});` };
  },
  stamp(P, T0, D, o) {
    return {
      html: `<div id="${P}-st" class="abs" style="left:140px;top:610px;width:800px;height:190px;border:12px solid ${COL.coral};border-radius:24px;display:flex;align-items:center;justify-content:center;font-family:'Archivo Black';font-size:${Math.floor(700 / (o.text.length * 0.74))}px;color:${COL.coral};background:rgba(255,77,94,.08)">${o.text}</div>`,
      js: `tl.fromTo('#${P}-st',{scale:2.4,opacity:0,rotation:-14},{scale:1,opacity:1,rotation:-7,duration:0.28,ease:'power4.out'},${T0});`,
    };
  },
  ruler(P, T0, D) {
    return {
      html: `<div id="${P}-line" class="abs" style="left:90px;top:640px;width:900px;height:10px;background:${COL.ink};transform-origin:0 50%"></div><div class="abs" style="left:84px;top:600px;width:10px;height:90px;background:${COL.ink}"></div><div id="${P}-tick" class="abs" style="left:986px;top:600px;width:10px;height:90px;background:${COL.ink}"></div>`,
      js: `tl.fromTo('#${P}-line',{scaleX:0},{scaleX:1,duration:0.6,ease:'power3.out'},${T0});tl.fromTo('#${P}-tick',{opacity:0},{opacity:1,duration:0.15},${r3(T0 + 0.5)});`,
    };
  },
  bigNum(P, T0, D, o) {
    const n = o.num;
    const lab = o.label ? `<div id="${P}-lab" class="t" style="top:${n.y + fit('1.300.000', n.size) + 40}px;font-size:84px;color:${COL[o.labelColor] || COL.ink}">${o.label}</div>` : '';
    const src = o.source ? `<div class="t ts" style="top:1040px;font-size:44px;color:${COL.soft}">${o.source}</div>` : '';
    return { html: numHTML(P, n) + lab + src, js: numJS(P, n, T0) + (o.label ? `tl.fromTo('#${P}-lab',{opacity:0,y:30},{opacity:1,y:0,duration:0.3,ease:'power3.out'},${r3(T0 + 0.1)});` : '') };
  },
  earthsRow(P, T0, D) {
    const dots = Array.from({ length: 109 }, (_, i) => `<span class="abs dot-${P}" style="left:${px(540 - 441 + i * 8.1 - 3.5)}px;top:${650 - 4}px;width:8px;height:8px;border-radius:50%;background:${COL.blue}"></span>`).join('');
    return { html: sunHTML(`${P}-sun`, 540, 650, 900) + dots, js: `tl.fromTo('.dot-${P}',{opacity:0},{opacity:1,duration:0.05,stagger:0.006},${r3(T0 + 0.1)});` + rot(`${P}-sun`, T0, D, 20) };
  },
  ball(P, T0, D, o) {
    const w = 660;
    return {
      html: `<div id="${P}-ball" class="ball" style="left:${540 - w / 2}px;top:${650 - w / 2}px;width:${w}px;height:${w}px"></div><svg class="abs" style="left:${540 - w / 2}px;top:${650 - w / 2}px" width="${w}" height="${w}" viewBox="0 0 100 100"><g fill="none" stroke="#2a1304" stroke-width="1.2"><circle cx="50" cy="50" r="49.4"/><path d="M50 0V100M0 50H100M17 14C36 34 36 66 17 86M83 14C64 34 64 66 83 86"/></g></svg>`,
      js: o.rot ? `tl.fromTo('#${P}-ball',{rotation:-20},{rotation:20,duration:${D},ease:'none'},${T0});` : '',
    };
  },
  macro(P, T0, D) {
    return {
      html: `<div class="ball" style="left:-900px;top:-250px;width:2880px;height:2880px"></div><svg class="abs" style="left:-900px;top:-250px" width="2880" height="2880" viewBox="0 0 100 100"><g fill="none" stroke="#2a1304" stroke-width="0.2"><path d="M50 0V100M0 50H100"/></g></svg><div id="${P}-dot" class="earth" style="left:${540 - 7}px;top:${650 - 7}px;width:14px;height:14px;box-shadow:none"></div>`,
      js: `tl.fromTo('#${P}-cam',{scale:1,transformOrigin:'540px 650px'},{scale:12,transformOrigin:'540px 650px',duration:${D},ease:'power3.in'},${T0});`,
    };
  },
  pin(P, T0, D) {
    return {
      html: `<div class="abs" style="left:0;top:0;width:1080px;height:1920px;background:repeating-linear-gradient(90deg,rgba(255,255,255,.07) 0 2px,transparent 2px 60px)"></div><div id="${P}-needle" class="abs" style="left:520px;top:560px;width:12px;height:560px;background:linear-gradient(90deg,#8a93a8,#e6ebf5,#8a93a8);border-radius:6px"></div><div id="${P}-head" class="pile" style="left:${526 - 55}px;top:${560 - 55}px;width:110px;height:110px"></div>`,
      js: `tl.fromTo('#${P}-needle',{y:-80,opacity:0},{y:0,opacity:1,duration:0.35,ease:'power4.out'},${T0});tl.fromTo('#${P}-head',{x:-140},{x:140,duration:${D},ease:'power1.inOut'},${T0});tl.fromTo('#${P}-needle',{x:-60},{x:60,duration:${D},ease:'power1.inOut'},${T0});`,
    };
  },
  lineSquare(P, T0, D) {
    return {
      html: `<div id="${P}-sq" class="abs sqb" style="left:260px;top:360px;width:560px;height:560px;border-radius:10px;transform-origin:50% 100%"></div>`,
      js: `tl.fromTo('#${P}-sq',{scaleY:0.014},{scaleY:1,duration:${r3(Math.min(1.1, D))},ease:'power3.inOut'},${r3(T0 + 0.15)});`,
    };
  },
  straightLine(P, T0, D) {
    return {
      html: `<svg class="abs" style="left:160px;top:330px" width="760" height="760" viewBox="0 0 760 760"><path d="M20 20V740H740" fill="none" stroke="${COL.ink}" stroke-opacity=".35" stroke-width="6"/><path id="${P}-path" d="M30 730L730 60" fill="none" stroke="${COL.amber}" stroke-width="16" stroke-linecap="round" stroke-dasharray="900" stroke-dashoffset="900"/></svg>`,
      js: `tl.fromTo('#${P}-path',{strokeDashoffset:900},{strokeDashoffset:0,duration:${r3(Math.min(1.0, D))},ease:'power2.out'},${r3(T0 + 0.1)});`,
    };
  },
  cube(P, T0, D, o) {
    const [r0, r1] = o.rot;
    return {
      html: `<div class="p3d"><div id="${P}-cube" class="cube${o.tone === 'blue' ? ' blue' : ''}"><div class="face f1"></div><div class="face f2"></div><div class="face f3"></div><div class="face f4"></div><div class="face f5"></div><div class="face f6"></div></div></div>`,
      js: `tl.fromTo('#${P}-cube',{rotationY:${r0},rotationX:-24},{rotationY:${r1},rotationX:-24,duration:${D},ease:'power1.inOut'},${T0});`,
    };
  },
  meltEarth(P, T0, D) {
    return {
      html: earthHTML(`${P}-earth`, 540, 640, 320) + `<div id="${P}-drop" class="abs" style="left:420px;top:540px;width:240px;height:290px;border-radius:50% 50% 50% 50% / 62% 62% 38% 38%;background:linear-gradient(180deg,#7CC8FF,#2E8BFF);opacity:0"></div><div id="${P}-splash" class="abs" style="left:300px;top:1000px;width:480px;height:70px;border-radius:50%;background:rgba(46,139,255,.55);opacity:0"></div>`,
      js: `tl.fromTo('#${P}-earth',{scale:1,opacity:1},{scale:0.8,opacity:0,duration:0.45,ease:'power2.in'},${r3(T0 + 0.1)});tl.fromTo('#${P}-drop',{opacity:0,scale:0.6},{opacity:1,scale:1,duration:0.4,ease:'power2.out'},${r3(T0 + 0.25)});tl.fromTo('#${P}-drop',{y:0},{y:430,duration:${r3(Math.max(0.5, D - 0.7))},ease:'power2.in'},${r3(T0 + 0.7)});tl.fromTo('#${P}-splash',{opacity:0,scaleX:0.2},{opacity:1,scaleX:1,duration:0.25,ease:'power3.out'},${r3(T0 + D - 0.3)});`,
    };
  },
  sunFill(P, T0, D, o) {
    const w = 860, [f0, f1] = o.fill;
    return {
      html: sunHTML(`${P}-sun`, 540, 650, w) + `<div class="abs" style="left:${540 - w / 2}px;top:${650 - w / 2}px;width:${w}px;height:${w}px;border-radius:50%;overflow:hidden"><div id="${P}-liq" class="abs" style="left:0;top:0;width:${w}px;height:${w}px;background:linear-gradient(180deg,#7CC8FF 0%,#2E8BFF 30%,#0A3C95 100%);opacity:.92"></div></div>`,
      js: `tl.fromTo('#${P}-liq',{y:${px(w * (1 - f0))}},{y:${px(w * (1 - f1))},duration:${D},ease:'power1.inOut'},${T0});` + rot(`${P}-sun`, T0, D, 25),
    };
  },
  earthSolo(P, T0, D) {
    return { html: earthHTML(`${P}-earth`, 540, 700, 560), js: `tl.fromTo('#${P}-earth',{rotation:-15},{rotation:15,duration:${D},ease:'none'},${T0});` };
  },
  spherePile(P, T0, D, o) {
    const rows = o.rows || 3, r = rows > 3 ? 70 : 90, items = [];
    for (let j = 0; j < rows; j++) {
      const n = 5 - (j % 2), y = 650 + (j - (rows - 1) / 2) * (r * 1.74);
      for (let i = 0; i < n; i++) { const x = 540 + (i - (n - 1) / 2) * r * 2; items.push(`<span class="pile pile-${P}" style="left:${px(x - r)}px;top:${px(y - r)}px;width:${r * 2}px;height:${r * 2}px"></span>`); }
    }
    return { html: items.join(''), js: `tl.fromTo('.pile-${P}',{opacity:0,y:60,scale:0.7},{opacity:1,y:0,scale:1,duration:0.3,ease:'back.out(1.4)',stagger:0.03},${T0});` };
  },
  gaps(P, T0, D) {
    const r = 84, circles = [], dia = [];
    for (let j = 0; j < 4; j++) for (let i = 0; i < 4; i++) { const x = 540 + (i - 1.5) * r * 2, y = 740 + (j - 1.5) * r * 2; circles.push(`<span class="pile" style="left:${x - r}px;top:${y - r}px;width:${r * 2}px;height:${r * 2}px"></span>`); if (i < 3 && j < 3) dia.push(`<span class="abs gp-${P}" style="left:${x + r - 20}px;top:${y + r - 20}px;width:40px;height:40px;background:${COL.coral};transform:rotate(45deg)"></span>`); }
    return { html: circles.join('') + dia.join(''), js: `tl.fromTo('.gp-${P}',{opacity:0,scale:0.2},{opacity:1,scale:1,duration:0.25,ease:'back.out(2)',stagger:0.03},${r3(T0 + 0.1)});` };
  },
  barFill(P, T0, D, o) {
    const w = 900, to = o.to, m = o.mode;
    const head = `<div class="abs" style="left:90px;top:560px;width:${w}px;height:170px;border:8px solid ${COL.ink};border-radius:20px;box-sizing:border-box"></div><div id="${P}-fill" class="abs" style="left:98px;top:568px;width:${w - 16}px;height:154px;border-radius:12px;background:linear-gradient(90deg,#2E8BFF,#7CC8FF);transform-origin:0 50%"></div>`;
    if (m === 'grow') return { html: head, js: `tl.fromTo('#${P}-fill',{scaleX:0},{scaleX:${to},duration:${r3(Math.min(1.3, D))},ease:'power3.out'},${T0});` };
    if (m === 'pct') return { html: head + `<div id="${P}-num" class="t" style="top:800px;font-size:210px;color:${COL.amber}">0%</div>`, js: `tl.set('#${P}-fill',{scaleX:${to}},0);{const E=document.getElementById('${P}-num');const S={v:0};tl.fromTo(S,{v:0},{v:74,duration:0.7,ease:'power3.out',onUpdate:()=>{E.textContent=Math.round(S.v)+'%'}},${T0});}` };
    return { html: head + `<div id="${P}-empty" class="abs" style="left:${98 + (w - 16) * to}px;top:568px;width:${(w - 16) * (1 - to)}px;height:154px;border-radius:0 12px 12px 0;background:repeating-linear-gradient(45deg,${COL.coral} 0 14px,transparent 14px 28px)"></div><div id="${P}-num" class="t" style="top:800px;font-size:${fit("26% VAZIO", 190)}px;color:${COL.coral}">26% VAZIO</div>`, js: `tl.set('#${P}-fill',{scaleX:${to}},0);tl.fromTo('#${P}-empty',{opacity:0},{opacity:1,duration:0.2},${T0});tl.fromTo('#${P}-num',{opacity:0,scale:0.7},{opacity:1,scale:1,duration:0.3,ease:'back.out(1.6)'},${r3(T0 + 0.1)});` };
  },
  compare(P, T0, D, o) {
    const top = o.focus === 'top';
    return {
      html: `<div id="${P}-a" class="abs" style="left:0;top:300px;width:1080px;height:300px"><div class="t" style="top:0;font-size:${fit('1,3 MILHÃO', 170)}px;color:${COL.amber}">1,3 MILHÃO</div><div class="t ts" style="top:190px;font-size:64px;color:${COL.soft}">se for volume</div></div><div id="${P}-b" class="abs" style="left:0;top:780px;width:1080px;height:300px"><div class="t" style="top:0;font-size:${fit('≈ 960 MIL', 170)}px;color:${COL.mint}">≈ 960 MIL</div><div class="t ts" style="top:190px;font-size:64px;color:${COL.soft}">Terras inteiras</div></div>`,
      js: `tl.fromTo('#${P}-${top ? 'b' : 'a'}',{opacity:1},{opacity:0.3,duration:0.3,ease:'power2.out'},${r3(T0 + 0.1)});tl.fromTo('#${P}-${top ? 'a' : 'b'}',{scale:0.94},{scale:1.04,duration:${D},ease:'power2.out'},${T0});`,
    };
  },
  starGiant(P, T0, D, o) {
    const g = (cy, w) => `<div id="${P}-giant" class="abs" style="left:${540 - w / 2}px;top:${cy - w / 2}px;width:${w}px;height:${w}px;border-radius:50%;background:radial-gradient(circle at 50% 30%,#FFB38A 0%,#FF5A36 40%,#8E1B0F 100%);box-shadow:0 0 200px 80px rgba(255,90,54,.35)"></div>`;
    if (o.stage === 1) return { html: g(1950, 2400) + sunHTML(`${P}-sun`, 540, 520, 160), js: `tl.fromTo('#${P}-giant',{y:160},{y:0,duration:${D},ease:'power2.out'},${T0});` };
    if (o.stage === 2) return { html: g(1800, 2800) + sunHTML(`${P}-sun`, 540, 300, 90), js: `tl.fromTo('#${P}-giant',{y:100},{y:0,duration:${D},ease:'power2.out'},${T0});` };
    return { html: g(1950, 3000) + sunHTML(`${P}-sun`, 780, 520, 40), js: `tl.fromTo('#${P}-giant',{x:30},{x:-30,duration:${D},ease:'power1.inOut'},${T0});tl.fromTo('#${P}-sun',{x:-110},{x:110,duration:${D},ease:'power1.inOut'},${T0});` };
  },
  quiz(P, T0, D, o) {
    const opts = o.options || [['A', '1 MIL'], ['B', '100 MIL'], ['C', '1 MILHÃO'], ['D', '1 BILHÃO']];
    const mode = o.mode || 'in', ans = o.answer || 'C';
    const head = mode === 'answer' ? 'ACERTOU!' : 'QUANTAS TERRAS CABEM?';
    const hcol = mode === 'answer' ? COL.mint : COL.ink;
    const rows = opts.map(([l, t], i) => `<div id="${P}-r${i}" class="qrow" style="top:${400 + i * 170}px"><span class="qlet">${l}</span><span>${t}</span></div>`).join('');
    const timer = mode === 'timer' ? `<div class="abs trk" style="left:110px;top:310px;width:860px;height:18px;border-radius:9px"></div><div id="${P}-tm" class="abs" style="left:110px;top:310px;width:860px;height:18px;border-radius:9px;background:linear-gradient(90deg,${COL.amber},${COL.coral});transform-origin:0 50%"></div>` : '';
    let js = '';
    if (mode === 'in') js = `tl.fromTo('#${P}-q-head',{opacity:0,y:-40},{opacity:1,y:0,duration:0.3,ease:'power4.out'},${T0});tl.fromTo('.qrow-${P}',{opacity:0,x:-140},{opacity:1,x:0,duration:0.32,ease:'power4.out',stagger:0.09},${r3(T0 + 0.08)});`;
    if (mode === 'timer') js = `tl.fromTo('#${P}-tm',{scaleX:1},{scaleX:0,duration:${D},ease:'none'},${T0});`;
    if (mode === 'answer') {
      const ix = opts.findIndex(([l]) => l === ans);
      js = opts.map((_, i) => i === ix ? `tl.fromTo('#${P}-r${i}',{scale:1},{scale:1.07,duration:0.3,ease:'back.out(2)'},${r3(T0 + 0.1)});` : `tl.fromTo('#${P}-r${i}',{opacity:1},{opacity:0.22,duration:0.25},${r3(T0 + 0.05)});`).join('') + `tl.fromTo('#${P}-q-head',{scale:0.6,opacity:0},{scale:1,opacity:1,duration:0.3,ease:'back.out(1.8)'},${T0});`;
    }
    const ixA = mode === 'answer' ? opts.findIndex(([l]) => l === ans) : -1;
    const rowsFixed = rows.replace(/class="qrow"/g, `class="qrow qrow-${P}"`).replace(new RegExp(`(<div id="${P}-r${ixA}" class="qrow qrow-${P}")`), `$1 data-win="1"`);
    const winCss = ixA >= 0 ? `<style>#${P}-r${ixA}{background:rgba(61,220,151,.22);border-color:${COL.mint}}</style>` : '';
    return { html: `<div id="${P}-q-head" class="t" style="top:200px;font-size:${fit(head, 100)}px;color:${hcol}">${head}</div>${timer}${rowsFixed}${winCss}`, js };
  },
  bigq(P, T0, D) {
    return { html: `<div id="${P}-q" class="t" style="top:430px;font-size:640px;color:${COL.amber}">?</div>`, js: `tl.fromTo('#${P}-q',{scale:0.35,opacity:0,rotation:-12},{scale:1,opacity:1,rotation:0,duration:0.4,ease:'back.out(1.8)'},${T0});` };
  },
  guess(P, T0, D) {
    const n = ['3', '2', '1'], seg = D / 3;
    return {
      html: n.map((x, i) => `<div id="${P}-n${i}" class="t" style="top:520px;font-size:520px;color:${i === 2 ? COL.coral : COL.ink};opacity:0">${x}</div>`).join(''),
      js: n.map((x, i) => `tl.fromTo('#${P}-n${i}',{opacity:0,scale:1.5},{opacity:1,scale:1,duration:0.18,ease:'expo.out'},${r3(T0 + i * seg)});tl.to('#${P}-n${i}',{opacity:0,duration:0.1},${r3(T0 + (i + 1) * seg - 0.1)});`).join(''),
    };
  },
  squares(P, T0, D) {
    const w = 180, items = [];
    for (let j = 0; j < 4; j++) for (let i = 0; i < 4; i++) items.push(`<span class="abs sqr sq-${P}" style="left:${540 + (i - 2) * w}px;top:${740 + (j - 2) * w}px;width:${w}px;height:${w}px"></span>`);
    return { html: items.join(''), js: `tl.fromTo('.sq-${P}',{opacity:0,scale:0.5},{opacity:1,scale:1,duration:0.25,ease:'back.out(1.6)',stagger:0.03},${r3(T0 + 0.05)});` };
  },
  endcard(P, T0, D, o) {
    if (o.big) {
      const sub = o.sub ? `<div id="${P}-b" class="t" style="top:760px;font-size:${fit(o.sub, 74)}px;color:${COL.ink}">${o.sub}</div>` : '', hd = o.handle ? `<div id="${P}-c" class="t ts" style="top:900px;font-size:52px;color:${COL.soft}">@desvendandoideias.ofc</div>` : '';
      return {
        html: `<div id="${P}-a" class="t" style="top:520px;font-size:190px;color:${COL.amber}">${o.big}</div>${sub}${hd}`,
        js: `tl.fromTo('#${P}-a',{opacity:0,scale:0.7},{opacity:1,scale:1,duration:0.35,ease:'back.out(1.6)'},${r3(T0 + 0.05)});` + (o.sub ? `tl.fromTo('#${P}-b',{opacity:0,y:40},{opacity:1,y:0,duration:0.3,ease:'power4.out'},${r3(T0 + 0.1)});` : '') + (o.handle ? `tl.fromTo('#${P}-c',{opacity:0},{opacity:1,duration:0.3},${r3(T0 + 0.3)});` : ''),
      };
    }
    return R.endcardPending(P, T0, D, o);
  },
  endcardPending(P, T0, D, o) {
    // CTA, mensagem final e próximo tema são decisões do usuário (portões 4 e 5): enquanto pendentes, só o @ e um aviso de rascunho.
    return {
      html: `<div id="${P}-c" class="t ts" style="top:760px;font-size:64px;color:${COL.ink}">@desvendandoideias.ofc</div><div id="${P}-p" class="t ts" style="top:900px;font-size:44px;color:${COL.soft}">${o.pending ? '(fecho a definir)' : ''}</div>`,
      js: `tl.fromTo('#${P}-c',{opacity:0,y:30},{opacity:1,y:0,duration:0.35,ease:'power4.out'},${r3(T0 + 0.1)});tl.fromTo('#${P}-p',{opacity:0},{opacity:1,duration:0.3},${r3(T0 + 0.4)});`,
    };
  },
};

// ---------- pele isométrica: esferas em camadas sobre um piso em losango ----------
if (THEME === 'iso') {
  const proj = (i, j, l, r, n) => ({ x: 540 + (i - j) * r * 1.55, y: 640 + (i + j) * r * 0.78 - l * r * 1.5 });
  const floorHTML = (n, r) => { const c = proj((n - 1) / 2, (n - 1) / 2, 0, r, n), sz = Math.round((n * r * 1.55 + r) * 1.4142); return `<div class="floor" style="left:${px(c.x - sz / 2)}px;top:${px(c.y + r * 0.55 - sz / 2)}px;width:${sz}px;height:${sz}px"></div>`; };
  R.spherePile = (P, T0, D, o) => {
    const rows = o.rows || 3, n = 3, layers = rows > 3 ? 3 : 2, r = 64, cells = [];
    for (let l = 0; l < layers; l++) for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) cells.push({ i, j, l });
    cells.sort((a, b) => a.l - b.l || (a.i + a.j) - (b.i + b.j));
    const sph = cells.map(({ i, j, l }) => { const p = proj(i, j, l, r, n); return `<span class="pile pile-${P}" style="left:${px(p.x - r)}px;top:${px(p.y - r)}px;width:${r * 2}px;height:${r * 2}px"></span>`; });
    return { html: floorHTML(n, r) + sph.join(''), js: `tl.fromTo('.pile-${P}',{opacity:0,y:60,scale:0.7},{opacity:1,y:0,scale:1,duration:0.3,ease:'back.out(1.4)',stagger:0.03},${T0});` };
  };
  R.gaps = (P, T0, D) => {
    const n = 4, r = 56, cells = [], marks = [];
    for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) cells.push({ i, j });
    cells.sort((a, b) => (a.i + a.j) - (b.i + b.j));
    const sph = cells.map(({ i, j }) => { const p = proj(i, j, 0, r, n); return `<span class="pile" style="left:${px(p.x - r)}px;top:${px(p.y - r)}px;width:${r * 2}px;height:${r * 2}px"></span>`; });
    for (let i = 0; i < n - 1; i++) for (let j = 0; j < n - 1; j++) { const p = proj(i + 0.5, j + 0.5, 0, r, n); marks.push(`<span class="abs gp-${P}" style="left:${px(p.x - 22)}px;top:${px(p.y + r * 0.5 - 12)}px;width:44px;height:24px;background:${COL.coral};transform:none;clip-path:polygon(50% 0,100% 50%,50% 100%,0 50%)"></span>`); }
    return { html: floorHTML(n, r) + sph.join('') + marks.join(''), js: `tl.fromTo('.gp-${P}',{opacity:0,scale:0.2},{opacity:1,scale:1,duration:0.25,ease:'back.out(2)',stagger:0.03},${r3(T0 + 0.1)});` };
  };
}

// ---------- monta as cenas ----------
fs.mkdirSync(path.join(OUT, 'compositions'), { recursive: true });
beats.forEach((B) => {
  const html = [], js = [];
  B.shots.forEach((s, idx) => {
    const rec = R[s.k];
    if (!rec) throw new Error('tipo de plano desconhecido: ' + s.k);
    const o = s.o || {}, T0 = s.start, D = s.dur;
    const { html: h, js: j } = rec(s.P, T0, D, o);
    html.push(`<div id="${s.P}" class="clip shot" data-start="${s.start}" data-duration="${s.dur}" data-track-index="1"><div class="bg" style="background:${BG[s.bg]}"><div class="stars"></div></div><div id="${s.P}-cam" class="cam" data-layout-allow-overflow>${D > 2.0 ? `<div id="${s.P}-cam2" class="cam" data-layout-allow-overflow>${h}${ovHTML(s.P, o.ov)}</div>` : `${h}${ovHTML(s.P, o.ov)}`}</div></div>`);
    const extra = [];
    if (D > 2.0) { const n = Math.ceil(D / 2.0) - 1; for (let q = 1; q <= n; q++) { const at = r3(T0 + (D * q) / (n + 1)); extra.push(`tl.fromTo('#${s.P}-cam2',{scale:${(1 + 0.09 * (q - 1)).toFixed(2)}},{scale:${(1 + 0.09 * q).toFixed(2)},duration:0.22,ease:'power3.out'},${at});`); } }
    js.push(`/* ${s.P} · ${s.st} · ${s.t} */`, j, ovJS(s.P, o.ov, T0, B.i + idx), camJS(s.P, T0, D, s.cam), ...extra);
  });
  const id = `beat${B.i}`;
  fs.writeFileSync(path.join(OUT, `compositions/${id}.html`), `<template>
<style>${COMMON_CSS}${THEMES[THEME].css}</style>
<div id="root" data-composition-id="${id}" data-width="1080" data-height="1920">
${html.join('\n')}
</div>
<script>
${fmtJS}
const tl = gsap.timeline({ paused: true });
${js.filter(Boolean).join('\n')}
window.__timelines = window.__timelines || {};
window.__timelines["${id}"] = tl;
</script>
</template>
`);
});

// ---------- legendas ----------
{
  const groups = [], js = [];
  beats.forEach((B) => B.shots.forEach((s, k) => {
    if (s.silent) return;
    const gid = `cg-${s.P}`, a = r3(B.G + s.start), d = r3(s.dur);
    const ws = B.words.filter((w) => w.pi === k);
    groups.push(`<div id="${gid}" class="clip cgh" data-start="${a}" data-duration="${d}" data-track-index="1"><div id="${gid}-g" class="cg">${ws.map((w, i) => `<span id="${gid}-w${i}" class="w">${w.w}</span>`).join(' ')}</div></div>`);
    js.push(`tl.fromTo('#${gid}-g',{opacity:0},{opacity:1,duration:0.08,ease:'power1.out'},${a});`);
    ws.forEach((w, i) => {
      const t0 = r3(Math.max(a, B.G + w.s)), t1 = r3(Math.min(a + d, B.G + w.e));
      js.push(`tl.to('#${gid}-w${i}',{color:'${COL.amber}',duration:0.05},${t0});tl.to('#${gid}-w${i}',{color:'${THEMES[THEME].base}',duration:0.05},${r3(Math.max(t0 + 0.05, t1))});`);
    });
    js.push(`tl.to('#${gid}-g',{opacity:0,duration:0.06},${r3(a + d - 0.06)});tl.set('#${gid}-g',{opacity:0},${r3(a + d)});`);
  }));
  fs.writeFileSync(path.join(OUT, 'compositions/captions.html'), `<template>
<style>
#root{position:absolute;inset:0}
.cgh{position:absolute;inset:0}
${THEMES[THEME].cap}
.w{display:inline-block}
</style>
<div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
${groups.join('\n')}
</div>
<script>
const tl = gsap.timeline({ paused: true });
${js.join('\n')}
window.__timelines = window.__timelines || {};
window.__timelines["captions"] = tl;
</script>
</template>
`);
}

// ---------- index ----------
{
  const hosts = beats.map((B) => `<div id="beat${B.i}" data-composition-id="beat${B.i}" data-composition-src="compositions/beat${B.i}.html" data-start="${B.G}" data-duration="${B.dur}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>`);
  const sfxOn = FULL && fs.existsSync(path.join(OUT, 'assets/sfx/sfx-mix.wav'));
  const audios = (sfxOn ? [`<audio id="sfx" src="assets/sfx/sfx-mix.wav" data-start="0" data-duration="${TOTAL}" data-track-index="6" data-volume="1"></audio>`] : []).concat(beats.map((B) => `<audio id="voz${B.i}" src="${B.audio.replace('assets/voz/', 'assets/voz/proc/')}" data-start="${B.G}" data-duration="${r3(B.audioDur)}" data-track-index="5" data-volume="1"></audio>`));
  fs.writeFileSync(path.join(OUT, 'index.html'), `<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * { margin: 0; padding: 0; box-sizing: border-box; }
      html, body { margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #04060f; }
      #captions { z-index: 20; }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="${TOTAL}" data-width="1080" data-height="1920">
      ${hosts.join('\n      ')}
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="${TOTAL}" data-track-index="2" data-track-kind="captions" data-width="1080" data-height="1920"></div>
      ${audios.join('\n      ')}
    </div>
    <script>
      const tl = gsap.timeline({ paused: true });
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
`);
}
fs.mkdirSync(path.join(OUT, 'assets/vendor'), { recursive: true });
fs.copyFileSync(path.join(MOTOR, 'vendor/gsap.min.js'), path.join(OUT, 'assets/vendor/gsap.min.js'));   // o ambiente bloqueia CDNs: GSAP local
if (OUT !== ROOT) {
  fs.mkdirSync(path.join(OUT, 'assets/voz/proc'), { recursive: true });
  beats.forEach((B) => { const f = B.audio.replace('assets/voz/', 'assets/voz/proc/'); fs.copyFileSync(path.join(ROOT, f), path.join(OUT, f)); });
  for (const f of ['hyperframes.json', 'meta.json', 'package.json']) if (fs.existsSync(path.join(ROOT, f))) fs.copyFileSync(path.join(ROOT, f), path.join(OUT, f));
}
console.log(`ok · tema ${THEME} · ${TOTAL} s · ${beats.reduce((a, b) => a + b.shots.length, 0)} planos · avisos de duração: ${warn} (ver PLANOS.md)`);
