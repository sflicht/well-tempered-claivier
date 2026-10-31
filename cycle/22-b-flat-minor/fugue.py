#!/usr/bin/env python3
"""Fugue XXII in B-flat minor, six voices (a 6; Bach's BWV 867 has five):
Tombeau "Ma fin est mon commencement" -- a crab fugue (third edition, Bach + 1).

The second half is the exact retrograde of the first half in every voice: a note that
starts at t and lasts d in the first half sounds again at T - t - d.  Only bars 1-34 are
written here, note by note; bars 35-68 are produced by one explicit transform, ``crab()``,
which merges tied notes, reverses each voice's note list (wtclib.retrograde) and re-bars it.
The axis is the barline 34|35.  ``build()`` checks that every voice of the built score is an
exact palindrome.

The subject begins with the head of Bach's B-flat-minor fugue, WTC I/22 (BWV 867):
B-flat F, a rest, the leap of a minor ninth to G-flat and the stepwise descent; it ends
with Bach's name, B-flat A C B-natural (B-A-C-H).  Read backwards it begins H-C-A-B, climbs
the scale and ends with BWV 867's opening read backwards: F -> B-flat, a cadence.  So the
piece begins with a lone B-flat and ends on the same lone B-flat.

Plan of the first half (the second half is the same, backwards):
  1-14   I. Exposition: alto (subject), tenor (answer) with the countersubject, bass (subject);
         codetta (two voices)
  15-20  soprano (answer, an octave up); episode G - C | D-flat (deceptive) - A-flat7
  21-26  II. Middle entry: mezzo-soprano, subject in D-flat major; episode to V
  27-34  III. Crux: the sixth voice (cantus firmus) enters with the subject in augmentation, the
         alto with the subject at its own speed from the same downbeat (canon per augmentationem);
         from b33 all six voices: over the cantus's B-flat A C B, the alto sings D-flat C E-flat D,
         the mezzo (F) E-flat G-flat F and the tenor (F) F-sharp A A-flat -- B-A-C-H's tail in its four
         minor-third transpositions, which end on the four notes of the axis chord B D F A-flat.

Every note of the first half is a literal token string placed at bar.quarter.  Thematic
statements are explicit transforms (transpose, scale_rhythm) of the hand-written subject.
No code chooses a pitch.
"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (2, 2)          # alla breve, as BWV 867
BAR = 16                # sixteenths per bar
H1 = 34                 # bars written by hand
NBARS = 2 * H1
T16 = NBARS * BAR       # total length in sixteenths; the axis is at T16 / 2

# ------------------------------------------------------------------ six voices
VOICES = [  # abbr, name, clef, base velocity
    ('S', 'Soprano', 'treble', 70),
    ('Mz', 'Mezzo-soprano', 'treble', 70),
    ('A', 'Alto', 'treble', 72),
    ('T', 'Tenor', 'treble_8', 70),
    ('B', 'Bass', 'bass', 70),
    ('P', 'Cantus firmus', 'bass', 74),
]
NAMES = [v[0] for v in VOICES]
ABBR = {'P': 'Cf'}
LONG = {v[0]: v[1] for v in VOICES}

# ------------------------------------------------------------------ material
# The subject (4 bars): BWV 867's head (B-flat F, rest, minor ninth up to G-flat, the descent),
# then B-A-C-H.  Long notes first, quarters after, so that read backwards it slows into a cadence.
S = 'Bb4:16 F4:8 R:4 Gb5:4 F5:4 Eb5:4 Db5:4 C5:4 Bb4:4 A4:4 C5:4 B4:4'
# Tonal answer in F minor (BWV 867's answer F B-flat, the leap of a tenth), ending F E G F#
# (B-A-C-H a fifth up).
ANS = 'F4:16 Bb3:8 R:4 Db5:4 C5:4 Bb4:4 Ab4:4 G4:4 F4:4 E4:4 G4:4 F#4:4'


def oc(s, n):
    """Octave transposition."""
    return W.transpose(s, 12 * n, 7 * n)


def tr(s, semis, letters):
    return W.transpose(s, semis, letters)


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


# ------------------------------------------------------------------ placement (first half only)
VO = {n: [] for n in NAMES}
ENTRIES = []          # (abbr, pos16, len16, label)
AXIS_TIE = set()      # voices whose last note before the axis is tied into its own mirror image


def pos(bar, q):
    """bar (1-based) and quarter within the bar (1-based, fractions allowed) -> sixteenths."""
    return Fr(bar - 1) * BAR + (Fr(q) - 1) * 4


def put(v, bar, q, toks):
    VO[v].append((pos(bar, q), ' '.join(toks.split())))


def theme(v, bar, q, toks, label):
    put(v, bar, q, toks)
    ENTRIES.append((v, pos(bar, q), dur16(toks), label))


def assemble(v):
    """The voice's first half as one token list of exactly H1 bars (rests filled in)."""
    segs = sorted(VO[v], key=lambda x: x[0])
    out, cur = [], Fr(0)
    for s, toks in segs:
        if s < cur:
            raise ValueError(f'{v}: overlap at bar {float(s / BAR + 1)}: {toks[:60]}')
        if s > cur:
            out.append(f'R:{s - cur}')
        out.extend(toks.split())
        cur = s + dur16(toks)
    total = Fr(H1 * BAR)
    if cur > total:
        raise ValueError(f'{v}: runs past the axis ({float(cur / BAR)} > {H1})')
    if cur < total:
        out.append(f'R:{total - cur}')
    return out


