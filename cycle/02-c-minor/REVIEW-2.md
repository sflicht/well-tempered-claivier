# Pair II in C minor: second review (the rebuilt pair, as built on 27 October)

**Scope.** I reviewed these files:
- `prelude.py`, which builds `prelude.json`;
- `fugue.py`, which builds `fugue.json`;
- `NOTES.md`, and the first review `REVIEW.md`, whose plan the rebuild follows.

**Method.** I read every bar and ran `tools/critic.py`, `tools/reduce.py` and `tools/stretto_finder.py`. I also used two scratch scans:
- every simultaneous attack forming a 2nd, 7th or 9th, at sixteenth resolution;
- a check of the prelude's group starts against every left-hand strike.

I have not heard the renders.

## Verdict

The rebuild did what REVIEW.md asked:
- three real voices;
- an exposition shaped like BWV 847's, with a cadencing link;
- every new key entered by a cadence;
- a stretto à 3 at the peak;
- a guest subject in the coda;
- the prelude rewritten by hand.

The surface is clean: 0 parallels and 0 unresolved dissonances in the fugue. The grouping plan in prelude section D matches the left hand at every group start.

What is left is **rhetoric**. Where the music should turn, it turns too fast or not at all:
- the fugue's deceptive cadence;
- the prelude's final section;
- one fugue episode.

Two devices are also used twice in quick succession, so the second use loses its force.

## Ranked issues (both movements)

