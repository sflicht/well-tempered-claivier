#!/usr/bin/env python3
"""Fugue XII in F minor, five voices: "Fuga a 4 soggetti, compiuta" (third edition, Bach + 1).

The completion Bach never wrote.  The last fugue of The Art of Fugue, BWV 1080
(the unfinished "Contrapunctus XIX", the "Fuga a 3 soggetti"), breaks off just
after its third subject, B-A-C-H, has been combined with the first two.
Gustav Nottebohm (1880) showed that the three subjects also combine with the
main theme of the whole work, so Bach planned a quadruple fugue, in four
voices.  This fugue writes that plan out in F minor (Bach's D minor up a minor
third) in Bach's four voices, and adds one: a fifth voice, held back for the
whole piece, which enters only for the final combination and sings the main
theme in augmentation in the bass -- the voice Bach never got to write.

Subjects (Bach's, copied exactly and transposed up a minor third; see NOTES.md):
  S1  stile-antico subject, Contrapunctus XIX b1-6:     F C Bb Ab Bb C F
  S2  running subject, Contrapunctus XIX b114-120 (41 notes)
  S3  B-A-C-H, Contrapunctus XIX b193-197:              Db C Eb D E F E D E F
  MT  main theme, Contrapunctus I b1-5:                 F C Ab F E F G Ab Bb Ab G F

Plan (66 bars, 4/4):
  I    1-13   S1, stile antico: tenor, alto (tonal answer), bass, soprano; half cadence
  II  13-26   S2 alone (tenor), its answer (soprano), S2 (alto) with S1 (bass); cadence in b-flat
  III 26-41   B-A-C-H alone (tenor), answer (soprano); Bach's triple combination in c minor
              (alto S2, bass S1, tenor S3, at Bach's own distances); an episode down the circle of
              fifths to the dominant
  IV  42-49   the quadruple combination in four voices (main theme on top), f minor;
              it breaks off on a dominant seventh, as Bach's manuscript breaks off
  V   50-63   the fifth voice: the main theme in the alto, answered a bar later by its
              augmentation in the new lowest voice; over the augmentation's close and its
              last note held as a tonic pedal, the quadruple combination returns with its
              voices exchanged (S2 on top): five voices, four subjects at once
  Coda 63-66  over the pedal, the name at its own pitch (B-flat A C B) and a Picardy third

Every note is written here.  Subject statements are the quoted subjects or explicit
transforms (wtclib.transpose, scale_rhythm); everything else is literal token strings
placed at bar.beat.  A scratch script ranked placements of whole subject statements
against one another (which subject may enter where); it did not write any notes.
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (4, 4)
NAMES = ['S', 'A', 'T', 'B', 'Q']
LONG = ['Soprano', 'Alto', 'Tenor', 'Bass', 'Quinta vox']
CLEF = ['treble', 'treble', 'treble_8', 'bass', 'bass']

# ---------------------------------------------------------------- the four subjects (Bach, BWV 1080)
# As read from Contrapunctus XIX / I in D minor (sixteenth units), then transposed up a minor third.
S1_D = 'D3:8 A3:12 G3:4 F3:16 G3:16 A3:16 D3:8'                    # XIX b1.3-6.3 (bass)
S1A_D = 'A3:8 D4:12 D4:4 C4:16 D4:16 E4:16 A3:8'                   # XIX b6.3-11.3 (tenor): Bach's tonal answer
S2_D = ('F4:2 G4:2 F4:2 E4:2 D4:2 C#4:2 D4:2 A3:2 D4:2 E4:2 F4:2 E4:2 D4:2 F4:2 '
        'E4:2 A3:2 E4:2 F4:2 G4:2 F4:1 E4:1 F4:2 G4:2 A4:2 G4:2 F4:2 G4:2 A4:10 G4:1 F#4:1 G4:2 A4:2 '
        'Bb4:10 A4:2 G4:2 F4:2 E4:2 D4:2 E4:2 G4:2 F4:4')              # XIX b114.2-120.1 (alto)
S3_D = 'Bb3:8 A3:8 C4:8 B3:6 C#4:2 D4:14 C#4:1 B3:1 C#4:8 D4:8'      # XIX b193.3-197.3 (tenor)
MT_D = 'D4:8 A4:8 F4:8 D4:8 C#4:8 D4:4 E4:4 F4:10 G4:2 F4:2 E4:2 D4:8'  # Contrapunctus I b1-5 (alto)


def tr(s, semis, letters):
    return W.transpose(s, semis, letters)


def octv(s, n):
    return W.transpose(s, 12 * n, 7 * n)


S1 = tr(S1_D, 3, 2)        # F3 C4 Bb3 Ab3 Bb3 C4 F3
S1A = tr(S1A_D, 3, 2)      # C4 F4 F4 Eb4 F4 G4 C4   (Bach's tonal answer)
S2 = tr(S2_D, 3, 2)        # Ab4 Bb4 Ab4 G4 F4 E4 | F4 C4 F4 G4 Ab4 G4 F4 Ab4 | ...
S3 = tr(S3_D, 3, 2)        # Db4 C4 Eb4 D4 E4 F4 E4 D4 E4 F4   (B-A-C-H transposed)
MT = tr(MT_D, 3, 2)        # F4 C5 Ab4 F4 E4 F4 G4 Ab4 Bb4 Ab4 G4 F4
S2A = tr(S2, 7, 4)         # real answer in c: Eb5 F5 Eb5 D5 C5 B4 | C5 G4 ...
S3A = tr(S3, 7, 4)         # real answer in c: Ab4 G4 Bb4 A4 B4 C5 B4 A4 B4 C5
S1R = tr(S1, 7, 4)         # S1 in c (real):   C4 G4 F4 Eb4 F4 G4 C4
MT_AUG = W.scale_rhythm(MT, 2)

# ---------------------------------------------------------------- placement helpers
VO = {n: [] for n in NAMES}
ENTRIES = []


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


def pos(bar, beat):
    return Fr(bar - 1) * 16 + (Fr(beat) - 1) * 4


def put(v, bar, beat, toks):
    VO[v].append((pos(bar, beat), toks))


def theme(v, bar, beat, toks, label, nbars=None):
    put(v, bar, beat, toks)
    n = nbars if nbars is not None else max(1, round(float(dur16(toks)) / 16))
    ENTRIES.append((LONG[NAMES.index(v)], bar, (Fr(beat) - 1), label, n))


def seq(v, bar, *bars):
    """Consecutive whole bars from `bar` (each must fill the bar; 'R' = a bar's rest)."""
    for k, b in enumerate(bars):
        if b.strip() == 'R':
            continue
        if dur16(b) != 16:
            raise ValueError(f'{v} bar {bar + k}: {dur16(b)} sixteenths: {b}')
        toks = b.split()
        lead = Fr(0)
        while toks and toks[0].startswith('R:'):
            lead += W.parse_tok(toks.pop(0))[1]
        while toks and toks[-1].startswith('R:'):
            toks.pop()
        if toks:
            put(v, bar + k, 1 + lead / 4, ' '.join(toks))


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


# ================================================================ I. S1, STILE ANTICO (b1-13)
# Tenor, alto (Bach's tonal answer), bass, soprano: entries 2, 3 and 2 bars apart -- the closest
# distances at which S1 and its answer overlap cleanly (Bach's own spacing is 5).
theme('T', 1, 3, S1, 'S1')
theme('A', 3, 3, S1A, 'S1 answer')
theme('B', 6, 3, octv(S1, -1), 'S1')
theme('S', 8, 3, octv(S1A, 1), 'S1 answer')
# Tenor after its subject (i - V - V4/2 - i6; rests under the soprano's entry; iv7 - v - v7 - i - i6 - ii65 - V)
put('T', 6, 3, 'Ab3:8')
seq('T', 7, 'G3:8 E3:8', 'F3:8 R:8', 'R:8 Ab3:8', 'G3:8 Bb3:8', 'Ab3:8 F3:8~', 'F3:8 E3:8')
# Alto after its answer
put('A', 8, 3, 'Eb4:8')
# (b10-11: the alto's E-flat is tied over the bass's final F as a 7-6 suspension; a fresh C4 there, under
# the soprano's F5 and over the bass's F2, was out of reach of two hands.)
seq('A', 9, 'Db4:12 C4:4~', 'C4:8 Eb4:8~', 'Eb4:4 Db4:4 C4:8', 'Db4:8 C4:8', 'E4:4 R:12')
# Bass after its subject: i6 - ii65 - V (half cadence, b13)
put('B', 11, 3, 'Ab2:8')
seq('B', 12, 'Bb2:8 C3:8~', 'C3:4 R:12')

# ================================================================ II. S2, THE RUNNING SUBJECT (b13-26)
theme('T', 13, 2, octv(S2, -1), 'S2')
theme('S', 15, 2, S2A, 'S2 answer')
theme('A', 19, 2, S2, 'S2')
theme('B', 20, 3, octv(S1, -1), 'S1 (with S2)')
# Tenor after its S2: a slow line under the combination (i - v - VI; rests; iv - V7 - i)
put('T', 19, 3, 'C4:8~')
seq('T', 20, 'C4:8 Ab3:8', 'C4:8 Ab3:8', 'Eb3:8 R:8', 'R:8 Db4:8', 'C4:16', 'Ab3:4 R:12')
# Soprano returns as a descant for the cadence: iv - V7(b9) - i, then V7 - i in b-flat minor
put('S', 23, 3, 'Bb5:8')
seq('S', 24, 'G5:8 E5:8', 'F5:8 Eb5:8', 'Db5:8 R:8')
# Alto and bass after their subjects: the cadence into b-flat minor (b26), then silence for B-A-C-H
put('A', 25, 2, 'G4:4 A4:8')
put('A', 26, 1, 'Bb4:8')
put('B', 25, 3, 'F3:8')
put('B', 26, 1, 'Bb2:8')

# ================================================================ III. B-A-C-H (b26-39)
theme('T', 26, 3, S3, 'S3 B-A-C-H')
theme('S', 28, 3, S3A, 'S3 answer')
# Bach's own triple combination (XIX b233-239) in c minor: S2, S1 five beats later, S3 four beats after S1
theme('A', 32, 2, S2A, 'S2 (triple combination)')
theme('B', 33, 3, octv(S1R, -1), 'S1 (triple combination)')
theme('T', 34, 3, octv(S3A, -1), 'S3 (triple combination)')
# Tenor between its two B-A-C-H statements (under the soprano's answer; c: i6 - v - V - i)
put('T', 30, 3, 'Ab3:8')
seq('T', 31, 'F3:8 G3:8', 'C4:8 G3:8', 'C4:8 R:8')
# Episode (b38.3-41): a sequence in three voices down the circle of fifths from c to the dominant of f
# (c - f7 - b-flat - E-flat7 - A-flat - D-flat maj7 - C7).  The alto turns S2's head (x, x+1, x, x-1) on
# each chord; the tenor's chain of sevenths and the bass move in tenths and sevenths; a beat of silence
# before the main theme.
put('A', 38, 3, 'G5:2 Ab5:2 G5:2 F5:2')
seq('A', 39, 'Ab5:2 Bb5:2 Ab5:2 G5:2 F5:2 G5:2 F5:2 Eb5:2', 'G5:2 Ab5:2 G5:2 F5:2 Eb5:2 F5:2 Eb5:2 Db5:2',
    'F5:2 G5:2 F5:2 Eb5:2 E5:4 R:4')
put('T', 38, 3, 'Eb4:8~')
seq('T', 39, 'Eb4:8 Db4:8~', 'Db4:8 C4:8~', 'C4:8 Bb3:4 R:4')
put('B', 38, 3, 'C3:8')
seq('B', 39, 'F3:8 Bb2:8', 'Eb3:8 Ab2:8', 'Db3:8 C3:4 R:4')

# ================================================================ IV. THE QUADRUPLE COMBINATION, four voices (b42-49)
# Nottebohm's discovery: the main theme over Bach's triple combination (main theme, S2 a beat later,
# S1 five beats after S2, S3 four beats after S1).
Q4 = 42
theme('S', Q4, 1, octv(MT, 1), 'main theme')
theme('A', Q4, 2, S2, 'S2 (quadruple combination)')
theme('B', Q4 + 1, 3, octv(S1, -1), 'S1 (quadruple combination)')
theme('T', Q4 + 2, 3, S3, 'S3 (quadruple combination)')
# (the soprano falls silent after the main theme and returns only with it, in section V)
# The combination closes on i (b48); iv6 - V7, and the music breaks off on the dominant seventh
put('A', Q4 + 6, 3, 'Bb4:8')
seq('A', Q4 + 7, 'Bb4:8 R:8')
put('T', Q4 + 6, 3, 'F4:8')
seq('T', Q4 + 7, 'E4:8 R:8')
put('B', Q4 + 6, 3, 'Db3:8')
seq('B', Q4 + 7, 'C3:8 R:8')

# ================================================================ V. THE FIFTH VOICE (b50-63)
# The alto sings the main theme alone; a bar later the fifth voice, silent until now, enters beneath it
# with the main theme in augmentation (a canon per augmentationem, one bar apart).
V5 = 50
theme('A', V5, 1, MT, 'main theme')
# the augmentation's last note is held on as the tonic pedal of the close, re-struck where the music needs its
# bass (b61.1 as the main theme ends, b63.1 with S1's last note, b66.1 with the last chord): a piano's F2 dies
# away.  Each re-strike falls where the other fresh notes lie within reach of the hands (the coda's first chord,
# b63.3, is struck over the pedal, not with it).
theme('Q', V5 + 1, 1, octv(MT_AUG, -2).rsplit(' ', 1)[0] + ' F2:32 F2:32 F2:48 F2:12', 'main theme in augmentation (fifth voice)', 9)
# The fifth voice enters alone under the alto.  Then the tenor (V - i6/4 - V7 - i6 - iv4/2 - i), and with
# the bass over the augmentation's E and G (i - vii-dim7 - i - V4/3 - i6)
seq('T', V5 + 2, 'G3:8 Ab3:8', 'C4:8 Bb3:8', 'Ab3:8 C4:8', 'Db4:8 Bb3:8', 'C4:8 Bb3:8', 'C4:8 R:8')
put('B', V5 + 4, 3, 'Ab3:8')
seq('B', V5 + 5, 'G3:16', 'Ab3:8 R:8')
put('A', V5 + 6, 3, 'Db5:8')
put('A', V5 + 7, 1, 'C5:4')
# The quadruple combination over the end of the augmentation and its pedal: five voices, four subjects.
# The voices are exchanged against section IV, as Bach restates his combinations in invertible counterpoint:
# from the top S2 (an octave higher, the soprano's return), B-A-C-H, the main theme (tenor, in canon with its
# own augmentation below), S1 (an octave higher), and the fifth voice.
QV = V5 + 7
# (Nov 2026: the main theme and S1 exchange octaves and voices.  With S1 in the bass at F3-C4, its C4 at b59.1
# fell between the fifth voice's F2 and the soprano's G5, out of reach of two hands; the main theme now sings in
# the bass voice, directly over its own augmentation, and S1's long notes lie in the tenor at F4-C5.)
theme('B', QV, 1, octv(MT, -1), 'main theme (with its augmentation)')
theme('S', QV, 2, octv(S2, 1), 'S2 (five voices)')
theme('T', QV + 1, 3, octv(S1, 1), 'S1 (five voices)')
theme('A', QV + 2, 3, octv(S3, 1), 'S3 B-A-C-H (five voices)')
# Bass after the main theme, into the coda (i6 under S1's own close); the soprano's S2 steps up into the signature
put('B', QV + 4, 3, 'Bb3:8')
seq('B', QV + 5, 'Ab3:8 C4:8', 'Ab3:8 R:8')

# ================================================================ CODA (b63-66): the name at its own pitch
# Over the fifth voice's pedal the soprano signs B-flat A C B (V7 - V7/iv - ii-half-dim 4/3 - vii-dim7/V)
# and its B rises to C; the bass's A-natural is the Picardy third.
C = QV + 6
put('S', C, 3, 'Bb5:8')
seq('S', C + 1, 'A5:8 C6:8', 'B5:8 C6:8~', 'C6:12 R:4')
put('A', C, 3, 'E5:8')
seq('A', C + 1, 'Eb5:8 D5:8~', 'D5:8 C5:8~', 'C5:12 R:4')
put('T', C, 3, 'G4:8')
seq('T', C + 1, 'F4:16~', 'F4:8 E4:8', 'F4:12 R:4')
put('B', C, 3, 'C4:8')
seq('B', C + 1, 'C4:8 Ab3:8~', 'Ab3:8 G3:8', 'A3:12 R:4')


def build(nbars):
    bars = {LONG[i]: assemble(n, nbars) for i, n in enumerate(NAMES)}
    q = lambda bar, beat=1: (bar - 1) * 4 + (beat - 1)
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Fugue XII in F minor, five voices: Fuga a 4 soggetti, compiuta',
            'composer': 'Claude / Sam, completing J. S. Bach (BWV 1080) after G. Nottebohm',
            'instrument': 'Keyboard (five voices)',
            'key': 'F', 'mode': 'minor', 'meter': list(METER), 'bpm': 72,
            'tempo_text': 'Grave e sostenuto', 'movement_number': 12, 'piece_type': 'fugue', 'edition': 'third',
            'markers': [{'t': q(1), 'label': 'I. S1, stile antico'}, {'t': q(13, 2), 'label': 'II. S2'},
                        {'t': q(26, 3), 'label': 'III. B-A-C-H'}, {'t': q(Q4), 'label': 'IV. The main theme: four subjects'},
                        {'t': q(V5), 'label': 'V. The fifth voice'}, {'t': q(C, 3), 'label': 'Coda: B-A-C-H'}],
            # I and III Grave; II a little quicker (the running subject); breaths at the half cadence (b13),
            # the b-flat cadence (b26) and the end of the episode (b41); IV broad, slowing into the dominant
            # seventh where the music stops (b49); V from the canon to the end; the coda broadens to the last chord.
            'tempo_map': [[q(1), 72], [q(12, 3), 72], [q(13, 2), 58, 'ramp'], [q(13, 2), 76],
                          [q(25, 1), 76], [q(26, 3), 60, 'ramp'], [q(26, 3), 72],
                          [q(40, 3), 72], [q(Q4, 1), 58, 'ramp'], [q(Q4, 1), 66],
                          [q(Q4 + 6, 1), 66], [q(Q4 + 7, 3), 48, 'ramp'],
                          [q(V5, 1), 64], [q(QV, 1), 66], [q(C, 3), 64], [q(C + 3, 4), 44, 'ramp']]}
    voices = [(LONG[i], NAMES[i], CLEF[i], 70 if NAMES[i] == 'Q' else 64) for i in range(len(NAMES))]
    dyn = {1: -8, 6: -5, 8: -3, 11: -1, 13: -6, 15: -4, 19: -2, 20: 0, 24: 2, 26: -7, 28: -5, 32: -2, 34: 0,
           38: -1, 40: -3, Q4: 4, Q4 + 2: 6, Q4 + 6: 4, V5: -4, V5 + 1: -2, V5 + 4: 0, QV: 6, QV + 2: 9,
           C: 6, C + 2: 3}

    def dynamics(b):
        v = 0
        for k in sorted(dyn):
            if b + 1 >= k:
                v = dyn[k]
        return v
    data = W.build_score(HERE / 'fugue.json', meta, voices, bars, entries=ENTRIES, subject=S1,
                         dynamics=dynamics, entry_boost=7)
    # Bach's triple combination (b34.3-38.1): B-A-C-H lies a third to a sixth above S1, low in the texture;
    # bring the tenor forward and the bass back so the two slow lines do not fuse.
    for v in data['voices']:
        for e in v['events']:
            if 134 <= e['t'] < 148:
                if v['name'] == 'Tenor':
                    e['v'] = min(118, e['v'] + 6)
                elif v['name'] == 'Bass':
                    e['v'] = max(24, e['v'] - 3)
    for vn, b0, off, lab, n in ENTRIES:
        t0 = float((b0 - 1) * 4 + off)
        for e in data['voices'][LONG.index(vn)]['events']:
            if abs(e['t'] - t0) < 1e-6:
                e['label'] = lab
                break
    (HERE / 'fugue.json').write_text(json.dumps(data, indent=1))
    return data


if __name__ == '__main__':
    end = max((s + dur16(t)) for v in VO.values() for s, t in v)
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else int(-(-end // 16))
    build(nb)
    print('bars', nb)
