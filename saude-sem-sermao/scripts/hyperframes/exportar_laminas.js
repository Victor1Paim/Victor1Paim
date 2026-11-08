const { chromium } = require('playwright');
(async () => {
  const dir = process.argv[2];
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1400 } });
  await p.goto('file://' + dir + '/carrossel.html', { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const s = await p.$$('section.s');
  for (let i = 0; i < s.length; i++) {
    await s[i].screenshot({ path: `${dir}/lamina-${String(i + 1).padStart(2, '0')}.png` });
  }
  console.log(dir.split('/').pop(), s.length, 'lâminas exportadas');
  await b.close();
})();
