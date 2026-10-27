#!/usr/bin/env python3
"""Fugue VII in E-flat major a 8: Fuga a due cori.

Two four-voice choirs, Coro I (left) and Coro II (right), in the manner of the
Venetian cori spezzati and of Bach's double-choir motet "Singet dem Herrn"
BWV 225.  Every note is written below as literal bar strings (sixteenth units).
The only operations applied to written material are explicit, named
transformations from tools/wtclib.py (`transpose`, `invert_diatonic`,
`scale_rhythm`) and the region-aware mirror `mirror()` defined here from them.
Their output is what the score holds.

Run:  python3 cycle/07-e-flat-major/fugue.py   -> cycle/07-e-flat-major/fugue.json
"""
import json
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
from wtclib import (build_score, concat_bars, transpose, scale_rhythm,  # noqa: E402
                    invert_diatonic, parse_tok)

METER = (4, 4)
BPM = 80
NAMES = ['I Soprano', 'I Alto', 'I Tenor', 'I Bass', 'II Soprano', 'II Alto', 'II Tenor', 'II Bass']
AB = {'S1': 'I Soprano', 'A1': 'I Alto', 'T1': 'I Tenor', 'B1': 'I Bass',
      'S2': 'II Soprano', 'A2': 'II Alto', 'T2': 'II Tenor', 'B2': 'II Bass'}
NBARS = 49
REST = 'R:16'
BARS = {n: [REST] * NBARS for n in NAMES}
TAGS = [''] * NBARS
ENTRIES = []          # (voice, bar, beat offset in quarters, label, bars to emphasise)


def put(bar, **parts):
    """Write token strings (whole bars, any length) into voices from `bar` on."""
    for k, s in parts.items():
        for i, b in enumerate(concat_bars(' '.join(s.split()), METER)):
            BARS[AB[k]][bar - 1 + i] = b


def tag(bar, text):
    TAGS[bar - 1] = text


def entry(v, bar, off, label, n=2):
    ENTRIES.append((AB[v], bar, off, label, n))


def T8(s, n):
    """Explicit octave transposition."""
    return transpose(s, 12 * n, 7 * n)


EB = [3, 5, 7, 8, 10, 0, 2]          # E-flat major, from the tonic

# ---------------------------------------------------------------------------
# THE MATERIAL (written by hand; see NOTES.md for how it was tested)
#
# Subject: the first line of "Wachet auf" (Eb G Bb .. C Bb) compressed into the
# canzona rhythm long-short-short-long-long, then a sixteenth turn, a leap to
# the summit F and a fall onto the leading tone: it ends open, on D.
SUBJ = 'Eb4:4 G4:2 Bb4:2 C5:4 Bb4:4 C5:2 D5:1 C5:1 Bb4:2 D5:2 F5:4 Eb5:2 D5:2'
HEAD = 'Eb4:4 G4:2 Bb4:2 C5:4 Bb4:4'                  # its first bar
# Tonal answer: first bar a fifth up (real), second bar a fourth up, so the
# answer travels V -> I where the subject travels I -> V.
ANS = 'Bb3:4 D4:2 F4:2 G4:4 F4:4 F4:2 G4:1 F4:1 Eb4:2 G4:2 Bb4:4 Ab4:2 G4:2'
# Countersubject (against the subject, above it; invertible at the octave):
# eighths where the subject declaims, quarters where it runs, and the
# F-minor -> F-major inflection (Ab -> A) that carries the subject into B-flat.
CS = 'R:2 Bb4:2 Eb5:2 D5:2 Eb5:2 F5:2 G5:2 F5:2 Eb5:4 F5:4 Ab5:2 A5:2 Bb5:4'
# The same, fitted to the tonal answer (bar 1 a fifth up, bar 2 a fourth up).
CS_ANS = 'R:2 F5:2 Bb5:2 A5:2 Bb5:2 C6:2 D6:2 C6:2 Ab5:4 Bb5:4 Db6:2 D6:2 Eb6:4'

# Inversion: diatonic mirror about G4 (the third of the tonic), which keeps the
# tonic triad and turns the dominant into the subdominant (Contrapunctus 12).
INV = invert_diatonic(SUBJ, 'G4', EB)   # Bb4 G4 Eb4 D4 Eb4 | D4 C4 D4 Eb4 C4 Ab3 Bb3 C4


