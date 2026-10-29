#!/usr/bin/env node
// Cria um vídeo novo: pasta producoes/NNN-slug/ (projeto HyperFrames) e roteiros/NNN-slug.md (a partir do modelo).
// Uso: node desvendando-ideias/motor/novo.mjs 002 geladeira "Como uma geladeira funciona?"
import fs from 'node:fs';
import path from 'node:path';

const [num, slug, ...tit] = process.argv.slice(2);
if (!/^\d{3}$/.test(num || '') || !/^[a-z0-9-]+$/.test(slug || '')) { console.error('uso: novo.mjs NNN slug "Título"   (NNN com 3 dígitos; slug em minúsculas, números e hífens)'); process.exit(1); }
const titulo = tit.join(' ') || slug;
const MOTOR = path.dirname(new URL(import.meta.url).pathname);
const BASE = path.resolve(MOTOR, '..');
const dir = path.join(BASE, 'producoes', `${num}-${slug}`);
const rot = path.join(BASE, 'roteiros', `${num}-${slug}.md`);
if (fs.existsSync(dir) || fs.existsSync(rot)) { console.error('já existe:', fs.existsSync(dir) ? dir : rot); process.exit(1); }
const hoje = new Date().toISOString().slice(0, 10);
fs.mkdirSync(path.join(dir, 'assets/voz'), { recursive: true });
fs.copyFileSync(path.join(MOTOR, 'molde/hyperframes.json'), path.join(dir, 'hyperframes.json'));
fs.writeFileSync(path.join(dir, 'package.json'), fs.readFileSync(path.join(MOTOR, 'molde/package.json'), 'utf8').replace(/"name": "[^"]*"/, `"name": "${num}-${slug}"`));
fs.writeFileSync(path.join(dir, 'meta.json'), fs.readFileSync(path.join(MOTOR, 'molde/meta.json'), 'utf8').replaceAll('__SLUG__', `${num}-${slug}`).replace('__DATA__', new Date().toISOString()));
fs.writeFileSync(path.join(dir, 'shots.json'), JSON.stringify({ titulo: `${num} · ${titulo}`, beats: [{ audio: 'assets/voz/beat0.wav', gap: 0.15 }], shots: [] }, null, 2) + '\n');
fs.writeFileSync(path.join(dir, '.gitignore'), '.hyperframes/\nnode_modules/\nrenders/\nassets/sfx/\n');
fs.writeFileSync(path.join(dir, 'README.md'), `# ${num} · ${titulo}

Roteiro e decisões: \`../../roteiros/${num}-${slug}.md\`. Motor compartilhado: \`../../motor/README.md\`.

\`\`\`sh
../../motor/voz-proc.sh                      # normaliza a voz de assets/voz/ para assets/voz/proc/
node ../../motor/build.mjs                   # gera index.html, compositions/, PLANOS.md e o som
node ../../motor/checar.mjs                  # confere duração, planos, voz, roteiro e (se houver) o render
npx hyperframes render --quality draft -o renders/${num}-${slug}-rascunho1.mp4
\`\`\`
`);
const modelo = fs.readFileSync(path.join(BASE, 'producao/roteiro-modelo.md'), 'utf8');
const corpo = modelo.slice(modelo.indexOf('<!-- MODELO:INICIO -->') + '<!-- MODELO:INICIO -->'.length).replaceAll('NNN', num).replaceAll('__TITULO__', titulo).replaceAll('__SLUG__', slug).replaceAll('__DATA__', hoje);
fs.writeFileSync(rot, corpo.trimStart());
console.log(`criado:\n  ${path.relative(process.cwd(), dir)}/\n  ${path.relative(process.cwd(), rot)}`);
