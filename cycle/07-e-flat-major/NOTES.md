# Pair VII in E-flat major: notes

**Files**
- Sources: `prelude.py` and `fugue.py`. Every note is written as literal bar strings in sixteenth units. The only operations applied to written material are explicit, named transforms from `tools/wtclib.py`: `transpose`, `invert_diatonic` and `scale_rhythm`. The fugue adds a region-aware `mirror()`, built from those three and defined in `fugue.py`.
- Built scores: `prelude.json` and `fugue.json`.
- Renders: `renders/` (listed at the end of this file).

**Basis and limits**
- Searches were used to *propose* material: the subject's pitches and the summit's entry levels and voice order. They ran as scratch scripts on the strict 16th-grid pair cost and `critic.analyse`. What they proposed was then written into the sources by hand. No search code is in the sources.
- **I cannot hear the renders.** Everything below comes from the score and the tools. None of it describes how the pair sounds.

---

## 1. Concept

**Fugue VII à 8, "Fuga a due cori"** is a fugue for two four-voice choirs.
- The models are the Venetian *cori spezzati* (Giovanni Gabrieli; Schütz's *Psalmen Davids*, 1619) and Bach's double-choir motet *Singet dem Herrn* BWV 225.
- Coro I (S A T B, left) sings the subject *rectus*. Coro II (S A T B, right) answers with the *inversion*. Its exposition is Coro I's exposition literally mirrored, as in Contrapunctus 12/13 of the *Art of Fugue*.
- The choirs then trade at shrinking distances: a bar, half a bar, a beat. They quarrel about the key, make up, and play a joke on each other. They meet in an eight-voice stretto in which every voice enters with the subject (Coro I) or the inversion (Coro II), the first six half a bar apart, the last two turning the harmony to the cadence.

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
| 31–35 | I, II, I, II, I | a bar | **The joke.** Coro I turns pompous: French-overture dotted rhythms over its bass, which starts the subject in **augmentation** (b31). Coro II twice cuts it short with the whole subject in **diminution**, chattered in one bar: S rectus (b32), then B inverted (b34). Coro I resumes each time, flustered: b33 continues the augmentation onto a deceptive C minor, and b35 continues it again. The augmentation's last bar (F–E♭–D) is never sung here. The tempo stays a steady 80: Coro I's pomp is played heavier (+6 velocity), Coro II's chatter lighter (−4) and detached. |
| 36 | I / II | **a beat** | Coro I gives up. The diminished head is tossed across the hall a beat apart, rectus left and inverted right. |
| 37–42 | **both** | half a bar | **Stretto à 8** (§4): six entries half a bar apart, then the last pair turns the harmony to the cadence (vi → ii6 → V4/2 → … V6/5 → I6/4 → V). |
| 43–49 | Coro I, then both | — | **Coda.** Chorale line 1 (*Wachet auf, ruft uns die Stimme*) in long notes in Coro I's tenor, the BWV 645 register, played louder (+10). Coro I alone becomes a chorale prelude, the prelude remembered: its alto opens with the head, its soprano runs in eighths (b44–46, the countersubject's figure), its bass walks in quarters. Under the chorale's C, Coro I's bass **finally finishes its augmentation** (b46: F–E♭–D). Coro II, silent since the summit, rejoins at b46–47 for the cadence: A-flat over B-flat again (b47), then E♭. Coro II has the last word: the head as a soft echo, **upside down** (S2, b48.3). The tempo moves on to 78 for the coda, then slows to 48 over b47–49. |

The choirs never double each other: `doubling_runs` is 0. The second choir is never a copy of the first. It is either Coro I inverted (the exposition) or a different, independently voiced harmony (everywhere else).

---

## 4. The eight-voice stretto (b37–42): proof

Entries alternate choirs: Coro I sings rectus, Coro II inversus, and every one of the eight voices enters. The first six come every half bar; the last two (revised after the second review) come a bar and then half a bar later, on new levels, so that the stretto drives into the cadence instead of circling A♭ and E♭:

| Entry | Voice | Form | Level (first notes) |
|---|---|---|---|
| 37.1 | I Tenor | rectus | c level, diatonic (C E♭ G A♭ G …): breaks in on C minor |
| 37.3 | II Tenor | inversus | on F (F D B♭ A♭ …) |
| 38.1 | I Soprano | rectus | A♭ (A♭ C E♭ F E♭ …) |
| 38.3 | II Alto | inversus | E♭ (B♭ G E♭ D …) |
| 39.1 | I Alto | rectus | A♭ |
| 39.3 | II Bass | inversus | E♭ (an octave down) |
| 40.3 | I Bass | rectus | **c level, in the bass** (C2 E♭2 G2 A♭2 …): vi; its tail D–C–B♭ lands on the dominant |
| 41.1 | II Soprano | inversus | **on F** (F5 D5 B♭4 A♭4 …): the inversion as a falling dominant-seventh fanfare over the bass's A♭ (V4/2 → I6) |

How it was found:
- A depth-first search over entry times, voice orders, forms and transposition levels proposed this plan ("plan K"). Each overlapping pair had to be clean on the strict 16th grid, with crossings between the choirs allowed.
- Entry levels were penalised unless the head outlined an E♭, B♭ or A♭ triad.
- For the second review, a second search kept the first six entries and tried every time and level for the last pair. The levels the reviewer suggested (Coro I's bass on F, Coro II's soprano on F, both at the old times) each make parallel fifths or octaves with an earlier statement. The c-level bass at 40.3 with the F-level soprano at 41.1 is clean. Over the bass's A♭ the soprano's F–D–B♭–A♭ is V4/2, and the harmony runs vi – ii6 – V4/2 – I6 – IV – I6 – V6/5 – vi – I6/4 – V – I (b40.3–43.1).
- The free voices around the entries were then written by hand.

Proof run (scratch script):
- Keep **only the eight statements**, each 8 quarters from its entry, delete every free note, and run `critic.analyse`.
- Result (revised plan): **parallels_error 0, parallels_weak 0, beat_parallels 0, unresolved 0**, tripled pitch classes 7.1%, low-register seconds 2 (b40.3, where the bass's C2 meets Coro II's bass passing D3).
- Each statement lasts two bars, so at most **four statements sound at once** (38.3–39.4). The other voices continue in free counterpoint.

In the finished summit, moving voices per bar for b37–42 are 6 7 8 7 7 6, a mean of **6.8**. Coro I's soprano climbs to C6 over the dominant fanfare (b41.3).

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
| **bad_doublings** (7th or leading tone doubled on a beat) | **4** (b23.4, b39.2, b41.1, b46.4) | 0 |
| stepwise_pct / leap_4th_plus_pct | 52.2 / 13.6 | 36.1 / 20.6 |
| beat_parallels | **0** | **0** |
| dissonance_unresolved | **0** | **0** |
| pc_tripled_on_beats_pct | 15.5 | 9.0 |
| low_register_seconds | 4 (b40.3, b40.3.75, b46.4, b47.1) | 0 |
| doubling_runs | 0 | 0 |
| mean moving voices | 4.8 overall; **7.2** in the 19 tutti bars (≥ 6 voices active); summit b37–42: 6.8; disagreement b27–30: 7.75 | 2.89 of 3 |
| keyboard (two hands) | 9.7% of onsets exceed two hands (choir texture; accepted by the brief) | 0% |
| tertian fit / longest static | 66.8% / 8 beats (the final chord) | 64.7% / 4 beats (final chord) |
| theme check | exposition 12/12 (answers 11/12, by tonal adjustment); all stretto statements on A♭/E♭/F 12/12 (the two c-level ones 3/12, diatonic); diminutions 12/12 | bass diminutions 12/12 |

On tripling: a pitch class is tripled on 15.5% of beats (fugue) and 9.0% (prelude). The tripled pitch classes are chord roots and fifths (checked bar by bar with a scratch lister). With eight voices, the better measure is `bad_doublings`, which is 4 (see below and weak spot 11).

`tools/reduce.py` gives a harmony change on most beats in both pieces. The longest static harmony is the final chord.

**Is each choir a complete harmonic unit?** On the 23 beats where both choirs have three or more voices sounding at the beat, Coro I's own notes contain a third on 19 beats and Coro II's on 21. The exceptions are listed under weak spots.

