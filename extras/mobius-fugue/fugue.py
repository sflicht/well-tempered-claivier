#!/usr/bin/env python3
"""Fuga sul nastro di Möbius (draft scaffolding; see NOTES.md)."""
from __future__ import annotations

import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (4, 4)
BAR = 16

V = [
    ('Vl1', 'Violino I', 'treble', 40, 72, (2.5, 6.5)),
    ('Vl2', 'Violino II', 'treble', 40, 70, (7.5, 6.5)),
    ('Va', 'Viola', 'alto', 41, 70, (7.5, 1.5)),
    ('Vc', 'Violoncello', 'bass', 42, 72, (2.5, 1.5)),
]
NAMES = [v[0] for v in V]
LONG = {v[0]: v[1] for v in V}

# ------------------------------------------------------------------ the mirror
LET = 'CDEFGAB'
NATMIN = [0, 2, 3, 5, 7, 8, 10]


def mirror(s, axis, tonic, shift=0):
    """Diatonic inversion in a minor key about `axis` (its third degree), as in Bach's
    Art of Fugue: 1<->5, 2<->4, 3 stays; the 6th and 7th degrees exchange so that a raised
    (melodic/harmonic) form becomes a natural one and vice versa (B<->Ab, A<->Bb in C minor),
    which keeps every semitone round the tonic and the dominant a semitone.  Other
    accidentals are mirrored exactly.  `shift` adds diatonic steps (7 = an octave)."""
    a_letter, a_oct = axis[0], int(axis.lstrip('ABCDEFG#b'))
    ai = LET.index(a_letter) + 7 * a_oct
    t_letter = tonic[0]
    t_pc = W.NAT[t_letter] + tonic.count('#') - tonic.count('b')
    assert (LET.index(a_letter) - LET.index(t_letter)) % 7 == 2, 'axis must be the third degree'
    out = []
    for tok in W._tokens(s):
        p, d, sp, tie = W.parse_tok(tok)
        if p is None:
            out.append(tok)
            continue
        L = sp[0].upper()
        octv = (p - (W.NAT[L] + (sp.count('is') - sp.count('es')))) // 12 - 1
        idx = LET.index(L) + 7 * octv
        deg = (LET.index(L) - LET.index(t_letter)) % 7
        nat_pc = (t_pc + NATMIN[deg]) % 12
        o = ((p % 12) - nat_pc + 6) % 12 - 6
        n = 2 * ai - idx + shift
        nl, no = LET[n % 7], n // 7
        ndeg = (LET.index(nl) - LET.index(t_letter)) % 7
        o2 = 1 - o if deg in (5, 6) else -o
        npc = (t_pc + NATMIN[ndeg]) % 12
        alter = (npc - W.NAT[nl] + 6) % 12 - 6 + o2
        acc = '#' * alter if alter > 0 else 'b' * (-alter)
        out.append(f"{nl}{acc}{no}:{tok.rsplit(':', 1)[1]}")
    return ' '.join(out)


def tr(s, semis, letters):
    return W.transpose(s, semis, letters)


# ------------------------------------------------------------------ material (C minor)
# Subject: the head is the opening of Bach's Thema Regium (Musical Offering, BWV 1079),
# C Eb G Ab B, compressed; the tail is new and is built so that it sounds against the first
# bar of the subject's own inversion (stretto per motum contrarium at one bar, finale).
S = 'C5:4 Eb5:2 G5:2 Ab5:4 B4:4 G5:1 F5:1 Eb5:1 D5:1 C5:1 D5:1 Eb5:1 C5:1 D5:2 B4:2 C5:4'
SI = mirror(S, 'Eb5', 'C')                       # inversus, same register
A = tr(S, -5, -3)                                # real answer, G minor (G4)
AI = mirror(A, 'Bb4', 'G')
# Countersubject, written against the answer (G minor), Violino I:
CS = ('R:2 Bb5:1 C6:1 D6:1 C6:1 Bb5:1 A5:1 G5:1 A5:1 Bb5:1 G5:1 A5:4 '
      'D6:4 Bb5:4 C6:2 A5:2 Bb5:4')
