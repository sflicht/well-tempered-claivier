# Pair VIII in E-flat minor: critic's review

Date: 27 Oct 2026. This review comes from the scores only. I did not hear any audio. Sam's listening reports count as the evidence about how the music sounds; the numbers below only locate the problems.

**Scores reviewed**

| Short name | File | What it is |
|---|---|---|
| P-v1 | `work/wtc-work/renders/pairVIII_v3/prelude-viii_v1.json` | French-overture Prelude. Source: `work/wtc-work/pairVIII/prelude.py` |
| P-draft | `editions/complete-cycle/baseline/scores/08-prelude-eflat-minor.json` and `editions/complete-cycle/scores/08-prelude-eflat-minor.json` | 12/8 "Night loom" Prelude: first draft and its second-edition melody revision |
| F-v1 | `work/wtc-work/renders/pairVIII_v1/fugue-viii_v1.json` | 22 bars, nine voices |
| F-v3 | `work/wtc-work/renders/pairVIII_v3/fugue-viii_v3.json` | 32 bars. Generator: `pairVIII/v2/{forms,cp,build}.py`; polish: `v3/polish.py` |
| F-2nd | `editions/complete-cycle/scores/08-fugue-eflat-minor.json` | 69-bar "A narrow stair", which contains the arrival Sam liked |
| F-proc | `work/fugue_viii_passage_revision/08-fugue-passage-revised.json` | 100-bar "The procession finds a dance floor" |

**Tools and baselines**

- `tools/critic.py`, `tools/reduce.py` and `tools/stretto_finder.py`.
- A few read-only scratch probes, described where they are used.
- Bach reference scores: BWV 869 and BWV 878 as JSON, and the BWV 849 and BWV 853 MIDI files.

Bar numbers are 1-based. `b12.3` means bar 12, beat 3.

---

## 0. Verdict in one paragraph

**The subject.** The v2/v3 subject is good, and it is better than the reports say. Its first six notes (E♭–B♭–C♭–B♭–A♭–G♭) are exactly the head of Bach's own D♯-minor fugue subject, BWV 853. That gives the pair a real, audible ancestry, but nobody has credited it or used it yet.

**F-v3 is not a nine-voice fugue.**
- It is a four-voice fugue on nine staves: on average 4.5 voices are moving per bar.
- Two staves never state the subject.
- Its climax is the subject in octaves over block chords.
- It was built by the method that was retired: a chord plan for every beat, a beam-search fill, then mechanical thinning.

**The old procession and Sam's complaint.** I checked whether the old procession's numbers explain "collisions that sound like mistakes", and they do, quantitatively:
- It is crowded in the low register.
- It saturates the scale: five or more pitch classes sound in 47 % of sixteenth-note slices. Bach's five-voice BWV 849 does this in 1.3 % of slices; the nine-voice F-2nd does it in 2.3 %.
- It has 220 same-direction parallel fifths and octaves.

**The Prelude.** P-v1 has a sound harmonic plan, but its inner voices are machine-chosen chord tones re-struck in a stereotyped dotted rhythm. It also throws away the 12/8 Prelude that Sam liked.

**The way forward.**
- Return the Prelude to the Night-loom texture.
- Rebuild the Fugue around a tested nine-voice stretto maestrale. In it, the bass carries the subject at quarter speed: E♭ | B♭ | C♭·B♭ | A♭ G♭ | F D | E♭.
- That bass is the bass route of the arrival Sam liked in F-2nd (E♭ … C♭ … A♭ … F … E♭), now made thematic.

---

## 1. What is good and must be preserved

### 1.1 The arrival Sam liked (F-2nd, bars 45–62)

The Reassessment locates it at q184–216; it sits inside the span below.

| Bars | What happens |
|---|---|
| b45 | VI, then i |
| **b46** | A whole bar of silence |
| **b47–48** | Full nine-voice E♭ minor, with the top voice opening up to B♭6 over an E♭2 bass |
| **b49–50** | C♭ major sounding over the E♭ pedal: the "VI glow" |
| **b51–52** | iv over A♭1 |
| **b53–55** | i |
| b56 | VI (C♭ in the bass) |
| b57 | iv |
| **b58** | A♭°7 (the vii°7 chord) with the soprano peak F7 |
| **b59** | F°7 with D7 on top |
| b60–61 | V |
| b62 | i |

**Keep three things:**
1. The silence-then-full-sonority pacing.
2. The registral opening.
3. The harmonic route i – ♭VI – iv – vii°7 – V – i, with the soprano reaching its peak over the diminished seventh.

**Do not keep the inner writing.** In b47–50 the lowest voice holds E♭2 for 16 beats, and voice 3 alternates G♭/E♭; this is what Sam meant by "harmony rather than counterpoint".

§3 shows how to rebuild the same route as nine real lines.

### 1.2 The v2/v3 subject, answer and countersubject (`pairVIII/v2/forms.py`)

**The subject:** E♭4 B♭4 | C♭5 (dotted 8th) B♭4 (16th) A♭4 G♭4 | F4 D4 E♭4. In wtclib tokens: `Eb4:4 Bb4:4 Cb5:3 Bb4:1 Ab4:2 Gb4:2 F4:2 D4:2 Eb4:4`.

