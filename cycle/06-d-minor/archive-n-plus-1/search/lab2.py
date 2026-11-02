"""Themes as chosen (rhythm search s6/s9, see NOTES) and placement helpers."""
from lab import notes, invert, grid, pair_cost, data_of, analyse, pname
SUBJECT = 'A4:8 Bb4:4 B4:4 C5:2 C#5:2 D5:6 C#5:2 E5:4 D5:12 A5:4'
GROUND = 'D3:16 C#3:8 C3:8 B2:4 Bb2:4 A2:12 Bb2:4 G2:8 A2:24 D2:8'
def subj(start_bar, shift=0, start_beat=1):
    return notes(SUBJECT, (start_bar - 1) * 12 + (start_beat - 1) * 4, shift)
def inv(start_bar, shift=0, start_beat=1):
    # descending form: mirror about A4 -> A4 G#4 G4 F#4 F4 E4 F4 D4 E4 A3
    return [(s, d, p + shift) for s, d, p in invert(notes(SUBJECT, (start_bar - 1) * 12 + (start_beat - 1) * 4), 69)]
def ground(start_bar, shift=0, scale=1):
    return notes(GROUND, (start_bar - 1) * 12, shift, scale)
