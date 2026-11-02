# Pair IX in E major: second review (third edition, as built on 27 October)

**Scope.**
- `prelude.py` → `prelude.json` (36 bars, 12/8, about 2:45), with the cents written by `tune_prelude.py`, and `prelude-tempered.json`;
- `fugue.py` → `fugue.json` (50 bars, 2/2, ten voices, about 3:01);
- `NOTES.md`.

**Method.** I read every bar and ran `critic.py` and `reduce.py --per beat`, plus these scratch scans (not in the repository):
- **Grid views** at quarter and eighth resolution.
- **Entry salience.** For each statement: its rank from the top at its first note, the other voices attacking at that instant, and its velocity.
- **Rhythmic activity and homophony** per four bars.
- **Melodic interval sizes in cents** after tuning.
- **Every fix below was tested.** I applied it to a scratch copy of the source, rebuilt it (for the prelude, re-tuned it as well) and re-ran the critic. The drone prototype in P1 was built and tuned the same way. Nothing in the repository was changed.

I have not heard the renders. In the prelude, beats are dotted quarters (`b7.4` = fourth dotted quarter). In the fugue, beats are quarters, as in the NOTES.

## Verdict

**The prelude's sound will be lovely.** Every chord is pure and every common tone is literally held. But its idea will not reach the ear:
- **The drift cannot be heard.** Nothing in the piece stays fixed to measure it against, and the 21.5 c per cycle is hidden inside pure chord changes.
- **The snap will be heard, but wrongly.** After a breath, the coda returns 86 c higher, close enough to a semitone that a listener hears the familiar tune suddenly **a half step up**: a slightly flat "truck-driver" key change. Many listeners will take it for a deliberate modulation or a glitch, few for "the keyboard restores the pitch".
- **Four identical cycles.** Meanwhile the piece asks for four statements of one 8-bar progression, and in three of them nothing moves faster than the tune's lilt.

**The fugue** is honest stile antico, but it is the slowest and most chordal fugue in the cycle:
- nothing shorter than a quarter note;
- ♩ = 72 (half note = 36), slowing to 40;
- 61 % of onset moments are three or more voices attacking together.

Sam's "plodding" and "harmony, not counterpoint" will apply to it directly. Its devices fare as follows:
- **The ring** is spatial only.
- **The six or seven "heads" per tutti** are three-note half-note cells in inner voices.
- **The ancestor at two speeds** (b19) is heard at one, because Soprano II covers the normal-speed statement.
- **The treble cantus** starts under Soprano II.
- **"The ring empties"** consists of note-offs on a chord that has been decaying for seven seconds or more.

## Ranked issues (both movements)

