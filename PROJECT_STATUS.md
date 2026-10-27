# Project status

Updated 27 October 2026.

## Current edition

The third edition lives in `cycle/`, one folder per prelude–fugue pair in
Bach's key order. See the README for the table of pairs and the
[listening room](https://claude.ai/artifact/BBJMS7b46MiEycNBM24yhB).

- **Pairs I–XI** are composed, checked and rendered, and each has had two
  independent bar-by-bar reviews (`REVIEW.md`, `REVIEW-2.md`) with fixes.
  Pairs I, III, VI, VII, IX, X and XI are new; II, IV, V and VIII were
  rebuilt from the October 23 auditions.
- **Fugues XIV (à 15), XV (à 16, with its prelude) and XXIV (à 25)** are
  finished first versions; their independent review is under way. XIV's
  summit is still thinner than fifteen real lines.
- **Being composed:** XII (second pass), XIII, XVI, XVII, XVIII, XIX, XX,
  XXI, XXII, XXIII, and Prelude XXIV. Each pair's concept is in the README
  table and in `cycle/IDEAS.md`.
- **Appendix:** Contrapunctus permutationum, a table canon and a tempo
  canon are finished.

The C-minor pair formerly called "Pair I" is now Pair II, as in Bach's
order, and its fugue has three voices instead of two.

## What was fixed

`cycle/PROBLEMS.md` lists 36 problems in the earlier movements and tools
with their fixes. The most important:

- The many-voice fugues now carry real independent lines; Fugue VIII no
  longer puts four-voice counterpoint on nine staves.
- The "collisions that sound like mistakes" in the 100-bar Fugue VIII were
  measurable: 218 parallel fifths/octaves, 294 accented parallels and 286
  low-register clashes. The new Fugue VIII has 0, 0 and 8.
- The checker missed parallels between crossed voices and on successive
  beats; `tools/critic.py` replaces it and is calibrated on Bach.
- Every movement can now breathe (tempo maps) and is rendered in a historical
  well-temperament (Bach–Lehman 1722 by default).

## Listener feedback still governing the work

From Sam's earlier listening: piano is the primary medium; avoid harmonic
collisions that sound like mistakes, long harmonically static stretches,
excessive length and distance from the WTC's language; the preludes were the
more promising strand (III and VIII especially); many-voice fugues must be
real counterpoint, not harmony.

## Not yet done

- Sam has not heard any third-edition movement. The renders are untested by
  ear; the next step is listening and feedback.
- Pairs XII–XXIII and Prelude XXIV are in progress (see above); the earlier
  versions of those keys exist only in the rejected complete drafts.
- The spatial film remains a goal; `tools/render_spatial.py` renders every
  fugue binaurally as a first step toward its sound.
