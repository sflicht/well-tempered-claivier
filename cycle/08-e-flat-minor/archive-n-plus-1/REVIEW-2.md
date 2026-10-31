# Pair VIII in E-flat minor: second review (third edition, as built on 27 October)

**Scope.**
- `prelude.py` → `prelude.json` (21 bars, 12/8, about 85 s);
- `fugue.py` → `fugue.json` (50 bars, nine voices, about 2:36);
- `NOTES.md`, and the first review `REVIEW.md`, whose plan this edition carries out.

**Method.** I read every bar of both sources and ran `critic.py` and `reduce.py --per beat`, plus these scratch scans (not in the repository):
- **Grid views** of every voice at quarter, eighth and sixteenth resolution.
- **Entry salience.** For each declared statement: its rank from the top among the voices sounding at its first note, how many other voices attack at the same instant, and its velocity against the others.
- **Struck semitones.** Pairs a minor second, major seventh or minor ninth apart that are attacked at the same instant.
- **Pitch-class saturation.** Sixteenth slices with five or more pitch classes. BWV 849, in five voices, has them in 1.3 % of slices.
- **Every fix below was tested.** I applied it to a scratch copy of the source, rebuilt it and re-ran the critic. Nothing in the repository was changed.

I have not heard the renders. In the fugue, `b38.2` means bar 38, quarter 2. In the 12/8 prelude, beats are dotted quarters (`b20.4` = the fourth dotted quarter).

## Verdict

**The prelude** is the right piece: the Night-loom texture Sam liked, now built on the subject's retrograde inversion. It needs one thing, a high point.

**The fugue's plan** is the strongest in this group:
- a nine-entry exposition;
- four speeds of one subject;
- a silence, then the nine-voice arrival over the subject at quarter speed;
- Bach's own subject as a guest over the prelude's melody.

**What will disappoint is local, and the fixes are small:**
1. **The final chord.** Its Picardy third arrives one beat early in the tenor, against C♭ and A♭, so the last thing heard sounds like a wrong note.
2. **The climax (b38–41).** It has seven struck semitones between neighbouring voices, three of them made by free lines. In bar 39, 13 of 16 sixteenths carry five or more pitch classes. Here the moving lines blur the harmonic arrival Sam liked.
3. **The arrival on the tonic (b42.1).** After the peak it is a diminished seventh, because of one free note.
4. **The guest.** It enters beautifully alone, but the part of Bach's subject that differs from ours is buried under three upper voices.

## Ranked issues (both movements)

| # | Mvt | Bars | Problem | Severity | Minimal fix (tested) |
|---|---|---|---|---|---|
| 1 | Fugue | 50.2 | Tenor's Picardy G4 a beat early, against C♭5, C♭3, A♭5 and A♭2 | **High** | T1 `'Ab4:4 F4:8 G4:6'` |
| 2 | Fugue | 38–41 | Struck semitones between adjacent voices at the climax; three come from free lines | **High** | Four free-line edits (F2) |
| 3 | Fugue | 42.1 | Arrival on i is E♭–G♭–A–C, because of a free A4 | **High** | A2 `'… D5:4 Bb4:4'` |
| 4 | Fugue | 46.2–47.4 | The guest's distinctive tail is masked by the descant and the augmented countersubject | Medium | S1 descant from b47; T1 louder |
| 5 | Fugue | 38–41, 25, 19 | Seven of the twelve maestrale statements, and the inner augmentations, are texture, not audible entries | Medium | Velocity shaping, or describe honestly |
| 6 | Prelude | 18–21 | No high point: the A♭5 ceiling of b5 is never exceeded; the tirade lasts one beat | Medium | b20–21 melody, below |
| 7 | Prelude | 14–17 | The soprano repeats b5–8 note for note; the new idea (the bass sings the line) is the quietest voice | Low–medium | Bass +8 in b14–17 |
| 8 | Fugue | 43.3–44 | The subito pp starts at the barline, on the third note of the C♭ subject | Low–medium | Drop the velocity from 43.3½ |

**Combined effect.** With fixes 1–4 applied together:
- The critic is unchanged: 0 parallel errors, 0 beat parallels, 2 bad doublings, 11 low-register clashes, 1 justified unresolved.
- All nine voices still move in every bar of b37–43.
- Struck adjacent semitones in b38–41 fall from 7 to 3. The three that remain are thematic against thematic.

