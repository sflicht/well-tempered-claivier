# Pair III in C-sharp major: second review (as built on 27 October)

**Scope.** I reviewed these files:
- `prelude.py`, which builds `prelude.json` (the second-draft prelude with four fixes);
- `fugue.py`, which builds `fugue.json`;
- `NOTES.md`.

**Method.** I read every bar, ran `tools/critic.py` and `tools/reduce.py`, and wrote two scratch scans:
- every simultaneous attack forming a 2nd, 7th or 9th;
- a per-beat count of how many beats sound only the pitch classes of a C♯ or G♯ triad (or G♯7).

I have not heard the renders.

## Verdict

**Prelude.** Keep it almost untouched. Sam liked this texture, and the four fixes in NOTES are correct. One note would improve the approach to the return.

**Fugue.** It is a well-made gigue:
- a characterful subject;
- clean counterpoint (0 parallels, 0 unresolved dissonances);
- a real binary form;
- a proven rectus/inversus coda.

It is also the most harmonically static fugue of the three pairs, which is Sam's complaint word for word. Its two showpieces, the reflection and the BWV 848 graft, sit on tonic harmony, where the ear cannot tell them from ordinary stamping. The fixes below cost few notes and use the piece's own material.

## Ranked issues (both movements)

| # | Mvt | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|---|
| 1 | Fugue | whole; worst 15–29 and 37–43 | Harmonic stasis: at least half the beats are bare C♯ or G♯ triads. Part 2 is back on the tonic at bar 23, its midpoint. | **High** | (a) Bass of 21–22 in the A♯-minor real mirror; (b) bar 9's bass under bar 42; (c) dotted ♩ = 96 |
| 2 | Fugue | 21–26 | Thin, low restart: one to three voices for six bars, all below C4 until bar 25, keys G♯ – C♯ – G♯ | Medium | Mostly cured by 1(a); optionally a few high bells above the lone bass |
| 3 | Prelude | 15–16 | The return is prepared by two bars of a bare G♯ triad with no seventh | Medium | One note: lower inner layer, bar 16, D♯3 → F♯3 |
| 4 | Fugue | 39–41 | The reflection is unarticulated: four equal voices on I6/I/viiø7, entered straight from V | Medium-low | Voice it (alto and tenor +8, CS pair −4) and add a short breath into 40.1 |
| 5 | Prelude | all | The deep bell sits mostly in octave 1 (E♯1/F♯1/G♯1): pitch and inversion are hard to hear | Low | Only if the render rumbles: a soft upper-octave doubling |
| 6 | Fugue | 45, 30–31 | The final bass lands on C♯3, not C♯2; Episode\* repeats Episode 1's plan mechanically | Low | Last bass note `C#2:6`; optional variation in bar 31 |

---

## Prelude III: "Glass bells"

### Must not be touched

- **The texture.** There are nine attacks per bar in the fixed rhythm 0 2 4 6 10 14 16 18 20, handed among four registers, with the silences part of the phrase. Do not add attacks or pedal the silences away.
- **The arc.** The top strand climbs to A♯6 (bar 18) and then descends by step to the final C♯5. The minor iv (A♮, bar 19) is the hush. Both are the best things in the piece.

### P1. Bars 15–16: the return is prepared by a bare triad (Medium)

**What is written.** Bar 14 is V/V; bar 15 is G♯, tonicised; bar 16 is G♯ again.
- Melody: `G#4 D#5 D#5 B#5`.
- Upper inner layer: `B#3 D#4 G#3`.
- Lower inner layer: `D#3 D#3`.
- Bass: G♯1.

**Why it fails.** That is G♯ major without a seventh, with two repeated D♯s in one bar: 7.5 s with no harmonic pull. Bar 16 is where G♯ must stop being a key and become a dominant again. Nothing in the notes says so, so bar 17 will sound like more of the same rather than a return.

