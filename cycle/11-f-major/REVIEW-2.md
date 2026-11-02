# Pair XI in F major: second review (third edition, as built on 27 October)

**Scope.**
- `prelude.py` → `prelude.json` (21 bars, 12/8, about 1:28);
- `fugue.py` → `fugue.json` (63 bars, 4/4, twelve voices, about 2:35);
- `NOTES.md`.

**Method.** I read every bar and ran `critic.py` and `reduce.py --per beat`, plus these scratch scans (not in the repository):
- **Grid views** down to sixteenths.
- **Entry salience.** For each statement: its rank from the top at its first note, other attacks at that instant, and velocity.
- **Struck semitones.** m2, M7 and m9 pairs attacked together.
- **Simultaneous chromatic pairs** (E♭ with E, A♭ with A, and so on).
- **Pitch-class saturation per sixteenth.** BWV 849, in five voices, has five or more pitch classes in 1.3 % of slices.
- **Every fix below was tested.** I applied it to a scratch copy of the source, rebuilt it and re-ran the critic. Nothing in the repository was changed.

I have not heard the renders. In the prelude, beats are dotted quarters.

## Verdict

**The liveliest and wittiest pair so far.**
- **The prelude** is a clean, motor two-part invention with a real surprise (the lone "C C" that lands in D♭).
- **The fugue** has the best concept in the group: Brandenburg 2, a natural-trumpet persona that has to sit out the minor keys, and a joke.

**What will not reach a listener on one piano:**
1. **The joke's punchline is smudged.** When the trumpet launches its F-major head against E major, the band has just stopped (a rest on beat 45.4), and a violin's G♯5–B5 sits above the trumpet. The "semitone off" clash is clear for only one beat.
2. **The twelve-voice stretto is a scale-saturated wash.** In b54–57 five to seven pitch classes sound in most sixteenths, and two of the countersubject diminutions put E♭ against three E naturals and A♭ against the bass's A. The four concertino heads, a beat apart on one triad, merge into one fanfare (the trumpet and violin even play F5 F5 in unison). What the ear will get is the walking bass, a high slow violin line and a shimmering F-major mass.
3. **The concerto contrast does not exist before b53.** The two middle "tuttis" have 3–5 voices sounding, as many as the solo episodes.
4. **After the climax the piece deflates.** It thins to 4 voices, under a ritardando from ♩ 100 to 52.

## Ranked issues (both movements)

| # | Mvt | Bars | Problem | Severity | Minimal fix (tested) |
|---|---|---|---|---|---|
| 1 | Fugue | 45–46 | The joke: the wrong-key head sounds over a rest and under Violino I.1's G♯5/B5; the clash is clear for only one beat | **High** | Hold the E chord through 45.4; Violino I.1's head an octave lower |
| 2 | Fugue | 54–56 | The tutti is a wash; E♭4 against E5/E5/E3 (54.4, last sixteenth) and A♭4 against the bass A2 (55.3, last sixteenth) | **High** | Remove two countersubject diminutions (Va1 54.3½, Vno 55.2½) |
| 3 | Fugue | 52.2 | Cello B♮2 struck against Viola 2's B♭3 | Medium | Va2 `'D4:4 R:4 C4:4 Bb3:4'` |
| 4 | Fugue | 23–28, 35–40 | The "tuttis" are 3–5 voices, the same as the solo episodes: the ripieno/concertino alternation is not heard | Medium | Fuller tuttis or leaner episodes; or describe it as an accumulation |
| 5 | Fugue | 58–63 | After the climax: 4 voices, then concertino only, under ♩ 100 → 52; the ripieno's last-chord entry lands in a ritardando | Medium | Keep the tempo to the end (≈ 2:33) |
| 6 | Fugue | 53 | The four concertino heads merge (Tr/Vno unison F5 F5, Ob/Vno octave C) | Low–medium | Accept as one fanfare; trumpet +8 |
| 7 | Prelude | 21 | The "fugue's first words" (C C F in sixteenths) are slowed to ♩ 56 by the final ritardando | Low–medium | Last bar a tempo |
| 8 | Prelude | 19–20 | The echo game is four beats of bare fifths and octaves | Low | Accept, or add thirds |

