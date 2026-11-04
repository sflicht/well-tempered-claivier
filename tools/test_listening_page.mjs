// Regression test for the listening room: gates, per-note tuning and chasing on seek/resume.
// It loads the built page headless and compares the player's own schedule (window.clavier, no
// audio) with tools/render_music.py performance_events(), the offline renderer's contract.
//
// Usage: node tools/test_listening_page.mjs [cycle/listening-room.html]
// Needs Node with Playwright (chromium) and python3; exits non-zero on any failure.
import { createRequire } from 'module';
import { spawnSync } from 'child_process';
import { readFileSync } from 'fs';
import { dirname, resolve } from 'path';
import { fileURLToPath, pathToFileURL } from 'url';

const require = createRequire(import.meta.url);
const { chromium } = require('playwright');
const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const PAGE = resolve(process.argv[2] || resolve(ROOT, 'cycle/listening-room.html'));
const TEMPS = ['equal', 'bach-lehman', 'werckmeister3', 'vallotti', 'meantone'];

let failures = 0, checks = 0;
function ok(cond, msg) { checks++; if (!cond) { failures++; console.log('FAIL ' + msg); } }
const near = (a, b, tol) => Math.abs(a - b) <= tol;
const cents = (hz, p) => 1200 * Math.log2(hz / 440) - 100 * (p - 69);

// The offline renderer's version of a movement: per note, voice, onset, performed start/end in
// seconds and the sounding pitch in cents from equal temperament (keyboard tuning + pitch bend).
function oracle(score, temperament) {
  const py = `
import json, sys
sys.path.insert(0, ${JSON.stringify(resolve(ROOT, 'tools'))})
from render_music import voice_channels, performance_events, seconds_at, tempo_points, temperament_offsets, meta_of
data = json.load(open(sys.argv[1])); temp = sys.argv[2]
pts = tempo_points(meta_of(data)); tdev = temperament_offsets(temp)
voice_of = {ch: i for i, chs in enumerate(voice_channels(data)) for ch in chs}
bend, ons, out = {}, {}, []
for t, _, ch, kind, p, v in performance_events(data, temperament=temp):
    if kind == 'bend': bend[ch] = p * 100 / 4096
    elif kind == 'on': ons[ch] = (t, p, bend.get(ch, 0.0))
    elif kind == 'off':
        t0, p0, b = ons.pop(ch)
        out.append([voice_of[ch], round(float(t0), 4), p0, seconds_at(t0, pts), seconds_at(t, pts), tdev[p0 % 12] + b])
print(json.dumps(out))`;
  const r = spawnSync('python3', ['-c', py, resolve(ROOT, score), temperament], { encoding: 'utf8', maxBuffer: 1 << 26 });
  if (r.status !== 0) throw new Error('render_music oracle failed: ' + r.stderr);
  return JSON.parse(r.stdout);
}
const key = (i, t, p) => `${i}|${t.toFixed(4)}|${p}`;

// A stand-in AudioContext that records every oscillator, so the real play()/stop() path can be checked.
const FAKE_AUDIO = () => {
  class Param { constructor(v = 0) { this.value = v; this.ev = []; }
    setValueAtTime(v, t) { this.ev.push(['set', v, t]); } linearRampToValueAtTime(v, t) { this.ev.push(['lin', v, t]); }
    setTargetAtTime(v, t, c) { this.ev.push(['target', v, t, c]); } }
  const node = extra => Object.assign({ connect() {} }, extra);
  class Fake {
    constructor() { this.currentTime = 0; this.state = 'running'; this.sampleRate = 8000; this.destination = {}; this.oscs = []; window.__fakeCtx = this; }
    resume() {} createDynamicsCompressor() { return node({ threshold: new Param(), ratio: new Param() }); }
    createGain() { const g = node({ gain: new Param(1) }); const o = this.oscs[this.oscs.length - 1]; if (o && !o.gainNode) o.gainNode = g; return g; }
    createConvolver() { return node({}); }
    createBuffer(ch, len) { return { getChannelData: () => new Float32Array(len) }; }
    createPeriodicWave() { return {}; } createBiquadFilter() { return node({ frequency: new Param() }); }
    createOscillator() { const c = this, o = node({ frequency: new Param(), stops: [], setPeriodicWave() {},
      start(t) { o.t0 = t; }, stop(t) { o.stops.push(t === undefined ? c.currentTime : t); } }); this.oscs.push(o); return o; }
  }
  window.AudioContext = Fake;
};

