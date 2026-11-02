# Pair X in E minor: second review (third edition, as built on 27 October)

**Scope.**
- `prelude.py` → `prelude.json` (35 bars, 4/4: Aria b1–17, Presto b18–35, about 1:47);
- `fugue.py` → `fugue.json` (56 bars, 12/8, eleven voices, about 4:06);
- `NOTES.md`.

**Method.** I read every bar and ran `critic.py` and `reduce.py --per beat`, plus these scratch scans (not in the repository):
- **Grid views** at dotted-quarter, eighth and sixteenth resolution.
- **Entry salience.** For each statement: its rank from the top at its first note, other attacks at that instant, and velocity.
- **Struck semitones.** m2, M7 and m9 pairs attacked together.
- **Unisons and near-unisons under the chorale.**
- **Every fix below was tested.** I applied it to a scratch copy of the source, rebuilt it and re-ran the critic. Nothing in the repository was changed.

I have not heard the renders. In the 12/8 fugue, beats are dotted quarters, as in the NOTES (`b51.3` = the third dotted quarter of bar 51).

## Verdict

**The best-conceived pair of the four for a listener.**
- **The chorale will emerge.** It is the top voice 100 % of the time, at +10 velocity, and never closer than a third to the voice below except for two passing unisons.
- **The Recognition (b26–29) will be audible.** The subject in G major runs directly under chorale line 3 in tenths with its E-minor form.

**Four things will disappoint:**
1. **The final stretto (b49–53) is buried by filler.** It is the fugue's last fugal argument. The second pass added one-note "answering" pecks so that all eleven voices attack in every bar (the NOTES admit as much), and they smother the two final entries. The chorale is heard; the fugue is not.
2. **Four minutes of one surface.** The rhythm is the same throughout (eighths and dotted quarters only, not one sixteenth in 56 bars) and the same procedure recurs (a chorale line every six bars, b14, 20, 26, 32, 38, 44, 50). The pair lasts six minutes.
3. **On one piano, the two choirs are one texture.**
4. **The prelude's aria** repeats one three-bar left-hand unit four times, note for note. The Presto's canon (b28–29) packs five struck ninths and sevenths and an A♯/A cross-relation into one bar.

## Ranked issues (both movements)

| # | Mvt | Bars | Problem | Severity | Minimal fix (tested) |
|---|---|---|---|---|---|
| 1 | Fugue | 49–53 | Final stretto entries (S1 inversion 50.1, Bar2 subject 51.3) buried under pecking filler and a soprano shadowing the chorale | **High** | Remove five free lines (F1) |
| 2 | Fugue | all | 4:06 of one rhythmic surface and one procedure; the broadening starts 8 bars before the end | Medium | ♩. = 60, broaden only from b53 (≈ 3:48) |
| 3 | Fugue | 11–13, 17–25, all | Coro I and Coro II are indistinguishable on one piano | Medium | Coro II −6 outside its statements; "Wen?/Wie?" accented |
| 4 | Prelude | 2–16 | The ground and figure are an identical 3-bar unit ×4; b13 ≡ b4; three half cadences on B | Medium | Figure in sixteenths in b14–16 |
| 5 | Prelude | 28–29 | Canon at one beat: 5 struck m9/M7 and an A♯5/A3 clash in one bar, two on beats | Low–medium | Left hand −8 in b28–29 (an echo canon) |
| 6 | Fugue | 48 | The mirror pair collapses into octave D's in the "breath" bar | Low | Accept, or re-voice Bar2 |
| 7 | Prelude | 2.3 | The chorale's repeated E5 is struck over the ground's D♯3 | Low | Accept |

---

## Prelude X: Aria e Presto

### Must not be touched

- **The Presto's invertible counterpoint** (b18–27). Motive M in sixteenths over the counter-line C in eighths, exchanged in B minor, then G major, then E minor: real two-part writing with drive.
- **The attacca.** The run-out stops on D♯4 over B1; the Fugue's first E4 resolves it.
- **The chorale paraphrase in the aria.** It plants "O Lamm Gottes" before the fugue makes it the eleventh voice.

### P1. b2–16: one left-hand unit, four times (Medium)

**What is written.**
- `GROUND[0..2]` and `FIGS[0..2]` accompany b2–4, b5–7, b11–13 and b14–16 identically: E–D♯–D–C♯–C–B in half notes, under the same two-note eighth oscillations (`G3 B3 G3 B3 | A3 F♯3 A3 F♯3 …`).
- b13 is b4 in all three voices (RH `'C5:4 A4:4 B4:8'`).
- The aria makes half cadences on B at b4, b7 and b13.
- The right hand is mostly quarters and halves.

**Why it fails.**
- Twelve of seventeen bars at ♩ 56 (about 50 s) have exactly the same accompaniment.
- The repeated half cadences make the aria feel as if it starts over three times.
- BWV 855, the model, keeps its left hand regular too, but its bass descends without repeating itself and its right hand is florid. Here the left hand repeats and the right hand is plain.

