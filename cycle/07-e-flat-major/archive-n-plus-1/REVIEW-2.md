# Pair VII in E-flat major: second review (third edition, as built on 27 October)

**Scope.**
- `prelude.py` → `prelude.json`;
- `fugue.py` → `fugue.json`;
- `NOTES.md`.

**Method.**
- I read every bar, and ran `critic.py` and `reduce.py`.
- Scratch scans:
  - every simultaneous attack forming a 2nd, 7th or 9th;
  - a per-voice audibility summary (time sounding, register, shared attacks, doubling);
  - eighth-resolution grids of the joke, the stretto and the coda.

I have not heard the renders.

## Verdict

This is the most *dramatic* fugue of the set, and the one most likely to delight a listener:
- two choirs, left and right;
- a mirrored exposition;
- a quarrel about the key at shrinking distances;
- a reconciliation on A♭-over-B♭;
- a joke (French pomp against Italian chatter);
- an eight-voice stretto.

The plot is in the notes, not only in the titles, and the chorale links to the prelude are real.

What still won't land:

- **The ending.** The fugue ends in seven bars of half and whole notes. The chorale cantus in the tenor cannot stand out against equally slow voices, and the "festivo" piece sags into a slow homophonic close under a ritardando to ♩ = 48.
- **The joke's tempo.** It is staged by bar-by-bar tempo jumps of ±12%, which on a piano render will sound like an unsteady performance.
- **The stretto à 8.** From 38.1 every entry is at the A♭ or E♭ level, in successive octaves. It will be heard as a shimmering wash of IV and I fanfares rather than as tension building towards the dominant.

The prelude is a charming chorale prelude with the cantus well voiced (chorale ≈ velocity 86, obbligato ≈ 66). Its obbligato rhythm is unbroken for 37 bars.

## Ranked issues (both movements)

| # | Mvt | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|---|
| 1 | Fugue | 43–49 | The coda is all half and whole notes. The tenor's chorale (E♭3 G3 B♭3 … C4 B♭3) has no moving voice to stand out against, and the festive fugue ends in a slow block chorale | **High** | Soprano I in the subject's eighth-note figure over 44–46; Coro I tenor +10 |
| 2 | Fugue | 31–36 | The joke's tempo map jumps 76 / 86 / 76 / 86 / 76 / 82, bar by bar | Medium | Steady ♩ = 80, or ±4% at most; the notes already carry the contrast |
| 3 | Fugue | 37–42 | From 38.1, all six entries outline A♭ (Coro I) or E♭ (Coro II) triads, each the same arpeggio in three octaves | Medium | Move the last two entries (B1 40.1, S2 40.3) towards the dominant; test with the finder |
| 4 | Prelude | 5–41 | The obbligato's cell (eighth + two sixteenths + two eighths) runs every half bar for 37 bars | Medium-low | One interlude or line with a different figure: line 6, "Halleluja" (30.3–32) |
| 5 | Fugue | all | The two choirs share registers (both sopranos E♭4/C4–B♭5; both basses B♭1–B♭3); they are told apart only by pan | Watch | Check a mono render; keep the wide pans |

---

## Prelude VII: chorale prelude on *Wachet auf*

### Must not be touched

- **The plan.** The chorale sits in the tenor in long notes, after BWV 645, and is voiced louder than the obbligato. The obbligato is made of the fugue subject in diminution, which previews the fugue without announcing it.
- **The close.** The last line is answered by its own mirror (A♭ E♭ A♭ G C B♭ C D E♭) over the subject and inversion in diminution in the bass (42.3–46). It is a lovely ending and plants Coro II's "plagal dialect".

### P1. Bars 5–41: the obbligato never changes step (Medium-low)

**What is written.** Every half bar from 5 to 41 is the head-rhythm cell, e.g. `Eb5:2 G5:1 Bb5:1 G5:2 Eb5:2`. The exceptions are the literal turns at 6, 24 and 35, and the full-speed subject bar at 19. Stepwise motion is 29%: it is arpeggiated figuration, as the NOTES admit.

**Why it fails.** For 2 min 24 s at ♩ = 80, the ear will settle into the pattern by line 2 and stop listening to the obbligato.

**Fix.** Change the figure for one line. Line 6, "Halleluja" (30.3–32), suits it best: the obbligato runs the subject's second bar in sixteenths, the turn-and-run `C D C B♭ D F E♭ D` shape, transposed to the harmony. Or it holds a long note against the chorale, the only place the obbligato breathes. Either way, the return of the cell at line 7 becomes an event.

---

## Fugue VII (a 8): *Fuga a due cori*

### Must not be touched

- **The quarrel and the reconciliation (25–30).** Coro I insists on B♭ with A♮ and Coro II answers in A♭ with D♭, at a bar, then half a bar, then a beat. Then comes A♭ over B♭ (IV over V), resolving into B♭7 → E♭. The argument is audible in the pitches themselves, which is exactly the "voices change one another's course" the brief asks for.
- **The subject.** Its head is Nicolai's first line (E♭ G B♭ … C B♭) in canzona rhythm, and its inversion is a falling fanfare. Rectus and inversus are distinguishable by ear in any register. That is why the antiphony and the stretto can be followed at all.

