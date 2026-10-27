# Pair IV in C-sharp minor: third edition

Sources, with every note written by hand:
- `prelude.py` builds `prelude.json` (3/4, 38 bars, "Allegro inquieto", quarter = 100, about 68 s).
- `fugue.py` builds `fugue.json` (3/4, 50 bars, five voices S A T Br B, "Moderato, sostenuto",
  quarter = 72, about 125 s).

Renders are in `renders/`: the PDF, MIDI, MusicXML, LilyPond and MP3 in Bach-Lehman
temperament, plus `*-equal.mp3` in equal temperament.

This edition was rebuilt from Prelude v6 and Fugue v7 following `REVIEW.md`, whose problem
numbers are used below. Nothing has been auditioned. The notes below describe the written
music and the checks. They are not claims about how it sounds.

**Borrowed material, credited.** The second subject of the fugue, called the *crux* here, is
J. S. Bach's first subject of WTC I, Fugue in C-sharp minor BWV 849: C#-B#-E-D#. It is also
planted in the prelude, bars 19-20. Both JSON scores carry this credit in `metadata.credits`.
`fugue.json` also lists every crux statement under `second_subject`.

## Checks before and after

`tools/critic.py`. The calibration is in `cycle/CONVENTIONS.md`.

| metric | Fugue v7 | **Fugue (3rd ed.)** | Prelude v6 | **Prelude (3rd ed.)** |
|---|---|---|---|---|
| parallels_error | 0 | **0** | 0 | **0** |
| parallels_weak | 0 | **0** | 0 | **0** |
| beat_parallels | 22 | **1** | 1 | **0** |
| pc_tripled_on_beats_pct | 19.4 | **8.0** | 0 | **0** |
| low_register_seconds | 8 | **9** | 0 | **0** |
| dissonance_unresolved | 2 | **0** | 1 | **0** |
| crossings | 0 | **0** | 0 | **0** |
| keyboard_unplayable_pct | 30.3 | **15.8** | 0 | **0** |
| bar where all 5 voices first sound | 33 | **10** | n/a | n/a |
| onset slots with 3+ simultaneous attacks | 41.4 % | **35.8 %** (BWV 849: 22.4 %) | n/a | n/a |
| bars | 56 | 50 | 38 | 38 |

How these numbers were taken:
- **Keyboard.** 42 of the fugue's 50 unplayable onsets become playable if the held bass note
  (the augmented crux or a pedal) is sustained with the sostenuto pedal. With that pedal, 2.5 %
  of onsets remain unplayable. BWV 849 has 0 %.
- **Simultaneous attacks.** This and the "first five-voice bar" row come from ad-hoc scripts
  run the same way on v7 and on the BWV 849 reference data.
- **Voices sounding per bar** (new fugue):
  `1 1 2 2 3 3 4 4 4 5 5 5 4 4 4 4 4 3 3 4 4 4 4 4 5 5 4 4 4 4 4 4 4 4 4 4 5 5 5 5 5 5 5 4 4 5 5 5 5 5`.
- **Theme check.** Every subject entry the critic verifies matches the subject 9/9 in
  intervals and rhythm, with three intentional exceptions:
  - the E-major modal entry (7/9);
  - the in-key stretto voice at bar 30 (5/9);
  - the dominant form with B# for B (7/9).

## Form map: Fugue