| # | Mvt | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|---|
| 1 | Fugue | 29 | The deceptive cadence lasts one eighth on a weak half-beat (29.3½) and is overwritten by iv | **High** | Bass and soprano rewrite of bar 29 only: VI on beat 4 for a quarter |
| 2 | Prelude | 25–29 | The return sits still at the loudest level: two-beat RH cells played twice over left-hand octave eighths | **Medium-high** | The left hand takes the same neighbour figure in sixteenths (BWV 847's two-hand texture) |
| 3 | Fugue | 19–20 | Episode 3 marks time: bar 20 plays i6–V twice | Medium | One bass note: 20.3 `Ab2:4` → `Ab2:2 Db3:2` |
| 4 | Fugue | 23–28 | The peak repeats the half-bar octave stretto heard four bars earlier, in the same key; bars 23–36 never leave C minor | Medium | Make 23–24 the subject plus the mirror answer a quarter apart (finder cost 8, 0 errors) |
| 5 | Prelude | 24 | The Adagio's bass resolves the long dominant to VI and spends the deceptive cadence that bar 28 needs | Low-medium | Adagio left hand `G2:8 F2:4 G2:4` |
| 6 | Fugue | 36 | The Picardy chord C2 – C5 – E5 is hollow | Low | Add notes, as Bach does: C2+C3, G4+C5, E5 |
| 7 | Fugue | 21–22 | The mirror trio is low and dark: three low seconds | Watch | Only if the render is muddy: alto −6 velocity |
| 8 | Prelude | 13–18 | Nineteen identical rising five-note waves | Watch | Only if Sam finds it un-Bachian: turn the waves down in 16–17 |

**At pair level**, the deceptive move V → VI happens three times: prelude 24.1, prelude 28 and fugue 29.3½. Items 1 and 5 together leave two, and make both count.

---

## Prelude II: "losing the beat"

### Must not be touched

- **The grouping dramaturgy.** The 16ths pass from fours, to threes against a steady left-hand beat, to fives with the left hand joining, to mixed groups over the pedal, to the Presto/Adagio break, and back to fours. It is "turned up to 11" while staying inside BWV 847's idiom of perpetual sixteenths.
  - **Section B (6–11)** is the best realisation: each three-note group begins on its highest note, so contour defines the threes, and the left-hand quarters keep a beat for them to lose.
  - **Section C's chromatic bass** (D♭–C–D♭–E–F–D♭–A♭ to the German sixth) is the best harmony of the pair.
- **The climb to the break (19–23).** Over the G pedal the harmony speeds up while the waves climb G5 → A♭6. Then come the 32nd-note diminished-seventh sweep and the held C5 at the end, which is the fugue's first note.

### P1. Bars 25–29: the return is the most static stretch, at the loudest level (Medium-high)

**What is written.**
- Bar 25 is `(E♭5 C6 B5 C6)(G5 C6 B5 C6)` played twice.
- Bar 28 is `(E♭5 C6 B♭5 C6)(A♭5 C6 B♭5 C6)` played twice.
- Bars 26–27 are two-beat cells, each played twice.
- The left hand plays octave eighths: `C3 C4 C3 C4 …`, `A♭2 A♭3 …`, `G2 G3 …`.
- The level is +16, so accented notes reach about velocity 94.

**Why it fails.** For 18 bars the grouping was the event. In section E only the harmony is left to happen, and the harmony is good (i | iv6 N6 | i6/4 V7 | VI | iv6 N6 i6/4 V7). But a C6–B5–C6 neighbour figure struck 16 times a bar for four bars over an octave-pumping left hand reads as an étude. It is also the least Bach-like texture in the pair, exactly when the piece should sound most like itself.

**Fix.** Give the left hand the same neighbour figure in sixteenths. Build it on the chord's third or fifth, so the neighbours move in sixths with the right hand and never in octaves; this is how BWV 847 itself is built.

| Bar | Left hand |
|---|---|
| 25 | `C3:1 Eb3:1 D3:1 Eb3:1` ×4 |
| 26 | `Ab2:1 C3:1 Bb2:1 C3:1` ×2, then `F2:1 F3:1 Eb3:1 F3:1` ×2 |
| 27 | `G2:1 Eb3:1 D3:1 Eb3:1` ×2, then `G2:1 D3:1 C3:1 D3:1` ×2 |
| 28 | `Ab2:1 Eb3:1 Db3:1 Eb3:1` ×4 |

- **Bar 28.** Do *not* use C3–B♭2–C3 under the right hand's C6–B♭5–C6: that makes parallel octaves.
- **Bar 29.** Work it out on the same principle.

The fix doubles the drive, turns the return into an audible homage, and adds no new harmony.

### P2. Bar 24: the Adagio spends the deceptive cadence that bar 28 needs (Low-medium)

**What happens.** Four bars of dominant pedal and the sweep over G1 (bar 23) lead into the Adagio, where the bass goes `Ab2 G2 F2 G2` under `C5 B4 D5 G4`. The long dominant therefore resolves deceptively onto A♭ at 24.1. At ♩ = 40, in two bare voices, that chord lasts 1.5 s and will be heard as the event.

**Why it matters.** Four bars later, bar 28's "deceptive cadence" repeats V → VI as a whole bar at the loudest level, and the listener has just heard that turn.

**Fix.** Keep the dominant through the Adagio: left hand `G2:8 F2:4 G2:4`.
- C5 over G2 is a cadential six-four that falls to B4 (4–3).
- D5 over F2 is V4/2.
- G4 over G2 leads to i at 25.

The recitative keeps the pedal's tension, and VI is saved for bar 28.

### P3. Bars 13–18: the waves (watch)

**What is written.** Six bars contain about nineteen identical rising five-note waves (`G4 Ab4 Bb4 Db5 Eb5 | Bb4 C5 Db5 Eb5 G5 | …`), with one chord per bar.

**The risk.** This is the pair's most Romantic, étude-like texture, and the furthest from the WTC; the chromatic bass justifies it.

**Fix, only if Sam finds it un-Bachian.** Turn the waves downward in bars 16–17. The section then rises and falls instead of rising nineteen times.

---

## Fugue II (a 3)

### Must not be touched

- **Bars 1–8.** The exposition follows BWV 847's plan: soprano, alto answer, a two-bar link that cadences (iv – ii°6 – i6/4 – V), then the bass entry at bar 7. It is unmistakably WTC in shape, and the mirrored answer (a counter-fugue answer, as in Art of Fugue Contrapunctus 5–7) is the twist. Don't "normalise" the answer.
- **The coda, 31–35.** BWV 847's subject, augmented in the bass under our mirror answer, is recognisable (C B C G A♭ …) and gives the close a cantus-firmus breadth.
- **Bars 15–18.** The subject, its augmentation and its inversion sound together; the texture is dense but harmonically clear (g: i – V – iiø – V – i).

### F1. Bar 29: the deceptive cadence is an eighth note on a weak half-beat (High)

**What is written.**
- Bass: `B2 C3 G2 G2 Ab2 F2`.
- V7 on beat 3 (G2 / B4 / F5) → VI on 3½ (A♭2 / C5 / E♭5) → iv on beat 4 (F2 / C5 / A♭5) → N6 on 30.1.

**Why it fails.** The VI lasts 0.375 s, on the "and" of beat 3, and iv overwrites it at once. The stretto peak drives toward this turn, but it will sound like a passing chord. REVIEW.md asked to keep this rhetoric (V7 → deceptive VI → N6 → V → i). It is still there on paper but compressed below hearing.

**Fix (bar 29 only; the alto is unchanged).**
- Bass: `B2:2 C3:4 G2:2 G2:4 Ab2:4`.
- Soprano: `F5:2 Eb5:2 G5:4 F5:4 Eb5:2 C6:2`.

The result:
- V7 holds beat 3. The alto's C5, the end of its subject, sounds over G2 at 3½ as a brief suspended fourth.
- VI arrives on beat 4 for a full quarter, while the soprano's seventh F5 falls to E♭5.
- C6 at 4½ steps up to D♭6 at the Neapolitan.

iv is dropped; VI → N6 keeps A♭ as a common tone. I checked by hand: no new parallels. A small tempo dip on 29.4 (a `tempo_map` point) would help the turn register.

### F2. Bars 19–20: Episode 3 marks time (Medium)

**What is written.**
- Soprano: `G5 Bb5 F#5 D5 G5 Bb5 E5 C5 | F5 Ab5 E5 C5 F5 Ab5 E5 C5`.
- Alto: the turn figure.
- Bass: `G2 D3 C3 Bb2 | Ab2 C3 Bb2 Ab2 C3`.

**Why it fails.** Bar 20 is i6 – V – V4/2 – i6 – V in f minor: soprano and alto play the same broken chord twice (beats 3–4 repeat beats 1–2) over the same harmonies. These are the prelude-style broken chords that REVIEW.md (P13) asked the fugue to leave behind. They also sit directly before the mirror trio, which starts in the same key on the same chord.

**Fix (one note).** At 20.3, change the bass `Ab2:4` to `Ab2:2 Db3:2`.
- The repeated soprano cell is now harmonised i6 – VI – V: A♭2 → D♭3 → C3, a Phrygian approach to V. The repetition becomes a reharmonisation.
- I checked it: the V4/2's seventh still resolves (B♭2 → A♭2 at 20.3), and D♭3–C3 against the soprano's A♭5–E5 makes no parallel.

### F3. Bars 23–28: the peak repeats the device just before it (Medium)

**What is written.**
- **23–24:** the subject in the soprano, with the alto entering at the octave half a bar later, in c.
- **27–28:** the subject at C6, C3 and C5, at half-bar distances, in c.

**Why it fails.** The peak is louder and has a third voice. To the ear, though, it is the second octave stretto at half a bar in the same key within about ten seconds, and both passages are harmonically i–V–i–V. From bar 23 to the end (14 bars) the music never leaves C minor.

**Fix.** Make 23–24 a different combination, so that bar 27 is the first of its kind.
- **What the finder offers.** `stretto_finder.py --subject "<subject>" --meter 4/4 --scale C:minor --forms rectus,inversus --axis Eb4 --max-offset 16 --offset-step 4 --steps=-11,-10,-7,-4,-3,3,4,7` gives the subject plus the mirror answer, the alto's form of bar 3 (`D4 Eb4 C4 G4 Bb3 …`), entering one quarter later: inversus, offset 4, steps +4, cost 8, 0 errors.
- **Why it fits.** That is the piece's own counter-fugue pairing, tighter than the peak, and new to the ear.
- **What remains.** Re-fit the bass of 23–24 around it and re-run the critic.
- **Alternative.** Keep the octave stretto but move 23–24 to E♭ or g.

### F4. Bar 36: a hollow Picardy chord (Low)

**What is written.** C2 – C5 – E5.

**Why it fails.** There are three octaves of nothing between bass and alto, and no fifth. After a dense coda, on a piano, it will sound thin. BWV 847 ends on a full chord.

**Fix.** Add notes to the final chord, as Bach does: bass `C2` + `C3`, alto `G4` + `C5`, soprano `E5`.

### F5. Bars 21–22: the mirror trio (watch)

**What is written.** The alto lies at E3–C4, the bass at D♭2–D♭3, and the soprano more than an octave above them. The trio produces the three low-register seconds (21.1½, 22.2¼, 22.2¾).

**What the listener hears.** Nobody will hear "the b7–8 block upside down". They will hear a dark f-minor passage, which is fine.

**Fix, only if the render is muddy.** Lighten the alto (−6 velocity). Raising it an octave would cross the soprano.

---

## Checked and found sound

- **Fugue II.**
  - **Entries.** Every entry begins on a consonance.
  - **Augmentation section.** The section at 15–18 is lucid.
  - **Peak.** The flash of III+ (E♭ G B) at 28.3 is a good Bachian colour.
  - **Coda.** The coda's two brief clashes (31.4½ and 32.2½) are passing, as the NOTES say.
- **Prelude II.**
  - **Section D.** In bars 19–22 every left-hand G strikes on a group start (checked against `group_starts()`).
  - **Section A.** The opening phrase (i – V – i6 – ii°6/5 – vii°/iv – V7) is a sound BWV 847-type tonic prolongation.
