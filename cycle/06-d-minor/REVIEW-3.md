# Fugue VI in D minor (a 4, *Passacaglia e fuga sopra il Crucifixus*): third review

**Scope.**
- `fugue.py` → `fugue.json`: 64 bars of 3/4, four voices.
- `NOTES.md`; `archive-n-plus-1/` (the seven-voice version) for comparison.
- The prelude is unchanged and not reviewed here (see `REVIEW-2.md`).

**Method.**
- I read every bar from the literal bar strings.
- I ran `critic.py` and `reduce.py --per beat`.
- Scratch tools, not kept: a quarter-note attack grid of the summit, and velocities per voice per bar.
- Fixes marked **tested** were built from a scratch copy of `fugue.py`, with the repository's `tools/` linked in, and checked with `critic.py`. They add no new flags unless stated.
- Positions are bar.beat in quarters. I have not heard the renders.

## Verdict

**Main question: yes for the ground and the fugue; only partly for the speeds.**

**The ground in every voice: yes.** Each station starts after silence in its voice, in an outer position:
- Bass, alone for two bars;
- Tenor, as the lowest voice (the bass is silent b9–16);
- Alto, as the top voice over the tenor alone (b21–24);
- Soprano at A5 (b45).

The stations also climb in register (D3 → A3 → F4 → A5), so a listener hears the lament rise through the texture, which is the point of the piece. The voicing pass (+7 for the station's voice, −3 for the others) supports it.

**The fugal entries are all after rests and clean.** The critic finds 0 parallels, 0 unresolved, 0 crossings and 0 % unplayable, and 9 or 8 of 9 intervals match in every entry.

**The three speeds: not as written.**
1. **The station pairs** (b3–4, b11–12, b23–24): the inversus moves with the ground in compound sixths or tenths, in the same rhythm for three notes. It sounds like the lament harmonised, and becomes "the ground at double speed" only when it reaches its cadence figure a bar early. NOTES says so. I tested a one-beat offset in Station I; it makes parallel fifths at b5.3, so I leave the pairs alone.
2. **The summit's outer voices** (b45–50), the combination NOTES singles out as the one a listener will hear, move **in rhythmic unison**. See issue 1. This is the main problem, and it has a clean fix.
3. **"Three speeds at once" (b49.3–52.3)** is on paper only. There the soprano holds E5 for two bars and the bass holds G2, then A2; only the tenor's inversus moves. What is heard is a tenor chromatic descent under two held notes.

## Ranked issues

| # | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|
| 1 | 45–50 | The soprano's ground and the bass's ×2 change notes together at 45.1, 46.2, 47.1, 47.3, 49.3 and 50.2: two speeds heard as one line in sixths | **High** | **Tested:** the soprano enters a beat later and catches up on its long E (a chain of 7–6 suspensions) |
| 2 | 41.1–3 | The tenor's inversus (the ground ×½) enters under the alto, which moves with it a 3rd–4th above in the same rhythm | Medium | **Tested:** the alto holds its D5 two beats and rests a beat (`D5:8 R:4`) |
| 3 | 49.3–52.3 | "Three speeds" is on paper: two of the three are sustained notes | Low-Medium | No note fix; describe it as the tenor's descent under the two grounds (NOTES, listening guide) |
| 4 | 51.3–55.2 | The bass's augmented A2 is held 16 beats, about 13 s at ♩ = 70 → 56, under the cadential 6/4. On a piano it is gone long before the cadence | Low | Optional: re-strike A2 at 53.1 in the performance data, or accept |
| 5 | 3–4, 11–12, 23–24 | The station pairs sound like harmonised laments | Low | Leave (offset tested: parallel fifths at b5.3) |

The tested fixes 1 and 2 together:
- 0 errors and 0 warnings, as now;
- suspensions 5 → 10;
- stepwise 67.0 → 66.9 %;
- keyboard still 0 %.

---

## Must not be touched

- **Station II's texture, b9–16.** The bass is silent, so the tenor's ground in A minor is the bass of the texture. It is the clearest "ground in another voice" in the piece.
- **The coda's rising augmented subject in D major, b57–64.** The lament turned upside down at its own speed, over a D pedal, with iv6/4, IV6/4 and V7/IV colours from the alto's F♯–G turns. It is the piece's argument (Crucifixus → Et resurrexit), and it is audible.
- **The bass's one-beat rest before the summit (b40)** and the alto's scale into it.

## 1. The outer voices move together (High)

**What is written.** A quarter-note grid of b45–50:

```
pos     S     A     T     B
45.1   A5     .     .    C3
46.2  G#5     .    B3    B2      <- together
47.1   G5    D4    G3   Bb2      <- together
47.3  F#5   Eb4    C4    A2      <- together
48.1   F5    E4    C4     |
48.2   E5    F4   C#4     |
49.2   F5    A4     .     |
49.3   D5    G4    D4   Bb2      <- together
50.2   E5     |   C#4    G2      <- together
```

- The ground's opening durations (D 16, C♯ 8, C 8 sixteenths) are the same as those of its ×2 from the third note on (C 16, B 8, B♭ 8). A ×1 started at the moment the ×2 reaches C therefore changes note **with** it: A5/C3, G♯5/B2, G5/B♭2, F♯5/A2, all compound sixths.
- The search that chose this placement (`summit_outer.py`, cost 0) rewarded exactly this: consonance on every attack.

**Why it fails.**
- The climax of the passacaglia is "the ground at two speeds in the outer voices". For 2½ bars it is heard as one chromatic line harmonised in sixths.
- The speeds separate only at 47.3–48.3, where the soprano moves F♯–F–E over the bass's held A2, and again for one note each at 49.3 and 50.2.

**Fix (tested).** Enter the soprano a beat later and give back the beat on the ground's long A (E5:12 → E5:8). The rest of the summit is unchanged from 49.2.

```
put(SU + 4, S=last_octave(G('A5'), 1) + '  F5:8 G5:4  Bb5:8 A5:4  G5:4 E5:4 F#5:4~  F#5:8 R:4')
entry('S', SU + 4, 'Ground (Soprano), at the dominant, over its augmentation', n=8)
→
put(SU + 4, S='R:4 A5:16 G#5:8 G5:8 F#5:4 F5:4 E5:8 F5:4 D5:8 E5:24 A5:8'
              '  F5:8 G5:4  Bb5:8 A5:4  G5:4 E5:4 F#5:4~  F#5:8 R:4')
entry('S', SU + 4, 'Ground (Soprano), at the dominant, over its augmentation', beat=2, n=8)
```

**What it gives.**
- **A chain of suspensions**, the Crucifixus's own idiom, in which the two speeds are audibly different:
  - 46.2: A5 over B2 (7) → 46.3 G♯5 (6);
  - 47.1: G♯5 over B♭2, with the alto's D4 entering, B♭–D–G♯: an Italian sixth → 47.2 G5 (6);
  - 47.3: G5 over A2 (7) → 48.1 F♯5 (6).
- **The soprano's A5 enters on beat 2**, after a beat of the bass's C3 alone (it was C♯3 a beat before).
- **Critic:** no new flag; suspensions 5 → 10. The ground's long A loses a beat (rhythm 8/9 for this entry), the only price.

**Rejected variants.**
- The one-beat delay without catching up: parallel fifths E5/A2 → F5/B♭2 at 49.3.
- A two-beat delay: parallel fifths F5/B♭2 → D5/G2.
- A one-beat anticipation: an augmented fifth G♯5/C3 on the downbeat of b46.
- An eighth-note delay: clean, but it turns the whole soprano ground into syncopation.

## 2. The tenor's entry under the alto, b41 (Medium)

**What is written.**
- Alto `D5:6 C#5:2 B4:4 | C#5:4 D5:4 C#5:4`, tenor `A4:8 G#4:4 | G4:4 F#4:2 F4:2 E4:4`.
- The alto sits a 4th, then a 3rd, above the tenor and moves on the same beat (41.3: B4 over G♯4).
- The soprano (F5, E5) is a 6th above that.
- NOTES's own weak spot: the inversus "may be heard as an inner voice of the chords".

**Fix (tested).** Alto b41: `D5:6 C#5:2 B4:4` → `D5:8 R:4`.
- The alto's scale (b40) still lands on D5, which it holds while the tenor's A4 → G♯4 starts the descent. At 41.3 it gets out of the way, and it comes back at b42.1 on C♯5.
- At 41.3 the chord is E/D (D3 G♯4 E5), the same V4/2 as now.
- Critic: clean.
- Resting the alto for the whole of b41 was also clean, but it leaves the alto's leading tone (C♯5 at 40.3) unresolved.

## 3. "Three speeds at once" (Low-Medium)

- In b49.3–52.3 the soprano's ground is on its long E5 (two bars), and the bass's ×2 is on B♭2 → G2 → A2, a note every 1⅓ bars. Only the tenor's inversus (`D4 C#4 C4 B3 Bb3 A3`) moves.
- The alto's subject ends there with the leap G4 → D5 (50.3), against the soprano's E5: a bare major second over C4 and G2.
- Nothing needs changing. But the listening guide should point to b45–48 (after fix 1) for "two speeds", and present b49–52 as the tenor's descent under the two grounds, not as three audible speeds.

## 4. The held A2 (Low)

- The augmented ground's A2 lasts from 51.3 to 55.2, through the cadential 6/4 (b53) and the A7(♭9) with the soprano's B♭5 (b54).
- With the summit at ♩ = 70 slowing to 56, that is about 13–15 s, and a piano's A2 will be inaudible by the time V resolves at 55.3.
- On the organ (the spatial render) this is no problem.
- For the piano render, re-striking the A2 at 53.1 would need a token split (`A2:48` → `A2:20 A2:28`) and costs the critic's 9/9 on that entry. I would accept the decay rather than do that.

## 5. The station pairs (Low)

- In b3–4, b11–12 and b23–24 the inversus starts on the same downbeat as the ground's C (or its equivalent) and moves with it for three notes in sixths or tenths. NOTES describes these as tenths and as "D C♯ C against A G♯ G"; the grid shows compound sixths against C–B–B♭ in b3–4.
- I tried the alto's inversus a beat late in Station I. It gives parallel fifths F4/B♭2 → D4/G2 at b5.3, so I would leave the pairs as they are.
- After fix 1, the summit's offset makes the contrast: the stations show the ground harmonised, and the summit shows it split.

## Better than the seven-voice version?

**Yes.**

| | a 7 (archive) | a 4 (now) |
|---|---|---|
| keyboard unplayable | 23.8 % | 0.0 % |
| pc tripled on beats | 26.6 % | 5.4 % |
| stepwise | 62.8 % | 67.0 % |

- **The ground's stations are audible.** Before, three were inner voices in long notes. Now each is an outer voice after a silence.
- **The episodes let the texture breathe.**
- **The coda has a meaning:** the lament rising. It was B-A-C-H garnish.

The summit's best idea, the two grounds in the outer voices, was kept from the earlier version. With fix 1 it becomes what NOTES says it is.
