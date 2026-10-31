# Fugue XXIII in B major (a 5, *Fantasia ut re mi fa sol la per tutti i tuoni*): third review

**Scope.**
- `fugue.py` → `fugue.json`: 91 bars of 4/4, a four-voice fugue with a cantus.
- `NOTES.md`; `archive-n-plus-1/` (the 24-voice version) for comparison.
- The prelude is not reviewed here.

**Method.**
- I read every bar from the literal bar strings.
- I ran `critic.py` and `reduce.py --per beat`.
- Scratch tools, not kept:
  - a per-bar cantus probe: velocity, number of voices above it, attacks on the same downbeat, nearest voice, and attacks within a fourth while each semibreve is held;
  - velocities per voice per bar;
  - quarter- and eighth-note grids of b43–50, b66–72 and b77–91.
- Fixes marked **tested** were built from a scratch copy of `fugue.py`, with the repository's `tools/` linked in, and checked with `critic.py`. They add no new flags unless stated.
- Positions are bar.beat in quarters. I have not heard the renders (equal, Bach-Lehman or meantone).

## Verdict

**Main question: the fugue is clear, the cantus mostly comes across, and the meantone bar works. The piece is the most mechanical of this batch.**

**Counterpoint.**
- The exposition (b1–8) is clean and textbook.
- Every later entry starts on the cantus's note or on its *sol*/*re*/*fa*, and every fugue entry has a rest before it (checked by script). Only the cantus's statements join without a break, by design.
- The critic finds 0 parallels, 0 unresolved and 0 bad doublings.
- The figures that show the density:
  - stepwise motion is 62.5 % (under the cycle's 65 % target);
  - tertian fit is 31.6 %;
  - 13.9 % of beats triple a pitch class;
  - 11.3 % of onsets need three hands;
  - mean moving voices are 3.81.
- This is the busiest of the five, with sixteenth-note divisions around a subject and countersubject that also run in sixteenths.

**The cantus through the keys: mostly yes.**
- It is the only voice in semibreves, every note starts on a downbeat, and it is played 12–16 velocity steps above the fugue voices (for example b35: cantus 82, others 67–68). So each new key's note is an audible accented "ping", and the step-wise joints let the ear connect them.
- **Where it is clearly heard:**
  - b9–14, a middle line in a three-voice texture;
  - b15–20, more than a 5th from every other voice;
  - b75–80, as the top voice;
  - b79–81, the homecoming (C as the Neapolitan, B♭ = A♯ → B).
- **Where it is masked:**
  - right after Bull's leap, b45–48 (issue 2);
  - at its two goals, the *la* on G♯5 (b86) and the final *ut* (b91), both under the soprano (issue 1);
  - in the five-voice episodes (b35–36, b59–60, b85), where three or more attacks fall within a fourth of it while it is held.

**The meantone bar: yes.**
- b69 is a full bar of bare A♭/E♭ in five voices over four octaves: A♭2 E♭3 A♭3 A♭4 E♭5.
- In quarter-comma meantone the wolf will be unmistakable (beats at about 6, 13 and 26 Hz, from NOTES's table). In Bach-Lehman it is a striking drone bar.
- One presentational problem: the meantone render plays all 91 bars. By b69 the listener has heard C♯, F♯ and B major with 427-cent thirds, so the wolf is one more out-of-tune moment. A short meantone excerpt (b66–72) beside the same bars in Bach-Lehman would make the demonstration land.

## Ranked issues

| # | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|
| 1 | 86, 91 | The cantus's two goals are under the soprano. Its *la* G♯5 ("the top of the piece" in NOTES, but the soprano reaches E6 at b84–85 and b87–88) sits under the soprano's held D♯6. Its last *ut* B4 is in the middle of the final chord | Medium | **Tested:** the soprano rests in b86, so the cantus's G♯5 and the bass's inversion are the outer voices at the turn |
| 2 | 45–48 | Right after Bull's leap (the tour's one big event), the cantus C4–F4 is sandwiched: alto triplets a 3rd above for 15 beats (the critic's longest crossing), the bass climbing to A3–C4 just below in b47–48, all at the quietest dynamic (−6) | Medium | **Tested:** the bass's free line in b47–48 an octave lower |
| 3 | 9–86 | Thirteen six-bar regions with the same plan (entry on the cantus's first note, division, entry at *sol* or *re*). The cantus is a clock, and over 3:47 the regularity will be heard | Medium (form) | No minimal fix. If anything, let one region break the pattern (e.g. drop the second entry in D, b51–56) |
| 4 | 69.4–71.1 | The bass leaps C2 → B♭2 (a 7th) and G2 → F3 (a 7th) right after the wolf bar | Low | **Tested:** `C3` instead of `C2` at 69.4 removes the first. The second is needed to avoid parallels with the rising cantus (tested: G3 or E♭3 instead make octaves or fifths) |
| 5 | b69 | The meantone demonstration is diluted by the whole-piece meantone render | Low | Render b66–72 in both temperaments as a separate pair (no note change) |

Fixes 1, 2 and 4 together:
- 0 errors and 0 warnings, as now;
- seventh leaps 3 → 2, compound same-way leaps 2 → 1;
- stepwise 62.5 → 62.7 %;
- keyboard 11.3 → 12.0 % (fix 2 costs 0.9 %, fix 1 saves 0.1 %).

---

## Must not be touched

- **The homecoming, b79–81.**
  - C major as the Neapolitan of B, F♯7, then B.
  - The cantus is the top voice. Its B♭ is spelled B♭ and sounds as A♯, and it steps up a semitone to B.
  - It is the best idea in the piece and it is audible.
- **The wolf bar, b69.** A bare A♭/E♭ in every voice, with the first third (A♭–C) arriving on beat 4.
- **The subject's head as the cantus in quick notes** (b9, b21, b33, b45, b57, b81). It is how a listener learns what the cantus is doing.

## 1. The cantus's goals are under the soprano (Medium)

**What is written.**
- b86: soprano `D#6:16`, cantus `G#5:16`, and the bass's inversion `G#2:6 F#2:1 E2:1 D#2:2 C#2:2 B1:4` (the turn).
- b87–90: the cantus falls F♯5 E5 D♯5 C♯5 under a soprano moving in quarters a 3rd–6th above (`E6 D#6 C#6 C#6 G#5 | B5 F#5 B5 G#5 | B5 A#5 C#6 A#5`).
- b91: soprano B5, cantus B4, alto D♯4, tenor F♯3, bass B1.
- NOTES calls G♯5 "the top of the piece". The soprano has E6 at 84.4–85.1, 87.3 and 88.1.

**Why it fails.**
- The tour's two goals are the highest *la* (where it turns) and the return to *ut*. A listener following the cantus loses it exactly there, under a soprano that holds a higher note (b86) or moves above it (b87–91).

**Fix (tested).**

```
sc.put('S', 86, 1, 'D#6:16 '
                   'A#5:6 C#6:2 E6:4 C#6:4')
→ sc.put('S', 86, 1, 'R:16 '
                     'A#5:6 C#6:2 E6:4 C#6:4')
```

- **b86.** The cantus's G♯5 becomes the top voice for its *la*. Under it the bass sings the inversion, *la sol fa mi re ut* in quick notes. The two hexachords, slow on top and fast in the bass, become the outer voices at the turn.
- **The soprano.** It ends its countersubject at 85.4¾ and re-enters at b87 on A♯5, so the rest is a breath, not a gap. The vi chord at 86.1 (G♯2 B3 B4 G♯5) gets its D♯ from the alto at 86.2.
- **Critic:** no new flag; keyboard 11.3 → 11.2 %.
- **b91** I would leave. Putting the cantus on top there would mean the soprano ends on A♯5 unresolved (b90), or crosses. The listening guide can say that the last *ut* is inside the chord.

## 2. Bull's leap masked (Medium)

**What is written** (b45–48):
- Cantus `C4 | D4 | E4 | F4`.
- Alto triplets from 45.2: `E4 F4 G4 A4 B4 C5 …` up to E5, a 3rd to a 10th above the cantus, with attacks on each downbeat from b46.
- Bass: the subject on C2, then `R:8 A3:2 B3:2 C4:2 A3:2 | F3:2 G3:2 A3:2 F3:2 D3:2 E3:2 D3:4`, rising to within a third of the cantus (C4 against E4, A3 against F4).
- Dynamic −6. The cantus is at 74, against 58–63 for the others.

**Why it fails.**
- The leap A4 → C4 (a sixth down, after the lone E6 of b44 and a ritardando to 80) is the tour's one structural surprise.
- For the next four bars the new cantus is the middle of a close three- or four-voice cluster in the C4–E5 octave. That is the point where the listener most needs to find it again.

**Fix (tested).** The bass's free line in b47–48 an octave lower:

```
sc.put('B', 47, 1, 'R:8 A3:2 B3:2 C4:2 A3:2 '
                   'F3:2 G3:2 A3:2 F3:2 D3:2 E3:2 D3:4')
→ sc.put('B', 47, 1, 'R:8 A2:2 B2:2 C3:2 A2:2 '
                     'F2:2 G2:2 A2:2 F2:2 D2:2 E2:2 D2:4')
```

- The space under the cantus is cleared, and the bass stays in the register of the deep subject it has just sung.
- Critic: no new flag. Keyboard +0.9 % (the hands are further apart in b47–48).
- The alto's triplets above stay. Lifting them an octave runs into the soprano's G5–C6 in b47–48.

## 3. The regularity (Medium, form)

- From b9 to b86 every region is six bars:
  - an entry on the cantus's first note (rectus over rising statements, inversion over falling ones);
  - two bars of division or episode;
  - an entry at *sol* (rising) or *re* (falling).
- Twenty-six entries in b9–86, at one tempo except for three breaths.
- Variety comes from voice, register and division type: sixteenths, triplets at b45, the drone at b69, the cantus on top at b75. The phrase rhythm never varies.
- Bull's own fantasia has the same machine, but there the cantus is the piece. Here a four-voice fugue is fitted to it, and the fugue's own form is the same unit thirteen times.
- **A minimal change, not tested.** Drop one modulating entry in the middle of the second staircase (for example the soprano's inversion on G at b55–56), and let the division run on into the E region. It breaks the pattern once where the ear is most likely to have learned it.

## 4. The bass after the wolf (Low)

**What is written.**
- `Ab2:12 C2:4 | Bb2:8 G2:8 | F3:4 A2:4 …`: C2 → B♭2 and G2 → F3, two rising sevenths.
- The critic flags both. NOTES keeps the second.

**Fix (tested).** `sc.put('B', 69, 1, 'Ab2:12 C3:4')`.
- The first third after the wolf (A♭–C) is kept, and C3 → B♭2 becomes a step.
- Critic: one seventh leap and one compound same-way leap fewer, nothing new.
- I also tested the second leap:
  - G3 at 70.3 makes parallel octaves with the tenor (G4/G3 → F4/F3);
  - E♭3 makes parallel fifths with the cantus (B♭4/E♭3 → C5/F3).
- So the G2 → F3 leap is the price of the rising cantus. Keep it.

## 5. The meantone demonstration (Low, presentation)

**What the meantone render does.**
- It plays the whole piece, which in quarter-comma meantone is out of tune from b15 on: C♯ major with 427-cent thirds. So the wolf bar is heard after a minute of sour thirds.
- **A suggestion, no note change:** a 20-second excerpt, b66–72, rendered twice (Bach-Lehman, then meantone) as the demonstration.

**What b69 does musically in the Bach-Lehman render.**
- It is a drone: the only bar in which every voice holds a bare fifth.
- It is preceded by the soprano's 7th leap C♯6 → E♭5 into the drone, which is fine as a re-voicing.

## Better than the 24-voice version?

**Yes.**

| | a 24 (archive) | a 5 (now) |
|---|---|---|
| pc tripled on beats | 43.7 % | 13.9 % |
| bad doublings | 8 | 0 |
| low-register 2nds/7ths | 7 | 5 |
| beat parallels | 1 | 0 |
| length | 96 bars, 4:18 | 91 bars, 3:47 |

- The 24 one-key voices are now one cantus that can be followed through all twelve keys.
- There is an exposition, and the homecoming is a composed event.
- The texture can thin to three voices.
