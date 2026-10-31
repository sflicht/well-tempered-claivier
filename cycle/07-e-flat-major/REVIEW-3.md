# Fugue VII in E-flat major (third edition, a 4: *Fuga a due cori*): third review

**Scope.**
- `fugue.py` → `fugue.json`: 46 bars of 4/4, four voices in two choirs (Coro II soprano + alto, Coro I tenor + bass).
- `NOTES.md`; `archive-n-plus-1/` (the eight-voice version) for comparison.
- `REVIEW-2.md` concerns the eight-voice fugue and the prelude. The prelude is unchanged and not reviewed here.

**Method.**
- I read every bar from the literal bar strings in `fugue.py`.
- I ran `critic.py` (whole piece and by passage) and `reduce.py --per beat`.
- Scratch tools, not kept: an attack grid at eighths and sixteenths, and velocities per voice per bar.
- Fixes marked **tested** were built from a scratch copy of `fugue.py`, with the repository's `tools/` linked in, and checked with `critic.py`. They add no new flags unless stated.
- Positions are bar.beat in quarters. I have not heard the renders.

## Verdict

**Main question: yes. Clear counterpoint, every voice audible, every full entry heard.** Most of the time it is two voices at once, which is the concept.
- **The critic finds no errors:** 0 parallels (consecutive, weak, beat-to-beat), 0 unresolved, 0 low-register seconds, 0 crossings, keyboard 0 of 317 onsets. There is one bad doubling (b44.1), already in NOTES. Tripling is 5.5 %.
- **Every one of the twelve full statements enters after a rest:**
  - the exposition: tenor b1 alone, bass b3 at the bottom, alto b5 alone, soprano b7 on top;
  - the middle: tenor b9 under the first four-voice chord, soprano b10 on top, bass b14 after two bars' rest, alto b16 after seven bars' rest as the top voice;
  - the stretto: alto 33.1 alone over a held G2, tenor 33.3 at the bottom, soprano 34.1 on top (E♭6), bass 35.3 at the bottom.
- The voices rest long enough to be new when they return: the alto from 9.2 to 16.1, the bass in b12–13 and from 33.3 to 35.3.

**The two choirs: yes.**
- On one piano Coro I is the left hand (C2–B♭4) and Coro II the right hand (A♭3–E♭6).
- The exposition teaches this before the choirs meet: a low duo (b1–4), then a high duo (b5–8).
- The one place where the hands share a register is the quarrel (issue 3).

**The mirror: yes, heard as an answer from above in the same rhythm.**
- b5–8 is b1–4 upside down and an octave and a half higher. The ear hears "the same thing, falling, from above".
- That the bass's answer has become the soprano's, and the whole texture is reflected, is a fact for the score rather than for the ear. That is fine.

**The quarrel: yes. It is the best passage.**
- It runs a bar, half a bar, then a beat (b19–23). Each block is one choir alone, so the shrinking distance is heard as an accelerating exchange.
- Each block's key note is in its lower voice: A♮2 in the bass (19.4½), D♭4 in the alto (20.3).
- The reconciliation (24.1: B♭2 / E♭4 A♭4 C5, then B♭7, then E♭ at 25.1) is the moment the piece has been waiting for.

**The joke: half.**
- **Audible:** the contrast of characters. Coro I's dotted French-overture rhythm is in the left hand (+6 velocity, b25, b27, b29). Coro II's detached sixteenths are in the right (−4, gate 0.55, b26, b28).
- **Weaker:**
  - The alternation is exactly one bar each, on the barline, so it is turn-taking more than interruption. Only b25 is really cut off: its dotted upbeat (F4:3 G4:1) is answered by Coro II, not by Coro I.
  - The punchline, Coro I's own subject mocked in diminution (b28), is the lower of two right-hand lines (issue 1).
  - The augmentation's missing last bar comes back at b43 (bass F3 E♭3 D3), fourteen bars and a stretto later, under the chorale. Nobody will hear it as the end of the b25–29 bass (issue 4).

**Climax register.** The climax (38.3: soprano C6 over A♭3 and B♭2) is lower than the soprano's E♭6 at 7.1 and 34.1. It works as a harmonic and dynamic climax (+8, ♩ 76 → 64). Leave it. I note it only so that nobody "fixes" it by pushing the soprano higher.

## Ranked issues

| # | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|
| 1 | 27.4–28.2 | The mocking rectus in diminution (alto) runs under the soprano's eighths, a third or sixth below, in the same hand: the joke's punchline is an inner voice | Medium | **Tested:** soprano b28 `R:8 Ab5:2 F5:2 Ab5:2 G5:2`; tenor b27 ends `Bb3:3 D4:1` |
| 2 | 34 | The stretto's fullest bar has no bass, and Coro II's A♭ grinds against Coro I's G in minor ninths and major sevenths on every half beat | Low–Medium | Listen first. All three lines are thematic; no note change keeps the entries |
| 3 | 20, 22 | In the quarrel the alto sits at C4–F4, where the tenor was a beat before: the choirs are told apart by the bass and by turn-taking, not by register | Low | **Tested option:** Coro II's b20 an octave up. Take it only if the quarrel sounds like one choir |
| 4 | 25–29 → 43 | The interrupted augmentation's ending at b43 is not audible as an ending | Low | Describe it in NOTES and the listening guide as a hidden detail, not as the joke |

Fix 1 is the one change I propose without reservation. With it the critic stays at zero on every count (keyboard 0 of 318), and stepwise rises from 54.2 to 54.4 %.

---

## Must not be touched

- **b1–8, the mirror exposition.** It is exact, and its register flip (low duo, then high duo) is what teaches the listener the two choirs.
- **b19–25.1, the quarrel and the reconciliation.** A bar, half a bar, a beat; A♮ against D♭; then A♭ over B♭ resolving through B♭7 to E♭.
- **The stretto's entry order (33.1, 33.3, 34.1, 35.3).** Each entry comes at an edge of the texture after a rest, and the levels fall by fifths to the tonic.

## 1. The punchline in b28 is an inner voice (Medium)

**What is written** (sixteenth grid):

```
pos       S     A     T     B
27.4      .     .   Bb3   (Bb2)      <- Coro I closes: a cadence, not a cut-off
28.1    G5   Eb4     .     .         <- alto: the subject rectus, diminished
28.1½  Eb5    G4     .     .
28.1¾    |   Bb4     .     .
28.2   Eb5    C5     .     .         <- soprano a sixth above
28.2½   G5   Bb4     .     .
28.3   Ab5    C5     .     .
28.3½   F5   Bb4     .     .
28.4   Ab5    F5     .     .         <- a third above
28.4½   G5   Eb5     .     .
```

**Why it fails.**
- The turn of the joke is "Coro II now sings Coro I's own subject, at double speed". It is in the alto, E♭4–F5.
- The soprano moves above it in eighths (G5 E♭5 E♭5 G5 | A♭5 F5 A♭5 G5), mostly a third or sixth above, in the same hand and at the same velocity (S 70–73, A 71–76).
- The ear follows the top line, so the subject's head E♭–G–B♭–C–B♭ is heard inside a harmonised figure.
- Also, b27 ends with a cadence (T … C4 B♭3) and b28 starts fresh. Nothing is snatched from Coro I.

**Fix (tested).**

```
put(28, ..., S='G5:2 Eb5:2 Eb5:2 G5:2 Ab5:2 F5:2 Ab5:2 G5:2')
→           S='R:8 Ab5:2 F5:2 Ab5:2 G5:2'

put(27, B='C3:8 Bb2:8', T='Eb4:3 D4:1 Eb4:2 R:1 F4:1 D4:3 C4:1 Bb3:4')
→                       T='Eb4:3 D4:1 Eb4:2 R:1 F4:1 D4:3 C4:1 Bb3:3 D4:1'
```

```
pos       S     A     T     B
27.4      .     .   Bb3   (Bb2)
27.4¾     .     .    D4   (Bb2)      <- Coro I's pompous dotted upbeat ...
28.1      .   Eb4     .     .        <- ... and Coro II takes the E-flat, at the same pitch
28.1½     .    G4     .     .
28.1¾     .   Bb4     .     .
28.2      .    C5     .     .
28.2½     .   Bb4     .     .
28.3   Ab5    C5     .     .         <- the soprano joins as before
```

- The tenor's dotted upbeat D4 now leads to an E♭4 that Coro I never sings. The alto takes it, at the same pitch, and runs off with Coro I's own subject, alone for two beats.
- This is the gesture b25 already has (F4:3 G4:1, cut off by Coro II), so the two interruptions rhyme.
- Critic: no new flags. The whole piece still has 0 parallels of any kind and 0 unresolved, and keyboard is 0 of 318.
- Either half works alone. The soprano's rest is the important one.

## 2. Bar 34: the stretto's A-flat against G (Low–Medium)

