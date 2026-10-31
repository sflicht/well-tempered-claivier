# Pair XIV in F-sharp minor: review of the five-voice recomposition

**Scope.**
- `fugue.py` → `fugue.json`: *Ricercar a 5 sopra il Thema Regio*, 78 bars of 2/2.
- `prelude.py` → `prelude.json`: the new Prelude XIV, *Canon cancrizans a 3*, 17 bars.
- `NOTES.md`.
- For comparison, `archive-n-plus-1/` (fifteen voices) and its REVIEW-2.

**Method.**
- I read every bar of both scores as the literal bar strings in the JSON, voice by voice, with the declared entries marked.
- I ran `critic.py` and `reduce.py --per beat`.
- Scratch scans:
  - per section: notes per bar, eighth slots attacked, onsets where three or more voices attack together, note-value histogram;
  - for each entry: its place in the texture and what attacks with it;
  - real times from `renders/fugue.mid`.
- Fixes marked **tested** were built from scratch copies of `fugue.py` / `prelude.py` and checked with `critic.py`: no new flags unless stated.
- I have not heard the renders.

## Verdict

**Main question: mostly yes.** The counterpoint is clean and the entries are staged well.

**Entries.**
- The theme alone, then the answer, then the trio.
- The Quintus enters with the answer at 32.3 into a full stop: Cantus, Altus and Tenor all rest on that beat.
- Every per-tonos dux and comes enters after a rest in its own voice.

**The three devices** come across on one piano to different degrees.
- **Canon per tonos (b44–61):** the most audible device of the four recomposed fugues.
  - The same canonic block returns a tone higher, C → D → E, and then comes home on F♯ over the augmentation.
  - Its top note climbs C5 → D5 → E5 → F♯5 without a break.
- **Canon per augmentationem et contrario motu (b22–42):** heard only in part.
  - The bass's inverted head (C♯3 A2 F♯2 E♯2 D3, whole notes) sounds as a bass line, not as the theme.
  - The device becomes audible at b35–38. There the Quintus's answer falls chromatically (G♯4 G4 F♯4 … C♯4) while the comes rises chromatically beneath it (A♯2 B2 B♯2 C♯3 D3).
- **The summit (b62–75):** clear.
  - The augmentation in the bass is the only whole-note line.
  - Above it the per-tonos pair returns in crotchets and the inversion climbs.

**What will disappoint is pacing and arrival.**
- In the fugue, 117 s pass before the first crotchet-based texture (b44, 2:01). Add the prelude, which also presents the theme on top in half notes at ♩ = 69: the pair spends about three minutes in half-note Royal Theme music.
- The per tonos is one block played three times in identical crotchet homophony.
- The summit's top note is an eighth in passing.

## Ranked issues

| # | Mvt | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|---|
| 1 | Pair | Prelude 1–9; fugue 1–42 | The prelude's top voice is the theme in half notes at ♩ = 69; the fugue then opens with the theme alone in half notes at ♩ = 84, and stays in half-note motion until b44 (2:01) | **Medium-High** | **Tested.** Prelude: exchange the upper voices (theme hidden in the Altus, then backwards on top). Fugue: tempo map ♩ 84/88/92/96 → 92/96/100/104 (about 3:15) |
| 2 | Fugue | 44–61 | Per tonos: three identical six-bar blocks, all four voices in crotchets (66–69 % of onsets have three or more voices attacking together); doubled leading tone at 45.1, 51.1, 57.1 | **Medium** | **Tested.** Block 1 without the tenor; tenor's second bar `B3:8` → `G3:8`; the blocks grow 3 → 4 → 5 voices as the canon rises |
| 3 | Fugue | 73–78 | The summit's peak F♯6 is an eighth inside the inversion's run (73.4½); the top then sinks C♯6 D6 C♯6 B5 A♯5 under the ritardando | **Medium** | **Tested.** Cantus b75 `C#6:8 D6:8` → `C#6:8 D6:4 F#6:4` |
| 4 | Fugue | 70–75 | Summit low register: the tenor strikes C♯3 six times over the augmentation's chromatic descent, under the Quintus (E3–B3); a bare G2/C♯3 tritone at 73.1 | Low | **Tested.** Tenor b73 `C#3:8 R:4 C#3:4` → `R:16` |
| 5 | Fugue | 76–78 | The cadence is i6 – iv4/2 – vii°6/5 – V4/3 – I: no root-position dominant, because the bass is the augmentation's last notes A–G♯–F♯ | Low | Keep it: it is the conceit, and it reads as a quiet, inevitable close |

---

## Fugue XIV

### Must not be touched

