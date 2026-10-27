#!/usr/bin/env python3
"""Fugue IX in E major, ten voices: "Ricercar a 10 in circulo".

Stile antico (alla breve, white notes and quarters) meets Tallis's forty-part
Spem in alium.  Ten real voices sit in a ring round the listener, in score
order: Choir I (S1 A1 T1 Bar1 B1) on the left half, from behind-left to
front-left; Choir II (S2 A2 T2 Bar2 B2) on the right half, from front-right to
behind-right.  Index order = ring order (tools/render_spatial.py --layout ring).

Subject (ours): B4 | E5~ | E5 D#5 | C#5 B4 A4 G#4 | A4 B4 -- it rises a fourth,
holds across the barline (a ready-made suspension), falls a sixth and climbs
back to the note it started on: a circle.  Its inversion answers it.
Ancestor: BWV 878's subject E F# A G# F# E (J. S. Bach, WTC II/9, borrowed from
J. C. F. Fischer's Ariadne musica), used as a genuine voice: in augmentation as
the bass of the first tutti (b19-25), at normal speed in Bach's own answer form
above it (b19-22), in A major for Choir II (b31-34), and in augmentation as the
treble cantus firmus of the final tutti (b39-45).

Every note is written here.  Statements are explicit transforms of the written
subject (dshift = diatonic transposition in E major; W.invert_diatonic;
W.scale_rhythm; W.transpose); all other material is literal token strings
placed at bar.quarter positions.  No code chooses pitches.  The entry paths and
head placements were found with throwaway scans (pairwise consonance of a
proposed placement, like tools/stretto_finder.py); the free counterpoint was
written by hand and corrected against tools/critic.py.
"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (2, 2)
NAMES = ['S1', 'A1', 'T1', 'Bar1', 'B1', 'S2', 'A2', 'T2', 'Bar2', 'B2']
LONG = ['Soprano I', 'Alto I', 'Tenor I', 'Baritone I', 'Bass I',
        'Soprano II', 'Alto II', 'Tenor II', 'Baritone II', 'Bass II']
CLEF = ['treble', 'treble', 'treble_8', 'bass', 'bass', 'treble', 'treble', 'treble_8', 'bass', 'bass']
SC = [4, 6, 8, 9, 11, 1, 3]          # E major from the tonic

S = 'B4:8 E5:16 D#5:8 C#5:4 B4:4 A4:4 G#4:4 A4:8 B4:8'   # the subject (its E is tied across the barline)
F = 'E4:16 F#4:8 A4:8 G#4:8 F#4:8 E4:8'                  # BWV 878 / Fischer (final note's length free)


def dshift(toks, steps):
    """Diatonic transposition within E major by `steps` scale degrees (explicit, letter-preserving)."""
    out = []
    for t in toks.split():
        p, d, sp, tie = W.parse_tok(t)
        if p is None:
            out.append(t)
            continue
        pc = p % 12
        deg = ((p - 4) // 12) * 7 + SC.index(pc)
        nd = deg + steps
        q = 4 + (nd // 7) * 12 + ((SC[nd % 7] - 4) % 12)
        nl = 'CDEFGAB'[('CDEFGAB'.index(sp[0].upper()) + steps) % 7]
        out.append(f"{W.name_of(q, nl)}:{t.rsplit(':', 1)[1]}")
    return ' '.join(out)


I = W.invert_diatonic(S, 'B4', SC)
VO = {n: [] for n in NAMES}
ENTRIES = []


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


def pos(bar, q):
    return Fr(bar - 1) * 16 + (Fr(q) - 1) * 4


def put(v, bar, q, toks):
    VO[v].append((pos(bar, q), toks))


def theme(v, bar, q, toks, label, nbars=None):
    put(v, bar, q, toks)
    n = nbars if nbars is not None else max(1, round(float(dur16(toks)) / 16))
    ENTRIES.append((v, bar, (Fr(q) - 1), label, n))


def assemble(v, nbars):
    segs = sorted(VO[v], key=lambda x: x[0])
    out, cur = [], Fr(0)
    for s, toks in segs:
        if s < cur:
            raise ValueError(f'{v}: overlap at bar {float(s / 16 + 1)}: {toks[:40]}')
        if s > cur:
            out.append(f'R:{s - cur}')
        out.append(toks)
        cur = s + dur16(toks)
    total = Fr(nbars * 16)
    if cur > total:
        raise ValueError(f'{v}: runs past the end')
    if cur < total:
        out.append(f'R:{total - cur}')
    return W.concat_bars(' '.join(out), METER)


# ---- exposition entries
theme('S1', 1, 1, S, 'S on B')
theme('A1', 3, 1, dshift(I, -3), 'I on F#')
theme('T1', 5, 1, dshift(I, -6), 'I on C#')
theme('Bar1', 7, 1, dshift(I, -11), 'I on E')
theme('B1', 9, 1, dshift(I, -14), 'I on B')
theme('S2', 11, 1, dshift(S, 3), 'S on E')
theme('A2', 13, 1, dshift(S, -6), 'S on C#')
theme('T2', 15, 1, dshift(S, -10), 'S on F#')
theme('Bar2', 17, 1, dshift(S, -7), 'S on B')

# ---- exposition: free continuations
put('S1', 5, 1, 'C#5:8 B4:16 C#5:8 E5:8 F#5:16 E5:8 B4:8 A4:16 G#4:8 C#5:24 D#5:8 C#5:8 B4:16 R:8 '
                 'B4:8 E5:16 C#5:8 E5:8 C#5:24')                                                   # b5-18
put('A1', 7, 1, 'G#4:8 B4:8 B4:4 A4:4 G#4:8 F#4:8 D#4:16 E4:24 F#4:8 D#4:8 R:16 R:8 B4:8 R:8 G#4:8 '
                 'R:8 A4:8 B4:16 A4:16')                                                             # b7-18
put('T1', 10, 3, 'B3:8 A3:12 B3:4')                                                                  # b10.3-11
put('T1', 16, 1, 'E4:16 R:8 A3:8')                                                                   # b16-17
put('Bar1', 12, 1, 'A3:8 B3:8 F#3:24 G#3:8')                                                         # b12-14
put('B1', 13, 1, 'A2:8 B2:16 G#2:8 B2:8 E2:8 G#2:8 F#2:8 G#2:8 C#3:16 B2:8')                         # b13-18 bass
put('S2', 15, 1, 'F#5:8 G#5:16 E5:8 G#5:8 A5:16 F#5:8')                                              # b15-18
put('A2', 18, 1, 'F#4:8 B3:8')

# ---- FIRST TUTTI (b19-25): ten voices over the ancestor in augmentation
theme('S1', 19, 1, 'B4:16 C#5:8 E5:8 D#5:8 C#5:8 B4:8', "BWV 878 answer at normal speed (Bach's answer form)", 4)
put('S1', 22, 3, 'D#5:8 E5:16 F#5:8 B4:8 E5:16')
theme('T1', 19, 1, 'E4:8 A4:16 G#4:8', 'S head on E', 2)
put('T1', 21, 1, 'A4:16 R:16 G#4:16 R:16 E4:16')
put('B1', 19, 1, 'B2:8 R:8')
theme('B1', 20, 1, 'F#3:8 B3:16 A3:8', 'S head on F#', 2)
put('B1', 22, 1, 'B3:8 R:8 R:8 B2:24 G#2:16')
put('S2', 21, 1, 'C#6:24 B5:12 A5:4 G#5:4 A5:4 B5:4 C#6:4 B5:24')   # 9-8 over B7/A, then a quarter-note turn
put('A2', 19, 1, 'B3:16 E4:16')
theme('A2', 21, 3, 'C#4:8 F#4:16 E4:8', 'S head on C#', 2)
put('A2', 23, 3, 'E4:8 R:16 B3:16')
put('T2', 19, 1, 'G#3:8 R:8')
theme('T2', 22, 3, 'F#3:8 B3:16 A3:8', 'S head on F#', 2)
put('T2', 24, 3, 'A3:8 G#3:16')
put('Bar2', 21, 1, 'F#3:16')
theme('Bar2', 23, 1, 'B2:8 E3:16 D#3:8', 'S head on B', 2)
put('Bar2', 25, 1, 'E3:16')
put('A1', 19, 1, 'G#4:8 F#4:16 E4:4 D#4:4 C#4:4 D#4:4 E4:8 D#4:8 R:8 R:8')
theme('A1', 23, 3, 'B4:8 F#4:16 G#4:8', 'I head on B', 2)
put('A1', 25, 3, 'G#4:8')
put('Bar1', 19, 3, 'A2:8 C#3:8 B2:8 R:16 F#3:8 R:8 R:16 R:16 B2:16')
theme('B2', 19, 1, W.transpose(W.scale_rhythm(F, 2), -24, -14), 'BWV 878 subject (Fischer/Bach) in augmentation x2', 7)


# ---- b26: GENERAL PAUSE (Spem in alium's silence)

# ---- ANTIPHONAL HALVES (b27-36)
# Choir I (left half of the ring), pp, C-sharp minor: the subject on G# in the tenor
theme('T1', 27, 1, 'G#3:8 C#4:16 B3:8 A3:4 G#3:4 F#3:4 E3:4 F#3:8 G#3:8', 'S on G# (c#, Aeolian; Choir I)', 4)
put('B1', 27, 1, 'C#3:8 A2:8 F#2:8 G#2:8 C#3:8 A2:16 G#2:8')
put('S1', 27, 1, 'E5:16 F#5:8 E5:16 A4:8 C#5:8 B#4:8')
put('A1', 27, 1, 'G#4:8 A4:16 G#4:8 E4:8 F#4:16 D#4:8')
put('Bar1', 27, 1, 'E3:16 A3:8 E3:16 C#3:16 D#3:8')
# Choir II (right half) answers with Fischer/Bach's subject in A major (deceptive: V of c# -> VI)
theme('Bar2', 31, 1, 'A3:16 B3:8 D4:8 C#4:8 B3:8 A3:16', 'BWV 878 subject in A major (Choir II)', 4)
put('B2', 31, 1, 'A2:8 F#2:8 D3:16 A2:8 G#2:8 A2:16')
put('S2', 31, 1, 'C#5:16 D5:8 F#5:8 E5:8 D5:8 C#5:16')
put('A2', 31, 1, 'E4:16 D4:8 A4:16 B4:8 E4:16')
put('T2', 31, 1, 'C#4:16 F#3:8 A3:8 A3:8 E3:8 E3:16')
# Choir I again, closer: the subject's head on E over IV - ii7 - V7 - I (its held A becomes the 7th)
theme('T1', 34, 3, 'E4:8 A4:16 G#4:8', 'S head on E (Choir I)', 2)
put('B1', 34, 3, 'A2:8 F#2:8 B2:8 E2:8')
put('S1', 34, 3, 'C#5:16 B4:16')
put('A1', 34, 3, 'A4:8 E4:8 D#4:8 E4:8')
put('Bar1', 34, 3, 'C#3:8 A3:8 F#3:8 E3:8')

# the exchanges accelerate: Choir II answers (vi), Choir I (IV), Choir II (V), each half a bar; then both
put('S2', 36, 3, 'G#5:8 R:8 B5:8')
put('A2', 36, 3, 'C#5:8 R:8 F#4:8')
put('T2', 36, 3, 'E4:8 R:8 D#4:8')
put('Bar2', 36, 3, 'G#3:8 R:8 F#3:8')
put('B2', 36, 3, 'E3:8 R:8 B2:8')
put('S1', 37, 1, 'C#5:8')
put('A1', 37, 1, 'E4:8')
put('T1', 37, 1, 'A4:8')
put('Bar1', 37, 1, 'C#3:8')
put('B1', 37, 1, 'A2:8')
# the halves converge
put('S1', 38, 1, 'B4:8 D#5:8')
put('A1', 38, 1, 'E4:8 F#4:8')
put('T1', 38, 1, 'G#4:8')
put('Bar1', 38, 1, 'E3:8')
put('B1', 38, 1, 'E2:8 B2:8')
put('S2', 38, 1, 'G#5:8 F#5:8')
put('A2', 38, 3, 'B4:8')
put('T2', 38, 1, 'B3:16')
put('Bar2', 38, 3, 'F#3:8')


# ---- FINAL TUTTI (b39-49): the ancestor moves from the floor to the roof: BWV 878 x2 as the treble cantus
# firmus, while the head travels on round the ring beneath it: A1, T1, Bar1, T2, S2, A2, T2, and finally S1,
# where the fugue began (S2 rests in b39-40 so the cantus's E5 is on top).  Coda: a double plagal close
# (bVII - IV - I), a Mixolydian D natural six beats after the last D-sharp.  The ring empties in pairs, each
# pair re-striking its note pp before it leaves.
theme('S1', 39, 1, W.transpose(W.scale_rhythm(F, 2), 12, 7), 'BWV 878 subject x2 as treble cantus firmus', 7)
put('S1', 46, 1, 'F#5:16')
theme('S1', 47, 1, 'E5:8 A5:16 G#5:32', 'S head on E: the circle closes where it began', 2)
put('S1', 50, 3, 'G#5:8')
put('B2', 39, 1, 'E2:8 C#3:4 B2:4 A2:8 G#2:8 B2:8 A2:16 B2:8 E2:8 C#3:8 A2:8 B2:8 E2:8 A2:4 G#2:4 F#2:12 G#2:4 A2:16 E2:40 E2:8')
theme('A1', 39, 1, 'G#4:8 C#5:16 B4:8', 'S head on G#', 2)
put('A1', 41, 1, 'B4:8 F#4:8 E4:8 R:8 E4:4 F#4:4 G#4:8 C#5:4 B4:4 A4:8 G#4:8 C#5:8 D5:24 C#5:8 B4:16 B4:8')
theme('T1', 40, 1, 'E4:8 B3:16 C#4:8', 'I head on E', 2)
put('T1', 42, 1, 'A3:4 G#3:4 F#3:8 G#3:8 C#4:16 B3:8 E4:16 A3:32 B3:16 B3:8')
theme('Bar1', 41, 1, 'F#3:8 C#3:16 D#3:8', 'I head on F#', 2)
put('Bar1', 43, 1, 'E3:8 R:8 R:16 R:8 E3:8 D3:16 E3:8 C#3:8 R:32')
theme('T2', 42, 1, 'C#4:8 F#4:16 E4:8', 'S head on C#', 2)
put('T2', 39, 1, 'B3:8 C#4:12 D#4:4 E4:8')
put('T2', 44, 1, 'E4:8 R:8 R:8')
theme('T2', 45, 3, 'A3:8 D4:16 C#4:8', 'S head on A (D natural)', 2)
put('T2', 47, 3, 'C#4:8 G#4:32 G#4:8')
theme('S2', 43, 1, 'B4:8 E5:16 D#5:8', 'S head on B (home)', 2)
put('S2', 41, 3, 'C#5:16 B4:8')
put('S2', 45, 1, 'G#5:8 A5:16 D5:8 A4:8 E5:32 E5:8')
theme('A2', 44, 1, 'F#4:8 B4:16 A4:8', 'S head on F#', 2)
put('A2', 39, 1, 'B4:8 E4:8 A4:8 R:8 F#4:4 G#4:4 A4:8')
put('A2', 46, 1, 'A4:16 E4:48 E4:8')
put('Bar2', 39, 1, 'E3:24 E3:8 R:8 A3:8 E3:8 R:8 B3:16 A3:8 R:8 E3:8 C#3:8 R:16 R:8 E3:48 E3:8')
put('B1', 39, 1, 'B2:8 R:8 C#3:8 R:8')
put('B1', 43, 1, 'B2:8 R:8 R:16 B2:8 R:8 R:16 R:16 B2:24 B2:8')


LETTER = 'CDEFGAB'


def _steps_and_durs(toks):
    out = []
    for t in toks.split():
        p, d, sp, tie = W.parse_tok(t)
        if p is None:
            continue
        octave = (p - (sp.count('is') - sp.count('es'))) // 12 - 1
        out.append((LETTER.index(sp[0].upper()) + 7 * octave, d))
    return out


def verify_entries():
    """Check every declared statement against the subject, its inversion or BWV 878 by scale steps
    (letter names, so tonal mutations such as B#, D natural are reported as such) and rhythm."""
    refs = {'S': S, 'I': I, 'F': F, 'F (x2)': W.scale_rhythm(F, 2)}
    rows = []
    for v, bar, off, label, n in ENTRIES:
        toks = [t for s, t in VO[v] if s == pos(bar, 1 + off)][0]
        got = _steps_and_durs(toks)
        best = None
        for name, ref in refs.items():
            r = _steps_and_durs(ref)
            k = min(len(r), len(got))
            if k < 3:
                continue
            si = sum(1 for j in range(k - 1) if got[j + 1][0] - got[j][0] == r[j + 1][0] - r[j][0])
            rh = sum(1 for j in range(k - 1) if got[j][1] == r[j][1])
            sc = (si + rh) / (2 * (k - 1))
            if best is None or sc > best[0]:
                best = (sc, name, f'{si}/{k - 1}', f'{rh}/{k - 1}', k == len(r))
        rows.append((f'b{bar}.{1 + float(off):g}', v, label, best[1], best[2], best[3], 'complete' if best[4] else 'head'))
    return rows


def build(nbars):
    bars = {LONG[i]: assemble(n, nbars) for i, n in enumerate(NAMES)}
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'Fugue IX in E major, ten voices: Ricercar a 10 in circulo',
            'composer': 'Claude / Sam (with the subject of J. S. Bach, BWV 878, after J. C. F. Fischer)',
            'instrument': 'Ten keyboards in a ring (open score, two choirs)',
            'key': 'E', 'mode': 'major', 'meter': list(METER), 'bpm': 92, 'tempo_text': 'Alla breve, stile antico',
            'movement_number': 9, 'piece_type': 'fugue', 'edition': 'third',
            'spatial_layout': 'ring: voice index = position, Choir I left half, Choir II right half',
            # broad at the first tutti, held back into the general pause, a tempo for the antiphony,
            # broad again for the final tutti, and a long ritardando as the ring empties
            'tempo_map': [[72, 84], [94, 84], [100, 69, 'ramp'], [100, 69], [104, 90], [148, 90],
                          [152, 82, 'ramp'], [184, 82], [188, 69, 'ramp'], [200, 51, 'ramp']]}
    voices = [(LONG[i], NAMES[i], CLEF[i], 62) for i in range(len(NAMES))]
    dyn = {1: -8, 9: -4, 13: 0, 17: 4, 19: 12, 23: 14, 25: 10, 27: -14, 31: -10, 35: -4, 36: -8, 38: 0,
           39: 8, 43: 12, 45: 14, 47: 8, 49: -10, 50: -14}

    def dynamics(b):
        v = 0
        for k in sorted(dyn):
            if b + 1 >= k:
                v = dyn[k]
        return v
    ents = [(LONG[NAMES.index(v)], b, o, l, n) for v, b, o, l, n in ENTRIES]
    return W.build_score(HERE / 'fugue.json', meta, voices, bars, entries=ents,
                         subject='B4:8 E5:16 D#5:8 C#5:4 B4:4 A4:4 G#4:4 A4:8 B4:8', dynamics=dynamics,
                         extra={'entry_verification': [list(r) for r in verify_entries()]})


if __name__ == '__main__':
    end = max((s + dur16(t)) for v in VO.values() for s, t in v)
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else int(-(-end // 16))
    build(nb)
    print('bars', nb)
    for row in verify_entries():
        print('  %-7s %-5s %-62s %-7s steps %-6s rhythm %-6s %s' % row)
