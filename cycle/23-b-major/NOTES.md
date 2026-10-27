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

- **Bars 66–71 (pair 10, A♭ major / F minor) are the wolf passage.** The tenor cantus (Ten II) rises
  from A♭3. The bass and the subject in Alto IV (S in A♭ at b66) sit on A♭ against E♭. At b66.1 the
  bare fifth A♭/E♭ (G♯/D♯) sounds in four voices, and every A♭-major and D♭-major chord in b66–70 is
  built on a 427-cent third. In meantone the passage is unusable. In Bach-Lehman the fifth is pure
  (700 ¢) and the thirds are 402–404 ¢.
- **Bars 41–44 (the seam):** the F♯7 halt is sour in meantone (F♯–A♯ = 427 ¢). The G7 → C that
  follows is the sweetest chord in the system. The ear goes from the worst to the best in two beats.
- **Bars 78–79:** E♭7 is respelled as D♯7 and resolves to G♯ minor. In meantone this pivot crosses
  the wolf directly. Bull's piece, and the whole circle, depends on that pivot being possible.
- The home key itself (B major) and its dominant are meantone's "bad" keys. The summit and coda
  would sound uniformly rough in meantone. The equal-temperament render
  (`renders/fugue-equal.mp3`) is provided for comparison. No meantone render is included, so as not
  to clutter the folder; it can be made with the same command and `--temperament meantone`.

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

MEASUREMENTS_PLACEHOLDER

## Weak spots

WEAKSPOTS_PLACEHOLDER
