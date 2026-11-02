#!/usr/bin/env python3
"""Verify the 24 Bach quotations of Prelude XXIV.

1. Score check (always): each head entry in prelude.json (metadata 'head_entries') sounds
   exactly Bach's head from metadata 'bach_heads', transposed by the stated octaves and with
   the stated rhythm factor (pitch and duration of every note and rest; the last note may be
   held longer).
2. --kern DIR: compares every head with the opening solo statement in the MuseData/Humdrum
   kern files wtc1f01.krn ... wtc1f24.krn (https://github.com/humdrum-tools/bach-wtc, kern/).
3. --midi DIR: compares pitches (enharmonically) and durations with Mutopia MIDI files named
   BWV<number>_*.mid whose name contains 'fug' or ends in 'b.mid' (the fugue of the pair).

Downloaded files are only read as data.  Run with python3 -I.
"""
import argparse
import json
import re
import sys
from fractions import Fraction as F
from pathlib import Path

NAT = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
ORDER = ['C', 'c', 'C#', 'c#', 'D', 'd', 'Eb', 'eb', 'E', 'e', 'F', 'f',
         'F#', 'f#', 'G', 'g', 'Ab', 'g#', 'A', 'a', 'Bb', 'bb', 'B', 'b']


def tok(t):
    name, d = t.rsplit(':', 1)
    d = F(d.rstrip('~'))
    if name == 'R':
        return None, d
    m = re.fullmatch(r'([A-G])(#{0,2}|b{0,2})(-?\d+)', name)
    L, acc, o = m.groups()
    return 12 * (int(o) + 1) + NAT[L] + acc.count('#') - acc.count('b'), d


def head_notes(head, octv=0, factor='1'):
    return [(None if p is None else p + 12 * octv, d * F(factor)) for p, d in map(tok, head.split())]


def score_check(data):
    heads = data['metadata']['bach_heads']
    voices = [v['events'] for v in data['voices']]
    bad = 0
    for e in data['metadata']['head_entries']:
        h = heads[e['key']]
        want = head_notes(h['head'], h['octave_shift'], h['rhythm'])
        ev = sorted(voices[e['voice']], key=lambda x: x['t'])
        t, got = F(e['t']).limit_denominator(64), []
        k = next(i for i, x in enumerate(ev) if abs(x['t'] - float(t)) < 1e-6)
        while len(got) < len(want) and k < len(ev):
            x = ev[k]
            st = F(x['t']).limit_denominator(64)
            if st > t:                                   # a rest
                got.append((None, (st - t) * 4))
                t = st
                continue
            got.append((x['p'], F(x['d']).limit_denominator(64) * 4))
            t = st + F(x['d']).limit_denominator(64)
            k += 1
        ok = got[:-1] == want[:-1] and got[-1][0] == want[-1][0] and got[-1][1] >= want[-1][1]
        bad += not ok
        print(f"{e['key']:3s} BWV {h['bwv']}  {len(want):2d} notes  score {'OK' if ok else 'MISMATCH'}")
    return bad


def kern_note(tk):
    tk = tk.split(' ')[0]
    m = re.match(r'^[\[\(\{]*(\d+)(\.*)', tk)
    if not m:
        return None
    dur = F(16, int(m.group(1)))
    add = dur
    for _ in m.group(2):
        add /= 2
        dur += add
    if 'r' in tk:
        return None, dur, False
    letters = re.search(r'([a-gA-G])\1*', tk).group(0)
    octv = 3 + len(letters) if letters[0].islower() else 4 - len(letters)
    acc = re.search(re.escape(letters) + r'([#\-n]*)', tk).group(1)
    p = 12 * (octv + 1) + NAT[letters[0].upper()] + acc.count('#') - acc.count('-')
    return p, dur, ('_' in tk or ']' in tk)


def kern_opening(path, n):
    """The first n notes (rests skipped, tied notes merged) of the first voice to enter."""
    rows = [ln.split('\t') for ln in path.read_text().splitlines()
            if ln and not ln.startswith(('!', '*', '='))]
    col = next(i for r in rows for i, x in enumerate(r) if x != '.' and 'r' not in x and re.search('[a-gA-G]', x))
    out = []
    for r in rows:
        x = r[col] if col < len(r) else '.'
        if x == '.':
            continue
        nt = kern_note(x)
        if nt is None:
            continue
        p, d, cont = nt
        if p is None:
            continue
        if cont and out and out[-1][0] == p:
            out[-1] = (p, out[-1][1] + d)
            continue
        if len(out) >= n:
            break
        out.append((p, d))
    return out


def midi_opening(path, n):
    import mido
    f = mido.MidiFile(path)
    notes = []
    for tr in f.tracks:
        t, on = 0, {}
        for m in tr:
            t += m.time
            if m.type == 'note_on' and m.velocity > 0:
                on[(m.channel, m.note)] = t
            elif m.type in ('note_off', 'note_on') and (m.channel, m.note) in on:
                s = on.pop((m.channel, m.note))
                notes.append((s, t - s, m.note))
    notes.sort()
    q = f.ticks_per_beat
    out = []
    for s, d, p in notes:
        if out and s < out[-1][0] + out[-1][1] * 0.9:
            break                                       # a second voice has entered
        out.append((s, d, p))
    return [(p, F(round(d / q * 8), 2)) for s, d, p in out][:n]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('score', nargs='?', default=Path(__file__).resolve().parent / 'prelude.json', type=Path)
    ap.add_argument('--kern', type=Path)
    ap.add_argument('--midi', type=Path)
    a = ap.parse_args()
    data = json.loads(a.score.read_text())
    bad = score_check(data)
    heads = data['metadata']['bach_heads']
    if a.kern:
        for i, k in enumerate(ORDER, 1):
            notes = [x for x in head_notes(heads[k]['head']) if x[0] is not None]
            got_notes = kern_opening(a.kern / f'wtc1f{i:02d}.krn', len(notes))
            ok = got_notes == notes
            bad += not ok
            print(f"{k:3s} kern wtc1f{i:02d}.krn  {'OK' if ok else 'MISMATCH ' + str(got_notes)}")
    if a.midi:
        for k in ORDER:
            bwv = heads[k]['bwv']
            files = [p for p in sorted(a.midi.glob(f'BWV{bwv}_*.mid'))
                     if 'fug' in p.name.lower() or p.name.lower().endswith('b.mid')]
            if not files:
                print(f"{k:3s} midi  (no Mutopia fugue file)")
                continue
            notes = [x for x in head_notes(heads[k]['head']) if x[0] is not None]
            got = midi_opening(files[0], len(notes))
            pitch_ok = [p for p, d in got] == [p for p, d in notes][:len(got)]
            # MIDI note-offs are performance lengths: compare durations within a sixteenth
            dur_ok = all(abs(dg - dw) <= 1 or dg <= dw for (pg, dg), (pw, dw) in zip(got, notes))
            ok = pitch_ok and dur_ok and len(got) >= min(len(notes), 7)
            bad += not ok
            print(f"{k:3s} midi {files[0].name:32s} {len(got):2d} notes  {'OK' if ok else 'MISMATCH ' + str(got)}")
    print('mismatches:', bad)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
