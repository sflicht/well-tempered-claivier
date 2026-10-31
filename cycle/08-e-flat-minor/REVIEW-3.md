# Fugue VIII in E-flat minor (fourth edition, a 4: three voices and a slow one): third review

**Scope.**
- `fugue.py` → `fugue.json`: 43 bars of 4/4, four voices.
- `NOTES.md`; `archive-n-plus-1/` (the nine-voice version) for comparison.
- `REVIEW.md` and `REVIEW-2.md` concern the prelude and the nine-voice fugue. The prelude is unchanged and not reviewed here.

**Method.**
- I read every bar from the literal bar strings.
- I ran `critic.py` and `reduce.py --per beat`.
- Scratch tools, not kept: an eighth-note attack grid of the stretto and of the guest, and velocities per voice per bar.
- Fixes marked **tested** were built from a scratch copy of `fugue.py`, with the repository's `tools/` linked in, and checked with `critic.py`. They add no new flags unless stated.
- Positions are bar.beat in quarters. I have not heard the renders.

## Verdict

**Main question: yes. This is the best-made of the five recompositions in this batch.**
- **The critic finds no errors at all:** 0 parallels, 0 beat parallels, 0 unresolved, 0 bad doublings, 0 low-register seconds, 0 crossings. Tripling is 1.9 %, Bach's own range.
- **The texture is mostly three voices.** Every full-length entry has a rest before it. The dance's diminutions (b14.2, b15.1) and the tail relay (b8.3, b9.2) run on without one, as a dance and a relay should.

**The slow voice: yes.** Its four statements are four events:
- S×2 at b5.3, alone on E♭2;
- I×2 at b18.3, alone on E♭3;
- S×4 under the stretto;
- RI×2 under Bach.

Between them it is silent or has a few cadence notes. So "slow" always means "the bass", as NOTES intends.

**The stretto: mostly.**
- The approach is the best dramaturgy in the batch:
  - the lone D6 (b25.2–4);
  - the general pause (b26);
  - the single block chord E♭2 G♭3 B♭4 E♭5 (b27.1), from which every voice begins a line.
- The ×4 bass is a cantus firmus more than an audible subject. Its C♭–B♭ sigh at b29 is the moment a listener can catch it.
- The tenor's inversion (b29.1½, nothing else attacking) and the soprano's summit entry (b31.3 → G♭6 on b32.1) are clean.
- Two entries are weak:
  - the alto's answer at b30.1½, which the soprano shadows (issue 1);
  - the alto's inversion at b27.4 (issue 3).

**Bach's guest: yes.** BWV 853's complete subject is on top, alone after nine beats' rest, with a +6 velocity boost and the tenor silent. **Our subject at half speed under it: no** (issue 2).

## Ranked issues

| # | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|
| 1 | 30.2½–30.3½ | The soprano's free line attacks with the alto's off-beat answer and moves with it a 3rd/2nd above: the stretto's fourth entry becomes the lower line of a duet | Medium | **Tested:** soprano `F5:8 Ab5:4 Bb5:4`, on the beats |
| 2 | 38–39 | Our subject ×2 (alto) doubles Bach at the octave on 38.3 and then moves in **parallel sixths, in the same rhythm**, for all of b39: heard as Bach harmonised, not as our subject slowly | Medium | **Tested option:** the alto sings the **inversion** ×2 instead (contrary motion to Bach). Otherwise re-describe in NOTES |
| 3 | 27.4–28.2 | The alto's inversion starts on E♭5 inside the soprano's falling tail (A♭5 G♭5 F5 D5 E♭5): one line, not two, until the soprano stops at 28.3 | Low-Medium | Listen first; the +8 lift is there. Moving it up or down an octave collides with the tenor or repeats the tenor's entry |
| 4 | 33–36 | The C♭/a♭ pp passage is the only relief from e♭ after b18 | Low | Leave (NOTES lists it) |

