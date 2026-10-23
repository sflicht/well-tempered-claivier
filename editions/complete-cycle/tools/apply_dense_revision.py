#!/usr/bin/env python3
"""Apply the exact accepted high-voice structural revisions to the first edition.

The deterministic edit bundle includes the authored score values, rather than
relying on a time-limited constraint search to choose the same solution again.
Root's subsequent rhythmic/harmonic edition is a separate revision stage.
"""
from pathlib import Path
import argparse,hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--baseline-dir',type=Path,default=ROOT/'baseline/scores');p.add_argument('--bundle',type=Path,default=ROOT/'work/revision/dense-final-edits.json');p.add_argument('--output',type=Path,default=ROOT/'work/revision/dense_fugues');a=p.parse_args();bundle=json.loads(a.bundle.read_text());a.output.mkdir(parents=True,exist_ok=True)
 for item in bundle['pieces']:
  source=a.baseline_dir/item['baseline_name']
  if sha(source.read_bytes())!=item['baseline_sha256']:raise ValueError(f'Immutable baseline differs: {source}')
  raw=json.dumps(item['score'],indent=2).encode()
  if sha(raw)!=item['score_sha256']:raise ValueError(f'Edit bundle differs: {item["number"]}')
  destination=a.output/f'{item["number"]:02d}-fugue.json';destination.write_bytes(raw)
  print(json.dumps(dict(number=item['number'],path=str(destination),sha256=item['score_sha256'])))
if __name__=='__main__':main()
