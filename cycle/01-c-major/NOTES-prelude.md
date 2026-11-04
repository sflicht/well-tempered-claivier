# Prelude I in C major — *Praeludium per omnes tonos*

57 bars, 4/4, ♩ = 70, about 3′18″. Source: `prelude.py` (composition) and
`shepard.py` (orchestration). Build with `python3 cycle/01-c-major/prelude.py`.

| file | what it is |
|---|---|
| `prelude-notation.json` | the written core: 4 staves (Cantus, Figure, Tenor, Bass) → `renders/prelude-score.pdf` |
| `prelude.json` | the performance score: the same notes, pedalled and sounded in octave layers (39 monophonic voices) |
| `renders/prelude.mp3` | performance, Bach–Lehman temperament |
| `renders/prelude-meantone.mp3` | performance, ¼-comma meantone (the demonstration of why the WTC needed a well-tempered keyboard) |
| `renders/prelude-equal.mp3` | performance, equal temperament |

I cannot hear audio. Nothing below describes how the renders sound. The
claims about register and loudness come from the score data and from signal
measurements of the rendered audio (spectral centroid and RMS per bar).

## Concept

The piece is BWV 846 with its middle replaced by the whole well-tempered
keyboard. It opens with Bach's first four bars, note for note. It then climbs
through all 24 keys in WTC order, a semitone at a time. It comes home to
Bach's first four bars again, unchanged, with a melody laid over them, and
closes with Bach's ending gesture.

**One device, made systematic.** In each major key, the dominant seventh
resolves to the *minor* tonic, or the tonic simply turns minor. So the change
of mode is a change of colour over the same root. The minor key's Neapolitan
sixth (♭II⁶) is then reinterpreted as I⁶ of the major key a semitone higher.
c minor's D♭/F *is* D♭ major. Twelve such steps raise the music an octave, and
b minor's Neapolitan is C major.

**The trick Bach could not do.** The performance sounds every written note in
octave layers under fixed loudness bells, a Shepard–Risset illusion. As the
keys rise, the upper layers fade out and the lower layers fade in. After 24
keys the music is a full octave "higher" and yet sits exactly where it began.
The da capo (bars 50–53) is note-for-note and velocity-for-velocity identical
to bars 1–4 in the performance score (64/64 notes compared). Two side effects
follow under octave layering:
- Bach's rising figure (a b c a b c, each step under a tritone in most
  voicings) becomes an endlessly rising spiral.
- The falling form (c b a c b a) becomes an endlessly falling spiral.

Major keys use the rising figure. Most minor keys from c♯ on use the falling
one, so there the small figure sinks while the keys climb.

## Key map (bar.beat; H = half-bar number used in `prelude.py`)

