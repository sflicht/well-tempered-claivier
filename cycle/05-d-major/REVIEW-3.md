# Fugue V in D major (fourth edition, a 5): third review

**Scope.**
- `fugue.py` → `fugue.json`: 53 bars of 4/4. Four home voices, plus the Guest, who sings only BWV 850.
- `NOTES.md`; `archive-n-plus-1/` (the six-voice third edition) for comparison.
- The prelude is unchanged and not reviewed here (see `REVIEW.md`, `REVIEW-2.md`).

**Method.**
- I read every bar from the literal bar strings.
- I ran `critic.py` (whole piece and by passage) and `reduce.py --per beat`.
- Scratch tools, not kept: a per-beat and per-eighth attack grid, and velocities per voice per bar.
- Fixes marked **tested** were built from a scratch copy of `fugue.py`, with the repository's `tools/` linked in, then compared with the current build by `critic.py`. They add no new flags unless stated.
- Positions are bar.beat in quarters. I have not heard the renders.

## Verdict

**Main question: yes.** This is clear counterpoint, mostly in three voices, and its devices come across.

**Every subject entry but three has a rest before it.**
- With a rest:
  - exposition A–T–S–B;
  - middle entries A b16, T b18;
  - Stretto II A b31, T b31.2½;
  - the cascade S b38, A b39, T b40, B b41;
  - the summit S b43.3, G b43.4, T b45.3, S b46.1½.
- Without one:
  - the bass's ×2 at b43.1 runs on from its cascade entry, but it drops an octave to A2 and is the only voice in half notes;
  - the alto's coda statement at b50.1 is the only upper voice there;
  - the alto's diminution at b24.2 re-strikes the note it holds (issue 4).

**The Guest is heard all three times.**
- **b10.2.** Alto and tenor stop. The soprano resolves G5→F♯5 exactly as the 32nd run starts.
  - The bass plays the cadence Bach's subject implies: D3, G2, A2, D3 under the run, the B. and the A.
  - Velocity: Guest about 82 against soprano 69 and bass 71.
- **b43.4.** In the middle register (D4–D5), between soprano F♯6–A6 and bass F♯3–A3, with alto and tenor silent.
- **b52.2.** Alone over the D2 pedal.
- In Episode 4 (b34–36) the home voices sing Bach's head in B minor and F♯ minor, so the quotation changes the fugue's own course.

**The cascade works as a chain of duets.**
- One entry per bar, from the top voice down, each a fifth lower: C♯5, F♯4, B3, E3.
- Each new head starts under the old tail; the tails turn upward, so nothing crosses.
- The supporting voices are long notes, and the voice that has finished rests.
- The fifth step, the bass's ×2 at b43, lands the chain in the bass.

**Prolation: partly.**
- It is audible at b43–44: the bass's ×2 head (A2, D3 D3 D3, F♯3 F♯3 F♯3) under the soprano's ×1 head two beats later.
- The "three speeds at once" of b46 is on paper only. There the bass's ×2 is already in its scalar tail (`D3 C#3 B2 A2 B2 C#3 D3`), so the bar sounds like a fast soprano statement over a walking bass, with the tenor's tail between.

## Ranked issues

| # | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|
| 1 | 43.4–44.4 | The summit is hollow and doubled. Soprano and bass are in octaves on 43.4, 44.1 and 44.3, and there is no D on 44.1–44.3. The critic's only error and only beat parallel are both here | Medium | **Tested:** the alto holds D5 through b44 (re-struck at 44.1) |
| 2 | 14.4–15.1 | Soprano/tenor octaves B5/B4 → G5/G4, exposed in a three-voice episode | Low-Medium | **Tested:** the tenor holds A4 to the barline |
| 3 | 45.3–46.1 | Two voices only at the centre of the summit (bass F♯3/E3, tenor D4 G4) | Low | Leave: it is a breath before the ×½ entry |
| 4 | 24.1–2 | The alto's diminution entry re-strikes the B4 it already holds, the one entry that is neither prepared by a rest nor alone | Low | **Tested:** `B4:2 R:2` before the diminution |
| 5 | 47.3–53 | 6½ bars on a D2 pedal, mostly with 1–2 upper voices | Low | Leave (trumpets and drums, then the Guest) |

All three tested fixes together:
- They pass the critic with weak parallels 2 → 1 and unresolved 1 → 0, and no new flags.
- Suspensions rise 15 → 16.
- Keyboard-unplayable onsets rise 3.3 % → 4.6 %.

---

## Must not be touched

- **The Guest's first entry, b9.4–12.2.**
  - The answer's cadence in A turns out to be V7 of D. The soprano's G5 resolves on the Guest's first 32nd.
  - The Guest hands its last F♯4 to the tenor, which starts Episode 1 on the same pitch.
  - The joke ("the fifth entry is not ours") is in the notes.
- **The cascade, b38–42**: one-bar duets, turned tails, soft supporting voices. It is the clearest stretto in the five fugues of this batch.
- **b50–53**: the alto's subject at its first pitch over the bass's tattoo on D2, then Bach's subject alone, its F♯ the third of the last chord.

## 1. The summit is hollow and doubled (Medium)

**What is written** (b43.3–44.4, the sounding notes per beat):

