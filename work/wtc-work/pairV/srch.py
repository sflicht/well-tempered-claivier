import subprocess,itertools,re,os
res=[]
def run(spec):
    env=dict(os.environ,ST1=spec)
    r=subprocess.run('../venv/bin/python build_fugue7.py fugue-v_tmp.json fugue_v7_bars >/dev/null && ../venv/bin/python chk.py fugue-v_tmp.json -v',shell=True,capture_output=True,text=True,env=env)
    o=r.stdout; bad=0;det=[]
    for line in o.splitlines():
        if re.match(r'(beat_dissonance|m2/M7|parallel_5ths_8ves\(eighth|par16_list|crossing_list|xrel_list)',line):
            items=re.findall(r"'(b2[5-7][^']*)'",line); w=3 if 'parallel' in line or 'xrel' in line or 'par16' in line else 1
            bad+=w*len(items); det+=items
    return bad,det
cands=[]
for cv,cl,csh in [('T',0,0),('T',0,-7),('T',4,0),('T',8,0),('T',4,-7),('T',8,-7),('Br',0,0),('Br',4,0),('Br',8,0),('A',4,7),('A',8,7),('A',4,0),('A',8,0),('T',0,-2),('T',4,-2),('T',8,-2),('T',0,2),('T',4,2),('T',8,2),('T',0,-5),('T',4,-5),('T',8,-5)]:
  for ent in [('A=0:0','S=4:7','Br=8:-7'),('T=0:0','S=4:7','B=8:-7'),('A=0:0','S=4:7','B=8:-7'),('S=0:7','A=4:0','Br=8:-7'),('S=0:7','A=4:0','B=8:-7'),('A=0:0','S=4:7','T=8:-7'),('A=0:0','S=4:7','Br=8:-7','B=12:-14')]:
    used={e.split('=')[0] for e in ent}
    if cv in used: continue
    spec=' '.join(ent)+f' c{cv}={cl}:{csh}'
    cands.append(spec)
for s in cands:
    b,d=run(s); res.append((b,s,d))
res.sort()
for b,s,d in res[:12]: print(b,s,d[:8])
