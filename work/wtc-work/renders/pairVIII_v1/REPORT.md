# Pair VIII (E-flat minor) v1: report

Files: prelude-viii_v1.{mp3,pdf,mid,musicxml,ly,json} and fugue-viii_v1.{...}. Checker output is in checks/p1.txt, checks/f1.txt and checks/f1_thematic_pairs.txt.
Sources are in pairVIII/: motifs.py (the subject, inversion and countersubject), fugue.py (the hand-written entry plan), engine.py (works out the harmony and fills the free voices), build_fugue.py and prelude.py. Prelude 1:23, fugue 1:31, both about −22 dB mean. Nothing is committed or pushed.
**I cannot hear the audio.** Everything below comes from the score and the checkers.

## Key
Pairs IV (C# minor) and V (D major) follow Bach's WTC numbering, so No. 8 is Bach's D#/E-flat minor. I wrote it in E-flat minor (six flats). Pair I's C minor doesn't fit that pattern, so the cycle's key plan is worth pinning down at some point.

## Prelude v1: French overture (16 bars, q=48, "Grave, pointé")
Following Sam's update, there are no running 16ths. The texture is five-part (Dessus, Haute-contre, Taille, Quinte, Basse), with double-dotted chords re-struck in dotted-eighth plus sixteenth patterns and 32nd-note tirades rushing into the cadences (b4, b8, b15). That's a deliberate contrast with Pair I's broken-chord 16ths and the IV/V textures.
- b1–4: i, then iv, V, VI, iiø7 and V. The harmony changes every half bar, apart from the opening whole bar.
- b5–8: Db7, then Gb major, the relative major, which arrives quietly over a held bar.
- b9–12: a circle through Cb, Ab minor, F7, Bb minor, Eb7, Ab minor, Cb and iiø7.
- b13: the harmonic rhythm tightens to quarters (i6/4, V7, VI). b14 is a deceptive VI, then iv6.
- b15–16: V and V7 with a falling tirade, then a **half cadence on V, held, leading straight into the fugue** without stopping. The prelude doesn't close in the tonic, so the fugue completes it.
- Allusion: the top line opens Eb–Gb–F–Eb (1–♭3–2–1) in dotted rhythm. The fugue subject shares that cell, but in 16ths in the middle of its first beat group. The pitch cell is shared, the rhythm and context are not.

## Fugue v1 (nine real voices, 22 bars, q=60, "Grave e pieno")
- Subject (1 bar, BWV 874-short): `Eb(q) Gb F Eb (8th+16ths) D Eb F Bb↓ (8ths)`, i to V. Inversion: `Eb C Db Eb F Eb Db Ab`. There are major-mode versions and heads (the first two beats) for fragments.
- Countersubject (1 bar, 8ths and 16ths, starting off the beat): `– Bb | Eb | Bb Ab F Eb D`. It recurs throughout, in about 13 statements.
- Voices: S1, S2, A1, A2, T1, T2, Baritone, B1, B2.
- b1–7: exposition. All nine enter in middle-out order (T1, A2, T2, A1, Bar, S2, B1, S1, B2), alternating subject and real answer. Entries come every bar at first. From b5 the entries speed up: each new subject is chased **one beat later** by the inversion at the 5th.
- b8: the only episode, one bar of quarter-staggered subject and inversion heads, modulating to Gb.
- b9–10: in Gb major, a stretto at **one beat at the 5th** (major subject), plus the major inversion.
- b11–12: in Ab minor, subject and inversion at one beat.
- b13–14: the build-up. A rising chain of entries every **half bar**, each a 5th higher (Ab, Eb, Bb, F), in climbing register.
- **b15–16: the peak.** The subject at the top (S1 up to G#6/Ab6, the highest point of the piece) with the inversion one beat later, all nine voices sounding, densest attacks (40/41 per bar), ff.
- b17–18: the release. It drops to about four voices, piano, over a dominant pedal (Bb2), with subject and inversion still overlapping.
- b19–21: **a tonic pedal (Eb2) with a final stretto** (subject plus inversion at one beat, then heads at one beat), all nine voices, crescendo.
- b22: the ending is a **plain nine-voice E-flat minor chord**, the full chord in open spacing, with no Picardy third. The pedal comes before the final bar instead of being the ending itself.

## Checker flags (honest)
- **Fugue:**
  - 36 m2/M7 clashes on attacks;
  - about 18 parallel 5ths/8ves on the 8th grid (19 on the 16th grid);
  - 96 grid "voice crossings", which is unavoidable with nine voices in a keyboard range (the voices share registers heavily);
  - 125 cross-relations;
  - only 61% of beats fit a plain tertian chord.
  - Many of the parallel 5ths are built in: the subject against its inversion at one beat, with the inversion a 5th *below*, makes D/G→Eb/Ab. That needs octave re-placement or a small change to the inversion.
  - The unprepared beat dissonances cluster in b10–16 and b19–21, the densest stretti, and are listed in checks/f1.txt.
- **Prelude:**
  - 93.8% tertian fit;
  - 17 attacked dissonances, mostly chord 7ths (Db7, iiø7, V7) struck as part of the chord, which is idiomatic;
  - 7 octave/5th parallels, caused by the melody moving inside a held chord;
  - no crossings.

## Honest weak spots
- **Free voices are machine-filled.** The planner places every subject, inversion and CS statement by hand. The leftover voices are filled with mostly held chord tones from a harmony the engine infers beat by beat. So the claim that "nearly every note is thematic" is only partly true. In the dense sections, maybe half the notes are thematic, and the rest is sustained padding that may sound like organ chords rather than lines.
- The counterpoint is noticeably rougher than Pairs I and V. The clash and parallel counts above are too high for a Bach-like fugue. A v2 needs a pass by hand on b9–21.
- Nine voices on one piano give a thick, muddy middle register. The score is hard to read (nine staves), and the voice identities won't come across by ear.
- The tempo was picked to avoid plodding, but the subject's first beat is a quarter note in every entry, so the rhythmic profile may feel samey after 20 entries. The only rhythmic contrast comes from the stretto overlap.
- The peak (b15–16) works on paper: highest register, densest texture, all nine voices, then a real thinning at b17. Whether it lands, I can't hear.
- Prelude: the inner voices are re-struck in the same dotted pattern throughout, so it could get stiff. The tirades are the only quick motion.
