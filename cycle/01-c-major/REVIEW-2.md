# Pair I in C major: second review (third edition, as built on 27 October)

**Scope.** I reviewed these files:
- `prelude.py` and `shepard.py`, which build `prelude-notation.json` (the written core) and `prelude.json` (the octave-layered performance);
- `fugue.py`, which builds `fugue.json`;
- `NOTES-prelude.md` and `NOTES-fugue.md`.

**Method.** I read every bar, ran `tools/critic.py` and `tools/reduce.py`, and wrote two scratch scans:
- **(a)** For the two-voice fugue, every simultaneous attack that forms a 2nd, 7th or 9th, at sixteenth resolution. The critic checks only beats.
- **(b)** For the performance score, every sixteenth of every bar: are two notes below G3 a semitone or a whole tone apart, both at velocity 35 or more?

I have not heard the renders. "Will sound" below is a prediction from the notes, the velocities and the register.

## Verdict

**Prelude.** The prelude is the boldest idea in the cycle so far, and the written core is sound. I checked every half-bar join of the climb (H2–H98; the rest are Bach's own bars and close): every voice moves by step or common tone, except chord re-voicings and the planned bass leaps. The risk is in the performance layer. At the climax it turns idiomatic dissonances into loud low-register clusters, and one pedalling rule smears the climax's resolution.

**Fugue.** The fugue is clean at every onset and has a good subject. Its form, however, is one 3½–4-bar module played eight times. The climax and the final cadence are smaller than the music before them. Sam's "preludes liked more than fugues" is likely to repeat here unless the ladder is made audible.

## Ranked issues (both movements)

| # | Mvt | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|---|
| 1 | Prelude | 34–37, esp. 36 | The layering turns V7♭9 and vii°7/V over the D♯ pedal into loud semitone clusters in octaves 2–3. The pedal rule also sustains the diminished seventh's E♯ through its own resolution. | **High** | Fix the hold rule; clip tenor and figure layers below D♯3 during H68–H73 |
| 2 | Fugue | 7–35 | Eight look-alike rungs, one every ≈9 s. The shrinking entry distance is inaudible until R2. Four of the eight joins use the same sixteenth sequence. | **High** | Group the ladder into three flights; replace Episode C with a new 2–3-bar episode; terrace the dynamics |
| 3 | Fugue | 32–35 | The R1 "climax" is lower, shorter and quieter than R2. The run-up falls, and R1 starts on a IV sonority. | **High** | R1 leader up an octave; Episode G rising; +6 velocity |
| 4 | Fugue | 41 | The final dominant lasts one eighth; B-A-C-H flashes past in eighths. | Medium | Same two bars, B-A-C-H in quarters over C7–F–F♯(V/V)–G–C |
| 5 | Fugue | 16.3½ (12.4) | The R6 follower enters on E4, a tone above the leader's sustained D4, and leaps away. | Medium | Omit R6's upbeat |
| 6 | Prelude | 5–7 | The Royal Theme sits on weak sixteenths while the Shepard fade blurs its signature drop. | Medium | Royal Theme as a held cantus in half notes; start the fade at H15 |
| 7 | Fugue | 1 | Bach's subject is quoted without Bach's rhythm. | Medium-low | Start it at beat 2 in its real rhythm; nothing else moves |
| 8 | Fugue | 21, 28 | Parallel ninths in the sixteenth turns of R5 and R3; F5/E3 at 21.4½. | Low | One note at 21.4½ |
| 9 | Prelude | 8–17 | Five keys in ten bars with the same pivot gesture. | Watch | Only if Sam hears sameness: hold one arrival |

---

## Prelude I: *per omnes tonos*

### Must not be touched

- **The frame.** Bars 1–4 and 50–53 are identical in the performance score. The b-minor Neapolitan at bar 47 sets BWV 846's own bar-1 notes (`E3 | C4 | G4 C5 E5`) over the wrong bass, so home is glimpsed and withdrawn. It is the best single musical idea in the pair.
- **The lament, H35–H42 (bars 18–21).** The bass falls E♭3 B♭2 A2 A♭2 G2 G♭2 F2 F♭2 under the falling figure, then F♭ lands as a subito E major. The voice-leading is exemplary: the only rising voice is E♭→F♭.

### P1. Bars 34–37: the pedal climax produces collisions in performance (High)

**What is written.** The bass D♯2 is tied for six half bars, and the harmonies above it are:
- H70 `C#4 | F##4 A#4 E5` (V7♭9);
- H71 `C##4 | G#4 B4 E#5` (vii°7/V);
- H72 `D#4 | G#4 B4 D#5` (i6/4).

In the written core these are wide intervals: D♯2 against C𝄪4 is a compound seventh. That is Bach's own pedal practice.

**What the performance score sounds.** σ = 13.5 puts every role into about five octaves. Over 36.1¼–36.2¾ the sounding notes include:
- D3 (tenor layer, v78) against E♭3 (bass layer, v83);
- D2 (v49) against E♭2 (v80);
- D4 (v83) against E♭4 (v58).

At 35.3–4 there are C♯2/E♭2 and E♭3/E3 at about v74. Scan (b) finds loud low seconds only in bars 33–37. Bar 36 is the worst: 15 of its 16 sixteenths. These are the collisions that sound like mistakes in Sam's feedback, and they fall on the loudest bars of the piece (velocity 90–98).

**A pedalling bug makes it worse.** `pedal_figure()` holds a figure note across the half-bar line when the bass is tied and `pcs[k] <= pcs[h]`. H72's set {D♯, G♯, B} is a subset of H71's {D♯, C𝄪, E♯, G♯, B}. So the diminished seventh's E♯, struck at 36.2¾, is held to 37.1 at v89 in octave 4, with layers in octaves 3, 5 and 6. Meanwhile D♯4/D♯5 (v85–93) resolve beneath it. The six-four's resolution is therefore smeared by its own appoggiatura. I checked every tied-bass half bar (H52–53, H68–73, H107–114); this is the only place where the subset rule holds a note that does not belong to the new chord.

**Fix (orchestration only; no written pitch changes).**
- (a) In `pedal_figure`, extend a held note into half bar *k* only while `e['p'] % 12 in pcs[k]`.
- (b) For H68–H73, skip tenor and figure layers below D♯3 (MIDI 51). Octaves 1–2 then belong to the D♯ pedal alone, which is also the BWV 846 image: a bare pedal under moving harmony.
- Re-run a low-seconds scan. Target: nothing above velocity 50.

### P2. Bars 5–7: the Royal Theme is written but will not be heard (Medium)

**Where the theme is.** The top notes C5 E♭5 G5 A♭5 B4 C5 (H9–H14) are the 3rd and 6th sixteenths of each half bar, the weak positions of the figure, with +7 velocity.

**What blurs it.** Over the same bars, `SHEPARD_MIX` rises from 0 to 0.5 (H9→H13). By H13 the theme's fingerprint, the diminished-seventh drop A♭5→B4, sounds in several octaves at once: B5 is present too, so the drop becomes ambiguous. "Allusions must be audible" is in the brief.

**Fix.**
- Sound the six notes as a held cantus on the Cantus staff, which is empty until bar 49. Use half notes, the theme's own values in the Musical Offering, about +12 over the figure, and do not layer them.
- Start the fade at the D♭ pivot instead of H9, e.g. `SHEPARD_MIX = [(1,0),(14,0),(15,.25),(17,.6),(19,1), …]`.
- Side benefit: the cantus is then heard once early, so its entry at 49.4 becomes a reprise rather than a new element in the last 8 bars.

### P3. Bars 8–17: the pivot formula (watch; do not fix blind)

**The risk.** Five keys pass in ten bars (D♭, c♯, D, d, E♭) at a near-constant two-bar pace, and every key change uses the same lift by step into the new I6. The variety listed in the NOTES is real but local: figure direction, the tenor suspension at 13.1. A listener who has caught the pivot at bar 8 can predict bars 9–17.

**Cheapest relief, if Sam reports sameness.** Hold one arrival. For example, let D major's I at 13.1 occupy the whole bar before d minor turns: the H26 cell becomes another D-major cell, with the tonic turning minor at 14.1.

### P4. Bars 53.2 and 50–57: minor points on the cantus (Low)

- **The F6 at 53.2.** It is a quarter-note passing tone of the augmented subject, sounding over pure C major while the figure's E5 is pedalled: a minor ninth held for a beat. It cannot be changed without breaking the exact augmentation.
- **Cantus velocity.** At +20 in octave 6 the cantus is the most exposed sound of the ending. Try +12 before deciding.

---

## Fugue I: *Scala strettarum*

### Must not be touched

- **The subject.** The upbeat fourth, dotted C, leap to a quarter-note G5, sixteenth cascade and rebound make a true Allegro gesture with an unmistakable downbeat. It carries the whole piece.
- **The coda, bars 36–40.** Bach's subject in his own rhythm (as his answer, 36.1½) sounds over our subject augmented in the bass (36.4). The device is learned and also audible: a slow bass under a famous tune. Keep it, together with the exposition's conceit that Bach's subject is our countersubject.

### F1. Bars 7–35: the ladder is one module heard eight times (High)

**The regularity.**
- **Spacing.** The leader entries fall at 7.4½, 11.4½, 15.4½, 19.4½, 23.2½, 26.4½, 30.2½ and 33.4½: a new key every 4, then every 3½ bars (about 9 s).
- **Content.** Each module is two complete statements, a 1–1½-bar sequence and a cadence.
- **Subject count.** The subject is heard complete 20 times in 97 s.

**The texture never changes.**
- Two voices run in continuous eighths and sixteenths throughout.
- Quarter notes occur only in the subject's own G and in the coda.
- Sustained dissonance is all but absent: the critic finds one suspension in 42 bars.

**The premise is below hearing.** The difference between 7, 6 and 5 eighths of entry distance cannot be heard; until R2 the listener simply hears "the subject again, in a new key".

**The joins repeat.** Four of the eight joins are the same "fall – rebound – drop" sixteenth sequence:
- the link at bar 7;
- Episode B, 14.4–15.4;
- Episode C, 18.3½–19.4 (B inverted);
- Episode F, 29.2–30.2 (B transposed).

**Fix.** Keep all eight distances, but make the ladder audible as three flights: R8–R6 (a, e, G), R5–R3 (d, F, C) and R2–R1 (G, C).
- **A real middle.** Replace Episode C with a 2–3-bar episode of a texture the piece lacks. Two options:
  - a chain of 7–6 suspensions in quarter notes in the treble, over the bass's tail-turn;
  - the countersubject's head (C D E F G) in close imitation over a falling bass.

  End it on a real half cadence in d (an A-major chord), so that R5 begins a second flight. The fugue is at the short end of the brief, so the extra bars are welcome.
- **Terraced dynamics.** Set roughly +0 / +6 / +12 by flight, with R1 at +18, instead of `int((bar-7)*0.4)`, which gives R1 only 3–4 units more than R2.

### F2. Bars 32–35: the climax is smaller than what precedes it (High)

**The comparison with R2.** R2 reaches D6 (31.1, 32.2). Episode G then descends E5→B4 (32.3½–33.4) while the bass bounces G2/G3. R1 enters with the leader on G4 and the follower on F4, a second apart in the middle of the keyboard (C5–G5 over F3–F4). Its first sonority is C over F (IV), and the dynamics add only +3.

**The stretto itself is inaudible.** At one eighth, with the follower's upbeat on the downbeat, the stretto is heard as one busy two-part texture in contrary motion. The climax must be carried by register and harmony, and at present both point downward.

**Fix.**
- **(a) Leader up an octave.** Write R1's leader an octave higher (`G5:2 C6:3 D6:1 E6:2 C6:2 G6:4 …`, and `C6:2 R:2` at 558). Every interval simply compounds, so there are no new parallels or dissonances. The voices start a ninth apart, the mirror's "scissors" open audibly, and R1 becomes the highest point of the piece (G6).
- **(b) Reverse Episode G.** Step the dotted figure up, not down, over the G pedal, so the run-up rises into the G5 upbeat. Add a bar of pedal if it needs room.
- **(c) Dynamics.** Add +6 velocity on 34–35.

### F3. Bar 41: the final cadence passes before it is heard (Medium)

**What is written.**
- Upper: `F5 G5 C6 B♭5 A5 C6 B5 | C6`.
- Lower: `D3 B2 E3 G3 F3 A2 G2 | C2`.

**Why it fails.** The dominant lasts one eighth (G2/B5 at 41.4½), preceded by an A-minor chord. The result is F–a–G–C in eighths, and B-A-C-H goes by as eighths in octave 6. After 40 bars of eighth-note motion, the ending needs one broad gesture.

**Fix (same two bars).**
- Bar 41: upper `F5:2 G5:2 C6:4 Bb5:4 A5:4`; lower `D3:2 B2:2 E3:4 C3:4 F2:4`.
- Bar 42: upper `C6:4 B5:4 C6:8`; lower `F#2:4 G2:4 C2:8`.

B-A-C-H now sounds in quarters over C7 – F – (D7)/F♯ – G – C. The seventh B♭ falls to A; C over F♯ implies V/V; F♯→G and C→B both resolve. The existing ritardando, which starts at 162 quarters, covers it. I checked it by hand: no parallels, and every dissonance resolves.

### F4. 16.3½ (and 12.4): an entry that sounds like a wrong note (Medium)

**R6.** The leader (bass) holds D4 on 16.3, the subject's accent. The follower's upbeat E4 enters at 16.3½, a whole tone above it in the same octave, and leaps on to A4 before anything resolves. The result is an eighth-long, unprepared, unresolved second at the exact moment the ear is looking for the new voice. In two-part writing this reads as a slip.

**R7.** At 12.4 the follower's B3 meets the leader's A3, and at 12.4½ its E4 meets F♯3. These are only sixteenths.

**Fix.** At R6, omit the follower's upbeat: `E4:2` → `R:2` at 250, and declare the entry from 252. The treble already rests on 16.3, so this only lengthens the rest to a beat, which also marks the entry. Fugue III uses the same remedy for its mirror entries. Leave R7.

### F5. Bar 1: the joke lacks Bach's fingerprint (Medium-low)

**What is written.** The bass plays `C3 D3 E3 F3 G3 F3 E3` in plain eighths from 1.1½.

**Why it fails.** BWV 846's subject is recognised by its rhythm, the dotted F and the 32nd-note G–F snap, more than by a C-major scale. In even eighths, low in the bass, it is a scale. The NOTES explain that Bach's rhythm cannot stand at his own metric position, because his A would fall under our upbeat as a seventh.

**Fix.** Start one eighth later, in Bach's rhythm. Lower voice, bar 1: `R:4 C3:2 D3:2 E3:2 F3:3 G3:0.5 F3:0.5 E3:2` (16 sixteenths). E3 then lands at 1.4½ under our G4 upbeat exactly as now, and A3 falls on 2.1 exactly as now, so nothing after bar 1 changes. Since nothing precedes the quote, no listener can tell it starts on beat 2 rather than 1½.

### F6. Bars 21 and 28: sixteenth-level rubs in R5 and R3 (Low)

**The rubs.**
- 21.2½ → 2¾: D5/C4 then C5/B♭3, parallel ninths with both notes attacked together.
- 21.4½: F5/E3, a minor ninth with both notes attacked together.
- 28.2¼ → 2½: C5/B3 then D5/C4, ninths again.

They lie inside subject statements and pass quickly at ♩ = 104. In two voices, however, parallel ninths sound smeared.

**Fix.** The F5 at 21.4½ belongs to free counterpoint (the segment at 334). Begin that segment with `A5:2`, repeating the subject's last note; A5/E3 is a fifth. Leave the rest.

---

## Checked and found sound

- **Fugue I.**
  - **Parallels.** None, at any onset at sixteenth resolution.
  - **Long dissonances.** Every dissonance of an eighth or longer is one of three things: a passing fourth, a chord seventh, or a 9–8 at a stretto's accent (20.3½, 24.3½, 34.3½). The one exception is F4 above.
- **Prelude I.**
  - **Written core.** No awkward joins in the core.
  - **Royal-Theme drop.** The A♭5→B4 drop at H12–H13 is deliberate.
  - **Pivots.** The pivot cells resolve their sevenths: V7→i at H44/45, H17/18 and H24/25 (the 4–3).

**Tool note.** `critic.py` cannot assess `prelude.json` meaningfully: 47 octave-layered voices produce thousands of "doublings" by design. Scan (b) above is the useful check for that file, and it would be worth adding to `tools/`.
