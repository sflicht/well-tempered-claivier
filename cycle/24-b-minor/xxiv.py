"""Shared material and placement helpers for Fugue XXIV in B minor (25 voices).

Nothing here chooses a note.  The materials below are written by hand (or quoted
exactly from the finished fugues of this edition); `Score.put` places literal token
strings at bar.beat positions, `Score.theme` does the same and records the entry so
the critic and check.py can verify it.  Explicit transforms (transpose, scale_rhythm)
are wtclib's and are named where used.
"""
from __future__ import annotations

import sys
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'tools'))
import wtclib as W  # noqa: E402

METER = (4, 4)

# ------------------------------------------------------------------ voices
# 25 real voices, named by register, highest first.
VOICES = [
    ('S1', 'Soprano I', 'treble'), ('S2', 'Soprano II', 'treble'), ('S3', 'Soprano III', 'treble'),
    ('S4', 'Soprano IV', 'treble'), ('S5', 'Soprano V', 'treble'),
    ('A1', 'Alto I', 'treble'), ('A2', 'Alto II', 'treble'), ('A3', 'Alto III', 'treble'),
    ('A4', 'Alto IV', 'treble'), ('A5', 'Alto V', 'treble'),
    ('T1', 'Tenor I', 'treble_8'), ('T2', 'Tenor II', 'treble_8'), ('T3', 'Tenor III', 'treble_8'),
    ('T4', 'Tenor IV', 'treble_8'), ('T5', 'Tenor V', 'treble_8'),
    ('Br1', 'Baritone I', 'bass'), ('Br2', 'Baritone II', 'bass'), ('Br3', 'Baritone III', 'bass'),
    ('Br4', 'Baritone IV', 'bass'), ('Br5', 'Baritone V', 'bass'),
    ('B1', 'Bass I', 'bass'), ('B2', 'Bass II', 'bass'), ('B3', 'Bass III', 'bass'),
    ('B4', 'Bass IV', 'bass'), ('B5', 'Contrabass', 'bass'),
]
NAMES = [v[0] for v in VOICES]

# ------------------------------------------------------------------ the subject set
# S: the twelve-tone subject (all twelve pitch classes; B minor).  It ends on the
# leading tone A#; the B that resolves it belongs to whatever follows.
#   | B4  D5 C#5  E#4.  F#4 | D#5.  E5  C5.  B4 | G4 G#4 A4 A#4 | (B4)
# Three leaning dotted figures (E#->F#, D#->E, C->B), then a chromatic climb.
S = "B4:4 D5:2 C#5:2 E#4:6 F#4:2 D#5:6 E5:2 C5:6 B4:2 G4:2 G#4:2 A4:2 A#4:2"
# Its exact mirror around B (also twelve-tone); the tail falls D# D C# C into B.
I = "B4:4 G#4:2 A4:2 E#5:6 E5:2 G4:6 F#4:2 A#4:6 B4:2 D#5:2 D5:2 C#5:2 C5:2"
# CS1: the suspension-chain countersubject (halves/quarters, tied), written above S.
CS1 = "R:4 F#5:8 E#5:2 C#6:2~ C#6:4 B5:8 A5:4 G5:4 F#5:8 E5:4"
# U: the urgent upbeat figure: three repeated eighths, a sixth's leap onto a leaning
# dotted quarter, a step down (the subject's own F#->D# leap and lean).
U = "C#4:2 C#4:2 C#4:2 A4:6 G4:2"
# R: the running sixteenth figure (lower-neighbour turn, then a climb).
R = "B4:1 A#4:1 B4:1 C#5:1 D5:1 C#5:1 D5:1 E5:1"

# ------------------------------------------------------------------ guests (exact quotations)
# Copied note for note from the first statements in the finished fugue.json files.
GUESTS = {
    'I': ("G4:2 C5:3 D5:1 E5:2 C5:2 G5:4 F5:1 E5:1 D5:1 C5:1 D5:2 G4:2 A4:1 B4:1 C5:1 B4:1 E5:2 F5:2 G5:2",
          'Fugue I in C major (cycle/01-c-major), subject, upbeat eighth'),
    'II': ("C5:4 B4:2 D5:2 G4:2 Eb5:2 G4:2 F5:2 Eb5:1 D5:1 C5:1 D5:1 Eb5:2 D5:1 C5:1 B4:2 C5:4 G4:2",
           'Fugue II in C minor (cycle/02-c-minor), subject'),
    'IV': ("G#4:2 E4:1 D#4:1 B3:2 F#4:6 A4:4 F#4:2 D#4:2 B#3:2 C#4:2",
           'Fugue IV in C-sharp minor (cycle/04-c-sharp-minor), subject (3/4, re-barred in 4/4)'),
    'V': ("A4:4 D5:2 D5:1 D5:1 F#5:2 F#5:1 F#5:1 A5:4 A5:3 G5:1 F#5:2 E5:2 D5:1 C#5:1 B4:1 A4:1 B4:1 C#5:1 D5:2",
          'Fugue V in D major (cycle/05-d-major), subject'),
    'VIII': ("Eb4:4 Bb4:4 Cb5:3 Bb4:1 Ab4:2 Gb4:2 F4:2 D4:2 Eb4:4",
             'Fugue VIII in E-flat minor (cycle/08-e-flat-minor), subject (head = BWV 853)'),
}


def tr(s, semis, letters):
    return W.transpose(s, semis, letters)


def octv(s, n):
    return W.transpose(s, 12 * n, 7 * n)


def aug(s, k):
    return W.scale_rhythm(s, k)


def dur16(toks):
    return sum(W.parse_tok(t)[1] for t in toks.split())


class Score:
    """Literal segments placed at bar.beat (bar 1-based, beat 1-based quarters)."""

    def __init__(self, first_bar=1):
        self.first = first_bar
        self.segs = {n: [] for n in NAMES}
        self.entries = []      # (voice, start16, label, theme_key, transform)
        self.marks = []

    def pos(self, bar, beat):
        return Fr(bar - self.first) * 16 + (Fr(beat) - 1) * 4

    def put(self, v, bar, beat, toks):
        self.segs[v].append((self.pos(bar, beat), ' '.join(toks.split())))

    def theme(self, v, bar, beat, toks, label, key, scale=1, semis=0, inverted=False):
        self.put(v, bar, beat, toks)
        self.entries.append((v, self.pos(bar, beat), label, key, scale, semis, inverted))

    def mark(self, bar, beat, text):
        self.marks.append((self.pos(bar, beat), text))

    def bars(self, nbars):
        out = {}
        for v in NAMES:
            segs = sorted(self.segs[v], key=lambda x: x[0])
            cur, toks = Fr(0), []
            for s, t in segs:
                if s < cur:
                    raise ValueError(f'{v}: overlap at bar {self.first + s / 16} ({t[:40]})')
                if s > cur:
                    toks.append(f'R:{s - cur}')
                toks.append(t)
                cur = s + dur16(t)
            if cur > nbars * 16:
                raise ValueError(f'{v}: runs past bar {self.first + nbars - 1}')
            if cur < nbars * 16:
                toks.append(f'R:{nbars * 16 - cur}')
            out[v] = W.concat_bars(' '.join(toks), METER)
        return out
