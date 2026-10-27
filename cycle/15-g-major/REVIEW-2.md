# Pair XV in G major: second review

**Fugue a 16 sopra "Vom Himmel hoch", and Pastorale**

**Scope.**
- `fugue.py` → `fugue.json`: 59 bars, sixteen voices in four SATB choirs.
- `prelude.py` → `prelude.json`: 16 bars of 12/8.
- `NOTES.md`.

**Method.**
- I read every bar as note lists and ran `critic.py`, `reduce.py --per beat` and `stretto_finder.py`.
- Scratch scans:
  - voices sounding vs. distinct pitches per beat, and a list of every unison;
  - pitch classes per beat;
  - attacks per sixteenth slot;
  - each voice's sounding bars.
- Fixes marked **tested** were built from a scratch copy of the source and compared with the current build with `critic.analyse`: no new parallels, unresolved dissonances or low-register clashes unless stated.
- The music21 corpus copy of BWV 248/23, which the NOTES cite, was read to check the allusion suggested for the prelude.

I have not heard the renders.

## Verdict

The best things here are the subject S1 and the idea of four choirs, each with its own diminution of one chorale line:
- S1 has a dotted skip, a held G on the weak beat, and a peal of sixteenths.
- S2 is a fanfare, S3 a siciliano, S4 bells.

Line 1 sung high over the S1 stretto (b11–14) is the piece's most beautiful and most audible moment.

But the advertised summit will not be heard as advertised, and the "sixteen voices" are mostly a relay of four-voice groups.

- **At the summit (b41–46) the four lines will not be heard together.** 47 two-beat scale figures, placed by a harness, attack on the same beats as the chorale notes. Some double them at the unison. 23 of the 24 beats contain all seven notes of G major.
  - Line 1 on top will be heard, and line 4 in the bass mostly.
  - Lines 2 and 3, and all four canonic answers, will not.
- **For 50 of 59 bars (b1–40, b47–56) only 3–6 voices sound** (section means 3.1–5.5). Choirs fall silent when the next one enters.
- **The summit has no arrival.** It stops on a mixture and drops from 12 voices to 6.
- **Harmonically it never leaves the seven notes of G major.** After b9 only five notes in fifty bars are chromatic. This is the root of the static harmony, and of the summit's white-note wash.
- **The tempo is an Allegro in name only.** The marking is "Allegro, con allegrezza" at ♩ = 66, and the tempo then keeps slowing: 58, 52, 42, 32.

## Ranked issues

| # | Mvt | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|---|
| 1 | Fugue | 41–46 | The four chorale lines are swamped. Figure attacks coincide with every chorale attack; figures double L2 at the unison; L2 inversus and L4 merge on D3; Bass I crosses under L4 | **High** | **Tested.** Delete the 17 figures in b41–42 (the summit becomes a crescendo, 8 → 14); boost the chorale statements |
| 2 | Fugue | 1–40, 47–56 | Sixteen staves, 3–5 sounding voices (means 3.1 / 5.0 / 4.6 / 4.6); voices pop in for a bar or two | **High** | **Tested instance.** Make sections II–III double fugues: earlier choirs keep singing their subject against the new one |
| 3 | Fugue | all | "Allegro, con allegrezza" at ♩ = 66, broadening five times; 3:54 | Medium-High | ♩ = 80, broaden only at b47 and the end: about 3:09 |
| 4 | Fugue | 10–55 | Harmonic stasis: after b9 only five notes in 50 bars leave the G-major scale (1.3 % of the piece, against 6.6–7.9 % in Fugues V and I); answers are modal, "E minor" has no D♯ | Medium-High | Make S2 and S3 answer tonally at least once; secondary dominants at the section cadences |
| 5 | Fugue | 46–47 | The summit ends without a cadence; 12 → 6 voices onto an unprepared C | Medium | **Tested.** Bass I lands on G2 at b46.3; the four last figures stop at 46.2 |
| 6 | Fugue | 56–58 | B-A-C-H in the tenor, in whole notes, under five voices | Medium | **Tested.** Give it to Soprano I (B♭5 A5 C6 B5) |
| 7 | Fugue | 20–23, 28–31 | Cantus lines 2 and 3 are inner voices, masked by neighbours in their register | Medium | Raise cantus velocity; keep neighbours out of their band |
| 8 | Prelude | 13, 7–8 | Misses its own source: BWV 248/23 is a 12/8 pastoral setting of this very chorale; 16 rhythmically identical bars | Low-Medium | **Tested.** Quote Bach's flute interlude at b13 (piffero rests); Bach's passing notes in line 2 |