| | key | starts | H | how it is reached / what happens |
|---|---|---|---|---|
| I | C | 1.1 | 1 | BWV 846 bars 1–4 exactly: I – ii⁴₂ – V⁶₅ – I, one harmony per bar |
| II | c | 5.1 | 9 | tonic turns minor at the phrase seam. Royal Theme head C E♭ G A♭ B C in the top voice and, held in half notes an octave up, in the cantus (second review). Bass falls C B♭ A♭ F G C. The N⁶ is first heard in its ordinary role (6.3 → V⁷♭⁹ → i) |
| III | D♭ | 8.1 | 15 | **c: N⁶ = D♭: I⁶** — the second time, the Neapolitan does not go to V. Then I⁶ – ii⁶₅ – V⁷ |
| IV | c♯ (d♭) | 9.3 | 18 | the D♭ cadence lands minor (written D♭ minor, respelled c♯ at bar 10). i – iv – V⁷ – i, falling figure |
| V | D | 11.3 | 22 | **c♯: N⁶ = D: I⁶** for a whole bar, V⁷ with its seventh tied over, 4–3 tenor suspension into I (13.1) |
| VI | d | 13.3 | 26 | tonic turns minor (F♯→F). i – iiø⁶₅ – V⁷ – i – iv⁶ |
| VII | E♭ | 16.1 | 31 | **d: N⁶ = E♭: I⁶** (iv⁶ → N⁶ share two notes). I⁶ – ii⁶₅ – V⁷ – I |
| VIII | e♭ | 18.1 | 35 | tonic turns minor. *Lamento*: the bass descends B♭ A A♭ G G♭ F F♭, the Royal Theme's chromatic tail from 5 down to ♭2. The darkest and softest place (velocity ≈ 43–48) |
| IX | E (F♭) | 21.3 | 42 | **e♭: ♭II in root position**: the lament bass lands on F♭, the leading tone E♭ (= D♯) rises to F♭ (= E). Written F♭, respelled E at bar 22. Subito brighter |
| X | e | 23.1 | 45 | E: IV – V⁷ → i (same dominant) |
| XI | F | 24.1 | 47 | **e: iv → N⁶ over a common bass A**: only E moves, to F |
| XII | f | 25.3 | 50 | tonic turns minor (A→A♭ in the tenor). Cadential ⁶₄ over a held C (26.3–27.2) |
| XIII | F♯ (G♭) | 28.1 | 55 | **f: N⁶ G♭/B♭, written F♯/A♯**. *stringendo*: keys now pass faster |
| XIV | f♯ | 30.1 | 59 | V⁷ → i |
| XV | G | 30.3 | 60 | **f♯: N⁶ = G: I⁶**, then V⁷ only (G's cadence is left to the minor) |
| XVI | g | 31.3 | 62 | i – iv⁶ |
| XVII | A♭ | 32.3 | 64 | **g: N⁶ = A♭: I⁶** – IV – V⁷ (= D♯⁷) |
| XVIII | g♯ (a♭) | 34.1 | 67 | *Pedale*, the climax: a dominant pedal on D♯ for three bars, after BWV 846's G pedal (bars 24–31). Above it: V⁷ – i⁶₄ – V⁷♭⁹ (the colour of bar 7) – a diminished seventh with every upper voice raised a semitone – i⁶₄ – V⁷ – i |
| XIX | A | 38.1 | 75 | **g♯: N⁶ = A: I⁶** — *Arrivo*, the loudest point (velocity 100). Broad: I⁶ (a whole bar) – IV – V⁷ – I – V⁷ |
| XX | a | 41.1 | 81 | same dominant → i – V⁶₅ – i |
| XXI | B♭ | 42.3 | 84 | **a: N⁶ = B♭: I⁶** – IV – V⁷ |
| XXII | b♭ | 44.1 | 87 | V⁷ → i – i⁶ |
| XXIII | B (C♭) | 45.1 | 89 | **b♭: N⁶ C♭/E♭, written B/D♯** – ii⁶₅ – V⁷ |
| XXIV | b | 46.3 | 92 | V⁷ → i. Its N⁶ **C/E** sounds for a whole bar (47), with Bach's bar-1 notes G C E over the wrong bass: home is glimpsed, then withdrawn (→ F♯⁷ → b) |
| I | C | 49.1 | 97 | the B of b minor stays in the bass and becomes C's leading tone: BWV 846 bar 3 (G⁷/B), then bar 50 = bar 1 |

Then: bars 50–53, da capo of bars 1–4 with the cantus. Bars 54–57 close over a
C pedal: C⁷ – F/C – G⁷/C – C (BWV 846 bars 32–35).

`python3 tools/reduce.py cycle/01-c-major/prelude-notation.json --per half`
shows the 24 keys in exactly this order. Its chord names are spelled with
sharps throughout; see the tool notes below.

### Variety in the climb

The danger was a 24-fold mechanical sequence, and several things break it up:
- **Key lengths vary** from one half bar (f♯) to eight (g♯), and in-between
  lengths of 2–7.
- **Key changes fall on beat 1 or beat 3**, irregularly.
- **The colour change happens three ways**: the dominant resolves minor
  (D♭, E, F♯, G, A♭, A, B♭, B); the tonic turns minor (C, D, E♭, F); or a
  suspension delays it.
- **Approaches to the Neapolitan differ**: from i, from iv⁶ (shared notes),
  from iv over a common bass, by root position at the end of a chromatic bass,
  and after a pedal.
- **Each region has its own event**:
  - the Royal Theme over a falling bass (c)
  - whole-bar harmony (D, A, b's glimpse of C)
  - the lament (e♭)
  - the subito light (E)
  - the cadential ⁶₄ over a held bass (f)
  - the stringendo (F♯–A♭)
  - the pedal climax (g♯)
  - the false homecoming (b)

## The Shepard–Risset implementation (`shepard.py`)

Only written notes sound. The script moves them by whole octaves and pedals
them. It chooses no pitch class and no rhythm.

1. **Pedalling.** A figure note belonging to its half bar's harmony is held
   until the harmony changes or the same pitch is struck again. This is what
   fingers and pedal do in BWV 846. The pedal is also held across a half-bar
   line when the bass is not re-struck, the new notes belong to the same chord
   *and* the held note itself belongs to the new half bar: the C⁷ and F/C bars
   and the final chord. Held notes are dealt to monophonic slots.
   A **register floor** (second review) keeps tenor and figure layers out of
   the low register in the loud stretch: none below D♯3 in bars 31–40, none
   below G3 over the D♯ pedal (bars 34.3–37.2).

2. **Octave layers.** Each written note *p* sounds at every *q = p + 12k*
   from A0 to A7, with amplitude weight

   `A(q,t) = (1 − g(t))·[q = p] + g(t)·exp(−½((q − c)/σ(t))²)`.

   The variables:
   - **c**, a *fixed* centre per role: bass B♭2 (46), tenor B♭3 (58), figure
     B♭4 (70). Separate centres keep the bass heard as a bass.
   - **g**, the illusion's mix: 0 in bars 1–7 (Bach's bars and the c-minor
     Royal Theme are plain), rising from the D♭ pivot (bar 8) to 1 at bar 10,
     1 until bar 45, falling through b minor (bars 46–49), 0 from the da capo
     on. So the piece emerges from Bach's own
     register and dissolves back into it.
   - **σ**, the bell width: 7 semitones at the start, 7.5 in the lament (more
     intimate), widening to 13.5 for the pedal and the arrival on A (the whole
     keyboard), then back to 7.5. σ widens symmetrically and c never moves, so
     the spectral centre stays put.

3. **Velocity.** On this soundfont amplitude is roughly proportional to v², so
   a layer's velocity is v_written·√A. Layers under velocity 9 are dropped.
   Each (role or slot, octave) pair is one performance voice, panned slightly
   by register.

**Checks** (after the second-review changes).
- Polyphony peaks at 30 notes, well under FluidSynth's 256.
- The energy-weighted register of the performance score (velocity⁴ × duration,
  spread over the bars a note spans) is MIDI 59–62 in every bar from 9 to 47,
  except bar 36 (64: over the D♯ pedal only the pedal sounds below G3). Over the
  same span the music rises 11 semitones. Bars 1–4 and the da capo both
  measure 66.
- Spectral centroid of the Bach–Lehman render: bars 1–4 ≈ MIDI 70. Bars 10–47
  stay between 59 and 66, except the two loudest pedal bars (35–36: 70–72).
  Those are brighter because the floor leaves only the pedal below G3 and loud
  samples are bright. The mean of bars 29–47 is 2.5 semitones above that of
  bars 10–28, against the 11 semitones the keys climb. This is a residual
  drift, concentrated in the climax, not a register climb.
- RMS per bar: −33 dB at the opening, −31/−32 dB in the lament, −18 dB at the
  pedal crest and arrival (bars 37–38), and back to −33 dB before the da capo.
  This is the planned arc.

**The written score.** The written core pays back the octave quietly, through
the bass's cadential leaps (for example C3→F2 in c minor and the lament's
descent to F♭2). The notation can stay on the staff and end at Bach's register
(bass C4), while in the performance those relocations are inaudible.

