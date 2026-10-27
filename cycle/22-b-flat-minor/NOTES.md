# Pair XXII in B-flat minor — Tombeau: "Ma fin est mon commencement"

Prelude XXII: *Tombeau* (one keyboard player, 20 bars, free tempo map, about 2 min 4 s).
Fugue XXII: twenty-three real voices in four choirs (5 + 6 + 6 + 6), 96 bars alla breve, about
4 min 32 s (bach-lehman render: 272 s). A crab fugue: the second half is the first half played
backwards, in every voice.

## Concept

Machaut's rondeau *Ma fin est mon commencement* is a crab: its last half is its first half
backwards. Fugue XXII is a tombeau on that motto. It begins with one note, B-flat4 in the alto of
Coro I, alone; voices gather one by one (23 first entrances, from b1 to b45.3); all 23 sound on the
axis (barline 48|49); and the retrograde takes them away again in exactly the reverse order, until
the same alto is alone and the piece ends on the B-flat4 it began with.

How it is made: bars 1–48 are written note by note in `fugue.py`. Bars 49–96 are produced by one
explicit transform, `crab()`: each voice's first half (tied notes merged into one note) is reversed
note by note (`wtclib.retrograde`) and re-barred, so a note that starts at *t* and lasts *d* in the
first half sounds again at *T − t − d* (T = 96 bars). Checked after building: all 23 voices of
`fugue.json` are exact palindromes. Two voices hold one note across the axis (S4's B-natural5 and
the contrabass's F1 pedal); they are tied into their own mirror image.

Making the palindrome audible (I cannot hear the result; these are the design decisions):

* The subject is built so that its retrograde is a gesture of its own. Forwards it begins with the
  head of Bach's B-flat-minor fugue (BWV 867) and ends with B-A-C-H; backwards it begins H-C-A-B
  and ends with BWV 867's opening read backwards, F → B-flat — a cadence. So the piece opens with a
  question and ends with an answer that is the same notes.
* Entrances and exits are the same events: the order of first entrances (table below) is the
  reverse order of last notes.
* The axis is a single symmetric sound: the common-tone diminished seventh of F (B-natural D F
  A-flat over the F1 pedal), a chord of equal intervals. It is struck on b48.4 by every voice and
  struck again, as its own mirror, on b49.1.
* Section labels in the score run I II III IV | IV III II I ("cancrizans").
* **The tempo map is symmetric** (a palindrome): a slow toll at both ends (60 → 88), q = 88
  throughout, a broadening into the axis (88 → 66) and its mirror image away from it. The dynamic
  arch is symmetric too (quiet at both ends, loudest at the axis).
* The spatial render uses the ring layout with the voices listed choir by choir, so the gathering
  and the dispersal also move round the ring.

## How the counterpoint works in both directions

The critic checks the first half, the second half and the whole separately; both halves must meet
the quality numbers. These are the rules I followed so that one hand-written half works both ways:

1. **Beats map to beats.** In 2/2 with an even number of bars, the reverse of a note boundary on a
   half-bar is a note boundary on a half-bar. But what is heard *on* a beat in the second half is
   what sounded *just before* the corresponding beat in the first half (the critic samples exactly
   these "pre-beat" verticals in half 2). So every vertical just before a beat had to be as good as
   the vertical on it. Passing and neighbour notes on weak quarters were placed so that both the
   vertical before and the vertical after are chords.
2. **Dissonances approached and left by step.** A passing or neighbour figure is its own mirror. A
   suspension (prepared, held, resolved down) becomes, backwards, a note approached by step from
   below and held into a consonance — a retardation. Where the critic in half 2 could not name the
   chord, I changed the preparation so that the note before the dissonance is a step away.
3. **Two-way suspensions**: one voice steps into the dissonance while the other steps out of it;
   reversed, the roles swap and both are still stepwise (used throughout the summit, where every
   inner strand enters its new note an eighth off the beat).
4. **Parallels are symmetric, rests are not.** Parallel fifths forwards are parallel fifths
   backwards, but a rest just before an attack becomes a rest just after a note: two voices that
   change a quarter apart in half 1 can change at the same moment in half 2 (e.g. S1/B3 at b35,
   B2/A2 at b29). These were found by checking half 2 and fixed by moving one voice's change.
5. **Cadences turn round.** V–i forwards is i–V backwards. The half cadences of half 1 (b5, b32,
   b37.3, b44) become authentic cadences in half 2; the final cadence of the piece (F → B-flat in
   the lone alto) is the subject's opening read backwards. The subject's B-natural resolves up to C
   forwards; backwards C falls to B-natural, which then *begins* the reversed subject (H-C-A-B).
6. **Leading tones and sevenths**: a seventh resolving down by step forwards is approached by step
   from below backwards (an appoggiatura from below). I kept chord sevenths stepwise on both sides.
7. **The axis**: each voice's last note before the axis is its first note after it. Voices that
   change at the axis strike the axis chord on b48.4 and again on b49.1 (a repeated chord); S4 and
   the contrabass hold through it.

## Credits and sources (verified)

* **J. S. Bach, WTC I, Fugue 22 in B-flat minor, BWV 867** (five voices, alla breve). Verified from
  the Humdrum `**kern` encoding of WTC I (GitHub `humdrum-tools/bach-wtc`, file `wtc1f22.krn`,
  encoded by David Huron from the Bach-Gesellschaft edition), downloaded into its own directory and
  read with my own parser under `python3 -I`. Bars 1–3, top voice: B-flat4 F4 (halves) | rest,
  G-flat5 F5 E-flat5 | D-flat5 C5 D-flat5 E-flat5 …; the answer (alto, b3): F4 B-flat3 | rest,
  D-flat5 C5 B-flat4 — a tonal answer with the leap of a tenth. (Mutopia has no BWV 867;
  kern.humdrum.org was down for maintenance.)
  Borrowed: the head (B-flat F, rest, the leap of a minor ninth to G-flat, the stepwise descent)
  → the first seven notes of my subject S; the tonal answer F B-flat, rest, D-flat C B-flat → the
  head of my answer ANS; the alla-breve metre and the five-voice first choir.
* **B-A-C-H** (B-flat A C B-natural), the traditional signature: the last four notes of S.
* **Machaut**, *Ma fin est mon commencement* (rondeau, a crab canon): the title and the idea only;
  no notes taken.
* **Froberger**, *Tombeau fait à Paris sur la mort de Monsieur Blancheroche* ("se joue fort
  lentement à la discrétion sans observer aucune mesure") and its falling scale; **Louis
  Couperin**, the unmeasured preludes (style brisé). Prelude: performance idea, texture and the
  falling scale as a gesture only, from general knowledge; no notes taken, no scores consulted.

## Material (fugue)

| | notes | use |
|---|---|---|
| S (subject, 4 bars) | B-flat4 (whole) F4 (half), rest, G-flat5 F5 E-flat5 D-flat5 C5 B-flat4 A4 C5 B-natural4 | BWV 867's head + B-A-C-H; long notes first, quarters after, so that backwards it slows into a cadence |
| ANS (tonal answer, F minor) | F4 B-flat3, rest, D-flat5 C5 B-flat4 A-flat4 G4 F4 E4 G4 F-sharp4 | BWV 867's answer; ends with B-A-C-H a fifth up |
| SMAJ / AMAJ | S in D-flat major (tail D-flat C E-flat D = B-A-C-H a third up) and its answer in A-flat | Section II |
| INV (inversion) | F5 B-flat5, rest, A4 B-flat4 C5 D-flat5 E-flat5 F5 G-flat5 E-flat5 E5 | diatonic mirror around D-flat; B-A-C-H mirrored chromatically (up a semitone, down a minor third, up a semitone); Section III |
| CS1 | countersubject against the answer (b5–8) | Section I |
| S×2 | S in augmentation, an octave up (S4, b41–48) | its B-natural lands on the axis |

## Section map (first half; the second half is the same in reverse)

| bars | section | events |
|---|---|---|
| 1–18 | I. Intonatio (Coro I) | A1 S (b1, alone); T1 ANS (b5) with CS1; B1 S (b9); S1 ANS (b13) and Bar1 S half a bar later (b13.3), in tenths; codetta down the circle of fifths to B-flat minor |
| 19–32 | II. Consolatio (Coro II, D-flat major → E-flat minor) | Ms2 AMAJ (b19) / T2 SMAJ (b19.3) in thirds; B2 AMAJ (b23.3) / S2 SMAJ (b24.1), the thirds inverted into sixths (a fauxbourdon down to B-flat minor); A2 answer in B-flat minor (b28) / Bar2 S in E-flat minor (b28.3); both B-A-C-H tails lead to C, the dominant of F |
| 33–40 | III. Speculum (Coro III) | Ms3 INV in E-flat minor (b33) / B3 S in E-flat minor a twelfth below (b33.3), over Coro I's half-bar chords; Bar3 S (b36.3) / S3 INV (b37), ending on the dominant and on the summit's downbeat; A3 enters (b40); Neapolitan sixth (C-flat over E-flat, the inversion's G-flat against the subject's B-natural) |
| 41–48 | IV. Crux | S4 S×2 (b41–48) with T3 S (b41, canon per augmentationem) and T4 S (b45, ending on the axis); Coro IV gathers (S4 and T3 b41, Bar4 b43, contrabass b44.3 on C2 → F1 pedal, A4 and T4 b45, Ms4 b45.3); the knell; the axis chord on b48.4 |
| 48│49 | axis | B-natural D F A-flat over F1, all 23 voices |

Order of first entrances (= reverse order of last notes): A1 b1, T1 b5, B1 b9, S1 b13, Bar1
b13.3, Ms2 b19, T2 b19.3, B2 b23.3, S2 b24.1, A2 b28, Bar2 b28.3, Ms3 b33, B3 b33.3, Bar3 b36.3,
S3 b37, A3 b40, T3 and S4 b41, Bar4 b43, B4 b44.3, A4 and T4 b45, Ms4 b45.3.

## The summit (b45–48, mirrored in b49–52)

* **S4**: the augmentation, F6 E-flat6 D-flat6 C6 B-flat5 A5 C6 B-natural5 in half notes; its H
  arrives on b48.3 and is held across the axis.
* **T4**: the subject at its own speed (B-flat3 …), ending on B-natural3 on b48.4 — the axis chord.
* **Contrabass (B4)**: C2 (ii-half-diminished, b44.3) into the dominant pedal F1, b45–52, tied
  across the axis.
* **The knell**: A4 (F5), Bar1 (F3) and B2 (F2) toll the dominant a staggered eighth apart; they
  never change pitch, so they colour the summit without doubling any moving line, and fall silent
  on the beat where the H arrives.
* **Counter-lines**: S1 and S3 (a slow counter-line and a stepwise descent under the augmentation),
  S2, Ms2, Ms3, Ms4, A1, A2, T1, T2, T3 (inner strands that enter their new notes an eighth off the
  beat, so that their held notes become suspensions on the beats), Bar4, B1, B3 (low strands that
  move a quarter before or after the themes).
* **The axis strike**: A3, Bar2 and Bar3 rest through the core and enter only on b48.4 with
  B-natural3, A-flat3, A-flat2 — the last three voices to enter and the first three to leave.
* Harmony, two chords a bar: b41 i VI | i6 iv | i6/4 i6 | V(4-3) ii-half-dim7 | i6/4 iv7/F | i6/4
  V(b9) | V(4-3) V+ | V7 → the axis chord.

Moving voices per bar at the summit: b45 20, b46 19, b47 19, b48 22 (23 sounding; the contrabass
holds) — mirrored b49 22 (19 + 3 repeated), b50 19, b51 19, b52 20.

## Critic numbers (`tools/critic.py`)

| | whole | half 1 | half 2 |
|---|---|---|---|
| parallels_error | 0 | 0 | 0 |
| parallels_weak | 4 | 2 | 2 |
| beat_parallels (≤ 8) | 4 | 1 | 3 |
| dissonance_unresolved (≤ 15) | 3 | 0 | 3 |
| bad_doublings (≤ 8) | 2 | 0 | 2 |
| low_register_seconds (≤ 16) | 0 | 0 | 0 |
| stepwise_pct (≥ 60) | 62.5 | 63.8 | 63.8 |

Mean moving voices: section I 2.8, II 4.5, III 4.8, IV 41–44 7.5, IV 45–48 20.0 per bar (the
second half mirrors these); whole piece 5.2.

The three unresolved items, all in the second half, justified:
* b53.1 (two items, the mirror of b44.4): the half-diminished seventh C E-flat G-flat B-flat on
  which the contrabass enters, with T3's B-natural (the subject's H) on the last quarter. Backwards,
  that H falls on the beat and resolves up to C a quarter later — an accented chromatic
  appoggiatura; with the H in it the critic cannot name the chord and flags the tritone C–G-flat
  between the contrabass/bass and S4.
* b54.3 (mirror of b43.2): the bass's F2 under Ms3's B-flat4 (a 6/4) while T3 passes E-flat4; the
  critic does not recognise the passing chord.

Bad doublings (half 2): doubled sevenths at b58.3 and b62.1 (mirrors of passing verticals at b39
and b35). Weak parallels: octaves between A1/T1 and T1/B1 in the summit, a sixteenth apart in
passing (b47 and its mirror b50).

## Tool changes (backward compatible)

* `tools/wtclib.py`: an entry may carry an optional sixth field, `form` (e.g. `'retrograde'`),
  written into `subject_entries`; entries without it produce exactly the same JSON as before.
* `tools/critic.py`, `check_themes`: an entry with `form` starting `retrograde` is checked against
  the subject read backwards and reported as `retrograde` / `retrograde inversus`; others as before.
* Tested on `cycle/02-c-minor/fugue.json`: rebuilt JSON and critic output identical.

Scripts in the scratchpad (not in the repository): `check.py` (builds the fugue, both halves, runs
the critic on each), `alts.py` and `probe.py` (rank or report on hand-written variants I typed;
they write nothing), `grid.py` and `motions.py` (displays), and `tsearch.py`, a timing search for
one hand-written line: given my notes, it tried shifting onsets by an eighth and scored each
placement with the critic, forwards and backwards. **Disclosure**: the eighth-note offsets of
several inner strands in b45–48 (S2, Ms2, Ms3, Ms4, A1, A2, T1, T2, T3) were chosen among
placements proposed by `tsearch.py`; the pitches are mine. No thematic material was placed by
script; the second half is the explicit retrograde transform described above.

## Prelude XXII: Tombeau

For one pianist (four voices, two staves' worth; the critic finds no onset beyond two hands). Measured
notation with a free tempo map (34–80 to the quarter; every cadence held back, the tomb chord very
broad, the falling scale fast); about 2 min 4 s.

| bars | |
|---|---|
| 1 | a low B-flat tolls; the tonic chord gathers from the bass up, note by note |
| 2–5 | BWV 867's head (B-flat, F, rest, the ninth to G-flat), the subject slowly, ending B-A-C-H; its B-natural sounds over F in the fugue's axis chord, which opens onto the dominant |
| 6–8 | the lament: the chromatic tetrachord B-flat A A-flat G G-flat F in the bass (i V6/5 v6 IV6 iv6 V7) under sighing appoggiaturas |
| 9–12 | consolation in D-flat (the key of the fugue's second section), back to B-flat minor |
| 13–15 | the climb (tonic arpeggio in both hands, VI, iv6, V) to the axis chord broken upwards, fortissimo |
| 16 | Froberger's fall: a scale tumbling two octaves down over the dominant |
| 17–20 | V7 – i; the tonic chord comes apart from the top down (bar 1 backwards), a last low B-flat, and a lone B-flat4 — the fugue's first (and last) note |

Critic: parallels 0, beat parallels 0, unresolved 0, bad doublings 0, low-register seconds 0,
stepwise 56 %.

## Renders

`renders/fugue.pdf|.mp3|.mid|.musicxml` (bach-lehman), `renders/fugue-equal.mp3`,
`renders/fugue-spatial.mp3` (ring), `renders/prelude.pdf|.mp3|…` (bach-lehman),
`renders/prelude-equal.mp3`. LilyPond engraved both scores without errors.

## Weak spots (what I would still improve)

* **The gathering is uneven.** Sections I–III stay thin (3–6 moving voices); b38–40 has only four
  moving voices, b41–44 seven to eleven, and then the summit jumps to twenty. I would write more
  inner voices in b37–44 so that the ascent to the axis is gradual and the "one by one" is heard
  as a steady accumulation rather than a last-minute crowd (four Coro IV voices first sound in
  b44–45).
* Coro III's alto sings only b40–42 and the axis strike; several Coro I/II voices rest through
  Section III. The texture in b33–40 is mostly a two-voice canon over half-bar chords.
* The pair template (answer, then subject half a bar later, in thirds or sixths) is used five
  times; an inversion stretto against the rectus, or a stretto at the quarter, would vary it.
* Extreme ranges for singers: the augmentation rises to G-flat6 and S1 to D-flat6 (the score is
  for keyboards, but the choir labels suggest voices).
* The three unresolved items and two doubled sevenths in half 2 (above), and the weak octaves in
  the summit, could be removed by re-voicing b43–44 and b35/b39.
* Whether the retrograde is *heard* as a retrograde is untested (I cannot listen); the symmetric
  tempo map and the axis broadening are guesses that the owner should judge.
* Prelude: stepwise motion is low (56 %); the brisé is written out in fixed values, so the
  freedom of an unmeasured prelude depends entirely on the tempo map; the falling scale passes in
  one bar and might want more room.