# ---------------------------------------------------------------------------
# THE MIRROR.  Coro II's exposition is Coro I's turned upside down, all four
# voices at once (I Soprano -> II Bass, I Alto -> II Tenor, I Tenor -> II Alto,
# I Bass -> II Soprano), an octave lower.  E-flat regions are mirrored about G
# (flats foreign to the key mirror to flats: B-flat minor <-> A-flat minor);
# B-flat regions are mirrored tonally into A-flat (transpose to E-flat, mirror,
# transpose down a fifth), so Coro I's dominant answers become Coro II's
# subdominant ones.

def _mirror_eb(seg):
    out = []
    for tok in seg.split():
        name, dur = tok.rsplit(':', 1)
        if name == 'R':
            out.append(tok)
            continue
        if name[1:2] == 'b' and name[0] in 'DGCF' and name[1:3] != 'bb':
            nat = name[0] + name[2:]
            m = invert_diatonic(f'{nat}:{dur}', 'G4', EB)
            mname, mdur = m.rsplit(':', 1)
            p, *_ = parse_tok(mname + ':1')
            letter = mname[0]
            octv = int(''.join(ch for ch in mname if ch.isdigit() or ch == '-'))
            acc = mname[1:].rstrip('0123456789-')
            acc = {'': 'b', 'b': 'bb', '#': ''}[acc]
            out.append(f'{letter}{acc}{octv}:{mdur}')
        else:
            out.append(invert_diatonic(tok, 'G4', EB))
    return ' '.join(out)


def _mirror_bb(seg):
    return transpose(_mirror_eb(transpose(seg, -7, -4)), -7, -4)


def _split(bar, cuts):
    """Split one bar string at the given sixteenth positions (ties kept)."""
    segs, cur, u = [], [], Fraction(0)
    cuts = list(cuts) + [16]
    ci = 0
    for tok in bar.split():
        name, d = tok.rsplit(':', 1)
        tie = d.endswith('~')
        d = Fraction(d.rstrip('~'))
        while d > 0:
            room = cuts[ci] - u
            take = min(d, room)
            rest = d - take
            t = f'{name}:{take}' + ('~' if (name != 'R' and (rest > 0 or tie)) else '')
            cur.append(t)
            u += take
            d = rest
            if u == cuts[ci]:
                segs.append(' '.join(cur))
                cur = []
                ci += 1
    return segs


def mirror(bars, regions):
    """bars: list of bar strings; regions: per bar, list of (cut_start, key)."""
    out = []
    for bar, reg in zip(bars, regions):
        cuts = [c for c, _ in reg[1:]]
        segs = _split(bar, cuts)
        m = []
        for seg, (_, key) in zip(segs, reg):
            m.append(_mirror_eb(seg) if key == 'Eb' else _mirror_bb(seg))
        out.append(T8(' '.join(m), -1))
    return out


# ===========================================================================
# 1. CORO I: EXPOSITION (b1-8, cadence on b9.1).  Entries top-down.
put(1, S1=SUBJ)
entry('S1', 1, 0, 'Coro I rectus (subject, E-flat)')
tag(1, 'Coro I: exposition, subject (soprano)')

put(3, A1=ANS, S1=T8(CS_ANS, -1))
entry('A1', 3, 0, 'Coro I rectus (tonal answer, B-flat)')
tag(3, 'Coro I: answer (alto) + countersubject')

put(5, T1=T8(SUBJ, -1), A1=T8(CS, -1),
    S1='Bb4:6 C5:2 Eb5:4 D5:4  Eb5:4 D5:4 C5:4 R:4')
entry('T1', 5, 0, 'Coro I rectus (subject, E-flat)')
tag(5, 'Coro I: subject (tenor)')

put(7, B1=T8(ANS, -1), T1=T8(CS_ANS, -2),
    A1='F4:8 Eb4:4 F4:4~  F4:4 Bb4:8 F4:2 G4:2',
    S1='D5:8 Bb4:4 A4:4  C5:4 G5:4 F5:4 D5:2 Eb5:2')
entry('B1', 7, 0, 'Coro I rectus (tonal answer, B-flat)')
tag(7, 'Coro I: answer (bass)')

put(9, S1='Bb4:4 R:12', A1='G4:4 R:12', T1='Eb4:4 R:12', B1='Eb3:4 R:12')

