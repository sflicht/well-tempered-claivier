# Pair V in D major: second review (third edition, as built on 27 October)

**Scope.**
- `prelude.py` → `prelude.json`;
- `fugue.py` → `fugue.json`;
- `NOTES.md`, and the first review `REVIEW.md`.

**Method.**
- I read every bar.
- Tools: `critic.py`, `reduce.py`, and `stretto_finder.py` (re-probing Stretto II).
- Scratch scans:
  - every simultaneous attack forming a 2nd, 7th or 9th;
  - a per-voice audibility summary (sounding time, register, shared attacks, doubling);
  - an eighth-resolution grid of the cascade and the summit.

I have not heard the renders.

## Verdict

The rebuild answers REVIEW.md:
- the octave strettos are gone;
- the key plan now travels: B minor, E minor, G, E minor, and the cascade F♯m–Bm–Em–A–D–G;
- the contrabass has its own line;
- the prelude carries a real top line.

The fugue's "trumpets and drums" character is clear and festive.

**What still won't land**, in order:
- **Stretto II.** The inversion enters one *sixteenth* off an eighth-note subdivision (7 sixteenths into the bar). Its drum tattoo then runs on the wrong sixteenths against the alto's, which will sound like an ensemble slip rather than *per arsin et thesin*.
- **The cascade's lower half.** The baritone, bass and contrabass entries go into a crowded A2–E4 band, where they blur.
- **Bach's ghost.** BWV 850's subject is buried in the baritone under the tenor's tattoo.

## Ranked issues (both movements)

| # | Mvt | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|---|
| 1 | Fugue | 32–34 | The inversion enters at 32.2¾. The tattoo's sixteenths land a sixteenth off the alto's, so it sounds like a slip | **High** | Enter at 32.2½ (`R:6`): finder cost 7 against 10 now, 0 errors |
| 2 | Fugue | 42–45 | The cascade's last three entries (Br E3, B A2, Cb inverted D3) blur. Br and B meet in unison at 43.3½ and cross at 43.4; low-register seconds at 43.3¾, 44.4¼, 45.3¾ | Medium-high | +8 on each cascade head bar; baritone rests in bar 44 |
| 3 | Fugue | 47 | The BWV 850 ghost's 32nd-note run (D3–G3) sits under the tenor's D4 tattoo: a rumble, not a quotation | Medium | Ghost +10, tenor −6 for bar 47 |
| 4 | Prelude | 24–28 | Five bars of V / I6/4 alternation over A, with both hands arpeggiating: the climb stalls | Medium | Cut bars 26–27, or give them one new chord |
| 5 | Fugue | 47–55 | Nine bars on D and A (×4 cantus over a 5-bar tonic pedal) | Low | Accept, or shorten the pedal by a bar |
| 6 | both | metadata | `'composer': 'Recomposed by Claudia / Sam'` | Low | `'Claude / Sam'` |

---

## Prelude V

### Must not be touched

- **The tattoo development (15–20).** The fugue's head cell (quarter + eighth + two sixteenths) passes between the hands over the fugue's Episode-1 progression. The pair link is audible here, not only on paper.
- **The return (33–38).** It runs over the fugue subject's head in the bass (`A2:4 D3:2 D3:1 D3:1 F#3:2 F#3:1 F#3:1 A3:4`), with the C♮ (36) and B♭ (37) colours. The reprise is varied and points to the fugue.

### P1. Bars 24–28: the climb stalls on the dominant (Medium)

**What is written.**

| Bar | Harmony |
|---|---|
| 24 | A7 over A1 |
| 25 | D/A – A7 |
| 26 | A7 |
| 27 | D/A, "climbing" |
| 28 | A7 at the top |

Both hands play sixteenth arpeggios throughout, before the deceptive Bm at 29.

**Why it fails.** That is about 11 s of I6/4–V7 alternation in the most generic texture of the piece (two hands of broken chords). It is the "harmonically static stretch" Sam names. The real events (the deceptive cadence, G♯°7, the E6 apex) come after it.

**Fix.** Cut bars 26 and 27. The joins work:
- the right hand at the end of 25 (`… A4 C#5 G5 E5`) leads into 28 (`E5 G5 C#6 G5`), E5 to E5;
- the left hand goes A7 → A7.

The climb still rises (G5 → E6), and the deceptive cadence arrives two bars sooner. The tempo map must shift by eight quarters.

**Alternative.** Keep the bars but make 27 a G♯°7 over the A pedal, previewing bar 30.

### P2. Bars 21–32: twelve bars of double arpeggios (Low)

**What happens.** The climb keeps v1's figures: both hands in sixteenth broken chords. The NOTES list the tritone count as the cost.

**Why it matters.** Even after the cut in P1 this is the least BWV 850-like stretch. It is acceptable as the prelude's "machine" passage, but don't extend it.

---

## Fugue V (a 6)

### Must not be touched

- **The subject.** `A4:4 D5:2 D5:1 D5:1 F#5:2 F#5:1 F#5:1 A5:4 …` is a trumpet call with a drum tattoo, recognisable in any voice, at any speed. That is what makes the cascade and the prolation possible at all.
- **The soprano's ×4 cantus over the summit (47–54).** The subject in whole and half notes on top (A5 → D6 D6 D6 → F♯6 F♯6 F♯6 → A6 …) is the most audible "device" in the six-voice fugues so far: a cantus firmus anyone can follow.

