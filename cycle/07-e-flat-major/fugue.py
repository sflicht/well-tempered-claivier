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
NAMES = ['Soprano', 'Alto', 'Tenor', 'Bass']
AB = {'S': 'Soprano', 'A': 'Alto', 'T': 'Tenor', 'B': 'Bass'}
NBARS = 46
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
# 3. THE CHOIRS MEET (b9-18).  For the first time all four voices sound
# together, on the tonic chord (9.1).  Entries a bar apart, choir against choir:
# the tenor's subject (E-flat) and, a bar later, the soprano's inversion on F
# above it; a two-voice episode down the lament bass c-B-flat-A-flat-G (b12-13);
# the bass's subject in c minor (b14); the alto's inversion in g minor (b16),
# which turns to B-flat (cadence 18.1).
put(9,
    T='Eb3:4 G3:2 Bb3:2 C4:4 Bb3:4  C4:2 D4:1 C4:1 Bb3:2 D4:2 F4:4 Eb4:2 D4:2  '
      'Eb4:4 D4:4 C4:4 B3:4  '
      'C4:8 Bb3:8  Ab3:8 G3:8  '
      'Eb3:4 G3:4 C4:4 F4:4  Eb4:4 Bb3:4 C4:4 A3:2 Bb3:2~  '
      'Bb3:8 A3:4 G3:4  Bb3:4 Bb3:4 G3:4 Bb3:2 A3:2  Bb3:8 R:8',
    B='Eb2:8 Ab2:4 G2:4  Ab2:4 Bb2:8 Eb3:4  F3:4 Bb2:4 C3:4 G2:2 R:2  '
      'R:16  R:16  '
      'C2:4 Eb2:2 G2:2 Ab2:4 G2:4  Ab2:2 Bb2:1 Ab2:1 G2:2 Bb2:2 D3:4 C3:2 Bb2:2  '
      'G2:8 D3:4 Eb3:2 C3:2  D3:4 Eb3:8 F3:4  Bb2:8 R:8',
    S='Bb5:4 R:12  F5:4 D5:2 Bb4:2 Ab4:4 Bb4:4  Ab4:2 G4:1 Ab4:1 Bb4:2 G4:2 Eb4:4 F4:2 G4:2  '
      'R:2 G5:4 F5:1 Eb5:1~ Eb5:4 D5:4  Eb5:6 D5:1 C5:1~ C5:4 B4:4  '
      'C5:6 D5:2 C5:4 B4:4  C5:4 D5:4 A4:4 R:4  R:16  '
      'F5:4 Eb5:8 D5:2 C5:2  Bb4:8 R:8',
    A='G5:4 R:12  R:16  R:16  R:16  R:16  R:16  R:16  '
      'D5:4 Bb4:2 G4:2 F#4:4 G4:4  F4:2 Eb4:1 F4:1 G4:2 Eb4:2 C4:4 D4:2 Eb4:2  D4:8 R:8')
entry('T', 9, 0, 'The choirs meet: subject (tenor, E-flat)')
entry('S', 10, 0, 'inversion on F (soprano), a bar later', 2, 'inversus')
entry('B', 14, 0, 'subject (bass, c minor)')
entry('A', 16, 0, 'inversion on D (alto, g minor, turning to B-flat)', 2, 'inversus')
tag(9, 'The choirs meet: entries a bar apart')
tag(12, 'Episode: the lament bass, tenor and soprano')
tag(18, 'Cadence in B-flat')


# ===========================================================================
# 4. THE QUARREL (b19-23): Coro I has reached B-flat and means it (its note is
# A natural); Coro II answers in A-flat (its note is D-flat).  A bar each, then
# half a bar, then a beat.
put(19, T='Bb3:4 D4:2 F4:2 G4:4 F4:4', B='Bb2:8 Eb3:4 F3:2 A2:2')
entry('T', 19, 0, 'Coro I: head in B-flat', 1)
tag(19, 'The quarrel: B-flat (Coro I) against A-flat (Coro II), a bar each')
put(20, S='Eb5:4 C5:2 Ab4:2 G4:4 Ab4:4', A='C4:4 Eb4:2 F4:2 Db4:4 C4:4')
entry('S', 20, 0, 'Coro II: inverted head in A-flat', 1, 'inversus')
put(21, T='Bb3:4 D4:2 F4:2 R:8  Bb3:2 D4:2 F4:2 A4:2 R:8',
        B='Bb2:4 F2:2 A2:2 R:8  Bb2:4 F2:4 R:8',
        S='R:8 Eb5:4 C5:2 Ab4:2  R:8 Db5:4 C5:2 Ab4:2',
        A='R:8 Ab4:6 Db4:2  R:8 F4:4 Eb4:2 C4:2')
