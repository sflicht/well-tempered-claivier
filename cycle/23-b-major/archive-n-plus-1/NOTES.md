# Fugue XXIII in B major, twenty-four voices: *Fantasia ut re mi fa sol la per tutti i tuoni*

After John Bull's keyboard fantasia *Ut, re, mi, fa, sol, la* (Fitzwilliam Virginal Book no. LI).

## The premise

Bull's piece is one of the earliest pieces of keyboard music that cannot be played in the tuning of its
day. The hexachord *ut re mi fa sol la* is held in semibreves while the other voices move around it.
After each statement it starts again a whole tone higher, and it goes on climbing until it has stood
on all twelve pitch levels. The Fitzwilliam editors (1899) noted that the passage "proves that some
kind of 'equal temperament' must have been employed". The Well-Tempered Clavier is the next chapter
of the same story, so the cycle's penultimate fugue borrows Bull's machine.

**24 voices = 24 keys.** Each voice owns one of the cycle's keys. In its key it sings the hexachord
as a long-note cantus: rising (*ut re mi fa sol la*) in a major key and falling (*la sol fa mi re ut*)
in a minor key. The step pattern W W H W W is a palindrome, so the falling minor hexachord is both
the inversion and the retrograde of its relative major's rising one, on the same six pitches. Each
major key is therefore paired with its relative minor. The pair sings a mirror canon:

- the major voice climbs in semibreves;
- a bar and a half later the minor voice enters an octave and a sixth higher and falls;
- its notes land on the rising notes as a 9-8 / 7-6 chain of suspensions.

A new pair begins every five and a half bars, alternately on beat 1 and on beat 3, and each one sits a
whole tone higher than the last, as in Bull's order.

## Bull's order, and how it was verified

The order of Bull's hexachord statements was read from two public-domain sources, which agree:

- *The Fitzwilliam Virginal Book*, ed. J. A. Fuller Maitland and W. Barclay Squire (Breitkopf &
  Härtel, 1899), vol. I p. 183 (no. LI) and the introduction p. xix. I worked from the scan on the
  Internet Archive, item `imslp-virginal-book-various`, file *TheFitzwilliamVirginalBookVol1.pdf*,
  PDF page 208. IMSLP's own download was bot-blocked.
- Edward W. Naylor, *An Elizabethan Virginal Book* (Dent, 1905), pp. 103–104, from Internet Archive
  item `elizabethanvirgi00nayluoft`.

Bull's order is G, A, B, D♭ (written C♯ in the source), E♭, F. The next step would return home, so
instead he leaps a minor third to A♭. Then come A♭, B♭, C, D, E, F♯, and finally home to G. Some
sources attribute the piece to Poglietti (Schulenberg, *JSCM* 11). The FVB copy carries Bull's name,
and so does this credit.

Transposed so that "home" is B, the order becomes:

**B** | C♯(D♭) E♭ F G A | (Bull's leap of a minor third) C D E F♯ A♭ B♭ | **B**.

That order is the tonal plan of the fugue. The *Canon per tonos* of the *Musical Offering* also
climbs by whole tones, which is the Bach link.

## Material (`x23.py`, all hand-written)

- **Cantus:** the hexachord in long notes (`hex_up`, `hex_dn` are transpositions of it).
- **S, the subject (2 bars):** it opens by spelling the hexachord in quick notes, B C♯ D♯ E F♯ G♯,
  then turns back in sixteenths to the dominant: `B4:6 C#5 D#5 E5:2 F#5:2 G#5:4 | F#5 E5 D#5 E5 C#5
  D#5 B4 C#5 A#4:2 B4:2 F#4:4`.
- **I:** the exact diatonic mirror of S, whose axis falls between *mi* and *fa*. It falls *la sol fa mi
  re ut* and is used for the minor keys.
- **CS / CSI:** a lively virginalist countersubject and its mirror.
- **HEAD / IHEAD:** the first bar of S and the first bar of I.

## Section map

| bars | section | what happens |
|---|---|---|
| 1–12 | Exposition | Alto V (the B voice) sings B C♯ D♯ E F♯ G♯ in breves. Over each of these notes the subject enters in that note's key: S in B (bass), I in c♯, I in d♯, S in E, S in F♯, I in g♯ (deep bass). The hexachord thereby spells out B major's family of keys. |
| 13–40 | First staircase | Pairs 1–5: D♭/b♭, E♭/c, F/d, G/e, A/f♯. Each pair carries a full S in its major key, placed at the cantus's *ut* (D♭, A) or *fa* (E♭, F, G), where the subject fits the suspension chain. The figuration changes from pair to pair: eighth-note divisions, sixteenth divisions, dotted alto, broken chords, and "hunting" repeated notes. |
| 41–43 | Seam | The bass descends F♯–E–D–C♯, comes to rest on F♯7 (the home dominant: five whole steps would bring B back too soon), slips a semitone to G7 and dives to C. This is Bull's leap. |
| 44–78 | Second staircase | Pairs 6–11: C/a (the dive, deep bass), D/b, E/c♯, F♯/d♯, A♭/f, B♭/g. S enters in each major key; pair 11 gathers HEADs (B♭ bass, E♭, F). At b78 the E♭7 is respelled as D♯7, the dominant of G♯ minor. |
| 79–91 | Summit | Six of the B family's hexachords return together, with I and S in stretto and a ii–V chorus (detail below). |
| 89–90 | Arrival | S in B in four voices at 1/8 and 1/2 bar, over the B1 pedal. |
| 92–96 | Coda | E rises and c♯ falls in minims, the "soft" plagal hexachords, over the pedal. The bass closes E2–F♯2–B1. |

Tempo: q = 92. It breathes at the seam (ramps to 74 into b44), broadens to 86 from the summit, and
slows to 62 in the last two bars. The audio lasts about 4:18.

## The summit (bars 79–91): who sings what

- **Frame:** Bass VI (the g♯ voice) falls *la→ut* in breves, G♯2 F♯2 E2 D♯2 C♯2 B1. This is the other
  half of the B voice's opening statement. It ends on the B1 pedal, which lasts until the end.
- **The dominant pair:** Tenor IV (F♯) rises F♯4… from b80, and Sop V (d♯) falls D♯6… from b81.3. They
  form the same suspension canon as in the tour. Alto V (B) rises B3… from b81.
- **I in G♯ minor:** Sop I at b79, Alto I at b79.3 (stretto at the octave below), and Sop III at b87.
  Alto III plays CSI.
- **IHEAD:** Sop IV (b81), Ten I in d♯ (b85), Bass I (b86).
- **Chorus over the ii–V (b86–89, G♯m7 | C♯m7 | F♯7 | B):** Sop IV, Sop VI, Alto II, Alto IV,
  Alto VI and Ten II. They are written as suspension chains, and each group attacks on its own beat
  (1, 2, 3 or 4), so that no two of the added lines ever move together.
- **Arrival (b89–90):** S in B in Alto III; S a fifth higher (diatonic, in B) in Sop II an eighth
  later; S an octave higher in Sop I half a bar later; S in Ten III a bar later.
- **Coda:** E rises in Ten VI and c♯ falls in Alto II, both in minims (their second statements).

The summit is the only place where any voice sings its hexachord a second time: F♯, d♯, B, E and c♯
come back there. Bass VI (g♯) and Alto V (B, in the exposition) sing their own hexachord only in
these outer sections.

## Meantone and well temperament: where they part

Rendered in quarter-comma meantone (`--temperament meantone`: eleven ¼-comma fifths, with the wolf
between G♯ and E♭), several passages break. The figures below are computed from
`tools/render_music.py`'s temperament table:

| interval | meantone | Bach-Lehman | equal |
|---|---|---|---|
| G♯–E♭ (A♭–E♭) fifth | **737.6 ¢ (wolf)** | 700.0 | 700 |
| A♭–C, D♭–F, B–D♯, F♯–A♯ major thirds | **427.4 ¢** | 402–404 | 400 |
| C–E, E♭–G, B♭–D major thirds | 386.3 ¢ (pure) | 392–400 | 400 |

- **Bars 66–71 (pair 10, A♭ major / F minor) are the wolf passage.** The pair opens at b66.1 on a
  bare fifth with no third: A♭2 A♭3 A♭4 A♭4 against E♭4 E♭5 (Bass II, Ten II's cantus, Alto IV's S in
  A♭, Sop V, Ten IV, Sop VI). In meantone that is the wolf, G♯–E♭ = 737.6 ¢, sounding in six voices.
  Every A♭-major and D♭-major chord in bars 66–70 rests on a 427-cent third (for example A♭/C at
  b68.3). In Bach-Lehman the fifth is pure (700 ¢) and the thirds are 402–404 ¢.
- **Bars 41–44 (the seam):** the F♯7 halt is sour in meantone (F♯–A♯ = 427 ¢). The G7 → C that
  follows is the sweetest chord in the system. The ear goes from the worst to the best in two beats.
- **Bars 78–79:** E♭7 is respelled as D♯7 and resolves to G♯ minor. In meantone this pivot crosses
  the wolf directly. Bull's piece, and the whole circle, depends on that pivot being possible.
- The home key itself (B major) and its dominant are meantone's "bad" keys. The summit and coda
  would sound uniformly rough in meantone.
- **Renders for comparison:** `renders/fugue-meantone.mp3` (audio only, with
  `--temperament meantone`), `renders/fugue.mp3` (Bach-Lehman) and `renders/fugue-equal.mp3`.

## Method

- **Composition order:** the summit was drafted first (frame, themes, then free lines one voice at a
  time). Then the exposition, then the tour pair by pair, then the seam, then the summit chorus.
- **Every note is written in `fugue.py` or `x23.py`.** Thematic statements are explicit transforms of
  the hand-written material: `in_key` (transposition by letter and semitone), `octv`, `hex_up` and
  `hex_dn`. The only scripted placement of thematic material is `tour_cantus()`, which places the 22
  tour cantus statements from the `TOUR` table: voice, *ut*, *la*, bar and beat, all chosen by hand.
  Each minor voice enters 1.5 bars after its major partner. The one programmed exception is the
  shortened *ut*: the minor voice's last note is shortened where the next pair's *la* enters (and to
  a dotted half at b78, so that Sop I can breathe before the summit's I).
- **Scratch tools (scratchpad only; none choose notes).**
  - A bench builds partial scores and runs `tools/critic.py`.
  - A sequential checker accepts or rejects whole hand-written lines and prints their clashes.
  - A helper appends an accepted pair to `fugue.py` as literal token strings.
  - A per-slot listing shows which chord tones are free.
  - Every rejected line was rewritten by hand: parallels with the rising cantus at the barline were
    the most common fault.
- **No tool changes** were made.

## Credits

- **John Bull**, *Ut, re, mi, fa, sol, la* (FVB LI): the hexachord through all twelve pitch levels,
  the order of keys, and the leap of a minor third. Verified as described above.
- **The hexachord itself** is Guido's.
- **The virginalist figurations** (divisions, broken chords, "hunting" repeated notes) are generic
  style; no specific source is quoted.

## Measurements (`python3 tools/critic.py cycle/23-b-major/fugue.json`)

Fugue (96 bars, about 4:18 in the Bach-Lehman render):

| measure | value | target |
|---|---|---|
| parallels_error | **0** | 0 |
| beat_parallels | **1** (b88.3 S5/T4, D♯5/G♯4 → C♯5/F♯4, a dominant cantus against a free line) | ≤ 8 |
| parallels_weak | 1 (b90.2.75 S2/T3, sixteenth passing notes inside the arrival stretto) | – |
| dissonance_unresolved | **0** | ≤ 15 |
| bad_doublings | **8** | ≤ 8 |
| low_register_seconds | **7** | ≤ 16 |
| stepwise_pct | **60.2** | ≥ 60 |

Notes on the counts:

- **Bad doublings.** Four are two thematic lines meeting on the same seventh: b80.2, I against the F♯
  cantus; b85.4, IHEAD in d♯ against Alto V's B-major cantus; b89.4, the arrival's S in B5 over the B1 pedal;
  b93.4, the E and c♯ coda cantus meeting on A. The other four are b7.4, b82.2, b84.3 and b84.4, in the
  exposition and the summit.
- **Low-register clashes.** These are at b48.1 (the 7–6 suspension of the deep C/a pair, G2 against F3),
  b82.3, b86, b88.2 and b94.1.
- **Themes.** The critic's theme check compares everything against S. The 29 cantus statements were
  checked separately: each is exactly *ut re mi fa sol la* rising (major) or falling (minor) in its key
  (29/29). The S and I entries match at 16/16.

**Moving voices (mean per bar).**

| section | mean | maximum |
|---|---|---|
| Exposition, b1–12 | 3.5 | 6 |
| First staircase, b13–40 | 5.5 | 7 |
| Seam, b41–43 | 4.3 | 5 |
| Second staircase, b44–78 | 5.8 | 7 |
| Summit, b79–91 | 9.9 | 16 |
| Coda, b92–96 | 8.0 | 9 |

Summit per bar: b79 7, b80 7, b81 10, b82 8, b83 10, b84 8, b85 11, **b86 15, b87 16, b88 16**, b89 10,
b90 6, b91 5.


## Weak spots

- **The summit is not dense enough.** The plan was 20 or more moving lines for several bars. The
  peak is 16, in bars 86–88. I tried more lines over the ii–V (eight further candidates in tenor and
  bass registers). Each one made parallels or unresolved suspensions against the 16 already there,
  and I did not keep any of them. Reaching 20 would need the summit's existing free lines (Bass V,
  Alto III, Ten VI) to be recomposed together with new ones. That is the first thing I would redo.
- **The tour is thinner than planned:** 5–7 moving voices, against 7–9 and then 10–13 in the plan. The
  climb into the summit is weak: bars 72–78 have only 3–6 moving voices, so the summit arrives more
  as a change of texture than as the end of a crescendo of voices. The dynamics map (velocity) carries
  the build-up more than the voice count does.
- **The arrival thins out.** After the stretto at b89–90 the texture falls to 5–6 voices until the coda's
  minim hexachords enter.
- **Several tour bass lines move only in half notes (Bass II, Bass IV).** That is functional but plain.
  I added passing notes by hand to the bass lines and to Ten III and Alto V, in b27, b37–38, b51,
  b54, b56, b58, b63, b68, b73 and b77. Each was checked with the critic and kept only if no
  measure got worse.
- **The free lines often keep to safe chord tones.** The most common fault I had to remove was a
  parallel octave or fifth with the rising cantus at the barline. As a result, many free lines move
  against the cantus by contrary motion or by a held note, rather than having melodic shapes of their
  own.
- **Pair 11 (B♭/g) has no complete subject.** No slot fitted the suspension chain, so it uses three
  HEADs instead (B♭ in the bass, E♭, F).
- **The theme labels are not all checked by the critic.** The critic checks themes only against S, so
  the cantus entries show as partial matches. They were verified separately (29/29).
- **Leaps at the joins.** There is a minor-seventh leap in Sop I at b79.1: the g-minor cantus's *ut*
  B♭4, then the summit's I on G♯5, across a quarter rest. There is also one augmented-second spelling
  (A2 E5 → D♭5) at the D♭ entry, b13.1.
- **I cannot hear the result.** The balance of 24 piano voices, the audibility of the cantus inside
  the texture, and the meantone effect are unverified by ear. The spatial render (`--layout ring`)
  was made to help the voices separate.


# Prelude XXIII in B major: *A Ground upon Ut re mi fa sol la*

## Concept

The prelude is an English virginalist's set of divisions on a ground: the kind of piece Byrd and Bull
wrote on the hexachord (Byrd's *Ut re mi fa sol la*, FVB no. CI; Bull's no. LI, the model of the
fugue). It is for one player.

- **The ground** is the fugue's cantus: the hexachord in minims, up and down, B C♯ D♯ E F♯ G♯ |
  G♯ F♯ E D♯ C♯ B, six bars.
- **Its harmony:** I – V4/3 | I6 – IV | V – vi | IV6 – V7 | ii6/5 – I6 | V4/3 – I.

It is stated four times, each time with a new division, and then closes:

| bars | division |
|---|---|
| 1–6 | The plainsong: treble in minims with a few crotchets, a mean voice, the ground in the bass. |
| 7–12 | Quaver divisions in the treble (broken chords, as on the virginals). The mean is rewritten so that it moves against them. |
| 13–18 | The ground moves to the treble. The bass divides in quavers, and the mean follows the ground in sixths. |
| 19–24 | Semiquaver runs in the treble over the ground, as in Bull's fastest variations. |
| 25–26 | Close: IV – V7 – I. The final B-major chord leaves room for the fugue's first breve, on the same B. |

Tempo: q = 72 ("like a pavan; the divisions in time"). It broadens in the last two bars. The audio
lasts about 1:27.

## Critic numbers (`tools/critic.py cycle/23-b-major/prelude.json`)

| measure | value |
|---|---|
| parallels_error | 0 |
| beat_parallels | 0 |
| unresolved dissonances | 0 |
| bad_doublings | 0 |
| low_register_seconds | 0 |
| keyboard_unplayable_pct | 0 (at most 3 notes at once) |
| stepwise_pct | 49 |

The stepwise figure is low because the divisions in bars 7–12 are broken chords, as virginal
divisions are.

## Method and credits

- Every note is a literal bar string in `prelude.py`, and the ground is written out each time.
- A first draft had parallel octaves between the mean and the treble's quavers (b8–11) and between
  the bass quavers and the treble ground (b6, b16, b18). They were rewritten by hand.
- The genre (ground and divisions on the hexachord) comes from Byrd and Bull. No notes are quoted.

## Weak spots

- It is short: four divisions. A virginalist set would usually go further, with triplets and a
  galliard-like proportion. Bars 19–24 drop the mean voice, so only two voices sound there.
- The harmony of the ground is the same in all four statements. Only the close is new.