REG_I = [[(0, 'Eb')], [(0, 'Eb'), (8, 'Bb')], [(0, 'Bb')], [(0, 'Eb')],
         [(0, 'Eb')], [(0, 'Eb'), (8, 'Bb')], [(0, 'Bb')], [(0, 'Eb')], [(0, 'Eb')]]

# ===========================================================================
# 2. CORO II: THE MIRROR EXPOSITION (b9-16, cadence on b17.1).  Entries
# bottom-up, every line of Coro I's exposition inverted.
for src, dst in (('I Soprano', 'B2'), ('I Alto', 'T2'), ('I Tenor', 'A2'), ('I Bass', 'S2')):
    m = mirror(BARS[src][0:9], REG_I)
    for k, b in enumerate(m):
        if k == 8:
            BARS[AB[dst]][16] = b
        else:
            BARS[AB[dst]][8 + k] = b
entry('B2', 9, 0, 'Coro II inversus (mirror of b1)')
entry('T2', 11, 0, 'Coro II inversus (mirror of the answer: A-flat)')
entry('A2', 13, 0, 'Coro II inversus (mirror of b5)')
entry('S2', 15, 0, 'Coro II inversus (mirror of the answer: A-flat)')
tag(9, 'Coro II: the mirror exposition (bass first)')


# ===========================================================================
# 3a. ANTIPHONY BY THE BAR (b17-20): the choirs alternate whole bars, the head
# rectus on the left, inverted on the right, round a circle of fifths
# E-flat -> f -> B-flat -> E-flat.  Each bar ends on a dominant that the other
# choir resolves across the hall; Coro II's bar ends plagally (its mirror dialect).
put(17, A1='Eb4:4 G4:2 Bb4:2 C5:4 Bb4:4',
        S1='R:2 Bb4:2 Eb5:2 D5:2 Eb5:2 F5:2 E5:2 G5:2',
        T1='G3:4 Bb3:4 Ab3:4 G3:4',
        B1='R:4 Eb2:4 Ab2:4 C3:4')
entry('A1', 17, 0, 'Coro I head (E-flat)', 1)
tag(17, 'Antiphony by the bar: heads round a circle of fifths')
put(18, S2='C5:4 Ab4:2 F4:2 E4:4 F4:4',
        A2='R:2 F4:2 C4:2 Db4:2 C4:2 Bb3:2 C4:4',
        T2='Ab3:4 F3:4 G3:4 A3:4',
        B2='F3:4 Ab2:4 C3:4 F2:4')
entry('S2', 18, 0, 'Coro II inverted head (f minor)', 1)
put(19, B1='Bb2:4 D3:2 F3:2 G3:4 F3:4',
        S1='R:2 F4:2 Bb4:2 A4:2 Bb4:2 C5:2 D5:4',
        A1='D4:4 F4:4 Eb4:4 Ab4:4',
        T1='F3:8 Bb3:4 Bb3:4')
entry('B1', 19, 0, 'Coro I head (B-flat)', 1)
put(20, T2='Bb3:4 G3:2 Eb3:2 D3:4 Eb3:4',
        S2='Bb4:4 Eb5:4 F5:4 Ab5:4',
        A2='G4:2 Ab4:2 Bb4:2 G4:2 F4:2 Bb3:2 C4:2 Eb4:2',
        B2='Eb3:4 G2:4 Bb2:4 Ab2:4')
entry('T2', 20, 0, 'Coro II inverted head (E-flat)', 1)


# ===========================================================================
# 3b. ANTIPHONY BY THE BAR, OVERLAPPING (b21-24): whole entries a bar apart,
# choir against choir, each overlapping the last by a bar (eight voices):
# c-level rectus (Coro I alto) over a falling C-Bb-Ab-G bass, the inversion on D
# (Coro II soprano), the E-flat rectus (Coro I tenor), which carries Coro I to
# a B-flat cadence while Coro II falls silent.
put(21, A1='C4:4 Eb4:2 G4:2 Ab4:4 G4:4  Ab4:2 Bb4:1 Ab4:1 G4:2 Bb4:2 D5:4 C5:2 Bb4:2',
        S1='Eb5:6 D5:2 F5:4 D5:4  Bb4:4 G5:4 R:8',
        T1='G3:4 C4:4 C4:4 B3:4  Bb3:12 G3:4',
        B1='C3:4 Bb2:4 F2:4 G2:4  Bb2:4 Eb3:4 D3:4 Eb3:4')
