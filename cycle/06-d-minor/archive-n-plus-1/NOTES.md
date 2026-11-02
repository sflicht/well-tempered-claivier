# Pair VI in D minor (third edition): notes

**Sources (literal):** `prelude.py`, `fugue.py`
**Built scores:** `prelude.json`, `fugue.json`
**Renders:** `renders/` holds PDF, MIDI, MusicXML and MP3 in Bach–Lehman temperament, plus `*-equal.mp3` in equal temperament and `fugue-spatial.mp3` (seven voices placed on an arc).
**Reviews:** `REVIEW-2.md` (second review). What changed in answer to it is in the last section.
**Analysis scripts:** `search/` holds searches and inspection tools only (see "How the numbers were reached").

**Not listened to.** Everything below comes from the score and the checkers. How it sounds is Sam's call.

**Durations (from the renders):** prelude about 1:46, fugue about 2:51.
- **Prelude.** The Adagio opening, the recitatives and the fermatas are slow and free (`tempo_map`); the Allegros run at dotted quarter = 112.
- **Fugue.** It holds ♩ = 76 from the first bar through the summit. Only the coda slows (to 68), and the last six quarters breathe (to 51).

## Concept

**Fugue VI à 7, *Passacaglia e fuga sopra un basso lamentoso*.**
- An 8-bar chromatic lament ground repeats throughout.
- The fugue subject is the ground turned upside down at double speed, so every fugal entry is the ground seen from another side.
- The ground passes through all seven voices. Each time it returns, its harmony and key change.
- **Summit.**
  - The ground sounds at three speeds and on three pitch levels a fifth apart:
    - augmented in the bass, on D;
    - at normal speed in Soprano I, on A;
    - at double speed (the inversus) in Alto I, on E.
  - All three sound together in bars 53–54.
  - Then the subject runs in stretto in the inner voices.
- **Surface.** From Var. 4 one free voice per variation runs in eighths, with sixteenth turns from Var. 5. The surface quickens towards the summit, as a passacaglia's should.

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
- **Subject.** It is the exact chromatic inversion of the ground in diminution: the intervals are mirrored and the rhythm is halved (16 8 8 4 4 12 4 8 24 8 → 8 4 4 2 2 6 2 4 12 4).
- **Inversus.** The subject's inversion, used as a fugal device, is therefore the ground at double speed (`INV`; `fugue.py` asserts this).
- **Critic's reading.** The critic recognises the ground as *subject inversus ×2*, the augmented ground as *inversus ×4*, and the inversus as *inversus ×1*. All 26 labelled entries match 9/9 in intervals and rhythm.

**How the rhythm was chosen.** It came from a search (`search/s3`–`s9`). The ground had to stay consonant over its own augmentation, with a second ground at the dominant entering at the augmentation's fifth bar. That is the summit's combination (bars 49–60).

## The ground's journey

| Var. | Bars | Key | Ground in | Other entries | Harmonisation (`reduce.py`, abridged, per bar) |
|---|---|---|---|---|---|
| 1 | 1–8 | D minor | **Bass** (D3) | subject A1 b5 (A4); answer A2 b7 (E4) | bb. 1–4 ground alone; then 2–3 voices: … Dm/A, D/A |
| 2 | 9–16 | D minor | **Tenor II** (D4) | subject S2 b13; answer Bass b15 (E2) | Dm E7/D · Dm A/C# C#o · D7/C Co7 G/B · Gm/Bb Fmaj7/A A · Bbmaj7 Gm · G A · A7/E Dm/F · D7/F# Gm |
| 3 | 17–24 | F major | **Tenor I** (F4) | inversus T2 b19 (C4): the sixth voice enters by inversion; subject S1 b21 (C5), the seventh voice | F Bo7 · F/A Am C/E · Cm G7 · Gø7 F/C C · C7/Bb Dbmaj7 Gø7 · Gm7 C · C7 Fm · F |
| 4 | 25–32 | A minor | **Alto II** (A4) | inversus T1 b27 (E4); subject T2 b29 (E3) | Am Am/C Dm · Dm/F E7 · Aø7 Am7/E B · Dm7 A E/B · E Fmaj7 G7/C · Bm E7 Am · Am E7 Am/E · Am/E Am/C |
| 5 | 33–40 | G minor | **Alto I** (G4) | inversus T1 b35 (D4); subject T2 b37 (D3) | Gm/Bb Ebmaj7 · Cm D7 · G7 A · Cm G D7/C · D Ebmaj7 Aø7/Eb · Am/G Dm · D7 Gm/D · Gm |
| 6 | 41–48 | D minor | **Soprano II** (D5) | inversus S1 b43 (A5); subject T1 b45 (A3); answer T2 b47 (E3), running into the summit | Dm Bbmaj7 · Gm A7 · F Am E7 · Gm D A/E · Fmaj7/E Bb C7 · Em7 A7 Dm/A · Fmaj7/A A7 Dm · D Bb/D A7/C# |
| Summit | 49–64 | D minor | **Bass, augmented** (D3, 16 bars) + **Soprano I at the dominant** (A5, bb. 53–60) | inversus A1 b51 on E (E5); subject A2 b58 (G4); subject T1 b60.3 (A3); answer T2 b62.3 (E3) | G/D Dm · Bø7/D Fmaj7/D E7/D · A over D and C#, under the inversus's E–D#–D–C# · A7/C# · Am/C · E/B · Gm/Bb D7/A · Dm7/A A7 · A7 Dm/A Bbmaj7 · Gm/Bb C/G · A/G G°7 Am · Am Dm7/A · A7 · Dm/A · A7 Dm/A **D** (b63.3) · G/D A7/D |
| Coda | 65–70 | D (major) | tonic pedal D2 | last subject S1 b66 (A4); B-A-C-H in A1 bb. 68–70 | E7/D A/D · Dm A7/D Gm/D · G/D D · Gm/D C7/D D · D7 G/D · D |

