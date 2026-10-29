// Gera index.html com 3 opções de capa (1080×1920) usando as receitas do motor, na pele Neo-brutalismo.
// Zona segura: todo texto e objeto-chave entre y 340 e 1580 e x 90 a 990, para sobreviver ao corte 4:5 do feed
// do Instagram (y 285–1635) e ao 3:4 da grade de perfil (y 240–1680).
import fs from 'node:fs';
import receitas from '../../../motor/receitas-dinheiro.mjs';
const COL = { amber: '#D90368', mint: '#007A4D', coral: '#B3001B', blue: '#3A86FF', ink: '#111111', soft: '#444444' };
const r3 = (n) => Math.round(n * 1000) / 1000, px = r3;
const fit = (text, size) => Math.min(size, Math.floor(864 / (String(text).length * 0.88)));
const R = receitas({ COL, r3, px, fit });
const t = (txt, y, size, color = COL.ink) => `<div class="t" style="top:${y}px;font-size:${size}px;color:${color}">${txt}</div>`;
const box = (txt, y, size, bg, color = '#111', rot = -3) => `<div class="box" style="top:${y}px;font-size:${size}px;background:${bg};color:${color};transform:translateX(-50%) rotate(${rot}deg)">${txt}</div>`;
const shift = (html, dy, s = 1) => `<div class="abs" style="left:0;top:0;width:1080px;height:1920px;transform:translateY(${dy}px) scale(${s});transform-origin:50% 0">${html}</div>`;

const A = `<div class="bg" style="background:#FFD60A"></div>`
  + t('CADÊ SEU', 360, 118) + t('DINHEIRO?', 500, 118, COL.amber)
  + shift(R.wallet('ca', 0, 1, {}).html, 330)
  + box('NINGUÉM TIROU. SUMIU.', 1400, 62, '#fff');
const B = `<div class="bg" style="background:#FFF3D6"></div>`
  + t('A NOTA DE R$ 100', 360, 92) + t('ENCOLHEU', 480, 136, COL.amber)
  + `<div class="lbl" style="left:70px;top:700px;width:520px">2010</div><div class="lbl" style="left:700px;top:700px;width:300px">HOJE</div>`
  + `<div class="abs" style="left:70px;top:790px;width:520px;height:247px">${R.note('cb1', 0, 1, {}).html.replace('left:140px;top:450px', 'left:0;top:0;width:520px;height:247px').replace('width="800" height="380"', 'width="520" height="247"')}</div>`
  + `<div class="arrow">→</div>`
  + `<div class="abs" style="left:745px;top:865px;width:210px;height:100px">${R.note('cb2', 0, 1, {}).html.replace('left:140px;top:450px', 'left:0;top:0;width:210px;height:100px').replace('width="800" height="380"', 'width="210" height="100"')}</div>`
  + box('COMPRA SÓ ~40%', 1200, 84, COL.coral, '#fff', -4) + t('do que comprava em 2010', 1400, 52, COL.soft);
const C = `<div class="bg" style="background:#B8F2D9"></div>`
  + t('MESMOS R$ 100', 360, 96) + t('MENOS COMPRAS', 480, 88, COL.coral)
  + shift(R.carts('cc', 0, 1, { keep: 4 }).html, 290)
  + box('É A INFLAÇÃO', 1400, 78, '#FFD60A');
const clip = (i, body) => `<div id="capa${i}" class="clip shot" data-start="${i}" data-duration="1" data-track-index="1">${body}</div>`;
const html = `<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
<head><meta charset="UTF-8" /><meta name="viewport" content="width=1080, height=1920" />
<script src="assets/vendor/gsap.min.js"></script>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
html, body { width:1080px; height:1920px; overflow:hidden; background:#FFF3D6; }
#root{position:absolute;inset:0;overflow:hidden;font-family:'Inter',sans-serif;color:#111}
.shot{position:absolute;inset:0;overflow:hidden}.bg{position:absolute;inset:0}.abs{position:absolute}
.obj{filter:drop-shadow(10px 10px 0 #111)}
.t{position:absolute;left:0;width:1080px;text-align:center;font-family:'Archivo Black',sans-serif;line-height:1;white-space:nowrap}
.lbl{position:absolute;text-align:center;font-family:'Archivo Black',sans-serif;font-size:64px;line-height:1;color:#111}
.box{position:absolute;left:50%;white-space:nowrap;font-family:'Archivo Black',sans-serif;line-height:1;border:8px solid #111;box-shadow:12px 12px 0 #111;padding:26px 40px}
.arrow{position:absolute;left:600px;top:850px;width:130px;text-align:center;font-family:'Archivo Black';font-size:110px;line-height:1;color:#111}
#ca-notes{opacity:.5}.cc-gone{opacity:0}
</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="3" data-width="1080" data-height="1920">
${clip(0, A)}
${clip(1, B)}
${clip(2, C)}
</div>
<script>window.__timelines = window.__timelines || {};const tl = gsap.timeline({ paused: true });window.__timelines["main"] = tl;</script>
</body></html>
`;
fs.writeFileSync(new URL('./index.html', import.meta.url), html);
console.log('ok');
