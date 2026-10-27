# Pair II in C minor: notes on the rebuild

These notes cover the rebuilt C-minor pair, renumbered from "Pair I" to Pair II (C minor is No. II in Bach's key order).

**Files**
- Sources: `prelude.py` and `fugue.py`. Every note is written literally, one call per bar.
- Built scores: `prelude.json` and `fugue.json`.
- Renders: `renders/` (see the end of this file).

**Basis and limits**
- The rebuild follows `REVIEW.md` (problems P1–P16) and the plan approved there.
- Thematic forms were derived by explicit transposition, diatonic mirroring (axis E-flat 4) or rhythmic doubling of hand-written lines, and then written out as tokens.
- Nothing from the v3 voicing search or the v5 `gen()`/`fill()` survives.
- **I cannot hear the renders.** Everything below comes from the score and the tools; it does not describe how the pair sounds.

---

## 1. Fugue II (a 3): bar map

36 bars, quarter = 80, about 108 s. v5 was 34 bars at quarter = 69, about 118 s.

| Bars | v5 source | Content | Key |
|---|---|---|---|
| 1–2 | 1–2 | **Soprano: subject.** Unchanged pitches and rhythm. | c |
| 3–4 | 3–4 | **Alto: answer.** The subject's mirror (C↔G, B↔Ab, D↔F, Eb↔Eb) transposed to the **dominant**: `D4 Eb4 C4 G4 Bb3 G4 A3 \| Bb3 C4 D4 C4 Bb3 C4 D4 Eb4 D4 G4`. The soprano plays the countersubject (CS) above it. The CS end is rewritten so that it does not cadence with the answer. | c→g |
| 5–6 | new | **Link.** Subject head in g (alto), then the dotted motif in c (alto) with the head in c (soprano). Cadence iv – ii°6 – i6/4 – V → c. | g→c |
| 7–8 | new | **Bass: subject**, the third entry. Soprano: CSI (the CS mirrored). Alto: **CS2**, a new syncopated second countersubject. | c |
| 9–10 | new | **Episode 1.** Soprano: the subject's 16th-note turn. Alto: suspension line, with each 7th prepared. Bass: broken 8ths. One-bar model, sequenced down a step; Bb7 → Eb. | c→Eb |
| 11–12 | 7–8 | **Soprano: subject (E-flat form).** Bass: CSI. Alto: CS2. v5's second E-flat entry (b9–10) is cut. | Eb |
| 13–14 | new | **Episode 2.** The same model with the lines exchanged: suspension line on top, turn motif in the bass. Eb → c → D7(6/5) → g. | Eb→g |
| 15–18 | 13–16 | **Bass: subject in augmentation** from 15.1. **Alto: subject** on beat 4 of b15. **Soprano: inversion** at 17.1.5. Subject, augmentation and inversion sound together in 17.3–18.3. | g |
| 19–20 | new | **Episode 3**, the third permutation. Turn motif in the alto; the bass takes the suspension line as V4/2 → I6 resolutions. g → f. | g→f |
| 21–22 | new (replaces 19–24) | **Mirror trio in f.** The whole b7–8 block upside down: soprano answer-mirror, alto CS2 mirrored, bass CS. Cadence VI–V → c. | f→c |
| 23–24 | new | **Stretto at the octave**, half a bar apart: soprano 23.1, alto 23.3. | c |
| 25–26 | 25–26 | **Build.** 4-3 suspension chain over the lament bass C–Bb–Ab–G. Diminished-7th ascent; the turn motif on V7. | c |
| 27–28 | 27–28 | **Peak: stretto à 3** at half-bar distances: soprano C6 (27.1), bass C3 (27.3), alto C5 (28.1). | c |
| 29–30 | 29–30 | V7 → **deceptive VI** (29.3.5) → iv → **Neapolitan** (30.1–2) → V with the dominant bariolage. | c |
| 31–35 | new | **Coda.** Bass: **J. S. Bach's BWV 847 fugue subject, augmented**, as a moving tonic pedal (from 31.2, after a literal quarter rest). Alto: the mirror answer (31.3.5). Soprano: a free descant, then the final cadence i6 – ii°6/5 – V7. | c |
| 36 | 34 | **Full C-major chord** (C2 – C5 – E5): the Picardy third, as at the end of BWV 847. | C |

Declared entries are checked by `critic.py` (subject declared in the score):
- 13 of 15 entries match at least 13/16 intervals.
- The E-flat entry scores 10/16 by design. It is the subject's modal E-flat form, used in v5 as well.
- The Bach entry scores 5/16 by design. It is Bach's subject, not ours, and its label says so.

## 2. Prelude II, "losing the beat": bar map

32 bars, quarter = 63. Continuous 16ths. A velocity accent marks the first note of every group (`group_starts()` in `prelude.py`).

| Bars | Grouping | Content |
|---|---|---|
| 1–5 | 4 (on the beat); LH steady 8ths | The accents spell **the fugue subject in augmentation** (C–B D \| G Eb G F \| Eb D C D Eb–D C \| B C–G). The kept rising bass C–D–Eb–F–G gives i, V4/3, i6, vii°4/3–iv, V. b5 is V7 with appoggiaturas (Eb→D, C→B, Ab→G). |
| 6–7 | 3; **LH quarters on every beat** | c → Ab → Fm7 → Bb7. The accented line sits above a repeating inner pair, so the threes are heard against the beat. |
| 8–11 | 3 | From **8.1, a 16th after the barline**, the accents spell **the fugue subject in its E-flat form** at dotted-8th speed: Eb D F Bb G Bb Ab \| G F Eb F G F Eb D Eb Bb. The harmony quickens to quarters in b11 (I vi ii6 V7). |
| 12 | 4 | E-flat: the downbeat regained (the 7th Ab5 resolves to G5 on 12.1). |
| 13–18 | 5; LH now strikes with the groups | The beat dissolves. Rising waves span no more than an octave. Kept chromatic bass: Db–C–Db–E–F–F–Db–Ab, giving Eb7/Db, Ab/C, Bbm/Db, C7/E, Fm, Db, Dø7/Ab, German sixth. |
| 19–22 | 3+5+3+3+5+5 / 3+5+3+3+5+5 / 3+3+5+5 | Dominant pedal (LH G2/G1 re-struck on group starts). Harmony over the pedal speeds up (i6/4–V7, iv6/4–vii°7/V, then by quarters, then V7♭9). The waves climb from G5 to **A-flat 6**, the highest note of the pair, with a crescendo. |
| 23 | written-out *Presto* | 32nd-note diminished-7th sweep over G1. |
| 24 | written-out *Adagio* | The subject's head C–B–D–G alone in quarter notes over a bare bass (after BWV 847's Presto/Adagio). |
| 25–29 | 4, both hands; LH 8ths | **The downbeat regained**, at the loudest level. Kept rhetoric: i \| iv6 N6 \| i6/4 V7 \| **VI deceptive** \| iv6 N6 i6/4 V7 in quarters. |
| 30–32 | 4 | Tonic pedal: i, iv6/4, vii°7, i in aligned groups of four, each chord at least half a bar. The last note is a held **C5, the fugue's first note**. |

