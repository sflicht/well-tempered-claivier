"""Binaural render of Fugue XIX with string sounds, without changing the score.

The four dancers as a string quartet: the sarabande (soprano) on the first violin, the allemande
(alto) on the second violin, the gigue (tenor) on the viola, the courante (bass) on the cello,
seated in an arc in front of the listener.
Run from the repo root: python3 cycle/19-a-major/render_strings.py
"""
import json, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = {'Sarabande': 40, 'Allemande': 40, 'Gigue': 41, 'Courante': 42}

data = json.loads((ROOT / 'cycle/19-a-major/fugue.json').read_text())
for v in data['voices']:
    v['gm_program'] = PROGRAM[v['name']]
with tempfile.TemporaryDirectory() as tmp:
    score = Path(tmp) / 'fugue-strings.json'
    score.write_text(json.dumps(data))
    subprocess.run([sys.executable, str(ROOT / 'tools/render_spatial.py'), str(score),
                    '--output', str(ROOT / 'cycle/19-a-major/renders/fugue-spatial-strings.mp3'),
                    '--layout', 'arc', '--instruments', '--temperament', 'bach-lehman'], check=True)
