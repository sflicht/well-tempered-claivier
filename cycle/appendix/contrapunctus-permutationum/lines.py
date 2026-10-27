"""The four lines of the Contrapunctus permutationum, written by hand.

Two bars of 4/4 in sixteenth units (wtclib tokens), in C major and C minor.
Every other key is a literal chromatic transposition of one of these two.

A  B-A-C-H in half notes: the motto as a cantus.  Kept chromatically exact in
   both modes (in C minor it reads b7, raised 6, 1, 7: the melodic-minor
   upper tetrachord), so the cipher is literally B-A-C-H in every key.
B  the sigh: enters a beat late, syncopated half notes resolving downward
   (7-6 / 2-3 against the cantus on beats 3 of each bar).
C  the walker: steady eighths, a walking bass that also works as a tune.
D  the spinner: sixteenths for seven beats, landing on a quarter note.

Harmonic frame (major): I7 | vii0/IV | IV | IV6 || I6 | V7/V | V9 | V
No two lines form a perfect fifth or fourth on any quarter beat, so every
pair can invert at the octave without producing a fourth over the bass.
"""

MAJOR = {
    'A': "Bb4:8 A4:8 C5:8 B4:8",
    'B': "R:4 G4:8 F4:4 E4:4 A4:8 G4:4",
    'C': "C3:2 D3:2 E3:2 C3:2 F3:2 G3:2 A3:2 G3:2 E3:2 G3:2 F#3:2 D3:2 B2:2 D3:2 G2:2 B2:2",
    'D': "C5:1 D5:1 E5:1 F5:1 G5:1 Bb5:1 A5:1 G5:1 A5:1 G5:1 F5:1 E5:1 F5:1 E5:1 F5:1 D5:1 "
         "C5:1 D5:1 E5:1 G5:1 A5:1 G5:1 F#5:1 G5:1 F5:1 E5:1 D5:1 F5:1 G5:4",
}

# Modal mapping, written out.  3rd and lower 6th/7th take the minor forms;
# where the cantus forces A-natural (bar 1, beats 3-4: IV in melodic minor) and
# where E is the leading note of that F-major chord, the raised forms stay.
MINOR = {
    'A': "Bb4:8 A4:8 C5:8 B4:8",
    'B': "R:4 G4:8 F4:4 Eb4:4 A4:8 G4:4",
    'C': "C3:2 Eb3:2 Bb2:2 D3:2 F3:2 G3:2 A3:2 G3:2 Eb3:2 G3:2 F#3:2 D3:2 B2:2 D3:2 G2:2 B2:2",
    'D': "C5:1 D5:1 Eb5:1 F5:1 G5:1 Bb5:1 A5:1 G5:1 A5:1 G5:1 F5:1 Eb5:1 F5:1 Eb5:1 F5:1 D5:1 "
         "C5:1 D5:1 Eb5:1 G5:1 A5:1 G5:1 F#5:1 G5:1 F5:1 Eb5:1 D5:1 F5:1 G5:4",
}

LINES = {'major': MAJOR, 'minor': MINOR}
