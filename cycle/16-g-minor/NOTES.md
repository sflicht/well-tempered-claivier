# Fugue XVI in G minor: *Fantasia e fuga a 17 per Reincken* (seventeen voices)

## 1. The story

In November 1720 Bach went to Hamburg and played the organ of St. Katharinen before Johann Adam Reincken,
its organist since 1663. The Obituary calls Reincken "nearly a hundred", following the traditional
birth year of 1623. Modern research puts his birth in 1643, which would make him about 77.

The Obituary by C. P. E. Bach and J. F. Agricola (1754) dates the visit "about the year 1722" and tells
the story:

> Bach, at the request of those present, performed extempore the chorale *An Wasserflüssen Babylon* at
> great length (for almost half an hour) in different ways, just as the better organists of Hamburg in
> the past had been used to do at the Saturday vespers. Particularly on this, Reinken made Bach the
> following compliment: "I thought that this art was dead, but I see that in you it still lives."

Reincken had himself written a huge chorale fantasia on the same melody. A tablature copy of it in the
15-year-old Bach's hand, dated 1700, was found in Weimar in 2005.

This movement imagines that half hour, compressed to four and a half minutes. It is a chorale fantasia in
the North German manner, for an imaginary organ of three manuals and double pedal, in seventeen real
voices:

| division | voices (staff names) |
|---|---|
| Oberwerk | OW S, OW A, OW T, OW B |
| Hauptwerk | HW S1, HW S2, HW A, HW T, HW Bar, HW B |
| Rückpositiv | RP S, RP A, RP T, RP Bar, RP B |
| Pedal | Ped. I, Ped. II |

Shape: 78 bars of 4/4 at a basic quarter = 72, with a tempo map. The render lasts 4:31.

### Credits

- **The chorale.** *An Wasserflüssen Babylon*, Wolfgang Dachstein, Strasbourg 1525 (a paraphrase of
  Psalm 137). The melody is copied from the soprano of Bach's four-part setting **BWV 267** (music21
  corpus `bach/bwv267`), note for note and in its own rhythm. To move it from G major into G minor:
  - B becomes B♭, and E becomes E♭, except in line 8, which keeps its E♮ (Dorian).
  - The C♯ of line 6 is kept. "Orgeln" therefore falls on an augmented second, B♭–C♯.
- **J. A. Reincken.** The idea of the whole: a chorale fantasia that takes the melody line by line.
- **J. S. Bach, BWV 653b.** *An Wasserflüssen Babylon* a 5 with double pedal, the Weimar version of the
  Leipzig chorale BWV 653. It suggested the two pedal voices; here they carry the chorale in canon at the
  octave.
- **J. S. Bach, Fugue in G minor BWV 542.** Its subject enters once, as a genuine voice (§5):
  - Copied from the Mutopia Project edition after Peters; the file was read as data only.
  - It resembles the Dutch song "Ik ben gegroet van...". Since Spitta it has been linked, without proof,
    to the 1720 Hamburg visit.
  - Its placement was searched with `tools/stretto_finder.py --against` (subject 10 against the BWV 542
    subject, both forms, several transpositions).
- **New in this piece:** the subjects made from the chorale lines, all counterpoint, the plan, the summit
  and the coda. They are by Claude, for Sam.

## 2. Files

- `fugue.py`: the source. Every note is written as wtclib bar strings by hand.
  - Thematic statements are explicit transforms of hand-written subjects: `oc` (octave), `tr` (real
    transposition), `dsh` (diatonic shift in G minor), `W.invert_diatonic`, and `cantus()`, which doubles
    the note values and lengthens the fermata note.
  - Scratch tools in the session only ranked placements of whole statements and listed clashes of
    hand-written lines. No code chose a pitch. No note was inserted or altered by script to move a critic
    number.
- `fugue.json`: built by `python3 fugue.py`. It carries 98 labelled entries; `subject=` is subject 1.
- `renders/`:
  - `fugue.pdf`: two A2 pages, staff size 14, empty staves hidden. LilyPond compiled cleanly.
  - `fugue.ly`, `fugue.mid`, `fugue.musicxml`.
  - `fugue.mp3`: Bach-Lehman temperament, 271 s.
  - `fugue-equal.mp3`: equal temperament, audio only.
  - `fugue-spatial.mp3`: the choir layout, with the seventeen voices fanned from −70° to +70° in score
    order. The Oberwerk is on the left, the Hauptwerk in the centre, the Rückpositiv on the right and the
    two pedals at the far right.
- No prelude (§9).

## 3. Chorale lines and their subjects