Why it works:
- It has a recognisable head: a rising fifth, then a sigh.
- It implies clear harmony (i – iv – V – i).
- It is singable.

It is also unusually stretto-friendly. Every placement below gives 0 parallel errors and 0 unresolved dissonances in the critic. I re-ran them with corrected diatonic code; see problem 14.

| Second voice enters with | Starting on | Delay after the subject | Where |
|---|---|---|---|
| Tonal answer | B♭ | 4 beats | — |
| Inversion at the 5th | B♭3, a 4th below | 1 beat (a "mirror pair") | — |
| Subject | octave below | 3 beats, or an off-beat 2½ | — |
| Inversion | E♭5 | 3 beats | — |
| Inversion at the 5th in augmentation (I5×2) | B♭ | — | against the subject in double augmentation |
| Major-mode subject in augmentation (SM×2) | G♭ | — | against the subject in double augmentation |

**Keep:**
- The tonal answer (B♭–E♭ mutation) used in b3.
- The countersubject (CS1). It enters off the beat with 16ths, then falls as a scale, so it moves where the subject holds.
- The clean three-voice opening of F-v3, b1–10. The critic finds 0 errors there.

### 1.3 F-v3's deceptive cadence (b25–27)

The sequence Fb (Neapolitan) → iiø7 → V7 → **deceptive C♭**, then the subject **subito pp in C♭ major** with only three voices, is a good dramatic idea. Keep it, but compose it properly (see problem 11).

### 1.4 F-v1: proof that nine lines can move

- Its exposition accelerates: each new subject is chased by the inversion one beat later (b5–7).
- Its build-up is a chain of entries every half bar, each a fifth higher (b13–14).
- It reaches nine genuinely moving voices in b15–16 and b19–22.

The material and voice-leading were rough (24 unresolved dissonances), but the accelerating exposition and the rising chain are worth reusing with the cleaner subject.

### 1.5 F-proc: techniques worth keeping, not material

**What to keep:**
- The "three-beat retort", a short figure derived from the subject, relayed at unequal distances across barlines. It runs at beats 80, 82.5, 85, 88 and 91 (b21–23) in clarinet, violin, cello, viola and horn.
- Entries that hurry one beat behind each other (b53).
- Inversions that answer two beats later (b57).

These are how an episode can pass initiative between voices without padding.

**What not to keep:** the chant/dance material, the modal language and the chamber scoring. These belong to the experiment; they are not the WTC-idiom Fugue VIII.

### 1.6 The Prelude

**P-draft (12/8 "Night loom"), the one Sam liked.** Keep:
- The separation of time scales: a slow, narrow cantabile over continuous inner eighths.
- The falling-and-returning arc. In the second edition this is b1–2: B♭–A♭–G♭, then G♭ embellished, reaching A♭ and returning.
- The held A♭ across the harmony change at b10–11.
- Its texture is the cycle's closest relative to BWV 853's arioso over repeated chords.

**P-v1 (French overture).** Its *harmonic plan* is sound (tertian fit 92 %, 0 parallel errors, 0 unresolved). Keep these pieces of it:

| Bars | What to keep |
|---|---|
| b8 | The quiet G♭-major arrival, held |
| b9–12 | The secondary-dominant circle (C♭, A♭m, F7, B♭m, E♭7, A♭m) |
| b13–14 | The deceptive cadence: i6/4 – V7 – VI – iv6 |
| b15–16 | The half cadence, which leads straight into the Fugue (attacca) |
| b4, b8, b15 | The 32nd-note tirades, as gestures |

---

## 2. Things that don't work, ranked

| # | Piece | Bars | Problem | Severity |
|---|---|---|---|---|
| 1 | F-v3 | whole | Nine voices are not real (4.5 moving per bar; Bar and B2 never state the subject) | Critical |
| 2 | F-v3 | b25–26 | The climax is homophony: subject in octaves over block chords, with an octave-doubled bass | Critical |
| 3 | F-proc | b11–60, b81–100 | The collisions Sam heard: low-register 2nds/9ths, scale clusters, 220 parallels | Critical (must not recur) |
| 4 | F-v3 | b9–31 | Retired method; the free voices are beam-search filler, fragmented by polishing | High |
| 5 | F-v3 | b22–24, b28–31 | Static stretti: entries at the octave on one pitch level, a 16-beat tonic pedal, 76 % of statements on E♭/B♭ | High |
| 6 | F-v3 | every entry | The subject closes with a cadence on beat 2 and has the same rhythm every time → plodding | High |
| 7 | P-v1 | whole | It discards the 12/8 Prelude Sam liked | High |
| 8 | P-v1 | b2–15 | Inner voices are algorithmic chord tones re-struck in a dotted rhythm | High |
| 9 | P-v1 | b2, b4, b10–13 | The top line is jagged, built from chord tones, with one rhythm cell throughout | Medium |
| 10 | Pair | — | The Prelude–Fugue link is broken, and the BWV 853 allusion is neither credited nor used | Medium |
| 11 | F-v3 | b26–28 | The C♭-major subito pp is a 1½-bar block shift with no pivot | Medium |
| 12 | F-v3 | b31–32 | The final approach zigzags (B5–F6 tritone, D♭6–D6 chromatic); the bass mud in b25 | Medium-Low |
| 13 | P-v1 | whole | 47 % of onsets exceed two hands; the bass leaps an octave on every half bar | Low-Medium |
| 14 | tools | — | `stretto_finder.py` puts some notes an octave off in E♭ minor | Medium (process) |
| 15 | F-proc | whole | Too long, harmonically samey, modal; far from the WTC idiom | Medium (retired) |

