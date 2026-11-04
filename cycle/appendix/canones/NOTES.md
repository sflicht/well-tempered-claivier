# Canones (appendix)

Bach closed collections with puzzle canons: the Musical Offering's crab canon
and its "Quaerendo invenietis" riddles, the Fourteen Canons BWV 1087 on the
Goldberg ground, the augmentation canons of the Art of Fugue. These are the
cycle's two: a canon that is its own image turned upside down, and a canon at
four speeds at once.

| | I. Canon cancrizans per motum contrarium | II. Canon per tempora |
|---|---|---|
| source | `table_canon.py` (dux literal) | `tempo_canon.py` (melody M literal) |
| score | `table-canon.json` | `tempo-canon.json` |
| renders | `renders/table-canon.{pdf,mp3,mid,musicxml}` (Bach-Lehman), `table-canon-equal.mp3` | `renders/tempo-canon.*` (Bach-Lehman), `tempo-canon-equal.mp3` |
| size | 32 bars 3/4, q = 60, ~96 s | 32 bars 6/4 + convergence bar, q = 96, ~124 s |
| proof | `python3 verify_canones.py` (reads only the JSON) | same script |

Rebuild: `python3 table_canon.py`, `python3 tempo_canon.py`. Check:
`python3 ../../../tools/critic.py table-canon.json` and so on. The workshops
(`table_workshop.py`, `tempo_workshop.py`) print the critic findings, a dyad
or chord grid, and, for I, the sixteenth-position rule described below.

I can't hear audio. Nothing below says how either piece sounds.

---

## I. Canon cancrizans per motum contrarium (a Tafelkanon)

### The trick

One line is printed. Player I (dux) reads it from the near side of a table.
Player II (comes) reads the same page from the far side. Turning a page
through 180° reverses time (cancrizans) and turns the staff upside down
(per motum contrarium). The canon is therefore its own retrograde inversion,
and the two-voice score equals itself rotated. Bach's Musical Offering crab
canon is retrograde only. The mirror duets attributed, doubtfully, to Mozart
are the familiar precedent for this table trick.

**Mathematics.** With T = 96 quarters and the axis D4 (MIDI 62):
comes(t) = 124 − dux(T − t). The vertical interval at time t is
dux(t) − comes(t) = dux(t) + dux(T − t) − 124, which is symmetric in t and
T − t. So the interval content of the harmony is a palindrome. Chord
*qualities* flip, because the mirror about D maps the C-major collection
onto itself (C↔E, F↔B, G↔A, D fixed):

| first half (sharps) | rotated half (flats) |
|---|---|
| A minor (A C E) | C major (G E C) |
| D minor | G major |
| E7 (dominant of A minor) | Dø7 = D F A♭ C (pre-dominant in C) |
| G♯ (leading tone) | A♭ (minor sixth) |
| C♯ (leading tone of D minor) | E♭ |

Consequences the piece uses:

- **The key plan is a descending circle of fifths, A → D ‖ G → C.** The first
  half is a minor-key journey (A minor, then D minor at the hinge). Its
  rotation is a major-key journey, G and then C. A minor i–iiø7–V7–i reads,
  from the other side, as a major I–iiø7–V7–I with the minor iv colour. The
  opening cadence of bars 1–4 in A minor (E | F–Dm | Bdim–E/G♯–E | Am) is the
  closing cadence of bars 29–32 in C (C | F**m**–Dø | G | C, the A♭ at bar 30
  being the rotated G♯ of bar 3).
- **Leading tones become sixths.** The first half is coloured with sharps and
  the second with flats (E♭, A♭): the same notes, seen from the other side of
  the table.

**Proof.** `verify_canones.py` reads `table-canon.json` and checks, note for
note, that rotating the dux gives the comes and rotating the comes gives the
dux. It also checks that the whole score (voices swapped, time reversed,
pitches mirrored) equals the score. Result: `rot(dux) == comes: True;
rot(comes) == dux: True; score == rotated score: True`. The build
(`table_canon.py`) also refuses to write the JSON unless the same check
passes. The only note that spans the centre is the axis itself: D4 in both
voices, beats 46–50.

### Rhythm: what survives being read backwards

Rotation maps a time *point* to T − t. Bar lines map to bar lines. In 3/4,
beat 2 maps to itself and beats 1 and 3 swap. A note's attack becomes its
release, so:

- A quarter on beat 2 stays on beat 2. The sarabande accent survives, and a
  passing quarter on beat 2 stays a passing quarter on beat 2 (bars 2 and 31
  are the same passing fourth, seen from both sides).
