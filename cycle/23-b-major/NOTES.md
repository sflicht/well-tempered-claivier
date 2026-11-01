# Fugue XXIII in B major, five voices: *Fantasia ut re mi fa sol la per tutti i tuoni*

After John Bull's keyboard fantasia *Ut, re, mi, fa, sol, la* (Fitzwilliam Virginal Book no. LI).
Five voices (Bach's B-major fugue, BWV 868, has four): a four-voice fugue and a cantus.
89 bars in 4/4, ♩ = 100 (92 at home), about 3:42 in the Bach-Lehman render.

I have not heard any render. Everything below comes from the score and from the tools.

## Concept at the new size

Bull's fantasia is one of the earliest keyboard pieces that needs every key to be usable: the
hexachord *ut re mi fa sol la*, held in semibreves, starts again a whole tone higher after each
statement until it has stood on all twelve pitch levels, a century before the Well-Tempered
Clavier. This fugue borrows his machine and gives it to one voice.

- **The Cantus** (the fifth voice) enters after the exposition and walks through Bull's thirteen
  statements in semibreves, one note per bar, with one exception: in the twelfth statement (B♭,
  b75–78) its first four notes move in minims, so that this one block lasts four bars instead of
  six and home arrives early. It rises on one level (*ut→la*) and falls on the next
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
- **Cantus**: the hexachord in semibreves, `hex_up` / `hex_dn`, transposed into each key; the B♭
  statement is written out by hand (`G5:8 F5:8 Eb5:8 D5:8 C5:16 Bb4:16`).

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
| 45–50 | 1:46 | **Bull's leap**: C, rising | Quiet. Subject in the deep bass (C2), whose free continuation stays low (b47–48) to leave the cantus room; a triplet division (Bull's sesquialtera) in the alto; subject on G (tenor) at *sol*. |
| 51–56 | 2:00 | D, falling | Inversion bass (D); the cantus's G is the seventh of A7; **no second entry**: the soprano's division turns dotted (b55–56) over the cantus and bass alone (the tenor rests from b53 to its entry at b57) and runs on into the E region. |
| 57–62 | 2:15 | E, rising | Subject tenor (E) with CS; episode a 5; subject on **B** (bass) at *sol*: the home key's subject returns under the cantus. |
| 63–68 | 2:29 | F♯, falling | Inversion alto (F♯) with the bass a tenth or less below it (b64–67 lie an octave higher than a bass usually would, so that one hand takes bass and alto); the cantus's B is the seventh of C♯7; inversion on B (soprano) at *re*. |
| 69–74 | 2:44 | A♭, rising | **b69: the drone**, a bare A♭/E♭ fifth in all voices (the meantone wolf). Subject on B♭ (tenor) at *re*; a turn to B♭ minor (b72, ii7 of A♭); subject on E♭ (alto) at *sol*. |
| 75–78 | 2:58 | **B♭, falling, compressed** (on top) | The one block that breaks the clock. The soprano rests; the cantus is the top voice and sings *la sol fa mi* in minims, twice its rate, over the bass's inversion (B♭): Gm – B♭, then F7 – G7 – C, its E♭ (the seventh of F7) falling to D, which hangs over the bass's C as a 9–8. *Re* and *ut* return to semibreves: a cadence into C (b77) which is the **Neapolitan of B**; the cantus's B♭ becomes **A♯** in F♯7 (b78). Four bars instead of six. |
| 79–84 | 3:08 | **B, rising: home** (an octave above its first entry) | Subject bass (B) with CS; subject on E (tenor) at *fa*; at the cantus's *la* (G♯5, its highest note; the soprano reaches E6 elsewhere) the soprano rests for a bar, so the cantus is on top while the bass sings the inversion under it: the turn. |
| 85–89 | 3:24 | B, falling: *sol fa mi re ut* | Coda: IV (6–5) – IV6 – ii7 – I6/4, then I6 – I – vi – I, V – V7, I under the falling cantus. The soprano comes down a ninth in tied steps (E6 → D♯5) and ends a third above the cantus's last *ut*; final chord B1 B2, F♯4 B4 D♯5. |

Tempo: ♩ = 100; a breath into Bull's leap (b44 ramps to 80), the wolf bar a little broader (90),
home at 92, and the last three bars slow to 60.

## The device and where to hear it

- **The cantus walking through the twelve keys.** It is the only voice in semibreves, struck a
  little louder (base velocity 72 against 64–66 for the fugue voices). Every new note is a new key
  centre at the start of a region, and the statements join by step. It is the top voice in b75–78
  and at its *la* in b84; in b79–83 it lies just under the soprano, and in the coda the soprano
  comes down to end a third above its last *ut* (B4), the second-highest note of the final chord.
