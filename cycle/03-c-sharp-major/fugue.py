#!/usr/bin/env python3
"""Fugue III in C-sharp major, four voices: "Giga a 4, rectus et inversus".

12/8, dotted quarter = 96 (quarter = 144), 45 bars.  A gigue in two halves:
Part 1 (bars 1-20) presents the subject rectus and cadences in G# major;
Part 2 (bars 21-39) presents it inversus and turns home; in the coda
(bars 40-45) a passage of Part 1 and its mirror image from Part 2 sound at
once.  See NOTES.md for the design, the searches and the proofs.

Every note is written here.  Thematic entries are hand-written material put
through named transforms (wtclib.transpose / wtclib.invert_diatonic); free
counterpoint is literal token strings.  Units: sixteenths (a 12/8 bar = 24).
"""
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import wtclib  # noqa: E402
from wtclib import build_score, invert_diatonic, parse_tok  # noqa: E402

HERE = Path(__file__).resolve().parent
METER = (12, 8)
BAR = 24
C_MAJ = [1, 3, 5, 6, 8, 10, 0]     # C# major, from the tonic (for diatonic mirrors)
G_MAJ = [8, 10, 0, 1, 3, 5, 7]     # G# major


def at(bar, eighth=0):
    """Sixteenth offset of an eighth-note position in a bar (1-based bar)."""
    return (bar - 1) * BAR + 2 * eighth


def T(s, semis, letters):
    """Transpose by a chromatic and a letter interval (explicit, exact)."""
    return wtclib.transpose(s, semis, letters)


def pick(s):
    """The pickup (first token) of a phrase written with its anacrusis."""
    return s.split()[0]


def nopick(s):
    return ' '.join(s.split()[1:])


def drop_last(s):
    return ' '.join(s.split()[:-1])


# ---------------------------------------------------------------------------
# MATERIAL (written by hand)

# Subject: four stamps up the tonic triad (long-short, long-short, long + a silent
# eighth: the hop), an octave drop to the low fifth with a sixteenth flick, a run up
# to F#, and the cadence 1-7-1.  Declared without its eighth-note pickup (G#4).
SUBJ = ("C#5:4 C#5:2 E#5:4 E#5:2 G#5:4 R:2 G#4:4 A#4:1 B#4:1 "
        "C#5:2 D#5:2 E#5:2 F#5:4 E#5:2 C#5:4 B#4:2 C#5:4")
SP = "G#4:2 " + SUBJ                      # with the pickup

# Countersubject (sounds above the subject): rises, hovers E#6-D#6, dips to G#5,
# hovers again and glides down against the subject's run.  Invertible at the 15th.
CS = ("E#5:4 F#5:2 G#5:6 E#6:4 D#6:2 G#5:6 "
      "E#6:2 D#6:2 C#6:2 A#5:4 G#5:2 E#5:4 D#5:2 E#5:4")

# J. S. Bach, WTC I, Fugue in C# major BWV 848: the head of the subject
# (reference/bach-subjects.md) re-barred as a gigue: G# A#-G# F#-G# E#' C#' G# F#-E# F# D#'.
# Our inversus ends G#:4 A#:2 G#..., i.e. with the first beat of Bach's head; the
# rest of the head is this continuation.
BWV848_REST = "G#5:2 F#5:2 G#5:2 E#6:4 C#6:2 G#5:4 F#5:1 E#5:1 F#5:4 D#6:2"

# ---------------------------------------------------------------------------
# DERIVED FORMS (named transforms of the material above)

ANS = T(SUBJ, -5, -3)                       # answer in G#, a 4th below (pickup C#: tonal)
CS_G = T(CS, -5, -3)                        # countersubject in G#
S_AM = ("A#3:4 A#3:2 C#4:4 C#4:2 E#4:4 R:2 E#3:4 F##3:1 G##3:1 "        # subject in A# minor
        "A#3:2 B#3:2 C#4:2 D#4:4 C#4:2 A#3:4 G##3:2 A#3:4")            # (melodic minor)
CS_AM = ("C#5:4 D#5:2 E#5:6 C#6:4 B#5:2 E#5:6 "                         # CS in A# minor
         "C#6:2 B#5:2 A#5:2 F#5:4 E#5:2 C#5:4 B#4:2 C#5:4")