Each line has its own subject, made from the line's own notes. Only the rhythm, the speed or the
chromatic filling changes. Lines 3-4 repeat lines 1-2 (bar form), so their section uses subjects 1 and 2
again, inverted ("remembered").

| line | text | chorale (G minor) | subject | gesture |
|---|---|---|---|---|
| 1 | An Wasserflüssen Babylon | D E♭ D C B♭ C D C B♭ C B♭ | **S1** = the line itself, in the chorale's rhythm | grave; real answer a 4th lower |
| 2 | da saßen wir mit Schmerzen | A B♭ C D C B♭ A G A G | **S2**: same notes, dotted ("limping"), 6 beats | sighs |
| 3-4 | als wir gedachten an Zion, da weinten wir von Herzen | = 1-2 | S1 and S2 inverted | remembered, in echoes |
| 5 | wir hingen auf mit schwerem Mut | G A B♭ C B♭ A B♭ A G | **S5**: same notes and values, shifted an eighth, so every note hangs across the beat | syncopes |
| 6 | die Harfen und die Orgeln gut | G A B♭ C D E♭ B♭ C♯ D | **S6**: at double speed, opening as a 16th-note tirata | the harps |
| 7 | an ihre Bäum der Weiden | B♭ C D E♭ D C B♭ C B♭ | **S7**: in triplet eighths around quarters | the willows swaying |
| 8 | die drinnen sind in ihrem Land | E E E A D C B♭ A | **S8**: repeated eighths, dotted fall | knocking at a foreign door (E♮) |
| 9 | da mussten wir viel Schmach und Schand | C B♭ A G A G F E♭ D | **S9**: the steps filled chromatically, C B B♭ A G A G F E E♭ D (passus duriusculus) | shame |
| 10 | täglich von ihn' erleiden | D G A B♭ C D C B♭ A B♭ C A G | **S10**: the line at double speed | daily |

- **Answers:** A1 a 4th lower (D minor); A5, A6 and A7 a 5th higher (A6 with G♯); A8 a 5th lower (in A); A9
  a 4th lower.
- **The pedal cantus:** each line in half notes, with the fermata note lengthened.

## 4. Section map

| bars | line | Vorimitation (subject entries) | pedal canon at the octave | episode / character |
|---|---|---|---|---|
| 1-11 | 1 | Hauptwerk: HW A S1 b1; HW T A1 b2.3; HW B S1 b4; HW S1 A1 b5.3; HW S2 S1 inverted b7 | Ped. II leads b6.3, Ped. I 10 beats later (b9); Ped. II's free cadence to B♭ (b11-13) | HW A's "waters" countersubject |
| 12-20 | 2 | Rückpositiv: RP T S2 b12; RP A in canon at the octave, 3 beats; RP S, RP B, RP T inverted, RP S answer, RP A inverted, RP Bar answer (b12-15.3); RP T S2 over the cantus b16.3, b18.3 | Ped. I leads b15.3, Ped. II 7 beats later | cadence on G, b21 |
| 21-32 | 3-4 | Oberwerk debut. Line 3: S1 inverted OW S b24, RP T b25.3, HW A b27. Line 4: S2 inverted OW S b28.3, S2 RP T b30, S2 inverted HW S1 b31.3 | Ped. I sings lines 3 and 4 without a break from b23.3; Ped. II 9 beats later | **echo**: the head of line 1 on the HW (b21.3), the same notes on the RP (b22.3), half of it on the OW (b23.3); slower tempo |
| 33-39 | 5 | HW T S5 b33; RP A A5 b34; OW S b35; RP T on C b36; HW S2 inverted b37; OW A on C b38; HW Bar b38.3 | Ped. II b35.3, Ped. I 3 beats later | syncopes over a suspended bass |
| 40-48 | 6 | the harps: OW S b40; RP A b40.3; HW T b41; RP S b42; HW A b42.3; OW A b44; RP T b44.3 | Ped. I b41.3, Ped. II 3 beats later. An **augmented sixth** forms at "Orgeln" (b44.3) | half cadence on D (b45-46); **b47 general pause** (the organ "hung up"); **b48** a lone RP S harp arpeggio, D7♭9 |
| 49-54 | 7 | HW A S7 b49; OW T A7 b49.3; HW Bar b50.3; HW S1 on E♭ b51; HW B inverted b51.3; RP S on G b52.3; HW B on E♭ b53.3; RP A inverted b54 | Ped. II b50.3, Ped. I 3 beats later | triplets throughout |
| 55-60 | 8 | RP T S8 b55.4; HW B b56; HW S2 b56.3; OW S b57; HW Bar b57.3; RP A A8 b58; OW B b58.3; OW T on A b59.3; RP S A8 b60; OW A b60.3: ten entries in 5 bars, all three manuals | Ped. II b56.3, Ped. I 3 beats later | E♮ and the turn to D minor and A |
| 61-64 | 9 | HW S2 S9 b61; HW B A9 b61.3; RP A on G b62; RP Bar A9 b63.3 | Ped. I b62.1, Ped. II 5 beats later | chromatic fall to D |
| 65-69 | 10 (Vorimitation) | S10 inverted OW A b65; RP T b66; HW A on A b67; OW T b67.3 (against the guest); RP S on C b68.2 | **BWV 542 guest in Ped. I, b67.1.5-b70.1** | the push to the summit (tempo 76) |
| 69.3-75 | 10 | summit (§6) | Ped. II leads b69.3 (upbeat D), Ped. I b70.2, 3 beats later | 11-14 moving voices |
| 75-78 | | coda (§7) | tonic pedal: Ped. II G2, Ped. I G3 | Picardy G major, all 17 voices |

