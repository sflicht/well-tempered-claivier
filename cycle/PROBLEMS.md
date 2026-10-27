# What didn't work, and what was done about it

Thirty-six problems found in the movements composed before this edition (the
October 23 auditions and the tools behind them), each with its fix. Every
pair was reviewed bar by bar against Bach's WTC I and II by a separate critic;
the full reviews are the `REVIEW.md` files in each pair folder, and each
pair's `NOTES.md` maps every review item to the bars that changed. Numbers
come from `tools/critic.py`, calibrated on Bach's own four-voice fugues
(BWV 869, BWV 878): 0 parallel 5ths/8ves, 1–2 accented (beat-to-beat)
parallels, 1–2 % of beats with a tripled pitch class, 3–9 low-register clashes.
Nobody has listened to the new renders yet; the listener's ear is still the
final judge.

## The cycle as a whole

1. **The C-minor pair was numbered I.** In Bach's key order C minor is No. II,
   so its fugue owed three voices, not two. *Fix:* renumbered Pair II and
   recomposed à 3 (`02-c-minor/`); a new C-major Pair I written (`01-c-major/`).
2. **Fugue VIII's subject was borrowed without credit.** Its first six notes
   are the head of Bach's D♯-minor fugue subject (BWV 853). *Fix:* credited, and
   turned into a feature: Bach's complete subject now enters as a guest voice
   near the end, revealing where ours came from.
3. **The many-voice fugues were "harmony, not counterpoint".** Fugue VIII v3
   averaged 4.5 moving voices on nine staves; its climax was the subject in
   octaves over block chords. *Fix:* nine real voices, a stretto maestrale
   instead of block chords, and a thickening pass on the middle section.
4. **Collisions that sounded like mistakes.** The 100-bar Fugue VIII had 218
   parallel 5ths/8ves, 294 accented parallels, 195 unresolved dissonances and
   286 low-register clashes. *Fix:* the new Fugue VIII has 0, 0, 1 (justified)
   and 8.
5. **Every movement stopped dead.** One fixed tempo, no ritardando, no way to
   hear a written Adagio. *Fix:* tempo maps in the renderer, MIDI, spatial
   renderer and listening page; every finished movement now broadens at its
   cadence and Prelude II's Adagio bar is audible.
6. **The README and status pages were stale.** They described the 100-bar
   Fugue VIII as current and never mentioned the October pairs. *Fix:*
   rewritten for this edition.

## The checking tools

7. **The old checker missed parallel fifths between crossed voices** (and
   flagged parallel fourths instead), because it assumed the lower-numbered
   voice was always on top. *Fix:* order-independent test in all 14 copies of
   `chk.py`/`pardet.py`, and in the new `tools/critic.py`.
8. **No check for accented parallels.** Fifths and octaves on successive beats
   with a passing note in between passed every check (Fugue IV v7 had 22,
   Fugue V v3 had 38). *Fix:* `beat_parallels` in the critic.
9. **No check for doubling and low mud.** *Fix:* tripled-pitch-class and
   low-register-clash measures, calibrated on Bach.
10. **The renderer misspelled flat keys** (F major used sharps). *Fixed.*
11. **The renderer dropped rehearsal marks that fell inside rests**, could not
    hide empty staves, and wrote duplicate notation files for each audio
    render. *Fixed* (`--audio-only`, `hide_empty_staves`).
12. **No temperament.** A project named after the well-tempered keyboard
    rendered everything in equal temperament. *Fix:* Bach–Lehman, Werckmeister
    III, Kirnberger III, Vallotti and meantone, plus per-note cents for just
    intonation.

## Pair II, C minor (formerly "Pair I")

13. **Fifteen of 34 fugue bars had code-chosen pitches**, against the project's
    own rule. *Fix:* every note rewritten by hand.
14. **No subject statement for twelve bars** (v5 b15–26); the "inversion
    canon" matched only 5 of 16 intervals. *Fix:* a thematic statement in
    every section; the subject, its augmentation and its inversion together in
    G minor (b15–18); a mirror trio in F minor (b21–22).
15. **Square, stop-start phrasing.** Every entry on a downbeat, subject and
    countersubject cadencing together, the texture collapsing to 7 attacks at
    every arrival. *Fix:* entries off the beat, joins that run across, 10–16
    attacks at arrivals.
