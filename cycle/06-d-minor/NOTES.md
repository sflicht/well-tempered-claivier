# Pair VI in D minor (third edition): notes

**Sources (literal):** `prelude.py`, `fugue.py`
**Built scores:** `prelude.json`, `fugue.json`
**Renders:** `renders/` holds PDF, MIDI, MusicXML and MP3 in Bach–Lehman temperament, plus `*-equal.mp3` in equal temperament and `fugue-spatial.mp3` (seven voices placed on an arc).
**Analysis scripts:** `search/` (searches and inspection only; they write no notes into the scores, except `patch_source.py`, which copies accepted passing notes into `fugue.py` as visible token edits, see below).

**Not listened to.** Everything below comes from the score and the checkers. How it sounds is Sam's call.

**Durations (from the renders):** prelude about 2:04, fugue about 3:22. Both use `tempo_map`. The prelude's toccata and recitatives are slow and free, and its fermatas are slowed beats. The fugue broadens into the summit (bb. 45–49, q 66 → 58), presses on slightly when the ground enters in the soprano (b. 53, q 61), broadens again into the Picardy arrival (bb. 62–63, q 54), and slows to about 75% over the last six quarters.

## Concept

**Fugue VI à 7, *Passacaglia e fuga sopra un basso lamentoso*.**
- An 8-bar chromatic lament ground repeats throughout.
- The fugue subject is the ground turned upside down at double speed, so every fugal entry is the ground seen from another side.
- The ground passes through all seven voices. Each time it returns, its harmony and key change.
- At the summit the ground sounds at three speeds at once:
  - augmented in the bass;
  - at double speed (the inversus) in Alto I;
  - at normal speed in Soprano I, at the dominant.
  - Meanwhile the subject runs in stretto in the inner voices.

**Prelude VI, *Toccata con recitativo*.**
- A keyboard toccata that opens with the gesture of BWV 565 and runs in the triplet motion of BWV 851.
- It is twice interrupted by recitatives. These declaim the fugue subject's pitches in free rhythm, first in the right hand, then in the bass.
- It ends on a half cadence that withholds its final D. The fugue's ground begins on that D.

## The two themes

```
GROUND  D3:16 C#3:8 C3:8 B2:4 Bb2:4 A2:12 Bb2:4 G2:8 A2:24 D2:8      (8 bars of 3/4)
        D  C#  C  B  Bb  A | Bb  G  A | D
SUBJECT A4:8 Bb4:4 B4:4 C5:2 C#5:2 D5:6 C#5:2 E5:4 D5:12 A5:4         (4 bars)
        A  Bb  B  C  C#  D | C#  E  D | A
```

**The ground.** It is the ground of the Crucifixus of the B-minor Mass, BWV 232 (taken from *Weinen, Klagen*, BWV 12), transposed to D: a chromatic fall from tonic to dominant, then Bb–G–A–D.

**How the two themes relate.**
- **Subject.** It is the exact chromatic inversion of the ground in diminution: the intervals are mirrored (−1 becomes +1, the closing fall of a fifth becomes a rise of a fifth) and the rhythm is halved (16 8 8 4 4 12 4 8 24 8 → 8 4 4 2 2 6 2 4 12 4).
- **Inversus.** The subject's inversion, used as a fugal device, is therefore the ground at double speed (`INV`; `fugue.py` asserts this).
- **Critic's reading.** The critic recognises the ground as *subject inversus ×2*, the augmented ground as *inversus ×4*, and the inversus as *inversus ×1*. All 26 labelled entries match 9/9 in intervals and rhythm.

**How the rhythm was chosen.** The ground's rhythm (and thus the subject's) came from a search (`search/s3`–`s9`). The ground had to be consonant over its own augmentation, with a second ground at the dominant entering at the augmentation's fifth bar. That is the summit's combination (bb. 49–60).

## The ground's journey

