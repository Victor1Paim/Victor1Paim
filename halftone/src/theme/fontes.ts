import {loadFont} from '@remotion/fonts';
import {staticFile} from 'remotion';

// Fontes locais (public/fonts, licença OFL), para o render não depender de rede.
// Subconjunto latin: cobre todo o português (ç, ã, é…).
const carregar = (family: string, arquivo: string, weight = '400', style = 'normal') =>
  loadFont({family, url: staticFile(`fonts/${arquivo}.woff2`), weight, style, format: 'woff2'});

carregar('Anton', 'anton-latin-400-normal');
carregar('Archivo Black', 'archivo-black-latin-400-normal');
carregar('IBM Plex Mono', 'ibm-plex-mono-latin-400-normal');
carregar('IBM Plex Mono', 'ibm-plex-mono-latin-500-normal', '500');
for (const w of ['400', '600', '700']) carregar('Inter', `inter-latin-${w}-normal`, w);
for (const w of ['400', '600']) carregar('Inter', `inter-latin-${w}-italic`, w, 'italic');

export const fontes = {
  titulo: 'Anton',
  marca: 'Archivo Black',
  mono: 'IBM Plex Mono',
  texto: 'Inter',
  textoItalico: 'Inter',
};
