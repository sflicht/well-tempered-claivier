# Pair XX in A minor — Preludio per violino solo / Fuga per un violino solo, moltiplicata

Third edition. Fugue in **21 real voices** (9 violins, 5 violas, 5 cellos, 2 double basses); prelude in **one line**.

| file | what |
|---|---|
| `fugue.py` → `fugue.json` | the fugue, 67 bars, 4/4, ~4:11 with the tempo map |
| `prelude.py` → `prelude.json` | the prelude, 30 bars, 4/4, ~1:44 |
| `renders/fugue.pdf .ly .mid .musicxml .mp3` | score + strings audio (Bach–Lehman), each voice on its own GM string instrument |
| `renders/fugue-equal.mp3` | the same, equal temperament |
| `renders/fugue-spatial.mp3` | binaural, every voice at its own place (`--layout score`, positions below) |
| `renders/prelude.pdf … prelude.mp3`, `prelude-equal.mp3` | prelude, piano (the one-hand version), Bach–Lehman and equal |
| `renders/prelude-violin.mp3` | prelude played by the GM violin |

I cannot hear audio. Nothing below claims how anything sounds.

## Concept

Bach's fugue for unaccompanied violin (Sonata No. 2 in A minor, BWV 1003) is a single line that implies three or four voices by jumping between registers (compound melody) and with a few double stops. This fugue **starts as that kind of piece**. Then the voices the violin only implies come out one at a time as real instruments. Each new voice becomes a compound line in turn and splits again, until **21 real voices move at the summit** (bars 39–47). After that the process runs backwards. The voices **fold back** into the voices they came from, in the reverse order of the splits, until the solo violin is alone again (bar 58). Alone, it **implies the summit's harmony** with string-crossing chords, as the Chaconne of BWV 1004 implies its ground. The solo violin's A is the last sound.

### The splitting procedure (the same every time)

1. A voice plays sixteenths that alternate between two registers (two *strands*). The subject's own tail is such a line. Its upper strand is C E D C B A G#, and its lower strand is the chromatic lament A G# G F# F E. That lament is the countersubject of BWV 1003, there as G# G F# F E.
2. A **new voice enters on one strand's note, at the exact sixteenth** where the old voice would have played it, and carries that strand on alone. This is usually the lower strand at beat 2.25; four times it is the upper strand at beat 2.
3. The old voice stops leaping and keeps the other strand, in eighths.

Bars 13–15 are the exception. There the solo violin's four-string chord sweeps (bars 9–12) give up their **strings**. The cello takes the G-string strand at 13.1, the viola the D string at 14.1, and the second violin the A string at 15.1. The violin's sweep narrows from three strings, to two (bariolage), to one line.

**Folding is the split played backwards.** The parent's line turns compound for one beat: sixteenths that alternate its own note P with the child's note X. The child's last note ends at the sixteenth where the parent plays X, and the parent goes on alone. The last three folds mirror bars 13–15. The second violin (A string), viola I (D string) and cello I (G string) return into the solo violin as its sweep widens again: two strings in b56, three in b57, four in b58.

### Family tree (split → fold)

```
Vl I (solo, the whole piece)
├─ Vc I    split b13.1 (G-string strand) ............................. folds into Vl I  b58.1
│  ├─ Cb I    b17.2.25 (lament strand of Vc I's subject) ................ into Vc I  b55.2
│  │  ├─ Vc V    b38.2 (upper strand of Cb I's subject) ................. into Cb I  b50.3
│  │  └─ Cb II   b43.2 (lament strand of Cb I's subject x4; 21st voice) . meets Cb I b47.1
│  └─ Vc III  b32.2.25 .................................................. into Vc I  b49.3
├─ Va I    b14.1 (D-string strand) ...................................... into Vl I  b57.1
│  ├─ Vc II   b19.2.25 .................................................. into Va I  b54.3
│  │  └─ Vc IV   b30.2.25 ............................................... into Vc II b50.1
│  └─ Va III  b28.2.25 .................................................. into Va I  b51.3
│     └─ Va V    b36.2.25 ............................................... into Va III b48.1
├─ Vl II   b15.1 (A-string strand) ...................................... into Vl I  b56.1
│  ├─ Va II   b21.2.25 .................................................. into Vl II b54.1
│  │  └─ Va IV   b29.2.25 ............................................... into Va II b51.1
│  └─ Vl VI   b27.2 (upper strand) ...................................... into Vl II b52.1
│     └─ Vl IX   b37.2.25 ............................................... into Vl VI b47.3
├─ Vl III  b23.2 (upper strand) ......................................... into Vl I  b53.3
│  └─ Vl IV   b25.2 (upper) ............................................. into Vl III b53.1
│     └─ Vl VII  b34.2 (upper; the top of the texture from then on) ..... into Vl IV b49.1
├─ Vl V    b26.2.25 ..................................................... into Vl I  b52.3
└─ Vl VIII b35.2.25 ..................................................... into Vl I  b48.3
```

