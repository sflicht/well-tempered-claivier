#!/usr/bin/env python3
"""Build the persistent audition package from the final note data and renders."""
from pathlib import Path
import json, shutil, zipfile, subprocess
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'
KEYS=['C major','C minor','C-sharp major','C-sharp minor','D major','D minor',
      'E-flat major','E-flat minor','E major','E minor','F major','F minor',
      'F-sharp major','F-sharp minor','G major','G minor','A-flat major','G-sharp minor',
      'A major','A minor','B-flat major','B-flat minor','B major','B minor']
IDEAS=[
 'A clear two-part conversation; the cycle begins at human scale.',
 'A compact trio with a more angular subject and unmistakable tonal direction.',
 'Four lines with displaced accents and a brilliant, lightly articulated surface.',
 'Five voices: a singable subject, two-bar stretto and augmentation. First audition.',
 'Six voices, broad registration, measured architectural expansion.',
 'Seven voices with unequal rhythmic profiles and carefully spaced entries.',
 'Eight individual voices, grouped into two exchanging quartets.',
 'Nine voices, three trios that progressively interlock.',
 'Ten voices with two complementary subjects and individually traceable entries.',
 'Eleven voices; one migrating line changes the balance between two groups.',
 'Twelve voices, three contrasting instrumental quartets.',
 'Thirteen voices; sustained counterpoint supports increasingly active layers.',
 'Fourteen voices, contrasting seven-part groups with different articulation.',
 'Fifteen voices, three quintets that trade the subject and change register.',
 'Sixteen voices, four quartets with increasingly close imitative entries.',
 'Seventeen voices; an exposed line emerges from, and rejoins, the larger texture.',
 'Eighteen voices, six trios sharing a transparent harmonic rhythm.',
 'Nineteen voices; long-note counterpoint under rapid, independently phrased entries.',
 'Twenty voices, four quintets with a cumulative simultaneous passage.',
 'Twenty-one voices, seven trios with overlapping phrase lengths.',
 'Twenty-two voices, differently articulated groups converging in a unified stretto.',
 'Twenty-three voices; the most chromatic stage of the cycle, with exposed quiet passages.',
 'Twenty-four voices, an affirmative, spacious preparation for the final movement.',
 'Twenty-five voices, five quintets; every individual part enters, and all meet in a substantial climax.'
]

