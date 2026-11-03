# Project status

Updated 1 November 2026.

## Current edition

The third edition lives in `cycle/`, one folder per prelude–fugue pair in
Bach's key order. See the README for the table of pairs and the
[listening room](https://claude.ai/artifact/BBJMS7b46MiEycNBM24yhB).

- **All 24 fugues and all 24 preludes exist**; every movement is checked,
  rendered and in the listening room.
- **New voice rule (October 2026).** After listening, Sam found the "Fugue N
  has N+1 voices" textures too thick. Each fugue now has at most one voice more
  than Bach's WTC I fugue in the same key (2–6 voices); XX, XXI and XXIV stay
  large because their idea is the crowd. Seventeen fugues (V–XIX, XXII,
  XXIII) were recomposed under the new rule; the earlier versions are kept
  in each pair's `archive-n-plus-1/`.
- **Reviews.** Every recomposed fugue had an independent bar-by-bar review
  (`REVIEW.md` or `REVIEW-3.md`) and a fix round.
- **PR #1 review round (November 2026).** The owner's review found real
  defects, now fixed: the critic merged runs of parallel fifths into a zero
  count and accepted "resolutions" that never came (it now keeps severity,
  verifies each resolution, and has positive controls in
  `tools/test_critic.py`); 56 solo-piano attacks no two hands could strike
  (now 1, kept on purpose in XI); the listening room dropped gates, per-note
  tuning and notes already sounding on seek; the notation lost tempo maps and
  XIX's metres in MusicXML; the binaural renderer clamped rear sources to the
  sides. Musically: XX's summit now chooses its arrival (all 21 on the
  dominant at b46), XXIV is described as a fugue for 25 parts (at most 14
  real lines) and its basses gained a canon rung, and XXIII's B-flat
  statement runs in double time so home comes early. Every pair changed has
  a "Review response (Nov 2026)" section in its NOTES.
- **Appendix:** Contrapunctus permutationum, a table canon and a tempo canon.
  **Extras:** `extras/mobius-fugue/`, a string-quartet fugue for a walking
  listener, with a video of its score folding into a Möbius band.

Start with `cycle/LISTENING_GUIDE.md`.

The C-minor pair formerly called "Pair I" is now Pair II, as in Bach's
order, and its fugue has three voices instead of two.

## What was fixed

`cycle/PROBLEMS.md` lists 36 problems in the earlier movements and tools
with their fixes. The most important:

- The many-voice fugues now carry real independent lines; Fugue VIII no
  longer puts four-voice counterpoint on nine staves.
- The "collisions that sound like mistakes" in the 100-bar Fugue VIII were
  measurable: 218 parallel fifths/octaves, 294 accented parallels and 286
  low-register clashes. The new Fugue VIII has 0, 0 and 0.
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

- Sam has heard some binaural renders (and liked Fugue XX's strings) but
  not yet the recomposed fugues. The renders are untested by ear; listening
  and feedback come next.
- An independent bar-by-bar review of the monument XXI (XX's summit was
  revised in the November review round, XXIV's description and release too).
- Binaural renders of Fugues I–IV and of the preludes.