**Melodic profile and doublings (fugue).** These are diagnostics, and I treated them that way.
- **Doublings.** The first finished version had 12 bad doublings. I fixed the ones that were real voice-leading faults by hand, with seven small edits:
  - b22: Coro II's alto no longer doubles the inversion's D.
  - b30: Coro II's 9–8 now really falls C–B♭ instead of rising onto a doubled D.
  - b38: Coro I's alto rests before its entry, and Coro II's bass takes B♭–C instead of D–B♭.
  - b39: Coro I's bass holds A♭.
  - b40: Coro II's alto rests after its statement.
  - The coda's doubling at b45–46 disappeared when the coda was rewritten for the second review (§10).
  - Four remain (weak spot 11).
- **Steps.** stepwise_pct is **52.2** (leaps of a fourth or more 13.6%), below the ~62 suggested for this fugue.
  - The subject itself is 8/12 steps.
  - Most non-step motion is in the free voices of the antiphonal exchanges (b17–20, b25–29, b36) and of the stretto (b37–40). The half-bar and one-beat exchanges assert their keys in arpeggios.
  - In those passages the choirs speak homophonically. The free voices there move among chord tones, as in Gabrieli's and Schütz's antiphonal tuttis.
  - I tried a scripted passing-note pass that raised the figure to 63%. I withdrew it, because notes inserted to move a number are not composed. The score holds only hand-written lines.
---

## 8. Honest weak spots

1. **b30 (reconciliation).** Coro I holds a bare B♭–F (no third) for three beats under Coro II's A-flat chord. The polychord is complete only as an eight-voice sum. Adding D to Coro I would anticipate the note into which Coro II's 11–10 suspension resolves. Coro I also lacks a third at b22.1. Coro II lacks one at b38.3, where its D would double Coro I's leading tone.
2. **"Chord (7th not resolved down)": 34 notes in the fugue.** Many are in Coro II's mirror, where inverted suspensions resolve upward by design. Others are inner-voice sevenths leaving by leap in the tutti. None is unresolved by the critic's definition.
3. **Crossings: 17 reported.** All are between voices of *different* choirs (e.g. II-S above I-S). This comes from the critic comparing the score's voice order; within each choir no voices cross.
4. **Theme-check scores below 12/12 are by design.**
   - The c-level statements (b21 Coro I alto; b37 Coro I tenor; b40.3 Coro I bass) are diatonic transpositions, so their interval match is 3/12.
   - The one-bar head entries score 4–7/12.
   - The augmentation (b31) is labelled as an entry although it is interrupted. Its last bar arrives only at b46.
5. **Length.** The fugue's 2:35 is at the low end of the 2:30–3:30 brief.
6. **Coro I's free soprano in b5–8 is plain** (halves and quarters). It is constrained by having to mirror cleanly into Coro II's bass.
7. **Four low-register seconds in the fugue**: b46.4 and b47.1, where the augmentation's F–E♭–D passes under the chorale; b40.3 and b40.3.75, where Coro I's bass enters on C2 under Coro II's bass, whose turn passes through D3. All four involve only thematic notes.
8. **Prelude, sameness.** The obbligato's head-rhythm figure still carries most of b5–41. Since the second review it is broken by long notes in b31–32, a rest at b33.1, a dotted bar (b34) and a hemiola (b40), besides the literal turns (b6, b24, b35) and the full-speed bar (b19).
9. **Prelude, compass and form.**
   - The second ritornello puts the diminished subject an octave up, so the obbligato reaches **F6** at b20. That is the top of a harpsichord's compass.
   - The chorale's Stollen is sung once, without the repeat that BWV 645 and the hymn have. This keeps the movement near 2½ minutes.
10. **Prelude b41.4–42.2.** The texture thins to the chorale's final E♭ with the bass while the obbligato rests, a breath before the mirror. On paper it is a bare octave.
11. **Four bad doublings remain in the fugue.**
    - b41.1: the doubled seventh is A♭2 in both basses, where Coro II's inversion ends as Coro I's c-level statement reaches its A♭. Both are thematic.
    - b39.2: the "seventh" is the E♭ of two stretto statements over an A-flat bass, read by the critic as F7 because of a passing F in the tenor's inversion.
    - b23.4: the doubled leading tone is the D of Coro II's inversion against Coro I's soprano. The soprano alternatives I tried made parallels with the subject in the tenor or the bass.
    - b46.4: the chorale's C against Coro II's bass, held from the ii chord, while Coro I's augmentation passes D2. The critic reads a half-diminished seventh on D.
