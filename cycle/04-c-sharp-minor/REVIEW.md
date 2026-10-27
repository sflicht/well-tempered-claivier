# Pair IV in C-sharp minor: composition review

Reviewed: **Prelude IV v6** (`work/wtc-work/v6/prelude_v6_bars.py` → `prelude-iv_v6.json`,
3/4, 38 bars, q=96) and **Fugue IV v7** (`work/wtc-work/v7/fugue_v7_bars.py` → `fugue-iv_v7.json`,
3/4, 56 bars, 5 voices, q=93).

This review comes from reading the score bar by bar. It is not a listening report: nothing
was auditioned. Bar numbers are real bar numbers. The prelude's tag comments are one higher
than the bar number from bar 22 on (for example, bar 22 is tagged "C23").
Notation: `b.beat` (for example 36.2), with tokens as in the sources.

## 0. The numbers

| check | Prelude v6 | Fugue v7 | Bach calibration |
|---|---|---|---|
| `critic.py` parallels (same-direction 5/8 on consecutive notes) | 0 | 0 | 0 |
| `critic.py` unresolved | 1 (21.3, a false positive: B#/F# are both in V7) | 2 (3.2, 32.3) | about 1 per 10–80 bars |
| **beat-to-beat (accented) parallel 5ths/8ves**, both voices moving, ad-hoc check | n/a | **25** | BWV 869: 1 in 76 bars; BWV 878: 0 |
| beats with ≥4 notes where one pitch class is tripled | n/a | **22.9 %** (2 quadrupled) | BWV 849 (5 voices): 11.6 %, never quadrupled |
| onset slots with ≥3 simultaneous attacks | n/a | **41.4 %** | BWV 849: 22.4 %; BWV 869: 16.5 % |
| onsets not playable by two hands (span ≤ a 10th) | 0 % | **30.3 %** (125/413) | BWV 849: **0/700** |
| S–A / A–T gaps wider than an octave (on beats) | n/a | 37/168, 40/168 | rare in Bach |
| voices sounding per bar | 2 | `1 1 2 2 3 3 2 2 2 2 3 4 …` (5 voices first at bar 33) | BWV 849: `1 1 1 2 2 2 3 3 3 3 3 4 4 5` (5 at bar 14 of 115) |

The official critic only compares consecutive notes. It misses octaves and fifths that land on
successive beats with a passing note in between. Those are the "collisions that sound like
mistakes" in this fugue. The ad-hoc checks were run on the built JSON and on the BWV 849/869/878
reference data. They are not committed. The method is in the table above.

---

## 1. What is good and must be preserved

### Prelude
- **The motif M** (bar 1, `E5:2 C#5:1 D#5:1 E5:2 G#5:3 F#5:1 E5:1 D#5:1`). The G# is a dotted
  eighth that starts on the "and" of beat 2 and carries across beat 3. That syncopation is the
  piece's spring. Keep its pitches and rhythm.
- **Three speeds of M.** M is augmented over the V pedal (19–20) and diminished into continuous
  sixteenths in the "drop" (22). That is real thematic work in the WTC manner.
- **The left-hand hemiola in 24–25.** Three groups of eight sixteenths span two bars of 3/4.
  This is a Baroque device and it is audible.
- **The pre-dominant chain 30–31.** A Neapolitan sixth (`F#3 A3 D4`) leads to a French sixth
  (`A C# D# F##`). It is rich and idiomatic. Keep it and fix its resolution (problems 7 and 14).
- **The closing tetrachord in 37** (`G#5:3 F#5:3 E5:3 D#5:3` → C#5). It is M's tail in
  triple augmentation, and an elegant way to end.
- **The idea of moving M into the tenor** (5, 10, 16, 29). Keep the idea and change its
  execution (problems 16 and 19).
- The prelude is clean: 0 parallels and fully playable. Its length (about 71 s) is right.

### Fugue
- **The subject** (T, bars 1–2: `G#4:2 E4:1 D#4:1 B3:2 F#4:6 | A4:4 F#4:2 D#4:2 B#3:2 C#4:2`).
  It is easy to recognise. The F# is held across beat 3, and the subject then falls through the
  diminished seventh A–F#–D#–B# to C#, a Bachian pathos figure. **Do not change a note of it.**
- **The entry order T–A–S–Br–B** and the two-bar regularity of the exposition.
- **The rhythmic idea of the countersubject in bar 3.** The CS holds G#3 while the answer runs
  in sixteenths, then runs (`E4 D#4 C#4 B3 A#3 B3`) under the answer's held note. That bar-3
  shape should become the fixed countersubject (problem 2).
- **The complete two-voice stretto in 25–27.** S and T enter a beat apart, two octaves apart,
  and both statements are complete. It is the only full stretto in the piece.
- **The release cadence in bar 46.** D#°7 → G#7/B# → C#m, under a soprano that falls by step
  F#6–E6–D#6–C#6.
- **The Neapolitan approach to the pedal in 49–50** (bass D–E–G#, with S and A in contrary
  motion), and the decision to end with a dominant-pedal stretto that resolves V→i at 53.1.

---

## 2. Things that don't work (ranked)

Severity scale: Critical, High, Medium, Low. Each problem has bars, evidence, why it fails,
and a fix.

### 1. The exposition thins instead of accumulating. The 5-voice promise starts at bar 33. *Critical (fugue)*
- **Bars:** 5–12, especially 7–10.
- **Evidence:** Voices sounding per bar are `1 1 2 2 3 3 2 2 2 2 3 4 4 …`. After their entries,
  A and T rest through bars 7–8, which are only S (CS) and Br (answer). Bars 9–10 are only Br
  and B. So the fifth entry, the bass, `G#2 E2 D#2 B1 F#2`, is heard with a single partner in
  the octave and a half B1–G#3. All five voices first sound together at bar 33, 59 % of the way
  through. Only 23 of 56 bars have five voices. In Bach's own five-voice C-sharp minor fugue
  the texture never decreases during the exposition (`1 1 1 2 2 2 3 3 3 3 3 4 4 5`).
- **Why it fails:** A fugal exposition is a growing argument: each new entry must change a
  texture that is already there. Passing a baton between duets is the "plodding" Sam hears, and
  it breaks the N+1 promise at the very moment it should be proved. The climactic bass entry
  sounds thin and muddy.
- **Fix:** Recompose 5–12 so that every voice continues after its entry: three voices in 5–6,
  four in 7–8, five in 9–10. Keep the entries and the CS (problem 2). Add a short link of one or
  two bars after bar 8, using the subject's head in sequence, so the bass entry is prepared and
  lands against four lines. Consider a **tonal answer**. The subject starts on ^5, and the
  normal answer to that begins on ^1 (C#). The real answer on D# forces an immediate move to
  G# minor and causes the critic's 3.2 error: the tenor's G#3 against the alto's F#4 is a
  seventh that leaps away (F#4→C#5). Range brief: keep S/A/T within the right hand's octave
  and a third, and Br/B within a tenth (see problem 5).

### 2. The "countersubject" is a rhythm template, not a melody. *Critical (fugue)*
- **Bars:** every "CS" tag: 3, 5, 7, 9, 13, 15, 19, 25, 31, 36, 41, 43, 47, 51.
- **Evidence:** The rhythm is always a long note plus six sixteenths, then 3-1-2-2-4. The
  pitches change at every entry:
  - 3 T `G#3:6 E4 D#4 C#4 B3 A#3 B3`: descending scale
  - 5 A `B3:6 D#4 E4 C#4 D#4 E4 G#4`: zig-zag rising
  - 7 S `F#5:6 G#5 F#5 A5 G#5 B5 A5`: zig-zag
  - 9 Br `B2:6 C#3 B2 D#3 E3 F#3 G#3`: rising scale
  - 19 T `A3:6 B3 C#4 A3 B3 A3 B3`: oscillation
  - 47 A `C#5:6 F#4 A4 D5 F#4 D5 A4`: arpeggio

  Its second bar also moves in eighths alongside the subject's eighths (bar 4: A
  `E5 C#5 A#4 F##4 G#4` / T `E4 F#4 E4 D#4 B3`).
- **Why it fails:** A countersubject exists so that the listener recognises a second identity
  and hears it change position, above and below the subject, through invertible counterpoint.
  Re-inventing the pitches every time leaves nothing to recognise. This is one main reason the
  fugue sounds like "harmony with a tune", and like the other fugues.
- **Fix:** Make the bar-3 version the fixed CS (`G#3:6 E4 D#4 C#4 B3 A#3 B3 | E4:3 F#4:1 E4:2
  D#4:2 B3:4`). Re-shape its second bar so it moves when the subject holds and holds when the
  subject moves. For example, a held suspension across beat 2 against the subject's
  `A4:4 F#4:2`. Prove it in double counterpoint at the octave and the fifteenth:
  `stretto_finder --subject <CS> --against <subject> --forms rectus --steps -7,-14,7,14`.
  Then use it verbatim, transposed to the key, at every entry. A second fixed CS for the fourth
  and fifth voices would make a real five-voice combination.

### 3. Collisions and voice-leading errors the official critic does not see. *High (fugue)*
- **Bars (beat-to-beat parallels, 25 in total):**
  - 4.1 A/T octaves (C#→E: two-voice texture, so very exposed)
  - 13.3 A/B; 15.3 A/T; 22.1 S/B; 27.3 S/T; 28.3 S/B; 33.3 S/A octaves; 31.3 S/A fifths
  - **36.2–36.3: T, Br and B in octaves F#–E–D on every beat** (`Br F#3:4 E3:4 D3:4` against
    bass `F#2 C#3 E2 A2 D2 A2`). This is a doubling. It is not a fifth real voice.
  - 38.1–39.2: the A major arpeggio in octaves in S, A, T and B
  - 41.3 and 42.1 T/B fifths (G#–D# → A–E → F#–C#); 45.1, 45.3 octaves; 47.3 S/A fifths
  - **50.2→50.3 S/T octaves G#5/G#4 → D#5/D#4**; 53.3 S/T fifths
- **Other evidence:**
  - One pitch class is tripled on 22.9 % of beats with four or more notes (BWV 849: 11.6 %).
    C# is quadrupled at 47.1 (`F#2 C#3 C#4 C#5 C#6`). G# is tripled over E at 15.2
    (`E2 G#3 G#4 G#5`, the third tripled). C# is tripled at 41.1 and at 42.1.
  - An augmented triad on a strong beat at 20.3 (`C#3 C#4 E#4 A5`).
  - The seventh is doubled at 18.2 (`B4` and `B5` over E#2).
  - An unresolved fourth at 32.3 (S `C#5` over `G#2`/A `B4`, a critic error).
  - The leading tone is doubled at 54.2 (`B#4` and `B#5`).
  - The final V7 at 55.3 has no leading tone and a doubled seventh (`G#2 G#3 F#4 F#5 D#6`).
    The tenor then takes its F#4 *up* to G#4.
- **Why it fails:** In Sam's words, these are the "harmonic collisions that sound like
  mistakes". Octaves landing on successive beats make the counterpoint sound hollow and
  amateur. The triplings come from wide spacing (problem 5).
- **Fix:** After recomposing, add a beat-level parallel check and a doubling check to the
  workflow (better still, to `tools/critic.py`). Target Bach's levels: 0–1 accented parallels
  and about 12 % tripling. Specific fixes:
  - Bar 36: Br `F#3:4 G#3:4 F#3:4` with T `A3:2 C#4:2 C#4:2 B3:2 A3:2 B3:2`. Checked on a
    scratch copy: this removes all three bar-36 parallels and adds none.
  - Bar 50: re-voice T so it stops shadowing S (`D4:4 B3:4 F#4:4`, a complete G#7 on beat 3
    with the seventh passed to the alto's E4 at 51.1). Checked: it removes the 50.3 octaves and
    adds no new error.
  - Bar 20: S `F#5:4 G#5:6 A5:2`, so the cadence on F#m arrives with A5 (then re-join bar 21
    by step).
  - Bar 54.2: keep a single B# (for example S `C#6:6 D#6:6`, A `A4:6 B#4:6`).
  - Bar 55.3: keep B# in the alto (`D#5:4 B#4:8` → C#5) and let the tenor's seventh F#4 fall
    to E#4, the Picardy third, instead of rising to G#4.

### 4. The subject is harmonised in E major, and its endings rarely land on the tonic. *High (fugue)*
- **Bars:** entries at 5, 25, 43 and 51. Subject endings at 6.3, 20.3, 26.3, 42.3, 44.3, 48.3.
- **Evidence:** The subject's first bar (G#–E–D#–B, then held F#) is repeatedly put over an E
  bass:
  - 5.1 `E3` under S `G#5`: reduction `Emaj7`
  - 25: bass `E2:10` under the stretto, so a whole bar of Emaj9 (`E2 … D#3 … F#5`)
  - 43.1–43.3: `G#2 E2` under the alto (reduction `Emaj7 | E/D# | B`)
  - 51: `E4` held over the `G#1` pedal

  The subject's final C# is then harmonised by something other than the tonic:
  - 6.3.5 `G#3 F#4 C#5` (G#7sus)
  - 20.3 `F#2 C#4 F#4 B5` (sus4)
  - 26.3 `F#2 D#3 A4 C#5` (D#ø7)
  - 42.3 `G#2 C#3 F#3 D#4 F#5` (sus)
  - 44.3 F#m; 48.3 over G#

  The stretto (25–27) never touches a root-position C# minor chord. The bass there goes
  E–F#–G#–F#.
- **Why it fails:** Bach's minor subjects define the tonic. That is the whole point of BWV 849's
  C#–B#–E–D#. Major-seventh "pad" sonorities at entries pull the piece away from the WTC idiom
  (Sam: "too much distance"). Endings that never reach the tonic give the long, harmonically
  vague stretches Sam described.
- **Fix:** Harmonise the subject as **i – VII – iv6 | vii°7 – i**. Over the head, use the bass
  `C#3:4 B2:4 A2:4`. Over the diminished bar, use `B#2:10 C#3:2`. Tested against the subject:
  0 parallels, 1 weak, 0 unresolved, roughness 2.17. The v7 bar-5 bass scores 1.87, but it is
  E major. The A→B# step can be decorated as a falling
  diminished seventh, A2→B#1, which is the subject's own pathos interval. End each entry on a
  root-position tonic, or on an intentional deceptive cadence. Keep the E-major colouring for
  one deliberate place only: the crux climax (Opportunity 1), where it means something.

### 5. Spacing: the texture is spread over four octaves, which makes it hollow and unplayable. *High (fugue)*
- **Bars:** worst 41 (8 unplayable onsets), 43 (8), 45 (9), 35 (7), 47 (7), 34 (6), 46 (5),
  13–18, 23–24.
- **Evidence:**
  - 30.3 % of onsets are unplayable at a tenth's span per hand; 52 % at a ninth. BWV 849:
    0 of 700.
  - Ranges: S B4–G#6, A B3–B5, T B2–B4, Br D#2–E4, B G#1–E3.
  - The gap between S and A exceeds an octave on 22 % of beats; between A and T, on 24 %.
  - Examples: 41.1 `C#2 G#3 | C#4 G#4 C#6`; 13.1 `E2 B3 G#4 B5`; 14.1 `E2 G#3 C#5 E6`.
- **Why it fails:** Bach's five-voice C-sharp minor fugue is written for one keyboardist, so its
  sonority is compact and blended. Our wide spacing causes the doublings in problem 3. It also
  makes the five voices sound like a bass, a pad and a descant, not five lines. Piano is now
  the primary medium (PROJECT_STATUS).
- **Fix:** Use the critic's keyboard check as a hard constraint in the recomposition: span at
  most a tenth per hand and at most three notes in the right hand. Narrow S and A to
  E4–E6 and B3–C#6, keep Br below the tenor, and allow at most an octave between S and A or
  A and T, except for a single climactic soprano note.

### 6. The climax (43–46) is not a contrapuntal event, and its "augmentation" is not one. *High (fugue)*
- **Bars:** 43–46.
- **Evidence:**
  - The bass "augmentation" is `G#2:3 E2:3 D#2:2 B1:4 | F#2:12 | A2:8 F#2:4 | D#2:2 F#2:2 B#1:2
    G#2:2 C#2:4`. A true augmentation is `G#2:4 E2:2 D#2:2 B1:4 F#2:12 | A2:8 F#2:4 D#2:4 B#1:4
    C#2:4`. Only 7 of 9 intervals and 3 of 10 durations match.
  - It starts at the same moment and on the same pitch class as the alto's normal entry
    (`G#4` / `G#2`), so the first beats sound like the subject doubled two octaves down, not a
    combination.
  - The subject is in the alto, buried under a "CS" in the soprano.
  - By their own tags, T and Br are "broken-chord eighths" (43–45).
  - The peak G#6 (45.2.5) is a passing eighth in a free voice over `A2 A3 A4 C#5` (an A major
    seventh), after the alto's subject has finished. The bass is static on `A2:8`.
- **Why it fails:** A climax must be the place where the materials meet in a way the listener
  can recognise. Here the highest note coincides with nothing thematic, and two of the five
  voices are accompaniment.
- **Fix:** Rebuild 41–47 as Opportunity 1 (the crux under two eighth-note strettos). Failing
  that, use a correct augmentation entering one bar after a normal entry and a fifth or octave
  away, with the peak note on the arrival of the second stretto voice.

### 7. The prelude never makes a structural root-position cadence. *High (prelude)*
- **Bars:** 7→8, 26→27, 31→33, 35→36, 37→38. Also 13–14 in E major.
- **Evidence:**
  - The return (27.1) has `G#3` as the bass on the downbeat, and E3 is the lowest note of the
    beat (`G#3 C#4 E3 C#4`). After eight bars of dominant, the tonic arrives as a 6/4 or 6/3,
    never in root position.
  - The French sixth (31) resolves to a cadential 6/4 (`G#2 E3 C#4 E3`, 32.1). That 6/4 never
    reaches V: 32.2 is `C#3` root and 32.3 is `G#2 C#3 E3` again.
  - 35→36 is V → i6 (`E3 G#3 B3 G#3`).
  - The final cadence (37.3→38) is V6/5 → i (`B#2 D#3 F#3 G#3` → `C#3`).
  - The only root-position V→i motions in the piece fall mid-bar inside the drop and the
    hemiola (23.1→23.2, 24.2→24.3). The A section closes with vii°6 → i (7.3→8.1).
  - The E-major area (9–14) also has no authentic cadence: 13.3 B7 → 14.1 B → 14.2 vi.
- **Why it fails:** Bach's preludes punctuate their forms with bass-leap cadences and close with
  one, often followed by a tonic pedal. Without them, the return and the ending feel provisional.
  This is the prelude's main formal weakness.
- **Fix:**
  - **32:** keep the 6/4 on beat 1, go to root V7 on beats 2–3
    (`G#2 B#2 D#3 F#3 G#2 D#3 F#3 B#3`), and make 33.1 the structural cadence on `C#2`/`C#3`.
  - **27:** put `C#3` on the downbeat (for example `C#3 G#3 E4 G#3 …`, or the falling version
    from `C#4 G#3 E3 C#3`).
  - **34–38:** turn into a tonic-pedal coda (problem 18), with the final V7 in root position
    (`G#2 D#3 F#3 B#3`) → `C#2`.

### 8. Strettos are timid, and the strettos at 40 and 51 use only the subject's head. *Medium-High (fugue)*
- **Bars:** 25–27, 40, 51–52.
- **Evidence:**
  - The only complete stretto (25) is the 1-beat offset two octaves down, which
    `stretto_finder` scores **14**. The subject allows better: in-key fifth at 2 beats (**7**),
    octave at **an eighth** (**10**).
  - At 40 (S, A, T) and 51 (S, T, Br), the voices enter one beat apart, all on G#, so each new
    voice is just an echo at the octave. The voices break off after 5–7 notes: 2/9, 3/9 and 2/9 of the
    subject's intervals at 51.
  - Bar 40 contains no B#, so the "dominant pedal" is really G# minor (v) with a major-seventh
    colour. It does not prepare the return at 41.
  - The subject is never inverted.
- **Why it fails:** Stretto is how a fugue intensifies. Cutting entries off after the head is a
  harmonic effect, not counterpoint.
- **Fix (tested):** Over the G#1 pedal at 51–52, use the dominant form of the subject, with B#
  in place of B (`G#:2 E:1 D#:1 B#:2 F#:6 | A:4 F#:2 D#:2 B#:2 C#:2`). Give it as a
  **three-voice stretto, complete, at offsets 0, an eighth and a quarter**, in G#5, G#4 and G#3.
  The pedal resolves to C#. `critic.analyse` on the four lines (pedal + 3 entries): **0 parallels,
  0 weak, 0 unresolved**. The fifth voice carries the fixed CS. In bar 40, add B# (for example
  in Br, `D#3 B#2 …`).

### 9. Static chord bars, homorhythmic eighths and filler voices: the "plodding". *Medium-High (fugue)*
- **Bars:**
  - Whole-bar chords: 12 (B7, arpeggiated by A, Br and B), 17 (A major; A and T arpeggiate
    together: `A4 C#5 E5 A4 C#5 E5` / `F#3 A3 E4 C#4 A3 C#4`), 30 (D#°7 in every voice over
    `D#2:12`), 38 (A major in S, A and B; it is tagged "N+ in the bass", but the bass is
    `A2 E3 C#3 A2 E3`, an arpeggio, and the declared bass entry at 38 matches only 2 of 9
    intervals).
  - Filler voices: 40 (Br oscillates `D#3 B2` six times); 21–24 (T in Alberti-style sixteenths:
    `F#3 D#3 A3 F#3 …`); 43–45 (T and Br broken chords; T trills `A4 G#4 A4 B4 …`).
- **Evidence:** 41.4 % of onset slots have three or more simultaneous attacks (BWV 849:
  22.4 %). The mean is 2.35 attacks per slot, against 1.84. Every entry starts on a downbeat,
  in two-bar units, except the stretto partners.
- **Why it fails:** The ear hears one block stepping on every eighth. Zest comes from staggered
  onsets, handing figures between voices, and harmony that moves at different speeds. Filler
  arpeggios also fail the "duplicating a function is not an extra voice" rule
  (ARTISTIC_DIRECTION).
- **Fix:** Every bar needs at least one voice holding or suspending while another moves.
  Replace arpeggio fillers with imitations of the CS's sixteenth run and of the subject's head
  at half-bar distances. Let at least two middle entries start on beat 3 or across the barline.
  `stretto_finder` gives an octave stretto at a dotted quarter (offset 6) a cost of 12, and the
  crux placement in Opportunity 1 favours an entry on 2.3.

### 10. The ending is a block-chord chorale with faulty voice leading. *Medium (fugue)*
- **Bars:** 53–56.
- **Evidence:** All of A, T, Br and B move in dotted halves or slower. 54.2 doubles the leading
  tone. 55.1 has Br and B in unison on G#2. 55.3 has a V7 with no B# and a doubled seventh.
  The fugue's own brief (`work/fugue_viii_passage_revision/next-fugue-iv-brief.txt`) asked for a
  "minor cadence with staggered resolutions rather than a long block-chord finish" and warned
  against repeating VIII's minor-to-major apotheosis.
- **Why it fails:** The energy built from 51 drains into hymn chords. Bach's fugues finish with
  moving lines over a tonic pedal.
- **Fix:** After the 52→53 V→i, write a 3–4-bar **tonic pedal (`C#2`)**:
  - the last subject statement, or the crux, or the prelude's M (Opportunity 3), in the soprano;
  - the CS run in the alto;
  - a chromatic descent in the tenor (B–A–G#–F##–G#);
  - staggered resolutions into the last chord.

  The Picardy third may stay, as in BWV 849, but compose its approach. Otherwise end in minor,
  as the brief asked.

### 11. Episodes are generic, not derived from the material. *Medium (fugue)*
- **Bars:** 21–24, 28–30, 33–35.
- **Evidence:**
  - 28–29: parallel thirds in S/A, descending scales in eighths
    (`D#6 C#6 B5 A5 G#5 F#5` / `B5 A5 G#5 F#5 E5 D#5`). The alto leaps up a ninth to join
    (critic: "leap > octave A4→B5").
  - 30: a whole bar of D#°7.
  - 33–34: contrary scales in sixteenths.
  - 21–24: the soprano saws up and down in sequence (7th up, octave up, 7th up: B4→A5,
    C5→B#5, B4→A5).
- **Why it fails:** Bach builds episodes from fragments of the subject and countersubject, so the
  argument never stops. Scales in thirds are generic galant/Vivaldi filler, the "too similar"
  sound of the retired method.
- **Fix:** Replace 28–35 with a second exposition of the crux (Opportunity 2). Or write sequences
  from the CS run (`E D# C# B A# B`) imitated between A and T at half-bar distances over a
  circle-of-fifths bass. Keep the falling-fifths bass of 28–29, which is good.

### 12. The tonal plan repeats F# minor, and the major-mode entries lose the subject. *Medium (fugue)*
- **Bars:** 13–16, 19, 36, 40–41, 47.
- **Evidence:**
  - Middle entries are in F#m three times (19, 36, 47) and in G#m only once (31).
  - The E-major "N+" (13, 15) matches only 2 of the subject's 9 intervals. Its diminished-seventh
    descent A–F#–D#–B# becomes a plain scale E–C#–B–A–G#, so the subject's most recognisable
    feature disappears.
  - The return at 41 is prepared by bar 40, which has no B# (see problem 8).
- **Fix:**
  - Swap one F#m entry (36 or 47) for A major (VI) or B major (VII).
  - Make the E-major statement a real modal transformation that keeps a diminished seventh,
    for example `… A#°7 → B` in place of the scale.
  - Prepare 41 with a real V (B# present).

### 13. The prelude and fugue share the same metre, tempo and character. *Medium (pair)*
- **Evidence:** Both are 3/4, "Allegro inquieto; lightly sprung", at q=96 and q=93
  (see `build_prelude.py` and `build_fugue.py`). Bach's two C-sharp minor pairs contrast a 6/4
  arioso with a 2/2 stile-antico fugue (WTC I) and a 9/8 prelude with a 12/16 fugue (WTC II).
  Sam: the fugues "sound too similar".
- **Fix:** Keep the prelude's Allegro. Give the fugue its own pulse: something like
  "Moderato, sostenuto", q≈80, in the gravity of a five-voice stile antico. Its density (five
  voices with sixteenths) is easier to follow slower, and the crux (Opportunity 1) belongs to
  that world. Or adopt the brief's 6/8 gigue, but that means recomposing the whole fugue.

### 14. A doubled augmented-sixth note in the prelude leads to octaves. *Medium, easy (prelude)*
- **Bars:** 31.3 → 32.1.
- **Evidence:** The right hand holds `F##5` from 31.3.25. The left hand's last sixteenth is
  `F##3` (`C#3 D#3 A3 F##3`). Both resolve to G#: the right hand to `G#5`, the left hand by
  falling a seventh to `G#2`. The tendency tone is doubled, and the voices arrive on octaves by
  contrary motion.
- **Fix:** Left hand, beat 3: `A2 C#3 D#3 A3` (or `C#3 D#3 A3 C#4`). Keep F## in the right hand
  only.

### 15. The dominant pedal (19–22) is harmonically frozen, and the "arrival" changes nothing. *Medium (prelude)*
- **Evidence:** The reduction runs 20.1–22.3 as `G#7 | G#7/D# | (E appoggiatura) | G#7 ×3 |
  (E appogg.) | G#7 ×2`: twelve beats on V7 (19 included), arpeggiated identically. The
  "arrival" at 21 (`D#5:2 F#5:4` over `G#2:6`) is the same chord as the two bars before it.
- **Why it fails:** Bach does use long dominant pedals (WTC I C minor prelude), but he moves the
  harmonies above the pedal. Here the climax of the piece has no harmonic event.
- **Fix:** Move the upper harmony every half-bar above the G# pedal:
  - 19: V7 → i6/4;
  - 20: iv6/4 (F#m/G#) → F##°7/G#;
  - 21: V7 with the held F#5 (keep it);
  - 22: the drop.

  Better still, put the crux in the right hand as two classic suspensions (Opportunity 3).

### 16. Galant texture and motif monotony: M at every barline, no imitation. *Medium (prelude)*
- **Evidence:**
  - The left-hand figure is an Alberti pattern (root, fifth, upper third, fifth:
    `C#3 G#3 E4 G#3`) under a one-bar tune.
  - M's rhythm `2 1 1 2 3 1 1 1` starts 13 right-hand bars and 4 left-hand bars, plus head
    variants. It always starts on a downbeat.
  - The hands never overlap M. The "hand switch" bars (5, 10, 16, 29) pass it at the barline.
- **Why it fails:** WTC preludes of this kind work through implied polyphony and imitation
  (the BWV 849 prelude is a three-voice imitative arioso). One bar repeated at the barline
  makes the plodding happen at the phrase level, and the Alberti bass pushes the piece toward
  the Classical style.
- **Fix:** In 5, 10, 16 and 29, let the left hand answer M **at the half-bar (offset 6
  sixteenths), a 4th or 11th below**. Kept in key, that is `B#3 G#3 A3 B#3 D#4 C#4 B#3 A3`,
  M on the dominant. `stretto_finder` scores this cost 2, roughness 0.40, 0 parallels. The left hand then enters on the right hand's syncopated G#, and the hands
  overlap. Elsewhere, re-voice the left hand so its lowest notes make a stepwise bass line
  (compound melody), not root–fifth–third–fifth.

### 17. The falling-thirds sequence (15–18) is mechanical. *Low-Medium (prelude)*
- **Evidence:** Four literal statements of M in A, F#m, D and B, with identical rhythm.
- **Fix:** Change the third link. Options: M inverted (mirror around E: `E G# F# E C# D# E F#`;
  `stretto_finder` scores the mirror an octave below against M at cost 7); or break M's tail G#–F#–E–D# into half-bar units so the harmonic rhythm accelerates
  into the pedal.

### 18. The lament bass in bar 34 is too compressed to be heard. *Low-Medium (prelude)*
- **Evidence:** `A3 E4 G#3 G3 F#3 D4 F3 D4 E3 B3 G#3 E4`. The chromatic line A–G#–G–F#–F–E is
  hidden as every other sixteenth in the tenor register, inside one bar.
- **Fix:** Spread it over two bars in the real bass, in quarter notes (`A2 G#2 G2 | F#2 F2 E2`),
  under M, arriving on the cadential 6/4 or the tonic pedal (problem 7). This is the *passus
  duriusculus*, which BWV 849's world invites.

### 19. Hand-switch bars lose the bass and collide on the motif's G#. *Low (prelude)*
- **Evidence:** In bar 29, the bar after the return, nothing sounds below `C#4`. At 5.2.5 and
  29.2.5, the motif's dotted G# (`G#3`/`G#4`) sits a minor ninth below the right hand's A
  (A-major figuration `C#5 A4 E5 A4` / `C#5 A5 E5 A5`).
- **Fix:** In these bars, harmonise beat 2 as C#m, not A, or keep the left hand's M an octave
  lower with the figuration below it. Problem 16's half-bar imitation removes most of this.

### 20. B# is cancelled at the final tonic arrival. *Low (prelude)*
- **Evidence:** `B#3` (35.3.75) → `B3` (36.1.5, left hand `E3 G#3 B3 G#3`). The leading tone is
  answered by B♮ in a C#m7.
- **Fix:** Left hand: `E3 G#3 C#4 G#3`.

---

## 3. "Turn it up to 11": opportunities for this pair

### Opportunity 1: The Crux. Bach's own BWV 849 subject as a cantus firmus under our subject in stretto at the eighth
Bach's WTC I C-sharp minor fugue (BWV 849) is built on the "cross" subject **C#–B#–E–D#**.
This review calls it *the crux*. **Credit it in NOTES.md:** J. S. Bach, WTC I, Fugue 4,
first subject.

Augmented in our 3/4 as `C#:24 | B#:12 | E:12 | D#:24 | C#:12`, it spans **7 bars**. Those
bars can replace the return and climax (v7 41–47). Two complete entries of our subject run over
it, each a **two-voice stretto at an eighth's distance**:

| crux bar | crux note | above it |
|---|---|---|
| 1–2 | C# (tonic pedal) | subject at G#5 + subject at G#4 an eighth later; the diminished bar becomes vii°7 over the pedal |
| 3 | B# | link: fixed CS; the 5th voice |
| 4 | E | subject + partner an eighth later; the head bar (G#–E–D#–B = **Emaj7**) sits exactly on the crux's E |
| 5–6 | D# | the subject's diminished bar A–F#–D#–B# = **D#°7 = B#°7**, the chord that contains both of the crux's leading notes |
| 7 | C# | resolution |

Why it works musically: the "E-major problem" of problem 4 becomes the *point*. The subject's
head is an E major seventh. Its second bar is the one diminished seventh that holds B# and D#,
the crux's two leading notes. Bach's subject turns out to be the harmonic skeleton of ours.

**Tests (`stretto_finder` engine plus `critic.analyse`):**
- Crux in the bass (`C#3…`), with the subject entering at G#5, then G#4 an eighth later (bars
  1–2), and at G#4, then G#5 an eighth later (bar 4): **0 parallel errors, 1 weak,
  1 unresolved**.
- Crux in the soprano (`C#6 B#5 E6 D#6`, which makes E6 the climax note), with the entry pairs
  at G#3/G#4: **0 parallels, 0 weak, 1 unresolved**.

So the combination is invertible at the octave and fifteenth, and can be used twice: at the
return with the crux in the bass, and at the climax with the crux in the soprano. The single
unresolved point is the same in both versions: bar 3.1, where the second stretto voice ends on
C# against the crux's B#. Fix it by bending that entry's last note (C#→B#→C#) or by tying the
crux's C# one eighth into bar 3.

The 5th voice is the fixed CS. All five voices are then real: crux, subject, subject, CS and a
free line. Bach never combined his crux with a foreign subject, never at an eighth-note stretto,
and never swapped it between outer voices in a five-voice texture.

### Opportunity 2: A double fugue, with triple-counterpoint rotation
Introduce the crux unaugmented (`C#4:12 B#3:6 E4:6 D#4:12`, bar-long notes in 3/4) as a quiet
**second exposition in stile antico**. It replaces the generic episodes 28–35 (problem 11) and
answers problem 13's need for gravity. The fugue becomes: subject exposition → crux exposition →
combination. That follows BWV 849's own triple-fugue plan, scaled to our forces.

Then rotate the combination (crux, subject stretto pair, CS) through three voice orders:
1. Return: crux in the bass. Tested.
2. Climax: crux in the soprano. Tested.
3. Coda: crux in the tenor over a `C#2` pedal, with the prelude's motif above it
   (Opportunity 3). Untested as a whole.

Every combination must still be written out by hand and re-checked with five voices sounding.
The tests above cover two- to four-line placements only.

### Opportunity 3: The crux as the bridge between prelude and fugue
The prelude's motif and the fugue subject do **not** combine cleanly: M + M-on-V against the
subject scores cost 21 at best, with an unresolved dissonance. The crux combines with both:
- The prelude's opening phrase (M | M on V | the closing tetrachord G#–F#–E–D#) over the crux in
  bar-long notes, entering one bar after it: **0 parallels, 0 unresolved** (cost 13, 9 quarters
  of overlap).
- Over the prelude's dominant pedal, the crux is a pair of textbook suspensions: in 19–20 the
  right hand plays `C#5:6 B#4:6 | E5:6 D#5:6` over G#7, a **4–3 then a 6–5**. Keep B# out of the
  left-hand arpeggio while the C# is held.

So:
- Plant the crux in the prelude: in the right hand at the V-pedal (19–20), and as the
  left hand's lowest notes at the return (27–30: C#, B#, E, D#, C#) under M.
- Let it come forward as a subject in the fugue (Opportunities 1–2).
- End the fugue's tonic-pedal coda with the prelude's M above the crux.

The listener learns Bach's subject in the prelude without being told, then hears it rise in the
fugue. This is cyclic thinking that the WTC itself never uses.
