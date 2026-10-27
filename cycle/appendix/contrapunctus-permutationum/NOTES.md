# Appendix — Contrapunctus permutationum

Keyboard, four independent voices (one staff each). 4/4, Allegro moderato,
quarter = 80. 74 bars, about 3 min 42 s of written music (3 min 45 s rendered
with the release tail).

Four hand-written lines in quadruple invertible counterpoint at the octave.
The piece states them 24 times, each time in a different vertical ordering
and a different key, so it uses all 24 permutations of four lines and all 24
keys of the cycle. The orderings follow a change-ringing method, the keys the
circle of fifths, and the extent "comes round" to its opening ordering for a
C-major coda. In the coda the B-A-C-H cantus is augmented, and its H, left
hanging at the end of every statement, finally resolves to C.

I cannot hear the renders. Everything below is from the score and the checks.
Nothing here claims how the piece sounds.

## The four lines (C major; every key is a literal transposition)

Written in `lines.py`, in sixteenth-unit tokens.

| line | character | rate | C major |
|---|---|---|---|
| **A** cantus | the motto B-A-C-H, chromatically exact | half notes | B♭4 A4 \| C5 B4 |
| **B** sigh | enters a beat late; syncopated half notes resolving down (7–6 / 2–3 against the cantus) | quarter + syncopated halves | r G4~ G4 F4 \| E4 A4~ A4 G4 |
| **C** walker | walking eighths; a bass line that also works as a tune | eighths | C3 D3 E3 C3 F3 G3 A3 G3 \| E3 G3 F♯3 D3 B2 D3 G2 B2 |
| **D** spinner | a rising scale "rocket", wavering descent, second rise, landing on a quarter | sixteenths, last beat a quarter | C5 D5 E5 F5 G5 B♭5 A5 G5 A5 G5 F5 E5 F5 E5 F5 D5 \| C5 D5 E5 G5 A5 G5 F♯5 G5 F5 E5 D5 F5 G5(q) |