- **The subject as the cantus in quick notes.** b9 (soprano and cantus start together on B), b21
  (tenor on E♭ under the cantus's E♭), b33 (bass on G), b45 (deep bass on C), b57 (tenor on E), b79
  (bass on B). Each time the head runs through in one bar the six notes that the cantus will take six
  bars to sing.
- **Rectus with the rising cantus, inversion with the falling one.** Every falling region opens with
  the inversion entering on the cantus's *la* (b15, b27, b39, b51, b63, b75).
- **Hexachord mutation as tonal plan.** Entries on *fa* (E at b82: the soft hexachord) and on *sol*
  (F♯ at b13, B♭ at b25, D at b37, G at b49, B at b61, E♭ at b73: the hard hexachord) are the
  modulations.
- **Bull's leap** (b44–45): the first staircase ends on a lone E6; C major arrives under it, quiet,
  with the subject in the deep bass and a new triplet figure.
- **The clock breaks once** (b75–78). Twelve six-bar blocks teach the ear when the next key will
  arrive. In the B♭ block, right after the wolf, the cantus (now the top voice) falls
  *la sol fa mi* in minims, so that the block lasts four bars and home comes two bars early.
- **The homecoming** (b77–79): a cadence into C turns out to be the Neapolitan of B; the cantus's
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
- **b78–79 (3:05–3:08)**: F♯7 → B. In meantone the "A♯" is the B♭ key, so F♯–A♯ is 427 cents, and the
  home chord B–D♯ is 427 cents too. Home itself is one of meantone's worst keys.
- **b15–20 (0:34)**: C♯ major, with C♯–E♯ at 427 cents in meantone.
- **The excerpt pair** `renders/meantone-demo-bach-lehman.mp3` and `renders/meantone-demo-meantone.mp3`
  plays b66–72 alone (about 20 seconds; the drone is the fourth bar), for a direct comparison.

## Critic numbers (`python3 tools/critic.py cycle/23-b-major/fugue.json`)

| measure | value | target |
|---|---|---|
| parallels_error | **0** | 0 |
| parallels_weak | 0 | – |
| beat_parallels | **0** | ≤ 2 |
| dissonance_unresolved | **0** (3 unverified, to check by ear: b43.2, a lower-neighbour C♯4 in the alto; b74.1 and b80.1, the countersubject's tied note resolving 4–3 while the partner the critic pairs it with moves on) | ≤ 3 |
| bad_doublings | **0** | ≤ 2 |
| low_register_seconds | **6** (b39.3.5, b40.2.5, b40.3.75, b58.2.5, b58.3.5: passing sixteenths of the inversion/CSI pair in tenor and bass, and of the tenor's subject over the bass; b87.2.5: the bass's passing A♯1 under the tenor's held B2) | ≤ 9 |
| stepwise_pct | **63.3** (leap ≥ 4th: 10.9) | ≥ 65 (missed) |
| crossings | 9 (all "alto above cantus"; see weak spots) | few |
| reach_errors | **0** (was 23) | 0 |
| keyboard_unplayable_pct | **5.5** (52 of 944 onsets, each with a held note a pedal can catch; was 11.8) | < 15 for 5 voices |
| mean moving voices | **3.76** | – |
| pc tripled on beats | 13.3 % | – |
| themes | 29 subject/inversion entries, all 16/16 intervals and rhythm | – |

The 14 cantus statements were checked separately (the critic compares everything with the
subject): each is exactly *ut re mi fa sol la* rising or *la…ut* falling in its key, 14/14 (the B♭
statement with its first four notes in minims), and the coda's five notes are *sol fa mi re ut* of B.

Moving voices per section: exposition 2.4; B 3.3; C♯ 3.0; E♭ 3.2; F 3.8; G 4.0; A 4.3; C (after the
leap) 3.5; D 3.8; E 4.0; F♯ 4.3; A♭ 4.5; B♭ 3.8; home 4.7; coda 4.4. All five voices move in 17 bars
(b35–36, 43–44, 59–60, 65–66, 69, 73–74, 79–80, 82–83, 86, 88).

Remaining critic notes: 45 "seventh not resolved down" notes (mostly the cantus, whose sevenths rise
with the hexachord, or sevenths held into the next chord); melody: two seventh leaps (b69 soprano
D♭6 → E♭5 into the drone; b71 bass G2 → F3, kept because G3 or E♭3 there make octaves with the
tenor or fifths with the rising cantus), one tritone (b41 bass, after the CSI), two leaps over an
octave after a rest (b19, the bass's inversion entry; b27, the bass's CSI), two compound same-way
leaps and two large leaps not recovered at once.

## Method and disclosure

- Every note is written in `fugue.py`. Thematic statements are explicit transforms of the
  hand-written subject, countersubject, inversion and CSI (`key`: chromatic + letter transposition;
  `octv`: octave shift). The cantus statements are `hex_up` / `hex_dn`, the hexachord transposed to
  each *ut* or *la*, chosen by hand; `last=12` shortens a statement's last note by a beat where the
  next harmony needs the space (b20, b32, b44, b56, b68). The B♭ statement (b75–78) is a literal
  token string. Everything else is a literal token string
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

- **Lines with life, partly.** The divisions (b11–12, b23–24, b35–36, b45–48, b59–60, b81) and the
  countersubject move; but several inner parts in the episodes still move in quarter-note chord tones
  (alto and tenor in b41–44, b53–54, b65–66, b76–78, b84), and stepwise motion is 63.3 %, under
  the 65 % target. The subject's own tail and the countersubject move partly in thirds, and the
  divisions are partly broken chords, as virginal divisions are.
- **The scheme is regular, until it is not.** Twelve of the thirteen regions last six bars; most have
  a rectus or inversion entry tied to the cantus and one modulating entry (25 entries in b9–84). The
  plan breaks in D (no second entry, a dotted division instead), A♭ (the drone, an entry on *re*, the
  turn to B♭ minor), B♭ (the clock itself: four bars, *la sol fa mi* in minims) and at home (entry on
  *fa*, the turn). Before b75 the clock is Bull's, unchanged, for 66 bars; whether its one break
  comes too late to relieve that is a question for the ear.
- **No stretto.** The cantus fixes the harmony a bar at a time; two subject entries closer than a bar
  conflict with it. The combination the piece offers is subject with cantus, not subject with
  subject.
- **The cantus is often an inner voice.** Until b74 it lies under the soprano and often under the
  alto too; on one piano an inner semibreve decays. The alto crosses above it in nine passages (the
  critic's 9 crossings), always while the cantus lies in the lower part of its range (B3–A♯4). It is
  the top voice in b75–78 and at b84, lies directly under the soprano in b79–83, and in the coda the
  soprano comes down to a third above it.
- **Keyboard.** Every attack now fits two hands (0 reach errors). 5.5 % of onsets still need a held
  note caught by the sostenuto pedal, nearly always the cantus's semibreve between a low bass and a
  high soprano: b16–18 (the C♯ division over the cantus), b47–48 (the bass lowered to clear the cantus
  after Bull's leap), b52, b58–60 and b74 (the soprano's tied E♭6 over the alto's subject).
- **A leap in the bass** at b71 (G2 → F3) was kept to avoid parallels with the rising cantus.
- **Not heard.** The balance of the cantus, the triplet passage and the meantone effect are
  unverified by ear.

## Review (response to `REVIEW-3.md`)

(Bar numbers in this section are those of the 91-bar version; from b79 on, subtract two.)

Applied, each built and checked with `tools/critic.py` (still 0 parallels, 0 beat parallels,
0 unresolved, 0 bad doublings):

1. **The cantus's goals.** The soprano rests in b86 (it ends its countersubject at 85.4¾ and returns
   on A♯5 at b87), so at its *la*, G♯5, the cantus is the top voice and the bass's inversion the
   lowest: the two hexachords, slow and fast, are the outer voices at the turn. NOTES no longer calls
   G♯5 the top of the piece (the soprano reaches E6 in b84–85 and b87–88). The final *ut* stays
   inside the last chord, as the review suggests; NOTES says so.
2. **Bull's leap.** The bass's free line in b47–48 is an octave lower (A2…D2), clearing the space
   under the cantus's C4–F4 after the leap. It costs keyboard reach in those two bars.
3. **After the wolf.** C3 instead of C2 at 69.4: the first third (A♭–C) still arrives on beat 4, and
   C3 → B♭2 is a step. The G2 → F3 leap at b71 stays; the review's tests (and mine) show the
   alternatives make octaves with the tenor or fifths with the cantus.
4. **Regularity.** The D region (b51–56) now has no second entry: the soprano's inversion on G is
   replaced by a dotted division (a figure the piece had not used) that runs on into the E region.
   With the A♭, B♭ and home regions, four of the thirteen regions now break the plan. I kept the
   six-bar clock: one cantus note per bar is Bull's machine, the piece's premise. A stretto is not
   possible against the cantus (see weak spots); the inverted countersubject (CSI) is already used in
   the F, A and F♯ regions. **Keyboard:** the bass's CSI in b27–28 now sits in its original octave
   (D3–E4) under the tenor's inversion, which brings it within reach (b28 had 7 three-hand onsets);
   with item 2 the total is 11.8 %. Raising the coda's bass (b89) was tried and dropped: it made a
   beat-parallel fifth with the alto.
5. **Meantone demonstration.** `renders/meantone-demo-meantone.mp3` and
   `renders/meantone-demo-bach-lehman.mp3` play b66–72 only (a scratch copy of `fugue.json` cut to
   those bars, same notes and tempo), so the wolf bar (b69, the fourth bar of the excerpt) is heard
   without a minute of meantone's wide thirds before it.

Not changed: the homecoming (b79–81), the wolf bar (b69) and the subject's head over the cantus
(b9, b21, b33, b45, b57, b81), as the review asks.

## Review response (Nov 2026)

The owner's review of the pull request (written by ChatGPT) made three points about this fugue.
I checked each against the score.

Playability was a real problem. The new reach check found 23 attacks that no division between two
hands could strike, among them the example the review gives (b17, G♯1 F♯4 B♯5). All of them came
from free voices placed around the cantus, never from the cantus or a declared entry, so I
revoiced only free voices. The soprano's division in b17–18 now starts within a tenth of the cantus
(D♯5, then E♯5). In b35 the tenor holds G3 and the bass holds B2. The alto turns differently in b41
(G♯4 instead of E4) and stops early in b44. In b55–56 the tenor's filler is gone, so the dotted
division is a trio and the tenor rests four bars before its E entry. In b64–67 the bass lies an
octave higher and the alto breathes for an eighth at b65. In b83 the alto holds D♯5 instead of
dropping to F♯4. In the
coda the bass stays deep, the tenor keeps within a tenth of it and the alto stays under the cantus
in the right hand, while the soprano comes down from E6 in tied steps to end on D♯5, a third above
the cantus's last *ut*. The piece used to end on a bright B5. It now ends on a closer, darker chord
with the cantus just under the top. I think that is the right ending for a tour that comes home,
but it is a real change. Reach errors went from 23 to 0, and onsets that need a pedal from 11.8 % to
5.5 %, with no new parallels or unresolved dissonances.

On form, the review suggested that thirteen six-bar blocks teach the clock too early, and I agree
that the second staircase only repeated the first one's length. I tried the smallest change that
alters the form rather than the surface. The B♭ statement, the last one before home and the first
after the wolf, now moves *la sol fa mi* in minims and lasts four bars. Its last two notes keep
their semibreves, so the homecoming (C heard as the Neapolitan of B, B♭ heard as A♯) is untouched
but comes two bars early, against an expectation that has had twelve blocks to form. Bull's pitch
itinerary is unchanged. The piece is now 89 bars. I did not overlap or interrupt a block: the
cantus is one voice, so an overlap would have to hand part of the hexachord to another voice and
blur the line the piece asks the ear to follow.

The listening-guide entry described the archived 24-voice version. It now describes this score. I
checked the review's claim about the wolf: the bare A♭/E♭ fifth is bar 69, as it says, and the
compression comes after it, so bar 69 is unchanged.

## From the N+1 version

- **Kept:** the title and concept (Bull's tour of twelve keys as a cantus, with a fugue around it);
  Bull's verified order and his leap as a dive into C with the subject in the deep bass; the subject
  and its mirror inversion; the A♭ region as the meantone wolf; the separate meantone render.
- **Changed:** twenty-four voices became five, 96 bars became 89 (4:18 → 3:42). The 24 one-key voices
  and the rising/falling mirror-canon pairs became a single cantus that alternates rising and falling
  statements, so the whole tour is one stepwise line. A four-voice exposition now comes first. The
  countersubject is new. Entries are tied to the cantus's direction (rectus over rising, inversion
  over falling) and to the hexachord slots where they fit. The wolf is now a full bar of bare fifths
  in every voice. The homecoming is new: C as the Neapolitan of B and B♭ heard as A♯. The 16-voice
  summit chorus became a five-voice home statement whose cantus falls back to *ut* in the coda.
- **Why:** with 24 voices the tour ran at 5–7 voices of mostly safe chord tones over half-note basses,
  and the summit's lines could not be followed. At five voices the cantus can be followed through all
  twelve keys, every entry has a rest before it and its own register, and the texture can thin to
  three or four voices (b15–20, b45–48, b55–56, b75–78) and fill to five where it matters (b35–36,
  b43–44, b79–89).

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