tag(21, 'half a bar')
put(23, T='Bb3:2 D4:1 F4:1 R:4 D4:2 F4:1 Bb4:1 R:4',
        B='Bb2:4 R:4 Bb2:4 R:4',
        S='R:4 Eb5:2 C5:1 Ab4:1 R:4 Eb5:2 Db5:1 C5:1~',
        A='R:4 C4:4 R:4 Ab4:4~')
tag(23, 'a beat')
# 5. RECONCILIATION (b24): Coro II's A-flat chord held over Coro I's B-flat,
# the tenor joining it on E-flat: A-flat over B-flat, the home dominant.  Then
# both give a step (soprano C-B-flat, tenor E-flat-D) into B-flat seven.
put(24, S='C5:8 Bb4:8', A='Ab4:16', T='Eb4:8 D4:8', B='Bb2:16')
tag(24, 'Reconciliation: A-flat over B-flat')


# ===========================================================================
# 6. THE JOKE (b25-30).  Reconciled, Coro I turns pompous: French-overture
# dotted rhythms in the tenor over the bass, which begins the subject in
# AUGMENTATION.  Coro II cuts it short with the whole subject in DIMINUTION,
# chattered in one bar (b26: soprano, inverted; b28: alto, rectus, mocking).
# Coro I resumes each time, flustered, on C minor.  Then it gives up, and the
# heads are tossed across a beat apart.  The augmentation's last bar (F E-flat D)
# is never sung -- until the coda.
put(25, S='Bb4:4 R:12', A='G4:4 R:12',
        T='Eb4:4 G3:3 Bb3:1 Eb4:3 D4:0.5 Eb4:0.5 F4:3 G4:1',
        B='Eb2:8 G2:4 Bb2:4')
entry('B', 25, 0, 'Coro I: augmentation (pompous)', 4)
tag(25, 'The joke: augmentation, interrupted by diminution')
put(26, S='Bb5:2 G5:1 Eb5:1 D5:2 Eb5:2 D5:1 C5:0.5 D5:0.5 Eb5:1 C5:1 Ab4:2 Bb4:1 C5:1',
        A='G4:2 Bb4:2 Bb4:2 G4:2 F4:2 Ab4:2 F4:2 Eb4:2')
entry('S', 26, 0, 'Coro II: inversion in diminution (interrupting)', 1, 'inversus')
put(27, B='C3:8 Bb2:8', T='Eb4:3 D4:1 Eb4:2 R:1 F4:1 D4:3 C4:1 Bb3:4')
put(28, A='Eb4:2 G4:1 Bb4:1 C5:2 Bb4:2 C5:1 D5:0.5 C5:0.5 Bb4:1 D5:1 F5:2 Eb5:1 D5:1',
        S='G5:2 Eb5:2 Eb5:2 G5:2 Ab5:2 F5:2 Ab5:2 G5:2')
entry('A', 28, 0, 'Coro II: the subject in diminution (mocking Coro I)', 1)
put(29, B='C3:4 D3:2 C3:2 Bb2:4 D3:4', T='G4:3 Ab4:1 F4:3 Eb4:1 D4:3 C4:1 Bb3:4')
put(30, T='Bb3:2 D4:1 F4:1 R:4 C4:2 Eb4:1 G4:1 R:4',
        B='Bb2:4 R:4 C3:4 R:4',
        S='R:4 Bb5:2 G5:1 Eb5:1 R:4 D5:2 A4:1 F#4:1',
        A='R:4 G4:4 R:8')
tag(30, 'Coro I gives up: heads a beat apart')


# ===========================================================================
# 7a. EPISODE: THE CHOIRS SWAP (b31-32).  Reconciled, each choir now sings the
# other's form: Coro II's soprano the subject's head RECTUS (g minor), Coro I's
# tenor the head INVERTED (g minor), over a three-part texture that closes on
# g (the alto rests, to enter the stretto).
put(31, S='G4:4 Bb4:2 D5:2 Eb5:4 D5:4  Bb4:4 D5:4 C5:4 Bb4:4',
        T='Bb3:8 C4:4 Bb3:4  D4:4 Bb3:2 G3:2 F#3:4 G3:4',
        B='G2:8 C3:4 G2:4  G2:8 D3:4 G2:4')
entry('S', 31, 0, 'Coro II sings the head rectus (g)', 1)
entry('T', 32, 0, 'Coro I sings the head inverted (g)', 1, 'inversus')
tag(31, 'Episode: the choirs swap forms')


