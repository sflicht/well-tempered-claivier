# Pair XIII in F-sharp major: review of the four-voice recomposition

**Scope.**
- `fugue.py` → `fugue.json`: *Fuga canonica a 4 sopra il fondamento di Goldberg*, 63 bars of 3/4.
- `check_canons.py`.
- `NOTES.md`.
- For comparison, `archive-n-plus-1/` (fourteen voices).
- The prelude is unchanged and not reviewed here.

**Method.**
- I read every bar as the literal bar strings in the JSON, voice by voice, with the declared entries marked.
- I ran `critic.py` and `reduce.py --per beat`, and re-ran `check_canons.py` logic by reading the canons against their dux bars.
- Scratch scans:
  - per section: notes per bar, eighth slots attacked, onsets where three or more voices attack together;
  - for each entry: its place in the texture and what attacks with it;
  - real times from `renders/fugue.mid`.
- Fixes marked **tested** were built from a scratch copy of `fugue.py` and checked with `critic.py`: no new flags unless stated.
- I have not heard the renders.

## Verdict

**Main question: yes. This is the clearest and most varied of the four recomposed fugues.**

**The texture.**
- The texture is the Goldberg canon texture: two canonic voices over the ground. A fourth voice brings extra entries and is silent half the time (the tenor sounds 50 % of the piece).
- The ground is always the lowest voice, one dotted half note per bar, so a listener can follow it throughout.
- Every canon's comes enters either:
  - after a rest in the dux (Canons I, III, VI), or
  - in contrary motion or a contrasting rhythm (II, IV, V).
- `check_canons.py` proves all seven canons exact.

**What comes across on one piano.**
- **Canon I** (b5–8) is the clearest canon of the cycle so far. The alto repeats the subject at the same pitch while the soprano lilts in triplets above it, and then the alto takes over the triplets.
- **The quodlibet** (b55–63) is an audible joke:
  - "Ich bin so lang" in the tenor, then alone in the alto at the octave with the soprano silent (b57–58);
  - "Kraut und Rüben" on top;
  - the ground itself turning into Kraut's second phrase in the bass.
- **The climbing interval** (unison, 2nd, 3rd …) is heard as "the subject again at a new pitch". Only an analyst will hear it as a climbing series. That is true of the Goldberg Variations too.

**What will disappoint is mostly rhythm at the joins.**
- The piece stops and restarts thinly every eight bars, with a tempo change at almost every join.
- One of those tempo changes lands on the quodlibet's upbeat, so the folk tune starts limping.

## Ranked issues

| # | Bars | Problem | Severity | Minimal fix |
|---|---|---|---|---|
| 1 | 54.3¼–55.1 | "Ich bin"'s upbeat C♯3 sits inside the Adagio's ritardando to ♩ = 42: it lasts 1.0 s, and the equal dotted quavers after it 0.6 s | Medium | Tempo map: end the ramp at the F♯ chord's release and start the quodlibet there: `[162, 42, 'ramp'], [162, 76]` → `[160.5, 44, 'ramp'], [160.5, 76]` |
| 2 | 10, 18, 26, 34, 46 | Every statement ends with a full cadence and restarts with two voices, at 18 and 26 after a full stop; the tempo changes at b19, 27, 39, 47, 55 | Medium-Low | **Tested** sample elision at b18–19: tenor `B3:4 C#4:4 D#4:4~` \| `D#4:4 R:8` |
| 3 | 13–15, 30 | Two comes entries are masked: Canon II's alto crosses the dux (13.1, 14.2½); Canon IV's tenor starts in octaves with the dux (G♯4/G♯3 → B♯4/B♯3, 30.1–30.2) | Low-Medium | Voicing only: comes +6, dux −3 in b13 (alto) and b30 (tenor) |
| 4 | 55.3–56.1 | Soprano subject and tenor "Ich bin" move in octaves A♯–B–C♯ into the downbeat | Low | Leave it (see below) |
| 5 | 62–63 | Ending low and close (F♯2 A♯3 C♯4 F♯4) under a ritardando to 40 | Low | Leave it; the tune ends there |

---

## Must not be touched

- **Canon I, b3–10.**
  - The unison canon, two bars apart.
  - The dux rests a beat so the comes enters alone on the same F♯.
  - The dux's triplets, later copied by the comes.
  - The tenor's inverted entry over V7–I that pivots to B.

  This passage teaches the listener what the whole piece does.
- **The quodlibet layout, b54¾–62.**
  - Bach's own arrangement of "Ich bin": tenor, then the octave above one Bach bar later, the soprano resting so it can be heard.
  - The ground giving way to Kraut 2, three of its four downbeats being the ground's own notes.

## 1. The quodlibet starts in the wrong tempo (Medium)

**What is written.** The tempo map ends the Adagio with a ramp to ♩ = 42 at q162 (b55.1) and only then jumps to 76:

```
[156, 52], [162, 42, 'ramp'], [162, 76]
```

The tenor's upbeat `C#3:3` begins at 54.3¼ (q161.25), inside that ramp. In the render:
- the upbeat lasts 1.0 s;
- the following F♯3, G♯3, A♯3, B3 (same written value) last 0.6 s each.

**Why it fails.** "Ich bin so lang" is a dance tune with an upbeat. Played this way the upbeat belongs to the Adagio and the tune lurches into tempo on its first downbeat. The quodlibet's surprise depends on the tune arriving as a tune.

