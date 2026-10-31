# Pair X in E minor: Aria e Presto, and Fuga a due cori con corale (three voices)

**Files.**
- Sources: `prelude.py`, `fugue.py`. Built scores: `prelude.json` (35 bars, 4/4, one keyboard), `fugue.json` (49 bars, 12/8, three staves: Choral, Coro I, Coro II).
- `renders/`: `prelude.*` and `fugue.*` (PDF, MIDI, MusicXML, MP3) in Bach/Lehman temperament; `*-equal.mp3` in equal temperament (audio only); `fugue-spatial.mp3`, binaural, `--layout score` (seats stored in `fugue.json`: Coro I at −55°, Coro II at +55°, the chorale in front at 0°, 4 m) with `--program 53` (Voice Oohs). The old `fugue-spatial-choir.mp3` is replaced by it and was deleted.
- Build: `python3 prelude.py`, `python3 fugue.py`, then the render commands in `cycle/CONVENTIONS.md`.
- The earlier eleven-voice fugue is kept in `archive-n-plus-1/`.

**Length.** The Prelude is about 110 s and the Fugue about 207 s (rendered durations, with the tempo maps). The Prelude ends on the dominant and runs straight into the Fugue: its last note, D♯4, is resolved by the Fugue's first, E4.

**Tempo maps** (`metadata.tempo_map`, t in quarters).
- Prelude: the Aria is at ♩ = 56 and slows to 48 into its cadence (b16.3–17). The Presto is at ♩ = 132 from b18 (t = 68). It broadens only over the last two bars (→ 96), into the attacca.
- Fugue: ♩. = 60 (♩ = 90). Small breaths (→ 84 and back within a beat or two) at the cadences of line 1 (b11.1), line 2 (b15.2) and line 5 (b34.3), and before the line-5 stretto (b30.4). A ritardando to 72 into the general pause before the Recognition (b18.4), then a tempo. The half cadence broadens (→ 80, b39–40.2); the dominant pedal is a tempo; a breath (→ 76) into the general pause at b42.4; the last line is a little broader (86). Final ritardando from the cadence (b47.3): 74, 60, 48.

I have not heard any of this. Everything below comes from the scores, `tools/critic.py`, `tools/reduce.py`, `tools/stretto_finder.py` and my own scratch checks.

---

## Prelude X: "Aria e Presto" (after BWV 855)

(Unchanged in this recomposition.)

| Bars | What happens |
|---|---|
| 1 | The walking ground alone: an eighth-note figure over E. |
| 2–4 | Chorale line 1 in E minor (E E E B \| C B) over a chromatic lament ground (E D♯ D C♯ C B, in half notes), ending on a half cadence. |
| 5–7 | Line 2 (B E F♯ G A G F♯ E), ending on a half cadence on B. |
| 8–10 | Line 5 in **G major**, over the ground moved to G (G F♯ F E E♭ D). |
| 11–13 | Line 6 (B C B \| B A G A \| A C B), ending on a half cadence; b13's melody is turned so that it does not repeat b4. |
| 14–17 | Line 7 (C B A G E \| C E D♯ E), with a perfect cadence at b17. In b14–16 the left-hand figure moves in sixteenths, so the aria gathers motion into its cadence. |
| 18–19 | **Presto.** Motive M in the right hand: the subject's beat-notes E E E B \| B C B (D♯), figured in sixteenths. The counter-line C runs in eighths in the left hand. |
| 20–21 | Hands exchanged, in B minor. M is an eleventh lower, in the left hand; C is a twelfth higher, in the right. |
| 22–23 | Fifths-sequence episode on M's head (b → e → a → D7) over a stepwise-falling bass. |
| 24–25 | M and C in G major: a diatonic third up, written out (D♯→F♯, A♯→C♯). |
| 26–27 | Exchanged again, in E minor. |
| 28–30.1 | M in canon with itself, one beat later and two octaves lower. The left hand plays 8 softer, as an echo. |
| 30–33 | Dominant pedal (B2–B3 octaves). The right hand climbs to B5. |
| 34–35 | Run-out over i – VI – iv to V: a 4–3 (E4–D♯4) over B, stopping on **D♯4**. The Fugue's first note, E4, resolves it. |

