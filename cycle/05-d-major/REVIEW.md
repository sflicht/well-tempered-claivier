# Pair V in D major: composition review

**Reviewed:** Prelude V v1 (`work/wtc-work/pairV/prelude-v_v1.json`, source `prelude_v1_bars.py`) and Fugue V v3 (`work/wtc-work/pairV/fugue-v_v3.json`, source `fugue_v7_bars.py`).

**Method:** I read every bar of the `literal_bars` and used the repository tools:
- `tools/critic.py`
- `tools/reduce.py --per beat`
- `tools/stretto_finder.py`

I also wrote some scratch analysis scripts:
- a per-beat triad estimator
- pedal-run, D/A-share and low-register-clash counters
- a harness that runs `critic.analyse` on trial combinations

The Bach comparisons come from the BWV 850 reference MIDI.

**Limits.** Nothing here was heard. This is score inspection, and Sam's listening has the last word. The judgements are a strict teacher's: the standard is the WTC, turned up, not abandoned.

---

## 0. Verdict in one paragraph

The subject is good: a D-major trumpet fanfare with a real rhythmic profile, the "tattoo" dactyl. The fugue does almost nothing harmonically with it:
- Bar 1 of the subject is one triad held for four beats.
- Every stretto is written at the unison or octave, usually over a held pedal.
- 21 of the 26 statements sit on the tonic or dominant.
- The last 13 bars have D or A in the bass on 81% of beats.

The piece is contrapuntally clean: 0 parallel errors and 1 unresolved dissonance, which is within the Bach calibration. It is harmonically frozen, rhythmically repetitive, and in places it is not counterpoint at all:
- Episode 2 is a three-voice scale in parallel tenths.
- Episode 3 is violin bariolage.
- Episode 4 is a prelude texture.
- The coda is in parallel sixths.

That is exactly the "plodding / too similar / harmonically static" complaint.

The prelude has a real dramatic arc in bb. 21–32 and an extrovert energy worth keeping. Around that arc it is a pure arpeggio etude. The same 8-bar progression is played three times, the hands sit about two octaves apart, and the register is an octave above anything in the WTC.

---

## 1. What is good and must be preserved

### Fugue V

1. **The subject's character (bb. 1–2).** A4 D5 D5 D5 F#5 F#5 F#5 A5 | A5. G F# E D C# B A B C# D.
   - It is a memorable head: a rising 4th, then the 8th + two 16ths tattoo on each triad note.
   - It ends in a scale tail that cadences properly.
   - D major is Bach's trumpet-and-drums key (BWV 1068/1069, the Christmas Oratorio), so the affect is right.
   - Keep the subject. The problem is how it is set.
2. **Episode 1 (bb. 13–16) is the best passage in the fugue.**
   - The head cell runs in a one-beat canon between soprano and tenor at the octave: S A5–D6, F#5–B5, D5–G5, B4–E5 against T F#4–B4, D4–G4, B3–E4.
   - The harmony moves by descending thirds over the bass D3–B2–G2–E3: D–Bm–G–Em.
   - It cadences via A–D, G–F#m into B minor, and the b. 15 soprano 16th-note scale gives lift.
   - It is derived, moving, two chords per bar. Make it the model for everything else, and for the climactic stretto (§3A).
3. **The accumulating exposition from v2.** Every voice continues after its entry with no drop-outs, reaching six voices at b. 11. Keep the principle; the writing needs fixes (problem 3).
4. **Off-beat entries at lags of 7 and 9 sixteenths** (b. 32 Br, b. 39 Br, b. 51 A, b. 54 S at lag 7; b. 54 B at lag 9). The tattoo lands *per arsin et thesin*, against the beat. This is the most interesting rhythmic idea in the fugue: keep the displacement and change the pitch levels.
5. **Stretto I's location (bb. 25–28).**
   - It is the only flat-side region: C♮ appears only in bb. 25–27.
   - The v3 tenor countersubject is complete and literal there.
   - Keep the subdominant region; recompose the texture.
6. **Episode 4's harmonic skeleton (bb. 35–38).**
   - Bm–Em | A–D | G–F#(A#) | Bm is the only real minor-mode sequence: descending fifths with a leading tone.
   - The alto suspensions D5:6 C#5:2 B4:6 D5:2 are good.
   - Keep the bass and harmony; replace the texture (problem 11).
7. **Episode 5's rising sequence (bb. 42–46).** A–Bm–(C#ø)–D–E reaches V/V at b. 46 and lands on V with the augmentation's A2 at b. 47.1. That is good dominant preparation.
8. **The augmentation (b. 47).** It is the only transformation of the subject in the piece. Keep the idea, then relocate and revoice it (problem 9).
9. **Clean basics.**
   - `critic.py`: 0 parallel errors, 2 weak parallels, 1 unresolved dissonance, 0 crossings.
   - Do not lose this while fixing the music.

### Prelude V

1. **The climax arc, bb. 25–32.**
   - An A dominant pedal climbs to A7 at the top (b. 28).
   - A deceptive move to Bm follows (b. 29), then G#°7 with the piece's only F♮ (b. 30).
   - Falling A7 arpeggios from E7 (b. 31) lead to arrival on D with the D2 bass (b. 32).
   - This is the only stretch where harmony makes tension and releases it. It is the model.
2. **The 7th-chord chain, bb. 21–24.** F#m7–Bm7–Em7–A7 is circle-of-fifths drive leading into the pedal.
3. **The pivot at b. 16.** The G♮ makes A into V7/IV and pulls back to D: a good joint.
4. **The affect and the motor.** It is bright and extrovert, with continuous propulsion. Sam finds the preludes more promising, so keep the energy and add line, register and form.
5. **The idea that the prelude previews the fugue** through the tattoo cell (bb. 17–20). The idea is right; the execution is not (problem 14).

