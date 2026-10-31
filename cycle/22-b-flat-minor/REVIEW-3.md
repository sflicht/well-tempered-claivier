# Fugue XXII in B-flat minor (a 6, crab fugue, *Tombeau "Ma fin est mon commencement"*): third review

**Scope.**
- `fugue.py` → `fugue.json`: 68 bars alla breve, six voices. Bars 35–68 are the exact retrograde of bars 1–34.
- `NOTES.md`; `archive-n-plus-1/` (the 23-voice version) for comparison.
- The prelude is not reviewed here.

**Method.**
- I read every bar of both halves from the literal bar strings.
- I ran `critic.py` on the whole piece and on each half alone (`XXII_HALVES`), the halves also read in 4/4 so that every quarter is checked. I also ran `reduce.py --per half` and `--per beat`.
- Scratch tools, not kept: a quarter-note grid of b31–37 and a count of note values.
- Fixes marked **tested** were built from a scratch copy of `fugue.py`, with the repository's `tools/` linked in. The built score passes the script's own palindrome check, and the whole piece and both halves were checked with `critic.py`.
- Positions are bar.beat in quarters (four per bar). I have not heard the renders.

## Verdict

**Main question: the counterpoint, yes; the palindrome, at its ends and in its shape, not in its middle.**

**Clear counterpoint: yes.**
- The texture grows one voice at a time: alto b1 alone, tenor b5, bass b9, soprano b15, mezzo b21, cantus b27.
- Five of the six first entries are the top or bottom voice after a rest. The exception is the alto at b27 (issue 3).
- The critic is clean in both halves and in the 4/4 reading: 0 parallels, 0 unresolved, 0 bad doublings, 0 % unplayable.

**The palindrome audible as such.** The listener can hear:
- **The ends.** The alto alone at both. The last four bars (`B4 C5 A4 Bb4 | C5 Db5 Eb5 F5 | Gb5 R F4 | Bb4`) are the first four read backwards, and they close on the lone B♭4 the piece began with.
- **The shape.** The voice count 1→6→1, the voices leaving in the order they came, and the symmetric tempo map.
- **The axis.** A held diminished seventh, with the cantus re-striking its B♮ on it.

In between (b37–64) a listener will not hear "backwards". They will hear a fugue whose entries end on cadences and whose voices fall away one by one. That is a fair result for a crab on one piano, and it is what NOTES predicts.

