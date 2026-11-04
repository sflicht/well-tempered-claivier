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
| 39–47 | **summit** (below): tutti, thinned for the stretto and for the lament, all 21 on the arrival (b46) | 6–21 | 60 |
| 47–58 | **folding**, over the lament as a three-bar chaconne bass (A G# │ G F# │ F E, three times); every half bar sounds the ground's chord, and a voice with no clean move rests and returns before its fold | 21 → 1 (7–10 at a time from b48.3) | 60 → 54 |
| 59–67 | **violino solo:** the ground as swept chords (b59–61), as a running scale (b62–64), then compressed into the subject itself: Bach's head at its first pitch (b65) and the tail, whose lower strand is the lament (b66). A last sweep, then A. | 1 | 63 → 44 |

## The summit (bars 39–47)

- **Bass:** Cb I has the **subject in four-fold augmentation** (E2 D#2 E2 E1 A1 C2 B1 D2, from b39.3). At **b43.2** its tail splits for the last time. The new Cb II, the **21st voice**, catches the lament A1 G#1 G1 F#1 F1 E1 in half notes, a quarter behind Cb I, which keeps the upper strand C E D C B A G#. From there the harmony changes on every beat: Am │ Dm7/C Am/C │ Bø7 │ Bø7/D │ Am/C Am Am E/G# │ E7/G# G C/G F#ø7 │ Bm7/F# Bø7/F Bø7/F Am/E (6/4) │ E │ A.
- **The governing arrival is the dominant on the downbeat of b46**, where the augmented subject reaches its last note (G#1 over E1). It is prepared by a cadential 6/4 at b45.4 and resolves to A at b47.1, where the two double basses meet. Three dissonances carry it: the top's **F6 over E1** (a flat ninth held from b45.2, resolving on the downbeat), the **6/4 itself** (A and C over E), and the **solo violin's A4 held into the E chord**, the only suspension left there, resolving to G#4 alone on beat 2. Every other voice arrives on E or B.
- **b39:** a dominant field. Every voice holds a tone of E major and turns once around it (E–D#–E or an upper neighbour), each at its own sixteenth, so that no two voices an octave or fifth apart move at the same moment (19 voices moving).
- **b40:** the texture thins and the **solo violin states the subject at its first pitch (E5)** inside the tutti. **b41:** a tutti A minor on beats 1–2, then **violin III answers in stretto on A** in a texture of eight voices (b41.3–42), as the solo violin's subject was heard in b40. Violin IV takes over violin III's A5 as the answer drops to A4 and holds it as a pedal.
- **b43:** the tutti returns; **all 21 sound together from b43.2**, the 21st voice's entry, on A minor.
- **b43.4–45.4, the lament window:** as the double basses' lament descends, the inner voices leave in turn (13 voices at b43.4, 8 at b44.2, 7 at the peak F#6 and 6 at the 6/4). A voice stops when it has no step left that does not double another voice's motion or blur the next chord. What remains is the lament, the top line, violin III, the solo violin and two inner lines: violin II (E │ F# G A . B │ C D │ E D │ C) and viola II (E D, the seventh of F#ø7 and the third of Bm7). Cello II adds D3 under the two B chords.
- **b46:** all 21 voices land on E (most on E or B; the third, G#, is in the bass, and above it only after the solo violin's resolution). Cello I fills in B G# E after that resolution; violin II's D5 on beat 4 makes it E7.
- **Top line (Vl VII):** E6 F6 E6 │ D6 F6 │ E6 C6 A5 B5 │ E6 D6 E6 **F#6** │ D6 F6 (the flat ninth over the basses' E) │ E6 │ C6.
- **Solo violin (Vl I):** C A │ B │ C . . B │ . . C A │ B . . A │ . G# . B │ A.
- **Moving voices per bar** (critic: at least one attack and sounding ≥ ¼ bar): b39 19, b40 20, b41 20, b42 8, **b43 21**, b44 8, b45 8, **b46 21**, b47 13. Every beat of b41–46 now sounds a recognisable chord, plus at most two suspensions resolving within the beat (before: five to eight pitch classes on most beats, eight at b44.1½).

## Timbre and space

- **Instruments:** Vl I–IX violin (GM 40), Va I–V viola (41), Vc I–V cello (42), Cb I–II contrabass (43). Ranges stay idiomatic: violins never go below G3 and violas never below C3. The cellos use their low string where a line needs it: cello I's subject drops E3–E2 at b16 (Bach's octave leap), cello V plays E2 on the summit's first downbeat (b39.1) and before it folds into the double bass (b50.1–50.3), and cello I goes down to E2 while it carries the ground at the end (b55–56). In the summit, cello I has B2 (b39–40), cello III A2 and cello IV C3 on the tutti A minor (b41.1), cello III B2 (b44.1) and cello II D3 (b45.1). Vl II's notes in b3–7 are double stops of the one violinist and are engraved on Vl I's staff.
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

**Fugue** (67 bars, 21 voices; critic, 4 Nov 2026):

| measure | value | target |
|---|---|---|
| parallels_error | **0** | 0 |
| beat_parallels | **0** (1 before the self-critique pass: b22.3, now fixed) | ≤ 8 |
| dissonance_unresolved | **4** (the lament's F#–F over the E pedal, b34–37; kept, see Review response) | ≤ 15 |
| dissonance_unverified | **3** (b24.4, b34.4, b40.4; kept, see Review response) | check by ear |
| bad_doublings | **2** (b27.3, b32.3: a passing note and a double pedal read as doubled sevenths; kept, see "Self-critique pass") | ≤ 8 |
| low_register_seconds | **0** | ≤ 16 |
| stepwise_pct | **43.4** (44.1 before the self-critique pass, 45.7 before the 1 Nov revision) | ≥ 60 — **missed**, see weak spots |
| leap_4th_plus_pct | 35.6 (34.1 before the pass) | |
| tertian fit, beats with 3+ pitch classes | 51.9% (45.9% before the pass) | |
| mean moving voices (whole piece) | 5.87 (6.33 before the pass) | |
| crossings | 35 (43 before the pass) | |

Stepwise motion by section (same rule as the critic, repeated notes counted): solo violin b1–12 14%, string sweeps b13–15 14%, generation 2 54%, generation 3 54%, generation 4 56%, **summit 62%** (b39–46; 166 melodic intervals, 284 before the 1 Nov revision), folding b47–55 37% (the fold figures are leaps by design), the last three folds' sweeps b56–58 5%, coda 36%.

Mean moving voices by section: b1–12 1.2, b13–15 3.0, b16–23 5.8, b24–32 7.9, b33–37 7.8, b38 7.0, **b39–46 15.6**, b47–58 6.1 (8.7 before the pass), b59–67 1.0.

**Prelude:** parallels/dissonance n/a (one line). Range G3–C6. stepwise 9.5% (the line is arpeggiated compound melody by design). tertian fit 88%.

## Honest weak spots (what I would still improve)

1. **The summit's lament window is sparse.** Since the Nov 2026 revision the inner voices rest while the lament descends (b43.4–45.4), so the peak F#6 sounds in seven voices directly after the 21-voice moment. That contrast is the point; since the self-critique pass the remaining lines play louder there (the crescendo peaks at b45–46, and the double basses keep their accent through the lament), but it should be checked by ear against the full arrival in b46.
2. **Stepwise motion is 43.4%, below the 60% target.** The concept is compound melody: the solo-violin sections (b1–12, 14%), the string sweeps (b13–15, 14%; b56–58, 5%), the fold figures and the coda's swept chords are made of leaps. The counterpoint sections are 54–62%. The two fixes once proposed here (the coda's first cycle as a scale, shorter fold figures) are declined; see "Self-critique pass".
3. **The inner lines of the summit and the folding are functional rather than thematic.** Both are written by hand (the summit's on 1 November 2026, the folding's in the self-critique pass): chord tones, common tones held across the ground's changes, and rests. They no longer crowd the harmony (every half bar of b47–55 sounds the ground's chord with at most one suspension, passing note or anticipation), but they do not carry the subject: there are no subject entries in the inner voices after b41.
4. **The bass register is light at the summit.** The cellos come below the tenor only on chord tones (cello V's E2 on the first downbeat, b39.1; cello I's B2 in b39–40; cello III's A2 and cello IV's C3 on the tutti A minor, b41.1; cello III's B2 at b44.1 and cello II's D3 at b45.1). Elsewhere they sit at E3–E4 to avoid seconds against the double basses, so through most of the lament window the bottom octave is the two double basses alone.
5. **The folds may be hard to hear.** The compound beat P X P X lasts one beat. Since the self-critique pass the texture around the folds is thinner (seven to ten voices from b48.3) and most children return from a rest to hold their X before the fold, which should help; whether the hand-over is audible needs a listener. The first fold (Cb II) is a unison meeting rather than a compound beat.
6. **Leftovers:** the critic's two doubled sevenths at b27.3 and b32.3, which are a passing note and a pedal read as chord sevenths (see "Self-critique pass"). The modal heads (G, C, F major) bend the subject's intervals.
7. **Dynamics are coarse.** A per-bar table shapes the crescendo into the summit (b33–46) and the diminuendo through the folding (b47–52), and the double basses keep an accent through the lament; there are no finer hairpins or articulations.
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
- `line.py`, `grid.py` and `grid2.py`: proposers. For one voice they search pitches (and, in `grid*`, rhythms on an eighth grid) against the texture as it stands and a harmony plan I wrote. They minimise critic faults and prefer steps, and print a few candidates. **In the first draft, many inner-voice lines of the summit (b41–47) and of the folding (b47–58) started as such proposals.** None of them remain: the summit's inner lines were rewritten by hand on 1 November 2026 and the folding's free lines in the self-critique pass (3 November), with display-only scratch scripts (a voice-by-eighth matrix with the pitch classes per half beat, and the critic). No script inserts or alters notes in the score.
- `arp()` in `fugue.py` only writes out chords I spelled as sixteenth sweeps, and `s16()` in `prelude.py` only appends `:1` to pitches I wrote.
- Thematic placements (`theme()`, `tr`, `oc`, `aug`) are explicit in the source.

## Review response (Nov 2026)

*1 November 2026.* The owner's review of PR #1 (written by ChatGPT) asked for the summit to be heard as one harmony: choose the governing arrival, decide which dissonances carry it, and rest or stagger inner parts whose resolutions obscure it. The claim checked out. At b44.1½ the 21 parts sounded eight pitch classes (C D E F F# G# A B). Most beats of b41–46 sounded five to seven, because 16 inner voices held notes across a bass that changes every beat and resolved them at staggered moments. The arrival on E at b46.1 sounded seven pitch classes and did not clear until beat 3. The critic, corrected in commit 09df800 so that a resolution must land within a beat on a consonance, found 31 unresolved and 19 unverified dissonances, most of them here.

**What changed.**
- The inner parts of b41–47.1 are rewritten (the double basses' subject and lament, the top line and violin III's stretto are kept). The arrival is the E chord on the downbeat of b46, the end of the augmented subject, prepared by a cadential 6/4 and carried by the top's flat ninth F6–E6, the 6/4 itself and the solo violin's A4–G#4. The voices now hold common tones and move only when no other voice makes the same motion. A voice with no such move rests. The texture therefore breathes: tutti on b41.1, eight voices for the stretto, all 21 from b43.2, a thinning window for the lament (seven voices at the peak F#6, six at the 6/4), all 21 again on b46. The solo violin's line is simplified to C A │ B │ C B │ B C A │ B A │ G# B │ A (its C on b42.1 and b45.1 had blocked the chords there), and violin III steps D6 C6 B5 into the arrival.
- Smaller fixes elsewhere, each a real clash: violin II at b19 and viola I at b23 resolve half a beat later, on the beat (they were stepping down in parallel seconds and sevenths with the tail); viola I reaches C# with the bass at b26.4. (The fold-cycle fixes in the rest of this item were superseded when the self-critique pass rewrote b47–55.) In the first fold cycle, cello III keeps its E4 from the arrival instead of striking D4 against it at b47.2 (which also made fifths with violin III). Viola V's C4 at b47.4 becomes an anticipation on the half beat. Viola III rests a beat after its fold and takes D4 with the D chord (b48). Viola IV's G#3 neighbour goes off the beat. Cello III goes A3–G#3 directly (b49). Violin III's passing B5 and cello II's line are adjusted so that violin IV's 9–8 at b50 resolves onto a consonance.
- Every note of the new lines is written in `fugue.py` by hand. To read the score I used two display-only scratch scripts (a per-voice grid by sixteenths and an interval counter) together with `tools/critic.py` and `tools/reduce.py`. Nothing proposed pitches.
- Critic, before → after: unresolved 31 → 4, unverified 19 → 3, parallels 0 → 0, beat-to-beat parallels 1 → 1, bad doublings 2 → 2, low-register seconds 0 → 0, crossings 51 → 43, tertian fit 39 → 46%. In b39–48 the critic logs 173 dissonance events instead of 694, and 'unprepared' suspensions fall from 99 to 4.

**What I kept, and why.**
- *Four 'unresolved' flags* (b34.3, b35.3 twice, b37.3): the lament's chromatic F# in a newly split voice, sounding across beat 3 while another voice strikes E over the E pedal. The line goes F#–F–E within half a beat. The critic checks only the next note (F, still a second from E), so it cannot see the arrival on E. The lament is thematic, so I left it.
- *Three 'unverified'*: b34.4 and b40.4 are 4–3 suspensions (A–G#) whose resolution meets the subject's D, the seventh of E7. They resolve half a beat late because violin VII and violin IV take A–G# on the beat in the octave above. b24.4 is a voice exchange (A3/B4 to B3/A4) inside B7 over the E pedal. These are check-by-ear cases, not errors.
- *The beat-to-beat octave at b22.3 and the doubled sevenths at b27.3 and b32.3*, as before. (b22.3 has since been fixed; b27.3 and b32.3 are explained in the self-critique pass.)
- *Stepwise motion fell from 45.7% to 44.1%, and leaps of a fourth or more rose from 32.0% to 34.1%.* All of the change is in the summit, where the review asked for rests. The summit's remaining lines are as stepwise as before (62% steps, 9.6% leaps, against 64% and 9.9%), but they have 118 fewer melodic intervals, and those were mostly steps. A note-by-note check of b44–46 shows why the old version needed its staggered suspensions: the fixed lines (top, violin III, solo, both basses) already make nearly every stepwise motion available on each beat, so any further moving voice either doubles one of them in octaves or holds a note across the change. I did not rewrite unrelated bars to win the ratio back.
- *Fewer moving voices*: the critic's 'bars with all 21 voices moving' falls from 3 (b43–45) to 2 (b43, b46), and the whole-piece mean from 6.99 to 6.33. The review's point was that a count of attacks does not make 21 arguments. All 21 parts still sound together, at the 21st voice's entry and at the arrival.
- *The 21 parts, the split/fold form and the last bass split's lament* are unchanged.


## Self-critique pass (Nov 2026)

*3–4 November 2026.* The open points of my own critique above, each fixed or declined.

- **The folding is rewritten, b47–55 (fixed).** The first fold cycle sounded six or seven pitch classes on most half beats (b47.4: C D E F# G# A B), because the free lines between the folds were still the edited proposals of the first draft: voices held notes of the old chord across the ground's change and resolved them late. Every free line of b47–55 is now written by hand on the ground's harmony, Am | E/G# ‖ C/G | D7/F# ‖ Dm/F | E. Each half bar sounds that chord, plus at most a suspension (cello I's E3 over D7 at b51.3, a 9–8; violin III's A5 over E at b52.3, rising to B5), a passing note, or a half-beat anticipation of a fold note. No upper voice moves with the bass's chromatic step (A–G#, G#–G, G–F#, F#–F, F–E), and that is what rules out most moves here. A voice with no clean move rests and comes back before its fold, holding its X as a common tone or reaching it by step. So from b48.3 seven to ten voices sound at a time instead of fifteen to twenty; the count still falls fold by fold to the solo violin at b58, and every voice still ends at its fold. The summit's E is held by most voices through Am, E/G# and C/G and let go during b48.
  - Four folds take new notes so that the hand-over is a common tone or a step: fold 3 (viola III's P is now the E3 it has been holding); fold 9 (viola IV hands E4 to viola II, whose P is G3; its old X, G3, was approached against the bass's G#); fold 10 (viola I's P is A3, leaving A4 free for violin VI's fold 11); fold 15 (viola II hands E4 to violin II; its old G4 and F4 sounded against G#2).
  - Violin V's G–G# at b52 is gone: it comes back on A4 and steps down to G#4, the leading tone it hands to the solo violin.
  - The solo violin changes two notes: D5 instead of B4 at b47.3 (the seventh of E7, resolving to C5), and A4 instead of C5 at b53.1 (to avoid a unison with violin II's resolution).
  - In b47–58 the critic finds no parallels, beat-to-beat parallels or unresolved dissonances, and the tertian fit of the whole fugue rises from 45.9% to 51.9%.
- **The beat-to-beat octave at b22.3 (fixed).** Cello I now steps C3–B2 and holds B2 into the B7 chord, instead of leaping C3–E3 in octaves with viola II's C4–E4; cello II goes C4–G3–A3 so that the two cellos do not move in octaves either.
- **The doubled sevenths at b27.3 and b32.3 (declined, with reasons).** At b27.3 the chord is G major over G1 (B3, G3, D5 twice, B5); the critic reads Em7/G because violin VI's E4 falls on the beat as a passing note of its eighth-note strand G F E D, the upper strand it has just taken over at its split. The "seventh" is the fifth of G, doubled. At b32.3 the double bass's tonic pedal A1 and violin IV's A5 (held since b31; it becomes the 4–3 suspension A–G# onto the E pedal at b33.1, which starts generation 4) sound under the subject's tail and the new lament; the critic counts the two A's of this double pedal as a doubled seventh of Bø7/A. Removing either would change a split strand or that suspension.
- **Stepwise motion (declined).** The two fixes this file once proposed would each cost the piece something its idea needs, for a gain of about three points (the coda) and one point (the fold figures). The coda's swept chords (b59–61) are the moment the solo violin has all four strings again, after the last three folds widened its sweep from two strings to four (b56–58): it states the ground as chords, as the Chaconne does, before the scale (b62–64) and the subject (b65–66) compress it. A scale there would give two scale cycles in a row and lose both that progression and its echo of b9–12. The four sixteenths of a fold figure (P X P X) are the only audible sign of a fold (weak spot 5), and halving them would make the folds harder to hear. Stepwise is now 43.4% (44.1% before this pass): the rewritten folding holds and rests more, so it has fewer melodic intervals (206 in b47–58 instead of 280), proportionally more of them in the fold figures and the sweeps.
- **A crescendo into the summit (fixed).** The velocities had no shape beyond each voice's base and the entry accents, so the mean onset velocity fell from about 66 to 63 approaching the arrival: more voices with lower base velocities joined, and the augmented subject's entry accent ended at b43.3, in the middle of the lament. A per-bar table in `fugue.py` (`DYNAMICS`, performance data only) now adds a crescendo from the stretto of generation 4 to the arrival (+1 at b33, +5 at b39, +9 at b43, +12 at b45–46) and a diminuendo through the first two fold cycles (+9 at b47 down to +1 at b52). The double basses keep a +6 accent from b43.3 to their meeting at b47.1 (`BASS_ACCENT`), so the subject's tail and the lament carry the thinning window. The mean onset velocity now rises from 66 (b33) to 76 (b46), and in the lament window (b44–45) the seven or eight remaining lines play louder rather than the music getting quieter.
- **Corrections in this file.** "Timbre" said the cellos reach E2 only at the end, and weak spot 4 said the summit's cellos stay at G3–E4; both are corrected above. Weak spots 2–7 and "Tools" are updated in place.
