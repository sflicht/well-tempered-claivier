# Fugue XXIII in B major, five voices: *Fantasia ut re mi fa sol la per tutti i tuoni*

After John Bull's keyboard fantasia *Ut, re, mi, fa, sol, la* (Fitzwilliam Virginal Book no. LI).
Five voices (Bach's B-major fugue, BWV 868, has four): a four-voice fugue and a cantus.
91 bars in 4/4, ♩ = 100 (92 at home), about 3:47 in the Bach-Lehman render.

I have not heard any render. Everything below comes from the score and from the tools.

## Concept at the new size

Bull's fantasia is one of the earliest keyboard pieces that needs every key to be usable: the
hexachord *ut re mi fa sol la*, held in semibreves, starts again a whole tone higher after each
statement until it has stood on all twelve pitch levels, a century before the Well-Tempered
Clavier. This fugue borrows his machine and gives it to one voice.

- **The Cantus** (the fifth voice) enters after the exposition and walks through Bull's thirteen
  statements in semibreves, one note per bar. It rises on one level (*ut→la*) and falls on the next
  (*la→ut*). Because *la* of one key and *la* of the key a tone higher are a step apart, and so
  are their two *ut*s, every joint between statements is a single step: the line is one continuous
  zigzag through all twelve keys. The only exceptions are Bull's own leap (A → C) and the last joint,
  B♭ → B, a semitone, where the B♭ is re-read as A♯, the leading note of home.
- **The fugue** (soprano, alto, tenor, bass) follows the cantus into each key. Its subject begins
  with the hexachord in quick notes, so over a rising statement the subject enters **rectus** on the
  cantus's own note: the cantus sings in six bars the six notes the subject's head runs through in
  one. Over a falling
  statement the subject enters **inverted** (*la sol fa mi re ut*), falling with the cantus.
- **One bar is a tuning experiment**: the A♭ statement opens with a bare A♭/E♭ fifth in all five
  voices. In Bach-Lehman it is an open fifth; in quarter-comma meantone it is the wolf.

## Bull's order, and how it was verified

Kept from the earlier version, which read it from two public-domain sources that agree:

- *The Fitzwilliam Virginal Book*, ed. J. A. Fuller Maitland and W. Barclay Squire (Breitkopf &
  Härtel, 1899), vol. I p. 183 (no. LI) and the introduction p. xix (Internet Archive item
  `imslp-virginal-book-various`, *TheFitzwilliamVirginalBookVol1.pdf*, PDF page 208).
- Edward W. Naylor, *An Elizabethan Virginal Book* (Dent, 1905), pp. 103–104 (Internet Archive item
  `elizabethanvirgi00nayluoft`).

Bull's order is G, A, B, D♭ (written C♯), E♭, F; the next step would return home, so he leaps a
minor third to A♭; then A♭, B♭, C, D, E, F♯, and home to G. Transposed so that home is B:

**B** | C♯ E♭ F G A | (leap) C D E F♯ A♭ B♭ | **B**.

Here the leap is taken downward (A4 → C4, a major sixth) so that the second staircase starts again
in the middle register.

## Material (all in `fugue.py`, written in B)

- **Subject** (2 bars, kept from the earlier version): `B4:6 C#5 D#5 E5:2 F#5:2 G#5:4 | F#5 E5 D#5 E5
  C#5 D#5 B4 C#5 A#4:2 B4:2 F#4:4`. The head climbs the hexachord (ut held, re mi in sixteenths,
  fa sol in eighths, la); the tail falls back through it in a virginalist division and drops to the
  dominant. Harmony: I – IV | V. Its only common tone of I and IV is *ut*, and its second bar wants
  *re* under it, which is why it fits a rising cantus exactly at *ut re*.
- **Answer**: real, on F♯, i.e. the "hard" hexachord on *sol*.
- **Countersubject** (new): `R:4 D#5 F#5 E5 G#5:4 A#5 B5:4~ | B5:4 A#5:4 F#5 E5 D#5 C#5 E5 D#5 C#5 A#4`.
  It waits a beat (the subject's *ut* is heard alone), runs in broken thirds, holds G♯, rises into a B
  tied over the barline (4–3 against the dominant), then falls in sixteenths while the subject's
  own sixteenths have stopped. Written above the subject; used below it at the octave (5–6 instead of
  4–3), with its last beat rewritten by hand where the harmony or the cantus required it.
- **Inversion**: the diatonic mirror around the axis between *mi* and *fa* (B↔G♯, C♯↔F♯, D♯↔E):
  *la sol fa mi re ut* in quick notes; harmony vi | V. **CSI**, the countersubject's mirror, is used
  with it in the tenor and bass (its tie resolves upward, a retardation).
- **Cantus**: the hexachord in semibreves, `hex_up` / `hex_dn`, transposed into each key.

**Where the subject can enter over the cantus.** Over a rising statement (*ut re mi fa sol la*) the
rectus fits wherever the cantus moves up a step from the subject's *ut*: on *ut* (its own key), on
*re* (the next key), on *fa* (the subdominant, the "soft" hexachord) and on *sol* (the dominant, the
"hard" hexachord). Over a falling statement the inversion fits wherever the cantus moves *la → sol*
of its key: on *la* (its own key), *mi* (dominant) and *re* (subdominant). The piece uses these slots
and no others. A rising region's entry on *sol* ends on the dominant of the dominant, which is the
next key's tonic (so the next falling region begins on its vi); a falling region's entry on *re*
ends on the next key's subdominant (so the next rising region begins with a plagal step).

## Section map (bar, time in the Bach-Lehman render)

| bars | time | cantus | entries and texture |
|---|---|---|---|
| 1–8 | 0:00 | – | Exposition a 4: subject tenor (B), answer alto (F♯) with CS below, subject soprano with CS below, answer bass (F♯) with CS above. Closes on V4/3 → I. |
| 9–14 | 0:19 | **enters**: B, rising | Subject soprano on *ut* (B4, while the cantus enters on B3 an octave below); a soprano division over a three-part texture; subject on F♯ (tenor) at *sol*, CS above. |
| 15–20 | 0:34 | C♯, falling | Inversion (C♯) soprano on *la*; three parts; inversion on F♯ in the bass at *re*. The cantus's F♯ is the seventh of G♯7 and falls to E♯. |
| 21–26 | 0:48 | E♭, rising | Subject tenor (E♭) with CS; the soprano's first sixteenth division; subject on B♭ (bass) at *sol*. |
| 27–32 | 1:02 | F, falling | Inversion tenor (F) with CSI in the bass; tenor/bass dialogue; inversion on B♭ (soprano) at *re*. |
| 33–38 | 1:17 | G, rising | Subject bass (G) with CS; episode in five voices; subject on D (alto) at *sol*. |
| 39–44 | 1:31 | A, falling | Inversion tenor (A) with CSI; the cantus's D is the seventh of E7; inversion on D (soprano) at *re*, ending on a lone E6. |
| 45–50 | 1:46 | **Bull's leap**: C, rising | Quiet. Subject in the deep bass (C2); a triplet division (Bull's sesquialtera) in the alto; subject on G (tenor) at *sol*. |
| 51–56 | 2:00 | D, falling | Inversion bass (D); the cantus's G is the seventh of A7; inversion on G (soprano) at *re*. |
| 57–62 | 2:15 | E, rising | Subject tenor (E) with CS; episode a 5; subject on **B** (bass) at *sol*: the home key's subject returns under the cantus. |
| 63–68 | 2:29 | F♯, falling | Inversion alto (F♯) with CSI; the cantus's B is the seventh of C♯7; inversion on B (soprano) at *re*. |
| 69–74 | 2:44 | A♭, rising | **b69: the drone**, a bare A♭/E♭ fifth in all voices (the meantone wolf). Subject on B♭ (tenor) at *re*; a turn to B♭ minor (b72, ii7 of A♭); subject on E♭ (alto) at *sol*. |
| 75–80 | 2:58 | B♭, falling (on top) | The soprano rests; the cantus is the top voice. Inversion bass (B♭); a cadence into C (b79) which is the **Neapolitan of B**; the cantus's B♭ becomes **A♯** in F♯7 (b80). |
| 81–86 | 3:13 | **B, rising: home** (an octave above its first entry) | Subject bass (B) with CS; subject on E (tenor) at *fa*; at the cantus's *la* (G♯5, the top of the piece) the bass sings the inversion: the turn. |
| 87–91 | 3:28 | B, falling: *sol fa mi re ut* | Coda: IV – ii7 | I6 – vi – I | V7 (4–3 in the soprano) | I under the falling cantus; the last *ut* (B4) sits in the middle of the final chord. |

Tempo: ♩ = 100; a breath into Bull's leap (b44 ramps to 80), the wolf bar a little broader (90),
home at 92, and the last three bars slow to 60.

## The device and where to hear it

- **The cantus walking through the twelve keys.** It is the only voice in semibreves, struck a
  little louder (base velocity 72 against 64–66 for the fugue voices). Every new note is a new key
  centre at the start of a region, and the statements join by step. It is the top voice in b75–80
  and lies just under the soprano in b81–91.
- **The subject as the cantus in quick notes.** b9 (soprano and cantus start together on B), b21
  (tenor on E♭ under the cantus's E♭), b33 (bass on G), b45 (deep bass on C), b57 (tenor on E), b81
  (bass on B). Each time the head runs through in one bar the six notes that the cantus will take six
  bars to sing.
- **Rectus with the rising cantus, inversion with the falling one.** Every falling region opens with
  the inversion entering on the cantus's *la* (b15, b27, b39, b51, b63, b75).
- **Hexachord mutation as tonal plan.** Entries on *fa* (E at b84: the soft hexachord) and on *sol*
  (F♯ at b13, B♭ at b25, D at b37, G at b49, B at b61, E♭ at b73: the hard hexachord) are the
  modulations.
- **Bull's leap** (b44–45): the first staircase ends on a lone E6; C major arrives under it, quiet,
  with the subject in the deep bass and a new triplet figure.
- **The homecoming** (b79–81): a cadence into C turns out to be the Neapolitan of B; the cantus's
  B♭ is spelled B♭ in the cantus but sounds as A♯ in F♯7, and steps up a semitone to B.

## Meantone and well temperament: where they part

`renders/fugue-meantone.mp3` is the same performance in quarter-comma meantone (eleven ¼-comma
fifths, the wolf between G♯ and E♭); the listening room can switch tuning. Interval sizes from
`tools/render_music.py`'s temperament table (cents), and beat rates computed from the tuned
frequencies (A4 = 440):

| interval | meantone | Bach-Lehman | equal |
|---|---|---|---|
| A♭–E♭ (G♯–E♭) fifth | **737.6** (the wolf) | 700.0 | 700 |
| E♭–A♭ fourth | 462.4 | 500.0 | 500 |
| A♭–C, C♯–E♯, B–D♯, F♯–A♯ major thirds | 427.4 | 402.0–403.9 | 400 |
| C–E, E♭–G, D–F♯, G–B major thirds | 386.3 (pure) | 392.2–400.0 | 400 |

- **b69 (2:44): the wolf.** A full bar of bare fifths, no third: bass A♭2, tenor E♭3, alto A♭3,
  cantus A♭4, soprano E♭5. In meantone the fifths A♭2–E♭3, A♭3–E♭5 and A♭4–E♭5 beat at about 6, 13
  and 26 times a second; in Bach-Lehman at about 0.35, 0.7 and 1.4. What to listen for: whether the
  drone is steady (Bach-Lehman) or wavers and grinds (meantone). On beat 4 the bass moves to C2, the
  first third (A♭–C, 427 cents in meantone).
- **b45–50 (1:46) and b21–26 (0:48)**, C major and E♭ major: meantone's best keys; their major thirds
  are pure (386.3 cents) in the meantone render, against 392–400 in Bach-Lehman.
- **b80–81 (3:10–3:13)**: F♯7 → B. In meantone the "A♯" is the B♭ key, so F♯–A♯ is 427 cents, and the
  home chord B–D♯ is 427 cents too. Home itself is one of meantone's worst keys.
- **b15–20 (0:34)**: C♯ major, with C♯–E♯ at 427 cents in meantone.

## Critic numbers (`python3 tools/critic.py cycle/23-b-major/fugue.json`)

| measure | value | target |
|---|---|---|
| parallels_error | **0** | 0 |
| parallels_weak | 0 | – |
| beat_parallels | **0** | ≤ 2 |
| dissonance_unresolved | **0** | ≤ 3 |
| bad_doublings | **0** | ≤ 2 |
| low_register_seconds | **5** (b39.3.5, b40.2.5, b40.3.75, b58.2.5, b58.3.5: passing sixteenths of the inversion/CSI pair in tenor and bass, and of the tenor's subject over the bass) | ≤ 9 |
| stepwise_pct | **62.5** (leap ≥ 4th: 11.3) | ≥ 65 (missed) |
| crossings | 9 (all "alto above cantus"; see weak spots) | few |
| keyboard_unplayable_pct | **11.3** (109 of 965 onsets) | < 15 for 5 voices |
| mean moving voices | **3.81** | – |
| pc tripled on beats | 13.9 % | – |
| themes | 30 subject/inversion entries, all 16/16 intervals and rhythm | – |

The 14 cantus statements were checked separately (the critic compares everything with the
subject): each is exactly *ut re mi fa sol la* rising or *la…ut* falling in its key, 14/14, and the
coda's five notes are *sol fa mi re ut* of B.

Moving voices per section: exposition 2.4; B 3.3; C♯ 3.0; E♭ 3.2; F 3.8; G 4.0; A 4.3; C (after the
leap) 3.5; D 4.2; E 4.0; F♯ 4.3; A♭ 4.5; B♭ 3.7; home 4.8; coda 4.8. All five voices move in 21 bars
(b35–36, 43–44, 56, 59–60, 65–66, 69, 73–74, 81–82, 84–86, 88–91).

Remaining critic notes: 44 "seventh not resolved down" notes (mostly the cantus, whose sevenths rise
with the hexachord, or sevenths held into the next chord); melody: three seventh leaps (b69 soprano
D♭6 → E♭5 into the drone; b70 and b71 bass), one tritone (b41 bass, after the CSI), one leap over
an octave (b19, the bass's inversion entry after a rest), two compound same-way leaps and two large
leaps not recovered at once.

## Method and disclosure

- Every note is written in `fugue.py`. Thematic statements are explicit transforms of the
  hand-written subject, countersubject, inversion and CSI (`key`: chromatic + letter transposition;
  `octv`: octave shift). The cantus statements are `hex_up` / `hex_dn`, the hexachord transposed to
  each *ut* or *la*, chosen by hand; `last=12` shortens a statement's last note by a beat where the
  next harmony needs the space (b20, b32, b44, b56, b68). Everything else is a literal token string
  placed at a bar and beat.
- Tools: `tools/critic.py` after every passage (parallels, doublings, keyboard reach); a scratch
  grid printer (scratchpad only) showing every voice at each eighth; `tools/stretto_finder.py` was
  run on the subject (it proposes a rectus stretto at the octave after two beats), but no stretto
  survived against the cantus and none is used. No tool wrote or chose notes.
- `x23.py` (the 24-voice version's helper) is removed from the pair folder; the archive keeps its
  copy.
- Renders: `renders/fugue.*` (Bach-Lehman, piano, with PDF/MIDI/MusicXML), `fugue-equal.mp3`,
  `fugue-meantone.mp3`, and `fugue-spatial.mp3` (binaural, `--layout arc`, General MIDI program 6,
  harpsichord, as the nearest sound to Bull's virginals; the main render stays piano).

## Honest weak spots

- **Lines with life, partly.** The divisions (b11–12, b23–24, b35–36, b45–48, b59–60, b83) and the
  countersubject move; but several inner parts in the episodes still move in quarter-note chord tones
  (alto and tenor in b41–44, b53–54, b65–66, b75–80, b86–87), and stepwise motion is 62.5 %, under
  the 65 % target. The subject's own tail and the countersubject move partly in thirds, and the
  divisions are partly broken chords, as virginal divisions are.
- **The scheme is regular.** Thirteen regions, each with a rectus or inversion entry tied to the
  cantus and one modulating entry: 26 entries in 82 bars. Voices, registers and figures change from
  region to region, but the six-bar rhythm of the tour does not.
- **No stretto.** The cantus fixes the harmony a bar at a time; two subject entries closer than a bar
  conflict with it. The combination the piece offers is subject with cantus, not subject with
  subject.
- **The cantus is often an inner voice.** Until b74 it lies under the soprano and often under the
  alto too; on one piano an inner semibreve decays. The alto crosses above it in nine passages (the
  critic's 9 crossings), always while the cantus lies in the lower part of its range (B3–A♯4). It is
  the top voice in b75–80 and lies directly under the soprano in b81–91.
- **Keyboard.** 11.3 % of onsets exceed two hands, mostly where the soprano is high over a low bass
  and an inner voice falls between the hands: b17–18 (the high inversion), b28 and b64–65 (the
  inversion/CSI pairs), b52, b58, b74, and the coda b88–89.
- **Leaps in the bass** at b70–71 (two sevenths) were kept to avoid parallels with the rising cantus.
- **Not heard.** The balance of the cantus, the triplet passage and the meantone effect are
  unverified by ear.

## From the N+1 version

- **Kept:** the title and concept (Bull's tour of twelve keys as a cantus, with a fugue around it);
  Bull's verified order and his leap as a dive into C with the subject in the deep bass; the subject
  and its mirror inversion; the A♭ region as the meantone wolf; the separate meantone render.
- **Changed:** twenty-four voices became five, 96 bars became 91 (4:18 → 3:47). The 24 one-key voices
  and the rising/falling mirror-canon pairs became a single cantus that alternates rising and falling
  statements, so the whole tour is one stepwise line. A four-voice exposition now comes first. The
  countersubject is new. Entries are tied to the cantus's direction (rectus over rising, inversion
  over falling) and to the hexachord slots where they fit. The wolf is now a full bar of bare fifths
  in every voice. The homecoming is new: C as the Neapolitan of B and B♭ heard as A♯. The 16-voice
  summit chorus became a five-voice home statement whose cantus falls back to *ut* in the coda.
- **Why:** with 24 voices the tour ran at 5–7 voices of mostly safe chord tones over half-note basses,
  and the summit's lines could not be followed. At five voices the cantus can be followed through all
  twelve keys, every entry has a rest before it and its own register, and the texture can thin to
  three or four voices (b15–20, b45–48, b75–80) and fill to five where it matters (b35–36, b43–44,
  b81–91).

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
| 25–26 | Close: IV – V7 – I. The final B-major chord leads into the fugue on the same B. |

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
