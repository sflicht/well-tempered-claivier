# Pair IV in C-sharp minor: second review (third edition, as built on 27 October)

**Scope.**
- `prelude.py` → `prelude.json`;
- `fugue.py` → `fugue.json`;
- `NOTES.md`, and the first review `REVIEW.md`, whose problem list this rebuild answers.

**Method.** I read every bar, ran `critic.py`, `reduce.py` and `stretto_finder.py`, and used three scratch scans:
- **Attack scan:** every simultaneous attack that forms a 2nd, 7th or 9th;
- **Voice summary:** for each voice, how often it sounds, its register, how many of its attacks coincide with other voices', and how often it doubles another voice;
- **Grid view:** a grid at eighth and sixteenth resolution.

I have not heard the renders.

## Verdict

The rebuild fixed what REVIEW.md asked for:
- the exposition accumulates (1-2-3-4-5);
- the countersubject is fixed;
- the climax carries the crux in exact augmentation;
- beat parallels fell from 22 to 1.

The prelude is a tight, lively 68-second toccata. Two things will still disappoint in the fugue:
- **The "strettos at an eighth" sound like octave echoes.** All of them are at the octave (or two octaves), so the listener hears one line with a shadow, not a new entry. The first of them lies low over the C♯2 pedal, where most of the low-register clashes are.
- **The crux is barely heard.** Bach's crux, the piece's best idea, enters twice as inner held notes under a running soprano. Its section is played quietly (−6), and the crux statements are not declared as entries, so they get no velocity emphasis.

## Ranked issues (both movements)

