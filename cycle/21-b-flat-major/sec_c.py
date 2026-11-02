"""Fugue XXI, section C ("I forestieri"): the strangers, bars 22-31.

Five strangers arrive one after another, each with the head of Bach's own subject in a key a fifth
lower than the last (B-flat, E-flat, A-flat, D-flat, G-flat).  Where Bach writes four repeated
sixths (G4 G4 G4 G4 in B-flat), a natural horn has no note; each stranger's horn cracks to its
seventh partial instead -- a minor seventh 31 cents flat -- and the cracked note turns the key
into a dominant seventh, which pulls the music one step further round the circle of fifths.
The friends laugh at each crack.  After cracking, each stranger takes over the countersubject
(it begins by resolving the cracked seventh) for the next stranger.  The last crack (F-flat in
G-flat) is an augmented sixth that lands on the dominant of B-flat (bar 32).
Each two-bar unit is the previous one transposed (an explicit sequence), with the roles passing
from voice to voice; the voices that do not change role are written afresh.
"""
from xxi import *  # noqa

CRACK = -31.17   # the seventh partial against the tempered minor seventh

# unit in B-flat (bars u1-u2):  I | V6 | vi7 | V || I | I | I7/3 | I7/3
HEAD = ("Bb3:4 R:2 Bb3:1 Bb3:1 F4:2 F4:2 F4:2 F4:2 "
        "D4:2 Bb3:2 Bb3:2 Bb3:1 Bb3:1 Ab4:2 Ab4:2 Ab4:2 Ab4:2")      # Bach's head, G4 cracked to Ab4
CS = "D4:4 C4:4 Bb3:4 C4:4 Bb3:4 D4:4 F4:8"                            # begins by resolving the last crack
BASS = "Bb2:4 A2:4 G2:4 F2:4 Bb2:8 D3:8"
SOP = "F5:4 F5:4 G5:4 A5:4 Bb5:4 F5:4 R:8"
INNER = "Bb4:4 C5:4 D5:4 Eb5:4 D5:8 Bb4:8"
HORN = "R:12 F5:2 F6:1 F5:1"                                   # the posthorn shows how
LAUGH = "R:8 R:8 R:8 Bb5:1 R:1 F5:1 R:1 Bb5:1 R:1 F5:1 R:1"


ROLE = {'HEAD': HEAD, 'CS': CS, 'BASS': BASS, 'SOP': SOP, 'INNER': INNER, 'HORN': HORN, 'LAUGH': LAUGH}
KEYS = [('B-flat', 0, 0), ('E-flat', 5, 3), ('A-flat', -2, -1), ('D-flat', 3, 2), ('G-flat', -4, -2),
        ('F', 7, 4), ('B-flat', 0, 0)]
# roles of each unit: role -> (partial of the voice, octave shift)
CAST = [
    {'HEAD': (7, 0), 'CS': (5, 0), 'BASS': (2, 0), 'SOP': (20, 0), 'INNER': (9, 0), 'HORN': (16, 0), 'LAUGH': (10, 0)},
    {'HEAD': (19, 1), 'CS': (7, 0), 'BASS': (2, 0), 'SOP': (20, 0), 'HORN': (8, -1), 'LAUGH': (15, -1)},
    {'HEAD': (13, 1), 'CS': (19, 2), 'BASS': (2, 0), 'SOP': (10, 0), 'HORN': (12, 0), 'LAUGH': (20, 0),
     'INNER': (5, -1)},
    {'HEAD': (17, 1), 'CS': (13, 1), 'BASS': (2, 0), 'SOP': (20, 0), 'HORN': (16, -1), 'LAUGH': (15, -1),
     'INNER': (6, -1)},
    {'HEAD': (11, 1), 'CS': (17, 2), 'BASS': (2, 0), 'SOP': (10, 0), 'HORN': (9, 0), 'LAUGH': (15, 0),
     'INNER': (3, -1)},
    {'HEAD': (21, 1), 'CS': (13, 1), 'BASS': (2, -1), 'SOP': (10, -1), 'HORN': (9, -1), 'LAUGH': (20, -1),
     'INNER': (6, -1)},
    {'HEAD': (14, 1), 'CS': (21, 2), 'BASS': (2, 0), 'SOP': (20, 0), 'HORN': (16, 0), 'LAUGH': (10, 0),
     'INNER': (4, -1)},
]
# the bass's last two beats of each unit, re-octaved so that the line keeps its register
# (an octave shift keeps every interval class, so the unit's counterpoint is unchanged);
# in G-flat the bass stays on G-flat under the cracked F-flat: the augmented sixth.
BASS_END = ['Bb2:8 D3:8', 'Eb3:8 G2:8', 'Ab2:8 C3:8', 'Db3:8 F2:8', 'Gb2:16', 'F2:8 A2:8', 'Bb2:8 D3:8']


def unit(sc, bar, k):
    name, semis, letters = KEYS[k]
    for role, (n, o) in CAST[k].items():
        toks = W.transpose(ROLE[role], semis + 12 * o, letters + 7 * o)
        if role == 'BASS':
            toks = ' '.join(toks.split()[:4]) + ' ' + BASS_END[k]
        if role == 'CS' and name == 'G-flat':
            # no D-flat in the augmented sixth (its resolution would move in fifths with G-flat)
            toks = toks.replace('Db6:8', 'R:8')
        if role == 'HEAD':
            sc.theme(V(n), bar, 1, toks, f"Bach's head in {name}; the sixth cracks to the 7th partial", 2)
            for beat in (3, 3.5, 4, 4.5):
                sc.tune(V(n), bar + 1, beat, CRACK)
        else:
            sc.put(V(n), bar, 1, toks)


def place(sc, b0=22):
    b = lambda k: b0 + k - 1  # noqa: E731
    for k in range(len(CAST)):
        unit(sc, b(1 + 2 * k), k)
    # ---- free voices (written for each unit; they accumulate as the strangers stay)
    # B-flat -> E-flat: Amico 5 (after its countersubject) and Corno 12
    sc.put(V(5), b(3), 1, "Eb4:4 Bb3:4 Eb4:4 D4:4 G3:4 Bb3:4 Bb3:8")
    sc.put(V(12), b(3), 2, "Bb4:2 Bb4:1 Bb4:1 R:8 Bb4:2 Bb4:1 Bb4:1 Bb4:4")      # tonguing on the dominant
    # E-flat -> A-flat: Forestiero 7 (after its countersubject), a chain of suspensions
    sc.put(V(7), b(5), 1, "C5:6 Bb4:4 Ab4:4 G4:2 Eb4:4 Ab3:4 Eb4:8")
    # A-flat -> D-flat: Forestiero 7 walks in the tenor
    sc.put(V(7), b(7), 1, "Ab3:8 Db4:4 Ab3:4 Ab3:8 Db4:8")
    # D-flat -> G-flat: Forestiero 13 (after its countersubject) suspends high, Forestiero 7 below
    sc.put(V(13), b(9), 1, "Db6:6 Cb6:4 Bb5:4 Ab5:2 Bb5:4 Db6:4 Bb5:8")
    sc.put(V(7), b(9), 1, "Db4:16")                             # it holds the dominant
    # G-flat -> F: the augmented sixth resolves, the strangers land on the dominant and listen
    sc.put(V(11), b(11), 1, "F5:2")
    sc.put(V(17), b(11), 1, "C6:6 Bb5:4 A5:4 G5:2")                  # Forestiero 17 suspends
    # F -> B-flat: Forestiero 11 takes up the chain of suspensions
    sc.put(V(11), b(13), 1, "D5:6 C5:4 Bb4:4 A4:2 F4:16")