def main():
    plan=dict(title='The Well-Tempered clAIvier',version='First audition - IV only',
       status='One prelude-fugue pair drafted; the other 23 pairs are a composition plan, not finished music.',
       rule='Fugue N contains N+1 independently composed monophonic voices.',
       proposed_voice_criteria=[
        'Stable named parts throughout the score.',
        'A subject or justified answer/variant is heard in every part.',
        'Octave doubling does not count as another voice.',
        'A substantial passage includes all the advertised voices simultaneously.',
        'Independence is evaluated in melody, rhythm, function and audibility, not track count alone.'
       ],movements=[dict(number=i+1,key=k,voices=i+2,status='Draft 1 delivered' if i==3 else 'Planned',idea=IDEAS[i]) for i,k in enumerate(KEYS)])
    (OUT/'cycle-plan.json').write_text(json.dumps(plan,indent=2))
    for stem in ['prelude_iv','fugue_iv']:
        shutil.copy2(ROOT/'work'/f'{stem}.json',OUT/f'{stem}.json')
    notes='''THE WELL-TEMPERED clAIvier
First audition: IV. Prelude and Fugue in C-sharp minor
Composed for Sam, October 2026

STATUS
This package contains one newly composed prelude-fugue pair, not a completed
24-pair cycle. The remaining keys are a compositional plan in cycle-plan.json.
The first milestone is deliberately the five-voice fugue: correctness and
musical interest must be established before density is increased.

WHAT IS HERE
The prelude lasts 32 bars in 4/4, quarter note = 80, on three study staves.
The fugue lasts 76 bars in 4/4, quarter note = 82, on five study staves.
Audio is a sampled GM piano MIDI realization, not a live acoustic performance.
The study scores separate the lines; physical two-hand playability was not a
constraint. The canonical note data is the two event-score JSON files.
The paired piano MP3 places two seconds between the separate renderings.
The optional chamber-color fugue uses flute, oboe, clarinet, cello and bassoon
samples to distinguish the same five parts. It is a timbre study of the same
notes and timing, not a separately composed orchestration.

FUGUE SUBJECT
C-sharp dotted quarter, G-sharp eighth, A eighth, G-sharp eighth, F-sharp quarter;
E quarter, D-sharp eighth, C-sharp eighth, D-sharp quarter, E quarter;
E half, F-sharp eighth, E eighth, D-sharp quarter;
C-sharp quarter, B eighth, A eighth, B quarter, C-sharp quarter.

FORM
1-20: Five successive entries: Alto II, Alto I, Soprano, Tenor, Bass.
21-24: A two-part descending sequence derived from the subject tail.
25-28: Subdominant entry.
29-32: Relative-major version of the subject.
33-36: An episode in the middle and lower register.
37-40: Dominant entry.
41-44: Tonic return.
45-52: Three entries at two-bar distances, descending through the registers.
53-56: Quiet two-part episode.
57-64: Augmented subject in the bass.
65-70: Final pair of overlapping dominant entries.
71-76: Last tonic statement and a Picardy-third close.

METHOD AND LIMITS
The subject, countersubject, episode, entry scheme and tonal itinerary were
composed explicitly. Finite-domain constraint search supplied supporting
counterpoint. Five prepared suspensions and eight passing-note edits give
selected free parts more rhythmic variety. Seven proposed suspensions were
removed after review because other parts anticipated their resolutions.
Exact note data, the scripts and the audit are included so the
work can be inspected and revised. The search objective is a compositional
aid, not a measurement of beauty. Passing mechanical checks does not prove
stylistic correctness, independence of every phrase, or parity with Bach.
This is Draft 1, intended for listening and detailed criticism.

The audit distinguishes actual shared-attack parallel intervals from a
coarser quarter-note reduction, and reports accented dissonances for review.
It cannot prove that the music sounds good or that a fugue is convincing.
Read the accompanying final-audit.json and audit-notes.txt for the actual
findings rather than inferring a blanket all-rules certificate.

REPRODUCTION
The JSON is the authoritative written score. MusicXML preserves its exact
pitches, onsets and durations. MIDI is a performance file with a 97 percent
default note gate for slight articulation; use JSON or MusicXML to recover
the notated durations. Rendering is deterministic apart from software and
soundfont version differences.
Re-running constraint search with a time budget can produce a different
feasible realization; it is not a byte-identical composition recipe.

Tools: Python 3, OR-Tools, mido, numpy, scipy, pyfluidsynth; LilyPond 2.24,
FluidSynth, a GM soundfont such as TimGM6mb, FFmpeg, and Poppler for PDF QA.
Example, from the unpacked project directory:
  python tools/render_music.py fugue_iv.json --output-prefix rendered-fugue
  python tools/audit_music.py fugue_iv.json -o regenerated-audit.json
The pre-refinement structural score is work/fugue_iv_structural.json.
The rhythmic-refinement record in fugue_iv.json documents both accepted
edits and subsequent manual removals. A fresh run of refine_fugue_rhythm.py
now avoids anticipated resolutions automatically; it may choose different
eligible edits from those retained in this fixed first audition.

The complete future cycle contains 324 part assignments across its fugues:
2+3+...+25. At 25 voices there are 300 pairs of lines to inspect. These counts
are bookkeeping requirements; musical transparency remains a separate goal.
'''
    (OUT/'README.txt').write_text(notes)
    print('Project plan and notes ready.')

if __name__=='__main__':main()
