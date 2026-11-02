#!/usr/bin/env python3
"""Print the sounding pitches of S A T B at every onset in a bar range."""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / 'tools')); sys.path.insert(0, str(HERE))
from critic import Score  # noqa
from chords import pname  # noqa
import source  # noqa
data, tags, rows = source.build()
S = Score(data)
lo, hi = map(int, sys.argv[1].split('-'))
for t in S.onsets:
    b = t // S.bar + 1
    if not lo <= b <= hi:
        continue
    snd = S.sounding(t)
    cells = []
    for i in range(4):
        if i in snd:
            k, att = snd[i]
            cells.append(f"{pname(S.note(i, k)['p'], S.flats):>4}{'*' if att else ' '}")
        else:
            cells.append('   . ')
    mark = '|' if t % S.beat == 0 else ' '
    print(f"{S.loc(t):>9} {mark} {tags[b-1]:4} " + ' '.join(cells))
