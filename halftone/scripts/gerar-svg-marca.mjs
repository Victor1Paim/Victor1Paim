// Gera marca/avatar.svg, marca/avatar-simplificado.svg e marca/logo.svg a partir da mesma
// geometria usada nos vídeos. O logo embute a Archivo Black (OFL) para abrir igual em qualquer lugar.
// Requer Node 22.18+ (lê .ts direto).
import {readFileSync, writeFileSync} from 'node:fs';
import {PONTO_VERMELHO, pontosSimbolo, raioVermelho} from '../marca/simbolo.ts';

const raiz = new URL('..', import.meta.url).pathname;
const cores = {preto: '#07090D', papel: '#EDE6D6', vermelho: '#E0413A'};
const n = (v) => +v.toFixed(4);

const simbolo = (simplificado) =>
  pontosSimbolo(simplificado).map((p) => `<circle cx="${n(p.x)}" cy="${n(p.y)}" r="${n(p.r)}"/>`).join('') +
  `<circle cx="${PONTO_VERMELHO.x}" cy="${PONTO_VERMELHO.y}" r="${raioVermelho(simplificado)}" fill="${cores.vermelho}"/>`;

const avatar = (simplificado) =>
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="-1.25 -1.25 2.5 2.5" width="1080" height="1080">` +
  `<rect x="-1.25" y="-1.25" width="2.5" height="2.5" fill="${cores.preto}"/>` +
  `<g fill="${cores.papel}">${simbolo(simplificado)}</g></svg>\n`;

writeFileSync(`${raiz}marca/avatar.svg`, avatar(false));
writeFileSync(`${raiz}marca/avatar-simplificado.svg`, avatar(true));

const fonte = readFileSync(`${raiz}public/fonts/archivo-black-latin-400-normal.woff2`).toString('base64');
const logo =
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 300" width="1600" height="300">` +
  `<style>@font-face{font-family:'Archivo Black';src:url(data:font/woff2;base64,${fonte}) format('woff2')}` +
  `text{font-family:'Archivo Black',sans-serif;font-size:190px;fill:${cores.papel}}</style>` +
  `<rect width="1600" height="300" fill="${cores.preto}"/>` +
  `<g transform="translate(150 150) scale(115)" fill="${cores.papel}">${simbolo(true)}</g>` +
  `<text x="310" y="222">HALFT</text>` +
  `<circle cx="1038" cy="152" r="70" fill="${cores.vermelho}"/>` +
  `<text x="1122" y="222">NE</text></svg>\n`;
writeFileSync(`${raiz}marca/logo.svg`, logo);
console.log('marca/avatar.svg, marca/avatar-simplificado.svg e marca/logo.svg gerados.');