## Allusions (all credited)

- **Bach, WTC I Prelude in C, BWV 846.**
  - Bars 1–4 are quoted exactly and quoted again as the da capo (50–53).
  - Bar 3 (G⁷/B) is the last step home (49).
  - The dominant pedal of bars 24–31 is transplanted to D♯ (34–37).
  - The ending, bars 32–35 (C⁷ – F/C – G⁷/C – C over a tonic pedal), closes
    bars 54–57. The flourishes in 55–56 are mine. Like Bach's, they break the
    pattern into continuous sixteenths.
- **Bach, Musical Offering, BWV 1079.**
  - The Royal Theme's head (C E♭ G A♭ B C, with its diminished-seventh drop)
    is the top voice of the c-minor bars.
  - Its chromatic tail (5 → ♭2) is the e♭-minor lament bass.
  - The title nods to the Offering's *Canon per tonos*, which also climbs
    through keys ("ascendenteque modulatione ascendat gloria regis"). Here the
    climb is a semitone per key pair, and it is made to return.
- **Gounod, *Méditation / Ave Maria* (1853/1859).** Gounod laid a melody over
  BWV 846's unchanged opening bars, and the da capo does the same. The melody
  is the subject of Fugue I (from `SUBJECT.txt`):
  - in augmentation ×2 and an octave up, over the da capo (upbeat at 49.4).
    Its accented G lands on bar 51's D-minor-seventh chord as an appoggiatura
    resolving to F;
  - then its head at true speed over the closing C⁷ (upbeat at 53.4½), a
    foretaste of the fugue.

  `tools/critic.py` verifies the augmented entry: 18/18 intervals and 18/18
  rhythms at scale 2.

