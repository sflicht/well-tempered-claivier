# Pair VI in D minor: second review (third edition, as built on 27 October)

**Scope.**
- `prelude.py` → `prelude.json`;
- `fugue.py` → `fugue.json`;
- `NOTES.md`;
- the passing-note pass: `search/passing.py` and `search/patch_source.py`, and the accepted edit list `pass_edits.json` that `patch_source.py` reads from the shared scratchpad.

**Method.** I read every bar and ran `critic.py` and `reduce.py`, plus these scratch scans:
- **Grid views** at quarter and eighth resolution.
- **Voice summary.** For each voice: how often it sounds, its register, how many of its attacks coincide with others, and how often it doubles another voice.
- **Rhythmic activity.** How often anything moves, eighth by eighth, per variation.
- **The 38 passing notes.** Each one located and checked against everything sounding at that moment.

I have not heard the renders.

## Verdict

The idea is the best-argued in the cycle so far:
- the Crucifixus ground;
- a subject that is the ground inverted in diminution;
- the ground migrating through all seven voices;
- the augmented ground under the ground at the dominant at the summit.

The surface is clean (0 parallel errors, 0 unresolved). As music for a listener, though, three things will disappoint:

1. **It plods.** In 70 bars nothing ever moves faster than an eighth (there is not one sixteenth). Half of all onset moments have three or more voices attacking together. The other fugues measure 34–41%, and BWV 849, as measured in Pair IV's NOTES, 22%. Rhythmic activity *falls* towards the summit, and the tempo map slows it further (♩ 66 → 58 → 54). Sam's three complaints meet here: "plodding", "static", "harmony not counterpoint". It is a seven-voice chorale harmonisation of a lament at Grave, for 3 min 22 s.
2. **The advertised devices are mostly inaudible.**
   - The migrating ground is an inner voice of long notes in Vars. 3–5, so on a decaying piano it will not be heard.
   - The "three speeds at once" coincide for a single bar.
3. **The script spoiled the Picardy arrival.** One of the script's 38 passing notes lands on the summit's arrival beat and turns the hard-won D major into a D7.

The prelude is lively and witty, but its own proportions are also mostly slow. The pair as a whole is about five and a half minutes, three quarters of it slow.

## Ranked issues (both movements)

| # | Mvt | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|---|
| 1 | Fugue | 63.3, 64.1½ | Script-chosen passing notes: C6 on the Picardy arrival makes it a D7; A5 at 64.1½ rubs against S2's G5 and T2's G♯3 | **High** | Revert both: S1 `C#6:4 D6:8 | B5:4 G5:4 A5:4` |
| 2 | Fugue | all, esp. 49–70 | Rhythmic stasis and block homophony. No sixteenths; eighth-level activity peaks at 75% (Var. 4), then falls to 60% (summit) and 56% (coda); 50% of onset slots have 3+ voices attacking together | **High** | ♩ = 76 not 66, without the summit slow-downs; one free voice in running eighths per variation from Var. 4, accelerating into the summit |
| 3 | Fugue | 17–40 | The migrating ground is inaudible in Vars. 3–5: inner voice, long notes, only +5 velocity | **High** | Ground voice +12 in its variation, other voices −3; the voice above the ground rests on each variation's first beat |
| 4 | Fugue | 49–60 | "Three speeds at once" coincide only in bar 53, because the double-speed inversus (A1, 50–53) ends as the soprano's ground begins | Medium | Start A1's inversus at 52 (test it), or describe the summit honestly as two speeds |
| 5 | Prelude | 1–4, 13–15, 24–26 | About 85 of the prelude's 124 s are slow. With the Grave fugue, the pair has almost no fast music | Medium | Fermata beats ♩ = 30 → 40; recitatives 72 → 80 |
| 6 | Prelude | 5–12, 16–23 | The "BWV 851" triplets are plain broken chords (`D5 F5 A5 D6 A5 F5 …`), not BWV 851's turning figure | Low-medium | Give 2–3 bars per Allegro a stepwise turn figure |
| 7 | Fugue | 38.1½ (and the other 35) | Passing-note pass: mostly natural. 19 of 38 are in the two sopranos, which now run scalar eighths. 38.1½ makes a semitone B♭4/A4 in a 7-voice chord | Low | Revert 38.1½; keep the rest |

---

## Prelude VI: *Toccata con recitativo*

### Must not be touched

- **The BWV 565 opening (1–4).** The mordent A–G–A, the run G F E D C♯ D, three times, each an octave lower, then the diminished seventh rolled up over low D. It is instantly recognisable: exactly the kind of cheeky, audible allusion the artistic direction asks for.
- **The ending (27–29).** The same figure returns and stops on C♯: a half cadence on A whose missing D is supplied by the fugue's ground. The pair is joined by a note. Keep the bass walking the ground in 6–8 too.

### P1. The pair has almost no fast music (Medium)

**The timings, from the tempo map.**

