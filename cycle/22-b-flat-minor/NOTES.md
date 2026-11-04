# Pair XXII in B-flat minor — Tombeau: "Ma fin est mon commencement"

Prelude XXII: *Tombeau* (one keyboard player, 20 bars, free tempo map, about 2 min 4 s).
Fugue XXII: six voices (Bach's BWV 867 has five), 68 bars alla breve, about 3 min 15 s
(bach-lehman render: 195 s). A crab fugue: the second half is the first half played backwards, in
every voice.

I have not heard any render. Everything below about the fugue comes from the score and the tools;
nothing here describes how it sounds.

## Fugue XXII — the concept at six voices

Machaut's rondeau *Ma fin est mon commencement* is a palindrome; Bach's *Musical Offering* has a
crab canon. Fugue XXII is a tombeau for Bach on that motto. It begins with one note, B-flat4 in the
alto, alone. Voices enter one at a time — alto b1, tenor b5, bass b9, soprano b15, mezzo-soprano
b21, the cantus firmus b27 — until all six sound together in b33–36. The axis is the barline 34|35.
After it, everything comes back backwards: the voices leave in the reverse order of their entries
(cantus b42, mezzo b48, soprano b54, bass b60, tenor b64), each one saying goodbye with its own first
entry read backwards, until the alto is alone and ends on the B-flat4 it began with.

At twenty-three voices (the earlier version) the palindrome existed on paper. At six it is meant to
be followed:

* **The subject is built so that its retrograde is a subject of its own.** Forwards it begins with
  the head of BWV 867 and ends with B-A-C-H. Backwards it begins H-C-A-B, climbs the scale B-flat –
  G-flat, rests, falls a minor ninth to F and ends F → B-flat: a cadence. The tonal answer read
  backwards ends B-flat → F, a half cadence. So in the last minute every voice leaves on a cadence,
  alternately full and half, and the texture thins 4 → 3 → 2 → 1.
* **The exposition is the clearest thing in the piece**, one voice at a time, each entry after a rest
  and in its own register, so that its mirror (b45–68, about the last 70 seconds, from 2:05) can be
  recognised: the countersubject comes back reversed above the reversed answer (b61–64), and the
  last four bars are the opening four bars backwards, alone.
* **The axis is a single held sound**: the diminished seventh B D F A-flat (the chord the prelude
  breaks upwards in its bars 13–15). The five upper voices hold their notes of it across the axis
  (each note tied into its own mirror image); only the cantus strikes its H again, on the axis.
* **The tempo map is a palindrome too** (below).

How it is made: bars 1–34 are written note by note in `fugue.py`. Bars 35–68 are produced by one
explicit transform, `crab()`: each voice's first half (tied notes merged) is reversed note by note
(`wtclib.retrograde`) and re-barred, so a note that starts at *t* and lasts *d* sounds again at
*T − t − d* (T = 68 bars). `build()` then checks the built score: all six voices are exact
palindromes. `XXII_HALVES=dir python3 fugue.py` also writes each half as its own score, so that the
critic can judge each half alone.

## Material

| | notes | use |
|---|---|---|
| S (subject, 4 bars) | B-flat4 (whole) F4 (half), rest, G-flat5 F5 E-flat5 D-flat5 C5 B-flat4 A4 C5 B-natural4 | BWV 867's head (its first note lengthened to a whole note, so that the final tonic, read backwards, is a whole note on a downbeat) + B-A-C-H; alto b1 and b27 (with its augmentation), bass b9 two octaves down |
| ANS (tonal answer, F minor) | F4 B-flat3, rest, D-flat5 C5 B-flat4 A-flat4 G4 F4 E4 G4 F-sharp4 | BWV 867's answer (the leap of a tenth); its tail is B-A-C-H a fifth up; tenor b5, soprano b15 an octave up |
| after the subject | H → C, a quarter rest, then onwards | in the exposition (alto, tenor, bass) each entry ends H → C (or F# → G) and breathes; backwards this gives each reversed entry a breath and an upbeat before its H-C-A-B |
| CS (countersubject, alto b5–8) | C5, rest, D-flat5 C5 · D-flat5 E-flat5 F5 · G5 F5 · D-flat5 E-flat5 | resolves the H, sighs (D-flat C, the subject's G-flat F a fifth up), climbs while the answer holds, moves in half notes while the answer runs down; only consonances on its half-note beats |
| SMAJ (subject in D-flat major) | D-flat5 A-flat4, rest, B-flat5 A-flat5 G-flat5 F5 E-flat5 D-flat5 C5 E-flat5 D5 | middle entry (mezzo, b21); its tail D-flat C E-flat D is B-A-C-H a minor third up and leads to E-flat minor |
| S×2 (augmentation) | B-flat2 (two bars) F2 (bar), rest, G-flat3 … C3 B-natural2 in half notes | the cantus firmus, b27–34, its H on the axis; backwards b35–42 it climbs H C A B-flat C D-flat E-flat F G-flat and cadences F2 → B-flat2 |
| B-A-C-H tails by minor thirds | cantus B-flat A C B; alto D-flat C E-flat D; mezzo (F) E-flat G-flat F; tenor (F) F-sharp A A-flat | b33–34, in half notes: the four transpositions of B-A-C-H a minor third apart end on the four notes of the axis chord B D F A-flat |
| B-A-C-H in quarters | soprano B-flat5 A5 C6 B-natural5 (b33) | over the cantus's B-A-C-H in half notes, from the same downbeat: the canon per augmentationem of b27 in the outer voices; backwards (b36) H-C-A-B on top, ending with the cantus's H-C-A-B |
| eighth-note wave | alto B C D B · C D E C (b19), soprano F G-flat A-flat F (b20) | the piece's first (and, backwards, last) eighth notes; every eighth that ends on a half-note beat is a chord tone, so its mirror (b49–50) lands on chord tones too |

## Section map (first half; the second half is the same backwards)

Times from the bach-lehman render (the tempo map included).

| bars | time | section | events |
|---|---|---|---|
| 1–4 | 0:00 | I. Exposition | alto: subject, alone |
| 5–8 | 0:12 | | tenor: answer (F minor); alto: countersubject |
| 9–12 | 0:23 | | bass: subject two octaves down; the tenor resolves F# → G and sighs G (rest) G-flat F; the alto rests two bars, then returns |
| 13–14 | 0:34 | codetta | three voices, V – i6 – iv – V of F minor; the bass breathes after its H → C |
| 15–18 | 0:39 | | soprano: answer, an octave up, above everything (the tenor rests two bars) |
| 19–20 | 0:50 | episode | G – C – D-flat (deceptive) – A-flat7; the first eighth notes (alto wave, answered by the soprano) |
| 21–24 | 0:56 | II. Middle entry | mezzo-soprano: subject in D-flat major (soprano and alto rest at first); the tenor falls chromatically D-flat C C-flat B-flat into E-flat minor |
| 25–26 | 1:07 | episode | three voices, iv – ii°6/5 – V, then a **half-bar general pause** (26.3–4); the alto rests almost two bars |
| 27–30 | 1:13 | III. Crux | the cantus firmus (sixth voice) enters with the augmentation; the alto sings the subject at its own speed from the same downbeat (canon per augmentationem); bar 30: an augmented sixth (G-flat C E) on the augmentation's G-flat under the alto's B-A-C-H |
| 31–32 | 1:24 | | V – V4/2 – i6 – V4/3 over the augmentation's descent; the soprano returns (b32) |
| 33–34 | 1:30 | | all six: i – vii°7 – vii°7 – B°7; the soprano sings B-A-C-H in quarters over the cantus's in half notes; the four B-A-C-H tails converge on the axis chord |
| 34│35 | 1:36 | axis | B D F A-flat, held; the cantus strikes its H again |

The second half: b35–36 the four H-C-A-B's leave the axis, the soprano's H-C-A-B in quarters on top
(b36, 1:39); b39–42 the canon per augmentationem backwards, ending with a cadence in B-flat minor
(cantus F2 → B-flat2, alto F4 → B-flat4) at 1:54–1:59, followed by the mirrored general pause
(43.1–2); b45–48 the mezzo's entry backwards, cadencing in D-flat; b49–50 the eighth-note waves
backwards (soprano, then alto); b51–54 the soprano's answer backwards; b57–60 the bass's subject backwards; b61–64 the tenor's answer and the alto's
countersubject backwards; b65–68 the alto alone.

## The devices, and where to hear them

1. **The crab** — the whole second half, most clearly the last 70 seconds (b45–68): the entries come
   back as cancrizans statements and the voices drop out one by one.
2. **Canon per augmentationem** — b27–30 (1:13): alto (subject) and cantus (subject in half and whole
   notes) start together on B-flat; backwards (b39–42, 1:48) they arrive together on B-flat. At b33
   (1:30) the soprano and the cantus repeat the idea with B-A-C-H alone (quarters against halves),
   and backwards at b35–36 they sing H-C-A-B together, ending on B-flat.
3. **Two mirrored landmarks in the middle**, so that the middle of the second half can be placed: the
   half-bar general pause before the crux (26.3–4, 1:11) returns as the silence after the cadence
   of b42 (43.1–2, 1:59); the first eighth notes of the piece (b19–20, 0:50) return as its last
   (b49–50, 2:16), the waves now falling.
4. **B-A-C-H in four transpositions** — b33–34 (1:30), half notes: the cantus (B-flat A C B), the
   alto (D-flat C E-flat D), the mezzo (E-flat G-flat F) and the tenor (F-sharp A A-flat) close on
   B, D, F, A-flat. The harmony underneath is i – vii°7 – vii°7 – B°7: from the second chord on,
   every voice slides by a semitone or moves within the diminished seventh. Backwards (b35–36) the
   four H-C-A-B's move away from the axis and resolve the diminished seventh to B-flat minor.

## Counterpoint that works in both directions: the rules I used

The critic was run on the whole piece and on each half alone (each half as its own score). These
are the rules that let one hand-written half work both ways.

1. **Metre and axis.** Alla breve (2/2) with the axis on a barline (T a whole number of bars).
   Then every note boundary on a half-bar maps to a half-bar, so half and whole notes keep their
   metric place, and a whole note on a downbeat stays one. Quarter notes swap places: the note on
   the first quarter of a bar comes back on the fourth, the second on the third. So what is heard
   *on* a beat in the second half is what sounded *just before* the matching beat in the first
   half. My grid tool shows, at every quarter of the first half, both verticals (just after and
   just before); I wrote so that both are chords at every half-note beat.
2. **Harmony moves in half notes; quarters are passing and neighbour notes.** A passing or
   neighbour note is its own mirror image. An unaccented passing quarter comes back as an accented
   passing quarter (still approached and left by step). I kept these mild: thirds, sixths, fourths
   and sevenths of the chord rather than seconds against a held note.
3. **Dissonance figures and their mirrors.** An appoggiatura (leap in, step out) comes back as an
   échappée (step in, leap out); a suspension (held, resolved down) comes back as a rising
   anticipation held into the next chord; a retardation comes back as a falling anticipation. I
   used few suspensions (the alto in b17; the soprano's 4–3 appoggiatura in b18) and checked each mirror.
4. **Progressions that work both ways.** Tonic and dominant oscillations, i6 – V4/3 – i
   (voice exchange), passing chords over a pedal (V – i6/4 – V), descending and ascending
   chromatic lines (the lament reads as a *passus duriusculus* backwards), and diminished sevenths,
   which are symmetric: V7 → B°7 forwards is B°7 → V7 backwards, a resolution. Falling-fifth
   chains, which reverse badly, are kept short (b18–19 D7 – G – C).
5. **Phrases framed I–V … V–I**: the subject itself does this (B-flat F … ; backwards … F B-flat).
   Half cadences forwards become openings backwards, so the cadences that matter backwards were
   written as openings forwards (the subject's head, the start of the canon at b27).
6. **Parallels are symmetric, rests are not.** Two voices that change a quarter apart around a rest
   in one half can change together in the other (in a draft, the bass and the soprano around the soprano's rest in b16; the bass was changed). I checked both halves.
7. **Sevenths.** A seventh resolving down by step forwards is approached by step from below
   backwards and leaves by whatever approached it forwards. So a seventh is idiomatic in both
   directions only if it is approached from the same note (re-struck) or from a step below, and
   left downwards by step: a neighbour seventh (F G-flat F, b20) or a prepared one re-struck (the
   alto's C5 in b18, the tenor's B-flat3 in b25). Passing sevenths in a falling line, and sevenths
   approached by leap, turn into sevenths that rise or leap away backwards. After the review I
   rewrote six of them; the critic's "7th not resolved down" notes in half 2 fell from 33 to 17
   (half 1: 6). The rest belong to the subject's own scale (G-flat, E-flat as passing sevenths), a
   lower neighbour (b24) and the diminished-seventh slides at the axis, whose mirror (A-flat rising to
   A, B°7 → V7) is the correct resolution.
8. **Eighth notes.** In this metre an eighth that ends on a half-note beat comes back on it. So in
   the two eighth-note figures (b19–20) the last eighth before each half-note beat is a chord tone;
   the passing eighths fall inside the beat in both directions.
9. **Keyboard.** The left hand takes the cantus and the two voices above it within a tenth, the right
   hand the upper three; this fixed the summit's voicing.

## Tempo map and dynamics: symmetric, deliberately

The tempo map is a palindrome around the axis (quarter-note time 136): a slow toll at both ends
(63 → 88 in bars 1–2, 88 → 63 in bars 67–68), a small breath at each mirrored pair of joins (14|15
and 54|55, 20|21 and 48|49, 26|27 and 42|43) and a broadening into the axis (88 → 72 over bars 31–34;
it was 66 before the review, which made the diminished-seventh plateau slowest where it is most
static) with its mirror image away from it. A dip that is symmetric around a barline works both ways: it
slows into the cadence forwards and slows out of the mirrored cadence backwards. So the performance,
like the score, reads the same backwards (apart from the piano's decay). The dynamic arch is
symmetric as well: quietest at both ends, loudest at the axis. Basic tempo quarter = 88 (half = 44).

## Critic numbers (critic, 4 Nov 2026: `tools/critic.py`)

| | whole | half 1 | half 2 | target |
|---|---|---|---|---|
| parallels_error | 0 | 0 | 0 | 0 |
| parallels_weak | 0 | 0 | 0 | |
| beat_parallels | 0 | 0 | 0 | ≤ 2 |
| dissonance_unresolved | 1 (b39.1, kept; see the review response) | 0 | 1 (b39.1) | ≤ 3 |
| dissonance_unverified (check by ear) | 2 (b17.3, b52.1) | 1 | 1 | |
| bad_doublings | 0 | 0 | 0 | ≤ 2 |
| low_register_seconds | 0 | 0 | 0 | ≤ 9 |
| stepwise_pct | 69.3 | 69.4 | 69.4 | ≥ 65 |
| leap_4th_plus_pct | 12.6 | 12.7 | 12.7 | |
| crossings | 1 | 1 | 1 | few |
| keyboard_unplayable_pct | 0.0 | 0.0 | 0.0 | ≤ 15 |
| mean moving voices | 3.12 | 3.12 | 3.12 | |
| pc tripled on beats | 7.6 % | 10.9 % | 4.3 % | |
| "7th not resolved down" (notes) | 22 | 6 | 18 | |
| reach_errors | 0 | 0 | 0 | 0 |

* All columns were recomputed with the critic of 4 November 2026 (the score has not changed since
  the review). The two unverified stepwise continuations are b17.3 and its mirror image b52.1 (alto
  under soprano, both moving by step), to be checked by ear.
* Because the critic checks dissonance only on half-note beats in 2/2, I also ran it on both halves
  with the metre read as 4/4 (every quarter a beat): 0 parallels, 0 beat parallels and 0 bad
  doublings in either half; the one unresolved note is again b39.1 (half 2), and the critic lists
  5 and 4 unverified stepwise continuations (passing quarters it cannot confirm against a moving
  partner).
* Mean moving voices by section: b1–14 2.1, b15–20 3.7, b21–26 3.5, b27–32 3.7, **b33–36 6.0**,
  b37–42 3.8, b43–48 3.3, b49–54 3.7, b55–68 2.1. Six voices move in four bars (b33–36).
* The one crossing: the bass sings above the cantus in b33–36, by design (the cantus is the lowest
  voice at the summit and the bass's own range lies below it elsewhere).
* Melody: 14 leaps larger than an octave, all of them BWV 867's minor ninth (subject) or tenth
  (answer), seven entries forwards and seven backwards.
* All 14 declared entries verify: subjects 10/10 intervals and rhythm, answers 8/10 (the tonal
  mutation), the D-flat-major entry 6/10 (the major mode), the augmentation 10/10 at time scale 2;
  the cancrizans entries are checked against the subject read backwards.

## Method and disclosure

Every note of bars 1–34 is written by hand in `fugue.py`; the second half is the explicit transform
above. Scratch tools (not in the repository): `check.py` (builds the piece and both halves, runs the
critic on all three), `grid.py` (both verticals at every quarter), `q44.py` (the 4/4 diagnostic),
`fit.py` (ranks two-voice placements of thematic forms against the cantus, scored in both
directions; it showed that no complete subject or answer fits over the cantus in b31–34, which is
why the summit uses the B-A-C-H tails instead), and `rhprop.py`, which listed right-hand voicings
for b31–34 that satisfy the doubling, parallel and hand-span rules. Its proposals were mostly held
F's; I rejected them and wrote the four-transposition idea by hand. No note was placed by script.

## Weak spots (honest)

* **The summit is still mostly half notes.** b31–36 is a six-voice stile-antico texture; since the
  review the soprano moves in quarters at b33 and b36 (B-A-C-H / H-C-A-B) and the broadening is
  gentler (72), but the inner B-A-C-H tails may still fuse into one chromatic chord stream.
* **The second half's harmony runs backwards.** Every passing quarter of the first half comes back
  accented (strong-beat ones at b38.1, b39.1, b46.1, b52.1, b62.1, b63.3; all stepwise), dominants
  move to pre-dominants at the reversed joins (e.g. b43–44, V → ii°6/5 → iv6), and 18 sevenths in half
  2 do not fall. The most exposed note is the alto's B-natural on the downbeat of b39 over the
  cantus's G-flat (the mirror of the subject's H in b30).
* **The alto's return at b27 is half masked**: it starts on B-flat4 under the mezzo's D-flat5 and
  only becomes recognisable at b28 (the rest and the leap of a ninth).
* **The soprano sings little**: an answer (b15–20), the summit (b32–37) and the answer backwards
  (b49–54); it rests eleven bars on each side of the axis. This is kept on purpose (see
  **Self-critique pass**): the silence leaves the mezzo's middle entry and the canon per
  augmentationem uncovered, and makes the soprano's return at b32–33 the start of the summit.
* **One middle entry only** (D-flat major). There is no stretto of the subject at normal speed; the
  piece's devices are the crab, the canon per augmentationem and the B-A-C-H convergence. Kept on
  purpose too (see **Self-critique pass**).
* **One surface speed.** Apart from the eighth-note waves of b19–20 (and b49–50) nothing is shorter
  than a quarter; b25–26 is still chordal.
* **The cadence in B-flat minor at b41–42** (the canon backwards) is a strong close in the middle of
  the second half; it may make the reversed exposition that follows sound like an epilogue.
* Whether the retrograde is *heard* as a retrograde is untested (I cannot listen); the symmetric
  tempo map, the general pause and the held axis chord are guesses for the owner to judge.

## Review (REVIEW-3.md) — what I changed and why

* **1. The summit plateau — applied (tested fix).** The soprano sings B-A-C-H in quarters at b33
  (`Bb5 A5 C6 B5`) over the cantus's B-A-C-H in half notes; the crab makes it H-C-A-B at b36. I also
  softened the axis broadening from 66 to 72 (still symmetric), since the plateau was slowest where
  it was most static.
* **2. The middle is not heard as backwards — partly addressed.** Two landmarks now return at
  mirrored places: a half-bar general pause before the crux (26.3–4), which comes back as the silence
  right after the cadence of b42 (43.1–2), and the first eighth notes of the piece (alto wave b19,
  soprano answer b20), which come back falling at b49–50 as the last ones. A listener will still not
  follow b37–64 as "backwards"; these give them two points to recognise.
* **3. Sevenths that become unidiomatic when reversed — reduced.** Rule 7 above. Rewritten in the
  first half without changing its harmony: alto b18 (C5 re-struck as the seventh of D7), tenor b22
  (D-flat instead of a passing E-flat), tenor b25 (B-flat3 re-struck as the seventh of C-half-dim),
  b26 (V without seventh before the pause), mezzo b30 (F5 E5 instead of F5 E-flat5 E5), alto b32
  (D-flat5 E-flat5 D-flat5, the seventh as an upper neighbour). Critic notes in half 2: 33 → 17.
* **4. Design risks — noted.** The early cadence at b41–42 stays: it is the mirror of the canon's
  start and cannot move without breaking the palindrome; the mirrored general pause after it now
  marks it as the end of a section rather than of the piece. Eighth notes: added at b19–20 only;
  more would change the stile-antico surface the subject's halves and quarters set up, and every
  eighth figure has to be written so that its chord tones fall on the half-note beats both ways.
* **Not done:** a mezzo rest at 27.2 to expose the alto (the reviewer also advised against it).
  Untouched, as asked: the alto alone at both ends with the slow toll of the tempo map, the axis (five
  voices tied, the cantus re-striking B2), the subject's design.
* After the changes: whole piece and both halves 0 parallels, 0 beat parallels, 0 unresolved, 0 bad
  doublings, 0 low-register seconds, 0 % unplayable (also clean in the 4/4 reading); all six voices
  are exact palindromes; all 14 entries verify. Renders redone (195 s).

## Self-critique pass (Nov 2026)

4 November 2026. No notes changed; `build()`'s palindrome check passes and the rebuilt score is
identical. An audit listed three open points.

- **Fixed: the counterpoint rules were numbered 7, 9, 8.** They are now 7 (sevenths), 8 (eighth
  notes), 9 (keyboard).
- **The listening guide's word for the second half.** Its row calls the second half's harmony "a
  little harsher". The score and the critic say otherwise: what the crab does is put the first
  half's passing quarters on the beats (all stepwise), make sevenths rise or leave by leap, and send
  dominants to pre-dominants at the reversed joins. None of that is an error in the 4/4 reading, and
  the one flag (b39.1) is a chromatic neighbour inside an augmented sixth. REVIEW-3 §4 hears it as
  "softer-edged and wandering", and I agree; I proposed that wording for the guide, which I do not
  edit myself.
- **Declined: a longer soprano part and a second middle entry.** The soprano rests b21–31 and,
  mirrored, b38–48. I kept both silences, for three reasons.
  1. Those eleven bars hold the two devices a listener can follow: the mezzo's D♭-major entry
     (b21–24), which is the top voice only because the soprano is silent, and the canon per
     augmentationem (b27–30), where the alto has only the mezzo above it and is already half
     masked. A soprano above either would cover it, and its mirror image would cover the reversed
     canon and its cadence (b39–42) and the reversed middle entry (b45–48).
  2. The only free span is the episode before the general pause (b25–26), and on one keyboard it
     has no room for a soprano. I tried one there (B♭5 – G♭5 – F5, the subject's own sigh, half
     notes, mirrored at b43–44). The counterpoint stayed clean in the whole piece, in both halves
     and in the 4/4 reading. But the episode's bass (E♭2) and tenor (B♭3) are a twelfth apart, so
     the right hand already holds the tenor with the mezzo's C5, and a soprano over them is out of
     reach (reach errors at b25.3 and its mirror b44.1; with a quarter-note G♭, still at b44.1).
     Making room would mean re-voicing the episode's lower voices and so the chord that the
     half-bar pause follows.
  3. A second middle entry needs four bars. Between the end of the mezzo's entry (b24) and the
     crux (b27) there are two and a half, so a second entry would have to overlap one of them as a
     stretto and take its exposure. And `fit.py` showed earlier that no complete subject or answer
     fits over the cantus in b31–34.

  The soprano's long silence also gives its return at b32–33 (B-A-C-H in quarters, on top) the
  weight of an entry: it opens the summit.

Critic (whole piece) before → after: unchanged (parallels 0, unresolved 1 at b39.1, unverified 2,
bad doublings 0, stepwise 69.3 %, reach errors 0, keyboard_unplayable 0.0 %).

## From the N+1 version

* **Kept:** the concept (a crab fugue on Machaut's motto, a tombeau for Bach), the subject (BWV 867's
  head + B-A-C-H, built so that its retrograde ends with a cadence) and the tonal answer, the
  diminished seventh B D F A-flat as the axis chord, the augmentation of the subject ending on the
  axis, a gathering one voice at a time and the dispersal in reverse order, the symmetric tempo map
  and dynamics, the explicit `crab()` transform and the check that every voice is a palindrome.
* **Changed:** 23 voices in four choirs → 6 voices; 96 bars → 68 (4:32 → 3:15). The exposition now
  has one entry at a time with a countersubject, instead of five "answer + subject half a bar later"
  pairs; one middle entry (D-flat major) instead of three choir sections; the augmentation moved from
  the top voice to a new lowest voice (the cantus firmus), so that its B-A-C-H becomes the bass
  progression V6/5 – V4/3 – B°7 and, backwards, a cadence; the alto sings the subject in canon with
  it; the summit is four B-A-C-H's a minor third apart instead of a knell and fifteen inner strands;
  the axis chord is held, with only the cantus restriking it. Critic: half 2 had 3 unresolved and 2
  doubled sevenths, now 0 and 0; stepwise 62.5 % → 69.3 %; keyboard from meaningless to 0 %
  unplayable. No placement was proposed by a timing search this time.
* **Why:** at 23 voices the gathering was uneven (the summit jumped from 7 to 20 moving voices) and
  the answer-pair template repeated; nothing in the reversed second half could be followed. At six,
  each entry has room, the texture can grow 1 → 2 → 3 → 4 → 6 and shrink again, and the reversed
  exposition at the end has a chance to be recognised.

## Credits and sources (verified)

* **J. S. Bach, WTC I, Fugue 22 in B-flat minor, BWV 867** (five voices, alla breve). Verified for the
  earlier version from the Humdrum `**kern` encoding of WTC I (`wtc1f22.krn`, Bach-Gesellschaft
  edition) and listed in `cycle/reference/bach-subjects.md` (kern + Wikipedia score example): top voice
  B-flat4 F4 (halves) | rest, G-flat5 F5 E-flat5 | D-flat5 C5 …; the answer F4 B-flat3 | rest, D-flat5
  C5 B-flat4 — a tonal answer with the leap of a tenth. Borrowed: the head (first note lengthened) →
  the first seven notes of S; the tonal answer's head → ANS; the alla-breve metre.
* **B-A-C-H** (B-flat A C B-natural), the traditional signature: the last four notes of S; its
  minor-third transpositions at the summit.
* **Machaut**, *Ma fin est mon commencement* (rondeau, a palindrome): the title and the idea only; no
  notes taken. **Bach**, *Musical Offering*, canon a 2 cancrizans: the idea of a crab only.
* **Froberger**, *Tombeau fait à Paris sur la mort de Monsieur Blancheroche* ("se joue fort
  lentement à la discrétion sans observer aucune mesure") and its falling scale; **Louis
  Couperin**, the unmeasured preludes (style brisé). Prelude: performance idea, texture and the
  falling scale as a gesture only, from general knowledge; no notes taken, no scores consulted.

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

`renders/fugue.pdf|.mp3|.mid|.musicxml` (bach-lehman, piano), `renders/fugue-equal.mp3`,
`renders/fugue-spatial.mp3` (binaural, arc layout, General MIDI 19 church organ: the cantus firmus's
long notes sustain), `renders/fugue-spatial-choir.mp3` (the same with 52 choir aahs, replacing the
earlier choir render), `renders/prelude.pdf|.mp3|…` (bach-lehman), `renders/prelude-equal.mp3`.
LilyPond engraved the fugue without errors (3 pages).

## Prelude: weak spot

* Prelude: stepwise motion is low (56 %); the brisé is written out in fixed values, so the
  freedom of an unmeasured prelude depends entirely on the tempo map; the falling scale passes in
  one bar and might want more room.

## Review response (Nov 2026)

1 November 2026. No notes changed in this pair; the crab check in `build()` still passes and the rebuilt
score is identical.

- **The corrected critic's new flag, b39.1 (alto B♮4 over the cantus's G♭3), is kept.** It is the first note
  of the alto's cancrizans subject, H, struck over the cantus's cancrizans augmentation at its G♭ (BWV 867's
  minor ninth). Its image in the first half is the subject's last note, H, on the weak fourth quarter of b30
  over the same G♭, an unaccented chromatic neighbour (C B C) inside the French sixth G♭ B♭ C E that resolves
  to V. The crab turns it into an accented neighbour on the downbeat, rising to C on the next quarter. The
  critic counts C against G♭ (a tritone, but a member of the augmented-sixth chord) as another dissonance and
  so calls the H unresolved. Both notes belong to subject statements in both halves, and the second half must
  be the exact retrograde of the first, so the only ways to remove the flag would be to alter the subject's
  B-A-C-H or the augmentation's G♭. I would rather keep the crab's one sharp downbeat: it is the moment the
  name begins to be read backwards.
- **Unverified (b17.3 and its mirror b52.1):** alto and soprano moving by step together; to check by ear.
- **"Phrase the reverse half as return and release"** (the owner's review). The performance data already
  do this within the palindrome: the dynamic arch falls from the axis to the end and the tempo map slows into
  the last lone B♭, mirroring the opening's rise. I did not make the dynamics or tempo asymmetric, because
  "the performance reads the same backwards" is part of the concept, but the crab check covers pitch, onset
  and duration only, so an asymmetric arch can be tried later by ear without touching a note.
- **The leaps separated by rests** (the 14 ninths and tenths of BWV 867's head, seven each way): agreed that
  they are the subject's, not defects; they are documented as such above.

Critic (whole piece) before → after: unchanged, reach_errors 0, keyboard_unplayable_pct 0.0, unresolved 1
(b39.1, kept), unverified 2.
