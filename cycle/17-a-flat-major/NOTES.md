# Pair XVII in A-flat major: notes

## Prelude XVII: "Wiegenlied" (the lullaby that never quite ends)

**Files.** `prelude.py` → `prelude.json` (19 bars of 12/8, one pianist; about 1:45 in the render). Renders: `renders/prelude.{pdf,ly,musicxml,mid,mp3}` (Bach-Lehman) and `renders/prelude-equal.mp3`. I have not heard them.

**Concept.**
- The children sing their father to sleep. Their lullaby is the fugue's subject in augmentation, over a rocking left hand. It is the same tune, at the same speed, that the father comes down singing at the end of the fugue (fugue bars 37-41), so the pair closes the circle: they sing it to him, and he sings it back.
- Like the fugue, the lullaby never cadences. Each of its four verses is deflected at its last note, each in a different way.
- The prelude has no perfect cadence: the same scan as for the fugue finds no V → I with the bass E♭ → A♭.

**Section map** (the cradle figure is a quarter and an eighth per beat, "rock-a").

| Bars | Time | What happens |
|---|---|---|
| 1-2 | 0:00 | The cradle alone, over A♭ (I; IV6/4 - I). |
| 3-6 | 0:10 | **Verse 1.** The tune in the soprano (A♭4-A♭5): I, IV - vi, ii, I6/4 - V. It rests on the dominant, the tune on *re*. |
| 7-10 | 0:29 | **Verse 2** starts over I6 before verse 1 can close (V → I6). A second voice sings in sixths below. It ends with a deceptive cadence: V → vi. |
| 11-14 | 0:48 | **Verse 3** in F minor. The alto sings the tune's first half and the soprano is silent. Then the harmony turns home: IV - ii7, ii6/5 - V7. |
| 15-18 | 1:08 | **Verse 4.** The V7 does not resolve: the bass stays on E♭ under I6/4, and the last verse is sung over that dominant pedal, softer. The cradle climbs a little and the second voice drops out. |
| 19 | 1:30 | The hands resolve to A-flat (C4 E♭4 A♭4). The bass never comes; only the father, at the end of the fugue, supplies it. |

**Critic (prelude.json).**
- parallels_error 0 / weak 0, beat_parallels 0, bad_doublings 0, low_register_seconds 0, crossings 0.
- dissonance_unresolved 2: the fourth of the cadential six-four (A♭3) inside the rocking figure in bars 6 and 10. It reaches G3 at the change to V, but only after a rocking C4, so the critic does not count it as resolved.
- keyboard_unplayable_pct 0.0, mean_moving_voices 3.0.
- stepwise_pct 32.4: the rocking figure is a broken chord. The tune itself moves by step except for its octave leap.
- The three statements of the whole tune verify 16/16.

**Weak spots.**
- The cradle figure keeps one rhythm in every bar. That is the point of a lullaby, but over 19 bars it may be monotonous.
- Verses 1, 2 and 4 use the same tune at the same pitch; only the harmony under it, the second voice and the dominant pedal change.
- The final chord has no bass by design. On paper it is a bar of three notes in the treble under a long hold in the tempo map, with no fermata sign.

## Fugue XVII: "Fuga, fuggendo la cadenza" (four children and their father)

**Files.** `fugue.py` → `fugue.json` (44 bars of 12/8; five staves, the fifth used only from bar 37). Renders in `renders/` (listed at the end). The earlier eighteen-voice version is in `archive-n-plus-1/`.

**I have not heard the renders.** Everything below comes from the score and the tools. Nothing here describes how the piece sounds.

### Concept at the new size

- **The term.** Zarlino called an evaded cadence *fuggir la cadenza*, "to flee the cadence". A *fuga* is a flight. This fugue flees every cadence it prepares.
- **The story.** It is told of Bach, and probably a legend: his children could get him out of bed by playing an unresolved chord, because he could not lie still until he had come down and resolved it.
- **The cast.** Bach's A-flat fugue in WTC I (BWV 862) has four voices, so this one has at most five.
  - The four voices of the fugue proper are the children.
  - The fifth, the father, is silent until bar 37.
