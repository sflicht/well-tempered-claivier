# Fugue XXIV in B minor (à 25): second review

**Scope.**
- `fugue.py`, which assembles `build1–5.py`, `conv_a/b/c.py` and `release.py` on the material in `xxiv.py`;
- the built `fugue.json` (63 bars, 25 voices);
- `NOTES.md`.

**Method.**
- I read every bar as note lists and ran `critic.py`, `reduce.py --per beat` and `stretto_finder.py`.
- Scratch scans:
  - voices sounding vs. distinct pitches per beat, with a list of every unison group;
  - pitch classes per beat;
  - every low-register clash with its voices;
  - velocities by voice;
  - section durations from the tempo map.
- Fixes marked **tested** were built from scratch copies of `conv_c.py` and `release.py` and compared with the current build over the whole piece with `critic.analyse`: no new parallels, unresolved dissonances or low-register clashes unless stated.

I have not heard the renders.

## Verdict

The premise is the most ambitious in the cycle, and much of it will reach a listener.
- **The subject is good:** twelve tones, three sighing "leans", a chromatic climb into the tonic. It is a true heir of BWV 869.
- **The guests are well staged.** Each enters as the *top* voice, the louder of the two top lines (velocity ≈ 76 against ≈ 70 for the free voices). Two of them enter at their own pitch in deliberately thinned textures: Fugue VIII at b47 over nine voices, Fugue II at b49 over eleven.
- **The augmentation is prepared.** The subject ×2 in the bass (b37–41) teaches the ear what the ×4 cantus will be.
- **The mirror wedge (b60–61) is clear.**

Four things will disappoint.

1. **The arrival at b53, the moment the whole cycle aims at, lands as a cluster.** On its downbeat 13 of 20 voices sound A♯, C♯, E or G against the B-major triad, and they resolve over three beats. The cause is an over-doubled A♯°7 in b52.
2. **The convergence's 25 voices are about 10 keys.** In b43–46, 17.7 voices sound but only 10.1 distinct pitches: 7.6 voices per beat sit in exact unison with another (e.g., b46.1: 18 voices, 7 pitches).
3. **The climax is broadened before it starts.** The tempo falls from 69 to 58 into the convergence. The guests run at 54–81 % of their own tempos, and Fugue I's "con brio" ladder at 45 %.
4. **The release is as long as the convergence** (51 s against 50 s), over a single struck B1 that will have died away. The last chord's five low neighbour notes make 19 of the piece's 58 low-register clashes, including a B1–C♯2–D♯2 cluster under the final sonority.

## Ranked issues

| # | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|
| 1 | 52–53 | Arrival smeared: 13/20 voices off the triad on 53.1, 8/21 on 53.2; 8 C♯s in the A♯°7 forced the staggering | **High** | **Tested.** Thin b52.3–4 (7 voices rest), resolve the rest on the downbeat, keep 4 upper appoggiaturas |
| 2 | 42–53 (and 32–41) | Unisons: 7–8 voices per beat on keys already sounding (b43.3 F♯3 ×5; b46.1 G♯3 ×5, G♯4 ×5, C♯5 ×3) | **High** | One voice per key; give the freed voices a band and a rhythm of their own (e.g., baritones as a walking quarter-note choir) |
| 3 | 41–63 | Tempo falls 69 → 58 into the convergence, 50 → 38 in the release; guests at half speed | **High** | Hold 69 to b51, broaden in c10–c11, release at 58: 4:01 instead of 4:15 |
| 4 | 62–63 | Low neighbour notes in Br4, B2, Br5, B3, B4 against the B1 pedal; D♯2 in the deepest third | Medium-High | **Tested.** The five low voices arrive directly; B3 ends on F♯2: low clashes 58 → 39. Re-strike the pedal at b60 |
| 5 | 54–59 | Release: 6 bars of B major over the pedal; Tenor II and Alto IV double the pedal note (B3, B4) for 5 bars | Medium | Tempo as in 3; rest Tenor II / Alto IV in b55–59 and let them re-enter at the wedge |
| 6 | 32–41 | Growth by doubling: unisons on 75–85 % of beats; nine voices "sustain and suspend" on the pedal; the Fugue V and VIII heads are buried (alto, baritone) | Medium | Put one guest head on top; let added voices enter with figures, not pads |
| 7 | — | The obvious allusion is missing: BWV 869, Bach's own twelve-tone B-minor finale subject (IDEAS.md says "after BWV 869"; the NOTES never name it) | Low-Medium | Quote its head once, in the release or over the pedal; verify the notes from Mutopia as was done for XIV |

---

## Must not be touched