def merge_ties(toks):
    """Tied notes -> single tokens (so that a tie is reversed as one note)."""
    out = []
    for t in toks:
        p, d, sp, tie = W.parse_tok(t)
        name = t.rsplit(':', 1)[0]
        if out and out[-1][2] and out[-1][0] == name and name != 'R':
            out[-1] = (name, out[-1][1] + d, tie)
        elif out and name == 'R' and out[-1][0] == 'R':
            out[-1] = (name, out[-1][1] + d, False)
        else:
            out.append((name, d, tie))
    for name, d, tie in out:
        if tie:
            raise ValueError(f'dangling tie on {name}')
    return [f'{n}:{d}' for n, d, _ in out]


def crab(toks):
    """The explicit retrograde: every note (and rest) of the first half, in reverse order."""
    return W.retrograde(merge_ties(toks)).split()


def voice_bars(v, half=None):
    h1 = merge_ties(assemble(v))
    h2 = crab(h1)
    if half == 1:
        return W.concat_bars(' '.join(h1), METER)
    if half == 2:
        return W.concat_bars(' '.join(h2), METER)
    if v in AXIS_TIE:
        p1, p2 = h1[-1].rsplit(':', 1)[0], h2[0].rsplit(':', 1)[0]
        assert p1 == p2 and p1 != 'R', (v, p1, p2)
        h1 = h1[:-1] + [h1[-1] + '~']
    return W.concat_bars(' '.join(h1 + h2), METER)


def mirrored_entries():
    """Entries of the first half and their cancrizans images in the second."""
    out = []
    for v, p, n, lab in ENTRIES:
        b, r = divmod(p, BAR)
        nb = max(1, round(float(n) / BAR))
        out.append((LONG[v], int(b) + 1, r / 4, lab, nb, None))
        q = T16 - p - n
        b2, r2 = divmod(q, BAR)
        out.append((LONG[v], int(b2) + 1, r2 / 4, lab + ' (cancrizans)', nb, 'retrograde'))
    return out


def check_palindrome(data):
    """Every voice of the built score must be its own mirror image around the axis."""
    T = NBARS * 4
    for v in data['voices']:
        ev = sorted((round(e['t'], 6), round(e['d'], 6), e['p']) for e in v['events'])
        mir = sorted((round(T - t - d, 6), d, p) for t, d, p in ev)
        if ev != mir:
            raise AssertionError(f"voice {v['name']} is not a palindrome")
    return True


def dynamics(b):
    """A symmetric arch: quiet at the ends, fullest at the axis (bar index b is 0-based)."""
    d = min(b, NBARS - 1 - b)          # distance from the nearer end, 0..H1-1
    return round(-8 + 14 * d / (H1 - 1))


BPM = 88    # quarter = 88, i.e. half = 44
# The tempo map is itself a palindrome around the axis (t = 136 quarters): a slow toll at both ends,
# a breath at each mirrored pair of section joins (14|15 and 54|55, 20|21 and 48|49, 26|27 and
# 42|43), and a broadening into the axis with its mirror image away from it.  So the performance,
# like the score, reads the same backwards.
TEMPO = {'tempo_map': [[0, 63], [8, BPM, 'ramp'],
                       [52, BPM], [56, 80, 'ramp'], [60, BPM, 'ramp'],
                       [76, BPM], [80, 80, 'ramp'], [84, BPM, 'ramp'],
                       [96, BPM], [104, 76, 'ramp'], [112, BPM, 'ramp'],
                       [120, BPM], [136, 66, 'ramp'], [152, BPM, 'ramp'],
                       [160, BPM], [168, 76, 'ramp'], [176, BPM, 'ramp'],
                       [188, BPM], [192, 80, 'ramp'], [196, BPM, 'ramp'],
                       [212, BPM], [216, 80, 'ramp'], [220, BPM, 'ramp'],
                       [264, BPM], [272, 63, 'ramp']]}