---

## Prelude VIII

### Must not be touched

- **The texture.** A slow melody in dotted halves over a continuous eighth-note figure and a bass in dotted halves. It is what Sam liked, and the melody, the subject's retrograde inversion, gives it a real line.
- **b10–11.** The held melody note becomes a prepared seventh twice (E♭5 over F7/A, then D♭5 over E♭7/G). This is the expressive heart of the piece.
- **b21.** The bass plays the fugue's head, E♭2 B♭2 C♭3 B♭2, under a half cadence, attacca.

### P1. b18–21: no high point (Medium)

**What is written.**
- The melody's ceiling, A♭5, is reached at b5.2 in the first G♭ phrase, again at b14 and again at b20.
- The approach to the end (b18–20: i6/4 – V7 – deceptive VI – iv – V) is the dynamic peak (+6), but its top notes are G♭5 and A♭5.
- The tirade in b20 is six sixteenths from B♭4 to G♭5 and lands on A♭5, the same note as b5.

**Why it fails.** For 21 bars the line moves between E♭5 and A♭5. The loudest passage has no registral climax, so the listener hears the same ceiling three times and the piece ends where it began.

**Fix (tested).**
- b20, Melody: `'D5:6 F5:6 Bb4:1 Cb5:1 D5:1 Eb5:1 F5:1 Gb5:1 Ab5:6'` → `'D5:6 F5:6 D5:1 Eb5:1 F5:1 Gb5:1 Ab5:1 Bb5:1 Cb6:6'`.
- b21, Melody: `'Gb5:6 F5:6 Eb5:6 D5:6'` → `'Bb5:6 Ab5:6 Gb5:6 D5:6'`.
- The C♭6 is the ♭9 of V7 and resolves to B♭5 over the tonic at b21.1.
- The line still ends on the leading tone D5, and the bass head is unchanged.
- Critic: 0 parallels, 0 beat parallels, 0 unresolved.
- One cost: two onsets in the tirade need a wide stretch (B♭2–F4 in the left hand).

### P2. b14–17: the reprise repeats the soprano and hides the bass (Low–medium)

**What is written.**
- The soprano of b14–17 is b5–8 note for note (`Gb5:12 Ab5:6 F5:6 | Eb5:12 Db5:6 Cb5:6 | …`). It is the third hearing of the same shape in 17 bars: 12 of the 21 bars carry this line.
- The new idea is underneath: the bass sings the retrograde inversion in tenths with it (`Eb3:12 F3:6 D3:6 | Cb3:12 Bb2:6 Ab2:6 | …`).
- The bass has base velocity 62, the melody 70.

**Why it fails.** The listener hears "phrase 2 again", and the bass canon in tenths stays underneath.

**Fix.**
- Raise the Bass by 8 and lower the melody by 4 in b14–17.
- `dynamics` in wtclib applies one offset to all voices per bar, so this needs a per-voice velocity pass after `build_score`, of the kind Pair VI's review proposed for its ground.

### P3. Smaller points

- **b8.1.** The melody's C♭5 is the seventh of D♭7 and leaps up to G♭5. The resolution B♭4 is in the figure, which is acceptable.
- **Bass leaps.** A♭1–G♭2 in b3–4 and b4 are sevenths. They are low and fast to pass, and acceptable.

---

## Fugue VIII à 9

### Must not be touched

- **b33–37, the arrival.**
  - The vii°7 of V is held for three beats, then V, with Soprano I's head on the dominant.
  - D6 is left alone, then a full bar of silence.
  - The nine-voice E♭-minor chord follows at 37.1, with G♭6 on top and the subject at quarter speed in the bass (E♭2 | B♭2 | C♭3·B♭2 | A♭2 G♭2 | F2 D2 | E♭2).
  - This is the arrival Sam liked, now thematic. The quarter-speed bass will be heard: it is the lowest voice and it moves once a bar.
- **45.3, the guest's entry.**
  - BWV 853's subject enters with no other attack, as the top of three voices.
  - Below it are the bass's retrograde inversion on E♭3 and the baritone's G♭3.
  - Its head (E♭ B♭ C♭ B♭ A♭ G♭) is heard clearly, and the long B♭ tells the knowing listener whose subject it is.