There is one player throughout: the right hand takes the aria and the upper Presto line; the left hand takes the ground and figure, then the lower Presto line. Critic: keyboard-unplayable 0 %.

**Prelude: what the second review (REVIEW-2.md) changed** (items 6–8 of the list in the eleven-voice NOTES, kept as they were).

6. **P1: the aria's repeated left-hand unit (applied).**
   - The figure moves in sixteenths in the last phrase (b14–16), using the reviewer's tested figuration.
   - b13 is turned in the right hand (C5 D5 C5 A4 | B4 … A4 B4), so it no longer repeats b4. My first version made beat-to-beat octaves with the ground (C→B), so I re-timed it.
7. **P2: the Presto canon's clashes (applied as proposed).** The left hand plays 8 softer in b28–30.1, as an echo canon. I kept the notes: as the reviewer found, other canon distances are no cleaner, because the clashes come from the motive's own neighbour notes.
8. **P3: b2.3 and b30–34.** Accepted as they are, as the reviewer suggested.

**Prelude critic numbers** (re-run, unchanged): parallels_error / weak 0 / 0; beat_parallels 0; dissonance_unresolved 0; pc_tripled_on_beats_pct 1.6; bad_doublings 0; low_register_seconds 0; stepwise_pct 51.9 (keyboard figuration); mean_moving_voices 2.46 (of 3); crossings 0; keyboard-unplayable 0 %.

**Prelude weak spots.**
- The Presto canon (b28–29) and the pedal bars give non-tertian verticals in `reduce.py`. They are linear, and clean by the critic.
- The Prelude runs about 1′50″, against the ~2′ asked for.
- Stepwise motion is 52.6 %, because the Presto is arpeggiated figuration.

---

## The chorale: version and credits

- **Tune:** "O Lamm Gottes, unschuldig", Nikolaus Decius (German Agnus Dei, c. 1522; first printed 1531).
- **Pitches, verified in this session:** the soprano of Bach's four-part setting **BWV 401**, read from the music21 corpus (`bach/bwv401`, F major): L1 F F F C C D(half) C; L2 C F G A B♭ A G-F F; L5 A A A G A F-E D C; L6 C D C C A-B♭ C B♭ A; L7 D C-B♭ A G A C A G(half) F. The tune is AAB, so lines 3 and 4 repeat lines 1 and 2. I transposed it to **G major**, the key in which the ripieno soprano sings it in BWV 244/1, and placed it an octave above the sung pitch (D5–E6), like a 4′ stop, so that it stays above both choirs.
  - L1, L3: G G G D D E D
  - L2, L4: D G A B C B A-G G
  - L5: B B B A B G-F♯ E D
  - L6: D E D D B-C D C B
  - L7: E D-C B A B D B A(half) G
- **Rhythm:** each quarter of BWV 401 becomes a dotted half (two 12/8 beats), each pair of eighths two dotted quarters. Two departures:
  - L1/L3's half-note E is one dotted half, not two, so that the line is exactly the subject's seven beat-notes in augmentation (see below).
  - The fermata notes are shortened so that the chorale breathes before the next line: L1/L3 end on D for three beats and a rest, L2/L4 on G for two beats and a two-beat rest, L5 on D for three beats and a rest. L6 keeps its full four beats (the half cadence), and L7's final G is held to the end.
  - L7 now has BWV 401's rhythm (B one unit, A a half note); the eleven-voice version had shortened both.
- I have not compared this note for note with the ripieno part of BWV 244/1, which may differ in small rhythmic details.
- **The Prelude's Aria** paraphrases the same chorale. Lines 1, 2, 5, 6 and 7 are moved a diatonic third down into E minor (L5 stays in G major), then ornamented and re-timed.