| Var. | Bars | Key | Ground in | Other entries | Harmonisation (`reduce.py`, abridged, per bar) |
|---|---|---|---|---|---|
| 1 | 1–8 | D minor | **Bass** (D3) | subject A1 b5 (A4); answer A2 b7 (E4) | bb. 1–4 ground alone; then 2–3 voices: … Dm/A, D/A |
| 2 | 9–16 | D minor | **Tenor II** (D4) | subject S2 b13; answer Bass b15 (E2) | Dm E7/D · Dm A/C# C#o · D7/C Co7 G/B · Gm/Bb Fmaj7/A A · Bbmaj7 Gm · G A · A7/E Dm/F · D7/F# Gm |
| 3 | 17–24 | F major | **Tenor I** (F4) | inversus T2 b19 (C4): the sixth voice enters by inversion; subject S1 b21 (C5), the seventh voice | F Bo7 · F/A Am C/E · Cm G7 · Gø7 F/C C · C7/Bb Dbmaj7 Gø7 · Gm7 C · C7 Fm · F |
| 4 | 25–32 | A minor | **Alto II** (A4) | inversus T1 b27 (E4); subject T2 b29 (E3) | Am Am/C Dm · Dm/F E7 · Aø7 Am7/G B · Dm A E/B · E Fmaj7 G7/C · Bm E7 Am · Aø7 E7 Am/E · Am |
| 5 | 33–40 | G minor | **Alto I** (G4) | inversus T1 b35 (D4); subject T2 b37 (D3) | Gm/Bb Gø7 Eb · Cm7 D7 · G7 A7 · Cm G D7/C · D Ebmaj7 Aø7/Eb · Am/G Dm · D7 Gm/D · Gm7 |
| 6 | 41–48 | D minor | **Soprano II** (D5) | inversus S1 b43 (A5); subject T1 b45 (A3); answer T2 b47 (E3), running into the summit | Dm Bb · Gm A7 · F F/A E7 · Gm D A/E · Fmaj7/E Bbmaj7 C7 · Em Am · Fmaj7/A A7 Dm · D Bb/D A7/C# |
| Summit | 49–64 | D minor | **Bass, augmented** (D3, 16 bars) + **Soprano I at the dominant** (A5, bb. 53–60) | inversus A1 b50 (A4); subject A2 b58 (G4); subject T1 b60.3 (A3); answer T2 b62.3 (E3) | Dm G/D Dm · Dm E7/D · A7/D D A/C# · … Am/C · Fmaj7/C E7/B · Gm/Bb D7/A · Dm7/A A7 · A7 Dm7/A Bb · Gm7/Bb C/G · A7/G Am · Am Dm7/A · A7 · Dm/A · A7 Dm/A **D** (b63.3) · G/D A7/D |
| Coda | 65–70 | D (major) | tonic pedal D2 | last subject S1 b66 (A4); B-A-C-H in A1 bb. 68–70 | E7/D A/D · Dm A7/D Gm/D · G/D D · Gm/D C7/D D · D7 G/D · D |

The ground passes through all seven voices in turn: B → T2 → T1 → A2 → A1 → S2 → S1, with the bass taking it back in augmentation.

**Keys.** The ground visits F major and A minor (and G minor, the darkest station) before the return in b. 41.

**Harmonisation.** It is never repeated. The same chromatic step is read, for example, as:
- D7/C → G/B (Var. 2);
- Cm → G7 (Var. 3, in F);
- Aø7 → Am7/G → B (Var. 4, in A minor).

## Form map