---

## 2. Measurements

### Fugue: 236 beats

| Measure | Value |
|---|---|
| Beats whose lowest note is a pedal held ≥ 6 beats | **77 / 236 = 33%** |
| …those pedals | B (b. 17–18), F# (b. 19–20), G (b. 24.4–27, 11 beats), A (b. 39–42, 16 beats), D (b. 51–59, 36 beats) |
| Beats with ≥ 90% of sounding duration inside one triad | **113 / 236 = 48%** |
| Beats whose estimated chord is D or A/A7 | **117 / 236 = 50%** |
| …by section | Expo 56%; Ep1 38%; M1 12%; Ep2 38%; Stretto I 8% (it is G instead); Ep3 44%; Stretto II 67%; Ep4 31%; Stretto III **83%**; Ep5 40%; Peak 62%; Final stretto **71%**; Coda **83%** |
| Lowest voice on D or A | 45% overall; **81% in bb. 47–59**; 71% in bb. 39–59 |
| Subject statements | **26** (31 entry labels minus 5 countersubject labels): **15 at the D level** (A-start), 6 at the A level, 3 in G, 1 Bm, 1 F#m. That is **81% tonic/dominant**, with none in a minor key after b. 20 and never E minor. |
| Bars in a D or A key area | about 36–40 of 59, two-thirds |
| Bars in a minor key | 12 (bb. 17–24, 35–38) |
| Chromatic vocabulary | C♮ only in bb. 25–27; A# only in b. 37; G# in the A-major passages. **No F♮, B♭, D#, E#.** |
| Longest identical-chord runs (estimator) | 8 beats D (b. 53.4); 7 beats A (b. 39.1); 7 beats G (b. 25.1); 7 beats D (b. 8.4–10.2) |
| Keyboard | 358 / 651 onsets = **55%** need more than two hands |
| Register | S G4–B6; 199 of 391 soprano notes (51%) above B5. BWV 850's highest note is B5. |

### Prelude: 160 beats

| Measure | Value |
|---|---|
| D- or A-rooted beats | **88 / 160 = 55%** (D 31%, A/A7 27%) |
| Bars on a single harmony / two / three | 19 / 18 / 3 |
| Chord-tone share | `critic` tertian fit **97.5%**. 69% of beats are ≥ 90% one triad; the rest are mostly 7th chords. |
| Repeated progression | The same 8-bar formula I \| IV–I6 \| ii–V \| V7–I \| vi–iii \| IV–I6 \| ii7–V7 \| I appears in **b. 1–8 (D), b. 9–16 (A), b. 33–39 (D)**: 23 of 40 bars |
| Chromatic vocabulary | G# in the A-major passages; F♮ only in b. 30. No C♮, B♭, D#, A#. |
| Gap between hands | ≥ an octave on **155 / 158 beats**; mean gap 21.8 semitones |
| RH register | A4–F#7, with **55%** of RH notes above B5. BWV 850's prelude RH spans F#3–B5. |
| LH | 626 sixteenths. BWV 850's prelude LH plays 156 eighths. |

---

## 3. Verification of the first impressions

| Impression | Verdict | Evidence |
|---|---|---|
| Arpeggio subject makes every stretto a static triad over a pedal (bb. 25–27, 51–55) | **Confirmed, and wider** | **b. 25–26:** G on 7 consecutive beats over Cb `G1:40` (+ Bass `G2:16`). **b. 32–33:** D; the three entries are on A4/A3/A2, all octaves. **b. 39–40:** A on 7 beats over Cb `A1:16~ A1:16~ A1:12`. **b. 51–55:** D over `D2:144`, with entries on A5/A4/A3 and then A3/A5/A2. |
| Exposition alternates I and V for 12 bars | **Confirmed** | Entries every 2 bars, alternating D and A: A b1, T b3, B b5, S b7, Br b9, Cb b11. There is no codetta. Also, the answer is **real** (E–A) where a **tonal** answer (D–A) is required (problem 3). |
| Ep2 bb. 21–24: parallel 10ths, identical 3+3+2 rhythm, 3 voices | **Confirmed exactly** | S/T are a 10th apart on **32 / 32** eighth-note samples. S, T and B all move `6+6+4` sixteenths for 4 bars. S runs D6→G4 by step. |
| Ep4 bb. 35–38 becomes a homophonic prelude texture | **Confirmed**, but its harmony is the best in the piece | S has 16th broken chords in 3+3+2. A, T and Cb have half notes. B has broken-chord eighths. There is no subject material. |
| Coda bb. 56–58: parallel-10th 16ths over a 9-bar D pedal | **Partly.** The pedal is 9 bars (b. 51–59). The coda's 16ths are parallel **6ths** in b. 57 (e.g. D6/F#5, C#6/E5, G6/B5), and 10ths and mixed intervals in b. 58. The problem is the same. | Scratch interval count, S/A b. 57: 6ths on 15 of 16 sixteenths |
| Bariolage bb. 28–30 leaps more than an octave every 16th | **Partly** | Bb. 28–29 alternate D6 with 3rds to 7ths (6 sevenths flagged). From b. 29.4.75 to b. 31.1 there are **14 consecutive leaps larger than an octave**, up to an 11th (D6–G4). |
| About 55% of onsets exceed two hands | **Confirmed** | 358 / 651 = 55.0% (`critic`) |

---

## 4. Things that don't work, ranked

[F] marks a fugue problem and [P] a prelude problem. Severity runs Critical / High / Medium / Low.

### 1. [F] The strettos and pedals freeze the harmony. **Critical.**

**Bars:** 25–27, 32–33, 39–42, 51–59 (also the drum pedals at 17–20).