- **The guests as top voices in thinned textures.**
  - Fugue VIII's head (Bach's BWV 853) on Soprano IV over nine voices at b47.
  - Fugue II at its own pitch on Soprano I at b49.3 over eleven.

  These are the clearest learned allusions in the three large fugues. Thinning the texture so that a quotation can be heard is exactly right.
- **The subject ×2 in the bass under CS1 ×2 (b37–41),** before the ×4 cantus. Without it the cantus could not be heard as the subject at all.
- **The mirror wedge (b60–61).**
  - S's tail rises in Tenor I (G4 G♯4 A4 A♯4).
  - I's tail falls in Alto III (D♯5 D5 C♯5 C5).
  - Both close on one B4 in a ten-voice texture.

  It is audible, witty and a real ending of the subject's story.

---

## 1. The arrival, b52–53: the climax lands as a cluster (High)

**What is written.**
- **b52.3–4 (c10): A♯°7 in 18–20 voices.** C♯ alone is in eight: Soprano II C♯6; Soprano IV and Alto III C♯5; Alto V (then Tenor III), Tenor I, Tenor IV and Baritone V C♯4; Bass I C♯3.
- **b53.1 (c11).** The cantus reaches B2, and the following voices hold or attack non-chord tones on the downbeat:

| Voice | Note on 53.1 | Resolves at |
|---|---|---|
| Soprano I | A♯5 | 53.1½ |
| Soprano II | C♯6 | 53.2 |
| Soprano III | E5 | 53.2 |
| Soprano IV | C♯5 | 53.1½ |
| Soprano V | C♯6 | 53.2½ (the U-figure lean) |
| Alto I | E4 | 53.3 |
| Alto II | G4, over the D♯3s: B–D♯–G, an augmented triad | 53.3 |
| Alto III | C♯5 | 53.3 |
| Alto V | A♯3 | 53.3 |
| Tenor II | E3 | 53.2 |
| Tenor III | A♯4, *attacked* | 53.4 |
| Tenor IV | E4, *attacked* | 53.4 |
| Baritone V | C♯4 | 53.3½ |

- Per beat, the voices on notes outside the B-major triad number **13 of 20, 8 of 21, 3 of 23, 0**. The pitch classes sounding per beat are 7, 7, 6, 3.

**Why it fails.** This is the cycle's goal, Sam's "almost religious ecstasy". A climax needs one unmistakable instant. Here the B-major triad crystallises only on beat 4, about 3.5 s after the cantus arrives. On the downbeat a piano will sound B, C♯, D♯, E, F♯, G and A♯ together.

The NOTES describe the staggering as intended ("the other leading notes resolve one after another"). But it is also forced. Resolving all eight C♯s at once makes parallel octaves. I tested resolving everything on the downbeat as written, and it produced 7 parallel octaves and 12 beat-to-beat octaves. The doubling must be cut *before* the arrival.

**Fix (tested).** In `conv_c.py`:
- seven voices release on 52.3 and *re-enter* on the arrival by leap;
- Alto II, Tenor II and Tenor IV resolve on the downbeat;
- Tenor III lands on F♯4.

| Voice | c10 (b52): now → new | c11 (b53): now → new |
|---|---|---|
| S4 | `C#5:16~` → `C#5:8 R:8` | `C#5:2 B4:14` → `B4:16` |
| A1 | `E4:16~` → `E4:8 R:8` | `E4:8 D#4:8` → `D#4:16` |
| A2 | `G#4:4 A4:4 E4:4 G4:4~` → `… G4:4` (untied) | `G4:8 F#4:8` → `F#4:16` |
| A3 | `D5:4 C#5:12~` → `D5:4 C#5:4 R:8` | `C#5:8 D#5:8` → `D#5:16` |
| A5 | `C#4:12 A#3:4~` → `C#4:8 R:8` | `A#3:8 B3:8` → `B3:16` |
| T1 | `C#4:16` → `C#4:8 R:8` | `B3:16` (unchanged) |
| T2 | `R:8 E3:8~` → `R:16` | `E3:4 F#3:12` → `F#3:16` |
| T3 | — | `A#4:12 B4:4` → `F#4:16` |
| T4 | last three sixteenths `B3:1 A#3:1 C#4:1` → `B3:1 C#4:1 E4:1` | `E4:12 D#4:4` → `B3:16` |
| Br5 | `B3:4 A3:4 C#4:8~` → `B3:4 A3:4 R:8` | `C#4:10 B3:6` → `B3:16` |

