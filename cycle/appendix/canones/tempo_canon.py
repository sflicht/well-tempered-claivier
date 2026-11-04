#!/usr/bin/env python3
"""Appendix canon II: Canon per tempora ("Four clocks, one hour").

One melody M sounds at four speeds, 4:3:2:1 (bass slowest, soprano fastest),
each voice an octave apart.  The entries are staggered so that every voice
attacks M's last note at the same instant -- the punctum convergentiae (bar
33), held as a fermata of equal length in all four voices.  Every duration
before that point is exactly proportional.

M begins with the Westminster (Cambridge) Quarters as struck before the hour
(changes 2-5: E G# F# B | E F# G# E | G# E F# B | B F# G# E), so each
entry is audibly another clock starting to chime: the bass at quarter speed
(bar 1, Big Ben), the tenor at bar 9, the alto at bar 17, the soprano at bar
25, each faster than the last.  After the chime, M sings a descending
sequence in the chime's rhythm reversed (q. e e e) whose long notes are the
bass line of bars 9-20 (C# B G# F# E C#), then the bells: two dominant
strikes (B), two tonic strikes (E), a long G#, a flourish that falls to the
leading tone (B G# D#), E -- and the convergence on E.  Because the voices
reach the flourish one after another, the four D# -> E resolutions arrive as
a stretto (bass b31-32, tenor b32.1, alto b32.3, soprano b32.5).

Because the bass sings M at quarter speed, M's later sections become the
pedals under everyone else's earlier material: a dominant pedal (bars 21-24)
under the alto's chime and development, the arrival on the tonic at bar 25
exactly where the fastest clock enters, and a tonic pedal to the end.

M is the authored text (literal).  The voices are produced by explicit
operations from tools/wtclib.py: scale_rhythm(M, r) and transpose by
octaves; their bars are written into the JSON.  tempo_search.py and
tempo_repair.py were used as aids (see NOTES.md); nothing they print enters
the score except through this file.
"""
import json
import sys

from canon_tools import W, HERE
from tempo_tools import derive, BAR

M = ' '.join([
    # Westminster Quarters, the hour sequence (changes 2-5), e e e q.
    'E4:2 G#4:2 F#4:2 B3:6', 'E4:2 F#4:2 G#4:2 E4:6',
    'G#4:2 E4:2 F#4:2 B3:6', 'B3:2 F#4:2 G#4:2 E4:6',
    # Development: the chime's rhythm reversed (q. e e e); long notes
    # C# B G# F# E C# are the bass line of bars 9-20.
    'C#5:6 B4:2 A4:2 G#4:2', 'B4:6 A4:2 G#4:2 F#4:2',
    'G#4:6 F#4:2 E4:2 C#4:2', 'F#4:6 E4:2 D#4:2 E4:2',
    'E4:6 F#4:2 E4:2 B4:2', 'C#5:6 B4:2 F#4:2 G#4:2',
    # The bells: two dominant strikes, two tonic strikes, the long third,
    # a flourish falling to the leading tone, and E.
    'B3:12 B3:12', 'E4:12 E4:12', 'G#4:12 B4:2 G#4:2 D#4:2 E4:6',
    # Punctum convergentiae (fermata, all voices together).
    'E4:1',
])

# (name, abbr, clef, ratio, semitones, letters)
VOICES = [('Bass: Big Ben (x4)', 'B', 'bass', 4, -24, -14),
          ('Tenor (x3)', 'T', 'bass', 3, -12, -7),
          ('Alto (x2)', 'A', 'treble', 2, 0, 0),
          ('Soprano (x1)', 'S', 'treble', 1, 12, 7)]
FERMATA = 24  # sixteenths: the final note, held equally by all


def dynamics(b):
    """Phrase shaping by bar index (0-based): each entry lifts the level."""
    if b < 8:
        return -4
    if b < 16:
        return -2 + (b - 8) // 4
    if b < 24:
        return 0 + (b - 16) // 3
    if b < 32:
        return 3 + (b - 24) // 2
    return 4


def build(out=HERE / 'tempo-canon.json'):
    bars, T, streams = derive(M, VOICES, fermata=FERMATA)
    nb = int(T // BAR)
    meta = {
        'title': 'The Well-Tempered clAIvier',
        'subtitle': 'Appendix: Canones. II. Canon per tempora (Four clocks, one hour)',
        'composer': 'Claude / Sam. Melody begins with the Westminster Quarters (Cambridge, 1793)',
        'instrument': 'Player piano or piano four hands (two players): one melody at four speeds '
                      '(4:3:2:1), converging',
        'score_tagline': 'All four voices attack the last note together: the punctum convergentiae',
        'key': 'E', 'mode': 'major', 'meter': [6, 4], 'bpm': 96,
        'tempo_text': 'Tempo giusto: one pulse, four clocks',
        'markers': [{'t': 0, 'label': 'Big Ben (x4)'}, {'t': 8 * 6, 'label': 'Tenor clock (x3)'},
                    {'t': 16 * 6, 'label': 'Alto clock (x2)'}, {'t': 24 * 6, 'label': 'Little clock (x1)'},
                    {'t': nb * 6, 'label': 'Punctum convergentiae'}],
    }
    # score order top-down (soprano first); dynamics weight the big clock
    voices = [(n, a, c, vel) for (n, a, c, *_), vel in reversed(list(zip(VOICES, (80, 74, 72, 70))))]
    entries = [(VOICES[0][0], 1, 0, 'Westminster Quarters, x4', 8),
               (VOICES[1][0], 9, 0, 'Westminster Quarters, x3', 6),
               (VOICES[2][0], 17, 0, 'Westminster Quarters, x2', 4),
               (VOICES[3][0], 25, 0, 'Westminster Quarters, x1', 2)]
    sizes = {len(v) for v in bars.values()}
    assert len(sizes) == 1, sizes
    W.build_score(out, meta, voices, {v[0]: bars[v[0]] for v in voices},
                  entries=entries, dynamics=dynamics,
                  tags=['bass solo'] * 8 + ['+tenor'] * 8 + ['+alto'] * 8 + ['+soprano'] * 8 + ['convergence'],
                  extra={'canon': {'kind': 'mensuration / tempo canon', 'ratios': [4, 3, 2, 1],
                                   'melody': M, 'convergence_t_quarters': float(T) / 4,
                                   'fermata_sixteenths': FERMATA}})
    mark_fermata(out)
    return bars, T


def mark_fermata(path):
    """Post-process: the shared final note of every voice carries a fermata."""
    data = json.loads(path.read_text())
    for v in data['voices']:
        last = max((e for e in v['events'] if e.get('p') is not None), key=lambda e: float(e['t']))
        last['fermata'] = True
    path.write_text(json.dumps(data, indent=1))


if __name__ == '__main__' and '--no-write' not in sys.argv:
    bars, T = build()
    print('wrote', HERE / 'tempo-canon.json', '| convergence at bar', int(T // BAR) + 1)