### F1. Bars 32–34: Stretto II enters a sixteenth off the grid (High)

**What is written.** `Br='R:7 ' + EM_INV5 + ' R:1 E3:4 C#4:4'`, where `EM_INV5 = 'E4:4 B3:2 B3:1 B3:1 G3:2 G3:1 G3:1 E3:4 …'`.

**Why it fails.**
- **Where it lands.** The head lands on the last sixteenth of beat 2. Its tattoo sixteenths (B3 B3, G3 G3) then fall on the second and fourth sixteenths of the beat, while the alto's rectus tattoo is on the beat.
- **What it sounds like.** With a subject whose whole identity is a metrical fanfare, a one-sixteenth displacement sounds like a player coming in early, not like a learned device.
- **What Bach does.** Bach's *per arsin et thesin* displaces by a beat or a half-beat.

**Fix.** `Br='R:6 ' + EM_INV5 + ' R:2 E3:4 C#4:4'`, and change the entry offset from 1.75 to 1.5. I re-ran `stretto_finder.py` on the E-minor subject against its inversion about B4 at the lower fifth:
- offset 6 (an eighth off the beat) costs **7**, with 0 parallels, 0 unresolved and 0 weak parallels;
- the current offset 7 costs 10.

Re-check S, T and Cb in 32–34 with the critic.

### F2. Bars 42–45: the cascade's lower half blurs (Medium-high)

**What is written.** Entries come one bar apart, a fifth lower each time: S (C♯5, 39), A (F♯4, 40), T (B3, 41), Br (E3, 42), B (A2, 43), Cb (inverted, D3, 44).

**What the upper half does.** The first three come into a texture with room above or below them, and their tattoo will be heard.

**What the lower half does.** The last three enter the same A2–E4 band in which the previous entry's tail is still falling:
- at 43 the baritone's tail (`E4 D4 C#4 B3 A3 F#3 …`) meets the bass's head (`A2 D3 D3 D3 F#3 F#3 F#3 A3`): a unison F♯3 at 43.3½ and a crossing at 43.4;
- at 44 the inverted contrabass (`D3 A2 A2 A2 F#2 …`) moves in sixteenths under the bass's tail;
- the critic's low-register seconds fall exactly there: 43.3¾, 44.4¼, 45.3¾.

The NOTES admit "cascade crossings".

**How it will be heard.** A clear descent through three voices, then a thickening rumble. The device's point, the trumpet call sinking into the depths, is lost exactly where it should arrive.

**Fix.**
- **Voicing.** Give each cascade entry +8 for its head bar: add a one-bar emphasis entry, or post-process velocities.
- **Make room.** Let the baritone rest through bar 44, after its statement ends at 43.4. Its free notes there (`D4:4 E4:4 A3:4 D4:4`) carry no theme. The contrabass's inverted entry then has the low register to itself, and the bass's tail is heard against it.

The Br/B overlap in bar 43 is between two subject statements, so it stays. The six-voice tutti still arrives at 45.

### F3. Bar 47: Bach's ghost is buried (Medium)

**What is written.**
- **Ghost.** The baritone plays BWV 850's subject: `D3:0.5 E3:0.5 F#3:0.5 G3:0.5 F#3:0.5 E3:0.5 F#3:0.5 D3:0.5 B3:3 B3:1 A3:3 G3:1 F#3:3 G3:1`.
- **Around it.**
  - the tenor's subject (`A3 D4 D4 D4 F#4 F#4 F#4 A4`), immediately above it;
  - the contrabass's quarters below it;
  - the alto's held F♯5/D5;
  - the soprano's A5.

**Why it fails.** The 32nd-note run in the baritone's octave, under a tenor tattoo on D4, will sound like a low flurry. BWV 850's subject is famous for its run and its dotted B.–A.–G; neither survives in the middle of the texture.

**Fix.** For bar 47 only, give the baritone +10 and the tenor −6 (performance data).

**Alternative.** Delay the tenor's subject by half a bar, so the run sounds alone under the held upper voices. That requires a re-check: `stretto_finder` approved the combination at offset 0 only.

### F4. Bars 47–55: the summit sits on D (Low)

**What is written.** 47 is D (Bm7 colour), 48 G/Bm, 49 D/F♯, 50 A for the whole bar, then 51–55 a tonic pedal.

**How it will be heard.** That is festive and earned, but about 20 s of D/A with a rallentando. The NOTES list bar 50 as a one-harmony bar.

**Fix (if Sam finds the end long).** Shorten the pedal by a bar: merge 52 and 53, keeping the B♭ colour.

### Note on the six voices

**Real lines.** Soprano, alto and tenor are real lines. The baritone carries thematic material at 10, 32, 42, 47 and 49. The contrabass is a genuine walking bass, the lowest voice whenever it sounds.

**The weak voice.** The **bass** voice is the weakest:
- it sounds only 44% of the time;
- 67% of its sounding time doubles another voice's pitch class;
- it rests through 28–38 and 47–49.

Episodes 3–4 and Stretto II are effectively five-voice. That is acceptable, but it is the voice to give a line if a line is ever added.

### Metadata

**The composer string.** Both `fugue.py` and `prelude.py` set `'composer': 'Recomposed by Claudia / Sam'`. Every other pair has "Claude / Sam". It will print on the PDFs.
