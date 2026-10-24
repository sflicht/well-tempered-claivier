# Pair I (C minor) v2 — report

Files: prelude-i_v2.{mp3,pdf,mid,musicxml,ly,json} and fugue-i_v2.{...}. Checker output is in checks/p2.txt and checks/f2.txt. The MP3s are gain-matched to a mean of −22.7 dB: the prelude runs 1:45 and the fugue 1:59.
Sources: pairI/prel2.py and build_prelude2.py (prelude); pairI/v2/s2.py → v2/lit.txt and fug2.py (fugue). Nothing has been pushed.
**I cannot hear the audio.** Everything below comes from the score and the checkers, not from listening.

## Prelude v2: "losing the beat" (28 bars, q=66)
The 16ths are continuous throughout. Accents fall on the start of each group rather than on the beat (velocity +8, with an extra accent on the structural downbeats).
- b1–4 (A): C minor in groups of 4 that line up with the beat (i–V6/5–i, iv–ø7, V). This sets up the meter.
- b5–10 (B): groups of 3 over a dotted-quarter bass (6+6+6+6+4+4 across each two-bar span), so the hemiola runs against 4/4. Moves toward Eb: Fm7–Bb7–Eb–Ab… F7/A–Bb7.
- b11: Bb sus → Bb7 with the 3-groups continuing over a regular bass.
- b12: **downbeat regained** on Eb, back to groups of 4, accented.
- b13–18 (C): groups of 5 over a syncopated bass (onsets 0/2/6/10/14). Eb7–Ab/C–Bbm/Db–B°7–C7–Fm–Dø7.
- b19–24 (D): dominant implied by a **re-struck G2** in 3+3+2 against a rotating 3/5/3/5/3 figure, which should be the most ambiguous stretch. The top note rises G5–Ab5–A5–Bb5–B5 against the fixed G2. This is the faint wedge (one-sided, nothing like the IV/V treatments).
- b25: **downbeat regained** in C minor (accented groups of 4); iv6, then a brief 3-group flicker over Dø/F and the cadential 6/4.
- b27–28: V7 → a plain C minor close. No Picardy third.

## Fugue v2 (two voices, 32 bars, q=66, Andante con moto)
- New tonal subject (2 bars): `C B D Ab Eb G F | Eb D C D Eb D C B C G`. It is a wedge around C, framed by the leading tone and diminished 7th and resolved functionally (in the BWV 855/889 spirit).
- The answer is the inversion that maps tonic↔dominant (it starts on G3). The CS is in 16ths, and the invertible version CSI is used too.
- Bar plan:
  - b1–4: exposition (S, then A + CS).
  - b5–6: E1, tail-motif sequence to Eb.
  - b7–10: S and A in Eb with CSI/CS.
  - b11–12: E2, descending sequence Eb→Ab→G°7→C7 (rewritten by hand).
  - b13–18: canon by inversion in F minor (lag of half a bar).
  - b19–20: E3.
  - b21–23: stretto at the half bar in G minor.
  - b23–24: E4, a 16th drive up to C6 over V7.
  - **b25–26: PEAK.** The subject at its highest (C6–F6) arrives on i, with the inversion entering a beat later on a G2 dominant bass. The tension builds to V7.
  - **b27: deceptive cadence** to Ab, then a Neapolitan (Db).
  - b28: dominant implied by re-struck G2 bariolage.
  - b29–31: final cadential stretto (S over S at the octave, half a bar apart), iv–V.
  - b32: plain C minor octave C5/C3. **No Picardy, no sustained pedal.**

## What changed from v1
- Prelude: rewritten from scratch. Groupings change by section (4 / 3 / 5 / mixed / 4), the bass rhythm changes by section, there are fewer modulations (Cm→Eb→Fm→V→Cm), and the downbeat comes back decisively at b12 and b25.
- Fugue: new tonal subject; cross-relations cut from many to 1; peak rebuilt (register plus V → deceptive cadence); Picardy third and pedal ending removed.

## Checker flags still open
- Fugue:
  - one octave/5th parallel on the 8th grid (b12.3, inside E2, F5/Bb2 → G5/C3);
  - one 16th parallel (b26.2, at the peak);
  - m2 clashes at b17.3 and b18.1 in the canon (passing Ab against G);
  - one cross-relation (b23, F vs F#, where the G-minor stretto hands over to E4);
  - no unprepared beat dissonances.
- Prelude:
  - 11 "unprepared dissonance" flags. Most are chord-tone 4ths over the bass (the 6/4 sound over the G pedal) or 7ths of 7th chords.
  - 5 octave parallels on the 8th grid, from broken-chord octaves (b1.3, b2.1, b6.1, b26.4, b28.1).
  - 13 short cross-relations in the checker's sense, mostly from chord changes inside the figuration.
  - No voice crossings.

## Honest weak spots
- The prelude's voicings are chosen automatically and hold for half a bar each, so the harmonic rhythm is regular even while the grouping isn't. It may still feel mechanical in the A and E sections.
- Whether the "lost beat" actually comes across depends on the MIDI velocity accents, which I can't audition. The 5-groups in C may just sound like noise.
- The fugue canon (b13–18) still circles E–F–G–Ab. The episodes are serviceable, not inspired.
- The peak (b25–27) is solid on paper, but whether it "hits" I can't judge without hearing it.