### 1. F-v3 is not a nine-voice fugue (Critical)

**Evidence.**
- The critic's texture row shows the subject-carrying staves bar by bar: `..A......` in bars 1–2, mostly 3–5 letters in bars 3–24. All nine moving staves appear only in b32, the final chord.
- Mean moving voices: 4.5.
- The exposition has five entries: A1 b1, S2 b3, T1 b5, S1 b7, B1 b9.
- T2 first states the subject at b18 and A2 at b19.
- **Baritone and Bass II never state the subject.**
- Bass II has 12 notes in 32 bars: the climax doubling, a pedal and the final chord. Baritone, A2 and T2 have about 50 notes each, while A1 has 192.
- The v2 report admits "nine-voice palette used sparingly as registers".

**Why it fails.** The pair exists to deliver nine-voice counterpoint. A four-voice fugue with occasional extra doublings is exactly the "harmony rather than nine-part counterpoint" verdict again.

**Fix.** Recompose using the plan in §3:
- All nine voices enter with the subject or answer in an exposition of bars 1–12.
- Every staff states the theme at least twice.
- The climax is a nine-voice stretto maestrale.

### 2. The climax is homophony (Critical)

**Evidence.**
- b25.2: the critic reports a doubling run S1/A1 P8 ×8, i.e. the subject in octaves.
- b25.2: also a doubling run B1/B2 P8 ×5, with the bass in octaves down to E1/Fb1.
- The other voices strike block chords in the subject's rhythm. `build.py` labels this "PEAK … homophonic massing … Beethoven-style block statement".

**Why it fails.** This is the precise failure Sam named. The loudest moment of the piece has the fewest independent lines.

**Fix.**
- Delete b25–26 as written.
- Keep their harmonic idea, Fb → iiø7 → V7 → deceptive VI, as the *destination* of lines.
- Put the climax in the stretto maestrale (§3.4). There the bass is the subject in double augmentation, and the vii°7/V/VI colours arise from the entries themselves.

### 3. F-proc: the collisions that "sound like mistakes" (Critical, explanatory)

The critic numbers, and a register probe I wrote, point the same way.

**Counts against Bach.**

| Measure | F-proc | Comparison |
|---|---|---|
| Same-direction parallel 5ths/8ves | 220 (139 P8, 81 P5) | — |
| Doubling runs | 47 | — |
| Unresolved dissonances | 195 (157 unprepared and unresolved) | — |
| Unresolved dissonances with a note below C3 | 82 | — |
| 2nds, 7ths and 9ths struck with the lower note below C3 | **231** | BWV 878: 9; BWV 869: 2 |

**Register crowding.**

| Measure | F-proc | BWV 878 | F-2nd |
|---|---|---|---|
| Average voices sounding below G3 | 2.6 | 1.16 | — |
| 16th slices where two adjacent voices below G3 are only a 2nd apart | **22 %** | 1.3 % | 0.3 % |

**Pitch-class saturation** (share of 16th slices).

| Pitch classes sounding at once | F-proc | BWV 849 (5 voices) | F-2nd (9 voices) |
|---|---|---|---|
| 5 or more | **47 %** | 1.3 % | 2.3 % |
| 6 or more | **17 %** | 0 % | 0 % |

Its tertian fit is 14.8 %.

**Examples of collisions:**
- b20.3: D2 (double bass) under D♭3 (horn) and C♭3 (cello). D against D♭ in the bottom octave, with a C♭–D♭ second on top.
- b20.4: B♭1 against a held C♭3, a minor 9th.
- b11.1: C♭3 against B♭1, again a minor 9th.

**Examples of doubled streams:**
- In b81–100 there are 89 parallel errors.
- At b96.1 four pairs move in octaves or fifths at once (Bsn/Db P8, Fl/Cl P8, Ob/Hn P5, Vla/Vc P5): nine parts moving as about four doubled chord streams.

**Why it fails.** Low 2nds and 9ths blur, scale clusters cancel any sense of harmony, and parallel streams make the texture sound like doubled chords. A listener hears wrong notes, not suspensions.

**Fix.** Treat these as acceptance gates for the new fugue (listed in §3.6):
- 0 parallel errors.
- At most two voices below G3 except at cadences.
- No unprepared 2nd or 9th between the two lowest voices.
- Never six pitch classes at once, and five in under 3 % of slices.

### 4. F-v3 uses the retired method, and polishing fragmented the lines (High)

