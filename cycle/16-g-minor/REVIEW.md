# Pair XVI in G minor: review of the five-voice recomposition

**Scope.**
- `fugue.py` → `fugue.json`: *Fantasia e fuga a 5 per Reincken*, 68 bars of 4/4, three manual voices and double pedal.
- `NOTES.md`.
- For comparison, `archive-n-plus-1/` (seventeen voices).
- The prelude is unchanged and not reviewed here.

**Method.**
- I read every bar as the literal bar strings in the JSON, voice by voice, with the declared entries marked.
- I ran `critic.py` and `reduce.py --per beat`.
- Scratch tools (not kept):
  - a vertical grid of attacks per eighth;
  - a time map integrated from `metadata.tempo_map`.
- Fixes marked **tested** were built from a scratch copy of `fugue.py` and compared with the current build by `critic.py`: no new warnings or errors unless stated.
- Positions are bar.beat in quarters. I have not heard the renders.

## Verdict

**Main question: mostly yes.** The counterpoint is clear again. Five voices sound together only in b64-68. Each line has a short fugato and then its pedal canon. In every line the Tenor falls silent before Pedal I enters, so the follower has the tenor register to itself; the Tenor rejoins only for b64-68. Almost every Vorimitation entry starts after a rest. The two exceptions continue on purpose from the note before: line 5's Tenor (b25) and line 9's Alt, whose C♯ falls to C (b52).

**The weakness is what the manual voices do once the pedal enters.** They stop working the line's subject and turn into a slow chordal accompaniment. That is the most important remaining problem (1).

**What comes across on one piano.**
- **The pedal canon, lines 1-8.** It is heard as a canon where the follower is exposed:
  - line 1 (b6-11): the follower finishes alone over the held B♭2;
  - line 6 (b34-39): B♭–C♯–D, then the augmented sixth at 37.3 and the general pause;
  - line 8 (b47-50): the repeated E's knocked between the two pedals: E3 at 47.3, 48.1 and 48.3; E4 at 48.2, 48.4 and 49.2.
- **The shrinking distance.** It is audible as "the echo comes sooner" from line 6 on.
- **The closing canon (b60.3-66).** It will not sound like a canon.
  - At 1½ beats behind a line in half notes, Pedal I is in octaves with Pedal II for half a beat. For the other beat and a half it sits a 7th or a 9th above: B♭2/A3 at 62.1 and 64.3; A2/B♭3 at 64.1½ and 65.1.
  - On a piano this is a bass with a late upper octave. That fits NOTES' "limping shadow", but it is an image, not an audible canon.
  - Above it, the stretto of S10 in the Diskant (60.3½) and the Alt (61.2½) is clear.
- **The BWV 542 guest (b57.2½-60.2½).** It comes across unmistakably: at its own pitch, on top, entering after a rest, with only the Alt below and the pedal.
  - It is heard as a quotation set between lines 9 and 10.
  - Nothing prepares it and nothing after it uses it (see the smaller points).
- **The echo passage (b19-24).** The manuals alone, the chorale on top, each line's close repeated 16 velocity steps softer at the same pitch. It is the clearest change of colour in the piece.

## Ranked issues

| # | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|
| 1 | 14-18 (also 6-9, 54-56) | Once the pedal enters, the manual voices drop the subject and move in quarters and half notes: the Alt ticks G4/F♯4/F4 for 4½ bars | Medium-High | **Tested:** the limping dotted figure of S2 in the Alt, b15-17 |
| 2 | 25-27.3 | S5's syncopes cannot be heard: the Tenor is alone, and then the Alt enters in the same phase, so nobody marks the beat until Pedal II at 27.3 | Medium | **Tested:** Alt `D4:4 F4:4 D4:4 F4:4` in b25 |
| 3 | 60.3-66 | The closest canon sounds like a delayed octave bass, with held 7ths and minor 9ths between D2 and D4 | Low-Medium | Leave the notes; Pedal I −6 in velocity from 60.3, so it reads as the shadow it is meant to be |
| 4 | 12.2, 13.1 | Line 2's canon entries begin in octaves with the voice before (A3/A4, then A4/A5) | Low | Voicing: +6 on the first bar of the Alt (b12) and the Diskant (b13) |
| 5 | 57-60 | The guest is bare at 58.3-58.4½ (Diskant over C2-E♭2-F2, four octaves apart) and at 59.4 (octave D's), and is never echoed | Low | No tested fix (an Alt G4 at 58.3 makes fifths with Pedal II); leave |

---

## Must not be touched

- **The echo passage, b19-24.** The chorale in the Diskant, and the close of each line repeated at the same pitch by Alt and Tenor at −16 velocity. It is the one place the piece changes colour without changing key, and it lets lines 3-4 be the bar form's repeat.
- **Line 8, b46-51.** The lone Tenor knocking on E after B♭ major. The repeated E's in canon between Pedal II and Pedal I (E3 at 47.3, 48.1 and 48.3; E4 at 48.2, 48.4 and 49.2) are the best moment of the pedal canon: the device and the image are the same thing.

## 1. The manual voices stall under the cantus (Medium-High)

**What is written.** The Alt from 14.4 to the end of b18:

```
G4:4 | G4:4 G4:4 F#4:4 F4:4 | G4:4 G4:4 F#4:4 G4:4 | F#4:4 F#4:4 G4:4 F#4:4 | G4:4 F#4:8 G4:4
```

- Over the same bars the Diskant moves in half notes (`Eb5:8 D5:8 | Eb5:8 D5:4 Bb4:4 | C5:4 A4:4 Bb4:4 D5:4 | D5:4 C5:8 Bb4:4`).
- The Tenor rests from 14.4.
- The two pedals move in half and quarter notes.
- So from 14.4 to 19.1 (0:47-1:01) no voice moves faster than a quarter note.
- The harmony is not static (`reduce.py` shows a new chord on almost every beat). The lines are: the Alt is a list of the chords' thirds and leading tones.
- The same thing happens in b6-9, where the Alt has `F#4:8 G4:8 | F#4:8 G4:4 F#4:4 | F#4:8 G4:2 F#4:2 G4:4 | G4:12` and the Diskant hovers A4-C5 above it in sixths. It happens again in b54-56 (Alt `G4:16 | G4 A4 F#4 G4 | Bb4 F4 G4 C4`).

**Why it fails.**
- In Bach's BWV 653b and in Reincken's fantasia, the manual voices keep working the line's motif while the cantus sounds. Here the subject disappears the moment the pedal enters.
- So each line is heard as "a fugato, then a chorale with accompaniment".
- The pedal canon gets chords around it rather than counterpoint, which is the washed-out quality the reset was meant to remove.
- Stepping back for the cantus is right. Standing still is not.

**Fix (tested), b15-17 as the model.** Give the Alt the dotted 3+1 limp of S2, on the chord tones it already has:

```
X('A', 13, 4, 'F#4:4 F4:4 Eb4:4 D4:4 G4:4 G4:4 G4:4 F#4:4 F4:4 G4:4 G4:4 F#4:4 G4:4 '
              'F#4:4 F#4:4 G4:4 F#4:4 G4:4 F#4:8 G4:4')
→
X('A', 13, 4, 'F#4:4 F4:4 Eb4:4 D4:4 G4:4 G4:3 F#4:1 G4:3 A4:1 F#4:4 F4:4 G4:3 F4:1 Eb4:3 F4:1 F#4:4 G4:4 '
              'F#4:3 E4:1 F#4:4 G4:4 F#4:4 G4:4 F#4:8 G4:4')
```

- Critic: no new warnings. Repeated notes fall from 4.9 % to 4.4 %, and the bad doublings stay at 1.
- There are two more "7th not resolved down" notes at 15.2: the G4 over A3 reaches F♯4 by way of A4.
- My first draft (B♭4 at 16.2) doubled the seventh of Cm7/B♭, and an E4→D4 at 17.3 made fifths with Pedal II. Both are avoided here.
- The same treatment would suit the Alt in b7-8 and b55-56 (not tested).

## 2. Line 5's syncopes have no beat (Medium)

**What is written.**
- After the echo passage, at a new tempo (♩ = 74), the Tenor is alone (1:23):

  ```
  b25  G3:2 A3:4 Bb3:4 C4:2 Bb3:2 A3:2~
  b26  A3:2 Bb3:4 A3:4 G3:6
  ```

- The Alt enters at 26.2 with the same shifted rhythm (`G4:2 A4:4 Bb4:4 C5:2`). Both voices attack A at 26.2½ (A4/A3) and move in the same phase.
- Between 25.1 and 27.3 every attack on a beat is a short note: the Tenor's G3 (25.1) and B♭3 (25.4), the Alt's G4 (26.2), and both voices at 27.1. Every long note starts half a beat late.

**Why it fails.**
- A syncope is heard only against a beat. Alone, "short-long-long-short-short-long" is heard as an eighth-note upbeat followed by plain quarters, with the bar line an eighth later than written.
- By the time Pedal II enters on the real beat (G2 at 27.3), the ear has adopted the shifted beat. The pedal sounds syncopated: the opposite of "every note hangs across the beat".

**Fix (tested).** A plain quarter-note pulse in the Alt for one bar, before its own entry (it rests at 26.1 and enters at 26.2 as now):

```
X('A', 25, 1, 'D4:4 F4:4 D4:4 F4:4')     # insert before the Alt's S5 entry
```

- Every attack is consonant with the Tenor: G3/D4, A3/F4, B♭3/D4 and B♭3/F4. The Tenor's C4 at 25.3½ is an unaccented neighbour against D4.
- Critic: no new flags. Variants tested and rejected:
  - `D4 F4 G4 F4`: fifths G4/C4 → F4/B♭3 at 25.4;
  - `D4 F4 D4 Eb4`: an appoggiatura flag.
- The cost is that the Tenor's entry is no longer solo. It keeps the bass and the dynamic lead, and the syncopation becomes the subject's character instead of a misreading.

## 3. The closest canon (Low-Medium)

**What is written.** Line 10 in half notes, Pedal I 1½ beats behind at the octave (60.3-66). The intervals between the pedals on the beats are:

| 61.3 | 62.1 | 62.4 | 63.1½ | 63.3 | 64.1½ | 64.3 | 65.1 | 66.1 |
|---|---|---|---|---|---|---|---|---|
| 7 | M7 | 7 | 7 | 9 | **m9** | M7 | **m9** | 9 |

Each lasts until Pedal I reaches the leader's note an octave higher, and that octave then lasts half a beat.

**Assessment.**
- This is the ladder's intended end ("a shadow one and a half beats behind"). It will be heard as a bass whose upper octave arrives late, not as a canon.
- In the D2-D4 register on a piano, the held minor 9ths (A2/B♭3) are rough.

**Recommendation.** Do not change the canon. If the render is muddy, soften Pedal I from 60.3 to the end. This is performance data, written after `build_score` as `soften_echoes` already is:

```
for e in voice['events']:          # voice['name'] == 'Pedal I'
    if 238 <= e['t'] < 272: e['v'] = max(24, e['v'] - 6)
```

The audible canons are lines 1, 6 and 8. If the shrinking distance is meant to be followed, NOTES could say that the last rung is a sound, not a canon.

## 4. Masked canon entries in line 2 (Low)

**What is written.**
- The Alt's S2 starts on A4 at 12.2 while the Tenor sings A3 (an octave).
- The Diskant's starts on A5 at 13.1 while the Alt sings A4.
- The canon at three beats makes every entry begin on the note of the voice before.
- Both entries are recognisable from their second note, the dotted rise B♭–C–D against the falling voice.

**Fix.** Voicing only: +6 for the Alt in b12 and the Diskant in b13.

## 5. The guest is bare and is never echoed (Low)

**What is written.**
- At 58.3-58.4½ the Diskant (`Eb5 C5 F4 F5`) sounds over Pedal II alone (`C2 Eb2 F2`), four octaves below, because the Alt rests while the subject dips.
- At 59.4 the Diskant's `D4 D5` sounds over Pedal II's D3: bare octaves.

**Assessment.**
- The quotation is heard. That was the point of moving it from Pedal I to the top.
- As music it is pasted in: a circle of fifths in the pedal, then line 10.
- I tried an Alt G4 at 58.3. It makes fifths with Pedal II (A4/D2 → G4/C2), so I would leave the texture.
- A later echo of the guest's head would make the visit part of the piece. One place: the Tenor's entry at b64 (`G4:8 F4:8 | D4:16~`), which is free. Not tested.

## Smaller points

- **Pedal I's first dissonance (8.1½).** Pedal I's E♭4 enters off the beat against the Alt's held F♯4 and Pedal II's D3. That is an augmented second inside a D chord, in the middle of the keyboard, for an eighth.
- **Line 9 (54.3½).** B♭3 over A2, with G4 and E♭5 above.
  - Both of these are the strict canon's anticipations, and NOTES lists them.
  - They are the places to listen to first in the render.
- **"Line 10 at three speeds" (NOTES §6).** It is two speeds, the eighths of S10 and the half notes of the pedals, plus the canon.
- **Stops.** The piece stops on purpose before line 8 (45.4: one beat of silence) and in the general pause (b39.3-40). Elsewhere a pedal note bridges each join. That is right for a chorale fantasia.

## Better than the seventeen-voice version?

**Yes, clearly.**

| | 17 voices | 5 voices |
|---|---|---|
| pitch class tripled on beats | 20.0 % | 6.9 % |
| bad doublings | 8 | 1 |
| crossings | 28 | 1 |
| low-register seconds | 7 | 2 |
| keyboard unplayable | 19.2 % | 6.5 % |

- **The canon.** It was at irregular distances (10, 7, 9, 3 … beats) under three manual divisions. It now shrinks steadily, and the follower has its own register.
- **The guest.** It moved from Pedal I, two octaves down, where it was almost certainly inaudible, to the top.
- **Lost:** the old summit's return of every subject. The new summit is thinner (NOTES says so). With fix 1 the manual voices would at least be counterpoint all the way to it.
