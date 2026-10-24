// Checklist automático de um ep.json (plano-mestre 10.4 e bíblia, seção 2).
// Uso: npm run checar -- series/ano-zero/t1/ep01/ep.json
import {readFileSync} from 'node:fs';

const arquivo = process.argv[2];
if (!arquivo) {
  console.error('Uso: npm run checar -- caminho/do/ep.json');
  process.exit(1);
}
const ep = JSON.parse(readFileSync(arquivo, 'utf8'));
const avisos = [];
const ok = [];
const palavras = (t) => t.split(/\s+/).filter((p) => /[\p{L}\d]/u.test(p)).length;

const conta = {narrador: 0, pensamento: 0, dialogo: 0, libras: 0};
for (const c of ep.cenas) {
  for (const l of c.legendas ?? []) if (l.tipo in conta) conta[l.tipo] += palavras(l.texto);
}
const total = conta.narrador + conta.pensamento + conta.dialogo + conta.libras;
const teste = ep.episodio === 0;

const faixa = (nome, v, min, max) => (v < min || v > max ? avisos : ok).push(`${nome}: ${v} (meta ${min}–${max})`);
if (!teste) {
  faixa('Duração (s)', ep.duracaoAlvoSeg, 65, 80);
  faixa('Palavras no total', total, 125, 160);
  faixa('Narrador', conta.narrador, 25, 40);
  faixa('Pensamentos', conta.pensamento, 20, 35);
  faixa('Diálogos + Libras', conta.dialogo + conta.libras, 60, 85);
}

const gancho = ep.cenas.find((c) => c.inicio === 0);
(gancho?.beat === 'gancho' && gancho.fim <= 3.5 ? ok : avisos).push('Gancho em 0–3 s');
((ep.apresentaEm ?? 3) >= 3 ? ok : avisos).push('"Halftone apresenta" depois do gancho');

const ordenadas = [...ep.cenas].sort((a, b) => a.inicio - b.inicio);
for (let i = 1; i < ordenadas.length; i++) {
  if (ordenadas[i].inicio < ordenadas[i - 1].fim) avisos.push(`Cenas sobrepostas: ${ordenadas[i - 1].id} e ${ordenadas[i].id}`);
}
const ultima = ordenadas.at(-1);
if (ultima.fim > ep.duracaoAlvoSeg - 2.5) avisos.push(`Cena ${ultima.id} invade o CTA final (últimos 2,5 s)`);

for (const c of ep.cenas) {
  const dur = c.fim - c.inicio;
  const ls = (c.legendas ?? []).map((l) => ({...l, i: l.inicio ?? 0, f: l.fim ?? dur})).sort((a, b) => a.i - b.i);
  for (let k = 1; k < ls.length; k++) if (ls[k].i < ls[k - 1].f) avisos.push(`Legendas sobrepostas na cena ${c.id}`);
  for (const l of ls) {
    const seg = l.f - l.i;
    const ritmo = palavras(l.texto) / seg;
    if (ritmo > 3.2) avisos.push(`Legenda rápida demais (${ritmo.toFixed(1)} palavras/s) em ${c.id}: "${l.texto}"`);
  }
}

const md = ep.momentoDecisao;
if (md) {
  const d = md.duracao ?? 2;
  (d >= 1.5 && d <= 2 ? ok : avisos).push(`Momento Decisão congela ${d} s (meta 1,5–2)`);
}

console.log(`\n${arquivo} — Ep. ${ep.episodio} "${ep.titulo}"`);
console.log(`Palavras: narrador ${conta.narrador} · pensamentos ${conta.pensamento} · diálogos ${conta.dialogo} · Libras ${conta.libras} · total ${total}\n`);
for (const o of ok) console.log(`  ✓ ${o}`);
for (const a of avisos) console.log(`  ✗ ${a}`);
console.log('\nManual: selo FICÇÃO e rótulo de IA · Libras revisada · capa · legenda e hashtags · comentário fixado.');
process.exitCode = avisos.length ? 1 : 0;