**Tempo map** (quarter = 72 unless stated):
- b21-23, the echoes: 63.
- b45-48, the half cadence, the general pause and the harp: broadens to 58.
- b67-69, under the guest: 76.
- b70-74, the summit: back to 72, broadening to 64 by the arrival.
- b76-78: 62, then a ritardando to 56 (b77) and to 44 at the end.

**Dynamics:** soft at the start, softest in the general pause, loudest on the summit and the last chord.

## 5. The BWV 542 guest

- **What:** Bach's fugue subject, exactly as first stated (the BWV542 constant in `fugue.py`).
- **Where:** two octaves down in Ped. I, from the offbeat of b67.1.5 to b70.1. It is the only pedal voice
  in b67-69, so it is the bass. Its circle of fifths leads into the summit, and its last note, G, is the
  summit's first downbeat (b70.1), where Ped. II's cantus of line 10 also arrives on G.
- **Against it:** OW T sings S10 (b67.3), and HW A and RP S sing S10 on A and on C. The placement came from
  `stretto_finder --against`, which tested S10 against the BWV 542 subject. It was then fitted by hand.

## 6. The summit (b69.3-b75.1): who sings what

**Line 10 in the pedal.** It is a canon at the octave, 3 beats apart:
- Ped. II leads, in the bass: D2 (upbeat), G2, A2, B♭2, C3, D3, C3, B♭2, A2, B♭2, C3, A2, G2.
- Ped. I follows an octave higher, so every move of the bass is met by a held note above it.

**Harmony over it:** i – V4/3 – i6 – III7 – iv7 – i6/4 – iv – i6 – V4/3 – i6 – Am7/C (Dorian ii) – Am7 –
V4/3 – i.

**Thematic statements, in order of entry:**

| voice | statement | from |
|---|---|---|
| HW T | S10, line 10 at four times the speed of the pedal | b69.3.5 |
| HW S1 | S1 an octave up (D6), on top | b69.3.5 |
| RP A | S2, shifted to B♭ | b70.1.5 |
| HW S2 | S8 on A | b70.3.5 |
| OW A | S7 on F | b71.2 |
| OW T | S5 on C | b71.2.5 |
| RP B | S8 on D, tenor register | b71.2.5 |
| HW Bar | S6 on B♭ | b71.3 |
| RP T | S6 at home (with its B♭–C♯) | b72.2 |
| OW B | S7 on D | b72.2.5 |
| HW B | S7 on G, low | b72.3.5 |
| HW S2 | S9 on G (real), the chromatic fall | b72.4 |
| HW A | S7 on G, inner | b72.4.5 |
| OW S | S8 on D | b73.2.5 |
| RP S | S2 at home, closing on G | b73.4.5 |
| RP Bar | S8 at home, with the E♮ | b73.4.5 |
| OW B | S1 returns in the tenor (the first line closes the piece) | b74.3 |

**Free lines, all hand-written:**
- OW S descant: G5 F♯5 G5 D6 C6 B♭5 … A5 D6 C6 B♭5.
- OW A: D5 E5 (b70), F♯6 G6 (b73). It then rises chromatically, E6 F6 F♯6 G6, into the arrival.
- OW B: a B♭3–A3 suspension (b70).
- HW S1: F6 E♭6, then A5 G5 A5 E5 D5, with the 6-5 over the arrival.
- HW T: B♭4 A4.
- HW Bar: resolves its F♯3 to G3 (b70), then E3 D3.
- HW B: F3 E♭3; A3 D3.
- RP S: G4 B♭4 G4 A4 B♭4 A4.
- RP A: G4 E4 C5 A4 B♭4.
- RP T: D4 F4 E♭4 D4.
- RP B: D3 C3 D3 C3, B♭2.

