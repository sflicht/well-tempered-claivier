# Fugue XXIV in B minor, for twenty-five parts

63 bars of 4/4. Quarter = 63 for the build-up, pushing to 69 (reached at bar 37) and held
through the convergence to bar 51; it broadens over c10–c11 (bars 52–53) into the arrival,
the release runs at 58 until the wedge (bar 60), then slows to 46 and 38 (tempo map from the
second review). The rendered audio lasts 4:04. Sources: `fugue.py` assembles `build1.py` … `build5.py`
(build-up), `conv_a.py`, `conv_b.py`, `conv_c.py` (convergence) and `release.py`. The shared
material is in `xxiv.py`. Built score: `fugue.json`. Renders: `renders/fugue.{pdf,mid,musicxml,ly,mp3}`
(Bach–Lehman, PDF engraved by LilyPond), `renders/fugue-equal.mp3` (equal temperament) and
`renders/fugue-spatial.mp3` (ring layout). The stage-1 study is `convergence.py` → `convergence.json`.
The prelude (`prelude.py` → `prelude.json`) is described in **Prelude XXIV** at the end of this file.

I cannot hear the renders. Nothing here describes how the piece sounds. Every statement comes
from the score and the tools.

This is the second version, revised twice since: **Second pass** and **Second review** below,
and **Review response (Nov 2026)** for the owner's review of PR #1. The before/after numbers are
in **Measurements**.

## The premise

A twelve-tone subject belongs to B minor and drives the whole piece, as in BWV 869, the
B-minor fugue that ends Bach's WTC I, whose subject also uses all twelve pitch classes; this
finale answers it in the same key. The decisive combination
was composed first. The subject sounds in four-fold augmentation in the Contrabass, the 25th
part, which enters only for it. Four subjects from earlier fugues of this edition arrive over
it, each where the cantus's own note makes it a tonic or a harmony tone. The build-up was then
written backwards from what the combination needs the listener to know: the subject and its
mirror, the countersubject, the upbeat figure, the run, and two-fold augmentation. The release
was written forwards from the arrival.