# Tonal inversus: diatonic mirror around E#, which maps the tonic triad onto itself
# (C#<->G#, E# fixed) and the leading-tone half-diminished seventh onto itself.
INV_C_T = invert_diatonic(SP, 'E#4', C_MAJ)          # tenor  (coda source, bars 23-24)
CSI_C_B = invert_diatonic(CS, 'E#4', C_MAJ)          # bass   (coda source, bars 23-24)
INV_C_S = invert_diatonic(SP, 'E#5', C_MAJ)          # soprano, bars 27-28
CSI_C_A = invert_diatonic(CS, 'E#5', C_MAJ)          # alto,    bars 27-28
INV_G = invert_diatonic(T(SP, 7, 4), 'B#4', G_MAJ)   # inversus in G# (mirror around B#)
CSI_G_B = invert_diatonic(T(CS, 7, 4), 'B#4', G_MAJ)

# Real inversus: the chromatic mirror around D#, which keeps the C#-major collection
# but turns it into A# minor (I <-> vi).  Found by search to make the closest
# rectus/inversus stretto (three dotted-quarter beats).
INV_D = invert_diatonic(SP, 'D#4', C_MAJ)

# ---------------------------------------------------------------------------
V = {'S': [], 'A': [], 'T': [], 'B': []}


def put(v, t, tok):
    V[v].append((t, tok))


# ======================= PART 1: rectus  (C# -> G#) =============================
# Exposition: soprano, alto, tenor, bass; the voice that has stated the subject
# continues with the countersubject above the next entry.
put('S', at(1), SUBJ)                                              # E1 rectus
put('A', at(2, 11), "C#4:2"); put('A', at(3), ANS)                 # E2 answer (G#)
put('S', at(3), CS_G)
put('T', at(4, 11), "G#3:2"); put('T', at(5), T(SUBJ, -12, -7))     # E3 rectus
put('A', at(5), T(CS, -12, -7))
put('S', at(5), "C#5:6 B#4:4 C#5:2 G#5:6 B#5:6 G#5:6 D#6:4 C#6:2 G#5:4 F#5:2 G#5:4")
put('B', at(6, 11), "C#3:2"); put('B', at(7), T(SUBJ, -29, -17))   # E4 answer (G#)
put('T', at(7), T(CS, -17, -10))
put('S', at(7), "B#5:12 F##5:10 R:2 G#5:6 A#5:4 G#5:2 D#6:4 C#6:2 B#5:4")
put('A', at(7), "G#4:2 B#4:2 G#4:2 G#4:2 A#4:2 G#4:2 D#5:6 B#4:4 A#4:2 "
                "D#5:2 C#5:2 D#5:2 C#5:4 D#5:12")
# E5: an extra tonic entry -- alto rectus with the countersubject ABOVE it in the
# soprano.  These two lines (bars 9-10) are the rectus half of the coda.
put('A', at(8, 11), "G#4:2"); put('A', at(9), SUBJ)               # E5 rectus
put('S', at(9), CS)
put('T', at(9), "E#4:2 D#4:2 C#4:2 G#3:6 C#4:12 G#3:6 B#3:4 C#4:6 G#3:6")
put('B', at(9), "A#2:6 B#2:6 C#3:6 E#3:6 C#3:2 B#2:2 A#2:2 D#3:4 E#3:6 G#2:2 C#3:4")

# Episode 1 (11-12), C# -> A# minor: the bass stamps the head round the circle of
# fifths (C# F# B#ø E#7); soprano falling runs (the inverted run) and tenor rising
# runs (the rectus run) take turns, each holding while the other moves.
put('B', at(11), "C#3:4 C#3:2 E#3:4 E#3:2 F#3:4 F#3:2 D#3:4 E#3:2 "
                 "B#2:4 B#2:2 D#3:4 D#3:2 E#3:4 E#3:2 G##2:4 E#2:2")
put('S', at(11), "C#6:2 B#5:2 A#5:2 G#5:4 A#5:14 B#5:2 A#5:2 G#5:2 F#5:6 D#5:12")
put('T', at(11), "E#4:12 C#4:2 D#4:2 E#4:2 F#4:4 E#4:2 D#4:12 B#3:2 C#4:2 D#4:2 E#4:4")