entry('A1', 21, 0, 'Coro I rectus (c minor level)')
tag(21, 'Antiphony by the bar, overlapping: entries a bar apart')
put(22, S2='D5:4 Bb4:2 G4:2 F4:4 G4:4  F4:2 Eb4:1 F4:1 G4:2 Eb4:2 C4:4 D4:2 Eb4:2',
        A2='F4:4 Eb4:4 R:8  R:16',
        T2='F3:4 G3:4 R:8  G3:4 Bb3:4 Ab3:4 F3:4',
        B2='Bb2:4 G2:4 Bb1:4 Eb2:4  Bb2:4 G2:4 Eb3:4 Bb2:4')
entry('S2', 22, 0, 'Coro II inversus (on D)')
put(23, T1='Eb3:4 G3:2 Bb3:2 C4:4 Bb3:4  C4:2 D4:1 C4:1 Bb3:2 D4:2 F4:4 Eb4:2 D4:2',
        S1='Bb4:4 Eb5:2 D5:2 Eb5:4 D5:4  C5:4 D5:4 C5:4 F5:4~',
        A1='G4:4 Eb4:8 Ab4:4  Ab4:4 F4:4 A4:8',
        B1='Eb2:8 Ab2:4 Bb2:4  Ab2:4 Bb2:4 A2:4 F2:4')
entry('T1', 23, 0, 'Coro I rectus (E-flat, to B-flat)')


# ===========================================================================
# 4. THE CHOIRS DISAGREE ABOUT THE KEY (b25-31).  Coro I has arrived on
# B-flat and means it (its signature note is A-natural); Coro II answers in
# A-flat (signature D-flat).  The exchanges shrink from a bar to half a bar to
# a beat.  Superimposed, the two chords are B-flat-eleven, the home dominant:
# when each choir concedes a semitone (A -> A-flat, D-flat -> D) they find
# B-flat-seven together, and E-flat.
put(25, S1='F5:8 Eb5:8',
        A1='D4:4 G4:2 A4:2 Bb4:2 C5:2 A4:2 C5:2',
        T1='Bb3:4 D4:2 F4:2 G4:4 F4:4',
        B1='Bb2:8 Eb3:4 F3:4')
entry('T1', 25, 0, 'Coro I head (B-flat!)', 1)
tag(25, 'Disagreement: Coro I in B-flat, Coro II in A-flat')
put(26, S2='Eb5:4 C5:2 Ab4:2 G4:4 Ab4:4',
        A2='R:2 Ab4:2 Eb4:2 F4:2 Eb4:2 Db4:2 C4:2 Db4:2',
        T2='Eb3:4 Ab3:4 Bb3:4 Ab3:4',
        B2='Ab2:4 C3:4 Eb3:4 Ab2:4')
entry('S2', 26, 0, 'Coro II inverted head (A-flat!)', 1)
# half a bar each
put(27, S1='Bb4:4 D5:2 F5:2 R:8  D5:4 F5:2 Bb5:2 R:8',
        A1='F4:2 A4:2 Bb4:4 R:8  F4:2 A4:2 Bb4:4 R:8',
        T1='D4:4 F4:4 R:8  Bb3:4 D4:4 R:8',
        B1='Bb2:8 R:8  D3:4 Bb2:4 R:8')
put(27, S2='R:8 Eb5:4 C5:2 Ab4:2  R:8 Ab4:4 Db5:2 C5:2',
        A2='R:8 Ab4:4 Eb4:2 F4:2  R:8 Eb4:4 Ab4:4',
        T2='R:8 C4:2 Db4:2 C4:4  R:8 Eb4:4 C4:2 Ab3:2',
        B2='R:8 Ab2:8  R:8 C3:4 Ab2:4')
tag(27, 'half a bar')
# a beat each, then together
put(29, S1='Bb4:2 D5:1 F5:1 R:4 D5:2 F5:1 Bb5:1 R:4',
        A1='F4:2 A4:2 R:4 F4:2 A4:2 R:4',
        T1='D4:4 R:4 D4:4 R:4',
        B1='Bb2:4 R:4 Bb2:4 R:4')