**Evidence: the method.**
- `v2/build.py` writes a chord for every one of 128 beats (the `CH` string).
- `cp.fill()` beam-searches the free voices from those chords.
- `v3/polish.py` then deletes "doubling" notes in the middle of phrases. `polish_log.txt` shows this, e.g. T1 at t = 32.5–37.5 and B1 at t = 64–67.5. It also shortens every free note to 75 %, and nudges notes by 1–5 semitones to satisfy the checker.

**Evidence: the result.**
- **41 of the 91 phrases in F-v3 last 1.5 beats or less (45 %).**
- For comparison: F-v2 has 0 of 27, BWV 878 has 0 of 25, BWV 869 has 2 of 27.
- Examples of one- to three-note blips: T2 b20–24, T1 b21–24 and b28, A2 b30–31, B1 b19–22. For instance, B1 at b21 plays A2 B♭2 A♭2 G♭2 G2 and then stops.
- 19 note lengths are off the 16th grid (0.9375 ×14, 1.125 ×4, 1.875 ×1), which forces 64th-note notation.

**Why it fails.** Isolated blips in inner voices sound like stray notes, which is one more source of "mistakes". The process also contradicts CONVENTIONS ("No code may choose pitches to fill voices").

**Fix.**
- Discard every free note of F-v3.
- Write all non-thematic material literally in wtclib bar strings, derived from CS1, the sigh (C♭–B♭ dotted) and the tail retort (A♭–G♭–F–D–E♭).
- Gate: no free phrase shorter than 2 beats.

### 5. Static, samey stretti and tonic saturation (High)

**Evidence.**
- Of 17 complete statements, 13 sit on the E♭ or B♭ level: E♭ ×8, B♭ ×5. G♭, D♭, A♭ and C♭ appear once each.
- **Stretto II** (b22.1, b22.4, b23.3) has three entries, all on B♭, in S2/S1/B1, at three-beat distance in octaves. It is a canon at the octave, and the harmony repeats every three beats.
- **The final stretto** (b28.1, b28.4, b29.3) has three E♭ entries over an E♭2 pedal held 16 beats (b28–31).

**Why it fails.** This is Sam's "long passages too similar harmonically" in miniature. Octave stretti cannot change the bass, so the closer the entries, the more static the harmony.

**Fix.**
- Use the stretto intervals that move the harmony (all verified; see §1.2): answer at four beats, mirror pair (subject + inversion at the 5th) at one beat, inversion at three beats, the octave only at 2½ beats.
- Cut the tonic pedal to at most 2 bars, at the very end.
- Put the long-range bass motion into the double augmentation (§3.4).

### 6. The subject closes, and its rhythm never varies (High)

**Evidence.** The subject ends with F–D–E♭, a V–i cadence that lands on beat 2 of its second bar.

All 17 statements have the identical rhythm: quarter, quarter | dotted 8th, 16th, 8th, 8th | 8th, 8th, quarter. There are no off-beat entries, no diminution and no augmentation; v2 says "No canons, inversions or augmentations". The tempo is ♩ = 72.

**Why it fails.** Each statement stops in its own tonic, and the next entry restarts on a downbeat. The diagnosis criticised exactly this ("a rounded shape and emphatic closure give the next voice little urgent unfinished business"). The result is the stop-start "plodding".

**Fix.**
- Keep the pitches.
- Shorten the last E♭ to an 8th, *elided* into the countersubject's off-beat 16ths, so the line never stops.
- Space the first four entries **six beats apart** instead of eight. Entries then alternate between beat 1 and beat 3.
- Use diminution (16ths) in episode 2 and augmentation from the middle section on.
- Tempo ♩ = 80.

### 7. P-v1 discards the Prelude Sam liked (High)

**Evidence.**
- Sam's positive reference is the 12/8 "Night loom" (P-draft); see COMPOSITION_BRIEF and the Reassessment's "what to retain".
- P-v1 shares nothing with it but the key: a different metre, texture, melody and genre.
- The v1 report justifies the change only as a contrast with other pairs.

**Why it fails.** The brief says to "preserve these as positive reference pieces" and to develop them selectively. Replacing the piece is the opposite of that.

**Fix.** Re-found Prelude VIII on the Night-loom texture (§3.7):
- Keep its time-scale separation and the falling-and-returning arc.
- Graft in P-v1's best harmonic events: the G♭ arrival (P-v1 b8), the deceptive cadence and the attacca half cadence (P-v1 b13–16), with a single tirade as the door into the Fugue.

### 8. P-v1 inner voices are chord-tone pumping (High)

**Evidence.**
- `prelude.py`, lines 25–48, chooses inner-voice pitches from the chord's pitch classes by minimising a cost. This is the retired chord-tone solver in miniature.
- Each half bar re-strikes the same pitch as a dotted-8th + 16th pair.
- Haute-contre plays only E♭5 and D♭5 for b9–12: 16 strikes.
- Taille re-strikes E♭4 eight times in b11–12.
- Quinte stays on B♭3 and C♭4 through b11–12.

**Why it fails.** The voices are rhythm, not lines. A real French overture moves its inner parts in the dotted rhythm and passes tirades between voices. Here only the Dessus moves.