## 3. Devices

1. **Mirror trio** (fugue b7–8 and b21–22). CS2 was written so that the complete three-voice block (bass subject, alto CS2, soprano CSI) has a working diatonic mirror image: soprano answer-mirror, alto CS2 mirrored, bass CS. This is the device of Bach's Art of Fugue, Contrapunctus 12/13, not found in the WTC. The rectus block opens the full texture in c; the inverted block opens the F-minor section.
2. **BWV 847 as a guest voice** (fugue b31–35). Bach's subject (`cycle/reference/bach-subjects.md`), doubled in note values and started after a literal quarter rest, lies in the bass from C3:
   `C3 B2 C3 G2 | Ab2 C3 B2 C3 D3 | G2 C3 B2 C3 D3 | F2 G2 Ab2 G2 F2 | Eb2`.
   It works as a moving tonic pedal under our mirror answer, and it ends on E-flat (i6), which opens the final cadence. Credited in the entry label, the score's composer line and here.
3. **Subject, augmentation and inversion together** (fugue b15–18). Placement re-probed after the tool fix: aug@0, subject@12, inversion@34 (in 16ths) gave 0 parallels and 0 unresolved dissonances with an 8th-level clash check.
4. **Stretto à 3 at the peak** (fugue b27–28): subject at C6, then C3 and C5 at half-bar distances. Tested clean.
5. **The subject hidden in the prelude's accents**: augmented in A, in its E-flat form and off the beat in B, alone in the Adagio (b24). This also links the pair.

## 4. Review problems → what changed

