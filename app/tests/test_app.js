// Usage: python3 tools/build_app.py --link && python3 -m http.server -d _site 8000 &
//        node app/tests/test_app.js http://localhost:8000/ [screenshot dir]
// Playwright checks for the listening app.  Usage: node test_app.js <base url> <shots dir>
const { chromium } = require('playwright');
const BASE = process.argv[2] || 'http://localhost:8000/';
const SHOTS = process.argv[3] || '.';
const results = [];
const ok = (name, cond, detail) => { results.push({ name, ok: !!cond, detail }); console.log(`${cond ? 'PASS' : 'FAIL'}  ${name}${detail !== undefined ? '  ' + JSON.stringify(detail) : ''}`); };

(async () => {
  const browser = await chromium.launch();
  const consoleErrors = [];
  const failed = [];
  async function newPage(opts = {}) {
    const ctx = await browser.newContext(Object.assign({ viewport: { width: 390, height: 844 } }, opts));
    const page = await ctx.newPage();
    page.on('console', m => { if (m.type() === 'error') consoleErrors.push(`${page.url()} :: ${m.text()}`); });
    page.on('pageerror', e => consoleErrors.push(`${page.url()} :: pageerror ${e.message}`));
    page.on('requestfailed', r => { const f = r.failure(); if (!f || !/ERR_ABORTED/.test(f.errorText)) failed.push(`${r.url()} ${f && f.errorText}`); });
    page.on('response', r => { if (r.status() >= 400) failed.push(`${r.url()} HTTP ${r.status()}`); });
    return page;
  }
  const noHScroll = async (page) => page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth && document.body.scrollWidth <= window.innerWidth);

  // ---------------- Home ----------------
  let page = await newPage();
  await page.goto(BASE + '#/');
  await page.waitForSelector('.pair-card');
  const home = await page.evaluate(() => {
    const secs = [...document.querySelectorAll('main section')];
    const byTitle = t => secs.find(s => (s.querySelector('h2') || {}).textContent === t);
    const pairs = [...document.querySelectorAll('.pair-card')];
    return {
      pairs: pairs.length,
      romans: pairs.map(c => c.querySelector('.roman').textContent).join(' '),
      appendix: byTitle('Appendix') ? byTitle('Appendix').querySelectorAll('.card').length : 0,
      extras: byTitle('Extras') ? byTitle('Extras').querySelectorAll('.card').length : 0,
      firstCard: pairs[0].innerText.replace(/\s+/g, ' '),
      picks: document.querySelectorAll('.picks li').length,
      guideLink: !!document.querySelector('a[href="#/guide/half-hour"]'),
    };
  });
  ok('home lists 24 pairs in WTC order', home.pairs === 24 && home.romans.startsWith('I II III IV V') && home.romans.endsWith('XXIII XXIV'), home.romans);
  ok('home lists the appendix (3 pieces)', home.appendix === 3, home.appendix);
  ok('home lists the extras (Möbius)', home.extras >= 1, home.extras);
  ok('pair card shows key, voices, duration, concept', /C major/.test(home.firstCard) && /Fugue à 2/.test(home.firstCard) && /\d:\d\d/.test(home.firstCard) && /endless rise/.test(home.firstCard), home.firstCard);
  ok('home has the half-hour picks and a link to the guide', home.picks === 5 && home.guideLink, home);
  ok('home: no horizontal scroll at 390x844', await noHScroll(page));
  await page.screenshot({ path: `${SHOTS}/t-home-390.png` });

  // Deep link + back/forward
  await page.click('.pair-card a.card-link >> nth=1');
  await page.waitForSelector('.piece-head h1');
  const h1a = await page.textContent('.piece-head h1');
  ok('card opens the pair page (#/pair/2)', page.url().endsWith('#/pair/2') && /Prelude II/.test(h1a), page.url());
  await page.click('.tabs a:has-text("Fugue")');
  await page.waitForFunction(() => location.hash === '#/pair/2/fugue' && /Fugue II/.test(document.querySelector('.piece-head h1').textContent));
  await page.goBack();
  await page.waitForFunction(() => location.hash === '#/pair/2' && /Prelude II/.test(document.querySelector('.piece-head h1').textContent));
  await page.goBack();
  await page.waitForSelector('.pair-card');
  ok('back/forward navigation works', page.url().endsWith('#/'), page.url());
  await page.goForward();
  await page.waitForFunction(() => location.hash === '#/pair/2');
  ok('forward goes to the pair again', true);

  // ---------------- Piece page: MP3 + strip + playhead ----------------
  await page.goto(BASE + '#/pair/15/fugue');
  await page.waitForSelector('.score-frame .tile');
  const a0 = await (await page.waitForFunction(() => { const a = document.getElementById('audio'); return a.duration > 0 && a.seekable.length && a.seekable.end(0) > 100 ? { dur: a.duration, src: a.currentSrc } : null; }, null, { timeout: 15000 })).jsonValue();
  ok('piece page loads its MP3 (audio has a duration)', a0.dur > 100, a0);
  await page.waitForFunction(() => [...document.querySelectorAll('.tile')].some(i => i.complete && i.naturalWidth > 0));
  const strip0 = await page.evaluate(() => ({ tr: document.querySelector('.strip-track').style.transform, n: document.querySelectorAll('.tile').length, labels: document.querySelectorAll('.entry-label').length, visible: getComputedStyle(document.querySelector('.strip-track')).display !== 'none' }));
  ok('engraved strip shows, with subject-entry labels', strip0.visible && strip0.n > 0 && strip0.labels > 10, strip0);
  // Wait until the media is seekable (on a server without Range support the app swaps in a Blob).
  await page.waitForFunction(() => { const a = document.getElementById('audio'); return a.seekable.length && a.seekable.end(0) > 100 && a.readyState >= 1; }, null, { timeout: 15000 });
  await page.evaluate(() => { document.getElementById('audio').currentTime = 60; });
  await page.waitForFunction(() => /bar 19 · 1:00/.test(document.querySelector('.clock').textContent), null, { timeout: 10000 }).catch(() => {});
  await page.waitForTimeout(300);
  const strip1 = await page.evaluate(() => ({ tr: document.querySelector('.strip-track').style.transform, clock: document.querySelector('.clock').textContent, ct: document.getElementById('audio').currentTime }));
  const tx = parseFloat((strip1.tr.match(/translate3d\(([-\d.]+)px/) || [])[1]);
  ok('playhead/strip moves when currentTime is set (expected tx -8700.6 at 60 s)', Math.abs(tx - (-8700.6)) < 1.5 && /bar 19/.test(strip1.clock), strip1);
  await page.waitForFunction(() => [...document.querySelectorAll('.tile')].every(i => i.complete && i.naturalWidth > 0));
  await page.screenshot({ path: `${SHOTS}/t-piece-390-60s.png` });
  ok('piece page: no horizontal scroll at 390x844', await noHScroll(page));

  // Media Session metadata
  const ms = await page.evaluate(() => navigator.mediaSession && navigator.mediaSession.metadata ? { title: navigator.mediaSession.metadata.title, album: navigator.mediaSession.metadata.album } : null);
  ok('Media Session metadata set', ms && /Fugue XV/.test(ms.title), ms);

  // Play / pause with keyboard; position remembered.
  await page.click('h1');
  await page.keyboard.press('Space');
  await page.waitForFunction(() => !document.getElementById('audio').paused, null, { timeout: 5000 }).catch(() => {});
  const playing = await page.evaluate(() => !document.getElementById('audio').paused);
  ok('Space starts playback', playing);
  await page.waitForTimeout(1200);
  await page.keyboard.press('ArrowRight');
  await page.waitForTimeout(200);
  const ctAfter = await page.evaluate(() => document.getElementById('audio').currentTime);
  ok('ArrowRight seeks forward 5 s', ctAfter > 65.5 && ctAfter < 68.5, ctAfter);
  await page.keyboard.press('Space');
  await page.waitForTimeout(200);
  const paused = await page.evaluate(() => document.getElementById('audio').paused);
  ok('Space pauses', paused);
  const saved = await page.evaluate(() => localStorage.getItem('wtc:pos:fugue-15:current'));
  await page.reload();
  await page.waitForFunction(() => document.getElementById('audio').readyState >= 1);
  await page.waitForTimeout(500);
  const restored = await page.evaluate(() => ({ ct: document.getElementById('audio').currentTime, status: document.querySelector('.status').textContent }));
  ok('position remembered per piece (localStorage)', saved && Math.abs(restored.ct - parseFloat(saved)) < 1 && /Resuming/.test(restored.status), { saved, restored });

  // Source switch to binaural keeps the position.
  await page.click('[data-src="binaural"]');
  await page.waitForFunction(() => /fugue-spatial\.mp3|^blob:/.test(document.getElementById('audio').src));
  await page.waitForTimeout(800);
  const sw = await page.evaluate(() => ({ ct: document.getElementById('audio').currentTime, hint: document.querySelector('.hint').textContent, paused: document.getElementById('audio').paused }));
  ok('switching to the binaural render keeps the position and shows the headphones hint', Math.abs(sw.ct - restored.ct) < 2 && /headphones/i.test(sw.hint), sw);
  await page.evaluate(() => document.getElementById('audio').pause());

  // ---------------- Live synth ----------------
  const errsBefore = consoleErrors.length;
  await page.click('[data-src="synth"]');
  await page.waitForSelector('.synth-panel:not([hidden])');
  await page.click('.player-panel .play-btn');
  await page.waitForTimeout(400);
  const c1 = await page.textContent('.clock');
  await page.waitForTimeout(1500);
  const c2 = await page.textContent('.clock');
  const synth = await page.evaluate(() => ({ voices: document.querySelectorAll('.voice').length, temps: document.querySelectorAll('[data-temp]').length, label: document.querySelector('.play-btn').getAttribute('aria-label') }));
  ok('live synth starts and advances, voices and temperaments shown', c1 !== c2 && synth.voices === 4 && synth.temps === 6 && synth.label === 'Pause', { c1, c2, synth });
  await page.click('[data-voice="0"]');
  await page.click('[data-temp="meantone"]');
  await page.waitForTimeout(300);
  await page.screenshot({ path: `${SHOTS}/t-synth-390.png`, fullPage: true });
  await page.click('.player-panel .play-btn');
  ok('live synth: no console errors', consoleErrors.length === errsBefore, consoleErrors.slice(errsBefore));
  await page.click('[data-src="piano"]');

  // ---------------- Queue: prelude -> fugue ----------------
  await page.goto(BASE + '#/pair/4/prelude');
  await page.waitForFunction(() => document.getElementById('audio').readyState >= 1);
  await page.click('[data-queue="pair"]');
  await page.click('.player-panel .play-btn');
  await page.waitForFunction(() => !document.getElementById('audio').paused);
  await page.evaluate(() => { const a = document.getElementById('audio'); a.currentTime = a.duration - 0.6; });
  const advanced = await page.waitForFunction(() => location.hash === '#/pair/4/fugue' && /fugue\.mp3|^blob:/.test(document.getElementById('audio').src) && !document.getElementById('audio').paused, null, { timeout: 15000 }).then(() => true).catch(() => false);
  ok('play-through: prelude continues into the fugue automatically', advanced, await page.evaluate(() => ({ hash: location.hash, src: document.getElementById('audio').src })));
  await page.evaluate(() => document.getElementById('audio').pause());

  // ---------------- Earlier version ----------------
  await page.goto(BASE + '#/pair/15/fugue?v=earlier');
  await page.waitForFunction(() => /archive-n-plus-1|^blob:/.test(document.getElementById('audio').src) && document.getElementById('audio').readyState >= 1, null, { timeout: 15000 }).catch(() => {});
  const early = await page.evaluate(() => ({ src: document.getElementById('audio').src, roll: !document.querySelector('canvas.roll').hidden, about: document.querySelector('.about h2').textContent, srcs: [...document.querySelectorAll('[data-src]')].map(b => b.textContent) }));
  ok('earlier version: its MP3s, piano roll and notes', early.roll && /earlier/.test(early.about) && early.srcs.length >= 3, early);
  await page.waitForTimeout(400);
  await page.screenshot({ path: `${SHOTS}/t-earlier-390.png` });

  // ---------------- Möbius ----------------
  await page.goto(BASE + '#/extras/mobius');
  await page.waitForSelector('video');
  const vid = await page.evaluate(() => new Promise(res => {
    const v = document.querySelector('video');
    const done = () => res({ readyState: v.readyState, duration: v.duration, error: v.error && v.error.code, w: v.videoWidth, h: v.videoHeight });
    if (v.readyState >= 1) return done();
    v.addEventListener('loadedmetadata', done); v.addEventListener('error', done); setTimeout(done, 15000);
  }));
  ok('Möbius video element loads (metadata)', vid.readyState >= 1 && vid.duration > 100, vid);
  const mob = await page.evaluate(() => ({ src: document.getElementById('audio').src, chosen: (document.querySelector('[data-src][aria-checked="true"]') || {}).textContent, map: (() => { const i = document.querySelector('img.figure'); return i && i.complete && i.naturalWidth; })(), strip: document.querySelectorAll('.tile').length }));
  ok('Möbius: walking render is the default, walk map and strip shown', /Walking/.test(mob.chosen) && mob.strip > 0, mob);
  ok('Möbius: no horizontal scroll at 390x844', await noHScroll(page));
  await page.screenshot({ path: `${SHOTS}/t-mobius-390.png`, fullPage: true });

  // ---------------- No horizontal scroll on every page ----------------
  const routes = ['#/', '#/guide', '#/appendix/contrapunctus-permutationum', '#/appendix/table-canon', '#/pair/24/fugue', '#/pair/1/prelude', '#/pair/9/prelude-tempered', '#/pair/23/fugue', '#/pair/20/fugue?v=earlier', '#/pair/7/fugue?v=earlier', '#/nope'];
  const wide = [];
  for (const r of routes) {
    await page.goto(BASE + r);
    await page.waitForTimeout(700);
    if (!(await noHScroll(page))) wide.push(r);
  }
  // Open every details element on a piece page (notes rendered from Markdown with tables).
  await page.goto(BASE + '#/pair/23/fugue');
  await page.waitForSelector('.fullnotes');
  await page.evaluate(() => document.querySelectorAll('details').forEach(d => { d.open = true; }));
  await page.waitForTimeout(800);
  if (!(await noHScroll(page))) wide.push('#/pair/23/fugue (notes open)');
  await page.goto(BASE + '#/guide');
  await page.waitForSelector('.guide table');
  if (!(await noHScroll(page))) wide.push('#/guide (loaded)');
  await page.screenshot({ path: `${SHOTS}/t-guide-390.png` });
  ok('no horizontal scroll at 390x844 on any page', wide.length === 0, wide);

  // Every pair page loads its strip (no missing strips).
  const missing = [];
  for (let n = 1; n <= 24; n++) for (const m of ['prelude', 'fugue']) {
    await page.goto(BASE + `#/pair/${n}/${m}`);
    const has = await page.waitForSelector('.score-frame .tile', { timeout: 8000 }).then(() => true).catch(() => false);
    if (!has) missing.push(`${n}/${m}`);
  }
  ok('every movement shows its engraved strip', missing.length === 0, missing);

  // ---------------- Desktop, dark ----------------
  const dpage = await newPage({ viewport: { width: 1280, height: 860 }, colorScheme: 'dark' });
  await dpage.goto(BASE + '#/pair/24/fugue');
  await dpage.waitForSelector('.score-frame .tile');
  await dpage.waitForFunction(() => { const a = document.getElementById('audio'); return a.seekable.length && a.seekable.end(0) > 100 && a.readyState >= 1; }, null, { timeout: 15000 });
  await dpage.evaluate(() => { document.getElementById('audio').currentTime = 150; });
  await dpage.waitForTimeout(1200);
  await dpage.screenshot({ path: `${SHOTS}/t-fugue24-desktop-dark.png` });
  await dpage.goto(BASE + '#/');
  await dpage.waitForSelector('.pair-card');
  await dpage.screenshot({ path: `${SHOTS}/t-home-desktop-dark.png`, fullPage: true });

  ok('no console errors anywhere', consoleErrors.length === 0, consoleErrors);
  ok('no failed requests', failed.length === 0, failed);
  await browser.close();
  const bad = results.filter(r => !r.ok);
  console.log(`\n${results.length - bad.length}/${results.length} checks passed`);
  process.exit(bad.length ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
