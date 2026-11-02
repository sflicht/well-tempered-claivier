# Pair XIX in A major: review of the four-voice recomposition

**Scope.**
- `fugue.py` → `fugue.json`: *Ballo a quattro*, 176 quarters (44 bars of the 4/4 master metre). Four voices, one dance each:
  - sarabande (soprano, 3/4);
  - allemande (alto, 4/4);
  - gigue (tenor, 12/8 with dotted quarter = quarter);
  - courante (bass, 3/2).
- `NOTES.md`.
- For comparison, `archive-n-plus-1/` (twenty voices in four bands).
- The prelude is unchanged and not reviewed here.

**Method.**
- I read every voice's literal bars, with the declared entries marked.
- I ran `critic.py` and `reduce.py --per beat`.
- Scratch tools (not kept):
  - an onset list per quarter, which shows triplet and sixteenth positions in each voice side by side;
  - real times integrated from `metadata.tempo_map`.
- Fixes marked **tested** were built from a scratch copy of `fugue.py` and compared with the current build by `critic.py`: no new flags unless stated.
- Positions are absolute quarters (q). I have not heard the renders.

## Verdict

**Main question: yes for clarity. Partly for the device.**

**The exposition (q0-48) is a model of clarity.**
- The allemande is alone.
- The courante's answer enters under it.
- The sarabande enters on top while the allemande rests (q20½-25¾).
- The gigue's answer enters over the bass alone (q39⅔).
- Each dance's rhythm is presented before it has to compete.

**Each dance is recognisable by its rhythm in the ball (q120-156, 1:45-2:16).**
- **The allemande:** running sixteenths with eighths on the beats, B4-F♯5.
- **The gigue:** long-short triplets, E3-G♯4. Three against the allemande's four in every beat, an octave lower: two streams, not a blur, on paper.
- **The sarabande:** long notes on top, with the weight on beat 2: A5 C♯6:2 (q126), B5 G♯5:2 (q132), A5 F♯5:2 (q135).
- **The courante** is the weakest: for its first eleven quarters it is a plain quarter-and-half-note bass (issue 3). Its dotted half-beats and hemiola appear only with its subject (q131).

**"Four dances in four metres at once" is heard as two metres, each in two guises.**
- The gigue's 12/8 bar is four quarters, the same as the allemande's 4/4, and `accent()` gives both the same accents (+4 on the bar, +1 on its third quarter). Their bar lines always coincide.
- The courante's 3/2 bar lines are a subset of the sarabande's 3/4 bar lines.
- So what the ear can follow is:
  - duple bars (allemande and gigue: straight against triplet subdivision);
  - against triple bars (sarabande and courante: 3/4 against 3/2 with hemiola).
- That is still a real polymetre, and it is the only way four dances can share one pulse. NOTES should not claim more.

**Subject entries.** All are heard except the gigue's two in the ball (q125⅔, and q143⅔, the race), which are hidden in the gigue's own figuration (issue 1).

## Ranked issues

| # | q | Problem | Severity | Minimal fix |
|---|---|---|---|---|
| 1 | 124-126, 142-144 | The gigue's ball entries are preceded by a single triplet-eighth rest and have the same long-short rhythm as its free figures, under the allemande's sixteenths. The race reads as an allemande flourish | Medium | **Tested:** the tenor rests 1⅔ beats before each entry |
| 2 | 156-176 | The convergence is four chords. Only the allemande and the courante dance the bourrée; the sarabande and gigue enter at q168 for IV – ii6 – I6/4 – V7 – I and a held A | Medium | Not tested: bring sarabande and gigue into the bourrée before q168 (see below) |
| 3 | 120-126 | The courante's free bass at the start of the ball (`A2:8 C#3:4 D3:4 E3:8`) has no courante rhythm, so the ball begins with three recognisable dances | Low-Medium | **Tested:** `A2:6 B2:2 C#3:6 D3:2 E3:8` |
| 4 | 48-99 | Two voices for 51 quarters (0:42-1:26): the quick duet, then the slow duet. Four voices sound together only at q45-48 and from q120 | Medium-Low | Not tested: let the gigue slip in at q93 instead of q99, softly, under the sarabande's subject |
| 5 | whole | Stepwise motion 63.2 % (target 65): the courante is 27 % leaps | Low | Leave; it is the dances' nature (NOTES) |

---

## Must not be touched

- **The exposition, q0-48.** Each dance enters alone or over one partner, in suite order. The sarabande's entry with the allemande silent and the gigue's over the bass alone teach the listener the four rhythms the ball depends on.
- **The ball's last six quarters, q150-156.**
  - The courante's hemiola cadence `C#3:8 D3:4 E3:12`.
  - Over it, the sarabande's suspended A5 resolving to G♯5 on its weighted beat 2, then all four on A at a common bar line.
  - It is the one place where three of the dances' identities (hemiola, beat-2 weight, triplets) coincide in a single cadence.

## 1. The gigue's entries are hidden in the ball (Medium)

**What is written.** The tenor dances continuously from q117 to q149:

```
q120  A3:8/3 B3:4/3 D4:4/3 C#4:4/3 B3:4/3 A3:8/3 G#3:4/3 F#3:8/3 G#3:4/3 A3:8/3 B3:4/3 G#3:4/3 R:4/3
q125⅔ subject (D level)  A3 | D4 C#4 E4 D4 F#4 E4 G#4 F#4 E4 C#4 D4 B3 | A3
…     A3:8/3 E4:4/3 A3:8/3 E4:4/3 B3:4/3 R:4/3
q143⅔ subject (A), the race
```

