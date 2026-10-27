# Fugue XXIV in B minor, twenty-five voices

63 bars of 4/4. Quarter = 63 for the build-up, pushing to 69 (reached at bar 37, held to
bar 41). It broadens to 58 for the cantus (bars 43–51) and to 50 by the start of the release
(bar 54). The release slows to 38.
The rendered audio lasts 4:18. Sources: `fugue.py` assembles `build1.py` … `build5.py`
(build-up), `conv_a.py`, `conv_b.py`, `conv_c.py` (convergence) and `release.py`. The shared
material is in `xxiv.py`. Built score: `fugue.json`. Renders: `renders/fugue.{pdf,mid,musicxml,ly,mp3}`
(Bach–Lehman, PDF engraved by LilyPond), `renders/fugue-equal.mp3` (equal temperament) and
`renders/fugue-spatial.mp3` (ring layout). The stage-1 study is `convergence.py` → `convergence.json`.
No prelude was written.

I cannot hear the renders. Nothing here describes how the piece sounds. Every statement comes
from the score and the tools.

This is the second version. What changed, and why, is in **Second pass** below; the
before/after numbers are in **Measurements**.

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
| cantus | S ×4, two octaves down (`B2:16 D3:8 C#3:8 E#2:24 …`) | whole notes and longer, Contrabass, bars 43–53 |

The mobile bass is free in every section. It leaps where S's own harmony needs it, and it
never doubles a theme in octaves.

## Form