**Fix.** If any of P-v1 is kept, hand-write the inner parts as lines with their own suspensions, and pass the tirades among Haute-contre, Taille and Basse. Better: adopt the fix for problem 7, which removes the problem.

### 9. P-v1 top line: jagged chord-tone line, one rhythm (Medium)

**Evidence.**
- b2 and b4 repeat the same figure: A♭5–C♭6–D5–F5–B♭5, which drops a diminished 7th and then leaps a 6th.
- b10: a tritone E♭5→A5. b12: a tritone F6→B5. b13: an augmented 2nd D6→C♭6.
- The cell "dotted quarter, 8th, dotted 8th, 16th, quarter" fills b1, b2, b5 and b6, and its half-bar form fills most of the rest.

**Why it fails.** The line arpeggiates whatever chord is underneath and never sings a phrase. The repeated cell, at ♩ = 48, makes 80 seconds feel static.

**Fix.** In the Night-loom rebuild, write a stepwise cantabile line seeded by the subject's retrograde inversion (§4c). Keep at most one diminished-7th drop, as an expressive peak.

### 10. The Prelude–Fugue link is broken, and the BWV 853 allusion is unused (Medium)

**Evidence.**
- P-v1's opening cell E♭–G♭–F–E♭ was the head of the **v1** subject. The v3 subject (E♭–B♭–C♭…) has no connection to the Prelude.
- The v3 subject's first six notes are BWV 853's subject: Bach's D♯–A♯–B–A♯–G♯–F♯, spelt in E♭ minor as E♭–B♭–C♭–B♭–A♭–G♭. None of the v2 or v3 reports mention it.

**Why it fails.** The pair has a strong built-in allusion and is wasting it. An unacknowledged borrowing also violates the ARTISTIC_DIRECTION's request for accurate credit.

**Fix.**
- Credit BWV 853 in NOTES.md.
- Make the allusion audible: Bach's complete subject enters at the end (§4b).
- Let the Prelude's last bars present the head E♭–B♭–C♭–B♭ in the bass as the attacca.

### 11. The C♭-major subito pp is under-composed (Medium)

**Evidence.**
- The A2 statement in C♭ major lasts 6 beats (b26.3–b27.4).
- At b28.1 the music jumps straight to E♭ minor and the tonic pedal, with no pivot. The v2 report itself calls it "possibly abrupt".

**Why it fails.** A surprise needs an aftermath. Here the surprise reads as a splice.

**Fix.**
- Give C♭ major two bars: the subject plus CS1 plus one bass line, three voices.
- Return through A♭ minor, the iv chord, which shares C♭ (C♭ → A♭m → vii°7 → V).
- Prepare it by letting the stretto maestrale pass through C♭ (its bar M3).

### 12. The ending, and bass mud (Medium-Low)

**Evidence.**
- At b31 S1 plays B5–F6 (a tritone leap) then E♭6 B5 D6 D♭6 D6 D6 into a G6 reached by a leap.
- At b25 B2 doubles B1 at the octave down to E1/F♭1, about 41 Hz, under a root-position Neapolitan.

**Fix.**
- Approach the Picardy G by step (F6–G6), or end the top voice on B♭5.
- Keep the lowest voice at or above B♭1.
- Never octave-double the bass inside a contrapuntal texture.

### 13. P-v1 is unplayable at the keyboard, with a pumping octave bass (Low-Medium)

**Evidence.**
- 52 of 110 onsets (47 %) exceed two hands; for example b2.1 sounds A♭2 A♭3 E♭4 B4 A♭5 at once.
- The bass leaps an octave on every half bar in b2–15; the critic flags 8 leaps larger than an octave.

**Fix.** The Prelude, unlike the Fugue, should be playable. In the rebuild:
- Keep the texture within two hands.
- Write a bass that walks; a descending tetrachord in the middle section is one option.

### 14. Tool bug: `stretto_finder.py` diatonic octave wrap (Medium, process)

**Evidence.**
- `diatonic_shift` and the diatonic `transform` sort the scale from the tonic, but they compute the octave from C. In E♭ minor this misplaces every D by an octave.
  - `diatonic_shift(62,1,Eb-minor)` returns 75 instead of 63.
  - B♭4 + 2 steps gives D4, not D5.
  - The subject's inversion ends …C♭4 **D3 F3** E♭4.
- Results for inversion and non-octave transpositions are therefore unreliable here: they show phantom leaps, and fourths and fifths get swapped.
- Diatonic "steps" in harmonic minor also produce modal hybrids, not tonal entries. For example, +2 steps gives G♭ D E♭ D C♭ B♭ A♭ F G♭, not a G♭-major entry.

**Fix.** These are tool changes, made as a separate task:
- Compute the octave relative to the tonic: `base+(idx//7)*12+(scale[idx%7]-base)%12`.
- Allow *chromatic* key transposition with major/minor variants of the subject.

My probes used a wrapper with this correction and did not modify the tool.

### 15. F-proc as a whole (Medium; it is already retired)

**Evidence.**
- 100 bars, about 3:42.
- The bar-level reduction stays on E♭ minor or B♭ through most of b10–24 and again b45–60.
- The modal Dies irae and dance language has a tertian fit of 14.8 %.