# M1 (13-14): rectus in A# minor, tenor, after a V7-VI deceptive arrival; the
# soprano's seventh D#5 resolves into the minor countersubject.
put('T', at(12, 11), "E#3:2"); put('T', at(13), S_AM)
put('S', at(13), CS_AM)
put('A', at(13), "F#4:6 E#4:6 A#4:4 G##4:2 A#4:6 E#5:6 A#4:10 E#4:6")
# (Nov 2026) the bass's A#2 is struck an eighth early, with the tenor's short C#4
# stamp: on the beat the tenor's E#4 and the soprano's C#6 lie 19 and 20 semitones
# from it, beyond any split of two hands; the A#-minor chord is already sounding.
put('B', at(13), "F#2:6 C#3:4 A#2:8 C#3:6 A#2:6 B#2:4 C#3:2 E#3:6 A#2:4")

# Episode 2 (15-16), A#m -> G#: the subject's hop (high note, silent eighth, octave
# drop, flick) is tossed soprano -> alto over ii - V7; V7 -> I6 - ii - V7.
put('S', at(15), "C#6:4 R:2 C#5:4 D#5:1 E#5:1 F##5:6 A#5:6 G#5:6 A#5:4 G#5:2 F##5:10")
put('A', at(15), "A#4:12 D#5:4 R:2 D#4:4 E#4:1 F##4:1 G#4:6 C#5:6 D#5:6 C#5:6")
put('T', at(15), "E#3:6 C#4:12 A#3:6 D#4:6 C#4:4 B#3:2 A#3:12")
put('B', at(15), "A#2:2 B#2:2 A#2:2 G#2:4 F##2:2 D#3:12 B#2:6 A#2:6 D#3:12")

# M2 (17-18): rectus in G#, soprano; the countersubject inverted at the 15th in the bass.
put('S', at(16, 11), "D#5:2"); put('S', at(17), T(SUBJ, 7, 4))
put('B', at(17), T(CS_G, -24, -14))
put('A', at(17), "B#4:6 F##4:6 F##4:4 G#4:2 A#4:6 D#5:6 G#4:6 B#4:4 C#5:2 B#4:4")
put('T', at(17), "G#3:6 F##3:6 D#4:6 A#3:6 R:12 D#4:10")

# Close of Part 1 (19-20): the head in the bass, I - I6 - IV - V, and the dancers stamp.
put('B', at(19), "G#2:4 G#2:2 B#2:4 B#2:2 C#3:4 R:2 D#3:6 G#2:4 G#2:2 G#2:4 G#2:2 G#2:4")
put('T', at(19), "G#3:6 D#4:6 E#4:6 A#3:6 B#3:4 B#3:2 B#3:4 B#3:2 B#3:4")
# (Nov 2026) alto G#5 F##5 (was G#4 F##4): the I6 of beat 2 is struck B#2 D#4 | G#5 D#6,
# two hands' reach (with G#4 one hand needed 19 semitones).
put('A', at(19), "D#5:6 G#5:12 F##5:6 B#4:4 B#4:2 D#5:4 D#5:2 G#5:4")
put('S', at(19), "B#5:6 D#6:6 C#6:6 B#5:4 A#5:2 G#5:4 G#5:2 B#5:4 B#5:2 D#6:4")

# ======================= PART 2: inversus  (G# -> C#) ===========================
# Exposition in the mirrored order: bass, tenor, alto, soprano.
put('B', at(21), nopick(INV_D))           # E1* inversus, real mirror: A# minor (VI after Part 1's G#)
put('S', at(21), "R:6 C#6:4 R:8 A#5:4 R:2 R:12 G#5:4 R:8 R:6 A#5:4 R:14 R:6 A#5:4 R:12")
# high bells over the lone bass (21-22) and over the tenor+bass pair (23-24): A#5 turns
# bar 23's second beat into vi and bar 24's into a full viiø7 (the pair itself is untouched)
put('T', at(22, 11), pick(INV_C_T)); put('T', at(23), nopick(INV_C_T))   # E2* (C#)
put('B', at(23), CSI_C_B)          # bars 23-24, tenor + bass: the inversus half of the coda
put('A', at(24, 11), T(pick(INV_G), 12, 7)); put('A', at(25), T(nopick(INV_G), 12, 7))  # E3* (G#)
put('B', at(25), CSI_G_B)
put('T', at(25), "D#4:2 E#4:2 F##4:2 G#4:4 E#4:2 D#4:6 B#3:6 G#3:2 A#3:2 B#3:2 C#4:4 D#4:2 G#4:12")
put('S', at(26, 11), pick(INV_C_S)); put('S', at(27), drop_last(nopick(INV_C_S)))  # E4* (C#)
put('A', at(27), CSI_C_A)
put('B', at(27), "R:6 E#3:6 A#2:6 F#2:6 C#3:6 R:6 C#3:6 R:6")
put('T', at(27), "C#4:4 B#3:2 C#4:2 D#4:2 C#4:2 A#3:2 B#3:2 C#4:2 A#3:2 G#3:2 F#3:2 E#3:4")