- "q h" becomes "h q". Both are native sarabande rhythms.
- **A suspension becomes an anticipation.** Preparation, dissonance and
  stepwise resolution read backwards as stepwise approach, dissonance, and a
  held note made consonant by the other voice moving. An échappée becomes an
  appoggiatura.
- **Eighths swap on-beat and off-beat**, so a weak passing eighth would
  become an accented one in the other half. A first draft with eighth-note
  figuration showed exactly that (15 on-beat dissonances in bars 18–24).
  **Sixteenths** behave better: positions within a beat map 0↔3 and 1↔2.
  The double therefore keeps positions 0 and 3 of every beat consonant and
  puts every passing or neighbour note on positions 1–2, which stay weak
  after rotation. `canon_tools.sixteenth_rule` enforces this; the only
  exceptions are the two beat-2 passing quarters above.

### Form (mirror pairs: bar k ↔ bar 33 − k)

- **1–8 Thema, A minor.** It opens on a bare E octave (the rotation of the
  final C octave). The tune is E5 | A4 | D5 B4 | C5 | B4 A4 | B4 G4 | A4 F4 |
  E4. Its beat-2 notes (E A B C A G F E) are the retrograde inversion of the
  **Goldberg ground in C**.
- **9–15 Double.** Sixteenths over the sarabande bass, rising to C6 at bar 12
  and falling, A minor → D minor (iiø7 / V7 / i / III / iv / A7).
