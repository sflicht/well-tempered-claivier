# Fugue IX in E major (fourth edition, a 4: *Ricercar in circulo*): third review

**Scope.**
- `fugue.py` → `fugue.json`: 58 bars of 2/2, four voices (S, A, T, B, standing in a ring in the spatial render).
- `NOTES.md`; `archive-n-plus-1/` (the ten-voice version) for comparison.
- `REVIEW-2.md` concerns the ten-voice fugue and the prelude. The prelude is not reviewed here.

**Method.**
- I read every bar from the token strings in `fugue.py`.
- I ran `critic.py`, `reduce.py --per half` and `stretto_finder.py`. I checked the guest against `cycle/reference/bach-subjects.md`.
- Scratch tools, not kept: an attack grid at quarters and eighths, and velocities per voice per bar.
- Fixes marked **tested** were built from a scratch copy of `fugue.py`, with the repository's `tools/` linked in, and checked with `critic.py` and the source's own `verify_entries()`.
- Positions are bar.quarter (b48.3 = the second half of bar 48). I have not heard the renders.

## Verdict

**Main question: yes until bar 48. The final tutti is where the counterpoint smears (issue 1).**
- **The critic:**
  - 0 parallels of any kind, 0 unresolved, 0 bad doublings, 0 crossings;
  - keyboard 0 of 198 onsets; one low-register second (50.4½), listed in NOTES;
  - stepwise 73.4 %, Bach's range; tripling 10.9 %.
