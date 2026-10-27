# Pair X in E minor: Aria e Presto, and Fuga a due cori con corale (eleven voices)

**Files.**
- Sources: `prelude.py`, `fugue.py`. Built scores: `prelude.json` (35 bars, 4/4, one keyboard), `fugue.json` (55 bars, 12/8, eleven staves).
- `renders/`: `prelude.*` and `fugue.*` (PDF, MIDI, MusicXML, MP3) in Bach/Lehman temperament; `*-equal.mp3` in equal temperament (audio only); `fugue-spatial.mp3`, binaural, layout `antiphonal-centre`.
- Build: `python3 prelude.py`, `python3 fugue.py`, then the render commands in `cycle/CONVENTIONS.md`.

**Length.** The Prelude is about 110 s and the Fugue about 243 s (rendered durations, with the tempo maps). The Prelude ends on the dominant and runs straight into the Fugue.

**Tempo maps** (`metadata.tempo_map`, t in quarters).
- Prelude: the Aria is at ♩ = 56 and slows to 48 into its cadence (b16.3–17). The Presto is at ♩ = 132 from b18 (t = 68). It broadens only over the last two bars (→ 96), into the attacca.
- Fugue: ♩. = 56 (♩ = 84). There is a breath into the Recognition (b25 → 76, then a tempo at b26). The last chorale line broadens: 84 at b48, 80 at b51, 74 at b54, and 54 at the final chord.

I have not heard any of this. Everything below comes from the scores, `tools/critic.py`, `tools/reduce.py` and my own checks.

## Concept

This pair is an homage to the opening chorus of the St Matthew Passion, BWV 244/1, "Kommt, ihr Töchter". Two choirs question and answer each other ("Sehet! – Wen? – den Bräutigam … Wie? – als wie ein Lamm"). Above them a ripieno soprano sings the chorale "O Lamm Gottes, unschuldig" as a cantus firmus, one phrase at a time.

The fugue subject *is* the chorale's first line, moved into the relative minor. So the eleventh voice and the other ten sing one tune at two speeds and in two modes. Section V ("Recognition") makes this audible.

**Staves.**
- Coro I: S1 A1 T1 Bar1 B1, on the left in the spatial render.
- Coro II: S2 A2 T2 Bar2 B2, on the right.
- CH, "Soprano in ripieno (Choral)": centre front, 0° at 4 m.

## The chorale: version and credits

- **Tune:** "O Lamm Gottes, unschuldig", Nikolaus Decius (German Agnus Dei, c. 1522; first printed 1531).
- **Pitches:** copied from the soprano of Bach's four-part setting **BWV 401** (music21 corpus `bach/bwv401`, read and checked in this session). That setting is in F major. I transposed it to **G major**, the key in which the ripieno soprano sings it in BWV 244/1.
- **Lines used** (the tune is AAB, so lines 3 and 4 repeat lines 1 and 2):
  - L1, L3: G G G D D E D
  - L2, L4: D G A B C B A-G G
  - L5: B B B A B G-F♯ E D
  - L6: D E D D B-C D C B
  - L7: E D-C B A B D B-A G
- **Rhythm:**
  - Each quarter of BWV 401 becomes a dotted half (two 12/8 beats), and each pair of eighths becomes two dotted quarters.
  - The fermata notes are lengthened to a whole bar instead of being held.
  - Three notes are shorter than this rule gives: L1's half-note E (one dotted half), and L7's last B and A (a dotted quarter each), so that the final G falls on b53.3. The final G is then held to the end.
- **Differences from Bach:**
  - I have not compared this note for note with the ripieno part of BWV 244/1, which may differ in small rhythmic details.
  - The line sits an octave above the vocal ripieno (G5–E6), like a 4′ stop, so that it stays above both choirs.
- **The Prelude's Aria** paraphrases the same chorale. Lines 1, 2, 5, 6 and 7 are moved a diatonic third down into E minor (L5 stays in G major), then ornamented and re-timed.

## Subject derivation