---

## Must not be touched

- **The exposition and first cantus, b1–14.**
  - S1 is lively and has a shape a listener can hold.
  - The codettas (b5, b10) move the harmony with purpose.
  - At b11–14, line 1 in half notes high in Coro II's soprano (G5 F♯5 E5 F♯5 D5 E5 F♯5 G5), over a stretto two beats and then 1½ beats apart, is the clearest realisation of the chorale-fugue idea in the piece.
- **Line 1's entry at the summit, b40.2.** It comes with the chorale's own upbeat, C6, at the top. It is the one chorale entry of the summit that a listener will certainly catch. Keep it at the top and keep its upbeat.
- **Prelude: the musette** (drone, piffero, siciliano tune) and the attacca half cadence answered by the fugue's lone G.

---

## 1. Summit, b41–46: the four lines are not heard together (High)

**What is written.** The combination itself is real.

| Line | Voice | Notes | Register band |
|---|---|---|---|
| L1 in C | Soprano I | C6 B5 A5 B5 G5 A5 B5 C6 | A5–C6 |
| L3 | Soprano III | B4 E5 E5 D5 F♯5 G5 E5 D5 | B4–G5 |
| L2 | Alto II | G4 G4 D4 D4 B3 D4 C4 B3 | B3–G4 |
| L4 | Bass IV | G3 F♯3 E3 D3 D3 C3-B2 A2 G2 | G2–G3 |

Each line has its own octave band, which is ideal for hearing four lines. Then the canonic answers enter (Alto III, Alto I, Bass II, Alto IV), the S1 stretto (Soprano IV, Tenor I, Soprano II, Tenor IV, Soprano I), 15 heads, and 47 two-beat figures (bells, tattoo, run, rounds, change) in every remaining voice.

**What happens on the keys.**
- **Attacks.** Every chorale note changes on beat 1 or 3, and every figure is placed on beat 1 or 3. In b41–42 every sixteenth slot has an attack. On 91 % of them three or more voices attack together (mean 5.9). On beats 1 and 3 of b41–42, 11–14 voices attack together, and each chorale note is just one of them.
- **Unisons on the chorale's own notes.**
  - Tenor II strikes D4 at 41.1 and B3 at 41.3 (its tattoo and change figures) and D4 at 42.1 (its S2 head). These are exactly Alto II's L2 notes at the same instants.
  - At b42.3–4, Bass II's L2 *inversus* (D3 D3) and Bass IV's L4 (D3 D3) are on the same key: two chorale lines merge into one.
  - Alto III's L3 inversus is doubled by Tenor I (E4, 42.2) and Tenor II (F♯4, 42.3).
- **The bass line is crossed.** Bass I's rounds go `B2 A2 G2 F#2` under L4's D3 at b42.3–4. L4 is a descending scale, and so are Bass I's and Bass III's ROUNDS figures around it, so L4 merges into them.
- **Harmony.** 23 of the 24 beats in b41–46 contain all seven pitch classes of G major (each for at least a fifth of the beat). The chorale lines' own harmony (C, G, D/F♯, Em, Em7/D, D7 …, as tabled in the NOTES) is inaudible as harmony.

**Which voices are lines.** The figure voices are patchworks. Bass I, b41–46, sings CHANGE, RUN, ROUNDS, ROUNDS, ROUNDS, CHANGE, the S1 head, BELLS, RUN, joined by leaps of a ninth to an eleventh (b43.1 and b46.3 F♯2 → C4). Alto I, Tenor III, Alto IV and Tenor II are made the same way. These voices are texture.

**What the listener will hear.**
- L1 on top in C: **yes**.
- L4 as the bass: **mostly**, except b42.3–4.
- L3: **only in b39–40**, where it enters in a four-voice texture.
- L2 and the four canonic answers (including line 4 per augmentationem in Alto IV): **no**, until the texture thins at b47.
- The rest: a bright, pandiatonic bell-wash. That is pleasant and seasonal, but it is not "the four lines together".

**Fix (tested).**