- **The exposition and the ring turned back are lucid.** Each entry is alone in its register or follows a rest:
  - the inversion at 21.1 (soprano, alone after the general pause);
  - 23.3 (bass, at the bottom);
  - 26.3 (tenor, after 6½ bars' rest);
  - 29.3 (alto, as the new top voice).
- **The antiphony is lucid.** Each exchange is a duet with the other half silent, so the halves are heard as a high duet answered by a low one. The shrinking 4-4-2-2-1-1-½-½ bars is audible as acceleration, and its harmony (V vi IV ii V V7) as one long cadence into the final tutti.

**The ring: not on one piano, and it does not need to be.**
- On a keyboard the clockwise exposition is the ordinary fugal order (middle-high, middle-low, low, top), and the counterclockwise inversion is top, bottom, middle-low, middle-high. Nothing tells a listener that these form a circle.
- What a piano listener does get from *Spem in alium* is the architecture: accumulation, first tutti, general pause, a second accumulation, antiphony of halves, final tutti. That is clear.
- The ring itself lives in `fugue-spatial.mp3`. NOTES says so honestly.

**The guest: yes as a second subject in the bass and as a cantus; not at its first entrance.**
- **R1 (b37–40).** BWV 878's subject at Bach's own pitch, `E3:16 F#3:8 A3:8 G#3:8 F#3:8 E3:4`, matches the reference file. It is the bottom line of the low duet and is clearly a different, slower subject.
- **The cantus (b48–53)** is on top with nothing above it, but on a piano it is the weakest line of the tutti (issue 4).
- **The first entrance (11.3)** is camouflaged by the alto (issue 2). So the idea "a fourth entry of our subject, but no" does not come across.
- **54.1:** the cantus's last E5 becomes the first note of our subject, in the same voice. That is the best idea in the piece.

## Ranked issues

| # | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|
| 1 | 49.4–50.2½ | Final stretto: the alto's and tenor's subjects fall in parallel seconds (E4/D♯4, D♯4/C♯4, C♯4/B3) and meet on a unison B3, under the cantus, with no bass under the first of them | Medium | **Tested:** the tenor's statement a quarter earlier (48.2), with its G♯3 at 48.1 shortened to an eighth |
| 2 | 11.2–11.3 | The guest enters on B4 right after the alto's B4, while the alto drops a third below it: it is heard as the alto holding on, not as a fourth voice | Medium | **Tested:** alto `... C#5:8 B4:2 A4:2` |
| 3 | 21–47 | Long thin middle: 27 bars (~65 s) of at most three voices, 15 of them (b33–47) duets | Low–Medium | Listen first. No note fix |
| 4 | 48–53 | On a piano the cantus's E5 (two bars, ~5 s at ♩ 90) decays under three moving subjects, and it is no louder than they are | Low | Performance only: soprano +6 from 48.1 to 54.1 |

Fixes 1 and 2 together give:
- 0 parallel errors and 0 beat-to-beat parallels, and **one weak (off-beat) fifth**: alto/tenor C♯4/F♯3 → D♯4/G♯3 at 50.3½–50.4, made by the tenor's own turn;
- 0 unresolved, 0 bad doublings, keyboard 0 of 199;
- low-register seconds still 1 (it moves from 50.4½ to 50.3½);
- stepwise 73.4 → 73.8 %;
- `verify_entries()`: all three stretto statements still 10/10 steps and 10/10 rhythm.

---

## Must not be touched

- **b16.3–20: the climb to A5 over IV after the deceptive cadence, V7–I, and the general pause.** It is the first tutti's arrival and the only silence in the piece.
- **54.1: the cantus's last note becoming our subject's first, in the soprano.**
- **b41–47: the shrinking exchanges**, two duets that never overlap, spelling one cadence.

## 1. The final stretto: two subjects a step apart (Medium)

**What is written** (eighth grid; S holds the cantus):

```
pos      S      A      T      B
48.1    E5     E4    G#3     E3     <- alto: subject on E
48.3     |     A4     B3      |     <- tenor: subject on B, half a bar later
49.1     |      |     E4      |
49.2     |    G#4      |      |
49.3     |    F#4      |      .     <- the bass's E3 ends
49.4     |     E4    D#4      .     <- a second, no bass
50.1   F#5    D#4    C#4     B2     <- a second (bass enters)
50.2     |    C#4     B3      |     <- a second
50.2½    |     B3      |      |     <- unison B3
50.3     |    C#4     A3     E3
50.4     |    D#4    G#3      |
50.4½    |      |    F#3      |     <- low second with the bass
```

**Why it fails.**
- The subject's identity is "rise a fourth and hold, then fall by step". The two inner statements start a fourth apart and half a bar apart. So when both fall, they fall a step apart, in the same rhythm, in the same octave (B3–E4).
- 49.4 is E4/D♯4 under the cantus's E5 with no bass. Then come D♯4/C♯4 and C♯4/B3, and at 50.2½ both voices are on B3.
- On a piano this is a smear of seconds in the tenor register. Two of the stretto's three subject statements become one blurred line just when the cantus needs a clean texture under it.
- NOTES lists 49.4 as a collision. The parallel seconds and the unison continue for three more attacks.

**What `stretto_finder.py` says.** For the subject on E against itself three steps lower, the half-bar distance (as written) costs 29, with roughness 7.29, among the worst of all distances and levels. One quarter costs 17 with roughness 3.68, the best of all the combinations I listed.

**Fix (tested).**

```
put('T', 48, 1, 'G#3:4')
→ put('T', 48, 1, 'G#3:2')

theme('T', 48, 3, 'B3:8 E4:12 D#4:4 C#4:4 B3:4 A3:4 G#3:2 F#3:2 G#3:4 A3:4 B3:8', ...)
→ theme('T', 48, 2, 'B3:8 E4:12 D#4:4 C#4:4 B3:4 A3:4 G#3:2 F#3:2 G#3:4 A3:4 B3:8', ...)
                                                    (same notes, label "a beat later")
```

```
pos      S      A      T      B
48.1    E5     E4    G#3     E3     <- tenor: an eighth of G#3, then a rest
48.2     |      |     B3      |     <- tenor enters
48.3     |     A4      |      |     <- the four rising-fourth notes, one per beat
48.4     |      |     E4      |
49.2     |    G#4      |      |
49.3     |    F#4    D#4      .     <- thirds
49.4     |     E4    C#4      .
50.1   F#5    D#4     B3     B2
50.2     |    C#4     A3      |
50.2½    |     B3      |      |
50.3     |    C#4    G#3     E3
50.3½    |      |    F#3      |
50.4     |    D#4    G#3      |
```

- The two rising fourths interlock, one attack per beat: E4 (alto), B3 (tenor), A4 (alto), E4 (tenor). Each head is heard.
- The descents run in thirds (F♯4/D♯4, E4/C♯4, D♯4/B3, C♯4/A3), the ordinary stile-antico way for two lines to move together. The unison is gone.
- The tenor now enters after an eighth's rest, and the order round the ring (A, T, B) is unchanged.
- **Cost:**
  - one weak fifth (C♯4/F♯3 at 50.3½ → D♯4/G♯3 at 50.4), made by the tenor's own turn on an off-beat eighth;
  - the low second against the bass's E3 moves from 50.4½ to 50.3½;
  - at 49.1 nothing is struck (all four voices hold).
- **Rejected:**
  - the tenor a fifth lower, on A3: a unison with the bass's E3 at 50.4½;
  - an octave lower: it crosses the bass at 50.4;
  - the alto an octave higher: a unison with the cantus's E5;
  - the tenor first at 48.1 and the alto at 48.3: a unison on E4 at the alto's entry.

## 2. The guest's entrance is camouflaged (Medium)

**What is written:**

```
pos      S      A      T      B
10.4     .    C#5     E4     A2
11.1     .      |      |     B2     <- double suspension (9-8, 4-3)
11.2     .     B4    D#4      |     <- alto resolves to B4
11.3    B4    G#4     E4     E3     <- soprano strikes B4 again; alto drops a third
11.4     |    F#4      |      |
```

**Why it fails.**
- The top line before the guest is the alto's C♯5 → B4. At 11.3 the soprano strikes B4 again, while the alto drops a third to G♯4 and the tenor and bass strike the tonic chord too.
- The ear follows the top: C♯5 B4 B4, one voice re-struck. The voice that seems new is the alto's G♯4, inside.
- For four beats, until the C♯5 at 12.3, nothing tells the listener the B4 is new. So the joke has no setup: our subject's first note on the very pitch where the piece began, then C♯ instead of E.

**Fix (tested).**

```
put('A', 8, 1, 'B4:16 R:8 C#5:12 G#4:8 C#5:8 B4:4')
→ put('A', 8, 1, 'B4:16 R:8 C#5:12 G#4:8 C#5:8 B4:2 A4:2')
```

```
pos      S      A      T      B
11.2     .     B4    D#4     B2     <- 9-8 still resolves on the beat
11.2½    .     A4      |      |     <- passing seventh over B2 D#4
11.3    B4    G#4     E4     E3     <- the alto has gone on down; B4 appears above it
```

- The alto's 9–8 still resolves to B4 on 11.2. It then passes through A4, a passing seventh over B2 and D♯4. The A4–D♯4 tritone resolves inward as the tenor rises to E4.
- So the alto line continues down by step, B4 A4 G♯4, and the soprano's B4 appears above it as a new voice, on the note where the piece began.
- Critic: no new flags. Stepwise 73.4 → 73.8 %.

## 3. The long thin middle (Low–Medium)

- From b21 to b47 no more than three voices sound. b21–32 builds up 1 → 2 → 3, and b33–46 is all duets. That is about 65 s out of 2:32.
- It is the design (Spem's antiphony), and NOTES lists it. The duets alternate registers, and the halving exchanges give it a direction.
- **Recommendation.** Listen. If it sags in the render, use the tempo (the map already presses to ♩ 104 from b45), not more voices. Do not thicken the duets: their clarity is what makes the final tutti an event.

## 4. The cantus on a piano (Low)

- In b48–53 the soprano holds E5 for two bars, then F♯5, A5, G♯5 and F♯5 for a bar each. On a piano each note decays while the three subject statements move underneath.
- Its velocities equal theirs:
  - b48: S 84, A and T 82–84;
  - b50: S 86, A and T 83–86, B 84–86;
  - b51: S 87, the others 85–87.
- **Recommendation (performance only, no notes):** add +6 to the soprano from 48.1 to 54.1 in `build()` or in `LEVEL`, as XI does for its trumpet. The binaural choir render sustains the notes and needs nothing.

## Better than the ten-voice version?

**Yes, by a wide margin.**

| | a 10 (archive) | a 4 (now) |
|---|---|---|
| bars / length (NOTES) | 50 / about 2:25 | 58 / about 2:32 |
| mean moving voices | 5.9 | 2.67 |
| pc tripled on beats | 42.2 % | 10.9 % |
| bad doublings | 5 | 0 |
| unresolved dissonances | 2 | 0 |
| crossings | 19 | 0 |
| keyboard unplayable | 24.4 % | 0.0 % |
| stepwise | 58.7 % | 73.4 % |

- The ten-voice version's ring existed only in the binaural render. This one is at least a pattern of registers, with an antiphony a piano can play.
- The new subject's eighth-note turn and the suspension chains answer the "plodding" of the earlier version.
