# Pair VI in D minor (third edition): notes

**Sources (literal):** `prelude.py`, `fugue.py`
**Built scores:** `prelude.json`, `fugue.json`
**Renders:** `renders/` holds PDF, MIDI, MusicXML and MP3 in Bach–Lehman temperament, plus `*-equal.mp3` in equal temperament and `fugue-spatial.mp3` (the four fugue voices on an arc, binaural, played on General MIDI church organ).
**Reviews:** `REVIEW-2.md` is the second review of the prelude and of the earlier seven-voice fugue. That fugue, with its own NOTES and renders, is kept in `archive-n-plus-1/`; the fugue below is new. `REVIEW-3.md` reviews the new four-voice fugue; what changed in answer to it is in the fugue's last section.
**Analysis scripts:** `search/` holds the inspection and search scripts used for the four-voice fugue (see "How the notes were written"). The scripts of the seven-voice version are in `archive-n-plus-1/search/`.

**Not listened to.** Everything below comes from the score and the checkers. How it sounds is Sam's call.

**Durations (from the renders):** prelude about 1:46, fugue about 2:47.
- **Prelude.** The Adagio opening, the recitatives and the fermatas are slow and free (`tempo_map`); the Allegros run at dotted quarter = 112.
- **Fugue.** ♩ = 76, with breaths at the joints of the form (see "Tempo and dynamics").

---

## Prelude VI, *Toccata con recitativo* (unchanged)

**Prelude VI, *Toccata con recitativo*.**
- A keyboard toccata that opens with the gesture of BWV 565 and runs in the triplet motion of BWV 851.
- It is twice interrupted by recitatives. These declaim the fugue subject's pitches in free rhythm, first in the right hand, then in the bass.
- It ends on a half cadence that withholds its final D. The fugue's ground begins on that D.

**Prelude.**
- **The opening of the Toccata in D minor BWV 565 (attributed to J. S. Bach).** Checked in Nov 2026 against the Bach-Gesellschaft text (BGA 1867) as typeset by the Mutopia Project (`BachJS/BWV565/ToccataFugue`, LilyPond source and MIDI). Bach states the figure three times in octaves, each an octave lower: A5/A4 with its ornament and the fall G F E D C♯ D; A4/A3 with the fall shortened to E F C♯ D; A3/A2 with the full fall. Then the pedal D, and the diminished seventh C♯3 E3 G3 B♭3 C♯4 E4 rolled up over it. Bars 1–3 here follow that, the second statement now shortened as Bach has it (it repeated the full fall before the check). The ornament is engraved there as a short trill sign on the A; it is written out here as A–G–A, the usual reading. The rhythm is fitted to 12/8. Two differences are kept on purpose: the diminished seventh is extended up to B♭5, and it resolves to D minor, the key of the Allegro that follows (Bach's resolves to D major, through the left hand's G–E–F♯).
- **The running triplets of the WTC I D-minor prelude BWV 851.**
  - This is an allusion of texture, not a quotation: a continuous three-to-the-beat right hand over a stepwise bass.
  - Bars 6, 9, 18 and 20 use a turning, stepwise figure; the other Allegro bars are broken chords.
- **The fugue's ground in the bass.** The bass of bars 6–8 walks it (D C# C B Bb A).

### Prelude: form

29 bars of 12/8. The running figure is written as plain eighths, three to the beat, because the renderer engraves tuplets badly.

