#!/usr/bin/env node
// Confere um vídeo antes de entregar. Uso (na pasta do vídeo): node ../../motor/checar.mjs [--dir pasta] [--full]
//   --full também roda `npx hyperframes check` (lint, runtime, layout, contraste; ~1 min).
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const argv = process.argv.slice(2);
const arg = (k, d) => { const i = argv.indexOf('--' + k); return i >= 0 ? argv[i + 1] : d; };
const DIR = path.resolve(arg('dir', process.cwd()));
const FULL = argv.includes('--full');
const rows = []; let fail = 0, warn = 0;
const add = (st, nome, det) => { rows.push([st, nome, det]); if (st === 'FALHA') fail++; if (st === 'AVISO') warn++; };
const rd = (p) => JSON.parse(fs.readFileSync(path.join(DIR, p), 'utf8'));
const ex = (p) => fs.existsSync(path.join(DIR, p));

if (!ex('shots.json')) { console.error('sem shots.json em', DIR); process.exit(1); }
const data = rd('shots.json');
if (!ex('build-out.json')) add('FALHA', 'Build', 'rode node ../../motor/build.mjs antes de checar');
const out = ex('build-out.json') ? rd('build-out.json') : null;

// 1. duração e planos
if (out) {
  const T = out.total;
  add(T >= 61 ? (T >= 70 && T <= 85 ? 'OK' : 'AVISO') : 'FALHA', 'Duração', `${T.toFixed(1)} s (monetização no TikTok: acima de 61 s; faixa do canal: 70–85 s)`);
  const sp = out.shots.filter((s) => !s.silent), long = sp.filter((s) => s.dur > 3.0);
  const longSemPunch = long.length; // planos >2 s recebem punch extra no meio; só registramos
  add('OK', 'Planos', `${out.shots.length} planos; ${long.length} acima de 3,0 s (recebem aproximação extra no meio); maior: ${Math.max(...out.shots.map((s) => s.dur)).toFixed(2)} s`);
  const maxLong = Math.max(0, ...out.shots.filter((s) => !s.hold).map((s) => s.dur));
  if (maxLong > 3.6) add('AVISO', 'Plano muito longo', `${maxLong.toFixed(2)} s: dividir em dois planos`);
  const curtos = out.shots.filter((s) => s.dur < 0.8 && !s.silent);
  if (curtos.length) add('AVISO', 'Planos curtos', `${curtos.map((s) => s.id).join(', ')} (< 0,8 s)`);
  // texto na tela: até 4 palavras por sobreposição
  const exc = [];
  for (const s of out.shots) for (const ov of (s.o.ov || [])) if (ov.text.trim().split(/\s+/).length > 4) exc.push(`${s.id}: "${ov.text}"`);
  add(exc.length ? 'AVISO' : 'OK', 'Texto na tela', exc.length ? `mais de 4 palavras: ${exc.join('; ')}` : 'todas as sobreposições com até 4 palavras');
  // ritmo da fala
  const words = data.shots.filter((s) => !s.silent).reduce((a, s) => a + s.t.trim().split(/\s+/).length, 0);
  const speech = out.beats.length ? out.shots.filter((s) => !s.silent).reduce((a, s) => a + s.dur, 0) : 0;
  add('OK', 'Ritmo da fala', `${words} palavras em ${speech.toFixed(0)} s de planos falados (${(words / speech).toFixed(2)} palavras/s)`);
}

// 2. voz
const faltam = [];
data.beats.forEach((b) => { if (!ex(b.audio)) faltam.push(b.audio); if (!ex(b.audio.replace('assets/voz/', 'assets/voz/proc/'))) faltam.push(b.audio.replace('assets/voz/', 'assets/voz/proc/')); });
add(faltam.length ? 'FALHA' : 'OK', 'Voz', faltam.length ? `faltam: ${faltam.join(', ')}` : `${data.beats.length} beats com voz crua e normalizada`);