**Fix (one note).** In the lower inner layer, bar 16, change the second bell from D♯3 to F♯3: `R:4 D#3:5 R:7 F#3:5 R:3`. The seventh resolves inside the same layer to E♯3, the first lower bell of bar 17. It sits a tone below the upper layer's G♯3 at sixteenth 18, which is an ordinary close spacing for a V7. It also removes one of the bar's two repeated notes.

### P2. The deep bell (Low)

**What is written.** The bass in bars 3–16 is A♯1 E♯1 F♯1 E♯1 F♯1 G♯1 E♯1 E♯1 A♯1 F♯1 F♯1 D♯1 G♯1 G♯1, and the lowest note, D♯1 (bar 14), falls inside the loudest pair of bars (13–14).

**Why it may fail.** In octave 1 on a sampled piano, the semitone E♯1–F♯1 is hard to hear. So is the difference between I6 (E♯1, bar 6) and IV (F♯1, bars 5 and 7), so the bass stops being heard as a line.

**Fix, only if the render rumbles.** Keep the deep bell: it is part of what Sam liked. Add a soft upper-octave doubling (the bass at +12, about half velocity). That restores pitch definition without lightening the sound.

---

## Fugue III: *Giga a 4, rectus et inversus*

### Must not be touched

- **The subject.** Four stamps up the triad, the silent hop, the octave drop with its flick, and the 1–7–1 close make a real dance with comic timing. It is also designed for inversion: I and viiø7 map onto themselves.
- **Bars 12–14.** The episode's circle of fifths turns E♯7 → F♯ (deceptive) into the A♯-minor entry. It is the one place in Part 1 where the harmony surprises.
- **Bars 32–36.** The rectus/real-mirror stretto moves F♯ → D♯m, then the G♯ pedal arrives with the hop passed from soprano to tenor. It is the harmonically richest stretch, and the model for the fixes below.

### F1. Harmonic stasis: the piece lives on C♯ and G♯ (High)

**The beat count.** I counted the beats whose sounding pitch classes belong only to a C♯ triad, a G♯ triad or G♯7. That strict count gives 92 of 178 beats (52%). If passing notes are allowed, it is about three quarters.

**The key map.**

| Bars | Key |
|---|---|
| 1–12 | C♯ |
| 13–14 | A♯m |
| 15–22 | G♯ |
| 23–29 | C♯/G♯, alternating every two bars |
| 31–34 | F♯ → D♯m |
| 35–36 | G♯ pedal |
| 37–45 | C♯ |

**Why it happens.** The subject and the countersubject both arpeggiate the tonic chord. Unless a free bass reharmonises an entry, its bar is a tonic or dominant bar. The few entries that are reharmonised are exactly the passages that will sound best:
- bar 9: vi – iii6/4 – I – I6;
- bar 13: over VI;
- bar 27: I6 – vi – IV;
- bar 32: over D♯3.

The longest uninterrupted C♯/G♯ stretch is 15–29, about 40 s. Part 2 is back on the tonic at bar 23, its midpoint.

**Fixes, cheapest first.**

**(a) Open Part 2 in A♯ minor.** Bars 21–22 are the bass alone. Replace its G♯ inversus with the real mirror, the A♯-minor reading `INV_D` that the piece already uses at 37–39 and 42–44, at pitch:

```
put('B', at(21), nopick(INV_D))
# = E#3:4 E#3:2 C#3:4 C#3:2 A#2:4 R:2 A#3:4 G#3:1 F#3:1 | E#3:2 D#3:2 C#3:2 B#2:4 C#3:2 E#3:4 F#3:2 E#3:4
```

- **The move.** Part 1's G♯ cadence then turns to vi, the same deceptive relationship the piece uses at bars 12–13.
- **The restart.** The lone bass sounds like a new situation rather than a repeat of the key just heard.
- **A preview.** The listener hears the stretto partner of bars 32, 37 and 42 before it is needed.
- **The join.** The line ends on E♯3, which is the first note of the bass's CS\* at 23.1 (I6), so the join is a common tone.

No other voice changes; update the entry label.