- Chorale line 1 is G G G D D E D. Moved a diatonic third down into the relative minor, it becomes **E E E B B C B**. These are the subject's seven dotted-quarter beat-notes.
- The subject in full, figured with a turn and a tail: `E4:6 E4:4 D#4:2 E4:2 F#4:2 G4:2 B4:4 A4:2 B4:4 G4:2 C5:6 B4:2 A4:2 G4:2 F#4:2 E4:2 D#4:2`. It is two bars long and ends on the leading tone, which elides into the next downbeat.
- **Inversion** (`invert_diatonic`, axis G4): B B B E | E D♯ E. It begins on the dominant and ends on the tonic, so it behaves like a tonal answer. Coro II's whole exposition is built from it.
- **The subject in G major** (RG, written out) has beat-notes G G G D D E D, which is exactly the chorale line. The chorale is therefore the subject in augmentation ×2. IG is RG's diatonic inversion (axis B).
- **Answer:** real, in B minor (`transpose`).
- **Countersubject** (B E G F♯ E D …, above the subject): used through the exposition (S1 b3, A1 b5, T1 b7, Bar1 b9).
- **Fit with the chorale.** I tested each whole statement against each chorale line, beat by beat, for 2nds, 7ths and tritones, and for parallels:
  - L1 fits the subject in E minor and in G major, both starting with it (b14, b26).
  - L7 fits the inversion starting with it, and the subject six beats later (b50, b51.3).
  - L2/L4 fits the G-major subject at half speed, starting five beats earlier (b30.4).
  - Where the subject's D♯ (or the answer's A♯) met the chorale's D (or A), the tail is in natural minor. This is labelled in the score.

## Prelude X: "Aria e Presto" (after BWV 855)

| Bars | What happens |
|---|---|
| 1 | The walking ground alone: an eighth-note figure over E. |
| 2–4 | Chorale line 1 in E minor (E E E B \| C B) over a chromatic lament ground (E D♯ D C♯ C B, in half notes), ending on a half cadence. |
| 5–7 | Line 2 (B E F♯ G A G F♯ E), ending on a half cadence on B. |
| 8–10 | Line 5 in **G major**, over the ground moved to G (G F♯ F E E♭ D). |
| 11–13 | Line 6 (B C B \| B A G A \| A C B), ending on a half cadence. |
| 14–17 | Line 7 (C B A G E \| C E D♯ E), with a perfect cadence at b17. |
| 18–19 | **Presto.** Motive M in the right hand: the subject's beat-notes E E E B \| B C B (D♯), figured in sixteenths. The counter-line C runs in eighths in the left hand. |
| 20–21 | Hands exchanged, in B minor. M is an eleventh lower, in the left hand; C is a twelfth higher, in the right. |
| 22–23 | Fifths-sequence episode on M's head (b → e → a → D7) over a stepwise-falling bass. |
| 24–25 | M and C in G major: a diatonic third up, written out (D♯→F♯, A♯→C♯). |
| 26–27 | Exchanged again, in E minor. |
| 28–30.1 | M in canon with itself, one beat later and two octaves lower. |
| 30–33 | Dominant pedal (B2–B3 octaves). The right hand climbs to B5. |
| 34–35 | Run-out over i – VI – iv to V: a 4–3 (E4–D♯4) over B, stopping on **D♯4**. The Fugue's first note, E4, resolves it. |

There is one player throughout: the right hand takes the aria and the upper Presto line; the left hand takes the ground and figure, then the lower Presto line. Critic: keyboard-unplayable 0 %.

## Fugue X: form and entry map