**The ground's route.** It passes through all seven voices in turn: B → T2 → T1 → A2 → A1 → S2 → S1. The bass then takes it back in augmentation.

**Keys.** The ground visits F major and A minor (and G minor, the darkest station) before the return in b. 41.

**Harmony.** It is never repeated. The same chromatic step is read, for example, as:
- D7/C → G/B (Var. 2);
- Cm → G7 (Var. 3, in F);
- Aø7 → Am7/E → B (Var. 4, in A minor).

**Making each station audible.**
- **Velocity.** The ground voice of every station is played 12 above its base velocity, and the other voices 3 below, while it sounds (a velocity pass after `build_score`; no notes change).
- **Space at the entry.** The voice just above the ground rests on its first beat:
  - Alto I at b. 17;
  - Soprano II at bb. 25 and 33;
  - Soprano I at b. 41.
- **Soprano I's entry (b. 53).** Soprano II stops running and rests for bars 53–54.

## Form map

| Bars | Section | What happens |
|---|---|---|
| 1–8 | Var. 1, exposition I | Ground alone in the bass for 4 bars. Then subject (A1) and tonal answer at the fifth (A2). |
| 9–16 | Var. 2, exposition II | Ground an octave up in T2; subject S2, answer in the Bass. 5 voices. |
| 17–24 | Var. 3, F major | Ground in T1. T2 enters with the **inversus** (an answer by inversion, cf. *Art of Fugue*, Cp. 5); S1 completes the seven. |
| 25–32 | Var. 4, A minor | Ground in A2; inversus and subject under it. **Soprano I runs in eighths.** |
| 33–40 | Var. 5, G minor | Ground in A1; the same pair of devices, regrouped. **Soprano II runs in eighths with sixteenth turns**; Soprano I rests for three bars. |
| 41–48 | Var. 6, D minor (return) | Ground in S2. Entries in stretto: inversus, subject, answer, two bars apart. **Alto II runs in eighths.** |
| 49–64 | Summit | Soprano II runs in eighths, then sixteenths, into the three speeds of the ground (bb. 53–54). Tenor I runs in eighths (bb. 55–59) under the subject's three-level stretto (G, A, E). Arrival on D major at b. 63.3, with T2's F#3 against D2. |
| 65–70 | Coda | Tonic pedal; the last subject in S1; B-A-C-H (Bb4 A4 C5 B4 → A4) in A1 resolving into the final D-major chord. The only place where the tempo yields. |

## Devices, and allusions credited

**Fugue.**
- **Ground.** The Crucifixus ground (BWV 232 / BWV 12), transposed.
- **Fugue over a migrating ostinato.** The passacaglia-and-fugue pairing points to BWV 582. There the ground also leaves the bass, though not through every voice.
- **Subject = ground inverted in diminution; answer by inversion (Var. 3).** Both after the inversion fugues of *Die Kunst der Fuge* (Cp. 5–7).
- **Ground at three speeds at once (bars 53–54).** A prolation device in the manner of *Art of Fugue* Cp. 6–7, here applied to the ostinato, on three levels a fifth apart.
- **Surface acceleration over the ground.** After BWV 582.
- **Tierce de Picardie at the summit's arrival (b. 63.3).** It comes from the stretto answer's own F#.
- **B-A-C-H in the coda (Alto I, bars 68–70).**