---

## Fugue X à 3: "Fuga a due cori con corale"

### Concept at the new size

Bach's E-minor fugue in WTC I (BWV 855) has two voices, so this one has three ("Bach + 1"). The concept is still the opening chorus of the St Matthew Passion, BWV 244/1: two choirs questioning and answering ("Sehet! – Wen? – den Bräutigam. Seht ihn! – Wie? – als wie ein Lamm"), with the chorale "O Lamm Gottes, unschuldig" floating above, line by line. With three voices each choir is **one line**, and each choir has a form:

- **Coro I** (the upper fugal voice, D4–C6; left in the binaural render) sings the **subject**: it is the "Sehet!" choir.
- **Coro II** (the lower fugal voice, tenor and bass register; right) answers in **inversion**: its questions ("Wen?", "Wie?", "Was?", "Wohin?") are the inversion's head, a *rising* semitone against the subject's falling one (E–D♯ ↔ B–C).
- **The chorale** (D5–E6; in front) is the third voice, in dotted halves, seven lines with interludes between them.

The dramaturgy is a dialogue that becomes agreement: the choirs first sing separately (Coro I under line 1, Coro II under line 2), recognise the chorale in their subject and sing it together (line 3), carry it slowly (line 4), exchange forms (line 5), agree again (line 6) and meet in a final stretto of both forms under the last line, where nothing else sounds.

### Material