---

## Prelude XI: Invention à 2

### Must not be touched

- **The pair P/Q.** The triplet fanfare head with its running tail, over a countersubject in sixteenths, heard both ways round. It is real invertible two-part writing at Bach's speed: 97–100 % of sixteenth slots move in b1–18.
- **b12–13, the surprise.** The half cadence on C, the right hand's lone `C6:1 C6:1`, a rest, then the theme in D♭ major. It is the one harmonic event of the piece, and the tempo map's breath before it is right.

### P1. b21: the joke in the last bar is slowed out of recognition (Low–medium)

**What is written.**
- `RH 'R:2 C6:1 C6:1 F6:20'` over `LH 'R:4 F2:20'`: the fugue subject's opening rhythm (two sixteenths and an F), "straight" after twenty bars of triplets.
- The tempo map takes the bar from ♩ 74 to 56.

**Why it matters.** At ♩ 56 the two sixteenths are no longer the fugue's figure; they sound like a slow grace. The final sound is also a bare four-octave F2/F6.

**Fix.** End the ritardando at the cadence (b20) and play the tag at the fugue's tempo: `[117, 70, 'ramp'], [120, 74], [126, 56, 'ramp']` → `[117, 70, 'ramp'], [120, 100]`. "C C F" is then literally the trumpet's call, a bar early. Duration ≈ 1:26.

### P2. b19–20: the echo game is hollow (Low)

**What is written.** Right hand `C6 C6 F6 | rest | F5 F5 B♭5 | rest`, answered by left hand `F2 | C3 C3 F3 | B♭2 | F3 F3 B♭2`. For four beats there is no third.

**Assessment.** It is horn-call fifths. That can be a deliberate hunting-horn colour, but after 18 bars of full two-part harmony it may sound empty rather than playful.

**Fix.** If an answer in thirds is wanted, the left hand's echo `C3 C3 F3` → `A2 A2 F3` (the same rhythm, now with a third). This is untested; check it with the critic.

### P3. The left hand's repeated-note head (Low)

The 5-5-1 repeated-note head carries most of both episodes (b4–5, b7–9) and returns in b14–15 and b19–20. The NOTES flag it. In an invention, motivic saturation is the point, so accept it. But if the prelude feels long, b7–9's left hand is the place to vary (Q's sixteenths instead of the head).

---

## Fugue XI à 12: Concerto fuga

### Must not be touched

- **The concertino exposition (b1–8).** Trumpet, flute, violin and oboe each enter alone (first of one; nothing else attacks), with the countersubject. The subject's off-beat tattoo (C C | F F F | A A C) is unmistakable and will be recognised for the rest of the piece.
- **The trumpet persona as written in the notes.**
  - The trumpet is absent through the minor keys.
  - It returns at b41 as a high C6 tattoo, the only note it trusts.
  - It echoes E E A meekly at b47.
  - It hammers C over V7 at b62.
  - The tattoo is the trumpet's audible signature on a piano, where nothing else identifies it.

### F1. b45–46: the punchline is smudged (High)

**What is written.**
- **45.1–45.3.** The band strikes an open E–B (V1b E5, V2b E4, Va2 B3, Vc B2, Vne E2). Violino I.1's E-major head (B4 B4 E5 …) brings G♯5 only at 45.3.
- **45.3½.** The trumpet starts its F-major head on C5: C5 C5 | F5 F5 F5 | A5 A5 C6.
- **45.4.** Every ripieno voice rests (`'… R:4 …'` in Vne, Vc, Va2, V2b, V1b, Va1). The trumpet's F5 F5 F5 sounds over nothing but Violino I.1's held **B5**, a tritone above.
- **46.1.** The E chord is struck again. The trumpet's A5 now rubs against Violino I.1's G♯5 in the same octave, and then the general pause follows.

**Why it fails.** The joke is "F major against E major, every note a semitone off". The listener must hear the head *against a sounding E-major chord*. At present they hear it mostly against silence, partly under a violin, with one beat of A/G♯ clash at the end. On one piano timbre that can read as a passing wrong note, not as a wrong entry.