The score has twenty-five parts, and it is a fugue for twenty-five parts with selective
participation, not a twenty-five-voice texture. The parts enter one by one through the
build-up; at most fourteen carry independent lines at once (eight to twelve through the
convergence, fourteen at the arrival), a part that could only double another at the unison
rests, and all twenty-five sound together only in the last chord.

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
| 32–36 | **dominant pedal on C#** | B2 holds C#2 from 32.4½ to the end of bar 36. Over it: the subject's head climbs T5 (b32), A3 (b33), S4 (b34); S3 sings CS1 complete (32.2–35.3; its last note, B, now arrives on 35.1); A1 sings **Fugue V's head** transposed to C# major (34.3–35.2); Br2 sings **Fugue VIII's head** transposed to F# minor (35.3–36.4), whose last note resolves into bar 37; B3 knocks U on the pedal (b33–34, again b36–37). S1, S2, A2, A4, A5, T2, Br3 and Br5 sustain and suspend, each on its own pitch (since the second review a voice that could only double another rests). Harmony: 32 i \| V/V–V; 33–34 i⁶₄ \| V(7), the heads' B# as appoggiaturas; 35 V7 \| i⁶₄; 36 V7 – V – i |
| 37–41 | S ×2 in F# minor | B2 in augmentation; S3 sings CS1 in augmentation complete except its last note (the convergence takes that over). Long-breath lines in S1, S2, A4, T5; I's head in T3 (b37, F# minor) and A2 (b38, on D# over G#7); U in T2 (b38) and A3 (b39), after Bass III's (b36–37); R in A5 (b38), T4 (b40), T3 (b41). Harmony F#m – G#ø7 – G#7/B# – C#7 – F#7/A# – Bm – G (Neapolitan) – C#ø7 – F#7 – Bm/D – B#°7 – C#m/E – C#7/E# |
| 42 (c0) | lead-in, F#7 | one A# (S2) and at most one E per beat (A5 on beat 1, S1 from beat 3); every other voice sits on F# or C#, one voice per key: nine to ten real voices |
| 43–53 (c1–c11) | **the convergence** | cantus S ×4 in B5; guests from Fugues V, VIII, II, IV (below). Since the second review 8–12 real voices, each on its own key; at c10.3 the inner voices release (S4 from c10.1 since the third review) and re-enter on the arrival (b53), which resolves on the downbeat in 14 voices |
| 53–56 | release; Fugue I's ladder, rung 1 | Bass IV leads Fugue I's subject in B major from 53.4½ (the bass line of bars 54–55, over the pedal); Baritone I follows an octave higher, three eighths later (Fugue I's own rung R3). Over them the arrival's lines let go and Fugue V's subject returns in B major (T3) |
| 55–60 | the ladder, rungs 2 and 3 | Br2 → T5, then A2 → S1, each rung an octave above the last. Each leader begins on the last note of the leader before (B4's F#3 → Br2, Br2's F#4 → A2), so the ladder climbs three octaves, from Bass IV to Soprano I. Five to seven lines over the pedal |
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
| Bass IV | 53.4½ | leads the first rung of Fugue I's ladder (the bass line of bars 54–55) |
| Baritone I | 54.2 | follows it an octave higher, three eighths later |
| Baritone IV | 56.1 | a slow line under the ladder's second rung |

Since the second review the late voices (S5, T1, Br4) enter only where they have a key of
their own; until then they rest rather than double another voice at the unison. Since the
third review Bass IV and Baritone I, which had sung only the last chord (Baritone I also one
B3 under Fugue IV), enter as the ladder's first rung (see **Review response (Nov 2026)**).

Voices moving per bar (critic): 1 1 2 2 2 3 3 4 4 4 4 4 6 5 7 7 7 7 5 5 9 7 6 6 7 8 7 8 8 9 9 8 10
11 10 10 11 12 11 11 12 | **10 11 10 13 11 8 11 11 9 11 12 14** | 10 5 7 6 6 5 7 8 18 5.

The longest rest of any voice between its first entry and c0 is 10 bars (S2, bars 23–33).

## The convergence, bar by bar (bars 42–53 = c0–c11)

Harmony: c0 F#7 | c1 Bm7 | c2 Bm7/D . C#ø7 | c3 E#°7 | c4 C#7/E# . F#7 | c5 D#m . B/D# . G#m/D# |
c6 A#7/D# . D#m . D#°7 . Em | c7 C | c8 B+ (B D# G) | c9 C/G . E7/G# | c10 A7 . A#°7 | c11 B.

The working rules for every bar: long-breath lines move on beats 1 and 3, suspension chains on
2 and 4, U-figures land on 1 or 3, and the sixteenth runs are relayed. At no onset do two voices
move between the same two pitch classes (checked with `hot.py`). In c0–c4 each beat has one
seventh and one leading tone at most: the F#7 of c0 has its A# only in S2 and at most one E per beat (A5 on beat 1, S1 from beat 3); the
Bm7 of c1–c2 has one A (T2's or A1's before Fugue V's, then the guest's); the C#ø7 has one B; the E#°7 has one D; the
C#7/E# has its E# only in the cantus. Since the second review a further rule holds: one voice
per key. A voice that could only double another at the unison rests.

- **c0 (b42)** F#7. S1 climbs C#6–D6–E6, its E arriving on beat 3 (A5's E is on beat 1 only, so it no longer rubs against A4's E#). S2 holds A#5. A4 has sixteenths with the A# only between the beats. T2 and S3 knock U upbeats into c1. B2 lands F#2 (end of S ×2); S3 ends CS1 ×2 on C#5.
- **c1 (b43)** The cantus B2 enters (Contrabass) on Bm7. At c1.2½ S1 sings **Fugue V** (D major, its own pitch, an octave up). The cantus's B–D–C# makes D major a harmony of its own line. T2 lands its U on A (the 7th, before the guest's A); A3's C# and T5's C# are 9–8 suspensions resolved on different beats; Br3 hands D3 to B1.
- **c2 (b44)** Bm7/D → C#ø7. S5 enters with a sixteenth turn. A1's U lands on G; Br2's F# is held over the C#ø7 and rises to G.
- **c3 (b45)** E#°7 under the cantus's long E#. T4 has sixteenths; S5 rises D–E# into c4.
- **c4 (b46)** C#7/E# → F#7. S1 has a 4–3 over F#7 (B→A#). A4 has sixteenths from beat 2½. The expected F#7 → Bm is prepared.
- **c5 (b47)** Deceptive turn: the cantus's 1½-bar D# becomes the tonic of **Fugue VIII**. S4 sings it in E-flat minor at its own pitch, at the top of a texture thinned to nine voices so that it can be heard.
- **c6 (b48)** A#7/D# – D#m – D#°7 – Em. VIII's D# is held and resolved up into E minor.
- **c7 (b49)** C major (Neapolitan). At c7.3 **Fugue II** enters at the top in C minor at its own pitch (S1).
- **c8 (b50)** B+ (B D# G): the cantus falls C→B. Fugue II's E♭ is the D#. Thinned to eleven voices.
- **c9 (b51)** C/G → E7/G#. At c9.4 **Fugue IV** enters, transposed to B minor and re-barred from 3/4 (S1). Under its entry S4 holds B4 and the cantus's G# is the only leading tone (since the third review A2 enters at c10.2, S4 rests through c10, and Baritone I's single B3 here is gone).
- **c10 (b52)** A7 → A#°7. Fugue IV peaks on G6 over A#°7.
- **c11 (b53)** Arrival on B major. At c10.3 the inner voices release (S4 already at c10.1); they and the rest arrive on the downbeat, where only four upper appoggiaturas (Fugue IV's A#→B, S2's C#→D#, S3's 4–3, S5's lean) are left to resolve, each within a beat. Bass III adds the low B1. Bass IV's upbeat F#2 at c11.4½ begins the release's ladder.

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
| Fugue I | `cycle/01-c-major` | B4 b53.4½ → Br1 b54.2; Br2 b55.4½ → T5 b56.2; A2 b57.4½ → S1 b58.2 (B major) | its own canon at the octave, 3 eighths (Fugue I's rung R3) | 12 each | 0 | 0 |
| Fugue V with Fugue I | as above | T3 against B4 (an eighth later); Br1 against T3 (a quarter later), b54–55 | each other | 11 / 18 | 0 / 0 | 0 / 1 |

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

## Review response (Nov 2026)

The owner's review of PR #1 (written with ChatGPT, offered as claims to check rather than
orders) asked two things of this fugue. First, the "25 real voices" claim did not survive the
second review's thinning: in the committed score Bass IV had one note, the last chord's low B,
doubling the Contrabass's pedal; Baritone I had three notes, one of them a stray B3 under
Fugue IV; Baritone IV had nine. The review asked me either to describe the piece accurately or
to give the thin parts necessary roles, without filler and without losing the transparency.
Second, the critic now checks that a resolution really arrives (commit 09df800), and under the
corrected check this fugue went from 0 unresolved dissonances to 17, with 26 "unverified
stepwise continuations".

On the voices I did both, in that order. The piece is described everywhere in this folder as
a fugue for twenty-five parts with selective participation: the parts enter one by one, at
most fourteen carry independent lines at once, and all twenty-five sound together only in the
last chord (the score's subtitle and instrument line now say so). I did not re-thicken the
convergence. Then I looked for a place where a thin part could do something the music needs,
and found one that the piece's own logic asks for: Fugue I's ladder in the release. Its rungs
are canons at the octave, three eighths apart, each rung an octave above the last, each leader
starting on the last note of the leader before. With two rungs (Baritone II/Tenor V, Alto
II/Soprano I) the ladder began in the middle of the texture. It now has a first rung in the
two lowest free parts: Bass IV leads from 53.4½, so the ladder starts from the bass, right
after the arrival, and Baritone I follows. Bass IV's last note, F#3, is the note on which
Baritone II begins, as the rule of the ladder requires, and the ladder climbs three octaves,
from Bass IV to Soprano I. The rung is a quotation (`check.py`: 28 of 28 themes exact) and
`verify_guests.py` gives it the same result as the other rungs (cost 12, no parallels, nothing
unresolved). It replaces filler rather than adding to it: Bass I's walk, the inner lines of
A1 and A5 and Baritone II's held F#3 in bars 54–55 made way, so those bars carry 6.5 voices a
beat (8.6 before), three of them thematic (Fugue V in T3 and the two rung voices). Soprano I
and II were rewritten in bar 55 to the ladder's harmony.

I did not invent jobs for Baritone IV and Baritone V. They are accompanying lines (the ladder's
inner drone in bars 56–59; slow lines in the pedal choir, bars 33–41), and the description
says so. Every other part has at least one thematic entry or figure (S5, T1 and Bass III, the
next thinnest, carry U figures, the wedge's tail of the subject and the knocks on the pedal).
Here I disagree with the review: an accompanying part in a large score is a legitimate part,
and the review itself allows rests and reinforcement. What was wrong was the claim, not the
existence of such parts.

On the critic: of the 17 unresolved dissonances I fixed 14, each by rewriting a free line, and
kept three (listed below with the reason). Every fix kept the declared themes and the guests
note for note (`check.py` 28 of 28, `verify_guests.py` unchanged for the convergence). The free
U figures were re-pitched in two places and removed in one, and Soprano III's complete CS1
(b32–35) has its last note delayed by half a bar. Several of the fixes uncovered faults that the old voicing had hidden from the chord check,
which I fixed too. By bar:

- b16–17: Alto I no longer anticipates C over the G bass (B, then C with the bass); Alto III
  resolves its seventh (F to E) and rests; Tenor II's knocking upbeat now knocks on E and leans
  on C. Before, it landed on E, doubling Soprano II's seventh, and Alto III then descended in
  parallel seconds with it. Baritone II's upbeat knocks on A and leans on F# (its D# had doubled
  Soprano II's leading tone); Alto I rests from 17.3; Tenor IV's run starts beat 3 on B.
- b18, b21: Alto III falls A–G into bar 18; Soprano I's line after the inversion ends with a 9–8 (E–D)
  instead of F5, which had sounded the resolution note above Alto V's 4–3 suspension.
- b30: Baritone II resolves its seventh C down to B (it rose to D, doubling CS1's D5).
- b32: Soprano I breathes and re-enters with the pedal (its held C#6 was a fourth over G#2
  while Soprano III resolved C# to B#).
- b34–35: CS1's last note (Soprano III) arrives on 35.1, so the head's B# no longer meets B and
  C# at once (a three-note cluster at 34.4). Alto III no longer turns B#–C# against Baritone II's
  C#–D (parallel semitones).
- b37: Baritone II's knocking upbeat is gone. It repeated Bass III's of b36 at the same pitch,
  and its C# and A clashed with Tenor III's inversion head (B#–B).
- b39: Tenor II's U leans E–D (D# was a fourth over the bass A#); Soprano II rests after F#5
  instead of descending in seconds against CS1 ×2.
- b41: Soprano IV's lone D#5 (a semitone against Soprano III's held D5) is gone.
- b42 (c0): Soprano I's E arrives on beat 3 and Alto V's E is on beat 1 only, so the F#7 is
  clean on beat 2 and Alto IV's E# no longer rubs against an E.
- b51–52 (c9–c10): Baritone I's B3, Alto II's G# (a second leading tone over the cantus's G#)
  and Soprano IV's early C# (a second against Soprano V's knocking D) are gone; Soprano IV holds
  B4 under Fugue IV's entry and rests through c10.
- b55, b58: Baritone II's held F#3 is gone (the ladder); Tenor V and Baritone II no longer walk
  down in parallel sevenths.

Result with the corrected critic: unresolved 17 → 3, unverified 26 → 17, parallels and
beat-to-beat parallels still 0, doubled sevenths or leading tones still 1 (b9.2, a theme
collision, below), low-register seconds 33 → 35 (the new low rung against the pedal). Bach's
WTC I fugues show 0–20 unresolved and 0–11 unverified under the same check, so the 17
unverified flags here are places to check by ear, not errors; each is listed below.

What I have not tested: I cannot hear the result. The new bars 54–55 put two guests together,
Fugue V in the tenor and Fugue I's first rung in sixteenths in the bass and baritone over the
pedal, at quarter = 58. Verified two at a time, they score 11 (Fugue V against the leader) and
18 (the follower against Fugue V, one two-voice unresolved that the full-score critic does not
flag). Whether the low sixteenths sound clear there is a listening question.

## Measurements

All numbers come from `tools/critic.py` (as it stands now), `texture.py` (it reproduces
`diagnosis/inspect_actual_texture.py`), `nct.py` (it classifies every non-chord tone against my
written harmonic plan, stored in `fugue.json` as `harmonic_plan`), `issues.py` (one listing of
the critic's flags with what each note does next) and `check.py` (each theme against its own
prototype). The old finale is `editions/complete-cycle/scores/24-fugue-b-minor.json`.

| measure | old finale | first version | second pass | second review | review 3 (now) |
|---|---|---|---|---|---|
| bars / duration (render) | – / 385.7 s | 61 / 250 s | 63 / 258 s | 63 / 244 s | 63 / tempo map unchanged (not re-rendered here) |
| parallels_error / weak | 0 / – | 0 / 0 | 0 / 0 | 0 / 0 | **0 / 0** |
| beat_parallels | 0 | 2 | 0 | 0 | **0** |
| dissonance_unresolved, critic before 09df800 | 2 | 122 | 0 | 0 | – |
| unresolved / unverified, corrected critic (09df800) | – | – | – | 17 / 26 | **3 / 17** |
| bad_doublings (7th or leading tone doubled on a beat) | 11 | 26 | 1 | 1 | **1** |
| stepwise_pct / leap ≥ 4th / repeated | 32.8 / 40.5 / – | 52.5 / 17.0 / 12.6 | 55.8 / 16.2 / 10.9 | 59.6 / 15.5 / 9.1 | 59.9 / 16.0 / 8.3 |
| low_register_seconds | 50 | 28 | 58 | 33 | 35 |
| voice crossings | 399 | 68 | 89 | 45 | 43 |
| themes verified exact | – | 26 / 26 | 26 / 26 | 26 / 26 | 28 / 28 |
| voices sounding / distinct pitches per beat, b32–41 | – | – | 12.6 / 10.1 | 9.8 / 9.4 | 9.5 / 9.2 |
| … c0–c4 (b42–46) | – | – | 17.4 / 9.9 | 9.4 / 9.4 | 9.4 / 9.4 |
| … c5–c11 (b47–53) | – | – | 12.9 / 8.7 | 9.0 / 8.6 | 8.8 / 8.4 |
| … the arrival, b53 | – | – | 21.8 / 11.2 | 14.0 / 12.2 | 14.0 / 12.2 |
| … release, b54–55 | – | – | – | 8.6 / 8.5 | 6.5 / 6.4 |
| … the last chord, b62–63 | – | – | – | 20.8 / 14.1 | 20.8 / 14.1 |
| mean moving voices, whole piece | – | 8.64 | 9.84 | 7.79 | 7.63 |
| … build-up from b26 to c0 | – | 8.3 (b26–39) | 12.2 (b26–41) | 9.9 (b26–41) | 9.7 (b26–41) |
| … convergence c0–c11 | 22.4 (old tutti) | 17.9 | 16.9 | 11.1 | 10.9 |
| … release, between arrival and last chord | – | 4–6 | 8–9 | 6–8 | 5–10 (mean 6.8, b54–61) |
| cantus window c1–c11: distinct pitch classes per instant | exactly 3 | 4.78 | 4.56 | 4.25 (≥4 at 83 %, ≥5 at 32 %) | 4.21 (≥4 at 83 %, ≥5 at 32 %) |
| cantus window: mean sounding parts / moving per bar | 25.0 / 22.4 | 15.8 / 18.0 | 15.1 / 16.8 | 9.3 / 11.2 | 9.2 / 11.0 |

The moving counts fell because the second review asked for real voices rather than many
staves: a voice that could only double another at the unison now rests (see **Second review**).
The third review's fixes removed a few more stray notes (see **Review response**).
The voices that remain are on distinct pitches on 95–100 % of their beats. Bars c5 and c8 are
still thinned on purpose so that Fugues VIII and II can be heard.

### What the critic still flags, and why it stays

Counts are from the corrected critic (09df800), which accepts a resolution only if the step comes
within a beat and lands on a consonance with the partner.

- **Unresolved dissonances: 3.**
  - b43.1, T2 A4 against S2 B5: the seventh and root of Bm7. Tenor II's U lands on the seventh
    before Fugue V's A and falls A–G–F#; Soprano II leaps to F#5 to clear the guest's entry. The
    critic cannot see Bm7 here because two 9–8 suspensions (A3, T5) sound on the same beat, so it
    tests the pair on its own.
  - b44.3, A1 G5 against the cantus's C#3: Alto I's U lands its lean on the G of C#ø7 (a chord
    tone, a tritone over the cantus) and steps to F#, where Alto I stops. The guest's A6 and
    Baritone II's retarded F#3 hide the chord from the critic. The F# is a real loose end; every
    continuation I tried made a unison with Soprano II or Soprano IV.
  - b48.1, S4 F5 against the cantus's D#3: Fugue VIII's own cadence (F–D–E♭ around its tonic)
    over the cantus's held E♭ = D#. Both are quotations and neither can move. `verify_guests.py`
    counts this as the guest's one two-voice unresolved against the cantus.
- **Unverified stepwise continuations: 17** (check by ear). The resolving step is there; the
  partner moves at the same time, or the template list cannot name the chord.
  - Exposition and middle entry, b6.3, b9.1 (2), b9.3, b11.2, b14.1: CS1's suspensions resolving
    while the bass moves. At b9.3 and b14.1 the 9–8 lands on the root of a V4/2 as the bass
    passes to the seventh; at b11.2 CS1's last note falls to A as the bass moves F# to B; at b6.3
    CS1's 4–3 lands on the E#–B tritone of C#7/E#; at b9.1 Tenor II's free line passes D–C#
    against the answer's lean.
  - The circle of fifths, b20.3 and b21.1 (3): Soprano II and Alto V exchange A and G; Alto V's
    4–3 resolves as the bass moves D to G, so its F is the seventh of G7.
  - b29.1, b29.2: Baritone II's U leans F#3 (a 9–8 over E2) under the subject's head.
  - b30.3 (2): CS1's 9–8 (A2, E5–D5) resolves as the bass moves D to E, so D is the seventh of E7.
  - b51.4, b52.2: Soprano V's knocks on D (the seventh of E7, a tritone over the cantus's G#)
    and its U lean (B5, a 9–8 over A7) against Tenor IV's run. Fugue IV enters on F#, the ninth,
    so the critic cannot name E7.
  - b60.2: Soprano I's E6 against Alto III's D#5, both in the wedge's E minor–major seventh, a
    chord the critic has no template for.
- **Doubled leading tone, b9.2 (S2 B#4 = C5, A3 B#4):** the answer's B# and CS1's B# meet
  at the unison for an eighth. Both notes are theme notes; I left them.
- **Low-register seconds (35, was 33):** the release's bass lines moving against the B1 pedal
  (now including Bass IV's rung, whose C#3 and A#2 rub against B1), the
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
the voices sounding and the distinct pitches on every beat; for the third review the corrected
`tools/critic.py`). Every collision was fixed by rewriting a free line by hand. No tool
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

- **Twenty-five parts, at most fourteen lines.** With one voice per key the convergence carries
  8–12 real lines (14 at the arrival) and the build-up peaks at 12. The climax is made by the
  cantus, the guests and the harmony, not by the number of parts. All twenty-five sound together
  only in the last chord, where unisons cannot be avoided (20.8 voices on 14.1 pitches a beat).
  Baritone IV and Baritone V are accompanying lines with no thematic entry. Several voices rest
  10–13 bars inside the convergence and release (A1 b52–61, A3 b49–59, Br3 b47–59).
- **Two guests at once in bars 54–55** (Fugue V in the tenor, Fugue I's first rung in the bass and
  baritone), in sixteenths in the low register. Verified two at a time, not heard.
- **The growth curve is gentler.** Real voices rise from about 8 (b26) to 12 (b38, b41)
  instead of to 20; the extra parts of the second pass were mostly unisons.
- The E#°7 bar (c3) arpeggiates the diminished chord: the critic notes two augmented seconds
  and a tritone leap in S2, S5 and A3 there.
- Each guest scored 15–26 against the cantus alone, rougher than a stretto between partners
  designed for each other. Fugue VIII keeps its E-flat spelling over a D#-minor harmony.
- I have not heard the piece. The tempo map and the dynamic plan (velocity offsets per bar) are
  untested by ear.

---

# Prelude XXIV in B minor: *Preludio per i 24 tuoni*

48 bars of 4/4 for one keyboard player: two upper voices over a walking bass in eighths, the
texture of Bach's B-minor Prelude in Book I (BWV 869, Andante). Source `prelude.py` (every note
a literal bar string) → `prelude.json`. Renders: `renders/prelude.{pdf,ly,mid,musicxml,mp3}`
(Bach–Lehman; PDF engraved by LilyPond with a key signature for each key) and
`renders/prelude-equal.mp3` (equal temperament). Quarter = 80; a breath into bar 25; a
ritardando from bar 45 (80 → 66 at bar 47) and a broadening to 46 on the last chord. The
rendered audio lasts 2:30. Heads checked by `verify_prelude_heads.py` (below). I have not heard
the renders; everything here comes from the score and the tools.

## Concept

The cycle's farewell walks once more through all 24 keys, in the order of the Well-Tempered
Clavier, two bars per key (48 bars, a nod to "the 48"), and stops on the dominant of B minor.
The prelude ends on F♯–A♯–C♯ with A♯4 in Upper voice II; Fugue XXIV begins with B4 alone in
Alto III, so the fugue's first note resolves the prelude's last. (The fugue subject itself ends
on A♯ and leaves its B to what follows.)

The WTC order gives the walk two moves, used twelve times each:

- **major → parallel minor.** The tonic stays. The major key cadences (V–I) and the last beat
  brings the minor sixth in a predominant, a vii°7 or a V(♭9) (bars 2, 6, 10, 14, 22, 26, 30,
  38, 42), or the major key's dominant simply resolves into the minor tonic (bars 18, 34, 46).
- **minor → its Neapolitan.** ♭II of each minor key is the next major key (c → D♭ = C♯,
  c♯ → D, d → E♭, e♭ → F♭ = E, e → F, f → G♭ = F♯, f♯ → G, g → A♭, g♯ → A, a → B♭,
  b♭ → C♭ = B). The second bar of each minor key cadences on beat 3 and puts the Neapolitan
  on beat 4, where it becomes the next tonic. In c, d, e and a the Neapolitan also opens that
  bar (N6 – V7 – i – N6), so it is heard first as a predominant, with the ♭2 falling to the
  leading tone by a diminished third (D♭–B in bar 4, F–D♯ in 20, B♭–G♯ in 40).

So the tonics climb the chromatic scale from C to B: the twelve pitch classes of the fugue's
twelve-tone subject, whose tail also climbs (G G♯ A A♯ → B). The tritone key F♯ is the walk's
midpoint (bar 25); BWV 869 is binary, and the breath in the tempo map marks the half. There
are no repeats (time).

**B-A-C-H.** In bar 44 (B♭ minor → B major) the bass walks in quarters under held upper
voices: B♭ (i), A (V6), C (V4/3), H = B♮, which is the Neapolitan of B♭ minor in root position
and, tied over, the tonic of H-dur. Upper voice II holds F4 for three beats and Upper voice I,
after the last notes of Bach's head, holds E♭5 from beat 3, so the bass is the moving line
(velocity +3 in the bar, the bass +6).

## The 24 quotations

In each key one upper voice quotes the head of Bach's Book I fugue subject in that key at
Bach's own pitch classes; the other voice answers in BWV 869's manner (held notes and
suspensions, a few passing eighths), and when the head is slow (C♯ minor) the roles reverse and
the answer moves in eighths. "UI"/"UII" = Upper voice I/II; "8va" = an octave above Bach's
pitch; "×½" = note values halved (for the alla breve and 6/4 subjects, so that Bach's half-note
pulse becomes our quarter). Every quoted note has Bach's pitch and duration (only the last
note may be held longer).

| bars | key | BWV | voice, entry | notes quoted | form |
|---|---|---|---|---|---|
| 1–2 | C | 846 | UII, 1.1½ | 13 | exact |
| 3–4 | c | 847 | UI, 3.1½ | 9 | exact |
| 5–6 | C♯ | 848 | UI, 5.2½ | 12 | exact |
| 7–8 | c♯ | 849 | UI, 7.1 | 4 (the "cross") | two 8vas up, ×½ |
| 9–10 | D | 850 | UII, 9.2 | 14 | 8va |
| 11–12 | d | 851 | UI, 11.1½ | 11 (its B♭ G A continue over N6 – V7 – i) | 8va |
| 13–14 | E♭ | 852 | UII, 13.1 | 10 | exact |
| 15–16 | e♭ | 853 (Bach: D♯ minor) | UI, 15.1 | 8 | 8va, spelled in E♭ minor |
| 17–18 | E | 854 | UI, 17.2½ | 13 (and its sixteenth rest) | 8va |
| 19–20 | e | 855 | UII, 19.1 | 12 | exact |
| 21–22 | F | 856 | UI, 21.1 | 10 | 8va |
| 23–24 | f | 857 | UII, 23.2 | 6 (C D♭ C B E F = vii°7/V – V – i) | exact |
| 25–26 | F♯ | 858 | UI, 25.1½ | 10 | exact |
| 27–28 | f♯ | 859 | UII, 27.2 | 6 | 8va, ×½ |
| 29–30 | G | 860 | UI, 29.1 | 12 | 8va |
| 31–32 | g | 861 | UII, 31.1½ | 11 (both phrases, with the rest between) | exact |
| 33–34 | A♭ | 862 | UI, 33.2 | 10 | 8va |
| 35–36 | g♯ | 863 | UII, 35.2 | 9 | 8va |
| 37–38 | A | 864 | UI, 37.1 | 9 (the A, its rest, the rising fourths) | exact |
| 39–40 | a | 865 | UII, 39.1½ | 9 | 8va |
| 41–42 | B♭ | 866 | UII, 41.1½ | 10 | exact |
| 43–44 | b♭ | 867 | UI, 43.1 | 7 (the rest, then the minor-ninth leap) | exact, ×½ |
| 45–46 | B | 868 | UI, 45.1½ | 11 | 8va |
| 47–48 | b | 869 | UII, 47.1½ | 11 (Bach's C♮ over the N6) | exact |

13 heads are in Upper voice I (on top), 11 in Upper voice II; each head gets +6 velocity for
the bar of its entry. Each entry is declared in `prelude.json` (`subject_entries`, with labels
naming the BWV number), and `prelude.py` stops the build if a quotation in the bars differs
from its `HEADS` entry under the stated transform.

## Sources and verification of the heads

- **MuseData / Humdrum kern** encodings of all 24 fugues of WTC I (David Huron, 1994), files
  `kern/wtc1f01.krn` … `wtc1f24.krn` of https://github.com/humdrum-tools/bach-wtc, downloaded
  into an empty scratch directory and read only as data.
- **Mutopia Project MIDI** (public domain) for the 15 fugues Mutopia has: BWV 846–851, 853,
  855–857, 860–862, 865, 869 (the files already in the scratchpad's `wtc_ref/`). Mutopia has
  no fugue file for BWV 852, 854, 858, 859, 863, 864, 866, 867, 868.
- BWV 867 also against the LilyPond example in the English Wikipedia article "Prelude and Fugue
  in B-flat minor, BWV 867" (B♭ F, rest, G♭ F E♭ D♭ C ...).

`python3 -I cycle/24-b-minor/verify_prelude_heads.py --kern <kern dir> --midi <midi dir>`
reports, for all 24: the score quotation equals the head (pitch and duration of every note and
rest); the head equals the opening solo statement in the kern file (pitches and durations,
ties merged); and, for the 15 with Mutopia files, the MIDI agrees (pitches; durations within a
sixteenth, since MIDI note-offs are performance lengths). Result: 0 mismatches. So 9 heads
(BWV 852, 854, 858, 859, 863, 864, 866, 868, and 867 apart from the Wikipedia example) rest on
one machine-readable source; none was guessed. The 18 heads not yet in
`cycle/reference/bach-subjects.md` were appended there as rows, each with its source.

## Harmony and cadences, key by key

Every key is established within its two bars by its head over its tonic and at least one
dominant–tonic progression: in the major keys a cadence on beat 3 of the second bar (C, C♯, D,
F♯, G, A♭, B♭) or a V–I on the second downbeat (E♭, as V4/2–I6; E, F, B); in the minor keys
the cadence on beat 3 of the second bar (all but b♭, which cadences V7–i on the downbeat of
bar 44 before B-A-C-H, and b, which ends on its dominant), often with a V–i inside the head
itself (f: C D♭ C B E F; g: its F♯–G). A major is the weakest: its rising
fourths outline I – iii – IV – V – vi and its dominant (38.3) resolves into A minor, so the
key is stated by the tonic, the subdominant and the dominant, not by a closing V–I.

The bass walks in eighths throughout, except quarters at a few cadences, in bar 44 (B-A-C-H)
and in the last bar (iv6 – N6 – V). Its line favours scales and turns over leaps: the C-major
bass rises in tenths with BWV 846; the C-minor bass descends C B♭ A♭ G into the dominant; the
E-major and F♯-major basses are scales (E F♯ G♯ A B, F♯ E♯ F♯ G♯ A♯ B C♯); the A-minor bass
falls C B A G♯; the A♭-major cadence walks E♭ D♭ C B♭ A♭.

## Critic numbers (`tools/critic.py cycle/24-b-minor/prelude.json`)

| measure | value | target |
|---|---|---|
| parallels_error / weak | 0 / 0 | 0 |
| beat_parallels | 0 | ≤ 2 |
| dissonance_unresolved | 0 | ≤ 3 |
| stepwise_pct | 66.0 (Upper I 74, Upper II 70, bass 57) | ≥ 65 |
| leap ≥ 4th | 14.1 % | — |
| bad_doublings / tripled pc on beats | 0 / 1.2 % | — |
| low_register_seconds | 0 | — |
| keyboard_unplayable | 0 % (max 3 notes) | 0 |
| mean moving voices | 3.0 (all three voices move in all 48 bars) | — |

The critic adds 14 notes of the kind "chord seventh not resolved down" (warnings, not errors),
at 3.3, 6.1, 22.4, 23.4 (2), 24.1, 29.2, 34.2, 34.4, 38.4, 44.3 (2), 45.2 and 46.4. Most are
a dissonant note that leaves by step upward or by leap to another chord tone, several of them
inside Bach's heads (the C♯ head's appoggiatura at 6.1, the F-minor head's B–E at 24.1); the
V4/2 chords at 23.4 and 46.4 move their bass seventh on through passing notes; 44.3 is the
deliberate pivot, where the E♭ of V4/3 in B♭ minor is held as the third of C♭ = B major. Melodic flags (a leap over an octave at 43.3½, tritone leaps
at 36.1½ and 48.1) are all inside Bach's heads (BWV 867's minor ninth, BWV 863's C𝄪, BWV 869).

## Method

The harmonic template (the two moves) was planned first, then each key was written by hand
around its head: bass and harmony to the head, then the answering voice. `critic.py`, a grid
view of the three voices per eighth and a per-bar count of stepwise intervals (scratch scripts)
were used to find parallels, clashes and leapy bars; each fix was rewritten by hand. A first
complete draft measured stepwise 58 % (bass 46 %), with 9 consecutive and 7 beat-to-beat
parallel octaves or fifths; the bass was then rewritten towards scales and the answering voices given passing
eighths where the harmony allowed. Software placed no note. `wtclib` transposition and rhythm
scaling are used only to *check* the quotations against `HEADS`.

## Credits

Texture and character after J. S. Bach, Prelude in B minor, BWV 869 (WTC I). Quoted: the heads
of the 24 fugue subjects of J. S. Bach, *Das wohltemperirte Clavier* I, BWV 846–869 (sources
above). The key order is Bach's. The B-A-C-H motif is Bach's name. Bass, answering voices,
harmonisation and joins: Claude, for Sam.

## Weak spots

- **The bass is the least stepwise line** (57 %): two-bar keys need a cadence every eight
  beats and a pivot on the eighth, and several bars still arpeggiate (27, 29, 31–33).
- **The template is regular.** Every key cadences near beat 3 of its second bar and pivots on
  beat 4; the heads vary the surface, but over 48 bars the harmonic rhythm may sound
  predictable. That regularity is the "ground" of the walk, but I cannot judge it by ear.
- **Heads in the middle.** Eleven heads are in Upper voice II under the other voice; the
  answering voice is mostly held there, and the head has +6 velocity, but audibility is untested.
- **Tempo versus the originals.** At quarter = 80 the quick subjects (BWV 850's run, 855, 856,
  860, 864) are slower than Bach's tempi and lose some of their dance; the three subjects at
  half values (849, 859, 867) are faster than his.
- **Enharmonic seams.** The pivot notes are re-struck at the barline in the new spelling
  (D♭5 → C♯5 at bar 5, C♭6 → B5 at bar 17, G♭ → F♯ at bar 25); at bars 34–35 the leading tone
  of A♭ is written G3 and resolves to G♯3 under the new G♯-minor signature, which reads as a
  chromatic step.
- **Length.** 2:30 rendered, at the 2.5-minute limit; there is no room for Bach's repeats.
