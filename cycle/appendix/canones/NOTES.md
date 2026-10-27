# Canones (appendix)

Bach closed his collections with puzzle canons: the Musical Offering's crab
canon and "Quaerendo invenietis" riddles, the Fourteen Canons BWV 1087 on the
Goldberg ground. This folder holds the cycle's equivalents.

## I. Canon cancrizans per motum contrarium (Tafelkanon), finished

`table_canon.py` → `table-canon.json`, renders in `renders/`.

One line is printed. Player I (Dux) reads it from the near side of the table.
Player II (Comes) reads the same page from the far side: the page turned
through 180 degrees, so the line runs backwards (cancrizans) and upside down
(per motum contrarium). In pitch terms the comes is the retrograde of the dux
mirrored about D4, the one pitch that maps to itself; around D the C-major
collection maps onto itself (C↔E, F↔B, G↔A, D fixed). The canon therefore
begins in A minor and ends in C major. Bach's Musical Offering crab canon is
retrograde only; this one is retrograde and inversion at once.

Sarabande in 3/4, 32 bars (mirror pairs: bar k ↔ bar 33-k):

- 1–8 **Thema**, A minor. The beat-2 notes of bars 1–8 (E A B C A G F E) are
  the retrograde inversion of the Goldberg ground in C, so the comes plays
  that ground the right way round in bars 25–32.
- 9–15 **Double**: sixteenths over the sarabande bass, A minor → D minor.
- 16–17 **Cardo** (the hinge): E4/C#4 → unison D4, the mirror axis → Eb4/C4.
- 18–24 The double rotated: a running bass under the sarabande tune, G → C.
- 25–32 **Fundamentum**: the ground of the Goldberg Variations BWV 988
  (C B A G E F G C) in the comes.

Proof: the build refuses to write the score unless the two-voice score is
note-for-note identical to itself rotated through 180°. An independent check
(retrograde-inversion of the dux about the axis, compared with the comes)
also passes.

Critic: 0 parallels (consecutive, weak and beat-to-beat), 0 unresolved
dissonances, 0 crossings, playable by two hands.

As a riddle it would be printed as a single treble-clef line with a second,
inverted C-clef and key signature at the end of the staff, upside down, and
the inscription "Quaerendo invenietis".

## II. Canon per tempora, not finished

A four-speed tempo canon (one melody at ratios such as 2:3:4:6, all voices
converging on the final cadence) was designed and partly searched
(`tempo_search.py`, `tempo_tools.py`, `tempo_workshop.py`) but the work was
stopped before a score was written. It remains an open idea.

The canon composer could not write these notes itself; they were compiled
from its source docstring and the checks above.
