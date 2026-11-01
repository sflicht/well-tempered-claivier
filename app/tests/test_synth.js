// Usage (with the site served as for test_app.js):
//        node app/tests/test_synth.js http://localhost:8000/ app/tests/synth_expect.json
// End-to-end check of the live synth: gates, per-note tuning and note chasing, against values
// computed in Python from render_music.py's rules (synth_expect.json).
const { chromium } = require('playwright');
const fs = require('fs');
const BASE = process.argv[2], X = JSON.parse(fs.readFileSync(process.argv[3]));
const results = [];
const ok = (n, c, d) => { results.push(!!c); console.log(`${c ? 'PASS' : 'FAIL'}  ${n}  ${JSON.stringify(d)}`); };
const midi = hz => 69 + 12 * Math.log2(hz / 440);
(async () => {
  const browser = await chromium.launch();
  const errors = [];
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 } });
  await ctx.addInitScript(() => {
    window.__osc = [];
    const orig = AudioContext.prototype.createOscillator;
    AudioContext.prototype.createOscillator = function () {
      const o = orig.call(this), rec = {}, st = o.start.bind(o), sp = o.stop.bind(o);
      o.start = w => { rec.when = w; rec.hz = o.frequency.value; window.__osc.push(rec); return st(w); };
      o.stop = w => { rec.stop = w; return sp(w); };
      return o;
    };
  });
  const page = await ctx.newPage();
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  page.on('pageerror', e => errors.push(e.message));
  async function playAt(route, t, waitMs, reload) {
    await page.goto(BASE + `#/${route}?src=synth&t=${t}`);
    if (reload) await page.reload();
    await page.waitForSelector('[data-src="synth"][aria-checked="true"]');
    await page.waitForTimeout(300);
    await page.evaluate(() => { window.__osc = []; });
    await page.click('.player-panel .play-btn');
    await page.waitForTimeout(waitMs);
    const osc = await page.evaluate(() => window.__osc.map(o => ({ when: o.when, hz: o.hz, dur: o.stop - 0.6 - o.when })));
    await page.click('.player-panel .play-btn');
    return osc;
  }
  // 1. Chase (Fugue VIII at quarter 87)
  let osc = await playAt('pair/8/fugue', X.chase.t, 400);
  const t0 = Math.min(...osc.map(o => o.when));
  const first = osc.filter(o => Math.abs(o.when - t0) < 1e-6);
  for (const n of X.chase.notes) {
    const hit = first.find(o => Math.abs(midi(o.hz) - n.p) < 0.3 && Math.abs(o.dur - n.remaining) < 0.01);
    ok(`chase: MIDI ${n.p} (onset ${n.onset}, length ${n.len}) starts at once for its remaining ${n.remaining.toFixed(3)} s`, hit, hit || first.map(o => [midi(o.hz).toFixed(2), o.dur.toFixed(3)]));
  }
  // 2. Gate (Fugue VII, bar 26: gate .55)
  osc = await playAt('pair/7/fugue', X.gate.t, 900);
  const g0 = Math.min(...osc.map(o => o.when));
  const g = osc.find(o => Math.abs(midi(o.hz) - X.gate.p) < 0.3 && Math.abs(o.when - g0 - X.gate.onset_sec_after) < 0.01);
  ok(`gate: the .55-gated B♭5 at quarter 100 lasts ${X.gate.dur.toFixed(3)} s (not ${X.gate.nominal_dur_097.toFixed(3)})`, g && Math.abs(g.dur - X.gate.dur) < 0.005, g);
  // 3. Per-note tuning (Fugue XXI, Bach-Lehman selected): tagged = ET + cents, untagged = Bach-Lehman
  osc = await playAt('pair/21/fugue', X.tuning.t, 800);
  for (const n of X.tuning.notes) {
    const hit = osc.find(o => Math.abs(o.hz - n.hz) < 0.02);
    ok(`tuning: XXI quarter ${X.tuning.onset}, MIDI ${n.p} ${n.tagged ? 'tagged (ET + cents)' : 'untagged (Bach-Lehman)'} at ${n.hz.toFixed(3)} Hz`, hit, hit || osc.filter(o => Math.abs(midi(o.hz) - n.p) < 0.5).map(o => o.hz));
  }
  // 4. Prelude IX: an explicit cents 0 stays at equal temperament under Bach-Lehman
  await page.evaluate(() => localStorage.setItem('wtc:temp', JSON.stringify('meantone')));
  osc = await playAt('pair/9/prelude', X.ix_zero.t, 500, true);
  const sel = await page.getAttribute('[data-temp][aria-pressed="true"]', 'data-temp');
  ok('meantone is the selected temperament for the next check', sel === 'meantone', sel);
  const z = osc.find(o => Math.abs(midi(o.hz) - X.ix_zero.p) < 0.3);
  ok(`Prelude IX (meantone selected): explicit cents 0 on MIDI ${X.ix_zero.p} sounds at ET ${X.ix_zero.hz_et.toFixed(3)} Hz, not meantone ${X.ix_zero.hz_mt.toFixed(3)}`, z && Math.abs(z.hz - X.ix_zero.hz_et) < 0.02, z);
  await page.evaluate(() => localStorage.setItem('wtc:temp', JSON.stringify('bach-lehman')));
  // 5. Temperament change while playing chases the sounding notes
  await page.goto(BASE + `#/pair/8/fugue?src=synth&t=${X.chase.t}`);
  await page.waitForSelector('[data-src="synth"][aria-checked="true"]');
  await page.click('.player-panel .play-btn');
  await page.waitForTimeout(200);
  await page.evaluate(() => { window.__osc = []; });
  await page.click('[data-temp="meantone"]');
  await page.waitForTimeout(150);
  osc = await page.evaluate(() => window.__osc.map(o => ({ when: o.when, hz: o.hz, dur: o.stop - 0.6 - o.when })));
  const m0 = Math.min(...osc.map(o => o.when));
  const chased = osc.filter(o => Math.abs(o.when - m0) < 1e-6).map(o => Math.round(midi(o.hz)));
  ok('temperament change chases the sounding notes (A♭2 and C♭3 restart in meantone)', chased.includes(44) && chased.includes(47), chased);
  await page.click('.player-panel .play-btn');
  ok('synth checks: no console errors', errors.length === 0, errors);
  await browser.close();
  console.log(`${results.filter(Boolean).length}/${results.length} synth checks passed`);
  process.exit(results.every(Boolean) ? 0 : 1);
})().catch(e => { console.error(e); process.exit(2); });