**Why it fails.** It matches Sam's points 4–6 (too similar harmonically, too long, too far from the WTC). It is the source of techniques worth reusing (§1.5), not of material.

**Fix.** Do not continue the concise 60-bar revision as Fugue VIII. Mine it only for the retort and relay techniques.

---

## 3. Plan: a genuinely nine-voice Fugue VIII that is still clear and singable

### 3.1 Premise

Bach's three-voice BWV 853 combines a subject with its inversion and its augmentation.

**The idea.** Fugue VIII teaches nine voices one subject at **four speeds and two directions**:
- Speeds: diminution in 16ths, normal, augmentation ×2, augmentation ×4.
- Directions: rectus (as written) and inversus (inverted).

The procession ends when **the bass itself becomes the subject at quarter speed**. Under it, every other voice enters, rectus and inversus, in stretto.

**The arrival.** The bass of that augmentation, E♭ | B♭ | C♭·B♭ | A♭ G♭ | F D | E♭, *is* the bass route of the arrival Sam liked: i … ♭VI … iv … vii°7 over F … i. That arrival becomes the consequence of the counterpoint instead of a block of harmony.

### 3.2 Material

All non-thematic notes are hand-written. Code may only transpose, invert or augment authored lines.

| Name | Notes (from E♭) | Role |
|---|---|---|
| **S**, subject | E♭ B♭ C♭· B♭ A♭ G♭ F D E♭ (final note shortened to an 8th, elided) | Theme |
| **A**, tonal answer | B♭ E♭ G♭· F E♭ D♭ C A B♭ | Answer |
| **I**, inversion | E♭ A♭ G♭· A♭ B♭ C♭ (or C♮ when rising) D F E♭ | Rectus/inversus pairs |
| **I5**, inversion at the 5th | B♭ E♭ D· E♭ F G♭ A♭ C♭ B♭ | Diatonic in E♭ minor and ends on the dominant: the "inverted answer" |
| **SM / IM** | Major-mode forms for G♭, D♭ and C♭ | Middle entries |
| **S×2, I×2, I5×2** | Augmentation | The slow "long breath" voice, a rate between normal and ×4 |
| **S×4** | Double augmentation (24 beats) | Climax bass |
| **S×½** | Diminution in 16ths (1½ beats) | Episode 2 "dance", the humour |
| **CS1** | v2 countersubject: 8th rest, B♭ A♭ (16ths), G♭ F E♭, C♭ B♭ A♭, G♭ F | Motor |
| **m1 sigh** | C♭–B♭, dotted 8th + 16th | Episodes, suspension chains |
| **m2 retort** | A♭–G♭–F–D–E♭ (2 beats) | Episode relays at unequal distances (the F-proc technique) |

### 3.3 How nine voices stay alive without padding

**Roles.** At any moment each voice has one role:
- **Theme**: S, A, I or I5 at normal speed.
- **Long breath**: ×2 or ×4, or a suspension chain built from m1.
- **Motor**: CS1, diminution, m2.
- **Rest.**

The roles rotate. Every staff, *including Baritone and Bass II*, states the theme at least **three** times in the piece, with at least one inverted and one augmented statement among the lower five.

**Density.** Outside the maestrale: at most four themes at once, one long-breath voice and one or two motors. Inside the maestrale: up to six themes at once.

**Rests.** Each voice rests about 20–35 % of the time, in rests of at least one bar, and re-enters on thematic material.

**Prohibitions:**
- Held notes longer than 2 bars, except a ×4 statement or the last two bars.
- Repeated-note pumping.
- Chord-tone redistribution.
- Doubling any voice at the octave, except the single chord at b37.1.

**Register.** Bass II stays between B♭1 and E♭3. At most two voices sound below G3 except at cadences. The two lowest voices stay at least a 5th apart below C3, unless one holds a prepared suspension.

### 3.4 Bar map (50 bars, 4/4, ♩ = 80, about 2′30″)