16. **The peak was the thinnest bar** (a bare C6/C3 octave). *Fix:* a
    three-voice stretto, the fullest bar of the piece.
17. **The exposition never left C minor; new keys arrived without cadences.**
    *Fix:* answer at the dominant; every key entered by a cadence.
18. **The prelude was a chord chart filled by a voicing optimiser**, 90 %
    chord tones, no melody, and a dominant pedal that went quieter. *Fix:*
    rewritten by hand with passing and neighbour notes (69.5 % chord tones,
    BWV 847's prelude 70.4 %); the group accents spell the fugue subject; a
    written Presto/Adagio after BWV 847; the pedal now climbs and grows.

## Pair IV, C-sharp minor

19. **The exposition thinned instead of building**: duets at b7–10, all five
    voices first together at bar 33. *Fix:* entries build 1→5 and stay; five
    voices by bar 10.
20. **The "countersubject" was only a rhythm**, its pitches reinvented at every
    entry. *Fix:* one fixed, invertible pitch shape.
21. **22 accented parallels, 19 % tripled beats**, three voices in octaves at
    b36. *Fix:* 1 and 8 %.
22. **Entries harmonised over E (an E major-seventh sound); subject endings on
    suspended chords.** *Fix:* a C♯–B–A lament bass under the entries.
23. **Generic episodes** (scales in thirds, contrary scales). *Fix:* episodes
    from the subject's head and Bach's "cross" motif in diminution.
24. **A block-chord ending with a doubled leading tone.** *Fix:* a tonic-pedal
    coda with the cross motif on top and a late Picardy third.
25. **The prelude never cadenced in root position on a strong beat**, and it
    shared its metre, tempo and tempo word with the fugue. *Fix:* root-position
    cadences at the return and the close; imitation between the hands; the
    fugue slowed to Moderato sostenuto for contrast.
26. **Twelve beats of the same G♯7** in the prelude's "arrival". *Fix:* the
    dominant pedal moves every half bar, with the cross motif as 4–3 and 6–5
    suspensions.

## Pair V, D major

27. **Every stretto collapsed onto a held triad over a pedal**; half the beats
    were D or A chords. *Fix:* strettos with diminution and inversion over
    walking basses; beats on D/A 50 % → 36 %, beats over a pedal 33 % → 12 %.
28. **The key plan never left D and A**, with no minor-key entry after bar 20.
    *Fix:* entries in B minor and E minor (inverted), a cascade through
    F♯m–Bm–Em–A–D–G.
29. **A real answer where a tonal one was needed**, and entries every two
    bars like clockwork. *Fix:* tonal answer, irregular spacing.
30. **The contrabass doubled the bass** and collided with it (low unisons and
    seconds). *Fix:* its own line; doubling runs 0; low clashes 29 → 10.
31. **Episode 2 was a scale in parallel tenths in lockstep**, and Episode 3 a
    violin bariolage over an oom-pah bass. *Fix:* five-voice episodes from
    the subject's tail and tattoo over a suspension chain.
32. **The prelude played one 8-bar progression three times**, as pure
    arpeggio with 55 % of right-hand notes above BWV 850's top note. *Fix:*
    irregular form, a B-minor region, a written top line, register brought
    down (10 % above B5), and a flourish into the fugue.

## Pair VIII, E-flat minor

33. **The prelude discarded the 12/8 "Night loom" draft Sam liked**, for a
    French overture whose inner voices re-struck algorithmic chord tones.
    *Fix:* rebuilt on the Night loom texture, its melody the fugue subject in
    retrograde inversion.
34. **Static stretti**: three entries on one pitch level in octaves over a
    16-beat tonic pedal. *Fix:* entries one to six beats apart at different
    levels; the arrival's bass is the subject at quarter speed.
35. **A plodding subject** that closed with a V–i cadence and the same rhythm
    in all 17 statements. *Fix:* final note elided so entries flow;
    augmentation, diminution (the "dance" episode) and inversion.
36. **The C♭-major surprise was a splice with no way back.** *Fix:* prepared
    by the C♭ of b39, entered by a real deceptive cadence, left through A♭
    minor.