| Section | Bars | Duration | Character |
|---|---|---|---|
| Adagio opening | 1–4 | ≈ 31 s | each bar's last beat at ♩ = 28–30 |
| Recitativo I | 13–15 | ≈ 16 s | |
| Recitativo II | 24–26 | ≈ 16 s | |
| Closing toccata | 27–29 | ≈ 14 s | |
| Allegro | 5–12 | ≈ 20 s | the only running music |
| Allegro | 16–23 | ≈ 20 s | the only running music |

**Why it matters.**
- The two Allegros are the only running music, about 40 of 124 s.
- The 3:22 Grave fugue follows.
- On its own the prelude is well shaped. As half of a pair, it is the first of two slow movements.

**Fix.**
- In `TEMPO_MAP`, raise the four fermata beats (`[4.5, 30] [10.5, 30] [16.5, 30] [22.5, 28]`) to 40.
- Start both recitatives at 80 instead of 72/70.
- This saves about 12 s and keeps the gestures.

### P2. Bars 5–12, 16–23: the triplets are arpeggios (Low-medium)

**What is written.** Every Allegro bar's right hand is broken-chord eighths (`D5 F5 A5 D6 A5 F5 G5 Bb5 D6 C#6 A5 E5`). Stepwise motion is 38%, as the NOTES admit. The left hand holds half-bar or whole-bar notes.

**Why it fails.** BWV 851's figure turns by step around a melody. This one is an étude pattern, 16 bars of it.

**Fix.** In each Allegro, rewrite two or three bars as stepwise turns around the top note. For example, bar 6 over D–C♯: `F5 E5 D5 E5 F5 A5 G5 F5 E5 F5 G5 A5`. Then the ear finds a line, and the lament bass under it (6–8) becomes the counter-line it was meant to be.

### P3. The recitative chords are sustained, not secco (Low)

**What is written.** The left hand holds whole-bar notes under the declamation (`LH2='D3:24'`, `'E3:24'`).

**Assessment.** On a piano this is fine. A truly secco realisation (short chords on the beats, silence under the voice) would make the recitative speak more and contrast more with the toccata. Optional.

---

## Fugue VI (a 7): *Passacaglia e fuga sopra un basso lamentoso*

### Must not be touched

- **The thematic identity.** The ground (BWV 232/12) and its inverted diminution as the subject: every entry is the ground seen from another side. Plus the ground alone in the bass for four bars at the start (Var. 1), which teaches the listener the theme.
- **Summit, bars 53–60.** The augmented ground in the bass under the ground at the dominant in Soprano I. Both outer voices descend chromatically at two speeds: the one learned combination in this fugue that a listener will plainly hear.

### F1. Bars 63–64: the script spoiled the arrival (High)

**The rule that let it through.** Two of the 38 passing notes chosen by `search/passing.py` passed the critic because no metric got worse. Musically, both are wrong.

**63.3.**
- Before the pass, Soprano I held `D6:8` through the arrival. The pass split it into `D6:4 C6:4`.
- At 63.3, the beat where T2's F♯3 makes the tierce de Picardie over D2, under the ritardando (about ♩ 55 by then), the top voice now sings **C natural**.
- The arrival chord is D–F♯–A–C: a **D7**, a dominant of G, not a tonic.
- The goal the whole summit has been driving at sounds like a transition.

**64.1½.** The split `B5:2 A5:2` puts A5 against Soprano II's G5 (a second) and against Tenor II's G♯3, which is attacked at the same instant. The result is a three-way clash (G, G♯, A) on a weak eighth, right after the arrival.

**Fix.** Revert both. In the Soprano I string from bar 61, `'… C#6:4 D6:4 C6:4  B5:2 A5:2 G5:4 A5:4 …'` becomes `'… C#6:4 D6:8  B5:4 G5:4 A5:4 …'`, the pre-pass reading.

### F2. The whole fugue: it will plod and sound like a chorale (High)

**The measurements.**

| Bars | Notes per bar | Eighth slots with an attack |
|---|---|---|
| 1–8 | 3.2 | 44% |
| 9–16 | 9.1 | 67% |
| 17–24 | 10.2 | 67% |
| 25–32 | 13.1 | 75% |
| 33–40 | 12.6 | 71% |
| 41–48 | 12.2 | 67% |
| 49–56 | 10.1 | 60% |
| 57–64 | 11.0 | 60% |
| 65–70 | 9.7 | 56% |

- **No sixteenths at all.**
- **Homophony.** 50% of onset slots have three or more voices attacking at once. Every voice shares 68–79% of its attacks with at least two others.
- **Tempo.** ♩ = 66, broadening to 58 into the summit, 54 at the arrival, ≈ 44 at the end.

**Why it fails.** A passacaglia lives by surface acceleration over a fixed ground. BWV 582 goes from quarters to eighths to sixteenths, and the summit is its busiest place. Here the summit is the *slowest* stretch, in notes and in tempo. Seven voices moving mostly together in quarters at Grave will be heard as a long harmonisation of a lament: Sam's "harmony rather than counterpoint" complaint about the old Fugue VIII, and "plodding".