Count: 4 (b16) → 8 (b23) → 15 (b32) → 20 (b38) → 21 (b43.2) → 1 (b58).
The `# SPLIT n` comments in `fugue.py` mark every split, and the `FOLDS` table holds every fold (time, child, parent, X, P).

## Credits and sources

- **Subject head: J. S. Bach**, Fuga of the Sonata No. 2 in A minor for solo violin, BWV 1003, bars 1–3: e'' dis'' e'' e' a' c'' h' d'' | c''. The answer is Bach's tonal answer, bars 3–5: a' gis' a' a | e' g' fis' a' | gis'. Bach's music is public domain.
- **Verification:** the notes were checked against the Mutopia Project edition of BWV 1003 Fuga (Mutopia-2008/06/15-1455). That edition is typeset by Hajo Dezelski from the Bach-Gesellschaft edition (1879, Band 27.1) and licensed CC BY-SA 3.0. I downloaded its `.ly`, `.mid` and `.rdf` into a separate scratch folder, treated them as untrusted data, and read the MIDI with `python3 -I`. Nothing of that edition (engraving, layout, text) is copied here; only Bach's pitches are used.
- The **countersubject idea** (the chromatic fourth G# G F# F E) is also Bach's, from the same fugue. Here it forms the lower strand of the subject's tail, which is new.
- The **chaconne idea** (a solo violin implying a ground's harmony with chords swept across the strings) follows the Ciaccona of BWV 1004. No notes are taken from it.
- Everything else is new: the tail, all other counterpoint, the summit, the folding, the coda and the prelude.

## Material

```
HEAD  (Bach)   R:2 E5:1 D#5:1 E5:2 E4:2 A4:2 C5:2 B4:2 D5:2          (bar 1)
TAIL  (new)    C5 A4 E5 G#4 D5 G4 C5 F#4 B4 F4 A4 E4 | G#4:4          (bar 2, sixteenths)
               upper strand C E D C B A G# / lower strand A G# G F# F E (the lament)
AHEAD (Bach's answer)  R:2 A4 G#4 A4 A3 E4 G4 F#4 A4 ; ATAIL = TAIL at the dominant
```

Every statement is an explicit transposition, octave shift or augmentation (`tr`, `oc`, `aug`) of the hand-written subject. Subject statements and splits are labelled in the JSON (24 entries). Heads in G, C and F major (b27–29) keep the subject's shape modally. The critic reports them as 5/8 intervals exact; the answers at b18 and b22 show 6/8 because of the tonal answer.

## Section map and tempo

| bars | section | voices | tempo |
|---|---|---|---|
| 1–8 | **Violino solo, exposition:** subject E5 (alto strand), Bach's answer A4 (tenor), subject E6 (soprano), subject in C from G4 down to the open G (bass). Vl II on Vl I's staff marks the double stops. | 1 (+ double stops) | ♩=66 |
| 9–12 | the four strings as four strands, Chaconne-style sweeps (C, G7/B, C7/Bb, F/A, G#o7, Am, Dm/A, E7/G#) | 1 | 66 |
| 13–15 | the strings come out: Vc I (G string), Va I (D), Vl II (A) | 4 | 72 |
| 16–23 | generation 2: each of the four states the subject or answer and splits in its tail | 4 → 8 | 72 |
| 24–32 | generation 3: a cascade of entries a bar apart (Em, Am, Dm, G, C, F, turn to E7; Vc I in A over a tonic pedal) | 8 → 15 | 72 |
| 33–38 | generation 4: stretto from the top down (E6, E5, E4, E5, E3) over dominant then tonic pedals; Cb I's tail gives Vc V | 15 → 20 | 72 → 60 |
| 39–47 | **summit** (below) | 20–21 | 60 |
| 47–58 | **folding**, over the lament as a three-bar chaconne bass (A G# │ G F# │ F E, three times) | 21 → 1 | 60 → 54 |
| 59–67 | **violino solo:** the ground as swept chords (b59–61), as a running scale (b62–64), then compressed into the subject itself: Bach's head at its first pitch (b65) and the tail, whose lower strand is the lament (b66). A last sweep, then A. | 1 | 63 → 44 |

## The summit (bars 39–47)

- **Bass:** Cb I has the **subject in four-fold augmentation** (E2 D#2 E2 E1 A1 C2 B1 D2, from b39.3). At **b43.2** its tail splits for the last time. The new Cb II, the **21st voice**, catches the lament A1 G#1 G1 F#1 F1 E1 in half notes, a quarter behind Cb I, which keeps the upper strand C E D C B A G#. The harmony therefore changes on every beat: Am │ Bø │ Am/C Am E/G# │ E7 G C/G F#o │ Bm/F# Bø/F Dm/F Am/E │ E │ A.
- **b39:** a dominant field. Every voice holds a tone of E major and turns once around it (E–D#–E or an upper neighbour), each at its own sixteenth, so that no two voices an octave or fifth apart move at the same moment (19 voices moving).
- **b40:** the texture thins and the **solo violin states the subject at its first pitch (E5)** inside the tutti. **b41:** violin III answers **in stretto on A**.
- **Top line (Vl VII):** E6 F6 E6 │ D6 F6 │ E6 C6 A5 B5 │ E6 D6 E6 **F#6** │ D6 F6 (a 9–8 over the basses' E) │ E6 │ C6.
- **Solo violin (Vl I):** a chain of suspensions C A │ C B │ C B │ B C A │ C B A │ G# B │ A.
- **The other 16 upper voices** sing slow, mostly stepwise lines, each moving at its own moment. Most notes are held across the bass's changes as suspensions or retardations and resolve by step. Examples: Vl VI A B A G# F# E D F E; Vl IX A B A B C D E; Va III A F E G# B A G F E; Vc II A B C D C D C B G#.
- **Moving voices per bar** (critic: at least one attack and sounding ≥ ¼ bar): b39 19, b40 20, **b41 20, b42 19, b43 21, b44 21, b45 21**, b46 20, b47 20. Mean over b39–46: **20.1**.

## Timbre and space

- **Instruments:** Vl I–IX violin (GM 40), Va I–V viola (41), Vc I–V cello (42), Cb I–II contrabass (43). Ranges stay idiomatic: violins never go below G3, violas never below C3, and cellos come down to E2 only while carrying the bass at the end. Vl II's notes in b3–7 are double stops of the one violinist and are engraved on Vl I's staff.
- **Space:** the solo violin sits at the front centre (0°, 3 m). Each generation sits further out and wider, and every child sits near its parent (e.g. Vl VII at 58°/7.2 m beside Vl IV at 40°/6.2 m). The `spatial` field of each voice holds this, and `render_spatial.py --layout score` uses it. Pan in the stereo renders is derived from the azimuth.
- **Score:** A2 paper, staff size 16, empty staves hidden, so the system grows from one staff to 21 and shrinks back to one.

## The prelude

A perpetual-motion *preludio* for one violin in sixteenths: **one line**, playable by one hand at the keyboard (the piano renders are that version). Every bar is two or three strands sounded one note at a time, the polyphony the fugue makes real.

- **Bar 1** interleaves Bach's subject head (E D# E E A C B D) with a pedal on the open A string. The fugue's subject is first heard as a strand inside a figuration.
- **Bars 5–7 and 26–28** carry the fugue's summit ground, the lament A G# G F# F E, in the lowest strand.
- **Bar 29** is the fugue's tail verbatim, which compresses that lament into one bar.
- Plan: tonic pedal (1–4), lament (5–8), circle of fifths (9–12), C major and E minor (13–18), return (19–22), dominant pedal on the open E string (23–25), lament on four strings (26–28), tail and A (29–30).
- ♩=72 with a final ritardando; 30 bars, about 1:44.

## Critic numbers (`tools/critic.py`)

**Fugue** (67 bars, 21 voices):

| measure | value | target |
|---|---|---|
| parallels_error | **0** | 0 |
| beat_parallels | **1** (b22.3 Va II/Vc I, C→E octaves; left) | ≤ 8 |
| dissonance_unresolved | **0** | ≤ 15 |
| bad_doublings | **2** (b27.3, b32.3: doubled 7th, from the A pedal; left) | ≤ 8 |
| low_register_seconds | **0** | ≤ 16 |
| stepwise_pct | **45.7** | ≥ 60 — **missed**, see weak spots |
| leap_4th_plus_pct | 32.0 | |
| mean moving voices (whole piece) | 6.99 | |

Stepwise motion by section (same rule as the critic, repeated notes counted): solo violin b1–12 14%, string sweeps b13–15 14%, generation 2 53%, generation 3 54%, generation 4 56%, **summit 64%**, folding 36%, coda 36%.

Mean moving voices by section: b1–12 1.2, b13–15 3.0, b16–23 5.8, b24–32 7.9, b33–37 7.8, b38 7.0, **b39–46 20.1**, b47–58 9.3, b59–67 1.0.

**Prelude:** parallels/dissonance n/a (one line). Range G3–C6. stepwise 9.5% (the line is arpeggiated compound melody by design). tertian fit 88%.

## Honest weak spots (what I would still improve)

1. **The summit may be thick.** To keep 21 lines moving with no parallels over a harmony that changes every beat, the inner voices hold notes across the changes as suspensions. On most beats of b41–46, two to four pitch classes outside the chord are sounding, each resolving by step. The critic accepts this, but the result may blur into clusters. A cleaner version would slow the double basses' lament to half the speed (whole-note strands) so that the harmony changes every half bar.
2. **Stepwise motion is 45.7%, below the 60% target.** The concept is compound melody: the solo-violin sections, the string sweeps and the folding figures are made of leaps. The counterpoint sections are 53–64%. Making the coda's first cycle a scale (as in b62–64) and the folding figures shorter would raise it.
3. **The inner lines of the summit and the folding are functional rather than thematic.** I chose them from candidate lines proposed by a scratch search tool (see "Tools"), then edited them. A few have chromatic wobbles: G–G# approaches in Vl V (b52) and Vc III (b49), and an F#–G anticipation in Va I (b44). There are no subject entries in the inner voices after b41.
4. **The bass register is thin at the summit.** The cellos sit in the tenor range (G3–E4) to avoid seconds against the double basses. The bottom octave is the two double basses alone.
5. **The folds may be hard to hear.** The compound beat P X P X lasts one beat inside a thick texture. The first fold (Cb II) is a unison meeting rather than a compound beat.
6. **Leftovers:** the beat-to-beat octave at b22.3 and the two doubled sevenths at b27.3 and b32.3. The modal heads (G, C, F major) bend the subject's intervals.
7. **No dynamics** beyond base velocities and entry accents; in particular there is no crescendo into the summit.
8. **The prelude** is almost all arpeggio figuration and may feel uniform; it has no slower episode.
9. **Length:** 67 bars (brief: about 70–110); duration about 4:11.

## Tools

**Changed (backward-compatible).** Every existing score renders identically: `cycle/02-c-minor/fugue.json` gives byte-identical `.ly`, `.mid` and `.musicxml` before and after.

- `tools/render_music.py`
  - A voice may carry `"share_staff": <name or abbr>`. It is then engraved on that voice's staff as `\voiceOne`/`\voiceTwo` (used here for the solo violin's double stops).
  - New `--instruments` flag: each voice plays its own `gm_program` (and `pan`) in MIDI and audio. Without the flag every voice is piano, as before.
- `tools/render_spatial.py`
  - New `--layout score`: each voice is placed at its own `spatial` [azimuth°, distance m], falling back to the arc.
  - New `--instruments` flag, as above.

**Scratch tools (in my scratchpad, not in the repo).**

- `chk.py`: the critic run on a bar window.
- `vl.py` and `alts.py`: show faults and one-note alternatives for a voice.
- `line.py`, `grid.py` and `grid2.py`: proposers. For one voice they search pitches (and, in `grid*`, rhythms on an eighth grid) against the texture as it stands and a harmony plan I wrote. They minimise critic faults and prefer steps, and print a few candidates. **Many inner-voice lines of the summit (b41–47) and of the folding (b47–58) started as such proposals.** I chose among them, edited them (endings, held notes, fold pitches), and wrote every note into `fugue.py` by hand. No script inserts or alters notes in the score.
- `arp()` in `fugue.py` only writes out chords I spelled as sixteenth sweeps, and `s16()` in `prelude.py` only appends `:1` to pitches I wrote.
- Thematic placements (`theme()`, `tr`, `oc`, `aug`) are explicit in the source.
