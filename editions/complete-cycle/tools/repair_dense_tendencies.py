#!/usr/bin/env python3
"""Contextual repairs to six non-cadential leading-note departures.

Use ascending weak-beat passing resolutions where the following line supports
one. Else choose a stable dominant chord tone; do not manufacture a cadence
where the phrase actually continues into another harmony.
"""
import copy,json,sys,itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'vendor'));sys.path.insert(0,str(ROOT/'tools'))
import audit_music,compose_cycle_fugues as cf
ALLOWED={0,1,2,3,4,5,7,8,9,12}
OUT=ROOT/'work/revision/dense_fugues'
CASES={16:(8,271),17:(17,306),19:(10,325),21:(20,52),23:(7,184),24:(12,391)}
METRICS=['data_errors','parallel_perfect_interval_candidates_at_shared_attacks','structural_grid_parallel_candidates','outer_similar_motion_into_perfect_with_upper_leap_candidates','accented_dissonance_observations','exact_octave_duplicate_pairs']
def melodic_ok(d,vi):
 es=d['voices'][vi]['events']
 for a,b in zip(es,es[1:]):
  if a['t']+a['d']==b['t'] and abs(a['p']-b['p'])not in ALLOWED:return False
 return True

def protected(d,v,t):
 for en in d['subject_entries']:
  if en['voice']!=v:continue
  duration=max(e['t']+e['d']for e in d['subjects'][en['subject_id']]['events'])*en.get('scale',1)
  if en['t']<=t<en['t']+duration:return True
 return False

def fix_surrounding_counterpoint(d,baseline,changed_voice):
 """Revoice newly composed, non-thematic neighbors of a genuine resolution."""
 result=audit_music.audit(d,max_examples=40)
 def score(a):return sum(max(0,a['summary'][k]-baseline[k])for k in METRICS)
 for iteration in range(5):
  bad=score(result)
  if bad==0:return d,result
  targets=set()
  names={v['name']:i for i,v in enumerate(d['voices'])}
  for bucket in ['parallel_perfect_interval_candidates','structural_grid_parallel_candidates','outer_similar_motion_candidates']:
   for issue in result[bucket]['examples']:
    for name in issue.get('voices',[]):
     v=names[name]
     if v==changed_voice:continue
     for t in [issue['t'],issue['t']-1]:
      if t>=0 and not protected(d,v,t):targets.add((v,t))
  best=None
  hs={h['t']:h for h in d['harmony']}
  for v,t in targets:
   es=d['voices'][v]['events'];index=next((i for i,e in enumerate(es)if e['t']<=t<e['t']+e['d']),None)
   if index is None:continue
   old=es[index];h=hs.get(int(t));
   if h is None:continue
   pcs=dict(cf.vocab(h['key'],d['metadata']['mode']))[h['chord']]
   pitches=[p for p in range(max(21,old['p']-12),min(108,old['p']+12)+1)if p%12 in pcs and p!=old['p']]
   pitches.sort(key=lambda p:abs(p-old['p']))
   for pitch in pitches:
    trial=copy.deepcopy(d);tes=trial['voices'][v]['events'];ev=tes[index];end=ev['t']+ev['d'];right=min(t+1,end)
    replacements=[]
    if ev['t']<t:replacements.append(dict(ev,d=t-ev['t']))
    replacements.append(dict(ev,t=t,d=right-t,p=pitch,source='Second-edition counterpoint around a resolved leading note'))
    if right<end:replacements.append(dict(ev,t=right,d=end-right))
    tes[index:index+1]=replacements
    if not melodic_ok(trial,v):continue
    ar=audit_music.audit(trial,max_examples=40);value=score(ar)
    if value>=bad:continue
    candidate=(value,abs(pitch-old['p']),trial,ar)
    if best is None or candidate[:2]<best[:2]:best=candidate
    if value==0:return trial,ar
  if best is None:return None,result
  d,result=best[2],best[3]
 return None,result

def try_repair(n):
 p=OUT/f'{n:02d}-fugue.json';d=json.loads(p.read_text());vi,t=CASES[n];es=d['voices'][vi]['events'];index=next(i for i,e in enumerate(es)if e['t']<=t<e['t']+e['d']);old=es[index]
 baseline=audit_music.audit(d,max_examples=0)['summary'];candidates=[]
 if n in [16,19,21,23]:
  # The new tonic pitch is a real ascending passing tone on the weak half beat.
  # Neighbor notes retain their pitch classes; only needed register repairs vary.
  follower_indices=[]
  prev=old
  for i,e in enumerate(es[index+1:],index+1):
   if e['t']!=prev['t']+prev['d']:break
   if len(follower_indices)>=6:break
   follower_indices.append(i);prev=e
  reg_options=[0,12,-12]if n in [16,21]else[0]
  patterns=list(itertools.product(reg_options,repeat=len(follower_indices)))
  patterns.sort(key=lambda x:sum(abs(y)for y in x))
  for shifts in patterns:
   trial=copy.deepcopy(d);tes=trial['voices'][vi]['events'];ev=tes[index];end=ev['t']+ev['d'];ev['d']-=.5
   new=dict(ev,t=end-.5,d=.5,p=old['p']+1,source='Second-edition weak-beat leading-note resolution',label='Ascending passing resolution',revision_role='resolved tendency tone')
   for j,sh in zip(follower_indices,shifts):tes[j]['p']+=sh
   tes.insert(index+1,new)
   if not melodic_ok(trial,vi):continue
   candidates.append((trial,'weak-beat stepwise resolution with the following line voiced in a continuous register'))
   if len(candidates)>=20:break
 else:
  # The phrase is not cadencing. Removing its unsupported leading-note thrust
  # makes the intervening dominant open and lets the continuation remain open.
  hs={h['t']:h for h in d['harmony']};h=hs[t];pcs=dict(cf.vocab(h['key'],d['metadata']['mode']))[h['chord']]
  poss=[pitch for pitch in range(max(21,old['p']-12),min(108,old['p']+12)+1)if pitch%12 in pcs and pitch%12!=(h['key']+11)%12]
  poss.sort(key=lambda pitch:abs(pitch-old['p']))
  for pitch in poss:
   trial=copy.deepcopy(d);trial['voices'][vi]['events'][index]['p']=pitch
   if not melodic_ok(trial,vi):continue
   candidates.append((trial,'stable dominant chord tone replaces an unsupported leading-note departure'))
 for trial,reason in candidates:
  trial,result=fix_surrounding_counterpoint(trial,baseline,vi)
  if trial is None:continue
  if result['summary']['matched_subject_entries']!=result['summary']['documented_subject_entries']:continue
  cf.apply_spellings(trial)
  rec=dict(number=n,voice=vi,t=t,old_event=old,reason=reason,new_context=[e for e in trial['voices'][vi]['events']if e['t']+e['d']>t-1 and e['t']<t+4],audit=result['summary'])
  trial['composition_record'].setdefault('second_edition_tendency_repairs',[]).append(rec)
  p.write_text(json.dumps(trial,indent=2));(OUT/f'{n:02d}-dense-audit.json').write_text(json.dumps(result,indent=2));print(json.dumps(rec),flush=True);return rec
 print('UNRESOLVED',n,flush=True);return dict(number=n,status='unresolved')
if __name__=='__main__':
 nums=list(map(int,sys.argv[1:]))or list(CASES)
 rs=[try_repair(n)for n in nums]
 (ROOT/'work/revision/dense-tendency-repairs.json').write_text(json.dumps(rs,indent=2))
