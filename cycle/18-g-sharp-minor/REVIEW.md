# Pair XVIII in G-sharp minor: review of the five-voice recomposition

**Scope.**
- `fugue.py` → `fugue.json`: *Vigilate*, 52 bars of 3/2, five voices (Soprano, Alto, Quintus, Tenor, Bass).
- `NOTES.md`.
- For comparison, `archive-n-plus-1/` (nineteen voices).
- The prelude is unchanged and not reviewed here.

**Method.**
- I read every bar as the literal bar strings in the JSON, with the declared entries marked.
- I ran `critic.py` and `reduce.py --per beat`.
- Scratch tools (not kept): a vertical grid of attacks per quarter, and real times integrated from `metadata.tempo_map`.
- Fixes marked **tested** were built from a scratch copy of `fugue.py` and compared with the current build by `critic.py`: no new flags unless stated.
- Positions are bar.beat in **half notes**, as in NOTES (b41.2 = the second half note of bar 41). `critic.py` prints quarter positions instead (its b41.3 is b41.2 here).
- I have not heard the renders.

## Verdict

**Main question: yes.** The counterpoint is clear.
- The four watchmen keep the first watch alone.
- The fifth voice is used for one job: it knocks at midnight, then rests, accompanies or knocks again.
- Mean 3.5 moving voices. Five-voice textures appear only at b21, b46 and b52.
- Every subject entry is in half notes on a strong beat, and every knock belongs to a whole door subject.

**What comes across on one piano.**
- **The single raised note per watch.** It is well placed. The three watch entries start at the same pitch (G♯4) over the same rise in tenths (E3-G♯3), so each change can be compared:

  | watch | where | how audible |
  |---|---|---|
  | II, A♯ | 16.2, alto | the top of a two-voice duet (0:53) |
  | III, E♯ | 28.1, soprano | the subject's long peak note, reached by the tritone B4-E♯5, over C♯ major (1:32). The most audible of the three: the subject's most prominent note changes |
  | IV, B♯ | 36.3, soprano | on top over the tenor's G♯3 and the Quintus's D♯4: the subject's own G♯-major chord (2:00) |

- **The knocks as lines.**
  - Every knock is part of a full door subject. Its rhythm (two staccato eighths, then a half note) differs from everything else in the piece.
  - The first, D♯3 alone in the silence after the E-major cadence (15.2, 0:49), cannot be missed.
  - The chromatic rise E-E♯-F♯-F𝄪-G♯ is heard as the knocker's continuation, because it always starts on the next beat.
- **The dawn (b46, 2:32).**
  - The arrival is strong: 2½ bars of dominant pedal (E♭ = D♯3), the soprano's held C♯5 (= D♭5, the seventh), the Quintus's last knock and its rise, then a full A-flat chord.
  - Two things weaken it at once:
    - the chord evaporates at 46.2 (issue 1);
    - the Quintus's new subject in major, the piece's last device, is an inner voice under the soprano's descant (issue 2).

## Ranked issues

| # | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|
| 1 | 46.2-47.2 | The dawn chord evaporates. At 46.2 only the soprano E♭5 and the Quintus B♭4 sound (`reduce.py`: `?310[A#4^D#5]`); the bass is silent until 47.2 and the alto until 49 | Medium | **Tested:** bass `Ab2:24`, alto `Eb4:24` in b46 |
| 2 | 46-48 | The Quintus's Ionian subject (the knock turned into the subject) is an inner voice under the soprano's eighth-note descant, and the tenor's stretto starts in octave with it (C4/C5 at 46.3) | Medium | **Tested:** the soprano holds E♭5 through b46 (descant from 47.1); plus Quintus +6 in velocity in b46-48 |
| 3 | 41.1-41.2 | At the summit the free alto doubles the soprano's B♯5, the top note of the piece and the leading tone of the C♯ cadence, at the octave (B♯4), and makes accented fifths with the tenor (D♯5/G♯4 → B♯4/E♯4) | Low-Medium | **Tested:** alto b41 `D#5:8 G#4:12 A#4:4` |
| 4 | 39.3, 40.2 | The summit chain's entries begin in octaves with the voice below: tenor B♯3 on the bass's B♯2; soprano D♯5 on the tenor's D♯4, with the bass's D♯3 half a beat later | Low | Leave the notes (built into a chain a third apart); voicing +6 for the tenor in b39 |
| 5 | 15-16, 26-27, 35-36 | Watches II-IV open on the same frame: a knock on D♯3 on beat 2 after a cadence chord, the rise E3-G♯3, the subject on G♯4. By watch IV it is a refrain | Low | Do not change the pitches (see "Must not be touched"); vary the knock's dynamics instead (e.g. watch IV's knock softer, `LEVEL[35] = -6`) |