**Evidence.**
- Every stretto places later entries at the unison or octave of the first, at lags of 4 to 14 sixteenths:
  - Stretto I: S1 D4, S2 D5, S3 D3
  - Stretto II: A4, A3, A2
  - Stretto III: E4, E3, E5
  - Final stretto: A5, A4, A3, then A3, A5, A2
- Because bar 1 of the subject is one triad, the result is a single chord thickened by three tattoos:
  - `reduce.py` b. 25: `?27[G1^D4] | ?027[G1^D5] | G[G1^G5] | G[G1^B5]`
  - b. 26: `G | G | Gmaj7 | Em/G`
  - b. 39: `A[A1^C#6] ×4`
  - b. 54: `?279 | ?2469 | D | D`
- Under three of the four strettos the contrabass holds a pedal: `G1:40`, `A1:16~…`, `D2:144`.
- Overall, a third of the piece sits on a held pedal and half of it on one triad per beat (§2).

**Why it fails.** A stretto is the place where a fugue's harmonic rhythm should *tighten*. Here it stops. With the subject's head in every voice, the listener hears a D-major (or A, or G) chord vibrating for two bars, then a scale. That is exactly "long harmonically static stretches". Bach's dense strettos (BWV 874 is the obvious D-major one) work because his entries are placed at intervals that make the overlaps form *progressions*, not doublings.

**Fix.**
- **(a) Never write a stretto entry at the octave or unison of the previous one.** `stretto_finder.py` shows the clean non-octave options this subject allows:
  - rectus + **inversus** at 3 beats (offset 12) at the lower 3rd/10th: cost 5, 0 parallels, 0 harsh. This is the cleanest combination of all.
  - inversus at lag 6 at the lower 5th / upper 4th: cost 7. At lag 7: cost 10.
  - rectus at 1 beat at the lower 3rd: cost 13, 2 weak parallels.
  - rectus at 1 bar at the lower 3rd: cost 13.
  - rectus diminution (×½) at 1 beat at the lower 3rd: cost 6.
  - inversus diminution at 2 beats: cost 4.
- **(b) Replace each pedal with a moving half-note bass that reharmonizes the arpeggio.**
  - Under the subject, a bass D–F# | G–A–(B)–G–A–D gives I–I6 | IV(9–8)–V–vi–IV–V–I.
  - The subject's long A at the start of bar 2 then becomes a **9–8 suspension** over G.
  - Tested in scratch: subject over `D3:8 F#2:8 | G2:4 A2:4 B2:2 G2:2 A2:2 D2:2` → 0 parallels, 0 unresolved, 0 crossings.
  - The bolder variant, D–B | G…, makes bar 1 into I–vi7. Tested: 0 parallels, harmony D D B B7 | A7/G D/A G/B D/A. The critic flags the held A over B (b1.4) as an unresolved 7th, because it turns into the 9–8 one 16th late; justify it in NOTES.
- **(c) Specific replacements.**
  - Stretto I in G becomes a mirror stretto: rectus on D4, inversus 3 beats later a 3rd lower, plus a diminution in a third voice, over the bass G2–E2 | C2–D2 (G–Em7 | C–D7), not G1.
  - Stretto II keeps the lag-7 displacement but moves to **E minor/B minor**: the second entry is the inversion at the lower 5th (cost 10, clean), and D# and A# finally appear.
  - Stretto III is cut. Its bars go to the cascade stretto (§5A).
  - The final pedal is reduced to 3–4 bars (problem 10).
- **(d)** Limit any pedal to 3 bars, and only at the end or before a structural arrival.

### 2. [F] The tonal plan is locked in D/A, and the harmonic palette is almost purely diatonic. **Critical.**

**Bars:** whole piece, worst in bb. 32–59.

**Evidence.**
- 21 of 26 statements (81%) are at the tonic or dominant level, and 15 of them at the *same* D level (A-start).
- About two-thirds of the bars are in D or A.
- Minor keys appear only in bb. 17–24 and 35–38. There is no entry in E minor, and no subject entry in any minor key after b. 20.
- From b. 39 to the end (21 bars) the key plan is A → (rising to E) → D, with the lowest voice on D/A on 71% of beats.
- Accidentals: C♮ only in bb. 25–27, A# only in b. 37. There is never F♮, B♭ or D#.

**Why it fails.** A 59-bar, six-voice fugue with this little tonal travel cannot avoid sounding "all the same". Sam's complaint that the fugues are "too similar" is partly a key-plan problem. A WTC major-key fugue typically gives middle entries in vi, ii or iii and IV, and often colours the end with ♭7 (V7/IV) or minor iv. This fugue has nothing of that after b. 27.

