# Pair II in C minor: composition review

This reviews the material currently labelled "Pair I": Prelude v3 "losing the beat" and Fugue v5.

**Material reviewed**
- Prelude v3: `work/wtc-work/renders/pairI_v3/prelude-i_v3.json`, built from `pairI/prel3.py` and `build_prelude3.py`. 31 bars, q=63.
- Fugue v5: `work/wtc-work/pairI/f5.json`, built from `pairI/v5/{head,s5,patch}.py` and `fug5.py`. 34 bars, q=69, two voices plus a one-note "Pedal" staff.

**How it was reviewed**
- I read the score bar by bar. I have not listened to the renders.
- Tools used: `tools/critic.py`, `tools/reduce.py --per beat` and `tools/stretto_finder.py`, plus scratch harnesses that call `critic.analyse` on combinations of lines and also flag dissonances of an eighth or longer on off-beats, which the critic does not check.
- References: BWV 846/847/870/871 from memory and from the reference MIDI.
- Calibration: on the per-staff MIDI of BWV 847, critic reports 0 parallel errors and 2 "unresolved" dissonances. v5 reports 0 errors and 1 unresolved. **The fugue's surface is already clean. Its problems are compositional: form, rhythm, harmonic direction and material, not error counts.**

Unless marked "new", bar numbers below are v5/v3 bar numbers.

---

## 0. Verdict in one paragraph

**Prelude.** The prelude has a real idea, metre as the subject matter (groups of 4 → 3 → 5 → 3/5 → 4), and a sound, Bach-like tonal plan with a fine chromatic bass in b13–18. But it is a chord chart arpeggiated by a voicing optimiser:
- no non-chord tones;
- no melody;
- a left hand that only re-strikes the bass;
- the "lost beat" is never dramatised against anything.