**Density** (moving voices per bar, critic definition):

| bar | 70 | 71 | 72 | 73 | 74 | 75 |
|---|---|---|---|---|---|---|
| moving voices | 11 | 14 | 14 | 14 | 13 | 9 |

- **Mean:** 13.2 over b70-74, 13.8 over b71-74.
- **Sounding at once:** up to 13, mean 10.3; distinct pitches mean 9.3.
- **Voices that sing:** all seventeen sing in the summit, and every one has its own line.

## 7. Coda (b75-78)

- **Arrival, b75.** G minor on the downbeat, with HW S1's E5 → D5 (6-5) and OW B's S1 going on in the
  tenor.
- **Tonic pedal.** Ped. II on G2 and Ped. I on G3 hold through the coda.
- **Chords over the pedal:** Cm/G – F♯°7/G – Gm – D7/G.
  - OW S falls E♭6 → D6.
  - OW A holds G6 above the pedal (an inverted pedal).
  - HW S1 sings C5 D5 C5 B4.
  - HW Bar and OW B move in the bass and tenor.
  - HW S2's F♯5 rises to G5.
- **Last chord (b78).** Nine more voices enter on a G-major chord with a tierce de Picardie, so all
  seventeen voices sound. B is in OW B (B3) and HW S1 (B4); the top is OW S D6 and OW A G6.

## 8. Critic numbers (`tools/critic.py`, final build)

**Whole piece:**

| measure | value | target |
|---|---|---|
| parallels error | 0 | 0 |
| parallels weak | 8 | |
| beat-to-beat parallels | 0 | ≤ 8 |
| unresolved dissonances | 0 | ≤ 15 |
| bad doublings | 8 | ≤ 8 |
| low-register seconds | 7 | ≤ 16 |
| stepwise motion | 82.1 % | ≥ 60 % |

Other measures:
- leaps of a fourth or more: 6.5 %
- pitch class tripled on 20.0 % of beats
- crossings: 28
- melodic augmented seconds: 10, all thematic (§8, last item)
- mean moving voices over the whole piece: 5.0

**Per section.** "Moving" follows the critic: a voice attacks in the bar and sounds at least a quarter of
it. "Sounding" and "distinct" are sampled on every beat.

| section | bars | moving mean | max | sounding mean | max | distinct pitches | time |
|---|---|---|---|---|---|---|---|
| A, line 1 | 1-11 | 3.4 | 5 | 3.1 | 5 | 3.1 | 37 s |
| B, line 2 | 12-20 | 4.4 | 6 | 3.9 | 5 | 3.9 | 30 s |
| C, lines 3-4 | 21-32 | 4.7 | 6 | 3.7 | 6 | 3.5 | 41 s |
| D, line 5 | 33-39 | 4.9 | 7 | 4.5 | 7 | 4.2 | 23 s |
| E, line 6 (+ pause, harp) | 40-48 | 3.1 | 6 | 2.8 | 6 | 2.7 | 32 s |
| F, line 7 | 49-54 | 4.7 | 6 | 3.7 | 6 | 3.5 | 20 s |
| G, line 8 | 55-60 | 5.2 | 7 | 4.1 | 6 | 3.9 | 20 s |
| H, line 9 | 61-64 | 3.8 | 5 | 3.4 | 4 | 3.3 | 13 s |
| Approach + BWV 542 | 65-69 | 4.4 | 6 | 3.8 | 6 | 3.6 | 16 s |
| **Summit** | **70-74** | **13.2** | 14 | 10.3 | 13 | 9.3 | 18 s |
| Arrival + coda | 75-78 | 8.0 | 12 | 10.4 | 17 | 8.9 | 17 s |

Moving voices per bar, b1-78:
`1 2 2 3 4 4 5 4 5 4 3 4 3 4 6 5 5 5 5 3 4 6 6 3 6 4 6 6 4 4 5 2 2 2 4 6 7 7 6 4 3 4 5 6 5 0 0 1 2 4 6 6 5 5 2 4 5 7 6 7 3 4 5 3 4 3 4 5 6 11 14 14 14 13 9 6 5 12`

**The flagged items, justified:**

