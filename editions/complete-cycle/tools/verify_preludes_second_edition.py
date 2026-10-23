#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,re
root=Path(__file__).resolve().parents[1];issues=[];movements=[]
for n in range(1,25):
 p=root/f'work/cycle_preludes/{n:02d}-prelude.json';d=json.loads(p.read_text());old=json.loads(next((root/'baseline/scores').glob(f'{n:02d}-prelude-*.json')).read_text());m=d['metadata'];bl=m['meter'][0]*4/m['meter'][1];hs=d.get('pedagogy',{}).get('harmony',[]);key=hs[0]['pitch_classes'][0] if hs else None
 end=max(e['t']+e['d'] for v in d['voices'] for e in v['events']);oldend=max(e['t']+e['d'] for v in old['voices'] for e in v['events'])
 assert end==oldend and m['meter']==old['metadata']['meter'] and m['bpm']==old['metadata']['bpm']
 upper_leaps=[];written_aug2=[];leading=[];nonchord=[];spelling=[]
 for vi,v in enumerate(d['voices']):
  for i,(a,b) in enumerate(zip(v['events'],v['events'][1:])):
   assert a['t']+a['d']<=b['t']+1e-7
   if abs(b['t']-a['t']-a['d'])>1e-6:continue
   if vi==0 and abs(a['p']-b['p'])>12:upper_leaps.append([vi,b['t'],a['p'],b['p']])
   if abs(a['p']-b['p'])==3 and a.get('spell') and b.get('spell') and abs('cdefgab'.index(a['spell'][0])-'cdefgab'.index(b['spell'][0])) in [1,6]:written_aug2.append([vi,b['t'],a['spell'],b['spell']])
   if hs:
    ba=min(len(hs)-1,int(a['t']//bl));bb=min(len(hs)-1,int(b['t']//bl))
    if ba!=bb and re.fullmatch(r'V(?:6|64|7|65|43|42)?',hs[ba]['roman']) and hs[bb]['roman'] in ['I','i','I6','i6','I64','i64','vi','VI','vi6','VI6'] and a['p']%12==(key+11)%12 and b['p']!=a['p']+1:leading.append([vi,b['t'],a['p'],b['p']])
  for i,e in enumerate(v['events']):
   assert e['d']>0 and 21<=e['p']<=108 and 1<=e.get('v',0)<=127
   if e.get('spell'):
    s=e['spell'];pc=({'c':0,'d':2,'e':4,'f':5,'g':7,'a':9,'b':11}[s[0]]+s[1:].count('is')-s[1:].count('es'))%12
    if pc!=e['p']%12:spelling.append([vi,e['t'],s,e['p']])
   if e.get('role') in ['passing tone','bass passing tone','accented passing tone','returning neighbor']:
    assert 0<i<len(v['events'])-1
    a,z=v['events'][i-1],v['events'][i+1]
    assert abs(a['t']+a['d']-e['t'])<1e-6 and abs(e['t']+e['d']-z['t'])<1e-6
    assert 1<=abs(e['p']-a['p'])<=2 and 1<=abs(z['p']-e['p'])<=2
    assert (a['p']==z['p']) if e['role']=='returning neighbor' else (e['p']-a['p'])*(z['p']-e['p'])>0
    nonchord.append([vi,e['t'],e['role']])
 assert not upper_leaps and not written_aug2 and not leading and not spelling,(n,upper_leaps,written_aug2,leading,spelling)
 movements.append({'number':n,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'duration_unchanged':True,'meter_tempo_unchanged':True,'upper_leaps_over_octave':upper_leaps,'explicitly_spelled_augmented_second_joins':written_aug2,'annotated_dominant_including_inversions_to_tonic_or_submediant_leading_note_flags':leading,'spelling_errors':spelling,'verified_scalar_nonchord_events':len(nonchord)})
report={'status':'passed','scope':'Independent read of final JSON: duration/meter/tempo preservation; monophonic non-overlap; actual flanking intervals and continuity for scalar ornaments; annotated dominant-family (V, V6, V64, V7 and inversions) to tonic/submediant leading-note joins in 23 preludes; written augmented seconds where both pitches explicitly spelled. Not a strict-counterpoint or artistic-quality certificate.','movements':movements}
(root/'work/revision/prelude-context-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: all 24 movements; scalar events',sum(x['verified_scalar_nonchord_events'] for x in movements))
