"""The four lines of the Contrapunctus permutationum, written by hand.

Two bars of 4/4 in sixteenth units (wtclib tokens), C major and C minor.
"""

MAJOR = {
    'A': "Bb4:8 A4:8 C5:8 B4:8",
    'B': "R:4 G4:8 F4:4 E4:4 A4:8 G4:4",
    'C': "C3:2 D3:2 E3:2 C3:2 F3:2 G3:2 A3:2 G3:2 E3:2 C3:2 F#3:2 D3:2 B2:2 D3:2 G2:2 B2:2",
    'D': "E5:1 D5:1 E5:1 F5:1 G5:1 Bb5:1 A5:1 G5:1 A5:1 G5:1 F5:1 E5:1 F5:1 E5:1 D5:1 B4:1 "
         "C5:1 D5:1 E5:1 F#5:1 A5:1 G5:1 F#5:1 E5:1 F5:1 E5:1 D5:1 F5:1 G5:1 F5:1 E5:1 D5:1",
}

MINOR = dict(MAJOR)

LINES = {'major': MAJOR, 'minor': MINOR}