put(29, S2='R:4 Eb5:2 C5:1 Ab4:1 R:4 Ab5:2 Eb5:1 C5:1~',
        A2='R:4 Ab4:2 Db5:2 R:4 Ab4:4~',
        T2='R:4 C4:4 R:4 Eb4:4~',
        B2='R:4 Ab2:4 R:4 Ab2:4')
tag(29, 'a beat')


# the two chords superimposed (A-flat over B-flat), then the concession:
# 9-8 and 11-10 in Coro II, its bass walking down B-flat-seven, into E-flat.
put(30, S1='F5:16', A1='Bb4:8 F4:4 D4:4', T1='Bb3:12 F3:4', B1='Bb2:16',
        S2='C5:4 Bb4:12~', A2='Ab4:16', T2='Eb4:4 D4:4 C4:4 Bb3:4', B2='Bb2:8 F3:4 Bb2:4')
tag(30, 'Reconciliation: A-flat over B-flat = the home dominant')


# ===========================================================================
# 5. THE JOKE (b31-36).  Reconciled, Coro I turns pompous: a French-overture
# dotted style over its bass, which begins the subject in AUGMENTATION.  Coro II
# twice cuts it short with the whole subject in DIMINUTION, chattered in a
# single bar (first rectus in the soprano, then inverted in the basses).  Coro I
# resumes each time, flustered (the first time on a deceptive C minor).  Then
# it gives up, and the choirs toss the diminished head across the hall a beat
# apart.  The augmentation's last bar is never sung -- until the coda.
AUG = scale_rhythm(SUBJ, 2)          # Eb4:8 G4:4 Bb4:4 C5:8 Bb4:8 C5:4 D5:2 C5:2 Bb4:4 D5:4 F5:8 Eb5:4 D5:4
DIM = scale_rhythm(SUBJ, '1/2')      # the whole subject in one bar
put(31, B1=T8('Eb4:8 G4:4 Bb4:4', -2),
        S1='Eb5:6 D5:2 Eb5:4 F5:4', A1='Eb4:6 F4:2 Bb4:4 F4:4', T1='G3:6 Ab3:2 Bb3:4 Bb3:4',
        S2='Bb4:4 R:12', A2='G4:4 R:12', T2='Bb3:4 R:12', B2='Eb3:4 R:12')
entry('B1', 31, 0, 'Coro I augmentation (pompous)', 4)
tag(31, 'The joke: augmentation interrupted by diminution')
put(32, S2=DIM, A2='Bb3:4 Eb4:4 C4:4 Bb3:4', T2='G3:4 Ab3:8 F3:4', B2='Eb3:4 Ab2:8 Bb2:4')
entry('S2', 32, 0, 'Coro II diminution (interrupting)', 1)
put(33, B1=T8('C5:8 Bb4:8', -2),
        S1='Eb5:6 F5:2 D5:8', A1='G4:6 Ab4:2 Bb4:8', T1='Eb4:8 F4:8')
put(34, B2=T8(invert_diatonic(DIM, 'G4', EB), -1),
        S2='G5:4 F5:2 G5:2 F5:2 Eb5:6', A2='Eb5:4 Bb4:8 C5:4', T2='Eb4:4 F4:6 G4:2 C4:4')
entry('B2', 34, 0, 'Coro II diminution, inverted (interrupting again)', 1)
put(35, B1=T8('C5:4 D5:2 C5:2 Bb4:4 D5:4', -2),
        S1='Ab5:6 G5:2 G5:4 F5:4', A1='Eb4:6 F4:2 Eb4:4 Bb4:4', T1='C4:6 Bb3:2 Bb3:4 Bb3:4')
# a beat each: the diminished head, rectus on the left, inverted on the right
put(36, S2='F5:2 D5:1 Bb4:1 R:12',
        A2='Bb4:4 R:4 D5:4 R:4',
        T2='D4:4 R:4 F4:2 D4:1 Bb3:1 R:4',
        B2='Bb2:4 R:4 Bb2:4 R:4',
        S1='R:4 Bb4:2 D5:1 F5:1 F5:4 Eb5:4',
        A1='R:4 F4:4 R:4 D4:2 F4:1 Ab4:1',
        T1='R:4 D4:4 R:8',
        B1='R:4 Bb2:8 Bb1:4')
tag(36, 'a beat')