12. **Fugue melodic profile.** stepwise_pct is 52.2, against roughly 71–75 in Bach and the ~62 suggested here. The block-chord antiphony and the arpeggiated key assertions in b25–29 are the main cause. A hand revision of those free lines into scalar figures is the obvious next step; I have not done it.
13. **Prelude melodic profile.** The obbligato is arpeggiated figuration, so the prelude's stepwise_pct is only 36.1% and its leaps of a fourth or more are 20.6%. The coordinator's melodic targets were set for the fugue; I did not revise the prelude for them.
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
- Fugue: it broadens into the b30 reconciliation (80 → 70) and returns to a steady 80 for the joke. It broadens into the summit (74), moves on in the coda (78) and makes a final ritardando to 48.
- Prelude: a ritardando from b42 to b46, 80 → 58.

For the stereo piano renders, the fugue sets `piano_pan` per voice, Coro I left and Coro II right.

---

## 10. Second review (REVIEW-2.md): what changed

I implemented all four requested fixes by hand. The quarrel and reconciliation (b25–30) and the prelude's mirrored close are untouched.

1. **Fugue coda (b43–49): the ending no longer sags.**
   - Coro I alone turns the coda into a chorale prelude, the prelude remembered. Its tenor carries *Wachet auf* line 1, played louder (+10 velocity).
   - Its soprano runs in eighths through b44–46, on the countersubject's figure (E♭ G F D E♭ C D E♭ …), climbing to A♭5 for the A♭-over-B♭ chord at b47.
   - Its bass walks in quarters (C G | E♭ D C B♭ | C G) into the augmentation's F–E♭–D.
   - Coro II, silent since the summit, rejoins at b46–47 for the cadence and keeps its soft upside-down echo at 48.3.
   - Removing Coro II's held E♭4 (b45–47), which sat just above the chorale, also unmasks the tenor.
   - Tempo: 74 → 78 for the coda, then the ritardando from b47 as before.
2. **The joke (b31–36) at a steady ♩ = 80.**
   - The bar-by-bar tempo jumps (76/86/76/86/76/82) are gone.
   - The contrast is now in the notes and the playing: Coro I's French-overture bars +6 velocity, and Coro II's diminution bars −4 velocity with every Coro II note detached (gate 0.55).
   - The interruption itself was already in the notes: Coro II cuts in with the whole subject in a bar.
3. **Stretto à 8 (b37–42): the last pair now drives to the cadence.**
   - The reviewer suggested F levels for both (bass at 40.1, soprano at 40.3). A re-search showed that each makes parallel fifths or octaves with an earlier statement.
   - The clean solution: Coro I's bass on the **c level at 40.3** (vi) and Coro II's soprano on **F at 41.1**, a falling dominant-seventh fanfare. Over the bass's A♭ it forms V4/2 → I6.
   - The result is vi – ii6 – V4/2 – I6 – IV – I6 – V6/5 – vi – I6/4 – V – I. The bass's subject ends D–C–B♭ on the dominant, and Coro I's soprano peaks on C6 (b41.3).
   - The stretto proof was re-run (§4): the statements alone have 0 parallels and 0 unresolved dissonances. The free parts of b40–42 were rewritten by hand.
4. **Prelude obbligato rhythm varied.**
   - b31–32 (*Halleluja*): long notes, B♭5 C6 | B♭5 G5, the obbligato singing with the chorale.
   - b33: a quarter rest.
   - b34: a dotted bar (dotted eighth and sixteenth) at "macht euch bereit".
   - b40: a 3+3+2 cadential hemiola (G5 E♭5 C5) before line 9's close.

**After the changes:**
- Fugue: parallels 0 (also weak and beat-to-beat), unresolved 0, bad_doublings 4, low-register clashes 4 (all between thematic notes).
- Prelude: parallels 0 (2 weak off-beat), unresolved 0, bad_doublings 0, keyboard 0%.
- The scores were rebuilt and all five renders made again (§9).
- Review item 5 (shared registers; the choirs are told apart by pan) needs no change. The wide pans stay.