1. **Delete the 17 figures in b41–42.** These are all the `put(...)` lines whose comment begins `# subject` (bells, tattoo, run, rounds, change) at bars 41 and 42:
   - Alto I: 41.1, 41.3, 42.1;
   - Bass II: 41.1, 41.3;
   - Tenor III: 41.1, 41.3;
   - Alto IV: 41.1, 41.3, 42.1, 42.3;
   - Tenor II: 41.1, 41.3;
   - Bass I: 41.1, 41.3, 42.1, 42.3.

   **Result.**
   - Moving voices b39–47 go from `4 8 15 14 14 14 12 12 6` to `4 8 9 12 14 14 12 12 6`: the summit becomes a crescendo, and all four lines plus the first canonic answer are heard entering.
   - Attacks per onset fall from 5.9 to 3.1, and slots with three or more attacks from 91 % to 45 %.
   - Four melodic flags disappear (b41.3, b42.1, b42.3, b43.1), and crossings in b39–47 drop from 33 to 24.
   - Nothing new is flagged.

   The figures stay for b43–46, which is the right place for the bells: the canons are running and the leaders are ending.
2. **Bring out the chorale statements.** After `build_score`, add +8 velocity to the events of the eight summit chorale statements, and −4 to the `put()` figures. The canons by inversion are sung by inner voices; without this they will not register even in the thinner texture.
3. **From b43 (not tested).** Keep the figures off the attack beats of the chorale notes: start them on beats 2 and 4, or shorten them to one beat. Then each chorale note is struck into a gap.

---

## 2. Sixteen voices, mostly three to five (High)

**What is written.**

| Section | Bars | Mean sounding voices |
|---|---|---|
| I | 1–14 | 3.1 |
| II | 15–23 | 5.0 |
| III | 24–31 | 4.6 |
| IV | 32–38 | 4.6 |
| Approach | 39–40 | 4.6 |
| Summit | 41–46 | 11.8 |
| Dissolution | 47–51 | 4.7 |
| Coda | 52–56 | 5.5 |
| Last chord | 57–59 | 11.3 |

Sounding bars before the summit, per voice:
- Bass II: 4 of the 24 bars after its entry;
- Bass III: 2 of 12;
- Tenor III: 4 of 13;
- Tenor I is silent from b15 to b35, Alto I from b20 to b33, Soprano III between its few entries.

The NOTES admit that "the accumulation 5 → 9 → 13 → 16 is nominal".

**Why it fails.** Each section is a four-voice choir fugue over a cantus, while the previous choir mostly rests. The listener hears four small fugues in succession, then a six-bar tutti, then a last chord. This is the brief's "many-voice fugues … harmony rather than counterpoint" turned inside out: here there is counterpoint, but never more than five lines of it until b41.

**Fix: double fugues, so the earlier choirs keep singing their own subject.**
- `stretto_finder` finds:
  - S1 inversus against S2 at +4 to +8 sixteenths;
  - S1 rectus a tenth below S3 at offset 0.

  Both have 0 parallels and 0 unresolved dissonances in two voices.
- **Tested in the full texture.** Tenor I (silent b15–35) answers Coro II's stretto with inverted S1 at b16.3:
  ```
  theme('T1', 16, 3, dshift(inv(S1, 'G4'), -3), 'I: subject 1 inverted against subject 2', 2)
  ```
  This gives `D4:3 E4:1 F#4:2 E4:2 G4:2 F#4:1 E4:1 D4:4 G3:1 A3:1 B3:1 C4:1 D4:1 E4:1 F#4:1 G4:1 F#4:1 E4:1 D4:1 C4:1 E4:2 G4:2`.
  - It needs one change: Soprano I's last note in `put('S1', 15, 1, …)`, `G5:8 F#5:4` → `G5:8 A5:4`. Otherwise the two make a weak octave G–F♯ at b18.1.
  - Result: no new flags, and two seventh flags at b18.2 disappear.
- My search over b16–18 found clean placements only for Tenor I; none for Alto I. In section III, try S1 a tenth below S3 in a tenor or bass of Coros I and II, which are idle there. Then the choirs accumulate for real: 5 → 7 → 9 → 11 → 16.

---

## 3. Tempo and character (Medium-High)

**What is written.**
- `bpm` 66 with "Allegro, con allegrezza".
- Ramps to 60 at the cadences of b14 and b31, to 58 for the summit, to 52 for the dissolution, then 42 → 32 on the last chord.
- The tempo map gives 3:54.

**Why it matters.**
- At 66 the subject's sixteenths are 4.4 notes per second: moderato.
- The cantus half notes at 58 last 2.1 s each.
- The summit, the piece's most jubilant moment, is slower than everything before it.
- After a 33-s summit come 63 s of dissolution and coda.