**Fix.** Re-plan the keys before rewriting notes:
- Exposition in D/A.
- Middle entries in **Bm and Em** (not Bm and F#m, which only reproduces I/V in the relative minor).
- Stretto I in **G**, with C♮.
- A minor-mode stretto in **Em/Bm**, with D# and A#.
- The climactic cascade through **F#m–Bm–Em–A–D–G** (§5A), with C♮.
- The final pedal with ♭7 (C♮) and one minor-iv colour (B♭/G minor) two bars before the end.

Targets: no more than about 50% of bars in D/A; no more than about 12 of about 20 statements at the D/A level; at least four accidentals beyond G#.

### 3. [F] The exposition has a real answer, metronomic I/V alternation, and free voices that fill in the triad. **High.**

**Bars:** 1–12.

**Evidence.**
- The answer is real: T b. 3 `E3:4 A3:2 A3 A3 C#4:2…`, and likewise S b. 7 E5 and Cb b. 11 E2. The subject opens ^5–^1 (A↑D), which by Bach's practice requires the tonal answer ^1–^5 (D↑A). The head of *Die Kunst der Fuge* (D–A answered by A–D) is the textbook case.
- The real answer's E head produces bare E octaves or A6/4 sonorities at each answer:
  - b. 3.1: E3 + E5
  - b. 11.1: E2 E3 E4 C#5 E5 C#6, four E's
- Six entries arrive exactly 2 bars apart with no codetta, so the key flips D/A/D/A/D/A.
- The free voices mostly arpeggiate the current triad:
  - b. 5–6 alto `A5:6 G5:2 D6:4 A5:4 | F#5:2 G5:2 A5:4 D6:4 G5:2 E5:2`
  - b. 9–10 soprano `D6:6 E6:2 F#6:4 A5:4 | D6:4 F#6:4 D6:4 B5:4`, tenor `D4 F#4 A4 B4 D5 | D5 A4 B4 D4`, bass `F#3 D3 D3 | F#3 D3 B2 B2 A2`
  - The estimator reads D on 7 beats in a row (b. 8.4–10.2).

**Why it fails.** The listener hears the same harmonic event six times at a fixed pulse. It is the "plodding" of the opening minute. The real answer also undercuts the tonic at every other entry.

**Fix.**
- **Tonal answer:** change only the first note. Tenor b. 3 becomes `D3:4 A3:2 A3:1 A3:1 C#4:2 C#4:1 C#4:1 E4:4 | (bar 2 unchanged)`. Likewise S b. 7 (D5) and Cb b. 11 (D2).
  - The countersubject's first note E5 would then make a 9th with D3. Tie the alto's final D5 of the subject over into b. 3 and start the CS from its second note.
- **Insert a 1-bar codetta after entry 2.** Build it from the 16th-note tail, imitated between A and T and closing via ii6–V, so that the third entry (Bass) is *arrived at*.
- **Bring the Cb answer in one bar early** (b. 10, overlapping the Br subject), which gives a stretto inside the exposition. Tested: Br subject on A3 plus Cb tonal answer on D2 at a 1-bar lag gives 0 parallels, 0 unresolved, 0 crossings.
- **Rewrite the free voices as suspension and syncopation lines** (tied quarters, 4–3 and 7–6), and give each new entry a different bass:
  - entry 3 over D–B (I–vi7)
  - entry 5 over D–F# | G (I–I6 | IV 9–8)

### 4. [F] The contrabass is not a sixth real voice; Bass and Cb double and collide. **High.**

**Bars:** 13–24 (rest), 25–28, 35–38, 39–42, 42–46, 47, 50, 51–59.

**Evidence.**
- The Cb has an independent contrapuntal line only in **bb. 11–12, 32–34 and 47–50: 9 of 59 bars**. Otherwise it rests (bb. 13–24, 29–31), holds pedals (bb. 25–28, 39–42, 51–59), or doubles the Bass's half-note roots.
- In Ep5 (bb. 42–46), Bass and Cb are at the octave or unison on **19 of 40** eighth-note samples. In Ep4 (bb. 35–38) it is 11 of 32.
- Unisons: B1 at b. 38.3–4, G2 at b. 45.3, E2 at b. 46.3, A2 at b. 47.1, A1 at b. 39.3.
- `critic` "weak" parallel at b. 50.2.5: **parallel unisons** B2/B2 → A2/A2 between Bass and Cb.
- Seconds between the two lowest voices below C3:
  - G2/A2 at b. 32.4.5, b. 45.3.5 and **b. 47.2** (the second beat of the "PEAK")
  - A1/B1 at b. 39.2.5 and b. 39.3.5 (the Bass countersubject grinding against the A1 pedal)
  - B2/C#3 at b. 50.1.5

**Why it fails.** The brief says it plainly: "duplicating a musical function does not fulfil the promise of another independent line." On the piano, seconds in the first and second octaves are the "collisions that sound like mistakes" Sam reported.

**Fix.**
- Decide the roles.
  - The Cb is the slow line: long notes, augmentations, cantus.
  - The Bass is the active eighth-note line, kept at least a 6th above the Cb.
  - No octave or unison between them on consecutive beats.
  - No seconds or ninths between them below C3 except prepared suspensions.
- Specific changes:
  - After b. 12 the Cb continues into Ep1 as a slow line (D2–B1–G1–E2 under the descending thirds) instead of resting for 12 bars.
  - Bb. 35–38: replace `B1:8 G1:8 | A1:8 F#1:8 | B1:8 A#1:4 F#1:4 | D2:8 B1:8` with a line in contrary motion to the Bass, for example tied syncopations that make 7–6 and 4–3 against it.
  - Bb. 39–41: delete the A1 pedal, or move the Bass countersubject up an octave.
  - Bb. 42–46: revoice to remove the unisons at b. 45.3 and b. 46.3.
  - B. 50: break the parallel unisons.

### 5. [F] Episode 2 is a three-voice parallel-10th scale in lockstep. **High.**

**Bars:** 21–24.

**Evidence.**
- S `D6:6 C#6:6 B5:4 | A5:6 G5:6 F#5:4 | E5:6 D5:6 C#5:4 | B4:6 A4:6 G4:4`.
- T is the same line a 10th below on 32 of 32 samples.
- B `B2:6 F#2:6 G2:4 | D3:6 E3:6 F#2:4 | A2:6 B2:6 F#2:4 | G2:6 D3:6 G2:4` moves in the identical 6+6+4 rhythm.
- Only 3 of 6 voices sound, and only 3 attack points per bar. These are the thinnest and slowest bars in the piece, at its formal centre.

**Why it fails.** It is a harmonized scale, not an episode. Nothing is imitated, nothing is developed, and the 3+3+2 accent loses its point when all three voices share it.

**Fix.** Recompose as a 5-voice episode from the subject's tail (the 16th-note figure D C# B A B C# D):
- S and A imitate at 2 beats, T and Br answer in inversion, and the Bass walks in eighths.
- Make it a descending-fifths sequence Em–A–D–G that prepares Stretto I in G.
- Keep the 3+3+2 "tresillo" in *one* voice only, the bass or a dance-like tenor, so it reads as an accent against the others.
- No run of parallel 10ths longer than 3 events.

### 6. [P] The prelude repeats one 8-bar progression three times in a square form with no minor-key region. **High.**

**Bars:** 1–8, 9–16, 33–39.

**Evidence.**
- The section tags give I | IV–I6 | ii–V | V7–I | vi–iii | IV–I6 | ii7–V7 | I in b. 1–8.
- B. 9–16 is the same formula in A: same tags, the same compound figure, and the same top-note E6 on 24 of 64 sixteenths in bb. 9–12.
- B. 33–39 is the same formula in D with the vi–iii bar removed; the v1 report's checker found b. 6 and b. 34 72% pitch-similar.
- The form is 5 × 8 bars, each block closing on I or V.
- 55% of beats are D- or A-rooted. B minor appears only as a chord (b. 5, 19, 22, 29), never as a key. There is no C♮ and no minor-mode colour except the F♮ of b. 30.

**Why it fails.** Twenty-three of 40 bars say the same thing. The "B section in the dominant" is a transposed copy, not a modulation: b. 9 jumps to A with no pivot.

**Fix.**
- Keep b. 1–8.
- Rewrite b. 9–16 as a *modulating* section, for example:
  - A (b. 9–10)
  - sequence E7–A–D–G#ø7–C#7 (b. 11–13)
  - F#m (b. 14)
  - G–C#7 → **F#m or Bm cadence** (b. 15–16)
- Then let b. 17 restart from the relative minor region rather than D.
- In the return, cut the formula to 2 bars and spend the rest on the close (problem 13).

### 7. [P] The prelude has no line: pure arpeggiation in both hands, a two-octave hole between them, and a register above the WTC. **High.**

**Bars:** 1–39.

**Evidence.**
- `critic` tertian fit is 97.5%. The RH has no stepwise motion, neighbour notes or suspensions: b. 1 RH `F#5 A5 F#5 D5 A5 F#5 D5 F#5 F#5 A5 D6 A5 F#5 D5 F#5 A5`.
- Melodic flags: 44 tritone leaps, 38 leaps larger than an octave, 52 compound same-direction leaps.
- The hands are an octave or more apart on 155 of 158 beats (mean 21.8 semitones).
- The RH spends 55% of its notes above B5 and reaches F#7. The LH plays continuous 16ths: 626 notes, against 156 eighths in BWV 850's LH.

**Why it fails.**
- BWV 850's figure is mostly *stepwise* around a pivot note (D E F# | A F# E D …), so it implies a melody. Its LH eighths give the bass air and articulation.
- BWV 846 arpeggiates but hides five-voice voice-leading with suspensions.
- This prelude has a muddy LH, a glassy RH, an empty middle register, and no tune. It is closer to a Czerny etude than to the WTC, which is "too much distance from the idiom".

**Fix.**
- **LH:** use eighths (bass note on the beat plus an inner note), BWV 850-style, in bb. 1–24 and 33–40. Switch to 16ths only for the climb in bb. 25–32, so that the surge is *felt*.
- **RH:** compose a top line first, in quarters and halves (for example b. 1–4: F#5 (G5 A5) | B5 A5 | G5 E5 | G5 F#5, so the 7th of the b. 4 V7 resolves). Make the 16ths a compound figure around it with passing and neighbour tones (BWV 850's pivot-figure model).
- **Register:** move the RH down an octave in A/B/E (about D4–B5), so the hands are within an octave most of the time. Reserve D7–F#7 for b. 28–32 only.

### 8. [F] Episode 3 uses bariolage over an oom-pah bass. **Medium-High.**

**Bars:** 28–31.

**Evidence.**
- S alternates D6 with a descending line, `D6:1 B5:1 D6:1 A5:1 … D6:1 G4:1`. D6 is the top note on all 12 beats of b. 28–30 (`reduce.py`: `^D6` ×12).
- There are 14 consecutive leaps larger than an octave (b. 29.4.75–b. 31.1) plus 6 sevenths.
- The Bass alternates root and fifth in quarters: `G2 D3 G2 D3 | B2 F#3 B2 F#3 | F#2 D3 F#2 D3 | A2 E3 A2 E3`.
- There is one harmony per bar, and Br and Cb are silent (4 voices).

**Why it fails.**
- Bariolage is a string-crossing device (the E-major Partita prelude). In a keyboard fugue's soprano it is not a line.
- The leaps are unplayable at q=108 in one hand.
- The same "fixed top note" device also fills the prelude's bb. 9–12, so the pair repeats itself.

**Fix.** Replace it with an invertible two-voice episode built on the tattoo cell:
- S and A exchange `x:2 x:1 x:1` cells on a descending sequence (G–Em–C–Am?–D7 if heading to G, or toward Em for the new plan).
- The bass moves stepwise in eighths, with Br and Cb in slow suspension lines.
- Two harmonies per bar.
- Keep a held D6 for 2 beats at most as a pedal colour.

### 9. [F] The "PEAK" buries the augmentation in low-register collisions, and its harmony is D almost throughout. **Medium-High.**

**Bars:** 47–50.

**Evidence.**
- The Bass augmentation `A2:8 D3:4 D3:2 D3:2 | F#3:4 F#3:2 F#3:2 A3:8 …` sits directly above the Cb augmented countersubject `A2:4 G2:4 F#2:6 E2:2 | D2:6 …`, which `fugue_v7_bars.py` hand-adjusted with `.replace()`, so it is not an exact augmentation.
- The two collide: A2/A2 unison at the climactic downbeat b. 47.1, G2/A2 second at b. 47.2, parallel unisons at b. 50.2.
- B. 47.1 sounds A2 A2 A3 C#5 A5: four A's.
- The estimator reads b. 47 F#m G D D | b. 48 D D D G, so D on 6 of 8 beats. The soprano statement (A5…) and tenor (lag 9) are both at the D level.
- The apex run (b. 49–50) is arpeggio again: `C#6 E6 A6 F#6 A6 E6 C#6 | D6 F#6 B6 G6…`.

**Why it fails.** An augmentation in the bass should be the moment the subject becomes a *cantus* that the other voices harmonize anew. Here it is just another D-major bar, made muddy.

**Fix.**
- Put the augmentation in the Cb alone (it is the "slow voice"; see problem 4).
- Give the Bass a free eighth-note line at least a 10th above.
- Start the augmentation on **D2 in G major** (the IV climax), or on A1 under a cascade arrival (§5A), so its bar-long notes are *reharmonized*. For example, A1 under A–D/A–Bm7/A–A7: the classic "climax over the dominant" with moving harmony.
- Replace the arpeggio apex with the subject in diminution (§5B).

### 10. [F] The ending is a 9-bar tonic pedal with all entries at D, no subdominant inflection, and a parallel-6th coda. **Medium-High.**

**Bars:** 51–59.

**Evidence.**
- Cb `D2:144` (36 beats, 15% of the piece).
- Both final stretto passes are on the D triad (A-start in S, A, T and B).
- There are no C♮, B♭ or F♮ in b. 51–59.
- B. 57: S/A in parallel 6ths for the whole bar (`D6/F#5, C#6/E5, D6/F#5, F#6/A5, G6/B5 …`). B. 58 has 10ths. T, Br and B play quarter-note chords (`A4 D5 C#5 A4 | …`).
- The bass voice ends on A3 over the Cb D2.

**Why it fails.** Bach's tonic pedals are short (2–4 bars) and *move above themselves*, typically through ♭7 → IV → ii6/5 → V7 → I. A 9-bar pedal plus a homophonic etude coda after a 4-bar D peak means bb. 47–59 are 81% D/A in the bass. That is "too long", "static", and "un-Bach" all at once.

**Fix.**
- Put the final stretto (the BWV 850 quodlibet, §5B) *before* the pedal, over a moving bass.
- The pedal starts at about b. 56 and lasts 3 bars, with C♮ on its second bar (V7/IV → G/D), one B♭ (minor iv over D), then E/D (ii⁶₅ colour) → A7/D → D.
- Give the pedal rhythm (see §5D) instead of 9 tied bars.
- Replace the parallel-6th 16ths with a last head-stretto in S/A/T at 1-beat lags. It does not need to be clean imitation: Bach often ends with fragments.

### 11. [F] Episode 4 is a homophonic, non-thematic texture. **Medium.**

**Bars:** 35–38.

**Evidence.**
- S plays 16th broken chords in 3+3+2 groups: `D6 B5 F#5 D6 B5 F#5 B5 D6 | B5 G5 E5 B5 G5 E5 G5 B5 …`.
- A, T and Cb are in half notes, and the Bass plays broken-chord eighths.
- There is no subject or countersubject material, and Bass/Cb double (problem 4).

**Why it fails.** It is the prelude's texture transplanted into the fugue. The harmony is excellent, but nobody is speaking.

**Fix.**
- Keep the bass progression (Bm–Em | A–D | G–F# | Bm) and the alto suspensions.
- Replace the soprano figure with the subject tail (16ths) imitated by the tenor one beat later a 10th below, with the tattoo answering in the Br.
- The Cb plays a slow syncopated line.
- Result: the same harmony, now made of voices.

### 12. [F] The subject recurs 26 times with no inversion and the same rhythm every time. **Medium.**

**Bars:** whole fugue.

**Evidence.**
- 26 statements, including 6 in the last 9 bars.
- No inversion, no rhythmic variation, one augmentation.
- The tattoo dactyl also saturates the free material: the Ep1 head cells (8×) and the M1 drum bass (7 cells, bb. 17–20).

**Why it fails.** The single most recognisable rhythm is heard about 65 times in 131 seconds (2 per statement plus the free cells). "Too similar" and "plodding" follow.

**Fix.**
- Cut to about 18–20 statements.
- Use the transformations this subject actually offers:
  - **inversion.** The diatonic mirror around A is A–E–E–E–C#–C#–C#–A, a falling *dominant* arpeggio. It is a ready-made "answer", and rectus + inversus at 3 beats is the cleanest combination (cost 5).
  - **diminution.** It gives the BWV 850 rhythm (§5B).
  - **head-only fragments.**
- Never place more than two consecutive entries at the D level.

### 13. [P] The prelude's return is a literal reprise followed by an abrupt stop, with no flourish and no handoff to the fugue. **Medium.**

**Bars:** 33–40.

**Evidence.**
- B. 33–39 is the b. 1–7 formula again.
- B. 39 is V7–I, then b. 40 is `A5:4 D6:12 / D3:4 D2:12`.
- After the b. 29–32 climax the piece rewinds and stops. There is no tonic pedal, no ♭7, and no closing improvisation such as BWV 850's flourish.

**Why it fails.** The strongest music (b. 25–32) is followed by the weakest. The prelude also says nothing about the fugue that follows.

**Fix.**
- Bb. 33–36: a varied return, with the opening tune in the LH (now eighths) and RH figuration above.
- Bb. 37–39: a tonic pedal with C♮ (V7/IV) and one B♭ (minor iv).
- Bb. 40–41: a 32nd-note flourish in BWV 850's manner that ends by stating the **fugue subject in diminution**, `A:2 D:1 D:½ D:½ F#:1 F#:½ F#:½ A:2 | …`, on the final beats, then attacca.

### 14. [P] The tattoo in bb. 17–20 is inaudible, and each of those bars holds one chord. **Medium-Low.**

**Bars:** 17–20.

**Evidence.**
- RH `A5 D6 D6 D6 F#6 D6 D6 D6 …` is in equal 16ths, so the fugue's 8th + 16th + 16th rhythm is not present.
- The harmony is one chord per bar: D | G | Bm | Em.

**Why it fails.** The intended link to the fugue cannot be heard, and the development section is as static as the exposition.

**Fix.**
- Write the tattoo in its real rhythm (`x:2 x:1 x:1`), passed between the hands one beat apart, exactly like the fugue's Ep1.
- Change chord every half bar using Ep1's progression: D–Bm | G–Em | A–D | G–F#m.
- The prelude then rehearses the fugue's best episode.

### 15. [F/P] The register is beyond the WTC compass, and the fugue's playability needs a policy decision. **Medium-Low.**

**Bars:** both pieces.

**Evidence.**
- Fugue soprano: 51% of notes above B5, up to B6.
- Prelude RH: 55% above B5, up to F#7.
- Fugue keyboard check: 55% of onsets need more than two hands.

**Why it matters.** Bach's only six-voice keyboard fugue, the *Ricercar a 6* from the Musical Offering (BWV 1079), is playable by two hands and lies within roughly the WTC compass. Its six voices are audible because they are spaced and frequently rest. The brief allows registers beyond a pianist's reach, but Sam asked for piano-first and less distance from the WTC. High registers on piano also blur six-voice texture.

**Fix.**
- Keep the fugue within about A1–B5 except for one climactic moment.
- Keep inner voices at least a 3rd apart.
- Target 2-hand playability for the episodes. The six-voice tutti can stay "three-handed" if Sam accepts it; ask him.

### 16. [F] The countersubject is a scale filler, plus local blemishes. **Low.**

**Bars:** 3–4 (and every countersubject statement), 26.4.5, 27.4, 48.4, 50.2.

**Evidence.**
- CS bar 1 is a plain eighth-note scale, `E5 D5 C#5 B4 A4 B4 C#5 D5`, that fills the static triad.
- CS bar 2, `E5:3 F#5:1 A5:2 G#5:2 F#5:2 E5:2 D5:2 C#5:2`, runs in parallel 3rds/6ths with the subject's descent.
- Local blemishes:
  - b. 26.4.5: P5 in 16ths S/Br (F#5/B3 → E5/A3)
  - b. 27.4: S C6 (the 7th of D7/F#) leaps *up* to D6 at b. 28.1
  - b. 48.4: alto B4 left unresolved over the bass A3 (`critic` error)
  - b. 50.2: parallel unisons B/Cb

**Fix.**
- CS bar 1: tie a note over the subject's downbeat (prepared 4–3 or 9–8) and add a syncopated passing tone that suggests IV on beat 3.
- CS bar 2: move in **contrary** motion (rising) against the falling tail.
- Fix the four local items as noted.

---

## 5. "Turn it up to 11": opportunities specific to this pair

### A. The circle-of-fifths cascade stretto (the top recommendation)

This fixes problems 1, 2, 4 and 12 at once.

**The idea.** Six entries, one per voice, from the top down, each a **fifth lower** than the last and **one bar** after it. The keys travel **F#m – Bm – Em – A – D – G**, followed by A7 → D. This is the opening exposition reversed in order (top → bottom instead of A, T, B, S, Br, Cb) and in key logic (a moving circle instead of I/V ping-pong). It is also Episode 1's progression grown into a stretto.

```
S   C#5 (F#m)  bar 1–2
A   F#4 (Bm)   bar 2–3
T   B3  (Em)   bar 3–4    tail with C#/D# (melodic minor) so it agrees with the A entry
Br  E3  (A)    bar 4–5
B   A2  (D)    bar 5–6    tail with C♮ (D Mixolydian = V7/IV) to lead to G
Cb  D2  (G)    bar 6–7    → A7 → D
```

**Why it works.**
- Each voice's 2-bar subject lies in exactly one octave, and the six octaves are nested by fifths. Registers are therefore natural: S C#5–C#6, A F#4–F#5, T B3–B4, Br E3–E4, B A2–A3, Cb D2–D3. Every voice gets an exposed entry.
- Each overlap is "scale tail of key k over arpeggio of key k + 1 (= its IV)". That combination is consonant.

**Tested in scratch** (entries only, through `critic.analyse`): **0 parallels, 0 unresolved dissonances, 0 crossings**. The harmony changes every bar.

**How to make it dense.**
- The four voices not carrying the subject carry the countersubject (rewritten per problem 16) and free suspension lines.
- Optionally add the diminution of each new entry one beat later at the lower 3rd (`stretto_finder`: rectus ×½, offset 4, −2 steps, cost 6), so that three forms of the subject sound in every bar.

**Where it goes.** It replaces Stretto III and the old peak (about bb. 39–46 in a re-plan).

**Beyond Bach?** Bach chains entries by fifths in expositions and sequences. A *stretto* whose six entries descend through six keys, one voice each, is a fresh construction in his grammar.

### B. A real entry of BWV 850's subject, with ours in diminution (a quodlibet)

**The data.** BWV 850's subject, taken from the reference MIDI, is:
- a 32nd-note turn: D E F# G F# E F# D
- then dotted pairs B. B | A. G | F#

Token form: `D4:0.5 E4:0.5 F#4:0.5 G4:0.5 F#4:0.5 E4:0.5 F#4:0.5 D4:0.5 B4:3 B4:1 A4:3 G4:1 F#4:4`.

**Results.**
- `stretto_finder --against` says it fits our subject **at offset 0** (cost 5, 0 parallels, 0 harsh), in unison, octave or double octave. Ours at ×2 fits it at offset 8 (cost 5). Ours at ×½ fits it at offset 8 (cost 6).
- **Harmonic bonus:** Bach's B. B lands on beat 2 of our static arpeggio bar. The estimator reads **D | G/B | D/A | D/F#** instead of D–D–D–D. The quotation *cures* the subject's stasis.
- **Three-voice test** (ours 8va in S; ours in diminution at the lower 3rd from beat 2; BWV 850's subject in T): **0 parallels, 0 unresolved, 0 crossings**.
- **Our subject at ×½ speed acquires BWV 850's rhythm:** A:2 D:1 D:½ D:½ … | A:1.5 G:0.5 … D:½ C#:½ B:½ A:½ B:½ C#:½. That gives a dotted 16th + 32nd and a 32nd-note run, the French-overture idiom. So the diminution reads audibly as a quotation: "the fanfare, played in Bach's D-major rhythm". The joke is in the notes, not the title.

**Where it goes.**
- In the fugue, as the final stretto before a short pedal.
- In the prelude's closing flourish, as the diminished subject (problem 13).

Credit BWV 850 in NOTES.md.

### C. A four-speed prolation stretto, beyond *Contrapunctus VII*

*Contrapunctus VII* ("per Augmentationem et Diminutionem") combines its subject at three note values. Here, four speeds are possible without falling back into stasis. The rule is: **put the static half (the arpeggio) only at the fast speeds, and the moving half (the scale tail) at the slow speeds.**
- **×4, tail only, in the Cb:** A G F# E D C# B A B C# D in half notes and quarters. This is a descending-scale "ground", the most Baroque of basses, under which every arpeggio entry is reharmonized: I, IV(9–8), I6, ii, I, V6, vi …
- **×2 in the Bass or Br**, inverted. `stretto_finder`: inversus ×2 at offset 2–4 at the lower 3rd, cost 6, clean.
- **×1 in the middle voices**: rectus and inversus at 3 beats (cost 5).
- **×½ in the soprano**: the BWV 850 rhythm. Inversus ×½ at offset 8 costs 4, the best score of any combination tested.

A 4–6 bar passage like this at the climax is genuinely "more than Bach managed". Each layer has been checked pairwise. The full combination still has to be composed and checked by ear and by `critic`.

### D. A smaller extra: the timpani joke

The M1 "drum" bass (bb. 17–20, tattoo on B and F#) is already a timpani figure. Baroque timpani in D-major works are tuned D/A, and the Christmas Oratorio's first chorus famously opens with solo timpani. So:
- Drop the B/F# drum pedals from M1. They are part of the stasis problem.
- Save the drum for the final 3-bar pedal: the Cb plays the subject's head rhythm on D2 and A1 only, `D2:4 A1:2 A1:1 A1:1 D2:2 D2:1 D2:1 A1:4`, under the moving ♭7–IV–V7 harmony.

The pedal gains rhythm, the D-major festival allusion is audible, and it costs nothing in harmonic motion.

---

## 6. A suggested re-plan

The plan below is a little shorter than now, which suits Sam's "too long" note.

**Fugue** (about 54–56 bars, q=108):

| Bars | Section | Keys / devices |
|---|---|---|
| 1–12 | Exposition. Tonal answers. 1-bar codetta after entry 2. Cb answer overlaps Br by one bar. | D/A. Free voices in suspensions. Each entry has a different bass. |
| 13–16 | Ep1 (keep) + Cb slow line | D–Bm–G–Em–A–D–G–F#m |
| 17–20 | Middle entries | **Bm (T), Em (Br)**, over a moving bass (no drum pedal) |
| 21–24 | Ep2 recomposed (5 voices, tail imitation) | Em–A–D–G descending fifths |
| 25–27 | Stretto I: mirror (rectus + inversus at 3 beats) + diminution | **G**, C♮. Bass G–E \| C–D |
| 28–31 | Ep3 recomposed (tattoo exchange, no bariolage) | G → Em → B7 |
| 32–34 | Stretto II *per arsin et thesin* (lag 7) with inversion | **Em/Bm**, D#, A# |
| 35–38 | Ep4: same harmony, now imitative | Bm descending fifths |
| 39–46 | **Cascade stretto** (§5A), six voices S → Cb | F#m–Bm–Em–A–D–G → A7 |
| 47–51 | **Quodlibet climax:** Cb ×4 tail ground, BWV 850 subject, our ×½ / ×1 / inversion (§5B–C) | D over a moving bass |
| 52–55 | 3-bar tonic pedal (timpani tattoo, §5D), ♭7 / minor iv, head fragments | D, C♮, B♭ |

**Prelude** (about 41 bars):

| Bars | Plan |
|---|---|
| 1–8 | Keep the progression. LH in eighths. RH compound figure around a composed top line, RH an octave lower. |
| 9–16 | A modulating section (A → F#m/Bm), not a transposed copy. |
| 17–20 | Tattoo in real rhythm, passed between the hands. Half-bar chords from the fugue's Ep1. |
| 21–32 | Keep (the 7th chain and the dominant-pedal climax). LH switches to 16ths here only. Top register reserved for b. 28–32. |
| 33–39 | Varied return, with the tune in the LH, then a tonic pedal with C♮ / B♭. |
| 40–41 | Improvisatory flourish in BWV 850's manner, ending with the fugue subject in diminution → attacca. |

After rewriting, re-run `critic.py`, `reduce.py --per beat` and the D/A and pedal measures from §2. Targets:
- pedal beats ≤ 10%
- beats ≥ 90% one triad ≤ 30%
- lowest voice on D/A ≤ 40% overall and ≤ 60% in the final 12 bars
- 0 Bass/Cb unisons or seconds below C3 (except prepared suspensions)

None of these numbers certifies the music, but each one catches a specific fault named above.
