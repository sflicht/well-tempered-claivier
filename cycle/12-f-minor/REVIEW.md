# Pair XII in F minor: review of the five-voice recomposition

**Scope.**
- `fugue.py` → `fugue.json`: *Fuga a 4 soggetti, compiuta*, 66 bars, five voices (S A T B + Quinta vox).
- `prelude.py` → `prelude.json`: the new Prelude XII, *The name, three times*, 16 bars, three voices.
- `NOTES.md`, and for comparison `archive-n-plus-1/` (thirteen voices, 88 bars).

**Method.**
- I read every bar of both scores as the literal bar strings stored in the JSON, voice by voice, with the declared entries marked, and ran `critic.py` and `reduce.py --per beat`.
- Scratch scans:
  - per section: notes per bar, share of eighth slots with an attack, share of onsets where three or more voices attack together;
  - for every declared entry: where it lies in the texture (top, inner, bottom), what sounds and what attacks with it, its velocity against the others;
  - real times from `renders/fugue.mid`, tempo map applied.
- **Piano decay.** The main render is the FluidR3_GM piano. I rendered held notes with the same soundfont: an F2 at velocity 85 loses about 10 dB in 2 s, 31 dB in 10 s, 43 dB in 15 s and 52 dB in 20 s. Long pedals on this piano do not last.
- Fixes marked **tested** were built from a scratch copy of `fugue.py` (outside the repository) and checked with `critic.py`. "No new flags" means no new parallels, unresolved dissonances, bad doublings or low-register clashes.
- I have not heard the renders.

## Verdict

**Main question: yes.** This is now clear counterpoint, and the device comes across on one piano, with one exception at the very end.

- **Each subject is introduced alone,** as in Bach's XIX:
  - S1 in the tenor (b1.3, two bars);
  - S2 in the tenor (b13.2, two bars);
  - B-A-C-H in the tenor (b26.3, two bars);
  - the main theme on top (b42.1, one beat).
- **Every later entry comes after a rest in its voice.**
- **The four subjects are four different rhythms:**
  - the main theme in halves;
  - S2 in running quavers;
  - S1 in whole notes;
  - B-A-C-H in halves with its dotted turn.

  The quadruple combination (b44.3–46.3) is therefore four audible layers rather than a chord stream.
- **The dramaturgy is the best of the four recomposed fugues:**
  - the music breaks off on C7 at b49, as Bach's manuscript breaks off;
  - two beats of silence follow;
  - the alto sings the main theme alone;
  - a bar later the silent fifth voice enters beneath it with the theme in augmentation.

  In that thin texture (b50–56, 4.6 notes per bar) the augmentation is easy to follow.

What will disappoint:

1. **The ending sounds in first inversion.** The Quinta vox's F2 is struck once at b59.1 (3:20 in the render) and held for 30 s. By the coda's B-A-C-H (b63.3, 3:36) it is about 45 dB down. By the Picardy chord (b66.1, 3:47) it is about 58 dB down: gone. The final chord is heard as A3 F4 C5 C6, a tonic six chord, approached from C/G.
2. **The climax repeats IV at the same pitch.** Section V (b57–63) restates IV's quadruple combination:
   - the main theme on top at the same pitch;
   - S2 at the same pitch;
   - the same vertical alignment, so the same pitch classes beat by beat.

   What the fifth voice adds there is mostly that decaying pedal.
3. **The pair is slow.** An Adagio chorale at ♩ = 54 is followed by a Grave fugue: about five minutes of slow music, with long thin stretches.

## Ranked issues

| # | Mvt | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|---|
| 1 | Fugue | 59–66 | The Quinta vox pedal F2 decays to nothing on piano; the coda's harmonies and the Picardy chord are heard without their bass, the last cadence as C/G → F/A | **High** | **Tested.** Re-strike the pedal at the coda and at the final chord: `F2:124` → `F2:72 F2:40 F2:12` |
| 2 | Fugue | 57–63 | V repeats IV's top two lines at the same pitch and harmony; B-A-C-H (alto C5) and S2 (tenor C5) strike the same key at 60.1 | **Medium-High** | **Tested.** Exchange the main theme and S2 in V: S2 on top an octave higher, the main theme in the tenor; three small free-voice changes |
| 3 | Fugue | 34.3–38.1 | In Bach's triple combination, B-A-C-H (tenor A♭3–C4) sits a third to a sixth above S1 (bass E♭3–G3), under an empty octave and a half (C4–E♭5); it is also the quietest of the three entries | Medium | Voicing: tenor +6 velocity for its S3 entry (b34.3–38.1), bass −3 |
| 4 | Both | whole pair | About 104 of 232 s of the fugue are long-note, thin textures, there are five ritardandi, and the prelude is an Adagio: five minutes, all slow | Medium-Low | Prelude ♩ = 54 → 63 (tempo map scaled); leave the fugue's tempi |
| 5 | Fugue | 54–56 | After the alto's main theme ends (54.1) the canon dissolves into held chords: E°7 for a whole bar (55, `Db4:16 / G3:16 / E2:16`) | Low | Leave it, or give the tenor `Db4:8 Bb3:8` in b55 (tested; it adds one critic note: the D♭ leaves by leap) |