# ===========================================================================
# 6. THE SUMMIT: STRETTO A 8 (b37-42).  Every one of the eight voices enters,
# half a bar apart, choir against choir: Coro I rectus (c, then A-flat three
# times), Coro II inversus (on F, then E-flat three times), found by searching
# levels and voice orders for which every overlapping pair is clean, then
# written out with the free parts by hand.  It breaks in deceptively on
# C minor and climbs to the soprano's B-flat.
SUB_c = 'C3:4 Eb3:2 G3:2 Ab3:4 G3:4 Ab3:2 Bb3:1 Ab3:1 G3:2 Bb3:2 D4:4 C4:2 Bb3:2'   # rectus, c level
INV_F = 'F4:4 D4:2 Bb3:2 Ab3:4 Bb3:4 Ab3:2 G3:1 Ab3:1 Bb3:2 G3:2 Eb3:4 F3:2 G3:2'   # inversus on F
SUB_Ab = transpose(SUBJ, -7, -4)                                                   # rectus, A-flat level
put(37, T2='R:8 ' + INV_F + ' R:8  R:8 D4:4 C4:4  R:16  R:16',
        T1=SUB_c + ' C4:4 R:12  Bb3:4 R:4 Bb3:4 R:4  Bb3:4 R:12  R:8 C4:4 R:4',
        S1='Eb5:8 C5:4 R:4  ' + T8(SUB_Ab, 1) + '  R:8 F5:4 C5:4  Bb4:8 R:8  R:8 Ab4:4 Bb4:4',
        A1='G4:8 Eb4:4 Bb3:4  Eb4:8 R:8  ' + SUB_Ab + '  F4:4 G4:4 F4:4 G4:4~  G4:4 F4:4 Eb4:4 D4:4',
        B1='R:8 F2:4 Bb2:4  C3:4 G2:4 Bb2:4 Eb2:4  Ab2:8 R:8  ' + T8(SUB_Ab, -1) + '  Eb3:8 F3:4 Bb2:4',
        B2='R:8 Ab2:4 R:4  Ab2:4 Eb3:4 Bb2:4 C3:4  R:8 ' + T8(INV, -1) + ' R:8  Ab2:8 R:8',
        A2='R:16  R:8 ' + INV + ' R:8  R:16  C4:8 R:8',
        S2='R:16  R:16  R:8 D5:4 C5:4  R:8 ' + T8(INV, 1))
for v, b, off, lab in (('T1', 37, 0, 'stretto a 8: Coro I rectus (c)'), ('T2', 37, 2, 'stretto a 8: Coro II inversus (on F)'),
                       ('S1', 38, 0, 'stretto a 8: Coro I rectus (A-flat)'), ('A2', 38, 2, 'stretto a 8: Coro II inversus (E-flat)'),
                       ('A1', 39, 0, 'stretto a 8: Coro I rectus (A-flat)'), ('B2', 39, 2, 'stretto a 8: Coro II inversus (E-flat)'),
                       ('B1', 40, 0, 'stretto a 8: Coro I rectus (A-flat)'), ('S2', 40, 2, 'stretto a 8: Coro II inversus (E-flat)')):
    entry(v, b, off, lab)
tag(37, 'Summit: stretto a 8, all voices enter half a bar apart')


# ===========================================================================
# 7. CODA (b43-49).  The first line of "Wachet auf" in long notes in Coro I's
# tenor, where BWV 645 puts the chorale; the subject's heads and tails around
# it in both choirs.  Under the chorale's C, Coro I's bass at last finishes the
# augmentation it was never allowed to finish (F - E-flat - D).  The final
# cadence is the reconciliation chord again (A-flat over B-flat), and Coro II
# has the last word: an echo of the head, upside down.
CHORALE_1 = 'Eb3:8 G3:8  Bb3:12 Bb3:4  Bb3:8 Bb3:8  C4:16  Bb3:16'   # Nicolai 1599, line 1
put(43, T1=CHORALE_1 + '  Bb3:16  Bb3:16',
        B1='R:8 C3:8  G2:8 Bb2:8  C3:8 G2:8  ' + T8('F5:8 Eb5:4 D5:4', -3) + '  Bb1:16  Eb2:16  Eb2:16',
        A1=HEAD + '  Bb4:8 F4:8  R:16  R:8 F4:8  F4:16  G4:8 R:8  Eb4:16',
        S1='Bb4:8 Eb5:8  Eb5:8 F5:8  Eb5:16  Ab5:16~  Ab5:16  G5:16  G5:16',
        S2='R:8 G5:8  G5:8 R:8  G5:16  G5:4 F5:4 R:8  Eb5:8 F5:8  Eb5:8 Bb4:4 G4:2 Eb4:2  Eb5:16',
        A2='R:16  R:16  Eb5:8 Bb4:8  Ab4:12 Bb4:4  C5:8 Bb4:8  Bb4:8 R:8  Bb4:16',
        T2='R:8 Eb4:8  Eb4:12 D4:4  C4:8 Eb4:8~  Eb4:16~  Eb4:16  R:16  G3:16',
        B2='R:16  R:16  G3:8 R:8  C3:16~  C3:8 D3:8  R:16  Eb3:16')