- **Subject** (Coro I, b1, unchanged from the eleven-voice version): `E4:6 E4:4 D#4:2 E4:2 F#4:2 G4:2 B4:4 A4:2 | B4:4 G4:2 C5:6 B4:2 A4:2 G4:2 F#4:2 E4:2 D#4:2`. Its seven dotted-quarter beat-notes are **E E E B B C B**: the chorale's first line, G G G D D E D, moved a diatonic third down into the relative minor. Two bars; it ends on the leading tone, which elides into the next downbeat.
- **Inversion** (`invert_diatonic`, axis G4, E harmonic minor): B B B E | E D♯ E, rising at the end to C. It begins on the dominant, so it serves as a counter-fugue answer (as in the Art of Fugue, Contrapunctus 5).
- **G-major forms**, written out: RG (beat-notes G G G D D E D, which *are* the chorale line), IG (RG's inversion); and SBG, the subject on B diatonic in G major (b37), so that it moves in exact diatonic tenths over RG. These are modal transfers, so the critic's `themes` check scores them 9–10/16 intervals (rhythm 16/16).
- **Augmentation** (`scale_rhythm` ×2, b24.4): the subject at the chorale's speed. In 12/8 its quarter-note groups (E F♯ G, B A G, F♯ E D♯) run two against the dotted-quarter beat, a hemiola under the chorale.
- **Diminution** (×½, written out): the subject's head ("Sehet!") and the inversion's head ("Wen?", "Was?", "Wohin?") in sixteenths, in the episode (b15.3–17.2) and the second dialogue (b29–30).
- **Countersubject** (Coro I, b3.1–5.1, against the inversion): sixteenths against the answer's eighths and quarters. It opens with the head of **Bach's BWV 855 subject** (E G B E D♯ E), a nod to the two-voice fugue this one is "plus one" of.
- **Natural-minor and altered statements:** the subject under line 1 and in the Recognition ends on D natural (against the chorale's D); the B-minor inversion in the Recognition has A natural (against the chorale's D); the final inversion keeps its head strict (B B C B A G E F♯), but its second half is re-voiced to fill the thirds the two forms leave open, and its tail turns down (… A3 G3 F♯3) to the dominant (8/16 intervals; see Review).

### Section map

Bar.beat in dotted quarters (b45.3 = third dotted quarter of bar 45).

| Bars | Section | What happens |
|---|---|---|
| 1–5.2 | **I. Exposition** (two voices) | Coro I: subject, alone (1.1). Coro II: inversion from the dominant (3.2), after the subject's E has sounded alone for a beat; Coro I's sixteenth countersubject above (from 3.1, BWV 855's head). Half cadence on V (5.2). |
| 5.3–7.4 | **II. Dialogue 1** | Coro I sings the subject in pieces (in B minor, turning to E minor for its last three beats); Coro II interrupts: "Sehet!" (5.3) – **"Wen?"** (6.1, F♯3–G3) – "den Bräutigam. Seht ihn!" (6.2) – **"Wie?"** (7.1, B3–C4) – "als wie ein Lamm" (7.2, the sigh C–B), whose leading tone resolves into… |
| 8–11 | **III. Chorale line 1** | …Coro I's subject (8.1), starting together with the chorale: the subject and its source at two speeds. Coro II runs below. Second half: Coro I in sixteenths over a walking Coro II, G – e – C♯ø7 – F♯7 (the chorale's E is its seventh) – **B minor** (11.1). |
| 12–15.2 | **IV. Line 2** | Coro II's inversion (12.2, after a rest) under the chorale; Coro I holds D5 for its first beat, then runs in sixteenths above. Cadence in **G major** (15.2). |
| 15.3–18.4 | **V. Episode 1** (two voices) | The questions in diminution: "Wen?" (Coro II, G, 15.3), "Sehet!" (Coro I, G, 16.1), "Wen?" (e, 16.3), "Sehet!" (e, 17.1); a falling sequence onto V; a **general pause** (18.4). |
| 19–23.1 | **VI. Recognition** (line 3 = line 1) | Coro I sings the subject **in G major**, whose beat-notes are the chorale line (an octave below the chorale for its first three beats); Coro II sings it **in E minor a tenth below**. After a beat in which only the chorale sounds (21.1), both choirs answer **in inversion**, in sixths (G-major and B-minor inversions, 21.2). |
| 23–28.4 | **VII. Line 4** (= line 2) | Coro I runs in sixteenths in BWV 855's manner (broken chords against a repeated note). Coro II enters after a rest with the **subject in augmentation** (24.4), under a held G4 in Coro I, at the chorale's own speed, and finishes it on the tonic after the chorale has ended (28.4). |
| 28.4–30.3 | **VIII. Dialogue 2** (two voices, diminution) | "Sehet!" (29.1) – **"Was?"** (29.2) – "seht die Geduld. Seht!" (29.3) – **"Wohin?"** (30.1) – "auf unsre Schuld" (30.2): the subject at double speed, one beat at a time, with Coro II's questions between. |
| 30.4–35.4 | **IX. Line 5** | The choirs **exchange forms**: Coro I sings the inversion (G major, 30.4, a beat before the chorale), Coro II the subject (E minor, 31.2): stretto at two beats. Second half to **B minor** (34.3; again E over F♯7). Link in sixteenths. |
| 36–40.2 | **X. Line 6** | Both choirs rectus **in tenths** (37.1): the subject on B over the subject in G. Half cadence VI6 – iv – V (39.1–39.3), the chorale's B over the dominant. |
| 40.3–42.4 | **XI. Dominant pedal** (two voices) | Coro II pulses on B in eighths (as the tonic pedal pulses at the opening of BWV 244/1); Coro I falls in sixteenths from the "Sehet" figure. A **general pause** (42.4). |
| 43–47.3 | **XII. Line 7: final stretto** | V → VI under the chorale's E (43.1). Then, after a rest each, **Coro II's inversion (45.1)** and **Coro I's subject (45.3)**, the only voices under the last line. V7 with the chorale's A as the seventh, over B2 then B3 (47.1–2); the subject's D♯ resolves with the chorale's final G, the third of E minor (47.3). |
| 47.3–49.4 | **XIII. Coda** | Tonic pedal (Coro II E3, then E2). Coro I: BWV 855's head once more (E G B E D♯ E), then the "Lamm" sigh four times (C–B, A–G, F♯–E, C–B), ending on B4 under the chorale's G5. |

**Thematic statements:** Coro I: 7 (subject in E minor ×3 at b1, 8, 45; subject in G major, b19; G-major inversion ×2, b21, 30; subject on B, b37) plus the dialogue fragments. Coro II: 8 (inversion in E minor ×3 at b3, 12, 45; B-minor inversion, b21; subject in E minor ×2, b19, 31; subject in augmentation, b24; subject in G major, b37) plus the questions. Chorale: 7 lines. The critic finds every declared entry (`themes`), with the interval scores noted above.

### The devices, and where to hear them

1. **The subject is the chorale.** Hear it at the **Recognition, b19–21**: the chorale's line 1 (G G G D D E D) with, an octave below, the same notes at double speed in Coro I, and the E-minor subject a tenth below them. It was prepared at b8, where the subject (E minor) and the chorale's line 1 start together.
2. **Two choirs, two forms.** The questions are inversions: b6.1, 7.1 ("Wen?", "Wie?"), 15.3 and 16.3 (in diminution), 29.2 and 30.1 ("Was?", "Wohin?"). On one piano the choirs differ by register (Coro I above, Coro II below), and Coro II's questions are 6 louder and detached; in the binaural render they are also left and right.
3. **Agreement.** The choirs move together three times: rectus in tenths (b19–20), inversus in sixths (b21.2–23.1), rectus in tenths (b37–38).
4. **Exchange.** Line 5 (b30.4/31.2): Coro I takes the inversion, Coro II the subject.
5. **Augmentation** under line 4 (Coro II, b24.4–28.3) and **diminution** in the episode and the second dialogue.
6. **Final stretto** (b45.1/45.3) with only two voices under the chorale; both entries come after a rest, the inversion in the tenor register (B3), the subject in the alto (E4).

### Critic numbers (final)

| | Fugue | Target |
|---|---|---|
| parallels_error / weak | 0 / 0 | 0 |
| beat_parallels | 0 | ≤ 2 |
| dissonance_unresolved | 0 | ≤ 3 |
| bad_doublings | 0 | ≤ 2 |
| pc_tripled_on_beats_pct | 0.0 | — |
| low_register_seconds | 0 | ≤ 9 |
| stepwise_pct | 67.7 | ≥ 65 |
| leap_4th_plus_pct | 8.5 | ~14 in Bach |
| crossings | 0 | few |
| **keyboard_unplayable_pct** | **0.0** (0 of 670 onsets) | < 5 |
| **mean_moving_voices** | **2.55** (of 3); 29 of 49 bars with all three moving | — |
| tertian_fit_pct | 37.6 | — |
| melody notes | 3 leaps larger than an octave, each across a rest (21.2, 43.1 ×2) | — |

Moving voices by section: exposition 1.5; dialogue 1 2.0; line 1 3.0; line 2 3.0; episode 2.0; Recognition 3.0; line 4 2.7; dialogue 2 2.0; line 5 2.8; line 6 3.0; dominant pedal 2.0; line 7 3.0; coda 2.0 (three sounding). The full texture is kept for the chorale lines; every episode and dialogue is in two voices.

**Rhythm.** Of 967 notes, 382 are sixteenths (363 in Coro I, 19 in Coro II), 351 eighths; Coro II also has quarter-note hemiolas (the augmentation) and the eighth-note pulse of the dominant pedal. The chorale moves in dotted halves throughout.

**Registers and playability.** The chorale sits high (D5–E6). Where it holds D6 or E6 and Coro I is below A♯4, Coro II stays within a tenth of Coro I (tenor register), so that one hand takes the chorale and the other both choirs; elsewhere the right hand takes the chorale and Coro I. The critic finds no onset that two hands cannot reach.

### How the notes were written

- Every note is a literal token string in `fugue.py`, placed at a bar and dotted-quarter beat, or an explicit transform (`transpose`, `invert_diatonic`, `scale_rhythm`) of the hand-written subject; RG, IG, SBG, the natural-minor tails and the diminutions are written out by hand.
- **Disclosure of scripted testing.** To choose where whole statements could sit under each chorale line, I used scratch scripts in my session scratchpad (not in the repository) that only **tested** placements: for each written form (S, INV, RG, IG, transpositions, augmentations) at each beat offset they listed the vertical intervals against the chorale line and ran `critic.analyse` on the three-voice fragment. `stretto_finder.py` tested subject/inversion strettos and diminution strettos. I chose among the candidates (the Recognition's inversion pair, the line-5 exchange, the line-6 tenths, the final stretto) and wrote every free voice by hand, fixing each parallel and clash the critic reported by changing the free line. No script chose or inserted notes, and nothing generates notes at build time.
- Performance data only (no notes): phrase dynamics per section, Coro II's questions +6 and detached, and the seats for the spatial render.

### Weak spots (honest)

1. **Bare dialogue.** In b5.3–7.1 and in b29–30 one choir sings at a time, so the texture is a single line for a beat or two at a time (by design: question, then answer). On a piano this may sound thin rather than antiphonal.
2. **Parallel motion.** In three passages (b19–20, b21.2–23.1, b37–38) the choirs move in parallel tenths or sixths: for about six bars the two choirs are one harmonised line under the chorale. It is the "agreement" of the concept, but it is less independent counterpoint than the rest.
3. **The final stretto is still partly bare.** After the third review's changes the choirs meet in a perfect interval on 5 of 24 eighths (was 9): the octave E4/E3 at 45.4 (both forms' own notes) and the dominant at 47.1–47.2 (B4/B2, F♯4/B3) remain. The price is a less literal inversion: its second half is re-voiced (8/16 intervals).
4. **Clashes with the held chorale notes.** Passing C♯ sixteenths in Coro I against the chorale's D in B minor (b11.1–11.3) and Coro II's passing C♯3 under it (b34.4); Coro I's D5 against the chorale's E6 for a quarter in the Recognition's inversion (b21.3, 21.4), which then rises to E. None is flagged by the critic, but they are audible frictions.
5. **Coro I is busy.** It has 363 sixteenths and runs almost continuously under lines 1 (second half), 2 and 4 and in the dominant pedal; since the third review it holds one beat over each of Coro II's entries below it (12.2, 24.4). The risk of étude-like figuration remains.
6. **Long two-voice opening.** The exposition has two entries (as BWV 855 does), and the chorale enters only at b8, after about 28 s of two-voice music.
7. **Tonal range.** E minor, B minor and G major, with A minor and C major only touched (b43, b48); there is no real subdominant key area.
8. **Modal and altered statements.** The G-major forms and the subject on B score 9–10/16 intervals as transfers; four statements have natural or altered tails (b8, b19, b21.2), and the final inversion's second half is re-voiced (b46).
9. **Spatial render.** With `--program 53` (Voice Oohs) the sixteenths may blur; I cannot judge from the files whether the front-centre chorale balances the two side choirs.
10. **Unheard.** Balance, whether the chorale reads as a cantus firmus above the sixteenths, whether the questions sound like questions, and the general pauses (b18.4, b42.4) are for Sam's ears.

### From the eleven-voice version

- **Kept:** the concept (BWV 244/1, two choirs and a ripieno chorale); the subject, note for note; the inversion as the second choir's form; the chorale (BWV 401 in G, an octave above the ripieno) with the chorale on top throughout; the first dialogue's procedure (the subject sung in pieces, interrupted by inverted questions) and its elision, "als wie ein Lamm" → line 1; the **Recognition** under line 3 (G-major subject with the E-minor subject a tenth below), with a breath before it; the final stretto of subject and inversion under line 7, resolving with the chorale's G as the third of E minor; the "Lamm" sigh C–B in the coda.
- **Changed:**
  - 11 voices → 3: each choir is one line, so every entry is a new voice after a rest, with no other voice in its register.
  - Two five-voice expositions → a counter-fugue exposition of two entries, as in BWV 855.
  - One 12/8 surface of eighths and dotted quarters → sixteenth countersubject and episodes (382 sixteenths, against 18 in the old version), diminution dialogues, an augmentation with a hemiola, and a pulsing pedal.
  - New: the Recognition's second half in inversion; the second dialogue with "Was?" and "Wohin?" (the old version used only "Wen?" and "Wie?"); the augmentation under line 4; the exchange of forms under line 5; the dominant-pedal breath before line 7.
  - The final stretto now has nothing else under the chorale (the old one had 6–10 moving voices around it).
  - The chorale breathes between lines; L7 follows BWV 401's rhythm.
  - Length 231 s → 207 s; keyboard-unplayable 35 % → 0 %; stepwise 60.9 % → 67.7 %; low-register seconds 9 → 0; bad doublings 3 → 0; the one beat-to-beat octave is gone.
- **Why:** the owner found the thick textures washed out the counterpoint; the second review found the final stretto buried (F1), four minutes of one rhythmic surface (F2) and two choirs indistinguishable on one piano (F3). Three voices answer F1 and F3 by construction (register, rests before entries, the seats in the spatial render); the sixteenths, diminutions and augmentation answer F2.

---

## Review (REVIEW-3.md) and what changed

The third review found nothing for the critic to report and ranked the fugue the clearest of its batch. Its "must not be touched" passages (b7.2–8.1, the Recognition b18.4–21.2, the cadence at 47.3) are unchanged.

1. **Coro I's perpetual motion (applied, as tested).** Coro I now holds one beat over each of Coro II's entries below it: D5 at 12.2 (under the chorale's D6, while the inversion enters on B3) and G4 at 24.4 (under the chorale's B5, while the augmentation enters on E3). Each entry has a beat to itself, and the two longest runs (b9.3–15.2, b22.4–28.4) are each broken once.
2. **The hollow final stretto (applied, my own remedy).** The reviewer's other distances tested worse, and a lower Coro II approach cost five unplayable onsets, so I kept the placement and re-voiced Coro II, by hand:
   - 46.1: G3–E3 for E3–G3 (Coro II takes the third of E minor under Coro I's E4, and a tenth under G4 replaces the octave G4/G3);
   - 46.3: F♯3–G3–E3 for E3–F♯3–G3 (the chord under the chorale's A and Coro I's B4 becomes B7 with its bass on F♯, and G4 gets E3 under it instead of G3);
   - 47.1: the dominant drops to B2 for a beat, then returns to B3, so the cadence has a bass below E3 without leaving two hands' reach (B2 under Coro I's E4 at 47.2 would not have been playable).
   - Perfect intervals between the choirs on the eighths of 45.3–47.2 fall from 9 of 24 to 5. The inversion's head (45.1–45.4), the part that announces it, is still strict; its second half scores 8/16 intervals, as declared in its label. A passing G3 at 45.4 was tried and rejected: the critic read it as an unresolved dissonance against the chorale's D.
3. **Key range (not changed).** I agree with the reviewer that it follows the chorale: its phrase-ends are D, G, D, G, D, B and G, which the fugue harmonises in B minor, G major and E minor, and BWV 244/1 itself stays close to E minor and G. A real move to A minor or C would have to fight the chorale's own phrase-ends.
4. **The bare dialogues (not changed),** for the reviewer's reason: the register gap and the accented questions make them a dialogue, and their thinness makes the arrival of the chorale at b8 felt.

Critic after the changes: parallels 0 / 0, beat parallels 0, unresolved 0, bad doublings 0, low-register seconds 0, crossings 0, stepwise 67.7 %, keyboard-unplayable 0 of 670 onsets, mean moving voices 2.55. Every note was written by hand; a scratch script only counted the perfect intervals in the stretto. Renders rebuilt: `fugue.*` (Bach/Lehman), `fugue-equal.mp3`, `fugue-spatial.mp3` (`--layout score --program 53`).

