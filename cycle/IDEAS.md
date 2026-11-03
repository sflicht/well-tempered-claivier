# Turning it up to 11: ambitious ideas

The test for each idea: it must be something Bach would recognise as his own
craft (learned counterpoint, allusion, the key cycle, the keyboard), pushed
past what one composer with pen and paper could check or play. Computation is
used to search and verify; the notes are still chosen and written.

Status: **[built]** implemented, **[next]** designed, not built.

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
13. **[built, smaller] Fugue XXIV as a quodlibet.** The plan was to combine the
    subjects of all 23 earlier fugues with its own, as the Goldberg Variations
    end in a quodlibet. Built: the subjects of Fugues I, II, IV, V and VIII
    arrive where the cantus makes their keys harmonies; the full 23-subject
    combination was not attempted, because the convergence was thinned for
    clarity.
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
device of its own. All of these are built. They were first composed under the
retired rule "Fugue N has N + 1 voices" (the old counts, à 7 to à 24, are kept
in each pair's `archive-n-plus-1/`); since November 2026 each fugue has at most
one voice more than Bach's in the same key, and the device was kept in the
smaller texture. Current voice counts are given below.

19. **[built] Pair III: Giga rectus et inversus** (4 voices). Part 2 mirrors
    Part 1, and in the coda bars of both halves sound simultaneously.
20. **[built] Pair VI: passacaglia and fugue** (4 voices). A lament ground that
    migrates through the voices; toccata prelude after BWV 565.
21. **[built] Pair VII: fuga a due cori** (4 voices). Two choirs of two,
    subject against inversion, quarrelling about the key; chorale prelude on
    *Wachet auf*.
22. **[built] Pair IX: the comma pump and the ring** (4 voices). A pastorale in
    adaptive just intonation that sinks a syntonic comma per cycle until the
    well-tempered keyboard corrects it; a stile-antico ricercar for four
    singers in a ring, rendered binaurally in a circle.
23. **[built] Pair X: St Matthew homage** (3 voices). One voice per choir in
    fugal dialogue beneath the chorale *O Lamm Gottes*, the subject derived
    from the chorale.
24. **[built] Pair XI: concerto fuga** (4 voices). Brandenburg 2's finale as a
    fugue for its four soloists, with a trumpet stuck in the wrong key.
25. **[built] Pair XII: the unfinished fugue, finished** (5 voices). The Art of
    Fugue breaks off just after B-A-C-H joins the first two subjects;
    Nottebohm inferred that the three combine with the main theme. Fugue XII is
    this work's conjectural completion of that quadruple fugue, with a fifth
    voice entering at the end.
26. **[built] Pair XIII: fuga canonica on the Goldberg ground** (4 voices).
    Canons at rising intervals over the ground in F-sharp, ending in a
    quodlibet with the two folk songs of Variation 30.
27. **[built] Pair XIV: ricercar on the Royal Theme** (5 voices). The Musical
    Offering's canonic devices and a canon per tonos that climbs and arrives
    home.
28. **[built] Fugue XXIV for twenty-five parts.** A twelve-tone B-minor subject
    (after BWV 869), strata moving at different rates, the convergence composed
    first, guest subjects from earlier fugues gathered at the end; at most 14
    real lines at once.
29. **[built] Pair XV: Vom Himmel hoch** (4 voices). Each voice has a subject
    from one chorale line; all four lines sound together at the summit, the
    trick that ends Bach's Canonic Variations BWV 769.
30. **[built] Pair XVI: Reincken's Hamburg chorale fantasia** (5 voices, organ
    in spirit). Each chorale line in canon between two pedal voices.
31. **[built] Pair XVII: fuggendo la cadenza** (5 voices). Every cadence
    evaded; the fifth voice, the father, arrives late and resolves the
    children's hanging dominant seventh.
    **[built] Pair XVIII: Vigilate** (5 voices). The four night watches of
    Mark 13:35, the subject brightening one note per watch until the dawn
    reaches the tonic major (written as A-flat); the knock at the door
    (BWV 61) as second subject.
32. **[built] Pair XIX: a suite in one fugue** (4 voices). Four dancers
    (sarabande, allemande, gigue, courante) on one pitch succession; at the
    ball all four dance at once, each in its own metre.
33. **[built] Pair XX: the solo violin multiplied** (21 parts). A fugue that
    begins as one line (after BWV 1003), whose implied voices split off into
    real ones until twenty-one sound, then fold back into one line.
34. **[built] Pair XXI: the posthorn capriccio** (22 parts). After BWV 992;
    twenty-two voices for the first twenty-two partials of B-flat, ending on
    the posthorn's own harmonic series in just intonation.
35. **[built] Pair XXII: Ma fin est mon commencement** (6 voices). A tombeau
    for Bach as a crab fugue: the second half is the first half backwards in
    every voice, ending on the lone note it began with.
36. **[built] Pair XXIII: ut re mi fa sol la per tutti i tuoni** (5 voices).
    After John Bull's hexachord fantasia, a cantus carries the hexachord
    through all twelve keys around a four-voice fugue; one passage is built to
    break in meantone, to show why the Well-Tempered Clavier was needed.
37. **[built] Prelude XXIV: per i 24 tuoni.** A walking-bass trio
    through all 24 keys in the WTC order, two bars each (48 bars), quoting the
    head of Bach's Book I fugue in each key, landing in B minor for the last
    fugue.
