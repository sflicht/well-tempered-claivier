# Fugue X in E minor (third edition, a 3: *Fuga a due cori con corale*): third review

**Scope.**
- `fugue.py` → `fugue.json`: 49 bars of 12/8, three voices: the chorale (*O Lamm Gottes*, BWV 401 in G, D5–E6), Coro I (subject, upper), Coro II (inversion, lower).
- `NOTES.md`; `archive-n-plus-1/` (the eleven-voice version) for comparison.
- `REVIEW-2.md` concerns the eleven-voice fugue and the prelude. The prelude is not reviewed here.

**Method.**
- I read every bar from the token strings in `fugue.py`.
- I ran `critic.py` and `reduce.py --per beat`.
- Scratch tools, not kept:
  - an attack grid in eighths;
  - a scan of Coro I against the sounding chorale note;
  - a scan for Coro I's longest runs without a note longer than an eighth;
  - a test of the final stretto at other distances with `critic.analyse`.
- Fixes marked **tested** were built from a scratch copy of `fugue.py`, with the repository's `tools/` linked in, and checked with `critic.py`.
- Positions are bar.beat in dotted quarters, as in NOTES; "+e" is an eighth later. I have not heard the renders.

## Verdict

**Main question: yes. This is the clearest of the four recompositions in this batch.**
- **The critic finds nothing:** 0 parallels (consecutive, weak, beat-to-beat), 0 unresolved, 0 bad doublings, 0 low-register seconds, 0 crossings, 0.0 % tripling, keyboard 0 of 679 onsets.
- **Three voices in three registers.**
  - The chorale is always on top.
  - Coro I never comes within a whole tone of a sounding chorale note; only 16 of its 628 notes are a third below it.
  - Coro II stays below Coro I.
- **Every statement enters after a rest or at an edge of the texture:**
  - Coro II's inversion at 3.2, 12.2, 21.2 and 45.1;
  - the augmentation at 24.4;
  - the subject at 31.2 at the bottom;
  - Coro I's statements at 1.1, 19.1, 21.2, 30.4, 37.1 and 45.3.

  The one elided entry, the subject at 8.1, is elided on purpose ("als wie ein Lamm" resolving into it).

**The dialogue: yes.**
- Coro I's phrases (B4–F♯5) and Coro II's two-note questions (F♯3–G3 at 6.1, B3–C4 at 7.1; +6 and detached) are an octave and more apart and never overlap. On one piano that is call and answer.
- Each question ends on a rising semitone, the inflection of a question.
- The second dialogue (b29–30, in diminution) works the same way, faster.

**The chorale above: yes.** It is always the top voice, in dotted halves with breaths between lines, and nothing crosses it.

**The Recognition: yes.**
- It is prepared by the general pause (18.4).
- At b19 Coro I starts on the chorale's own G, an octave below it. It then runs ahead (G G G D D E D at twice the chorale's speed) while the chorale is still on its second G. Coro II's E-minor subject runs a tenth below.
- A listener who heard line 1 at b8 hears the chorale and its diminution together.
- The beat at 21.1 where only the chorale sounds is exactly the right punctuation before the inversions.

## Ranked issues

| # | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|
| 1 | 9.3–15.2, 22.4–28.4 | Coro I never holds a note longer than an eighth for 23–24 beats at a time (110 and 122 notes), straight through the moments where Coro II enters below it (12.2, 24.4) | Low–Medium | **Tested:** one held beat over each entry, `D5:6` at 12.2 and `G4:6` at 24.4 |
| 2 | 45.3–47.1 | The final stretto is hollow: the choirs meet in octaves or twelfths on 45.4, 46.1, 46.3 and 47.1, with nothing below E3 | Low–Medium | Listen first. The tested alternatives are not better |
| 3 | whole | Key range: E minor, G major and B minor only; C and A minor are touched for a bar (b43) and as a colour (48.1) | Low | No note fix (it follows the chorale's own cadences) |
| 4 | 5.3–7.4, 28.4–30.3 | The dialogues are a single line at a time and may sound thin | Low | Leave: the register gap is what makes them a dialogue |

---

## Must not be touched

- **7.2–8.1:** "als wie ein Lamm" (C5 B4 A4 G4 F♯4 E4 D♯4, in tenths with Coro II) resolving into the subject's E4 at the moment the chorale begins.
- **18.4–21.2:** the general pause, the Recognition, and the beat at 21.1 with the chorale alone.
- **47.3:** the subject's D♯4 resolving to E4 together with the chorale's final G5, the third of E minor.

## 1. Coro I's perpetual motion (Low–Medium)

**What is written.**
- Coro I has 628 of the piece's 975 notes.
- Its longest stretches without a note longer than an eighth:

  | stretch | beats | notes |
  |---|---|---|
  | b22.4–28.4 | 24 | 122 |
  | b9.3–15.2 | 23 | 110 |
  | b32.2–35.1 | 11 | 47 |

- At 12.2, Coro II's inversion enters (B3) under Coro I's `D5:2 C5:1 B4:1 A4:1 B4:1`.
- At 24.4, the augmentation enters (E3) under `G4:1 B4:1 E5:1 D#5:1 E5:1 B4:1`, an E-minor arpeggio, the busiest figure of the bar.

**Why it matters.**
- Both entries are low and come after a rest, so they will be heard. But each one's first beat competes with the most active moment above it.
- Six bars at a time of unbroken figuration is the étude risk NOTES itself names (weak spot 5).
- It is also an opportunity: Coro I's stillness can announce Coro II.

**Fix (tested).**

```
put('C1', 12, 1, 'G4:1 A4:1 B4:1 C5:1 D5:1 B4:1 D5:2 C5:1 B4:1 A4:1 B4:1 D5:1 ...')
→ put('C1', 12, 1, 'G4:1 A4:1 B4:1 C5:1 D5:1 B4:1 D5:6 D5:1 ...')

in put('C1', 23, 2, ...):  '... G4:1 F#4:1 G4:1 B4:1 E5:1 D#5:1 E5:1 B4:1 ...'
                         → '... G4:1 F#4:1 G4:6 ...'
```

- **At 12.2** Coro I lands on D5 and holds it under the chorale's D6 while B3 enters. That is one beat of G major with only the new voice moving.
- **At 24.4** Coro I holds G4 under the chorale's B5 while the augmentation's first long E3 enters. That is one beat of still E minor.
- Each entry gets one beat to itself, and each of the two longest runs is broken once.
- Critic: no change in any count (zero everywhere), keyboard 0 of 670.

## 2. The final stretto is hollow (Low–Medium)

**What is written** (Coro II's inversion from 45.1, Coro I's subject from 45.3):

```
pos       Ch     I      II
45.3      D6    E4     B3     <- subject enters; D6 a seventh, no third
45.4       |    E4     E3     <- octave
46.1      B5    E4     E3     <- octave; the chorale adds the fifth, not the third
46.1+2e    |    G4     G3     <- octave
46.2       |    B4    D#3
46.3      A5    B4     E3     <- twelfth
46.3+2e    |    G4     G3     <- octave
46.4       |    C5     A3
47.1       |    B4     B3     <- octave under the chorale's A: B7 without D#
47.3      G5    E4     E3     <- E minor
```

**Why it matters.**
- The inversion maps E to B, so subject and inversion keep landing on E and B together.
- With only two voices under the chorale, and nothing below E3, the piece's last statement of its idea is a series of open octaves and fifths, in the tenor register.
- Every entry is heard. The question is whether it sounds like a climax.

**What I tested** (the same three voices, scored with `critic.analyse`; I counted the perfect consonances between the choirs on the beats where both sound):

| placement | critic | octaves/fifths between the choirs |
|---|---|---|
| inversion one beat ahead (45.2) | 1 weak parallel | 2 of 7 beats |
| **two beats ahead (as written)** | clean | 3 of 6 beats |
| three beats ahead (44.4) | 2 unresolved dissonances | 3 of 5 beats |
| as written, with Coro II's approach (b43–44) an octave lower, so that line 7 has a bass | clean | as written |

The last row costs 5 onsets beyond two hands (b43.3: A2 A4 E6) and a leap F♯2 → B3 into the inversion.

**Recommendation.** Keep it and listen. Under "Erbarm dich unser" the open octaves may sound right: archaic and bare. If they sound empty, the remedy is a larger change than a review should propose, such as a different level for one of the statements.

## 3. Key range (Low)

- The chorale cadences in G and B minor, and the fugue follows it: E minor, B minor (b11, b34), G major (b15, the Recognition, b37). C and A minor appear only for a bar under line 7's first notes (b43), and C again as a colour over the coda's tonic pedal (48.1).
- Over 3½ minutes the harmony never leaves the triangle e–G–b for longer than a bar.
- That is honest to *O Lamm Gottes* and to BWV 244/1. It is a property to know about, not a fault to fix.

## 4. The bare dialogues (Low)

In 5.3–7.4 and 28.4–30.3 one line sounds at a time. On a piano that may sound thin rather than antiphonal (NOTES weak spot 1). I would leave it: the two choirs are an octave and more apart, and the questions are louder and detached. The thinness is what makes the full texture at b8 an arrival.

## Better than the eleven-voice version?

**Yes, by a wide margin.**

| | a 11 (archive) | a 3 (now) |
|---|---|---|
| bars | 56 | 49 |
| mean moving voices | 5.82 | 2.55 |
| pc tripled on beats | 41.1 % | 0.0 % |
| bad doublings | 3 | 0 |
| low-register 2nds/7ths | 9 | 0 |
| crossings | 27 | 0 |
| keyboard unplayable | 35.0 % | 0.0 % |
| stepwise | 60.9 % | 67.9 % |

- REVIEW-2 found three problems: the final stretto buried (F1), one rhythmic surface for four minutes (F2), and two choirs indistinguishable on one piano (F3). All three are answered:
  - the stretto has nothing else under the chorale;
  - the sixteenths, diminutions, augmentation and pulsing pedal vary the surface;
  - each choir is one line in its own register.