| Bars | Section | Entries (voice, bar.beat in dotted quarters) |
|---|---|---|
| 1–10 | **I. Exposition, Coro I alone**, from the top down | S1 subject 1.1 → A1 answer (b) 3.1 → T1 subject 5.1 → Bar1 answer 7.1 → B1 subject 9.1. The countersubject lies above each new entry. |
| 11–13 | **II. Dialogue** | A1 "Sehet!" (subject head) 11.3. **Coro II's first sound**: S2 "Wen?" (inversion head B B C), with T2 and B2, 12.3. A1 "den Bräutigam" 13.1. Coro II (S2 A2 B2) "Wie?" 13.3. A1 "als wie ein Lamm", the sigh C5–B4, 13.4. |
| 14–16 | **III. Chorale line 1** | The chorale (CH 14.1) and the subject (T1 14.1, natural-minor tail) start together: the source and its diminution. |
| 17–25 | **IV. Coro II's mirror exposition**: all inversions, from the bass up | B2 (b) 17.1 → T2 (b) 18.1 → Bar2 (e) 20.2, under **line 2** (20.1) → A2 (b) 22.3 → S2 (b) 24.3, with Coro II alone. Coro I's S1 and A1 accompany b17–23. |
| 26–29 | **V. Recognition**: **line 3** (= line 1) | A1 sings the subject in G major, whose beat-notes are the chorale. Bar2 sings it in E minor a tenth below (the one deliberate stretch of parallel tenths). Then B2 answer 28.2 and S1 inversion in D 28.4. |
| 30–37 | **VI. Line 4** (= line 2) at 32.1 | A2 G-major subject 30.3. B1 the same at **half speed** 30.4 (a prolation stretto, one beat apart), carrying line 4. T2 G-major inversion 32.3. T1 subject (e) 35.1, cadencing in E minor at b37. |
| 37–43 | **VII. Line 5** at 38.1, B minor | One-beat exchange: Coro II asks, Coro I answers (37.2–37.4). T1 answer 38.1 (A♮ tail against the chorale's A). Bar2 inverted answer, as the bass, 39.3. Dialogue in the gap: A1 head / S2 inversion head, 42.3–43.1. |
| 43–49 | **VIII. Line 6** at 44.1 | B2 subject (natural-minor tail) 43.2. A1 G-major inversion 45.2. Half cadence: S1 answer and A2 inverted answer **as a mirror pair** over a B pedal, 47.3. |
| 49–55 | **IX. Line 7** at 50.1: final stretto and coda | B2 G-major inversion 49.1 → S2 inversion (e) 50.1 → T1 subject (e) 51.3 → coda 53.3: T1 subject head against S1 inversion head (the mirror, as question and answer at once) over the tonic pedal. Then iv–i with all eleven voices sounding. |

Thematic statements per staff. In the critic's `themes` check every statement has exact rhythm and intervals, with these exceptions: the natural-minor tails (15/16 intervals); the G-major forms, which are diatonic (modal) transfers and so match the minor subject's intervals only 10/16 (rhythm 16/16); the cut mirror pair at b47 (13–14/16); and the dialogue heads.

| Staff | Statements |
|---|---|
| S1 | 3 + coda head |
| A1 | 3 + "Sehet!" head |
| T1 | 5 + coda head |
| Bar1 | 1 |
| B1 | 2 (one at half speed) |
| S2 | 2 + "Wen?" head |
| A2 | 3 |
| T2 | 2 |
| Bar2 | 3 |
| B2 | 4 |
| CH | 7 lines |

## Final stretto: what is in it and why it holds

- **Beat-level verticals (from the score, b50.1–53.2).**
  - Against the chorale, the inversion (S2) gives E6/B4, E6/B4, D6/B4, C6/E4, B5/E4, B5/D♯4, A5/E4, A5/A4.
  - Against the chorale, the subject (T1) gives A5/E3, A5/E3, B5/E3, B5/B3, D6/B3, **D6/C4**, B5/B3, A5/F♯3.
  - Against the chorale, the bass inversion (B2) gives G2, F♯2, G2, C3.
  - Every sonority is a 3rd, 5th, 6th or octave (compound), with two exceptions. Two 4ths stand above a real bass (b50.1 over G2, b51.3 over C3). The one 9th, at b52.4, is the 7th of D7/A. This agrees with the fit test: the inversion at the chorale's start has 0 clashes, and the subject six beats later has 1, at that D7.
- **Stretto distances.** B2 → S2: 4 beats. S2 → T1: 6 beats. Then the coda pair is simultaneous (T1 subject head against S1 inversion head).
- **The two choirs.**
  - Coro II has the inversion twice (b49, b50).
  - Coro I has the subject (b51.3) and the subject/inversion heads (b53.3).
  - Coro II's last subject comes one line earlier (B2 b43.2, under line 6). See the weak spots.
- **Rejected.** Bar1 subject at b49.3 (two beats before line 7) made parallel octaves with the chorale (C6/C4 → B5/B3), so I dropped it. The b47 mirror pair is cut at b49.1, 13 of 16 notes, so that it does not run into B2's inversion.
- **Density in the last line, third pass.** Voices moving per bar for b49–55: 5, **10, 9, 9, 9**, 8, 8. Voices sounding: 5, 10, 9, 9, 9, **11, 11**. B1 rests in b49–50 and returns on the tonic at b51.1. The chorale holds its last G and Coro I's bass holds the E pedal from b53.3, so no bar has all eleven voices *attacking*. All eleven *sound* in the closing iv–i (b54.4–55).

## Critic numbers (final)

| | Fugue | Prelude | Target |
|---|---|---|---|
| parallels_error / weak | 0 / 0 | 0 / 0 | 0 |
| beat_parallels | 0 | 0 | ≤ 6 |
| dissonance_unresolved | 0 | 0 | 0 |
| pc_tripled_on_beats_pct | 32.5 | 1.6 | ≤ 25 (fugue: judged by bad_doublings) |
| bad_doublings | 3 (b15.2.5, b35.4, b50.4: doubled 7ths) | 0 | ≤ 5 |
| low_register_seconds | 5 | 0 | ≤ 12 |
| stepwise_pct | 61.7 | 52.6 (keyboard figuration) | ≥ 62 |
| mean_moving_voices | 5.67 over the whole fugue | 2.46 (of 3) | — |
| tutti mean (both choirs + chorale: b20–23, 26–29, 32–35, 38–41, 44–47, 50–53) | **6.79** | — | ≥ 7 (report) |
| crossings | 18 notes (all between the two choirs except T2 above A2 at b52.1) | 0 | — |

Moving voices by section:

| Section | Moving voices |
|---|---|
| Exposition | 2.9 (one choir, accumulating) |
| Dialogue | 6.7 |
| III | 5.3 |
| IV | 5.6 |
| V | 5.0 |
| VI | 6.0 |
| VII | 6.5 |
| VIII | 6.3 |
| IX | 8.3 |

`reduce.py` shows a directed harmonic route:
- e → (b) → G → e for lines 1–4.
- B minor for line 5, back to e via C and G for line 6, a half cadence on B (b47–48), then e.
- The chorale's phrase-ends (D, G, D, G, D, B, G) are harmonised as D or b, G, D, G, b, V of e. The final G is the third of the E-minor chord.
- The non-tertian labels at b30–31 and b47–48 come from the augmentation passage and from the mirror pair over the dominant pedal.

## How the notes were written

- Every note is a literal token string in `prelude.py` or `fugue.py`.
- Thematic statements are explicit transforms (`transpose`, `invert_diatonic`, `scale_rhythm`) of the hand-written subject, or are written out by hand: RG, IG, the natural-minor tails, and the G-major Presto statement.
- Scratch scripts in the session scratchpad only **checked** candidates that I wrote: the critic run on a trial line, and a fit test listing which whole-statement placements clash with a chorale line. No script chose or inserted notes, and nothing generates notes at build time.
- The third pass (b38–40, b44, b49–54) added hand-written inner lines one voice at a time. Each was re-checked, and each parallel the critic found was fixed by changing my new line, not the existing ones.

## Weak spots (honest)

1. **Not a full eleven-part texture most of the time.**
   - The whole-fugue mean is 5.7 moving voices. In tutti it is 6.8, below the 7 asked for.
   - The Recognition (b26–29: 5, 4, 6, 5) is bass-less by design. I tried a Coro I bass under it, and it made parallel 5ths and 8ves with the tenths, so I removed it.
   - b48 has three voices: the mirror pair over the pedal.
2. **"All eleven lines moving" in the final phrase is not met.** The best is 10 (b50), then 9. Some of the third-pass inner lines are held tones rather than real counterpoint: Bar1 B2 in b51–54, Bar1 F♯3 in b38–39, A2 B4 in b40. They also lower stepwise motion (61.7 %).
3. **The final stretto is lopsided between the choirs.** Coro II has no subject under line 7, and Coro I's inversion there is only a head (b53.3).
4. **Unequal staves.** Bar1 has a single entry (b7) and 58 notes. S2 has 74 notes. B2 and T1 carry most of the late entries.
5. **Altered statements.**
   - Natural-minor tails in four statements against the chorale: b14 T1, b26 Bar2, b38 T1 (A♮), b43 B2.
   - Two statements are cut to 13 notes (b47.3 S1/A2).
6. **Tripling.** Pitch classes are tripled on 32.5 % of beats (eleven voices on triads). There are 3 doubled sevenths (b15, b35, b50). In the final tutti there are single-beat unisons between the choirs: S2/S1 B4 at b53.2, A2/S2 G4 at b51.1, T1/Bar2 at b52.1. None of them is sustained as colla parte doubling.
7. **Register.** The chorale sits an octave above a sung ripieno (top E6), and S1 reaches B5. In the renders these are keyboard voices, not singers.
8. **Prelude.**
   - The Presto canon (b28–29) and the pedal bars give non-tertian verticals in `reduce.py`. They are linear, and clean by the critic.
   - The Prelude runs about 1′50″, against the ~2′ asked for.
   - Stepwise motion is 52.6 %, because the Presto is arpeggiated figuration.
9. **Spatial.** With `antiphonal-centre`, Coro I is on the left (−80…−25°), Coro II on the right (+25…+80°) and the chorale at the centre front. I cannot judge from the files whether the centre chorale stands out enough or swamps the choirs.
10. **Unheard.** I cannot hear the renders. Balance, the 12/8 lilt at ♩. = 56, and whether the chorale reads as a cantus firmus are all for Sam's ears.