# Section labels; the second half carries the same sections in reverse order.
MARKS = [(1, 'I. Exposition (alto, tenor, bass, soprano)'), (13, 'codetta'), (15, 'soprano: answer'),
         (19, 'episode'), (21, 'II. Middle entry, D-flat major (mezzo-soprano)'), (25, 'episode'),
         (27, 'III. Crux: cantus firmus in augmentation, alto in canon'),
         (33, 'B-A-C-H in four transpositions -> axis'),
         (35, 'Axis: III. Crux cancrizans'), (43, 'episode cancrizans'),
         (45, 'II. cancrizans'), (49, 'episode cancrizans'), (51, 'soprano: answer cancrizans'),
         (55, 'codetta cancrizans'), (57, 'I. Exposition cancrizans'), (65, 'alto alone: the subject backwards')]


def build(path=None, half=None):
    bars = {LONG[v]: voice_bars(v, half) for v in NAMES}
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Fugue XXII in B-flat minor, six voices: '
                        'Tombeau "Ma fin est mon commencement" (crab fugue)',
            'composer': 'Claude / Sam (subject after J. S. Bach, BWV 867, ending B-A-C-H)',
            'instrument': 'Keyboard - six voices',
            'key': 'Bb', 'mode': 'minor', 'meter': list(METER), 'bpm': BPM,
            'tempo_text': 'Grave, alla breve -- the second half is the first played backwards',
            'movement_number': 22, 'number': 22, 'piece_type': 'fugue', 'edition': 'third',
            'voice_order': 'high_to_low'}
    if half is None:
        meta.update(TEMPO)
        meta['markers'] = [{'t': float((b - 1) * 4), 'label': txt} for b, txt in MARKS]
        entries = mirrored_entries()
    else:
        meta['subtitle'] += f' -- half {half} alone'
        ents = mirrored_entries()
        if half == 1:
            entries = [e for e in ents if e[5] is None]
        else:
            entries = [(e[0], e[1] - H1) + tuple(e[2:]) for e in ents if e[5] is not None]
    voices = [(LONG[v], ABBR.get(v, v), cl, base) for v, _, cl, base in VOICES]
    data = W.build_score(path or HERE / 'fugue.json', meta, voices, bars, entries=entries, subject=S,
                         dynamics=dynamics if half is None else None)
    if half is None:
        check_palindrome(data)
    return data


