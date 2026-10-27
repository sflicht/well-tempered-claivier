# Fugue XXIV in B minor, twenty-five voices

61 bars of 4/4. Quarter = 63 for the build-up, pushing to 69 (bars 26–35). It broadens to
58 for the cantus (bars 41–48) and to 50 at the arrival (bar 51). The release slows to 38.
The rendered audio lasts 4:10. Sources: `fugue.py` assembles `build1.py` … `build5.py`
(build-up), `conv_a.py`, `conv_b.py`, `conv_c.py` (convergence) and `release.py`. The shared
material is in `xxiv.py`. Built score: `fugue.json`. Renders: `renders/fugue.{pdf,mid,musicxml,ly,mp3}`
(Bach–Lehman, PDF engraved by LilyPond), `renders/fugue-equal.mp3` (equal temperament) and
`renders/fugue-spatial.mp3` (ring layout). The stage-1 study is `convergence.py` → `convergence.json`.
No prelude was written.

I cannot hear the renders. Nothing here describes how the piece sounds. Every statement comes
from the score and the tools.

## The premise

A twelve-tone subject belongs to B minor and drives the whole piece. The decisive combination
was composed first. The subject sounds in four-fold augmentation in the Contrabass, the 25th
voice, which enters only for it. Four subjects from earlier fugues of this edition arrive over
it, each where the cantus's own note makes it a tonic or a harmony tone. The build-up was then
written backwards from what the combination needs the listener to know: the subject and its
mirror, the countersubject, the upbeat figure, the run, and two-fold augmentation. The release
was written forwards from the arrival.

## The subject set and its rates

| name | tokens (written key) | rate / role |
|---|---|---|
| **S** | `B4:4 D5:2 C#5:2 E#4:6 F#4:2 D#5:6 E5:2 C5:6 B4:2 G4:2 G#4:2 A4:2 A#4:2` | quarters/eighths, three dotted "leans" (E#→F#, D#→E, C→B), then the chromatic climb G G# A A#. All twelve pitch classes. Ends on the leading tone; the B belongs to what follows |
| **I** | `B4:4 G#4:2 A4:2 E#5:6 E5:2 G4:6 F#4:2 A#4:6 B4:2 D#5:2 D5:2 C#5:2 C5:2` | the exact mirror around B (also twelve-tone); its tail falls D# D C# C |
| **CS1** | `R:4 F#5:8 E#5:2 C#6:2~ C#6:4 B5:8 A5:4 G5:4 F#5:8 E5:4` | halves and quarters, tied: a suspension chain written above S |
| **U** | `C#4:2 C#4:2 C#4:2 A4:6 G4:2` | three knocking eighths, a sixth's leap onto a leaning dotted quarter, a step down (S's own leap-and-lean). Used freely as an upbeat figure ("knocking") |
| **R** | `B4:1 A#4:1 B4:1 C#5:1 D5:1 C#5:1 D5:1 E5:1` | sixteenth runs, relayed between voices |
| cantus | S ×4, two octaves down (`B2:16 D3:8 C#3:8 E#2:24 …`) | whole notes and longer, Contrabass, bars 41–51 |

The mobile bass is free in every section. It leaps where S's own harmony needs it, and it
never doubles a theme in octaves.

## Form