| Bars | Section | Keys | Voices | Content |
|---|---|---|---|---|
| 1–12 | **Exposition, accelerating** | e♭ | 1 → 9 | See the entry list below |
| 13–15 | Episode 1 | e♭ → G♭ | 5 | m2 retort relayed down through 5 voices at 3, 2½ and 3½ beats; m1 sigh chain in the long-breath voice; cadence in G♭ |
| 16–21 | Middle entries I | G♭, D♭ | 5–7 | SM (S2, b16.1) + IM a 3-beat stretto (A1, verified clean); SM-answer in D♭ in B1 at +3 (verified); **first augmentation**: Baritone SM×2 (b19–21) under normal-speed SM/IM in S1/T1; CS1 continuous; cadence in b♭ |
| 22–24 | Episode 2 ("the dance") | b♭ → a♭ | 4 | S×½ in 16ths, tossed between S1, B1 and A2 at unequal distances (a running joke that briefly takes over); light |
| 25–30 | Middle entries II | a♭, b♭ | 7–8 | B1 S×2 in a♭ (b25–27) with S in a♭ above and S in e♭ a 5th up at 3 beats (verified), then at 2½; T2 I×2 in b♭ (b28–30) with mirror pairs at 1 beat; distances shrink from 6 to 3 to 2½ to 1 |
| 31–35 | **Approach** | → V | 9 → 1 | Bass rises G♭2 (b31), A♭2 (b32), A♮2 (vii°7/V, b33), B♭2 (b34–35). Nine *heads* (first 2¾ beats: E♭–B♭–C♭·B♭, alternating rectus and inversus) climb from B2 to S1 at one-beat distance (b31.1–b33.1), using F-v1's rising chain. Voices then drop out one by one until S1's D6 is left alone at b35.4 |
| **36** | **General pause** | — | 0 | F-2nd's b46 silence |
| **37–42** | **Arrival and stretto maestrale** | e♭ | 9 | b37.1: the only block chord in the piece, a wide nine-voice E♭-minor sonority with B♭5/E♭6 on top. **Every note is the first note of a line.** Bass II's E♭2 begins S×4. Then the skeleton in §3.5 follows. Harmony: i (b37), V (b38), ♭VI–V (b39), iv–i6 (b40), **vii°7 over F with the soprano peak, then V6 (b41)**, i with a common-tone °7 (b42). Climax at b41.3 |
| 43–44 | Aftermath | C♭ | 3 | V7 → **deceptive ♭VI**, subito pp. SM in C♭ (A2) with CS1 (S2) and one bass line. F-v3's idea, now prepared by b39 |
| 45–47 | Return and guest | e♭ | 7–9 | Via A♭m (iv) and vii°7. **BWV 853's own subject** in T1, with our S×2 an octave above in S2 entering 3 beats later (verified 0/0). B2 has the subject's retrograde inversion ×2 (= the Prelude's melody, §4c). CS1 and m1 fill the rest |
| 48–50 | Coda | e♭ → E♭ | 9 → 1 | Heads in stretto over at most 2 bars of tonic pedal; iv – vii°7 – V – I (Picardy, as BWV 853's fugue ends major). Lines finish at different moments: bass b49.1, inner suspensions b49.3 and b50.1, soprano b50.1 |

**Exposition entry list (b1–12).** The voice and beat columns come first so the order is easy to follow.

| Entry | Voice | Starts | Form and pitch | Distance from previous |
|---|---|---|---|---|
| E1 | A1 | b1.1 | S on E♭4 | — |
| E2 | S2 | b2.3 | A on B♭4 | 6 beats |
| E3 | T1 | b4.1 | S on E♭4 | 6 beats |
| E4 | B1 | b5.3 | A on B♭2 | 6 beats |
| (codetta) | — | b7.1–2 | m1 | — |
| E5 | A2 | b7.3 | S on E♭4 | Mirror pair with E6 (verified 0/0) |
| E6 | Bar | b7.4 | I5 on B♭3 | 1 beat |
| E7 | S1 | b9.3 | I on E♭5 | — |
| E8 | T2 | b10.3 | A on B♭3 | 4 beats (verified 0/0) |
| E9 | B2 | b11.3 | S on E♭2 | The ninth voice enters at the bottom |

- I ran the critic on these nine entries alone, with no free voices: 0 parallels, 0 unresolved and 0 crossings.
- CS1 accompanies every entry from E2 on.
- Voices that have finished their entry continue with CS1 or m1, or rest.
- The exposition closes with a cadence at b13.1.

### 3.5 The stretto maestrale skeleton (b37–42), tested

M1 = b37, M2 = b38 and so on; beats are counted from b37.1 = 0. I built only the thematic lines and ran the critic on them.

| Voice | Form | Speed | Starts | Pitch |
|---|---|---|---|---|
| **B2** | S | ×4 | M1.1 | E♭2 (to M6.4) |
| S2 | S | ×1 | M1.2 | E♭5 |
| A1 | I | ×1 | M1.3 | E♭5 |
| S1 | I | ×1 | M1.4 | E♭6 |
| **Bar** | I5 | ×2 | M2.1 | B♭3 (to M4.4) |
| T2 | S on B♭ (real answer) | ×1 | M2.4 | B♭3 |
| A2 | S | ×1 | M3.1 | E♭4 |
| **B1** | SM (G♭ major) | ×2 | M3.2 | G♭3 (to M6.1) |
| T1 | S | ×1 | M4.2 | E♭4 |
| T2 | I | ×1 | M4.4 | E♭4 |
| S1 | S on B♭ | ×1 | M5.1 | B♭5 (peak G♭6 at M5.3) |
| A1 | S on B♭ | ×1 | M5.3 | B♭4 |

**What the critic reports on this skeleton:**
- 12 statements in 9 voices over 6 bars, covering rectus, inversus, inversion at the 5th, ×2 and ×4.
- **0 parallel errors, 0 weak parallels, 0 doublings, 0 unresolved dissonances, 1 voice crossing.**
- 5–6 themes sound at once from beat 4 to beat 20.
- The reduction reproduces the liked route:
  - M3: C♭ (♭VI).
  - M5.2: F–A♭–C♭–D under F6, which is F-2nd's b59 sonority.
  - M6: E♭ with the common-tone A♮/C♮ diminished seventh before the cadence.

**What still needs composing:**
- 13 "7th not resolved down" notes at M2.2–2.4, M4.1 and M6.1. The 3–4 free voices or small rhythmic shifts should resolve them.
- Five low 2nds and 9ths: T2's B♭-level answer (A3/C4 against B♭2 at M3.3–M4.1) and G♭3 against F2 at M5.2. I tested moving that first B♭ answer up an octave into T1 at M2.3. It cut the low clashes to one, but it added one parallel and two unresolved dissonances, so it is the composer's call.
- The 3–4 non-thematic voices at each moment take CS1 fragments and m1 suspensions, written by hand.

### 3.6 Acceptance gates (checks that remove mistakes; they do not make the music good)

- `critic.py` must show:
  - 0 `parallels_error`.
  - At most 5 `UNRESOLVED` across the piece, each justified in NOTES.md.
  - Doubling runs only at b37.1.
- In b37–42 the texture row must show at least 7 moving voices per bar, no `=`, and all nine letters.
- No free phrase of 1.5 beats or less (the F-v3 fragment check).
- 5 or more simultaneous pitch classes in under 3 % of 16th slices; never 6.
- At most two voices below G3 outside cadences.
- Every staff states the theme three or more times. Bar and B2 each have at least one ×2 or ×4 statement plus two at normal speed.
- The free voices are literal bar strings: no `fill()` and no `polish.py`.
- Piano rendering first, then a check that each line can be heard. Then Sam listens.

### 3.7 Prelude VIII rebuild, briefly

- 12/8, the Night-loom texture, about 24–28 bars, playable with two hands.
- **The melody is the subject's retrograde inversion in long values: E♭ F D C♭ B♭ A♭ G♭ A♭ E♭.** Its segment B♭–A♭–G♭–A♭ *is* the liked falling-and-returning arc.
- The inner eighths change their broken-chord shape every 2–4 bars. Their patterns sometimes adopt m1 (C♭–B♭) and CS1's rhythm, and they suspend across harmony changes.
- The bass walks: a lament tetrachord in the middle section, then a chromatic rise to V.
- The harmonic events come from P-v1: G♭ arrival, circle of fifths, then i6/4–V7–VI–iv6–V.
- The last bar is a single tirade and the bass head E♭–B♭–C♭–B♭, leading attacca into the Fugue's solo alto.

---

## 4. "Turn it up to 11" opportunities

### (a) A nine-voice stretto maestrale: four rates, both directions, all at once

**What BWV 853 does.** Bach's three voices combine the subject in stretto, inversion and augmentation.

**What this adds.** The skeleton in §3.5 does all of that at once, with nine voices and three rates: ×4 bass, ×2 inverted in the Baritone and ×2 major in Bass I, and normal-speed rectus and inversus above.

**Optional extra.** Add a fourth rate in the free S1 or S2 voice at M5: S×½, the episode-2 "dance" in 16ths, which is the joke returning at the summit. This still needs verifying.

**Why it is audible.**
- The listener has learned each rate separately: augmentation at b19 and b25, diminution at b22, the mirror pair at b7.
- The bass's slow E♭ | B♭ | C♭ is unmistakable once the GP has cleared the air.

It is tested clean at the skeleton stage.

### (b) Bach's own subject as a guest

**The move.** At b45–47 T1 states BWV 853's complete subject in E♭-minor spelling:
`Eb4:4 Bb4:6 Cb5:2 Bb4:2 Ab4:2 | Gb4:2 Ab4:2 Bb4:4 Eb4:4 Ab4:6 | Gb4:2 F4:4`
Our subject enters in augmentation an octave above, three beats later. The critic finds 0 parallels and 0 unresolved dissonances, with low roughness.

**What the listener hears.** The two subjects share six notes and then part, Bach's continuing where ours cadences. So the listener discovers in real time that our subject was Bach's all along.

**Other verified combination:** Bach's subject at normal speed over our ×4 bass, entering 2 beats in, gives 0 parallel errors and 0 unresolved.

Credit it in NOTES.md.

### (c) The pair as a palindrome

**The idea.** The Prelude's melody is the Fugue subject's retrograde inversion (§3.7), and the Fugue's bass brings that melody back in augmentation in b45–47.

**Tested combinations:**
- Retrograde inversion ×2 in the bass against the inversion at the 5th entering 5 beats later: 0/0.
- The same bass against the subject entering 1 beat later: 0/0.

**What the listener hears.** The pair ends by playing its opening backwards and upside down underneath its own subject. The Prelude's last bass gesture, E♭–B♭–C♭–B♭, is the subject's head, so each piece contains the other's seed.

---

### Appendix: reproducing the probes

The probes are read-only scratch scripts and are not in the repo. They use `tools/critic.py` `analyse()` on lines built from the forms in §3.2, starting at the beats in the §3.5 table. Chromatic transposition was used, and the inversion was computed relative to the tonic (see problem 14).

The pairwise checks reuse the roughness measure from `stretto_finder.py`. Rebuild the §3.5 skeleton in `cycle/08-e-flat-minor/fugue.py` as authored lines before adding any free voice.