- **16–17 Cardo (the hinge).** The dux falls E4 → D4 while the comes rises
  C♯4 → D4: a two-voice cadence onto a **unison on D4, the axis**, on beat 2
  (the sarabande's own cadence beat), tied across the centre line. It leaves
  by the mirror motion D → E♭ / D → C. The axis pitch is approached from its
  two mirror neighbours, C♯ (from below, as leading tone) and E♭ (from above).
  It is the only pitch that maps to itself. On one piano both parts strike
  the same key, and the MIDI doubles it.
- **18–24 Double rovescio.** The double rotated into a running bass under the
  sarabande tune, G → C.
- **25–32 Fundamentum.** The comes plays the first eight notes of the
  Goldberg ground (BWV 988), transposed to C, as half notes on the downbeats:
  C B A G E F G C. That is the ground on which Bach built the Fourteen Canons
  BWV 1087. The dux sings over it, peaks on C6 with the A♭ of the minor iv
  (bar 30), and closes D5 C5 B4 | C5 over G | C.

### Printing it as a one-line riddle

- One staff, no key signature. Treble clef and 3/4 at the left.
- At the right-hand end, printed upside down: an **F-clef on the third line
  (baritone clef)** and an inverted 3/4. Why that clef: the treble staff's
  middle line is B4. Under rotation a note s steps above the middle line
  reappears s steps below it, and the comes must read 2·D4 − (B4 + s) =
  F3 − s. So the far reader needs F3 on the middle line, which is the
  baritone F-clef.
- Inscription (my Latin): *Canon cancrizans per motum contrarium. Alter ex
  adverso mensae legat; ♯ et ♭ inter se commutentur.* ("Let the other read
  from the opposite side of the table; let ♯ and ♭ exchange.") A rotated ♯
  still looks like a ♯, but the mirror turns G♯ into A♭ and C♯ into E♭. ♮ is
  unchanged.
- Write the dotted halves (bars 1, 2, 4, 8, 25, 29, 31, 32) as half tied to
  quarter, so that no augmentation dot lands on the wrong side of a note head
  for the far reader. Ties and beams rotate correctly; the hinge tie is its
  own mirror.

### Critic (critic, 2026-11-04)

parallels_error 0, parallels_weak 0, beat_parallels 0, unresolved 0,
unverified 0, bad_doublings 0, reach_errors 0;
dissonances: 2 accented passing (b2.2 and b31.2, the same quarter-note passing
fourth seen from both sides); melody: 1 note ("large leap not recovered",
b15.3, the comes A2–A3–C♯4 climbing to the hinge); crossings 0; two hands
throughout. Most beats are two-note
sonorities (the critic now counts them apart, dyad beats 76%), so the
"tertian fit" figure (30%, of the beats with three or more pitch classes)
says little about two-voice music.

### Weak spots (honest)

- **Very consonant.** I traded expressive suspensions for symmetry (each would
  become a weak-beat anticipation in the other half). Apart from the two
  passing fourths, the beat-level counterpoint has no dissonance at all. Some
  will hear chastity, others blandness.
- The double (9–15) and its rotation (18–24) are continuous sixteenths. Its
  melodic identity rests on sequence shapes (rising tetrachords in bar 11,
  falling ones in 13) more than on a memorable figure. Some will hear it as
  figuration.
- The bare-octave first bar is a curtain, not a theme. A minor is confirmed
  only at bar 4, and the ear may take the opening for E or C.
- Bar 26's diminished-seventh leap A♭5–B4 and its mirror, F3–G♯2 in bar 7,
  are deliberate (the dux's B4 then resolves to C5) but angular.
- The hinge (a held unison D4 for four beats) is the conceptual climax. Whether
  it lands as a "clink of glasses" or as a gap is untested by ear.

---

## II. Canon per tempora ("Four clocks, one hour")

### The trick

One melody M sounds at **four speeds, 4 : 3 : 2 : 1** (bass slowest, soprano
fastest), the voices at octaves. Bach's augmentation canons use 1 : 2.
Ockeghem's Missa prolationum uses mensural ratios. Nancarrow's player-piano
tempo canons converge on a point. Here the entries are staggered so that
**every voice attacks M's last note at the same instant**, the *punctum
convergentiae* at bar 33 (the score's last bar), held there as an equal
fermata in all voices (each final note carries `"fermata": true`). Every
duration before it is exactly proportional.

**M begins with the Westminster Quarters** (the Cambridge Quarters, Great St
Mary's, 1793, traditionally credited to Joseph Jowett with William Crotch, the
opening drawn from a phrase of Handel's "I know that my Redeemer liveth"). It
uses the hour sequence, changes 2–5:
E G♯ F♯ B | E F♯ G♯ E | G♯ E F♯ B | B F♯ G♯ E. Each entry is therefore
another clock starting to chime, each faster than the last:

| bar | voice | speed | the chime in that voice |
|---|---|---|---|
| 1 | bass "Big Ben" | ×4 | half notes and whole bars, alone |
| 9 | tenor | ×3 | dotted quarters (two per bar against the bass's three halves) |
| 17 | alto | ×2 | quarters |
| 25 | soprano, the little clock | ×1 | eighths |
| 33 | all | — | convergence on E |

The 6/4 metre puts every voice's "M-beat" (12 units at ×1) on a dotted-half
beat, so the four speeds share barlines. Inside each bar the voices run 3
against 2 against 4 against 6.

### Making the harmony controllable

At a time τ before the convergence, the voice at speed r is τ/r from the end
of M. So the slow bass is always singing *later* material than the fast
voices. Its last quarter of M runs under the soprano's whole statement, and so
on. Functional harmony cannot be "the same" in all four positions at once.
The design therefore makes M's later sections into pedals under everyone
else's earlier material:

- **M = chime (I)**, then a **development** in the chime's rhythm reversed
  (q. e e e) whose long notes C♯ B G♯ F♯ E C♯ are the bass line of bars 9–20.
  The bass's long notes under each chime entry are chime-compatible (I, vi,
  iii, V). Then come the **bells**: two dominant strikes (B), two tonic
  strikes (E), a long G♯, a flourish B G♯ D♯ that falls to the leading tone,
  and E.
- In the piece this gives: bass chime alone (1–8); a moving bass under the
  tenor's chime (9–16); the bass continues (17–20) under the alto's chime;
  **dominant pedal B** (21–24), over which the alto's development resolves
  D♯ → E into bar 25. The **tonic arrives in the bass exactly where the
  little clock enters (bar 25)**, and a tonic pedal runs to the end. Over the
  pedal the tenor, alto and soprano reach their own B and E strikes one after
  another, and the four speeds land on E together. Because the voices reach
  the flourish one after another, its D♯ → E sounds four times in stretto:
  bass b31.5 → b32.1, tenor b32.1 → b32.2.5, alto b32.3 → b32.4, soprano
  b32.5 → b32.5.5.
- **The convergence and parallels.** In an octave canon, just before a
  simultaneous convergence every voice holds M's penultimate note in octaves.
  If that note moves to the final one, every pair of voices makes parallel
  octaves (the first full build had exactly these errors). M therefore ends
  D♯ → E → E: the voices *land* on E one by one (bass first, soprano last),
  each from its own leading tone, and then all strike it together.
- **The ratio rule.** A melodic move at distance x from the end in one voice
  sounds at the same moment as a move at distance 2x, 3x, 4x, 3x/2 or 4x/3 in
  another. Identical moves at such distances are therefore parallel octaves.
  An early tail that alternated E and G♯ produced four of them; the final tail
  uses only distinct moves.

### How the computation was used (and what it did not do)

- `tempo_tools.partner_map` lists which notes of M meet which others on beats.
  It showed about ten partners per note, which is why the work needed tools.
- `tempo_search.py` is a beam search over Westminster "changes" (rectus or
  inverted) and their degrees, with a cost copied from the critic's rules. It
  established feasibility. Its best candidates oscillate between G♯ and B,
  which is harmonically safe but static, so I **rejected them**. The
  development in the score is **hand-written** (the descending sequence above).
- `tempo_repair.py --blame` maps each critic error back to the notes of M
  that cause it. `--try` reports the error counts for one note changed at a
  time. Starting from my hand-written line (3 parallel errors, 9 unresolved),
  I made **seven single-note edits** after reading those reports: in the
  development (C♯4 at the end of the third cell, E4 ending the fourth, A4
  and B4 in the fifth, F♯4 and G♯4 in the sixth) and in the flourish (G♯4
  for A4). The result was 0 / 0 under the critic of that time. Flourishes
  containing the leading tone (A F♯ D♯, B F♯ D♯ and others) produced 1–7
  unresolved clashes against the E strikes, so a pentatonic flourish
  (B G♯ F♯) stayed. In the Nov 2026 pass the stricter critic found an
  unresolved clash at b18.3 and an unverifiable one at b31.5, and I made two
  more single-note edits: E4 for A4 in the fifth development cell, and D♯4
  for F♯4 in the flourish. B G♯ D♯ E is the leading-tone flourish the first
  attempts were after, and it makes no clash against the E strikes.
- `verify_canones.py` confirms from the JSON that each voice equals M (pitch
  sequence up to whole octaves; durations ×r; no gaps), that all four last
  notes are attacked at quarter 192 and that all end at quarter 198.

### Critic (critic, 2026-11-04)

parallels_error 0, parallels_weak 0, beat_parallels 0; unresolved 1 (b19.3);
unverified 1 (b25.2); bad_doublings 1 (b26.3); crossings 2; reach_errors 2;
pedal 20, suspension 5 (+1 unprepared), retardation 1 (+1 unprepared),
accented passing 9, appoggiatura 10, chord 4, "chord (7th not resolved down)"
8 notes; no melodic findings.

- **Fixed: b18.3** (bass A2 under the alto's G♯4, an unprepared major seventh
  that the alto left by leap). The fifth development cell now reads
  E F♯ E B instead of E F♯ A B, so the bass has E2 there (E major under the
  alto's chime). The same note change also removed an unprepared suspension
  at b18.3 and the passing seventh at b21.6.
- **Fixed: b31.5** (bass F♯2 under the tenor's B3, which the critic could not
  follow to a resolution). The flourish is now B G♯ D♯ E, see above.
- **The one UNRESOLVED (b19.3), justified.** Bass and tenor share C♯3 in
  unison while the alto has F♯4, a fourth above. The bass resolves it
  (C♯ → B, the next note of its line); the tenor, in unison with it, leaves
  by leap, and the critic gives the "bass" role to the tenor. The tools
  agent is fixing the critic's choice between unison bass voices in this
  pass; the event itself is a fourth resolved by the bass.
- **b25.2 unverified, declined.** The soprano's first chime, E5 G♯5 F♯5 B4 in
  eighths: its F♯5 is the Westminster chime's own passing note, on a weak
  eighth inside the dotted-half beat, against the alto's long E4. The critic
  cannot verify a resolution because the two voices then exchange the notes
  (alto E4 → F♯4, soprano → E5 on b25.4). The chime is the quotation and every
  voice sings it; the alto's E4 is the development's long E, the bass note
  of bar 17.
- **b26.3 bad doubling, declined.** E2 B2 under B4 and C♯5: the critic reads
  C♯m7 over E with its "seventh" B doubled. Over the tonic pedal it is E with
  an added sixth: the alto's C♯5 falls to B4 on the next beat (6–5), and B is
  the chord's fifth. Every note is structural (the chime's B, the
  development's C♯ peak, the bells).
- **Crossings 2, declined.** b9.5.5 (bass C♯3 above tenor B2) and b26.2.5 (alto
  C♯5 above soprano B4), 1.5 beats each, by a whole tone. In a canon at the
  octave a melody that spans more than an octave must overlap the voice an
  octave above it. M runs from B3 (the chime's low B) to C♯5 (the
  development's peak), a ninth, and both crossings are exactly these two
  notes meeting. Changing either breaks the Westminster chime or the bass
  line of bars 9–20.
- **"7th not resolved down" (8 notes).** Three are passing sevenths over the
  pedals (b17.3, b26.1, b28.6). Five are the flourish's D♯ over the tonic
  pedal (b31.5 twice, b32.1, b32.3 twice): the critic reads D♯ as the major
  seventh of Emaj7 and expects it to fall, but it is the leading tone and
  rises to E in every voice.
- low_register_seconds 9 (bars 9–20 plus b32.1: bass and tenor a second apart
  around B1–C♯3).
- **Keyboard: for player piano or two players, not one pianist.** 25 of 149
  onsets need more than two hands, and no division between two hands can
  reach the attacks at b21.1 (B1 E3 C♯5) and b27.1 (E2 E3 B3 C♯6). The canon
  fixes the voices an octave apart with the bass two octaves below the alto,
  so these spans cannot be closed. `metadata.instrument` says so: "Player
  piano or piano four hands (two players)". Primo takes soprano and alto,
  secondo tenor and bass, one voice per hand, and every attack is reachable.
  The critic therefore no longer treats the score as solo keyboard.

### Weak spots (honest)

- **Harmonically it is a bell piece.** The harmony is tonic- and
  dominant-based with pedals. The only real progression is in bars 9–20 and in
  the upper voices over the pedals. Many four-voice beats are triads with an
  added sixth or seventh over a pedal, not Bach-style functional chords. The
  critic is clean; that does not make the harmony rich.
- **Bars 1–8 are a solo bass** (with ratios 4:3:2:1 the slowest clock is
  necessarily alone for a quarter of the piece). Bars 29–30 move slowly (B
  strikes over E/G♯).
- **The final approach.** The structural V–I with D♯ → E is at bars 24–25.
  Since Nov 2026 the flourish also falls to the leading tone, so each voice
  reaches the final E from D♯, one after another, over the tonic pedal.
  Whether the convergence sounds like a goal or only like a coincidence of
  strikes cannot be judged here. The bass's D♯2 lasts two beats under the
  soprano's E5 (b31.5–6), a semitone clash three octaves wide: the harshest
  moment of the piece.
- The fermata is an equal held note in all voices, and each final note now
  carries `"fermata": true` for the engraving (`tempo_canon.mark_fermata`).

---

## Notes for the tools (not edited; outside this folder)

- `critic.check_dissonance`: when two voices share the lowest pitch, the
  "bass" role goes to one of them regardless of which resolves, so the
  classification (suspension vs UNRESOLVED) can depend on voice order (canon
  II, b19.3). Being fixed by the tools agent (Nov 2026).
- `critic.check_crossing` once assumed the voices were listed top-down; it now
  orders voices by mean pitch (fixed).
- `chords.chord_candidates` needs three pitch classes, so in two-voice music
  every dissonance falls through to the suspension/passing logic, and
  `reduce.py` printed "?" for most dyads. The tools agent is adding two-voice
  chord naming (Nov 2026); the critic now reports dyad beats separately.
- `render_music.py` had no fermata; the tools agent is adding engraving for the
  event field `"fermata": true`, which canon II now sets. Also, the voice names
  are not wrapped: long `name`s are clipped at the left margin of the PDF.

---

## Self-critique pass (Nov 2026)

Canon II (tempo canon) was checked against the critic after its fix of
09df800, which also follows each dissonance to its resolution and checks hand
reach. Any change to M sounds in all four voices, so each edit was tried in
all four and `verify_canones.py` still passes.

- **Fixed:** the unprepared, unresolved seventh at b18.3 (M's fifth cell:
  A4 → E4) and the unverifiable dissonance at b31.5 (flourish F♯4 → D♯4). The
  second edit also answers the old weak spot "no leading tone": each voice now
  reaches the final E from D♯, in stretto.
- **Fixed:** the final notes carry `"fermata": true` (set by
  `tempo_canon.mark_fermata` after the build), ready for the engraving support
  the tools agent is adding.
- **Declined, with reasons in the Critic section:** b25.2 (the quoted chime's
  passing F♯, exchanged with the alto), the b26.3 doubling (E with an added
  sixth, B is the fifth), the two crossings (a ninth-wide melody in an octave
  canon) and the two unreachable attacks (the piece is for player piano or two
  players; `metadata.instrument` now says so).
- **Left to the tools agent:** b19.3 (the critic's choice between unison bass
  voices) and two-voice chord naming, which mostly concerns canon I.
- Canon I (table canon) needed nothing: its critic figures are unchanged.
