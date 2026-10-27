# Fugue XXIV in B minor, twenty-five voices

63 bars of 4/4. Quarter = 63 for the build-up, pushing to 69 (reached at bar 37) and held
through the convergence to bar 51; it broadens over c10–c11 (bars 52–53) into the arrival,
the release runs at 58 until the wedge (bar 60), then slows to 46 and 38 (tempo map from the
second review). The rendered audio lasts 4:04. Sources: `fugue.py` assembles `build1.py` … `build5.py`
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

A twelve-tone subject belongs to B minor and drives the whole piece, as in BWV 869, the
B-minor fugue that ends Bach's WTC I, whose subject also uses all twelve pitch classes; this
finale answers it in the same key. The decisive combination
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
| 32–36 | **dominant pedal on C#** | B2 holds C#2 from 32.4½ to the end of bar 36. Over it: the subject's head climbs T5 (b32), A3 (b33), S4 (b34); S3 sings CS1 complete (32.2–34.4); A1 sings **Fugue V's head** transposed to C# major (34.3–35.2); Br2 sings **Fugue VIII's head** transposed to F# minor (35.3–36.4), whose last note resolves into bar 37; B3 knocks U on the pedal (b33–34, again b36–37). S1, S2, A2, A4, A5, T2, Br3 and Br5 sustain and suspend, each on its own pitch (since the second review a voice that could only double another rests). Harmony: 32 i \| V/V–V; 33–34 i⁶₄ \| V(7), the heads' B# as appoggiaturas; 35 V7 \| i⁶₄; 36 V7 – V – i |
| 37–41 | S ×2 in F# minor | B2 in augmentation; S3 sings CS1 in augmentation complete except its last note (the convergence takes that over). Long-breath lines in S1, S2, A4, T5; I's head in T3 (b37, F# minor) and A2 (b38, on D# over G#7); U in Br2 (b37), T2 (b38), A3 (b39); R in A5 (b38), T4 (b40), T3 (b41). Harmony F#m – G#ø7 – G#7/B# – C#7 – F#7/A# – Bm – G (Neapolitan) – C#ø7 – F#7 – Bm/D – B#°7 – C#m/E – C#7/E# |
| 42 (c0) | lead-in, F#7 | one A# (S2) and one E per beat (A5 on beats 1–2, S1 from beat 3); every other voice sits on F# or C#, one voice per key: nine to ten real voices |
| 43–53 (c1–c11) | **the convergence** | cantus S ×4 in B5; guests from Fugues V, VIII, II, IV (below). Since the second review 8–12 real voices, each on its own key; at c10.3 seven voices release and re-enter on the arrival (b53), which resolves on the downbeat in 14 voices |
| 54–55 | release | the arrival's lines let go one by one; Fugue V's subject in B major (T3) |
| 55–59 | Fugue I's ladder | canon at the octave three eighths apart (Fugue I's own rung R3): Br2 → T5, then A2 → S1, an octave higher. Each entry takes over the last note of the one before. Six to seven lines over the pedal |
| 60–61 | mirror wedge | T1: S's tail G–G#–A–A# ×4; A3: I's tail D#–D–C#–C ×4; over a B pedal (the Contrabass strikes its B1 again) and an E pedal (Br2). Br3, T4, T2 and A4 join. Em(maj7) – E7 – A – French sixth → both tails close on one B4 |
| 62–63 | last chord | B major. Eleven lines carry on into it (the cantus's B pedal, T1, A3, A2, S1, B1, Br2, T2, A4, Br3, T4); the other fourteen voices arrive one to three per beat over six beats: the upper nine each from a neighbour note resolving by step, the five lowest (Br4, B2, Br5, B3, B4) directly, so that no neighbour note sounds below G3 |

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
| Contrabass | 43.1 | the cantus |
| Soprano V | 44.1 | a sixteenth turn in c2 |
| Tenor I | 47.1 | the chromatic inner line under Fugue VIII |
| Baritone I | 51.4 | under Fugue IV |
| Baritone IV | 56.1 | a line under Fugue I's ladder |
| Bass IV | 63.1 | the last chord's low B |

Since the second review the late voices (S5, T1, Br1, Br4, B4) enter only where they have a
key of their own; until then they rest rather than double another voice at the unison.

Voices moving per bar (critic): 1 1 2 2 2 3 3 4 4 4 4 4 6 5 7 7 7 7 5 5 9 7 6 6 7 8 7 8 8 9 9 8 10
11 10 10 12 13 11 11 13 | **10 11 10 13 11 8 11 11 9 13 12 14** | 12 7 7 6 6 6 7 8 18 5.

The longest rest of any voice between its first entry and c0 is 10 bars (S2, bars 23–33).

## The convergence, bar by bar (bars 42–53 = c0–c11)

Harmony: c0 F#7 | c1 Bm7 | c2 Bm7/D . C#ø7 | c3 E#°7 | c4 C#7/E# . F#7 | c5 D#m . B/D# . G#m/D# |
c6 A#7/D# . D#m . D#°7 . Em | c7 C | c8 B+ (B D# G) | c9 C/G . E7/G# | c10 A7 . A#°7 | c11 B.

The working rules for every bar: long-breath lines move on beats 1 and 3, suspension chains on
2 and 4, U-figures land on 1 or 3, and the sixteenth runs are relayed. At no onset do two voices
move between the same two pitch classes (checked with `hot.py`). In c0–c4 each beat has one
seventh and one leading tone at most: the F#7 of c0 has its A# only in S2 and one E per beat (A5, then S1); the
Bm7 of c1–c2 has one A (T2's or A1's before Fugue V's, then the guest's); the C#ø7 has one B; the E#°7 has one D; the
C#7/E# has its E# only in the cantus. Since the second review a further rule holds: one voice
per key. A voice that could only double another at the unison rests.

- **c0 (b42)** F#7. S1 climbs C#6–D6–E6. S2 holds A#5. A4 has sixteenths with the A# only between the beats. T2 and S3 knock U upbeats into c1. B2 lands F#2 (end of S ×2); S3 ends CS1 ×2 on C#5.
- **c1 (b43)** The cantus B2 enters (Contrabass) on Bm7. At c1.2½ S1 sings **Fugue V** (D major, its own pitch, an octave up). The cantus's B–D–C# makes D major a harmony of its own line. T2 lands its U on A (the 7th, before the guest's A); A3's C# and T5's C# are 9–8 suspensions resolved on different beats; Br3 hands D3 to B1.
- **c2 (b44)** Bm7/D → C#ø7. S5 enters with a sixteenth turn. A1's U lands on G; Br2's F# is held over the C#ø7 and rises to G.
- **c3 (b45)** E#°7 under the cantus's long E#. T4 has sixteenths; S5 rises D–E# into c4.
- **c4 (b46)** C#7/E# → F#7. S1 has a 4–3 over F#7 (B→A#). A4 has sixteenths from beat 2½. The expected F#7 → Bm is prepared.
- **c5 (b47)** Deceptive turn: the cantus's 1½-bar D# becomes the tonic of **Fugue VIII**. S4 sings it in E-flat minor at its own pitch, at the top of a texture thinned to nine voices so that it can be heard.
- **c6 (b48)** A#7/D# – D#m – D#°7 – Em. VIII's D# is held and resolved up into E minor.
- **c7 (b49)** C major (Neapolitan). At c7.3 **Fugue II** enters at the top in C minor at its own pitch (S1).
- **c8 (b50)** B+ (B D# G): the cantus falls C→B. Fugue II's E♭ is the D#. Thinned to eleven voices.
- **c9 (b51)** C/G → E7/G#. At c9.4 **Fugue IV** enters, transposed to B minor and re-barred from 3/4 (S1).
- **c10 (b52)** A7 → A#°7. Fugue IV peaks on G6 over A#°7.
- **c11 (b53)** Arrival on B major. At c10.3 seven voices release; they and the rest arrive on the downbeat, where only four upper appoggiaturas (Fugue IV's A#→B, S2's C#→D#, S3's 4–3, S5's lean) are left to resolve, each within a beat. Bass III adds the low B1.

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
   fourteen voices arrive one to three per beat over six beats, each by step. (Points 2 and 4
   were revised after the second review; see below.)

## Second review

`REVIEW-2.md` found five problems. What I did about each, by hand:

1. **The arrival (b53) landed as a cluster** (13 of 20 voices off the B-major triad on the
   downbeat, resolving over three beats). Adopted the reviewer's tested fix in `conv_c.py`:
   seven voices release at c10.3 and re-enter on the downbeat. With the unison thinning (2)
   the arrival is now 14 voices on 12 keys; the voices off the triad per beat are 4, 1, 0, 0
   (the four upper appoggiaturas: Fugue IV's A#→B, S2's C#→D#, S3's 4–3, S5's lean). T4's run
   now turns down to D#4, and Bass III adds the low B1 under the arrival.
2. **Twenty-five staves, about ten keys.** In c1–c4 17.7 voices sounded on 10.1 pitches. I
   rewrote the free voices of b32–53 under a second rule: one voice per key. In each unison
   group the voice that carries a figure or arrives by step stays; the others rest (each
   removal is marked in the source), and where a voice could move to a free chord member
   in another octave without a new parallel it moved (for example S4's C#6 and Bass III's
   G#2 in c4, T4's D#4 at the arrival). Voices sounding / distinct pitches per beat:

   | bars | before | after |
   |---|---|---|
   | 32–36 pedal | 11.6 / 9.9 | 9.7 / 9.4 |
   | 37–41 S ×2 | 13.7 / 10.4 | 9.8 / 9.3 |
   | 42 c0 | 16.2 / 9.0 | 8.8 / 8.8 |
   | 43–46 c1–c4 | 17.7 / 10.1 | 9.6 / 9.6 |
   | 49–50 c7–c8 | 12.2 / 8.1 | 8.0 / 8.0 |
   | 51–53 c9–c11 | 16.6 / 10.4 | 10.8 / 10.1 |

   b46.1, the reviewer's example (18 voices on 7 keys), now has 10 voices on 10 keys. The
   critic's moving count falls with it (convergence 16.9 → 11.1 per bar): fewer real lines
   rather than more fake ones. The reviewer's walking-baritone layer was not added: with
   the one-seventh rule the D3–A3 band has two or three free keys per beat.
3. **Tempo.** Adopted the proposed map: 69 held through c9, broadened over c10–c11, the release
   at 58 until the wedge, then 46 and 38. The render is 4:04 (was 4:18). The guests now run at
   64–96 % of their own tempos.
4. **The last chord's low neighbour notes** (19 of 58 low clashes): the five lowest voices
   (Br4, B2, Br5, B3, B4) now arrive directly, Bass III ends on F#2 instead of D#2, and the
   Contrabass strikes its B1 pedal again at the wedge (b60). Low clashes 58 → 33.
5. **BWV 869** is named in the premise and the credits. It is not quoted.

Also from the review: Tenor II and Alto IV no longer double the pedal B in b55–59; they enter
with the wedge, so Fugue I's ladder sounds in six to seven lines. Not done: moving Fugue V's head
in the pedal to the top voice (it would need S1's line in b34–35 rewritten). The must-not-touch
passages are unchanged: Fugues VIII and II on top of thinned textures, S ×2 in the bass under
CS1 ×2, the mirror wedge.

## Measurements

All numbers come from `tools/critic.py` (as it stands now), `texture.py` (it reproduces
`diagnosis/inspect_actual_texture.py`), `nct.py` (it classifies every non-chord tone against my
written harmonic plan, stored in `fugue.json` as `harmonic_plan`), `issues.py` (one listing of
the critic's flags with what each note does next) and `check.py` (each theme against its own
prototype). The old finale is `editions/complete-cycle/scores/24-fugue-b-minor.json`.

| measure | old finale | first version | second pass | second review (now) |
|---|---|---|---|---|
| bars / duration (render) | – / 385.7 s | 61 / 250 s | 63 / 258 s | 63 / 244 s |
| parallels_error / weak | 0 / – | 0 / 0 | 0 / 0 | **0 / 0** |
| beat_parallels | 0 | 2 | 0 | **0** |
| critic dissonance_unresolved | 2 | 122 | 0 | **0** |
| bad_doublings (7th or leading tone doubled on a beat) | 11 | 26 | 1 | **1** |
| stepwise_pct / leap ≥ 4th / repeated | 32.8 / 40.5 / – | 52.5 / 17.0 / 12.6 | 55.8 / 16.2 / 10.9 | 59.6 / 15.5 / 9.1 |
| low_register_seconds | 50 | 28 | 58 | 33 |
| voice crossings | 399 | 68 | 89 | 45 |
| themes verified exact | – | 26 / 26 | 26 / 26 | 26 / 26 |
| voices sounding / distinct pitches per beat, b32–41 | – | – | 12.6 / 10.1 | 9.8 / 9.4 |
| … c0–c4 (b42–46) | – | – | 17.4 / 9.9 | 9.4 / 9.4 |
| … c5–c11 (b47–53) | – | – | 12.9 / 8.7 | 9.0 / 8.6 |
| … the arrival, b53 | – | – | 21.8 / 11.2 | 14.0 / 12.2 |
| mean moving voices, whole piece | – | 8.64 | 9.84 | 7.79 |
| … build-up from b26 to c0 | – | 8.3 (b26–39) | 12.2 (b26–41) | 9.9 (b26–41) |
| … convergence c0–c11 | 22.4 (old tutti) | 17.9 | 16.9 | 11.1 |
| … release, between arrival and last chord | – | 4–6 | 8–9 | 6–8 (mean 6.7) |
| cantus window c1–c11: distinct pitch classes per instant | exactly 3 | 4.78 | 4.56 | 4.25 (≥4 at 83 %, ≥5 at 32 %) |
| cantus window: mean sounding parts / moving per bar | 25.0 / 22.4 | 15.8 / 18.0 | 15.1 / 16.8 | 9.3 / 11.2 |

The moving counts fell because the second review asked for real voices rather than many
staves: a voice that could only double another at the unison now rests (see **Second review**).
The voices that remain are on distinct pitches on 95–100 % of their beats. Bars c5 and c8 are
still thinned on purpose so that Fugues VIII and II can be heard.

### What the critic still flags, and why it stays

- **Unresolved dissonances: none.**
- **Doubled leading tone, b9.2 (S2 B#4 = C5, A3 B#4):** the answer's B# and CS1's B# meet
  at the unison for an eighth. Both notes are theme notes; I left them.
- **Low-register seconds (33):** the release's bass line moving against the B1 pedal, the
  pedal choir's low lines (for example Br5 F#2 against Br3 G#2, b33.4) and a few passing notes
  in the build-up. The last chord's low neighbour notes, which made 19 of them, are gone: the
  five lowest voices now arrive directly.
- `hot.py` still lists three octaves reached in contrary motion (b29.3, b29.4½, b31.3); the
  critic does not count them as parallels.

## Method

Notes are written as literal wtclib token strings, placed at bar.beat by `Score.put` and
`Score.theme` in `xxiv.py`. Themes are explicit `transpose` and `scale_rhythm` calls on the
material. Software was used only to propose placements (`stretto_finder.py`: the mirror stretto
I-in-E with S-in-D at half a bar; S-in-A with I-on-B; Fugue V and Fugue I in B; the chord-plan
fit for the guests) and to report problems (`check.py`, `hot.py`, `issues.py`, `nct.py`,
`grid.py`, `texture.py`, and for the second review `unisons.py` and `beatmap.py`, which list
the voices sounding and the distinct pitches on every beat). Every collision was fixed by rewriting a free line by hand. No tool
chose, inserted or altered a note.

## Credits

Subject, countersubject, figures and all free lines: Claude, for Sam. Guest subjects are quoted
from this edition: Fugue I in C major (its canon at the octave three eighths apart is its own rung
R3), Fugue II in C minor, Fugue IV in C-sharp minor, Fugue V in D major, and Fugue VIII in E-flat
minor, whose head is J. S. Bach's (WTC I/8, BWV 853). The model for the whole fugue is the
last fugue of WTC I, BWV 869 in B minor, whose subject is also built on all twelve pitch
classes; this finale answers it in the same key with a twelve-tone subject of its own. BWV 869's
subject is not quoted (its notes were not taken from a verified source, and I did not write
them from memory).

## Weak spots

- **Fewer voices at the climax than the score's 25.** With one voice per key, the convergence
  carries 8–12 real voices (14 at the arrival); the build-up peaks at 13. The climax is now made
  by the cantus, the guests and the harmony rather than by more parts. Four voices (S5, T1, Br1,
  Br4) enter only in or after the convergence, and Bass IV sings only the last chord's low B.
  Several voices rest 10–13 bars inside the convergence and release (Br3 b46–60, A3 b48–60).
- **The growth curve is gentler.** Real voices rise from about 8 (b26) to 13 (b38, b41)
  instead of to 20; the extra parts of the second pass were mostly unisons.
- The E#°7 bar (c3) arpeggiates the diminished chord: the critic notes two augmented seconds
  and a tritone leap in S2, S5 and A3 there.
- Each guest scored 15–26 against the cantus alone, rougher than a stretto between partners
  designed for each other. Fugue VIII keeps its E-flat spelling over a D#-minor harmony.
- I have not heard the piece. The tempo map and the dynamic plan (velocity offsets per bar) are
  untested by ear.