# its mirror keeps every vertical third/sixth/octave (double counterpoint at the double
# octave by contrary motion): reflected about Bb5, i.e. s -> 14 - s round the answer's axis.
CSI = mirror(CS, 'Bb4', 'G', 14)

VO = {n: [] for n in NAMES}
ENTRIES = []


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


def pos(bar, beat=1):
    return Fr(bar - 1) * BAR + (Fr(beat) - 1) * 4


def put(v, bar, beat, toks):
    VO[v].append((pos(bar, beat), ' '.join(toks.split())))


def theme(v, bar, beat, toks, label, nbars=2):
    put(v, bar, beat, toks)
    first = toks.split()[0]
    off = W.parse_tok(first)[1] if first.startswith('R:') else Fr(0)
    t = pos(bar, beat) + off
    b = int(t // BAR) + 1
    ENTRIES.append((LONG[v], b, (t - (b - 1) * BAR) / 4, label, nbars))


def assemble(v, nbars):
    segs = sorted(VO[v], key=lambda x: x[0])
    out, cur = [], Fr(0)
    for s, toks in segs:
        if s < cur:
            raise ValueError(f'{v}: overlap at bar {float(s / BAR + 1)}: {toks[:60]}')
        if s > cur:
            out.append(f'R:{s - cur}')
        out.append(toks)
        cur = s + dur16(toks)
    total = Fr(nbars * BAR)
    if cur > total:
        raise ValueError(f'{v}: runs past the end')
    if cur < total:
        out.append(f'R:{total - cur}')
    return W.concat_bars(' '.join(out), METER)


def oc(s, n):
    return W.transpose(s, 12 * n, 7 * n)


# =================================================================== LAP 1 (rectus)
def lap1_exposition():
    theme('Vl1', 1, 1, S, 'S (Vl I, C minor)')
    theme('Vl2', 3, 1, A, 'A (Vl II, G minor)')
    put('Vl1', 3, 1, CS)
    # codetta: the tail figure in Vl II over V7 of C minor
    put('Vl2', 5, 1, 'F4:1 Eb4:1 D4:1 C4:1 B3:1 C4:1 D4:1 B3:1 C4:2 Ab4:2 G4:4')
    put('Vl1', 5, 1, 'B5:4 D6:4 Eb6:2 C6:2 B5:4')
    theme('Va', 6, 1, oc(S, -1), 'S (Va, C minor)')
    put('Vl2', 6, 1, tr(CS, -7, -4))
    put('Vl1', 6, 1, 'C6:4 Bb5:4 Ab5:4 G5:4 B5:4 C6:4 Ab5:2 G5:6~')
    theme('Vc', 8, 1, oc(A, -2), 'A (Vc, G minor)')
    put('Va', 8, 1, oc(CS, -2))
    put('Vl1', 8, 1, 'G5:4 F5:4 Eb5:4 D5:4 F#5:4 G5:4 D6:2 C6:2 Bb5:4')
    put('Vl2', 8, 1, 'D5:4 Bb4:4 C5:4 A4:8 Bb4:4 F#4:2 D5:6')


def lap1_episode():
    # b10-12: the circle of fifths C - F - Bb - Eb - Ab - Bb7 (-> Eb).  The viola runs the
    # subject's tail, alternately rectus (falling) and inversus (rising), one half bar each:
    # the Moebius strip in miniature.  Violino II: a chain of prepared sevenths and a 4-3.
    put('Va', 10, 1, 'G4:1 F4:1 Eb4:1 D4:1 C4:1 D4:1 Eb4:1 C4:1 A3:1 Bb3:1 C4:1 D4:1 Eb4:1 D4:1 C4:1 Eb4:1 '
                     'F4:1 Eb4:1 D4:1 C4:1 Bb3:1 C4:1 D4:1 Bb3:1 G3:1 Ab3:1 Bb3:1 C4:1 D4:1 C4:1 Bb3:1 D4:1 '
                     'Eb4:1 D4:1 C4:1 Bb3:1 Ab3:1 Bb3:1 C4:1 Ab3:1 Bb3:1 C4:1 D4:1 Eb4:1 F4:1 Eb4:1 D4:1 F4:1')
    put('Vl2', 10, 1, 'R:4 Eb5:12 Eb5:4 D5:12 C5:8 Bb4:8')
    put('Vc', 10, 1, 'C3:4 G2:4 F2:4 C3:4 Bb2:4 F2:4 Eb2:4 Bb2:4 Ab2:4 F2:4 Bb2:8')


# Subject in E-flat major (III): the subject moved up a third inside the same seven notes
# (C minor's natural scale is E-flat major's), so B natural becomes D and the falling
# diminished seventh a minor seventh.
S_EB = 'Eb5:4 G5:2 Bb5:2 C6:4 D5:4 Bb5:1 Ab5:1 G5:1 F5:1 Eb5:1 F5:1 G5:1 Eb5:1 F5:2 D5:2 Eb5:4'
CS_EB_BELOW = ('R:2 G4:1 Ab4:1 Bb4:1 Ab4:1 G4:1 F4:1 Eb4:1 F4:1 G4:1 Eb4:1 F4:4 '
               'Bb4:4 G4:4 Ab4:2 F4:2 G4:4')     # the countersubject, two octaves down: below


def lap1_return():
    # b13-14: Violino I, the subject in E-flat major; the countersubject below it (Vl II)
    theme('Vl1', 13, 1, S_EB, 'S (Vl I, E-flat major)')
    put('Vl2', 13, 1, CS_EB_BELOW)
    put('Va', 13, 1, 'Bb3:4 Eb4:4 G3:4 Ab3:8 G3:4 C4:2 Ab3:2 G3:4')
    put('Vc', 13, 1, 'Eb3:4 G2:4 C3:2 F2:2 Bb2:4 D3:4 Eb3:4 Ab2:2 Bb2:2 Eb3:4')
    # b15-16: back to C minor (the deceptive C minor chord of b14.4 is its tonic), the tail
    # once more in the viola, a chromatic bass C Eb F F# G, and a half cadence: 6/4 - 5/3 on G.
    put('Vl1', 15, 1, 'G5:8 Ab5:4 A5:4 G5:16')
    put('Vl2', 15, 1, 'Eb5:8 C5:4 Eb5:4 Eb5:8 D5:8')
    put('Va', 15, 1, 'G4:1 F4:1 Eb4:1 D4:1 C4:1 D4:1 Eb4:1 D4:1 C4:16 B3:8')
    put('Vc', 15, 1, 'C3:4 Eb3:4 F3:4 F#3:4 G3:4 G2:12')
    # b17: general pause (the first seam)
    put('Vl1', 17, 1, 'R:16')


SECTIONS = [lap1_exposition, lap1_episode, lap1_return]


def build(path=None):
    VO.update({n: [] for n in NAMES})
    ENTRIES.clear()
    for f in SECTIONS:
        f()
    end = max((s + dur16(t) for segs in VO.values() for s, t in segs), default=0)
    nbars = int((end + BAR - 1) // BAR)
    bars = {LONG[n]: assemble(n, nbars) for n in NAMES}
    meta = {'title': 'The Well-Tempered clAIvier — extra',
            'subtitle': 'Fuga sul nastro di Möbius',
            'key': 'C', 'mode': 'minor', 'meter': list(METER), 'bpm': 66}
    voices = [(v[1], v[0], v[2], v[4]) for v in V]
    data = W.build_score(path or HERE / 'fugue.json', meta, voices, bars, entries=ENTRIES,
                         subject=S, entry_boost=5)
    for vd, v in zip(data['voices'], V):
        vd['gm_program'] = v[3]
        vd['seat'] = list(v[5])
    Path(path or HERE / 'fugue.json').write_text(json.dumps(data, indent=1))
    return data


if __name__ == '__main__':
    print('S ', S)
    print('SI', SI)
    print('A ', A)
    print('AI', AI)
    print('CS', CS)
    print('CSI', CSI)
    d = build()
    print('bars', len(next(iter(d['literal_bars']['bars'].values()))))