# The soprano's inversus ends G#-A#-G#: the first beat of Bach's own C#-major subject,
# which therefore carries straight on (BWV 848 guest), while the tenor answers with
# the inversus in stretto, displaced so that its stamps fall on beats 2-3-4.
put('S', at(28, 9), BWV848_REST)
put('S', at(29, 9), "B#5:6")
put('T', at(28, 2), pick(INV_C_T)); put('T', at(28, 3), drop_last(nopick(INV_C_T)))
put('A', at(29), "C#5:6 E#5:6 A#4:6 F#5:6 E#5:4")
put('B', at(29), "A#2:6 E#2:6 B#2:6 G#2:6")

# Episode* (30-31), mirror of Episode 1: the soprano stamps the head up the circle of
# fifths (C# G#7 D#m A#7), alternately inverted (falling) and rectus (rising); the
# tenor's rising runs grow out of the inversus' last note.
put('S', at(30), "G#5:4 G#5:2 E#5:4 E#5:2 D#5:4 D#5:2 F#5:4 F#5:2 "
                 "F#5:4 F#5:2 D#5:4 D#5:2 C##5:4 C##5:2 E#5:4 E#5:2")
put('T', at(30), "G#3:2 A#3:2 B#3:2 C#4:6 D#4:2 E#4:2 F#4:2 G#4:4 F#4:2 "
                 "A#3:2 B#3:2 C#4:2 D#4:6 E#4:2 F##4:2 G#4:2 A#4:6")
put('B', at(30), "C#3:6 E#3:6 G#3:6 B#2:6 D#3:6 F#3:6 A#3:6 C##3:4 A#2:2")

# Stretto rectus + real inversus (32-34): rectus in F# (alto), its real mirror -- which
# turns F# major into D# minor -- in the bass three beats later.
S_F = T(SP, -7, -4)
INV_D_B = T(INV_D, -7, -4)
put('A', at(31, 11), pick(S_F)); put('A', at(32), nopick(S_F))
put('S', at(32), "A#4:4 B4:2 C#5:6 A#5:4 G#5:2 C#5:6")            # CS (F#), first bar
put('S', at(33), "A#4:6 D#5:4 C#5:2 A#4:6 C#5:6 C##5:6 E#5:6 C##5:6 D#5:6")
put('B', at(32), "D#3:6 R:4"); put('B', at(32, 8), pick(INV_D_B)); put('B', at(32, 9), nopick(INV_D_B))
put('T', at(32), "A#3:6 F#4:12 A#3:6 C#4:6 B3:6 A#3:6 F#3:6 A#3:6 C##4:6 A#3:12")
put('A', at(34), "G#4:6 E#4:12 F#4:6")
put('B', at(34, 8), "R:2 D#3:6")

# Dominant pedal (35-36): the bass stamps G#; the hop passes soprano -> tenor; I6/4 - V7.
put('B', at(35), "G#2:4 G#2:2 G#2:4 G#2:2 G#2:4 G#2:2 G#2:4 G#2:2 "
                 "G#2:4 G#2:2 G#2:4 G#2:2 G#2:4 G#2:2 G#2:4")
put('S', at(35), "D#6:4 R:2 D#5:4 E#5:1 F#5:1 G#5:6 B#5:6 G#5:4 A#5:2 B#5:6 C#6:4 B#5:2 D#6:6")
put('A', at(35), "R:6 G#4:6 B#4:6 D#5:6 D#5:6 F#5:6 E#5:6 F#5:6")   # (Nov 2026) rest was F#4
# (Nov 2026) the downbeat was struck G#2 D#4 F#4 D#6 (a hand needed 19+): now the tenor
# steps A#3-B#3 and climbs B#3-D#4 to the hop's F#4, and the alto breathes for the first
# beat, so the pedal opens on V struck G#2 B#3 | D#6; the seventh comes with the hop.
put('T', at(35), "B#3:6 D#4:6 F#4:4 R:2 F#3:4 G#3:1 A#3:1 B#3:6 G#3:12 B#3:6")