| bars | section | what happens |
|---|---|---|
| 1–11 | exposition | A3 S; T2 answer in F# minor with CS1 above it in A3; B1 S in the bass with CS1 in T2; S2 answer on top. Four voices |
| 11–17 | codetta, S in D | U appears (T2, Br2), R appears (A5, T4); A1 S in D with CS1 in S2; episode through G7–C–F#ø–B7 to E minor |
| 18–20 | **mirror stretto** | S1 enters with I in E minor over a texture thinned to five voices. Half a bar later T3 enters with S in D (finder cost 6, no parallels). Neapolitan sixth – cadential 6/4 – E7 in A minor, turned aside to B7 – E minor, then on towards D minor |
| 21–25 | S in C, bass | B2 enters with the subject in C as a bass. S3's line copies CS1's opening shape; the cadence turns to C major. Br3 and Br4 enter knocking (U) |
| 26–28 | S/I stretto | T1 enters with S in A minor and A4 with I on B, half a bar later. In this register the pair sounds an eleventh apart: the finder's fifths become fourths |
| 29–31 | S in E with CS1 | A5 S, A2 CS1 (new voice), S1 descant, T4 sixteenths, Br1 (entered with U at b28) |
| 32–34 | dominant region, pedal on C# from b33 | the subject's head (F#–A–G#–B#–C#) climbs T5 (b32, new), A3 (b33), S4 (b34, new). B3 holds and knocks the C# pedal from b33; B4 knocks C# above it. Each bar runs F#m(⁶₄) – G#7 – C#7 |
| 35–39 | S ×2 in F# minor | B2 in augmentation; S3 sings CS1 in augmentation (its first five notes, then free). Harmony F#m – G#ø7 – G#7 – C#7 – F#7 – Bm – G (Neapolitan) – C#ø7 – F#7 – Bm/D – B#°7 – C#m/E – C#7 |
| 40 (c0) | lead-in, F#7 | the remaining voices enter one after another across the bar (A1, A4 on 1; S4, T5, Br3, Br4 on 2; A2 on 2½; A3, B4, S5, T4 on 3; S3 on 3½) |
| 41–51 (c1–c11) | **the convergence** | cantus S ×4 in B5; guests from Fugues V, VIII, II, IV (below) |
| 52–53 | release | the arrival's lines let go one by one; Fugue V's subject in B major (T3) |
| 53–57 | Fugue I's ladder | canon at the octave three eighths apart (Fugue I's own rung R3): Br2 → T5, then A2 → S1, an octave higher. Each entry takes over the last note of the one before |
| 58–59 | mirror wedge | T1: S's tail G–G#–A–A# ×4; A3: I's tail D#–D–C#–C ×4; over a B pedal (cantus) and an E pedal (Br2). Em(maj7) – E7 – A – French sixth → both tails close on one B4 |
| 60–61 | last chord | B major; seven voices on beat 1, six more on beat 3, the last twelve on bar 61 |

## The build-up: when each voice enters and what it changes

| voice | first note | what the entry does |
|---|---|---|
| Alto III | 1.1 | the subject alone |
| Tenor II | 3.3 | answer in F# minor; A3 turns to CS1 (first suspension chain) |
| Bass I | 6.1 | subject in the bass; T2 takes CS1 |
| Soprano II | 8.3 | answer on top; B1 becomes the free bass |
| Alto I, Alto V | 13.1 | S in D (A1); first sixteenth run (A5) |
| Baritone II | 15.3½ | first U (knocking upbeat) |
| Tenor IV | 16.3 | R in the tenor; the episode reaches E minor |
| Soprano I | 18.1 | the inversion, first time, in a thinned texture |
| Tenor III | 18.3 | S in D in stretto with the inversion |
| Bass II | 21.3 | subject in C as the bass; B1 hands the bass over and rests |
| Soprano III | 21.4 | CS1-shaped suspension line at the top |
| Baritone III, IV | 24.2½, 24.4½ | U knocks, staggered, into C major and A minor |
| Tenor I | 26.1 | S in A minor |
| Alto IV | 26.3 | I on B (stretto) |
| Baritone I | 28.3½ | U landing on a leaning F# (Em9) |
| Alto II | 29.2 | CS1 in E minor |
| Tenor V | 32.1 | the head of S over the C# pedal |
| Bass III, Baritone V | 33.1 | pedal knocks; a slow line above the pedal |
| Bass IV | 33.3½ | U knocks on C# |
| Soprano IV | 34.1 | the head at the top |
| Soprano V | 40.3 | the last upper voice, in c0 |
| Contrabass | 41.1 | the cantus |

Voices sounding per bar: 1, 1, 2, 2, 2, 3, 3, 4, 4, 4, 4, 4, 6, 5, 7, 7, 7, 7, 5, 5, 9, 7, 6, 7,
7, 8, 7, 7, 6, 7, 6, 7, 9, 9, 9, 10, 9, 9, 11 | **21, 22, 21, 22, 23, 9, 15, 19, 11, 18, 21, 23** | 22, 5, 5, 6, 5, 4, 5, 5, 13, 25.

## The convergence, bar by bar (bars 40–51 = c0–c11)

Harmony: c0 F#7 | c1 Bm7 | c2 Bm7/D . C#ø7 | c3 E#°7 | c4 C#7/E# . F#7 | c5 D#m . B/D# . G#m/D# |
c6 A#7/D# . D#m . D#°7 . Em | c7 C | c8 B+ (B D# G) | c9 C/G . E7/G# | c10 A7 . A#°7 | c11 B.

The working rule for every bar: long-breath lines move on beats 1 and 3, suspension chains on
2 and 4, U-figures land on 1 or 3, and the sixteenth runs are relayed. At no onset do two voices
move between the same two pitch classes (checked with `hot.py`).

