// Gera index.html com 3 opções de capa (1080×1920) do 003 na pele Isométrico, usando as receitas do motor.
// Zona segura: texto e objeto-chave entre y 340 e 1580 e x 90 a 990 (corte 4:5 do feed: y 285–1635; grade 3:4: y 240–1680).
import fs from 'node:fs';
import saude from '../../../motor/receitas-saude.mjs';
const COL = { amber: '#FFC857', mint: '#7CFFCB', coral: '#FF6B6B', blue: '#2DD4BF', ink: '#F2FBFF', soft: '#9CC9C9' };
const r3 = (n) => Math.round(n * 1000) / 1000, px = r3;
const R = saude({ COL, r3, px });
const t = (txt, y, size, color = COL.ink) => `<div class="t" style="top:${y}px;font-size:${size}px;color:${color}">${txt}</div>`;
const box = (txt, y, size, bg, color = '#0A1F26', rot = -3) => `<div class="box" style="top:${y}px;font-size:${size}px;background:${bg};color:${color};transform:translateX(-50%) rotate(${rot}deg)">${txt}</div>`;
const place = (html, dx, dy, s = 1) => `<div class="abs" style="left:0;top:0;width:1080px;height:1920px;transform:translate(${dx}px,${dy}px) scale(${s});transform-origin:50% 0">${html}</div>`;
const BG = `<div class="bg"></div>`;
const A = BG + t('O LAGARTO', 360, 130) + t('POR TRÁS DO', 500, 96, COL.soft) + t('OZEMPIC', 610, 150, COL.amber)
  + place(R.lizard('ca', 0, 1, { venom: true }).html, 0, 330) + box('1992', 1400, 90, COL.amber);
const B = BG + t('OZEMPIC TEM', 360, 120) + t('VENENO?', 500, 160, COL.coral)
  + place(R.lizard('cb', 0, 1, { cross: true }).html, 0, 300) + box('NÃO É BEM ASSIM', 1380, 78, COL.mint);
const C = BG + t('DO VENENO', 360, 128, COL.amber) + t('À CANETA', 500, 128)
  + place(R.lizard('cc', 0, 1, { venom: true }).html, -230, 560, 0.5) + place(R.pen('cp', 0, 1, {}).html, 250, 620, 0.5)
  + `<div class="arrow">→</div>` + box('A ORIGEM DO OZEMPIC', 1400, 56, COL.amber);
const clip = (i, body) => `<div id="capa${i}" class="clip shot" data-start="${i}" data-duration="1" data-track-index="1">${body}</div>`;
fs.writeFileSync(new URL('./index.html', import.meta.url), `<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<script src="assets/vendor/gsap.min.js"></script>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:1080px; height:1920px; overflow:hidden; background:#051217; }
#root{position:absolute;inset:0;overflow:hidden;font-family:'Inter',sans-serif;color:#F2FBFF}
.shot{position:absolute;inset:0;overflow:hidden}.abs{position:absolute}
.bg{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 30%,#12383F 0%,#0A1F26 62%,#051217 100%)}
.bg::after{content:'';position:absolute;inset:0;background:repeating-linear-gradient(30deg,rgba(242,251,255,.07) 0 2px,transparent 2px 72px),repeating-linear-gradient(150deg,rgba(242,251,255,.07) 0 2px,transparent 2px 72px)}
.obj{filter:drop-shadow(14px 10px 0 rgba(0,0,0,.38))}
.t{position:absolute;left:0;width:1080px;text-align:center;font-family:'Archivo Black',sans-serif;line-height:1;white-space:nowrap;text-shadow:0 6px 24px rgba(0,0,0,.6)}
.box{position:absolute;left:50%;white-space:nowrap;font-family:'Archivo Black',sans-serif;line-height:1;border-radius:18px;box-shadow:12px 10px 0 rgba(0,0,0,.4);padding:26px 40px}
.arrow{position:absolute;left:470px;top:840px;width:140px;text-align:center;font-family:'Archivo Black';font-size:110px;line-height:1;color:#F2FBFF}
</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="3" data-width="1080" data-height="1920">
${clip(0, A)}
${clip(1, B)}
${clip(2, C)}
</div>
<script>window.__timelines = window.__timelines || {};const tl = gsap.timeline({ paused: true });window.__timelines["main"] = tl;</script>
</body></html>
`);
console.log('ok');
