"""Binaural render of Fugue XIX with string sounds, without changing the score.

Each band is a five-part French string band (Lully's 'vingt-quatre violons'):
dessus = violin, haute-contre / taille / quinte = viola, basse = cello.
The four bands sit in the four quarters of a ring around the listener.
Run from the repo root: python3 cycle/19-a-major/render_strings.py
"""
import json, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROGRAM = {'Dessus': 40, 'Haute-contre': 41, 'Taille': 41, 'Quinte': 41, 'Basse': 42}

data = json.loads((ROOT / 'cycle/19-a-major/fugue.json').read_text())
for v in data['voices']:
    part = (v.get('name') or '').split(':')[-1].strip()
    v['gm_program'] = PROGRAM[part]
with tempfile.TemporaryDirectory() as tmp:
    score = Path(tmp) / 'fugue-strings.json'
    score.write_text(json.dumps(data))
    subprocess.run([sys.executable, str(ROOT / 'tools/render_spatial.py'), str(score),
                    '--output', str(ROOT / 'cycle/19-a-major/renders/fugue-spatial-strings.mp3'),
                    '--layout', 'ring', '--instruments', '--temperament', 'bach-lehman'], check=True)