| Bars | Section | Content |
|---|---|---|
| 1–4 | Toccata (Adagio) | The BWV 565 figure in octaves, three statements a register lower each time, the second shortened (A–G–A, E F C♯ D) as in Bach; a diminished seventh rolled up over D2, resolved to D minor. |
| 5–12 | Allegro | Running triplets over a tonic pedal, then the bass walks the lament (D C# C B Bb A). The run is cut off by C#°7/G (fermata). |
| 13–15 | Recitativo I | Right hand: A Bb B C C# D C# E D A in free rhythm, over chords (Dm/F, Bb, A7/G, A, Dm, F). It ends on A over F: the music turns to F major. |
| 16–23 | Allegro | F major, a fifths sequence, Bb → E7 → A minor, halted on E. |
| 24–26 | Recitativo II | Left hand (the bass): the subject at the E level, E F F# G G# A G# B A E, under right-hand chords (Am, F, D/F#, G, E, Am, E, A). It ends on A/E. |
| 27–29 | Presto → Adagio | Diminished-seventh cascade falling onto A1. The BWV 565 figure again, but stopping on C#: a half cadence on A (fermata), attacca. |

### Prelude: critic numbers

**Prelude** (critic, 2026-11-04):

| Measure | Value |
|---|---|
| `parallels_error` / `parallels_weak` | **0 / 0** |
| `doubling_runs` | 7: the octave statements of the BWV 565 figure (bars 1–3, 28), declared as doublings in the metadata (R.H./R.H. inner, R.H./L.H. inner, L.H. inner/L.H.) |
| `beat_parallels` | 0 (the one at b28 lies inside the same declared octave figure) |
| `dissonance_unresolved` | 0 |
| unverified | 1 (13.5½, below) |
| `bad_doublings` | 1 (28.2½, below) |
| Keyboard | **0/274 onsets exceed two hands**; max 4 notes at once; reach errors 0 |
| `stepwise_pct` | 45.2% (38% before the turn figures; 46.7% before the second BWV 565 statement was shortened) |
| `low_register_seconds` | 3: b4 (C#3 against the D2 pedal, the BWV 565 chord) and b21 (E2–D3) |

- **Doublings.** An earlier critic recognised these octave runs by itself; the current
  one exempts only pairs the score declares, and before the declaration it reported the
  same octaves as 7 weak parallels and 1 beat parallel. They are one line doubled at the
  octave, as on the organ; these three voice pairs make no other parallel in the piece.
- **28.2½, the doubled seventh.** The BWV 565 figure in octaves passes G5/G4 (32nds,
  the start of its fall G F E D C♯) over A1 and E2, so the critic reads A7 with its
  seventh doubled. It is one doubled line, and the G is a passing note of the fall.
- **13.5½, unverified.** The recitative's C5, the subject's chromatic step between B
  and C♯, sounds over B♭2 (a ninth) and moves by a semitone to C♯5 over A7/G (the
  dominant's ⁴₂), where the bass is the seventh and C♯/G a tritone, so the critic cannot
  call the step a resolution. The subject's pitches are fixed; the C♯ is the chord's third.

### Prelude: weak spots

**Prelude.**
- **Most Allegro bars are still broken chords.** Only four bars use the turning figure.
- **Still more slow than fast.** About 35 of its 106 seconds are fast (the two Allegros and the Presto); the rest is the Adagio, the two recitatives and the closing fermata.

**Both movements.** Tempo, dynamics and fermata lengths were set by reasoning about the score, not by listening.

### Prelude: changes made after the second review

| # | Issue | Change |
|---|---|---|
| 5 | Prelude mostly slow | Fermata beats ♩ 28–30 → 40–44; recitatives 72 → 84; Adagio 60 → 66; Allegros dotted quarter 100 → 112. 124 s → 106 s. |
| 6 | Prelude triplets are arpeggios | Bars 6, 9, 18 and 20 rewritten as stepwise turning figures (e.g. b6 `F5 E5 D5 E5 F5 A5 G5 F5 E5 F5 G5 A5` over the lament bass). |

---

## Fugue VI a 4, *Passacaglia e fuga sopra il Crucifixus*

### Concept at four voices

Bach's D-minor fugue BWV 851 has three voices, so this one has four.

- **A passacaglia whose ground climbs.** The eight-bar Crucifixus ground passes up through the four voices, one station each: **Bass** (D minor, b1), **Tenor** (A minor, b9), **Alto** (F major, b21), **Soprano** (b45, at the dominant, at the summit). When it reaches the top, the Bass takes it back in augmentation.
- **The fugue subject is derived from the ground.** It is the ground turned upside down and in diminution. Its inversion (the *inversus*) is therefore the ground at double speed. Every fugal entry is the ground seen from another side.
- **One plan per station.** At the ground's third bar the inversus enters in another voice and runs with it in parallel compound sixths or tenths: the lament harmonised by itself at double speed. At the ground's fifth bar the subject enters in a third voice and climbs against both.
- **Episodes without the ground.** Between stations the ground stops (b17–20, b29–40), so that each new station starts after silence. These are the places where voices rest and the texture thins to two or three parts.
- **Summit (b41–56).** The ground in the Bass at half speed (16 bars); the Tenor's inversus over it at double speed (b41); the Soprano's ground at normal speed (45.2), a beat behind the Bass, so that the outer voices form a chain of 7–6 suspensions rather than one line in sixths. Then the Alto's subject (b47) and the Tenor's second inversus (49.3) enter between them. In 49.3–52.3 three speeds are present on paper, but two of them are long held notes: what is heard is the Tenor's descent under the two grounds. In 49.3–50.3 all four voices carry a form of the ground.
- **Coda (b57–64).** The subject in augmentation in the Soprano, over a D pedal, in D major. At this speed it is the ground's exact mirror at the ground's own speed: the falling lament now rises. In the B-minor Mass the Crucifixus is followed by the Et resurrexit, in D major and 3/4; this ending points to that. It is an allusion of idea, not a quotation.

### The themes

```
GROUND    D3:16 C#3:8 C3:8 B2:4 Bb2:4 A2:12 Bb2:4 G2:8 A2:24 D2:8         (8 bars of 3/4)
          D  C#  C  B  Bb  A | Bb  G  A | D
SUBJECT   A4:8 Bb4:4 B4:4 C5:2 C#5:2 D5:6 C#5:2 E5:4 D5:12 A5:4           (4 bars)
          A  Bb  B  C  C#  D | C#  E  D | A
INVERSUS  D5:8 C#5:4 C5:4 B4:2 Bb4:2 A4:6 Bb4:2 G4:4 A4:12 D4:4           (= the ground at double speed)
```

- **Ground.** The Crucifixus ground of the B-minor Mass, BWV 232 (taken from the cantata *Weinen, Klagen*, BWV 12), transposed to D: a chromatic fall from tonic to dominant, then Bb–G–A–D. The rhythm is the earlier version's (chosen by search so that the ground fits its own augmentation; see `archive-n-plus-1/NOTES.md`).
- **Subject.** The ground's exact chromatic inversion with the note values halved. `fugue.py` asserts that the inversus equals the ground at double speed.
- **Answer.** Real, at the fifth (the subject at the E level).
- **Critic's reading.** The ground is *subject inversus ×2*, the augmented ground *inversus ×4*, the coda's subject *rectus ×2*. Sixteen of the 17 labelled entries match the rhythm 9/9; the Soprano's summit ground is 8/9 (its long E is a beat shorter, see "Review"). Nine match the intervals 9/9 and eight 8/9: those eight take their closing leap the other way (see "Variant endings").

### Section map

| Bars | Section | Key | Voices | What happens | Harmony (reduce.py, abridged) |
|---|---|---|---|---|---|
| 1–8 | **Station I**: ground in the **Bass** | D minor | 1 → 2 → 3 | Ground alone for two bars. b3: inversus in the **Alto** (A4), in tenths above the Bass. b5: **subject** in the Soprano (A4). | i · i–V6 · Am/C–E/B · Gm/Bb–D/A–A · Bbmaj7–E°/G · Em/G–Am–A · A–Dm/A · Asus4–Dm |
| 9–16 | **Station II**: ground in the **Tenor** | A minor | 3 (Bass rests) | The Tenor is now the lowest voice. b11: inversus in the **Soprano** (E5). b13: **answer** in the Alto (E4). | Am · Am–E/G# · C/G–D#°7 · Dm/F–A/E–E · E–Fmaj7–Bø/D · Bm/D–Em–E · Am/E–E7–Am/E · Esus4–Am |
| 17–20 | **Episode 1** | → F major | 3 (Tenor rests) | Falling fifths with sevenths: A7–Dm, G7–C, F7–Bb, Gm–C. The Alto's sevenths fall a step a bar (G F, F E, Eb D); the Bass returns. | A7 · Dm · G7 · C · F7 · Bb · Gm · C |
| 21–28 | **Station III**: ground in the **Alto** | F major | 2 → 3 → 4 | The Soprano rests four bars, so the Alto's ground is the top voice over the Tenor alone. b23: the **Bass** returns with the inversus, in tenths *below* the ground. b25: **subject** in the Soprano (C5). First four-voice bars. | F · C/E · Cm–G/B · Bbm–F/A–Fm/Ab–C/G · Dbmaj7/F–E°7/G · Gm–C/G–F/C · C7 · F |
| 29–34 | **Episode 2**: the surface quickens | → G minor → D minor | 3 → 4 | The Soprano runs in sixteenths: a one-bar figure sequenced down a step three times, then climbing in the same cells (b32), over a Bass falling by fifths (Gm7–C7, F–Bb, Eø7–A7, Dm–Gm). The Tenor's sevenths fall a step a bar (F E Eb D C# C Bb). The Alto rests, back at b34. | Gm7 · C7 · F · Bb · Eø7 · A7 · Dm · Gm · Gm/Bb · A7 · Dm · A |
| 35–40 | **Stretto** | D minor → A | 3 → 4 → 3 | **Subject** in the **Tenor** (A3, its first fugal entry), **answer** in the Alto one bar later (E4). The Bass walks, then rests b40; the Tenor rests on b40.3. Half cadence on A; the Alto runs up a scale into the summit. | Dm · Bb · Em/G–A · Bm–A7–Dm · Bø–E/G#–A · Dm7/F–F–E7 · A |
| 41–44 | **Summit I** | D minor | 4 → 3 | **Ground in the Bass at half speed** (D, 2⅔ bars; C#). **Inversus in the Tenor** (A4) over it: ×2 and ×½ together; the Alto holds D5 and rests on 41.3 so the Tenor's descent is exposed. Alto and Soprano in quarters over the pedal. The Soprano rests b44. | Dm · E7/D · A7/D · D–Dm · A7/D · Dm · Gm/D · A/C# |
| 45–52 | **Summit II**: the two grounds, then four forms | (D minor, at A) | 1 → 4 | 45.2: the **Soprano** enters with the **ground at normal speed** (A5), a beat after the Bass's C, over the Bass alone: the outer voices fall chromatically at two speeds, offset by a beat, as a chain of 7–6 suspensions (A5/B2 → G#5, G#5/Bb2 → G5, G5/A2 → F#5). b47: **subject** in the **Alto** (D4 level). 49.3: **inversus** in the **Tenor** (D4), descending under the two grounds' long notes; all four voices carry a form of the ground in 49.3–50.3. | Am/C · E7/B · Gm/Bb–F#°7/A · Fmaj7/A–A7 · Gm/Bb · C#°7/G · A7/G · A |
| 53–56 | **Arrival** over the long A | → D major | 4 | Cadential 6/4 (b53), A7 with a flat ninth: the Soprano's B-flat (b54), the highest note of the fugue. b55.3: the Bass reaches D, the Soprano F#: D major. | Dm/A · A7 · A7(b9) · A7 · **D** |
| 57–64 | **Coda** | D major | 3 → 4 | **Subject in augmentation** in the Soprano (A4 → D5 → A5) over a D pedal. Plagal close: G in the Bass (b63), then D. The Tenor returns for the last three bars (from b62.2). | D · Gm/D · G/D · D7 · A7/D · D · A7/D · D · G · D |

### The device, and where to hear it

1. **Two speeds inside each station.** The inversus runs with the ground in parallel compound sixths (b3–6, Alto over Bass; b11–14, Soprano over Tenor). In b23–26 the pair is turned upside down: Bass under Alto, in tenths. For their first three notes the two move in rhythmic unison (in b3–4, the ground's C B Bb against the inversus's A G# G); then the faster one pulls away. Heard, this is the lament harmonised by its own diminution; it becomes recognisably the ground at double speed only at its cadence figure, a bar ahead of the ground's.
2. **The ground's climb.** Bass (b1), Tenor (b9), Alto (b21), Soprano (b45). Each station starts after silence in that voice, and in an outer position (see the next section).
3. **Stretto at one bar** (b35–36). Subject in the Tenor, answer a fifth higher in the Alto. The Soprano rests on the Tenor's first beat.
4. **The summit's speeds.**
   - b41–44: the Bass at half speed, the Tenor's inversus at double speed.
   - 45.2–49.2: **the place to hear two speeds.** The Bass at half speed and the Soprano at normal speed in the outer voices, the Soprano a beat behind, so that each of its notes is struck while the Bass holds and the two never change note together: 7–6 suspensions at 46.2–3, 47.1–2 and 47.3–48.1, then the Soprano's F#–F–E over the Bass's held A. This combination was kept from the earlier version (see "From the seven-voice version").
   - 49.3–52.3: three speeds on paper (Bass ×2, Soprano ×1, Tenor ×½). Heard: the Tenor's chromatic descent under the Soprano's long E5 and the Bass's long notes.
   - 49.3–50.3: all four voices; the Alto adds the subject, the ground's mirror.
5. **The coda.** The rising line in the Soprano is the subject at twice its normal length, the only augmentation of the subject in the piece.

### Making each station audible

- **Station I.** The Bass plays alone for two bars.
- **Station II.** The Bass rests for the whole station (b9–16), so the Tenor's ground is the lowest voice. It is also the Tenor's first note in the fugue.
- **Station III.**
  - The Alto rests on b20.3.
  - The Soprano rests b21–24, and the Bass rests b21–22, so for two bars the Alto's ground is the top voice over the Tenor alone.
  - The voices then join one by one: Bass b23, Soprano b25.
- **Summit.**
  - The Bass rests in b40, before its augmented D3, and the Tenor on b40.3, before its inversus: the summit's downbeat follows a beat of upper voices alone.
  - The Soprano rests in b44 and on 45.1. Its A5 at 45.2 is struck over the Bass's C alone: the Alto rests b45–46 and the Tenor until 45.3.
- **Velocity.** While a station sounds, its voice is played 12 above its base velocity (the usual entry boost of 5, plus 7), and the other voices 3 below. This is a pass after `build_score`; it changes no notes.
- **Fugal entries.** Each one starts after a rest in its own voice: S b5, S b11, A b13, B b23, S b25, T b35, A b36, T b41, A b47, T 49.3, S b57.

### Variant endings

Eight entries take their closing leap the other way (a fourth instead of a fifth, or the reverse). This avoids unisons and crossings where two themes end on the same note, and keeps the hands within reach. In `fugue.py` the change is the named function `last_octave`.

| Entry | Written | Instead of |
|---|---|---|
| b11 Soprano inversus | … B4 → **E5** | E4 |
| b13 Alto answer | … A4 → **E4** | E5 |
| b21 Alto ground | … C4 → **F4** | F3 |
| b23 Bass inversus | … G2 → **C3** | C2 |
| b25 Soprano subject | … F5 → **C5** | C6 |
| b35 Tenor subject | … D4 → **A3** | A4 |
| b36 Alto answer | … A4 → **E4** | E5 |
| b45 Soprano ground | … E5 → **A5** | A4 |

### Critic numbers

`python3 tools/critic.py cycle/06-d-minor/fugue.json` (critic, 2026-11-04):

| Measure | Value |
|---|---|
| `parallels_error` / `parallels_weak` | **0 / 0** |
| `beat_parallels` | **0** |
| `dissonance_unresolved` | **0** |
| `bad_doublings` | **0** |
| `low_register_seconds` | **0** |
| `stepwise_pct` / `leap_4th_plus_pct` | **66.5%** / 9.5%. By voice: Soprano 70%, Alto 77%, Tenor 67%, Bass 40%. The Bass has the ground's falling fifth and the root-position bass of three fifths sequences. |
| `pc_tripled_on_beats_pct` | 5.4% |
| `crossings` | **0** |
| `keyboard_unplayable_pct` | **0.0%** (0 of 275 onsets need more than two hands); at most 4 notes at once |
| `mean_moving_voices` | **2.95** (4 voices) |
| Onset slots with 3+ voices attacking together | 21.5% (the seven-voice version: 42%) |
| Sixteenths | 60, all in b29–33 |
| `tertian_fit_pct` | 67% (the critic's revised chord naming, Nov 2026; 50% the old way) |
| `chord (7th not resolved down)` | 28 notes (24 before the critic's revised chord naming). The chromatic ground and the inversus move sevenths by semitone or sideways (D–C# under a C, for instance), and in the sequences of Episodes 1–2 the seventh sometimes passes to another voice. None is a free dissonance; the critic classifies each as a chord member. |
| Suspensions (critic) | 10, one of them unprepared (5 before the third review: the summit's offset adds the 7–6 chain; the climbing fourth statement of Episode 2, b32, adds two) |
| Themes | 17 labelled entries, rhythm 9/9 for sixteen (8/9 for the Soprano's summit ground); intervals 9/9 for nine, 8/9 for the eight variant endings above |

**Texture by section.** "Eighth slots" is the share of eighth-note positions on which some voice attacks.

| Section | Bars | Eighth slots with an attack | Mean sounding voices |
|---|---|---|---|
| Station I | 1–8 | 50% | 2.2 |
| Station II | 9–16 | 69% | 3.0 |
| Episode 1 | 17–20 | 88% | 2.8 |
| Station III | 21–28 | 65% | 3.2 |
| Episode 2 | 29–34 | 94% | 3.0 |
| Stretto | 35–40 | 75% | 3.6 |
| Summit | 41–56 | 62% | 3.6 |
| Coda | 57–64 | 31% | 3.3 |

**Off-beat dissonances.** The critic checks beats. `search/offbeat.py` scans every off-beat attack that is not approached and left by step. It finds 24 (27 when first run; run now on the score as it was before the Nov 2026 change to b32, it also finds 24), and all are one of three kinds:
- chord sevenths: the A7, G7, F7 chain of Episode 1, and the sixteenth-note figure of Episode 2 sounding against the Tenor's held seventh;
- anticipations;
- a passing eighth that the scan cannot see because the step out is to a held note.

### Tempo and dynamics

- **Tempo.** ♩ = 76.
- **Breaths.** Ritardandi into b17 (to 68), b21 (to 64) and b29 (to 62).
- **Station III** is a little calmer, at 72.
- **Into the summit.** The half cadence in b40 slows to 60, and the summit goes at 70.
- **Arrival.** b53–55 broaden to 56 for the arrival on D major.
- **Coda.** It goes at 60 and slows to 42 over the last two bars.
- **Dynamics.** Phrase dynamics rise from quiet (Station I) through Episode 2 and the stretto to the summit (loudest at the Soprano's B-flat, b54), then fall away in the coda.

### How the notes were written

- **By hand.** Every note is a literal token string in `fugue.py`.
- **Named operations.** The only operations applied to written material are these:
  - `move`: transposition of the ground, subject and inversus to their levels;
  - `scale_rhythm`: augmentation (the summit's Bass, the coda's Soprano);
  - `last_octave`: the variant endings above;
  - `last_tie`: tying a theme's last note into the next note of the same pitch.
- **Searches.** The scripts in `search/` placed the hand-written themes against one another and scored the result: consonance on beats, then `tools/critic.py`. They only proposed; every choice was made and written by hand. They decided:
  - the inversus at the ground's third bar, in parallel tenths (`station_placements.py`: cost 0, the cleanest placement of any theme over the ground);
  - the Soprano's ground at A5 from the augmentation's fifth bar (`summit_outer.py`: cost 0, as in the earlier version), then, after the third review, delayed by a beat by hand so that the two speeds do not change note together;
  - the Alto's subject at D4 from b47 and the Tenor's inversus at D4 from b49.3 (`summit_inner_critic.py`, `summit_inner_eval.py`: of ten candidate pairs tested with the critic, one of the few with no parallels, no unresolved dissonance and no crossing that also overlaps the Soprano's ground);
  - the stretto at one bar (`stretto_pairs.py`, `stretto_mirror.py`).
- **Rejected.** A mirror stretto of subject against inversus (`stretto_mirror.py`, `stretto_diverging.py`): either the lines collide in one register, or the clean pairs need remote keys.
- **Correction.** Lines were then corrected bar by bar against `search/look.py` (a beat or eighth grid with chord names and critic flags) and `search/offbeat.py`.
- **No notes were placed or inserted by script.**

### Honest weak spots

- **The inversus at the summit's start may still be masked.** In b41–44 the Tenor's inversus runs at A4–A3 under the Alto's descant. A beat of rest before it, the Alto's rest on 41.3 and its entry boost set it apart; from b42 the Alto moves with it again.
- **The four-voice moment is short, and the three speeds are not heard as such.** All four forms of the ground sound together for only 1⅓ bars (49.3–50.3). In 49.3–52.3 two of the three speeds are long held notes (Soprano E5, Bass Bb2–G2–A2), so the ear gets the Tenor's descent, not three speeds. The search found no longer overlap without parallels or crossings. The Alto's subject there is at the G-minor level (D4), not at a tonic level.
- **The Bass's long A fades on a piano.** The augmented ground's A2 is held from 51.3 to 55.2 (about 13–15 s with the broadening), through the cadential 6/4 and the B-flat of b54. On the organ render it holds; on the piano it will have decayed before V resolves. Re-striking it would break the augmentation's rhythm, so it stays.
- **The two speeds may blend.** Inside a station the inversus moves in parallel tenths or sixths with the ground, and in the same rhythm for its first three notes. That is why it is consonant, but it may be heard as a harmonisation of the ground rather than as the ground again at double speed.
- **The stations repeat one plan.** Each has ground, inversus at bar 3, subject at bar 5. Only the voices and keys change. Each station also ends with the ground's cadence. Ties and overlaps at the joins soften the sections: the Soprano's A5 runs from b8 into b9, the Bass picks up the Tenor's last A at b17.
- **Episode 2 is still a sequence.** Its sixteenth-note figure falls a step a bar three times (b29–31); the fourth statement now climbs instead (see the self-critique pass), but the bass's falling fifths run on unchanged under all four bars.
- **The coda is spare.** For five and a half bars it has three voices (Soprano, Alto, a D2 re-struck every two bars), and the Alto mostly turns between F# and G. The piece ends on the subject's last note, A5, the fifth of the chord, on top.
- **Thin by design.** Bars 1–4 and 21–22 have two voices or fewer.
- **Bass line.** It moves by step only 40% of the time.
- **Not heard.** Tempo, dynamics and voicing were set by reasoning about the score.

### From the seven-voice version (`archive-n-plus-1/`)

**Kept.**
- The three themes, unchanged in pitch and rhythm: ground, subject, inversus.
- The migrating ground.
- The combination the second review singled out as the one a listener will plainly hear: the augmented ground in the Bass under the ground at the dominant in the Soprano, both outer voices falling chromatically at two speeds.
- Station II in the Tenor with the Bass silent.
- The arrival on D major.
- The prelude, untouched.

**Changed, and why.**

| Earlier version (7 voices) | Now (4 voices) | Why |
|---|---|---|
| The ground through seven voices, three of its stations inner voices in long notes (REVIEW-2 F3: inaudible) | Four stations, each in an outer position at its entry (Tenor as lowest voice, Alto as top voice), each after silence in that voice | Audibility comes from the texture itself, not only from velocity |
| The ground in every bar, 70 bars | Episodes without the ground (b17–20, b29–40); each voice rests after its station | The texture breathes; each new station is an entry after silence |
| Four bars of the ground alone | Two bars alone; the inversus joins at bar 3 in tenths | The double speed is heard from the start, and it is the cleanest combination the search found |
| No sixteenths until turns were added; 42% of onset slots had 3+ attacks | A sixteenth-note episode (b29–33); 22% | Less chorale, more lines (REVIEW-2 F2) |
| No subdominant region before the summit | Episode 2 goes through G minor; the summit's subject is at the G-minor level | A real tonal plan: i, v, III, iv, i |
| Three speeds together for two bars (b53–54), with dissonances the critic could not name; the two grounds changing note together | The two grounds offset by a beat as a 7–6 chain (45.2–49.2); three speeds on paper in 49.3–52.3 (heard as the Tenor's descent under two long notes), clean, plus the subject for 1⅓ bars | REVIEW-2 F4, REVIEW-3 #1 and #3 |
| Subject stretto at three levels over the dominant pedal | A stretto at one bar (Tenor, Alto) before the summit; two inner entries between the two grounds in the summit | Fewer voices: one stretto, placed where it can be heard |
| Coda: the subject in Soprano I, B-A-C-H in Alto I | The subject in augmentation in the Soprano over D (the lament inverted at its own speed); no B-A-C-H | The ending now belongs to the concept (Crucifixus → resurrexit); B-A-C-H was a garnish |
| `keyboard_unplayable_pct` 23.8%; tripling 26.6% | 0.0%; 5.4% | Four voices, kept within two hands |
| 2:51 | 2:47 | |

**The notes are new.** No notes were carried over from the seven-voice score except the themes. No script-chosen passing notes were used: the earlier version's passing-note pass is not repeated.

### Review (third review, `REVIEW-3.md`)

| # | Issue | Response |
|---|---|---|
| 1 | b45–50: the Soprano's ground and the Bass's augmentation changed note together six times, so the two speeds sounded like one line in sixths | **Adopted, as tested by the reviewer.** The Soprano enters a beat later (45.2) and gives the beat back on its long E (E5:12 → E5:8), so everything from 49.2 is unchanged. The outer voices now form a chain of 7–6 suspensions (46.2, 47.1, 47.3). The cost is the entry's rhythm match, 8/9. I also moved the Tenor's first eighths after the rest from 45.2 to 45.3, so the Soprano's A5 is struck over the Bass alone. |
| 2 | b41: the Tenor's inversus hidden under the Alto | **Adopted.** Alto b41 `D5:6 C#5:2 B4:4` → `D5:8 R:4`; the Alto's scale still lands on D5 and its C#5 returns on b42. |
| 3 | b49.3–52.3: "three speeds at once" is on paper only | **Agreed; described honestly** (concept, section map, device, weak spots). The Tenor entry is relabelled "Inversus (Tenor) under the two grounds". The place to hear two speeds is 45.2–49.2. |
| 4 | The Bass's A2 held 16 beats fades on a piano | **Accepted, as the reviewer recommends**; listed under weak spots. The organ render sustains it. |
| 5 | The station pairs sound like a harmonised lament | **Left, as the reviewer recommends** (a one-beat offset gives parallel fifths at b5.3). The description now says compound sixths in b3–6 and b11–14, tenths in b23–26, and that the pairs are heard as the lament harmonised. |

The "must not be touched" items (Station II's texture, the coda, the Bass's rest in b40 and the Alto's scale into the summit) are unchanged. All notes of the changes were written by hand in `fugue.py`. Critic after the changes: 0 parallels, 0 beat parallels, 0 unresolved, 0 bad doublings, 0 low-register seconds, 0 crossings, 0.0% unplayable; suspensions 5 → 10; stepwise 67.0 → 66.5%.

---

## Self-critique pass (Nov 2026)

**Fixed: the BWV 565 allusion, checked against a score.** Source: the Bach-Gesellschaft
edition (BGA, 1867) as typeset by the Mutopia Project, `BachJS/BWV565/ToccataFugue`
(its LilyPond source and MIDI, read note by note for bars 1–3). The three statements in
octaves, each an octave lower, the pedal D and the rolled diminished seventh over it were
right. The second statement was not: Bach shortens it to A (ornament), E F C♯ D. Bar 2 now
has that (`E4:1 F4:1 C#4:2 D4:6` in octaves, the rhythm fitted to 12/8 as in bar 1). Two
differences are kept and now described as differences: our diminished seventh climbs on
to B♭5, and it resolves to D minor, where Bach's resolves to D major (G–E–F♯ in the left
hand); the Allegro that follows is in D minor. The weak spot "the allusions are from
memory" is gone.

**Fixed: the prelude's critic table.** It said 4 doubling runs and 1 beat parallel; the
current critic counts the BWV 565 octaves as 7 weak parallels and 1 beat parallel unless
the score declares the doubling. The prelude now declares its three octave pairs
(`metadata.doublings`), so they read as 7 doubling runs, 0 weak and 0 beat parallels. The
bad doubling (28.2½, the doubled figure's passing G over A1/E2) and the unverified step
(13.5½, the recitative's C5 moving chromatically to C♯5 over A7/G) are explained under the
table.

**Fixed (optional): Episode 2 of the fugue.** Its figure fell a step a bar four times. Now
it falls three times (b29–31) and the fourth statement (b32) climbs a beat at a time in the
same sixteenth cells (A4 B♭4 C5 A4 | D5 C5 D5 E5 | F5 E5 D5 C5), against the tenor's
still-falling sevenths, and steps into bar 33's D5. Critic: 0 parallels, 0 beat
parallels, 0 unresolved, stepwise 66.5 % as before; the off-beat scan lists the same 24
spots; the `fugue.py` assertion (inversus = ground at double speed) holds.

**Declined.**
- **REVIEW-2 P3, secco recitative chords** (optional). The recitatives declaim the
  subject's chromatic pitches in long values (A4 for ten sixteenths, C♯5 for nine), and
  what makes each of them speak is the harmony under it: B♮ against the B♭ chord, C against
  B♭, C♯ over A7/G. With short chords the long declaimed notes would decay over silence
  and those clashes would go. The contrast with the toccata already comes from tempo
  (quarter = 84 against 168) and texture (two-note chords against running triplets), and
  on a piano the held chords fade under the voice by themselves. The review rated it
  optional and "fine on a piano".
- **More turning figures in the Allegros.** Twelve of the sixteen Allegro bars are
  broken chords because that is BWV 851's own figuration (triplet broken chords over a
  stepwise bass), the texture the prelude alludes to. The turning figure is kept for the
  bars that move: the bass walking the lament (6) and the turns of the two sequences (9,
  18, 20). Spread over more bars it would stop marking them.
- **The fugue's spare coda.** REVIEW-3 lists the coda among the things not to touch,
  and its spareness is the idea: the subject in augmentation, the lament turned upwards,
  rising alone over the D pedal (the piece's only augmentation of the subject). A fourth
  voice earlier would cover it.