- Before each entry there is one triplet-eighth rest (about 0.3 s).
- The entry has the same long-short rhythm and the same register as the free figures around it.
- Above it the allemande runs in sixteenths.
- NOTES says "each statement enters after a rest in its own voice". For the gigue, the rest is too short to hear.

**Why it fails.**
- The gigue's subject can be told from its own counterpoint only by contour.
- The race (q143⅔-150, 2:05) depends on hearing two statements of one tune at two speeds:
  - the allemande's, a fifth higher, enters 2¹⁄₁₂ beats later and catches up;
  - without the gigue's, the listener hears the alto rising to A5 alone.

**Fix (tested).** Silence the tenor for 1⅔ beats before each entry:

```
… F#3:8/3 G#3:4/3 A3:8/3 B3:4/3 '
                  'G#3:4/3 R:4/3')
→ … F#3:8/3 G#3:4/3 R:4 R:8/3')                 # tenor silent q124 - q125⅔

… A3:8/3 E4:4/3 A3:8/3 E4:4/3 B3:4/3 R:4/3')
→ … A3:8/3 E4:4/3 R:4 R:8/3')                   # tenor silent q142 - q143⅔
```

- The harmony is complete without the removed notes: A/E → E7 at q124-125 (sarabande, allemande, courante); A → E7 at q142-143.
- Critic: no new flags. One "7th not resolved down" note (q125) disappears.
- The entry boost (+6) then works on an entry that starts out of silence.

## 2. The convergence is four chords (Medium)

**What is written.**
- After the ball's last chord (q156, held) the allemande plays Bach's bourrée alone (q157½), and the courante joins with Bach's left hand in sixteenths (q161½). These two dancers really do change into the bourrée's metre.
- The sarabande and the gigue are silent from q157½ to q168. They return only for four quarter-note chords:
  - S `D6 B5 A5 G#5`, T `A3 D4 C#4 E4`;
  - harmony IV – ii6 – I6/4 – V7 – I;
  - then a held A (2:27-2:36).

**Why it matters.**
- The plan's last step is "all four voices dance that bourrée in one metre". As written, two of the four dances never dance it.
- The moment where four metres become one is a homophonic cadence: the listener hears an ending, not a convergence.
- The artistic direction asks that the final convergence carry force because the listener "can recognize what has changed".

**Suggestion (not tested).**
- Let the sarabande enter at q164 (bourrée bar 4) with the bourrée's head in minims a tenth above the allemande. Let the gigue enter at q166 with the head's first five notes in straight eighths: the gigue giving up its triplets is the change a listener can hear.
- Or extend the coda by one bourrée bar (2 quarters) in which all four play the head in imitation, a quarter apart, before the IV chord.
- Either needs its own counterpoint check: the courante is in the tenor register (A3-E4) at q162-168.

## 3. The courante starts the ball without a courante (Low-Medium)

**What is written (q120-131).**

```
A2:8 C#3:4 D3:4 E3:8 F#3:4 C#3:4 E3:4 B2:4 R:4
```

- These are plain halves and quarters. The sarabande enters on top at q122, the gigue and allemande are already dancing, and the bass is just a bass.
- The courante's identity (dotted half-beats, hemiola) appears only with its subject at q131 (1:54).

**Fix (tested), the first courante bar only.**

```
'A2:8 C#3:4 D3:4 E3:8 F#3:4'  →  'A2:6 B2:2 C#3:6 D3:2 E3:8 F#3:4'
```

- This is [A. B][C♯. D][E], the rhythm of the courante subject's first bar, so all four dances are present from q120.
- Critic: no new flags (one passing note now classed as a retardation).
- Combined with fix 1: no new flags; stepwise 63.2 % → 63.6 %; keyboard 2.6 % → 2.2 %.

## 4. The long two-voice middle (Medium-Low)

**What is written.**
- q48-71: the quick duet (gigue and allemande, F♯ minor, C♯ minor).
- q71-99: the slow duet (courante and sarabande, B minor, D), marked −5 in velocity.
- The gigue slips in at q99. The soprano then rests from q104 to q122.
- Four voices sound together only at q45-48 and from q120 (1:45). Nearly three quarters of the piece (about 128 of 176 quarters) has three voices or fewer.

**Assessment.**
- The duets are useful: each shows two metres against each other before the ball (12/8 over 4/4, 3/4 over 3/2).
- The slow duet (25 s of halves and quarters, two voices, soft) is the risk.
- **Suggestion (not tested).** Let the gigue enter softly at q93, under the second half of the sarabande's subject in D, rather than at q99. That makes the slow duet a trio for its last bars and announces the trio section.

## Smaller points

- **The race's alignment.** The gigue ends E3 at q149 and the allemande B4 at q149½: they end together on the dominant within half a beat, as NOTES says. With fix 1 the listener can hear that.
- **The sarabande's A5 (from q151) over the courante's E3 (q153), resolving to G♯5 at q154,** is the clearest dissonance-and-resolution in the ball. Keep its weight on beat 2.
- **Tempo.** ♩ = 69 makes a slow gigue (dotted quarter = 69) and a measured bourrée (minim = 69). It is right for the sarabande and the allemande. One pulse for four dances is the concept, so leave it.

## Better than the twenty-voice version?

**Yes, by far.**

| | 20 voices | 4 voices |
|---|---|---|
| weak parallels | 131 | 0 |
| unresolved dissonances | 11 | 0 |
| low-register seconds | 16 | 0 |
| crossings | 54 | 0 |
| keyboard unplayable | 48.4 % | 2.6 % |

- **The polymetre.** In the old version it was between massed bands and appeared only after q156. Now it is between single lines from the second entry on.
- **Lost:** the old version's mass at the summit. The new ball is 36 quarters (31 s) out of 176. That is why issues 2 and 4 matter: the piece builds slowly to a short ball and leaves it quickly.