| bars | what happens |
|---|---|
| 1-11 | **Exposition**, descending order S (C#m) - A (answer, G#m) - T - Br (answer) - B. Each voice that has just stated the theme carries the fixed countersubject (CS) directly above the next entry. The texture grows 1-2-3-4-5 and nobody drops out. The bass enters at bar 10 against four voices. |
| 9 | Link: the bass line steps G#-F#-A so that the bass entry (G#) continues it. |
| 12 | Codetta i - VI - V7 of III. |
| 13-14 | Subject in **E major, modal**. The minor sixth C natural keeps the diminished seventh (C-A-F#-D#). CS above, mapped into the mode. Lament bass E-D-C \| A-F#-B-E. |
| 15-16 | Episode 1: the head of the subject in half-bar sequence (E - A \| D#o7 - G#7), so the harmonic rhythm runs in dotted quarters against 3/4. |
| 17-25 | **Crux exposition (double fugue)**, quiet, in stile antico bar-long notes: T (C#m, 17-19), A (G#m, using Bach's own answer G#-F##-B-A#, 20-22), S (C#m, 23-25). The S opens with the CS's first bar against the first crux statement. There is running counterpoint in S (21-22) and T (23-25). Br enters on the leading tone E# (25). |
| 26-27 | Subject in **F# minor** (T) + CS (A) + lament bass F#-E-D \| B-G#-C#-F#. |
| 28-29 | Episode 2: the head in S over a bass that sings the crux in diminution (F#-E#-A-G#, then G#-F##-B-A#), sequenced up a step. |
| 30-32 | Answer in **G# minor** in the bass (Br) with a stretto two beats later in A, a fifth higher, in key (stretto_finder cost 7, its best rectus placement). It ends on D# (half cadence in G#m). |
| 33-34 | Episode 3: head imitation S/T over the crux in diminution in the bass (C#-B#-E-D#). The S leaps the crux's own interval B#-E into the climax. |
| 35-41 | **Climax.** The crux augmented in the bass, exactly double its bar-17 values: C# (2 bars), B#, E, D# (2 bars), C#. Above it are two complete strettos of the subject an eighth apart: T + A (35-36) with the CS in S, and Br + S (38-39) with the CS in T. The subject's E-major-seventh head bar lands on the crux's E (38), and its diminished-seventh bar on the crux's D# (39), where the S reaches A5. The S peaks on C#6 as the crux resolves (41). |
| 42-43 | iv - Neapolitan sixth (S falls in dotted rhythm while A rises), then viio7 of V. The bass rises chromatically F#-F##-G#. |
| 44-46 | **Dominant pedal** on G#1: the subject in its dominant form (B# for B), complete, in S, A (an eighth later) and T (a quarter later). This combination was tested before writing: 0 parallels, 0 unresolved. |
| 47-50 | **Tonic pedal coda** on C#2: the crux in S (i - iv6/4 - i \| viio7 - i \| iio4/2 - V7 \| I). The Picardy third arrives late: the alto's held F# falls to E# on beat 2 of the last bar. |

## Form map: Prelude

| bars | what happens |
|---|---|
| 1-4 | Motif M twice over C#m (kept from v6). |
| 5-6 | **Imitation**: the L.H. states M in the tenor. The R.H. rests, then answers on the "and" of beat 2, on the dominant (B#-G#-A-B#-D#-C#-B#-A; stretto_finder cost 2, roughness 0.40, 0 parallels). V-i in root position at 6.2.5. |
| 7-8 | M on V, then i, then a B7 pivot (kept). |
| 9-14 | E major: M (9), imitation with the L.H. leading (10-11), a walking-eighths L.H. (12-13), and a 4-3 over B (13). |
| 15-18 | A major M (15); **imitation in F#m** (16-17) answering on C#7 and then turning to D (VI of F#m, the Neapolitan of C#m); B major M (18). |
| 19-22 | **Dominant pedal that moves.** Bars 19-20: the R.H. sings the **crux**, C#-B# (a 4-3 over G#) then E-D# (6-5, over i6/4 then V7). The harmony changes every half bar: V7sus4-V7 \| i6/4-V7 \| Vb9-V7 (with the held F#5, bar 21) \| the diminution "drop" i6/4-V-V7 (22). |
| 23-26 | Flurry, the L.H. hemiola (24-25), V7 approach (kept). |
| 27-29 | **Return on root-position i**: bar 1's left hand comes back. Then M on V; the tenor M (29) now has a bass and C#m figuration above it. |
| 30-33 | Neapolitan sixth - French sixth (F## in the R.H. only) - cadential 6/4 - V7 - **i in root position at 33** (the structural cadence), then M with its rising tail. |
| 34-35 | **Lament bass** in quarters: A-G#-G \| F#-E#-E (VI - III6 - C#o/G \| N6 - V/iv - i6). |
| 36-38 | M on V7 - i (37) - the closing tetrachord G#-F#-E-D# over i - iv6 - V7 (6-5 on beat 3) - **final V7-i in root position** (37-38). |

**Pair contrast (problem 13).** The prelude stays in 3/4 because its motif and hemiola are
built in sixteenths of 3/4. The two movements now differ in pace and character instead:
- The prelude is two-voice, sixteenth-note *Allegro inquieto* at quarter = 100.
- The fugue is five-voice *Moderato, sostenuto* at quarter = 72, with suspensions, a stile-antico
  second subject and pedal points.

This follows the slow five-voice character of Bach's C-sharp minor fugue and keeps the
five-voice texture readable.

## Review problems and what changed

1. **The exposition thinned out.** Entries are now in descending order with the CS carried by
   the previous voice, so voices accumulate. All five voices sound from bar 10 to bar 12. After
   the exposition the texture is mostly four voices; it drops to three only in the quiet crux
   exposition (18-19).
   - Deviation from my own preserve list: the v7 order T-A-S-Br-B could not carry a CS that
     sits above the subject (see weak spots).
2. **The CS had no fixed pitches.** It is now one pitch shape:
   `E5:6 D#5 B4 C#5 B4 A4 B4 | C#5:6 B#4:2 D#5:2 E5:2`.
   - Its held E is a 4-3 suspension over the subject's B.
   - Its sixteenths run while the subject holds F#.
   - It holds while the subject moves in eighths.

   It sounds above the subject or answer at 3, 5, 7, 10, 26, 35 and 38, mapped modally at 13.
   Its first bar is also the counterpoint to the first crux statement (17).
3. **Collisions and voice leading.**
   - beat_parallels 22 → 1; tripling 19.4 % → 8.0 %.
   - No simultaneous doubled leading tones in either movement (checked for B#, E# and F##).
   - No unresolved dissonances.
   - The final V7 has its leading tone, and the seventh resolves to the Picardy third.
4. **Entries sat on E major.** Upper-voice entries now sit on the lament bass
   (i - VII - iv6 \| iv - iio7 - V - i): bars 13 (in E) and 26 (in F#m). Over the climax the
   subject's E-major head bar is placed deliberately on the crux's E (38). Subject endings
   now land on a tonic: 6.3.5 (C#m), 11.3.5, 27.3.5 (F#m), 36.3.5 (over the tonic pedal).
5. **Spacing and playability.** Unplayable onsets 30.3 % → 15.8 % (2.5 % with a sustained
   bass). Upper-voice gaps wider than an octave: S-A on 14/150 beats (v7: 37/168), A-T on 29/150
   (v7: 40/168).
6. **The climax was not an event.**
   - The bass augmentation is now exact: the crux at double the values of its own bar-17
     statement.
   - Both strettos above it are complete.
   - The fixed CS rides each pair.
   - The highest notes are thematic: A5 is the subject's own high note on the diminished
     seventh (39), and C#6 coincides with the crux's resolution (41).
7. **Prelude cadences** (prelude bars). The return is now on root C#3 (27.1). The cadential 6/4
   now goes to V7 and on to i at 33.1. The ending has V7-i in root position at 36-37 and 37-38.
   There is also a root-position V-i at 6.2.5.
8. **Timid strettos.** There are now five complete strettos:
   - 30-31: two beats apart, at the fifth, in key;
   - 35-36 and 38-39: an eighth apart;
   - 44-46: three voices an eighth and a quarter apart over the dominant pedal.

   None stops after the head. Bar 40, the old dominant without B#, no longer exists; the climax
   reaches V through iio7 (40).
9. **Static chord bars and filler voices.**
   - The whole-bar chord arpeggios of v7 bars 12, 17, 30, 38 and 40 are gone.
   - The crux exposition got running counterpoint (21-25).
   - Onsets with three or more simultaneous attacks fell from 41.4 % to 35.8 %.
10. **The ending.** There is no longer a block-chord ending with a doubled leading tone. The
    coda states the crux over the tonic pedal, and the resolutions are staggered (the alto's
    F#→E# arrives after the others).
11. **Generic episodes.** All three episodes are built from the subject's head and the crux in
    diminution in the bass. Episode 1 runs in a dotted-quarter harmonic rhythm.
12. **The tonal plan.** The middle entries are E major (modal), F# minor (once), G# minor (as a
    stretto), then the Neapolitan region before the dominant pedal.
13. **Pair contrast.** Tempo and character now differ (see above).
14. **Doubled F##** (prelude bar 31). The L.H. no longer plays F##; only the R.H. has the
    augmented sixth.
15. **Frozen dominant pedal** (prelude 19-22). The harmony now moves every half bar, and the
    crux sounds as 4-3 and 6-5 suspensions.
16. **Alberti texture and the motif at every barline.**
    - Half-bar imitations between the hands in 5-6, 10-11 and 16-17. The R.H. rests at the start
      of 5, 10 and 16.
    - The L.H. is rewritten as walking or compound lines in 6, 11-13, 17, 19-22, 34-35 and 37.
17. **The mechanical falling-thirds chain** (15-18) is broken at 16-17 by the imitation and the
    turn from C#7 to D.
18. **The lament bass** now runs in real-bass quarters over two bars (34-35).
19. **Hand-switch bars.** Bars 5, 10 and 16 became imitations. Bar 29 keeps the tenor M, now
    from E3, with C#m figuration above it (no A against the motif's G#).
20. **B# cancelled by B natural at the final tonic.** The tonic arrival is now 37.1 with
    `C#3 E3 G#3 E3` in the L.H., and it carries no B natural.

## Devices
- **Fugue:**
  - fixed countersubject over a lament-bass harmonisation;
  - modal (E major, minor-sixth) transformation of the subject;
  - real answer, and an in-key answer used for the stretto at the fifth;
  - strettos at two beats, an eighth and a quarter;
  - Bach's crux (BWV 849) as a genuine second subject in normal values, with Bach's answer, in
    diminution (episode basses) and in augmentation (climax bass);
  - the double-fugue combination of crux and subject;
  - dominant and tonic pedals, Neapolitan sixth, Picardy third by suspension.
- **Prelude:**
  - imitation at the half-bar on the dominant;
  - M in augmentation (now also sounding the crux) and in diminution;
  - L.H. hemiola;
  - Neapolitan → French sixth → cadential 6/4;
  - passus duriusculus lament bass.

## Honest weak spots
- **Unheard.** The audio renders were made but not listened to. Nothing here says how the
  music sounds.
- **The CS is not in every entry.** It is modally altered in E major (bar 13: G#-F#-D-E-D-C-D),
  and it is absent from the G#m stretto (30-31) and the pedal stretto (44-46). Strict octave
  invertibility was not achieved: the CS works above the subject. Below the subject it works
  only at the double octave with a real bass under it, which the score never uses.
- **The entry order changed** from v7's T-A-S-Br-B to S-A-T-Br-B. The S's first CS note is
  reached by a rising seventh (C#5 → B5, bars 2-3).
- **E-major colour remains where the subject is the bass.** At 5-6 (T), 7-8 (Br), 10-11 (B)
  and 30-31 (Br), its head is still heard over E/G# or B/D#. The lament harmonisation only
  applies where a free bass exists (13, 26).
- **One subject note is altered.** The alto's final C# at 37.1 is split into C#-D# sixteenths so
  that it passes over the crux's B# (the "unresolved spot" named in the review).
- **The remaining beat parallel** (45.2, A/T octaves) is built into the octave canon at an
  eighth over the pedal. Every tested alternative produced unresolved dissonances.
- **Low-register seconds** are 9, the top of Bach's 3-9 range. They are mostly in the climax,
  where the crux bass lies under the tenor's subject.
- **Tripled roots at three cadences** (41.1, 47.1, 50.1).
- **Still more homorhythmic than Bach:** 35.8 % against 22.4 % of onsets with three or more
  simultaneous attacks. The crux bars (17-25), the approach 42-43 and the coda move in long,
  shared values by design.
- **Still not fully two-hand playable:** 15.8 % of onsets need more than two hands as written,
  or 2.5 % if the held bass note is sustained.
- **The middle of the fugue is mostly four voices.** The Br rests in 13-24 and 27-29.
- **The B#→E leap** (the crux interval) in the S at 34-35 and in the prelude R.H. at 19-20 and
  32-33 leaves the leading tone unresolved in that voice. Another voice takes the tonic.
- **The prelude** still has root-fifth-third broken chords in about half of its bars, and the
  motif M still dominates. The contrast between the two movements comes from tempo, texture and
  character, not metre.