**Kept as appoggiaturas** (one per upper register, all resolving within a beat):
- Soprano I's A♯5 → B5, the end of Fugue IV;
- Soprano II's C♯6 → D♯6;
- Soprano III's 4–3, E5 → D♯5;
- Soprano V's lean;
- Bass I's 4–3 in b52 (D3 → C♯3), which must stay. Releasing Bass I instead leaves its D3 unresolved.

**Result.**
- Voices off the triad per beat: **4, 1, 0, 0**; pitch classes 6, 4, 3, 3.
- b52.3–4 thins from 18–20 to 11–13 voices, so the downbeat of b53 is a re-entry of 20. The arrival becomes an *event*: a held breath, then the tutti.
- Whole piece: no new flags; nine "seventh not resolved" notes at b52.3 disappear; low clashes 58 → 55.
- Tenor III's U-figure (repeated C♯4s into a sixth) loses its leap: F♯4, not A♯4. A small price.

---

## 2. Twenty-five staves, about ten keys (High)

**What is written.** Voices sounding vs. distinct pitches, per beat:

| Bars | Section | Voices | Pitches | Voices in unison with another |
|---|---|---|---|---|
| 32–36 | pedal | 11.6 | 9.9 | 1.65 per beat; unisons on 75 % of beats |
| 37–41 | S ×2 | 13.7 | 10.4 | 3.25 per beat; 85 % of beats |
| 42 | c0 | 16.2 | 9.0 | |
| 43–46 | c1–c4 | 17.7 | 10.1 | 7.6 per beat; every beat |
| 49–50 | c7–c8 | 12.2 | 8.1 | |
| 51–52 | c9–c10 | 15.8 | 10.4 | |

Examples (`*` = attacked on that beat):

| Beat | Voices | Pitches | Unison groups |
|---|---|---|---|
| b43.3 | 22 | 11 | F♯3 in T4/Br1*/Br2/Br3*/Br5*; D4 in A4/T1*/T3/Br4; D5 in S3*/S4/S5* |
| b44.1 | 20 | 11 | D3 in Br1*/Br4*/B5*. The cantus's D is doubled at the unison by two baritones on its own attack |
| b46.1 | 18 | **7** | G♯3 in T3/T5/Br1*/Br4/Br5; G♯4 in A2/A3/A4*/A5*/T2; C♯5 in S2*/S3*/A1*, three voices striking one key together |

**Why it fails.** Each voice is rendered on its own channel, so a unison is two strikes of the same piano key: louder, not a second part. The NOTES' rule ("one seventh and one leading tone per beat") was met by putting every other voice on the root or fifth, mostly in the same octave. On paper the convergence has 17–22 parts. To the ear it is about ten pitches plus the guests: the brief's "distribution of one role among more staves" in its purest form.

**Fix.** It is not "fewer voices"; it is "every voice its own key and its own job".
- **One voice per key.**
  - In each unison group keep the voice that arrived by step or carries a figure.
  - Move the others to an unoccupied chord member in another octave, or let them rest so that they can re-enter later as an event (as in fix 1).
  - Target: distinct pitches ≥ ¾ of the voices sounding.
- **Give the freed baritones a band and a rhythm.** In c1–c4, Br1–Br5 and T4 crowd onto F♯3/G♯3. The D3–A3 band under the tenors holds nothing but these unisons.
  - Make the five baritones a *walking choir* in quarters (Baritone III already walks in quarters at c1) moving in contrary motion pairs. That is a fifth rhythmic layer, between the cantus's whole notes and the sixteenth runs.
  - Check each pair with the critic as the c0–c4 rewrite was checked.
- **b46.1 concretely.**
  - Of the five G♯3s, keep Tenor III (held from b45). Let Tenor V, Baritone IV and Baritone V end with b45 and re-enter at c5 (b47) with new material, where the texture is deliberately thinned to nine, so that c5 becomes a change of colour rather than a hole. Rest Baritone I, or move it to an unoccupied chord member and check the one-seventh rule.
  - Of the five G♯4s, keep Alto II's held note and Alto IV's run, which leaves at once; rest Alto III, Alto V and Tenor II.
  - Of the three C♯5s struck together (Soprano II, Soprano III, Alto I), keep one.
  - Not tested as a set. Each of these notes is a chord tone, so resting it cannot create a parallel or an unresolved dissonance; any note that is *moved* must be checked.

---

## 3. Tempo: the climax is broadened before it begins (High)

**What is written.**
- `tempo_map`: 63 → 69 from b26 to b37, 69 held to b41, then **a ramp down to 58 across b41–42**. That is 58 for the whole convergence, 50 by b54, 46 at b62, 38 at the end.
- Durations: build-up 153 s, convergence 50 s, release 51 s; 4:15 in all.
- The guests' own tempos (from their `fugue.json`) and their speed here:

| Guest | Own tempo | Here | Fraction |
|---|---|---|---|
| V | 108 | 58 | 54 % |
| VIII | 80 | 58 | 73 % |
| II | 80 | 58 | 73 % |
| IV | 72 | 58 | 81 % |
| V in B (release, b54) | 108 | ≈ 50 | 46 % |
| Fugue I's ladder | 104 | ≈ 47 | 45 % |

**Why it fails.**
- The marking is "Largo, poi con fuoco". The fuoco peaks at 69 *before* the convergence, so the climax is slower than everything before it, including the Largo exposition (63).
- A tattoo at half speed is a different tune. Fugue V's "trumpets and drums" and Fugue I's "con brio" will be heard as hymns, which makes the cycle-memory game harder exactly where it should pay off.
- The cantus does not need slowing to be heard. At 69 its whole notes still last 3.5 s, and it is already the loudest voice (velocity ≈ 84).

**Fix.**
```
'tempo_map': [[100, 63], [144, 69, 'ramp'], [c0 + 40, 69], [c0 + 48, 58, 'ramp'],
              [c0 + 72, 58], [c0 + 80, 46, 'ramp'], [c0 + 88, 38, 'ramp']]
```
- Hold 69 through c9, broaden over c10–c11 into the arrival, and keep the release at 58 until the wedge.
- Convergence 42 s, release 46 s, total 4:01.
- Guests at 64–96 % of their tempos, Fugue I at 56 %.
- **Option (not tested).** Quote Fugues V and I in diminution, which at 69/58 is close to their original speed. Fugue V in diminution lasts one bar (b43.2½–44.2½), so S1 would need a new continuation in b44–45.

---

## 4. The last chord: mud in the bottom octave (Medium-High)

**What is written.**
- In `release.py`'s `arrive` list, five *low* voices approach the chord by a neighbour note:
  - Baritone IV `A#2 → B2` (62.1);
  - Bass II `C#3 → B2` (62.2);
  - Baritone V `C#3 → D#3` (62.3);
  - Bass III `C#2 → D#2` (62.4);
  - Bass IV `C#2 → B1` (63.1).
- They sound against the B1 pedal, Bass I's F♯2 and each other. At 63.1, B1, C♯2 and D♯2 sound together, and C♯2 also rubs against B2, D♯3 and D♯3.
- These are 19 of the piece's 58 low-register clashes.
- Bass III's final note puts the chord's third, D♯2, a major third above B1 in the deepest octave.
- The B1 pedal (Contrabass) is struck **once**, at b54.1, and held for 40 quarters (≈ 51 s). On a piano it will have decayed long before b62, so the bottom of the last chord is these neighbour notes.

**Fix (tested).**
- The five low voices arrive directly. In the `arrive` loop:
  ```
  if v in ('Br4', 'B2', 'Br5', 'B3', 'B4'):
      P(v, r(k), beat, f"{f}:{left}")
  else:
      P(v, r(k), beat, f"{a}:4 {f}:{left - 4}")
  ```
- Bass III's final note `D#2` → `F#2`.
- Bass IV's direct B1 at 63.1 then *re-strikes* the pedal under the last chord.
- Re-strike the Contrabass at the wedge as well: in the pedal loop, write bar 59 as `B1:16`, untied, so that b60 starts a new note.

**Result.** Low clashes 58 → 39 (all 19 at the last chord gone); nothing new flagged; one more crossing. The upper voices keep their neighbour-note bloom, which on a piano will sound like a chord opening.

---

## 5. The release, b54–59 (Medium)

**What is written.**
- Ten bars after the arrival. Harmony: B major for six bars, with E/B and F♯7/B inflections over the pedal. Then Em(maj7)–E7–A–Fr6 (the wedge), then B.
- Fugue V in B major (Tenor III, b54), then Fugue I's canon at the octave, 3 eighths apart, in two rungs:
  - Baritone II → Tenor V;
  - Alto II → Soprano I.
- Tenor II and Alto IV hold B3 and B4 for most of b55–59, resting in the canon's F♯7 bars. The NOTES: "every move they could make there collided with the canon."

**Why it matters.**
- A 51-second release, 30 s of it on the tonic over one pedal, after a 50-second convergence, is the "long harmonically static stretch" Sam objected to.
- The two inner pedals add nothing the Contrabass's B does not already say.
- They count toward "8–9 lines", but they are doublings, and they thicken the register where the first rung of the ladder (F♯3–F♯5) has to be heard.

