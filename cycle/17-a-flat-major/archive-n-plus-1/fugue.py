#!/usr/bin/env python3
"""Fugue XVII in A-flat major, eighteen voices: "Fuga, fuggendo la cadenza" (third edition).

Zarlino called an evaded cadence "fuggir la cadenza", to flee the cadence.  This fugue flees its own:
the subject is a cheerful 12/8 tune that ends on the most expected cadence there is (re held, then do),
and every time the music prepares a perfect cadence it is evaded, and a new voice enters.  Seventeen
evasions admit seventeen voices.  Nine of them form a running gag: deceptive cadences in a row, each
dropping the tonic a third (A-flat, f, D-flat, b-flat, G-flat, e-flat, C-flat, a-flat, F-flat = E,
c-sharp = d-flat), round the flat side of the key circle and back home in the minor, then into E major
and back through D-flat minor.  The last evasion is a dominant seventh left hanging in silence: the old
anecdote (told of Bach and of others) of the children who could get their father out of bed by playing
an unresolved chord.  The eighteenth voice, the father, enters with the subject in augmentation and
supplies the bass 5-1 that the children's tune never had: the first perfect cadence of the piece.

Guest: the subject of Bach's A-flat fugue BWV 862 (WTC I), at its own note values (eighths), enters
once at an evaded cadence ("a familiar cadence turns out to be the entrance of a different subject").

Every note is written here by hand as a literal token string.  Thematic statements are explicit
transforms (realisation of the hand-written subject's scale degrees in a key, octave transposition,
diatonic inversion, augmentation) of the hand-written subject.  Scratch tools only checked material.
"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (12, 8)
BAR = 24                                  # sixteenths per bar; a beat (dotted quarter) is 6
# Voice order: left choir (high to low), right choir (high to low), the father in the centre.
# (render_spatial --layout antiphonal-centre puts the first nine left, the next eight right, the last
# in front.)  Entries alternate left/right.
VOICES = [
    # abbr,  name,                    clef,       base velocity
    ('LS1', 'Left Soprano I',        'treble',   66),
    ('LS2', 'Left Soprano II',       'treble',   62),
    ('LS3', 'Left Soprano III',      'treble',   62),
    ('LA1', 'Left Alto I',           'treble',   62),
    ('LA2', 'Left Alto II',          'treble',   62),
    ('LT1', 'Left Tenor I',          'treble_8', 64),
    ('LT2', 'Left Tenor II',         'treble_8', 62),
    ('LBr1', 'Left Baritone I',      'bass',     62),
    ('LBr2', 'Left Baritone II',     'bass',     62),
    ('RS', 'Right Soprano',          'treble',   66),
    ('RA1', 'Right Alto I',          'treble',   64),
    ('RA2', 'Right Alto II',         'treble',   62),
    ('RT1', 'Right Tenor I',         'treble_8', 62),
    ('RT2', 'Right Tenor II',        'treble_8', 62),
    ('RBr', 'Right Baritone',        'bass',     62),
    ('RB1', 'Right Bass I',          'bass',     66),
    ('RB2', 'Right Bass II',         'bass',     64),
    ('P', 'The Father (Bass)',       'bass',     74),
]
NAMES = [v[0] for v in VOICES]
LONG = {v[0]: v[1] for v in VOICES}

# ---------------------------------------------------------------- the subject (hand-written)
# As scale degrees (0 = do, 7 = the octave above, -1 = ti below) with durations in sixteenths.
# do. DO' ti la sol fa mi fa | re mi fa sol la | sol. fa mi | re.  (-> do: the cadence it never gets)
SUBJ_DEG = [(0, 6), (7, 4), (6, 2), (5, 2), (4, 2), (3, 2), (2, 4), (3, 2),
            (1, 4), (2, 2), (3, 2), (4, 2), (5, 2), (4, 3), (3, 1), (2, 2), (1, 6)]
MAJOR = [0, 2, 4, 5, 7, 9, 11]
MINOR = [0, 2, 3, 5, 7, 8, 10]            # natural minor: the subject never needs the leading tone
NAT = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
LET = 'CDEFGAB'


def realize(degs, tonic, mode='major', octave=4, raise7=()):
    """Write scale degrees in a key.  tonic like 'Ab', 'F#'; octave of the tonic (do = 0)."""
    L = tonic[0]
    alt = tonic.count('#') - tonic.count('b')
    t = 12 * (octave + 1) + NAT[L] + alt
    sc = MAJOR if mode == 'major' else MINOR
    out = []
    for k, (d, u) in enumerate(degs):
        if d is None:
            out.append(f'R:{u}')
            continue
        p = t + 12 * (d // 7) + sc[d % 7] + (1 if (k in raise7 and d % 7 == 6) else 0)
        letter = LET[(LET.index(L) + d) % 7]
        out.append(f'{W.name_of(p, letter)}:{u}')
    return ' '.join(out)


def subj(tonic, mode='major', octave=4, aug=1, inv=False, upto=None, shift=0):
    """The subject in a key; shift = diatonic (modal) transposition by scale steps within that key."""
    degs = [((-d if inv else d) + shift, Fr(u) * aug) for d, u in SUBJ_DEG]
    if upto is not None:
        degs = degs[:upto]
    return realize(degs, tonic, mode, octave)


def oc(s, n):
    return W.transpose(s, 12 * n, 7 * n)


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


# J. S. Bach, Fugue in A-flat major BWV 862 (WTC I): the subject as first stated (tenor, from beat 2),
# Ab3 Eb4 C4 Ab3 F4 Db4 Eb4, in eighths with the last note longer (checked against the Mutopia MIDI).
BWV862 = 'Ab3:2 Eb4:2 C4:2 Ab3:2 F4:2 Db4:2 Eb4:4'

# ---------------------------------------------------------------- placement
VO = {n: [] for n in NAMES}
ENTRIES = []


def pos(bar, off=0):
    """bar is 1-based; off in sixteenths from the barline (a beat is 6)."""
    return Fr(bar - 1) * BAR + Fr(off)


def put(v, bar, off, toks):
    VO[v].append((pos(bar, off), toks))


def theme(v, bar, off, toks, label, nbars=None):
    put(v, bar, off, toks)
    n = nbars if nbars is not None else max(1, round(float(dur16(toks)) / BAR))
    ENTRIES.append((LONG[v], bar, Fr(off) / 4, label, n))


def line(v, bar, off, *chunks):
    """Place consecutive hand-written chunks (strings) one after another."""
    put(v, bar, off, ' '.join(chunks))


def assemble(v, nbars):
    segs = sorted(VO[v], key=lambda x: x[0])
    out, cur = [], Fr(0)
    for s, toks in segs:
        if s < cur:
            raise ValueError(f'{v}: overlap at bar {float(s / BAR + 1):.3f}: {toks[:60]}')
        if s > cur:
            out.append(f'R:{s - cur}')
        out.append(toks)
        cur = s + dur16(toks)
    total = Fr(nbars * BAR)
    if cur > total:
        raise ValueError(f'{v}: runs past the end ({float(cur / BAR)} > {nbars})')
    if cur < total:
        out.append(f'R:{total - cur}')
    return W.concat_bars(' '.join(out), METER)


# =====================================================================================================
# SECTIONS are defined below as functions of their starting bar; the summit was composed first.
# =====================================================================================================

# ---------------------------------------------------------------- companions (hand-written, as degrees)
# Countersubject: enters on beat 2 of the subject (after the previous entrant's landing note) and rises
# while the subject falls, then falls while it rises: do re mi | fa re ti(below) sol(below).
CS_DEG = [(0, 6), (1, 6), (2, 6), (3, 6), (1, 6), (-1, 6), (-3, 6)]
# Module bass under a subject entry: do (held) fa sol | re sol (held) sol(octave lower).
BASS_DEG = [(0, 12), (3, 6), (4, 6), (1, 6), (4, 12), (-3, 6)]


def cs(tonic, mode='major', octave=3):
    """Countersubject in a key; in minor the ti (index 5) is the raised leading tone."""
    return realize(CS_DEG, tonic, mode, octave, raise7=(5,) if mode == 'minor' else ())


def bassline(tonic, mode='major', octave=2):
    return realize(BASS_DEG, tonic, mode, octave, raise7=())


def lit(s):
    return ' '.join(s.replace('|', ' ').split())


# =====================================================================================================
# I. EXPOSITION (bars 1-10).  Tenor, alto, soprano, bass; each answer enters on the previous voice's
# landing note ("do"), which it gently re-hears (A-flat as the subdominant of E-flat, and back).
# =====================================================================================================
def exposition():
    CSAb = cs('Ab', octave=3)
    CSEb = cs('Eb', octave=3)
    theme('LT1', 1, 0, subj('Ab', octave=3), 'subject (tenor)', 2)
    put('LT1', 3, 0, lit('Ab3:6 ' + CSEb + ' | Bb3:6 ' + CSAb + ' | G3:4 Bb3:2 Db4:6 C4:6 Bb3:6 | Ab3:12 F3:12 |'
                         ' Bb3:6 C4:6 Db4:12 | Db4:6 Ab3:6 Bb3:12'))
    theme('RA1', 3, 0, subj('Eb', octave=4), 'answer (alto), evasion 1: the landing A-flat re-heard as IV of E-flat', 2)
    put('RA1', 5, 0, lit('Eb4:6 C4:6 F4:4 Eb4:2 Eb4:6 | F4:6 Db4:4 C4:2 Bb3:6 Eb4:6 | Bb3:6 ' + oc(CSEb, 1) +
                         ' | G4:6 Ab4:18 | F4:6 Eb4:6 Db4:12'))
    theme('LS1', 5, 0, subj('Ab', octave=4), 'subject (soprano), evasion 2', 2)
    put('LS1', 7, 0, lit('Ab4:2 G4:4 Bb4:6 Eb5:6 Bb4:4 Ab4:2 | C5:6 D5:6 F5:4 Eb5:2 D5:6 | Eb5:6 C5:6 F5:4 Eb5:2 Db5:6 |'
                         ' Db5:6 C5:6 Bb4:12'))
    theme('RB1', 7, 0, subj('Eb', octave=2), 'answer (bass), evasion 3', 2)
    put('RB1', 9, 0, lit('Eb2:6 Ab2:6 Db3:6 Bb2:6 | Db3:6 Eb3:12 Eb2:6'))


exposition()


# =====================================================================================================
# II. THE RUNNING GAG (bars 11-30).  Nine deceptive cadences in a row, each dropping the tonic a third:
# A-flat -> f -> D-flat -> b-flat -> G-flat -> e-flat -> C-flat -> a-flat -> F-flat (= E) -> c-sharp.
# Every subject lands on "do" over the submediant, and a new voice enters on that chord's root.
# =====================================================================================================
CHAIN = [  # bar, key, mode, entering voice, octave, CS voice, CS octave, bass voice (or None), bass octave
    (11, 'F', 'minor', 'LA2', 4, 'LT1', 3, 'RB1', 2),
    (13, 'Db', 'major', 'RS', 5, 'LA2', 4, 'RB1', 2),
    (15, 'Bb', 'minor', 'LT2', 3, 'RS', 4, 'RB1', 1),
    (17, 'Gb', 'major', 'RBr', 2, 'LA2', 4, None, 0),
    (19, 'Eb', 'minor', 'LA1', 4, 'RBr', 3, 'RB1', 2),
    (21, 'Cb', 'major', 'RB2', 3, 'LA1', 4, None, 0),
    (23, 'Ab', 'minor', 'LS2', 4, 'RB2', 2, None, 0),
    (25, 'E', 'major', 'RT1', 3, 'LS2', 5, 'RB1', 2),
    (29, 'C#', 'minor', 'LBr2', 3, 'RT1', 4, None, 0),
]
NAMEKEY = {'F': 'F minor', 'Db': 'D-flat major', 'Bb': 'B-flat minor', 'Gb': 'G-flat major', 'Eb': 'E-flat minor',
           'Cb': 'C-flat major', 'Ab': 'A-flat minor', 'E': 'E major (= F-flat)', 'C#': 'C-sharp minor (= D-flat minor)'}


def chain_skeleton():
    for k, (bar, key, mode, v, o, csv, cso, bv, bo) in enumerate(CHAIN):
        theme(v, bar, 0, subj(key, mode, octave=o), f'evaded cadence {k + 4}: subject in {NAMEKEY[key]}', 2)
        if k:
            pk, pm, pv, po = CHAIN[k - 1][1], CHAIN[k - 1][2], CHAIN[k - 1][3], CHAIN[k - 1][4]
            put(pv, bar, 0, realize([(0, 6)], pk, pm, po))          # the landing "do", on the wrong chord
        c = cs(key, mode, octave=cso)
        if bv is None and k != 6:                                  # subject in the bass: end on re, not sol
            c = ' '.join(c.split()[:-1] + [realize([(1, 6)], key, mode, cso)])
        put(csv, bar, 6, c)
        if bv:
            b = bassline(key, mode, octave=bo)
            if bo == 1:                                            # keep the low "sol" an octave up
                t = b.split(); b = ' '.join(t[:-2] + [t[-2].split(':')[0] + ':18'])
            put(bv, bar, 0, b)


chain_skeleton()


def chain_free():
    """Free counterpoint around the chain (written by hand, module by module)."""
    # E4, F minor (bars 11-12): the first real joke - the full cadence prepared since bar 9 lands on f.
    put('LS1', 11, 0, 'Ab4:6 R:18')
    put('RA1', 11, 0, lit('C4:12 Db4:6 C4:6 | Db4:6 C4:6 Bb3:6 C4:6'))
    # E5, D-flat major (bars 13-14)
    put('LS1', 13, 0, lit('Ab4:18 Bb4:6~ | Bb4:6 C5:6 Eb5:4 Db5:2 C5:6'))
    put('LT1', 13, 0, lit('F3:12 Gb3:6 Eb3:6 | Eb3:6 Eb3:6 F3:6 C3:6'))
    # E6, B-flat minor (bars 15-16)
    put('LS1', 15, 0, lit('F5:12 Gb5:6 F5:6~ | F5:12 Eb5:6 C5:6'))
    put('LT1', 15, 0, lit('Db3:12 Eb3:6 C3:6~ | C3:6 A2:6 C3:12'))
    # E7, G-flat major (bars 17-18): the subject in the bass
    put('LS1', 17, 0, lit('Db5:12 Gb5:6 Db5:6 | Eb5:12 F5:8 Eb5:4'))
    # E8, E-flat minor (bars 19-20)
    put('LS1', 19, 0, lit('Gb5:12 Eb5:12 | F5:18 D5:6'))
    put('LT2', 19, 0, lit('Bb3:12 Cb4:6 Bb3:6 | Bb3:12 Ab3:6 F3:6'))
    # E9, C-flat major (bars 21-22): the subject in the bass again
    put('LS1', 21, 0, lit('Eb5:12 Fb5:6 Gb5:6 | Fb5:6 Eb5:8 Db5:10'))
    put('LT2', 21, 0, lit('Gb3:12 R:12 | Ab3:6 Bb3:6 Db4:12'))
    # E10, A-flat minor (bars 23-24): home - but in the minor, and pianissimo.  Three voices only.
    put('LA1', 23, 0, lit('Eb4:12 Fb4:6 Eb4:6 | Db4:6 Fb4:6 Db4:12'))
    # E11, E major (= F-flat, bars 25-28): the farthest key, and the softest.  After the entry, the dream:
    # the tune's first bar in augmentation, floating over an imperfect (first-inversion) landing.
    put('LA1', 25, 0, lit('B3:6 G#4:6 A4:6 E5:6~ | E5:2 C#5:4 B4:12 A4:6 | G#4:12 B4:8 A4:4 | G#4:6 C#4:6 E4:6 F#4:6'))
    theme('LS2', 27, 0, realize([(d, 2 * u) for d, u in SUBJ_DEG[:8]], 'E', 'major', 4),
          'the dream: the first bar of the subject in augmentation (E major)', 2)
    put('RB1', 27, 0, lit('G#2:12 E2:6 B2:6 | C#3:6 A2:6 B2:12'))
    put('RT1', 27, 0, lit('E3:12 G#3:6 F#3:6 | E3:6 C#3:6 D#3:12'))


chain_free()


def turn_home():
    """E12 (c-sharp minor, bars 29-30) and the turn home (bars 31-32): c-sharp = d-flat, the subdominant
    minor of A-flat; the dominant arrives - and the cadence it prepares is dodged once more, in passing."""
    # E12 free voices (sharps), then d-flat minor (flats) from bar 31.
    put('LS2', 29, 0, lit('G#4:12 F#4:6 G#4:6 | A4:6 G#4:4 F#4:2 G#4:6 B#4:6 |'
                          ' Db5:12 Fb5:6 Db5:6 | C5:6 Db5:12 Eb5:6'))
    put('LA1', 29, 0, lit('E4:12 B3:12 | C#4:6 B3:6 D#4:6 F#4:6 | Fb4:12 Ab4:6 G4:6 | Ab4:6 F4:6 Ab4:6 G4:6'))
    put('LBr2', 31, 0, lit('Db3:6 Fb3:6 Db3:6 Eb3:6 | F3:6 Db3:6 Bb2:6 Eb3:6'))
    put('RT1', 31, 6, lit('Ab3:6 Bb3:12 | Ab3:12 Bb3:12'))
    put('LS1', 32, 6, lit('Ab5:6 Db6:6 Bb5:6'))


turn_home()


# =====================================================================================================
# III. THE FRENZY AT HOME (bars 33-42).  Back in A-flat, and every cadence is still dodged, each in a
# new way (vi7, flat VI, V7 of IV, the minor tonic); the remaining children crowd in.
# =====================================================================================================
def frenzy():
    # E13 (bars 33-34): V -> vi7.  The newcomer is a guest: the subject of Bach's own A-flat fugue
    # (BWV 862), at its own pitch and note values; its eighths fall naturally into 12/8, and it runs
    # straight on into the second bar of our subject, so the guest finishes our sentence (and is denied
    # our cadence like everyone else).
    theme('RA2', 33, 0, BWV862 + ' Db4:2 C4:4 Db4:2', 'evaded cadence 13 (V - vi7): guest, the subject of BWV 862 (WTC I), at pitch', 1)
    put('RA2', 34, 0, ' '.join(subj('Ab', octave=3).split()[8:]))
    put('LA1', 33, 0, lit('Ab4:14 Bb4:4 C5:6 | Db5:6 Bb4:6 G4:6 Eb4:6'))       # countersubject (do re mi | fa re ti sol)
    put('RB1', 33, 0, lit('F2:12 Eb2:6 C3:6~ | C3:2 Bb2:10 Eb2:12'))
    put('LS1', 33, 0, lit('Ab5:15 G5:3 Ab5:6~ | Ab5:8 G5:6 Bb5:4 Ab5:3 G5:3'))
    put('LS2', 33, 0, lit('F5:14 Eb5:10 | F5:9 Eb5:11 Db5:4'))
    put('RT1', 33, 0, lit('F3:12 G3:8 Ab3:4~ | Ab3:6 Bb3:12 G3:6'))
    put('LBr2', 33, 0, lit('C3:6 Db3:6 Bb2:6 Eb3:6~ | Eb3:2 Db3:10 Bb2:12'))
    # E14 (bars 35-36): V -> flat VI.  Left Soprano III enters; the countersubject returns to its first
    # singer (Left Tenor I).
    put('RA2', 35, 0, 'Ab3:6')
    theme('LS3', 35, 0, subj('Ab', octave=4), 'evaded cadence 14 (V - flat VI): subject', 2)
    put('LT1', 35, 6, lit('Ab3:6 Bb3:6 C4:6 | Db4:6 Bb3:6 G3:6 Eb3:6'))
    put('RB1', 35, 0, lit('Fb2:12 Db3:6 Ab2:6 | Bb2:12 Eb2:12'))
    put('LS1', 35, 0, lit('Ab5:6 R:18 | R:6 Bb5:8 Ab5:4 G5:6'))
    put('LS2', 35, 0, lit('Cb5:12 Bb4:6 Eb5:6'))
    put('LA1', 35, 6, lit('Fb4:6 F4:6 Ab4:6~ | Ab4:6 G4:6 Eb4:6 Db4:6'))
    put('LBr2', 35, 6, lit('Db3:6 F3:6 Eb3:6 | Db3:6 Eb3:6 Bb2:12'))
    put('RA1', 36, 0, lit('F4:6 Eb4:6 Db4:6 Bb3:6'))
    # E15 (bars 37-38): V -> V4/2 of IV: the bass slips up to G-flat instead of A-flat.  Right Tenor II
    # enters; Left Alto II, the first of the deceived, sings the countersubject.
    put('LS3', 37, 0, 'Ab4:6')
    theme('RT2', 37, 0, subj('Ab', octave=3), 'evaded cadence 15 (V - V4/2 of IV): subject', 2)
    put('LA2', 37, 10, lit('Ab4:2 Bb4:6 C5:6 | Db5:6 Bb4:6 G4:6 Eb4:6'))
    put('RB2', 37, 0, lit('Gb2:6 F2:6 Db3:6 Ab2:6 | Bb2:12 Eb2:12'))
    put('LS1', 37, 0, lit('Ab5:14 Bb5:4 Ab5:6~ | Ab5:4 G5:2 Eb5:6 Db5:12'))
    put('LA1', 37, 0, lit('C4:6 Db4:12 Eb4:6~ | Eb4:2 F4:4 G4:6 Bb4:12'))
    put('LBr2', 37, 6, lit('Db3:6 F3:6 Eb3:6 | Db3:6 Eb3:6 Bb2:12'))
    put('LT1', 37, 0, lit('Eb3:6 F3:6 Bb3:8 Ab3:4 | F3:6 Bb3:12 G3:6'))
    put('RS', 38, 6, lit('Bb5:12 Ab5:3 G5:3'))
    # E16 (bars 39-40): V -> i.  At last the bass reaches A-flat - but the chord is minor.  Left Baritone I
    # enters with the subject in the bass, in A-flat minor; Right Alto I has the countersubject.
    put('RT2', 39, 0, 'Ab3:6')
    theme('LBr1', 39, 0, subj('Ab', 'minor', octave=2), 'evaded cadence 16 (V - i): subject in A-flat minor (bass)', 2)
    put('RA1', 39, 6, cs('Ab', 'minor', octave=4))
    put('LS1', 39, 0, lit('Cb5:12 Db5:6 Eb5:6 | Fb5:6 Db5:18'))
    put('RS', 39, 0, 'Ab5:6')
    put('LA1', 39, 0, lit('Bb4:2 Ab4:4 Cb4:6 Fb4:6 Eb4:6 | Db4:6 Fb4:8 Eb4:4 Bb4:6~'))
    put('LA2', 39, 0, lit('Eb4:12 Ab3:12~ | Ab3:14 G3:10'))
    put('LT1', 39, 0, 'Eb3:6')

def climax():
    # Bars 41-43: all seventeen children at once.  Left Soprano II has the subject; Left Tenor I the
    # countersubject; heads of the subject crowd in everywhere; the cadence is prepared with everything
    # they have - and at its dominant seventh they stop dead.  The chord hangs; then silence.
    theme('LS2', 41, 0, subj('Ab', octave=4) + '~', 'stretto of all the children: subject', 2)
    put('LS2', 43, 0, 'Bb4:18')
    put('LT1', 41, 6, lit(cs('Ab', octave=3) + '~ Eb3:18'))
    put('LBr1', 41, 0, lit('Ab2:6 Eb3:6 F3:12 | Db3:6'))
    put('RB1', 41, 6, lit('Ab2:6 Db3:6 F2:6 | Bb2:6 Eb2:18~ | Eb2:18'))
    put('LS1', 41, 0, lit('C5:6 R:18 | F5:6 Bb5:6 Ab5:3 G5:3 Bb5:6~ | Bb5:18'))
    put('LA1', 41, 0, lit('Bb4:2 Ab4:12 F4:10 | F4:8 Eb4:16~ | Eb4:18'))
    put('LA2', 41, 0, lit('Ab3:6 C4:6 Db4:6 Ab3:6~ | Ab3:6 G3:6 Eb4:10 Bb3:2~ | Bb3:18'))
    theme('RT1', 41, 18, ' '.join(subj('Ab', octave=3, shift=-5).split()[:5]), 'stretto: head (on the mediant)', 1)
    put('LS3', 42, 6, lit('Bb4:12 Eb5:6~ | Eb5:18'))
    put('LBr2', 41, 18, 'C3:6')
    put('RB2', 42, 6, lit('Bb2:18~ | Bb2:18'))
    theme('RA1', 41, 4, ' '.join(subj('Ab', octave=4, shift=-3).split()[:7]), 'stretto: head (on the dominant)', 1)
    put('RA1', 42, 2, lit('Ab4:4 Bb4:18~ | Bb4:18'))
    theme('RT2', 42, 6, ' '.join(subj('Ab', octave=3, shift=-3).split()[:6]) + ' G3:18', 'stretto: head (on the dominant)', 1)
    theme('RS', 41, 6, ' '.join(subj('Ab', octave=5, shift=-5).split()[:7]), 'stretto: head (on the mediant)', 1)
    put('RS', 42, 4, lit('Db5:2 Bb5:6 Db6:12~ | Db6:18'))


# =====================================================================================================
# IV. THE SUMMIT (bars 44-49), composed first.  After the silence the eighteenth voice, the father, enters
# alone on low A-flat - and the children's hanging seventh (Right Soprano's D-flat) falls to C at once.
# He sings the subject in augmentation; the children re-enter around him with the subject (Right Alto I),
# the subject on the subdominant level (Left Soprano II), a cascade of heads (some inverted), and finally
# the subject at the top (Left Soprano I) against its own inversion (Left Alto I), converging on the
# tonic as the father adds the bass 5-1 the tune never had: the first perfect cadence of the piece.
# =====================================================================================================
SUMMIT = 44
SUM = {   # hand-written lines, six bars each from bar 44 (thematic statements entered in summit())
    'RS': 'C6:16 Bb5:2 Db6:6~ | Db6:4 C6:8 Db6:4 C6:2 Bb5:6 | Eb6:8 Db6:4 Eb6:6 Db6:4 C6:2 |'
          ' R:6 Eb6:6 Db6:4 C6:2 Bb5:2 Ab5:4~ | Ab5:12 G5:6 Eb5:6 | Eb5:24',
    'RB2': 'R:6 Eb3:12 Db3:6~ | Db3:6 Eb3:6 Bb2:12 | C3:4 Eb3:4 F3:4 Eb3:12 | F3:4 Eb3:4 C3:4 Eb3:6 Bb2:2 C3:4 |'
           ' Db3:12 Bb2:12 | Eb3:24',
    'LA1': 'R:14 C4:4 F4:6~ | F4:6 Eb4:8 Db4:4 Bb3:6~ | Bb3:2 Ab3:4 R:18',
    'RA1': 'Ab4:4 Eb5:8~ | Eb5:2 Db5:6 C5:4 R:12 | F5:14 Eb5:2 Db5:8 | C5:24',
    'LS2': 'G5:8 Ab5:4 | R:8 Ab4:4 Bb4:12 | Bb4:24 | C5:24',
    'LA2': 'R:14 | R:20 Ab4:4 | F4:16 Eb4:8 | Eb4:24',
    'LS3': 'C5:2 Bb4:4 C5:2 | F5:16 Eb5:4 R:4 | R:6 Db5:6 R:12 | C5:24',
    'RT1': 'F4:2 | Db4:6 C4:6 G3:6 Ab3:6 | Bb3:14 Eb4:10 | Eb4:24',
    'LBr1': 'Eb3:4 Ab3:4 R:12 | F3:12 R:12 | C3:24',
    'RA2': 'R:2 | R:2 Eb5:6 Eb4:4 F4:2 G4:2 Ab4:2 R:6 | R:2 C5:6 C4:4 Db4:2 Eb4:2 F4:2 G4:2 Ab4:4 | R:24 | Ab4:24',
    'RT2': 'R:24 | R:10 C4:4 Bb3:2 Ab3:2 G3:2 F3:2 G3:2~ | G3:1 Ab3:1 Bb3:2 C4:6 R:14 |'
           ' R:12 Bb3:4 C4:2 Db4:2 Eb4:2 F4:2 | Eb4:3 Db4:1 C4:2 Bb3:6 R:12 | Eb4:24',
    'LBr2': 'R:24 | R:24 | R:8 G3:4 Ab3:2 Bb3:2 C4:2 Db4:2 C4:3 Bb3:1 | Ab3:2 G3:6 R:16 | R:24 | Ab3:24',
    'RBr': 'R:20 | R:12 Eb4:4 Db4:2 C4:2 Bb3:2 Ab3:2 | Bb3:3 C4:1 Db4:2 Eb4:6 R:12 | R:24 | Eb3:24',
    'RB1': 'R:24 | R:24 | R:24 | R:24 | F2:12 R:12 | Ab2:24',
    'LT2': 'C4:4 R:16 | Db4:12 R:12 | C4:24',
}


def summit():
    S = SUMMIT
    H = lambda inv, sh, o, n=7: ' '.join(subj('Ab', octave=o, inv=inv, shift=sh).split()[:n])
    theme('P', S, 0, 'Ab1:12~ ' + subj('Ab', octave=1, aug=2, upto=16) + ' Bb1:12 Eb2:12 Ab1:24~',
          'after evasion 17 (the hanging seventh): the father, the subject in augmentation, with the bass 5-1 it never had', 6)
    put('RS', S, 0, lit(SUM['RS']))
    put('RB2', S, 0, lit(SUM['RB2']))
    put('LA1', S, 0, lit(SUM['LA1']))
    theme('LA1', S + 3, 0, subj('Ab', octave=4, inv=True), 'summit: the subject inverted (mirror of Left Soprano I)', 2)
    put('LA1', S + 5, 0, 'Ab4:24')
    theme('RA1', S, 12, subj('Ab', octave=4), 'summit: subject', 2)
    put('RA1', S + 2, 12, lit(SUM['RA1']))
    theme('LS2', S, 18, ' '.join(subj('Ab', octave=4, shift=5).split()[:-1]), 'summit: subject on the subdominant level', 2)
    put('LS2', S + 2, 12, lit(SUM['LS2']))
    put('RBr', S, 12, H(False, -5, 3, 5))
    put('RBr', S + 1, 4, lit(SUM['RBr']))
    put('RA2', S + 1, 6, H(False, 0, 3, 5))
    put('RA2', S + 1, 22, lit(SUM['RA2']))
    put('LT1', S + 1, 8, H(False, -6, 4, 5))
    put('LT1', S + 4, 14, H(True, 0, 4, 5) + ' C4:18')
    theme('LA2', S + 1, 12, H(False, -2, 4), 'summit: head cascade', 1)
    put('LA2', S + 1, 34, lit(SUM['LA2']))
    theme('LS3', S + 1, 18, H(False, -6, 5), 'summit: head cascade', 1)
    put('LS3', S + 2, 16, lit(SUM['LS3']))
    put('RT2', S, 0, lit(SUM['RT2']))
    theme('RT1', S + 2, 0, H(True, 0, 4) + '~', 'summit: head cascade (inverted)', 1)
    put('RT1', S + 2, 22, lit(SUM['RT1']))
    theme('LBr1', S + 2, 6, H(False, -5, 3) + '~', 'summit: head cascade', 1)
    put('LBr1', S + 3, 4, lit(SUM['LBr1']))
    put('LBr2', S, 0, lit(SUM['LBr2']))
    put('RB1', S, 0, lit(SUM['RB1']))
    put('LT2', S + 2, 12, H(False, 0, 3, 5))
    put('LT2', S + 3, 4, lit(SUM['LT2']))
    theme('LS1', S + 3, 0, subj('Ab', octave=5), 'summit: subject at the top', 2)
    put('LS1', S + 5, 0, 'Ab5:24')



# =====================================================================================================
# V. CODA (bars 50-52).  Over the father's held A-flat the first child (Left Tenor I) sings the head once
# more, softly, at the pitch where the fugue began; the first answerer and the eldest soprano close above
# it; then the family gathers on one quiet chord.
# =====================================================================================================
def coda():
    put('P', 50, 0, lit('Ab1:24~ | Ab1:24~ | Ab1:24'))
    theme('LT1', 50, 0, ' '.join(subj('Ab', octave=3).split()[:8]), 'coda: the head, where it began', 1)
    put('LT1', 51, 0, lit('C4:24~ | C4:24'))
    put('RA1', 50, 0, lit('C5:12 Db5:8 C5:4 | C5:6 Bb4:6 Ab4:12~ | Ab4:24'))
    put('LS1', 50, 0, lit('Ab5:14 F5:4 Eb5:6 | Eb5:6 Db5:6 C5:12~ | C5:24'))
    put('LBr2', 50, 0, lit('Eb3:12 F3:6 Ab3:6 | Ab3:6 G3:6 Ab3:12~ | Ab3:24'))
    for v, n in (('RS', 'Eb5'), ('LA1', 'Eb4'), ('RB2', 'Eb2'), ('LS3', 'Ab4'), ('RT2', 'Eb3'), ('LA2', 'C4')):
        put(v, 52, 0, n + ':24')

frenzy()
climax()
summit()
coda()


NB = 52


def q(bar, beat=1):
    """Quarter-note time of a bar and dotted-quarter beat (1-4) in 12/8."""
    return (bar - 1) * 6 + (beat - 1) * Fr(3, 2)


# A gentle gigue: dotted quarter about 56.  The far keys and the dream are slower; the crowding at home is
# a little quicker; the cadence that the children prepare broadens into the hanging chord, which is held
# and then followed by a long silence (the rest is short on paper and very slow in time); the father's
# summit is broad; the coda slows to the end.
TEMPO = {'tempo_map': [[0, 84], [float(q(23)), 81], [float(q(25)), 75], [float(q(29)), 78],
                       [float(q(31)), 84, 'ramp'], [float(q(33)), 87], [float(q(42, 2)), 87],
                       [float(q(43)), 68, 'ramp'], [float(q(43, 3)), 50, 'ramp'], [float(q(43, 4)), 30],
                       [float(q(44)), 80], [float(q(48, 3)), 80], [float(q(49, 4)), 64, 'ramp'],
                       [float(q(50)), 72], [float(q(51)), 68], [float(q(52)), 48, 'ramp']]}
DYN = {1: -4, 11: -2, 19: -4, 23: -12, 25: -12, 27: -10, 29: -8, 31: -4, 33: 0, 35: 1, 37: 2, 39: 3,
       41: 6, 42: 9, 43: 10, 44: 2, 45: 4, 46: 6, 47: 8, 49: 9, 50: -8, 52: -10}


def accents(path):
    """12/8 metric accents on the written velocities (beats 1 and 3 strong, 2 and 4 medium)."""
    import json
    d = json.loads(Path(path).read_text())
    for v in d['voices']:
        for e in v['events']:
            pos = Fr(e['t']).limit_denominator(48) % 6
            add = 4 if pos == 0 else 2 if pos == 3 else 1 if pos in (Fr(3, 2), Fr(9, 2)) else 0
            if e['d'] < 0.5:
                add -= 2
            e['v'] = max(24, min(118, int(e['v']) + add))
    Path(path).write_text(json.dumps(d, ensure_ascii=False, indent=None, separators=(',', ':')))


def build(path=None):
    path = path or HERE / 'fugue.json'
    bars = {LONG[n]: assemble(n, NB) for n in NAMES}
    meta = {'title': 'The Well-Tempered clAIvier',
            'subtitle': 'Fugue XVII in A-flat major, eighteen voices: Fuga, fuggendo la cadenza',
            'composer': 'Claude / Sam (guest subject: J. S. Bach, Fugue in A-flat major BWV 862)',
            'instrument': 'Two choirs (nine and eight voices) and the father (open score, eighteen keyboards)',
            'key': 'Ab', 'mode': 'major', 'meter': list(METER), 'bpm': 84,
            'tempo_text': 'Allegretto giocoso, alla giga (dotted quarter = 56)', 'movement_number': 17,
            'piece_type': 'fugue', 'edition': 'third',
            'motto': 'Fuggir la cadenza (Zarlino)',
            'score_layout': {'paper': 'a2', 'staff_size': 19, 'staff_distance': 9, 'hide_empty_staves': True},
            'markers': [{'t': float(q(1)), 'label': 'Exposition (four children)'},
                        {'t': float(q(11)), 'label': 'The running gag: deceptive cadences falling by thirds'},
                        {'t': float(q(23)), 'label': 'Home, but minor (pianissimo)'},
                        {'t': float(q(25)), 'label': 'E major, the farthest key; the dream'},
                        {'t': float(q(31)), 'label': 'The turn home'},
                        {'t': float(q(33)), 'label': 'Dodging at home; the guest (BWV 862)'},
                        {'t': float(q(41)), 'label': 'All the children: stretto and the cadence'},
                        {'t': float(q(43)), 'label': 'The hanging seventh; silence'},
                        {'t': float(q(44)), 'label': 'Summit: the father'},
                        {'t': float(q(50)), 'label': 'Coda'}]}
    meta.update(TEMPO)
    voices = [(LONG[n], n, clef, vel) for n, _, clef, vel in VOICES]

    def dynamics(b):
        v = 0
        for k in sorted(DYN):
            if b + 1 >= k:
                v = DYN[k]
        return v
    r = W.build_score(path, meta, voices, bars, entries=ENTRIES, subject=subj('Ab', octave=3),
                      dynamics=dynamics, accents=False)
    accents(path)
    return r


if __name__ == '__main__':
    build(Path(sys.argv[1]) if len(sys.argv) > 1 else None)
    print('bars', NB)