# =================================================================================== FIRST HALF
theme('A', 1, 1, S, 'Subject (after BWV 867, ending B-A-C-H)')
# b5-8: the tenor answers below; the alto's countersubject resolves the H, breathes, sighs (D-flat C),
# climbs while the answer holds, and moves in half notes while the answer runs down.
theme('T', 5, 1, ANS, 'Answer (tonal, F minor)')
put('A', 5, 1, 'C5:4 R:4 Db5:4 C5:4 Db5:4 Eb5:4 F5:8 G5:8 F5:8 Db5:8 Eb5:8')
# b9-12: the bass enters, two octaves down; the tenor resolves F# to G and falls G (rest) G-flat F;
# the alto breathes for two bars.
theme('B', 9, 1, oc(S, -2), 'Subject (bass)')
put('T', 9, 1, 'G4:4 R:4 Gb4:4 F4:4 A4:8 Bb4:8 A4:8 F4:8~ F4:8 Eb4:4 D4:4')
put('A', 9, 1, 'Db5:4')
put('A', 11, 1, 'C5:8 Bb4:4 C5:4 Db5:4 C5:4 A4:4 Ab4:4')
# b13-14: codetta: V - i6 | iv - V of F minor; the alto sighs (G, rest, A-flat G), the tenor too
# (D-flat C), over a bass that breathes after its H -> C.
put('B', 13, 1, 'C3:4 R:4 Ab2:8 Bb2:8 C3:8')
put('T', 13, 1, 'E4:8 C4:8 Db4:8 C4:8')
put('A', 13, 1, 'G4:4 R:4 Ab4:4 G4:4 F4:8 E4:8')
# b15-18: the soprano answers an octave up, above everything; the tenor breathes for two bars.
theme('S', 15, 1, oc(ANS, 1), 'Answer (soprano, F minor)')
put('A', 15, 1, 'F4:4 G4:4 Ab4:8 F4:8 Bb4:8 G4:12 F4:4 G4:12 C5:4')
put('B', 15, 1, 'F2:16 Bb2:16 Eb3:8 F3:8 C3:12 A2:4')
put('T', 17, 1, 'G3:8 Ab3:8 G3:8 E3:4 D3:4')
# b19-20: episode: G - C | D-flat (deceptive) - A-flat7, into D-flat major.
put('S', 19, 1, 'G5:16 F5:8 Gb5:4 F5:4')
put('B', 19, 1, 'G2:8 C3:8 Db3:8 Ab2:8')
put('A', 19, 1, 'B4:8 C5:8 Ab4:16')
put('T', 19, 1, 'D3:8 E3:8 F3:8 C4:8')
# b21-24: middle entry: the mezzo-soprano, with the subject in D-flat major (its tail D-flat C E-flat D is
# B-A-C-H a minor third up), leading to E-flat minor.  Soprano and alto rest at first; the tenor
# falls chromatically (D-flat C C-flat B-flat) into E-flat minor.
SMAJ = 'Db5:16 Ab4:8 R:4 Bb5:4 Ab5:4 Gb5:4 F5:4 Eb5:4 Db5:4 C5:4 Eb5:4 D5:4'
theme('Mz', 21, 1, SMAJ, 'Subject in D-flat major (mezzo-soprano)')
put('B', 21, 1, 'Db3:8 Bb2:8 F2:8 Gb2:8 Ab2:8 Db3:8 Bb2:4 Ab2:12')
put('T', 21, 1, 'Db4:4 Eb4:4 F4:8 F4:4 Eb4:4 Bb3:8 C4:8 Db4:8~ Db4:4 Eb4:4 C4:4 Cb4:4')
put('A', 23, 1, 'Ab4:24 Gb4:4 F4:4')
# b25-26: episode for three voices, E-flat minor - ii-half-dim 6/5 | V - V7; the alto rests for almost
# two bars and the bass breathes before the cantus and the alto enter together.
put('Mz', 25, 1, 'Eb5:4 Db5:4 C5:8 C5:8 Eb5:8')
put('A', 25, 1, 'Gb4:4')
put('T', 25, 1, 'Bb3:16 A3:8 C4:8')
put('B', 25, 1, 'Gb2:8 Eb2:8 F2:16')

# =================================================================================== SUMMIT (b27-34)
# The sixth voice, the cantus, enters with the subject in augmentation (B-flat2 ... B-A-C-H in half
# notes, its H on the axis); the alto sings the subject at its own speed from the same downbeat
# (canon per augmentationem).
theme('P', 27, 1, W.scale_rhythm(oc(S, -2), 2), 'Subject in augmentation (cantus; B-A-C-H on the axis)')
theme('A', 27, 1, S, 'Subject with its augmentation (canon per augmentationem)')
put('Mz', 27, 1, 'Db5:8 Gb5:8 F5:8 Bb5:8 C6:8 Bb5:4 A5:4 F5:4 Eb5:4 E5:8 F5:16')
put('T', 27, 1, 'Db4:8 Eb4:8 Db4:8 Bb3:8 A3:8 F3:8~ F3:8 R:8 A3:12 G3:4 F3:16')
# b31-34: everyone converges on the axis.  Over the cantus's B-flat A C B, three more voices sing the
# tail of B-A-C-H transposed by minor thirds -- the alto D-flat C E-flat D, the mezzo (F) E-flat G-flat F,
# the tenor (F) F-sharp A A-flat -- so that the four transpositions end on the four notes of the
# diminished-seventh axis chord, B D F A-flat; the soprano returns (b32) and climbs to D6.
put('A', 31, 1, 'C5:16 Bb4:8 Eb5:8 Db5:8 C5:8 Eb5:8 D5:8')
put('Mz', 33, 1, 'F5:8 Eb5:4 F5:4 Gb5:8 F5:8')
put('T', 33, 1, 'F3:8 F#3:8 A3:8 Ab3:8')
put('B', 33, 1, 'Db3:8 Eb3:8 Eb3:8 F3:8')
put('S', 32, 1, 'Bb5:8 A5:8 Bb5:8 C6:8 C6:8 D6:8')
# The five upper voices hold their notes of the axis chord across the axis (each note tied into its own
# mirror image); the cantus alone strikes its H again on the axis, where the piece turns round.
AXIS_TIE.update({'S', 'Mz', 'A', 'T', 'B'})

if __name__ == '__main__':
    import os
    out = os.environ.get('XXII_HALVES')
    build()
    if out:
        build(Path(out) / 'h1.json', 1)
        build(Path(out) / 'h2.json', 2)
