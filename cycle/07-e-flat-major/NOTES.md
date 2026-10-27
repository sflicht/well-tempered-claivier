# Pair VII in E-flat major: notes

**Files**
- Sources: `prelude.py` and `fugue.py`. Every note is written as literal bar strings in sixteenth units. The only operations applied to written material are explicit, named transforms from `tools/wtclib.py`: `transpose`, `invert_diatonic` and `scale_rhythm`. The fugue adds a region-aware `mirror()`, built from those three and defined in `fugue.py`.
- Built scores: `prelude.json` and `fugue.json`.
- Renders: `renders/` (listed at the end of this file).

**Basis and limits**
- Searches were used to *propose* material: the subject's pitches, the summit's entry levels and voice order, and passing notes for the fugue's free voices (§7). They ran as scratch scripts on the strict 16th-grid pair cost and `critic.analyse`. What they proposed was then written into the sources by hand. No search code is in the sources.
- **I cannot hear the renders.** Everything below comes from the score and the tools. None of it describes how the pair sounds.

---

## 1. Concept

**Fugue VII à 8, "Fuga a due cori"** is a fugue for two four-voice choirs.
- The models are the Venetian *cori spezzati* (Giovanni Gabrieli; Schütz's *Psalmen Davids*, 1619) and Bach's double-choir motet *Singet dem Herrn* BWV 225.
- Coro I (S A T B, left) sings the subject *rectus*. Coro II (S A T B, right) answers with the *inversion*. Its exposition is Coro I's exposition literally mirrored, as in Contrapunctus 12/13 of the *Art of Fugue*.
- The choirs then trade at shrinking distances: a bar, half a bar, a beat. They quarrel about the key, make up, and play a joke on each other. They meet in an eight-voice stretto in which every voice enters, half a bar apart, with the subject (Coro I) or the inversion (Coro II).

**Prelude VII** is a chorale prelude on Philipp Nicolai's *Wachet auf, ruft uns die Stimme* (1599), after Bach's Schübler chorale BWV 645, which is also in E-flat.
- The chorale sounds in long notes in the **tenor**, the register in which it sounds in BWV 645.
- Above it, a dancing obbligato is made from the fugue subject in **diminution**. Below it runs a walking bass.
- The chorale's last line is answered by **its own inversion**.

The two pieces share material in both directions:
- The fugue subject opens with the chorale's first notes.
- The chorale's line 1 returns in the fugue's coda, in Coro I's tenor.
- One chord ties the pair together: A-flat over B-flat (IV over V, a "B-flat eleven"). The fugue's choirs are reconciled on it, and it is the chord Bach puts under the chorale's last C in BWV 140/7. The prelude uses it at b39.4, and the fugue at b30 and b47.

---

## 2. Fugue: material

| | Notes (written in `fugue.py`) | Design |
|---|---|---|
| **Subject** (2 bars) | `Eb4:4 G4:2 Bb4:2 C5:4 Bb4:4 \| C5:2 D5:1 C5:1 Bb4:2 D5:2 F5:4 Eb5:2 D5:2` | The head **E♭–G–B♭ … C–B♭** is the first line of *Wachet auf* (E♭ G B♭ B♭ B♭ B♭ C B♭), compressed into the canzona rhythm long–short–short–long–long. Bar 2 has a sixteenth turn, a leap to the summit F, and a fall onto the leading tone. It ends open, on D. |
| **Tonal answer** | `Bb3:4 D4:2 F4:2 G4:4 F4:4 \| F4:2 G4:1 F4:1 Eb4:2 G4:2 Bb4:4 Ab4:2 G4:2` | Bar 1 is a fifth up, bar 2 a fourth up. The answer travels V → I where the subject travels I → V. |
| **Countersubject** | `R:2 Bb4:2 Eb5:2 D5:2 Eb5:2 F5:2 G5:2 F5:2 \| Eb5:4 F5:4 Ab5:2 A5:2 Bb5:4` (and the same fitted to the answer) | Eighths where the subject declaims, quarters where it runs. The A♭→A♮ inflection carries the subject into B-flat. It was written by hand, then checked on the 16th grid: cost 2.1 above the subject and 1.1 inverted an octave below. |
| **Inversion** | `invert_diatonic(SUBJ, 'G4', E♭ major)` = B♭ G E♭ D E♭ \| D C D E♭ C A♭ B♭ C | This is a diatonic mirror about G4, the third of the tonic. It keeps the tonic triad, turns V into IV and ii into vii°, and lands on C. Coro II's harmonic "dialect" follows from it: plagal cadences, and suspensions that resolve **upward**. |

**How the subject was chosen.**
- The rhythm and the chorale head (degrees 1–3–5) were fixed by hand.
- An annealing search over the remaining pitches proposed contours. Each contour was scored by the strict pair cost of the subject against itself and against its inversion, at distances of a beat, half a bar and a bar.
- The adopted line (search cost 59, the lowest found) is clean against both forms at all three distances. This is what makes the antiphony at shrinking distances possible.

**The mirror exposition (b9–16).**
- Coro II sings Coro I's whole b1–9 block upside down, all four voices together and an octave lower: I-S → II-B, I-A → II-T, I-T → II-A, I-B → II-S.
- E-flat regions are mirrored about G. Foreign flats mirror to flats, so B-flat minor becomes A-flat minor.
- B-flat regions are mirrored *tonally*: transpose to E-flat, mirror, transpose down a fifth. Coro I's dominant answers therefore become Coro II's **subdominant** answers (II-T b11 and II-S b15 are in A-flat).
- This needed one constraint on Coro I's free soprano: it avoids chord roots on strong beats, because they mirror into dissonances.

---

## 3. Fugue: antiphony map

49 bars in 4/4, Allegro festivo, quarter = 80 with a tempo map. About 2:35 (`renders/fugue.mp3`: 155 s).

| Bars | Who | Distance | Content |
|---|---|---|---|
| 1–8 (→9.1) | **Coro I** | — | Exposition top-down: S subject (b1), A tonal answer + CS in S (b3), T subject + CS in A (b5), B answer + CS in T (b7). Cadence on E♭ at 9.1. |
| 9–16 (→17.1) | **Coro II** | — | **Mirror exposition**, bottom-up: B inversion (b9), T inverted answer **in A♭** (b11), A inversion (b13), S inverted answer in A♭ (b15). |
| 17–20 | I, II, I, II | **a bar** | Heads by the bar: rectus on the left, inverted on the right, round E♭ → f → B♭ → E♭. Each bar ends on a dominant that the other choir resolves; Coro II's bars end plagally. |
| 21–24 (→25) | I, II, I | **a bar, overlapping** | Whole entries a bar apart, each overlapping the last: I-A rectus at the c level over a falling C–B♭–A♭–G bass (b21), II-S inversion on D (b22, all eight voices in b22–23), I-T rectus in E♭ (b23). It carries Coro I to a B-flat cadence while Coro II falls silent. |
| 25–26 | I, II | a bar | **The choirs disagree about the key.** Coro I is in B-flat and means it: head in the tenor, A♮ in the alto. Coro II answers in A-flat: inverted head in the soprano, D♭ in the alto. |
| 27–28 | I / II | **half a bar** | The same argument at half the distance. |
| 29 | I / II | **a beat** | A beat each; Coro II's last block is tied over. |
| 30 | both | superimposed | **Reconciliation.** Coro II's A-flat chord sounds over Coro I's B-flat: IV over V, the home dominant. Coro II then concedes by step (9–8 and 11–10) into B♭7. E♭ follows at b31.1. Tempo broadens into this bar (80 → 70). |
| 31–35 | I, II, I, II, I | a bar | **The joke.** Coro I turns pompous: French-overture dotted rhythms over its bass, which starts the subject in **augmentation** (b31). Coro II twice cuts it short with the whole subject in **diminution**, chattered in one bar: S rectus (b32), then B inverted (b34). Coro I resumes each time, flustered: b33 continues the augmentation onto a deceptive C minor, and b35 continues it again. The augmentation's last bar (F–E♭–D) is never sung here. The tempo map alternates 76 (pomp) and 86 (chatter). |
| 36 | I / II | **a beat** | Coro I gives up. The diminished head is tossed across the hall a beat apart, rectus left and inverted right. |
| 37–42 | **both** | half a bar | **Stretto à 8** (§4). |
| 43–49 | both | — | **Coda.** Chorale line 1 (*Wachet auf, ruft uns die Stimme*) in long notes in Coro I's tenor, the BWV 645 register. Coro I's alto opens with the head. Under the chorale's C, Coro I's bass **finally finishes its augmentation** (b46: F–E♭–D, in the bass's low octave). Final cadence: A-flat over B-flat again (b47), then E♭. Coro II has the last word: the head as a soft echo, **upside down** (S2, b48.3). Ritardando 76 → 48. |

The choirs never double each other: `doubling_runs` is 0. The second choir is never a copy of the first. It is either Coro I inverted (the exposition) or a different, independently voiced harmony (everywhere else).

---

## 4. The eight-voice stretto (b37–42): proof

Entries come every half bar, alternating choirs. Coro I sings rectus, Coro II inversus, and every one of the eight voices enters:

| Entry | Voice | Form | Level (first notes) |
|---|---|---|---|
| 37.1 | I Tenor | rectus | c level, diatonic (C E♭ G A♭ G …): breaks in on C minor |
| 37.3 | II Tenor | inversus | on F (F D B♭ A♭ …) |
| 38.1 | I Soprano | rectus | A♭ (A♭ C E♭ F E♭ …) |
| 38.3 | II Alto | inversus | E♭ (B♭ G E♭ D …) |
| 39.1 | I Alto | rectus | A♭ |
| 39.3 | II Bass | inversus | E♭ (an octave down) |
| 40.1 | I Bass | rectus | A♭ (an octave down) |
| 40.3 | II Soprano | inversus | E♭ (an octave up), climbing to the soprano's B♭ |

How it was found:
- A depth-first search over entry times, voice orders, forms and transposition levels proposed this plan ("plan K"). Each overlapping pair had to be clean on the strict 16th grid, with crossings between the choirs allowed.
- Entry levels were penalised unless the head outlined an E♭, B♭ or A♭ triad.
- The free voices around the entries were then written by hand.

Proof run (scratch script):
- Keep **only the eight statements**, each 8 quarters from its entry, delete every free note, and run `critic.analyse`.
- Result: **parallels_error 0, parallels_weak 0, beat_parallels 0, unresolved 0, low-register seconds 0**, tripled pitch-classes 7.1%. The only remarks are 12 "chord (7th not resolved down)" notes.
- Each statement lasts two bars, so at most **four statements sound at once** (38.3–40.4). The other voices continue in free counterpoint.
- All eight voices are moving in b39–40.

In the finished summit, moving voices per bar for b37–42 are 6 7 8 8 6 7, a mean of **7.0**.

---

## 5. Prelude: chorale treatment

46 bars in 4/4, Andante con moto, quarter = 80, with a ritardando to 58 over the last four bars. About 2:24 (`renders/prelude.mp3`: 144 s).
- **The chorale** is Nicolai's melody as Bach harmonised it in BWV 140/7. Each line is in long notes in the tenor (half notes, as in the hymnal), separated by obbligato interludes.
- **The obbligato** comes from the fugue subject in diminution:
  - The ritornello (b1–4) states the diminished subject, its inversion and its tonal answer.
  - Throughout, the obbligato's generating figure is the diminished head's rhythm (eighth, two sixteenths, eighth, eighth) spread over the harmony.
  - The diminished turn-and-run (C–D–C–B♭–D–F–E♭–D) returns literally at b6 and b24. The answer's second half returns at b35.
  - Line 3's cadence (b19) is the subject's own second bar at full speed.
  - b20–21 bring the diminished subject and its inversion back as a short second ritornello.
- **Harmonisation** follows BWV 140/7 in its large moves:
  - Line 1 makes a half close through F7, with A♮.
  - Line 2 cadences in B-flat.
  - From b39 the bass is Bach's own: G–E♭ | A♭–B♭ | C | F | B♭ | E♭, including the A♭-over-B♭ chord under the chorale's C.
  - My line 5 closes deceptively on C minor. BWV 140/7 makes its deceptive close one line earlier.
- **The answer by inversion** (b42.3–46):
  - The last line (B♭ E♭ B♭ C G A♭ G F E♭) is mirrored about its final E♭ (`invert_diatonic(LINES[9], 'Eb3', …)`, two octaves up). It becomes **A♭ E♭ A♭ G C B♭ C D E♭**, sung in the obbligato's voice.
  - The original falls to the tonic through the supertonic. The mirror starts on the subdominant and **rises** to the tonic through the leading tone. This is Coro II's plagal dialect, previewed.
  - Underneath, the bass takes the subject in diminution (b43, 12/12) and then its inversion (b44, 12/12). This is the fugue's two choirs in miniature.
- **Playability:** two hands. The right hand plays the obbligato. The left hand plays chorale and bass, and the right hand takes a chorale note where the bass lies low. Critic keyboard check: **0 of 471 onsets** need more than two hands (at most 5 notes and a 16-semitone span per hand). On an organ the bass may go to the pedal, as in BWV 645.

| Bars | Chorale line (stanza 1 text) | Harmony / notes |
|---|---|---|
| 1–4 | — (ritornello) | subject ↓ dim., inversion, tonal answer, cadence |
| 5–9 | 1 *Wachet auf, ruft uns die Stimme* | half close on B♭ through F7 |
| 10.3–15 | 2 *der Wächter sehr hoch auf der Zinne* | cadence in B-flat |
| 16.3–20.2 | 3 *wach auf, du Stadt Jerusalem* | home; the subject's bar 2 at full speed |
| 20–22.2 | — (ritornello) | subject (8va) and inversion, diminished |
| 22.3–25 | 4 *Wohlauf, der Bräut'gam kömmt* | V7 – I |
| 26.3–29 | 5 *steht auf, die Lampen nehmt* | deceptive close on C minor |
| 30.3–32 | 6 *Halleluja* | |
| 33.3–35.2 | 7 *macht euch bereit* | the answer's second half in the obbligato |
| 36–37 | 8 *zu der Hochzeit* | |
| 38–42.2 | 9 *ihr müsset ihm entgegen gehn* | Bach's bass from b39; A♭ over B♭ at b39.4 |
| 42.3–46 | 9 inverted (obbligato) | bass: subject ↓ dim. (b43), inversion (b44); I6 – vi – V – I |

---

## 6. Allusions and credits

- **Philipp Nicolai**, *Wachet auf, ruft uns die Stimme* (1599). The melody follows **J. S. Bach's harmonisation in Cantata BWV 140, movement 7**. Line labels use Nicolai's first stanza.
- **J. S. Bach, *Wachet auf* BWV 645** (Schübler chorales; from BWV 140/4). It is the model for the prelude: same key, chorale in the tenor register, an independent obbligato above. The obbligato here is not Bach's; it is made from this pair's fugue subject.
- **J. S. Bach, *Singet dem Herrn ein neues Lied* BWV 225**, and the Venetian **cori spezzati** of **Giovanni Gabrieli** and **Heinrich Schütz** (*Psalmen Davids*, 1619) are the models for the double-choir fugue.
- **J. S. Bach, *Die Kunst der Fuge*, Contrapunctus 12/13** is the model for the mirror exposition: a whole texture inverted.
- In the joke, the French-overture dotted style (Coro I's pomp) is set against Italian *chatter* (Coro II's diminutions).
- The fugue subject's head quotes the chorale's first line. The coda brings the chorale's first line back, in the tenor.

---

## 7. Critic numbers (`python3 tools/critic.py …`)

| | Fugue (8 voices) | Prelude (3 voices) |
|---|---|---|
| parallels_error | **0** | **0** |
| parallels_weak (off-beat) | 0 | 2 (b23.2, b39.1) |
| **bad_doublings** (7th or leading tone doubled on a beat) | **3** (b23.4, b40.1, b46.3) | 0 |
| **stepwise_pct** / leap_4th_plus_pct | **63.4** / 10.0 | 34.5 / 20.8 |
| beat_parallels | **0** | **0** |
| dissonance_unresolved | **0** | **0** |
| pc_tripled_on_beats_pct | 13.7 | 10.4 |
| low_register_seconds | 2 (b46.4, b47.1) | 0 |
| doubling_runs | 0 | 0 |
| mean moving voices | 5.0 overall; **7.14** in the 22 tutti bars (≥ 6 voices active); summit b37–42: 7.0; disagreement b27–30: 7.75 | 2.89 of 3 |
| keyboard (two hands) | 5.9% of onsets exceed two hands (choir texture; accepted by the brief) | 0% |
| tertian fit / longest static | 60.7% / 8 beats (the final chord) | 66.8% / 4 beats (final chord) |
| theme check | exposition 12/12 (answers 11/12, by tonal adjustment); all stretto statements on A♭/E♭/F 12/12; diminutions 12/12 | bass diminutions 12/12 |

On tripling: a pitch class is tripled on 13.7% of beats (fugue) and 10.4% (prelude). The tripled pitch classes are chord roots and fifths (checked bar by bar with a scratch lister). With eight voices, the better measure is `bad_doublings`, which is 3 (see below and weak spot 12).

`tools/reduce.py` gives a harmony change on most beats in both pieces. The longest static harmony is the final chord.

**Is each choir a complete harmonic unit?** On the 31 beats where both choirs have three or more voices sounding at the beat, Coro I's own notes contain a third on 26 beats and Coro II's on 29. The exceptions are listed under weak spots.

**Melodic-profile revision (fugue).** The first finished version had **stepwise_pct 52.3 and 12 bad doublings**. Its free voices were assembled too much from chord tones.
- A scratch script proposed passing notes for the free voices only: a third filled with a passing eighth, a fourth filled with two sixteenths, a repeated note turned into a neighbour. Thematic material and Coro II's mirror bars were excluded; the mirror was recomputed from Coro I's revised exposition.
- Each proposal was accepted only if no critic count got worse (parallels, beat parallels, unresolved dissonances, bad doublings, low-register clashes, melodic faults, crossings).
- I then struck by ear-on-paper the proposals that put a foreign note into a choir's key: a D♮ in Coro II's A-flat bars, an A♭ against Coro I's A♮. I fixed nine doublings by hand: for example, Coro II's 9–8 at b30 now really falls C–B♭ instead of rising onto a doubled D.
- All 43 changed bar strings are written literally in `fugue.py`.
- Result: **stepwise 63.4%, leaps of a fourth or more 10.0%, bad doublings 3**, with every other count at its previous level or better.

---

## 8. Honest weak spots

1. **b30 (reconciliation).** Coro I holds a bare B♭–F (no third) for three beats under Coro II's A-flat chord. The polychord is complete only as an eight-voice sum. Adding D to Coro I would anticipate the note into which Coro II's 11–10 suspension resolves. Coro I also lacks a third at b22.1 and b40.3. Coro II lacks one at b38.3, where its D would double Coro I's leading tone.
2. **"Chord (7th not resolved down)": 22 notes in the fugue.** Many are in Coro II's mirror, where inverted suspensions resolve upward by design. Others are inner-voice sevenths leaving by leap in the tutti. None is unresolved by the critic's definition.
3. **Crossings: 20 reported.** All are between voices of *different* choirs (e.g. II-S above I-S). This comes from the critic comparing the score's voice order; within each choir no voices cross.
4. **Theme-check scores below 12/12 are by design.**
   - The c-level statements (b21 Coro I alto; b37 Coro I tenor) are diatonic transpositions, so their interval match is 3/12.
   - The one-bar head entries score 4–7/12.
   - The augmentation (b31) is labelled as an entry although it is interrupted. Its last bar arrives only at b46.
5. **Length.** The fugue's 2:35 is at the low end of the 2:30–3:30 brief.
6. **Coro I's free soprano in b5–8 is plain** (halves and quarters). It is constrained by having to mirror cleanly into Coro II's bass.
7. **Two low-register seconds in the fugue**, at b46.4 and b47.1, where the augmentation's F–E♭–D passes under the chorale.
8. **Prelude, sameness.** The obbligato's head-rhythm figure runs almost unbroken from b5 to b41. The literal turns (b6, b24, b35) and the full-speed bar (b19) are the main contrasts.
9. **Prelude, compass and form.**
   - The second ritornello puts the diminished subject an octave up, so the obbligato reaches **F6** at b20. That is the top of a harpsichord's compass.
   - The chorale's Stollen is sung once, without the repeat that BWV 645 and the hymn have. This keeps the movement near 2½ minutes.
10. **Prelude b41.4–42.2.** The texture thins to the chorale's final E♭ with the bass while the obbligato rests, a breath before the mirror. On paper it is a bare octave.
12. **Three bad doublings remain in the fugue.**
    - b40.1: every note of the doubled seventh (A♭) belongs to a stretto statement.
    - b23.4: the doubled leading tone is the D of Coro II's inversion against Coro I's soprano. Every alternative tried for the soprano made parallels with the subject in the tenor or the bass.
    - b46.3: Coro II's held E♭4 against the E♭ of Coro I's augmentation. The alternatives left a dissonance unresolved.
13. **Prelude melodic profile.** The obbligato is arpeggiated figuration, so the prelude's stepwise_pct is only 34.5% and its leaps of a fourth or more are 20.8%. The coordinator's melodic targets were set for the fugue; I did not revise the prelude for them.
14. **No listening.** I cannot judge balance, the effect of the bach-lehman tuning, or whether the antiphony reads in the spatial render.

---

## 9. Renders

```
python3 tools/render_music.py cycle/07-e-flat-major/fugue.json   --output-prefix cycle/07-e-flat-major/renders/fugue   --temperament bach-lehman
python3 tools/render_music.py cycle/07-e-flat-major/fugue.json   --audio-only --temperament equal --output-prefix cycle/07-e-flat-major/renders/fugue-equal
python3 tools/render_spatial.py cycle/07-e-flat-major/fugue.json --output cycle/07-e-flat-major/renders/fugue-spatial.mp3 --layout antiphonal
python3 tools/render_music.py cycle/07-e-flat-major/prelude.json --output-prefix cycle/07-e-flat-major/renders/prelude --temperament bach-lehman
python3 tools/render_music.py cycle/07-e-flat-major/prelude.json --audio-only --temperament equal --output-prefix cycle/07-e-flat-major/renders/prelude-equal
```

- `fugue.{pdf,mid,musicxml,ly,mp3}` and `fugue-equal.mp3` run 155 s.
- `fugue-spatial.mp3` runs 157 s. Its antiphonal layout puts Coro I S A T B on the left arc (−80° to −25°) and Coro II S A T B on the right (+25° to +80°).
- `prelude.{pdf,mid,musicxml,ly,mp3}` and `prelude-equal.mp3` run 144 s.

The tempo maps are in each score's metadata:
- Fugue: it broadens into the b30 reconciliation, alternates pomp and chatter in the joke, takes the summit broad (74) and makes a final ritardando to 48.
- Prelude: a ritardando from b42 to b46, 80 → 58.

For the stereo piano renders, the fugue sets `piano_pan` per voice, Coro I left and Coro II right.