**What is written** (eighth grid; the bass rests from 33.3 to 35.3):

```
pos       S      A      T
34.1    Eb6     F4    Ab3
34.1½     |    Eb4      |
34.2     C6     G4     G3
34.2½   Ab5    Eb4      |     <- Ab5 over G3: a minor ninth
34.3     G5     C4    Ab3     <- G5 over Ab3: a major seventh
34.3½     |      |    Bb3
34.4    Ab5     D4     G3     <- Ab5 over G3 again, with D4
34.4½     |    Eb4    Bb3
35.1     G5    Bb4     D4     <- G minor: the rubbing stops
```

**Why it matters.**
- The soprano's inversion in A♭ runs over the tenor's subject on C and the alto's inversion in G minor. Every half beat a G and an A♭ sound a ninth or a seventh apart. With no bass under them, the sonorities have no root.
- It may sound like the quarrel come back inside the stretto, which would be good. It may also sound sour. NOTES weak spot 6 asks the same question.
- **No note fix.** All three lines are thematic. Moving the soprano down an octave crosses the alto at 35.1. Bringing the bass in earlier takes away its entry at the bottom.

**Recommendation.** Listen first. If it is sour, the cheapest remedy is performance: soften the alto by 4–6 in b34, so that the two outer statements carry the bar.

## 3. The quarrel's registers (Low)

**What is written.**
- b19 (Coro I): T `Bb3 D4 F4 G4 F4`, B `Bb2 Eb3 F3 A2`.
- b20 (Coro II): S `Eb5 C5 Ab4 G4 Ab4`, A `C4 Eb4 F4 Db4 C4`.
- The alto's C4–F4 is exactly where the tenor was a beat earlier (G4 at 19.3, A4 at 22.2½).
- The choirs are still told apart. Coro I has a bass (B♭2, F2) and Coro II has none, and they never overlap. So this is a small point.

**Tested option.**

```
put(20, S='Eb5:4 C5:2 Ab4:2 G4:4 Ab4:4', A='C4:4 Eb4:2 F4:2 Db4:4 C4:4')
→ put(20, S='Eb6:4 C6:2 Ab5:2 G5:4 Ab5:4', A='C5:4 Eb5:2 F5:2 Db5:4 C5:4')
```

- **Gain:**
  - It is clean (no new flags).
  - The first exchange becomes low against high: B♭2–G4, then C5–E♭6.
  - As the exchanges shrink (b21–23), Coro II comes down an octave, which can read as the choirs closing in.
- **Cost:**
  - a third E♭6 before the climax's C6;
  - a leap E♭6 → E♭5 across the rest (b20 → 21.3).
- Take it only if, in the render, the quarrel sounds like one choir talking to itself.

## 4. The augmentation's ending (Low)

- The bass's augmentation is sung in pieces: E♭2 G2 B♭2 (b25), C3 B♭2 (b27), C3 D3 C3 B♭2 D3 (b29). Its last bar, F E♭ D, is missing until 43.1–43.4, where the bass sings F3 E♭3 D3 under the chorale's C4.
- At ♩ 72, with a stretto, a dominant pedal and a ritornello in between, a listener cannot connect b43 with b29. This is a hidden detail, which the cycle is allowed to have.
- I tried making b42's bass repeat b29's bar (`C3:4 D3:2 C3:2 Bb2:4 D3:4`) so that b43 would be heard to complete it. It gives a weak fifth S/B (G5/C3 → F5/B♭2 at 42.3) and a D3 under the soprano's E♭5 at 42.4. Not worth it.
- **Recommendation.** In NOTES and the listening guide, sell the joke as pomp against chatter and the stolen subject (issue 1), not as the unfinished augmentation.

## Better than the eight-voice version?

**Yes, clearly.**

| | a 8 (archive) | a 4 (now) |
|---|---|---|
| bars / tempo | 49 / ♩ 80 | 46 / ♩ 76 |
| mean moving voices | 4.82 | 3.04 |
| pc tripled on beats | 15.5 % | 5.5 % |
| bad doublings | 4 | 1 |
| low-register 2nds/7ths | 4 | 0 |
| crossings | 17 | 0 |
| keyboard unplayable | 9.7 % | 0.0 % |

- The choirs are now hands and registers. This answers REVIEW-2's F4: in the eight-voice version they were told apart only by pan.
- The stretto is four entries on four levels, falling by fifths to the tonic, never more than three at once. In the eight-voice version it was a sound rather than a build.
