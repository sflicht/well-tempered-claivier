# Pair X in E minor: Aria e Presto, and Fuga a due cori con corale (eleven voices)

**Files.**
- Sources: `prelude.py`, `fugue.py`. Built scores: `prelude.json` (35 bars, 4/4, one keyboard), `fugue.json` (56 bars, 12/8, eleven staves).
- `renders/`: `prelude.*` and `fugue.*` (PDF, MIDI, MusicXML, MP3) in Bach/Lehman temperament; `*-equal.mp3` in equal temperament (audio only); `fugue-spatial.mp3`, binaural, layout `antiphonal-centre`.
- Build: `python3 prelude.py`, `python3 fugue.py`, then the render commands in `cycle/CONVENTIONS.md`.

**Length.** The Prelude is about 110 s and the Fugue about 249 s (rendered durations, with the tempo maps). The Prelude ends on the dominant and runs straight into the Fugue.

**Tempo maps** (`metadata.tempo_map`, t in quarters).
- Prelude: the Aria is at ♩ = 56 and slows to 48 into its cadence (b16.3–17). The Presto is at ♩ = 132 from b18 (t = 68). It broadens only over the last two bars (→ 96), into the attacca.
- Fugue: ♩. = 56 (♩ = 84). There is a breath into the Recognition (b25 → 76, then a tempo at b26). The last chorale line broadens: 84 at b48, 80 at b51, 74 at b54, 60 at b56 and 50 at the end.

I have not heard any of this. Everything below comes from the scores, `tools/critic.py`, `tools/reduce.py` and my own checks.