# ===========================================================================
# 7. STRETTO A 4 (b33-37): the choirs alternate, Coro II on the downbeats and
# Coro I on the half bars, and the levels fall by fifths to the tonic: alto
# inversion on D (g minor, b33.1); tenor subject on C (c minor, b33.3); soprano
# inversion on E-flat (A-flat, Coro II's plagal dialect, b34.1); and, last and
# lowest, the bass's subject in E-flat, home (b35.3).  The bass's subject ends
# on the leading tone and becomes a dominant pedal (b37.3-38): the tenor's head
# over it, then Coro II's soprano singing the RECTUS head up to C over
# A-flat-over-B-flat (b38.3), the reconciliation chord as the climax.
put(33,
    A='D5:4 Bb4:2 G4:2 F#4:4 G4:4  F4:2 Eb4:1 F4:1 G4:2 Eb4:2 C4:4 D4:2 Eb4:2  '
      'Bb4:4 F4:4 G4:4 G4:4  G4:4 Bb4:4 Ab4:4 Bb4:4  Ab4:16  '
      'G4:4 Bb4:4 Eb5:4 D5:4',
    T='R:8 C3:4 Eb3:2 G3:2  Ab3:4 G3:4 Ab3:2 Bb3:1 Ab3:1 G3:2 Bb3:2  D4:4 C4:2 Bb3:2 R:8  '
      'C4:4 D4:4 Eb4:4 D4:4  C4:4 R:4 Bb3:4 D4:2 F4:2  '
      'Bb3:4 Bb3:4 Ab3:8',
    S='R:16  Eb6:4 C6:2 Ab5:2 G5:4 Ab5:4  G5:2 F5:1 G5:1 Ab5:2 F5:2 D5:4 Eb5:2 F5:2  '
      'Eb5:4 D5:4 C5:4 F5:4  Ab5:4 F5:4 D5:4 F5:4  '
      'Eb5:4 G5:2 Bb5:2 C6:4 Bb5:4',
    B='G2:8 R:8  R:16  R:8 Eb2:4 G2:2 Bb2:2  C3:4 Bb2:4 C3:2 D3:1 C3:1 Bb2:2 D3:2  F3:4 Eb3:2 D3:2 Bb2:8  '
      'Bb2:8 Bb2:8')
entry('A', 33, 0, 'stretto: inversion on D (alto, g)', 2, 'inversus')
entry('T', 33, 2, 'stretto: subject on C (tenor, c)')
entry('S', 34, 0, 'stretto: inversion on E-flat (soprano, A-flat)', 2, 'inversus')
entry('B', 35, 2, 'stretto: subject in E-flat (bass, home)')
entry('T', 37, 2, 'dominant pedal: head (tenor)', 1)
entry('S', 38, 0, 'Coro II sings the rectus head, up to the climax', 1)
tag(33, 'Stretto a 4: the levels fall by fifths to the tonic')
tag(37, 'Dominant pedal')
tag(38, 'Climax: A-flat over B-flat')


# ===========================================================================
# 8. CODA (b39-46): the prelude remembered.  A ritornello bar (the alto: the
# inversion in diminution, as in the prelude's opening bars), then the first line of "Wachet auf" in long notes
# in the tenor (the register of BWV 645), louder, with the soprano running above
# it, the alto in quarters and the bass walking.  Under the chorale's C (b43)
# the bass at last finishes the augmentation it was never allowed to finish
# (F - E-flat - D, in the octave where it broke off).  The cadence is the
# reconciliation chord again (A-flat over B-flat, b44), then E-flat, and Coro
# II's last word: the head, upside down and soft.
put(39,
    S='G5:4 F5:4 D5:2 C5:2 R:4  '
      'R:2 Bb4:2 Eb5:2 D5:2 Eb5:2 F5:2 G5:2 F5:2  '
      'F5:4 G5:2 F5:2 Eb5:2 F5:2 D5:2 Eb5:2  '
      'Eb5:2 F5:2 G5:4 F5:2 D5:2 Eb5:2 C5:2  '
      'C5:2 D5:2 Eb5:6 D5:2 F5:4  '
      'Eb5:8 D5:8  '
      'Eb5:8 Bb5:4 G5:2 Eb5:2  D5:4 Eb5:12',
    A='Bb4:2 G4:1 Eb4:1 D4:2 Eb4:2 D4:1 C4:0.5 D4:0.5 Eb4:1 C4:1 Ab3:2 Bb3:1 C4:1  '
      'G4:12 Bb4:4  Bb4:4 G4:8 F4:4  G4:4 Bb4:8 G4:4  Ab4:8 C5:4 Ab4:4  '
      'C5:4 Ab4:12  G4:16  Bb4:16',
    T='G3:4 R:12  Eb3:8 G3:8  Bb3:12 Bb3:4  Bb3:8 Bb3:8  C4:16  Bb3:16  G3:16  G3:16',
    B='Eb3:4 Bb2:4 Bb2:2 Ab2:2 F2:4  '
      'Eb2:4 G2:4 C3:4 Bb2:4  D3:4 Eb3:4 G2:4 Ab2:4  G2:4 Eb3:4 Bb2:4 C3:4  '
      'F3:8 Eb3:4 D3:4  Bb2:16  Eb2:16  Eb2:16')
