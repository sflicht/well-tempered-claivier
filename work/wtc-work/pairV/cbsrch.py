import subprocess,re,os,json,sys
sys.path.insert(0,'.')
from chk import load,nm
from lib5 import midi
base=open('fugue_v6_bars.py').read()+open('adds7.py').read()
def build(cbmap):
    s=base+'\n'+'\n'.join(f"putseq('Cb',{b},'{v}')" for b,v in cbmap.items())+'\n'
    open('fugue_v7s_bars.py','w').write(s)
    subprocess.run('../venv/bin/python build_fugue7.py fugue-v_tmp.json fugue_v7s_bars >/dev/null',shell=True)
    o=subprocess.run('../venv/bin/python chk.py fugue-v_tmp.json -v',shell=True,capture_output=True,text=True).stdout
    return o
def score(o,bars):
    sc=0
    for line in o.splitlines():
        if re.match(r'(beat_dissonance|m2/M7|parallel_5ths_8ves\(eighth|par16_list|xrel_list)',line):
            for it in re.findall(r"'b(\d+)[^']*'",line):
                if int(it) in bars: sc+= 3 if ('parallel' in line or 'xrel' in line) else (1 if 'par16' in line else 2)
    return sc
if __name__=="__main__":
  bars=list(range(35,39))+list(range(42,47))
  cur={}
  # start from rests in those bars
  d,G,A,SP,bl,nb=load('fugue-v_v3.json')
  Bi=4  # Bass voice index
  prev=midi('F#2')
  for b in bars:
    notes=[]
    for h in (0,8):
      x=(b-1)*16+h
      pcs={int(G[i,x])%12 for i in range(5) if G[i,x]>=0}
      bass=int(G[Bi,x]) if G[Bi,x]>=0 else 50
      cands=[p for p in range(midi('E1'),min(bass,midi('D3'))+1) if p%12 in pcs and p%12!=(bass+7)%12]
      best=None
      for p in cands:
          trial=' '.join(notes+[nm(p)+':8'])+(' R:8' if h==0 else '')
          o=build({**cur,b:trial}); sc=score(o,[b])*10+abs(p-prev)/2+(0 if p%12==bass%12 else 1)
          if best is None or sc<best[0]: best=(sc,p)
      notes.append(nm(best[1])+':8'); prev=best[1]
    cur[b]=' '.join(notes); print(b,cur[b],best[0],flush=True)
  json.dump(cur,open('cb_choice.json','w'))