**Second pass on the Fugue (coordinator's request).**

| Moving voices per bar | Before | After |
|---|---|---|
| Final line, b50–53 | 10, 9, 9, 9 | **10, 11, 11, 11** |
| Tutti mean (both choirs + chorale: b20–23, 26–29, 32–35, 38–41, 44–47, 50–53) | 6.79 | **8.21** |
| Whole fugue | 5.67 | 6.05 |
| Bars in which all eleven voices move | 0 | 3 (b51–53) |

What changed:
- **Final stretto (b49–56).** The choirs now trade forms, so each has its own entry under line 7:
  - Coro I's soprano sings the inversion with the chorale (b50.1).
  - Coro II's baritone sings the subject, the final cadence (b51.3).
  - Coro I's tenor sings the **countersubject** against it, as in the exposition.
  - Coro II's bass still sings the G-major inversion before them (b49.1).
- **Free lines in b50–53.** The other voices were rewritten as short answering phrases, so every line attacks in every bar from b51 to b53.
- **Coda (b53.3–56).** The tenor turns the countersubject into the subject's head as Coro II's alto sings the inversion's head (the mirror, across the choirs). Then the lines reach the closing chord one or two at a time, each by step on its own beat. The last four arrive by an upper-neighbour eighth (C–B, C–B, C–B, F♯–E), so their final notes fall on successive beats from b54.4 to b55.3. Bar 56 is added for the full chord.
- **The held fillers are gone.** These were Bar1's B2 in b51–54, Bar1's F♯3 in b38–39 and A2's B4 in b40. In their place:
  - Coro II's alto sings the **countersubject in B minor** against Coro I's answer (b38–39; natural-minor tail against the chorale's A).
  - Coro I's baritone gets its **second entry**: the subject in D major at b45.3, with its last note C♮ against the chorale's C.
  - New moving lines: Coro I's tenor in b20–24 and b32–34, a Coro I bass under the Recognition (b26–28), and lines for Coro I's alto and Coro II's baritone, bass and soprano at the cadences of lines 4–5.
- **b48 stays at three voices.** It is a deliberate breath: the mirror pair over the dominant pedal, before the last line.
- **Method.** Every added note was written by hand and checked with the critic one voice at a time. Each parallel or unresolved dissonance was fixed by changing the new line.

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
| 37–43 | **VII. Line 5** at 38.1, B minor | One-beat exchange: Coro II asks, Coro I answers (37.2–37.4). T1 answer 38.1 (A♮ tail against the chorale's A), with A2 singing the countersubject in B minor against it. Bar2 inverted answer 39.3. Dialogue in the gap: A1 head / S2 inversion head, 42.3–43.1. |
| 43–49 | **VIII. Line 6** at 44.1 | B2 subject (natural-minor tail) 43.2. A1 G-major inversion 45.2; one beat later Bar1 subject in D major 45.3 (its second entry). Half cadence: S1 answer and A2 inverted answer **as a mirror pair** over a B pedal, 47.3. b48 is left at three voices as a breath. |
| 49–56 | **IX. Line 7** at 50.1: final stretto and coda | B2 (Coro II) G-major inversion 49.1 → S1 (Coro I) inversion (e) 50.1 → Bar2 (Coro II) subject (e) 51.3 with T1 (Coro I) countersubject → coda 53.3: T1 subject head against A2 inversion head (the mirror, across the choirs) over the tonic pedal. Then the eleven lines reach the closing chord in turn (b53.3–55.3). |

Thematic statements per staff. In the critic's `themes` check every statement has exact rhythm and intervals, with these exceptions: the natural-minor tails (15/16 intervals); the G-major forms, which are diatonic (modal) transfers and so match the minor subject's intervals only 10/16 (rhythm 16/16); the cut mirror pair at b47 (13–14/16); Bar1's D-major entry (last note C♮); and the dialogue heads.

| Staff | Statements |
|---|---|
| S1 | 4 |
| A1 | 3 + "Sehet!" head |
| T1 | 4 + coda head, + countersubject b51.3 |
| Bar1 | 2 |
| B1 | 2 (one at half speed) |
| S2 | 1 + "Wen?" head |
| A2 | 3 + coda head, + countersubject b38 |
| T2 | 2 |
| Bar2 | 4 |
| B2 | 4 |
| CH | 7 lines |

## Final stretto: what is in it and why it holds

- **Entries.** B2 (Coro II) G-major inversion 49.1 → S1 (Coro I) inversion 50.1, with the chorale's last line → Bar2 (Coro II) subject 51.3, with T1 (Coro I) countersubject → coda 53.3: T1 (Coro I) subject head and A2 (Coro II) inversion head together. Each choir has both forms.
- **Beat-level verticals (from the score, b50.1–53.2).**
  - Against the chorale, the inversion (S1) gives E6/B4, E6/B4, D6/B4, C6/E4, B5/E4, B5/D♯4, A5/E4, A5/A4.
  - Against the chorale, the subject (Bar2) gives A5/E3, A5/E3, B5/E3, B5/B3, D6/B3, **D6/C4**, B5/B3, A5/F♯3.
  - Against the chorale, the countersubject (T1) gives A5/B3, A5/G4, B5/E4, B5/D4, D6/D4, D6/A4, B5/D♯4, A5/F♯4.
  - Against the chorale, the bass inversion (B2) gives G2, F♯2, G2, C3.
  - Every sonority is a 3rd, 5th, 6th or octave (compound), with these exceptions:
    - Two 4ths above a real bass (b50.1, b51.3).
    - The countersubject's held B3 at b51.3 (a prepared 9th, as in the exposition).
    - The 9th at b52.4, which is the 7th of D7/A.
  - This agrees with the fit test: the inversion at the chorale's start has 0 clashes, and the subject six beats later has 1, at that D7.
- **Where the countersubject meets the inversion (b51.4).** It sings G4 against the inversion's A4. Over B7 the A is the chord seventh and the G a 6–5 appoggiatura that falls to F♯ on the next eighth.
- **Stretto distances.** B2 → S1: 4 beats. S1 → Bar2: 6 beats. Then the coda heads enter together.
- **Rejected.**
  - Bar1 subject at b49.3, two beats before line 7: parallel octaves with the chorale (C6/C4 → B5/B3).
  - A second subject entry under line 7 in either choir: none of the forms fits beside the b51.3 subject without parallels or 2nds on the beat. The test was beat by beat; the rejected placements are listed in the session notes.
- **The cut.** The b47 mirror pair is cut at b49.1 (13 of 16 notes), so that it does not run into B2's inversion.
- **The one beat-to-beat octave.** T1's last countersubject note F♯4 → head E4 against the subject's F♯3 (E3 D♯3) → E3 at b53.2–53.3. There is a D♯ eighth between them. It is the only beat parallel left in the fugue.
- **Arrivals at the closing chord (E2 B2 E3 G3 B3 E4 G4 B4 B4 E5 G5).**

  | Beat | Arrives | By |
  |---|---|---|
  | b53.3 | chorale G5 | A5 |
  | b53.3 | Bar2 E3 (subject's end) | D♯3 |
  | b54.1 | Bar1 G3 | F♯3 |
  | b54.1 | T2 B3 | A3 |
  | b54.3 | T1 G4 | A4 |
  | b54.3 | A2 E4 | F♯4 |
  | b54.4 | B2 B2 | C3 |
  | b55.1 | A1 B4 | C5 |
  | b55.2 | S2 B4 | C5 |
  | b55.3 | S1 E5 | F♯5 |

  Coro I's bass reaches E2 at b53.3 by the cadential leap B→E and holds it as a pedal. It is the one line that does not arrive by step.

## Critic numbers (final)

| | Fugue | Prelude | Target |
|---|---|---|---|
| parallels_error / weak | 0 / 0 | 0 / 0 | 0 |
| beat_parallels | 1 (b53.2–53.3, see above) | 0 | ≤ 2 |
| dissonance_unresolved | 0 | 0 | 0 |
| pc_tripled_on_beats_pct | 43.0 | 1.6 | ≤ 25 (fugue: judged by bad_doublings) |
| bad_doublings | 3 (b15.2.5, b35.4, b52.4: doubled 7ths) | 0 | ≤ 5 |
| low_register_seconds | 11 | 0 | ≤ 12 |
| stepwise_pct | 60.9 | 52.6 (keyboard figuration) | ≥ 60 |
| mean_moving_voices | 6.05 over the whole fugue (5.67 before the second pass) | 2.46 (of 3) | — |
| tutti mean (both choirs + chorale: b20–23, 26–29, 32–35, 38–41, 44–47, 50–53) | **8.21** (6.79 before) | — | ≥ 8 |
| crossings | 32 notes, mostly between the two choirs; inside a choir, A1 rises above S1 for a few beats in b50–52, where S1's inversion dips to E4 | 0 | — |

Moving voices by section:

| Section | Moving voices |
|---|---|
| Exposition | 2.9 (one choir, accumulating) |
| Dialogue | 6.7 |
| III (Coro I + chorale only) | 5.3 |
| IV | 6.3 |
| V | 6.8 |
| VI | 6.9 |
| VII | 7.7 |
| VIII | 6.7 |
| IX (b49–56, including the closing bars) | 7.0 |

In b50–53 the moving voices per bar are 10, 11, 11, 11.

`reduce.py` shows a directed harmonic route:
- e → (b) → G → e for lines 1–4.
- B minor for line 5, back to e via C and G for line 6, a half cadence on B (b47–48), then e.
- The chorale's phrase-ends (D, G, D, G, D, B, G) are harmonised as D or b, G, D, G, b, V of e. The final G is the third of the E-minor chord.
- The non-tertian labels at b30–31 and b47–48 come from the augmentation passage and from the mirror pair over the dominant pedal.

## How the notes were written

- Every note is a literal token string in `prelude.py` or `fugue.py`.
- Thematic statements are explicit transforms (`transpose`, `invert_diatonic`, `scale_rhythm`) of the hand-written subject, or are written out by hand: RG, IG, the natural-minor tails, and the G-major Presto statement.
- Scratch scripts in the session scratchpad only **checked** candidates that I wrote: the critic run on a trial line, and a fit test listing which whole-statement placements clash with a chorale line. No script chose or inserted notes, and nothing generates notes at build time.
- The later passes added hand-written lines one voice at a time:
  - Third pass: b38–40, b44 and b49–54.
  - Second-pass request: b20–24, b26–29, b32–35, b38–41, b45–47 and b49–56. This includes the swap of forms in the final stretto and the new coda.
  - Each line was re-checked. Each parallel the critic found was fixed by changing the new line, except where noted.

## Weak spots (honest)

1. **Density is uneven.**
   - The tutti mean is now 8.2.
   - The Recognition (b26–29: 7, 6, 8, 6) is lighter by design. It is built on the two choirs' tenths and has a new, simple Coro I bass.
   - b44–46 are at 6–7.
   - The exposition (one choir, entering voice by voice) and b48 (a three-voice breath before the last line) are thin on purpose.
2. **Some added lines are short answering phrases.** Many of the voices added to b50–53 sing one to three notes and then rest. That is how every line moves in every bar there. It is closer to the dialogue style of BWV 244/1 than to eleven continuous lines.
3. **Pedals and holds.**
   - Coro I's bass holds a B pedal under the B-minor answer (b38–39).
   - After their arrivals, the voices hold the closing chord.
   - Coro I's bass reaches the final tonic by the cadential leap, not by step.
4. **One beat-to-beat octave** at b53.2–53.3: the countersubject's end against the subject's end.
5. **Altered and cut statements.**
   - Natural-minor tails against the chorale: b14 T1, b26 Bar2, b38 T1 (A♮) with its countersubject, b43 B2, and Bar1's D-major entry (C♮ at the end).
   - Two statements are cut to 13 notes (b47.3).
6. **Unequal staves.** Coro II's soprano has only one full entry, at b24.3; its b50 inversion moved to Coro I's soprano. T2 and B1 have two each.
7. **Tripling.** Pitch classes are tripled on 43 % of beats (eleven voices on triads), and there are 3 doubled sevenths. Single-beat unisons between the choirs are frequent in b50–55. None is a sustained colla parte doubling.
8. **Register.** The chorale sits an octave above a sung ripieno (top E6), and S1 reaches B5. In the renders these are keyboard voices, not singers.
9. **Prelude.**
   - The Presto canon (b28–29) and the pedal bars give non-tertian verticals in `reduce.py`. They are linear, and clean by the critic.
   - The Prelude runs about 1′50″, against the ~2′ asked for.
   - Stepwise motion is 52.6 %, because the Presto is arpeggiated figuration.
10. **Spatial.** With `antiphonal-centre`, Coro I is on the left (−80…−25°), Coro II on the right (+25…+80°) and the chorale at the centre front. I cannot judge from the files whether the centre chorale stands out enough or swamps the choirs.
11. **Unheard.** I cannot hear the renders. Balance, the 12/8 lilt at ♩. = 56, the staggered close, and whether the chorale reads as a cantus firmus are all for Sam's ears.
