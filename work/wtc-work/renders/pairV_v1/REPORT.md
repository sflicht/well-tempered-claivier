# Pair V (D major) - v1 report
All music is hand-authored note by note (new material; the old 05-* drafts were used only to see what was weak). Code only transposes/doubles motifs I wrote. NOTHING WAS LISTENED TO - everything below comes from score analysis (chk.py, implied.py) and engraving checks.

## Prelude V (40 bars, 4/4, Allegro, quarter=104, ~95 s)
Continuous 16ths in BOTH hands bar 1-39 (final bar held D). Bright "fanfare" D major, arpeggio waves, different from IV.
- A  b1-8   : D-major arpeggio waves (I | IV-I6 | ii-V | V7-I | vi-iii | IV-I6 | ii7-V7 | I)
- B  b9-16  : A major, compound line (repeated high E6 against moving line, LH in 10ths)
- C  b17-24 : development; "tattoo" cell (rising 4th + 3 repeated notes) over D-G-Bm-Em, then 7th-chain F#m7-Bm7-Em7-A7 (b21-24)
- D  b25-32 : A dominant pedal climb (b25-28) -> deceptive Bm b29 -> G#dim7 climbing to D7 (b30) -> PEAK b31 (E7 apex, falling A7 arpeggios) -> arrival on D b32 (RH to F#7, D2 in bass)
- E  b33-40 : shortened return, plain close, last rise b39, held D b40
Peak: b30-32. Dynamics are authored (peak ~100 vel, return ~80).
Fugue subject alludes to the prelude through the rising-4th/repeated-note "tattoo" cell and the D-F#-A trumpet arpeggio.

## Fugue V (6 voices S/A/T/Br/B/Cb, 59 bars, 4/4, Allegro quarter=108, ~134 s)
- Exposition b1-12: A(b1) T(b3) B(b5) S(b7) Br(b9) Cb(b11); CS enters with the answer (b3) and stays alongside every later entry
- Ep1 b13-16; M1 b17-20 (Bm then F#m, with CS); Ep2 b21-24
- Stretto I b25-27 (3 voices, G/D, CS in T; first lag 4 then 3)
- Ep3 b28-31 (bariolage in S); Stretto II b32-34 (4 voices + subject sequence, CS in Cb, entries a few beats apart, every lag under a bar)
- Ep4 b35-38 (hemiola 3+3+2); Stretto III b39-41 (4 voices, CS)
- Ep5 b42-46 rising sequence toward the dominant
- PEAK b47-50: subject augmented in Bass, augmented CS in Contrabass, subject in S (8va) and T, apex run in S reaching B6 at b50
- Final stretto over the D2 tonic pedal (Cb holds D2 b51-59): pass 1 b51-53 (lags 7+7 sixteenths), pass 2 b54-56 (lags 7 then 2 - very tight); CS in Br (pass 1) and T (pass 2)
- Coda b56-59, plain close
Every stretto lag is under one bar. Countersubject also in M1, M2 (T), M3 (Cb), M4 (B), the augmentation (b47) and both final-stretto passes.

## Checkers (outputs saved as *.check.txt, prelude-v_v1.implied.txt)
Fugue: beat dissonance 0, m2/M7 clashes 0, parallel 5ths/8ves (8th and 16th grid) 0, crossings 0.
 Left: intentional C/C# cross-relations b26-27 (M2); similar-bar flags (identical repeated Alto entries b1/b32/b51/b54 and the matching bars 2/33/52/55 - these are the subject entries recurring); 5-bar identical rhythm run in S/A/T in Ep5 b42-46.
Prelude: beat dissonance 0, m2/M7 0, parallels (8th and 16th grid) 0, crossings 0, implied chord fit 312/312 beat groups, 0 non-fitting.
 Left: one cross-relation b29-30 (F# in Bm -> F natural of the G#dim7), bars 6 and 34 are 72% pitch-similar (intentional return), "identical rhythm run" 39 bars (inherent to continuous 16ths), implied-bass notes: 11 par_bass/7 par_top/10 bass_leap warnings from implied.py (octave/5th movement between hands in places, e.g. b14, b21, b23, b34, b39).

## Suspected weak spots (unverified by ear)
1. Fugue Ep5 (b42-46): five bars of the same rhythm in S/A/T - the plodding texture Sam dislikes; I only varied the bass. Biggest known problem.
2. Fugue final stretto: lags 7+7 and 7/2 are tight but my search found no clean template with a shorter first lag; the 7-then-2 pass may sound crowded rather than climactic.
3. Fugue coda has quarter-note T/Br/B chords under 16th S/A - may be thin/static; the augmented CS in the peak is hand-adjusted (3 lengthened notes) so it is not an exact augmentation.
4. Fugue Alto A4 entry is the same each time (b1, b32, b51, b54) - repetitive.
5. Prelude: RH and LH often sit in octaves/10ths on strong beats, so the two hands can sound thin/doubled (see implied.py warnings); section B (b9-16) with repeated E6 may feel static; the b31 peak is one bar of falling arpeggio - may be less spectacular than it looks on paper; b30-31 chromatic G#dim7 not heard. Return b33-40 is close to b1-8.
6. Prelude/fugue transitions and the overall "wow" - uncertain without listening; velocity arcs are authored but untested.
7. Fugue stave layout: six staves, piano-sounding GM rendering (FluidR3), no real polyphonic timbre.

## Files (all in /workspace/wtc-work/renders/pairV_v1/)
fugue-v_v1.{mp3,pdf,mid,musicxml,ly,json,wav}, prelude-v_v1.{mp3,pdf,mid,musicxml,ly,json,wav}
fugue-v_v1.check.txt, prelude-v_v1.check.txt, prelude-v_v1.implied.txt, *.engraving.log (both PDFs compiled clean, 0 warnings; fugue 5 pages, prelude 3 pages)
fugue_v_source_bars.py, prelude_v_source_bars.py (hand-authored sources; prelude file has revision overrides at the bottom), build_fugue6.py, build_prelude5.py, chk.py, implied.py, gains.txt
MP3s loudness-normalized to ~-19.2 LUFS (true peak -3.6 / -5.7 dBFS).