## Critic numbers

**Notation score** (`python3 tools/critic.py cycle/01-c-major/prelude-notation.json`; critic, 2026-11-04):

| measure | result |
|---|---|
| `parallels_error` | 0 |
| `parallels_weak` | 0 |
| doubling runs | 0 |
| `beat_parallels` | 0 |
| suspensions | 5 (including the tenor 4–3 at 13.1, unprepared in the critic's reading) |
| retardations | 5 |
| pedal dissonances | 12 |
| tertian fit | 90.7 % (moves as the critic's chord naming is revised) |
| `UNRESOLVED` flags | 5, for three events (below) |
| unverified | 2 (5.3, 54.4; below) |
| `low_register_seconds` | 2 (10.3¼, 56.1¼; below) |
| `keyboard_unplayable_pct` | 5.0 % (the cantus: bars 5–7 and 54–57) |
| `bad_doublings` | 1: the cantus's passing F6 at 53.2 (review P4; it belongs to the exact augmentation) |

**Performance score** (`prelude.json`): its octave layers are declared as doublings in the
metadata (`doublings`, written by `shepard.py`), so the critic labels their octave runs
`doubling` (570 runs) and reports 0 `parallels_error` and 0 weak parallels. Its dissonance
and register figures describe octave-transposed copies of the written notes and are not a
counterpoint measure; the notation score is the one to judge.

The three `UNRESOLVED` events are all justified:
- **6.2** (two flags): A♭–G in the A♭maj⁷ chord (VI⁷) that carries the Royal
  Theme's G. The G rises to A♭ as the next note of the theme. The critic sees
  only the bass and one note of the broken chord at that instant.
- **21.2**: the F half-diminished seventh in the falling figure. At beat 2 the
  figure's note is C♭ against the tenor F. The chord is complete within the
  half bar; the flag comes from reading the compound line one note at a time.
- **51.2** (two flags): the cantus's G6 appoggiatura over Dm⁷/C (the subject's
  accent), resolving to F6 on beat 3. With the G6 sounding, the critic can no
  longer name the chord, so it also flags Bach's own ⁴₂ of bar 2 (the figure's F5
  over the bass C4, the seventh in the bass), which it accepts in bar 2 itself.

The two unverified spots are steps the critic cannot follow to a consonance:
- **5.3**: the cantus's E♭6 over the passing B♭2 (C minor over its seventh, ⁴₂ in
  passing). The bass steps on to A♭2 under the cantus's G6, the major seventh of
  VI⁷ that rises to A♭ with the Royal Theme.
- **54.4**: F6, a passing sixteenth in the cantus's fall G6 F6 E6 D6 C6 (the fugue
  subject's head at true speed) over the C⁷ figure. Its next step, E6, meets the
  figure's B♭3, the tritone inside C⁷.

The two low-register sevenths are chord sevenths of the written core:
- **10.3¼**: V⁷ of c♯ in root position, G♯2 in the bass and the seventh F♯3 in the
  tenor. In the performance the layers spread it over the keyboard.