---

## Must not be touched

- **The common frame of the watch entries.** At b16, b27 and b36: the subject on G♯4 in the top voice, over a rise E3-E♯3-F♯3-F𝄪3-G♯3 in tenths below, two beats after a knock. This is what makes A→A♯, E→E♯ and B→B♯ comparable. Change anything around it, not it.
- **The dawn's pivot, b45-46.1.** The Quintus's rise `E4:4 E#4:4 F#4:4 F##4:4` runs into A♭4 and continues `Bb4 C5 | F5`. The door subject becomes the subject in one rising line, and the soprano's D♭5 resolves to C5 on the same beat.

## 1. The dawn chord evaporates (Medium)

**What is written (b46).**

```
S  C5:8 Eb5:8 Ab5:2 G5:2 F5:2 Eb5:2 | …
A  Eb4:8 R:16                          (silent until b49)
Q  Ab4:8 Bb4:8 C5:8 | F5:12 …          (the Ionian subject)
T  Ab3:8 R:8 C4:8 …                    (its stretto entry at 46.3)
B  Ab2:8 R:16 | R:8 Eb2:8 …            (its answer at 47.2)
```

**Why it fails.**
- The piece has waited 45 bars for this chord: the night has no perfect cadence on the tonic. The dominant pedal has just held for 2½ bars.
- Half a beat later it is gone. 46.2 is a two-voice moment, a fourth (E♭5/B♭4) with no bass. The bass does not return for a full bar (three half-note beats).
- The light "comes down" (NOTES) before it has come up.

**Fix (tested).** Hold the chord's root and fifth under the first bar of daybreak:

```
put('B', 46, 0, 'Ab2:8')  →  put('B', 46, 0, 'Ab2:24')
put('A', 46, 0, 'Eb4:8')  →  put('A', 46, 0, 'Eb4:24')
```

- The bass's answer still enters at 47.2, after one half-note beat of rest.
- Critic: no new warnings.
  - The "crossing" (Quintus above alto) now lasts six beats instead of two. That is the Quintus taking the alto's register at daybreak, which it does anyway.
  - Keyboard 1.1 % → 1.5 % (held bass, sustain pedal).

## 2. The fifth voice's last subject is hidden (Medium)

**What is written.**
- The Quintus's Ionian subject `Ab4 Bb4 C5 | F5. Eb5 Db5 | C5 Bb4 Ab4 G4` is the point of the whole design: the knocker's line becomes the subject.
- Above it the soprano moves with it in b46 (`C5 Eb5` over `Ab4 Bb4`), then runs in eighths from 46.3 (`Ab5 G5 F5 Eb5 | Ab5 Bb5 Ab5 G5 …`). It is the only voice in eighths, a third to a sixth above.
- At 46.3 the tenor's stretto entry starts on C4 while the Quintus sings C5.

**Why it fails.** The ear follows the top voice and the fastest voice. Here both are the soprano. The Quintus's line will be heard as harmony until its leap to F5 (47.1).

**Fix (tested), with fix 1.**
- Let the soprano hold its E♭5 through the last two beats of b46, so the Quintus's B♭4-C5 and the tenor's entry rise alone beneath a held note. The descant then starts at 47.1, as the Quintus leaps:

  ```
  put('S', 46, 0, 'C5:8 Eb5:8 Ab5:2 G5:2 F5:2 Eb5:2 '
  →
  put('S', 46, 0, 'C5:8 Eb5:16 '
  ```

- Critic, with fixes 1 and 3: no new flags.
- Add voicing, after `build_score`: Quintus +6 in b46-48.