**Fix.**
- The tempo change in 3 already shortens the release to 46 s.
- Rest Tenor II and Alto IV in b55–59 and let them enter with the wedge (b60), where their present lines `A3:8 C4:8~ | C4:4 B3:12` and `C#5:16 | B4:16` are real counter-lines. The ladder then sounds in 6–7 clear lines, and the wedge gains by contrast.

---

## 6. The pedal and S ×2 bars, b32–41 (Medium)

**What is written.**
- The voice count rises from 9 to 20, mostly by sustained doublings. The NOTES: "S1, S2, A2, A4, A5, T2, Br3, Br5 and B1 sustain and suspend"; "several (A3, A4, T2, Br3) sustain C♯ as an inner pedal".
- Unisons on 75–85 % of beats (table in 2).
- The two new guest heads are inner voices in 13–15-voice textures:
  - Fugue V's head on Alto I, C♯ major, b34.3, G♯4–G♯5, under Sopranos I, II and IV;
  - Fugue VIII's head on Baritone II, F♯ minor, b35.3, E♯3–D4.

**Why it matters.** These bars are the crescendo that makes the convergence an arrival. Growth by held unisons is heard as louder harmony, not as more voices. And a guest head is the one thing in these bars a listener could *recognise*.

**Fix.**
- Give the Fugue V head to the top voice, e.g. by exchanging it with Soprano I's E♯6–C♯6 line in b34.3–35.2, an octave up. That makes it a foretaste the ear can catch, and it sets up the full Fugue V on top at b43. Not tested.
- Leave Fugue VIII's head where it is, as a hidden pre-echo: its real entry at b47 is the audible one.
- Apply the one-voice-per-key rule of 2 to the C♯ inner pedals.

---

## 7. The missing allusion: BWV 869 (Low-Medium)

**What is written.**
- `IDEAS.md` describes this fugue as "a twelve-tone B-minor subject (after BWV 869)".
- The NOTES never mention BWV 869, and nothing quotes it.
- WTC I ends with Bach's own twelve-tone subject in B minor, the WTC finale this cycle's finale answers.

**Fix.**
- Credit the model in the NOTES.
- Consider quoting the BWV 869 subject's head once, for instance as the release's first entry instead of a second Fugue V (b54), or over the dominant pedal (b33–36), checked with `stretto_finder --against`.
- Take the notes from the Mutopia MIDI with `python3 -I`, as was done for the Royal Theme in XIV. They are not in `cycle/reference/bach-subjects.md`, and I have not written them here from memory.

---

## Will the advertised devices be heard?

- **The quarter-speed cantus (b43–53).** It is heard as the bass: the lowest and loudest voice, 84 against about 70. It is recognisable as the subject only at its chromatic close, G–G♯–A–A♯–B (b51–53), which will be heard as a rising bass into the arrival. The ×2 statement at b37–41 is what makes even that possible.
- **Fugue V (b43, Soprano I, D major, an octave up).** Its repeated-note tattoo identifies it, even at 54 % speed. Yes.
- **Fugue VIII (b47, Soprano IV, E♭ minor, nine voices).** The best placed; Bach's BWV 853 head. Yes.
- **Fugue II (b49.3, Soprano I, own pitch, eleven voices).** Yes.
- **Fugue IV (b51.4, Soprano I, transposed and re-barred from 3/4).** Weakest: new metre and new key. Partly.
- **Fugue I's ladder (b55–59).**
  - Rung 1 (Baritone II → Tenor V) is audible in an 8-line texture, better without Tenor II and Alto IV (fix 5).
  - Rung 2 (Alto II → Soprano I) is clearly audible on top.
  - At 45 % of Fugue I's tempo it sounds like a chorale canon, not like Fugue I.
- **The last chord's arrival.** The real arrival is b53; fix 1 makes it one. The last chord (b62–63) is a slow bloom, which works once the bass mud (fix 4) is gone.

## Note on the twenty-five voices

| Bars | What sounds |
|---|---|
| 1–31 | An honest 4–9-voice fugue: real lines with the subject, its answer, its inversion, CS1, U and R |
| 32–41 | Growth to 20 voices, partly by held inner pedals; 1.7–3.3 voices per beat in unison with another |
| 43–46, 49–53 | Twelve to twenty-two parts on paper, 8–14 keys on the instrument (b43–46: 17.7 voices, 10.1 keys) |
| Every texture | Audible lines: the top (guests), the cantus, one or two runs (R relays in Soprano V, Alto IV, Tenor IV) and the knocking U figures |
| 54–59 | 8–9 lines, two of which are pedal doublings |

The structure is sound, and it is the right one for a finale. The work left is to make the voices that are present *different from each other*: different keys, different rhythmic layers, and rests that let entries happen.