- **The plot.**
  - The subject ends on *re*, the note that most wants to fall to *do*. Every time the music prepares a perfect cadence, the cadence is evaded, fourteen times in all, each in a way the listener can follow.
  - First comes a running gag of deceptive cadences that drifts round the flat side of the key circle and speeds up. Then a dream in E major (the far point), with the subject in augmentation. Back home, the children try more desperate dodges.
  - At last all four children stop on a dominant seventh and wait.
  - The father enters alone in the bass with the subject in augmentation. His tune ends on *re* like everyone's, and then he supplies what the children's tune never had, the bass *sol → do*: the first perfect authentic cadence of the piece (bar 42).
- **The coda.** The first child, the tenor who began the fugue, sings the second half of the subject once more, and this time it is allowed to end on *do*.

### Material

- **Subject** (tenor, bar 1, two bars, kept from the earlier version).
  - As scale degrees: *do. | DO' ti | la sol fa | mi fa ‖ re mi | fa sol la | sol. fa mi | re.*
  - In A-flat: A♭3 A♭4 G4 F4 E♭4 D♭4 C4 D♭4 | B♭3 C4 D♭4 E♭4 F4 E♭4 D♭4 C4 B♭3.
  - The octave leap and the descending scale are its fingerprint. In minor keys it uses the natural minor.
- **The gag's signature.** Each evasion of the running gag has the same two-part gesture: the soprano trills on *re* (sometimes on the leading tone) and gets her *do*, and the bass, which should fall a fifth, steps up a degree instead (V → vi or VI). The listener can learn this gesture and then hear it come faster.
- **The guest.** Bach's BWV 862 subject at Bach's pitch, in Bach's voice (the tenor), alone as at the start of his fugue: A♭3 E♭4 C4 A♭3 F4 D♭4 E♭4 (5/16) D♭4 C4 D♭4.
  - I checked it against the Humdrum kern edition (`wtc1f17.krn`, spine 2) and it agrees with `cycle/reference/bach-subjects.md`.
  - I quote Bach's tenor through his bar 3 (the sixteenths that follow the subject, to the G4-F4 suspension). The bass enters with Bach's own tonal answer (E♭3 A♭3 G3 E♭3 C4 A♭3 B♭3) and three more eighths of his bass.
  - Both voices are moved together, so every vertical interval is Bach's. Only the barring changes: his eighths fall into 12/8 groups of three.
- **Transformations** (named transforms of the hand-written subject in `fugue.py`):
  - realisation in other keys and modes;
  - diatonic (modal) transposition (`shift`) for the stretto entries on E-flat and B-flat;
  - augmentation ×2 (the dream, the father);
  - diatonic inversion (the alto over the father);
  - the head alone (the bass in the running gag);
  - the second half alone (coda).
- **No countersubject.** The 18-voice version had a fixed countersubject and a fixed "module bass". Both are gone: the counterpoint around each entry is written freshly, and the recurring companion is the soprano's trill.

### Section map (44 bars, about 3:34 in the render)

Times come from the tempo map. "Moving" is the critic's count of voices that move in each bar.

