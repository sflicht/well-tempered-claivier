#!/usr/bin/env python3
"""Fugue XVI in G minor, five voices: "Fantasia e fuga a 5 per Reincken" (third edition, Bach + 1).

Hamburg, 1720: Bach improvises for nearly half an hour on the chorale "An Wasserflüssen Babylon"
before Johann Adam Reincken, who had written a vast fantasia on that chorale.  Reincken: "I thought
this art was dead, but I see that in you it still lives."  This movement imagines a few minutes of
that improvisation as a chorale fantasia for an organ with two pedal voices, in five real voices,
the number of Bach's own setting with double pedal, BWV 653b (a 5 voci, a 2 Clav. e doppio Pedale):

  Diskant, Alt, Tenor (the manuals)          Pedal I (8'), Pedal II (16')

Every chorale line is first treated by the three manual voices in a short fugal fore-imitation
(Vorimitation) on a subject made from that line's own notes; then the line itself sounds in long
notes in the pedal, as a canon at the octave: Pedal II (the bass) leads, Pedal I follows an octave
higher.  The follower comes in a little sooner in every line -- 6 1/2, 5, 4 1/2, 4, 3 1/2, 3,
2 1/2 and 1 1/2 beats after the leader -- so the canon closes in as the piece goes on.  Lines 3-4
(the repeat of lines 1-2) are an echo passage for the manuals alone.  Before the last line, the
subject of Bach's G-minor organ fugue BWV 542 (linked since Spitta with the Hamburg visit) enters
once, on top, as a guest; the last line then joins its closest canon to a stretto of its own
subject in the manuals.

The chorale is copied from the soprano of Bach's four-part setting BWV 267 (music21 corpus
bach/bwv267) and moved from G major into G minor (B -> B-flat; E -> E-flat except in line 8, which
keeps its E natural; the C-sharp of line 6 is kept).  Every other note is written here by hand.
Thematic statements are explicit transforms (octave, real or diatonic transposition, augmentation)
of the hand-written subjects; nothing chooses pitches.
"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (4, 4)
NAMES = ['S', 'A', 'T', 'P1', 'P2']
LONG = ['Diskant', 'Alt', 'Tenor', 'Pedal I', 'Pedal II']
ABBR = ['Disk.', 'Alt', 'Ten.', 'Ped. I', 'Ped. II']
CLEF = ['treble', 'treble', 'treble_8', 'bass', 'bass']
GNAT = [7, 9, 10, 0, 2, 3, 5]          # G natural minor from the tonic, for diatonic shifts

# ---------------------------------------------------------------- the chorale
# "An Wasserflüssen Babylon" (Wolfgang Dachstein, 1525), soprano of BWV 267, in G minor, in its own
# rhythm (BWV 267's quarter = 4 sixteenths).  Lines 3-4 repeat lines 1-2 (bar form AAB).
CHORALE = {
    1: 'D5:4 Eb5:4 D5:2 C5:2 Bb4:2 C5:2 D5:4 C5:2 Bb4:2 C5:4 Bb4:4',      # An Wasserflüssen Babylon
    2: 'A4:4 Bb4:4 C5:4 D5:4 C5:2 Bb4:2 A4:2 G4:2 A4:4 G4:4',             # da saßen wir mit Schmerzen
    5: 'G4:4 A4:4 Bb4:4 C5:2 Bb4:2 A4:4 Bb4:4 A4:4 G4:4',                 # wir hingen auf mit schwerem Mut
    6: 'G4:2 A4:2 Bb4:4 C5:4 D5:4 Eb5:4 Bb4:4 C#5:4 D5:4',                # die Harfen und die Orgeln gut
    7: 'Bb4:2 C5:2 D5:4 Eb5:4 D5:2 C5:2 Bb4:4 C5:8 Bb4:4',                # an ihre Bäum der Weiden
    8: 'E5:4 E5:4 E5:4 A4:4 D5:4 C5:4 Bb4:4 A4:4',                         # die drinnen sind in ihrem Land
    9: 'C5:4 Bb4:4 A4:4 G4:4 A4:2 G4:2 F4:4 Eb4:4 D4:4',                   # da mussten wir viel Schmach und Schand
    10: 'D4:4 G4:4 A4:4 Bb4:6 C5:2 D5:4 C5:2 Bb4:2 A4:4 Bb4:2 C5:2 A4:8 G4:4',  # täglich von ihn' erleiden
}
CHORALE[3], CHORALE[4] = CHORALE[1], CHORALE[2]


# ---------------------------------------------------------------- transforms of written material
def oc(s, n):
    return W.transpose(s, 12 * n, 7 * n)


def tr(s, semis, letters):
    return W.transpose(s, semis, letters)


def dsh(toks, steps, scale=GNAT):
    """Diatonic (modal) transposition within G minor; chromatic notes keep their inflection."""
    out = []
    t0 = scale[0]
    for t in toks.split():
        p, d, sp, tie = W.parse_tok(t)
        if p is None:
            out.append(t)
            continue
        pc = p % 12
        nl = 'CDEFGAB'[('CDEFGAB'.index(sp[0].upper()) + steps) % 7]
        if pc in scale:
            deg = ((p - t0) // 12) * 7 + scale.index(pc)
            nd = deg + steps
            q = t0 + (nd // 7) * 12 + ((scale[nd % 7] - t0) % 12)
        else:
            q = None
            for alt in (-1, 1):
                if (pc - alt) % 12 in scale:
                    base = p - alt
                    deg = ((base - t0) // 12) * 7 + scale.index(base % 12)
                    nd = deg + steps
                    q = t0 + (nd // 7) * 12 + ((scale[nd % 7] - t0) % 12) + alt
                    break
        out.append(f"{W.name_of(q, nl)}:{t.rsplit(':', 1)[1]}")
    return ' '.join(out)


def cantus(line, octaves, last=None):
    """The chorale line in augmentation (x2) for the pedal; the last note lasts `last` sixteenths."""
    toks = W.scale_rhythm(CHORALE[line], 2).split()
    if last is not None:
        toks[-1] = toks[-1].rsplit(':', 1)[0] + f':{last}'
    return oc(' '.join(toks), octaves)


# ---------------------------------------------------------------- subjects (all hand-written)
# Each chorale line becomes a subject with its own speed and gesture; the notes are the line's own.
S1 = 'D5:4 Eb5:4 D5:2 C5:2 Bb4:2 C5:2 D5:4 C5:2 Bb4:2 C5:4 Bb4:4'          # 1: the line as sung, grave
S2 = 'A4:3 Bb4:1 C5:3 D5:1 C5:2 Bb4:2 A4:3 G4:1 A4:4 G4:4'                 # 2: "mit Schmerzen", limping
S5 = 'G4:2 A4:4 Bb4:4 C5:2 Bb4:2 A4:4 Bb4:4 A4:4 G4:6'                     # 5: "hingen", hung across beats
S6 = 'G4:1 A4:1 Bb4:1 C5:1 D5:2 Eb5:2 Bb4:2 C#5:2 D5:4'                    # 6: "Harfen und Orgeln", tirata
S7 = 'Bb4:4/3 C5:4/3 D5:4/3 Eb5:4 D5:4/3 C5:4/3 Bb4:4/3 C5:4 Bb4:4'       # 7: "Weiden", swaying triplets
S8 = 'E5:2 E5:2 E5:2 A4:2 D5:3 C5:1 Bb4:2 A4:2'                            # 8: "in ihrem Land", knocking
S9 = 'C5:4 B4:2 Bb4:2 A4:4 G4:4 A4:2 G4:2 F4:2 E4:2 Eb4:4 D4:4'            # 9: "Schmach", chromatic fall
S10 = 'D4:2 G4:2 A4:2 Bb4:3 C5:1 D5:2 C5:1 Bb4:1 A4:2 Bb4:1 C5:1 A4:4 G4:4'  # 10: "täglich", eighths
# J. S. Bach, Fugue in G minor BWV 542, the subject as first stated (soprano, b1.2.5-b4.2.5; Mutopia
# edition, read as data).  Starts on the offbeat of beat 2; ends on G.
BWV542 = ('D5:2 Bb4:1 C5:1 A4:1 Bb4:1 G4:2 G5:2 F#5:1 G5:1 E5:1 F#5:1 D5:2 G5:1 D5:1 Eb5:2 C5:2 F4:2 F5:2 '
          'D5:1 Eb5:1 C5:1 D5:1 Bb4:2 Eb5:1 Bb4:1 C5:2 A4:2 D4:2 D5:2 Bb4:1 C5:1 A4:1 Bb4:1 G4:2')

A1 = tr(S1, -5, -3)          # answer a fourth lower (D minor, ending on F)

# ---------------------------------------------------------------- placement
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


def X(v, bar, beat, toks, label=None):
    if label:
        theme(v, bar, beat, toks, label)
    else:
        put(v, bar, beat, toks)


def assemble(v, nbars):
    segs = sorted(VO[v], key=lambda x: x[0])
    out, cur = [], Fr(0)
    for s, toks in segs:
        if s < cur:
            raise ValueError(f'{v}: overlap at bar {float(s / 16 + 1)}: {toks[:50]}')
        if s > cur:
            out.append(f'R:{s - cur}')
        out.append(toks)
        cur = s + dur16(toks)
    total = Fr(nbars * 16)
    if cur > total:
        raise ValueError(f'{v}: runs past the end ({float(cur / 16)} > {nbars})')
    if cur < total:
        out.append(f'R:{total - cur}')
    return W.concat_bars(' '.join(out), METER)


# ================================================================ A: line 1 (bars 1-11)
# "An Wasserflüssen Babylon".  Exposition of subject 1 (Tenor, Alt answer, Diskant), the Tenor's
# countersubject flowing in eighths (the waters); then the line in the pedal, Pedal II leading in
# the bass, Pedal I following an octave higher 6 1/2 beats later; cadence in B-flat over the held
# B-flat of Pedal II.
X('T', 1, 1, oc(S1, -1), 'line 1 Vorimitation: subject 1 (Tenor)')
X('A', 2, 3, A1, 'line 1 Vorimitation: answer (Alt)')
X('S', 4, 1, S1, 'line 1 Vorimitation: subject 1 (Diskant)')
X('T', 3, 1, 'D4:2 C#4:2 D4:2 Bb3:2 A3:2 Bb3:2 C4:2 A3:2 G3:4 A3:4 Bb3:4 G3:4 F3:4 Eb3:4 D3:4 G3:4')
X('A', 4, 3, 'F4:4 G4:4 Bb4:4 G4:4 F#4:4 G4:4')
X('P2', 6, 1, cantus(1, -2, last=36), 'cantus line 1 (Pedal II, canon dux)')
X('P1', 7, 3.5, cantus(1, -1, last=10), 'cantus line 1 (Pedal I, canon at the octave, 6 1/2 beats)')
X('S', 6, 1, 'A4:8 C5:8 A4:8 Bb4:4 A4:4 A4:4 C5:6 A4:2 D5:4 Eb5:4 D5:2 C5:2 Eb5:4 D5:4 '
             'D5:4 Eb5:4 D5:4 C5:4 Bb4:8')
# (Nov 2026) Under the pedal canon the Alt keeps the Tenor's running eighths (b6-7, b9) instead of
# leaning on F#-G in half notes; b8 stays (Pedal I's E-flat4 - D4 lies a third below it).
X('A', 6, 1, 'F#4:2 D4:2 E4:2 F#4:2 G4:2 Eb4:2 F4:2 G4:2 F#4:2 E4:2 D4:2 E4:2 G4:4 F#4:4 F#4:8 G4:2 F#4:2 G4:4 '
             'Eb4:2 F4:2 G4:2 A4:2 G4:4 F4:4 F4:4 A4:4 Bb4:4 A4:4 F4:8')


# ================================================================ B: line 2 (bars 11-18)
# "da saßen wir mit Schmerzen".  The limping subject climbs through the manuals in canon at the
# octave, three beats apart (Tenor, Alt, Diskant); then the line in the pedal, the follower now
# 5 beats behind; the Stollen closes on G over the held G of Pedal II.
X('T', 11, 3, oc(S2, -1), 'line 2 Vorimitation: subject 2 (Tenor)')
X('A', 12, 2, S2, 'line 2 Vorimitation: subject 2 in canon at the octave, 3 beats (Alt)')
X('S', 13, 1, oc(S2, 1), 'line 2 Vorimitation: subject 2 in canon at the octave, 3 beats (Diskant)')
X('T', 13, 1, 'F3:4 A3:4 Bb3:4 D4:4 C4:8 Bb3:4')
X('A', 13, 4, 'F#4:4 F4:4 Eb4:4 D4:4 G4:4 G4:3 F#4:1 G4:3 A4:1 F#4:4 F4:4 G4:3 F4:1 Eb4:3 F4:1 F#4:4 G4:4 '
              'F#4:3 E4:1 F#4:4 G4:4 F#4:4 G4:4 F#4:8 G4:4')
X('S', 14, 3, 'G5:4 F5:4 Eb5:8 D5:8 Eb5:8 D5:4 Bb4:4 C5:4 A4:4 Bb4:4 D5:4 D5:4 C5:8 Bb4:4')
X('P2', 14, 1, cantus(2, -2, last=28), 'cantus line 2 (Pedal II, canon dux)')
X('P1', 15, 2, cantus(2, -1, last=4), 'cantus line 2 (Pedal I, canon at the octave, 5 beats)')


# ================================================================ C: lines 3-4 (bars 19-24), manuals alone
# "als wir gedachten an Zion, da weinten wir von Herzen".  The repeat of lines 1-2 is an echo
# passage for the manuals: the chorale itself in the Diskant (where BWV 653b has it), and the close
# of each line echoed softly at the same pitch by Alt and Tenor (velocities lowered in ECHO below).
X('S', 19, 1, 'D5:4 Eb5:4 D5:2 C5:2 Bb4:2 C5:2 D5:4 C5:2 Bb4:2 C5:4 Bb4:4', 'line 3: the chorale in the Diskant')
X('A', 19, 1, 'G4:2 F4:2 Eb4:2 G4:2 F#4:4 G4:2 F#4:2 G4:4 Eb4:8 D4:4')
X('T', 19, 1, 'Bb3:4 C4:4 A3:4 G3:2 A3:2 Bb3:4 A3:4 F3:4 Bb2:4')
X('A', 21, 1, 'D5:4 C5:2 Bb4:2 C5:4 Bb4:4', 'line 3: echo of "an Zion" (Alt)')
X('T', 21, 1, 'Bb3:4 A3:4 F3:4 Bb2:4')
X('S', 22, 1, 'A4:4 Bb4:4 C5:4 D5:4 C5:2 Bb4:2 A4:2 G4:2 A4:4 G4:4', 'line 4: the chorale in the Diskant')
X('A', 22, 1, 'R:4 D4:4 G4:4 F#4:4 G4:4 F#4:8')
X('T', 22, 1, 'F#3:4 G3:4 Eb3:4 D3:4 A2:4 D3:4 D3:4 G2:4')
X('A', 24, 1, 'C5:2 Bb4:2 A4:2 G4:2 A4:4 G4:4', 'line 4: echo of "von Herzen" (Alt)')
X('T', 24, 1, 'A2:4 D3:4 D3:4 G2:4')
ECHO = [('A', 21, 22, -16), ('T', 21, 22, -16), ('A', 24, 25, -16), ('T', 24, 25, -16)]

# ================================================================ D: line 5 (bars 25-32)
# "wir hingen auf mit schwerem Mut".  The subject hangs across the beats; Tenor, Alt and then the
# pedal (the line in augmentation) enter five beats apart; the Diskant enters free above, and
# Pedal I follows the pedal line 4 1/2 beats behind.  The line closes on G over the held G.
X('T', 25, 1, oc(S5, -1), 'line 5 Vorimitation: subject 5 (Tenor)')
X('A', 25, 1, 'D4:4 F4:4 D4:4 F4:4')
X('A', 26, 2, S5, 'line 5 Vorimitation: subject 5, 5 beats later (Alt)')
X('P2', 27, 3, cantus(5, -2, last=20), 'cantus line 5 (Pedal II, canon dux)')
X('T', 27, 1, 'G3:2 F#3:4 G3:2 D4:4 C4:12')
X('A', 28, 2, 'F#4:4 D4:4 Eb4:4 G4:2 F#4:2 F#4:4 F4:10 Eb4:10 D4:4 G4:10 F#4:8 G4:6')
X('S', 28, 3, 'G5:4 F5:4 Eb5:2 D5:2 C5:8 Eb5:4 D5:2 Eb5:4 D5:2 C5:8 D5:8 C5:10 Bb4:4')
X('P1', 28, 3.5, cantus(5, -1, last=6), 'cantus line 5 (Pedal I, canon at the octave, 4 1/2 beats)')

# ================================================================ E: line 6 (bars 32-39)
# "die Harfen und die Orgeln gut".  The harps are rushing scales (tirate) falling through the
# manuals, Diskant, Alt (the answer, on D), Tenor; the organs are the pedal canon, 4 beats
# apart, where the line's B-flat - C-sharp ("Orgeln") makes an augmented sixth over C-sharp in the
# bass.  Half cadence on D; then the organ is "hung up": a general pause.
X('S', 32, 3, oc(S6, 1), 'line 6 Vorimitation: subject 6, the harps (Diskant)')
X('A', 32, 4.5, dsh(S6, -3), 'line 6 Vorimitation: answer on D (Alt)')
X('T', 33, 4, oc(S6, -1), 'line 6 Vorimitation: subject 6 (Tenor)')
X('S', 33, 3, 'E6:4 C#6:4 D6:4 E6:4 D6:4 C6:4 Bb5:8 G5:4 F#5:4 G5:8 G5:4 Eb5:4 F5:8 G5:16 F#5:16')
X('A', 33, 4.5, 'G4:2 F4:4 G4:8 F#4:4 G4:8 Eb4:4 D4:4 D4:8 G4:8 F4:8 Bb4:16 A4:16')
X('P2', 34, 3, cantus(6, -2, last=24), 'cantus line 6 (Pedal II, canon dux)')
X('P1', 35, 3, cantus(6, -1, last=8), 'cantus line 6 (Pedal I, canon at the octave, 4 beats)')

# ================================================================ F: line 7 (bars 40-45)
# "an ihre Bäum der Weiden".  After the pause, B-flat major: the subject sways in triplets (Alt) over
# its own mirror image in the Tenor (the willow reflected in the water), the Diskant follows at the
# octave two beats later and keeps swaying above the pedal canon, now 3 1/2 beats apart.
S7M = oc(dsh(W.invert_diatonic(S7, 'Bb4', GNAT), -3), -1)
X('A', 40, 1, S7, 'line 7 Vorimitation: subject 7 (Alt)')
X('T', 40, 1, S7M, 'line 7 Vorimitation: subject 7 mirrored, at the same time (Tenor)')
X('S', 40, 3, oc(S7, 1), 'line 7 Vorimitation: subject 7 at the octave, 2 beats later (Diskant)')
X('P2', 41, 1, cantus(7, -2, last=20), 'cantus line 7 (Pedal II, canon dux)')
X('P1', 41, 4.5, cantus(7, -1, last=6), 'cantus line 7 (Pedal I, canon at the octave, 3 1/2 beats)')
X('S', 41, 4, 'F5:4 Eb5:4/3 F5:4/3 G5:4/3 G5:4 F5:4/3 Eb5:4/3 D5:4/3 Eb5:4 Eb5:4/3 D5:4/3 C5:4/3 D5:4 Eb5:4 '
              'G5:4 E5:4 F5:8 Eb5:8 D5:4')
X('A', 41, 2, 'A4:4 F4:4 Bb4:4 G4:8 Bb4:4 G4:4 G4:4 Bb4:4 G4:4 Eb4:4 G4:4 C5:4 F4:20')

# ================================================================ G: line 8 (bars 46-51)
# "die drinnen sind in ihrem Land".  The line keeps its E natural: after B-flat major, a lone Tenor
# knocks on E, the Diskant answers at the octave two beats later, and the pedal knocks on E in canon,
# 3 beats apart.  The line closes on A with a Phrygian B-flat - A in Pedal I over A in Pedal II.
X('T', 46, 1, oc(S8, -1), 'line 8 Vorimitation: subject 8 (Tenor)')
X('S', 46, 3, S8, 'line 8 Vorimitation: subject 8 at the octave, 2 beats later (Diskant)')
X('P2', 47, 3, cantus(8, -2, last=12), 'cantus line 8 (Pedal II, canon dux)')
X('P1', 48, 2, cantus(8, -1, last=4), 'cantus line 8 (Pedal I, canon at the octave, 3 beats)')
X('T', 47, 1, 'Bb3:4 G3:4')
X('A', 46, 3, 'G#4:2 A4:2 G4:2 F4:2 D4:6 E4:2 G#4:4 A4:4 G#4:4 A4:4 G#4:8 A4:16 C5:4 A4:4 '
              'F4:4 G4:4 A4:4 C#5:12')
X('S', 47, 3, 'B4:4 C5:4 D5:4 C5:4 B4:8 C#5:4 E5:4 F5:8 E5:4 F5:4 D5:4 E5:4 F5:4 G5:12')

# ================================================================ H: line 9 (bars 52-57)
# "da mussten wir viel Schmach und Schand".  The Alt's C-sharp falls to C and the subject fills the
# line's descent chromatically (passus duriusculus) over a chromatic bass in the Tenor; the pedal
# canon, now 2 1/2 beats apart, turns the line's end into a lament bass G - F - E-flat - D and a
# half cadence on D.
X('A', 52, 1, S9, 'line 9 Vorimitation: subject 9 (Alt)')
X('S', 52, 1, 'F5:8 D5:4 C5:4 C5:4 D5:4 C5:4 A4:4')
X('T', 52, 1, 'D3:4 G3:4 F3:4 E3:4 Eb3:4 D3:4')
X('P2', 53, 3, cantus(9, -2, last=24), 'cantus line 9 (Pedal II, canon dux)')
X('P1', 54, 1.5, cantus(9, -1, last=14), 'cantus line 9 (Pedal I, canon at the octave, 2 1/2 beats)')
X('S', 54, 1, 'Bb4:4 Eb5:8 D5:4 D5:4 C5:8 Bb4:4 D5:4 C5:8 A4:4 Bb4:2')
# (Nov 2026) b55-56: the dotted 3+1 limp of b15-17 instead of quarters.
X('A', 54, 1, 'G4:6 F#4:2 F4:4 D4:4 G4:3 F#4:1 E4:4 F#4:3 E4:1 G4:4 Bb4:3 A4:1 F4:4 G4:3 F4:1 C4:4 D4:4 F#4:4 G4:4 D4:4 A4:8 R:8 F4:4 G4:4 '
              'Eb4:4 R:4 G4:4 D4:4')

# ================================================================ I: the guest (bars 57-60)
# J. S. Bach's G-minor fugue subject (BWV 542) enters once, on top, at its own pitch, over the held
# D of the pedal and then a pedal bass walking its circle of fifths; Alt alone accompanies, below.
X('S', 57, 2.5, BWV542, 'guest: J. S. Bach, Fugue in G minor BWV 542, subject (Diskant)')
X('P2', 58, 3, 'C2:2 Eb2:2 F2:4 Bb2:4 Eb3:4 A2:4 D3:4 D2:4 G2:4')

# ================================================================ J: line 10, the summit (bars 60-66)
# "täglich von ihn' erleiden".  The pedal canon at its closest, 1 1/2 beats; above it the line's
# subject (the line at four times the speed of the pedal) in stretto, Diskant and then Alt an
# octave lower; the Tenor joins for the cadence, the only stretch with five voices moving.
X('P2', 60, 3, cantus(10, -2, last=48), 'cantus line 10 (Pedal II, canon dux)')
X('P1', 60, 4.5, cantus(10, -1, last=42), 'cantus line 10 (Pedal I, canon at the octave, 1 1/2 beats)')
X('S', 60, 3.5, oc(S10, 1), 'summit: subject 10 (Diskant), with its own augmentation in the pedal')
X('A', 61, 2.5, S10, 'summit: subject 10 an octave lower, 3 beats later (Alt)')
X('S', 62, 2, 'F5:4 G5:4 Eb5:4 D5:4 F#5:4 A5:4 Bb5:4 C6:4 D6:8 Eb6:4 D6:8 C6:4 A5:2 C6:2 Bb5:8')
# (Nov 2026) b65: the seventh C5 falls through B-flat4 to A4 (it leapt to A4).
X('A', 63, 1, 'G4:4 A4:2 D5:2 Bb4:1 C5:1 A4:1 Bb4:1 G4:4 Eb5:4 D5:8 C5:6 Bb4:2 A4:4 F#4:8 G4:8')
X('T', 64, 1, 'G4:8 F4:8 D4:28')

# ================================================================ K: coda (bars 66-68)
# Over the held G of both pedals, the Tenor, which began the piece, sings the head of line 1 once
# more and turns its last B-flat into B natural: G major.
X('T', 66, 4, 'Eb4:4 D4:2 C4:2 Bb3:2 C4:2 D4:4 C4:4 B3:16', 'coda: head of line 1 (Tenor), ending in G major')
X('S', 66, 3, 'A5:4 G5:4 G5:8 F#5:8 G5:16')
X('A', 66, 3, 'F#4:4 G4:4 G4:4 Eb4:4 C5:4 A4:4 D5:16')

# ================================================================ BUILD
BPM = 72
# Tempo map, t in quarters (bar b starts at 4*(b-1)).  Grave for the Stollen; the echo passage
# slower; lines 5-6 a little quicker; the half cadence of line 6 broadens into the general pause;
# lines 7-8 move on; line 9 slows into its half cadence; the guest a little brisker; the summit
# broadens into its cadence; a long final ritardando over the tonic pedal.
TEMPO = {'tempo_map': [[0, 72], [40, 69, 'ramp'], [42, 72], [72, 66], [96, 74], [148, 74],
                       [154, 56, 'ramp'], [156, 76], [204, 74], [224, 64, 'ramp'], [225, 76],
                       [238, 72], [256, 64, 'ramp'], [262, 60], [268, 50, 'ramp'], [272, 40, 'ramp']]}
# phrase dynamics (velocity offsets from this bar on)
DYN = {1: -6, 6: -3, 11: -4, 14: -1, 19: -4, 25: -3, 32: 0, 36: 3, 38: 1, 40: -3, 46: -1, 52: 1,
       57: 3, 60: 6, 63: 8, 66: 5, 68: 7}
# registration: Diskant leads, Alt and Tenor a little softer, the pedals full; Pedal I (the canon's
# follower, in the tenor register) as strong as the leader so the canon can be heard
BASEVEL = [70, 63, 64, 68, 70]
MARKS = [(1, 'Line 1: subject 1 (Tenor, Alt, Diskant)'), (6, 'Line 1 in the pedal, canon at 6 1/2 beats'),
         (11, 'Line 2: limping subject, canon at the octave'), (14, 'Line 2 in the pedal, canon at 5 beats'),
         (19, 'Lines 3-4: echo (manuals alone)'), (25, 'Line 5: syncopated subject'),
         (27, 'Line 5 in the pedal, canon at 4 1/2 beats'), (32, 'Line 6: the harps (tirate)'),
         (34, 'Line 6 in the pedal, canon at 4 beats; augmented sixth at b37'), (39, 'General pause'),
         (40, 'Line 7: triplets and their mirror; canon at 3 1/2 beats'),
         (46, 'Line 8: E natural, knocking; canon at 3 beats'),
         (52, 'Line 9: chromatic fall; canon at 2 1/2 beats'), (57, 'Guest: BWV 542 subject (Diskant)'),
         (60, 'Summit: line 10, canon at 1 1/2 beats, stretto of subject 10'), (66, 'Coda: line 1 returns; G major')]


# Voicing (performance data, not notes), as (voice, from quarter, to quarter, velocity change):
# line 2's canon entries begin on the note of the voice before, so the entering voice is lifted for
# its first bar (review item 4); at the summit Pedal I, the canon's follower, is lifted and Pedal II
# lowered, so the late upper line is heard as a line of its own rather than as a doubled bass.
VOICING = [('A', 44, 48, 6), ('S', 48, 52, 6), ('P1', 238, 266, 6), ('P2', 238, 266, -4)]


def soften_echoes(path):
    """Performance data, not notes: the echo bars are played on a softer manual; VOICING applied."""
    import json
    data = json.loads(Path(path).read_text())
    table = [(v, (b0 - 1) * 4, (b1 - 1) * 4, dv) for v, b0, b1, dv in ECHO] + VOICING
    for v, t0, t1, dv in table:
        name = LONG[NAMES.index(v)]
        for voice in data['voices']:
            if voice['name'] != name:
                continue
            for e in voice['events']:
                if t0 <= e['t'] < t1:
                    e['v'] = max(24, min(118, e['v'] + dv))
    Path(path).write_text(json.dumps(data, indent=1))


def build(nbars, path=None):
    bars = {LONG[i]: assemble(n, nbars) for i, n in enumerate(NAMES)}
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Fugue XVI in G minor, five voices: Fantasia e fuga a 5 per Reincken',
            'composer': 'Claude / Sam (on "An Wasserflüssen Babylon"; after Reincken, BWV 653b and BWV 542)',
            'instrument': 'Organ in spirit (three manual voices and double pedal); playable on one keyboard '
                          'except at the summit',
            'key': 'G', 'mode': 'minor', 'meter': list(METER), 'bpm': BPM,
            'tempo_text': 'Fantasia: Grave',
            'movement_number': 16, 'piece_type': 'fugue', 'edition': 'third',
            'voice_order': 'high_to_low',
            'markers': [{'t': float((b - 1) * 4), 'label': txt} for b, txt in MARKS]}
    meta.update(TEMPO)
    voices = [(LONG[i], ABBR[i], CLEF[i], BASEVEL[i]) for i in range(len(NAMES))]

    def dynamics(b):
        v = 0
        for k in sorted(DYN):
            if b + 1 >= k:
                v = DYN[k]
        return v
    out = path or HERE / 'fugue.json'
    data = W.build_score(out, meta, voices, bars, entries=ENTRIES, subject=S1, dynamics=dynamics)
    soften_echoes(out)
    return data


if __name__ == '__main__':
    end = max((s + dur16(t)) for v in VO.values() for s, t in v)
    nb = int(sys.argv[1]) if len(sys.argv) > 1 else int(-(-end // 16))
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    build(nb, out)
    print('bars', nb)