**(b) Bar 42: give the last rectus entry a bass.** At present the soprano stamps the subject over a bass that rests until the mirror entry (42.4). Give the bass bar 9's own reharmonisation, `A#2:6 B#2:6 C#3:6`, before that entry.
- **The harmony.** vi – iii6/4 (passing) – I sounds under the stamps.
- **The check.** I checked it against soprano, alto and tenor: consonant, with the six-four passing as in bar 9.
- **One side effect.** Bass C♯3 → E♯3 against the alto's C♯5 → E♯4 makes octaves by contrary motion into 42.4. If that bothers you, move the alto's 42.4 E♯4 down to C♯4; it continues smoothly to E♯4 in bar 43.

**(c) Tempo.** Dotted ♩ = 88 is a walking gigue. At 96 (`'bpm': 144`, with the `tempo_map` scaled to match) the I/V blocks pass at dance speed and the stamps get their lift. The NOTES' reason for 88, keeping the piece over two minutes, is not a musical reason. At 96 the fugue still lasts about 1:55, ritardando included.

### F2. Bars 21–26: the restart is long, thin and low (Medium)

**What happens.** After the tutti stamps of bar 20, the texture drops to one voice (bars 21–22), then two (23–24), then three (25–26). Until bar 25 everything lies between E♯2 and C♯4. That is 16 s of rebuilding in the middle of a two-minute piece.

**Context.** The gigue form justifies it: Part 2 begins with the inverted subject alone. The cost is energy: this is where attention will sag.

**Fix.** Fix 1(a) gives the restart a new key, which is most of the cure. If the render still sags, let the soprano ring two or three high bells over the lone bass in bars 21–22 (e.g. G♯5, C♯6). That keeps a top in the texture and nods to the prelude, which has no other link to the fugue.

### F3. Bars 39–41: the reflection is not presented as the summit (Medium-low)

**What happens.** Bar 39 is V7 – I – V, and bar 40 begins the reflection on I6. The harmony of the device is I6 – I – I6 – (open fifth) | I6 – viiø7 – I6 – I6, which to the ear is a tonic flourish. What *is* audible is the wedge: the alto stamps up while the tenor stamps the same figure down. At present all four voices are equal and mezzo (DYN +8), so the wedge is buried in the countersubject pair.

**Fix (performance data only).**
- **Voicing.** Raise the alto and tenor by +8 velocity in bars 40–41 and lower the CS/CS\* pair by 4.
- **A breath.** Add a short ritardando into 40.1 and return a tempo, e.g. `tempo_map` points at 232.5 (♩ = 132), 234 (♩ = 112, `'ramp'`), then 234 (♩ = 132). Scale these values if F1(c) changes the tempo.

The listener is then told that something arrives.

### F4. Ending and episodes (Low)

- **Bar 45.** The bass alternates `C#2 C#3 C#2 C#3` and lands on C♯3. The final chord (C♯3 G♯3 E♯5 C♯6) has no low root and a two-octave hole in the middle. Write the last bass note as `C#2:6`. The silent fourth beat is witty; keep it.
- **Bars 30–31.** Episode\* has the soprano stamp each pitch twice, sixteen times in a row (`G#5 G#5 E#5 E#5 D#5 D#5 F#5 F#5 | F#5 F#5 D#5 D#5 C##5 C##5 E#5 E#5`). It follows the same plan as Episode 1, a stamping head around the circle of fifths. Optionally, break bar 31 into the rectus run so that the second bar answers rather than repeats.

---

## Checked and found sound

- **Fugue III.**
  - **Counterpoint.** No parallels; every off-beat dissonance is passing or a chord seventh, as the NOTES' audit says.
  - **The BWV 848 graft (28–29).** It is a real voice. Recognition is uncertain at this speed, but it does no harm.
  - **The rectus/real-mirror strettos.** All three are clean.
- **Prelude III.** The four NOTES fixes are correct. FIX 2 (bar 20) and FIX 4 (bar 5) in particular repair genuine layer collisions.