const browser = await chromium.launch();
try {
  const page = await browser.newPage();
  const errors = []; page.on('pageerror', e => errors.push(String(e)));
  await page.route(/^https?:/, r => r.abort());  // fonts: the test runs offline
  await page.goto(pathToFileURL(PAGE).href, { waitUntil: 'domcontentloaded' });
  await page.waitForFunction(() => window.clavier);
  const manifest = JSON.parse(readFileSync(resolve(ROOT, 'cycle/listening-manifest.json'), 'utf8'));
  const entries = manifest.groups.flatMap(g => g.pieces);

  // 0. Every movement: each note's gate and cents survive the payload (absent cents stay absent).
  const notesOf = id => page.evaluate(id => window.clavier.prep(window.clavier.pieces.find(p => p.id === id)).map(n => [n.t, n.p, n.g, n.c]), id);
  for (const e of entries) {
    const data = JSON.parse(readFileSync(resolve(ROOT, e.score), 'utf8'));
    const want = data.voices.flatMap(v => v.events).filter(x => x.p != null)
      .map(x => [Math.round(x.t * 1e4) / 1e4, x.p, x.gate ?? 0.97, 'cents' in x ? x.cents : null]);
    const got = await notesOf(e.id);
    // cents travel rounded to 0.01 (below the renderer's 0.024-cent pitch-bend step)
    const s = a => a.map(([t, p, g, c]) => [`${t}|${p}|${g}|${c === null ? '-' : 'c'}`, c]).sort((x, y) => x[0] < y[0] ? -1 : x[0] > y[0] ? 1 : x[1] - y[1]);
    const [w, g] = [s(want), s(got)];
    ok(w.length === g.length && w.every((x, k) => x[0] === g[k][0] && (x[1] === null || near(x[1], g[k][1], 0.0051))), `${e.id}: notes, gates or cents differ from ${e.score}`);
  }

  // Compare one movement's uninterrupted schedule with the offline renderer, note by note.
  async function againstRenderer(id, score, temps, tolCents = 0.02) {
    for (const temp of temps) {
      const ref = new Map(oracle(score, temp).map(r => [key(r[0], r[1], r[2]), r]));
      const got = await page.evaluate(([id, temp]) => window.clavier.schedule(id, 0, { temp }).map(s => [s.n.i, s.n.t, s.n.p, s.start, s.dur, s.hz]), [id, temp]);
      let bad = 0;
      for (const [i, t, p, start, dur, hz] of got) {
        const r = ref.get(key(i, t, p));
        if (!r || !near(start, r[3], 2e-3) || !near(start + dur, r[4], 2e-3) || !near(cents(hz, p), r[5], tolCents)) {
          if (bad++ < 3) console.log('  mismatch', id, temp, { i, t, p, start, dur, cents: cents(hz, p) }, r);
        }
      }
      ok(got.length === ref.size && bad === 0, `${id} (${temp}): ${bad} of ${got.length} notes differ from render_music (${ref.size} notes)`);
    }
  }

  // (a) Gates.  Fugue VII's detached chatter (gate .55, bars 26 and 28) against an ordinary note.
  await againstRenderer('fugue-7', 'cycle/07-e-flat-major/fugue.json', ['bach-lehman']);
  const ref7 = new Map(oracle('cycle/07-e-flat-major/fugue.json', 'bach-lehman').map(r => [key(r[0], r[1], r[2]), r]));
  const s7 = new Map((await page.evaluate(() => window.clavier.schedule('fugue-7', 0).map(s => [s.n.i, s.n.t, s.n.p, s.dur])))
    .map(r => [key(r[0], r[1], r[2]), r[3]]));
  const ev7 = JSON.parse(readFileSync(resolve(ROOT, 'cycle/07-e-flat-major/fugue.json'), 'utf8')).voices
    .flatMap((v, i) => v.events.filter(e => e.p != null).map(e => ({ i, ...e })));
  const short = ev7.filter(e => e.gate === 0.55), plain = ev7.find(e => e.gate === 0.975 && e.d === 1);
  ok(short.length === 38, `fugue-7: expected 38 notes with gate .55 in the score, found ${short.length}`);
  for (const e of [...short, plain]) {
    const k = key(e.i, e.t, e.p), r = ref7.get(k), dur = s7.get(k), want = r[4] - r[3];
    ok(dur !== undefined && near(dur, want, 1e-6), `fugue-7: gate-${e.gate} note at q${e.t} (bar ${e.bar}) lasts ${dur}s; render_music: ${want}s`);
  }
  // A score without gates takes the renderer's default .97.
  const noGate = await page.evaluate(() => window.clavier.prep(window.clavier.pieces.find(p => p.id === 'before-fugue-viii')).every(n => n.g === 0.97));
  ok(noGate, 'before-fugue-viii: notes without a gate should get .97');

  // (b) Chasing.  Fugue VIII from quarter 87 must sound what uninterrupted playback sounds there.
  await againstRenderer('fugue-8', 'cycle/08-e-flat-minor/fugue.json', ['bach-lehman']);
  for (const tempo of [1, 0.7]) {
    const r = await page.evaluate(tempo => {
      const c = window.clavier, P = c.pieces.find(p => p.id === 'fugue-8'), q = 87, s87 = c.secAt(P, q) / tempo;
      const whole = c.schedule('fugue-8', 0, { tempo }), from = c.schedule('fugue-8', q, { tempo });
      const id = x => `${x.n.i}|${x.n.t}|${x.n.p}`;
      // sounding at 87 in the uninterrupted run: started at or before 87, performed end after it
      const want = whole.filter(x => x.start <= s87 + 1e-9 && x.start + x.dur > s87 + 1e-9).map(x => [id(x), x.start + x.dur]);
      const got = from.filter(x => x.start === 0).map(x => [id(x), s87 + x.dur, x.chased, x.n.p, x.dur]);
      return { want, got, s87, ab: c.secAt(P, 86 + 6 * 0.985) / tempo - s87, cb: c.secAt(P, 86 + 2 * 0.975) / tempo - s87 };
    }, tempo);
    const gotMap = new Map(r.got.map(x => [x[0], x]));
    ok(r.want.length === r.got.length && r.want.every(([k, end]) => gotMap.has(k) && near(gotMap.get(k)[1], end, 1e-9)),
      `fugue-8 @87 (tempo ${tempo}): sounding notes ${JSON.stringify(r.want.map(x => x[0]))} vs resumed ${JSON.stringify(r.got.map(x => x[0]))}`);
    const ab = r.got.find(x => x[3] === 44 && x[2]), cb = r.got.find(x => x[3] === 47 && x[2]);
    ok(ab && near(ab[4], r.ab, 1e-9), `fugue-8 @87: Bass A♭2 should be chased for ${r.ab}s, got ${ab && ab[4]}`);
    ok(cb && near(cb[4], r.cb, 1e-9), `fugue-8 @87: Tenor C♭3 should be chased for ${r.cb}s, got ${cb && cb[4]}`);
  }
  // The real player: seek, pause/resume, tempo and temperament changes all chase (stand-in audio).
  await page.evaluate(FAKE_AUDIO);
  const live = await page.evaluate(() => {
    const c = window.clavier, C = () => window.__fakeCtx, $ = id => document.getElementById(id), tempo = $('tempo');
    const at = t => { C().currentTime = t; };  // each restart happens before playback has advanced, so at 87
    const started = () => { const t0 = C().currentTime + 0.08;  // play() starts 80 ms ahead
      return C().oscs.filter(o => Math.abs(o.t0 - t0) < 1e-9).map(o => ({ hz: o.frequency.value, stop: o.stops[0] - t0 - 0.6, lvl: o.gainNode.gain.ev[1][1] })); };
    const out = {};
    c.load('fugue-8'); $('play').click(); at(1); c.seek(87); out.seek = started();              // seek while playing
    $('play').click(); at(5); $('play').click(); out.resume = started(); out.pos = c.state().startPos;  // pause, resume
    at(5.08); tempo.value = 50; tempo.dispatchEvent(new Event('input')); out.tempo = started();  // tempo change
    at(5.16); [...$('temps').children].find(b => b.dataset.k === 'meantone').click(); out.meantone = started();
    $('play').click(); tempo.value = 100; tempo.dispatchEvent(new Event('input'));
    [...$('temps').children].find(b => b.dataset.k === 'bach-lehman').click();
    return out;
  });
  const hzAt = (p, dev) => 440 * Math.pow(2, (p - 69 + dev / 100) / 12);
  const has = (list, p, dev, dur) => list.some(o => near(o.hz, hzAt(p, dev), 1e-6) && (dur === undefined || near(o.stop, Math.max(0.05, dur), 1e-6)));
  const ab1 = 60 * (86 + 6 * 0.985 - 87) / 72, cb1 = 60 * (86 + 2 * 0.975 - 87) / 72;  // bars 22-23: steady 72 bpm
  ok(has(live.seek, 44, 3.91, ab1) && has(live.seek, 47, 0, cb1), 'player: seek to 87 should start A♭2 and C♭3 at once for their remaining durations');
  const abLive = live.seek.find(o => near(o.hz, hzAt(44, 3.91), 1e-6)), abPeak = Math.pow(75 / 127, 1.6) * 0.16;  // synth's peak for v=75
  ok(abLive && abLive.lvl > 0.25 * abPeak && abLive.lvl < 0.99 * abPeak, 'player: a chased note enters at its decayed level, not struck again');
  ok(near(live.pos, 87, 1e-6) && has(live.resume, 44, 3.91, ab1) && has(live.resume, 47, 0, cb1), `player: pause/resume at 87 should chase A♭2 and C♭3 (resumed at ${live.pos})`);
  ok(has(live.tempo, 44, 3.91, ab1 * 2) && has(live.tempo, 47, 0, cb1 * 2), 'player: tempo change should chase at the new tempo');
  ok(has(live.meantone, 44, -17.108) && has(live.meantone, 47, -6.843), 'player: temperament change should chase in the new temperament');

  // (c) Tuning.  Fugue XXI: untagged notes follow the temperament; the natural series (cents from
  // equal temperament) does not, and its B♭ sits at ET +3.91, the Bach–Lehman B♭.
  await againstRenderer('fugue-21', 'cycle/21-b-flat-major/fugue.json', TEMPS);
  const xxi = await page.evaluate(temps => {
    const c = window.clavier, P = c.pieces.find(p => p.id === 'fugue-21'), ns = c.prep(P);
    const plain = ns.find(n => n.p % 12 === 10 && n.c === null), series = ns.find(n => n.p % 12 === 10 && n.c === 3.91);
    return { cr: P.cr, tagged: P.tagged, total: ns.length, rows: temps.map(t => [t, c.centsOf(P, plain, t), c.centsOf(P, series, t)]) };
  }, TEMPS);
  const score21 = JSON.parse(readFileSync(resolve(ROOT, 'cycle/21-b-flat-major/fugue.json'), 'utf8'));
  const notes21 = score21.voices.flatMap(v => v.events.filter(e => e.p != null));
  const tagged21 = notes21.filter(e => 'cents' in e).length, total21 = notes21.length;
  ok(xxi.cr === 'equal' && xxi.tagged === tagged21 && xxi.total === total21, `fugue-21: cents_reference ${xxi.cr}, ${xxi.tagged} of ${xxi.total} tagged (score: ${tagged21} of ${total21})`);
  const dev10 = { 'equal': 0, 'bach-lehman': 3.91, 'werckmeister3': 7.82, 'vallotti': 5.865, 'meantone': 17.108 };
  for (const [t, plain, series] of xxi.rows) {
    ok(near(plain, dev10[t], 1e-9), `fugue-21 (${t}): untagged B♭ at ${plain}¢, expected the temperament's ${dev10[t]}¢`);
    ok(near(series, 3.91, 1e-9), `fugue-21 (${t}): natural-series B♭ at ${series}¢, expected ET +3.91¢`);
  }
  // Prelude IX: fully specified adaptive just intonation, rendered on an equal-tempered keyboard:
  // every note at ET + its cents whatever temperament is selected (as before this change).
  await againstRenderer('prelude-9', 'cycle/09-e-major/prelude.json', ['equal']);
  const score9 = JSON.parse(readFileSync(resolve(ROOT, 'cycle/09-e-major/prelude.json'), 'utf8'));
  const want9 = new Map(score9.voices.flatMap((v, i) => v.events.filter(e => e.p != null).map(e => [key(i, e.t, e.p), e.cents])));
  let first9 = null;
  for (const temp of TEMPS) {
    const got = await page.evaluate(temp => window.clavier.schedule('prelude-9', 0, { temp }).map(s => s.hz), temp);
    const ids = await page.evaluate(() => window.clavier.schedule('prelude-9', 0).map(s => [s.n.i, s.n.t, s.n.p]));
    ok(got.length === want9.size && ids.every(([i, t, p], k) => near(cents(got[k], p), want9.get(key(i, t, p)), 0.0051)), `prelude-9 (${temp}): not at ET + its cents`);
    if (first9) ok(got.every((hz, k) => hz === first9[k]), `prelude-9: frequencies differ between ${TEMPS[0]} and ${temp}`); else first9 = got;
  }
  await page.evaluate(() => window.clavier.load('prelude-9'));
  const ui9 = await page.evaluate(() => ({ disabled: [...document.querySelectorAll('#temps button')].every(b => b.disabled), note: document.getElementById('tnote').textContent }));
  ok(ui9.disabled && /fixes its tuning/.test(ui9.note), 'prelude-9: temperament buttons should be disabled, with a note saying why');
  await page.evaluate(() => window.clavier.load('fugue-21'));
  const ui21 = await page.evaluate(() => ({ enabled: [...document.querySelectorAll('#temps button')].every(b => !b.disabled), note: document.getElementById('tnote').textContent }));
  ok(ui21.enabled && ui21.note.includes(`${tagged21} of ${total21} notes`), `fugue-21: buttons enabled, note names the ${tagged21} tagged notes: ${ui21.note}`);

  ok(errors.length === 0, 'page errors: ' + errors.join('; '));
} finally {
  await browser.close();
}
console.log(`${checks - failures}/${checks} checks passed` + (failures ? `, ${failures} FAILED` : ''));
process.exit(failures ? 1 : 0);