- **The exordium, b1–21.** The theme alone, the tonal answer under the syncopated "Ascensus", and the trio with "Descensus". It is idiomatic stile antico, and the earlier review rightly asked to keep it. The tempo fix below leaves its notes alone.
- **The pivot b43 and the per-tonos entries.**
  - C♯7 becomes G7♭9 with three common tones, a tritone shift into the King's own key, at Frederick's own pitch.
  - The two-bar canon at the octave in which the dux rests for the comes' last two bars, and the comes for the dux's first two.

  This is the clearest canon staging in the cycle so far.

### 1. Half-note music for three minutes (Medium-High)

**Timings from the render.**

| Bars | Section | Duration | Surface |
|---|---|---|---|
| 1–21 | exordium | 60 s | 1–3 voices, halves and wholes |
| 22–42 | canon per augmentationem | 57 s | halves and wholes; 30–36 % of eighth slots attacked; 54–59 % of onsets with 3+ voices together |
| 44–61 | per tonos | 47 s | crotchets |
| 62–78 | summit and cadence | 45 s | crotchets and quavers over whole notes |

**Before the fugue.** The prelude (1:03) is built on the same theme. Its first half puts the theme on top in half notes at ♩ = 69.

**Why it fails.**
- ♩ = 84 in 2/2 is a minim of 42, slow for alla breve.
- By the time the per tonos starts, the listener has heard the King's theme in half notes six times (prelude, Altus, Tenor answer, Bassus, Cantus dux, Quintus answer), plus the comes in whole notes.
- The design, *grave e poi animato*, is right. The grave part is simply too long for its material.