| Bars | Section | What happens |
|---|---|---|
| 1–8 | Var. 1, exposition I | Ground alone in the bass for 4 bars. Then subject (A1) and tonal answer at the fifth (A2). |
| 9–16 | Var. 2, exposition II | Ground an octave up in T2; subject S2, answer in the Bass. 5 voices. |
| 17–24 | Var. 3, F major | Ground in T1. T2 enters with the **inversus** (an answer by inversion, cf. *Art of Fugue*, Cp. 5); S1 completes the seven. |
| 25–32 | Var. 4, A minor | Ground in A2; inversus over it, subject under it. |
| 33–40 | Var. 5, G minor | Ground in A1; the same pair of devices, regrouped. |
| 41–48 | Var. 6, D minor (return) | Ground in S2. Entries in stretto: inversus, subject, answer, two bars apart. |
| 49–64 | Summit | The ground at three speeds (see above); the subject at three levels (G, A, E) in stretto at 2½-bar distances; arrival on D major (b. 63.3, F#3 in T2 against D2). |
| 65–70 | Coda | Tonic pedal; the last subject in S1; B-A-C-H (Bb4 A4 C5 B4 → A4) in A1 resolving into the final D-major chord. |

## Devices, and allusions credited

- **Ground.** The Crucifixus ground (BWV 232 / BWV 12), transposed.
- **Fugue over a migrating ostinato.** The passacaglia-and-fugue pairing points to BWV 582. There the ground also leaves the bass, though not through every voice.
- **Subject = ground inverted in diminution; answer by inversion (Var. 3).** Both after the inversion fugues of *Die Kunst der Fuge* (Cp. 5–7).
- **Ground at three speeds at once (bb. 49–60).** A prolation device in the manner of *Art of Fugue* Cp. 6–7, here applied to the ostinato.
- **Tierce de Picardie at the summit's arrival (b. 63.3).** It comes from the stretto answer's own F# rather than from an added voice.
- **B-A-C-H in the coda (Alto I, bb. 68–70).**
- **Prelude.**
  - The opening of the Toccata in D minor BWV 565 (attributed to J. S. Bach): the mordent A–G–A, the fall G F E D C# D in octaves, three times, each an octave lower, then a diminished seventh built up over a low D. This is written from memory of the gesture, not copied from a score; the rhythm is simplified to fit 12/8.
  - The running triplet motion of the WTC I D-minor prelude BWV 851. This is an allusion of texture (a continuous three-to-the-beat right hand over a stepwise bass), not a quotation.
  - The bass of bb. 6–8 walks the fugue's ground (D C# C B Bb A).

## Prelude: form

29 bars of 12/8. The running figure is written as plain eighths, three to the beat, because the renderer engraves fractional (tuplet) durations badly. The 4/4-with-triplets draft is not kept.

| Bars | Section | Content |
|---|---|---|
| 1–4 | Toccata (Adagio) | The BWV 565 figure in octaves, three statements a register lower each time; a diminished seventh rolled up over D2, resolved to D minor. |
| 5–12 | Allegro | Running triplets over a tonic pedal, then the bass walks the lament (D C# C B Bb A). The run is cut off by C#°7/G (fermata). |
| 13–15 | Recitativo I | Right hand: A Bb B C C# D C# E D A in free rhythm, over secco chords (Dm/F, Bb, A7/G, A, Dm, F). It ends on A over F: the music turns to F major. |
| 16–23 | Allegro | F major, a fifths sequence, Bb → E7 → A minor, halted on E. |
| 24–26 | Recitativo II | Left hand (the bass): the subject at the E level, E F F# G G# A G# B A E, under right-hand chords (Am, F, D/F#, G, E, Am, E, A). It ends on A/E. |
| 27–29 | Presto → Adagio | Diminished-seventh cascade falling onto A1. The BWV 565 figure again, but stopping on C#: a half cadence on A (fermata), attacca. |

## Critic numbers

**Fugue** (`python3 tools/critic.py cycle/06-d-minor/fugue.json`):

| Measure | Value |
|---|---|
| `parallels_error` | **0** |
| `beat_parallels` | 2: b29.2 S1/T1 B5/B3→A5/A3 and b37.2 A2/T1 A4/A3→G4/G3, both octaves on successive beats with passing notes between |
| `dissonance_unresolved` | **0** |
| `bad_doublings` | **3**: b27.2 (seventh), b37.3 (seventh), b45.3 (leading tone of C7) |
| `pc_tripled_on_beats_pct` | 19.3%. With seven voices on a triad some pitch class must be tripled; the final D-major chord alone gives 3 beats. |
| `stepwise_pct` / `leap_4th_plus_pct` | 62.8% / 18.4%, from 54.9% / 19.1% before the passing-note pass (see below) |
| `low_register_seconds` | 2 (b29.2, b37.2: retardations under G3 in the subject's chromatic climb) |
| Mean moving voices | 4.81 over the whole piece; **5.5 from b. 21** (all seven voices entered); 4 bars with all seven moving |
| `longest_static_harmony_beats` | 4 |
| `keyboard_unplayable_pct` | 24.2%: an open score for seven voices, which the brief allows to be beyond one keyboard |
| Themes | 26/26 labelled entries match 9/9 (rectus, inversus, inversus ×2 and ×4) |

**Prelude:**

| Measure | Value |
|---|---|
| `parallels_error` | **0** |
| `doubling_runs` | 4: the octave statements of the BWV 565 figure (bb. 1–3, 28), intended |
| `beat_parallels` | 1 (b28, inside the same octave figure) |
| `dissonance_unresolved` | 0 |
| `bad_doublings` | 1 |
| Keyboard | **0/276 onsets exceed two hands**; max 4 notes at once; hands within a 10th |
| `low_register_seconds` | 3: b4 (C#3 against the D2 pedal, the BWV 565 chord) and b21 (E2–D3 in the left hand) |

## How the numbers were reached

Notes were written by hand as token strings. They were then corrected bar by bar against `look.py`, a beat grid with chord labels and critic flags.

Several tools helped:
- `alts.py` and `fixtrip.py` list single-note alternatives that add no fault.
- `fixdbl.py` does the same for doubled sevenths and leading tones.
- `triples.py` lists the beats where a pitch class is tripled.

**Passing notes (CONVENTIONS' stepwise target).**
- The free voices leapt too much (54.9% steps).
- `search/passing.py` looked at every leap of a third in a free voice (never in a theme) whose first note is a quarter or longer. For each, it tried splitting the note into itself plus a diatonic passing note in the local key. It kept a split only if no critic measure got worse.
- 38 such splits were accepted. `patch_source.py` wrote them into the literal strings of `fugue.py`, where they can be read as ordinary tokens (e.g. Alto I, b. 9: `D5:2 E5:2`; Soprano I, b. 63: `D6:4 C6:4`).
- The critic chose these notes; a person did not. Each one should be checked by ear.

## Weak spots (honest)

**Fugue: texture and register.**
- **The opening is sparse.** The ground is alone for four bars, and Var. 1 never has more than three voices. That is the price of letting the ground be heard plainly first.
- **Free voices are still leapier than Bach's.** 62.8% steps against Bach's 71–75%. The Bass is the leapiest voice (about 43% steps): in Vars. 2–6 it is a free harmonic bass under a ground in an upper voice.
- **Unisons on beats.** Several voices meet in brief unisons, mostly where a theme ends on the ground's own note: b22.3, b32.2, b39.2–3, b40.2, b46.3, b48.2.
- **Crossings.** Alto II stays above Alto I for 15 beats from b. 58, so that the stretto subject can enter at the G level.

**Fugue: harmony and doubling.**
- **Unexplained sevenths.** There are many "7th not resolved down" notes (59). The chromatic ground moves sevenths by semitone or sideways instead of resolving them; the critic flags these as notes, not errors.
- **Tertian fit fell to 50%.** After the passing-note pass the critic's tertian-fit figure dropped from about 61% to 50%: more non-chord tones now fall inside the beats. This was not a target measure, but it shows that the texture got busier.
- **Three bad doublings remain** (b27.2, b37.3, b45.3). No single-note change fixed them without adding a fault. At b. 45 the doubled E is between a free voice and the soprano's inversus.

**Prelude.**
- **The allusions are from memory.** The BWV 565 opening is paraphrased, not checked against a score. Its rhythm is regularised for 12/8.
- **The running figure is arpeggio-built** (prelude `stepwise_pct` about 38%). That is typical of toccata figuration but plainer than BWV 851's.

**Both movements.** Tempo, dynamics and the fermata lengths were set by reasoning about the score, not by listening.