| bars | section | what happens |
|---|---|---|
| 1–11 | exposition | A3 S; T2 answer in F# minor with CS1 above it in A3; B1 S in the bass with CS1 in T2; S2 answer on top. Four voices |
| 11–17 | codetta, S in D | U appears (T2, Br2), R appears (A5, T4); A1 S in D with CS1 in S2; episode through G7–C–F#ø–B7 to E minor |
| 18–20 | **mirror stretto** | S1 enters with I in E minor over a texture thinned to five voices. Half a bar later T3 enters with S in D (finder cost 6, no parallels). Neapolitan sixth – cadential 6/4 – E7 in A minor, turned aside to B7 – E minor, then on towards D minor |
| 21–25 | S in C, bass | B2 enters with the subject in C as a bass. S3's line copies CS1's opening shape; the cadence turns to C major. Br3 enters knocking (U); Br2 returns with U |
| 26–28 | S/I stretto | T4 sings S in A minor and A4 enters with I on B, half a bar later (in this register the finder's fifths become fourths). S1 returns over the E half-diminished chord |
| 29–31 | S in E with CS1 | A5 S, A2 CS1 (new voice), S1 descant, T4's R, Br2 a line under the tenors, T2 a long breath (B–C–G–B–C#), A1 knocking |
| 32–36 | **dominant pedal on C#** | B2 holds C#2 from 32.4½ to the end of bar 36. Over it: the subject's head climbs T5 (b32), A3 (b33), S4 (b34); S3 sings CS1 complete (32.2–34.4); A1 sings **Fugue V's head** transposed to C# major (34.3–35.2); Br2 sings **Fugue VIII's head** transposed to F# minor (35.3–36.4), whose last note resolves into bar 37; B3 knocks U on the pedal (b33–34, again b36–37). S1, S2, A2, A4, A5, T2, Br3, Br5 and B1 sustain and suspend. Harmony: 32 i \| V/V–V; 33–34 i⁶₄ \| V(7), the heads' B# as appoggiaturas; 35 V7 \| i⁶₄; 36 V7 – V – i |
| 37–41 | S ×2 in F# minor | B2 in augmentation; S3 sings CS1 in augmentation complete except its last note (the convergence takes that over). Long-breath lines in S1, S2, A4, T5; I's head in T3 (b37, F# minor) and A2 (b38, on D# over G#7); U in Br2 (b37), T2 (b38), A3 (b39); R in A5 (b38), T4 (b40), T3 (b41). Harmony F#m – G#ø7 – G#7/B# – C#7 – F#7/A# – Bm – G (Neapolitan) – C#ø7 – F#7 – Bm/D – B#°7 – C#m/E – C#7/E# |
| 42 (c0) | lead-in, F#7 | one A# (S2) and one E per beat (A5 on beats 1–2, S1 from beat 3); every other voice sits on F# or C# on the beats |
| 43–53 (c1–c11) | **the convergence** | cantus S ×4 in B5; guests from Fugues V, VIII, II, IV (below) |
| 54–55 | release | the arrival's lines let go one by one; Fugue V's subject in B major (T3) |
| 55–59 | Fugue I's ladder | canon at the octave three eighths apart (Fugue I's own rung R3): Br2 → T5, then A2 → S1, an octave higher. Each entry takes over the last note of the one before. T2 and A4 hold the tonic as inner lines (resting in the canon's F#7 bars) |
| 60–61 | mirror wedge | T1: S's tail G–G#–A–A# ×4; A3: I's tail D#–D–C#–C ×4; over a B pedal (cantus) and an E pedal (Br2). Br3 and T4 join. Em(maj7) – E7 – A – French sixth → both tails close on one B4 |
| 62–63 | last chord | B major. Eleven lines carry on into it (the cantus's B pedal, T1, A3, A2, S1, B1, Br2, T2, A4, Br3, T4); the other fourteen voices arrive one to three per beat over six beats, each from a neighbour note resolving by step, one falling and one or two rising on each beat |

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
| Bass II | 21.3 | subject in C as the bass; B1 hands the bass over |
| Soprano III | 21.4 | CS1-shaped suspension line at the top |
| Baritone III | 24.2½ | U knocks into C major |
| Alto IV | 26.3 | I on B (stretto with T4's S in A) |
| Alto II | 29.2 | CS1 in E minor |
| Tenor V | 32.1 | the head of S, first bar of the pedal |
| Baritone V | 33.1 | a slow line in the pedal choir |
| Bass III | 33.4½ | U knocks on the pedal |
| Soprano IV | 34.1 | the head at the top |
| Bass IV | 37.1 | first bar of S ×2 |
| Baritone IV, Tenor I | 40.3 | C#ø7 over the Neapolitan bar |
| Soprano V | 41.3 | the last upper voice, one beat before c0 |
| Contrabass | 43.1 | the cantus |
| Baritone I | 43.2 | the last voice, in c1 |

Voices moving per bar (critic): 1 1 2 2 2 3 3 4 4 4 4 4 6 5 7 7 7 7 5 5 9 7 6 6 7 8 7 8 8 9 9 10 10
13 14 15 15 16 16 17 20 | **18 19 15 21 17 9 15 18 11 17 20 23** | 22 9 9 8 8 8 8 8 18 6.

The longest rest of any voice between its first entry and c0 is now 10 bars (S2, bars 23–33);
every other voice rests 8 bars or less (first version: Br4 14, Br2 13½, T2 13).

## The convergence, bar by bar (bars 42–53 = c0–c11)

Harmony: c0 F#7 | c1 Bm7 | c2 Bm7/D . C#ø7 | c3 E#°7 | c4 C#7/E# . F#7 | c5 D#m . B/D# . G#m/D# |
c6 A#7/D# . D#m . D#°7 . Em | c7 C | c8 B+ (B D# G) | c9 C/G . E7/G# | c10 A7 . A#°7 | c11 B.

The working rules for every bar: long-breath lines move on beats 1 and 3, suspension chains on
2 and 4, U-figures land on 1 or 3, and the sixteenth runs are relayed. At no onset do two voices
move between the same two pitch classes (checked with `hot.py`). In c0–c4 each beat has one
seventh and one leading tone at most: the F#7 of c0 has its A# only in S2 and one E per beat (A5, then S1); the
Bm7 of c1–c2 has its A only in Fugue V's subject; the C#ø7 has one B; the E#°7 has one D; the
C#7/E# has its E# only in the cantus.

- **c0 (b42)** F#7. S1 climbs C#6–D6–E6. S2 holds A#5. A4 has sixteenths with the A# only between the beats. T2 and S3 knock U upbeats into c1. B2 lands F#2 (end of S ×2); S3 ends CS1 ×2 on C#5.
- **c1 (b43)** The cantus B2 enters (Contrabass) on Bm7. At c1.2½ S1 sings **Fugue V** (D major, its own pitch, an octave up). The cantus's B–D–C# makes D major a harmony of its own line. S5 has sixteenths; T2 lands its U on A (the 7th, before the guest's A); A3's C# and T5's C# are 9–8 suspensions resolved on different beats; Br3 walks in quarters.
- **c2 (b44)** Bm7/D → C#ø7. A1's U lands on G. A5 has sixteenths. Br1 knocks D and rises to B, then C#.
- **c3 (b45)** E#°7 under the cantus's long E#. T1 echoes Fugue V's tattoo (B B B B). T4 has sixteenths; S3 knocks into c4.
- **c4 (b46)** C#7/E# → F#7. S1 has a 4–3 over F#7 (B→A#). A4 has sixteenths. The expected F#7 → Bm is prepared.
- **c5 (b47)** Deceptive turn: the cantus's 1½-bar D# becomes the tonic of **Fugue VIII**. S4 sings it in E-flat minor at its own pitch, at the top of a texture thinned to nine voices so that it can be heard.
- **c6 (b48)** A#7/D# – D#m – D#°7 – Em. VIII's D# is held and resolved up into E minor.
- **c7 (b49)** C major (Neapolitan). At c7.3 **Fugue II** enters at the top in C minor at its own pitch (S1).
- **c8 (b50)** B+ (B D# G): the cantus falls C→B. Fugue II's E♭ is the D#. Thinned to eleven voices.
- **c9 (b51)** C/G → E7/G#. At c9.4 **Fugue IV** enters, transposed to B minor and re-barred from 3/4 (S1).
- **c10 (b52)** A7 → A#°7. Fugue IV peaks on G6 over A#°7.
- **c11 (b53)** Arrival on B major. The cantus's A# resolves to B2 on the downbeat; the other leading notes resolve one after another.

## Guests: sources, placement, verification

Each guest is copied note for note from the first statement in the finished pair's `fugue.json`
(the strings are in `xxiv.py`, `GUESTS`). Each is transposed only by an explicit `transpose`.
`verify_guests.py` runs `tools/stretto_finder.py --against` for each placement. It passes the
guest at its sounding pitch and the line it was fitted to, with `--forms rectus --steps 0` and
the actual entry distance. Results are in `guest-verification.json`.

| guest | source | where | finder vs. its partner | cost | parallels | 2-voice unresolved |
|---|---|---|---|---|---|---|
| Fugue V | `cycle/05-d-major` | S1, b43.2½ (c1), D major (own key), 8ve up | the cantus | 26 | 0 | 1 |
| Fugue VIII | `cycle/08-e-flat-minor` (head = Bach, BWV 853) | S4, b47 (c5), E♭ minor (own key) | the cantus | 22 | 0 | 1 |
| Fugue II | `cycle/02-c-minor` | S1, b49.3 (c7), C minor (own key) | the cantus | 15 | 0 | 0 |
| Fugue IV | `cycle/04-c-sharp-minor` (3/4, re-barred) | S1, b51.4 (c9), down a whole step to B minor | the cantus | 24 | 0 | 1 |
| Fugue V | as above | T3, b54, B major | the B1 pedal | 10 | 0 | 0 |
| Fugue I | `cycle/01-c-major` | Br2 b55.4½ → T5 b56.2; A2 b57.4½ → S1 b58.2 (B major) | its own canon at the octave, 3 eighths (Fugue I's rung R3) | 12 each | 0 | 0 |

New in this version, in the pedal: the *heads* of Fugue V (its first bar, `A4:4 D5:2 D5:1 D5:1
F#5:2 F#5:1 F#5:1 A5:4`, down a semitone to C# major, A1 b34.3) and of Fugue VIII (its whole
subject, `Eb4:4 Bb4:4 Cb5:3 Bb4:1 Ab4:2 Gb4:2 F4:2 D4:2 Eb4:4`, up a minor third to F# minor,
Br2 b35.3). They are written as explicit transpositions in `build4.py` but are not declared as
theme entries, because the Fugue V quotation is a fragment; the finder was not run on them.

## Second pass: what changed

1. **The convergence's clashes.** The first version's c0–c4 voiced several sevenths and
   leading tones in four to six voices and kept non-chord suspensions on the beats of the
   diminished chords, so the critic counted 10–37 unresolved pairs per bar in b41–44 (old
   numbering). Every free voice of c0–c4 was rewritten under the rule above (one seventh, one
   leading tone per beat; suspensions resolved by step on a weak beat; held notes over a change
   of harmony continue by step). The cantus and the guests are unchanged. The few flags left
   in the early bars (b11, b16, b19, b25) were fixed the same way, by hand: CS1's last note
   now falls to A, two inner notes became step resolutions, a run turns round by step.
2. **The growth curve.** Two bars were added to the dominant pedal (now bars 32–36), so the
   convergence starts at bar 42. From bar 28 the voices join about one per bar (8 → 20 by
   bar 41): CS1 complete over the pedal, the subject's head three times, the heads of Fugues V
   and VIII, the inversion's head twice over S ×2, U and R figures, and long-breath lines.
   Where a line had been given to a voice entering late (T1's S in A, Br4's and Br1's U figures),
   it was handed to an earlier voice that was resting (T4, Br2), so the late voices enter
   when they are needed and stay.
3. **Doubled sevenths / leading tones** went from 26 to 1: the convergence rule above, plus
   single fixes in bars 16, 17, 20, 22, 25 and 26.
4. **The ending.** The release keeps 8–9 lines in every bar between the arrival and the last
   chord (first version: 4–6). T2 and A4 hold the tonic as inner lines and move with the wedge;
   Br3 and T4 join for the wedge. Eleven lines carry on into the last chord, and the other
   fourteen voices arrive one to three per beat over six beats, each by step.

## Measurements

All numbers come from `tools/critic.py` (as it stands now), `texture.py` (it reproduces
`diagnosis/inspect_actual_texture.py`), `nct.py` (it classifies every non-chord tone against my
written harmonic plan, stored in `fugue.json` as `harmonic_plan`), `issues.py` (one listing of
the critic's flags with what each note does next) and `check.py` (each theme against its own
prototype). The old finale is `editions/complete-cycle/scores/24-fugue-b-minor.json`.

| measure | old finale | first version | now |
|---|---|---|---|
| bars / duration (render) | – / 385.7 s | 61 / 250 s | 63 / 258 s |
| parallels_error / weak | 0 / – | 0 / 0 | **0 / 0** |
| beat_parallels | 0 | 2 | **0** |
| critic dissonance_unresolved | 2 | 122 | **0** |
| bad_doublings (7th or leading tone doubled on a beat) | 11 | 26 | **1** |
| stepwise_pct / leap ≥ 4th / repeated | 32.8 / 40.5 / – | 52.5 / 17.0 / 12.6 | 55.8 / 16.2 / 10.9 |
| low_register_seconds | 50 | 28 | 58 (worse; see weak spots) |
| voice crossings | 399 | 68 | 89 |
| themes verified exact | – | 26 / 26 | 26 / 26 |
| mean moving voices, whole piece | – | 8.64 | 9.84 |
| … build-up from b26 to c0 | – | 8.3 (b26–39) | 12.2 (b26–41) |
| … convergence c0–c11 | 22.4 (old tutti) | 17.9 | 16.9 |
| … release, between arrival and last chord | – | 4–6 | 8–9 (mean 8.3) |
| cantus window c1–c11: distinct pitch classes per instant | exactly 3 | 4.78 | 4.56 (≥4 at 86 %, ≥5 at 43 %) |
| cantus window: mean sounding parts / moving per bar | 25.0 / 22.4 | 15.8 / 18.0 | 15.1 / 16.8 |

The convergence's mean moving count fell a little: in c0 three voices tie into the bar from
bar 41 (A1, T3, B1: the critic counts them as held), and in c2 (15) several voices rest at the
C#ø7, where only one B is allowed. Bars c5 and c8 (9 and 11 movers) are thinned on purpose
so that Fugues VIII and II can be heard.

### What the critic still flags, and why it stays

- **Unresolved dissonances: none.**
- **Doubled leading tone, b9.2 (S2 B#4 = C5, A3 B#4):** the answer's B# and CS1's B# meet
  at the unison for an eighth. Both notes are theme notes; I left them.
- **Low-register seconds (58):** 19 are the last chord's low neighbour notes (C#2, A#2, C#3)
  against the B1 pedal; 12 are the release's bass line moving against the same pedal; 9 are
  in the convergence; 18 are in bars 27–41, most in the new low lines of the pedal and S ×2
  bars (for example Br5 F#2 against Br3 G#2, b33.3). Any step into a low chord tone forms a second with the pedal or a neighbouring chord
  tone, so I kept the step arrivals the brief asked for.
- `hot.py` still lists three octaves reached in contrary motion (b29.3, b29.4½, b31.3); the
  critic does not count them as parallels.

## Method

Notes are written as literal wtclib token strings, placed at bar.beat by `Score.put` and
`Score.theme` in `xxiv.py`. Themes are explicit `transpose` and `scale_rhythm` calls on the
material. Software was used only to propose placements (`stretto_finder.py`: the mirror stretto
I-in-E with S-in-D at half a bar; S-in-A with I-on-B; Fugue V and Fugue I in B; the chord-plan
fit for the guests) and to report problems (`check.py`, `hot.py`, `issues.py`, `nct.py`,
`grid.py`, `texture.py`). Every collision was fixed by rewriting a free line by hand. No tool
chose, inserted or altered a note.

## Credits

Subject, countersubject, figures and all free lines: Claude, for Sam. Guest subjects are quoted
from this edition: Fugue I in C major (its canon at the octave three eighths apart is its own rung
R3), Fugue II in C minor, Fugue IV in C-sharp minor, Fugue V in D major, and Fugue VIII in E-flat
minor, whose head is J. S. Bach's (WTC I/8, BWV 853).

## Weak spots

- **The pedal and S ×2 bars rely on unisons.** With 15–20 voices on a dominant pedal and on
  seventh chords that allow one seventh and one leading tone, most added voices double the
  root or fifth, often at the unison, and several (A3, A4, T2, Br3) sustain C# as an inner
  pedal for a bar or two. The count rises steadily, but some of the added lines are long
  notes rather than themes.
- **The release's inner lines are plain.** T2 and A4 hold B for most of bars 55–59 and rest
  in the canon's F#7 bars; every move they could make there collided with the canon.
- Low-register seconds doubled (28 → 58), mostly in the last chord and the release (above).
- The new E#°7 bar (c3) arpeggiates the diminished chord: the critic notes two augmented
  seconds and a tritone leap in S2, S5 and A1 there.
- Each guest scored 15–26 against the cantus alone, rougher than a stretto between partners
  designed for each other. Fugue VIII keeps its E-flat spelling over a D#-minor harmony.
- The convergence's moving count dips in c2 (15 voices), where the C#ø7 allows one B.
- I have not heard the piece. The tempo map and the dynamic plan (velocity offsets per bar) are
  untested by ear.
