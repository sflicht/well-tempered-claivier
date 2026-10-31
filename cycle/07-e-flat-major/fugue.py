#!/usr/bin/env python3
"""Fugue VII in E-flat major a 4: Fuga a due cori (Bach + 1 edition).

Two choirs of two voices, after the Venetian cori spezzati (Gabrieli's "coro
acuto" and "coro grave") and Bach's double-choir motet "Singet dem Herrn"
BWV 225:

  Coro I  (coro grave):  Tenor + Bass.     It sings the subject RECTUS, and its
                          dialect is the dominant (B-flat, with A natural).
  Coro II (coro acuto):  Soprano + Alto.   It answers with the INVERSION, and its
                          dialect is the subdominant (A-flat, with D-flat).

On one piano the choirs are the two hands: Coro II the right, Coro I the left.

Every note is written below as literal bar strings in sixteenth units.  The
one derived block is Coro II's exposition (b5-9.1), which is the exact
diatonic mirror of Coro I's (b1-5.1) about G4, as computed by
wtclib.invert_diatonic and written out here literally (a check in NOTES.md).

Run:  python3 cycle/07-e-flat-major/fugue.py   -> cycle/07-e-flat-major/fugue.json
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
from wtclib import build_score, concat_bars  # noqa: E402

METER = (4, 4)
BPM = 80
NAMES = ['Soprano', 'Alto', 'Tenor', 'Bass']
AB = {'S': 'Soprano', 'A': 'Alto', 'T': 'Tenor', 'B': 'Bass'}
NBARS = 23
BARS = {n: ['R:16'] * NBARS for n in NAMES}
TAGS = [''] * NBARS
ENTRIES = []          # (voice, bar, beat offset in quarters, label, bars to emphasise[, form])


def put(bar, **parts):
    """Write token strings (whole bars, any length) into voices from `bar` on."""
    for k, s in parts.items():
        for i, b in enumerate(concat_bars(' '.join(s.split()), METER)):
            BARS[AB[k]][bar - 1 + i] = b


def tag(bar, text):
    TAGS[bar - 1] = text


def entry(v, bar, off, label, n=2, form=None):
    ENTRIES.append((AB[v], bar, off, label, n) + ((form,) if form else ()))


# ---------------------------------------------------------------------------
# THE MATERIAL
#
# Subject (kept from the earlier version; the prelude's obbligato is made of it):
# the first line of "Wachet auf" (E-flat G B-flat .. C B-flat) in the canzona
# rhythm long-short-short-long-long, then a sixteenth turn, a leap to the summit
# and a fall onto the leading tone.  It ends open, on D.
SUBJ = 'Eb4:4 G4:2 Bb4:2 C5:4 Bb4:4 C5:2 D5:1 C5:1 Bb4:2 D5:2 F5:4 Eb5:2 D5:2'
# Tonal answer: bar 1 a fifth up, bar 2 a fourth up.
#   Bb3:4 D4:2 F4:2 G4:4 F4:4 | F4:2 G4:1 F4:1 Eb4:2 G4:2 Bb4:4 Ab4:2 G4:2
# Inversion (diatonic mirror about G4, the third of the tonic: the tonic triad
# maps onto itself, the dominant onto the subdominant):
#   Bb4:4 G4:2 Eb4:2 D4:4 Eb4:4 | D4:2 C4:1 D4:1 Eb4:2 C4:2 Ab3:4 Bb3:2 C4:2
# Countersubject (new, diatonic so that it mirrors exactly): an eighth rest, a
# climb in eighths, a syncopation over the barline, a fall to the cadence.
#   over the answer:  R:2 F:2 Bb:2 Ab:2 Bb:2 C:2 D:4~ | D:4 Eb:4 D:4 C:2 Bb:2


# ===========================================================================
# 1. EXPOSITION OF CORO I (b1-5.1): tenor subject, bass answer + countersubject.
put(1, T='Eb3:4 G3:2 Bb3:2 C4:4 Bb3:4  C4:2 D4:1 C4:1 Bb3:2 D4:2 F4:4 Eb4:2 D4:2  '
         'R:2 F3:2 Bb3:2 Ab3:2 Bb3:2 C4:2 D4:4~  D4:4 Eb4:4 D4:4 C4:2 Bb3:2  G3:4 R:12',
       B='R:16  R:16  Bb2:4 D3:2 F3:2 G3:4 F3:4  F3:2 G3:1 F3:1 Eb3:2 G3:2 Bb3:4 Ab3:2 G3:2  Eb3:4 R:12')
entry('T', 1, 0, 'Coro I: subject (tenor, E-flat)')
entry('B', 3, 0, 'Coro I: tonal answer (bass, B-flat)')
tag(1, 'Coro I (tenor, bass): exposition')

# 2. EXPOSITION OF CORO II (b5-9.1): the whole of b1-5.1 mirrored about G4
# (invert_diatonic(..., 'G4', E-flat major)), so the tenor's line becomes the
# alto's and the bass's becomes the soprano's; the bass's answer at the dominant
# becomes the soprano's answer at the subdominant.  On the keyboard the right
# hand plays what the left hand played, reflected.
put(5, A='Bb5:4 G5:2 Eb5:2 D5:4 Eb5:4  D5:2 C5:1 D5:1 Eb5:2 C5:2 Ab4:4 Bb4:2 C5:2  '
         'R:2 Ab5:2 Eb5:2 F5:2 Eb5:2 D5:2 C5:4~  C5:4 Bb4:4 C5:4 D5:2 Eb5:2  G5:4 R:12',
       S='R:16  R:16  Eb6:4 C6:2 Ab5:2 G5:4 Ab5:4  Ab5:2 G5:1 Ab5:1 Bb5:2 G5:2 Eb5:4 F5:2 G5:2  Bb5:4 R:12')
entry('A', 5, 0, 'Coro II: inversion (alto; the mirror of b1)', 2, 'inversus')
entry('S', 7, 0, 'Coro II: inverted answer (soprano, A-flat; the mirror of b3)', 2, 'inversus')
tag(5, 'Coro II (soprano, alto): the mirror exposition')


# ===========================================================================
# 3. THE CHOIRS MEET (b9-16).  For the first time all four voices together, on
# the tonic chord (9.1).  Entries a bar apart, choir against choir: the tenor's
# subject (E-flat), the soprano's inversion on F a bar later; the bass in
# c minor (b12), the alto's inversion in g minor (b14), which turns to B-flat.
put(9,
    T='Eb3:4 G3:2 Bb3:2 C4:4 Bb3:4  C4:2 D4:1 C4:1 Bb3:2 D4:2 F4:4 Eb4:2 D4:2  '
      'Eb4:4 D4:4 C4:4 B3:4  C4:4 G3:4 Eb4:4 F4:4  Eb4:4 Bb3:4 C4:4 A3:2 Bb3:2~  '
      'Bb3:8 A3:4 G3:4  Bb3:4 Bb3:4 G3:4 Bb3:2 A3:2  Bb3:4 R:12',
    B='Eb2:4 Eb3:4 Ab2:4 G2:4  Ab2:4 Bb2:8 Eb3:4  F3:4 Bb2:4 C3:4 G2:2 R:2  '
      'C2:4 Eb2:2 G2:2 Ab2:4 G2:4  Ab2:2 Bb2:1 Ab2:1 G2:2 Bb2:2 D3:4 C3:2 Bb2:2  '
      'G2:8 D3:4 Eb3:2 C3:2  D3:4 Eb3:8 F3:4  Bb2:4 R:12',
    S='Bb5:4 R:12  F5:4 D5:2 Bb4:2 Ab4:4 Bb4:4  Ab4:2 G4:1 Ab4:1 Bb4:2 G4:2 Eb4:4 F4:2 G4:2  '
      'Eb5:6 D5:2 C5:4 B4:4  C5:4 D5:4 A4:4 R:4  R:16  '
      'F5:4 Eb5:8 D5:2 C5:2  Bb4:4 R:12',
    A='G5:4 R:12  R:16  R:16  R:16  R:16  '
      'D5:4 Bb4:2 G4:2 F#4:4 G4:4  F4:2 Eb4:1 F4:1 G4:2 Eb4:2 C4:4 D4:2 Eb4:2  D4:4 R:12')
entry('T', 9, 0, 'The choirs meet: subject (tenor, E-flat)')
entry('S', 10, 0, 'inversion on F (soprano), a bar later', 2, 'inversus')
entry('B', 12, 0, 'subject (bass, c minor)')
entry('A', 14, 0, 'inversion on D (alto, g minor, turning to B-flat)', 2, 'inversus')
tag(9, 'The choirs meet: entries a bar apart')


# ===========================================================================
# 4. THE QUARREL (b17-21): Coro I has reached B-flat and means it (its note is
# A natural); Coro II answers in A-flat (its note is D-flat).  A bar each, then
# half a bar, then a beat.
put(17, T='Bb3:4 D4:2 F4:2 G4:4 F4:4', B='Bb2:8 Eb3:4 F3:2 A2:2')
entry('T', 17, 0, 'Coro I: head in B-flat', 1)
tag(17, 'The quarrel: B-flat (Coro I) against A-flat (Coro II), a bar each')
put(18, S='Eb5:4 C5:2 Ab4:2 G4:4 Ab4:4', A='C4:4 Eb4:2 F4:2 Db4:4 C4:4')
entry('S', 18, 0, 'Coro II: inverted head in A-flat', 1, 'inversus')
put(19, T='Bb3:4 D4:2 F4:2 R:8  Bb3:2 D4:2 F4:2 A4:2 R:8',
        B='Bb2:4 F2:2 A2:2 R:8  Bb2:4 F2:4 R:8',
        S='R:8 Eb5:4 C5:2 Ab4:2  R:8 Db5:4 C5:2 Ab4:2',
        A='R:8 Ab4:6 Db4:2  R:8 F4:4 Eb4:2 C4:2')
tag(19, 'half a bar')
put(21, T='Bb3:2 D4:1 F4:1 R:4 D4:2 F4:1 Bb4:1 R:4',
        B='Bb2:4 R:4 Bb2:4 R:4',
        S='R:4 Eb5:2 C5:1 Ab4:1 R:4 Eb5:2 Db5:1 C5:1~',
        A='R:4 C4:4 R:4 Ab4:4~')
tag(21, 'a beat')
# 5. RECONCILIATION (b22): Coro II's A-flat chord held over Coro I's B-flat --
# A-flat over B-flat, the home dominant; then both give a step (C-Bb, Eb-D).
put(22, S='C5:8 Bb4:8', A='Ab4:16', T='Eb4:8 D4:8', B='Bb2:16')
tag(22, 'Reconciliation: A-flat over B-flat')
put(23, S='Bb4:4 R:12', A='G4:4 R:12', T='Eb4:4 R:12', B='Eb3:4 R:12')

# === SECTIONS-END ===


def DYN(b):
    bar = b + 1
    if bar <= 8:
        return -3
    if 17 <= bar <= 22:
        return 3
    return 0


PAN = {'Soprano': 30, 'Alto': 40, 'Tenor': 88, 'Bass': 98}
TEMPO_MAP = [[0, BPM]]


def build(path=HERE / 'fugue.json'):
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'Fugue VII in E-flat major (a 4): Fuga a due cori',
            'composer': 'Claude / Sam', 'instrument': 'Two choirs of two voices (Coro II: soprano, alto; Coro I: tenor, bass)',
            'key': 'Eb', 'mode': 'major', 'meter': list(METER), 'bpm': BPM, 'tempo_map': TEMPO_MAP,
            'tempo_text': 'Allegro festivo', 'movement_number': 7, 'piece_type': 'fugue',
            'edition': 'third (Bach + 1)', 'voice_order': 'high_to_low',
            'markers': [{'t': (b - 1) * 4, 'label': t} for b, t in enumerate(TAGS, 1) if t]}
    voices = [('Soprano', 'S', 'treble', 72), ('Alto', 'A', 'treble', 70),
              ('Tenor', 'T', 'bass', 72), ('Bass', 'B', 'bass', 72)]
    data = build_score(path, meta, voices, BARS, entries=ENTRIES, subject=SUBJ, dynamics=DYN, tags=TAGS)
    for v in data['voices']:
        v['piano_pan'] = PAN[v['name']]
    data['voices'][1]['share_staff'] = 'Soprano'
    data['voices'][3]['share_staff'] = 'Tenor'
    Path(path).write_text(json.dumps(data, indent=1))
    return data


if __name__ == '__main__':
    build()
    print('bars', NBARS)
