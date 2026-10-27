# Turning it up to 11: ambitious ideas

The test for each idea: it must be something Bach would recognise as his own
craft (learned counterpoint, allusion, the key cycle, the keyboard), pushed
past what one composer with pen and paper could check or play. Computation is
used to search and verify; the notes are still chosen and written.

Status: **[built]** implemented, **[in progress]** being composed now, **[next]** designed, not built.

## Top ten

1. **[built] Actually well-tempered.** Every movement renders in a historical
   temperament, Bradley Lehman's 1722 reading of the loops on Bach's own title
   page by default, with Werckmeister III, Kirnberger III, Vallotti, equal and
   quarter-comma meantone available (`tools/render_music.py --temperament`).
   Keys now have colours; meantone renders show why the collection existed.

2. **[built] Praeludium per omnes tonos (Prelude I, C major).** BWV 846's
   broken-chord texture travels through all 24 keys in WTC order. Each minor
   key's Neapolitan becomes the next major tonic. A Shepard–Risset voicing
   makes it climb a semitone per key yet arrive home in the starting register:
   an endless ascent no harpsichord could produce.

3. **[built] Scala strettarum (Fugue I, C major, two voices).** A subject
   designed by search so that it combines with itself in stretto at every
   distance from a whole bar down to a single eighth note; the fugue climbs
   that ladder rung by rung.

4. **[built] The stretto finder.** `tools/stretto_finder.py` scores every
   offset, interval, inversion and augmentation of a subject (or against a
   foreign subject) with the critic, so the combinations a subject permits are
   known before the form is planned.

5. **[built] Bach's subjects as real voices.** (Fugue I: BWV 846 as countersubject; II: BWV 847 augmented in the coda; III: BWV 848 grows out of the inversion; IV: BWV 849's cross as a second subject; V: BWV 850 as a baritone voice; VIII: BWV 853 as a guest.) Where a recomposed fugue meets
   its key-twin in the WTC, Bach's own subject enters as a genuine contrapuntal
   line found by search and fitted by hand, not quoted on top of the texture.

6. **[built] Prolation stretto.** (Fugue VIII's arrival: subject at quarter speed in the bass under inverted, augmented and normal-speed statements; Fugue V: the subject at x4, x2, x1 and x1/2, three at once.) The many-voice climaxes combine the subject
   with its inversion, augmentation and double augmentation at once: what
   BWV 853 does with three voices, at nine.

7. **[built] Contrapunctus permutationum.** Four lines in quadruple invertible
   counterpoint; all 24 vertical orderings are used, one in each of the 24
   keys. The whole key cycle compressed into one movement.

8. **[built] Canon cancrizans per motum contrarium.** A table canon: the
   second voice is the first played backwards and upside down, so the page
   rotated 180° is the same piece.

9. **[built] Canon per tempora.** ("Four clocks, one hour": the melody opens with the Westminster Quarters; speeds 4:3:2:1; all four voices strike the final E together.) One melody at four simultaneous speeds,
   staggered so that every voice reaches the final cadence together. No single
   player could perform it.

10. **[built] The listening room.** (https://claude.ai/artifact/BBJMS7b46MiEycNBM24yhB, built by `tools/build_listening_page.py`) A web page that plays every movement from
    its score in the browser, with a temperament switch, voice solo/mute,
    subject entries marked on a piano roll, and critic numbers per movement.

## Further ideas (not yet built)

11. **[built] A nine-voice spatial render.** (`tools/render_spatial.py`) Each voice placed in a virtual
    cathedral (binaural), so attention can travel between parts the way the
    project's planned film intends.
12. **[next] A cantus firmus across the cycle.** One phrase of "Vor deinen Thron
    tret ich hiermit" (the chorale appended to the Art of Fugue) in long notes
    in each fugue's coda; Fugue XXIV states the whole chorale.
13. **[in progress] Fugue XXIV as a quodlibet.** The 25-voice finale combines the
    subjects of the 23 earlier fugues plus its own, each in a fitted
    transposition and rate, as the Goldberg Variations end in a quodlibet.
14. **[next] A self-similar key plan.** The order of a fugue's middle-entry
    keys spells its own subject in mega-augmentation.
15. **[next] Polymetric convergence.** A prelude whose 3-, 4- and 5-beat
    ostinati drift apart and coincide exactly at the climax.
16. **[next] Riddle canons in every PDF.** One-line canons printed with only
    clefs and signs ("Quaerendo invenietis"), solved in the movement itself.
17. **[next] An attacca chain.** Every fugue's coda pivots into the next
    pair's key so the 48 pieces can be played as one continuous work.
18. **[next] Soggetto cavato signatures.** B-A-C-H answered by
    C-L-A-U-D-E (C E A G D E in the French letter mapping) hidden in the final
    cadence of every pair.

## Raising the ambition: the rest of the cycle

With the top ten built, the next step is the cycle itself, each pair with a
device of its own:

19. **[built] Pair III: Giga rectus et inversus.** Part 2 mirrors Part 1, and
    in the coda bars of both halves sound simultaneously.
20. **[built] Pair VI: passacaglia and fugue à 7.** A lament ground that
    migrates through all seven voices; toccata prelude after BWV 565.
21. **[built] Pair VII: fuga a due cori à 8.** Two complete four-voice
    choirs, subject against inversion, merging in an eight-voice stretto;
    chorale prelude on *Wachet auf*.
22. **[built] Pair IX: the comma pump and the ring.** A pastorale in
    adaptive just intonation that sinks a syntonic comma per cycle until the
    well-tempered keyboard corrects it; a ten-voice stile-antico ricercar
    whose motif travels round a ring of voices (Spem in alium), rendered
    binaurally in a circle.
23. **[in progress] Pair X: St Matthew homage à 11.** Two choirs in fugal
    dialogue beneath the chorale *O Lamm Gottes*, the subject derived from
    the chorale.
24. **[in progress] Pair XI: concerto fuga à 12.** Brandenburg 2's finale as
    a twelve-voice fugal concerto, concertino of four against a ripieno of
    eight.
26. **[in progress] Pair XII: the unfinished fugue, finished à 13.** The
    Art of Fugue breaks off just after B-A-C-H joins the first two subjects;
    Nottebohm showed the three combine with the main theme. Fugue XII
    completes that quadruple fugue in F minor, in thirteen real voices.
27. **[in progress] Pair XIII: fuga canonica à 14 on the Goldberg ground.**
    Canons at every interval, as in the Goldberg Variations, accumulating over
    the ground in F-sharp, ending in a quodlibet with the two folk songs of
    Variation 30.
28. **[in progress] Pair XIV: Ricercar a 15 on the Royal Theme.** Frederick
    the Great asked Bach for six voices; this answers with fifteen, including
    the Musical Offering's canonic devices and a canon per tonos.
25. **[in progress] Fugue XXIV à 25.** A twelve-tone B-minor subject (after
    BWV 869), strata moving at different rates, the convergence composed
    first, the cycle's subjects gathered at the end.