Fix 1 is the note change I propose without reservation; fix 2 is a tested option. Both together:
- the critic stays at zero on every count;
- stepwise 67.7 → 67.4 %;
- keyboard 0.4 % → 0.0 %. Fix 1 alone leaves it at 0.4 %; two alternatives to fix 1 raised it to 1.1 %. Fix 2 removes the one three-hand onset at 38.2½.

---

## Must not be touched

- **b25–27: the lone D6, the general pause, the open block chord.**
  - The soprano's subject and the ×4 bass start from the same downbeat.
  - It is the one moment of the cycle so far where silence is composed.
- **b33.3: the deceptive cadence into C♭ with the subito pp** (iv6 – V7 – ♭VI), and the subject in C♭ major on top with its countersubject below.
- **b37.1–2: the RI in the bass alone for a beat, then Bach's subject entering alone on top.**

## 1. The soprano shadows the alto's answer (Medium)

**What is written** (eighth grid; the soprano's line is `Gb5:16 F5:6 Gb5:4 Ab5:2 Bb5:4 C6:6`):

```
pos      S     A     T     B
30.1    F5     .    C4   Ab2
30.1½    |   Bb4    D4     |     <- answer enters (alto)
30.2     |     |    F4     |
30.2½  Gb5   Eb5   Eb4     |     <- S and A attack together, a 3rd apart
30.3     |     |   Bb3   Gb2
30.3½  Ab5   Gb5     |     |     <- together again, a 2nd apart
30.4   Bb5     |     |     |
```

**Why it fails.**
- The answer's identity is its head, B♭ → E♭ → G♭ (a 4th and a 3rd up, off the beat). The soprano doubles both steps a 3rd above, in the same off-beat rhythm, so the top voice carries the gesture.
- NOTES flags this entry only for its attack with the tenor's tail. The soprano is the bigger problem, because it is the top voice.

**Fix (tested).**

```
put('S', 29, 1, 'Gb5:16 F5:6 Gb5:4 Ab5:2 Bb5:4 C6:6')
→ put('S', 29, 1, 'Gb5:16 F5:8 Ab5:4 Bb5:4 C6:6')
```

- The soprano now moves only on beats 3 and 4, and the alto's answer only off the beat, so the two never attack together.
- The A♭5 on beat 3 is an appoggiatura over E♭m/G♭ that rises to B♭5 on beat 4. The rise to C6 at b31.1 is kept.
- Critic: no flags. Keyboard unchanged: at 30.2½ the soprano must stay at or below G♭5 for the right hand to reach the tenor's E♭4, and here it holds F5.
- **Rejected:**
  - `F5:4 Bb5:12`: clean, but two more three-hand onsets;
  - `F5:8 Bb5:8`: one beat-parallel fifth, S/A F5/B♭4 → B♭5/E♭5.

## 2. Our subject ×2 under Bach (Medium)

**What is written:**

```
b38  S  Bb5:2 Ab5:2 Gb5:2 Ab5:2 Bb5:4 Eb5:4      A  Eb4:8 Bb4:8
b39  S  Ab5:6 Gb5:2 F5:4 Eb5:4                   A  Cb5:6 Bb4:2 Ab4:4 Gb4:4
b40  S  R:8 Gb5:4 R:4                            A  F4:4 D4:4 Eb4:4 R:4
```

**Why it fails.**
- BWV 853's subject and ours share their head, so the second bar of Bach's subject has the same rhythm as the second bar of ours at ×2 (dotted quarter, eighth, quarter, quarter).
- With the alto entering three beats after Bach, the two lines meet:
  - at 38.3 on B♭ in octaves (B♭4 under B♭5, attacked together);
  - for all of b39 in parallel sixths in identical rhythm: C♭5/A♭5, B♭4/G♭5, A♭4/F5, G♭4/E♭5.
- A listener hears Bach's subject sweetly harmonised in sixths. "Ours slowly underneath" is audible only as the closing F–D–E♭ alone in b40.

**What I tried** (each one a scratch build, checked with the critic over b37–40):

| variant | result |
|---|---|
| alto ×2 one beat earlier (37.4) | 3 unresolved dissonances (39.4, 40.2) |
| alto ×2 one bar earlier (37.1) | parallel octaves S/A E♭5/E♭4 → B♭5/B♭4 at 37.3, plus 1 unresolved |
| Bach one beat earlier (37.1) | weak parallel fifths S/A F5/B♭4 → E♭5/A♭4 at 39.3 |
| **alto: inversion ×2 in place of the subject ×2** | **clean on every count** (whole piece still 0 errors, 0 warnings) |

**The tested option.**

```
theme('A', 38, 1, aug(SQ, 2).rsplit(' ', 1)[0] + ' Eb4:4', 'S augmentation x2 under Bach\'s subject', 3)
→ theme('A', 38, 1, aug(octv(IC, 1), 2).rsplit(' ', 1)[0] + ' Eb5:4', 'I augmentation x2 under Bach\'s subject', 3)
```

The alto sings `Eb5:8 Ab4:8 | Gb4:6 Ab4:2 Bb4:4 C5:4 | D5:4 F5:4 Eb5:4`.
- **Against Bach's head.** Bach's head rises a fifth (E♭5 → B♭5). Three beats later ours falls a fifth from the same E♭5, slowly: a mirror the ear can catch.
- **b39.** The two lines now move in the same rhythm but in **contrary motion**, a wedge from a 9th to a 3rd (A♭5/G♭4, G♭5/A♭4, F5/B♭4, E♭5/C5) over A♭2–E♭3. That reads as two lines.
- **b40.** The alto closes alone with the inversion's own cadence, D5 F5 E♭5, over V–i.
- **The price.**
  - b39.4 becomes E♭ with the melodic-minor C♮ (no G♭).
  - The alto's first E♭5 is struck with Bach's B♭5 a fifth above.
  - The story in NOTES changes from "ours, slowly" to "our mirror, slowly".
  - The inversion ×2 has already been heard in the bass (b18.3), which helps recognition.

**Recommendation.**
- Listen to both. If the sixths in b39 sound like a lovely duet and not like a lost statement, keep the notes and change the description: "Bach's subject on top; ours, slowly, joins it in sixths and closes alone (F D E♭)".
- If "ours under Bach" must be heard, take the inversion.

## 3. The alto's inversion at b27.4 (Low-Medium)

**What is written.**
- The soprano: `… Ab5:2 Gb5:2 | F5:2 D5:2 Eb5:2 R:10`.
- The alto: `Bb4:8 R:4 Eb5:4 | Ab4:4 Gb4:3 Ab4:1 Bb4:2 C5:2 D5:2 F5:2`.
- The alto's E♭5 is struck at 27.4 between the soprano's G♭5 and its F5–D5. Its leap down to A♭4 (28.1) coincides with the soprano's cadence.
- So for two beats the ear hears one descending line.

**Options considered.**
- An octave lower (E♭4) runs into the tenor's held G♭3 (a unison at 28.2).
- Delaying it to 28.3 turns it into a canon at the octave with the tenor's inversion 2½ beats later, and leaves the alto two beats before its answer.

**Recommendation.** Listen first. From 28.3 the alto is alone above the slow bass and is clearly a new voice, and the +8 lift on its first two beats is already in `balance()`.

## 4. Tonic weight (Low)

- b18–32 and b37–43 are all in e♭. The C♭/a♭ passage (b33.3–36) is the only relief.
- It is well placed (pp, after the summit) and long enough (3½ bars). Leave it.

## Better than the nine-voice version?

**Yes, by a wide margin.**

| | a 9 (archive) | a 4 (now) |
|---|---|---|
| mean moving voices | 6.02 | 2.93 |
| pc tripled on beats | 24.0 % | 1.9 % |
| low-register 2nds/7ths | 11 | 0 |
| crossings | 29 | 0 |
| keyboard unplayable | 37 % | 0.4 % |
| stretto statements | 12 in nine voices, about 6 countable | 6 statements, never more than 3 at once |