| # | Mvt | Bars | Problem | Severity | Minimal fix (tested) |
|---|---|---|---|---|---|
| 1 | Prelude | 1–33 | Drift inaudible; the snap sounds like a flat half-step key change, not a correction | **High** | A fixed-pitch musette drone at each cycle's start (P1) |
| 2 | Fugue | all | Plods: quarters the fastest value, ♩ = 72 → 40, 61 % block attacks, 3:01 | **High** | ♩ = 92, tempo map scaled (≈ 2:22) |
| 3 | Fugue | 19–22, 39–41 | The ancestor at two speeds and the treble cantus are masked by Soprano II | **High** | Soprano II rests at b19–20 and b39–40 |
| 4 | Prelude | 1–8, 17–36 | Static: 4½ statements of one progression; 28 of 36 bars only the siciliano moves; cycle 4 is a slower literal repeat | Medium | Cycle 4 in the "pipes" texture, a tempo |
| 5 | Prelude | 7, 31 | The theme's cadence V7 has no leading tone and a doubled or tripled seventh | Medium | Alto `'G#4:12 B4:6 D#4:6'` |
| 6 | Fugue | 1–18, 19–25, 39–47 | Exposition 1 minute of white notes; "heads round the ring" are texture | Medium | Tempo (#2); describe honestly |
| 7 | Fugue | 48–50 | "The ring empties": note-offs on a held, decaying chord (≈ 15 s at ♩ 54 → 40) | Medium–low | Each pair re-strikes its note pp before leaving |
| 8 | Fugue | 45–47 | The "English false relation" is a Mixolydian ♭VII, 1½ bars from the last D♯ | Low | Relabel, or juxtapose D♯/D♮ |
| 9 | Prelude | 4→5 etc. | The comma lands in a 133 c "semitone" A→G♯ at every V7–I | Low | Observation |

---

## Prelude IX: Pastorale in just intonation

### Must not be touched

- **The tune, and its ties across the barlines** (G♯ across I→vi, C♯ and E across vi→ii7, A across ii7→V7). On a piano a held note cannot retune, so the ties make common-tone just intonation literally true. With pure thirds, the held chords should glow.
- **Cycle 2, "the pipes"** (alto in running eighths). It is the only cycle that flows: 90–100 % of eighth slots carry an attack.

### P1. The drift is not heard; the snap will be (High)

**What is written.**
- The tonic E sinks 21.51 c per cycle. Within each cycle it happens in steps hidden inside pure chord changes: vi→ii7 puts F♯ at 10/9, ii7→V7 puts B a comma low, V→I lands a comma flat.
- After four cycles it is −86.03 c. Bar 32 ends with a rest and a slowing to ♩ 58.
- Bar 33 begins the coda at ♩ 80, louder (+8 against cycle 4), in Bach–Lehman, **86 c higher**.

**Is the drift musically motivated?**
- Only as an idea. The music never modulates, so nothing in it makes the drift matter.
- Without a fixed reference, a listener without absolute pitch cannot hear a 21.5 c sink spread over 34 s. The cycles sound like one key throughout.
- The only audible product of the tuning is its sweetness (pure thirds, no beating), and that is real and worth having.
- But four identical harmonic cycles are justified here by a process nobody will hear.

**Will the snap sound intentional?**
- **Not as intended.** The listener's sense of the key has followed the drift. After the breath, the familiar tune (the coda is the head plus the same loop) comes back 0.86 of a semitone higher, louder and faster.
- This is the gesture of the "truck-driver" modulation, the last chorus up a half step, but 14 c short of a true semitone.
- The coda's Lehman major thirds are also 20 c wider than the pure thirds of the last 2½ minutes.
- **Probable readings**, most to least likely:
  - a deliberate key change up a half step, slightly sour;
  - a render glitch;
  - only rarely, "the keyboard restores the pitch".

**Fix: give the ear a yardstick (tested).** A pastorale's natural yardstick is the musette drone.

Edits to `prelude.py`:
- `VOICES = ['Soprano', 'Alto', 'Tenor', 'Bass', 'Drone']`.
- The coda loop: `**{v: CODA[v][k] for v in VOICES if v != 'Drone'}`.
- After the bars: `for b in (1, 9, 17, 25, 33): B.put('Drone', b, ['E2:24'])`.
- The voices list: add `('Drone', 'Dr', 'bass', 48)`.

Edits to `tune_prelude.py`, in `tune()`:
- Before `if t >= t_just:`, add `if v['name'] == 'Drone': e['cents'] = round(LEHMAN[pc], 3); continue`.
- Exclude the drone from `purity()`. Its mistuning is now the point.

Result of the prototype build:
- The drone E2 stays at −1.96 c throughout.
- The bass E3 at the start of cycles 2, 3 and 4 is at −23.46, −44.97 and −66.47 c.
- At b33 the two agree again.
- On the drone's octave partial, the mismatch beats at about 2, 4 and 6 Hz in cycles 2, 3 and 4: a gentle wobble, then sour, then plainly out.
- The joke now has a plot: the shepherds' pipes sink away from the bagpipe, and the well-tempered keyboard puts them back together.
- The critic shows 0 parallels and 0 unresolved. The drone needs the sostenuto pedal: 2 % of onsets are beyond two hands.

The risk is real: cycle 4 will sound out of tune, deliberately. If that is too much, strike the drone only at b1, b25 and b33. The reference is then weaker, but the da capo of b25 is heard against the opening's pitch.

### P2. Four identical cycles, three of them almost motionless (Medium)

**What is written.**
- One progression, I–vi–ii7–V7 | I–IV–I6/4 V7–I, is stated four times, plus its antecedent again in the coda.
- In cycles 1, 3 and 4 and in the coda (28 of 36 bars), nothing moves faster than the tune's quarter–eighth siciliano: only 44–46 % of eighth slots carry an attack.
- The alto holds dotted halves, the bass whole bars, and the tenor rocks in dotted quarters.
- Cycle 4 is cycle 1's notes again, at ♩ 74 instead of 84.

**Why it fails.** About 2:45 of unchanging harmony is exactly the "long harmonically static stretch" of Sam's feedback. Slowing the literal repeat makes it longer still.

**Fix (tested).**
- Make cycle 4 a da capo of cycle 2 (tune over the pipes) instead of cycle 1: `B.bar(f'{25 + k} cycle 4 (da capo)', Soprano=TUNE[k], Alto=A2[k], Tenor=T2[k], Bass=BASS[k])`.
- The harmony, and therefore the drift (−21.51 c), are unchanged. Critic: 0 parallels, 0 beat parallels, 0 unresolved.
- Take cycle 4 a tempo: `[138, 84], [144, 74, 'ramp'], [186, 74]` → `[138, 84], [144, 76, 'ramp'], [144, 84], [186, 84]`.
- The piece then ends with motion before the breath, and "same notes, lower" is still audible as cycle 2 against cycle 4.

### P3. b7 and b31: the cadential V7 has no leading tone (Medium)

**What is written.**
- Bar 7 (and its da capo, b31), second half, over the B2 pedal:
  - dotted beat 3: S F♯5, A A4, T A3;
  - dotted beat 4: S A5, A A4, T F♯3.
- There is no D♯ anywhere in the dominant of the theme's only perfect cadence. The seventh A is doubled on both beats.
- The alto's A4 then leaps to E4. The critic counts these four of its six bad doublings.

**Why it fails.** The cadence of every cycle 1 and 4 sounds hollow and open-fifth-like. That might pass as pastoral, but it also weakens the V→I that carries the comma.

**Fix (tested).** `A1[6]`: `'G#4:12 A4:12'` → `'G#4:12 B4:6 D#4:6'`. The D♯4 resolves to E4 at b8.
- Bad doublings fall from 6 to 2. The remaining two are the held E of ii7, which the pump needs.
- 0 parallels.
- Do not use `'G#4:12 F#4:6 D#4:6'`: it makes octaves with the tune (G♯5→F♯5).

### P4. Where the comma goes (Low, observation)

- Common-tone tuning keeps the prepared seventh A at the pitch it had as the third of ii7.
- So it falls to the new tonic's G♯ by a **133 c semitone**, 33 c wider than equal temperament: the tenor A3→G♯3 at b4→5, 12→13, 20→21 and 28→29, and the tune's A5→G♯5 at b4.
- It is the audible trace of the pump, a slightly sour leading step once per cycle. Keep it; it is honest. But the NOTES should mention it.

---

## Fugue IX à 10: Ricercar a 10 in circulo

### Must not be touched

- **b26, the general pause**, after the first tutti's cadence. *Spem*'s silence is a real event, and the pp antiphony after it is a true contrast.
- **b47–48, Soprano I's last head.** E5 A5 G♯5, with A5 held as the final 4–3 over the E-major chord. It is the top voice and the voice that began alone: the circle closing is audible.
- **The BWV 878 augmentation in the bass** (b19–25, E2 F♯2 A2 G♯2 F♯2 E2). As the lowest voice it is heard as a slow bass line under the first tutti.

### F1. It will plod (High)

**What is written.**
- No value shorter than a quarter. Of 440 notes, 58 % are half notes, 26 % whole notes or longer, and 15 % quarters.
- ♩ = 72 (half note = 36), then 66 in the first tutti, 54 into the pause, 70, 64, then 54 → 40 at the end.
- Onset moments with three or more voices attacking together: 61 % overall, 80–83 % in b21–28 and 100 % in b33–36.
- The NOTES already observe that in the tuttis only 2–3 voices per bar have two or more attacks.

**Why it fails.** BWV 878, the model, has running quarter and eighth countersubjects and is rarely taken below half note = 44. Here the surface is half notes at half note ≈ 33–36 for three minutes. That is heard as a ten-part chorale harmonisation: Sam's "harmony, not counterpoint", and "plodding".

**Fix.**
- `'bpm': 72` → `92`.
- Scale the map by 1.28: `[[72, 84], [94, 84], [100, 69, 'ramp'], [100, 69], [104, 90], [148, 90], [152, 82, 'ramp'], [184, 82], [188, 69, 'ramp'], [200, 51, 'ramp']]`.
- Duration ≈ 2:22 instead of ≈ 3:01. The exposition then takes 47 s instead of 60.
- If more is wanted, give one voice per tutti a quarter-note line (Soprano II in b21–25 is the obvious candidate).

### F2. The ancestor at two speeds, and the treble cantus, are covered by Soprano II (High)

**What is written.**
- **b19.** Soprano I sings BWV 878's answer at normal speed (B4, C♯5, E5, D♯5, C♯5, B4, in wholes and halves). Soprano II's descant (E5 D♯5 E5 F♯5 G♯5, up to C♯6) is above it, so Soprano I is second from the top under nine voices.
- **b39.** Soprano I begins the treble cantus (E5 held 2 bars, then F♯5 A5 G♯5 F♯5 E5). Soprano II's B5 G♯5 A5 is above its first note.

**Why it fails.**
- The NOTES' "ancestor at two speeds at once" is heard at one speed, the bass.
- The cantus becomes audible only at b41, the F♯5. Without its E→F♯→A opening, BWV 878's subject is not recognisable.

**Fix (tested together; critic unchanged).**
- b19: `put('S2', 19, 1, 'E5:8 D#5:4 E5:4 F#5:8 G#5:8 C#6:24 B5:12 A5:4 G#5:8 B5:32')` → `put('S2', 19, 1, 'R:32 C#6:24 B5:12 A5:4 G#5:8 B5:32')`. Soprano I is now the top voice at b19 over the bass augmentation, and Soprano II's entry on C♯6 at b21 becomes the tutti's peak.
- b39: `put('S2', 39, 1, 'B5:8 G#5:8 A5:8 R:8 R:8 C#5:16 B4:8')` → `put('S2', 39, 1, 'R:40 C#5:16 B4:8')`. The cantus's E5 is the top note of the final tutti.
- Optional: re-strike the cantus's first note, which otherwise decays for 7 s: write the statement as `'E5:16 E5:16 F#5:16 A5:16 G#5:16 F#5:16 E5:16'`.

### F3. Ten voices: lines or texture? The ring, the heads (Medium; describe honestly)

**The exposition (b1–18).** Each Choir I entry is audible, because each comes in as the new lowest voice (B4, F♯4, C♯4, E3, B2). Soprano II enters as the new top (E5). Choir II's inner entries are third to fourth of five or six voices, in half notes: they will be heard as the texture thickening, not as entries: Alto II (C♯4, b13), Tenor II (F♯3, b15), Baritone II (B3, b17).

**The ring.**
- It is purely spatial. On the piano renders, the main deliverable, it is not there.
- In the binaural render it may work, but only for entries that are audible in the first place.

**The "heads round the ring" in the tuttis.**
- Each head is a three-note cell (rise a fourth, hold, step down) in half and whole notes.
- They enter as the 3rd–7th voice from the top, with 4–8 other voices attacking at the same instant: T1 19.1, B1 20.1, A2 21.3, T2 22.3, Bar2 23.1, A1 23.3, and seven more in b39–46.
- Free voices move in the same values, so the heads are indistinguishable from them.

**What is audible.** Soprano II's head on its "home" B at b43.1 (second voice) is the only one that may be heard.

**Verdict.** The outer voices are lines. The inner eight are a slow, well-voiced chorale texture. That suits stile antico, but the NOTES should not describe the heads, or the ring on a piano, as heard events.

### F4. b48–50: "the ring empties" is inaudible (Medium–low)

**What is written.**
- The final chord is complete at 48.1.
- After Soprano I's A5→G♯5 at 48.3, nothing is struck again. Voices release in pairs: A1/T1 at 49.3, B1/S2 at 50.1, A2/T2 at 50.3.
- This happens under a ritardando from ♩ 54 to 40, about 15 s.

**Why it fails.** A piano note held for ten seconds has nearly decayed. Releasing it is barely audible, so the device is a fading chord.

**Fix (tested; critic unchanged).** Make each departure audible: each pair re-strikes its note pp half a bar before it leaves. Then the farewell travels round the ring, audibly on the piano and spatially in the binaural render.

| Voice | Now | Change to |
|---|---|---|
| A1 | `B4:24` | `B4:16 B4:8` |
| T1 | `B3:24` | `B3:16 B3:8` |
| B1 | `B2:32` | `B2:24 B2:8` |
| S2 | `E5:40` | `E5:32 E5:8` |
| A2 | `E4:56` | `E4:48 E4:8` |
| T2 | `G#4:40` | `G#4:32 G#4:8` |
| S1 | `G#5:40` | `G#5:32 G#5:8` |
| Bar2 | `E3:56` | `E3:48 E3:8` |
| B2 | `E2:48` | `E2:40 E2:8` |

### F5. The "English false relation" (Low)

**What is written.** D♮ enters at 46.1 (Alto I D5, Tenor II D4; ♭VII – IV – I). The last D♯ is Soprano II's D5 at 44.3–44.4, six beats earlier.

**Assessment.** That is a Mixolydian plagal colour, not a Tallis false relation. A false relation needs D♯ and D♮ adjacent or simultaneous in different voices. Either relabel it, or let a D♯ sound in one voice on the beat before the D♮ chord, and check it with the critic. For example (untested), Tenor I's held E4 could step to D♯4 at 45.4, over Bass II's G♯2.
