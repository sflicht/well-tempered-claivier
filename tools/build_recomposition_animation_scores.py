#!/usr/bin/env python3
"""Add listening captions to the two completed audition scores.

The authoritative musical source stays unchanged. Annotated copies preserve
every written voice event and record the source hash for review.
"""
from pathlib import Path
import copy
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'work/recomposition'
OUT = BASE / 'animation_scores'


def annotation(t, end, title, text):
    return dict(t=t, end=end, title=title, text=text)


STUDIES = [
    ('fugue_i/01-fugue-recomposed.json', 'fugue-i-annotated.json', [
        annotation(0, 8.5, 'A subject that wants to continue',
                   'The upper voice begins after an eighth-note rest. Its final B leads onward to C instead of closing the phrase.'),
        annotation(8.5, 16, 'The answer enters below',
                   'The lower voice takes the theme in G. Above it, the first voice changes to a longer-note companion.'),
        annotation(16, 24.5, 'Recoil and continuation',
                   'The full theme gives way to shorter gestures. Follow the descending recoil and the rising tail between entries.'),
        annotation(24.5, 32, 'The roles change places',
                   'The upper voice now carries the G statement. The recurring companion is below it.'),
        annotation(32, 40.5, 'The bass takes the head',
                   'The lower voice repeats the opening gesture at new pitches. The upper voice carries the motion between those starts.'),
        annotation(40.5, 48, 'The subject turns to A minor',
                   'The theme returns below with its intervals adapted to the minor key. Its companion continues above.'),
        annotation(48, 64.5, 'A sequence changes hands',
                   'The opening gesture moves through descending thirds, then passes to the lower voice on the way back to C.'),
        annotation(64.5, 72.5, 'Home, in the lower voice',
                   'The complete C-major subject returns below the companion. The two lines keep different rhythms.'),
        annotation(72.5, 80, 'Home, in the upper voice',
                   'The subject and companion exchange registers once more. The same pair of ideas produces a different texture.'),
        annotation(80, 88, 'The head arrives earlier',
                   'Shorter returns of the opening gesture press toward the cadence. These are fragments, not new complete subject entries.'),
        annotation(88, 100, 'The tail becomes a conclusion',
                   'The closing passage draws on the subject tail. The two voices finally agree on the tonic arrival.'),
    ]),
    ('prelude_iv/prelude-iv-new.json', 'prelude-iv-annotated.json', [
        annotation(0, 12, 'A spring across the beat',
                   'The opening figure reaches G-sharp before beat three and holds across it. A descending tail answers that displaced weight.'),
        annotation(12, 24, 'The bass receives the gesture',
                   'The rhythmic figure moves into the lower voice. The upper line continues through held tensions and their resolutions.'),
        annotation(24, 36, 'The phrase opens into E major',
                   'The opening rhythm remains recognizable while its pitches change. E major gives way to A as the bass moves onward.'),
        annotation(36, 48, 'A turn through F-sharp minor',
                   'The middle passage carries the same gesture through a darker key area. Listen for lines continuing across the barline.'),
        annotation(48, 60, 'A second reply from below',
                   'The bass again takes the gesture. A rising bridge then recovers the register needed for the opening idea to return.'),
        annotation(60, 72, 'The opening returns',
                   'C-sharp minor comes back, but the phrase continues toward a higher point instead of closing here.'),
        annotation(72, 84, 'A higher peak over a changing bass',
                   'The upper voice reaches C-sharp an octave higher. The bass redirects the phrase and moves more quickly toward the cadence.'),
        annotation(84, 96, 'The dominant holds; the line continues',
                   'The bass approaches and holds G-sharp while the upper line keeps moving. The final bar supplies the closing C-sharp-minor tonic.'),
    ]),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for source_name, target_name, annotations in STUDIES:
        source = BASE / source_name
        data = json.loads(source.read_text())
        result = copy.deepcopy(data)
        result['pedagogy'] = {'annotations': annotations}
        result['metadata']['animation_source'] = {
            'path': str(source.relative_to(ROOT)),
            'sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
            'note_events_unchanged': True,
        }
        assert result['voices'] == data['voices']
        target = OUT / target_name
        target.write_text(json.dumps(result, indent=2) + '\n')
        manifest.append({'score': str(target), 'source': str(source),
                         'source_sha256': result['metadata']['animation_source']['sha256'],
                         'note_events_identical': result['voices'] == data['voices']})
    (OUT / 'annotation-sources.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(manifest, indent=2))


if __name__ == '__main__':
    main()