Harmonic frame (major): I⁷ (the B♭ is the motto's B) | vii°/IV | IV | IV⁶ ‖ I⁶ | V⁷/V | V⁹ (rootless) | V.
Every statement therefore opens on a tonic coloured by its own flat seventh,
and closes on an open half cadence.

**The invertibility rule.** Every pair of lines is the bass/upper pair in some
ordering, so no two lines may form a perfect fifth or fourth at any
quarter-beat onset. A fifth would become a fourth over the bass. The beat
sonorities are therefore thirds and sixths with doublings, rootless or
fifthless sevenths, diminished triads, and, in minor, diminished sevenths.
Fifths and complete triads appear only on offbeats. The suspensions are
7–6 against 2–3: B's G over the cantus's A in bar 1, and B's A over the
cantus's B in bar 2. A 9–8 suspension would invert badly, so none is used.

**Minor (modal mapping, written out by hand in `lines.py`).** The cantus
stays exact: B♭ A C B in C minor is ♭7, ♮6, 1, ♮7, the melodic-minor upper
tetrachord. That makes bar 1's IV a major chord (Dorian colour) in every
minor statement. Three written adjustments were needed:

- In minor, the third (E♭) against the cantus's B♭ would be a perfect fifth
  on a beat. So the spinner starts from the tonic in both modes, and the
  minor third arrives on offbeats.
- In minor, the walker arpeggiates C–E♭–B♭–D in bar 1 instead of C–D–E–C.
- The sigh line's E♭→A♮ becomes an augmented fourth, stepping back down to
  G. A falling diminished fifth was tried, but it crossed the cantus and
  blurred the ordering.

## Proof: all 24 orderings × both modes

`prove.py` places the four lines in every top-to-bottom ordering by octave
transposition only. It runs `tools/critic.py`'s `analyse()` on each ordering
and adds two stricter checks: a 4th against the lowest note at any
quarter-beat onset, and a P4/P5 between any two lines at any quarter-beat
onset.

Columns: parallels_error · parallels_weak · accented (beat-to-beat)
parallels · unresolved dissonances · 4th against the bass on beats · 4th/5th
between any pair on beats · (critic "7th not resolved down" notes).

| ordering | major | minor | minor melody |
|---|---|---|---|
| ABCD | 0 · 0 · 0 · 0 · 0 · 0 · (2) | 0 · 0 · 0 · 0 · 0 · 0 · (1) | tritone leap 1 |
| ABDC | 0 · 0 · 0 · 0 · 0 · 0 · (0) | 0 · 0 · 0 · 0 · 0 · 0 · (0) | tritone leap 1 |
| ACBD | 0 · 0 · 0 · 0 · 0 · 0 · (2) | 0 · 0 · 0 · 0 · 0 · 0 · (1) | tritone leap 1 |
| ACDB | 0 · 0 · 0 · 0 · 0 · 0 · (2) | 0 · 0 · 0 · 0 · 0 · 0 · (1) | tritone leap 1 |
| ADBC | 0 · 0 · 0 · 0 · 0 · 0 · (0) | 0 · 0 · 0 · 0 · 0 · 0 · (0) | tritone leap 1 |
| ADCB | 0 · 0 · 0 · 0 · 0 · 0 · (2) | 0 · 0 · 0 · 0 · 0 · 0 · (1) | tritone leap 1 |
| BACD | 0 · 0 · 0 · 0 · 0 · 0 · (2) | 0 · 0 · 0 · 0 · 0 · 0 · (1) | tritone leap 1 |
| BADC | 0 · 0 · 0 · 0 · 0 · 0 · (0) | 0 · 0 · 0 · 0 · 0 · 0 · (0) | tritone leap 1 |
| BCAD | 0 · 0 · 0 · 0 · 0 · 0 · (2) | 0 · 0 · 0 · 0 · 0 · 0 · (1) | tritone leap 1 |
| BCDA | 0 · 0 · 0 · 0 · 0 · 0 · (1) | 0 · 0 · 0 · 0 · 0 · 0 · (0) | tritone leap 1 |
| BDAC | 0 · 0 · 0 · 0 · 0 · 0 · (0) | 0 · 0 · 0 · 0 · 0 · 0 · (0) | tritone leap 1 |
| BDCA | 0 · 0 · 0 · 0 · 0 · 0 · (1) | 0 · 0 · 0 · 0 · 0 · 0 · (0) | tritone leap 1 |
| CABD | 0 · 0 · 0 · 0 · 0 · 0 · (2) | 0 · 0 · 0 · 0 · 0 · 0 · (1) | tritone leap 1 |
| CADB | 0 · 0 · 0 · 0 · 0 · 0 · (2) | 0 · 0 · 0 · 0 · 0 · 0 · (1) | tritone leap 1 |
| CBAD | 0 · 0 · 0 · 0 · 0 · 0 · (2) | 0 · 0 · 0 · 0 · 0 · 0 · (1) | tritone leap 1 |
| CBDA | 0 · 0 · 0 · 0 · 0 · 0 · (1) | 0 · 0 · 0 · 0 · 0 · 0 · (0) | tritone leap 1 |
| CDAB | 0 · 0 · 0 · 0 · 0 · 0 · (2) | 0 · 0 · 0 · 0 · 0 · 0 · (1) | tritone leap 1 |
| CDBA | 0 · 0 · 0 · 0 · 0 · 0 · (1) | 0 · 0 · 0 · 0 · 0 · 0 · (0) | tritone leap 1 |
| DABC | 0 · 0 · 0 · 0 · 0 · 0 · (0) | 0 · 0 · 0 · 0 · 0 · 0 · (0) | tritone leap 1 |
| DACB | 0 · 0 · 0 · 0 · 0 · 0 · (2) | 0 · 0 · 0 · 0 · 0 · 0 · (1) | tritone leap 1 |
| DBAC | 0 · 0 · 0 · 0 · 0 · 0 · (0) | 0 · 0 · 0 · 0 · 0 · 0 · (0) | tritone leap 1 |
| DBCA | 0 · 0 · 0 · 0 · 0 · 0 · (1) | 0 · 0 · 0 · 0 · 0 · 0 · (0) | tritone leap 1 |
| DCAB | 0 · 0 · 0 · 0 · 0 · 0 · (2) | 0 · 0 · 0 · 0 · 0 · 0 · (1) | tritone leap 1 |
| DCBA | 0 · 0 · 0 · 0 · 0 · 0 · (1) | 0 · 0 · 0 · 0 · 0 · 0 · (0) | tritone leap 1 |

The bracketed "7th" notes are critic naming artifacts. The rootless C⁷
(E–G–B♭) and rootless D⁷ (F♯–A–C) are read as diminished sevenths built
on whichever member is lowest, so the critic expects the wrong note to fall.
The one melodic warning is the minor sigh line's E♭→A augmented fourth,
described above.

How the proof got there: `skeleton_search.py`, a pitch-class dynamic program,
mapped which fifth-free beat plans exist over the motto. The lines were then
written by hand and revised against `prove.py`. It rejected:

- an offbeat parallel octave (D's C5→B4 against the cantus) and an offbeat
  parallel fifth between C and D;
- the walker's C→F♯ tritone;
- in minor, the downbeat E♭ against B♭ (a fifth on beat 1);
- a swapped spinner figure that made accented octaves with the cantus.

## Keys, orderings, bars

Keys: the circle of fifths, each major followed by its relative minor:
C a G e D b A f♯ E c♯ B g♯ F♯ e♭ D♭ b♭ A♭ f E♭ c B♭ g F d → C.

Orderings: the 24 rows of **Plain Bob Minimus**, a traditional English
change-ringing method. Its place notation is x.14.x.14.x.14.x.12, rung three
times. Bells 1–4 are lines A D B C, and positions 1–4 run top to bottom.
Consecutive orderings differ only by swaps of adjacent staves, so each link
is literally a change. The treble (B-A-C-H) "hunts" steadily down and up
through the four staves, three times. Each line is the bass in exactly 6
statements and the top in exactly 6. Statement 9 rings ABCD, and statement
13 rings DCBA: B-A-C-H in the bass at the climax.

| # | key | ordering (top→bottom) | bars | joined by | role |
|---|---|---|---|---|---|
| 1 | C major | ADBC | 1–2 | — | rounds; motto on top, walking bass |
| 2 | A minor | DACB | 4–5 | link 3 | |
| 3 | G major | DCAB | 7–8 | link 6 | |
| 4 | E minor | CDBA | 10–11 | link 9 | motto first in the bass |
| 5 | D major | CBDA | 13–14 | link 12 | |
| 6 | B minor | BCAD | 16–17 | link 15 | |
| 7 | A major | BACD | 19–20 | link 18 | |
| 8 | F♯ minor | ABDC | 21–22 | elided (V→vi) | |
| 9 | E major | ABCD | 24–25 | link 23 | the "alphabetical" row; registral valley |
| 10 | C♯ minor | BADC | 27–28 | link 26 | |
| 11 | B major | BDAC | 30–31 | link 29 | crescendo begins |
| 12 | G♯ minor | DBCA | 32–33 | elided | widest register so far |
| 13 | **F♯ major** | **DCBA** | 36–37 | 2-bar link 34–35 | **climax**: farthest key, motto in the bass (E2), widest span |
| 14 | E♭ minor | CDAB | 38–39 | elided | sudden hush after the enharmonic turn |
| 15 | D♭ major | CADB | 41–42 | link 40 | |
| 16 | B♭ minor | ACBD | 43–44 | elided | |
| 17 | A♭ major | ACDB | 46–47 | link 45 | |
| 18 | F minor | CABD | 48–49 | elided | |
| 19 | E♭ major | CBAD | 51–52 | link 50 | |
| 20 | C minor | BCDA | 54–55 | link 53 | motto as a low pedal line (B♭1) |
| 21 | B♭ major | BDCA | 57–58 | link 56 | motto as a low pedal line (A♭1) |
| 22 | G minor | DBAC | 60–61 | link 59 | |
| 23 | F major | DABC | 63–64 | link 62 | |
| 24 | D minor | ADCB | 66–67 | link 65 | |
| coda | C major | ADBC (come round) | 69–74 | link 68 | summit: motto augmented, H→C |

Every statement is labelled in the score: a boxed mark with number, key and
ordering, and an italic label on the cantus entry (`subject_entries`).
`critic.py` verifies all 25 declared entries, the coda's at double length.

## Links (written bar by bar in `source.py`)

There are 19 links. Five joins are elided: statements 8, 12, 14, 16 and 18
enter directly as deceptive cadences, V of the major moving to i of the
relative minor. They were elided only where every staff could move smoothly.
Each link hands the roles over. A staff first continues the character of the
line it has just played (long notes, syncopes, eighths or sixteenths), then
turns towards the character of its next line. Harmony is cadential:

- after a major statement: I → V⁷ of the relative minor (L1 adds vi and iv⁶
  over a falling bass);
- after a minor statement: i, which is ii of the next major → V⁷ of that
  major.

Where a staff's last note is the 3rd of V and its next note is the motto's
flat seventh, it slides a semitone (G♯→G, B→B♭). This is the motto's own
chromaticism. Some links thin to three voices, so the next entry is fresh:
L2 tenor, L8 soprano, L14 alto. L12 is two bars. A C♯ pedal sits under a
sudden breath, then the spinner's rising head enters in stretto, alto then
soprano, into the climax.

## Arc

- Dynamics (velocity offsets): about mf at the opening; a dip to about mp
  through statements 6–9; a crescendo through 11–13 to ff at the climax;
  subito p at 14; a steady rebuild to 24; the coda at ff, relaxing for the
  last two bars.
- Register is planned per statement by octave choice only (`plan.py`, frozen
  in `OCTAVES`). The widest span is at 12–13, it narrows at 14, and widens
  again towards 23–24.
- **Coda (summit, bars 69–74):** B-A-C-H in whole notes in the soprano over
  I⁷ | IV–V⁷/V | V with the cantus C held as a whole-bar 4–3 (a cadential
  6/4 over a walking dominant pedal) | V⁷ | I. The H, unresolved in every
  statement, resolves to C. The alto then signs off with B-A-C-H in quarter
  notes over a tonic pedal, a plagal "signature", before the last chord.

## Borrowing and allusion (credited)

- **B-A-C-H** (B♭–A–C–B♮): J. S. Bach's name in German note-letters. He wrote
  it into the unfinished last fugue of *The Art of Fugue*, BWV 1080, and many
  later composers used it. Here it is the cantus in every key.
- The title imitates *The Art of Fugue*'s "Contrapunctus" headings.
- **Plain Bob Minimus**: a traditional English change-ringing method (17th
  century onwards). Only its permutation order is used.
- All other material (lines B, C, D, every link, the coda) is original.

## Scripted vs written

Written by hand: the four lines in both modes, all 19 links, and the coda.
Scripted: chromatic transposition of the C-major and C-minor lines to each key
(`wtclib.transpose`), and their octave placement per staff.
`plan.place()` proposed the placement as a search over octave shifts only.
The choices are frozen in `source.py` and two were edited by hand (the motto
dropped an octave in statements 20–21). No code chooses pitches.

Files:

- `lines.py`: the four lines;
- `prove.py`: the 24 × 2 proof;
- `skeleton_search.py`: proposal tool;
- `plan.py`: keys, orderings, placement search;
- `source.py`: the movement, builds `score.json`;
- `check.py` and `show.py`: per-link critic windows and a vertical display;
- `renders/`: `contrapunctus.pdf/.musicxml/.mid/.mp3` (Bach–Lehman
  temperament) and `contrapunctus-equal.*` (equal temperament).

## Whole-piece critic (`python3 tools/critic.py score.json`)

parallels_error 0, parallels_weak 0, beat_parallels 0, dissonance_unresolved 0,
crossings 0, longest static harmony 4 beats (the final bar). Explained notes:

- **12 tritone leaps:** the minor sigh line's E♭→A, once per minor statement.
- **2 seventh leaps,** both at elided joins:
  - bar 21, bass E3→F♯2 at the deceptive cadence into F♯ minor;
  - bar 38, soprano C♯6→D♯5, the fall from the climax into the hushed E♭
    minor (intended).
- **4ths against the bass on beats, coda only:** the cadential 6/4 in bar 71
  and the plagal pedal 6/4 in bar 73. They lie outside the invertible
  combination and are treated as normal tonal dissonances.
- **40 "7th not resolved down" notes:** mostly the naming artifacts above. A
  few are sevenths in link figuration that leap rather than step.
- **15 low-register seconds/ninths,** in statements 5, 9 and 20–22, where the
  half-note motto sits under a running line. Dropping the motto to B♭1/A♭1
  in 20–21 turned seconds into ninths, which is better but still dark.
- **Keyboard:** 20% of onsets exceed two hands. This is a four-staff
  realisation, not a pianist's reduction.

## Honest weak spots

- The same two-bar progression is heard 24 times. Variety comes from key,
  ordering, register, the links and dynamics. Whether that sustains 3¾
  minutes is a listening question I cannot answer.
- Fifth-free beats keep the statements' harmony lean: dyads and incomplete
  sevenths on beats, full chords only on offbeats. Each statement's downbeat
  is a bare tonic plus flat seventh. In minor the third cannot sound on beats
  1–2, and bar 1 is Dorian-tinged.
- The links share two harmonic templates. That keeps them clearly cadential,
  but the pattern may be audible.
- The coda's augmentation is of the cantus only. The other three lines
  continue in character but are newly written, because the combination
  cannot be laid literally over an augmented cantus.
- Balance is unverified: a decaying piano half note against sixteenths. The
  cantus gets the entry velocity boost.

Tool notes, for whoever maintains `tools/`. Nothing outside this folder was
edited.

- `critic.check_parallels` does not reset its previous-onset state across a
  silent stretch. While links were placeholder rests, it reported parallels
  "across" empty bars.
- `chord_candidates` prefers a diminished-seventh reading on the bass note
  for rootless dominant sevenths. That produces spurious "7th not resolved"
  notes.
