# Pair XII in F minor

The prelude (a short chorale on the name) is described at the end. The fugue comes first here.

# Fugue XII in F minor: *Fuga a 4 soggetti, compiuta* (five voices)

## Concept at the new size

The last fugue of *The Art of Fugue* (BWV 1080, the unfinished Contrapunctus XIX) breaks off just after
B-A-C-H has been combined with the first two subjects. Gustav Nottebohm (1880) showed that the three
subjects also combine with the main theme of the whole work, and inferred that Bach planned a quadruple
fugue in four voices. The inference is widely shared, but it is an inference: the combination proves that
the four subjects fit together, not that Bach meant to end the fugue with them, nor how he would have
done it. This fugue is one conjectural completion along those lines, in F minor (Bach's D minor up a
minor third), in Bach's four voices, plus one of my own: a **fifth voice, the Quinta vox, silent for
fifty bars**, which enters only for the final combination and sings the main theme in augmentation in
the bass. Nothing in Bach's sources calls for it; it is this work's addition, not a reconstruction.

Bach's WTC I fugue in F minor (BWV 857) has four voices, so this one has five (Bach + 1). Four voices
carry the four subjects; the fifth is the trick.

66 bars in 4/4, *Grave e sostenuto*, about 3:52 (crotchet 72; 76 for the running subject; 64-66 for IV and
V; the coda broadens to 44).

Files: `fugue.py` (source; every note written there), `fugue.json` (built score), `renders/`:
`fugue.pdf`, `.ly`, `.musicxml`, `.mid`; `fugue.mp3` (piano, Bach-Lehman); `fugue-equal.mp3` (piano,
equal temperament); `fugue-spatial.mp3` (binaural, arc layout, General MIDI 19 church organ, because
the organ holds the long notes of S1 and of the augmentation that a piano lets decay, and the Art of
Fugue completions are traditionally heard on the organ; the fifth voice sits in the centre of the arc).

## Material

Bach's subjects, copied exactly and transposed up a minor third. I re-read them from the MIDI files of
Contrapunctus I and XIX in the session scratchpad and they match the strings verified for the earlier
version (sixteenth units):

| | source (D minor) | F minor |
|---|---|---|
| S1, stile antico | XIX b1.3-6.3, bass: D A G F G A D (8 12 4 16 16 16 8) | F C B♭ A♭ B♭ C F |
| S1, Bach's tonal answer | XIX b6.3-11.3, tenor: A D D C D E A | C F F E♭ F G C |
| S2, running (quavers) | XIX b114.2-120.1, alto, 41 notes | A♭ B♭ A♭ G F E │ F C F G A♭ G F A♭ │ ... A♭ |
| S3, B-A-C-H | XIX b193.3-197.3, tenor: B♭ A C B C♯ D C♯ B C♯ D | D♭ C E♭ D E F E D E F |
| MT, main theme | Contrapunctus I b1-5, alto: D A F D C♯ D E F G F E D | F C A♭ F E F G A♭ B♭ A♭ G F |

B-A-C-H appears in the body in its transposed form D♭ C E♭ D (same intervals as Bach's B♭ A C B, so every
combination carries over exactly); the literal name B♭ A C B is signed once, in the coda.