- **Weak parallels (8).** In each case one of the two notes is an offbeat sixteenth or eighth inside a
  thematic figure:
  - b8.1, HW S2/HW A, octaves;
  - b10.3, HW S2/Ped. I, octaves;
  - b15.2, RP A/RP T, fifths;
  - b53.2, OW T/RP S, fifths;
  - b68.1.25, OW T/HW A, fifths;
  - b71.2.5, HW S1/HW S2, fifths;
  - b73.4.5, HW S2/HW A, fifths;
  - b75.1.5, OW B/RP S, fifths.

  A ninth case, OW B against HW T's S10 at b70.3, was removed by rewriting OW B as a B♭–A suspension.
- **Bad doublings (8), each on a thematic or canonic note:**
  - b13.2: the line-1 cadence B♭ in both pedals, under passing C and G.
  - b16.4: line 2's C in Ped. I against RP T's S2.
  - b17.4: Ped. II catches up with Ped. I's B♭ in the 7-beat canon. The doubling is the octave canon
    itself.
  - b52.1: the line-7 canon on D in both pedals, under the E♭ of S7 on E♭.
  - b65.2: RP Bar's S9 answer ends on A2 as the line-9 cantus reaches A2. The critic reads F7 because of
    Ped. I's E♭.
  - b71.3: the cantus A3 against RP A's S2, as B♭maj7.
  - b72.2: F in HW Bar (S6), OW A (S7) and HW S1, as Gm7/D.
  - b73.4: G in HW B (S7) and OW S (S8), as Am7/C.
- **Low-register seconds (7):**
  - b4.2: S1 against A1.
  - b51.4: Ped. II against HW B's S7.
  - b56.3: S8 against the cantus E.
  - b64.3 and b64.4: RP Bar's chromatic S9 against Ped. I.
  - b66.2: the line-9 pedal canon, E♭2 against D3.
  - b69.4.25: the BWV 542 guest's C3 against Ped. II's upbeat D2.
- **Unresolved dissonances: none.** The critic still lists notes of the kind "chord (7th not resolved
  down)", mostly sevenths that pass to another chord tone in a thick texture.
- **Augmented seconds (10).** All are the B♭–C♯ of line 6 ("Orgeln") or its answer F–G♯, in S6 and in
  the line-6 cantus.

## 9. Weak spots, and what I would still improve

- **The summit falls just short of its density target.** Bars 71-73 have 14 moving voices; b74 has 13 and
  b70 has 11. The summit mean is 13.2 (13.8 over b71-74), against a target of ≥ 14.
  - At most 13 voices sound at one moment.
  - Further lines were tried in b70 and b74. At b70.3 every line that moved B♭→A made octaves with OW B and
    HW T, and every G→A made octaves with the pedal. In b74, any C or F♯ doubled the seventh or the
    leading tone of the D7. I left those bars as they are rather than pad them.
- **The summit is short.** It is five bars (about 18 s), because line 10 in augmentation lasts five bars.
  A second, slower statement of line 10, or a longer approach, would give it more weight.
- **The rest of the texture is thin.** Outside the summit, 3-5 voices move per bar (the whole-piece mean
  is 5.0).
  - Each line is worked mainly by one division plus the pedals, as in Reincken's fantasia, so seventeen
    voices are heard only at the end.
  - Lines 1, 6 and 9 are the thinnest.
- **Length.** The piece is 78 bars and 4:31, a little under the brief's 80-110 bars and about five
  minutes.
- **There is little stylus phantasticus between the lines.** It amounts to one echo passage (b21-23), one
  general pause (b47) and one harp solo (b48). There is no free toccata episode and no chromatic surge
  between lines apart from subject 9 and OW A's rise into the arrival. One or two short free episodes
  would make the fantasia side more audible:
  - a passaggio over a pedal point after line 2;
  - a chromatic surge before line 9.
- **The coda thins out, then jumps to the full chord.** After the arrival (9 moving voices) the coda drops
  to 5-6 moving voices over the tonic pedal, and all seventeen then enter on the final chord. It is meant
  as the full organ's last chord, but it is a large jump. A two-bar build-up would be smoother.
- **Bad doublings are at the limit (8),** all thematic or canonic. Crossings are frequent (28), mostly OW A
  above RP S and HW S1 above OW S in the summit.
- **The score is hard to read.** Two A2 pages hold 78 bars, many to a system.
- **I have not heard it.** I cannot say:
  - whether the pedal canon is audible under the manuals;
  - whether the BWV 542 guest is recognisable two octaves down;
  - how long the general pause feels;
  - whether seventeen voices on a General MIDI organ balance at all.

  These need a listener.
- **No Prelude XVI.** The optional stylus-phantasticus Fantasia, alluding to the opening of BWV 542's
  Fantasia, was not written; the time went into the fugue's summit.