| Bars | Time | What happens | Voices / moving |
|---|---|---|---|
| 1-8 | 0:00 | **Exposition.** Tenor subject (A♭), alto answer (E♭), soprano subject, bass answer. Each enters after a rest. The tenor's first *re* slips down to *ti* instead of *do*. | 1-2-3-4 |
| 9-10 | 0:33 | **Evasion 1.** First full cadence: ii, ii6, cadential 6/4, the soprano's trill on B♭5 ... V → vi. The alto, after a rest, starts the subject in F minor on that very chord. | 4 |
| 11-13 | 0:42 | **Evasion 2.** In F minor: trill (leading tone), V → VI. The tenor, after a breath, takes the subject in D-flat. Soprano, tenor and bass only in bar 12. | 3-4 |
| 13-17 | 0:50 | **The running gag speeds up** (evasions 3-7). D-flat → b♭ → G♭ (one bar each; the bass sings the subject's head and then steps up), then e♭ → C♭ → a♭ (half a bar each). The note of the soprano's trill falls a third each time: E♭, C, A♭, F, D♭. | 4 |
| 17 | 1:06 | **A-flat minor: home, but minor.** Everyone stops except the bass, who sings the head alone, pianissimo. Evasion 8: E♭7 → F♭. | 1-2 |
| 18-22 | 1:11 | **The dream.** F-flat = E major, slower, pianissimo. Soprano: the subject in augmentation (E5-E6, bars 19-22). Tenor: the subject at its own speed beneath it (bars 19-20). Then a dominant pedal, and evasion 9: B7 → c♯. | 3-4 |
| 23-24 | 1:38 | **The way home.** c♯ = d♭, iv of A-flat. Chromatic bass D♭-D-E♭; C♭ → C turns minor into major. Cadential 6/4 and the soprano's longest trill. | 4 |
| 25-26 | 1:47 | **Evasion 10, the guest.** At the cadence soprano, alto and bass stop. The tenor's leading tone rises alone to A♭3, which is the first note of Bach's BWV 862, at pitch; the bass answers with Bach's answer. Bach's own V7 → I (bar 26, beat 3) is turned to vi. The soprano lands her trill, a bar late, on A♭5. | 1-3 |
| 27-30 | 1:56 | **At home: evasion 11, the trill that will not stop.** Soprano subject in A-flat. Its *re* becomes a trill that lasts five beats while the others call (falling thirds) and the bass knocks. When it lets go, the tonic arrives with G♭ in the bass (V → V4/2 of IV). | 4 |
| 30-32 | 2:08 | **Evasion 12, the trap door.** ii6/5 - V7 → ♭VI: the bass falls a seventh (E♭3 → F♭2), subito pianissimo. A German sixth climbs back to 6/4 - V7. | 4 |
| 33-36 | 2:21 | **Evasion 13 and the stretto.** The bass starts the subject on E-flat, so the V7 does not resolve at all. Alto (E♭4), tenor (B♭2) and soprano (B♭4) follow every half bar. ii6/5 - I6/4 - V7, then **evasion 14**: all four stop on E♭7 with D♭5 on top (held, about 3.5 s), then silence (about 3.75 s). | 2-4 |
| 37-41 | 2:42 | **The father.** He enters alone on A♭1 with the subject in augmentation. The soprano's D♭ falls to C at last. The alto sings the subject inverted against him (she climbs while he walks down); the tenor joins in bar 40. His tune ends on *re* over ii7, then E♭2 under the cadential 6/4 and V7, with the soprano's trill on B♭5. | 1-3-4 |
| 42 | 3:12 | **The first perfect authentic cadence**: bass E♭2 → A♭1, soprano B♭5 → A♭5, all five voices. | 5 |
| 42-44 | 3:12 | **Coda** over the father's A♭: the tenor sings *re mi fa sol la, sol fa mi, re* ... and *do*. | 5 |

### The fourteen evasions, and where to hear the devices

1. **Evasions 1-9: deceptive cadences, on purpose.** They are the running gag, and their variety is in texture and timing rather than in harmony:
   - a new subject entry starts on the deceptive chord (1, 2);
   - the bass sings the head and steps up (3, 4, 7);
   - two arrive per bar (6, 7);
   - one arrives at A-flat minor, where the music stops (7);
   - one opens a dream (8), and one, pianissimo, leads home (9).
2. **Evasion 10, Zarlino's own kind.** The bass is silent at the cadence, and a new subject, Bach's, begins in its place. Bars 24-25.
3. **Evasion 11, the stuck trill.** It ends on the tonic with its seventh in the bass. Bars 28-30.
4. **Evasion 12, the trap door to ♭VI.** Bars 30-31.
5. **Evasion 13, V7 → V.** The stretto simply starts on the dominant. Bars 32-33.
6. **Evasion 14, the chord left hanging, then silence.** Bar 36.
7. **The perfect cadence.** A scan of every eighth-note position (my scratch script `pac.py`, which only reads the score) finds exactly one place where a sonority with E♭ in the bass and the leading tone sounding is followed by an A-flat major chord over A♭ in the bass: bar 42.1.

Devices:
- **Augmentation with the subject at its own speed** (the dream, bars 19-20): soprano on top, tenor at the bottom, the bass silent.
  - `stretto_finder.py` rated this combination clean (no parallels, no dissonance errors) at distance 0, two octaves apart.
  - The father's augmentation (bars 37-40) is the low mirror image of the dream: the dream's augmentation is the highest voice, the father's the lowest.
- **Inversion against augmentation** (bars 37-39). The alto's inverted subject enters half a bar after the father's augmentation, at an offset `stretto_finder.py` rated clean (cost 13).
- **Stretto of all four children** (bars 33-36):
  - entries every half bar: bass E♭2, alto E♭4, tenor B♭2, soprano B♭4;
  - `stretto_finder.py` rated all six pairings clean;
  - I chose the order after a first version (tenor second, alto third) crossed the tenor above the alto.
- **The guest** (bars 25-26). Alone in the tenor for a bar, at Bach's pitch, then with Bach's bass answer.

### Critic (tools/critic.py on fugue.json)

| Measure | Value | Target |
|---|---|---|
| parallels_error / weak | 0 / 0 | 0 |
| beat_parallels | 0 | ≤ 2 |
| dissonance_unresolved | 1 | ≤ 3, justified |
| bad_doublings | 0 | ≤ 2 |
| low_register_seconds | 3 (b13.4.75, b34.6.5, b35.4.75) | ≤ 9 |
| stepwise_pct | 67.9 | ≥ 65 |
| leap_4th_plus_pct | 12.0 | - |
| crossings | 0 | few |
| keyboard_unplayable_pct | 4.0 (16 of 400 onsets) | < 5 (4 voices), < 15 (5-6) |
| mean_moving_voices | 3.64 | - |
| pc_tripled_on_beats_pct | 4.9 | - |
| tertian_fit_pct | 58.9 | - |
| longest static harmony | 4 beats (the final chord) | - |

**Details behind the numbers.**
- **The unresolved dissonance** (b26.2.5, tenor F4 over bass E♭3) is Bach's own passing ninth in the quoted bars: tenor F4 against bass E♭3 at the same moment of his bar 3. I left it as Bach wrote it.
- **The three low-register sevenths** are passing sixteenths or eighths of the subject or its tail over a held bass.
- **Melody flags.**
  - The tenor's leap from E4 down to D♭3 across a rest into its bar-12 entry.
  - The trap-door seventh in the bass (E♭3 → F♭2, the point of evasion 12).
  - The bass's E♭2 → D♭3 into the final ii6/5.
- **Unplayable onsets.**
  - Two in the trill over the bass's low A♭1 (bar 13).
  - A few in bars 38-40, where the father's low line and three children span more than two hands.
  - Most of the rest are in the five-voice cadence and coda over the father's held A♭1, which a pianist would hold with the sustain pedal.
- **Theme check.**
  - All exposition, middle and augmented entries verify 16/16.
  - The stretto entries on E-flat and B-flat are diatonic (modal) forms, so the critic shows 14/16 and 8/16 intervals.
  - The heads in bars 14, 15 and 17 are partial statements by design.
  - The guest is Bach's subject, not ours, so it does not match, as its label says.

### Honest weak spots

- **Bar 16 is chordal.** The fastest part of the running gag is four voices moving in dotted quarters with the soprano's trills. It may sound like a hymn with ornaments rather than counterpoint.
- **Evasions 1-9 share one harmonic type** (V → vi/VI). That is the joke, but a listener may tire of it before bar 17.
- **Inner voices that carry the point.**
  - The alto's inversion over the father (bars 37-39) and the tenor's "*do* at last" in the coda (bar 43) are inner voices, under a soprano line.
  - Their audibility rests on the entry velocity boost and on the soprano moving in longer notes there.
  - I have not verified this by ear.
- **The fermata and the silence exist only in the tempo map.** On paper bar 36 shows a dotted-quarter chord and a dotted-quarter rest, with no fermata sign; a player reading the PDF needs the map or an added fermata.
- **Static alto.** In bars 7-8 the alto sits on E♭4 for most of two bars while the bass has the answer.
- **Ranges.**
  - The dream's augmentation reaches E6.
  - The tenor is notated in the bass clef up to C5 (many ledger lines).
  - The father's line lies in octave 1-2 (A♭1-A♭2). It may be muddy on some pianos.
- **Spelling at the enharmonic turns.** The dream is spelled in E major (sharps) between flat-key bars 17 and 23, so the score switches spelling abruptly at bar 18 and again at bar 23.
- **The guest is re-barred.** Bach's eighths in 4/4 become groups of three in 12/8. The pitches, durations and vertical intervals are Bach's; the metric accents are not.

### From the 18-voice version (`archive-n-plus-1/`)

**Kept.**
- The concept and the subject.
- The chain of deceptive cadences falling by thirds (A♭ → f → D♭ → b♭ → G♭ → e♭ → C♭ → a♭ → F♭ = E → c♯ = d♭).
- The dream in E major with the subject in augmentation.
- The guest at Bach's pitch.
- The hanging seventh, and the father's augmentation with the bass *sol → do*.

**Changed, and why.**
- **Size and texture.** 18 voices became 4 + 1, and 52 bars became 44 (3:56 → 3:34). The texture now breathes: 1-2-3 voices at the exposition, the bar-17 solo, the guest and the father's entry; four voices for most of the rest; five only at the cadence and coda. Every voice is one continuous line.
- **The gag is now followable.** Each evasion in the chain carries one recurring gesture (soprano trill + bass up-step), and the chain accelerates (2, 2, 1, 1, ½, ½ bars) to a stop in A-flat minor. Before, every link was the same module of subject, countersubject, module bass and free voices, two bars each, nine times.
- **The home evasions are different kinds.** Silence and a guest, a stuck trill landing on the tonic with its seventh in the bass, a trap door to ♭VI, a stretto that starts on the dominant, the hanging chord. They replace the four V → ? modules that ended with the same ii7 - V4/3 - V7 - V bar.
- **The guest.** It was buried at A♭3 in a seven-voice texture. Now it begins alone in the tenor, as in BWV 862 itself, with Bach's bass answer.
- **The dream.** The augmentation is now on top, with the subject at its own speed beneath, instead of the first bar only.
- **The father's passage.** The alto now sings the inversion against him (a two-voice device you can follow) instead of a cascade of heads in 15 voices.
- **The coda.** It finally gives the tune its *do*.
- **Removed.** The fixed countersubject and module bass; the antiphonal two-choir layout.

### Renders

- `renders/fugue.pdf`, `.ly`, `.musicxml`, `.mid` and `fugue.mp3`: Bach-Lehman temperament, LilyPond succeeded. Empty staves are hidden, so the father's staff appears from bar 37.
- `renders/fugue-equal.mp3`: equal temperament, audio only.
- `renders/fugue-spatial.mp3`: binaural, `--layout arc`, piano. The soprano and bass are at the sides, the alto and tenor inside them, and the father in front.
- `renders/fugue-spatial-choir.mp3`: the same with `--program 52` (Choir Aahs). It replaces the earlier version's choir render of the same name.

Rebuild:
```
python3 cycle/17-a-flat-major/fugue.py
python3 tools/critic.py cycle/17-a-flat-major/fugue.json
python3 tools/render_music.py cycle/17-a-flat-major/fugue.json --output-prefix cycle/17-a-flat-major/renders/fugue --temperament bach-lehman
python3 tools/render_music.py cycle/17-a-flat-major/fugue.json --audio-only --temperament equal --output-prefix cycle/17-a-flat-major/renders/fugue-equal
python3 tools/render_spatial.py cycle/17-a-flat-major/fugue.json --output cycle/17-a-flat-major/renders/fugue-spatial.mp3 --layout arc
```

### Credits and method

- **Fuggir la cadenza.** Gioseffo Zarlino's term for an evaded cadence (*Le istitutioni harmoniche*, 1558, book III). Evasion 10 is his kind: a voice rests where the cadence should land.
- **The anecdote.** The story of the children and the unresolved chord is told of Bach (and of others). I treat it as a legend.
- **J. S. Bach, Fugue in A-flat major BWV 862 (WTC I).**
  - Subject, its continuation and the bass answer, bars 1-3, quoted at pitch in bars 25-26.
  - Checked against the Humdrum kern edition (`wtc1f17.krn`).
  - Credited in the entry label and the score's composer line.
- **Method.** Every note is written in `fugue.py`.
  - The thematic statements are named transforms of the hand-written subject (key, mode, diatonic shift, inversion, augmentation, truncation).
  - The written-out trills are produced by a small helper (`trill()`) that alternates the two notes I chose for the length I chose.
  - `tools/stretto_finder.py` proposed clean distances for the stretto, the dream and the father's passage; I chose among them and wrote the counterpoint around them.
  - `tools/critic.py`, `tools/reduce.py` and scratch scripts (a vertical-grid viewer, a low-register pair lister, the cadence scan) only reported problems; I made every correction by hand.