**Verification.** A scratch check compares every one of the 23 labelled entries in `fugue.json` with the
tokens placed in `fugue.py`, and the tokens with Bach's subjects (intervals and rhythm, at ×1 or ×2). All
23 are complete, exact statements. The single change: the augmentation's last note (F) is held on as the
tonic pedal of the close and re-struck at b61.1, b63.1 and b66.1 (a piano's F2 dies away; see Review). No subject heads or fragments are labelled as entries.

## Section map (bar, time in the Bach-Lehman render)

| bars | time | section | what happens |
|---|---|---|---|
| 1-13 | 0:00 | **I. S1, stile antico** | tenor b1.3 (alone two bars), alto (tonal answer) b3.3, bass b6.3, soprano (answer) b8.3: entries 2, 3, 2 bars apart, the closest S1 and its answer allow; half cadence on V (b13) |
| 13-26 | 0:40 | **II. S2 alone, then with S1** | S2 alone in the tenor b13.2 (two bars; nothing else sounds once the soprano's answer ends, b13.3); soprano answer in c b15.2 (a two-voice duet for four bars); alto S2 b19.2 with S1 in the bass b20.3, five beats later (Bach's own distance): i - v - VI - iv - V7 - i; cadence in b-flat (b26.1) |
| 26-38 | 1:22 | **III. B-A-C-H, then Bach's triple combination** | B-A-C-H alone in the tenor b26.3 (two bars, as at XIX b193), soprano answer b28.3; Bach's triple combination (XIX b233-239) in c minor, three voices: alto S2 b32.2, bass S1 b33.3, tenor S3 b34.3; cadence in c (b38.1) |
| 38-41 | 2:02 | episode | three voices down the circle of fifths, c - f7 - b♭ - E♭7 - A♭ - D♭maj7 - C7: the alto turns S2's head on each chord, the tenor makes a chain of sevenths against the bass; a beat of silence |
| 42-49 | 2:16 | **IV. The quadruple combination, four voices** | the main theme's first appearance, soprano b42.1, alone for a beat; S2 alto b42.2; S1 bass b43.3; S3 tenor b44.3: all four subjects at once b44.3-46.3, each in its own register (main theme E5-C6, S2 C4-D♭5, S3 C4-F4, S1 F2-C3); the soprano then falls silent; i (b48) - iv6 - V7, and the music breaks off on a dominant seventh (b49), as Bach's manuscript breaks off; two beats of silence |
| 50-63 | 2:46 | **V. The fifth voice** | the alto sings the main theme alone (b50.1); a bar later the Quinta vox enters beneath it with the main theme in augmentation (b51.1, F2, nine bars): a canon per augmentationem; tenor and bass join quietly; the quadruple combination returns with its voices exchanged: the main theme in the bass voice (b57.1, E3-C4, in canon with its own augmentation directly below), the soprano's return with S2 an octave higher on top (b57.2), S1 in the tenor b58.3 (F4-C5), B-A-C-H alto b59.3, while the augmentation closes (A♭ B♭ A♭ G F, its last note at b59.1) and its F becomes the tonic pedal, re-struck at b61.1 and b63.1: **four subjects in motion at once over the pedal, b59.3-61.3**; S2's last A♭ steps up into the coda |
| 63-66 | 3:34 | **Coda** | over the pedal the soprano signs the name at its own pitch, B♭ A C B (V7 - V7/iv - iiø4/3 - vii°7/V), the B rises to C, and the bass's A♮ is the Picardy third |

Key plan: f - (c) - f - b♭ │ b♭/f - c - circle of fifths to V │ f │ f with tonic pedal - F.

## The device and where to hear it

- **Each subject alone first.** S1 (b1), S2 (b13) and B-A-C-H (b26) each begin with a solo statement, as
  Bach's do. The main theme first sounds at b42.1 alone on top for one beat.
- **Bach's combinations.** S2 with S1 at b19-25; the triple combination at b32-38 (c minor).
- **Nottebohm's quadruple combination**, four voices, b42-48; all four at once b44.3-46.3. The
  alignment (main theme, S2 a beat later, S1 five beats after S2, B-A-C-H four beats after S1) is the one
  my placement test found best by far; I do not claim it is Nottebohm's printed alignment.
- **The fifth voice** enters at b51.1 on F2, alone beneath the alto's main theme, which it imitates a bar
  later in notes twice as long, so the augmentation is recognisable as the theme just heard. Over its last five notes and its held F, the quadruple combination returns in a new order,
  the way Bach restates combinations in invertible counterpoint: from the top S2 (A♭5-D♭6), B-A-C-H
  (C5-F5), S1 (tenor, F4-C5), the main theme (bass voice, E3-C4, directly over its own augmentation), the
  augmentation. IV read main theme / S2 / B-A-C-H / S1, so the main theme goes from the top of the
  texture to the bottom of the four subjects.
- **How many subjects at once, exactly.** Five voices sound from b59.3, but they are not five active
  themes. The augmentation makes its last move (G2 to F2) at b59.1, two beats before B-A-C-H enters; its
  last note's written value ends at b60.1, and from then on it is a pedal. So all five statements overlap
  only for those two beats (b59.3-60.1), and then only as a held F under four moving subjects. What a
  listener can follow is four subjects in motion together over the pedal (main theme, S2, S1, B-A-C-H),
  b59.3-61.3, as in IV (b44.3-46.3); the fifth voice's contribution is the canon per augmentationem that
  leads into it (b51-59) and the bass that carries it.
- **Audibility.** Every entry follows a rest in that voice and lies in its own register; subject entries
  get +7 velocity over the free voices; the Quinta vox has a higher base velocity (it sits at E2-C3); in
  the triple combination (b34.3-38.1) the tenor's B-A-C-H gets +6 more and the bass -3, so the two slow
  low lines do not fuse.

## Critic numbers (`tools/critic.py`; critic, 4 Nov 2026)

| measure | result | target |
|---|---|---|
| parallels_error | 0 | 0 |
| parallels (weak) | 0 | |
| beat_parallels | 1 | ≤ 2 |
| unresolved dissonances | 0 | ≤ 3 |
| unverified stepwise continuations | 6 | check by ear |
| bad_doublings | 0 | ≤ 2 |
| low_register_seconds | 2 | ≤ 9 |
| stepwise_pct | 75.7 % | ≥ 65 % |
| leap_4th_plus_pct | 11.6 % | |
| crossings | 1 | few |
| keyboard_unplayable_pct | 4.5 % | < 15 % for 5 voices |
| reach_errors (fresh attacks no two hands can strike) | 0 | 0 |
| mean moving voices | 3.09 | |
| pc tripled on beats | 3.7 % | |

Mean moving voices per section: I 2.83, II 2.92, III 2.58, episode 3.0, IV 3.25, V 3.62, coda 4.0. Five
voices move together only in b57, 59, 61 and 63; the full texture is saved for V.

- **The beat-to-beat parallel** (b54.1, alto/Quinta vox, octaves A♭ → F) is inside the canon: the
  augmentation moves A♭-F a bar after the main theme does, and the main theme's passing B♭ A♭ G lies
  between. It is the price of the one-bar canon.
- **The low-register sevenths** (b58.4, b59.1) are the main theme's F3 against the augmentation's passing
  G2, and its leading tone E3 struck with the augmentation's arrival on F2, rising to F3 two beats later:
  the leading tone over the tonic pedal (an octave lower than before the Nov 2026 exchange, see below).
- **The crossing** (b32.2) is the alto's S2 entry (E♭5) one beat before the soprano's answer ends (C5).
- **Keyboard.** Every fresh attack can be struck by two hands (reach_errors 0). 15 of 333 onsets have
  more *sounding* notes than two hands can hold: in IV, where Bach's own spacing puts S1 in the low bass
  (F2-C3) under three upper subjects, and in b59-66, where the F2 pedal is held. Those held notes need the
  sostenuto pedal, caught at a re-strike. A pedal only catches what the hands could strike, so each
  re-strike of F2 now falls where the other fresh notes lie within reach (b61.1 with F3 in the left hand,
  b63.1 with A♭3, b66.1 with A3); see the review response below.

## Method and disclosure

Every note is written by hand in `fugue.py`: subject statements as the quoted strings or explicit
transforms (`transpose`, `scale_rhythm`), everything else as literal bar strings. **Scripted placement**:
a scratch script of mine ranked placements of *whole subject statements* (form, octave, start) against
one another with a pairwise counterpoint score and `tools/critic.py`. It was used for (1) the main theme
over Bach's triple combination (it confirmed the main-theme-one-beat-before-S2 alignment), (2) where the
augmentation can lie under the quadruple combination (it proposed the quadruple starting six bars after
the augmentation, so that the augmentation's close and its last note carry it), (3) the canon distance
between the main theme and its augmentation (one bar), and (4) the stretto distances of S1 and S2 with
their answers. I chose among the options and placed each statement by hand; the script wrote no notes,
and all free counterpoint was written and corrected by hand against the critic.

## Honest weak spots

- **The quadruple combination is heard twice in F minor** (IV and V) with the same alignment, so the
  pitch classes above the bass are the same beat by beat. V now reorders the voices (S2 on top, the main
  theme in the bass voice, directly over its own augmentation) and adds the fifth voice and the pedal, so
  the lines a listener follows differ; the harmony does not.
- **The main theme is not on top at the climax.** In V it sings in the bass voice (E3-C4), under S1 and
  B-A-C-H and directly over its own augmentation; it was on top in IV and in the canon's alto just before.
- **There is no real five-subject moment.** The augmentation's written notes end at b60.1 and its last
  move comes before B-A-C-H enters; from there its F is a pedal. Four subjects move at once for two bars
  in V (b59.3-61.3) over that pedal, as for two bars in IV (b44.3-46.3).
- **Bars 3-6 are two long-note voices** (stile antico subject against its answer). Static by design, as
  at the start of XIX, but slow.
- **Only one episode** (b38-41). The form is mostly entries and cadences, closer to XIX than to a WTC
  fugue.
- **The S2 duet (b15-19) is two running voices only**, four bars without a bass.
- **Nothing has been heard.** I cannot listen; nothing here says how it sounds.

## From the N+1 version

- **Kept:** the concept and title; the four verified subject strings and Bach's tonal answer; the S1
  exposition (tenor, alto, bass, soprano at 2-3-2 bars); S2 entering as a duet with its answer; Bach's
  triple combination; the main-theme-first quadruple alignment; the coda's literal B-A-C-H signature over
  the pedal with the Picardy A.
- **Changed:** thirteen voices became five, 88 bars became 66 (5:11 to about 3:52). The mirror section,
  the stretto finale and the 23 labelled subject *heads* (most of them proposed by a search) are gone; every entry is now a complete
  subject (23 in all). The S1 augmentation finale is replaced by the main theme in augmentation, in a new
  fifth voice held back until b51. The triple combination moved to c minor so the quadruple arrives in
  the tonic; a sequential episode and a stop on the dominant seventh (b49) were added; all free voices
  were rewritten, with rests before every entry.
- **Why:** at thirteen voices, the combinations were complete on paper and lost in the texture (10
  lines at once, many of them fragments). At five, each subject has its own register and is heard alone
  first, the quadruple combination is a four-voice texture a listener can follow, and the extra voice has
  a single, audible job.

# Prelude XII in F minor: *The name, three times*

A short chorale prelude for one pianist, in three voices: a new chorale-like melody in the soprano
(crotchets), a slow inner voice, and a bass that walks in quavers and becomes a pulsing tonic pedal, after
the manner of an Orgelbüchlein chorale (Bach's *Ich ruf zu dir*, BWV 639, is also in F minor; nothing of it
is quoted). The first edition of *The Art of Fugue* (1751) followed the unfinished fugue with a chorale;
here the chorale comes first. 16 bars in 4/4, *Andante, come un corale*, crotchet = 63 (58 for the name
in the bass), about 1:05 in the render: a walking chorale before a Grave fugue.

**Material.** The melody is made of two crosses, each resolving to C:
- **C D♭ C B**, the first four notes of the subject of Bach's WTC I fugue in F minor (BWV 857; checked
  against `cycle/reference/bach-subjects.md`), the Book I fugue in this key (b1, again over the tonic pedal
  in b13);
- **B♭ A C B**, the name at its own pitch, sung three times: by the soprano (b2-3), by the bass in half
  notes while the texture thins (b9-10, marked +10 velocity), and by the soprano again over the tonic pedal
  (b14).

The fugue then uses the name only in its transposed form until its own coda, where the soprano signs
B♭ A C B once more over the fifth voice's pedal, so the pair begins and ends with the signature.

**Plan.** b1-4: the cross and the name (i - iv - V - vii°7/V - V - V7 - V7/iv - VI7 - vii°6/5 - V), cadence
in f (b5); b5-8: an ascent through A♭ major to a half cadence (b8); b9-12: the name in the bass
(iv - V6/iv - V7(♭9) - vii°7/V - V), cadence (b12-13); b13-16: tonic pedal, the cross and the name again,
last cadence on a plain F-minor chord (the Picardy third is kept for the end of the fugue).

**Critic numbers** (`tools/critic.py prelude.json`): parallels 0 (errors and weak), beat-to-beat
parallels 0, unresolved dissonances 0, bad doublings 0, low-register seconds 0, keyboard unplayable 0 %,
tertian fit 75 %. Stepwise motion is only 42.7 % and repeated notes 10.6 %, because the bass is a walking
quaver bass and then a repeated-note pedal; the melody moves mostly by step and third.

**Weak spots.** Two melodic tritones (soprano D5-A♭4 inside the diminished seventh, b10; bass D3-A♭2,
b3); the inner voice is plain, mostly held notes; the piece is short and does one thing. Nothing has
been heard.

**Renders.** `renders/prelude.pdf`, `.ly`, `.musicxml`, `.mid`; `prelude.mp3` (Bach-Lehman),
`prelude-equal.mp3` (equal temperament). No binaural render for the prelude.

# Review (response to `REVIEW.md`)

| # | Item | What changed |
|---|---|---|
| 1 | The Quinta vox's held F2 has died away by the coda, so the last chord is heard over A3 | Agreed. The pedal is re-struck. At first this was `F2:32 F2:40 F2:40 F2:12`, at b59.1 (the augmentation's last note), b61.1 (as the subjects end), b63.3 (the coda's signature) and b66.1 (the Picardy chord): the reviewer's tested `F2:72 F2:40 F2:12` plus the optional strike at b61.1. Since the Nov 2026 response (below) the re-strikes are at b61.1, b63.1 and b66.1, so that every one can be struck with the notes that begin with it. |
| 2 | V repeats IV's top two lines at the same pitch; B-A-C-H and S2 meet on C5 at b60.1 | Agreed, with the reviewer's tested exchange: S2 on top an octave higher (the soprano's return, b57.2), the main theme below it (b57.1; first in the tenor, and since the Nov 2026 response in the bass voice, an octave lower). The tenor's free close (B♭4 A♭4 C5 C5) and the alto's link (D♭5 C5, b56.3-57.1) were rewritten by hand for it. The unison becomes an octave, and S2's last A♭5 steps into the coda's B♭5. The cost (the main theme is no longer on top at the climax) is listed under weak spots. |
| 3 | B-A-C-H in the triple combination (b34.3-38.1) sits too close above S1 and too quietly | Agreed; voicing only, as proposed: the tenor gets +6 and the bass -3 velocity there. The notes are unchanged. An octave shift would collide with the alto's run. |
| 4 | The pair is slow | Agreed for the prelude: crotchet 54 → 63, tempo map scaled (about 1:05 instead of 1:17). The fugue's tempi are unchanged, as the reviewer advised. |
| 5 | b55 is a whole bar of held diminished seventh | Applied the tested `Db4:8 Bb3:8` in the tenor. The critic adds one *note*, not an error: the D♭ leaves by leap, within the chord. |
| — | Must not be touched | Left as written: the break-off and the fifth voice's entry (b48-51), the solo expositions (b1-41), and the prelude's name in the bass (b9-10). |

The critic after the changes: parallels 0 errors and 0 weak, beat-to-beat 1 (the canon at b54.1, as
before), unresolved 0, bad doublings 0, low-register 1, crossings 1. Repeated notes rise from 1.2 % to
2.0 % (the re-struck pedal), and keyboard_unplayable from 10.0 % to 10.5 %. All 23 entries are still
exact. All renders were redone: the fugue in Bach-Lehman (full), in equal temperament (audio only) and
binaural (organ, arc); the prelude in Bach-Lehman and equal temperament.

# Review response (Nov 2026)

1 November 2026. The owner's review of PR #1 and the corrected critic (which now checks whether two hands
can strike every fresh attack) found three attacks out of reach: b11.1 (F2 A♭3 C4 F5, 17 semitones in one
hand), b59.1 (F2 C4 E4 G5, 19) and b63.3 (F2 C4 G4 E5 B♭5, 19). The review was right that the old note
here, which said a sostenuto pedal caught at each bass re-strike made b59-66 fit two hands, overlooked the
re-strike itself: the pedal holds a note only after the hand has struck it together with everything else
that begins at that instant.

- **b10-11.** The alto's E♭4 is now tied over the bar as a 7-6 suspension over the bass's final F of S1,
  falling to D♭4 on beat 2 and to C4 on beat 3 (`C4:8 Eb4:8~ | Eb4:4 Db4:4 C4:8`). The fresh C4 on the
  downbeat, between the bass's F2 and the soprano's F5, was the only note neither hand could reach.
- **b56-63.** The main theme and S1 exchange voices and octaves in the five-voice combination: the main
  theme now sings in the bass voice an octave lower (E3-C4, b57.1), directly over its own augmentation,
  and S1 in the tenor an octave higher (F4-C5, b58.3). With S1 at F3-C4, its C4 at b59.1 lay between the
  fifth voice's F2 and the soprano's G5, out of reach; no free voice was involved, so a subject had to
  move as a whole. All subjects are complete and exact; the alignment (main theme, S2 a beat later, S1,
  B-A-C-H) is unchanged, and wherever S1 and the main theme were an octave apart the chords are the same.
  The tenor and bass exchange their link (b56.3-57.1) and their tails (the bass now B♭3 A♭3 C4 A♭3 after
  the main theme, b61.3-63.1, under S1's own close). Cost: the main theme moves from the middle of the
  texture to the bottom of the four subjects, and its leading tone E3 meets the pedal's F2 at b59.1 (a
  second low-register seventh; it rises to F3 two beats later).
- **The pedal re-strikes** are now at b61.1, b63.1 and b66.1 (`F2:32 F2:32 F2:48 F2:12`). b63.1 is S1's
  last note and the tonic arrival, and its other fresh notes (A♭3 | F4 F5 A♭5) fit the hands; the coda's
  first chord (b63.3, C4 G4 E5 B♭5) is then struck over a pedal already caught. Nothing in the coda's notes
  changed.
- **Prose.** The section map, the device notes and the weak spots no longer say "five voices, every one
  singing a subject": the augmentation's last move comes before B-A-C-H enters, so the passage is four
  subjects in motion over a pedal, with five statements overlapping on paper for two beats only. The
  concept paragraph now presents the completion as this work's conjecture, following Nottebohm's
  inference, and the fifth voice as an addition of mine rather than "the voice Bach never got to write".

Critic before → after: reach_errors 3 → 0; keyboard_unplayable_pct 10.5 → 4.5; unresolved 0 → 0;
unverified 6 → 6 (the same places, b58.4's partner is now the bass voice); parallels 0 errors, beat-to-beat
1 (unchanged); low-register seconds/sevenths 1 → 2 (b59.1, above); crossings 1.

# Self-critique pass (Nov 2026)

No notes were changed.
- **Removed** the stale "Renders not yet redone" from the review response: the renders were redone after it.
- **Fixed: where the main theme sings in V.** The first weak spot put it "in the tenor", the next ones "in the bass voice". The score has it in the Bass voice at b57.1 (E3–C4), directly over its own augmentation. That has been the case since the Nov 2026 response; the tenor placement came first, from REVIEW item 2. The weak spot, the review table (items 1 and 2: the re-strike bars and the theme's voice) and the comment in `fugue.py` now agree with the score. The rebuilt `fugue.json` is identical.
- **Listening guide (proposed in the report).** It said "b56–63" for the brief four-subject passage. Four subjects move together over the pedal only in b59.3–61.3.
- **Refreshed: the critic table** (critic, 4 Nov 2026). The numbers are unchanged.
