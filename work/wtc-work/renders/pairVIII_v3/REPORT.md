# Fugue VIII v3 (E-flat minor): polish pass on v2

This is a polish of v2, not a rewrite. The subject, countersubject, form, climax (bars 25–26), Cb-major subito-pp return, tonic-pedal final stretto and Picardy ending are all unchanged. Prelude VIII v1 is copied unchanged.

Files: `fugue-viii_v3.{mp3,pdf,mid,json,musicxml}`, `prelude-viii_v1.*`. The `checks/` folder holds the checker output, the parallel diagnosis, `polish.py` (the edit script) and `polish_log.txt` (every single edit).

## Changes
1. **Tempo:** q=66 Andante maestoso became q=72 Andante con moto.
2. **Thinner texture outside the climax:**
   - At most 4 notes sound together, except in the climax and the final bar.
   - Thematic notes and the bass line are always kept. The free notes that went first were the ones doubling a pitch class already sounding, starting with the lowest.
   - Free bass notes below about D3 that doubled another low voice were removed.
3. **Bars 20–24 thinned:** attacks per bar went from 40/78/34/51/51 to 34/49/22/28/27. During the strettos at most one free voice plays alongside the subject entries.
4. **More air:** free-voice notes a beat or longer are shortened to 75% of their length, leaving small rests. Free voices are also slightly softer (velocity −8), so the themes stand out.
5. **The 18 free-voice parallels fixed:** each flagged spot was fixed by hand, one edit at a time, and checked again after each edit. Each fix moves one free note by 1–5 semitones, or turns it into a rest, keeping whichever option scored best on the checker (see `polish_log.txt`). Thinning had already removed a few of them along the way.
6. **Dissonance faults:**
   - **b19.1:** the countersubject's Db (a 7th over V of Ab minor) used to attack together with the answer's Eb. The countersubject now holds its Eb through the beat, and the Db comes in an 8th later as a passing note.
   - **b23.3:** the bass entry of stretto II (Bb2) used to make a 6/4 against the soprano's Eb. The bass now enters an 8th late, after a rest, and the doubled Gb in the upper voice was dropped.
   - Two other faults turned up while fixing these (b17.3/4, b20.4, b21.4) and were fixed the same way.

## Checker numbers, v2 → v3
| check | v2 | v3 |
|---|---|---|
| parallel 5ths/8ves between free voices | 18 | **0** |
| parallels with one theme voice and one free voice | 16 | **0** |
| parallels inside the climax doublings (intentional) | 16 | 12 |
| unprepared dissonances (both notes attacking) | 11 | 8 (all are the 7ths of the climax's iiø7 and V7 block chords) |
| m2/M7 clashes | 11 | 4 |
| voice crossings | 50 | 27 |
| beats that fit a tertian chord | 67% | 58% |

## Honest critique
- I still can't hear the audio. The "something funny" Sam heard was most likely one of the free-voice parallels, but I can't confirm that by ear.
- The fixes were mechanical: one free note at a time, re-checked with the checker. A semitone shift can leave a passing tone that sounds odd, even when the checker is happy.
- The tertian-fit score went **down** (67% to 58%). This is mostly because thinner beats leave two-note intervals, which the metric doesn't count as full chords. Even so, some beats may now be less clearly defined harmonically.
- Note-shortening is applied to every free note, so it isn't phrased by hand.
- The climax is deliberately as heavy as before, including the octave bass.