| beat | soprano | Guest | bass | sounds as |
|---|---|---|---|---|
| 43.3 | A5 | – | D3 | (alto D5, tenor F♯4: D) |
| 43.4 | D6 D6 D6 | D4–G4 run | D3 D3 | octave D6/D3 |
| 44.1 | F♯6 | B4 (dotted) | F♯3 | F♯–B–F♯, octave F♯6/F♯3 |
| 44.2 | A6 | A4 | F♯3 | F♯–A only |
| 44.3 | A6 (re-struck) | F♯4 | A3 | octave A6/A3, F♯–A only |
| 44.4 | F♯6 E6 | run A4–C♯5 | A3 | A |

**Why it fails.**
- The soprano's ×1 is placed two beats after the bass's ×2, so its arpeggio coincides with the bass's on three of four beats. The two speeds are heard as one D-major arpeggio in triple octaves.
- I checked the alternatives: one beat earlier or one beat later turns these octaves into consecutive ones.
- The bar of the climax has no root. The Guest's B4 sits as a bare fourth over F♯3: the critic's `UNPREPARED+UNRESOLVED`.
- So the summit, the loudest bar (DYN +8), is the thinnest sonority of its section.

**Fix (tested).** The alto keeps the D5 it reaches at 43.3, re-strikes it at 44.1 and holds it to the end of the bar.

```
put(43, ... A='C#5:8 D5:4 R:4  R:16  R:16  R:16  R:8 A4:4 D5:4', ...)
→       A='C#5:8 D5:8  D5:16  R:16  R:16  R:8 A4:4 D5:4'
```

- At 44.1 the Guest's B4 becomes the sixth of a B-minor 6/4 over F♯ (F♯3 B4 D5 F♯6). It is a neighbour 6/4 that resolves B→A onto D/F♯: Bach's own figure, now with its harmony.
- D sounds on every beat of b44. The D5 lies above the Guest's register (its run tops out at C♯5 until it reaches D5 at b45.1, after the alto has stopped) and two octaves under the soprano.
- Critic: the b44.1 error disappears. The S/B octave warning at 44.1 remains: it is the cost of the prolation and NOTES justifies it.
- Keyboard: +5 unplayable onsets (b44 already needs three hands).
- Performance: add `('Alto', 44): -8` to `adj`, so the D5 colours the sound and does not compete.
- A variant with the alto stepping D5–C♯5–A4 crosses the Guest at b45.1. A variant with D5–E5 makes parallel fifths with the Guest at 44.4. Both were rejected.

## 2. Octaves into b15 (Low-Medium)

**What is written.** At b14.4 the soprano ends its run `C#6:1 D6:2 B5:1` and the tenor plays `B4:4`. Both fall to G at b15.1 (`G5:4`, `G4:8`): B5/B4 → G5/G4.

**Why it matters.** Three voices, the soprano's last sixteenth and the tenor's quarter both moving into the downbeat by a third. The ear hears the soprano doubled.

**Fix (tested).** Tenor b14 `A4:2 A4:1 A4:1 A4:8 B4:4` → `A4:2 A4:1 A4:1 A4:12`.
- The tenor's A4 becomes a suspension over the bass's B2–A2 and falls to G4 under the soprano's B5→G5.
- The critic's b15.1 warning is gone, with no new flag. A version with D5 instead of the held A4 was also clean, but it makes a D6/D5 octave on the way into the downbeat.

## 3. Two voices at b45.3–46.1 (Low)

The Guest has finished (45.1), the soprano rests before its ×½ (from 45.3), and alto and tenor are silent. Only the bass's ×2 tail (F♯3, E3) and the tenor's new entry (`D4 G4 G4 G4`) sound.

- It lasts two beats (about 1.4 s) and works as an upbeat to the three-speed bar.
- Leave it, unless the render shows a hole. NOTES lists it.

## 4. The diminution's entry (Low)

**What is written.** b24, the alto: `B4:4` then the diminution `B4:2 E5:1 E5:0.5 E5:0.5 …`. The entry starts by re-striking the note the voice already holds.

**Fix (tested).** `A='B4:2 R:2 ' + EM_DIM + …`
- The downbeat keeps its third, and the 32nd-note tattoo now enters from a breath, like every other entry.
- Critic: clean.

## 5. The coda's pedal (Low)

- From b47.3 the bass holds D2 for 6½ bars: two bars of S/A thirds, the alto's subject over the drum tattoo, and the Guest's last word.
- That is about 20 s on D. REVIEW-2's complaint about the old coda (nine bars on D and A) is answered in part.
- I would leave it. Each of the three events in it is new, and the last chord is the only five-voice tutti.

## Better than the six-voice version?

**Yes, clearly.**

| | a 6 (archive) | a 5 (now) |
|---|---|---|
| mean moving voices | 4.44 | 3.06 |
| keyboard unplayable | 53.7 % | 3.3 % |
| pc tripled on beats | 7.5 % | 4.8 % |
| low-register 2nds/7ths | 6 | 0 |
| BWV 850 | one entry, buried in the baritone | three entries, each with room |
| cascade | six entries in an A2–E4 band, crossings | four one-bar duets, no crossings |