### F1. b50.2: the Picardy third arrives a beat early (High)

**What is written.**
- Tenor I has `'Ab4:4 F4:4 G4:10'` from 49.4, so G4 is struck at 50.2.
- At that beat the V9 over the tonic pedal is still sounding: Alto II C♭5, Baritone C♭3, Alto I A♭5, Bass I A♭2, Soprano II F5, Tenor II D4. Soprano I has just moved from C♭6 to B♭5.
- The vertical is E♭2 A♭2 C♭3 D4 **G4** C♭5 F5 A♭5 B♭5.
- The real arrival, with Alto I's A♭5→G5 and everyone else, is at 50.3.

**Why it fails.**
- G♮ against two C♭s is a diminished fourth, and against two A♭s a minor ninth.
- It comes one beat before its chord, in the final ritardando (about ♩ 65 here). That beat lasts about a second, on the last chord of the piece.
- It will sound like a wrong note in the tenor.

**Fix (tested).** `put('T1', 49, 4, 'Ab4:4 F4:4 G4:10')` → `'Ab4:4 F4:8 G4:6'`. G4 now arrives at 50.3 with Alto I's G5. The Picardy third is doubled at the octave in inner voices, which is acceptable on a final chord.

### F2. b38–41: struck semitones in the climax (High)

**What is written.** These are attacked together, in neighbouring voices:

| Where | Notes | Source |
|---|---|---|
| 38.1 | A1 G♭4 against A2 F4 **and** T1 F4 | A1 inversion (thematic); A2, T1 free |
| 38.2 | S1 G♭5 / S2 F5 | both thematic (rectus and inversus two beats apart) |
| 38.3 | A1 D5 / S2 E♭5 | both thematic |
| 39.2 | A2 B♭4 / A1 C♭5 | A2 thematic; A1 free (`'Cb5:8 R:4 Bb4:4'`) |
| 39.4 | T2 C4 / B1 D♭4 (and S2 D♭5) | both thematic (B♭-minor answer against the G♭-major augmentation) |
| 41.4 | A1 F5 / S2 G♭5 | A1 thematic; S2 free (its long line anticipates the tonic's G♭) |

Pitch-class saturation is high here too: bar 38 has five or more pitch classes in 8 of 16 sixteenths, bar 39 in 13 of 16.

**Why it fails.**
- This is the passage whose harmony Sam liked in the old version. The inner lines were the right thing to add.
- But every free note that lands a semitone from a thematic one, at f, in the middle register, is a collision that sounds like a mistake.
- The thematic rubs are the price of the stretto. The free ones are not.

**Fix (tested together).** The critic is unchanged and all nine voices still move in every bar of b37–43.
- A2 b38: `'F4:4 Ab4:4 R:4 Bb4:4'` → `'R:4 Ab4:4 R:4 Bb4:4'`.
- T1 b37: `'Eb4:16 F4:8'` → `'Eb4:16 D4:8'`.
- A1 b39.2: `'Cb5:8 R:4 Bb4:4'` → `'Gb5:8 R:4 Bb4:4'`.
- S2, the long line from b39: end `'… Bb5:4 Ab5:4 Gb5:4'` → `'… Bb5:4 Ab5:8'`.
- S2 b42: `'Eb5:4 Gb5:12'` → `'Gb5:16'`.

With the last two edits, the seventh A♭5 is held over V7 and resolves to G♭5 on the downbeat of 42, instead of anticipating it against Alto I's F5.

**What remains.** Three thematic rubs remain (38.2, 38.3, 39.4). If they sound harsh, use balance rather than notes: Tenor II and Bass I 6 softer in b39.

### F3. b42.1: the arrival after the peak is a diminished seventh (High)

**What is written.**
- At 42.1 the bass has E♭2, with E♭3, G♭3, G♭4, E♭4, E♭5 and G♭5 above it.
- Two more notes sound with them:
  - Soprano I's C6, a passing note of its answer on B♭;
  - Alto II's **A4**, a free note, the end of `'Gb4:8 Bb4:8 F5:4 D5:4 A4:4'`.
- E♭–G♭–A–C is a diminished seventh over the tonic bass. The plain tonic comes only at 42.4.

**Why it fails.** The peak (G♭6 at 41.3, over vii°7) has to resolve, and the listener needs E♭ minor at 42.1. The NOTES already suspect it "may sound brighter than expected". It will sound unresolved.

**Fix (tested).** Alto II: `'Gb4:8 Bb4:8 F5:4 D5:4 A4:4'` → `'Gb4:8 Bb4:8 F5:4 D5:4 Bb4:4'`. Soprano I's C6 and A5 then pass over an E♭-minor chord, as colour, not as a new harmony.

### F4. b46.2–47.4: the guest's own part is masked (Medium)

**What is written.**
- BWV 853's subject (Tenor I, from 45.3) differs from ours only after its sixth note. The B♭4 is held a dotted quarter, then come A♭ G♭ A♭ B♭ | E♭ A♭ G♭ F E♭.
- At 46.2 three voices start above it at once:
  - Soprano I's descant, G♭6;
  - Soprano II's subject at half speed, E♭5;
  - from 46.3, Alto I's countersubject at half speed, in eighths: B♭5 A♭5 G♭5 F5 E♭5.
- Alto I moves in the same rhythm and contour as the guest, an octave and more above it.

**Why it fails.** What the ear follows is Alto I. The tenor becomes an inner voice exactly where it stops being our subject and becomes Bach's.

**Fix (tested).**
- Delay the descant by a bar: `put('S1', 46, 2, 'Gb6:8 F6:4 Eb6:12 R:4 D6:4')` → `put('S1', 47, 1, 'Eb6:12 R:4 D6:4')`. The critic is unchanged; bar 46 has five moving voices instead of six.
- With a per-voice velocity pass, also give Tenor I +10 in 45.3–47.4 and Alto I −4.

### F5. Lines or texture? The nine voices, and the advertised device (Medium: describe honestly)

**Exposition (b1–13).** Every entry is audible. Each one enters either as the new top or new bottom voice, or into a held note:
- Tenor I alone;
- Alto I as the top of two;
- the Baritone and Bass I as the new bass;
- Soprano II, then Soprano I, as the new top;
- Bass II on E♭2.

The exception is Alto II's answer at b10.3, third of six voices.

**Middle (b13–31).** Five or six voices. Outer lines and new entries are heard; the augmentations in inner voices are not:
- Tenor II's a♭ subject at b25.1 is fourth of five, in quarters and halves;
- Alto II's countersubject at half speed (b19.2) is third of five.

The diminution "dance" (b22–24) will be heard as a change of surface.

**The stretto maestrale (b37–42).** Six things will be heard:
- the chord;
- Soprano II's subject entering into the held chord at 37.2 (no other attack);
- Alto I's mirror at 37.3 and Soprano I's at 37.4;
- the quarter-speed bass;
- Soprano I's subject on B♭ at 41.1, with the peak G♭6.

The other seven statements will not be heard as entries: Baritone 38.1, Tenor II 38.4, Alto II 39.1, Bass I 39.2, Tenor I 40.2, Tenor II 40.3 and Alto I 41.3. Each starts fourth to seventh from the top, with four to seven other voices attacking at the same instant, and only 2–3 velocity above the rest.

**Verdict.** The climax is a moving harmonic mass between an audible bass and an audible top. Nine real lines are there on paper, five or so by ear. That is a legitimate maestrale texture, provided it is clean (F2, F3). The NOTES should not promise twelve audible statements. If a few should be heard, give each statement's first two beats +10 velocity and the free lines −4.

### F6. b43.3–44: the subito pp starts mid-subject (Low–medium)

**What is written.** The deceptive cadence is at 43.3, and the C♭ subject (Alto II) and countersubject (Soprano II) begin at 43.3 and 43.3½. But `dyn` changes only at the barline (43: 0, 44: −16). So the C♭ passage begins at the dynamic of the cadence, and the pp arrives on the subject's third note.

**Fix.** Apply −16 to Alto II, Soprano II and Bass I from 43.3½. This also needs a per-voice or sub-bar velocity pass. The C♭ moment, the one tender place in the piece, then starts tender.
