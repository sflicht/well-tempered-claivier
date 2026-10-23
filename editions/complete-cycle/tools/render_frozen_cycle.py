#!/usr/bin/env python3
"""Render only composer-frozen files; resume by exact source hash."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,time
ROOT=Path(__file__).resolve().parents[1]

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def render(row):
    n=row['number'];source=Path(row['path']);out=ROOT/'work/cycle_render';out.mkdir(exist_ok=True)
    prefix=out/f'{n:02d}-fugue';receipt=prefix.with_suffix('.source.json')
    if digest(source)!=row['sha256']:raise ValueError(f'{n}: frozen source changed before rendering')
    if receipt.exists():
        old=json.loads(receipt.read_text())
        if old.get('sha256')==row['sha256'] and all(prefix.with_suffix('.'+e).exists() for e in ['mp3','wav','pdf','musicxml','mid']):return n,'already rendered',row['sha256']
    p=subprocess.run(['python3',str(ROOT/'tools/render_music.py'),str(source),'--output-prefix',str(prefix)],capture_output=True,text=True)
    prefix.with_suffix('.batch.log').write_text(p.stdout+'\n'+p.stderr)
    if p.returncode:raise RuntimeError(f'{n}: renderer failed: {p.stderr[-1500:]}')
    if digest(source)!=row['sha256']:raise ValueError(f'{n}: source changed during rendering')
    receipt.write_text(json.dumps({'number':n,'sha256':row['sha256'],'source':str(source)},indent=2)+'\n')
    return n,'rendered',row['sha256']

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--watch',action='store_true');ap.add_argument('--workers',type=int,default=3);args=ap.parse_args()
    pending={};finished=set();failures=[]
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        while True:
            path=ROOT/'work/cycle_fugues/freeze_manifest.json'
            try:rows=json.loads(path.read_text()).get('pieces',[])
            except (FileNotFoundError,json.JSONDecodeError):rows=[]
            for row in rows:
                key=(row['number'],row['sha256'])
                if key not in finished and key not in pending:
                    pending[key]=ex.submit(render,row)
            for key,f in list(pending.items()):
                if f.done():
                    del pending[key];finished.add(key)
                    try:print(json.dumps({'result':f.result()}),flush=True)
                    except Exception as e:failures.append(str(e));print(json.dumps({'error':str(e)}),flush=True)
            current={(r['number'],r['sha256']) for r in rows}
            if not pending and (not args.watch or len(rows)==24) and current.issubset(finished):break
            time.sleep(2)
    if failures:raise SystemExit('\n'.join(failures))

if __name__=='__main__':main()