entry('T1', 43, 0, 'Chorale "Wachet auf", line 1 (tenor)', 5)
entry('A1', 43, 0, 'Coro I head', 1)
entry('B1', 46, 0, 'Coro I finishes its augmentation', 1)
entry('S2', 48, 2, 'Coro II: the echo, upside down', 1)
tag(43, 'Coda: "Wachet auf" in the tenor; the augmentation finished')
tag(47, 'Final cadence: A-flat over B-flat, then E-flat')

# === SECTIONS-END ===


def DYN(b):
    """Phrase dynamics by bar index (0-based): the expositions moderate, the
    argument louder, the joke's chatter lighter, the summit and coda full."""
    bar = b + 1
    if bar <= 16:
        return -4
    if 25 <= bar <= 30:
        return 3
    if 37 <= bar <= 42:
        return 6
    if bar >= 43:
        return 4
    return 0


# Performance only (no notes): Coro I on the left, Coro II on the right; the
# chatter of the diminutions detached; the final echo soft.
PAN = {'I Soprano': 22, 'I Alto': 32, 'I Tenor': 42, 'I Bass': 52,
       'II Soprano': 106, 'II Alto': 96, 'II Tenor': 86, 'II Bass': 76}
TEMPO_MAP = [[0, BPM],
             [112, BPM], [120, 70, 'ramp'],           # b29-30: broadening into the reconciliation
             [120, 76],                               # b31 Coro I, pompous
             [124, 86], [128, 76], [132, 86], [136, 76],   # chatter v. pomp
             [140, 82],                               # b36: a beat
             [144, 74],                               # b37: the summit, broad
             [168, 76],                               # b43: coda
             [184, 76], [196, 48, 'ramp']]            # final ritardando


def build(path=HERE / 'fugue.json'):
    meta = {'title': 'The Well-Tempered clAIvier', 'subtitle': 'Fugue VII in E-flat major (a 8): Fuga a due cori',
            'composer': 'Claude / Sam', 'instrument': 'Two four-voice choirs (Coro I left, Coro II right)',
            'key': 'Eb', 'mode': 'major', 'meter': list(METER), 'bpm': BPM, 'tempo_map': TEMPO_MAP,
            'tempo_text': 'Allegro festivo', 'movement_number': 7, 'piece_type': 'fugue',
            'edition': 'third', 'markers': [{'t': (b - 1) * 4, 'label': t} for b, t in enumerate(TAGS, 1) if t]}
    voices = [('I Soprano', 'S1', 'treble', 74), ('I Alto', 'A1', 'treble', 70), ('I Tenor', 'T1', 'treble_8', 70),
              ('I Bass', 'B1', 'bass', 72), ('II Soprano', 'S2', 'treble', 74), ('II Alto', 'A2', 'treble', 70),
              ('II Tenor', 'T2', 'treble_8', 70), ('II Bass', 'B2', 'bass', 72)]
    data = build_score(path, meta, voices, BARS, entries=ENTRIES, subject=SUBJ, dynamics=DYN, tags=TAGS)
    for v in data['voices']:
        v['piano_pan'] = PAN[v['name']]
        for e in v['events']:
            t = float(e['t'])
            if (v['name'] == 'II Soprano' and 124 <= t < 128) or (v['name'] == 'II Bass' and 132 <= t < 136):
                e['gate'] = 0.62                      # the chatter, detached
            if v['name'] == 'II Soprano' and 190 <= t < 192:
                e['v'] = max(30, int(e['v']) - 24)    # the echo, upside down and soft
    Path(path).write_text(json.dumps(data, indent=1))
    return data


if __name__ == '__main__':
    build()
    print('bars', NBARS)
