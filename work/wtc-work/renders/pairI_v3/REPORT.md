# Pair I (C minor) v3 — report
Files: prelude-i_v3.{mp3,pdf,mid,musicxml,ly,json}, fugue-i_v3.{...}; checks in checks/p3.txt, checks/f3.txt. Prelude 2:01 (31 bars, q=63), fugue 2:01 (34 bars, q=69).
Sources: pairI/prel3.py + build_prelude3.py; pairI/v3/s3.py -> v3/lit.txt -> fug3.py (build.py). Not committed or pushed.
**I cannot hear the audio.** This critique is based on the score and the checkers.

## Prelude v3 — kept 16ths (texture choice)
Sam allowed a change of texture. I kept continuous 16ths because "losing the beat" depends on an even surface that the accents can regroup.
- **Harmonic rhythm is no longer a half-bar grid.** Chord lengths now run 24/8/16/8/4/4 and so on.
  - Long holds: i for 1.5 bars at the start, a whole bar of V at b5, Bb7 for two full bars (b8–9) under groups of three, and F minor for 1.5 bars (b16–17).
  - Acceleration into every cadence: quarter-note changes into Eb (b10–11), into V (b23) and into the final cadence (b29).
- **Clearer groups of five (b13–18).** These now use a five-note voicing spanning a 10th to a 13th, played as a strict rising wave from an accented low note. The groups of three alternate between two rising cells. Over the pedal, the 3/5 mix is 3,5,3,3,5,5. The LH re-strikes the bass only at RH group starts, so the bass reinforces the grouping instead of the barline.
- **Tonal plan:** Cm → (Bb7 pedal) Eb → Eb7, Ab, Fm (via C7/E) → Ger+6 → G pedal → Cm. Then a deceptive Ab (held a bar), N6, a quick cadence, and a close over a tonic pedal (i–iv–vii°7–i). It ends in plain minor.

## Fugue v3
The exposition and Eb entries (b1–10) are kept, with the same subject and the same recurring CS/CSI.
- **E1 (b5–6), new:** a head-motif sequence with dotted and syncopated rhythms in both voices. The lower voice moves in mixed values (quarters, 8ths and 16ths) instead of even 8ths.
- **E2 (b11–12):** the v2 upper line is kept, with a new lower voice in mixed rhythm that turns toward G minor.
- **b13–16, canon per augmentationem (new, Hofstadter-style):** the lower voice plays the subject at half speed from G2 under the subject in normal values in G minor. A free line then climbs to D6 and descends.
- **E3 (b17–18), new:** a falling-fifths sequence from the CS cell, with syncopated 3+1 rhythms, moving from G minor to F minor.
- **b19–24, canon by inversion:** it now spans C4–Db6, about 2 octaves (v2 circled E–Ab). Its rhythm mixes quarters, dotted 8ths and 16ths.
- **b25–26, build (new):** the rhythm speeds up from quarters to 8ths to 16ths over a descending bass (C–Bb–Ab, then F–F#–G), rising to B5 on V.
- **b27–28, PEAK:** the subject at C6, rising to F6, with the inversion entering **a quarter later** in the bass. This is the tightest stretto in the piece, the loudest point (velocity ~96–98), and the highest register.
- **b29:** it peaks at G6 and breaks into a deceptive Ab and then Db (N6). b30 is bariolage on V.
- **b31–32:** the final stretto (S over S at the octave, half a bar apart) over a **tonic pedal C2**.
- **b33–34:** iv–V–i without the pedal, ending in minor on a falling C–G–Eb. No Picardy third.

## Checker flags (open)
- **Fugue:**
  - 8 unprepared beat dissonances. Most are in the build and peak (b25–26 and b29, where the upper line was fitted to the chord plan rather than to my hand-written bass) and at b13.4.
  - 2 parallel 8ves/5ths on the 8th grid at b24, and one at b28.4.
  - A 16th parallel run at b28 (the peak's scale run against the inversion).
  - 5 cross-relations at b24–26 and b29.
- **Prelude:** 6 "unprepared" flags, mostly pedal tones over G2/C2. 6 octave/5th parallels from broken-chord octaves, a handful of par_top flags in the b10–11 acceleration, and no crossings.

## Honest weak spots
- The b25–26 build and the b29 descent were generated against chord labels, not hand-checked against the bass. They may sound rough rather than tense, and they are the first place to hand-edit.
- The peak's quarter-note stretto is dense but short (2 bars). Whether it reads as *the* climax, rather than just loud, needs a listen.
- The prelude's Bb7 hold (b8–9) under groups of three could feel static instead of floating. The groups of five now have a clear contour but still change chords every 8–16 units.
- The augmentation canon's free upper line (b15–16) is auto-filled and may be the most "workmanlike" bar left.