# Last entry of Part 2 (37-39): rectus in the bass -- its pickup is the pedal's last
# stamp -- and its real mirror (A# minor reading) in the soprano three beats later.
SB = T(SP, -24, -14)
INV_D_S = invert_diatonic(SB, 'D#4', C_MAJ)
put('B', at(36, 11), pick(SB)); put('B', at(37), nopick(SB))
put('S', at(37), "E#6:6"); put('S', at(37, 9), nopick(INV_D_S))   # (enters on its first stamp)
put('S', at(39, 8), "D#5:6")
put('A', at(37), "E#5:6 G#4:6 B#4:12 G#4:6 F#4:6 E#4:4 G#4:8 F#4:6 G#4:6 A#4:6 B#4:4")
put('T', at(37), "C#4:4 D#4:2 C#4:6 B#3:12 E#4:6 C#4:10 D#4:2 C#4:6 D#4:6 C#4:12 B#3:4")
put('B', at(39), "G#2:6 C#3:12 G#2:6")

# ======================= CODA: the gigue meets its reflection ====================
# 40-41: Part 1's bars 9-10 (soprano CS + alto S) and Part 2's bars 23-24 (tenor S* +
# bass CS*) at once, at pitch: the lower pair is the diatonic mirror of the upper pair
# around E#4, with no time offset.
put('A', at(39, 11), "G#4:2"); put('A', at(40), SUBJ)
put('S', at(40), CS)
put('T', at(39, 11), pick(INV_C_T)); put('T', at(40), nopick(INV_C_T))
put('B', at(40), CSI_C_B)
# 42-44: last stretto -- rectus (soprano) and its real mirror (bass) three beats later.
put('S', at(41, 11), pick(SP)); put('S', at(42), nopick(SP))
put('B', at(42), "A#2:6 B#2:6 C#3:6")                               # bar 9's bass: vi - iii6/4 - I
put('B', at(42, 9), nopick(INV_D))                                   # (enters on its first stamp)
put('A', at(42), "E#4:6 G#4:6 C#5:6 E#4:6 E#4:6 C#5:6 E#4:12 G#4:6 C#5:12 B#4:6")
put('T', at(42), "C#4:6 E#3:12 G#3:6 G#3:6 F#3:6 C#4:4 D#4:2 C#4:6 G#3:18 F#3:6")
# 44-45: cadence -- the soprano's last word over the dominant is Bach's turn
# G#-A#-G#-F#-G#; then everyone stamps the tonic.
put('S', at(44), "D#5:6 E#5:6 G#5:4 A#5:2 G#5:2 F#5:2 G#5:2")
put('B', at(44, 9), "G#2:6")
put('S', at(45), "C#6:4 C#6:2 E#6:4 E#6:2 C#6:6")
put('A', at(45), "E#5:4 E#5:2 G#5:4 G#5:2 G#5:6")
put('T', at(45), "E#3:4 E#3:2 E#3:4 G#3:2 E#3:6")
put('B', at(45), "C#2:4 C#3:2 C#2:4 C#3:2 C#2:6")

NBARS = 45

# Subject entries (voice, bar, offset in quarters, label, bars to emphasise).
ENTRIES = [
    ('Soprano', 1, 0, 'rectus', 2), ('Alto', 3, 0, 'rectus: answer (G#)', 2),
    ('Tenor', 5, 0, 'rectus', 2), ('Bass', 7, 0, 'rectus: answer (G#)', 2),
    ('Alto', 9, 0, 'rectus (coda source)', 2), ('Tenor', 13, 0, 'rectus (A# minor)', 2),
    ('Soprano', 17, 0, 'rectus (G#)', 2),
    ('Bass', 21, 0, 'inversus, real mirror (A# minor)', 2), ('Tenor', 23, 0, 'inversus (coda source)', 2),
    ('Alto', 25, 0, 'inversus (G#)', 2), ('Soprano', 27, 0, 'inversus', 2),
    ('Tenor', 28, 1.5, 'inversus stretto (displaced)', 2), ('Soprano', 28, 3, 'BWV 848 guest', 1),
    ('Alto', 32, 0, 'rectus (F#), stretto', 2), ('Bass', 32, 4.5, 'inversus, real mirror (D# minor), stretto', 2),
    ('Bass', 37, 0, 'rectus', 2), ('Soprano', 37, 4.5, 'inversus, real mirror, stretto', 2),
    ('Alto', 40, 0, 'rectus = bar 9 (reflection)', 2), ('Tenor', 40, 0, 'inversus = bar 23 (reflection)', 2),
    ('Soprano', 42, 0, 'rectus, stretto', 2), ('Bass', 42, 4.5, 'inversus, real mirror, stretto', 2),
]

