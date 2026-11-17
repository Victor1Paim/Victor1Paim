// Capa 9:16 de um corte de live: quadro de fundo + logo + etiqueta + gancho (mesmo estilo das capas do canal).
// Uso: node capa.js <quadro.jpg> '<["LINHA 1","LINHA 2"]>' <destaque> <etiqueta> <saida.jpg>
const {chromium} = require('playwright');
const fs = require('fs');
const path = require('path');
const [quadro, ganchoJson, destaque, etiqueta, saida] = process.argv.slice(2);
const raiz = path.resolve(__dirname, '..');
const fonte = (f) => 'file://' + path.join(raiz, 'modelo', 'public', 'fonts', f);
const logo = fs.readFileSync(path.join(raiz, 'modelo', 'public', 'logo.svg'), 'utf8');
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const linhas = JSON.parse(ganchoJson).map((l) => {
  const e = esc(l);
  return destaque && l.includes(destaque) ? e.replace(esc(destaque), `<span style="color:#ffd23f">${esc(destaque)}</span>`) : e;
});
const maior = Math.max(...JSON.parse(ganchoJson).map((l) => l.length));
const html = `<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{font-family:Anton;src:url(${fonte('anton.woff2')})}
@font-face{font-family:Inter;font-weight:800;src:url(${fonte('inter-800.woff2')})}
*{margin:0;padding:0;box-sizing:border-box} .c{-webkit-text-stroke:14px #000;paint-order:stroke fill}
</style></head><body style="width:1080px;height:1920px;position:relative;overflow:hidden;background:#0d0718">
<img src="file://${path.resolve(quadro)}" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:saturate(1.15) contrast(1.05)">
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(13,7,24,.55) 0%,transparent 28%,transparent 45%,rgba(13,7,24,.92) 82%)"></div>
<div style="position:absolute;top:320px;left:0;right:0;display:flex;justify-content:center;align-items:center;gap:18px">
  <div style="width:92px;height:92px;filter:drop-shadow(0 6px 0 #000)">${logo}</div>
  <div class="c" style="font-family:Anton;font-size:64px;color:#fff;-webkit-text-stroke:7px #000">MODO <span style="color:#ffd23f">REPLAY</span></div></div>
<div style="position:absolute;left:50px;right:50px;top:1040px;text-align:center">
  <div style="display:inline-block;font-family:Anton;font-size:60px;color:#fff;background:#e0242e;padding:8px 28px;border-radius:12px;transform:rotate(-3deg);box-shadow:0 8px 0 #000;margin-bottom:30px">${esc(etiqueta)}</div>
  <div class="c" style="font-family:Anton;font-size:${maior <= 15 ? 150 : 124}px;line-height:1.02;color:#fff">${linhas.join('<br>')}</div>
</div></body></html>`;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({viewport: {width: 1080, height: 1920}});
  const tmp = saida + '.html';
  fs.writeFileSync(tmp, html);
  await p.goto('file://' + path.resolve(tmp));
  await p.evaluate(() => document.fonts.ready);
  await p.screenshot({path: saida, type: 'jpeg', quality: 92});
  await b.close();
  fs.unlinkSync(tmp);
})();