---

## Fugue XII

### Must not be touched

- **The break-off and the fifth voice, b48–51.** These are the piece's best idea, and audible:
  - iv6 – V7 and the stop on C7 (`Bb4:8 / E4:8 / C3:8`, then silence);
  - the alto's main theme alone;
  - the Quinta vox entering on F2 one bar later, in notes twice as long.
- **The exposition of each subject alone, b1–41.** It is the clearest stretch of fugal writing in the four pieces reviewed here:
  - the stile-antico entries 2, 3 and 2 bars apart;
  - the S2 duet (b15–18);
  - B-A-C-H answered in two-voice stretto with its 2–3 bass suspension and its diminished fifth resolving inward (b29).

### 1. b59–66: the pedal has gone by the time it matters (High)

**What is written.** The augmentation ends at b59.1, and its last note is held as `F2:124`. That is seven and three-quarter bars, 30.3 s in the render (199.9 s → 230.2 s). Everything from b61 to the end is written as harmony over this F:

- the coda's V7 → V7/iv → iiø4/3 → vii°7/V (b63.3–65.1);
- the C chord at 65.3;
- the Picardy chord at 66.1, whose third is the *bass voice's* A3.

**What a piano does.** Measured with the render's soundfont, the F2 is about 45 dB below its attack when the soprano begins B-A-C-H (16 s later). It is about 58 dB below at the last chord (27 s later). The other notes of that chord are struck fresh at velocity 68–70. So the listener hears:

- 63.3: C7 with C4 in the bass, root position, not "V7 over the tonic pedal";
- 65.3: C6 C5 E4 G3, a C chord over G;
- 66.1: C6 C5 F4 A3. That is F major in first inversion. The tierce de Picardie has become the bass note of a weak V6/4 → I6 close.

**Fix (tested).** Re-strike the pedal where the music needs it. In `fugue.py`, the Quinta vox theme call:

```
theme('Q', V5 + 1, 1, octv(MT_AUG, -2).rsplit(' ', 1)[0] + ' F2:124', ...)
→
theme('Q', V5 + 1, 1, octv(MT_AUG, -2).rsplit(' ', 1)[0] + ' F2:72 F2:40 F2:12', ...)
```

- The pedal is then struck at 59.1, at the start of the coda (63.3), and with the final chord (66.1).
- The critic is unchanged except for repeated notes (1.2 → 1.6 %).
- A pianist would do exactly this, or would catch the F with the sostenuto pedal (the organ in the spatial render does not need it).
- An extra strike at 61.1, where the main theme ends, would keep the pedal present through the five-subject passage as well. Optional.

### 2. b57–63: V is IV again (Medium-High)

**What is written.**

| | IV, b42–48 | V, b57–63 |
|---|---|---|
| Main theme | soprano, F5 | soprano, F5 (same) |
| S2 | alto, A♭4 | tenor, A♭4 (same pitch) |
| S1 | bass, F2 | bass, F3 |
| B-A-C-H | tenor, D♭4 | alto, D♭5 |

The four statements keep the same alignment (main theme, S2 a beat later, S1 five beats after S2, B-A-C-H four beats after S1). Every beat of V therefore has IV's pitch classes, over a pedal. The top two lines, the ones a listener follows, are identical, 57 s apart.

The octave exchange also creates the unison NOTES admits at **60.1**: B-A-C-H's second note `C5:8` (alto) and S2's `C5:2` (tenor) are the same key. On one piano, B-A-C-H's C is not struck separately. For bars 60–62 the alto (C5–F5) and the tenor (C4–D♭5) run in the same octave.

**Fix (tested).** Use the invertible counterpoint Bach would use: S2 on top an octave higher, the main theme in the tenor. In `fugue.py`:

```
theme('S', QV, 1, octv(MT, 1), 'main theme (with its augmentation)')
theme('T', QV, 2, S2, 'S2 (five voices)')
→
theme('T', QV, 1, MT, 'main theme (with its augmentation)')
theme('S', QV, 2, octv(S2, 1), 'S2 (five voices)')

put('S', QV + 4, 3, 'Db6:8')
seq('S', QV + 5, 'Ab5:8 C6:8', 'Ab5:8 R:8')
→
put('T', QV + 4, 3, 'Bb4:8')
seq('T', QV + 5, 'Ab4:8 C5:8', 'C5:4 R:12')

put('A', V5 + 6, 3, 'E4:8')
put('A', V5 + 7, 1, 'F4:4')
→
put('A', V5 + 6, 3, 'Db5:8')      # the alto no longer lands on the tenor's F4 at 57.1
put('A', V5 + 7, 1, 'C5:4')
```

**What it gives.**
- **The soprano's return.** It returns at 57.2 after a ten-bar rest with the running subject at A♭5–D♭6, the brightest texture of the piece, over the augmentation's close.
- **A new order of the subjects.** From the top, V now reads S2 / B-A-C-H / main theme / S1 / pedal, against IV's main theme / S2 / B-A-C-H / S1. Same counterpoint, new sound.
- **No more unison.** The 60.1 unison becomes an octave (C6/C5).
- **A join into the coda.** S2's last note A♭5 (63.1) steps up to the coda's B♭5 (63.3), so the signature grows out of the running subject.

