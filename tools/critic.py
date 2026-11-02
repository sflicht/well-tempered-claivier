#!/usr/bin/env python3
"""Contrapuntal critic for JSON event scores.

It reports concrete, bar-located evidence. It does not certify music.

Checks
  parallels      parallel/consecutive P5 and P8/P1 between *every* pair of
                 voices, independent of voice order (the older chk.py assumed
                 the lower-numbered voice was always higher, so it missed
                 fifths between crossed voices and flagged fourths instead).
  direct         hidden 5ths/8ves into the outer voices with a leaping top.
  dissonance     every beat-level dissonance, classified as suspension,
                 chord seventh, accented passing/appoggiatura, pedal friction,
                 or UNRESOLVED. A resolution counts only if the step comes
                 within a beat and lands on a consonance with the partner;
                 a step that cannot be verified (partner moves to another
                 dissonance or falls silent) is 'unverified', not 'ok'.
  melody         augmented seconds, tritone and seventh leaps, leaps beyond
                 an octave, unrecovered large leaps, compound same-way leaps.
  crossing       sustained crossings between adjacent voices.
  texture        real voices per bar, octave-doubling detection, pedal notes.
  themes         verifies each declared subject entry against the subject.
  keyboard       whether the sounding notes fit two hands (<=5 notes and a
                 <=10th span per hand).
  reach          fresh attacks only (held notes can be caught by a pedal):
                 notes struck together that no split between two hands can
                 reach (span > 16 semitones in a hand). Reported for every
                 score; it matters for the solo-keyboard ones.

Parallels between the same pair are merged into one row per run, keeping the
worst severity and the number of transitions. Only a run of octaves/unisons
between voices the score declares as doublings (metadata 'doublings':
[[voiceA, voiceB], ...], or a voice's 'doubles': name) is exempted.
  harmony        per-beat chord labels, longest static harmony.

Usage: critic.py score.json [--json out.json] [--bars 12-20] [--quiet]
"""
from __future__ import annotations

import argparse
import collections
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from chords import chord_candidates, name_chord, pname  # noqa: E402

TPQ = 48  # ticks per quarter note
LETTER = {'c': 0, 'd': 1, 'e': 2, 'f': 3, 'g': 4, 'a': 5, 'b': 6}


def ticks(x):
    return int(round(float(x) * TPQ))