**Prelude.**
- **The opening of the Toccata in D minor BWV 565 (attributed to J. S. Bach).** The mordent A–G–A, then the fall G F E D C# D in octaves, three times, each an octave lower, then a diminished seventh built up over a low D. This is written from memory of the gesture, not copied from a score. The rhythm is fitted to 12/8.
- **The running triplets of the WTC I D-minor prelude BWV 851.**
  - This is an allusion of texture, not a quotation: a continuous three-to-the-beat right hand over a stepwise bass.
  - Bars 6, 9, 18 and 20 use a turning, stepwise figure; the other Allegro bars are broken chords.
- **The fugue's ground in the bass.** The bass of bars 6–8 walks it (D C# C B Bb A).

## Prelude: form

29 bars of 12/8. The running figure is written as plain eighths, three to the beat, because the renderer engraves tuplets badly.

| Bars | Section | Content |
|---|---|---|
| 1–4 | Toccata (Adagio) | The BWV 565 figure in octaves, three statements a register lower each time; a diminished seventh rolled up over D2, resolved to D minor. |
| 5–12 | Allegro | Running triplets over a tonic pedal, then the bass walks the lament (D C# C B Bb A). The run is cut off by C#°7/G (fermata). |
| 13–15 | Recitativo I | Right hand: A Bb B C C# D C# E D A in free rhythm, over chords (Dm/F, Bb, A7/G, A, Dm, F). It ends on A over F: the music turns to F major. |
| 16–23 | Allegro | F major, a fifths sequence, Bb → E7 → A minor, halted on E. |
| 24–26 | Recitativo II | Left hand (the bass): the subject at the E level, E F F# G G# A G# B A E, under right-hand chords (Am, F, D/F#, G, E, Am, E, A). It ends on A/E. |
| 27–29 | Presto → Adagio | Diminished-seventh cascade falling onto A1. The BWV 565 figure again, but stopping on C#: a half cadence on A (fermata), attacca. |

## Critic numbers (after the second review)

**Fugue** (`python3 tools/critic.py cycle/06-d-minor/fugue.json`):

| Measure | Value |
|---|---|
| `parallels_error` | **0** |
| `beat_parallels` | 1: b37.2, A2/T1, A4/A3 → G4/G3, octaves on successive beats with a passing note between |
| `dissonance_unresolved` | **0** |
| `bad_doublings` | **2**: b45.3 (E in C7, free T2 against the soprano's inversus); b52.2 (C# in A7, both voices thematic: the augmented ground and the inversus) |
| `stepwise_pct` / `leap_4th_plus_pct` | 62.8% / 17.4% |
| Sixteenths | 14 (before: 0) |
| Eighth slots with an attack | Vars. 1–3: 44 / 67 / 67%. Vars. 4–6: 96 / 92 / 94%. Summit: 88 / 75%. Coda: 53%. |
| Onset slots with 3+ voices attacking together | 42% (before: 50%) |
| `pc_tripled_on_beats_pct` | 26.6%. Seven voices on triads must triple; doubling is judged by `bad_doublings`. |
| `low_register_seconds` | 2 (b29.2, b37.2: retardations under G3 in the subject's chromatic climb) |
| Mean moving voices | 4.76 over the whole piece; about 5.4 from b. 21 |
| `keyboard_unplayable_pct` | 23.8%: an open score for seven voices |
| Themes | 26/26 labelled entries match 9/9 |

**Prelude:**

| Measure | Value |
|---|---|
| `parallels_error` | **0** |
| `doubling_runs` | 4: the octave statements of the BWV 565 figure (bars 1–3, 28), intended |
| `beat_parallels` | 1 (b28, inside the same octave figure) |
| `dissonance_unresolved` | 0 |
| `bad_doublings` | 1 |
| Keyboard | **0/276 onsets exceed two hands**; max 4 notes at once |
| `stepwise_pct` | 46.7% (was 38% before the turn figures) |
| `low_register_seconds` | 3: b4 (C#3 against the D2 pedal, the BWV 565 chord) and b21 (E2–D3) |

## How the numbers were reached

**Hand correction.** Notes were written by hand as token strings and corrected bar by bar against `search/look.py`, a beat or eighth grid with chord labels and critic flags. `search/chk.py` rebuilds the fugue and prints the key numbers.

**Helper scripts.** These only list options; the choices were made by hand:
- `alts.py`, `fixtrip.py`: single-note alternatives that add no fault;
- `fixdbl.py`: the same for doubled sevenths and leading tones;
- `triples.py`: beats where a pitch class is tripled.

**Passing notes (first round).**
- `search/passing.py` split 38 notes in free voices into a note plus a diatonic passing note, keeping a split whenever no critic number got worse. `patch_source.py` copied them into `fugue.py`.
- The second review found two of them musically wrong (b63.3 and b64.1½) and one harsh (b38.1½); all three are reverted.
- A fourth, at b68.3, had broken the B-A-C-H motif; it is reverted too.
- Most of the rest in Vars. 4–6 and the summit have been replaced by the hand-written running lines.
- No notes were inserted by script in this revision.

## Weak spots (honest)

**Fugue: texture and register.**
- **The opening is sparse.** The ground is alone for four bars, and Var. 1 never has more than three voices. That is the price of letting the ground be heard plainly first.
- **Running lines in a crowded space.**
  - The running voices sit between other moving voices. To avoid parallels, some take an odd turn: Alto II at b44 begins with an eighth rest; Soprano I's E6 at b30 is the highest note of the piece.
  - Each line was checked by eye and by the critic, not by ear.
- **The Bass is the leapiest voice** (about 42% steps). In Vars. 2–6 it is a free harmonic bass under a ground in an upper voice.
- **Unisons on beats.** Several voices meet in brief unisons, mostly where a theme ends on the ground's own note: b22.3, b32.2, b39.2–3, b40.2, b46.3, b48.2.
- **Crossings.** Alto II stays above Alto I for 15 beats from b. 58, so that the stretto subject can enter at the G level.

**Fugue: harmony.**
- **The three speeds are dissonant where they meet.** In bars 51–54, the inversus's chromatic fall (E D# D C# C B) meets the augmented bass's C# and C. That gives chords the critic cannot name (D5 over C#3 at b52.1, for instance). All of them resolve, by the critic's rules.
- **Three speeds for only two bars.** The overlap is bars 53–54, not three bars. A start at b52 gave three bars, but put B4 against the bass's Bb2 at b55.
- **Unexplained sevenths.** Many "7th not resolved down" notes remain. The chromatic ground moves sevenths by semitone or sideways.
- **Tertian fit is about 42%.** The running lines put more non-chord tones inside the beats.

**Prelude.**
- **The allusions are from memory.** The BWV 565 opening is paraphrased, not checked against a score.
- **Most Allegro bars are still broken chords.** Only four bars use the turning figure.
- **Still more slow than fast.** About 35 of its 106 seconds are fast (the two Allegros and the Presto); the rest is the Adagio, the two recitatives and the closing fermata.

**Both movements.** Tempo, dynamics and fermata lengths were set by reasoning about the score, not by listening.

## Second review (REVIEW-2.md): what changed

**Kept, as the review asked:**
- the ground/subject design;
- the 4-bar unaccompanied ground at the start;
- the outer-voice two-speed summit (augmented bass under the soprano's ground at the dominant, bars 53–60);
- the BWV 565 opening and the withheld-D ending.

| # | Issue | Change |
|---|---|---|
| 1 | Script passing notes spoil the Picardy arrival (63.3 C6 made a D7) and clash at 64.1½ | Soprano I restored to `C#6:4 D6:8 \| B5:4 G5:4 A5:4`; 63.3 is a D-major chord again. Also reverted: 38.1½ (Soprano II `C5:4`) and 68.3 (the passing B♭ inside B-A-C-H). |
| 2 | It plods | ♩ 66 → **76**, with no slowing into the summit; only the coda yields. One free voice per variation now runs by hand: S1 in Var. 4, S2 in Var. 5 (with sixteenth turns), A2 in Var. 6, S2 into the summit (eighths, then sixteenths), T1 in bars 55–59. Eighth-slot activity is now 92–96% in Vars. 4–6 (was 67–75%). Onset slots with 3+ simultaneous attacks: 50% → 42%. Duration 3:22 → 2:51. |
| 3 | The migrating ground is inaudible | Ground voice +12 velocity, other voices −3 while it sounds. The voice above it rests on each station's first beat (A1 b17, S2 b25 and b33, S1 b41). Soprano II rests in bars 53–54 for the soprano's ground entry. |
| 4 | The three speeds meet for one bar | The inversus (A1) now enters at b51 on **E** (it was A4 at b50), so the double-speed ground sounds over the bass's D and under the soprano's A: together in bars 53–54. This is two bars, not one; see weak spots for why not three. |
| 5 | Prelude mostly slow | Fermata beats ♩ 28–30 → 40–44; recitatives 72 → 84; Adagio 60 → 66; Allegros dotted quarter 100 → 112. 124 s → 106 s. |
| 6 | Prelude triplets are arpeggios | Bars 6, 9, 18 and 20 rewritten as stepwise turning figures (e.g. b6 `F5 E5 D5 E5 F5 A5 G5 F5 E5 F5 G5 A5` over the lament bass). |
| 7 | Other passing notes | Reviewed by eye. 42.3 (T1 B♭3, accented ♭9) is kept. The rest either remain as natural diminution or were absorbed into the new running lines. |

**Bad doublings 3 → 2 along the way.** One fix each:
- b27.2: the bass now goes to E2 instead of G2;
- b37.3: Soprano I rests on the beat;
- b59.2: Tenor I and Soprano II are revoiced.

**The cost.** The new b52.2 doubling is between two themes and is kept.
