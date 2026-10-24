// Lista as placas (PNG em camadas) existentes em public/series para o Remotion saber
// quais já foram geradas. Placas que faltam aparecem como rascunho no vídeo.
import {readdirSync, statSync, writeFileSync, mkdirSync} from 'node:fs';
import {join, relative} from 'node:path';

const raiz = new URL('..', import.meta.url).pathname;
const publico = join(raiz, 'public');
const base = join(publico, 'series');

const achados = [];
const varrer = (dir) => {
  for (const nome of readdirSync(dir)) {
    const caminho = join(dir, nome);
    if (statSync(caminho).isDirectory()) varrer(caminho);
    else if (/\.(png|webp|jpg)$/i.test(nome)) achados.push(relative(publico, caminho));
  }
};
varrer(base);

mkdirSync(join(raiz, 'src/gerado'), {recursive: true});
writeFileSync(join(raiz, 'src/gerado/placas.json'), JSON.stringify(achados.sort(), null, 2) + '\n');
console.log(`${achados.length} placa(s) no manifesto.`);