**Fugue.** The fugue has a good subject (a cousin of BWV 847's), a genuinely invertible mirror answer and countersubject pair, and a good closing rhetoric (deceptive VI, Neapolitan, V, stretto). Its middle, however, is machine filler:
- **15 of 34 bars** contain pitches chosen by `gen()` in at least one voice;
- b17–26 contain **no subject statement**;
- every structural arrival collapses into the same square two-bar unit, which explains "plodding";
- the "peak" is the thinnest bar in the piece.

**The fix.** The three-voice rebuild required by the renumbering is the right occasion to fix all of this. The material supports it. I tested a CS2 that makes the exposition a mirror-invertible trio, a stretto à 3, and an "S + inversion + augmentation" combination. BWV 847's own subject also fits as an augmented bass under the coda. All pass the critic with 0 parallels and 0 unresolved dissonances (§3.2).

---

## 1. What is good and must be preserved

### Prelude v3

1. **The dramaturgy of grouping.** A 4/3/5/mixed/4 regrouping of continuous 16ths is a "turn it up to 11" idea that stays within the WTC idiom: BWV 847's perpetual 16ths with one more dimension. Keep the concept and the section boundaries (b6, b12, b13, b19, b25).
2. **b1–5 opening phrase.** The bass rises C3–D3–Eb3–F3–G2 (i, V4/3, i6, iv, ii°6/5, V7): a clear phrase that sets the beat before the beat is undermined.
3. **b10–11 harmonic acceleration into Eb.** Quarter-note changes Eb, Ab/C, Bb/D, Eb, Cm, Fm/Ab, Bb7, landing in b12. Good: the harmony speeds up exactly where the grouping blurs.
4. **b13–18 chromatic bass.**
   - Bass: Db3, C3, Db3, E3, F2 … Db3, D, Ab2.
   - Harmony: Eb7/Db, Ab/C, Bbm/Db, C7/E, Fm, Db, Dø/Ab, Ger+6 (Ab C Eb F#), then i6/4 over G at b19.
   - This is the best harmonic writing in the pair and the most Bachian. Keep it note for note in the bass.
5. **b19–24 internal acceleration over the pedal.** The harmonies over G move at 2 bars, then half-bars, then quarters (i6/4, V7; iv, vii°7/V, i6/4, V7 twice, the second time twice as fast). It is a good idea; only the length and dynamics are wrong (§2, P7).
6. **b26–29 cadence rhetoric.**
   - b26–27: iv6, N6 (Db/F), i6/4, V7.
   - b28: deceptive Ab, held for a bar.
   - b29: the same progression compressed into quarters.
   - This is a written-out acceleration. Keep.
7. **b6 left-hand tresillo** (C3:6 C4:6 C3:4, i.e. 3+3+2). This is the one bass rhythm with character.

### Fugue v5

1. **The subject.**
   ```
   C5:4 B4:2 D5:2 G4:2 Eb5:2 G4:2 F5:2 | Eb5:1 D5:1 C5:1 D5:1 Eb5:2 D5:1 C5:1 B4:2 C5:4 G4:2
   ```
   - It is a compound melody: a rising line C–D–Eb–F over a G "pedal" in the same voice, then a 16th turn and a leading-tone cadence.
   - It is an audible relative of BWV 847 (C–B–C–G–Ab), without being a copy.
   - The v5 change (Ab4 to G4) removed the D–Ab tritone and the B…Ab diminished 7th. Keep the subject unchanged.
2. **The mirror system.**
   - The answer is the diatonic mirror of S around D4 (C↔G, B↔Ab, D↔F, Eb↔Eb).
   - The countersubject CS and its mirror CSI form pairs that are invertible both by mirror and at the octave. stretto_finder against the actual lines:
     - CS over A: cost 7.
     - CS under A (-14 steps): cost 8.
     - CSI under S, as in Eb at b7: cost 7.
     - CSI over S: cost 8.
     - None of these has parallels or unresolved dissonances.
   - This is an Art-of-Fugue resource. It is the seed of the three-voice plan.
3. **The tonal plan.** C minor, then Eb, G minor, F minor, back to C minor (i–III–v–iv–i). This is exactly Bach's practice. Keep.
4. **The E1 upper line, b5–6** (`Eb5:3 D5:1 F5:2 B4:2 | …`). It is the only dotted, characterful rhythm in the fugue, and its head (Eb–D–F–B) is a variant of the subject head (C–B–D–G). It should become the episode motif.
5. **The augmentation idea, b13–16.** S over its own augmentation, as at BWV 871 b14. The device is right. Its execution needs work (P9).
6. **The closing rhetoric, b28–31.** V7, then the deceptive Ab (F6 resolving to Eb6, b28.4–29.1), the Neapolitan Db arpeggio (b29.3–4), the dominant bariolage (b30) and the tonic. Keep this harmonic sequence.
7. **The final stretto at the octave, half a bar apart (b31–32).** stretto_finder ranks this as S's best self-stretto (offset 8, −7 steps, cost 5). Keep it in the coda.
8. **The b25–26 bass**, C–Bb–Ab–G | F–F#–G (lament descent, then vii°7/V–V). The skeleton is right; the upper voice is not (P13).

---

## 2. Things that don't work (ranked)

Severity scale: **Critical** means it blocks the pair. **High** is a main cause of Sam's complaints. **Medium** is audible and to be fixed during the rebuild. **Low** is polish.

| # | Movement | Bars | Problem | Severity |
|---|---|---|---|---|
| P1 | Fugue | all | Two voices; as No. II it must be a three-voice fugue | Critical |
| P2 | Fugue | b15–26 (and 5–6, 11–12, 30) | No subject for 12 bars; the "canon by inversion" is generated filler that is not the subject; 15/34 bars machine-filled | Critical |
| P3 | Fugue | 1–4, 7–10, 13, 27, 31 | Square 2-bar stop-start: every entry starts on a downbeat and ends in a simultaneous cadence; the texture collapses at every arrival | High |
| P4 | Fugue | 27–28 | The "peak" is the thinnest bar of the piece: bare octave, homorhythm, no real stretto | High |
| P5 | Fugue | 1–4, 6–7, 12–13, 18–19 | The exposition never leaves C minor; every new key is entered without a cadence | High |
| P6 | Prelude | all | A chord chart with no melody, no non-chord tones and no voice-leading (pitches chosen by an optimiser) | High |
| P7 | Prelude | 1, 3, 5, 8–9, 12, 16–17, 19–24, 25, 28 | Literal repetition over static chords; the 6-bar dominant pedal recedes instead of climaxing | High |
| P8 | Prelude | 6–24 | "Losing the beat" is not dramatised: the left hand follows the right-hand groups, so there is no beat to lose; the left hand is inert | Medium-High |
| P9 | Fugue | 13–16 | Augmentation section: unprepared 4th, accented M7, weak placement, generated free voice, hollow end | Medium |
| P10 | Fugue | 11–12 | E2 collisions: diminished 3rd F#–Ab, minor 9th A2/Bb4, C7 aimed at F minor that lands in G minor | Medium |
| P11 | Fugue | 31–32 | The tonic pedal is unplayable and a fake third voice | Medium |
| P12 | Fugue | 33–34 | A double ending; the second cadence is the weaker; it ends on a bare two-note 10th | Medium |
| P13 | Fugue | 25–26 | The build is prelude-style broken chords over a good bass; no thematic approach to the peak | Medium-Low |
| P14 | Prelude | 13–18, 11, 26, 29 | Romantic 13th-span wave figure; bass doubled in octaves on accents | Low-Medium |
| P15 | Prelude | 30–31; all | The final cadence is squeezed (vii°7 = four 16ths); no motivic link to the fugue | Low |
| P16 | Fugue | all | q=69 "sempre avanti" with a quarter-note subject head; too slow for a 16th fugue | Low |

### P1. The fugue has two voices, but No. II needs three (Critical)

**Evidence**
- `f5.json` has voices Upper (324 notes) and Lower (232 notes), plus "Pedal", a single C2 note at b31–32 (`fug5.py` EXTRA).
- critic texture: 1.97 moving voices on average; only one bar has three.

**Why it fails.** In Bach's key order C minor is No. II, so Fugue II needs three real voices (BWV 847 is à 3). The pedal note is not a voice.

**Fix.** See §3. Renumber all metadata: subtitle "Fugue II in C minor", `movement_number` 2, folder `cycle/02-c-minor/`.

### P2. No subject from b15 to b26; the "inversion canon" is generated filler (Critical)

**Evidence**
- `s5.py` composes these bars with `gen()` and `fill()`, a beam search over chord labels: the E1 lower voice (b5–6), the E2 lower voice (b11–12), the free upper voice (b15–16), E3 in both voices (b17–18), the whole b19–24 "canon by inversion" (`gen(..., canon=(fc,8))`, a generated line followed by its mirror), and the b30 upper voice.
- That makes 15 of 34 bars with machine-chosen pitches. This contradicts `cycle/CONVENTIONS.md` ("No code may choose pitches to fill voices").
- With the subject declared, critic's theme check reports:
  - b19 "Canon by inversion: lead": intervals 5/16, rhythm 7/16;
  - the follower: 3/16;
  - b27 "PEAK: inversion": 3/16 (and declared at the wrong beat).
  - These labelled "entries" are not the subject.
- After the G minor subject ends at b14.3 (the augmentation's tail runs to b16), the next subject statement is at b27. That is 12 bars, about 40 s at q=69, roughly a third of the piece.
- The generated canon collapses into the tenor:
  - b22–24 both voices sit inside C4–Ab4, mostly in thirds (b23.1 G4/E4, Ab4/F4, E4/Db4, E4/C4);
  - the leader circles E–F–G–Ab, the v2 problem that was supposedly fixed;
  - harmonically this is i–V in F minor for three bars.

**Why it fails.** This is the "plodding" middle and the "fugues sound the same" problem in a nutshell. In BWV 847 the subject is absent for at most 2–4 bars at a time, and every episode is built from the subject head or a countersubject in invertible counterpoint. A generated contour line in mirror canon has no motive for the ear to follow.

**Fix**
- Delete b17–24 and recompose the middle by hand from three sources: an episode model made of the subject head plus the E1 dotted motif, used in three permutations (§3.3); the mirror trio in F minor; and a genuine stretto.
- Keep the middle to 10 new bars (§3.3, new bars 19–24).
- Declare `subject` in the score so that `critic.py` verifies every labelled entry.

### P3. A square 2-bar grid with simultaneous cadences: the cause of "plodding" (High)

**Evidence**
- Every entry starts on the downbeat of an odd bar (subject_entries t = 0, 8, 24, 32, 48, 72, 104, 120 quarters).
- The subject begins with a quarter on the downbeat and ends `B4:2 C5:4`. The CS is written to end `Eb5:2 B4:2 C5:2` at the same moment, so both voices cadence together:
  - b4.4: B4/G3 then C5/C4, an octave;
  - b10.4: D5/Bb3 then Eb5/Eb4, an octave;
  - b16.4: a bare D5/D3, held for a beat;
  - b6.3: G5/G2, held for a beat.
- Attack-point profiles show the same collapse at every structural arrival. b1, b13, b27 and b31 are all `x...x.x.x.x.x.x.` (7 attacks), while the bars before them carry 12–16. For example, b26 has 16 attacks and b27 has 7.

**Why it fails.** The listener hears a stop every two bars and a deflation at every important moment. Bach avoids this by overlapping:
- the CS keeps running through the subject's last note;
- the next entry or episode starts before the cadence;
- entries begin off the beat (847's subject starts after an eighth rest).

**Fix**
- Rewrite the CS's last three notes so that it does not cadence with the subject. Let it run on in 16ths across the bar line into the next unit.
- Stagger the entries: the third entry at b6.3 rather than b7.1, the Eb entry after an eighth rest, and the stretto entries every half bar.
- In three voices, always keep one voice moving in 16ths through the subject's opening quarter. CS2 (§3.2) is designed to syncopate across beat 2.

### P4. The "peak" (b27–28) is the weakest bar rhythmically and texturally (High)

**Evidence**
- b27: Upper `C6:4 B5:2 D6:2 G5:2 Eb6:2 G5:2 F6:2`; Lower `C3:4 G2:4 C3:2 F2:2 C3:2 Eb2:2`.
  - The two voices move in identical rhythm.
  - The bar opens with a bare C6/C3 octave held for a beat at velocity 96.
  - It has 7 attacks.
- The promised "inversion a quarter later" survives only as the fragment G2 C3 F2 C3 Eb2 (A is G Ab F C Eb): 3/16 intervals.
- b27.3.5: Eb6 over F2, a 7th left by leap in both voices.
- b28.1.5: C6 over B2, a minor 9th in 16ths at ff.
- The v4 report admits the real stretto had to be dropped because it clashed.

**Why it fails.** The loudest point has the least counterpoint. A climax needs maximum contrapuntal density: Bach's are strettos, or the subject over a pedal with full harmony.

**Fix.** Use a stretto à 3 of S at the half bar, tested with 0 parallels, 0 unresolved and 0 eighth clashes (§3.2 B4):
- soprano S at C6;
- bass S at C3, half a bar later;
- alto S at C5, another half bar later.

Arrive on V7 at new b28.4 and keep the deceptive cadence.

### P5. The exposition never leaves the tonic, and no middle key is entered by a cadence (High)

**Evidence**
- The answer (b3–4, `G3:4 Ab3:2 F3:2 C4:2 Eb3:2 C4:2 D3:2 | … Ab3:2 G3:4 C4:2`) begins on G but is entirely in C minor, and it closes with a perfect cadence in C at b4.4.
- New keys:
  - Eb (b7): b6.4 is Ab5/C3, then b7.1 has Eb5 alone and Ab3 enters under it. The new key arrives on its IV, with no V–I.
  - G minor (b13): b12.4 is C7 (C3, E5, G5, Bb5), V7 of F minor, followed by bare G5/G3. That is V7/iv to v, a non-sequitur.
  - F minor (b19): b18.4 is A4/C3 (F major 6/4) going to F2/C5.

**Why it fails.** There is no tonic–dominant tension in the exposition. BWV 847 answers in G minor at b3, and every later entry is prepared by a cadence or a sequence that cadences. Without arrivals, the key plan in §1 is inaudible, which is part of what Sam hears as harmonically static.

**Fix**
- Answer with the mirror at the dominant, transposed real +7: `D5 Eb5 C5 G5 Bb4 G5 A4 | Bb4 C5 D5 C5 Bb4 C5 D5 Eb5 D5 G5`. Its pair with CS (transposed to G minor) is the same tested combination as in C.
- Give the codetta (new b5–6) the job of returning to C for the bass entry, as 847 b5–6 does.
- End each episode with V–i in the new key, so that the entry follows the cadence or completes it.

### P6. The prelude is a chord chart with no line, no non-chord tones and no voice-leading (High)

**Evidence**
- `prel3.py` builds every note from `voicing()`, a search over chord-tone combinations, followed by a fixed `fig()` order. There is not a single passing tone, neighbour note or suspension in 31 bars.
- critic tertian fit is 90.3%, against 70.4% for BWV 847's prelude with the same tool. Bach's figure (C–Eb–D–Eb over the bass) has a built-in neighbour note; this one (`Eb4 C5 Eb5 G4`) does not.
- The top line (reduce `^top`) is:
  - Eb5–F5 alternating for b1–12;
  - G5–Ab5–Bb5 for b13–18;
  - Eb5–A5 for b19–24;
  - G5–Ab5 for b25–30;
  - C6 only as the final note.
- Writing the music in code also violates CONVENTIONS ("every note written as a bar string").

**Why it fails.** Bach's figuration preludes are voice-leading in disguise: three or four implied voices move by step, with suspensions and neighbour tones that create the forward pull. Here the implied voices jump to wherever the optimiser put them, so harmony changes but nothing "goes". This is the "too far from the WTC idiom" complaint.

**Fix**
- Rewrite as literal bar strings.
- For each section, first write a 3- or 4-voice chorale skeleton (soprano line, inner voice with 7–6 and 4–3 suspensions, and the present bass, which is good), then derive the figuration from it.
- Give the figure one non-chord tone per group: a lower neighbour on the second 16th, as in 847, or a passing tone between group tops.
- Make the soprano a real line with an arc that peaks in the pedal section (see P7, and §4.3 for the subject hidden in the accents).

### P7. Literal repetition over static chords; the dominant pedal recedes (High)

**Evidence**
- One chord with one 4-note cell repeated four times fills each of b1, b3, b5, b12, b25 and b28. b1 and b3 have identical right-hand notes.
- b8–9: the cell D4 Ab4 Bb4 | Ab4 Bb4 F5 is repeated 5⅓ times over Bb2, for 32 sixteenths of Bb7.
- b16–17: F minor for 1½ bars of the same wave.
- b19–24: the left hand plays only G2 for 6 bars (19% of the piece). The level drops from 74 (b13–18) to 70 (`build_prelude3.py` lvl), and the right hand stays within Eb4–A5.

**Why it fails**
- A single figure on a single chord for a whole bar can work (847 does it), but there the voicing changes every bar and a stepwise line runs through it. Here the same notes recur after the "return" (b25 = b1).
- The six-bar pedal is the moment of maximum metric chaos, yet it is static, quiet and registrally capped. It should be the climax.

**Fix**
- Cut the pedal to 4 bars (keep the 2-bar, half-bar, quarter acceleration).
- Make the top voice climb through it, from G5 to C6 or Eb6, with a crescendo to the highest level of the piece.
- Break off with a rhetorical rupture (§4.3), then regain the downbeat at b25.
- Give b8–9 a moving inner line (Ab4–G4–F4 under the Bb7, or a 4–3 over Bb) so that two bars of the same chord become a suspension chain.
- Re-voice b3, b12, b25 and b28 so that no bar repeats another's notes.

### P8. "Losing the beat" is not dramatised; the left hand is inert (Medium-High)

**Evidence**
- From b6 on, the left hand re-strikes only at right-hand group starts (`prel3.py`: "LH attack at chord changes and at group starts"). The listener never hears a steady beat for the 3- and 5-groups to contradict, so the beat is lost by vagueness rather than by conflict.
- The left hand has 80 notes, against 487 in the right hand.
- Awkward isolated bass pops:
  - b9: `Bb3:1` on the last 16th;
  - b16–17: `F3:9~ | F3:1 F2:7`, an octave drop on the second 16th of the bar.

**Why it fails.** A cross-rhythm needs a reference. This is the difference between the "metric dissonance" the concept promises and mere irregular accents.

**Fix.** Script the beat explicitly:
- **A (b1–5).** Left hand on beats, in 8ths (a real bass line, not re-strikes).
- **B (b6–11).** Left hand keeps a quarter- or 8th-note bass line on the beat while the right hand groups in 3s, so the conflict is audible.
- **C (b13–18).** Left hand begins to follow the 5-groups; the beat dissolves.
- **D (pedal).** No beat at all, then the rupture.
- **E (b25–).** Both hands slam back onto the downbeat.

Share 16ths between the hands in A and E, as in 847.

### P9. The augmentation section (b13–16) undermines its own device (Medium)

**Evidence**
- b13.4: D5 against A3, an unprepared and unresolved 4th. This is critic's only error.
- b13.2: F#5 against G3, an accented major 7th for an eighth, approached from above and left by a leap of a 3rd.
- stretto_finder for S against its augmentation (C3) does not rank S at offset 0 and the octave (the v5 placement) in its top 25. The cleanest placements are:
  - the mirror inversion starting on D, entering at the second bar of the augmentation (offset 16, +4 or +11 steps): cost 8, 0 unresolved;
  - S at offset 4, a third higher: cost 13.
- b15–16 upper voice is generated.
- The section ends on a bare D5/D3 octave held for a beat (b16.4), and b13 has only 7 attacks.

**Why it fails.** The section's selling point, "the subject over its own augmentation", opens with a clash and ends in an empty octave, and half of it is filler.

**Fix (three voices, new b15–18)**
- Bass: augmentation from G2, 4 bars.
- Alto: S in G minor, moved so that the b13.4 4th becomes a 3rd or 6th; alternatively start a quarter later.
- Soprano: the mirror inversion entering at new b16.1 (offset 16), the best tested placement.
- The result is subject, inversion and augmentation together, with a free voice made from CS and CS2 fragments instead of `gen()`. Cadence into the episode, not onto an octave.

### P10. E2 collisions (b11–12) that "sound like mistakes" (Medium)

**Evidence**
- Lower b11 `Eb3:3 F3:1 G3:2 F#3:2 Ab3:4`: F#3 to Ab3 is a melodic diminished 3rd (b11.2.5 to b11.3), with Db5 arriving two 16ths later in the upper voice (b11.3.25).
- b12.1: lower `Db3 C3 A2`; A2 enters under Db5 (a diminished 4th) and then sits under Bb4 (a minor 9th, b12.1.75).
- b12.4: tritone leap Bb5–E5 in the upper voice (critic).
- The bar ends on C7 (b12.4), which leads to F minor, but b13 is G minor (see P5).

**Why it fails.** There are three chromatic inflections in a single beat (F#, Db, A) with no harmonic logic. This is precisely the "collision" Sam objects to.

**Fix.** Discard both voices. New b13–14 (E2) should be the episode model with voices exchanged, a diatonic falling-fifths sequence (Eb, Ab, D7, g) that cadences V–i in G minor. Introduce F# only as the leading tone of the cadence.

### P11. The tonic pedal (b31–32) is unplayable and a fake voice (Medium)

**Evidence**
- critic: 3 onsets exceed two hands at b32.1–32.2 (C2 + G3 + Eb5; C2 + G3 + D5).
- The left hand would need to hold C2 while playing the lower stretto voice in G3–F4, a span of 29 semitones.
- The pedal lives on a separate "Pedal" staff of one note.

**Why it fails.** It cannot be played as written on a piano, and it inflates the voice count.

**Fix.** In three voices the bass is the pedal voice. Either:
- keep the inner voice within a 10th of the pedal (pedal on C3, inner voice in G3–Eb4) and give the stretto to soprano and alto in the right hand plus the top of the left hand; or
- (better, §4.2) replace the static pedal with BWV 847's subject in augmentation, which is itself a quasi-pedal (C–B–C–G–Ab–C–B–C–D…) and is playable because it moves in quarters and halves.

### P12. A double ending; the final sonority is a bare 10th (Medium)

**Evidence**
- b30 V goes to b31 i, with the pedal starting there. Then the pedal is abandoned (b32), and a second, thinner cadence follows: iv–V–i in b33–34 (`D5 Eb5 G5 Eb5 C5 Bb4 Ab4 C5 D5 B4 | C5:4 G4:4 Eb4:8` over `B3 C4:4 G3 Ab3 F3 Ab3 G3 G2 | C3:8 C2:8`).
- The last two beats are C2 and Eb4 only.

**Why it fails.** Bach's order is cadence, then pedal coda with the subject over it, then a full final chord (847 ends with a Picardy C major chord over the pedal). v5 does it backwards: the coda comes first and a weaker cadence follows it, ending on a two-note interval after an ff peak.

**Fix**
- Make the final cadence (V at new b30 to i) the start of the coda.
- Run the coda over the bass (pedal, or the augmented 847 subject) to the end.
- Finish on a full three-voice chord. A Picardy C major (E4 or E5 on top) is the 847 homage. If the minor ending is kept deliberately, voice the full C–G–Eb triad and document the choice in NOTES.md.

### P13. The build (b25–26) is prelude figuration, not fugue (Medium-Low)

**Evidence**
- Upper b25–26: `Eb5 G5 D5 G5 C5 F5 Ab5 C6 B5 G5 D5 G5 | F5 Ab5 C6 Ab5 A5 C6 Eb6 C6 D6 G6 D6 Eb6 D6 C6 B5 D6`. These are broken-chord arpeggios; the author's report calls it "plain and functional … textbook".
- critic flags a weak P8 at b26.1 (G5/G2 to F5/F2).
- There is no subject material from b24.3 to b26.

**Why it fails.** The approach to the climax should be thematic accumulation, such as head-motif strettos, not arpeggio.

**Fix.** Keep the lament bass. Above it, alto and soprano exchange the subject head (C–B–D–G) and its mirror (G–Ab–F–C) a beat apart, climbing by step per half bar to G6. The bass joins the head in the last half bar of b26, which leads straight into the stretto à 3.

### P14. Romantic wave figuration; octaves on accents (Low-Medium)

**Evidence**
- b13–18 5-groups span a 10th to a 13th, with an octave-plus return every group. For example b13: `Db4 Eb4 G4 Bb4 G5 | Db4 …`, and b14 Ab5 to C4.
- critic reports 41 "leap > octave" across the prelude. The right hand must reposition its hand on every group.
- Weak P8 between the outer voices on accents (critic): b11.4 Ab4/Ab2 to Bb4/Bb2; b26.3 and b29.2 Ab4/Ab2 to F4/F2.

**Why it fails.** It sounds like a 19th-century étude rather than WTC. Bach's figures stay within one hand position per bar. The octaves hollow out the accent that is supposed to articulate the group.

**Fix.** Use 5-note figures within an octave, for example rising 1–3–5–8 plus a neighbour back, or split them between the hands (left hand plays notes 1–2, right hand 3–5). Voice each group's accented note so that it does not double the bass pitch class on beats.

### P15. A squeezed final cadence; no motivic link to the fugue (Low)

**Evidence**
- b30: `C4 Eb4 G4 Eb5 Ab5 | C4 F4 Ab4 F5 Ab5 | B3 D4 G4 Eb5 G5 Eb5` over a C2 pedal. Because the 5-groups straddle the chord changes, the vii°7 lasts four 16ths (F5 Ab5 B3 D4) and the leading tone is a single low 16th.
- No pitch, rhythm or contour of the fugue subject appears anywhere in the prelude.

**Fix**
- Give b30 two bars (i–iv–vii°7–i) in aligned groups of 4.
- Plant the fugue subject in the prelude's accented notes (§4.3).

### P16. Tempo and character (Low)

**Evidence.** q=69 "Andante con moto, sempre avanti" with a subject that opens on a quarter plus six eighths. The 34 bars last about 118 s.

**Why it fails.** It is too slow for a 16th-driven fugue, and it reinforces P3. Typical performance tempi for BWV 847 are q≈80–90.

**Fix.** Use q≈80, and judge it again only after P3 is fixed.

---

## 3. Three-voice expansion plan (Fugue II à 3)

### 3.1 Voices and roles

| Voice | Range | Role |
|---|---|---|
| Soprano | B4–G6 | Plays the answer in the exposition. |
| Alto | G3–Ab5 | Opens with the subject, as in 847. |
| Bass | C2–D4 | The third entry at b7 in the tonic, as in 847. |

Material:
- **S**: the subject.
- **A**: the mirror answer. Transpose it real +7 (start on D) for the exposition answer; keep the C-minor form for later.
- **CS / CSI**: the countersubject and its mirror.
- **CS2 (new)**: a slow, syncopated line in 8ths and quarters with a 4–3 suspension feel. It must stay in triple counterpoint with S+CSI and, by mirror, with A+CS.

### 3.2 Tested building blocks

All combinations were checked by critic and the off-beat clash harness: **0 parallel errors and 0 unresolved dissonances in every case**. "Rough" is the stretto_finder roughness summed over voice pairs; "8th clashes" counts eighth-or-longer dissonances on off-beats that no voice leaves by step.

| ID | Block | Lines and offsets (16ths) | Result |
|---|---|---|---|
| B1 | Third exposition entry (rectus trio) | Bass S `C3` @0. Soprano CSI `F5:1 Eb5:1 D5:1 C5:1 B4:1 D5:1 C5:1 B4:1 C5:1 D5:1 Eb5:1 G5:1 F5:1 D5:1 \| C5:2 F5:2 G5:1 A5:1 B5:1 A5:1 G5:1 F5:1 Eb5:2 Ab5:2 G5:2` @2. Alto CS2 sketch `R:2 G4:4 F4:2 Eb4:4 D4:4 \| Eb4:2 Ab4:2 G4:4 D4:2 C4:2 Eb4:2 D4:2` | 0 weak parallels, no 8th clashes, rough 7.2 |
| B2 | The same trio mirrored around D4 (inversus trio) | Soprano A `G5`. Alto CS2I `R:2 C4:4 D4:2 Eb4:4 F4:4 \| Eb4:2 B3:2 C4:4 F4:2 G4:2 Eb4:2 F4:2`. Bass CS `D3…` | 0 weak parallels, one 6/4 eighth at the end, rough 6.1 |
| B3 | S + inversion + augmentation | Bass S×2 from C3; mirror inversion on D at offset 16 | Pair cost 8, the best placement (stretto_finder `--against` the augmentation, `--axis D4`) |
| B3′ | Full trio variant over the augmentation | S `C5` @10 and A `D5` (real +19) @22 | 1 weak parallel, no 8th clashes |
| B4 | Stretto à 3 at the half bar | S `C6` @0, S `C3` @8, S `C5` @16 | 0 weak parallels, no 8th clashes, rough 6.9 |
| B4 alt | Stretto à 3 with the mirror in the bass | S `C6` @0, S `C5` @8, A `G3` @18 | Clean, rough 6.7 |
| B5 | BWV 847 subject augmented in the bass (coda) | Bach `C3` augmented, after a literal quarter rest (@4). Our A `G4` @10, our S `C6` @30 | Clean, rough 9.1 |

CS2 is a sketch, but it works rectus and mirrored, so the exposition trio has a complete mirror image. Its job is harmonic glue:
- it holds G through the V6 at b1.2;
- it moves Eb–D under the i6/4–V;
- it suspends Ab to G in bar 2.

Polish it by ear, then re-test it against the Eb forms used later.

### 3.3 Bar map: before (v5) and after (new)

| New bars | From v5 | Content | Key | Voices |
|---|---|---|---|---|
| 1–2 | 1–2 | **Alto: S (C5).** Unchanged. | c | 1 |
| 3–4 | 3–4 | **Soprano: A at the dominant (D5).** Alto: CS (G-minor form, from A4; tested invertible at −14). The CS ending is rewritten to run on, not cadence (P3). | c→g | 2 |
| 5–6 | 5–6 (recomposed) | **Codetta.** The E1 dotted head motif as a true 1-bar model, sequenced down a step, g→c, ending on V. Both voices hand-written. | g→c | 2 |
| 7–8 | new | **Bass: S (C3), the third entry.** Soprano: CSI. Alto: CS2 (block B1). First full texture. Can start at b6.3 to break the grid. | c | 3 |
| 9–10 | replaces 9–10 | **Episode 1.** The episode model in triple invertible counterpoint: soprano and alto in canon on the head motif at a half bar, bass in CS-derived 8ths. Cadences V7–I in Eb. | c→Eb | 3 |
| 11–12 | 7–8 | **Soprano: S in Eb** (v5 b7 upper). Bass: CSI (v5 b7 lower). Alto: CS2 in Eb. The second Eb entry (v5 b9–10) is cut. | Eb | 3 |
| 13–14 | replaces 11–12 | **Episode 2** = Episode 1 with soprano and bass exchanged. Falling fifths Eb–Ab–D7–g, V–i in G minor. Fixes P10. | Eb→g | 3 |
| 15–18 | 13–16 | **Augmentation section.** Bass: S augmented (G2). Alto: S in G (repositioned, P9). Soprano: mirror inversion entering at 16.1 (block B3). Bars 17–18: alto and soprano continue with CS/CS2 fragments, no filler. | g | 3 |
| 19–20 | replaces 17–18 | **Episode 3** = the third permutation (alto on top). Cadences in F minor. | g→f | 3 |
| 21–22 | replaces 19–24 | **Inversus trio (block B2) in F minor:** the whole exposition texture played upside down. | f | 3 |
| 23–24 | replaces 19–24 | **Stretto à 2** at the octave, half a bar apart (S self-stretto, cost 5). Alto then soprano; bass walks to the dominant of C. | f→c | 3 |
| 25–26 | 25–26 | **Build.** Lament bass kept. Head-motif stretto in alto and soprano a beat apart, climbing to G6. Bass takes the head at 26.3 (P13). | c: V | 3 |
| 27–28 | 27–28 | **Peak: stretto à 3** (block B4). Soprano C6, bass C3, alto C5 at half-bar distances. Ends on V7 at 28.4. | c | 3 |
| 29–30 | 29–30 | **Deceptive VI, N6, V.** Keep the harmony. The alto adds 7–6 suspensions over the bariolage bass. | c | 3 |
| 31–35 | 31–34 (recomposed) | **Coda.** Bass: BWV 847 subject augmented from C3 (block B5), as the animated pedal; it lands on Eb2 (i6) at 35.1. Alto: A (G4) from 31.3.5. Soprano: S (C6) from 32.4.5, then into the final stretto. b35.2–4: iv–V (or iv–vii°7–V). | c | 3 |
| 36 | 34 | **Final full chord.** Picardy C major, or a voiced minor triad (P12). | C | 3 |

**Totals.** 36 bars, against 34 now. At q≈80 that is about 108 s, against 118 s now. Entries:
- 3 exposition entries;
- Eb entry;
- G minor (S, augmentation, inversion);
- F minor inversus trio and stretto;
- stretto à 3;
- coda with the 847 guest.

The longest stretch without a subject statement is 2 bars (each episode).

### 3.4 What the third voice does in each section

- **Exposition (1–8).** The third voice is the bass, entering in the tonic at b7 under CSI and CS2. From then on, CS2 gives each beat a third chord member. This alone makes the harmonic rhythm audible: today reduce shows mostly `?` dyads.
- **Episodes (9–10, 13–14, 19–20).** One model in triple counterpoint, heard in three permutations (847 does this with its b5–6 and b9–10 episodes). The voice entering on top changes each time, so the listener recognises the episode and hears that it has changed.
- **Middle (15–24).** The third voice makes the combinations possible: subject, inversion and augmentation together; the mirror trio; a stretto with a free accompanying voice.
- **Build (25–26).** Two voices exchange the head, while the third keeps the lament bass that v5 already has.
- **Peak (27–28).** All three voices state S, half a bar apart.
- **Coda (31–36).** The bass carries the 847 subject in augmentation. The two upper voices state the inversion and the subject, then close the final stretto into a full chord.

### 3.5 Process requirements (non-negotiable)

1. Write every bar in `cycle/02-c-minor/fugue.py` as literal tokens. Do not import `gen` or `fill`, and do not transform material by code except with the explicit `transpose`, `invert_diatonic` and `scale_rhythm` helpers.
2. Build with `wtclib.build_score(..., subject=S)` so that critic verifies every declared entry. Every label must score ≥14/16 intervals, or say "modified".
3. Re-run `stretto_finder --against` for every combination that is changed by hand, and the critic on the whole piece.

---

## 4. "Turn it up to 11": three opportunities to implement while fixing

### 4.1 The mirror trio: the whole exposition played upside down

**What it is.** v5 already has the hardest ingredient: a subject, answer and countersubject that mirror exactly around D4. With CS2 (block B1), the complete three-voice texture of the third entry has a working diatonic mirror image (block B2). Rectus and inversus both pass with 0 errors.

**Where it goes.** Present it rectus at new b7–8 in C minor and inversus at new b21–22 in F minor:
- what was the bass subject becomes the soprano answer;
- the soprano countersubject becomes the bass countersubject;
- CS2's syncopations turn upside down.

This is the device of Contrapunctus 12/13 in *The Art of Fugue*, which Bach never put into the WTC. Because CS2's suspensions invert into recognisable "retardations", the trick should be audible as well as on paper.

**Optional extension.** Make the Eb entry (new b11–12) the mirror trio as well. The finder shows the Eb pairs are just as clean (cost 6–8).

### 4.2 BWV 847's subject as a guest: the coda's pedal is Bach's subject in augmentation

**What it is.** Bach's subject, augmented and transposed to C3, with its eighth rest augmented to a quarter rest:

```
R:4 C3:2 B2:2 C3:4 G2:4 | Ab2:4 C3:2 B2:2 C3:4 D3:4 | G2:4 C3:2 B2:2 C3:4 D3:4 | F2:2 G2:2 Ab2:8 G2:2 F2:2 | Eb2:4
```

It is almost a tonic pedal that happens to be a famous subject. Over it:
- our inversion at G4, entering at b1.3.5;
- our subject at C6, entering at b2.4.5.

This is clean (block B5). It replaces v5's unplayable static C2 pedal (fixes P11), keeps Bach's own closing gesture (subject over a tonic pedal, 847 b29–31), and ends on Eb2 (i6), which leads naturally into the final iv–V–I.

**A normal-speed alternative cameo.**
- Bach's subject transposed real +7 (G5 F#5 G5 D5 Eb5 …) entering an eighth after our subject's downbeat, which is exactly Bach's own eighth rest: cost 9, 0 unresolved.
- Bach's tonal answer (G F# G C Eb …) at the same distance: cost 11.

Either could replace the soprano in new b23–24 or appear as a single "guest entry" in the Eb or G-minor middle.

**Credit.** Credit the quotation in NOTES.md.

### 4.3 Prelude: the accents spell the fugue subject, and the lost beat ruptures as in 847

**Accents spell the subject.** In sections B (3-groups) and C (5-groups), make the accented first note of each group trace the fugue subject:
- **3-groups:** C–B–D–G–Eb–G–F… at one note per 3 sixteenths. The subject sounds as a hemiola melody in dotted 8ths against the left hand's steady beat (P8).
- **5-groups (b13–18):** the accented low notes trace the mirror answer (G–Ab–F–C–Eb–C–D) in quintuple 16ths over the chromatic bass, which is kept.

This gives the prelude the melody it lacks (P6), audibly links the pair (P15), and makes "losing the beat" literal: the subject is there, in the wrong metre.

**The rupture.** At the end of the shortened dominant pedal:
1. Let the regrouping collapse into an unmeasured run (a free 32nd-note flourish over G, like 847's "Presto").
2. Stop on a fermata at vii°7/V.
3. Add a two-bar "Adagio" recitative, with the subject head C–B–D–G in single notes.
4. Regain the beat fortissimo at b25.

This is BWV 847's rhetoric re-purposed as the climax of this prelude's own story.

---

## Appendix: reproducing the key tests

```
# S self-stretto (best: offset 8, -7 steps, cost 5)
python3 tools/stretto_finder.py --subject "C5:4 B4:2 D5:2 G4:2 Eb5:2 G4:2 F5:2 Eb5:1 D5:1 C5:1 D5:1 Eb5:2 D5:1 C5:1 B4:2 C5:4 G4:2" --scale C:minor --top 20

# S / inversion against the augmentation (best: inversus, axis D4, offset 16, +4/+11 steps, cost 8)
python3 tools/stretto_finder.py --subject "<S>" --against "C3:8 B2:4 D3:4 G2:4 Eb3:4 G2:4 F3:4 Eb3:2 D3:2 C3:2 D3:2 Eb3:4 D3:2 C3:2 B2:4 C3:8 G2:4" --scale C:minor --forms rectus,inversus --axis D4 --max-offset 32 --steps=0,2,4,7,9,11,14

# BWV 847 subject against ours (diatonic -5/-12 at offset 2 = Bach's own Eb-major form, cost 9)
python3 tools/stretto_finder.py --subject "C5:1 B4:1 C5:2 G4:2 Ab4:2 C5:1 B4:1 C5:2 D5:2 G4:2 C5:1 B4:1 C5:2 D5:2 F4:1 G4:1 Ab4:4 G4:1 F4:1 Eb4:2" --against "<S>" --scale C:minor --forms rectus --max-offset 16
```

The trio, stretto-à-3 and augmented-847 checks used a scratch harness built on `critic.analyse` with the exact tokens and offsets given in §3.2. Re-creating them as a small JSON score and running `tools/critic.py` gives the same result.