entry('A', 39, 0, 'ritornello: the inversion in diminution (as in the prelude)', 1, 'inversus')
entry('T', 40, 0, 'Chorale "Wachet auf", line 1 (tenor)', 5)
entry('B', 43, 0, 'Coro I finishes its augmentation (F E-flat D)', 1)
entry('S', 45, 2, 'Coro II: the head, upside down', 1, 'inversus')
tag(39, 'Coda: ritornello, then "Wachet auf" in the tenor')
tag(43, 'The augmentation finished')
tag(44, 'A-flat over B-flat, then E-flat')

# === SECTIONS-END ===


LEVEL = {1: -4, 9: 0, 12: -3, 14: 0, 19: 2, 21: 3, 23: 4, 24: 5, 25: 2, 31: 0, 33: 2, 35: 4, 37: 6, 38: 8,
         39: -1, 40: 0, 44: 2, 45: -2}


def DYN(b):
    """Phrase dynamics by bar index (0-based)."""
    bar, v = b + 1, 0
    for k in sorted(LEVEL):
        if k <= bar:
            v = LEVEL[k]
    return v


# Performance only (no notes).  Coro II (soprano, alto) on the left, Coro I
# (tenor, bass) on the right; in the joke Coro I's pomp is heavier and Coro II's
# chatter lighter and detached; the chorale in the coda sings out; Coro II's
# last word is soft.
PAN = {'Soprano': 30, 'Alto': 40, 'Tenor': 88, 'Bass': 98}
BPM = 76
TEMPO_MAP = [[0, BPM],
             [66, BPM], [68, 66, 'ramp'], [72, BPM],        # b17.3-18: breath at the B-flat cadence
             [88, BPM], [94, 62, 'ramp'], [96, BPM],        # b23-24: broadening into the reconciliation
             [146, BPM], [151, 64, 'ramp'], [152, 72],      # b37.3-38: the climax, then the coda
             [172, 72], [184, 50, 'ramp']]                  # b44-46: final ritardando


def q(bar, beat=1):
    return (bar - 1) * 4 + (beat - 1)


def build(path=HERE / 'fugue.json'):
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'Fugue VII in E-flat major (a 4): Fuga a due cori',
            'composer': 'Claude / Sam', 'instrument': 'Keyboard: two choirs of two voices (Coro II right hand, Coro I left hand)',
            'key': 'Eb', 'mode': 'major', 'meter': list(METER), 'bpm': BPM, 'tempo_map': TEMPO_MAP,
            'tempo_text': 'Allegro festivo', 'movement_number': 7, 'piece_type': 'fugue',
            'edition': 'third (Bach + 1)', 'voice_order': 'high_to_low',
            'markers': [{'t': (b - 1) * 4, 'label': t} for b, t in enumerate(TAGS, 1) if t]}
    voices = [('Soprano', 'S', 'treble', 72), ('Alto', 'A', 'treble', 70),
              ('Tenor', 'T', 'bass', 72), ('Bass', 'B', 'bass', 72)]
    data = build_score(path, meta, voices, BARS, entries=ENTRIES, subject=SUBJ, dynamics=DYN, tags=TAGS)
    coro_ii = ('Soprano', 'Alto')
    for v in data['voices']:
        v['piano_pan'] = PAN[v['name']]
        for e in v['events']:
            t = float(e['t'])
            if v['name'] not in coro_ii and any(q(b) <= t < q(b + 1) for b in (25, 27, 29)):
                e['v'] = min(112, int(e['v']) + 6)       # the joke: Coro I's pomp, heavier
            if v['name'] in coro_ii and any(q(b) <= t < q(b + 1) for b in (26, 28)):
                e['v'] = max(30, int(e['v']) - 4)        # Coro II's chatter, lighter
                e['gate'] = 0.55                         # and detached
            if v['name'] == 'Tenor' and q(40) <= t < q(45):
                e['v'] = min(112, int(e['v']) + 10)      # the chorale sings out
            if v['name'] == 'Soprano' and t >= q(45, 3):
                e['v'] = max(30, int(e['v']) - 18)       # the last word, soft
    data['voices'][1]['share_staff'] = 'Soprano'
    data['voices'][3]['share_staff'] = 'Tenor'
    Path(path).write_text(json.dumps(data, indent=1))
    return data


if __name__ == '__main__':
    build()
    print('bars', NBARS)