**Fix (tested; critic: 0 parallels, 0 unresolved, playable).** In the last phrase, let the figure double its speed. The aria then gathers motion into its cadence and towards the Presto:
- b14 Figure: `'G3:1 B3:1 E4:1 B3:1 G3:1 B3:1 E4:1 B3:1 F#3:1 A3:1 B3:1 A3:1 F#3:1 A3:1 B3:1 F#3:1'`
- b15 Figure: `'G3:1 B3:1 D4:1 B3:1 G3:1 B3:1 D4:1 B3:1 E3:1 G3:1 B3:1 G3:1 E3:1 G3:1 B3:1 G3:1'`
- b16 Figure: `'E3:1 A3:1 C4:1 A3:1 E3:1 A3:1 C4:1 A3:1 F#3:1 A3:1 B3:1 A3:1 F#3:1 A3:1 B3:1 A3:1'`

Avoid D♯4 in b16's figure: it doubles the melody's leading tone. Also avoid ending b14 on A3, which makes octaves with the melody's A4→G4.

**Optional.** Ornament the right hand of phrase 4 (b11–13) with BWV 855-style turns, so that b13 no longer duplicates b4.

### P2. b28–29: the canon's collisions (Low–medium)

**What is written.** Motive M against itself one beat later, two octaves lower. In bar 29 these are struck together:
- A♯5 against A3 (a chromatic clash, 29.1, 2nd sixteenth);
- G5/F♯3;
- C6/B3 on beat 2;
- B5/A♯3;
- B5/C4 on beat 3.

**Assessment.**
- At ♩ 132 they pass in under two seconds, but in two parts every vertical is exposed, and at the Presto's loudest (+10).
- I tried other canon intervals and distances; none is clearly cleaner, because the clashes come from the motive's own neighbour notes.

**Fix.** Keep the canon, but play the left hand 8 softer in b28–29, an echo canon. The ear then takes the lower voice as a shadow, not as a collision.

### P3. Smaller points

- **b2, dotted beat 3 (2.3).** The chorale's second E5 is re-struck against the ground's D♯3: tonic over leading tone, a minor ninth, for a dotted quarter, resolving to D♯5 only for the last sixteenth. It is expressive and very Bach. Accept it, but it is the first thing the melody does, so make sure the render does not accent it.
- **b30–34.** 4½ bars of pumping B2/B3 octave eighths, then a B7 arpeggio to B5 (b33). This is étude figuration rather than M and C. It is short at Presto; acceptable.

---

## Fugue X à 11: Fuga a due cori con corale

### Must not be touched

- **The chorale's placement.**
  - It is always the top voice (G5–E6), at +10 velocity.
  - The nearest choir voice is almost always a third or more below. It meets the chorale in unison only for three eighths in b20 (Soprano I) and one in b26 (Soprano II), and comes within a whole tone for a few eighths in b26, b53 and b55. F1's fix removes the b53 case.
  - Each chorale note is re-struck every two beats, so it will not decay away.
  - The device will be heard.
- **V. Recognition (b26–29).**
  - Alto I's subject in G major is the second line under the chorale, moving in tenths with Baritone II's E-minor form.
  - Chorale line 3 (= line 1) sounds above at half its speed.
  - This is the one place where a listener can hear that the subject is the chorale.
- **The ending.** The chorale's final G5 becomes the third of E minor. The coda's staggered arrivals by upper neighbour (C5→B4 in Alto I at 55.1, C5→B4 in Soprano II at 55.2, F♯5→E5 in Soprano I at 55.3) are audible sighs over a held chord: the "Lamm" sigh C–B, three times.
- **II. Dialogue (b11–13).** Coro I is silent during each of Coro II's interjections ("Wen?" at 12.3, "Wie?" at 13.3), so the question and answer are clean.

### F1. b49–53: the final stretto is buried (High)

**What is written.**
- **Thematic.** Bass II's G-major inversion (49.1) is audible as the bass. Soprano I's inversion under the chorale (50.1) and Baritone II's subject with Tenor I's countersubject (51.3) are the two final entries.
- **Soprano I's entry.** It begins fourth from the top, with nine other voices attacking at the same instant. Above it are the chorale, Soprano II's free line (`'G5:6 A5:6 B5:6 G5:12 F#5:18 G5:18 A5:6 A5:6'`, which shadows the chorale in thirds and sixths), and Alto I's free `'E5:6 A4:6 D5:6 E5:6 E5:6 …'`. The critic notes that Alto I rises above Soprano I.
- **Baritone II's subject.** It is sixth of seven.
- **The second-pass pecking.** Around them:
  - Alto II: `'G4:6 R:12 G4:6 R:6 B4:6 R:6 B4:6 R:6 G4:12 R:6 B4:12'`;
  - Baritone I: `'E3:6 R:18 B2:6 R:12 F#3:6 R:6 G3:6 R:6 D3:6'`;
  - Bass II: `'E3:6 R:18 G2:6'`.

