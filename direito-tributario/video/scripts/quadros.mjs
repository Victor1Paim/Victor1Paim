// Renderiza quadros soltos para conferência: node scripts/quadros.mjs <composição> <pasta> 120 300 ...
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import path from 'node:path';

const [id, pasta, ...frames] = process.argv.slice(2);
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
const composition = await selectComposition({serveUrl, id});
for (const f of frames) {
  await renderStill({composition, serveUrl, frame: Number(f), output: `${pasta}/f${f}.png`, scale: 0.4});
  console.log('ok', f);
}