**Fix, smallest first.**
1. **Tempo.** `BPM = 76` with `TEMPO_MAP` limited to the final breath, dropping the 66→58 and 61→54 ramps. The fugue becomes ≈ 2:55, and the ground's long notes move.
2. **A running voice.** From Var. 4 on, give *one* free voice per variation continuous eighths:
   - Var. 4: Soprano I. Its line is already half in eighths after the passing-note pass.
   - Var. 5: Soprano II, the "slower descant" at bar 33.
   - Var. 6: Alto II.
   - Summit: Soprano II, its 49–56 line.

   Do it by hand, as diminution of the line already there. This is what the script's passing notes were reaching for: do it per voice, by design.
3. **Coda.** Keep it as the one place where everything slows.

### F3. Vars. 3–5: the migrating ground is not heard (High)

**What is written.**
- **Var. 2.** The ground is in Tenor II at D4, and it is the lowest voice until the bass enters at 15, so it is audible.
- **Var. 3.** The ground is in Tenor I (F4) under three upper voices, over Tenor II and the bass.
- **Var. 4.** It is in Alto II (A4) under two sopranos.
- **Var. 5.** It is in Alto I (G4) under two sopranos.
- **Rhythm.** Its notes are long throughout: the first lasts 1⅓ bars, the A two bars.
- **Velocity.** It gets the standard +5 entry boost (≈ 74, against 70–74 for the others).

**Why it fails.** On a piano, a held inner note fades under moving voices. Vars. 3–5 (24 bars, ≈ 66 s) will be heard as a five-to-seven-voice fugue with "something chromatic somewhere". The listener can follow the ground in Var. 1 (bass), Var. 2 (lowest voice), Var. 6 (Soprano II, though Soprano I's inversus is above it) and the summit. "The ground passes through all seven voices" is true on paper for the three inner stations, not by ear.

**Fix.**
- **Voicing.** Give the ground voice +12 in its variation and the other voices −3. Post-process velocities after `build_score`, as Pair III does for pans.
- **Expose each station's first note.** Let the voice directly above the ground rest on the ground's first beat in each of Vars. 3–5, so that the new station is struck into a gap:
  - Var. 3: Alto I at 17.1;
  - Var. 4: Soprano II at 25.1;
  - Var. 5: Soprano II at 33.1.

  The ear then knows where to look, and the long notes can be followed.

### F4. Bars 49–60: the three speeds barely meet (Medium)

**What is written.**
- Bass: ground ×2, bars 49–64.
- Alto I: the inversus, i.e. the ground at double speed, `I('A4')`, bars 50–53, 48 sixteenths.
- Soprano I: the ground at the dominant, from bar 53.

**Why it fails.** The double-speed version ends in the bar where the soprano's begins, on its last two notes (E4, A3). The listener hears two speeds at a time, in succession. The NOTES' "three speeds at once" is one bar long.

**Fix.**
- Move A1's inversus two bars later (52–55) so that it overlaps the soprano's first three bars. Test it with the critic first: the search tested the bass/soprano pair, not this triple.
- If it fails, describe the summit honestly. What will be heard is still strong: two speeds of the ground in the outer voices, 53–60.

### F5. The other 35 passing notes (Low)

**Where they are.** In all, 38 notes were split: S1 11, S2 8, A1 7, T1 5, A2 3, B 3, T2 1. All are eighths except 21.2 (B), 42.3 (T1) and 63.3 (S1).

**Assessment.**
- Most are off-beat eighths filling a third in the local scale, e.g. Alto I 9.3½ `D5 E5 F5`, Soprano II 18 `F5 G5 A5 Bb5 C6`. That is natural diminution, and better than the leaps it replaced.
- 42.3, Tenor I B♭3 on the beat over A2, is an accented ♭9 for a quarter. It reads as A7♭9 and is acceptable.
- **38.1½** is the one other clash worth removing. Soprano II's passing B♭4 sounds against Alto II's held A4, a semitone, inside a seven-voice chord (E3 A3 C4 A4 B♭4 E5). Revert to `C5:4`.

**A wider point.** Concentrated in the two sopranos, the pass turns their lines into scales at Vars. 3–4. Fine, but it is the texture getting busier at the top while the inner voices stay still. Fix F2's running voice should be planned with that in mind.

### Note on the seven voices

**Which are lines.** Soprano I, Soprano II, Tenor I and the bass are lines.

**Where they merge.**
- **The altos.** Alto I and Alto II share G3–A5 and cross for 15 beats from bar 58. Each spends about a third of its time within a tone of its neighbour. In the summit they will merge.
- **The tenors.** Tenor I and Tenor II overlap similarly in Vars. 4–5, where both carry themes under the ground.

**Verdict.** Seven voices exist and move independently in pitch. Rhythmically they mostly move together. Fixes F2 and F3 are what would let the listener hear seven parts.