**Fix.** `BPM = 80`, and a map that keeps the cadential breaths but slows only after the summit:
```
[[0, 80], [52, 80], [56, 72, 'ramp'], [56, 80], [120, 80], [124, 72, 'ramp'], [124, 80],
 [184, 80], [202, 66, 'ramp'], [222, 60], [230, 48, 'ramp'], [236, 36, 'ramp']]
```
That is about 3:09, and the summit lasts 24 s instead of 33.

---

## 4. Harmony: three minutes inside the seven notes of G major (Medium-High)

**What is written.**
- Only 24 of the fugue's 1,781 notes (1.3 %) lie outside the G-major scale. By the same count Fugue V of this edition has 6.6 % and Fugue I 7.9 %.
- Nineteen of them are the C♯s and the G♯ of the exposition's real answers and codettas (b3–9). After b9 there are five in fifty bars: D♯ at b23 (two), C♯ at b31 (two), B♭ at b56.
- S2, S3 and S4 are all answered "modally", inside the G-major scale (the NOTES cite Pachelbel's chorale fugues). So:
  - "D" is D-mixolydian;
  - the "E minor" of section III (b24–31) has no D♯; its harmony runs `Em C D Em | D7 Em D7 G | …`;
  - "B phrygian" has no C♯.

**Why it matters.**
- From b10 to b55 the ear never changes key. Every cadence is to G, D-mixolydian or E-aeolian with the same seven notes.
- That is the root of Sam's "long harmonically static stretches" in this piece, and of the bland "too far from the WTC idiom" sound. Bach's chorale fugues answer modally at the entry but still modulate by their secondary dominants.
- It is also why the summit saturates into a white-note cluster (issue 1): there is no leading tone to give any beat a direction.

**Fix (not tested).**
- Answer S2 and S3 tonally at least once, as S1 is answered at b3 and b8:
  - the soprano's S2 entry at b18 (`dshift(S2, 4)`) as a real answer in D, `W.transpose(S2, 7, 4)`, which has C♯;
  - Soprano III's S3 answer at b25 as a real answer, `W.transpose(S3, 7, 4)`, in B minor with C♯.

  Rewrite the Coro I/II quarter-note accompaniment around them.
- Give the section cadences their secondary dominants:
  - A major (C♯) before the D chords that approach the G cadence at b14.3;
  - B7 (D♯) instead of D7 before the E-minor chords of b24–27 (`D7 Em D7 G` → `B7 Em D7 G`).
- In the summit's b43–46 figures, one chromatic inflection per bar, such as a C♯ in a bells figure over D or a G♯ over E, would give the bell-wash a harmonic direction.

---

## 5. b46–47: the summit has no arrival (Medium)

**What is written.**
- b46 ends on figures: Soprano II and Soprano III bells, Alto III change, Bass III change, Bass I run C4 B3 A3 B3 G3 E3.
- The harmony of b46.3–4 reads Gmaj7/A | Eø7.
- b47.1 brings Bass I's C2 under D4, D4, G4 and A3, a C-add-9 with 6 voices left.
- Six bars of 12–15 voices simply stop.

**Fix (tested).**
- `put('B1', 46, 3, oc(dshift(RUN, 0), -1))` → `put('B1', 46, 3, 'G2:8')`. Bass I's bells end on F♯2, which now resolves to G2.
- Delete the four figures at 46.3: `S2` bells, `S3` bells, `A3` change, `B3` change.

**Result.**
- The summit lands on G at b46.3 with Alto IV's L4-augmented G4, the subject tails of Soprano I and Tenor III, and Alto II.
- The dissolution then begins on C (IV) as written.
- Two "leap > octave" flags in Bass I (b46.3, b47.1) disappear, and nothing new is flagged.

---

## 6. b56–58: B-A-C-H is hidden (Medium)

**What is written.**
- Tenor I sings `Bb3:16 A3:8 C4:8 B3:24` in whole and half notes.
- Over it: Soprano I G5 D6 B5, Soprano II A5 D6, the altos, and at b56.1–2 still the end of the coda's head stretto.
- The NOTES expect it to be "probably hidden".
- B♭ is the only flat in the piece. Put it on top and nobody can miss it.

**Fix (tested).** Swap the two lines and adjust Soprano II:
```
theme('S1', 56, 3, 'Bb5:16 A5:8 C6:8 B5:24', 'I: B-A-C-H', 3)
put('T1', 56, 3, 'G3:16 D4:16 B3:24')
put('S2', 56, 3, 'R:16 D5:16 D5:24')
```
- Soprano II's old `A5` would double the signature's A at the unison, and `F#5 → G5` makes octaves with the bass's F♯2 → G2.
- Result: no new flags; the signature ends on the third of the last chord, at the top.

---

## 7. Cantus lines 2 and 3 are inner voices (Medium)

**What is written.**
- **L2 (Alto III, b20–23: G4 G4 D4 D4 B3 D4 C4 B3).** From b21, Alto II moves in quarters just above it (F♯4 E4 F♯4 A4 over D4), and that is the line the ear will follow. L2 has Soprano I, Soprano II and Alto II above it, and Tenor II and the basses below.
- **L3 (Tenor IV, b28–31: B3 E4 E4 D4 F♯4 G4 E4 D4).** Alto III's inverted S3 runs triplets through E4–B3 at b29–30, right in the cantus's band.
- The registral idea "vom Himmel hoch … da komm ich her" (the cantus descends choir by choir) is clever on paper. By ear, L1 (top) and L4 (bass) will be heard; L2 and L3 will not.

**Fix.**
- Give every cantus statement +8–10 velocity (as in 1.2).
- In b21–22, keep Alto II a sixth or more above L2, or give it longer notes on L2's attack beats. Its `F#4:4 E4:4 F#4:4 A4:4` sits a third above L2's D4.
- Moving Alto III's b29 inversion an octave up was tried: it makes a beat-to-beat fifth with the cantus at b29.3. An octave down gives six new low-register clashes. So the cure at b29–30 is to thin, not to transpose: let Alto III start its inversion a bar later, after the cantus's E4 E4 (not tested).

---

## 8. Prelude: "Pastorale for the shepherds" (Low-Medium)

**What is written.**
- Sixteen bars of 12/8, all with the same layering:
  - the piffero plays twelve eighths in every bar, broken chords, 38 % stepwise;
  - the bordone plays four dotted quarters, rocking G2–D3.
- The tune is the chorale in siciliano rhythm (3–1–2).
- About 1:14.

**A missed allusion, verified.** The NOTES cross-check the tune against BWV 248/23, but `corpus.parse('bach/bwv248.23')` shows that this movement is itself in **12/8**. It is a pastoral setting of exactly this chorale, with **flute interludes** between the lines. Those interludes are the Christmas Oratorio's shepherd music, in G, using the prelude's own 3–1–2 rhythm. Its bar 3 (flutes) is:
```
G5:3 E6:1 D6:2 D6:3 G5:1 F#5:2 G5:3 E6:1 D6:2 D6:3 G5:1 F#5:2
```
That is an audible, exact, cheeky allusion the piece already half-makes.

**Fix (tested).**
- **b13.** Replace the "bells" bar with Bach's flute bar at its own pitch, rest the piffero and turn the drone into G–B:
  ```
  B.bar('bells', Zampogna='G5:3 E6:1 D6:2 D6:3 G5:1 F#5:2 G5:3 E6:1 D6:2 D6:3 G5:1 F#5:2',
        Piffero='R:24', Bordone='G2:6 B2:6 G2:6 B2:6')
  ```
  - The piffero's one-bar silence is also the prelude's only change of texture.
  - Keeping the G2–D3 drone instead makes beat-to-beat octaves with the tune (G5/G2 → D6/D3), and keeping the piffero makes the right hand span B4–E6.
- **b7–8, line 2.** Currently `G5:6 G5:6 D5:6 D5:6 | B4:6 D5:6 C5:6 B4:6`: two repeated notes in plain dotted quarters, the stiffest bars. Use Bach's own soprano from BWV 248/23:
  ```
  b7: 'G5:6 G5:6 D5:6 D5:4 C5:2'     b8: 'B4:4 C5:2 D5:6 C5:6 B4:6'
  ```
- Both changes together: 0 parallels, 0 unresolved, 0 % unplayable. Credit BWV 248/23 in the NOTES.

---

## Note on the sixteen voices

| Bars | Lines | Texture |
|---|---|---|
| 1–40 | 3–5 at a time, real (subjects, countersubject, free lines, cantus), passed from choir to choir | |
| 41–46 | The four chorale lines, the four answers and the S1 stretto. On the keys: 11.8 voices sounding, 9.6 distinct pitches | The figure voices: Bass I, Alto I, Tenor III, Alto IV, Tenor II, Bass III and parts of Soprano III and Soprano II |
| 47–56 | 5–6 lines with heads in stretto | |
| 58 | All sixteen strike the last chord; eight of them enter only for it | |

The piece is a lively chorale fantasia for four alternating SATB choirs with one tutti. Fixes 1, 2 and 5 are what would let a listener hear sixteen parts as more than a count of entries. Fix 4 is what would make them go somewhere.