- **56.1¼**: C2 and B2, the G⁷ over the tonic pedal of BWV 846's own penultimate
  bar (checked against the music21 corpus copy of BWV 846).

All of the unplayable onsets lie in the cantus bars (5–7 and 54–57). There the
cantus needs a third hand, or a second player as in Gounod. The core alone fits
two hands throughout.

**Chorale reduction.** `tools/critic.py` cannot see parallels inside a
broken-chord figure: Bach's figure rests on every beat 1, so the figure and
the bass are never compared across a harmony change. I therefore also checked
the implied five-part chorale: bass, tenor and the three figure notes, each
held for its half bar. This is a scratch file, not part of the score.
- 0 `parallels_error` and 0 weak parallels.
- One flag at 36.1: the D♯ pedal, re-struck in the reduction, so it is not
  recognised as a pedal.
- Nine sevenths that do not fall. These are the VI⁷ G above, the E♭ = D♯
  rising into E at bar 21, the doubled G♭ of the diminished seventh at 19.1
  (one G♭ resolves, the tenor's leaps), and dominant sevenths that move within
  their chord before resolving.

The melody warnings for the R.H. staff are the leaps of the broken chord
itself and are not meaningful.

## Weak spots, honestly

- **Unheard.** I have not heard any of it. Whether the illusion convinces on
  this soundfont, and whether the faint outer layers read as ghosts or as mud,
  is for a listener to judge.
- **Steady harmonic pulse.** The harmonic rhythm is mostly one chord per half
  bar, broken by whole-bar broadenings (11–12, 38, 47, 49) and held basses
  (26–27, 34–37). BWV 846 is a steady one-chord-per-bar tread, so this is in
  character. Still, bars 8–17 may feel like the same step taken repeatedly.
- **A recurring pivot gesture.** At most key changes the upper voices lift by
  step into the new I⁶. It is meant as the piece's refrain, but it could read
  as formula.
- **Very brief keys.** Some keys are established by little more than one
  cadence: f♯ (one half bar), g, e and b♭ (two each). G major has no
  root-position tonic, only I⁶ – V⁷ with the cadence left to g minor. The keys
  are unambiguous in the reduction, but they pass quickly.
- **Smeared voice-leading.** Under the layers (bars 10–45), inversions and
  individual lines are blurred by design. The separate bass centre keeps the
  bass lowest only on balance.
- **Untested cross-fades.** During the fade-in (bars 5–10) and fade-out (bars
  46–49) the audible register of the bass moves by up to an octave towards the
  written notes. It is placed to coincide with the music's own last rise, but
  it is untested by ear.
- **Possible boom at the climax.** The pedal climax still puts loud layers on
  D♯1–D♯3, now alone in that register (see the second review below).

## Tool notes (not edited; for whoever maintains `tools/`)

- **`critic.py` and compound melodies.** It compares voices only at shared
  onsets, so parallels or dissonances inside a broken-chord figure
  (BWV 846-type textures) are invisible. A chorale reduction is needed.
- **`critic.py` and `reduce.py` spelling.** Both name pitches with one global
  sharp/flat choice taken from the metadata key. They ignore `key_changes` and
  each event's `spell`, so D♭/F is printed "C#/F".
- **`render_music.py` markers.** Markers are printed only where voice 0 has a
  segment start. With a resting top staff, a mid-bar marker silently
  disappears. All markers here are on barlines.
- **`render_music.py` duplicate by-products.** Every audio render rewrites
  `.ly`, `.musicxml` and `.mid`, which are identical across temperaments. I
  deleted the duplicates for `-meantone` and `-equal`.
- **`render_music.py` header.** A long `instrument` string overlaps the
  composer line.

## Second review (REVIEW-2.md), what changed

The written core, the frame (bars 1–4 = 50–53) and the C/E glimpse of home at
bar 47 are untouched.

**P1. Pedal climax, bars 34–37 (High).** Two changes, both orchestration only;
no written pitch changed.
- **(a) Hold rule fixed in `pedal_figure()`.** A held note now crosses a
  half-bar line only if it belongs to the new half bar (or nothing at all is
  struck there). Before, the subset rule let the diminished seventh's E♯
  (36.2¾) ring at v89 through the i⁶₄ that resolves it. It now stops at 36.3.
- **(b) Register floor.** Tenor and figure layers below G3 are dropped over
  the pedal (H68–H73), so octaves 1–3 below G3 belong to the D♯ pedal alone,
  the BWV 846 image the review asked for. The review proposed D♯3, but a scan
  at that setting still found E♭3 against E3/E♯3 at velocity 58–63 (the
  review's own 35.3–4 case), so the floor is G3. The same scan found the
  phenomenon wherever a loud dominant seventh puts root and seventh a tone
  apart in octave 3:
  - D⁷ at 31 (v55);
  - E♭⁷ at 33 (v65, plus C♯2/D♯2);
  - E⁷ at 39 (v51).

  A D♯3 floor for tenor and figure therefore also covers bars 31–40 (H61–H80).
  The floors are fixed in pitch, so the spectral envelope stays fixed and the
  illusion is unaffected.
- **Verification**, with a scan like the review's (b): every sixteenth, two
  notes below G3 a semitone or tone apart, both at velocity ≥ 35.
  - Before: bars 22, 29, 31, 33, 35, 36 and 39–41, with bar 36 at 15/16 in
    the review's count.
  - After: only bars 22, 29 and 41, all at velocity ≤ 50 (the review's target),
    and none in bars 33–37.
- **Side effects.** The pedal bars sound brighter (audio centroid 70–72), and
  the performance score drops from 47 to 39 voices.

**P2. Royal Theme, bars 5–7 (Medium).**
- **A held cantus.** The six notes C E♭ G A♭ B C now also sound as a held
  cantus in half notes, the theme's own values in the Musical Offering. They
  are an octave above the figure's top voice, in the register of the da-capo
  cantus, not layered, and about +12 velocity over the figure. The
  diminished-seventh drop A♭6→B5 is heard plainly.
- **The fade now starts at the D♭ pivot.** `SHEPARD_MIX` is 0 to H15 and
  reaches 1 at H19 (bar 10), so all of c minor is plain.
- **The cantus returns.** It is now heard once early, so its entry at 49.4 is
  a return.
- **Cost.** Bars 5–7 now need a third hand (keyboard-unplayable 3.5 % → 5.0 %).
  The critic adds two appoggiaturas (the cantus's E♭6 over the passing B♭ bass
  at 5.3 and its G6 over A♭ at 6.1, the major seventh that rises to A♭) and
  still reports 0 parallels.

**After the changes.**
- The da capo is still identical to bars 1–4 (64/64 notes, same velocities).
- The register stays stable (see Checks above).
- Notation critic: 0 `parallels_error`, the same three justified `UNRESOLVED`
  events (6.2, 21.2, 51.2), and one `bad_doublings` (53.2, review P4).

**Not changed.**
- **P3 (pivot sameness in bars 8–17).** The review marks it "watch, do not fix
  blind"; it waits for Sam's listening.
- **P4 (cantus F6 at 53.2; cantus velocity +20 vs +12).** Left as they are; I
  cannot judge the balance without hearing.

**Re-rendered.**
- `renders/prelude-score.pdf`;
- the performance MIDI and MusicXML;
- the three MP3s, with `--audio-only` (the `-meantone`/`-equal` `.render.json`
  files are from the first render; the audio is new).

## Self-critique pass (Nov 2026)

No notes changed.
- **Critic section refreshed.** It still listed 4 `UNRESOLVED` flags and 6
  suspensions. The current critic reports 5 flags for the same three events (51.2
  now counts twice), 5 suspensions, 2 unverified steps (5.3, 54.4) and 2 low-register
  sevenths (10.3¼, 56.1¼); each is explained above. The performance score's octave
  layers are now declared as doublings, and that is noted there too.
- **Deleted** the weak spot "Empty cantus staff" and the tool note saying
  `render_music.py` cannot hide empty staves. `prelude.py` sets
  `score_layout.hide_empty_staves`, and the renderer removes the empty Cantus staff.

