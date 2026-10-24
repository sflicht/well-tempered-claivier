# Fugue V — v3 (changes from v2)

Only Stretto I (bars 25–27) and the contrabass (bars 25–28 and 35–46) changed. Everything else is identical to v2, which I checked with a bar-by-bar diff of the source. Prelude V v1 is untouched.

## Changes by bar
- **b25–27, Stretto I (G major)**
  - In v2 this passage had 3–4 voices and cross-relations at b26–27. It now has 6 voices.
  - Entries:
    - Subject in the alto on D4 at 25.1.
    - Subject in the soprano on D5 at 25.2 (½ bar later).
    - Subject in the baritone on D3 at 25.3 (½ bar later again).
  - The countersubject is complete and literal in the tenor from 25.2, paired with the soprano. It ends C4–B3 over E3 in b27.
  - Bass: G2 | D3 G2 B2 | E3 A2 D3.
  - Contrabass: G1 pedal through b25–27¹, then F#1 under the D7 that arrives into b28.
- **b28**: the contrabass carries over (G1 for the first half), then rests as in v2.
- **b35–38 (Cb line)**: B1 G1 | A1 F#1 | B1 A#1 F#1 | D2 B1.
- **b39–41 (Cb)**: an A1 dominant pedal.
- **b42–46 (Cb line)**: A1 | D2 B1 | G1 C#2 | F#2 G2 | B1 E2.
- **b51–59**: the D2 tonic pedal under the final stretto (9 bars) was already in v2. I left it unchanged.

## Voice counts per bar (v3)
1 1 2 2 3 3 4 4 5 5 6 6 5 5 4 5 5 5 5 5 3 3 3 3 **6 6 6 5** 4 4 4 5 6 5 **5 5 5 5 5 6 5 5 5 5 5 5** 5 6 6 6 5 6 5 5 6 4 6 6 6

| Voices | v2 bars | v3 bars |
|---|---|---|
| 3 | 7 | 6 |
| 4 | 21 | 7 |
| 5 | 16 | 27 |
| 6 | 11 | 15 |

## Checkers (fugue-v_v3.check.txt)
- No unprepared dissonances.
- No parallel 5ths or octaves.
- No cross-relations (v2 had them at b26–27).
- Remaining flags:
  - m2/M7 clashes:
    - b26.1.50 tenor C4 against baritone B3, a passing tone.
    - b40.2.50 bass G#2 against the A1 pedal.
    - b56 bass C#3 against the D2 pedal (same as v2).
  - Parallel 16ths at b26.4.50, soprano and baritone.
  - Voice crossings: alto and tenor at b26.3 (the literal CS rises above the alto), and baritone and bass touching at b27.1.
- implied.py: par_bass at b29 and par_top at b35–36 and b58. These bars were not changed and the flags are the same as in v2.

## Weak spots
- b21–24 is still 3 voices.
- The Cb in b35–38 and b42–46 moves in steady half notes.
- b39–41 is a pedal, not a line.
- The tenor countersubject crosses the alto at b26.
- I have not heard the audio. The mp3 is gain-matched to v2 (mean −22.7 dB).