| # | Problem | Change (bars) |
|---|---|---|
| P1 | Two voices | **Three real voices** throughout from b7 (critic: mean 2.78 moving voices, 30/36 bars with all three moving). The one-note "Pedal" staff is gone. |
| P2 | No subject b15–26; 15 bars machine-filled | **All 15 code-filled bars recomposed by hand** (no `gen`/`fill`). A thematic statement (subject, answer, augmentation, mirror or Bach's subject) runs through every section. Stretches without a complete statement never exceed two bars: the b5–6 link (head motifs only), the three episodes, b26, b30 and b35. The episodes use subject material: the turn and the dotted motif. |
| P3 | Square two-bar stop-start; texture collapses at arrivals | Entries off the downbeat: 15.4, 17.1.5, 23.3, 27.3, 31.2, 31.3.5. The CS end (b4) and the CSI/CS2 openings (b7.1) were rewritten so that they run across the join instead of cadencing or resting. Attacks per bar at the arrivals: b7 15, b11 15, b15 12, b21 14, b23 10, b27 16 (v5: 7 at b1, 13, 27, 31). Below 9 attacks: only the solo opening b1 (7) and the final cadence b35 (6). |
| P4 | Peak was the thinnest bar | b27 is a stretto à 3 and the **fullest bar of the piece (16/16 sixteenth positions attacked)**. Soprano C6–F6, bass from C3, alto in 16ths. |
| P5 | Exposition never left c; keys entered without cadences | Answer at the **dominant**. Every arrival is cadenced: G7→c (b7), Bb7→Eb (b11), D7(6/5)→g (b15), C7→f (b21), VI–V→c (b23), V7→c (b27), deceptive VI (29.3.5), G7→c (b31), V7→I (b36). |
| P6 | Prelude was a chord chart | Every note hand-written. Passing, neighbour and appoggiatura notes in every section. Critic tertian fit 90.3% → **69.5%** (BWV 847 prelude: 70.4%). Audible top lines: the accented subject in A and B, the climbing waves in C and D. |
| P7 | Literal repetition; the pedal recedes | No bar repeats another's notes except the deliberate 28 → 29 compression. Pedal cut to **4 bars** (b19–22), climbing to A-flat 6 with a crescendo (level +6 → +15), then the Presto/Adagio break. |
| P8 | No beat to lose; inert LH | LH in steady 8ths (A) and **quarters on every beat** (B) under the groups of three. It joins the groups in C and D, plays plain quarters in the Adagio and returns in 8ths in E. The odd 16th bass pops are gone. |
| P9 | Augmentation section: 4th, accented 7th, filler, hollow end | b15–18 rebuilt: subject + augmentation + inversion, no free filler, no bare octave at the end. Two small adjustments to the augmentation are documented in §5. |
| P10 | E2 collisions | E2 (b13–14) rewritten. No F#–Ab, no minor 9ths. The route is diatonic (Eb, G7/B, c, D7/F#) and cadences into g. |
| P11 | Unplayable pedal; fake voice | No separate pedal. Critic keyboard check: **0%** of onsets exceed two hands (v5: 0.8%). |
| P12 | Double ending; bare 10th | One final cadence (b35: i6 – ii°6/5 – V7). A full C-major chord ends the piece (Picardy). |
| P13 | Build was broken chords | b25: 4-3 suspension chain over the lament bass, while the alto finishes the stretto subject. b26: diminished-7th ascent and the turn motif on V7 into the peak. Still less thematic than the rest; see weak spots. |
| P14 | 13th-span waves; octaves on accents | 5-note waves span no more than an octave (b13–18). Critic parallels between hands: 0 (v3: 3 weak + 3 beat-to-beat). |
| P15 | Squeezed final cadence; no link | Tonic-pedal close over two bars (b30–31), vii°7 for half a bar. Final C5 = the fugue's first note. The subject appears in the prelude (b1–4, b8–11, b24). |
| P16 | Too slow | Quarter = 80, "Allegro moderato" (prelude stays at 63). |

## 5. Deviations from the approved plan (and why)

- **Exposition order.** The plan said alto first. The fugue is soprano – alto (answer) – bass. Inverting the CS below the answer turns its 5ths into 4ths over the lowest voice, so the CS must stay above the answer. The answer therefore has to sit in a lower voice than the CS.
- **Coda.** The plan put our subject in the soprano over Bach's augmented subject (review block B5). Re-probing with an 8th-level clash check showed the tested placement (soprano entry at 32.4.5) lands on a D3 / E-flat 4 / C6 cluster. Every other placement either barely overlapped Bach's line or produced similar clusters. The coda therefore keeps **our mirror answer** over Bach's subject, and the soprano is a free descant. Our subject's last complete statements are the stretto à 3 just before.
- **Mirror axis.** REVIEW.md said "around D4"; the true axis is **E-flat 4** (erratum added there). All inversion probes were re-run with the fixed `stretto_finder.py`/`wtclib.invert_diatonic`.
- **Small thematic adjustments** (each made to remove a parallel or a clash):
  - Augmentation: D2 → D3 at 16.3 and at 18.4; dotted rhythm Bb2:3 A2:1 at 17.1.
  - Mirror-trio CS: one 16th (F2) removed at 21.4. The CS and the mirrored CS2 cadence differently at 22.4.
  - The alto subject at b29 ends A-flat instead of G (into the deceptive cadence).
  - Countersubject rests at 3.1, 7.1, 11.1 and 21.1 are replaced by arrival notes, so a full chord sounds on each downbeat.
- **Length.** 36 bars as planned. The coda needed bar 35 for the cadence after Bach's subject ends on 35.1.

## 6. Critic, before and after

| | Fugue v5 | **Fugue II** | Prelude v3 | **Prelude II** |
|---|---|---|---|---|
| parallels_error | 0 | **0** | 0 | **0** |
| parallels_weak | 2 | **0** | 3 | **0** |
| beat_parallels | 1 | **0** | 3 | **0** |
| dissonance_unresolved | 1 | **0** | 13 | 18 (all justified below) |
| low_register_seconds | 0 | **3** (limit 3) | 0 | **0** |
| pc_tripled_on_beats_pct | 0 | **0** | 0 | **0** |
| keyboard unplayable | 0.8% | **0%** | 0% | **0%** |
| crossings | 0 | **0** | 0 | **0** |
| mean moving voices | 1.97 | **2.78** | 2.0 | 2.0 |
| tertian fit | 39% | 52% | 90.3% | **69.5%** |

**Targets.** `beat_parallels` ≤ 1 is met (0). `low_register_seconds` ≤ 3 is met (3).

**The three low-register seconds** are all in the mirror trio (21.1.5, 22.2.25, 22.2.75). The alto's held F3 sits over the bass countersubject's 16th-note scale (G2, Eb2). They are passing 16ths in the dark low register chosen for the "upside-down" block.

**The 18 prelude flags** are figuration that the critic cannot parse:
- **9: dominant pedal**, b20–23. The 4ths, 7ths and 9ths of the upper harmonies (i6/4, iv6/4, vii°7/V, V7♭9) sit against the re-struck G pedal. The critic only treats notes held two bars or longer as a pedal.
- **3: V4/2 chord** (Eb7 over Db, b13). The bass is the chord's 7th and resolves to C in b14.
- **1: accented passing note**: G4 in the Bbm/Db wave, 15.2.
- **2: tonic pedal**: iv6/4 over C2, 30.3–4.
- **3: chord 7ths resolved in another register**:
  - vii°4/3 at 4.1 (B4 → C5 at 4.2);
  - V7 at 11.4 (Ab → G5 at 12.1);
  - V7 at 27.4 (F5 → Eb5 at 28.1).

**Fugue "chord (7th not resolved down)"** notes (12) are chord 7ths left by leap inside the figuration; none is an error.

**Harmonic reduction** (`tools/reduce.py --per beat`) shows the cadences listed under P5. Prelude: V7 → i at b6, Bb7 → Eb at b12, German sixth → i6/4 at b19, V7 → i at b30.

## 7. Honest weak spots

- **Unheard.** Whether the velocity accents make the threes, fives and the accent-spelled subject audible is untested. The subject at dotted-8th speed in its E-flat modal form (b8–11) may simply sound like figuration.
- **The mirror trio is low and dark.** Alto E3–C4, bass Db2–Db3. It may be muddy on a piano; it produced the three low-register seconds. Raising it a 4th would make the soprano reach F6 before the peak, so I kept it low.
- **The Adagio is only notated.** The renderer supports a single tempo, so b24 is one bar of quarter notes at quarter = 63 (about 4 s), not a real tempo change.
- **The episodes are not strict triple counterpoint.** They are the same three lines (turn motif, suspension line, broken bass) permuted, with adjustments at the joins. The alto in Episode 1 is mostly a harmonic filler.
- **The build (b25–26) is still the least thematic stretch**: suspensions and a diminished-7th run, not subject strettos.
- **Coda clashes.** Bach's line under our answer produces two brief clashes inherent to the combination: Ab4 over G2 at 31.4.5 (a passing ♭9) and C5 over B2 at 32.2.5 (Bach's lower neighbour). Both are 8ths.
- **The final cadence broadens to 6 attacks a bar** (b35). This is deliberate, but the coda is less dense than the peak.
- **The subject still starts on a downbeat quarter.** The rhythmic variety comes from entry placement, not from changing the theme.

## 8. Renders

All in `renders/`.
- `fugue.{mp3,pdf,mid,musicxml,ly}` and `prelude.{...}`: Bach–Lehman temperament, with score.
- `fugue-equal.{mp3,mid,musicxml,ly}` and `prelude-equal.{...}`: equal temperament.

Rebuild:
```
python3 cycle/02-c-minor/fugue.py && python3 cycle/02-c-minor/prelude.py
python3 tools/critic.py cycle/02-c-minor/fugue.json
python3 tools/render_music.py cycle/02-c-minor/fugue.json --output-prefix cycle/02-c-minor/renders/fugue --temperament bach-lehman
python3 tools/render_music.py cycle/02-c-minor/fugue.json --no-pdf --output-prefix cycle/02-c-minor/renders/fugue-equal --temperament equal
```
(The same two render commands apply to the prelude.)