# Phrase dynamics (velocity offset per bar).
DYN = ([0, 0, 1, 1, 2, 2, 3, 3, 5, 5, -1, 0, 2, 2, 3, 3, 4, 4, 6, 6]           # Part 1
       + [-5, -5, -3, -3, -1, -1, 2, 3, 3, 0, 1, 4, 4, 4, 7, 8, 6, 6, 5]      # Part 2
       + [8, 8, 6, 6, 9, 9])                                                   # coda


def assemble(segs, nbars):
    segs = sorted(segs, key=lambda x: x[0])
    out, u = [], Fraction(0)
    for t, tok in segs:
        t = Fraction(t)
        if t < u:
            raise ValueError(f'overlap at bar {t // BAR + 1}: {tok[:40]}')
        if t > u:
            out.append(f'R:{t - u}')
        out.append(tok)
        u = t + sum(parse_tok(x)[1] for x in tok.split())
    if u < nbars * BAR:
        out.append(f'R:{nbars * BAR - u}')
    return wtclib.concat_bars(' '.join(out), METER)


def build(out=HERE / 'fugue.json'):
    names = {'S': 'Soprano', 'A': 'Alto', 'T': 'Tenor', 'B': 'Bass'}
    bars = {names[k]: assemble(V[k], NBARS) for k in 'SATB'}
    end_q = NBARS * 6
    meta = {
        'title': 'The Well-Tempered clAIvier', 'subtitle': 'III. Fugue in C-sharp major',
        'composer': 'Claude / composed for Sam', 'instrument': 'Piano (four voices)',
        'key': 'C#', 'mode': 'major', 'meter': list(METER), 'bpm': 144,
        'tempo_text': 'Giga a 4, rectus et inversus. Allegro (dotted quarter = 96)',
        # a breath into the reflection (bar 40), a tempo, and a final ritardando
        'tempo_map': [[232.5, 144], [234, 120, 'ramp'], [234, 144], [end_q - 12, 144], [end_q, 108, 'ramp']],
        'character': 'Gigue and its reflection',
        'score_tagline': 'Third edition - Fugue III (see NOTES.md)',
        'markers': [{'t': 0.0, 'label': 'Part 1: rectus'}, {'t': 60.0, 'label': 'Episode'},
                    {'t': 72.0, 'label': 'A# minor'}, {'t': 96.0, 'label': 'G# major'},
                    {'t': 120.0, 'label': 'Part 2: inversus'}, {'t': 165.0, 'label': 'BWV 848'},
                    {'t': 186.0, 'label': 'Stretto rectus/inversus'}, {'t': 204.0, 'label': 'Pedal'},
                    {'t': 234.0, 'label': 'Coda: reflection'}],
    }
    voices = [('Soprano', 'S.', 'treble', 70), ('Alto', 'A.', 'treble', 66),
              ('Tenor', 'T.', 'bass', 66), ('Bass', 'B.', 'bass', 72)]
    entries = [(v, b, Fraction(o).limit_denominator(4), lab, n) for v, b, o, lab, n in ENTRIES]
    data = build_score(out, meta, voices, bars, entries=entries, subject=SUBJ,
                       dynamics=lambda b: DYN[b], tags=[])
    pans = {'Soprano': 74, 'Alto': 66, 'Tenor': 60, 'Bass': 54}
    # The reflection (bars 40-41, with the pickups at the end of 39): bring out the
    # subject and its mirror (alto, tenor), recede the countersubject pair.
    lift = {'Soprano': -4, 'Alto': 8, 'Tenor': 8, 'Bass': -4}
    for v in data['voices']:
        v['piano_pan'] = pans[v['name']]
        for e in v['events']:
            if 39 * 6 - 0.5 <= e['t'] < 41 * 6:
                e['v'] = max(24, min(118, e['v'] + lift[v['name']]))
    Path(out).write_text(json.dumps(data, indent=1))
    return data


if __name__ == '__main__':
    build()
