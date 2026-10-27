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
    theme('RA1', 3, 0, subj('Eb', octave=4), 'answer (alto)', 2)
    put('RA1', 5, 0, lit('Eb4:6 C4:6 F4:4 Eb4:2 Eb4:6 | F4:6 Db4:4 C4:2 Bb3:6 Eb4:6 | Bb3:6 ' + oc(CSEb, 1) +
                         ' | G4:6 Ab4:18 | F4:6 Eb4:6 Db4:12'))
    theme('LS1', 5, 0, subj('Ab', octave=4), 'subject (soprano)', 2)
    put('LS1', 7, 0, lit('Ab4:2 G4:4 Bb4:6 Eb5:6 Bb4:4 Ab4:2 | C5:6 D5:6 F5:4 Eb5:2 D5:6 | Eb5:6 C5:6 F5:4 Eb5:2 Db5:6 |'
                         ' Db5:6 C5:6 Bb4:12'))
    theme('RB1', 7, 0, subj('Eb', octave=2), 'answer (bass)', 2)
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
        theme(v, bar, 0, subj(key, mode, octave=o), f'deceptive cadence {k + 1}: subject in {NAMEKEY[key]}', 2)
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
