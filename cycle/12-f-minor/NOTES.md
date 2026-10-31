# Fugue XII in F minor: *Fuga a 4 soggetti, compiuta* (five voices)

## Concept at the new size

The last fugue of *The Art of Fugue* (BWV 1080, the unfinished Contrapunctus XIX) breaks off just after
B-A-C-H has been combined with the first two subjects. Gustav Nottebohm (1880) showed that the three
subjects also combine with the main theme of the whole work, so Bach planned a quadruple fugue, in four
voices. This fugue writes that plan out in F minor (Bach's D minor up a minor third) in Bach's four voices,
and adds one: a **fifth voice, the Quinta vox, silent for fifty bars**, which enters only for the final
combination and sings the main theme in augmentation in the bass. It is the voice Bach never got to
write.

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
tonic pedal of the close (b59-66). No subject heads or fragments are labelled as entries.

## Section map (bar, time in the Bach-Lehman render)

| bars | time | section | what happens |
|---|---|---|---|
| 1-13 | 0:00 | **I. S1, stile antico** | tenor b1.3 (alone two bars), alto (tonal answer) b3.3, bass b6.3, soprano (answer) b8.3: entries 2, 3, 2 bars apart, the closest S1 and its answer allow; half cadence on V (b13) |
| 13-26 | 0:40 | **II. S2 alone, then with S1** | S2 alone in the tenor b13.2 (two bars, nothing else sounding); soprano answer in c b15.2 (a two-voice duet for four bars); alto S2 b19.2 with S1 in the bass b20.3, five beats later (Bach's own distance): i - v - VI - iv - V7 - i; cadence in b-flat (b26.1) |
| 26-38 | 1:22 | **III. B-A-C-H, then Bach's triple combination** | B-A-C-H alone in the tenor b26.3 (two bars, as at XIX b193), soprano answer b28.3; Bach's triple combination (XIX b233-239) in c minor, three voices: alto S2 b32.2, bass S1 b33.3, tenor S3 b34.3; cadence in c (b38.1) |
| 38-41 | 2:02 | episode | three voices down the circle of fifths, c - f7 - b♭ - E♭7 - A♭ - D♭maj7 - C7: the alto turns S2's head on each chord, the tenor makes a chain of sevenths against the bass; a beat of silence |
| 42-49 | 2:16 | **IV. The quadruple combination, four voices** | the main theme's first appearance, soprano b42.1, alone for a beat; S2 alto b42.2; S1 bass b43.3; S3 tenor b44.3: all four subjects at once b44.3-46.3, each in its own register (main theme E5-C6, S2 C4-D♭5, S3 C4-F4, S1 F2-C3); the soprano then falls silent; i (b48) - iv6 - V7, and the music stops on the dominant seventh (b49), where Bach's manuscript stops; two beats of silence |
| 50-63 | 2:46 | **V. The fifth voice** | the alto sings the main theme alone (b50.1); a bar later the Quinta vox enters beneath it with the main theme in augmentation (b51.1, F2, nine bars): a canon per augmentationem; tenor and bass join quietly; the soprano returns with the main theme (b57.1), S2 tenor b57.2, S1 bass b58.3, B-A-C-H alto b59.3, while the augmentation closes (G A♭ B♭ A♭ G F) and its F becomes the tonic pedal: **five voices, b59.3-61.3, every one singing a subject** |
| 63-66 | 3:34 | **Coda** | over the pedal the soprano signs the name at its own pitch, B♭ A C B (V7 - V7/iv - iiø4/3 - vii°7/V), the B rises to C, and the bass's A♮ is the Picardy third |

Key plan: f - (c) - f - b♭ │ b♭/f - c - circle of fifths to V │ f │ f with tonic pedal - F.

## The device and where to hear it

- **Each subject alone first.** S1 (b1), S2 (b13) and B-A-C-H (b26) each begin with a solo statement, as
  Bach's do. The main theme first sounds at b42.1 alone on top for one beat.
- **Bach's combinations.** S2 with S1 at b19-25; the triple combination at b32-38 (c minor).
- **Nottebohm's quadruple combination**, four voices, b42-48; all four at once from b44.3. The
  alignment (main theme, S2 a beat later, S1 five beats after S2, B-A-C-H four beats after S1) is the one
  my placement test found best by far; I do not claim it is Nottebohm's printed alignment.
- **The fifth voice** enters at b51.1 on F2, alone beneath the alto's main theme, which it imitates a bar
  later in notes twice as long, so the augmentation is recognisable as the theme just heard. Over its last five notes and its held F, the quadruple combination returns with S2 and
  B-A-C-H exchanged (B-A-C-H now above S2, S1 an octave higher), the way Bach restates combinations in
  invertible counterpoint.
- **Audibility.** Every entry follows a rest in that voice and lies in its own register; subject entries
  get +7 velocity over the free voices; the Quinta vox has a higher base velocity (it sits at E2-C3).

## Critic numbers (`tools/critic.py`, final build)

| measure | result | target |
|---|---|---|
| parallels_error | 0 | 0 |
| parallels (weak) | 0 | |
| beat_parallels | 1 | ≤ 2 |
| unresolved dissonances | 0 | ≤ 3 |
| bad_doublings | 0 | ≤ 2 |
| low_register_seconds | 1 | ≤ 9 |
| stepwise_pct | 75.9 % | ≥ 65 % |
| leap_4th_plus_pct | 12.1 % | |
| crossings | 1 | few |
| keyboard_unplayable_pct | 10.0 % | < 15 % for 5 voices |
| mean moving voices | 3.05 | |
| pc tripled on beats | 3.7 % | |

Mean moving voices per section: I 2.83, II 2.92, III 2.58, episode 3.0, IV 3.25, V 3.54, coda 3.5. Five
voices move together only in b57 and b59; the full texture is saved for V.

- **The beat-to-beat parallel** (b54.1, alto/Quinta vox, octaves A♭ → F) is inside the canon: the
  augmentation moves A♭-F a bar after the main theme does, and the main theme's passing B♭ A♭ G lies
  between. It is the price of the one-bar canon.
- **The low-register seventh** (b58.4) is S1's F3 against the augmentation's passing G2.
- **The crossing** (b32.2) is the alto's S2 entry (E♭5) one beat before the soprano's answer ends (C5).
- **Keyboard.** 33 of 331 onsets exceed two hands. Most lie in b59-66 over the held F2: with that pedal
  caught by the sostenuto pedal (or played on an organ pedalboard) the passage fits two hands. The rest
  are in IV, where Bach's own spacing puts S1 in the low bass (F2-C3) under three upper subjects.

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

- **The quadruple combination is heard twice in F minor** (IV and V) with the same alignment. V changes
  the voicing (S2 and B-A-C-H exchanged), adds the fifth voice and ends over a tonic pedal, but the
  harmonic progression above the bass is the same. I kept it because the point of V is to let the
  listener hear what the fifth voice changes; a listener may still hear it as a repeat.
- **The five-subject moment is short.** The augmentation's own notes end at b60.1; from there its held F
  is a pedal. All five voices sing subjects for two bars (b59.3-61.3), four subjects at once for two bars
  in IV (b44.3-46.3).
- **In V, B-A-C-H's second note (C5) meets S2's C5 in unison** at b60.1 for one beat, a side effect of the
  exchanged voicing.
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
  the stretto finale and the 23 search-proposed subject *heads* are gone; every entry is now a complete
  subject (23 in all). The S1 augmentation finale is replaced by the main theme in augmentation, in a new
  fifth voice held back until b51. The triple combination moved to c minor so the quadruple arrives in
  the tonic; a sequential episode and a stop on the dominant seventh (b49) were added; all free voices
  were rewritten, with rests before every entry.
- **Why:** at thirteen voices, the combinations were complete on paper and lost in the texture (10
  lines at once, many of them fragments). At five, each subject has its own register and is heard alone
  first, the quadruple combination is a four-voice texture a listener can follow, and the extra voice has
  a single, audible job.