| # | Mvt | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|---|
| 1 | Fugue | 35–39 | The climax strettos "an eighth apart" are octave echoes. Pair 1 lies at G♯3–B2 over the C♯2 pedal, where 4 of the 9 low seconds fall | **High** | Re-space pair 1: alto a dotted quarter later (finder: offset 6, octave above, cost 14, 0 errors); keep the eighth echo only for pair 2 |
| 2 | Fugue | 17–22 | The first two crux entries are held inner notes under a running soprano. They are quiet (−6) and not declared, so they get no entry boost | **High** | Declare the crux entries; give them +10 velocity; thin the soprano in 17.1–17.2 |
| 3 | Fugue | 44–46 | The pedal "stretto" is the same line in three octaves (G♯5/G♯4/G♯3) an eighth and a quarter apart: a smear. The only beat parallel (45.2) and the remaining bad doubling (44.3) come from it | Medium | Keep S and A; the tenor holds chord tones instead of a third copy |
| 4 | Prelude | 7, 28, 36 | Motif M sounds 14 times, always from a downbeat; the dominant form is literal three times | Medium | Bar 36: replace M with the crux as four dotted eighths |
| 5 | Prelude | 19–21 | The crux plant is played at −6, then a subito +14 at bar 21. The link to the fugue is the quietest thing in the piece | Low | Bars 19–20 at 0, bars 21–22 at +10 |
| 6 | Fugue | 1–11 | Every exposition entry bar sounds E major or B major (the subject's head outlines III); C♯ minor is stated only at cadences | Watch | No action; already disclosed in NOTES |

---

## Prelude IV

### Must not be touched

- **The half-bar imitations (5–6, 10–11, 16–17).** The right hand answers the left on the "and" of beat 2. They break the motif's downbeat habit and make the prelude a dialogue.
- **The crux plant over the moving dominant pedal (19–20).** The right hand sings `C#5:6 B#4:6 | E5:6 D#5:6` as a 4–3 then a 6–5. The left hand deliberately leaves out B♯ under the C♯. It is the best-prepared link in the third edition so far.
- **The lament bass (34–35).** The left hand walks `A2 G#2 G2 | F#2 E#2 E2` in quarters under `C#6 B5 C#6 | D6 G#5`.

### P1. Bars 7, 28, 36: the motif is everywhere, and literally so (Medium)

**What is written.** Motif M (`E5:2 C#5:1 D#5:1 E5:2 G#5:3 F#5:1 E5:1 D#5:1`) opens 14 of the 38 bars, every time on a downbeat:
- in the right hand: bars 1, 3, 7, 9, 15, 18, 27, 28, 33, 36;
- in the left hand: bars 5, 10, 16, 29.

The dominant form `D#5:2 B#4:1 C#5:1 D#5:2 F#5:3 E5:1 D#5:1 C#5:1` sounds identically at bars 7 and 28. Bar 36 repeats it with G♯5 for F♯5.

**Why it fails.** By bar 28 the listener knows what the next bar will be. At ♩ = 100 the motif comes back about every 4 seconds.

**Fix.** At bar 36, put the crux in place of M, in four dotted eighths, exactly as bar 37's tetrachord moves:
- `U='C#5:3 B#4:3 E5:3 D#5:3'`;
- `L=S('G#2 D#3 F#3 D#3 G#2 D#3 F#3 D#3 G#2 B#2 D#3 F#3')`, with no B♯ under the C♯, as in bar 19.

The result: a 4–3 and a 6–5 over V7 in one bar, then bar 37's G♯ F♯ E D♯. The last two bars before the tonic become a written-out broadening, and the prelude's last melodic idea is the fugue's second subject.

### P2. Bars 19–22: the plant is the quietest thing in the piece (Low)

**What is written.** `dynamics()` gives bars 19–20 −6, then 21–22 +14.

**Why it fails.**
- The crux sits in the right hand's dotted quarters at −6 against a left hand of continuous sixteenths at the same level.
- Then comes a 20-unit subito at bar 21.

**Fix.** Set 19–20 to 0 and 21–22 to +10. Better still, add +6 to the right hand only in 19–20.

### P3. Bar 38: a bare octave ending (Low)

**What is written.** The last sonority is C♯5 over C♯3 → C♯2, with no third. It follows a V7 whose leading tone is in the left hand.

**Why it may fail.** It is not wrong, but after 37 bars in C♯ minor the open octave sounds unfinished.

**Fix (optional).** End the left hand `C#2:6` under an E4 in the right hand, which means writing the right hand's last bar as a dyad. Or accept the open octave as the attacca into the fugue's lone G♯4.

---

## Fugue IV (a 5)

### Must not be touched

- **The crux in exact augmentation in the bass under the climax (35–41).** The bass plays `C#2:24 B#1:12 E2:12 D#2:24 C#2:12`. Above it, the subject's E-major head bar lands on the crux's E (38), and its diminished-seventh bar on the crux's D♯ (39). This is a real double-fugue combination, and a bass line is the most audible place for it.
- **The exposition as built.** S – A – T – Br – B enter top-down, each previous voice carrying the countersubject above the new entry, and nobody drops out. The 4–3 in the CS's held E over the subject's B is a fine, idiomatic detail.

### F1. Bars 35–39: the strettos at an eighth sound like octave echoes (High)

**What is written.**
- **Pair 1 (35–36).** Tenor `G#3:2 E3:1 D#3:1 B2:2 F#3:6 | A3:4 F#3:2 D#3:2 B#2:2 C#3:2`. The alto follows an eighth later, an octave higher: `R:2 G#4:2 E4:1 D#4:1 B3:2 F#4:4~ …`.
- **Pair 2 (38–39).** Baritone at G♯3, soprano at G♯5 an eighth later.

**Why it fails.** At this distance and interval, every follower note repeats the leader's previous note an octave up. The ear hears one melody with an octave shadow, a thickened line rather than two entries. Two things make it worse:
- **Low register.** Pair 1 sits at B2–A3, directly over the augmented crux on C♯2/B♯1. The scan puts four of the fugue's nine low-register seconds here (35.1¾, 35.2, 36.2½, 36.3), e.g. B♯2/D♯3 against C♯2.
- **Buried countersubject.** The countersubject in the soprano (`E5:6 D#5 B4 C#5 …`) is the only line the ear can follow clearly.

The NOTES count these as two of five "complete strettos". As heard, they are doublings.

**Fix.** Make the two pairs different.
- **Pair 1.** Move the alto's entry to a dotted quarter after the tenor (35.2½). `stretto_finder.py` (subject, rectus, follower an octave above) gives offset 6 at cost 14 with 0 parallels and 0 unresolved, against cost 10 for the present eighth. The finder rates it slightly rougher; what it gains is audibility, because each head is heard before the next starts.
- **Pair 2.** Keep it at the eighth, two octaves apart and on top, where the echo is a sound worth having.
- Re-run the critic on 35–37 afterwards. Write the alto's bar 37 (`C#4:1 D#4:1 F#4:6 G#4:4`) one eighth later.

### F2. Bars 17–22: the crux is planted where it cannot be heard (High)

**What is written.**
- **Tenor (17–19).** `C#4:12 | B#3:6 E4:6 | D#4:12`.
- **Alto (20–22).** `G#4:12 | F##4:6 B4:6 | A#4:12`.
- **Soprano (17).** The countersubject's sixteenths, `E5:6 D#5:1 B4:1 C#5:1 B4:1 A4:1 B4:1`, then free eighths.
- **Dynamics.** `dynamics()` sets the whole section to −6.

**Why it fails.**
- **No emphasis.** The crux statements are in `CRUX`, not in `ENTRIES`, so `build_score` gives them none of its +5.
- **Decay.** A whole-bar tenor C♯4 at ♩ = 72 lasts 2.5 s and fades under a moving soprano.
- **Only the soprano statement (23–25) will register.** It is the top voice.

Bach's whole notes in BWV 849 work because his texture is slow too. Here the crux exposition will sound like a quiet stretch with nothing in particular to follow.

**Fix.**
- Add the five crux statements to the emphasis (append them to `ENTRIES`, or post-process their velocities to +10).
- At 17.1–17.2, let the soprano hold E5 (`E5:8` in place of `E5:6 D#5:1 B4:1`) so that the tenor's C♯4 is struck into a still texture.

### F3. Bars 44–46: the pedal stretto is one line in three octaves (Medium)

**What is written.**
- Soprano `G#5 E5 D#5 B#4 F#5 …`.
- Alto the same an eighth later at G♯4.
- Tenor the same a quarter later at G♯3.
- All over G♯1.

**Why it fails.** The texture is the same line in three octaves. It will be heard as a smear rather than three entries. It also accounts for:
- the fugue's only beat parallel (45.2, A/T F♯→A octaves);
- its last bad doubling (44.3, the long F♯ in S and A).

**Fix.** Keep the soprano and alto, the canon at the eighth on top, where it reads as an echo. Give the tenor sustained chord tones instead of a third copy:
- 44 `D#4:6 C#4:6`, where the C♯ is a 4–3 over the pedal;
- 45 `B#3:6 D#4:6`.

I checked these by hand against S and A: no doubled B♯ and no parallels. The A/T beat parallel at 45.2 disappears. Bar 46's tenor (`B#2:2 C#3:2 E3:2 B#2:6`) then needs a bridge from D♯4: re-voice it or add a passing note. Do not simply raise it an octave, because B♯3 would then sit a semitone under the alto's C♯4.

### F4. Bars 1–11: the exposition sounds in E and B (Watch)

**The harmony.** The subject's head (G♯ E D♯ B F♯) outlines E major. Where the entering voice is the lowest (5, 7, 10), the entry bar is E major or B major. C♯ minor is stated only by cadences (2.3½, 7.3, 12.1).

**Assessment.** This is disclosed in NOTES, and the ambiguity is not unattractive (it is BWV 849-like). No action, but it is one reason the fugue may feel tonally soft until the codetta.

### Note on the five voices

**The Baritone.** It sounds 41% of the time; outside its entries (7, 10–11, 38) it fills in a third above the bass. That is acceptable: BWV 849's voices rest a lot too. The middle of the fugue is a four-voice piece, and the NOTES say so.