## 3. The summit's top note doubled (Low-Medium)

**What is written (b41).**
- Alto `D#5:4 A#4:4 B#4:8 G#4:4 A#4:4`.
- At 41.2 the soprano leaps F♯5 → B♯5, the highest note of the piece and its cockcrow interval once more. The alto takes B♯4 under it at the same moment.
- The alto's D♯5 → B♯4 against the tenor's G♯4 → E♯4 is the critic's one beat-to-beat fifth. NOTES excuses it because the alto is "the only free voice", which is exactly why it can move.

**Fix (tested).**

```
'D#5:4 A#4:4 B#4:8 G#4:4 A#4:4 '  →  'D#5:8 G#4:12 A#4:4 '
```

- The alto holds D♯5 over the tenor's F♯4 (a sixth), then sits on G♯4 a third above the tenor's E♯4 while the soprano's B♯5 sounds alone.
- Critic: the beat-to-beat fifth disappears; no new flags.
- Rejected variants:
  - `D#5:4 C#5:4 …`: fifths D♯5/G♯4 → C♯5/F♯4;
  - the original A♯4 → G♯4: octaves with the bass's A♯2 → G♯2.

## 4. The summit chain's octave starts (Low)

**What is written.**
- Entries a third apart and two beats apart begin on the third note of the voice below:
  - the tenor's B♯3 (39.3) on the bass's B♯2;
  - the soprano's D♯5 (40.2) on the tenor's D♯4. Half a beat later the bass has D♯3, so D♯ sounds in three octaves with only the alto's F♯4 between (40.2½).
- The soprano's entry is still clear (top voice, after a rest). The tenor's is not, until its leap D♯4 → G♯4 at 40.3.

**Fix.** Voicing: tenor +6 in b39-40. The doubling is the price of the chain and NOTES lists it.

## 5. The same frame, three times (Low)

**What is written.** Each watch opens the same way:

| | cadence | knock on D♯3 | subject |
|---|---|---|---|
| II | on E (15.1) | Quintus, 15.2 | alto G♯4, 16.1 |
| III | on B (26.1) | bass, 26.2 | soprano G♯4, 27.1 |
| IV | on F♯ (35.1) | tenor, 35.2 | soprano G♯4, 36.1 |

The rise below is the same each time. Between watches the tempo rises (104, 108, 112, 116) and the cadence key climbs a fifth.

**Assessment.**
- This is a strophic form, and the sameness is what makes the single raised note audible (see "Must not be touched").
- The risk is that by watch IV the listener hears a refrain and stops listening for the change.
- Vary what is not the frame:
  - the dynamic of the knock, e.g. watch IV's tenor knock softer (`LEVEL[35] = -6`, now −2), as if heard from further off at dawn;
  - or which voice holds above it (now soprano D♯5 in III, alto F♯5 in IV).

## Smaller points

- **Watch I** is 49 s of conventional four-voice exposition in half notes, the subject alone for its first 10 s. It is the slowest stretch, and NOTES says so. CS1 in eighths keeps it moving from b4.
- **The bass's subject at b21**, under the soprano's door subject, is heard from its leap B2 → E3 (22.1), not from its start.
- **The tenor's cockcrow (31.1)**, B3 → E♯4 under the Quintus's G♯4, is the second crow NOTES promises. It is audible because the Quintus holds.
- **The final chord** is A♭2 A♭3 C4 E♭4 A♭4. The soprano ends at the subject's own pitch, A♭4, where the piece began (G♯4). Low for a dawn, but it is the point.

## Better than the nineteen-voice version?

**Yes, clearly.**

| | 19 voices | 5 voices |
|---|---|---|
| pitch class tripled on beats | 50 % | 5.6 % |
| repeated notes | 20.6 % (knock relays) | 5.6 % |
| crossings | 28 | 1 |
| keyboard unplayable | 42.3 % | 1.1 % |
| stepwise motion | 50 % | 69 % |

- **The knocks** were twelve voices relaying two- or three-note figures. They are now nine complete door subjects.
- **The raised notes** were buried. Each now sits on top, on a strong beat.
- **The dawn** was plain half notes. It is now a prepared cadence and a stretto. With fixes 1-2 it would also stay lit.