**Fix, fugue (tempo only; the exordium's notes stay).**

```
TEMPO = {'tempo_map': [[q(1), 92], [q(21), 92], [q(22), 88, 'ramp'], [q(22), 96], [q(42), 96],
                       [q(43, 3), 78, 'ramp'], [q(44), 100], [q(61), 100], [q(62), 104, 'ramp'],
                       [q(75), 104], [q(77), 80, 'ramp'], [q(78, 3), 60, 'ramp']]}
```

- The acceleration from section to section stays.
- The fugue shortens from 3:33 to about 3:15.
- The per-tonos crotchets at 100 and the summit's quavers at 104 are still comfortable.

**Fix, prelude:** see the Prelude section. It removes the first statement of the theme on top.

### 2. Per tonos: one block, three times, in crotchet homophony (Medium)

**What is written.**
- `BLOCK` is stated three times with all four voices transposed: C, D, E minor.
- Only the Quintus's six beats at 60.3 differ.
- Dux, comes, tenor and bass all move mainly in crotchets (62 of 86 notes in a block). Two thirds of all onsets are three or more voices attacking together.
- In the block's second bar the tenor doubles the dux's leading tone over the dominant: B4/B3 at 45.1, C♯5/C♯4 at 51.1, D♯5/D♯4 at 57.1.
- **Inherent, keep:** the octave between dux and comes on k4.1 (47.1 and so on) comes from the canon at the octave two bars apart.

**Why it matters.**
- Exact repetition *is* the canon per tonos, and the rise is audible.
- But the free voices repeat too, so the passage sounds like a sequence copied twice rather than something growing. The motto says "ascendat Gloria Regis".
- The earlier review asked for the same thing: let later statements *add* lines rather than re-score the block.

**Fix (tested).** Two small changes in `fugue.py`:

```
    for v, toks in BLOCK.items():
        if k == 0 and v == 'T':          # block 1: the King's theme, its comes and the bass only
            continue
```

```
'T': ("G3:8 C4:4 B3:4 B3:8 C4:4 D4:4 ...
→
'T': ("G3:8 C4:4 B3:4 G3:8 C4:4 D4:4 ...      # no doubled leading tone in the block's bar 2
```

**Result.**
- Block 1 (C minor, Frederick's pitch) is three voices: the theme in diminution over the bass, then its comes. It is transparent.
- Block 2 adds the tenor.
- Block 3 adds the Quintus (60.3, as now).
- The summit has five voices.

**Critic.**
- parallels 0 / 1 / 1 (unchanged);
- unresolved 0;
- bad doublings 0;
- mean moving voices 3.51 → 3.44.

**Further, untested.** `CS1D` (countersubject I in diminution) is defined in `fugue.py` and never used. It is the natural extra line for block 3's tenor, if a stronger growth is wanted.

### 3. The summit's peak is not an arrival (Medium)

**What is written.**
- The inversion in diminution climbs `A#5:6 B5:2 B#5:2 C#6:2 D6:2 F#6:2` and turns straight back `C#6:2 G#5:2 …` (b73–74).
- F♯6, the highest note of the piece, lasts an eighth: about 0.3 s.
- After the inversion the top line is `C#6:8 D6:8 | C#6:8 B5:8~ | B5:16 | A#5:16`, falling through the ritardando.

**Fix (tested).** One more F♯6, held, at the start of the ritardando:

```
SUMMIT['C'] bar 75:  'C#6:8 D6:8'  →  'C#6:8 D6:4 F#6:4'
```

- At 75.4 F♯6 sounds over B minor (B2 B3 F♯5; D6 sounded on the beat before).
- It falls a fourth to C♯6 over A2 (i6) at 76.1.
- The run's fleeting peak thus returns as a held peak just before the cadence.
- No new flags in b73–78.

### 4. Low register in the summit (Low)

**What is written.**
- The augmentation: A♯2, A2, A2–G♯2, G2–F♯2, E♯2–C♯2 (b70–74).
- The tenor: C♯3 struck six times in b70–75 (`C#3:16`, `C#3:16`, `D3:16`, `C#3:8 R:4 C#3:4`, `C#3:16`, `C#3:8 R:8`).
- The Quintus: E3–B3.
- Nothing between C♯4 and A4.

**Why it matters.** Each new augmentation note is struck together with the same C♯3 a third or fourth above it, so the chromatic descent is heard as a chain of dyads. At 73.1 the augmentation's G2 sounds against C♯3 as a bare low tritone.

**Fix (tested).** Rest the tenor in b73: `'C#3:8 R:4 C#3:4'` → `'R:16'`. G2–F♯2 then sound under the Quintus's A♯3–A3 alone. No new flags.

### 5. The cadence (Low; keep)

The augmentation's last notes A2–G♯2–F♯2 make the bass step down into the tonic. A root-position dominant is therefore impossible without breaking the conceit. With the tempo map's broadening and the Picardy A♯5 on top, it should sound like a quiet, inevitable close.

---

## Prelude XIV: *Canon cancrizans a 3*

The construction is exact and clean: the critic finds nothing, and the palindromic bass works. As music it is a modest, slow riddle (1:03).

### Must not be touched

The palindrome: the bass is its own retrograde, the turn falls at 9.3, and the second half is produced by `retrograde` and nothing else.

### P1. It pre-empts the fugue's opening (Medium-High, pair level)

**What is written.**
- The first half's top voice is the King's theme, `F#5:8 A5:8 C#6:8 D6:8 …`, in half notes at ♩ = 69.
- The fugue then opens with the same theme alone, in half notes at ♩ = 84.
- In the second half the theme runs backwards in the Altus. As NOTES says, a listener will not recognise it, except for its chromatic line.
- The top voice ends on A5 over a plagal close.

**Fix (tested).** Publish the canon's other reading. Read backwards, the piece is itself with the upper voices exchanged, so exchanging them is musically guaranteed. In `prelude.py`:

```
top = THEME + ' ' + W.transpose(W.retrograde(LINE), 12, 7)
mid = LINE + ' ' + W.transpose(W.retrograde(THEME), -12, -7)
→
top = W.transpose(LINE, 12, 7) + ' ' + W.retrograde(THEME)
mid = W.transpose(THEME, -12, -7) + ' ' + W.retrograde(LINE)
```

The entries change accordingly: the theme in the Altus at b1, the cancrizans in the Cantus at b9.3, and `subject` = the theme an octave lower.

**Result.**
- The critic summary is identical: every count is the same; only the positions of the flagged sevenths move.
- **First half:** the counter-line is the tune on top, and the King's theme is hidden in the Altus. "Quaerendo invenietis" is now literal.
- **Second half:**
  - the theme backwards is on top, so its rising chromatic line F♯5 G5 G♯5 A5 A♯5 B5 B♯5 C♯6 (b12–15) becomes the prelude's climax;
  - the top voice ends `D6:8 C#6:8 | A5:8 F#5:8`, on the tonic.
- **The join:** the prelude ends with the theme's head backwards (D C♯ A F♯), and the fugue begins with it forwards (F♯ A C♯ D). The crab hands the theme to the ricercar.

### P2. Reversed harmony (Low)

**What is written.** In the second half, progressions run backwards: V → iv → III → i at the end, and sevenths are approached by step and left by leap.

**Assessment.** This is inherent and well documented. The exchange in P1 does not change it, but it gives the second half a clear melodic goal on top.

---

## Better than the fifteen-voice version?

**Yes.**

| | 15 voices | 5 voices |
|---|---|---|
| keyboard unplayable | 41.6 % | 1.4 % |
| crossings | 37 | 1 |
| pitch class tripled on beats | 56 % | 1.7 % |
| low-register seconds | 8 | 0 |

**The three faults the earlier review named are fixed:**
- the per-tonos comes no longer shadows the dux in thirds; it enters two bars later at the octave, after a rest;
- the per-tonos climb no longer drops an octave halfway;
- the summit is no longer whole-note pads at a slowing tempo: the augmentation is the only long-note line, and the tempo rises into it.

**What remains of the old faults** is proportion (issue 1) and the block repetition (issue 2), both much reduced.