**Fix.** End the ritardando where the F♯-major chord is released (54.2½, q160.5). The dotted-quaver rest and the upbeat are then in the new tempo:

```
[156, 52], [160.5, 44, 'ramp'], [160.5, 76]
```

## 2. Eight-bar blocks (Medium-Low)

**What is written.**

| Join | What happens |
|---|---|
| b10–11 | the soprano stops (`F#5:2 R:10`); tenor and bass alone |
| b18 | all three upper voices stop on beat 1 (`D#5:4 R:8`, `B4:4 R:8`, `B3:4 R:8`); the bass holds B1 alone for two beats; the soprano begins G♯ minor alone at a new tempo (64) |
| b26 | a whole-bar G♯-major chord; the alto begins alone at a new tempo (74) |
| b34 | tenor and bass only |
| b46–47 | the alto stops; the Adagio begins alone at 52 |

Each statement lasts 20–28 s.

**Why it matters.**
- By b27 the listener can predict the pattern: cadence, stop, two voices, entry.
- Momentum accumulates only in the retransition (b35–38) and the return (b39–46).
- The Goldberg set breathes between variations too. In a single movement, though, one or two elisions would make it feel like one piece rather than a suite of short ones.

**Fix (tested), a sample at the weakest join.** Let the tenor carry the common tone D♯ from B major into G♯ minor. In `put('T', 11, [...])`:

```
'B3:4 R:8',            # b18
→
'B3:4 C#4:4 D#4:4~',   # b18
'D#4:4 R:8',           # b19
```

- The soprano's dux still enters with no other attack at 19.1, over a held D♯4 (the fifth of G♯ minor).
- Critic: no new flags (parallels 0, unresolved 0, bad doublings 0).
- A similar link at b26 (the soprano's B♯4 moving on through C♯5) would remove the second full stop. Not tested.

## 3. Two masked comes entries (Low-Medium)

**Canon II, b13–15.**
- The comes (alto, B4) enters a third *above* the dux's G♯4 for a quaver.
- At 14.2½ the alto's F♯5 is above the soprano's D♯5 (the critic's one crossing).
- In b14–15 both lines run in quavers in the same octave.
- The entry itself is audible: a dotted descent against the dux's springing tail. Its second bar is not.

**Canon IV, b30.**
- The tenor's inverted subject starts G♯3, B♯3 while the soprano plays G♯4, B♯4 on the same beats (the critic's beat-to-beat octave).
- The comes therefore sounds at first like an octave doubling of the dux. It is identified only when it keeps rising while the dux falls.

Both are built into strict canon with this subject. Bar 2 of the subject starts on the note where the comes begins. They cannot be removed without changing the canon.

**Fix.** Voicing, after `build_score` (as the pans already are): +6 for the comes and −3 for the dux in those bars.

```
for v in data['voices']:
    for e in v['events']:
        if (v['name'], e['bar']) in {('Alto', 13), ('Tenor', 30)}: e['v'] += 6
        if (v['name'], e['bar']) in {('Soprano', 13), ('Soprano', 30)}: e['v'] -= 3
```

## 4. Octaves at the start of the quodlibet (Low)

**What is written.**
- The soprano's subject ends its first bar `… A#4:3 B4:1 | C#5`.
- "Ich bin" goes `… A#3:3 B3:3 | C#4`.
- The two voices sound A♯, B and C♯ in octaves at 55.3, 55.4¾ and 56.1 (the critic's weak and beat-to-beat octaves).

**Assessment.**
- No other placement of the subject works:
  - on A♯ it doubles the leading tone of V6 at 56.1;
  - on C♯ it puts E♯ on beat 3 over the tonic.
- "Ich bin" is Bach's tune.
- I tested dropping the subject's last semiquaver (`A#4:4`): it removes only the B–C♯ octave and costs the subject its dotted figure.

**Recommendation.** Leave it. Two tunes agreeing for three notes is acceptable in a quodlibet. A line in NOTES would cover it.

## 5. The ending (Low)

**What is written.**
- The final chord is F♯2 A♯3 C♯4 F♯4, after a ritardando to 40.
- The soprano ends on F♯4 because Kraut ends on the lower tonic.

**Assessment.** It is quiet and in the middle of the keyboard. That suits a quodlibet that, in Bach, leads back to the Aria. I would keep it. If a brighter close is wanted, change only the alto, not the tune.

## Smaller points

- **The Adagio (b47–54).** It is the longest section (28 s) and the plainest: diatonic, mostly dotted crotchets and minims. After the subject, the dux holds two long notes (NOTES' own point).
  - It is a calm place, which the plan needs before the quodlibet.
  - With fix 1 it also no longer drags into ♩ = 42 for its last two beats.
- **Retransition (b35–36).** The two upper voices move in block crotchets over the bass's entry. The bass's subject is the point, so this is acceptable.

## Better than the fourteen-voice version?

**Yes, in every respect a listener can hear.**

| | 14 voices | 4 voices |
|---|---|---|
| canons sounding at once | six | one |
| pitch class tripled on beats | 40 % | 8.8 % |
| bad doublings | 18 | 0 |
| low-register seconds | 14 | 2 |
| keyboard unplayable | 48.5 % | 0.5 % |

- **The ground now travels:** I – IV – ii – V – I – i – I. The piece has key areas, a retransition and a return, instead of ten statements in F♯.
- **The quodlibet** now follows Bach's own layout and can be heard.