class Score:
    def __init__(self, data):
        self.data = data
        self.meta = data.get('metadata', data.get('meta', {}))
        m = self.meta.get('meter', [4, 4])
        if isinstance(m, str):
            m = [int(v) for v in m.split('/')]
        self.num, self.den = int(m[0]), int(m[1])
        self.bar = ticks(self.num * 4 / self.den)
        compound = self.den == 8 and self.num % 3 == 0
        self.beat = ticks(1.5) if compound else ticks(4 / self.den)
        if self.den == 2:
            self.beat = ticks(2)
        self.voices = []
        self.names = []
        for i, v in enumerate(data['voices']):
            evs = []
            for e in sorted(v['events'], key=lambda e: float(e['t'])):
                if e.get('p') is None:
                    continue
                evs.append({'s': ticks(e['t']), 'e': ticks(float(e['t']) + float(e['d'])),
                            'p': int(e['p']), 'spell': e.get('spell'), 'th': e.get('th'),
                            'label': e.get('label')})
            self.voices.append(evs)
            self.names.append(v.get('abbr') or v.get('name', f'V{i+1}')[:3])
        alias = {}
        for i, v in enumerate(data['voices']):
            for key in (v.get('name'), v.get('abbr'), self.names[i]):
                if key:
                    alias[key] = self.names[i]
        self.doublings = set()
        for a, b in self.meta.get('doublings', []):
            if a in alias and b in alias:
                self.doublings.add(frozenset((alias[a], alias[b])))
        for i, v in enumerate(data['voices']):
            if v.get('doubles') in alias:
                self.doublings.add(frozenset((self.names[i], alias[v['doubles']])))
        inst = str(self.meta.get('instrument', '')).lower()
        self.solo_keyboard = any(w in inst for w in ('piano', 'keyboard')) and \
            not any(w in inst for w in ('organ', 'open score', 'strings', 'shepard', 'players'))
        self.end = max((n['e'] for v in self.voices for n in v), default=0)
        self.nbars = math.ceil(self.end / self.bar) if self.bar else 0
        self.flats = any(ch in str(self.meta.get('key', '')) for ch in 'b') or \
            (self.meta.get('mode') == 'minor' and self.meta.get('key') in ('C', 'D', 'G', 'F'))
        self.onsets = sorted({n['s'] for v in self.voices for n in v})
        self._idx = [0] * len(self.voices)

    # --- time helpers ---------------------------------------------------
    def loc(self, t):
        b = t // self.bar
        r = (t % self.bar) / TPQ
        return f"b{b+1}.{r + 1:g}"

    def strength(self, t):
        r = t % self.bar
        if r == 0:
            return 3
        if r % self.beat == 0:
            return 2
        if r % (self.beat // 2 if self.beat % 2 == 0 else self.beat) == 0:
            return 1
        return 0

    def sounding(self, t):
        """{voice: (note, attacked_now)} for every voice sounding at tick t."""
        out = {}
        for i, v in enumerate(self.voices):
            # binary search would be nicer; linear with cached index is fine
            lo, hi = 0, len(v)
            while lo < hi:
                mid = (lo + hi) // 2
                if v[mid]['s'] <= t:
                    lo = mid + 1
                else:
                    hi = mid
            k = lo - 1
            if k >= 0 and v[k]['s'] <= t < v[k]['e']:
                out[i] = (k, v[k]['s'] == t)
        return out

    def note(self, i, k):
        return self.voices[i][k]

    def next_note(self, i, k):
        v = self.voices[i]
        return v[k + 1] if k + 1 < len(v) else None

    def prev_note(self, i, k):
        return self.voices[i][k - 1] if k > 0 else None


def iclass(a, b):
    return abs(a - b) % 12


def is_perfect(a, b):
    c = iclass(a, b)
    return c in (0, 7)


def check_parallels(S, rng=None):
    out = []
    nv = len(S.voices)
    for i in range(nv):
        for j in range(i + 1, nv):
            times = sorted({n['s'] for n in S.voices[i]} | {n['s'] for n in S.voices[j]})
            prev = None
            for t in times:
                snd = S.sounding(t)
                if i not in snd or j not in snd:
                    prev = None
                    continue
                ki, _ = snd[i]
                kj, _ = snd[j]
                a, b = S.note(i, ki)['p'], S.note(j, kj)['p']
                if prev is not None:
                    pki, pkj, pa, pb, pt = prev
                    # successive notes only: a rest longer than a beat breaks the line
                    gap_i = S.note(i, ki)['s'] - S.note(i, pki)['e'] if ki != pki else 0
                    gap_j = S.note(j, kj)['s'] - S.note(j, pkj)['e'] if kj != pkj else 0
                    if gap_i > S.beat or gap_j > S.beat:
                        prev = (ki, kj, a, b, t)
                        continue
                    moved_i = ki != pki and a != pa
                    moved_j = kj != pkj and b != pb
                    if moved_i and moved_j and is_perfect(pa, pb) and is_perfect(a, b) \
                            and iclass(pa, pb) == iclass(a, b):
                        same_dir = (a - pa) * (b - pb) > 0
                        kind = 'P8' if iclass(a, b) == 0 else 'P5'
                        strong = min(S.strength(t), S.strength(pt))
                        sev = 'error' if same_dir and strong >= 2 else ('warn' if same_dir else 'note')
                        if not same_dir:
                            kind = 'contrary ' + kind
                        out.append({'t': t, 'loc': S.loc(t), 'voices': (S.names[i], S.names[j]),
                                    'kind': kind, 'sev': sev,
                                    'what': f"{pname(pa, S.flats)}/{pname(pb, S.flats)} -> {pname(a, S.flats)}/{pname(b, S.flats)}"})
                prev = (ki, kj, a, b, t)
    return collapse_runs(out, S.doublings)


SEV_RANK = {'ok': 0, 'note': 1, 'warn': 2, 'error': 3}


def collapse_runs(items, declared=frozenset()):
    """Merge consecutive parallels between the same pair into one row per run.

    The row keeps the worst severity among its transitions ('count' of them,
    'errors' of which were errors), so merging reduces rows, never the
    classification. Only an octave/unison run between a pair declared as a
    doubling is relabelled 'doubling'."""
    items.sort(key=lambda x: (x['voices'], x['t']))
    out = []
    for it in items:
        if out and out[-1]['voices'] == it['voices'] and it['t'] - out[-1].get('t_last', out[-1]['t']) <= 2 * TPQ \
                and out[-1]['kind'].split()[-1] == it['kind'].split()[-1]:
            o = out[-1]
            o['count'] += 1
            o['errors'] += it['sev'] == 'error'
            o['t_last'] = it['t']
            if SEV_RANK[it['sev']] > SEV_RANK[o['sev']]:
                o['sev'] = it['sev']
            continue
        out.append(dict(it, count=1, errors=int(it['sev'] == 'error')))
    for o in out:
        base = o['kind']
        if o['count'] >= 3:
            o['kind'] = f"run ({base} x{o['count']})"
        if base.split()[-1] == 'P8' and not base.startswith('contrary') and frozenset(o['voices']) in declared:
            o['sev'] = 'doubling'
    out.sort(key=lambda x: x['t'])
    return out


def check_beat_parallels(S):
    """Accented parallels: P5/P8 on successive beats between the same pair,
    both voices having moved, even when passing notes intervene (BWV 869: 1 in
    76 bars; BWV 878: 0)."""
    out = []
    nv = len(S.voices)
    beats = list(range(0, S.end, S.beat))
    snds = [S.sounding(t) for t in beats]
    for i in range(nv):
        for j in range(i + 1, nv):
            for k in range(1, len(beats)):
                a0, a1 = snds[k - 1], snds[k]
                if not (i in a0 and j in a0 and i in a1 and j in a1):
                    continue
                pa, pb = S.note(i, a0[i][0])['p'], S.note(j, a0[j][0])['p']
                qa, qb = S.note(i, a1[i][0])['p'], S.note(j, a1[j][0])['p']
                if pa == qa or pb == qb:
                    continue
                if is_perfect(pa, pb) and is_perfect(qa, qb) and iclass(pa, pb) == iclass(qa, qb) \
                        and (qa - pa) * (qb - pb) > 0:
                    out.append({'t': beats[k], 'loc': S.loc(beats[k]), 'sev': 'warn',
                                'voices': (S.names[i], S.names[j]),
                                'kind': 'beat-to-beat ' + ('P8' if iclass(qa, qb) == 0 else 'P5'),
                                'what': f"{pname(pa, S.flats)}/{pname(pb, S.flats)} -> {pname(qa, S.flats)}/{pname(qb, S.flats)}"})
    return collapse_runs(out, S.doublings)


def sonority_stats(S):
    """Doubling and low-register clash measures on beats/attacks."""
    tripled = beats = 0
    for t in range(0, S.end, S.beat):
        ps = [S.note(i, k)['p'] for i, (k, _) in S.sounding(t).items()]
        if len(ps) >= 3:
            beats += 1
            c = collections.Counter(p % 12 for p in ps)
            if max(c.values()) >= 3:
                tripled += 1
    # Doublings that matter: the seventh of a seventh chord, or the third of a
    # dominant seventh (the leading tone), sounding in two or more voices.
    bad = []
    for t in range(0, S.end, S.beat):
        ps = [S.note(i, k)['p'] for i, (k, _) in S.sounding(t).items()]
        if len(ps) < 3:
            continue
        cnt = collections.Counter(p % 12 for p in ps)
        cands = chord_candidates(set(cnt), min(ps) % 12)
        if not cands:
            continue
        root, q = cands[0]
        seventh = {'7': 10, 'm7': 10, 'ø7': 10, 'o7': 9, 'maj7': 11, '7(no5)': 10, 'm(no5)7': 10}.get(q)
        if seventh is not None and cnt[(root + seventh) % 12] >= 2:
            bad.append(S.loc(t) + ' 7th')
        if q in ('7', '7(no5)') and cnt[(root + 4) % 12] >= 2:
            bad.append(S.loc(t) + ' leading tone')
    low = []
    for t in S.onsets:
        snd = S.sounding(t)
        ps = sorted((S.note(i, k)['p'], i, att) for i, (k, att) in snd.items())
        for x in range(len(ps)):
            for y in range(x + 1, len(ps)):
                a, b = ps[x][0], ps[y][0]
                if b < 55 and (b - a) in (1, 2, 10, 11, 13, 14) and (ps[x][2] or ps[y][2]):
                    low.append(S.loc(t))
    return {'pc_tripled_on_beats_pct': round(100 * tripled / max(1, beats), 1),
            'bad_doublings': len(bad), 'bad_doubling_examples': bad[:12],
            'low_register_seconds': len(low), 'low_register_examples': sorted(set(low))[:12]}


def check_direct(S):
    out = []
    prev = None
    for t in S.onsets:
        snd = S.sounding(t)
        if len(snd) < 2:
            prev = None
            continue
        notes = [(S.note(i, k)['p'], i, k) for i, (k, _) in snd.items()]
        top = max(notes)
        bot = min(notes)
        if prev is not None:
            ptop, pbot = prev
            if top[1] == ptop[1] and bot[1] == pbot[1] and top[2] != ptop[2] and bot[2] != pbot[2]:
                if is_perfect(top[0], bot[0]) and not is_perfect(ptop[0], pbot[0]):
                    dt, db = top[0] - ptop[0], bot[0] - pbot[0]
                    if dt * db > 0 and abs(dt) > 2 and S.strength(t) >= 2:
                        out.append({'t': t, 'loc': S.loc(t), 'sev': 'note',
                                    'what': f"direct {'8ve' if iclass(top[0], bot[0]) == 0 else '5th'} "
                                            f"{S.names[top[1]]}/{S.names[bot[1]]} top leaps {dt:+d}"})
        prev = (top, bot)
    return out


def is_dissonant(lo, hi, lo_is_bass):
    c = iclass(lo, hi)
    if c in (1, 2, 10, 11):
        return True
    if c == 5 and lo_is_bass:
        return True
    if c == 6:
        return True
    return False


def step(a, b):
    return b is not None and 1 <= abs(b - a) <= 2


def pitch_at(S, i, t):
    k = S.sounding(t).get(i)
    return None if k is None else S.note(i, k[0])['p']


def continuation(S, i, k, partner):
    """How note k of voice i leaves a dissonance against voice `partner`.

    'resolved'   the next note follows within a beat, by step, and is
                 consonant with the partner's note sounding then (or, if the
                 partner has fallen silent, with the bass);
    'unverified' it steps on time but lands on another dissonance while the
                 partner also moved (parallel seconds, change of bass, chains):
                 the step alone does not show a resolution;
    None         no timely step (a rest, a leap, or the end)."""
    n = S.note(i, k)
    nxt = S.next_note(i, k)
    if nxt is None or not step(n['p'], nxt['p']) or nxt['s'] - n['e'] > S.beat:
        return None
    t = nxt['s']
    snd = S.sounding(t)
    pp = pitch_at(S, partner, t)
    if pp is None:
        others = [S.note(j, kk)['p'] for j, (kk, _) in snd.items() if j != i]
        if not others:
            return 'resolved'
        pp = min(others)
    lo, hi = min(pp, nxt['p']), max(pp, nxt['p'])
    bass = min(S.note(j, kk)['p'] for j, (kk, _) in snd.items())
    if not is_dissonant(lo, hi, lo == bass):
        return 'resolved'
    partner_moved = partner in snd and snd[partner][1]
    return 'unverified' if partner_moved else None


def prepared(S, i, k, partner):
    """A held dissonance is a prepared suspension only if it was consonant
    with the partner when it was struck (or the partner was silent then)."""
    n = S.note(i, k)
    pp = pitch_at(S, partner, n['s'])
    if pp is None:
        return True
    snd = S.sounding(n['s'])
    bass = min(S.note(j, kk)['p'] for j, (kk, _) in snd.items())
    lo, hi = min(pp, n['p']), max(pp, n['p'])
    return not is_dissonant(lo, hi, lo == bass)


def check_dissonance(S):
    """Classify beat-level dissonances."""
    out = []
    pedal_len = 2 * S.bar
    for t in S.onsets:
        if S.strength(t) < 2:
            continue
        snd = S.sounding(t)
        if len(snd) < 2:
            continue
        items = [(S.note(i, k)['p'], i, k, att) for i, (k, att) in snd.items()]
        items.sort()
        bass = items[0][0]
        pcs = {p % 12 for p, *_ in items}
        cands = chord_candidates(pcs, bass % 12)
        chord_ok = bool(cands)
        seventh_chord = chord_ok and cands[0][1] in ('7', 'o7', 'ø7', 'm7', 'maj7', '7(no5)', 'm(no5)7')
        for x in range(len(items)):
            for y in range(x + 1, len(items)):
                lo, ilo, klo, alo = items[x]
                hi, ihi, khi, ahi = items[y]
                if not is_dissonant(lo, hi, lo == bass):
                    continue
                if not (alo or ahi):
                    continue  # both held: was evaluated when attacked
                nlo, nhi = S.note(ilo, klo), S.note(ihi, khi)
                if (nlo['e'] - nlo['s']) >= pedal_len or (nhi['e'] - nhi['s']) >= pedal_len:
                    kind = 'pedal'
                elif chord_ok and iclass(lo, hi) in (6, 10, 11, 1, 2, 5) and seventh_chord:
                    # chord member: check the seventh resolves down by step
                    root = cands[0][0]
                    sev_pc = {'7': 10, 'm7': 10, 'ø7': 10, 'o7': 9, 'maj7': 11, '7(no5)': 10, 'm(no5)7': 10}[cands[0][1]]
                    kind = 'chord'
                    for p, i, k, a in items:
                        if (p - root) % 12 == sev_pc:
                            nxt = S.next_note(i, k)
                            if nxt is not None and nxt['s'] - S.note(i, k)['e'] <= S.beat and \
                                    not (-2 <= nxt['p'] - p <= 0):
                                kind = 'chord (7th not resolved down)'
                elif chord_ok and iclass(lo, hi) in (5, 6):
                    kind = 'chord'  # 6/4 or diminished triad
                else:
                    held, new = (None, None)
                    if alo and not ahi:
                        held, new = (ihi, khi, hi), (ilo, klo, lo)
                    elif ahi and not alo:
                        held, new = (ilo, klo, lo), (ihi, khi, hi)
                    if held:
                        hi_, hk, hp = held
                        ni, nk, np_ = new
                        res = continuation(S, hi_, hk, ni)
                        if res == 'resolved':
                            nxt = S.next_note(hi_, hk)
                            kind = 'suspension' if nxt['p'] < hp else 'retardation'
                            if not prepared(S, hi_, hk, ni):
                                kind += ' (unprepared)'
                        else:
                            res2 = continuation(S, ni, nk, hi_)
                            if res2 == 'resolved':
                                kind = 'accented passing'
                            elif 'unverified' in (res, res2):
                                kind = 'unverified stepwise continuation'
                            else:
                                kind = 'UNRESOLVED (held)'
                    else:
                        r = {continuation(S, ilo, klo, ihi), continuation(S, ihi, khi, ilo)}
                        if 'resolved' in r:
                            kind = 'appoggiatura'
                        elif 'unverified' in r:
                            kind = 'unverified stepwise continuation'
                        else:
                            kind = 'UNPREPARED+UNRESOLVED'
                out.append({'t': t, 'loc': S.loc(t), 'kind': kind,
                            'sev': 'error' if kind.startswith('UN') else
                            'unverified' if kind.startswith('unverified') else
                            'note' if ('7th not' in kind or 'unprepared' in kind) else 'ok',
                            'what': f"{S.names[ilo]}{pname(lo, S.flats)}/{S.names[ihi]}{pname(hi, S.flats)}"})
    return out


def letter_dist(sp1, sp2, p1, p2):
    if not sp1 or not sp2:
        return None
    o1 = (p1 - (sp1.count('is') - sp1.count('es') - (1 if sp1 in ('as', 'es') else 0)))
    l1 = LETTER[sp1[0]] + 7 * (o1 // 12)
    o2 = (p2 - (sp2.count('is') - sp2.count('es') - (1 if sp2 in ('as', 'es') else 0)))
    l2 = LETTER[sp2[0]] + 7 * (o2 // 12)
    return abs(l2 - l1)


def check_melody(S):
    out = []
    for i, v in enumerate(S.voices):
        for k in range(1, len(v)):
            a, b = v[k - 1], v[k]
            if b['s'] - a['e'] > S.beat:  # separated by a real rest
                continue
            iv = b['p'] - a['p']
            ab = abs(iv)
            loc = S.loc(b['s'])
            nm = f"{S.names[i]} {pname(a['p'], S.flats)}->{pname(b['p'], S.flats)}"
            if ab == 3:
                ld = letter_dist(a.get('spell'), b.get('spell'), a['p'], b['p'])
                if ld == 1:
                    out.append({'t': b['s'], 'loc': loc, 'sev': 'warn', 'kind': 'augmented 2nd', 'what': nm})
            if ab == 6:
                out.append({'t': b['s'], 'loc': loc, 'sev': 'warn', 'kind': 'tritone leap', 'what': nm})
            if ab in (10, 11):
                out.append({'t': b['s'], 'loc': loc, 'sev': 'warn', 'kind': 'seventh leap', 'what': nm})
            if ab > 12:
                out.append({'t': b['s'], 'loc': loc, 'sev': 'warn', 'kind': 'leap > octave', 'what': nm})
            if k + 1 < len(v) and v[k + 1]['s'] - b['e'] <= S.beat:
                c = v[k + 1]
                iv2 = c['p'] - b['p']
                if ab >= 5 and abs(iv2) >= 5 and iv * iv2 > 0 and abs(iv + iv2) > 12:
                    out.append({'t': b['s'], 'loc': loc, 'sev': 'note', 'kind': 'compound same-way leap',
                                'what': nm + f"->{pname(c['p'], S.flats)}"})
                if ab >= 8 and not (iv * iv2 < 0) and (b['e'] - b['s']) <= S.beat:
                    out.append({'t': b['s'], 'loc': loc, 'sev': 'note', 'kind': 'large leap not recovered',
                                'what': nm + f"->{pname(c['p'], S.flats)}"})
    return out


def check_crossing(S):
    """Crossings between voices adjacent in register (ordered by mean pitch,
    so the check does not depend on the order voices are listed in)."""
    out = []
    nv = len(S.voices)
    order = sorted((i for i in range(nv) if S.voices[i]),
                   key=lambda i: -sum(n['p'] for n in S.voices[i]) / len(S.voices[i]))
    for a in range(len(order) - 1):
        i, j = order[a], order[a + 1]
        start = None
        for t in S.onsets + [S.end]:
            snd = S.sounding(t) if t < S.end else {}
            crossed = i in snd and j in snd and S.note(j, snd[j][0])['p'] > S.note(i, snd[i][0])['p']
            if crossed and start is None:
                start = t
            elif not crossed and start is not None:
                if t - start >= S.beat:
                    out.append({'t': start, 'loc': S.loc(start), 'sev': 'note',
                                'what': f"{S.names[j]} above {S.names[i]} for {(t - start) / TPQ:g} beats"})
                start = None
    return out


def texture(S):
    rows = []
    for b in range(S.nbars):
        b0, b1 = b * S.bar, (b + 1) * S.bar
        active = []
        for i, v in enumerate(S.voices):
            notes = [n for n in v if n['s'] < b1 and n['e'] > b0]
            dur = sum(min(n['e'], b1) - max(n['s'], b0) for n in notes)
            attacks = [n for n in notes if n['s'] >= b0]
            if dur >= S.bar * 0.25:
                kind = 'line'
                if not attacks:
                    kind = 'held'
                active.append((i, kind, attacks))
        # doubling: two active voices whose attacks coincide and intervals are all P8/P1
        doubled = set()
        for x in range(len(active)):
            for y in range(x + 1, len(active)):
                i, _, ai = active[x]
                j, _, aj = active[y]
                if len(ai) >= 2 and len(ai) == len(aj) and all(p['s'] == q['s'] and iclass(p['p'], q['p']) == 0
                                                             for p, q in zip(ai, aj)):
                    doubled.add(j)
        real = [i for i, kind, _ in active if kind == 'line' and i not in doubled]
        held = [i for i, kind, _ in active if kind == 'held']
        rows.append({'bar': b + 1, 'active': len(active), 'moving': len(real), 'held': len(held),
                     'doubled': len(doubled),
                     'who': ''.join(S.names[i][0] if i in real else ('-' if i in held else ('=' if i in doubled else '.'))
                                    for i in range(len(S.voices)))})
    return rows


def keyboard(S, max_span=16, max_notes=5):
    bad = []
    maxn = 0
    for t in S.onsets:
        ps = sorted(S.note(i, k)['p'] for i, (k, _) in S.sounding(t).items())
        maxn = max(maxn, len(ps))
        ok = False
        for split in range(0, len(ps) + 1):
            L, R = ps[:split], ps[split:]
            if len(L) > max_notes or len(R) > max_notes:
                continue
            if L and L[-1] - L[0] > max_span:
                continue
            if R and R[-1] - R[0] > max_span:
                continue
            ok = True
            break
        if not ok:
            bad.append({'t': t, 'loc': S.loc(t), 'what': ' '.join(pname(p, S.flats) for p in ps)})
    return {'max_simultaneous': maxn, 'unplayable_onsets': len(bad), 'onsets': len(S.onsets),
            'examples': bad[:12]}


def hand_split(ps, span, per_hand=5):
    """Smallest achievable 'largest hand span' for keys struck together."""
    ps = sorted(set(ps))
    best = None
    for k in range(len(ps) + 1):
        L, R = ps[:k], ps[k:]
        if len(L) > per_hand or len(R) > per_hand:
            continue
        m = max(L[-1] - L[0] if L else 0, R[-1] - R[0] if R else 0)
        best = m if best is None else min(best, m)
    return best if best is not None else 99


def reach(S, span=16):
    """Fresh attacks that no division between two hands can reach.

    Only notes struck at the same instant count: a held note can be caught by
    the sustain or sostenuto pedal, but the hand still has to strike every new
    key. Write a roll or an anticipation as separate onsets if one is meant."""
    by_t = collections.defaultdict(list)
    for v in S.voices:
        for n in v:
            by_t[n['s']].append(n['p'])
    out = []
    for t in sorted(by_t):
        need = hand_split(by_t[t], span)
        if need > span:
            out.append({'t': t, 'loc': S.loc(t), 'sev': 'error', 'span': need,
                        'what': ' '.join(pname(p, S.flats) for p in sorted(set(by_t[t])))})
    return out


def harmony(S):
    rows = []
    static = (0, None, None)
    run = 0
    last = None
    run_start = 0
    fit = tot = 0
    for t in range(0, S.end, S.beat):
        pcs = collections.Counter()
        lows = []
        for i, v in enumerate(S.voices):
            for n in v:
                if n['s'] < t + S.beat and n['e'] > t:
                    w = min(n['e'], t + S.beat) - max(n['s'], t)
                    pcs[n['p'] % 12] += w + (S.beat if n['s'] <= t else 0)
                    lows.append(n['p'])
        if not pcs:
            rows.append(None)
            continue
        bass = min(lows) % 12
        keep = {pc for pc, w in pcs.items() if w >= S.beat * 0.5}
        name = name_chord(keep, bass, S.flats) or name_chord(set(pcs), bass, S.flats)
        tot += 1
        if name:
            fit += 1
        rows.append(name)
        key = (frozenset(keep), bass)
        if key == last:
            run += 1
        else:
            if run > static[0]:
                static = (run, S.loc(run_start), rows[-2] if len(rows) > 1 else None)
            run, run_start, last = 1, t, key
    if run > static[0]:
        static = (run, S.loc(run_start), rows[-1])
    return {'labels': rows, 'tertian_fit_pct': round(100 * fit / max(1, tot), 1),
            'longest_static_beats': static[0], 'longest_static_at': static[1]}


def load_subject(data):
    subj = data.get('subject')
    if subj:
        return [(ticks(n['d']), int(n['p'])) for n in subj]
    return None


def check_themes(S, data):
    subj = load_subject(data)
    entries = data.get('subject_entries', [])
    if not subj or not entries:
        return None
    sd0 = [d for d, _ in subj]
    si0 = [subj[k + 1][1] - subj[k][1] for k in range(len(subj) - 1)]
    res = []
    for e in entries:
        # An entry may declare form 'retrograde' (cancrizans): it is then checked against the
        # subject read backwards (rectus = retrograde, inversus = retrograde inversion).
        # Entries without a 'form' key are checked exactly as before.
        sd, si = sd0, si0
        if str(e.get('form', '')).startswith('retrograde'):
            rs = list(reversed(subj))
            sd = [d for d, _ in rs]
            si = [rs[k + 1][1] - rs[k][1] for k in range(len(rs) - 1)]
        vi = int(e['voice'])
        t0 = ticks(e['t'])
        v = S.voices[vi]
        k0 = next((k for k, n in enumerate(v) if n['s'] == t0), None)
        if k0 is None:
            res.append({'loc': S.loc(t0), 'voice': S.names[vi], 'label': e.get('label'), 'match': 'NO NOTE AT ENTRY'})
            continue
        best = None
        for scale in (1, 2, 4, 0.5):
            notes = v[k0:k0 + len(subj)]
            if len(notes) < len(subj):
                continue
            dur = [n['e'] - n['s'] for n in notes]
            rhythm_ok = sum(1 for a, b in zip(dur[:-1], sd[:-1]) if abs(a - b * scale) <= 1)
            iv = [notes[k + 1]['p'] - notes[k]['p'] for k in range(len(notes) - 1)]
            rect = sum(1 for a, b in zip(iv, si) if a == b)
            inv = sum(1 for a, b in zip(iv, si) if abs(a + b) <= 1)
            for kind, m in (('rectus', rect), ('inversus', inv)):
                score = m + rhythm_ok
                if best is None or score > best[0]:
                    best = (score, kind, scale, m, rhythm_ok)
        if best:
            score, kind, scale, m, r = best
            if str(e.get('form', '')).startswith('retrograde'):
                kind = 'retrograde' if kind == 'rectus' else 'retrograde inversus'
            res.append({'loc': S.loc(t0), 'voice': S.names[vi], 'label': e.get('label'), 'form': kind,
                        'scale': scale, 'intervals_ok': f"{m}/{len(si)}", 'rhythm_ok': f"{r}/{len(sd) - 1}"})
    return res


def analyse(data, bars=None):
    S = Score(data)
    R = {'title': S.meta.get('subtitle', S.meta.get('title')), 'bars': S.nbars, 'voices': len(S.voices),
         'meter': f"{S.num}/{S.den}", 'bpm': S.meta.get('bpm'),
         'duration_s': round(S.end / TPQ * 60 / float(S.meta.get('bpm', 80)), 1)}
    par = check_parallels(S)
    dis = check_dissonance(S)
    mel = check_melody(S)
    R['parallels'] = par
    R['direct'] = check_direct(S)
    R['beat_parallels'] = check_beat_parallels(S)
    R['sonority'] = sonority_stats(S)
    R['dissonance'] = dis
    R['melody'] = mel
    R['crossing'] = check_crossing(S)
    R['texture'] = texture(S)
    R['keyboard'] = keyboard(S)
    R['reach'] = reach(S)
    R['harmony'] = harmony(S)
    R['themes'] = check_themes(S, data)
    ranges = {}
    for i, v in enumerate(S.voices):
        if v:
            ranges[S.names[i]] = f"{pname(min(n['p'] for n in v), S.flats)}-{pname(max(n['p'] for n in v), S.flats)} ({len(v)} notes)"
    R['ranges'] = ranges
    if bars:
        lo, hi = bars
        for k in ('parallels', 'beat_parallels', 'direct', 'dissonance', 'melody', 'crossing', 'reach'):
            R[k] = [x for x in R[k] if lo <= x['t'] // S.bar + 1 <= hi]
    steps = leaps = reps = nint = 0
    for v in S.voices:
        for a, b in zip(v, v[1:]):
            if b['s'] - a['e'] > S.beat:
                continue
            iv = abs(b['p'] - a['p'])
            nint += 1
            steps += 1 <= iv <= 2
            leaps += iv >= 5
            reps += iv == 0
    c = collections.Counter
    R['summary'] = {
        # melodic profile: Bach's fugues (BWV 869/878) move by step ~71-75%, leap a 4th+ ~14%;
        # lines built from chord tones leap far more.
        'stepwise_pct': round(100 * steps / max(1, nint), 1),
        'leap_4th_plus_pct': round(100 * leaps / max(1, nint), 1),
        'repeated_note_pct': round(100 * reps / max(1, nint), 1),
        'parallels_error': sum(1 for x in par if x['sev'] == 'error'),
        'parallels_error_transitions': sum(x['errors'] for x in par if x['sev'] == 'error'),
        'parallels_weak': sum(1 for x in par if x['sev'] == 'warn'),
        'doubling_runs': sum(1 for x in par if x['sev'] == 'doubling'),
        'beat_parallels': sum(1 for x in R['beat_parallels'] if x['sev'] != 'doubling'),
        'pc_tripled_on_beats_pct': R['sonority']['pc_tripled_on_beats_pct'],
        'bad_doublings': R['sonority']['bad_doublings'],
        'low_register_seconds': R['sonority']['low_register_seconds'],
        'dissonance_unresolved': sum(1 for x in dis if x['sev'] == 'error'),
        'dissonance_unverified': sum(1 for x in dis if x['sev'] == 'unverified'),
        'dissonance_kinds': dict(c(x['kind'] for x in dis)),
        'melody': dict(c(x['kind'] for x in mel)),
        'crossings': len(R['crossing']),
        'mean_moving_voices': round(sum(r['moving'] for r in R['texture']) / max(1, len(R['texture'])), 2),
        'bars_with_all_voices_moving': sum(1 for r in R['texture'] if r['moving'] == len(S.voices)),
        'keyboard_unplayable_pct': round(100 * R['keyboard']['unplayable_onsets'] / max(1, R['keyboard']['onsets']), 1),
        'solo_keyboard': S.solo_keyboard,
        'reach_errors': len(R['reach']),
        'tertian_fit_pct': R['harmony']['tertian_fit_pct'],
        'longest_static_harmony_beats': R['harmony']['longest_static_beats'],
    }
    return R


def print_report(R, quiet=False):
    print(f"== {R['title']} | {R['bars']} bars, {R['voices']} voices, {R['meter']} q={R['bpm']} (~{R['duration_s']}s)")
    print('summary:', json.dumps(R['summary'], ensure_ascii=False))
    print('ranges:', R['ranges'])
    if quiet:
        return
    print('-- parallels (error = same direction, both on beats):')
    for x in R['parallels']:
        if x['sev'] in ('error', 'warn', 'doubling'):
            print(f"   [{x['sev']}] {x['loc']} {x['voices'][0]}/{x['voices'][1]} {x['kind']}: {x['what']}")
    print('-- beat-to-beat (accented) parallels, passing notes between:')
    for x in R['beat_parallels']:
        print(f"   [{x['sev']}] {x['loc']} {x['voices'][0]}/{x['voices'][1]} {x['kind']}: {x['what']}")
    if R['sonority']['low_register_examples']:
        print('-- low-register seconds/sevenths/ninths at:', ', '.join(R['sonority']['low_register_examples']))
    print('-- unresolved / problem dissonances:')
    for x in R['dissonance']:
        if x['sev'] != 'ok':
            print(f"   [{x['sev']}] {x['loc']} {x['kind']}: {x['what']}")
    print('-- melody:')
    for x in R['melody']:
        if x['sev'] == 'warn':
            print(f"   {x['loc']} {x['kind']}: {x['what']}")
    if R['crossing']:
        print('-- crossings:', '; '.join(f"{x['loc']} {x['what']}" for x in R['crossing'][:15]))
    print('-- texture (moving voices per bar):', ' '.join(str(r['moving']) for r in R['texture']))
    kb = R['keyboard']
    print(f"-- keyboard: max {kb['max_simultaneous']} notes, {kb['unplayable_onsets']}/{kb['onsets']} onsets exceed two hands",
          '; '.join(f"{e['loc']} {e['what']}" for e in kb['examples'][:4]))
    if R['reach'] and R['summary']['solo_keyboard']:
        print(f"-- reach: {len(R['reach'])} attacks no two hands can strike:",
              '; '.join(f"{e['loc']} {e['what']} (needs {e['span']})" for e in R['reach'][:8]))
    h = R['harmony']
    print(f"-- harmony: tertian fit {h['tertian_fit_pct']}%, longest static {h['longest_static_beats']} beats at {h['longest_static_at']}")
    if R['themes']:
        print('-- themes:')
        for x in R['themes']:
            print('  ', x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('score', type=Path)
    ap.add_argument('--json', type=Path)
    ap.add_argument('--bars')
    ap.add_argument('--quiet', action='store_true')
    a = ap.parse_args()
    data = json.loads(a.score.read_text())
    bars = tuple(int(x) for x in a.bars.split('-')) if a.bars else None
    R = analyse(data, bars)
    print_report(R, a.quiet)
    if a.json:
        a.json.write_text(json.dumps(R, indent=1, ensure_ascii=False, default=str))


if __name__ == '__main__':
    try:
        main()
    except BrokenPipeError:
        pass