**Why it fails.**
- These lines exist to make every voice "move" in every bar. They are chord tones struck on the beat, exactly what the brief says does not count as a voice.
- They make b50–53 a busy chorale harmonisation. The fugue's last stretto, which the coda then mirrors, is not heard.

**Fix (tested; critic unchanged: 0 parallel errors, 0 unresolved, the one beat parallel at 53.2–53.3 as before; low-register clashes 11 → 9).**
- `put('A2', 50, 1, 'G4:6 R:12 …')` → `put('A2', 50, 1, 'R:84')`.
- `put('Bar1', 50, 1, 'E3:6 R:18 …')` → `put('Bar1', 50, 1, 'R:72')`.
- `put('B2', 51, 1, 'E3:6 R:18 G2:6')` → `put('B2', 51, 1, 'R:30')`.
- `put('S2', 50, 1, 'G5:6 A5:6 …')` → `put('S2', 50, 1, 'R:78')`.
- `put('A1', 50, 1, 'E5:6 A4:6 D5:6 E5:6 E5:6 R:24 B4:12 D5:6')` → `put('A1', 50, 1, 'R:54 B4:12 D5:6')`.

**Results.**
- Soprano I's inversion is then the second voice, directly under the chorale.
- Moving voices in b50–53 become 6, 6, 7, 10, instead of 10, 11, 11, 11.
- The eleven still converge at 53.3, so the growth from the stretto to the full close becomes an audible event.
- Also give Baritone II's subject at 51.3 +8 velocity. It is the final cadence, and it is still fifth of six.

### F2. Four minutes of one surface (Medium)

**What is written.**
- Note values: 487 eighths, 514 dotted quarters, 182 quarters, nothing shorter.
- 58–85 % of eighth slots are attacked in every four-bar span, so the surface is a constant 12/8 lilt.
- Two complete five-voice expositions (Coro I b1–10, Coro II b17–25) take the first 1:45.
- The chorale lines then arrive every six bars. The tempo map broadens from b48 (♩ 84 → 80 → 74 → 60 → 50), so the last eight bars are progressively slower.

**Why it fails.**
- BWV 244/1 sustains its seven minutes with orchestral sixteenth figures, a pulsing bass and constant changes of scoring.
- On one piano, without timbre, this fugue's variety has to come from rhythm and harmony, and the rhythm never changes.
- At 4:06 it is the longest fugue so far, after a 1:47 prelude: "excessive length" is the risk.

**Fix.**
- `'bpm': 84` → `90` (♩. = 60).
- `tempo_map` → `[[144, 90], [150, 82, 'ramp'], [150, 90], [312, 90], [324, 78, 'ramp'], [330, 64, 'ramp'], [336, 54, 'ramp']]`.
- This keeps the breath before the Recognition and broadens only from the coda (b53). Duration ≈ 3:48.
- If more is wanted, let one free voice in each chorale gap move in sixteenths, like the flutes of BWV 244/1, for example the "Sehet" head in diminution at b42.3–43.1.

### F3. Two choirs, one piano (Medium)

**What is written.**
- The two choirs occupy the same registers.
- The antiphony is spatial (`antiphonal-centre`). On the piano renders, Coro II's "Wen?" (B4 B4 C5 / G4 F♯4 E4 / E3 G2 A2) is just a three-note chord in the middle register.
- Coro II's soprano sounds only 25 % of the time.

**Why it matters.** The dialogue is cleanly composed (F1's "must not be touched"), but nothing identifies the answering choir.

**Fix.**
- Give Coro II a constant −6 base velocity outside its declared statements (the entry boost keeps those up), so that it becomes the "other" choir on one instrument.
- Accent its "Wen?" and "Wie?" interjections (+8, gate 0.7), so that they cut in as questions.

### F4. b47–48: octaves in the breath bar (Low)

**What is written.** The mirror pair (Soprano I's answer, Alto II's inverted answer) meets Baritone II's line on D twice in the three-voice "breath": D5/D4/D3 on the third eighth of dotted beats 1 and 3.

**Assessment.** For a moment the three voices sound as one. This is inherent to a mirror about its axis. Accept it, or re-voice Baritone II's line in b48 (untested).

### Eleven voices: lines or texture?

- **Audible lines.**
  - The chorale.
  - Coro I's soprano, which is the highest sounding voice for 40 % of the time it sings.
  - The bass (Bass I or Bass II, whichever is lower).
  - Each new entry in the two expositions, because they enter one at a time, from the top down (Coro I) or from the bass up (Coro II).
  - Alto I in the Recognition.
- **Texture.** The inner choir voices in the tuttis. Six of them sound most of the time and nine to eleven at the end.

**The advertised device.** The chorale above two choirs will be heard as a cantus firmus above a choral fugue. It will not be heard as two choirs, except in the spatial render.
