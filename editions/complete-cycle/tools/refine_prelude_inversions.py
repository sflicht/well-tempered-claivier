#!/usr/bin/env python3
"""Apply the bounded final V6-context repair to VI and XIV only."""
from pathlib import Path
import copy,hashlib,json
import revise_preludes as rp
ROOT=Path(__file__).resolve().parents[1]
records=[]
for n in (6,14):
 path=ROOT/f'work/cycle_preludes/{n:02d}-prelude.json';data=json.loads(path.read_text());before=copy.deepcopy(data);oldhash=hashlib.sha256(path.read_bytes()).hexdigest()
 changes=rp.refine_inverted_dominants(data,n)
 errors=rp.validate(data,rp.PLANS[n]);assert not errors,errors
 # Every original onset retains its velocity/articulation/dynamic indication.
 for oldvoice,voice in zip(before['voices'],data['voices']):
  by_t={e['t']:e for e in voice['events']}
  for e in oldvoice['events']:
   for k in ('v','gate','dynamic'):assert e.get(k)==by_t[e['t']].get(k),(n,e['t'],k)
 path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
 records.append({'number':n,'before_sha256':oldhash,'after_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'before':rp.metrics(before),'after':rp.metrics(data),'changes':changes,'existing_performance_values_unchanged':True,'validation_errors':errors})
report={'status':'passed','scope':'Final bounded correction of missed first-inversion dominant contexts; upper voices, ground-arrival pitches, all existing performance values, meter, tempo and duration preserved except the documented inner resolution in XIV. No auditory assessment claimed.','movements':records}
(ROOT/'work/revision/prelude-inverted-dominant-repair.json').write_text(json.dumps(report,indent=2)+'\n')
p=ROOT/'work/revision/prelude-revision.json';review=json.loads(p.read_text())
for row in review['movements']:
 path=ROOT/f"work/cycle_preludes/{row['number']:02d}-prelude.json";d=json.loads(path.read_text());row['revised']=rp.metrics(d);row['revised_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
 if row['number'] in (6,14):row['inverted_dominant_refinements']=d['second_edition']['inverted_dominant_refinements']
review['totals']['notes_after']=sum(x['revised']['notes'] for x in review['movements'])
review['totals']['inverted_dominant_bass_connections']=4
review['totals']['inverted_dominant_inner_repairs']=1
p.write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
txt=ROOT/'work/revision/prelude-revision.txt';text=txt.read_text();addition='Final V6-context correction: VI bar 2 and XIV bars 2, 10 and 18 now lead from the bass leading note through tonic and supertonic into the retained first-inversion tonic third. XIV bar 19 also resolves its inner E-sharp to F-sharp. The contextual verifier now includes dominant inversions; every original event retains its existing velocity, gate and dynamic indication.'
if addition not in text:txt.write_text(text+'\n'+addition+'\n')
print(json.dumps(report,indent=2))
