/* The Well-Tempered clAIvier: listening app.
   Plain JavaScript, no build step.  Reads catalog.json (written by tools/build_app.py), plays the
   rendered MP3s or a live synth driven by the score, and scrolls the engraved score strip in time
   with whichever is playing.  Routes live in the hash: #/, #/pair/15, #/pair/15/fugue,
   #/appendix/table-canon, #/extras/mobius, #/guide (optional ?v=earlier, ?t=seconds). */
'use strict';
(() => {
  // ------------------------------------------------------------------------------------------
  // Small helpers
  // ------------------------------------------------------------------------------------------
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => [...root.querySelectorAll(sel)];
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const fmt = s => { s = Math.max(0, Math.floor(s || 0)); return Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0'); };
  const fmtLong = s => { const m = Math.round((s || 0) / 60); return m < 1 ? '< 1 min' : m + ' min'; };
  const fmtSize = b => b >= 1e6 ? (b / 1e6).toFixed(1) + ' MB' : Math.max(1, Math.round(b / 1e3)) + ' KB';
  const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
  const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  const store = {
    get(k, d) { try { const v = localStorage.getItem('wtc:' + k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem('wtc:' + k, JSON.stringify(v)); } catch (e) { /* storage unavailable */ } },
    del(k) { try { localStorage.removeItem('wtc:' + k); } catch (e) { /* storage unavailable */ } },
  };
  const jsonCache = new Map();
  const loadJSON = url => {
    if (!jsonCache.has(url)) jsonCache.set(url, fetch(url).then(r => { if (!r.ok) throw new Error(url + ': ' + r.status); return r.json(); }));
    return jsonCache.get(url);
  };
  const textCache = new Map();
  const loadText = url => {
    if (!textCache.has(url)) textCache.set(url, fetch(url).then(r => { if (!r.ok) throw new Error(url + ': ' + r.status); return r.text(); }));
    return textCache.get(url);
  };
  const h = (html) => { const t = document.createElement('template'); t.innerHTML = html.trim(); return t.content.firstElementChild; };

  // ------------------------------------------------------------------------------------------
  // Catalogue
  // ------------------------------------------------------------------------------------------
  let CAT = null;
  let ORDER = [];              // every piece, in display order
  const ROUTES = {};           // route -> piece id
  const P = id => CAT.pieces[id];
  const groupOf = p => CAT.groups.find(g => g.pieces.includes(p.id));
  const dataOf = (p, version) => (version === 'earlier' && p.earlier) ? p.earlier : p;
  const groupLabel = g => g.kind === 'pair' ? `Pair ${g.roman} · ${g.key}` : g.title;
  const pieceLabel = p => p.short + (p.sub ? ' · ' + p.sub : '');
  const hrefOf = (p, version, extra) => '#/' + p.route + ((version === 'earlier' || extra) ? '?' + [version === 'earlier' ? 'v=earlier' : '', extra || ''].filter(Boolean).join('&') : '');

  // ------------------------------------------------------------------------------------------
  // Timing: score quarters <-> seconds under the movement's tempo map (as tools/render_music.py)
  // ------------------------------------------------------------------------------------------
  function scoreEnd(score) {
    let end = 0;
    for (const v of score.voices) if (v.e.length) { const e = v.e[v.e.length - 1]; end = Math.max(end, e[0] + e[1]); }
    return end;
  }
  function makeTiming(score) {
    const m = score.tmap && score.tmap.length ? score.tmap : [[0, score.bpm, 0]];
    const end = scoreEnd(score);
    const secOf = q => {
      let sec = 0;
      for (let k = 0; k < m.length; k++) {
        const [t0, b0] = m[k]; const nx = m[k + 1] || [Infinity, b0, 0]; const [t1, b1, ramp] = nx;
        if (q <= t0) break;
        const e = Math.min(q, t1);
        if (ramp && b1 !== b0 && isFinite(t1)) { const bt = b0 + (b1 - b0) * (e - t0) / (t1 - t0); sec += 60 * (t1 - t0) / (b1 - b0) * Math.log(bt / b0); }
        else sec += (e - t0) * 60 / b0;
        if (q <= t1) break;
      }
      return sec;
    };
    const qOf = sec => {
      if (sec <= 0) return 0;
      let lo = 0, hi = end + 64;
      for (let k = 0; k < 44; k++) { const mid = (lo + hi) / 2; if (secOf(mid) < sec) lo = mid; else hi = mid; }
      return (lo + hi) / 2;
    };
    const barQ = score.meter[0] * 4 / score.meter[1];
    return { secOf, qOf, end, total: secOf(end), barQ, barOf: q => 1 + Math.floor(Math.max(0, Math.min(q, end - 1e-3)) / barQ + 1e-6) };
  }

  // ------------------------------------------------------------------------------------------
  // Live synth (the listening room's engine): any temperament, per-note cents, solo/mute
  // ------------------------------------------------------------------------------------------
  const TNAMES = { 'equal': 'Equal', 'bach-lehman': 'Bach–Lehman 1722', 'werckmeister3': 'Werckmeister III', 'kirnberger3': 'Kirnberger III', 'vallotti': 'Vallotti', 'meantone': '¼-comma meantone' };
  const TBLURB = {
    'equal': 'Every fifth narrowed by 2¢. All keys identical; no key has a colour of its own.',
    'bach-lehman': 'Lehman’s reading of the loops on Bach’s 1722 title page: C–E region sweet, sharp keys brighter, every key playable.',
    'werckmeister3': 'Four narrowed fifths (C–G–D–A, B–F♯). Near keys pure-ish, remote keys tense.',
    'kirnberger3': 'Four narrowed fifths C–G–D–A–E, the rest pure: very pure C major, sharper remote keys.',
    'vallotti': 'Six narrowed fifths F–B, six pure. A gentle circulating temperament.',
    'meantone': 'Pure major thirds in the near keys, a howling wolf between G♯ and E♭. The system the well-tempered keyboard escaped.',
  };
  const Synth = {
    ctx: null, master: null, wave: null, live: new Set(), timer: null, playing: false,
    startCtx: 0, startPos: 0, ptr: 0, flat: [], score: null, timing: null, tempo: 1,
    temp: store.get('temp', 'bach-lehman'), state: {}, hasCents: false, onend: null, key: null,
    ensure() {
      if (this.ctx) return;
      const ctx = this.ctx = new (window.AudioContext || window.webkitAudioContext)();
      const comp = ctx.createDynamicsCompressor(); comp.threshold.value = -18; comp.ratio.value = 4;
      this.master = ctx.createGain(); this.master.gain.value = 0.9;
      const dry = ctx.createGain(); dry.gain.value = 0.8; const wet = ctx.createGain(); wet.gain.value = 0.22;
      const rev = ctx.createConvolver(); const len = Math.floor(ctx.sampleRate * 2.2), ir = ctx.createBuffer(2, len, ctx.sampleRate);
      for (let c = 0; c < 2; c++) { const d = ir.getChannelData(c); for (let k = 0; k < len; k++) d[k] = (Math.random() * 2 - 1) * Math.pow(1 - k / len, 3.2); }
      rev.buffer = ir; this.master.connect(dry); this.master.connect(rev); rev.connect(wet); dry.connect(comp); wet.connect(comp); comp.connect(ctx.destination);
      const n = 12, re = new Float32Array(n), im = new Float32Array(n);
      [0, 1, .42, .26, .18, .1, .07, .045, .03, .02, .012, .008].forEach((a, k) => { im[k] = a; });
      this.wave = ctx.createPeriodicWave(re, im);
    },
    // Notes: [onset, performed length (quarters, = max(1/32, d * gate) as in render_music.py),
    // pitch, velocity, voice, cents or null].  score.perf (tools/build_app.py) carries the exact
    // gates and per-note cents; without it, a 0.97 gate and the compact score's cents are used.
    load(score, timing, key) {
      if (this.key === key) return;
      this.stop(); this.key = key; this.score = score; this.timing = timing; this.state = {}; this.startPos = 0;
      const flat = [];
      if (score.perf) score.perf.v.forEach((evs, i) => evs.forEach(e => flat.push([e[0], e[1], e[2], e[3], i, e.length > 4 ? e[4] : null])));
      else score.voices.forEach((v, i) => v.e.forEach(e => flat.push([e[0], Math.max(1 / 32, e[1] * 0.97), e[2], e[3], i, e.length > 4 ? e[4] : null])));
      flat.sort((a, b) => a[0] - b[0]); this.flat = flat;
      this.tagged = flat.filter(n => n[5] !== null).length;
      this.hasCents = this.tagged > 0;
    },
    // Per note: an untagged note follows the selected temperament; a note with its own cents
    // sounds at equal temperament + cents.  That is render_music.py's rule for scores with
    // cents_reference "equal" (Fugue XXI's natural harmonics), and for Prelude IX, whose cents
    // are measured from the equal temperament it is rendered in.  An explicit 0 is a tagged note.
    hz(p, c) { const dev = CAT.temps[this.temp] || CAT.temps['equal']; return 440 * Math.pow(2, (p - 69 + (c !== null && c !== undefined ? c : dev[((p % 12) + 12) % 12]) / 100) / 12); },
    note(when, dur, p, v, cents, elapsed) {
      const ctx = this.ctx, o = ctx.createOscillator(), g = ctx.createGain(), f = ctx.createBiquadFilter();
      o.setPeriodicWave(this.wave); o.frequency.value = this.hz(p, cents);
      f.type = 'lowpass'; f.frequency.value = Math.min(9000, 900 + v * 40 + (p - 40) * 30);
      const peak = Math.pow(v / 127, 1.6) * 0.16, tau = Math.max(0.25, Math.min(2.4, 1.9 - (p - 60) * 0.03));
      g.gain.setValueAtTime(0, when);
      if (elapsed > 0) {   // a chased note: enter at the level its decay has reached
        const lvl = peak * 0.25 + peak * 0.75 * Math.exp(-elapsed / tau);
        g.gain.linearRampToValueAtTime(lvl, when + 0.015); g.gain.setTargetAtTime(peak * 0.25, when + 0.015, tau);
      } else { g.gain.linearRampToValueAtTime(peak, when + 0.005); g.gain.setTargetAtTime(peak * 0.25, when + 0.005, tau); }
      const off = when + Math.max(0.05, dur); g.gain.setTargetAtTime(0, off, 0.07);
      o.connect(f); f.connect(g); g.connect(this.master); o.start(when); o.stop(off + 0.6);
      this.live.add(o); o.onended = () => this.live.delete(o);
    },
    audible(i) {
      const st = this.state; const solos = Object.keys(st).filter(k => st[k] === 'solo');
      if (st[i] === 'muted') return false; return !solos.length || st[i] === 'solo';
    },
    cycleVoice(i) {
      const st = this.state[i] || 'on'; const solos = Object.values(this.state).filter(x => x === 'solo').length;
      this.state[i] = st === 'on' ? 'solo' : st === 'solo' ? 'muted' : 'on';
      if (st === 'on' && solos) this.state[i] = 'solo';
    },
    pos() { return this.playing ? this.timing.qOf(this.timing.secOf(this.startPos) + (this.ctx.currentTime - this.startCtx) * this.tempo) : this.startPos; },
    play() {
      this.ensure(); if (this.ctx.state === 'suspended') this.ctx.resume();
      if (this.startPos >= this.timing.end - 0.01) this.startPos = 0;
      this.playing = true; this.startCtx = this.ctx.currentTime + 0.08;
      this.ptr = this.flat.findIndex(n => n[0] >= this.startPos - 1e-6); if (this.ptr < 0) this.ptr = this.flat.length;
      // Chase: after a seek, resume, tempo, tuning or voice change, notes already sounding
      // (onset < position < performed end) start at once with their remaining duration.
      const T = this.timing, s0 = T.secOf(this.startPos);
      for (let k = 0; k < this.ptr; k++) {
        const [t, len, p, v, i, c] = this.flat[k];
        if (t + len > this.startPos + 1e-6 && this.audible(i)) this.note(this.startCtx, (T.secOf(t + len) - s0) / this.tempo, p, v, c, (s0 - T.secOf(t)) / this.tempo);
      }
      clearInterval(this.timer); this.timer = setInterval(() => this.sched(), 30); this.sched();
    },
    sched() {
      if (!this.playing) return;
      const T = this.timing, ahead = this.ctx.currentTime + 0.25, s0 = T.secOf(this.startPos);
      while (this.ptr < this.flat.length) {
        const [t, len, p, v, i, c] = this.flat[this.ptr]; const st = T.secOf(t), when = this.startCtx + (st - s0) / this.tempo;
        if (when > ahead) break;
        if (this.audible(i) && when >= this.ctx.currentTime - 0.02) this.note(when, (T.secOf(t + len) - st) / this.tempo, p, v, c, 0);
        this.ptr++;
      }
      if (this.pos() >= T.end + 0.5) { this.stop(); this.startPos = 0; if (this.onend) this.onend(); }
    },
    stop() {
      if (this.playing && this.ctx) this.startPos = this.pos();
      this.playing = false; clearInterval(this.timer);
      this.live.forEach(o => { try { o.stop(); } catch (e) { /* already stopped */ } }); this.live.clear();
    },
    seek(q) { const w = this.playing; this.stop(); this.startPos = clamp(q, 0, this.timing ? this.timing.end : 0); if (w) this.play(); },
    restart() { if (this.playing) { this.stop(); this.play(); } },
  };

  // ------------------------------------------------------------------------------------------
  // Player: one piece at a time, from a rendered MP3 or the live synth, with a queue
  // ------------------------------------------------------------------------------------------
  const audio = document.getElementById('audio');
  const family = k => (k.startsWith('binaural') || k === 'walk') ? 'binaural' : k.startsWith('excerpt') ? 'excerpt' : k;
  const savedPos = (p, version) => store.get(`pos:${p.id}:${version}`, 0);
  function sourcesOf(p, version) {
    const d = dataOf(p, version);
    return [...d.audio.map(e => ({ type: 'audio', key: e.kind, label: e.label, entry: e })), { type: 'synth', key: 'synth', label: 'Live synth' }];
  }
  function chooseSource(srcs, want) {
    want = want || store.get('source', 'piano');
    const full = srcs.filter(s => s.type === 'audio' && s.entry.start_q == null);
    return srcs.find(s => s.key === want)
      || full.find(s => family(s.key) === family(want))
      || full.find(s => s.key === 'walk') || full.find(s => s.key === 'piano')
      || full[0] || srcs.find(s => s.type === 'synth');
  }

  const Player = {
    piece: null, version: 'current', score: null, timing: null, source: null, playing: false,
    pendingSeek: null, token: 0, lastSave: 0, lastPosState: 0, error: null,
    get queue() { return store.get('queue', 'pair'); },
    set queue(v) { store.set('queue', v); },
    isActive(p, version) { return !!this.piece && this.piece.id === p.id && this.version === version; },
    offset() { const e = this.source && this.source.entry; return e && e.start_q != null ? this.timing.secOf(e.start_q) : 0; },
    scoreSec() {
      if (!this.source) return 0;
      if (this.source.type === 'synth') return this.timing.secOf(Synth.pos());
      return (this.pendingSeek != null ? this.pendingSeek : (audio.currentTime || 0)) + this.offset();
    },
    q() {
      if (!this.timing) return 0;
      if (this.source && this.source.type === 'synth') return Synth.pos();
      return this.timing.qOf(this.scoreSec());
    },
    timeline() {   // what the clock and the slider show, in the source's own seconds
      if (!this.source) return { cur: 0, dur: 0 };
      if (this.source.type === 'synth') return { cur: this.timing.secOf(Synth.pos()) / Synth.tempo, dur: this.timing.total / Synth.tempo };
      const dur = isFinite(audio.duration) && audio.duration > 0 ? audio.duration : Math.max(1, this.timing.total - this.offset() + 3);
      return { cur: this.pendingSeek != null ? this.pendingSeek : (audio.currentTime || 0), dur };
    },
    load(p, version = 'current', opts = {}) {
      const promise = this.doLoad(p, version, opts);
      this.pending = { id: p.id, version, promise };
      promise.finally(() => { if (this.pending && this.pending.promise === promise) this.pending = null; });
      return promise;
    },
    async doLoad(p, version, opts) {
      const token = ++this.token;
      this.stopAll(true);
      const d = dataOf(p, version);
      let score;
      try { score = await loadJSON(d.score); } catch (e) { this.error = 'Could not load the score.'; emit(); return; }
      if (token !== this.token) return;
      this.piece = p; this.version = version; this.score = score; this.timing = makeTiming(score); this.error = null;
      this.touched = !!opts.autoplay;
      const srcs = sourcesOf(p, version);
      this.source = chooseSource(srcs, opts.sourceKey);
      let pos = opts.posSec != null ? opts.posSec : savedPos(p, version);
      if (pos > this.timing.total - 2) pos = 0;
      this.resumedAt = opts.posSec == null && pos > 3 ? pos : 0;
      this.setup(pos, !!opts.autoplay);
      setMediaMetadata();
      emit();
    },
    pendingFor(p, version) { return this.pending && this.pending.id === p.id && this.pending.version === version ? this.pending.promise : null; },
    setup(scoreSecPos, autoplay) {
      const s = this.source;
      if (s.type === 'synth') {
        if (!audio.paused) audio.pause();
        Synth.load(this.score, this.timing, this.piece.id + ':' + this.version);
        Synth.onend = () => this.ended();
        Synth.startPos = this.timing.qOf(scoreSecPos);
        if (autoplay) this.play();
        return;
      }
      const off = this.offset(), e = s.entry;
      let target = scoreSecPos - off;
      if (e.start_q != null && (target < 0 || scoreSecPos > this.timing.secOf(e.end_q))) target = 0;
      target = Math.max(0, target);
      const url = new URL(e.src, location.href).href;
      const cur = audio.getAttribute('src') || '';
      const same = audio.src === url || (blobs.has(e.src) && cur === blobs.get(e.src));
      if (!same) { audio.src = blobs.get(e.src) || e.src; this.pendingSeek = target; }
      else if (audio.readyState >= 1) { audio.currentTime = target; this.pendingSeek = null; }
      else this.pendingSeek = target;
      if (autoplay) this.play();
    },
    play() {
      if (!this.source) return;
      this.touched = true;
      pauseVideos();
      if (this.source.type === 'synth') { Synth.play(); this.playing = true; this.afterStateChange(); return; }
      const pr = audio.play();
      if (pr && pr.catch) pr.catch(err => { if (err && err.name !== 'AbortError') { this.error = 'Playback was blocked or failed: ' + err.message; } this.playing = false; emit(); });
    },
    pause() {
      if (!this.source) return;
      if (this.source.type === 'synth') { Synth.stop(); this.playing = false; this.save(true); this.afterStateChange(); return; }
      audio.pause();
    },
    toggle() { if (this.playing) this.pause(); else this.play(); },
    stopAll(save) {
      if (save && this.piece) this.save(true);
      if (Synth.playing) Synth.stop();
      if (!audio.paused) audio.pause();
      this.playing = false;
    },
    seekScoreSec(sec) {
      if (!this.source) return;
      sec = Math.max(0, sec);
      if (this.source.type === 'synth') { Synth.seek(this.timing.qOf(sec)); }
      else {
        const t = Math.max(0, sec - this.offset());
        if (audio.readyState >= 1 && isSeekable()) { audio.currentTime = Math.min(t, (audio.duration || t + 1) - 0.05); this.pendingSeek = null; }
        else this.pendingSeek = t;      // applied on loadedmetadata (or after the Blob swap)
      }
      this.save(true); kick();
    },
    seekQ(q) { this.seekScoreSec(this.timing.secOf(q)); },
    seekBy(ds) {   // ds in source seconds
      if (!this.source) return;
      if (this.source.type === 'synth') this.seekScoreSec(this.scoreSec() + ds * Synth.tempo);
      else this.seekScoreSec(this.scoreSec() + ds);
    },
    seekTimeline(cur) {
      if (!this.source) return;
      if (this.source.type === 'synth') this.seekScoreSec(cur * Synth.tempo);
      else this.seekScoreSec(cur + this.offset());
    },
    setSource(key) {
      const srcs = sourcesOf(this.piece, this.version);
      const s = srcs.find(x => x.key === key); if (!s) return;
      const pos = this.scoreSec(), was = this.playing;
      this.stopAll(false);
      this.source = s; store.set('source', key);
      this.setup(pos, was);
      setMediaMetadata();
      emit();
    },
    save(force) {
      if (!this.piece || !this.timing) return;
      const now = Date.now(); if (!force && now - this.lastSave < 3000) return;
      this.lastSave = now;
      const sec = this.scoreSec();
      if (sec > 2 && sec < this.timing.total - 2) store.set(`pos:${this.piece.id}:${this.version}`, Math.round(sec * 10) / 10);
      else store.del(`pos:${this.piece.id}:${this.version}`);
    },
    afterStateChange() {
      if ('mediaSession' in navigator) { try { navigator.mediaSession.playbackState = this.playing ? 'playing' : 'paused'; } catch (e) { /* unsupported */ } }
      emit(); kick();
    },
    tick() {
      if (!this.playing) return;
      this.save(false);
      const now = Date.now();
      if (now - this.lastPosState > 1000 && this.source && this.source.type === 'audio' && 'mediaSession' in navigator && navigator.mediaSession.setPositionState && isFinite(audio.duration) && audio.duration > 0) {
        this.lastPosState = now;
        try { navigator.mediaSession.setPositionState({ duration: audio.duration, playbackRate: audio.playbackRate || 1, position: Math.min(audio.currentTime, audio.duration) }); } catch (e) { /* ignore */ }
      }
    },
    neighbour(dir, mode) {
      if (!this.piece) return null;
      if (mode === 'off') return null;
      if (mode === 'pair') {
        const g = groupOf(this.piece); const list = g.play.includes(this.piece.id) ? g.play : g.pieces;
        const i = list.indexOf(this.piece.id); return list[i + dir] ? P(list[i + dir]) : null;
      }
      const list = CAT.cycle; const i = list.indexOf(this.piece.id);
      if (i >= 0) return list[i + dir] ? P(list[i + dir]) : null;
      const j = ORDER.indexOf(this.piece.id); return ORDER[j + dir] ? P(ORDER[j + dir]) : null;
    },
    async skip(dir, autoplay) {
      const nx = this.neighbour(dir, 'cycle');
      if (!nx) return;
      const follow = View.pieceId === this.piece.id;
      const want = this.source ? this.source.key : undefined;
      await this.load(nx, 'current', { sourceKey: want, autoplay: autoplay == null ? this.playing : autoplay, posSec: 0 });
      if (follow) navigate(hrefOf(nx), true);
    },
    async ended() {
      this.playing = false;
      if (this.piece) store.del(`pos:${this.piece.id}:${this.version}`);
      const nx = this.version === 'current' ? this.neighbour(1, this.queue) : null;
      if (!nx) { this.afterStateChange(); return; }
      const follow = View.pieceId === this.piece.id;
      await this.load(nx, 'current', { sourceKey: this.source ? this.source.key : undefined, autoplay: true, posSec: 0 });
      if (follow) navigate(hrefOf(nx), true);
    },
  };

  // A static server without HTTP Range support (python3 -m http.server) makes MP3s unseekable:
  // then fetch the whole file once and play it from a Blob, which is always seekable.
  const blobs = new Map();
  const isSeekable = () => {
    const sk = audio.seekable;
    return (audio.getAttribute('src') || '').startsWith('blob:') || (sk.length > 0 && sk.end(sk.length - 1) >= Math.min(5, (audio.duration || 10) - 1));
  };
  async function makeSeekable() {
    const src = audio.getAttribute('src') || '';
    if (!src || isSeekable()) return;
    const token = Player.token, entry = Player.source && Player.source.entry;
    try {
      if (!blobs.has(src)) {
        const r = await fetch(src); if (!r.ok) return;
        blobs.set(src, URL.createObjectURL(await r.blob()));
        if (blobs.size > 6) { const [k, u] = blobs.entries().next().value; URL.revokeObjectURL(u); blobs.delete(k); }
      }
      if (token !== Player.token || !Player.source || Player.source.entry !== entry) return;
      const was = !audio.paused, at = Player.pendingSeek != null ? Player.pendingSeek : audio.currentTime;
      Player.pendingSeek = at; Player.swapping = true;
      audio.src = blobs.get(src);
      if (was) Player.play();
    } catch (e) { /* keep the unseekable stream */ }
  }
  audio.addEventListener('loadedmetadata', () => {
    Player.swapping = false;
    const want = Player.pendingSeek, seekable = isSeekable();
    if (want != null) { try { audio.currentTime = Math.min(want, Math.max(0, audio.duration - 0.05)); } catch (e) { /* ignore */ } }
    Player.pendingSeek = seekable ? null : want;     // kept for the Blob below
    if (!seekable) makeSeekable();
    emit(); kick();
  });
  audio.addEventListener('play', () => { Player.playing = true; Player.error = null; Player.afterStateChange(); });
  audio.addEventListener('pause', () => { if (Player.source && Player.source.type === 'audio' && !Player.swapping) { Player.playing = false; Player.save(true); Player.afterStateChange(); } });
  audio.addEventListener('ended', () => Player.ended());
  audio.addEventListener('seeked', () => kick());
  audio.addEventListener('timeupdate', () => { if (!Player.playing) kick(); });
  audio.addEventListener('error', () => { if (audio.getAttribute('src')) { Player.error = 'This recording could not be loaded.'; Player.playing = false; emit(); } });
  window.addEventListener('pagehide', () => Player.save(true));

  function pauseVideos() { $$('video').forEach(v => { if (!v.paused) v.pause(); }); }

  // Media Session: lock-screen title and controls on phones.
  function setMediaMetadata() {
    if (!('mediaSession' in navigator) || !Player.piece) return;
    const p = Player.piece, g = groupOf(p);
    try {
      navigator.mediaSession.metadata = new MediaMetadata({
        title: pieceLabel(p) + (Player.version === 'earlier' ? ' (earlier version)' : ''),
        artist: 'The Well-Tempered clAIvier',
        album: groupLabel(g) + (Player.source ? ' · ' + Player.source.label : ''),
      });
    } catch (e) { /* unsupported */ }
  }
  if ('mediaSession' in navigator) {
    const set = (a, f) => { try { navigator.mediaSession.setActionHandler(a, f); } catch (e) { /* unsupported action */ } };
    set('play', () => Player.play());
    set('pause', () => Player.pause());
    set('stop', () => Player.pause());
    set('previoustrack', () => Player.skip(-1));
    set('nexttrack', () => Player.skip(1));
    set('seekbackward', d => Player.seekBy(-((d && d.seekOffset) || 10)));
    set('seekforward', d => Player.seekBy((d && d.seekOffset) || 10));
    set('seekto', d => { if (d && d.seekTime != null) Player.seekTimeline(d.seekTime); });
  }

  // State fan-out and the animation loop.
  const listeners = new Set();
  const emit = () => listeners.forEach(f => { try { f(); } catch (e) { console.warn(e); } });
  let rafOn = false;
  const kick = () => { if (!rafOn) { rafOn = true; requestAnimationFrame(loop); } };
  function loop() {
    rafOn = false;
    if (View.frame) View.frame();
    Mini.frame();
    Player.tick();
    if (Player.playing) kick();
  }

  // ------------------------------------------------------------------------------------------
  // Score view: the engraved strip (tiles + time_to_x), or the piano roll
  // ------------------------------------------------------------------------------------------
  class ScoreView {
    constructor(host, { score, timing, strip, onSeek }) {
      this.host = host; this.score = score; this.timing = timing; this.strip = strip; this.onSeek = onSeek;
      this.mode = strip ? store.get('scoremode', 'strip') : 'roll';
      if (this.mode === 'strip' && !strip) this.mode = 'roll';
      this.zoomK = store.get('zoom', 1);
      this.q = 0; this.tx = 0; this.drag = null; this.tiles = new Map();
      host.innerHTML = `
        <div class="score-tools">
          <div class="seg" role="group" aria-label="Score display">
            <button type="button" data-mode="strip" ${strip ? '' : 'disabled title="No engraved strip for this piece"'}>Score</button>
            <button type="button" data-mode="roll">Piano roll</button>
          </div>
          <span class="score-hint">Drag or tap to move</span>
          <div class="seg zoom" role="group" aria-label="Zoom">
            <button type="button" data-zoom="-1" aria-label="Zoom out">−</button>
            <button type="button" data-zoom="1" aria-label="Zoom in">+</button>
          </div>
        </div>
        <div class="score-frame">
          <div class="score-scroll" tabindex="0" role="img" aria-label="Score following the music. Drag sideways or tap to move through the piece.">
            <div class="strip-track"></div>
            <canvas class="roll"></canvas>
          </div>
          <div class="playhead" aria-hidden="true"></div>
        </div>`;
      this.frame = $('.score-frame', host); this.scroll = $('.score-scroll', host);
      this.track = $('.strip-track', host); this.canvas = $('.roll', host);
      $$('[data-mode]', host).forEach(b => b.addEventListener('click', () => { this.mode = b.dataset.mode; store.set('scoremode', this.mode); this.layout(); }));
      $$('[data-zoom]', host).forEach(b => b.addEventListener('click', () => this.zoom(+b.dataset.zoom)));
      this.bindPointer();
      this.onResize = () => this.layout();
      window.addEventListener('resize', this.onResize);
      this.layout();
    }
    destroy() { window.removeEventListener('resize', this.onResize); }
    zoom(dir) { this.zoomK = clamp(this.zoomK * (dir > 0 ? 1.25 : 0.8), 0.2, 4); store.set('zoom', this.zoomK); this.layout(); }
    layout() {
      const strip = this.mode === 'strip' && this.strip;
      $$('[data-mode]', this.host).forEach(b => b.setAttribute('aria-pressed', String(b.dataset.mode === this.mode)));
      this.track.hidden = !strip; this.canvas.hidden = !!strip;
      const W = this.scroll.clientWidth || this.host.clientWidth || 320;
      this.W = W; this.playX = Math.round(Math.min(W * 0.3, 260));
      this.head = $('.playhead', this.host);
      const maxH = clamp(Math.round(window.innerHeight * 0.48), 200, 560);
      if (strip) {
        const S = this.strip;
        const fit = maxH / S.h;
        this.s = clamp(Math.min(0.9, Math.max(fit, 0.5)) * this.zoomK, Math.min(fit, 0.5) * 0.6, 1.6);
        this.scroll.style.height = Math.min(Math.ceil(S.h * this.s), maxH) + 'px';
        this.track.style.width = (S.w * this.s) + 'px'; this.track.style.height = (S.h * this.s) + 'px';
        this.tiles.forEach(img => img.remove()); this.tiles.clear();
        $$('.entry-label', this.track).forEach(el => el.remove());
        if (this.s >= 0.3) {
          const frag = document.createDocumentFragment();
          for (const [v, t, label, x, y] of S.entries) {
            const el = document.createElement('span'); el.className = 'entry-label'; el.textContent = label;
            el.style.left = (x * this.s) + 'px'; el.style.top = Math.max(0, y * this.s - 15) + 'px';
            frag.appendChild(el);
          }
          this.track.appendChild(frag);
        }
        const t2x = S.t2x; this.xs = t2x.map(p => p[1]); this.ts = t2x.map(p => p[0]);
        this.trackW = S.w * this.s;
        // Keep the playhead where the first note is, so the clefs show at the start.
        this.playX = Math.round(clamp(this.xs[0] * this.s + 4, W * 0.25, Math.max(W * 0.25, Math.min(W * 0.6, 320))));
      } else {
        this.rollH = clamp(Math.round(maxH * 0.6), 200, 320);
        this.scroll.style.height = this.rollH + 'px';
        const span = Math.max(this.timing.barQ * 4, Math.min(this.timing.barQ * 8, 24)) / this.zoomK;
        this.pxq = W / span;
        const all = this.score.voices.flatMap(v => v.e.map(e => e[2]));
        this.lo = Math.min(...all) - 2; this.hi = Math.max(...all) + 2;
        this.trackW = (this.timing.end + 2) * this.pxq;
      }
      this.lastTx = null; this.lastHx = null; this.render();
    }
    // score quarters <-> track x (CSS px)
    qToX(q) {
      if (this.mode !== 'strip' || !this.strip) return q * this.pxq;
      const ts = this.ts, xs = this.xs;
      if (q <= ts[0]) return xs[0] * this.s;
      if (q >= ts[ts.length - 1]) return xs[xs.length - 1] * this.s;
      let lo = 0, hi = ts.length - 1;
      while (hi - lo > 1) { const m = (lo + hi) >> 1; if (ts[m] <= q) lo = m; else hi = m; }
      return (xs[lo] + (xs[hi] - xs[lo]) * (q - ts[lo]) / (ts[hi] - ts[lo])) * this.s;
    }
    xToQ(x) {
      if (this.mode !== 'strip' || !this.strip) return clamp(x / this.pxq, 0, this.timing.end);
      const ts = this.ts, xs = this.xs; x /= this.s;
      if (x <= xs[0]) return ts[0];
      if (x >= xs[xs.length - 1]) return ts[ts.length - 1];
      let lo = 0, hi = xs.length - 1;
      while (hi - lo > 1) { const m = (lo + hi) >> 1; if (xs[m] <= x) lo = m; else hi = m; }
      return ts[lo] + (ts[hi] - ts[lo]) * (x - xs[lo]) / (xs[hi] - xs[lo]);
    }
    update(q, playing) { this.q = q; this.playing = playing; if (!this.drag || !this.drag.moved) this.render(); }
    minTx() { return Math.min(0, this.W - this.trackW); }
    render() {
      const dragging = this.drag && this.drag.moved;
      const X = this.qToX(this.q);
      const tx = dragging ? this.drag.tx : clamp(this.playX - X, this.minTx(), 0);
      const hx = dragging ? this.drag.hx : X + tx;
      if (hx !== this.lastHx) { this.head.style.transform = `translateX(${hx.toFixed(1)}px)`; this.lastHx = hx; }
      if (this.mode === 'strip' && this.strip) {
        if (this.lastTx !== null && Math.abs(tx - this.lastTx) < 0.2) return;
        this.lastTx = tx; this.tx = tx;
        this.track.style.transform = `translate3d(${tx.toFixed(1)}px,0,0)`;
        this.ensureTiles(tx);
      } else { this.tx = tx; this.drawRoll(tx); }
    }
    ensureTiles(tx) {
      const S = this.strip, s = this.s, a = -tx - this.W, b = -tx + 2 * this.W;
      const keep = new Set();
      for (const [x, w, src] of S.tiles) {
        if ((x + w) * s < a || x * s > b) continue;
        keep.add(src);
        if (!this.tiles.has(src)) {
          const img = new Image(); img.decoding = 'async'; img.alt = ''; img.draggable = false; img.className = 'tile';
          img.style.left = (x * s) + 'px'; img.style.width = (w * s) + 'px'; img.style.height = (S.h * s) + 'px';
          img.src = src; this.track.appendChild(img); this.tiles.set(src, img);
        }
      }
      this.tiles.forEach((img, src) => { if (!keep.has(src)) { img.remove(); this.tiles.delete(src); } });
    }
    drawRoll(tx) {
      const c = this.canvas, d = window.devicePixelRatio || 1, W = this.W, H = this.rollH;
      if (c.width !== Math.round(W * d) || c.height !== Math.round(H * d)) { c.width = Math.round(W * d); c.height = Math.round(H * d); c.style.width = W + 'px'; c.style.height = H + 'px'; }
      const g = c.getContext('2d'); g.setTransform(d, 0, 0, d, 0, 0); g.clearRect(0, 0, W, H);
      const T = this.timing, t0 = Math.max(0, -tx / this.pxq), t1 = (-tx + W) / this.pxq;
      const x = t => t * this.pxq + tx, lo = this.lo, hi = this.hi;
      const y = p => H - 8 - (p - lo) / (hi - lo) * (H - 16), nh = Math.max(2.5, (H - 16) / (hi - lo) * 0.9);
      g.font = '10px ' + css('--f-mono'); g.fillStyle = css('--muted'); g.strokeStyle = css('--rule'); g.lineWidth = 1;
      for (let b = Math.floor(t0 / T.barQ); b * T.barQ <= t1; b++) { const bx = x(b * T.barQ); g.beginPath(); g.moveTo(bx, 0); g.lineTo(bx, H); g.stroke(); if (bx > 2) g.fillText(String(b + 1), bx + 3, 11); }
      const synth = Player.source && Player.source.type === 'synth' && Synth.score === this.score;
      const now = this.q;
      this.score.voices.forEach((v, i) => {
        const on = !synth || Synth.audible(i);
        g.fillStyle = css('--v' + (1 + i % 9));
        for (const e of v.e) {
          if (e[0] > t1) break; if (e[0] + e[1] < t0) continue;
          const xa = x(e[0]), xb = x(e[0] + e[1]); const lit = this.playing && e[0] <= now && now < e[0] + e[1];
          g.globalAlpha = on ? (lit ? 1 : 0.72) : 0.15;
          g.fillRect(xa, y(e[2]) - nh / 2, Math.max(1.5, xb - xa - 1), lit ? nh + 1.5 : nh);
        }
        g.globalAlpha = 1;
      });
      g.fillStyle = css('--entry'); g.strokeStyle = css('--entry');
      for (const en of this.score.entries) {
        if (en[1] < t0 - 4 || en[1] > t1) continue;
        const ex = x(en[1]); g.globalAlpha = 0.9; g.beginPath(); g.moveTo(ex, 14); g.lineTo(ex, H); g.setLineDash([2, 3]); g.stroke(); g.setLineDash([]);
        const v = this.score.voices[en[0]]; g.fillText((v ? v.a + ' ' : '') + en[2], ex + 3, 24); g.globalAlpha = 1;
      }
    }
    bindPointer() {
      const f = this.frame;
      f.addEventListener('pointerdown', e => {
        if (e.button !== 0 || e.target.closest('button')) return;
        this.drag = { x0: e.clientX, y0: e.clientY, tx0: this.tx, hx: this.lastHx || 0, moved: false, id: e.pointerId };
      });
      f.addEventListener('pointermove', e => {
        const d = this.drag; if (!d || d.id !== e.pointerId) return;
        const dx = e.clientX - d.x0;
        if (!d.moved && Math.abs(dx) > 6 && Math.abs(dx) > Math.abs(e.clientY - d.y0)) { d.moved = true; try { f.setPointerCapture(e.pointerId); } catch (err) { /* ignore */ } f.classList.add('dragging'); }
        if (d.moved) { d.tx = clamp(d.tx0 + dx, this.minTx(), 0); this.lastTx = null; this.render(); }
      });
      const finish = (e, cancel) => {
        const d = this.drag; if (!d || d.id !== e.pointerId) return;
        this.drag = null; f.classList.remove('dragging');
        if (cancel) { this.lastTx = null; this.render(); return; }
        let q;
        if (d.moved) q = this.xToQ(d.hx - d.tx);
        else { const r = this.scroll.getBoundingClientRect(); q = this.xToQ(e.clientX - r.left - this.tx); }
        this.lastTx = null;
        this.onSeek(clamp(q, 0, this.timing.end));
      };
      f.addEventListener('pointerup', e => finish(e, false));
      f.addEventListener('pointercancel', e => finish(e, true));
    }
  }

  // ------------------------------------------------------------------------------------------
  // Markdown (enough for the notes and the guide: headings, lists, tables, code, emphasis, links)
  // ------------------------------------------------------------------------------------------
  function resolveLink(u, baseDir) {
    if (/^(https?:|mailto:)/.test(u)) return u;
    if (u.startsWith('#')) return null;
    const parts = (baseDir ? baseDir + '/' + u : u).split('/'); const out = [];
    for (const p of parts) { if (p === '..') out.pop(); else if (p && p !== '.') out.push(p); }
    return CAT.repo + '/blob/main/' + out.join('/');
  }
  function mdInline(s, baseDir) {
    const codes = [];
    let x = esc(s).replace(/`([^`]+)`/g, (m, c) => { codes.push(c); return `\u0000${codes.length - 1}\u0000`; });
    x = x.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, (m, t, u) => {
      const href = resolveLink(u.replace(/&amp;/g, '&'), baseDir);
      return href ? `<a href="${esc(href)}" target="_blank" rel="noopener">${t}</a>` : t;
    });
    x = x.replace(/\*\*([^*]+?)\*\*/g, '<strong>$1</strong>');
    x = x.replace(/(^|[^\w*])\*(?!\s)([^*]+?)\*(?!\w)/g, '$1<em>$2</em>');
    x = x.replace(/(^|[^\w])_(?!\s)([^_]+?)_(?!\w)/g, '$1<em>$2</em>');
    return x.replace(/\u0000(\d+)\u0000/g, (m, k) => `<code>${codes[+k]}</code>`);
  }
  function md(text, baseDir) {
    const L = text.replace(/\r/g, '').split('\n'); const out = []; let i = 0;
    const isTableSep = s => /^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$/.test(s);
    const cells = s => s.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(c => c.trim());
    while (i < L.length) {
      const line = L[i];
      if (!line.trim()) { i++; continue; }
      let m;
      if (/^```/.test(line)) { const buf = []; i++; while (i < L.length && !/^```/.test(L[i])) buf.push(L[i++]); i++; out.push(`<pre><code>${esc(buf.join('\n'))}</code></pre>`); continue; }
      if ((m = line.match(/^(#{1,6})\s+(.*)$/))) { const n = Math.min(6, m[1].length + 1); const id = m[2].toLowerCase().replace(/[^\w]+/g, '-').replace(/^-|-$/g, ''); out.push(`<h${n} id="md-${id}">${mdInline(m[2], baseDir)}</h${n}>`); i++; continue; }
      if (/^\s*(---|\*\*\*)\s*$/.test(line)) { out.push('<hr>'); i++; continue; }
      if (/^\s*\|/.test(line) && i + 1 < L.length && isTableSep(L[i + 1])) {
        const head = cells(line); i += 2; const rows = [];
        while (i < L.length && /^\s*\|/.test(L[i])) rows.push(cells(L[i++]));
        out.push('<div class="table-wrap"><table><thead><tr>' + head.map(c => `<th>${mdInline(c, baseDir)}</th>`).join('') + '</tr></thead><tbody>' +
          rows.map(r => '<tr>' + r.map(c => `<td>${mdInline(c, baseDir)}</td>`).join('') + '</tr>').join('') + '</tbody></table></div>');
        continue;
      }
      if (/^\s*>/.test(line)) { const buf = []; while (i < L.length && /^\s*>/.test(L[i])) buf.push(L[i++].replace(/^\s*>\s?/, '')); out.push(`<blockquote>${md(buf.join('\n'), baseDir)}</blockquote>`); continue; }
      if (/^\s*([-*+]|\d+\.)\s+/.test(line)) {
        // a list, possibly nested by indentation
        const items = [];
        while (i < L.length && (L[i].trim() === '' ? (i + 1 < L.length && /^\s*([-*+]|\d+\.)\s+/.test(L[i + 1])) : true)) {
          const l = L[i];
          if (!l.trim()) { i++; continue; }
          const mm = l.match(/^(\s*)([-*+]|\d+\.)\s+(.*)$/);
          if (mm) items.push({ ind: mm[1].length, ord: /\d/.test(mm[2]), text: mm[3] });
          else if (/^\s+\S/.test(l) && items.length) items[items.length - 1].text += ' ' + l.trim();
          else break;
          i++;
        }
        let html = ''; const stack = [];
        for (const it of items) {
          while (stack.length && it.ind < stack[stack.length - 1].ind) { html += `</li></${stack.pop().tag}>`; }
          if (!stack.length || it.ind > stack[stack.length - 1].ind) { const tag = it.ord ? 'ol' : 'ul'; stack.push({ ind: it.ind, tag }); html += `<${tag}><li>`; }
          else html += '</li><li>';
          html += mdInline(it.text, baseDir);
        }
        while (stack.length) html += `</li></${stack.pop().tag}>`;
        out.push(html); continue;
      }
      const buf = [];
      while (i < L.length && L[i].trim() && !/^(#{1,6}\s|```|\s*\||\s*>|\s*([-*+]|\d+\.)\s+)/.test(L[i])) buf.push(L[i++].trim());
      if (!buf.length) { buf.push(L[i++].trim()); }
      out.push(`<p>${mdInline(buf.join(' '), baseDir)}</p>`);
    }
    return out.join('\n');
  }
  const dirOf = mediaPath => mediaPath.replace(/^media\//, '').split('/').slice(0, -1).join('/');

  // ------------------------------------------------------------------------------------------
  // Views
  // ------------------------------------------------------------------------------------------
  const main = document.getElementById('main');
  const View = { name: null, pieceId: null, frame: null, destroy: null };
  function setView(name, html) {
    if (View.destroy) View.destroy();
    View.name = name; View.pieceId = null; View.frame = null; View.destroy = null;
    main.innerHTML = html;
  }

  function navigate(hash, replace) {
    if (location.hash === hash) return;
    if (replace) { history.replaceState(null, '', hash); route(); } else location.hash = hash;
  }

  function parseHash() {
    const raw = location.hash.replace(/^#\/?/, '');
    const [path, qs] = raw.split('?');
    const params = new URLSearchParams(qs || '');
    return { path: path.replace(/\/$/, ''), params };
  }

  let lastPath = null, routed = 0;
  function route() {
    const { path, params } = parseHash();
    const scroll = lastPath !== path; lastPath = path; routed++;
    if (!path) renderHome();
    else if (path === 'guide' || path.startsWith('guide/')) renderGuide(path.split('/')[1]);
    else if (ROUTES[path]) renderPiece(P(ROUTES[path]), params.get('v') === 'earlier' ? 'earlier' : 'current', params);
    else renderNotFound(path);
    Mini.update();
    if (scroll) { window.scrollTo(0, 0); const h1 = $('h1', main); if (h1 && routed > 1) h1.focus({ preventScroll: true }); }
  }

  // ---------- home ----------
  function pairCard(g) {
    const ids = g.play; const pre = ids.map(P).find(p => p.slug === 'prelude'); const fug = ids.map(P).find(p => p.slug === 'fugue');
    return `<article class="card pair-card${g.recomposed ? ' recomposed' : ''}">
      <h3><a class="card-link" href="#/${g.route}"><span class="roman">${g.roman}</span> <span class="key">${esc(g.key)}</span></a></h3>
      <button type="button" class="icon-btn card-play" data-play-group="${g.id}" aria-label="Play Pair ${g.roman}, ${esc(g.key)}: prelude then fugue">${ICON.play}</button>
      <p class="meta"><span>Fugue à ${g.voices}</span><span>${fmt(g.duration)}</span>${g.recomposed ? '<span class="badge" title="Recomposed in October 2026; the earlier version is on the fugue’s page">recomposed</span>' : ''}</p>
      <p class="concept">${mdInline(g.concept || (fug ? fug.sub : ''), '')}</p>
      <div class="card-actions">
        ${pre ? `<a href="${hrefOf(pre)}">${esc(pre.sub || 'Prelude')}</a>` : ''}${fug ? `<a href="${hrefOf(fug)}">${esc(fug.sub || 'Fugue')}</a>` : ''}
      </div>
    </article>`;
  }
  function pieceCard(p) {
    return `<article class="card piece-card">
      <h3><a class="card-link" href="${hrefOf(p)}">${esc(p.short)}</a></h3>
      <p class="meta"><span>${p.voices} voices</span><span>${fmt(p.duration)}</span></p>
      <button type="button" class="icon-btn card-play" data-play-piece="${p.id}" aria-label="Play ${esc(p.short)}">${ICON.play}</button>
      <p class="concept">${esc(p.sub || p.concept || '')}${p.sub && p.concept ? ': ' + esc(p.concept) : ''}</p>
    </article>`;
  }
  function renderHome() {
    document.title = 'The Well-Tempered clAIvier';
    const pairs = CAT.groups.filter(g => g.kind === 'pair');
    const others = CAT.groups.filter(g => g.kind !== 'pair');
    const total = CAT.cycle.reduce((s, id) => s + P(id).duration, 0);
    setView('home', `
      <section class="hero">
        <p class="eyebrow">24 preludes and fugues · the key order of Bach’s Book I</p>
        <h1 tabindex="-1">The Well-Tempered <em>clAIvier</em></h1>
        <p class="lede">An AI-composed cycle of 24 preludes and fugues in Bach’s key order, C major to B minor, that tries to push his ethos further rather than away: learned counterpoint, allusion and the key cycle, with computation used to search, verify, tune and render. Every note is written by hand in its source file. Each movement here has piano renders in a historical temperament and in equal temperament, many fugues have binaural renders for headphones, and a live synth plays any movement in any tuning, while the engraved score scrolls along with whatever you hear.</p>
        <p class="lede small">Nobody involved in writing it could listen to it. Your ears are the first real test.</p>
        <div class="hero-actions">
          <button type="button" class="btn primary" data-play-cycle>${ICON.play}<span>Play the whole cycle</span></button>
          <a class="btn" href="#/guide">Listening guide</a>
          <span class="muted">${CAT.cycle.length} movements · about ${Math.round(total / 60)} min</span>
        </div>
      </section>
      ${CAT.picks.length ? `<section class="picks" aria-labelledby="picks-h">
        <h2 id="picks-h">If you have half an hour</h2>
        <ol>${CAT.picks.map((k, i) => { const id = ROUTES[k.route]; return `<li>
          <button type="button" class="icon-btn small" data-pick="${i}" aria-label="Play ${esc(k.label)}">${ICON.play}</button>
          <div><a href="#/${k.route}"><strong>${esc(k.label)}</strong></a> ${mdInline(k.text, '')}</div></li>`; }).join('')}</ol>
        <p class="muted small">From the <a href="#/guide/half-hour">listening guide</a>: the pieces whose idea should be audible on a first hearing.</p>
      </section>` : ''}
      <section aria-labelledby="pairs-h">
        <div class="section-head"><h2 id="pairs-h">The 24 pairs</h2><span class="muted small">prelude and fugue in each key</span></div>
        <div class="cards">${pairs.map(pairCard).join('')}</div>
      </section>
      ${others.map(g => `<section aria-labelledby="g-${g.id}">
        <div class="section-head"><h2 id="g-${g.id}">${esc(g.title)}</h2><span class="muted small">${esc(g.sub || '')}</span></div>
        <div class="cards">${g.pieces.map(id => pieceCard(P(id))).join('')}</div>
      </section>`).join('')}
      <footer class="site-foot">
        <p>Renders are synthesised from the written scores (piano: FluidR3 GM soundfont; binaural: voices placed around the listener). Scores, MIDI and MusicXML can be downloaded on each piece’s page. Source: <a href="${esc(CAT.repo)}" target="_blank" rel="noopener">${esc(CAT.repo.replace('https://', ''))}</a>.</p>
        <p class="small">Keys: <kbd>Space</kbd> play/pause · <kbd>←</kbd>/<kbd>→</kbd> 5 s · <kbd>J</kbd>/<kbd>L</kbd> 10 s · <kbd>N</kbd>/<kbd>P</kbd> next/previous piece. Built ${esc(CAT.built)}.</p>
      </footer>`);
    main.querySelector('[data-play-cycle]').addEventListener('click', () => { Player.queue = 'cycle'; startPiece(P(CAT.cycle[0]), { posSec: 0 }); });
    $$('[data-play-group]', main).forEach(b => b.addEventListener('click', () => {
      const g = CAT.groups.find(x => x.id === b.dataset.playGroup); if (Player.queue === 'off') Player.queue = 'pair';
      startPiece(P(g.play[0]), { posSec: 0 });
    }));
    $$('[data-play-piece]', main).forEach(b => b.addEventListener('click', () => startPiece(P(b.dataset.playPiece), {})));
    $$('[data-pick]', main).forEach(b => b.addEventListener('click', () => {
      const k = CAT.picks[+b.dataset.pick]; const p = P(ROUTES[k.route]);
      if (k.queue === 'pair' && Player.queue === 'off') Player.queue = 'pair';
      startPiece(p, { posSec: k.queue === 'pair' ? 0 : undefined });
    }));
  }
  function startPiece(p, opts) {
    Player.load(p, 'current', Object.assign({ autoplay: true }, opts)).then(() => kick());
    navigate(hrefOf(p));
  }

  // ---------- guide ----------
  function renderGuide(section) {
    document.title = 'Listening guide · The Well-Tempered clAIvier';
    setView('guide', `<nav class="crumbs"><a href="#/">All pieces</a></nav><article class="md guide"><p class="muted">Loading the listening guide…</p></article>`);
    loadText(CAT.guide).then(text => {
      if (View.name !== 'guide') return;
      const art = $('.guide', main);
      art.innerHTML = md(text, dirOf(CAT.guide));
      const h1 = $('h2', art); if (h1) { const n = document.createElement('h1'); n.innerHTML = h1.innerHTML; n.tabIndex = -1; h1.replaceWith(n); }
      $$('h3', art).forEach(x => { if (/half an hour/i.test(x.textContent)) x.id = 'half-hour'; });
      // Link the pieces the guide names to their pages.
      $$('strong', art).forEach(s => { const m = s.textContent.match(/^(Pair|Fugue|Prelude) ([IVXL]+)$/); if (m) { const r = linkFor(m[1], m[2]); if (r) s.innerHTML = `<a href="#/${r}">${esc(s.textContent)}</a>`; } });
      $$('tbody tr', art).forEach(tr => { const td = tr.cells[0]; const m = td && td.textContent.match(/^([IVXL]+)\s/); if (m) { const r = linkFor('Pair', m[1]); if (r) td.innerHTML = `<a href="#/${r}">${td.innerHTML}</a>`; } });
      if (section === 'half-hour') { const el = $('#half-hour'); if (el) el.scrollIntoView(); }
    }).catch(() => { if (View.name === 'guide') $('.guide', main).innerHTML = '<p class="error">Could not load the listening guide.</p>'; });
  }
  function linkFor(kind, roman) {
    const g = CAT.groups.find(x => x.kind === 'pair' && x.roman === roman); if (!g) return null;
    if (kind === 'Pair') return g.route;
    const p = g.pieces.map(P).find(x => x.slug === kind.toLowerCase()); return p ? p.route : g.route;
  }

  function renderNotFound(path) {
    document.title = 'Not found · The Well-Tempered clAIvier';
    setView('404', `<section class="hero"><h1 tabindex="-1">Not found</h1><p class="lede">There is no page at <code>#/${esc(path)}</code>.</p><p><a class="btn" href="#/">All pieces</a></p></section>`);
  }

  // ---------- piece ----------
  const ICON = {
    play: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5.5v13l11-6.5z" fill="currentColor"/></svg>',
    pause: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M7 5h3.5v14H7zM13.5 5H17v14h-3.5z" fill="currentColor"/></svg>',
    back: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M12.5 7.5 7 12l5.5 4.5zM18 7.5 12.5 12l5.5 4.5z" fill="currentColor"/></svg>',
    fwd: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M11.5 7.5 17 12l-5.5 4.5zM6 7.5 11.5 12 6 16.5z" fill="currentColor"/></svg>',
    prev: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 5h2v14H6zM19 5.5v13L9 12z" fill="currentColor"/></svg>',
    next: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M16 5h2v14h-2zM5 5.5v13L15 12z" fill="currentColor"/></svg>',
    phones: '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M4 14v-2a8 8 0 0 1 16 0v2" fill="none" stroke="currentColor" stroke-width="2"/><rect x="3" y="13" width="5" height="7" rx="1.5" fill="currentColor"/><rect x="16" y="13" width="5" height="7" rx="1.5" fill="currentColor"/></svg>',
  };

  function renderPiece(p, version, params) {
    if (version === 'earlier' && !p.earlier) version = 'current';
    const d = dataOf(p, version), g = groupOf(p);
    const earlier = version === 'earlier';
    document.title = `${pieceLabel(p)}${earlier ? ' (earlier version)' : ''} · The Well-Tempered clAIvier`;
    const siblings = g.pieces.map(P);
    const idx = ORDER.indexOf(p.id), prevP = ORDER[idx - 1] ? P(ORDER[idx - 1]) : null, nextP = ORDER[idx + 1] ? P(ORDER[idx + 1]) : null;
    const facts = [d.key, d.meter ? d.meter.join('/') : '', d.bpm ? '♩ = ' + Math.round(d.bpm) : '', d.voices + ' voices', d.bars ? d.bars + ' bars' : '', fmt(d.duration)].filter(Boolean);
    const downloads = d.downloads.concat(d.audio, p.video && !earlier ? p.video : []);
    setView('piece', `
      <nav class="crumbs" aria-label="Breadcrumb"><a href="#/">All pieces</a> <span aria-hidden="true">›</span> <span>${esc(groupLabel(g))}</span></nav>
      ${siblings.length > 1 ? `<nav class="tabs" aria-label="Movements">${siblings.map(s => `<a href="${hrefOf(s)}"${s.id === p.id ? ' aria-current="page"' : ''}>${esc(s.slug === 'prelude-tempered' ? 'Prelude, well-tempered' : s.group === 'pair' ? s.slug.replace(/^./, c => c.toUpperCase()) : s.short.replace(/\s*\(.*\)$/, ''))}</a>`).join('')}</nav>` : ''}
      <header class="piece-head">
        <h1 tabindex="-1">${esc(p.short)}${p.sub ? `<span class="sub">${esc(p.sub)}</span>` : ''}</h1>
        <p class="facts">${facts.map(f => `<span>${esc(f)}</span>`).join('')}${earlier ? '<span class="badge">earlier version</span>' : ''}</p>
      </header>
      ${p.earlier ? `<div class="version seg" role="group" aria-label="Version">
        <button type="button" data-version="current" aria-pressed="${!earlier}">Current · ${p.voices} voices</button>
        <button type="button" data-version="earlier" aria-pressed="${earlier}">Earlier version · ${p.earlier.voices} voices</button>
      </div>` : ''}
      <section class="player-panel" aria-label="Player">
        <div class="score-host"></div>
        <div class="transport">
          <button type="button" class="play-btn" aria-label="Play">${ICON.play}</button>
          <button type="button" class="icon-btn" data-skip="-1" aria-label="Previous piece">${ICON.prev}</button>
          <button type="button" class="icon-btn" data-seek="-10" aria-label="Back 10 seconds">${ICON.back}</button>
          <button type="button" class="icon-btn" data-seek="10" aria-label="Forward 10 seconds">${ICON.fwd}</button>
          <button type="button" class="icon-btn" data-skip="1" aria-label="Next piece">${ICON.next}</button>
          <div class="seekwrap"><input type="range" class="seek" min="0" max="1000" step="1" value="0" aria-label="Position in the recording"><span class="clock" aria-live="off">bar 1 · 0:00 / 0:00</span></div>
        </div>
        <div class="sources-row">
          <span class="muted small" id="src-l">Recording</span>
          <div class="sources" role="radiogroup" aria-labelledby="src-l"></div>
        </div>
        <p class="hint" hidden></p>
        <div class="queue-row">
          <span class="muted small" id="queue-l">When it ends</span>
          <div class="seg queue" role="group" aria-labelledby="queue-l">
            <button type="button" data-queue="off">Stop</button>
            <button type="button" data-queue="pair">${g.kind === 'pair' ? 'Play the pair' : 'Play the group'}</button>
            <button type="button" data-queue="cycle">Continue the cycle</button>
          </div>
        </div>
        <p class="status" role="status"></p>
        <div class="synth-panel" hidden>
          <div class="synth-row"><h3>Tuning</h3><div class="seg temps" role="group" aria-label="Temperament"></div></div>
          <p class="tnote small muted"></p>
          <div class="synth-row"><label class="tempo">Tempo <input type="range" min="50" max="140" step="5" value="100" aria-label="Synth tempo"><span class="tempoval">100%</span></label></div>
          <div class="synth-row"><h3>Voices</h3><p class="small muted">Tap a voice to solo it, again to mute it, again to restore.</p></div>
          <div class="voices"></div>
        </div>
      </section>
      <section class="about" aria-labelledby="about-h">
        <h2 id="about-h">${earlier ? 'About the earlier version' : 'About this piece'}</h2>
        <div class="notes">${earlier ? '<p class="muted">Loading…</p>' : esc(p.notes).split(/\n\n+/).map(t => `<p>${t}</p>`).join('')}</div>
      </section>
      <details class="entries-sec fullnotes" hidden>
        <summary>Subject entries <span class="muted small entries-count"></span></summary>
        <div class="entries"></div>
      </details>
      ${!earlier && p.video.length ? `<section aria-labelledby="video-h"><h2 id="video-h">Video</h2>
        ${p.video.map(v => `<video class="video" controls playsinline preload="metadata" src="${esc(v.src)}" aria-label="${esc(v.label)}"></video>`).join('')}
        <p class="small muted">The score folding into a Möbius band as the walking render plays (it begins with an 8-second title).</p></section>` : ''}
      ${!earlier && p.images.length ? `<section aria-labelledby="img-h"><h2 id="img-h">${esc(p.images[0].label)}</h2>
        ${p.images.map(im => `<a href="${esc(im.src)}" target="_blank" rel="noopener"><img class="figure" src="${esc(im.src)}" alt="${esc(im.label)}: the listener’s path through the room" loading="lazy"></a>`).join('')}</section>` : ''}
      <section class="downloads" aria-labelledby="dl-h">
        <h2 id="dl-h">Score and downloads</h2>
        <ul>${downloads.map(e => `<li><span class="dl-label">${esc(e.label)}</span><span class="dl-file">${esc(e.file)} · ${fmtSize(e.bytes)}</span>
          <span class="dl-actions">${e.type === 'pdf' ? `<a href="${esc(e.src)}" target="_blank" rel="noopener">View</a>` : ''}<a href="${esc(e.src)}" download="${esc(downloadName(p, e))}">Download</a></span></li>`).join('')}</ul>
        <p class="small muted">Source score: <a href="${esc(CAT.repo)}/blob/main/${esc(d.source)}" target="_blank" rel="noopener">${esc(d.source)}</a></p>
      </section>
      ${(earlier ? d.notes_md : p.notes_md) ? `<details class="fullnotes notes-details"><summary>${earlier ? 'Notes on the earlier version' : 'Composer’s notes'} <span class="muted small">(${esc((earlier ? d.notes_md : p.notes_md).split('/').pop())})</span></summary><div class="md"><p class="muted">Loading…</p></div></details>` : ''}
      <nav class="prevnext" aria-label="Neighbouring pieces">
        ${prevP ? `<a href="${hrefOf(prevP)}" rel="prev"><span class="muted small">Previous</span>${esc(prevP.short)}</a>` : '<span></span>'}
        ${nextP ? `<a href="${hrefOf(nextP)}" rel="next"><span class="muted small">Next</span>${esc(nextP.short)}</a>` : '<span></span>'}
      </nav>`);
    View.pieceId = p.id;
    const root = main;
    const isActive = () => Player.isActive(p, version);
    let score = null, timing = null, strip = null, sv = null, viewQ = 0, viewSrcKey = null, destroyed = false;

    // Load the score (and strip), then attach the score view.
    const ready = Promise.all([loadJSON(d.score), !earlier && p.strip ? loadJSON(p.strip).catch(() => null) : Promise.resolve(null)]).then(([sc, st]) => {
      if (destroyed) return;
      score = sc; timing = makeTiming(sc); strip = st;
      const t = params.get('t');
      const pending = Player.pendingFor(p, version);
      if (pending) return pending;
      if (!isActive() && !Player.playing && !Player.pending) {
        return Player.load(p, version, { posSec: t != null ? +t : undefined, sourceKey: params.get('src') || undefined });
      }
      if (isActive() && t != null) Player.seekScoreSec(+t);
      viewQ = timing.qOf(savedPos(p, version));
    }).then(() => {
      if (destroyed || !score) return;
      sv = new ScoreView($('.score-host', root), { score, timing, strip, onSeek: q => { activate().then(() => Player.seekQ(q)); } });
      renderEntries(); sync(); kick();
    }).catch(err => { $('.status', root).textContent = 'Could not load this piece: ' + err.message; });

    function activate(autoplay) {
      if (isActive()) { if (autoplay) Player.play(); return Promise.resolve(); }
      const pending = Player.pendingFor(p, version);
      if (pending) return pending.then(() => { if (autoplay) Player.play(); });
      return Player.load(p, version, { sourceKey: viewSrcKey || undefined, autoplay: !!autoplay, posSec: timing ? timing.secOf(viewQ) : undefined });
    }

    // Sources
    const srcBox = $('.sources', root);
    const srcs = sourcesOf(p, version);
    srcBox.innerHTML = srcs.map(s => `<button type="button" role="radio" aria-checked="false" data-src="${esc(s.key)}" class="chip${s.entry && s.entry.headphones ? ' phones' : ''}${s.type === 'synth' ? ' synth' : ''}">${s.entry && s.entry.headphones ? ICON.phones : ''}${esc(s.label)}</button>`).join('');
    $$('[data-src]', srcBox).forEach(b => b.addEventListener('click', () => {
      const key = b.dataset.src; store.set('source', key);
      if (isActive()) Player.setSource(key);
      else { viewSrcKey = key; activate(true); }
    }));
    function renderSources() {
      const cur = isActive() && Player.source ? Player.source.key : (viewSrcKey || chooseSource(srcs).key);
      $$('[data-src]', srcBox).forEach(b => { const on = b.dataset.src === cur; b.setAttribute('aria-checked', String(on)); b.tabIndex = on ? 0 : -1; });
      const sel = srcs.find(s => s.key === cur);
      const hint = $('.hint', root);
      if (sel && sel.entry && sel.entry.headphones) {
        hint.hidden = false;
        hint.innerHTML = `${ICON.phones}<span>${sel.key === 'walk' ? 'Use headphones: you walk round the quartet, and halfway the room turns into its mirror image.' : 'Use headphones: each voice is placed around you, so the lines stay distinct.'}</span>`;
      } else if (sel && sel.entry && sel.entry.start_q != null) {
        hint.hidden = false; hint.textContent = 'A short excerpt (bars 66–72) for comparing the two tunings; the score follows it.';
      } else if (sel && sel.type === 'synth') {
        hint.hidden = false; hint.textContent = 'Live synth: a simple keyboard sound made in your browser from the score, in any temperament, with any voice soloed or muted.';
      } else hint.hidden = true;
    }
    srcBox.addEventListener('keydown', e => {   // arrow keys move within the radio group
      if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(e.key)) return;
      const bs = $$('[data-src]', srcBox); const i = bs.indexOf(document.activeElement); if (i < 0) return;
      e.preventDefault(); e.stopPropagation();
      const j = (i + (e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? -1 : 1) + bs.length) % bs.length; bs[j].focus();
    });

    // Transport
    const playBtn = $('.play-btn', root), seek = $('.seek', root), clock = $('.clock', root);
    playBtn.addEventListener('click', () => { if (isActive()) Player.toggle(); else activate(true); });
    $$('[data-seek]', root).forEach(b => b.addEventListener('click', () => activate().then(() => Player.seekBy(+b.dataset.seek))));
    $$('[data-skip]', root).forEach(b => b.addEventListener('click', () => activate().then(() => Player.skip(+b.dataset.skip))));
    let seeking = false;
    seek.addEventListener('input', () => { seeking = true; activate().then(() => { const tl = Player.timeline(); Player.seekTimeline(seek.value / 1000 * tl.dur); seeking = false; }); });
    $$('[data-queue]', root).forEach(b => b.addEventListener('click', () => { Player.queue = b.dataset.queue; sync(); }));
    $$('[data-version]', root).forEach(b => b.addEventListener('click', () => {
      const v = b.dataset.version; if (v === version) return;
      navigate(hrefOf(p, v), true);
    }));

    // Synth panel
    const tempsBox = $('.temps', root);
    tempsBox.innerHTML = Object.keys(CAT.temps).map(k => `<button type="button" data-temp="${k}">${esc(TNAMES[k] || k)}</button>`).join('');
    $$('[data-temp]', tempsBox).forEach(b => b.addEventListener('click', () => { Synth.temp = b.dataset.temp; store.set('temp', Synth.temp); Synth.restart(); syncSynth(); }));
    const tempo = $('.tempo input', root);
    tempo.value = Math.round(Synth.tempo * 100); $('.tempoval', root).textContent = tempo.value + '%';
    tempo.addEventListener('input', () => { const w = Synth.playing; if (w) Synth.stop(); Synth.tempo = tempo.value / 100; $('.tempoval', root).textContent = tempo.value + '%'; if (w) Synth.play(); kick(); });
    function syncSynth() {
      const show = isActive() && Player.source && Player.source.type === 'synth';
      $('.synth-panel', root).hidden = !show;
      if (!show || !score) return;
      $$('[data-temp]', tempsBox).forEach(b => b.setAttribute('aria-pressed', String(b.dataset.temp === Synth.temp)));
      $('.tnote', root).textContent = !Synth.hasCents ? (TBLURB[Synth.temp] || '')
        : Synth.tagged === Synth.flat.length ? 'Every note of this movement carries its own tuning (just intonation), so the temperament buttons do not change it.'
          : `${Synth.tagged} of ${Synth.flat.length} notes carry their own tuning (natural harmonics) and keep it; the temperament applies to the rest. ${TBLURB[Synth.temp] || ''}`;
      const vb = $('.voices', root);
      if (vb.dataset.for !== Synth.key) {
        vb.dataset.for = Synth.key;
        vb.innerHTML = score.voices.map((v, i) => `<button type="button" class="voice" data-voice="${i}" aria-label="${esc(v.n)}: playing"><span class="sw" style="background:var(--v${1 + i % 9})"></span><span class="nm">${esc(v.n)}</span><span class="st">on</span></button>`).join('');
        $$('[data-voice]', vb).forEach(b => b.addEventListener('click', () => { Synth.cycleVoice(+b.dataset.voice); Synth.restart(); syncSynth(); kick(); }));
      }
      $$('[data-voice]', vb).forEach(b => {
        const i = +b.dataset.voice, st = Synth.state[i] || 'on', aud = Synth.audible(i);
        b.dataset.state = st; b.classList.toggle('silent', !aud);
        $('.st', b).textContent = st === 'on' ? (aud ? 'on' : 'off') : st;
        b.setAttribute('aria-label', `${score.voices[i].n}: ${st === 'solo' ? 'solo' : st === 'muted' ? 'muted' : aud ? 'playing' : 'silent'}`);
      });
    }

    function renderEntries() {
      const box = $('.entries', root), sec = $('.entries-sec', root);
      if (!score.entries.length) { sec.hidden = true; return; }
      sec.hidden = false;
      $('.entries-count', sec).textContent = `(${score.entries.length}; tap one to jump there)`;
      box.innerHTML = score.entries.slice(0, 120).map((en, k) => { const v = score.voices[en[0]]; return `<button type="button" class="entry" data-entry="${k}"><span class="bar">b${timing.barOf(en[1])}</span><span class="sw" style="background:var(--v${1 + en[0] % 9})"></span>${esc(v ? v.a : '')} <span class="lab">${esc(en[2])}</span></button>`; }).join('');
      $$('[data-entry]', box).forEach(b => b.addEventListener('click', () => { const en = score.entries[+b.dataset.entry]; activate().then(() => Player.seekQ(en[1])); }));
    }

    // Notes
    if (earlier) {
      Promise.all([d.readme_md ? loadText(d.readme_md) : Promise.resolve(''), Promise.resolve(p.notes)]).then(([readme]) => {
        if (destroyed) return;
        $('.about .notes', root).innerHTML = (readme ? md(readme.replace(/^#.*\n/, ''), dirOf(d.readme_md)) : '') +
          `<p class="small muted">The current version: ${esc(p.voices)} voices, ${fmt(p.duration)}. <a href="${hrefOf(p)}">Back to the current version</a>.</p>`;
      });
    }
    const det = $('.notes-details', root);
    if (det) det.addEventListener('toggle', () => {
      if (!det.open || det.dataset.loaded) return; det.dataset.loaded = '1';
      const path = earlier ? d.notes_md : p.notes_md;
      loadText(path).then(t => { if (!destroyed) $('.md', det).innerHTML = md(t, dirOf(path)); }).catch(() => { $('.md', det).innerHTML = '<p class="error">Could not load the notes.</p>'; });
    });
    $$('video', root).forEach(v => v.addEventListener('play', () => { if (Player.playing) Player.pause(); }));

    // Keep the view in step with the player.
    function sync() {
      const act = isActive();
      renderSources();
      const playing = act && Player.playing;
      playBtn.innerHTML = playing ? ICON.pause : ICON.play;
      playBtn.setAttribute('aria-label', playing ? 'Pause' : 'Play');
      playBtn.classList.toggle('playing', playing);
      $$('[data-queue]', root).forEach(b => b.setAttribute('aria-pressed', String(b.dataset.queue === Player.queue)));
      const st = $('.status', root);
      if (act && Player.error) st.textContent = Player.error;
      else if (!act && Player.piece && Player.playing) st.innerHTML = `Now playing elsewhere: <a href="${hrefOf(Player.piece, Player.version)}">${esc(pieceLabel(Player.piece))}</a>. Press play to switch to this piece.`;
      else if (act && Player.resumedAt && !Player.playing) st.innerHTML = `Resuming at ${fmt(Player.resumedAt)}. <button type="button" class="linkish" data-restart>Start from the beginning</button>`;
      else st.textContent = '';
      const rb = $('[data-restart]', st); if (rb) rb.addEventListener('click', () => { Player.resumedAt = 0; Player.seekScoreSec(0); sync(); });
      syncSynth();
      frame();
    }
    function frame() {
      if (!timing) return;
      const act = isActive();
      const q = act ? Player.q() : viewQ;
      if (sv) sv.update(q, act && Player.playing);
      let cur, dur;
      if (act) ({ cur, dur } = Player.timeline());
      else { cur = timing.secOf(viewQ); dur = timing.total; }
      if (!seeking && document.activeElement !== seek) seek.value = String(dur ? Math.round(cur / dur * 1000) : 0);
      seek.setAttribute('aria-valuetext', `${fmt(cur)} of ${fmt(dur)}, bar ${timing.barOf(q)}`);
      clock.textContent = `bar ${timing.barOf(q)} · ${fmt(cur)} / ${fmt(dur)}`;
    }
    listeners.add(sync);
    View.frame = frame;
    View.destroy = () => { destroyed = true; listeners.delete(sync); if (sv) sv.destroy(); };
    renderSources(); sync();
    return ready;
  }
  function downloadName(p, e) {
    const g = groupOf(p);
    const prefix = g.kind === 'pair' ? `wtc-${String(g.num).padStart(2, '0')}` : `wtc-${g.kind}`;
    return `${prefix}-${e.src.includes('/archive-n-plus-1/') ? 'earlier-' : ''}${e.file}`;
  }

  // ------------------------------------------------------------------------------------------
  // Mini player (whenever the playing piece is not the page on screen)
  // ------------------------------------------------------------------------------------------
  const Mini = {
    el: document.getElementById('mini'),
    init() {
      this.el.innerHTML = `<div class="mini-progress"><span></span></div>
        <div class="mini-row">
          <button type="button" class="play-btn small" aria-label="Play">${ICON.play}</button>
          <a class="mini-title" href="#/"></a>
          <button type="button" class="icon-btn" data-mini-next aria-label="Next piece">${ICON.next}</button>
        </div>`;
      $('.play-btn', this.el).addEventListener('click', () => Player.toggle());
      $('[data-mini-next]', this.el).addEventListener('click', () => Player.skip(1));
      listeners.add(() => this.update());
    },
    update() {
      const show = !!Player.piece && Player.touched && View.pieceId !== Player.piece.id;
      this.el.hidden = !show; document.body.classList.toggle('has-mini', show);
      if (!show) return;
      const p = Player.piece;
      const a = $('.mini-title', this.el); a.href = hrefOf(p, Player.version);
      a.innerHTML = `<strong>${esc(pieceLabel(p))}</strong><span class="muted small">${esc(groupLabel(groupOf(p)))}${Player.source ? ' · ' + esc(Player.source.label) : ''}</span>`;
      const b = $('.play-btn', this.el); b.innerHTML = Player.playing ? ICON.pause : ICON.play; b.setAttribute('aria-label', Player.playing ? 'Pause' : 'Play');
      this.frame();
    },
    frame() {
      if (this.el.hidden || !Player.piece) return;
      const tl = Player.timeline(); $('.mini-progress span', this.el).style.width = (tl.dur ? clamp(tl.cur / tl.dur, 0, 1) * 100 : 0) + '%';
    },
  };

  // ------------------------------------------------------------------------------------------
  // Theme, keyboard, boot
  // ------------------------------------------------------------------------------------------
  function initTheme() {
    const btn = document.getElementById('theme');
    const names = { auto: 'Theme: follows the system', light: 'Theme: light', dark: 'Theme: dark' };
    const apply = t => {
      if (t === 'auto') delete document.documentElement.dataset.theme; else document.documentElement.dataset.theme = t;
      btn.setAttribute('aria-label', names[t] + ' (change)'); btn.title = names[t]; btn.dataset.mode = t;
      kick();
    };
    let t = store.get('theme', 'auto'); apply(t);
    btn.addEventListener('click', () => { t = t === 'auto' ? 'light' : t === 'light' ? 'dark' : 'auto'; store.set('theme', t); apply(t); });
  }
  document.addEventListener('keydown', e => {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    const t = e.target, tag = t && t.tagName;
    if (tag === 'TEXTAREA' || tag === 'SELECT' || (t && t.isContentEditable)) return;
    if (tag === 'INPUT' && t.type !== 'range') return;
    const k = e.key;
    const onControl = tag === 'BUTTON' || tag === 'A' || tag === 'SUMMARY' || tag === 'INPUT';
    const viewPlay = () => { const b = View.name === 'piece' ? $('.player-panel .play-btn', main) : null; if (b) b.click(); else if (Player.piece) Player.toggle(); };
    if ((k === ' ' && !onControl) || k === 'k' || k === 'K') { e.preventDefault(); viewPlay(); }
    else if ((k === 'ArrowLeft' || k === 'ArrowRight') && tag !== 'INPUT' && !t.closest('[role=radiogroup]') && Player.piece) { e.preventDefault(); Player.seekBy(k === 'ArrowLeft' ? -5 : 5); }
    else if ((k === 'j' || k === 'l') && Player.piece) { e.preventDefault(); Player.seekBy(k === 'j' ? -10 : 10); }
    else if ((k === 'n' || k === 'p') && Player.piece) { e.preventDefault(); Player.skip(k === 'n' ? 1 : -1); }
  });

  async function boot() {
    initTheme();
    try { CAT = await loadJSON('catalog.json'); }
    catch (e) { main.innerHTML = '<section class="hero"><h1>The Well-Tempered clAIvier</h1><p class="error">Could not load catalog.json. Build the site with <code>python3 tools/build_app.py --link</code> and serve the _site folder.</p></section>'; return; }
    ORDER = CAT.groups.flatMap(g => g.pieces);
    for (const id of ORDER) ROUTES[P(id).route] = id;
    for (const g of CAT.groups) if (g.route) ROUTES[g.route] = g.pieces[0];
    Mini.init();
    window.addEventListener('hashchange', route);
    route();
  }
  boot();
})();