// 3. roteiro
const nome = path.basename(DIR);
const rotDir = path.resolve(DIR, '../../roteiros');
const rotFile = fs.existsSync(rotDir) ? fs.readdirSync(rotDir).find((f) => f.startsWith(nome.split('-')[0] + '-')) : null;
if (!rotFile) add('FALHA', 'Roteiro', `sem roteiros/${nome.split('-')[0]}-*.md`);
else {
  const txt = fs.readFileSync(path.join(rotDir, rotFile), 'utf8');
  const tem = (h) => new RegExp('^## .*' + h, 'mi').test(txt);
  add(tem('Decisões') ? 'OK' : 'FALHA', 'Roteiro: decisões', tem('Decisões') ? 'seção "Decisões" presente' : 'falta a seção "Decisões" (hook, ordem, CTA, fecho)');
  add(tem('Conferência de fatos') ? 'OK' : 'FALHA', 'Roteiro: fatos', tem('Conferência de fatos') ? 'seção "Conferência de fatos" presente' : 'falta a seção "Conferência de fatos"');
  const pend = (txt.match(/A confirmar|a confirmar|conferir|pendente/g) || []).length;
  add(pend ? 'AVISO' : 'OK', 'Fontes', pend ? `${pend} marcações de fonte pendente no roteiro (não publicar antes de resolver)` : 'sem pendências de fonte marcadas');
  if (/Fonte: NASA/.test(JSON.stringify(data)) && /NASA/.test(txt) && /(falta|conferir).*NASA|NASA.*(falta|conferir)/i.test(txt)) add('AVISO', 'Fonte na tela', 'o vídeo mostra "Fonte: NASA" mas o roteiro ainda marca a fonte como a conferir');
}

// 4. render mais recente
const rdir = path.join(DIR, 'renders');
const mp4 = fs.existsSync(rdir) ? fs.readdirSync(rdir).filter((f) => f.endsWith('.mp4')).map((f) => ({ f, t: fs.statSync(path.join(rdir, f)).mtimeMs })).sort((a, b) => b.t - a.t)[0] : null;
if (!mp4) add('AVISO', 'Render', 'nenhum renders/*.mp4 ainda');
else {
  const file = path.join(rdir, mp4.f);
  const pr = spawnSync('ffprobe', ['-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate:format=duration', '-of', 'json', file], { encoding: 'utf8' });
  const j = JSON.parse(pr.stdout || '{}'), st = (j.streams || [])[0] || {}, dur = parseFloat((j.format || {}).duration || 0);
  add(st.width === 1080 && st.height === 1920 && st.r_frame_rate === '30/1' ? 'OK' : 'FALHA', `Render ${mp4.f}`, `${st.width}×${st.height}, ${st.r_frame_rate}, ${dur.toFixed(1)} s`);
  if (out && Math.abs(dur - out.total) > 0.8) add('AVISO', 'Render desatualizado?', `render ${dur.toFixed(1)} s ≠ build ${out.total.toFixed(1)} s`);
  const lo = spawnSync('ffmpeg', ['-hide_banner', '-nostats', '-i', file, '-af', 'ebur128=peak=true', '-f', 'null', '-'], { encoding: 'utf8' }).stderr || '';
  const I = parseFloat((lo.match(/\n\s+I:\s+(-?[\d.]+) LUFS/g) || []).pop()?.match(/-?[\d.]+/)?.[0]), P = parseFloat((lo.match(/\n\s+Peak:\s+(-?[\d.]+) dBFS/g) || []).pop()?.match(/-?[\d.]+/)?.[0]);
  add(I >= -16.5 && I <= -11.5 ? 'OK' : 'AVISO', 'Loudness', `${I} LUFS integrado (alvo −16 a −12)`);
  add(P <= -1 ? 'OK' : 'FALHA', 'Pico', `${P} dBFS (limite −1)`);
  const au = spawnSync('ffprobe', ['-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=codec_name', '-of', 'csv=p=0', file], { encoding: 'utf8' }).stdout.trim();
  add(au ? 'OK' : 'FALHA', 'Áudio', au ? `faixa de áudio ${au}` : 'sem faixa de áudio');
}

// 5. hyperframes check (opcional)
if (FULL) {
  const r = spawnSync('npx', ['hyperframes', 'check', '--json'], { cwd: DIR, encoding: 'utf8', maxBuffer: 1 << 28 });
  try {
    const d = JSON.parse(r.stdout);
    const e = ['lint', 'runtime', 'layout', 'motion', 'contrast'].reduce((a, k) => a + ((d[k] || {}).errorCount || 0), 0), w = ['lint', 'runtime', 'layout', 'motion', 'contrast'].reduce((a, k) => a + ((d[k] || {}).warningCount || 0), 0);
    add(e ? 'FALHA' : w ? 'AVISO' : 'OK', 'hyperframes check', `${e} erros, ${w} avisos (contraste: ${(d.contrast || {}).warningCount || 0})`);
  } catch { add('FALHA', 'hyperframes check', 'não consegui ler a saída'); }
} else add('AVISO', 'hyperframes check', 'não rodado (use --full)');

const icon = { OK: '✓', AVISO: '!', FALHA: '✗' };
console.log(`\nChecagem de ${nome}\n`);
for (const [st, n, d] of rows) console.log(` ${icon[st]} ${st.padEnd(5)} ${n.padEnd(26)} ${d}`);
console.log(`\n${fail ? 'REPROVADO' : 'APROVADO'} · ${fail} falhas · ${warn} avisos`);
process.exit(fail ? 1 : 0);