- **c0 (b40)** F#7. S1 climbs C#6–D6–E6. S2 holds A#5. A4 has sixteenths. T2 and S3 knock U upbeats into c1. B2 lands F#2 (end of S ×2). The last voices enter across the bar.
- **c1 (b41)** The cantus B2 enters (Contrabass) on Bm7. At c1.2½ S1 sings **Fugue V** (D major, its own pitch, an octave up). The cantus's B–D–C# makes D major a harmony of its own line. S5 has sixteenths; T2 lands its U on A (the 7th); T5's A#→B is a retardation; Br3 walks in quarters.
- **c2 (b42)** Bm7/D → C#ø7 (chosen over A7/C# for the common tones). A1 has U landing on G. A5 has sixteenths. Br1 knocks. S4's 4–3 chain goes A→G over C#ø7.
- **c3 (b43)** E#°7 under the cantus's long E#. T1 echoes Fugue V's tattoo (B B B B). T4 has sixteenths; S3 and Br1 knock into c4.
- **c4 (b44)** C#7/E# → F#7. S1 has a 4–3 over F#7 (B→A#). A4 has sixteenths. The expected F#7 → Bm is prepared.
- **c5 (b45)** Deceptive turn: the cantus's 1½-bar D# becomes the tonic of **Fugue VIII**. S4 sings it in E-flat minor at its own pitch, at the top of a texture thinned to nine voices so that it can be heard.
- **c6 (b46)** A#7/D# – D#m – D#°7 – Em. VIII's D# is held and resolved up into E minor. T5 has an upbeat figure; the baritones begin to rebuild.
- **c7 (b47)** C major (Neapolitan). At c7.3 **Fugue II** enters at the top in C minor at its own pitch (S1). A4 runs under it; T2, Br3 and Br4 move in halves and quarters.
- **c8 (b48)** B+ (B D# G): the cantus falls C→B. Fugue II's E♭ is the D#; S4 has C over B as a 9–8. Thinned to eleven voices.
- **c9 (b49)** C/G → E7/G#. At c9.4 **Fugue IV** enters, transposed to B minor and re-barred from 3/4 (S1). S5 knocks; A4 has sixteenths; T1 begins the descending wedge E–D–C# against the cantus's rising G–G#–A.
- **c10 (b50)** A7 → A#°7. Fugue IV peaks on G6 over A#°7. A4 and T4 have sixteenths; T3 and T5 knock into the arrival.
- **c11 (b51)** Arrival on B major. The cantus's A# resolves to B2 on the downbeat. The other leading notes resolve one after another: S1 (Fugue IV's A#→B) and S4 an eighth after the cantus, A5 on beat 3, T3 on beat 4. T1's wedge closes C#→B on the downbeat.

## Guests: sources, placement, verification

Each guest is copied note for note from the first statement in the finished pair's `fugue.json`
(the strings are in `xxiv.py`, `GUESTS`). Each is transposed only by an explicit `transpose`.
`verify_guests.py` runs `tools/stretto_finder.py --against` for each placement. It passes the
guest at its sounding pitch and the line it was fitted to, with `--forms rectus --steps 0` and
the actual entry distance. Results are in `guest-verification.json`.

| guest | source | where | finder vs. its partner | cost | parallels | 2-voice unresolved |
|---|---|---|---|---|---|---|
| Fugue V | `cycle/05-d-major` | S1, c1.2½, D major (own key), 8ve up | the cantus | 23 | 0 | 1 |
| Fugue VIII | `cycle/08-e-flat-minor` (head = Bach, BWV 853) | S4, c5.1, E♭ minor (own key) | the cantus | 22 | 0 | 1 |
| Fugue II | `cycle/02-c-minor` | S1, c7.3, C minor (own key) | the cantus | 15 | 0 | 0 |
| Fugue IV | `cycle/04-c-sharp-minor` (3/4, re-barred) | S1, c9.4, down a whole step to B minor | the cantus | 24 | 0 | 1 |
| Fugue V | as above | T3, b52, B major | the B1 pedal | 10 | 0 | 0 |
| Fugue I | `cycle/01-c-major` | Br2 b53.4½ → T5 b54.2; A2 b55.4½ → S1 b56.2 (B major) | its own canon at the octave, 3 eighths (Fugue I's rung R3) | 12 each | 0 | 0 |

The two-voice "unresolved" counts are for each guest against the cantus alone. In the full
texture those notes are harmony notes of the plan. The plan-aware check marks two notes as
"quoted guest note (free)" (in Fugue V and IV). Fugue I's R3 rung scored 13 in its own fugue.

## Measurements

All numbers come from `tools/critic.py` (as it stands now), `texture.py` (it reproduces
`diagnosis/inspect_actual_texture.py`), `nct.py` (it classifies every non-chord tone against my
written harmonic plan, which is stored in `fugue.json` as `harmonic_plan`) and `check.py` (it
checks each theme against its own prototype). The old finale is
`editions/complete-cycle/scores/24-fugue-b-minor.json`; its tutti window is bars 104–121.

| measure | old finale | new |
|---|---|---|
| duration (render) | 385.7 s (q = 84) | 250 s (tempo map 63–69–58–50–38) |
| parallels_error / weak | 0 / – | **0 / 0** |
| beat_parallels | 0 | 2 (b30.3 T4/B2 inside a sixteenth run; b34.3 S1/Br5 at beat level) |
| low_register_seconds | 50 | 28 |
| bad_doublings (7th or leading tone doubled on a beat) | 11 | 26 (12 in the convergence) |
| critic dissonance_unresolved | 2 | 122 (sevenths, diminished and pedal chords read without context) |
| unresolved against the written plan (`nct.py`) | – | **0** (suspension 66, passing 97+6, neighbour 27, appoggiatura 22, retardation 16, anticipation 18, escape 5, quoted guest note 2) |
| themes verified exact | – | 26 / 26 |
| stepwise_pct / leap ≥ 4th / repeated | 32.8 / 40.5 / – | 52.5 / 17.0 / 12.6 (60 % of moves that change pitch are steps) |
| voice crossings | 399 | 68 |
| **tutti window** | bars 104–121 | bars 41–51 (cantus) |
| distinct pitch classes per instant | exactly 3 throughout | mean 4.78, min 3; ≥4 at 87.5 %, ≥5 at 51.7 % of beats |
| mean sounding parts | 25.0 | 15.8 |
| attacks (off the quarter) | 800 (0) | 525 (186) |
| stepwise transitions | 7 of 775 | 206 of 443 |
| octave transitions | 103 | 1 |
| longest note | 20 beats | 7 beats |
| voices moving per bar (critic) | 22.4 | 18.0 (22 20 20 21 9 15 19 11 18 20 23) |
| whole piece: mean distinct pitch classes | 2.8 | 3.7 |

The old finale's higher moving count comes from 25 parts re-voicing the same three pitch classes.
Bars c5 and c8 (9 and 11 movers) are thinned on purpose so that Fugues VIII and II can be heard.

## Method

Notes are written as literal wtclib token strings, placed at bar.beat by `Score.put` and
`Score.theme` in `xxiv.py`. Themes are explicit `transpose` and `scale_rhythm` calls on the
material. Software was used only to propose placements (`stretto_finder.py`: the mirror stretto
I-in-E with S-in-D at half a bar; S-in-A with I-on-B; Fugue V and Fugue I in B; the chord-plan
fit for the guests) and to report problems (`check.py`, `hot.py`, `nct.py`, `grid.py`). During stage 1, `alts.py` compared a few hand-written alternatives for convergence passages. Every
collision was fixed by rewriting the free line by hand. No tool chose or altered a note.

## Credits

Subject, countersubject, figures and all free lines: Claude, for Sam. Guest subjects are quoted
from this edition: Fugue I in C major (its canon at the octave three eighths apart is its own rung
R3), Fugue II in C minor, Fugue IV in C-sharp minor, Fugue V in D major, and Fugue VIII in E-flat
minor, whose head is J. S. Bach's (WTC I/8, BWV 853).

## Weak spots

- **The growth curve flattens.** Real lines reach 9–11 by bars 33–39 and stay there. The other
  ten voices enter in c0. They are staggered across the bar, but it is still a step from 11 to 21,
  not the steady climb to 24 that the brief asked for. Several voices that have entered then rest
  for long spans: T2 bars 23–36, Br2 22–35, Br3 and Br4 26–39, B1 for most of 21–37. I tried
  thickening bars 35–38 with extra parts, but the only free slots were held notes, so I left
  those bars as they are.
- **Doubled sevenths and leading tones: 26.** Half of them are in the convergence, where twenty
  voices share four-note chords. The rest are scattered single beats (for example b16.1, b22.2).
- **The dissonance count depends on my own plan.** "0 unresolved" is measured against
  `harmonic_plan`, which I wrote. The plain critic reads 122 unresolved, mostly chord sevenths and
  pedal chords.
- Stepwise motion is 52.5 %. The U knocks, the pedal knocks and the Fugue V tattoo make 12.6 % of
  the moves repeated notes.
- Low-register seconds: 28. Most of them are pedal-chord tones and U-landing appoggiaturas
  (b28–b35, b39).
- Each guest scored 15–24 against the cantus alone, rougher than a stretto between partners
  designed for each other. Fugue VIII keeps its E-flat spelling over a D#-minor harmony.
- The release is thin: 4–6 voices in bars 53–59. The last chord is a held tonic in all 25 voices
  by design.
- I have not heard the piece. The tempo map and the dynamic plan (velocity offsets per bar) are
  untested by ear.
