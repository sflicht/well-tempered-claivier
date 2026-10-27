"""The four lines of the Contrapunctus permutationum, written by hand.

Two bars of 4/4 in sixteenth units (wtclib tokens), C major and C minor.
draft 1
"""

MAJOR = {
    'A': "Bb4:8 A4:8 C5:8 B4:8",
    'B': "R:4 G4:8 F4:4 E4:4 A4:8 G4:4",
    'C': "C4:2 G4:2 E4:2 C4:2 F4:2 A4:2 B4:2 G4:2 C5:2 G4:2 F#4:2 A4:2 F4:2 D4:2 G4:2 B3:2",
    'D': "E5:1 D5:1 E5:1 C5:1 G5:1 F5:1 E5:1 G5:1 A5:1 G5:1 F5:1 E5:1 F5:1 E5:1 D5:1 C5:1 "
         "E5:1 D5:1 C5:1 B4:1 A4:1 C5:1 E5:1 C5:1 B4:1 C5:1 D5:1 B4:1 F4:1 G4:1 A4:1 B4:1",
}

MINOR = dict(MAJOR)

LINES = {'major': MAJOR, 'minor': MINOR}