**Critic, with fix 1 included.**
- parallels: 0 errors, 0 weak;
- beat-to-beat: 1 (the existing b54.1 canon octave);
- unresolved: 0;
- bad doublings: 0;
- crossings: 1 (the existing b32.2);
- keyboard: 10.0 → 10.6 %.

**Costs, honestly.**
- The main theme is no longer on top at the climax. It enters in the tenor at 57.1 together with the alto's C5 and the bass's C4.
- The alto's link becomes ii° → i6 (G2 B♭3 D♭5 → A♭2 C4 F4 C5) instead of vii° → i6. It anticipates B-A-C-H's D♭–C two bars early.

If the main theme must stay on top, keep the present layout but apply fix 1 and accept the repeat as "the same combination, now completed".

### 3. b34.3–38.1: B-A-C-H wedged on the bass (Medium)

**What is written.**
- Bass: S1 at `C3 G3 F3 Eb3 F3 G3 C3`, whole notes.
- Tenor: the B-A-C-H answer an octave down, `Ab3 G3 Bb3 A3 B3 C4 B3 A3 B3 C4`.
- Alto: S2 running in E♭5–A♭5.

The two low lines are a third to a sixth apart (b37: tenor C4 B3 A3 B3 over bass G3). Nothing sounds between C4 and E♭5. The tenor's entry velocity (72) is below the alto's (74).

**Why it matters.** This is the first time B-A-C-H is combined with anything, and Bach's own combination. On a piano, two close slow lines low in the texture fuse into a muddy dyad under a bright running line.

**Fix.** Voicing only: tenor +6 for its S3 statement (events of the Tenor from t = 134 to 148 quarters), bass −3 for the same span. Moving the tenor up an octave was considered and rejected: it lands on the bottom of the alto's run (C5 against B4 at 37.3½).

### 4. The pair is slow (Medium-Low)

**Timings from the render.**

| Bars | Duration | Texture |
|---|---|---|
| 1–12 | 40 s | 4.2 notes per bar; bars 3–5 two voices in whole notes |
| 26–31 | 20 s | B-A-C-H, two voices in half notes |
| 50–56 | 26 s | 4.6 notes per bar |
| 63–66 | 18 s | five-voice chorale in half notes |

**Ritardandi** come at b13, 26, 42, 49 and the coda. The prelude adds 71 s at ♩ = 54.

**Assessment.**
- Inside the fugue this is the stile antico of XIX, and the S2 sections (b13–25, 32–37, 42–47, 57–62) give it real motion. I would not speed the fugue up.
- The pair, however, has no fast music at all.

**Fix.** Lift the prelude, below.

### 5. b54–56 (Low)

Bar 55 is a whole-bar diminished seventh in three held voices over the augmentation's E2. It is defensible: the augmentation's leading tone should be heard.

A tenor `Db4:8 Bb3:8` in b55 gives it a breath of motion. It is tested and clean apart from a critic note that the D♭ leaves by leap.

---

## Prelude XII: *The name, three times*

A short Orgelbüchlein-style chorale:
- the soprano sings a tune made of BWV 857's cross (C D♭ C B) and the name B♭ A C B;
- the bass walks, then pulses on F.

The critic is clean in every category. The name is audible in all three places:
- inside the soprano tune (b2.3–3.2);
- in the bass in half notes as the texture thins (b9–10, +10 velocity);
- over the tonic pedal (b14).

At b14.2 the name's A♮ over the F pedal flashes F major, a quiet foreshadowing of the fugue's Picardy third.

**Must not be touched:** the name in the bass, b9–10. The walking bass stops to sing it, and that is the prelude's one memorable event.

**P1. Tempo (Medium-Low).** At ♩ = 54 the crotchet tune is a slow hymn before a Grave fugue.

Fix:
- `'bpm': 63`;
- `tempo_map`: `[[26, 63], [32, 54, 'ramp'], [32, 58], [44, 58], [48, 63], [58, 63], [64, 46, 'ramp']]`.

The prelude then lasts about 61 s, and the pair has at least one movement in a walking pace.

**P2. The alto is a pad (Low).** For example `F4:16` (b9) and `C4:16` (b15). Acceptable in a three-voice chorale. The voice exists to complete the harmony.

---

## Better than the thirteen-voice version?

**Yes, decisively.**

| | 13 voices | 5 voices |
|---|---|---|
| bars / length | 88 / 5:11 | 66 / about 3:52 |
| pitch class tripled on beats | 41 % | 3.7 % |
| crossings | 31 | 1 |
| keyboard unplayable | 26.7 % | 10 % |
| entries | 69, of which 23 are heads | 23, all complete |

**What a listener gains:**
- each subject can be learned alone before it is combined;
- each combination has one voice per subject, in its own register and rhythm;
- the extra voice has one job, which can be heard.

**What was lost:** the mirror section and the stretto finale. They were not audible in the old texture, so nothing was lost by ear.