**Fix (tested).** The critic reports seven new "held unresolved" dissonances at 45.4: the trumpet's F5 against the sustained E chord, which is the point. Nothing else changes.
- Hold the chord through beat 4:

  | Voice | Now | Change to |
  |---|---|---|
  | Vne | `'E2:8 E2:4 R:4 E2:8'` | `'E2:8 E2:8 E2:8'` |
  | Vc | `'B2:8 B2:4 R:4 B2:8'` | `'B2:8 B2:8 B2:8'` |
  | Va2 | `'B3:8 B3:4 R:4 B3:8'` | `'B3:8 B3:8 B3:8'` |
  | V2b | `'E4:8 E4:4 R:4 E4:8'` | `'E4:8 E4:8 E4:8'` |
  | V1b | `'E5:4 D5:4 E5:4 R:4 E5:8'` | `'E5:4 D5:4 E5:8 E5:8'` |
  | Va1 | `'R:8 E3:4 R:4 E3:8'` | `'R:8 E3:8 E3:8'` |

- Take Violino I.1's E-major head an octave lower: `'B3:1 B3:1 E4:2 E4:1 E4:1 G#4:2 G#4:1 B4:5'`, and `put('V1a', 46, 1, 'G#4:8')`.
- The trumpet's F5 then lands a semitone above Violino I.2's sustained E5, as the top voice, over a full E-major chord.
- With a per-voice velocity pass, give the trumpet +10 from 45.3½. The general pause (2 beats at ♩ 56) can be a little longer, a full bar, for the "oops" to register.

### F2. b54–57: the twelve-voice tutti is a wash (High)

**What is written.**
- **Saturation.** Pitch classes per sixteenth in bar 54 (4 3 4 3 5 3 5 5 5 6 6 7 5 6 6 6), bar 55 (5 4 5 5 6 6 6 6 6 5 5 5 4 5 3 4) and bar 56 (6 5 5 4 3 3 5 6 7 6 5 5 6 4 5 5). That is five or more in 11, 12 and 11 of 16 slices, and up to seven: the whole F-major scale at once.
- **Two chromatic collisions** from the countersubject's characteristic flat notes in diminution:
  - Viola 1's E♭4 at 54.4 (last sixteenth), against Tromba E5, Violino E5 and Violoncello E3;
  - Violino's A♭4 at 55.3 (last sixteenth), against Violone A2 and Viola 2 A3.
- **The concertino stretto at one beat.** The triad-preserving mirror makes the heads coincide: Tromba and Violino play F5 F5 together at 53.2½, and Oboe and Violino play C4/C5 together at 53.3½. The four entries will be heard as one F-major fanfare spread over four octaves.
- **The second wave of inversions is inaudible.** Violino II.1 at 54.3½ is sixth of twelve, with 43 other attacks within two beats. Viola 1 at 55.3½ (sixth of nine) and Violino II.2 at 55.4½ (third of eight) start in the thick of the sixteenths.
- **Violino I.1's line `'A6:6 Bb6:2 G6:8 F6:6 G6:2 F6:4 C6:2'`** is the top of the whole texture. The source comment says the first violins descend "under the recorder", but they are a sixth above it.

**Why it fails.**
- A Brandenburg tutti is busy, but its harmony is clear on every beat.
- Here the listener will hear three things: the violone's walking augmentation (clear, a real achievement), the high slow violin line, and a shimmering mass between them.
- The two flat-against-natural clashes are "collisions that sound like mistakes" at the loudest moment of the piece.

**Fix (tested; critic: the doubling run at 55.1½ shrinks to a single weak octave, the weak fifth at 55.2½ disappears, and nothing new appears).**
- Remove the two countersubject diminutions that carry the clashes: `put('Va1', 54, 3.5, CSdim)` and `put('Vno', 55, 2.5, W.transpose(CSdim, 5, 3))`.
- Slices with 5+ pitch classes in bar 55 fall from 12 to 7.
- Moving voices in b54–57 become 11, 11, 10, 11, instead of 12, 11, 11, 11.
- Correct the source comment about Violino I.1. Keep the line, because it is the one melody the ear can follow in the tutti.
- Give the trumpet +8 for 53.1½–55.1, so that the fanfare is led by the trumpet.

