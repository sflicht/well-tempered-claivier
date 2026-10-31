#!/usr/bin/env python3
"""Fugue VI in D minor a 4: Passacaglia e fuga sopra il Crucifixus.

Every note is written below as literal token strings (sixteenth units, see
tools/wtclib.py).  The only operations applied to written material are the
named transformations `transpose` (via `move`) and `scale_rhythm`
(augmentation), used to place the hand-written ground, subject and inversus at
other pitch levels and speeds.  Their output is what fugue.json holds.

Material (see NOTES.md):
  GROUND   the descending chromatic lament D C# C B Bb A | Bb G A D (the
           Crucifixus ground of BWV 232 / BWV 12, transposed), 8 bars of 3/4.
  SUBJECT  the ground inverted and in diminution (note values halved):
           A Bb B C C# D | C# E D A, 4 bars.
  INVERSUS the subject inverted = the ground at double speed.

Run:  python3 cycle/06-d-minor/fugue.py   -> cycle/06-d-minor/fugue.json
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
from wtclib import build_score, concat_bars, transpose, scale_rhythm, parse_tok, LETTERS  # noqa: E402

METER = (3, 4)
NAMES = ['Soprano', 'Alto', 'Tenor', 'Bass']
AB = {'S': 'Soprano', 'A': 'Alto', 'T': 'Tenor', 'B': 'Bass'}
NBARS = 58
REST = 'R:12'
BARS = {n: [REST] * NBARS for n in NAMES}
TAGS = [''] * NBARS
ENTRIES = []


def put(bar, **parts):
    """Write token strings (whole bars, ties allowed across barlines) from `bar` on."""
    for k, s in parts.items():
        for i, b in enumerate(concat_bars(' '.join(s.split()), METER)):
            BARS[AB[k]][bar - 1 + i] = b


def tag(bar, text):
    TAGS[bar - 1] = text


def entry(voice, bar, label, beat=1, n=4):
    ENTRIES.append((AB[voice], bar, beat - 1, label, n))


def move(s, frm, to):
    """Explicit transposition of a token string so that note `frm` becomes `to`."""
    a = parse_tok(frm + ':1')[0]
    b = parse_tok(to + ':1')[0]
    la = LETTERS.index(frm[0]) + 7 * int(frm[-1])
    lb = LETTERS.index(to[0]) + 7 * int(to[-1])
    return transpose(s, b - a, lb - la)


# ---------------------------------------------------------------------------
# The themes, written by hand.
GROUND = 'D3:16 C#3:8 C3:8 B2:4 Bb2:4 A2:12 Bb2:4 G2:8 A2:24 D2:8'
SUBJ = 'A4:8 Bb4:4 B4:4 C5:2 C#5:2 D5:6 C#5:2 E5:4 D5:12 A5:4'
# The subject's inversion is the ground at double speed.
INV = 'D5:8 C#5:4 C5:4 B4:2 Bb4:2 A4:6 Bb4:2 G4:4 A4:12 D4:4'
assert INV == move(scale_rhythm(GROUND, '1/2'), 'D3', 'D5')


def G(to):            # the ground with D3 moved to `to`
    return move(GROUND, 'D3', to)


def S(to):            # the subject with A4 moved to `to`
    return move(SUBJ, 'A4', to)


def I(to):            # the inversus with D5 moved to `to`
    return move(INV, 'D5', to)


def last_octave(s, k):
    """The same line with its last note moved k octaves (the closing leap of a
    fifth taken as a fourth the other way): an explicit, named variant."""
    toks = s.split()
    name, d = toks[-1].rsplit(':', 1)
    toks[-1] = transpose(toks[-1], 12 * k, 7 * k)
    return ' '.join(toks)


# ===========================================================================
# STATION I (bars 1-8), D minor: the ground in the BASS.
# Two bars alone; the inversus (= the ground at double speed) joins at the
# twelfth in the Alto (bar 3), so the lament sounds at two speeds in tenths;
# the Subject (Soprano, bar 5) climbs against it.
tag(1, 'Station I (D minor): the ground in the Bass')
put(1, B=G('D3'))
entry('B', 1, 'Ground (Bass)', n=8)
tag(3, 'Inversus = the ground at double speed (Alto)')
put(3, A=I('A4') + '  A3:4 C#4:2 E4:2 F4:4  E4:4 F4:6 A4:2')
entry('A', 3, 'Inversus (Alto): the ground at double speed')
tag(5, 'Subject (Soprano)')
put(5, S=S('A4'))
entry('S', 5, 'Subject (Soprano)')

# ===========================================================================
# STATION II (bars 9-16), A minor: the ground in the TENOR, now the lowest
# voice (the Bass rests).  The same pair of entries, voices exchanged:
# inversus in the Soprano (bar 11), answer in the Alto (bar 13).
tag(9, 'Station II (A minor): the ground in the Tenor; the Bass rests')
put(9, T=G('A3') + '~  A2:4 C#3:4 D3:4  B2:4 G2:4 C3:4  A2:4 F2:4 Bb2:4  G2:4 C3:8')
entry('T', 9, 'Ground (Tenor), A minor', n=8)
put(9, S='A5:4 G5:2 F5:2 E5:4  C5:4 B4:4 R:4')
put(9, A='C5:4 B4:2 A4:2 G#4:2 A4:2  E4:4 E4:4 D4:4  C4:2 D4:2 E4:4 A4:4  A4:8 G#4:2 R:2')
tag(11, 'Inversus (Soprano)')
put(11, S=last_octave(I('E5'), 1) + '  C5:2 B4:2 D5:4 C5:4  B4:4 C5:8')
entry('S', 11, 'Inversus (Soprano)')
tag(13, 'Answer (Alto)')
put(13, A=last_octave(S('E4'), -1))
entry('A', 13, 'Answer (Alto)')

# ===========================================================================
# EPISODE 1 (bars 17-20), A minor -> F major.  Three voices: a chain of
# dominant sevenths (A7-Dm, G7-C, F7-Bb) whose sevenths fall in the Alto
# (G F | F E | Eb D: the lament once more); the Soprano turns above.
tag(17, 'Episode 1: falling fifths to F major')
put(17, A='G4:8 F4:4~  F4:8 E4:4  Eb4:8 D4:4  D4:4 E4:4 R:4')
put(17, S='A5:2 G5:2 E5:2 F5:2 D5:2 F5:2  G5:2 F5:2 D5:2 E5:2 C5:2 E5:2  F5:2 Eb5:2 C5:2 D5:2 Bb4:2 D5:2'
          '  Bb4:2 A4:2 C5:4 R:4')

# ===========================================================================
# STATION III (bars 21-28), F major: the ground in the ALTO, first as the top
# voice (the Soprano rests four bars), over the Tenor alone.  Station I's
# trio, regrouped: the Bass returns with the inversus in tenths BELOW the
# ground (bar 23), the Soprano with the subject above it (bar 25).
tag(21, 'Station III (F major): the ground in the Alto; the Soprano rests')
put(21, A=last_octave(G('F4'), 1))
entry('A', 21, 'Ground (Alto), F major', n=8)
put(21, T='F3:4 G3:2 A3:2 Bb3:4  A3:4 G3:2 F3:2 E3:2 G3:2  G3:8 G3:4  F3:4 F3:4 E3:4  E3:4 F3:4 E3:4'
          '  D3:4 G3:4 A3:4  G3:4 Bb3:4 A3:4  E3:4 A3:8')
tag(23, 'Inversus (Bass), in tenths under the ground')
put(23, B=last_octave(I('C3'), 1) + '~  C3:12~  C3:4 F2:8')
entry('B', 23, 'Inversus (Bass)')
tag(25, 'Subject (Soprano), F major')
put(25, S=last_octave(S('C5'), -1))
entry('S', 25, 'Subject (Soprano), F major')

# ===========================================================================
# EPISODE 2 (bars 29-34): stretto.  The Tenor, which has had only the ground,
# takes the subject (D minor); one bar later the Alto answers at the fifth
# above (A minor).  The Bass walks, then falls silent for the summit.
tag(29, 'Episode 2: subject (Tenor) and answer (Alto) in stretto, one bar apart')
put(29, T=last_octave(S('A3'), -1) + '  C4:4 A3:4 B3:4  A3:12')
entry('T', 29, 'Subject (Tenor), stretto')
put(30, A=last_octave(S('E4'), -1) + '  E4:4 C#4:4 E4:4')
entry('A', 30, 'Answer (Alto), stretto at one bar')
put(29, A='R:12')
put(29, B='D3:4 F3:4 G3:4  E3:4 A2:4 D3:4  B2:4 A2:4 D3:4  B2:4 G#2:4 A2:4  F2:8 E2:4  R:12')
put(29, S='R:4 F5:2 E5:2 D5:4  E5:8 D5:4~  D5:4 C#5:4 D5:2 F5:2  F5:4 E5:4 C#5:4  D5:4 C5:4 D5:4  C#5:12')

# ===========================================================================
# SUMMIT (bars 35-50).  The ground returns to the Bass in augmentation
# (16 bars).  Over its D the Tenor sings the inversus (the ground at double
# speed); the Soprano falls silent, then enters (bar 39) with the ground at
# normal speed at the dominant: the two outer voices descend chromatically at
# two speeds in sixths.  From bar 43 every voice carries a form of the ground:
# Bass x2, Soprano x1, Tenor inversus x1/2, Alto subject (its mirror) x1/2.
# Over the long A the voices close on D major (bar 49).
tag(35, 'Summit: the ground augmented in the Bass; inversus (Tenor)')
put(35, B=scale_rhythm(G('D3'), 2))
entry('B', 35, 'Ground augmented (Bass)', n=16)
put(35, T=I('A4') + '  R:4 E4:2 D4:2 C4:2 B3:2  A3:2 B3:2 D4:2 E4:2 D4:2 B3:2  G3:2 A3:2 Bb3:2 G3:2 C4:2 A3:2'
          '  C4:4 C#4:4 R:4')
entry('T', 35, 'Inversus (Tenor) over the augmented ground')
put(35, A='D5:8 B4:4  C#5:4 D5:4 C#5:4  D5:4 Bb4:4 A4:4  G4:4 A4:2 G4:2 E4:4  R:12  R:12')
put(35, S='F5:8 E5:4  E5:4 A5:4 G5:4  F5:4 G5:4 E5:4  R:12')
tag(39, 'Ground in the Soprano (at the dominant): two speeds in the outer voices')
put(39, S=last_octave(G('A5'), 1) + '  F5:8 G5:4  Bb5:8 A5:4  G5:4 E5:4 F#5:4  F#5:12')
entry('S', 39, 'Ground (Soprano), at the dominant, over its augmentation', n=8)
tag(41, 'Subject (Alto) between the two grounds')
put(41, A=S('D4') + '  C#5:12  C#5:4 E5:4 E5:4  D5:8 C#5:4  E5:8 E5:4  E5:4 C#5:4 A4:4  A4:12')
entry('A', 41, 'Subject (Alto) between the two grounds')
tag(43, 'Inversus (Tenor): the ground at three speeds at once')
put(43, T='R:8 ' + I('D4') + '  E3:4  G3:8 E3:4  C#3:4 E3:4 D3:4  D3:12')
entry('T', 43, 'Inversus (Tenor): the third speed', beat=3)

# ===========================================================================
# CODA (bars 51-58), D major, over the tonic: the subject (the ground turned
# upside down) in augmentation in the Soprano, rising from A to A.
tag(51, 'Coda: the subject augmented (Soprano) over the tonic')
put(51, S=scale_rhythm(S('A4'), 2))
entry('S', 51, 'Subject augmented (Soprano), D major', n=8)
put(51, B='D2:24  D2:24  D2:24  G2:12  D2:12')
put(51, A='F#4:12  F#4:4 G4:8  G4:8 A4:4  G4:4 F#4:8  F#4:4 E4:4 G4:4  G4:4 F#4:8  E4:4 G4:8  F#4:12')
put(51, T='R:12  R:4 D3:8  D3:8 A2:4  A2:4 D3:8  D3:4 A2:8  A2:4 D3:8  B2:8 D3:4  D3:12')

# ---------------------------------------------------------------------------
BPM = 76
TEMPO_MAP = [[0, BPM], [NBARS * 3 - 6, BPM], [NBARS * 3, 54, 'ramp']]

_DYN = [(1, -6), (8, -3), (16, 0), (24, 1), (34, 4), (40, 8), (49, 12), (51, 4), (58, -2)]


def DYN(b):
    bar = b + 1
    for (b0, v0), (b1, v1) in zip(_DYN, _DYN[1:]):
        if b0 <= bar <= b1:
            return round(v0 + (v1 - v0) * (bar - b0) / max(1, b1 - b0))
    return 0


def build(path=HERE / 'fugue.json'):
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'Fugue VI in D minor (a 4)',
            'composer': 'Claude / Sam (ground after J. S. Bach, Crucifixus BWV 232)',
            'instrument': 'Keyboard - four voices',
            'key': 'D', 'mode': 'minor', 'meter': list(METER), 'bpm': BPM,
            'tempo_text': 'Passacaglia e fuga sopra il Crucifixus',
            'tempo_map': TEMPO_MAP,
            'movement_number': 6, 'piece_type': 'fugue', 'edition': 'third',
            'markers': [{'t': (b - 1) * 3, 'label': t} for b, t in enumerate(TAGS, 1) if t]}
    voices = [('Soprano', 'S', 'treble', 72), ('Alto', 'A', 'treble', 68),
              ('Tenor', 'T', 'treble_8', 68), ('Bass', 'B', 'bass', 72)]
    data = build_score(path, meta, voices, BARS, entries=ENTRIES, subject=SUBJ,
                       dynamics=DYN, tags=TAGS)
    Path(path).write_text(json.dumps(data, indent=1))
    return data


if __name__ == '__main__':
    build()