### F1. Bars 43–49: the coda sags (High)

**What is written.**
- **Coro I tenor (the chorale's line 1, after BWV 645).** `Eb3` (half) `G3` (half) | `Bb3` … | `Bb3 Bb3` | `C4` (whole) | `Bb3` (whole) ….
- **Everything else is just as slow.** From 44.3 almost every voice moves in halves and wholes:
  - S1 E♭5 F5 E♭5 A♭5;
  - S2 G5 (whole) G5 F5;
  - A2 E♭5 B♭4 A♭4.
- **Tempo.** ♩ = 76 through 43–46, then a ritardando to 48 over 47–49.

**Why it fails.** A cantus firmus is heard *against* motion. Here it is the tenor of a slow chorale harmonisation, in the middle of seven voices with the same note values, so it will not emerge, even though it is the pair's most important link. And the fugue that began "Allegro festivo" ends with about 25 s of block chords: the "static, plodding" risk lands on the last impression.

**Fix.**
- **Motion.** Over 44–46, give Soprano I continuous motion made of the subject: the head-rhythm cell, or the countersubject's eighths, as the prelude's obbligato does. This turns the coda into a brief chorale-prelude texture, the prelude remembered. Keep Coro II's soft inverted echo at 48.3 as it is.
- **Voicing.** Coro I tenor +10 for 43–47.
- **Tempo.** Leave the ritardando where it is (from 47).

### F2. Bars 31–36: the joke's tempo will sound unsteady (Medium)

**What is written.** `tempo_map` has `[120,76] [124,86] [128,76] [132,86] [136,76] [140,82]`: an abrupt ±12% change at every barline for six bars.

**Why it fails.**
- **The notes already carry the contrast.** Coro I's dotted French-overture rhythm over the augmented subject against Coro II's whole subject in sixteenths (diminution) is the joke, and it is already in the notes.
- **The tempo jumps sound like the player.** On a sampled piano, the tempo lurching every 3 s will read as an unsteady player, not as two characters.

**Fix.** Steady ♩ = 80 through 31–36, or at most 78/82. If more contrast is wanted, use velocity: Coro I's pomp +6, Coro II's chatter −4 and lighter gates.

### F3. Bars 37–42: the stretto à 8 sounds as one chord-pair (Medium)

**The eight entries.**

| Entry | Voice | Form | Head |
|---|---|---|---|
| 37.1 | I Tenor | rectus | C3 E♭3 G3 A♭3 |
| 37.3 | II Tenor | inversus | F4 D4 B♭3 A♭3 |
| 38.1 | I Soprano | rectus | A♭4 C5 E♭5 F5 |
| 38.3 | II Alto | inversus | B♭4 G4 E♭4 D4 |
| 39.1 | I Alto | rectus | A♭3 C4 E♭4 F4 |
| 39.3 | II Bass | inversus | B♭3 G3 E♭3 D3 |
| 40.1 | I Bass | rectus | A♭2 C3 E♭3 F3 |
| 40.3 | II Soprano | inversus | B♭5 G5 E♭5 D5 |

**Why it fails.**
- **The levels.** From 38.1 on, Coro I's three entries are the same A♭ arpeggio in three octaves, and Coro II's three are the same E♭ arpeggio in three octaves.
- **The harmony.** The reduction shows 38–41 circling A♭, B♭ and Cm. It reaches the dominant only at 42 (Fm7 → B♭).
- **How it will be heard.** A bright, bell-like alternation of rising and falling fanfares: attractive, and the rectus/inversus antiphony *will* be heard. But it is a sound, not a build. The listener cannot tell the eighth entry from the sixth, because they say the same thing two octaves apart.

**Fix.** Let the last pair carry the harmony forward:
- the Coro I bass at 40.1 on the F level (F A♭ C D♭ C …, ii);
- the Coro II soprano at 40.3 on the B♭ level.

Bars 40–42 then move through ii and V into the cadence. The search penalised these levels, so re-run it (or `stretto_finder.py` on those two pairs) before writing.

### F4. One piano, two choirs (Watch)

**The registers.** Both sopranos (E♭4–B♭5 and C4–B♭5) and both basses (B♭1–B♭3) share registers, and the critic counts 21 cross-choir crossings.

**How the choirs are told apart.** In the stereo piano render, by pan: Coro I at 22–52, Coro II at 76–106. In the spatial render, by position. In mono, or on one speaker, the antiphonal sections still read, because the choirs alternate in time. The tutti (22–23, 37–42) fuse.

**Fix.** None needed. Keep the wide pans, and check the mono fold-down once.

### Note on the eight voices

**Coro II.** Its voices sound 40–52% of the time, which is right for antiphony.

**Real counterpoint.** Eight-voice counterpoint is real in 22–23 and 37–42. The antiphonal stretches (17–20, 25–29, 36) are deliberately four-voice blocks, Gabrieli-style.

**Sam's "harmony, not counterpoint" concern.** It applies here only to those blocks, and they are short and dramatised. Their key-asserting arpeggios account for the low stepwise figure (52.6%); revising them into scalar lines (NOTES' weak spot 12) would help, but is not urgent.