### F3. b52.2: B against B♭ (Medium)

**What is written.** In the approach, the cello's chromatic bass reaches B♮2 at 52.2 (`… Bb2:4 B2:4 C3:4 …`). At the same instant Viola 2 strikes B♭3 (`'D4:4 Bb3:4 C4:4 Bb3:4'`): G7 with both thirds.

**Fix (tested; no new critic findings).** `put('Va2', 52, 1, 'D4:4 R:4 C4:4 Bb3:4')`. Holding D4 instead makes octaves with Violino I.2.

### F4. The concerto contrast (Medium)

**What is written.**
- **Stretto I, "tutti", d minor (b23–28).** On average 3.5 voices sound (at most 6): the four ripieno entries, the oboe and the violone, in rotation. At b25.2–26.4 only two to four play.
- **Tutti II (b35–40).** On average 4.5 voices (at most 7).
- **Solo episodes.** Episode 1 (b17–22) averages 3.9 voices (at most 5), Episode 2 (b28–34) 2.6.
- **For comparison.** The twelve-voice tutti (b53–57) averages 8.3.

**Why it matters.** On one piano timbre, density and dynamics are the only cues for "ripieno" against "concertino", so the alternation the NOTES describe will not be perceived. The listener gets a concertino fugue that gradually thickens into one real tutti at b53–57. That can be a good shape, an accumulation of forces, but it is not the advertised concerto form.

**Fix.**
- **Either fill the middle tuttis.** In b23–28, Violini I.2, II.2 and Viola 2 are silent throughout; give them the countersubject in d (CSd) and continuations against the violone's cadence entry at 26.1½, so that 6–8 voices sound.
- **Or make the episodes leaner (2–3 voices) and softer (−8).** At present the episodes are −4 and the tuttis +4.
- **Or describe it honestly** as an accumulation.

### F5. b58–63: the ending deflates (Medium)

**What is written.**
- After the 11–12-voice tutti, b58 thins to four lines over the C pedal.
- The trumpet's final entry (b59–60) is accompanied by three voices (Oboe countersubject, Viola 1 inversion, Violone).
- b61 has seven voices, b62 concertino and continuo only, and the ripieno enters on the last chord.
- All of this happens under `[240, 100], [248, 76, 'ramp'], [248, 70], [252, 52, 'ramp']`, so the last chord arrives at ♩ 70 → 52.

**Why it fails.**
- A concerto's tutti that enters on the final chord works as a slam a tempo.
- After a 30 % ritardando it sounds like a late entry.
- After a 10-second climax, about 15 s of thinner music at slowing speed makes the piece end smaller than it peaked.

**Fix.**
- Keep the tempo: replace the last four points with `[244, 100], [248, 90, 'ramp'], [248, 84]`. Duration ≈ 2:33, and the final chord is held at ♩ 84.
- Optionally, let Violini II and Viola 2 join the cadence on V7 at 62.3 (so the last chord is not a jump from six voices to twelve). Check this with the critic: the obvious notes make octaves with the oboe and the flute.

### Twelve voices: lines or texture?

- **Solo passages and expositions.** Real, audible lines:
  - each concertino entry is first of one or two voices;
  - the ripieno's first four entries (b9–12) are mostly audible;
  - the stretto entries of b13–14 are not (Va2 4/6, V2b 4/6, Vne 7/7).
- **The joke.** Audible lines, each head alone in its register (b41–44).
- **The twelve-voice tutti.** Three audible strands (bass, top violin, trumpet's head at its start) and a texture.
  - The advertised "four-way stretto per motum contrarium" will be heard as one fanfare.
  - The six countersubject diminutions and the second-wave inversions will not be heard as such.
  - Twelve real lines are there on paper, and they are clean of doubling (held = 0, doubled = 0), but the ear gets three.