**Both halves idiomatic: the first yes; the second mostly.**
- **The reversed subject is a good tune in its own right:** H-C-A-B, a rising scale, the drop of a ninth, F → B♭.
- **Each reversed entry is introduced** by a quarter rest and a one-note upbeat (the mirror of the forward entries' H → C and rest), so it is announced, though not by silence directly before it.
- **But the reversal shows in the harmony.**
  - The critic counts 33 "seventh not resolved down" in half 2 against 12 in half 1, and 17 appoggiaturas against 4.
  - Dominants move to pre-dominants at the reversed cadences, for example b43–44: F7 – F – Cø7/E♭ – E♭m7/G♭ (V7 → iiø6/5 → iv6).
  - Every reversed passing quarter is accented: the alto's B♮4 over the cantus's G♭3 on the downbeat of b39 is the sharpest.
- **This is the price of the device.** It makes the second half sound like the first "un-happening". I would not try to fix it note by note.

**Character.** There is no note shorter than a quarter in 68 bars: 208 quarters, 194 halves, 41 wholes. As a stile-antico tombeau that is a choice, not a fault. But the piece has one surface speed for 3:16, and the summit (issue 1) adds none.

## Ranked issues

| # | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|
| 1 | 33–36 | The summit is six voices in half notes on a plateau of diminished sevenths (A°7 = C°7, then B°7, held, and back). The four B-A-C-H's fuse into one chromatic chord stream, and the axis has no audible "turn" | Medium | **Tested:** the soprano sings B-A-C-H in quarters at b33 (`Bb5:4 A5:4 C6:4 B5:4`). The crab makes it H-C-A-B on top at b36 |
| 2 | 41–42 | The reversed canon cadences V–i in B♭ minor 7 bars after the axis. With the arrival coloured by the alto's G♭5 (41.1), the second half then sounds like a 26-bar epilogue of cadences | Low-Medium | No minimal fix; the design (NOTES lists it) |
| 3 | 27.1 | The alto's subject (B♭4, a whole note) starts as an inner voice under the mezzo's D♭5, together with the cantus's entry. It becomes audible only with the leap at 28.4 | Low | Listen first. A quarter rest for the mezzo at 27.2 is possible but hardly helps a held B♭ |
| 4 | 43–44, 49–51 and the other reversed joins | Dominant → pre-dominant progressions (the mirror of b25–26 and b18–20) | Low | Accept: it is what a crab does to tonal harmony |

With fix 1:
- whole piece and both halves still 0 errors and 0 warnings; the palindrome check passes;
- stepwise 69.7 → 70.0 %;
- keyboard 0 %.

---

## Must not be touched

- **The alto alone at both ends**, with the symmetric tempo map (63 → 88 in b1–2 and 88 → 63 in b67–68). The first and last 12 seconds are the clearest statement of the idea.
- **The axis: the five upper voices tied across 34|35, the cantus re-striking B2.** On a piano the re-struck low B under a decaying diminished seventh is the one audible "hinge". Keep it.
- **The subject's design**: BWV 867's head + B-A-C-H, built so that its retrograde is itself a cadencing subject. It is what makes the second half music and not a reversed tape.

## 1. The summit: a plateau, and no audible turn (Medium)

**What is written** (half notes, b33–36; the second half mirrors it exactly):

| | 33.1 | 33.3 | 34.1 | 34.3 ‖ 35.1 | 35.3 | 36.1 | 36.3 |
|---|---|---|---|---|---|---|---|
| S | B♭5 | C6 | C6 | D6 ‖ D6 | C6 | C6 | B♭5 |
| Mz | F5 | E♭5–F5 | G♭5 | F5 ‖ F5 | G♭5 | F5–E♭5 | F5 |
| A | D♭5 | C5 | E♭5 | D5 ‖ D5 | E♭5 | C5 | D♭5 |
| T | F3 | F♯3 | A3 | A♭3 ‖ A♭3 | A3 | F♯3 | F3 |
| B | D♭3 | E♭3 | E♭3 | F3 ‖ F3 | E♭3 | E♭3 | D♭3 |
| Cf | B♭2 | A2 | C3 | B2 ‖ B2 | C3 | A2 | B♭2 |
| chord | i | A°7 | C°7 (same set) | B°7 ‖ B°7 | C°7 | A°7 | i |

**Why it fails.**
- The four transpositions of B-A-C-H move together, in the same half notes, in the middle register. The ear gets a chromatic chord stream, not four signatures; NOTES says so.
- Harmonically it is two diminished sevenths (A C E♭ G♭ and B D F A♭) for three bars, at the slowest tempo of the piece (66).
- Nothing marks the turn except the cantus's re-struck B2.
- The canon per augmentationem at b27 (alto ×1 against cantus ×2, from one downbeat) is the piece's clearest device, and the summit does not echo it.

**Fix (tested).** The soprano, which enters at b32, sings B-A-C-H itself in quarter notes over the cantus's half-note B-A-C-H, from the same downbeat.

```
put('S', 32, 1, 'Bb5:8 A5:8 Bb5:8 C6:8 C6:8 D6:8')
→ put('S', 32, 1, 'Bb5:8 A5:8 Bb5:4 A5:4 C6:4 B5:4 C6:8 D6:8')
```

**What it gives.**
- **b33.** The outer voices sing B-A-C-H at two speeds from one downbeat: soprano B♭5 A5 C6 B♮5 in one bar, cantus B♭2 A2 C3 B♮2 in two. It is the canon per augmentationem of b27, now in the outer voices and with the name.
- **b36.** By the crab, the soprano sings **H-C-A-B** (B♮5 C6 A5 B♭5) and ends together with the cantus's H-C-A-B in half notes (b35–36). So the axis is framed by the name forwards and backwards on top, the most audible thing a palindrome can offer.
- **Critic.**
  - Whole piece and both halves, also read in 4/4: no new flag. The palindrome check passes.
  - The soprano's A5 (33.2) is an unaccented échappée (step in, third out), and B♮5 (33.4) a lower neighbour of C6. Their mirrors are an appoggiatura (A5 at 36.3, a third in, resolved up to B♭5) and an accented lower neighbour (B♮5 at 36.1). Both are resolved by step: the same kinds of note the half already has.
- **Unchanged:** the four tails, the axis chord, and the soprano's climb to D6.

## 2. The cadence at b41–42 (Low-Medium)

**What is written.**
- b40: V7, with the cantus on F2 and the alto climbing `C5 Db5 Eb5 F5`.
- b41.1: the cantus reaches B♭2, but the alto lands on G♭5, the reversed ninth, so the arrival chord is G♭/B♭ for two beats. Then the alto's F4 (41.3) and the long B♭4 (b42) make B♭ minor.

**Why it matters.** It is the strongest close of the second half, 26 bars before the end. Everything after it is a sequence of entries ending on cadences:
- the mezzo in D♭ (b48);
- the soprano on F (b54);
- the bass on B♭ (b60);
- the tenor on F (b64);
- the alto on B♭ (b68).

This is the design ("each voice leaves on a cadence"), and in a tombeau it may be moving. The risk is that b43–68 sounds like a long coda.

**Fix.** None that keeps the palindrome: it is the mirror of the canon's start, b27. I would leave it, and let the symmetric tempo map's breaths (b42|43, b48|49, b54|55) do the phrasing. If it sounds static, the place to act is the tempo map: a slightly faster tempo from b43 is not symmetric, so it would have to be applied to b20–26 as well.

## 3. The alto's entry at b27 (Low)

**What is written.**
- At 27.1 four voices attack: cantus B♭2 (new), tenor D♭4, alto B♭4 (the subject's whole note), mezzo D♭5.
- The alto is an inner voice a third under the mezzo, and the new event the ear follows is the cantus's low B♭.
- The alto's entry becomes recognisable at 28.4 (the rest, then G♭5).

**Recommendation.** Leave it. The alto's statement is the companion of the cantus's augmentation, and it is clear by its second bar. A mezzo rest at 27.2 (`Db5:4 R:4 Gb5:8`) would expose a B♭ that is already decaying, so it would not help.

## 4. The reversed harmony (Low)

- **What the second half has.** Accented passing notes on downbeats, at 38.1, 39.1, 46.1, 52.1, 62.1 and 63.3, all stepwise. Sevenths approached by step and left by leap, for example the mezzo's E♭5 → C5 over F7 at 43.1–3. And V → ii progressions at the reversed joins.
- **What the critic says.** None is an error in the 4/4 reading.
- **What the ear will hear.** A second half that is harmonically "softer-edged" and wandering.
- I would present it that way in the listening guide, not fix it.

## Better than the 23-voice version?

**Yes.**

| | a 23 (archive) | a 6 (now) |
|---|---|---|
| unresolved (half 2) | 3 | 0 |
| weak / beat parallels | 4 / 4 | 0 / 0 |
| pc tripled on beats | 28.3 % | 5.3 % |
| stepwise | 62.5 % | 69.7 % |
| length | 96 bars, 4:32 | 68 bars, 3:16 |

The gathering is now one voice at a time, and the reversed exposition at the end can be recognised. The archive's summit (7 → 20 moving voices) could not be followed. This one can, and with fix 1 it also says its name.
