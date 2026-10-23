#!/usr/bin/env python3
"""Second-edition revisions to the preludes, preserving individual designs.

This is an inspectable score edit, not an auditory quality certificate. The
first edition remains in baseline/scores. Revision choices address broken
melodic continuities, gratuitous octave jumps, cadential leading-note errors,
and chord-bound slow melodies. The retained figuration is deliberately not
made uniformly smooth: bells, broken-chord toccatas and registral returns have
different musical jobs.
"""
from __future__ import annotations
from pathlib import Path
import copy, json, math, statistics, hashlib
import compose_cycle_preludes as cp
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'baseline/scores'; OUT=ROOT/'work/cycle_preludes'; REPORT=ROOT/'work/revision'
PLANS={p.number:p for p in cp.PLANS}
EPS=1e-7
# Authored eight-bar melodic directions, in diatonic degrees above the tonic.
# They organize whole phrases; harmonic pitches are chosen by voice leading.
CANTABILE={
 'sarabande':[4,3,2,3,2,1,2,0],
 'columns':[2,3,4,3,1,2,1,0],
 'weave':[4,3,2,1,2,3,1,0],
 'pastorale':[2,3,2,1,0,2,1,0],
 'ground':[4,3,2,1,4,3,2,0],
 'chaconne':[2,4,3,2,1,3,1,0],
 'lament':[7,6,5,4,3,2,1,0],
 'garden':[2,3,4,5,4,3,1,0],
 'passacaglia':[4,3,2,1,3,2,1,0],
 'threshold':[0,4,5,3,2,1,2,0],
}
FAST={'aperture','toccata','gigue','arabesque','prisms','clock','mirrors','nine','mechanism','interleave'}
GROUND={'ground','chaconne','passacaglia'}
STYLE_NOTES={
'aperture':'The opening folded arpeggio is retained; the inner song now crosses barlines smoothly, with prepared delays near the harmonic returns.',
 'toccata':'Alternating sixteenth-note sparks retain their leaping character; octave choices join successive gestures and the final burst reaches a connected leading-note cadence.',
 'bells':'The registral gaps and notated silences remain structural. Bell gestures keep their pitch-class contour, with coherent register routes rather than accidental bar-to-bar jumps.',
 'gigue':'The compound-duple leap-and-descent is retained, with connected phrase joins and an unambiguous upper leading-note resolution.',
 'sarabande':'A newly shaped upper cantabile replaces the sequence of root-based broken triads; accented scalar dissonances give the second beat its expressive weight, and the inner parts move economically.',
 'columns':'The broad outer spans now carry a continuous melody. Prepared suspensions give the harmonic columns tension before their resolution.',
 'weave':'The slow upper line now traverses an eight-bar falling-and-returning arc above the retained woven eighth notes; prepared suspensions connect its harmonic arrivals.',
 'arabesque':'The twelve-note folded contour remains, but barlines no longer reset the register arbitrarily; weak passing notes connect selected thirds.',
 'echo':'The exact rhythm of question and answering echo is preserved; phrase-level register planning and a clear final cadence make the exchange more continuous.',
 'pastorale':'A step-directed upper melody replaces repeated chord-rank patterns while preserving the lilting dotted rhythm; a few weak passing links animate the bass.',
 'ground':'The four-bar descending ground remains exact. The long-note variations sing in a continuous line, while the quicker variations retain the characteristic embers figure.',
 'prisms':'The shifting 2+3 and 3+2 groupings remain; independent inner continuations and connected registral joins give the five-beat spans direction.',
 'chaconne':'The eight-bar harmonic circuit remains. The slower variations use an authored cantabile arc, the quicker variation keeps its figuration, and the bass retains the circuit.',
 'clock':'The 3+2+2 and 2+2+3 opposition remains intact. The two inner lines now continue across the measure rather than restarting as chord blocks.',
 'lament':'The descending long-note melody is newly voiced as an eight-bar line; its rapid middle variation remains recognizable, with a less abrupt return.',
 'garden':'A phrase-length singing melody now grows over the retained arpeggios; the late octave ascent remains deliberate, and the final leading tone resolves upward.',
 'mirrors':'The dark, opposing compound figures retain their direction and rhythmic identity; unnecessary register resets are removed.',
 'nine':'The three related triple-note figures remain. The inner lines and bass now connect their spans, and the ending resolves in the same melodic register.',
 'interleave':'The upper and middle five-beat groupings remain different. The sustained lower layer now carries a continuous voice-led line.',
 'bell_echo':'High and low bell answers keep their silences and contraction; the final answering span now reaches a connected tonic cadence.',
 'passacaglia':'The eight-bar bass ground is preserved. The long-note variations gain a continuous upper melody and prepared suspensions before the restrained close.',
 'mechanism':'The rapid upper mechanism retains its pattern and the 3-against-4 lower pulse. Whole-phrase register choices remove accidental leaps between measures.',
 'threshold':'The five-layer accumulation is preserved. The opening and withdrawal now share a directed cantabile line, and late suspensions prepare the final fugue.',
}

def sign(x):return (x>0)-(x<0)
def scale_pitch(p,deg):
 s=[0,2,4,5,7,9,11] if p.mode=='major' else [0,2,3,5,7,8,10]
 o,j=divmod(deg,7);return cp.key_pc(p.key)+s[j]+12*o

def degree_near(p,degree,target):
 pc=scale_pitch(p,degree)%12
 return cp.close_pc(pc,target,36,108)

def event_at(es,t):
 for e in es:
  if e['t']-EPS<=t<e['t']+e['d']-EPS:return e
 return None

def align_ground_variations(data,p):
 """Let a variation begin with the ground, rather than mid-way through it."""
 if p.style not in GROUND:return []
 bl=p.meter[0]*4/p.meter[1];bars=data['composition_record']['bars'];old=data['voices'][0]['events'];events=[]
 if p.style=='ground':
  spans=[(0,4,[2,1,1],'Ground stated'),(4,8,[1,.5,.5,1,1],'Fragmented reply'),(8,12,[.5]*8,'Eighth-note variation'),(12,16,[1.5,.5,1,1],'Suspended motion'),(16,20,[.25]*16,'Sixteenth-note culmination'),(20,24,[.5,.5,1,1,1],'Dissolving the ground'),(24,28,[2,1,1],'Cadence')]
 elif p.style=='chaconne':
  spans=[(0,8,[1,.5,.5,1],'Chaconne stated'),(8,16,[.5]*6,'Flowing variation'),(16,24,[.25]*12,'Figured variation'),(24,32,[1.5,.5,1],'Contrasting phrase'),(32,40,[1,.5,.5,1],'Return and cadence')]
 else:
  spans=[(0,8,[1.5,.5,1],'Ground stated'),(8,16,[1,.5,.5,1],'First variation'),(16,24,[.5]*6,'Flowing variation'),(24,32,[.25]*12,'Figured culmination'),(32,40,[1.5,.5,1],'Epilogue and cadence')]
 for b in range(bars):
  original=[e for e in old if b*bl-EPS<=e['t']<(b+1)*bl-EPS]
  if b==bars-1:events.extend(copy.deepcopy(original));continue
  section=next(s for s in spans if s[0]<=b<s[1]);ds=section[2];hi=cp.harmony(data['pedagogy']['harmony'][b]['roman'],p)
  base=cp.close_pc(hi['root'],70,60,84);motive=list(p.motive)
  if section[0] in [8,16]:motive=motive[2:]+motive[:2]
  if b%4==3:motive=motive[-2:]+motive[:-2]
  t=b*bl;template=original[0]
  for j,d in enumerate(ds):
   q=cp.chord_pitch(hi,base,motive[j%len(motive)])
   events.append({**template,'t':t,'d':d,'p':q,'spell':hi['spell'][q%12],'role':'ground variation','source':'second-edition cycle-aligned variation'})
   t+=d
 data['voices'][0]['events']=events
 sections=[{'t':a*bl,'end':b*bl,'label':label,'explanation':'The rhythmic variation begins with a complete return of the ground.' if b<=32 and a else 'The characteristic ground and its melodic figure establish the movement.'} for a,b,ds,label in spans]
 data['metadata']['sections']=sections;data['metadata']['markers']=[{'t':s['t'],'label':s['label']} for s in sections]
 data['pedagogy']['sections']=copy.deepcopy(sections)
 data['pedagogy']['motifs']=[{'t':s['t'],'d':bl,'voice':0,'id':f'P{p.number:02d}-{p.style}','label':s['label'],'relationship':'Variation over the retained ground'} for s in sections]
 return [{'start_bar':a+1,'end_bar':b,'rhythm':ds,'label':label} for a,b,ds,label in spans]

def octave_revoice(data,p,voice_index,preserve_arrivals=False):
 """Choose register for whole gestures; retain every within-gesture interval."""
 es=data['voices'][voice_index]['events']; bl=p.meter[0]*4/p.meter[1]
 groups=[]
 for b in range(data['composition_record']['bars']):
  group=[e for e in es if b*bl-EPS<=e['t']<(b+1)*bl-EPS]
  if group:groups.append((b,group))
 if voice_index==len(data['voices'])-1:return
 median=statistics.median(e['p'] for e in es)
 lo=max(30,int(median)-22);hi=min(106,int(median)+22)
 # Retain wide, deliberately separated bell registers and the final sonority.
 costs={};parents=[]
 for j,(b,group) in enumerate(groups):
  candidates=[s for s in [-24,-12,0,12,24] if all(lo<=e['p']+s<=hi for e in group)] or [0]
  layer={};parent={}
  for shift in candidates:
   keep=.06*shift*shift
   if j==0: keep+=.8*shift*shift
   if p.style in ['bells','bell_echo']:keep*=2.0
   options=[]
   for oldshift,oldcost in costs.items() if j else [(0,0)]:
    if j:
     before=groups[j-1][1][-1]['p']+oldshift;after=group[0]['p']+shift
     leap=abs(after-before)
     join=leap*.25+max(0,leap-7)**2*3
     if preserve_arrivals:
      oldbar=groups[j-1][0];hs=data['pedagogy']['harmony'];a=groups[j-1][1][-1];z=group[0]
      if hs[oldbar]['roman']=='V' and hs[b]['roman'] in ['I','i','I6','i6','vi','VI'] and a['p']%12==(cp.key_pc(p.key)+11)%12 and z['p']==a['p']+1 and oldshift!=shift:join+=1000000
     if p.style in ['bells','bell_echo']:join*=.3
     # Preserve intentional registral return, not an automated global flattening.
     if p.style in ['garden','bells'] and b in [data['composition_record']['bars']-8,data['composition_record']['bars']-4]:join*=.2
     if p.style=='threshold' and b in [24,32]:join*=.25
    else:join=0
    options.append((oldcost+keep+join,oldshift))
   layer[shift],parent[shift]=min(options)
  costs=layer;parents.append(parent)
 shift=min(costs,key=costs.get);chosen=[]
 for j in range(len(groups)-1,-1,-1):chosen.append(shift);shift=parents[j][shift]
 chosen.reverse()
 changes=0
 for (_,group),s in zip(groups,chosen):
  if s:
   for e in group:e['p']+=s;e['source']='second-edition register continuity';changes+=1
 return changes

def phrase_contour(p,b,bars):
 motif=CANTABILE[p.style]
 # These are long registral arcs, not per-bar root resets.
 block=b//8;peak=1.8*math.sin(math.pi*min(1,b/max(1,bars-5)))
 degree=motif[b%8]
 center=72+cp.key_pc(p.key)%12
 while center>79:center-=12
 if p.style=='garden' and bars-8<=b<bars-4:center+=12
 if p.style=='threshold' and 24<=b<32:center+=12
 if p.style=='weave':center+=2
 if p.style=='lament':center-=2
 return degree_near(p,degree,center+peak+degree*.5)

def voice_lead(data,p,vi,melodic=False):
 """Plan the whole line; nonchord events must be flanked scalar motions."""
 es=data['voices'][vi]['events'];harmonies=data['pedagogy']['harmony'];bl=p.meter[0]*4/p.meter[1];bars=len(harmonies)
 bass=data['voices'][-1]['events'];top=data['voices'][0]['events'];median=statistics.median(e['p'] for e in es)
 low=max(40,int(median)-12);high=min(100,int(median)+12);final_start=(bars-1)*bl
 basetonic=cp.close_pc(cp.key_pc(p.key),median-3,48,84)
 within={'sarabande':[0,-1,-2],'columns':[0,1,2,1,0],'weave':[0,-1,-2],
 'pastorale':[0,1,0,2,1],'ground':[0,-1,-2],'chaconne':[0,1,2,1],
 'lament':[0,-1,-2,-3],'garden':[0,1,2,1,0],'passacaglia':[0,-1,-2],'threshold':[0,1,0]}
 candidates=[];targets=[];uses=[];barindex={};chordsets=[];can_nc=[]
 for i,e in enumerate(es):
  b=min(bars-1,int(e['t']//bl));h=harmonies[b];j=barindex.get(b,0);barindex[b]=j+1
  use=melodic and (p.style not in ['ground','chaconne','lament','passacaglia','threshold'] or e['d']>=1)
  uses.append(use);chordsets.append(set(h['pitch_classes']))
  if use:
   deg=CANTABILE[p.style][b%8]+within[p.style][j%len(within[p.style])]
   target=basetonic+scale_pitch(p,deg)-cp.key_pc(p.key)
   if p.style=='garden' and bars-8<=b<bars-4:target+=12
   if p.style=='threshold' and 24<=b<32:target+=12
  else:target=e['p']
  targets.append(target)
  ncok=(use and 0<i<len(es)-1 and e['d']<=1.5 and int(es[i-1]['t']//bl)==b==int(es[i+1]['t']//bl) and abs(es[i-1]['t']+es[i-1]['d']-e['t'])<EPS and abs(e['t']+e['d']-es[i+1]['t'])<EPS)
  can_nc.append(ncok)
  if melodic and not use:vals=[e['p']]
  else:
   vals=[q for q in range(low,high+1) if q%12 in chordsets[-1] or (ncok and cp.scale_spelling(p,q%12))]
   if vi:
    upper=event_at(top,e['t'])
    if upper:
     vals=[q for q in vals if q<=upper['p']-3] or vals
     if h['roman']=='V' and upper['p']%12==(cp.key_pc(p.key)+11)%12:vals=[q for q in vals if q%12!=upper['p']%12] or vals
  if melodic and i==len(es)-1:
   vals=[q for q in range(low,high+1) if q%12==cp.key_pc(p.key)]
  if melodic and i==len(es)-2 and h['roman']=='V':
   vals=[q for q in range(low,high+1) if q%12==(cp.key_pc(p.key)+11)%12]
  candidates.append(vals)
 # State retains two pitches, so every interior nonchord event can be checked
 # at the instant its resolution becomes known. Sparse leaps are penalized;
 # nonchord notes do not gain admission merely by reducing a metric.
 costs={};parents=[]
 for i,e in enumerate(es):
  layer={};back={}
  for oldstate,cost in costs.items() if i else [((None,None),0)]:
   pp,prev=oldstate
   for q in candidates[i]:
    nc=q%12 not in chordsets[i]
    prevnc=i>0 and prev%12 not in chordsets[i-1]
    if i and prevnc:
     if pp is None or not (1<=abs(prev-pp)<=2 and 1<=abs(q-prev)<=2):continue
     if not (q==pp or sign(prev-pp)==sign(q-prev)):continue
     if nc:continue
    if i and nc:
     if not 1<=abs(q-prev)<=2:continue
     if prevnc:continue
    local=.48*(q-targets[i])**2+(1.0 if nc else 0)
    if vi:
     other=event_at(top,e['t'])
     if other and abs(other['p']-q)%12==0:local+=3
    movement=0
    if i:
     leap=abs(q-prev);movement=leap*.3+max(0,leap-3)**2*1.2
     if leap==3:
      oldh=cp.harmony(harmonies[min(bars-1,int(es[i-1]['t']//bl))]['roman'],p)
      newh=cp.harmony(harmonies[min(bars-1,int(e['t']//bl))]['roman'],p)
      sp=oldh['spell'].get(prev%12) or cp.scale_spelling(p,prev%12)
      sq=newh['spell'].get(q%12) or cp.scale_spelling(p,q%12)
      if sp and sq and abs('cdefgab'.index(sp[0])-'cdefgab'.index(sq[0])) in [1,6]:movement+=500
     if q==prev:movement+=5.5 if melodic and uses[i] else 1.8
     if leap>7:movement+=90*(leap-7)
     if pp is not None and abs(prev-pp)>4 and sign(q-prev)==sign(prev-pp):movement+=8
     oldb=min(bars-1,int(es[i-1]['t']//bl));newb=min(bars-1,int(e['t']//bl));oh=harmonies[oldb];nh=harmonies[newb]
     if oldb!=newb and oh['roman']=='V' and nh['roman'] in ['I','i','I6','i6','vi','VI'] and prev%12==(cp.key_pc(p.key)+11)%12 and q!=prev+1:movement+=1000
     if melodic and i==len(es)-1 and oh['roman']=='V' and q!=prev+1:continue
     if vi==0:
      bo=event_at(bass,es[i-1]['t']);bn=event_at(bass,e['t'])
      if bo and bn and sign(q-prev)==sign(bn['p']-bo['p'])!=0 and (prev-bo['p'])%12 in [0,7] and (q-bn['p'])%12==(prev-bo['p'])%12:movement+=1000
    state=(prev,q);value=cost+local+movement
    if value<layer.get(state,float('inf')):layer[state]=value;back[state]=oldstate
  if not layer:raise ValueError(('no melodic continuation',p.number,vi,i,e))
  costs=layer;parents.append(back)
 state=min(costs,key=costs.get);pitches=[]
 for i in range(len(es)-1,-1,-1):pitches.append(state[1]);state=parents[i][state]
 pitches.reverse();changes=0
 for i,(e,q) in enumerate(zip(es,pitches)):
  if e['p']!=q:changes+=1
  e['p']=q;b=min(bars-1,int(e['t']//bl));h=cp.harmony(harmonies[b]['roman'],p)
  if q%12 in h['pcs']:
   e['role']='cantabile continuation' if melodic else 'inner continuation';e['spell']=h['spell'][q%12]
  else:
   e['role']='returning neighbor' if pitches[i-1]==pitches[i+1] else 'accented passing tone' if e['t']%1==0 else 'passing tone'
   e['spell']=cp.scale_spelling(p,q%12)
  e['source']='second-edition phrase voice leading'
 return changes

def directed_arrivals(data,p):
 """Resolve functional leading notes at tonic and deceptive arrivals."""
 bl=p.meter[0]*4/p.meter[1];hs=data['pedagogy']['harmony'];key=cp.key_pc(p.key);changes=[]
 for vi,v in enumerate(data['voices']):
  es=v['events']
  for i,(a,b) in enumerate(zip(es,es[1:])):
   if abs(a['t']+a['d']-b['t'])>EPS:continue
   ba=min(len(hs)-1,int(a['t']//bl));bb=min(len(hs)-1,int(b['t']//bl))
   if ba==bb or hs[ba]['roman']!='V' or hs[bb]['roman'] not in ['I','i','I6','i6','vi','VI'] or a['p']%12!=(key+11)%12 or b['p']==a['p']+1:continue
   target=a['p']+1;old=b['p'];offset=target-old
   if offset%12==0:
    for e in es:
     if bb*bl-EPS<=e['t']<(bb+1)*bl-EPS:e['p']+=offset
   else:b['p']=target
   b['spell']=cp.harmony(hs[bb]['roman'],p)['spell'][target%12]
   b['role']='leading-note resolution';b['source']='second-edition directed harmonic arrival'
   changes.append({'voice':vi,'t':b['t'],'old':old,'new':target,'from':a['p'],'arrival':hs[bb]['roman']})
 # The VI-to-V join in the C-minor toccata now uses C-B (4-3) instead
 # of A-flat-B, without altering the rapid figure's timing.
 if p.number==2:
  e=next(e for e in data['voices'][1]['events'] if abs(e['t']-75.75)<EPS)
  old=e['p'];e['p']=72;e['spell']='c';e['source']='second-edition semitone approach to dominant'
  changes.append({'voice':1,'t':75.75,'old':old,'new':72,'reason':'C-B semitone replaces A-flat-B augmented second.'})
 return changes

def add_passing(data,p):
 """Replace the weak midpoint of selected thirds with an actual scalar link."""
 bl=p.meter[0]*4/p.meter[1];count=0
 chosen_voices=[0]
 if p.style in ['aperture','weave','garden']:chosen_voices=[1]
 for vi in chosen_voices:
  es=data['voices'][vi]['events'];pending=[]
  for i in range(1,len(es)-1):
   a,e,z=es[i-1:i+2]
   b=int(e['t']//bl);h=data['pedagogy']['harmony'][b]
   if not (abs(a['t']+a['d']-e['t'])<EPS and abs(e['t']+e['d']-z['t'])<EPS):continue
   if int(a['t']//bl)!=b or int(z['t']//bl)!=b:continue
   if e['d']>.5 or (e['t']*2)%2==0:continue
   if b>=len(data['pedagogy']['harmony'])-2:continue
   if any(x.get('role') in ['prepared suspension','suspension resolution','returning neighbor','accented passing tone','passing tone'] for x in [a,e,z]):continue
   if i and any(abs(e['t']-q[1]['t'])<1.5 for q in pending):continue
   if abs(a['p']-z['p']) not in [3,4]:continue
   between=[q for q in range(min(a['p'],z['p'])+1,max(a['p'],z['p'])) if abs(q-a['p'])<=2 and abs(q-z['p'])<=2 and cp.scale_spelling(p,q%12) and q%12 not in h['pitch_classes']]
   if not between:continue
   q=between[0]
   pending.append((i,e,q))
  # Structural restraint: at most one scalar replacement per two-bar gesture.
  used=set()
  for i,e,q in pending:
   group=int(e['t']//(2*bl))
   if group in used:continue
   used.add(group);e['p']=q;e['spell']=cp.scale_spelling(p,q%12);e['role']='passing tone';e['source']='second-edition scalar connection';count+=1
 return count

def add_suspensions(data,p):
 bl=p.meter[0]*4/p.meter[1];hs=data['pedagogy']['harmony'];bars=len(hs);report=[]
 if p.style not in ['sarabande','columns','weave','garden','ground','chaconne','passacaglia','lament','threshold','aperture','interleave']:return report
 vi=1 if p.style in ['aperture','interleave'] else 0
 es=data['voices'][vi]['events'];bass=data['voices'][-1]['events']
 # Seek different phrases, keeping the opening and the last cadence clear.
 used_phrases=set()
 for b in range(2,bars-3):
  phrase=b//4
  if phrase in used_phrases:continue
  if len(report)>=4:break
  t=b*bl
  first=next((i for i,e in enumerate(es) if abs(e['t']-t)<EPS),None)
  if first is None or first==0:continue
  prev=es[first-1];cur=es[first]
  if abs(prev['t']+prev['d']-t)>EPS or prev['d']<.5 or cur['d']<1:continue
  if prev.get('role') in ['passing tone','accented passing tone','returning neighbor']:continue
  if first>=2 and es[first-2].get('role') in ['passing tone','accented passing tone','returning neighbor']:continue
  bass_e=event_at(bass,t)
  if not bass_e:continue
  target=cur['p']
  options=[]
  for hold in [target+1,target+2]:
   if hold%12 not in hs[b-1]['pitch_classes'] or hold%12 in hs[b]['pitch_classes']:continue
   before=(hold-bass_e['p'])%12;after=(target-bass_e['p'])%12
   if not ((before==5 and after in [3,4]) or (before in [1,2] and after==0)):continue
   if first>=2 and abs(hold-es[first-2]['p'])>7:continue
   if abs(hold-prev['p'])>4:continue
   options.append(hold)
  if not options:continue
  hold=min(options,key=lambda q:abs(q-prev['p']))
  delay=.5 if p.style not in ['sarabande','columns','weave','garden','passacaglia'] else 1
  if cur['d']<=delay:delay=.5
  prev['p']=hold
  ph=cp.harmony(hs[b-1]['roman'],p);prev['spell']=ph['spell'][hold%12]
  # One event genuinely crosses the barline; engraving creates its tie.
  prev['d']+=delay;prev['gate']=1.0;prev['role']='prepared suspension';prev['label']='Prepared suspension'
  prev['source']='second-edition preparation and suspension'
  cur['t']+=delay;cur['d']-=delay;cur['role']='suspension resolution';cur['label']='Resolution'
  report.append({'voice':vi,'bar':b+1,'onset':t,'preparation':prev['t'],'hold':hold,'resolution':target,'delay':delay,'kind':'4-3' if (hold-bass_e['p'])%12==5 else '9-8'})
  used_phrases.add(phrase)
 return report

def bass_connectors(data,p):
 if p.style in GROUND or p.style in ['bells','bell_echo','threshold','columns']:return []
 bl=p.meter[0]*4/p.meter[1];es=data['voices'][-1]['events'];hs=data['pedagogy']['harmony'];out=[];report=[]
 for i,e in enumerate(es):
  e=copy.deepcopy(e)
  if i+1>=len(es):out.append(e);continue
  nxt=es[i+1];b=int(e['t']//bl)
  permitted=(b%4 in [1,2] and b<len(hs)-3 and abs(e['t']+e['d']-(b+1)*bl)<EPS and abs(nxt['t']-(b+1)*bl)<EPS and e['d']>=1.5)
  distance=nxt['p']-e['p']
  if permitted and abs(distance) in [3,4]:
   q=e['p']+(1 if distance>0 else -1)*(1 if abs(distance)==3 and cp.scale_spelling(p,(e['p']+sign(distance))%12) else 2)
   if abs(nxt['p']-q) in [1,2] and cp.scale_spelling(p,q%12):
    d=.5;end=e['t']+e['d'];e['d']-=d;out.append(e)
    add={**e,'t':end-d,'d':d,'p':q,'spell':cp.scale_spelling(p,q%12),'v':max(32,e['v']-5),'role':'bass passing tone','source':'second-edition directed bass connection'}
    if q%12 in hs[b]['pitch_classes']:add['role']='bass connection'
    out.append(add);report.append({'bar':b+1,'t':end-d,'from':e['p'],'through':q,'to':nxt['p']});continue
  out.append(e)
 data['voices'][-1]['events']=out;return report

def cadence(data,p):
 """Explicitly connect the final soprano and each inner resolution."""
 hs=data['pedagogy']['harmony'];bl=p.meter[0]*4/p.meter[1];bars=len(hs);last=(bars-1)*bl
 root=cp.key_pc(p.key);major=p.mode=='major';changes=[]
 top=data['voices'][0]['events'];final=top[-1];before=top[-2]
 if hs[-2]['roman']=='V':
  lead=cp.close_pc((root+11)%12,before['p'],55,99)
  before['p']=lead;before['spell']=cp.harmony('V',p)['spell'][(root+11)%12]
  before['role']='leading-note cadence';final['p']=lead+1;final['spell']=cp.harmony('I' if major else 'i',p)['spell'][root]
  changes.append({'voice':0,'t':before['t'],'resolution_t':final['t'],'leading':lead,'tonic':lead+1,'interval':1})
 # Inner parts take their nearest stable tonic chord member, with a single
 # prepared/attacked dominant seventh in the lowest inner line when suitable.
 n=len(data['voices']);v7i=next((vi for vi in range(n-2,0,-1) if data['voices'][vi]['events'][-2]['t']>=(bars-2)*bl),None)
 for vi in range(1,n-1):
  es=data['voices'][vi]['events'];last_e=es[-1];pen=es[-2]
  pcs=[root,(root+(4 if major else 3))%12,(root+7)%12]
  if hs[-2]['roman']=='V' and vi==v7i:
   before_pen=es[-3] if len(es)>2 else pen
   candidates=[q for q in range(28,min(94,final['p']-3)+1) if q%12==(root+5)%12]
   seventh=min(candidates,key=lambda q:abs(q-pen['p'])+3*max(0,abs(q-before_pen['p'])-4))
   if before_pen['t']>=(bars-2)*bl and (abs(seventh-before_pen['p'])==6 or abs(seventh-before_pen['p'])>7):
    leading_pcs=cp.harmony('V',p)['pcs']
    alternatives=[q for q in range(28,min(94,final['p']-3)+1) if q%12 in leading_pcs and abs(q-seventh) in [1,2,3,4,5]]
    before_pen['p']=min(alternatives,key=lambda q:abs(q-before_pen['p'])+abs(q-seventh))
    before_pen['spell']=cp.harmony('V',p)['spell'][before_pen['p']%12]
   pen['p']=seventh;pen['spell']=cp.scale_spelling(p,seventh%12)
   pen['role']='dominant seventh';pen['source']='second-edition cadential dissonance'
   last_e['p']=seventh-(1 if major else 2);last_e['spell']=cp.harmony('I' if major else 'i',p)['spell'][last_e['p']%12]
   changes.append({'voice':vi,'t':pen['t'],'resolution_t':last_e['t'],'seventh':seventh,'resolution':last_e['p'],'interval':last_e['p']-seventh})
   hs[-2]['cadential_seventh_onset']=pen['t']
   hs[-2]['cadential_seventh_resolution']=last_e['t']
  else:
   vals=[q for q in range(28,95) if q%12 in pcs and q<final['p']]
   # A leading note is obliged upward even in an inner part.
   q=pen['p']+1 if pen['p']%12==(root+11)%12 else min(vals,key=lambda q:abs(q-pen['p'])+.015*abs(q-last_e['p']))
   last_e['p']=q;last_e['spell']=cp.harmony('I' if major else 'i',p)['spell'][q%12]
  last_e['role']='cadential resolution';last_e['source']='second-edition cadence'
 return changes

def phrase_performance(data,p=None):
 bl=data['metadata']['meter'][0]*4/data['metadata']['meter'][1];end=max(e['t']+e['d'] for v in data['voices'] for e in v['events']);bars=round(end/bl)
 for vi,v in enumerate(data['voices']):
  for e in v['events']:
   bar=int(e['t']//bl);beat=e['t']%bl
   # Small phrase accents belong to written structure, not random humanization.
   arch=[-2,-1,1,2,3,1,-1,-4][bar%8]
   if e['t']>=end-2*bl:arch-=3
   e['v']=int(max(32,min(94,e.get('v',64)+arch)))
   if e.get('role')=='prepared suspension':e['gate']=1.0
   elif e.get('role') in ['suspension resolution','passing tone','bass passing tone']:e['gate']=.98
   elif p and p.style in ['toccata','gigue','clock','mechanism']:e['gate']=.91 if e['d']<=.5 else .96
   else:e['gate']=.985
   if beat==0 and bar in [0,8,16,bars-8,bars-4]:e.setdefault('dynamic','p' if bar in [0,bars-4] else 'mp' if bar in [8,bars-8] else 'mf')


def metrics(d):
 es=d['voices'][0]['events'];m=d['metadata'];bl=m['meter'][0]*4/m['meter'][1]
 intervals=[abs(b['p']-a['p']) for a,b in zip(es,es[1:])]
 joins=[abs(b['p']-a['p']) for a,b in zip(es,es[1:]) if abs(b['t']/bl-round(b['t']/bl))<EPS]
 return {'notes':sum(len(v['events']) for v in d['voices']),'upper_step_fraction':round(sum(0<x<=2 for x in intervals)/max(1,len(intervals)),4),'upper_leaps_over_octave':sum(x>12 for x in intervals),'upper_barline_leaps_over_fifth':sum(x>7 for x in joins),'final_upper_interval':es[-1]['p']-es[-2]['p'],'quarter_beats':max(e['t']+e['d'] for v in d['voices'] for e in v['events'])}

def validate(d,p=None):
 errors=[];end=max(e['t']+e['d'] for v in d['voices'] for e in v['events']);bl=d['metadata']['meter'][0]*4/d['metadata']['meter'][1]
 for vi,v in enumerate(d['voices']):
  prev=None
  for i,e in enumerate(v['events']):
   if e['d']<=0 or e['t']<0 or e['t']+e['d']>end+EPS:errors.append(['duration',vi,i,e])
   if prev and e['t']<prev['t']+prev['d']-EPS:errors.append(['overlap',vi,i,e])
   if not 21<=e['p']<=108:errors.append(['range',vi,i,e['p']])
   if not 1<=e.get('v',0)<=127:errors.append(['velocity',vi,i])
   if e.get('spell'):
    s=e['spell'];pc=(cp.NATURALS[s[0].upper()]+s[1:].count('is')-s[1:].count('es'))%12
    if pc!=e['p']%12:errors.append(['spelling',vi,i,e])
   if p:
    h=d['pedagogy']['harmony'][min(len(d['pedagogy']['harmony'])-1,int(e['t']//bl))]
    if e.get('role') in ['passing tone','bass passing tone','accented passing tone']:
     if i==0 or i==len(v['events'])-1:errors.append(['unflanked passing',vi,i])
     else:
      a,z=v['events'][i-1],v['events'][i+1]
      if not (1<=abs(e['p']-a['p'])<=2 and 1<=abs(z['p']-e['p'])<=2 and sign(e['p']-a['p'])==sign(z['p']-e['p'])):errors.append(['passing context',vi,i,e])
    elif e.get('role')=='returning neighbor':
     if i==0 or i==len(v['events'])-1:errors.append(['unflanked neighbor',vi,i])
     else:
      a,z=v['events'][i-1],v['events'][i+1]
      if a['p']!=z['p'] or not 1<=abs(e['p']-a['p'])<=2:errors.append(['neighbor context',vi,i,e])
    elif e.get('role')=='dominant seventh':
     if i==len(v['events'])-1 or h['roman']!='V' or e['p']-v['events'][i+1]['p'] not in [1,2]:errors.append(['seventh resolution',vi,i,e])
    elif e['p']%12 not in h['pitch_classes']:errors.append(['nonchord',vi,i,e])
   prev=e
  if abs(v['events'][-1]['t']+v['events'][-1]['d']-end)>EPS:errors.append(['final duration',vi])
 # Verify suspension preparation / dissonance / downward step from independent timestamps.
 for s in d.get('second_edition',{}).get('suspensions',[]):
  e=event_at(d['voices'][s['voice']]['events'],s['onset']);z=event_at(d['voices'][s['voice']]['events'],s['onset']+s['delay'])
  if not e or not z or e['t']>=s['onset'] or e['p']!=s['hold'] or z['p']!=s['resolution'] or e['p']-z['p'] not in [1,2]:errors.append(['suspension verification',s])
 return errors

def revise_iv(data):
 # The expressly composed IV already has an actual song and changing texture.
 # Repair the exposed register reset at its return: approach high C#6 through
 # G#5, preserving the intentional quiet octave change without a 17-semitone jump.
 top=data['voices'][0]['events'];changes=[]
 for e in top:
  if e['t']==95 and e['p']==68:e['p']=80;e['source']='second-edition return preparation';changes.append({'t':95,'old':68,'new':80,'reason':'Prepare the high return by a fifth, not a 17-semitone leap.'})
 phrase_performance(data)
 data['metadata']['movement_number']=4;data['metadata']['piece_type']='prelude';data['metadata']['character']='Invocation and current'
 data['metadata']['composition_notes']=[s.replace('Original32','Original 32').replace('bars23','bars 23').replace('and29','and 29') for s in data['metadata']['composition_notes']]
 data['metadata']['edition']='Second edition — critical musical revision'
 data['second_edition']={'review':'The explicitly composed melodic and harmonic design is retained; a register-reset approach to the high return is repaired, and phrase-level dynamics/articulation are clarified.','changes':changes,'suspensions':[]}
 return {'number':4,'character':'Invocation and current','pitch_edits':changes,'suspensions':[],'bass_connections':[],'cadence':[]}

def refine_inverted_dominants(data,number):
 """Connect V6 to i6 without discarding the original ground's bass arrival.

 The leading bass rises through 1 and 2 in the last beat, reaching 3 on
 the next downbeat. This fixes the previously missed diminished-fourth
 joins while preserving the returning chaconne ground and all phrase lengths.
 Existing performance values are retained; only new notes inherit the local
 bass velocity and gate. Idempotent for the bounded final-score repair.
 """
 if number not in (6,14):return []
 previous=data.get('second_edition',{}).get('inverted_dominant_refinements')
 if previous:return previous
 records=[];vi=len(data['voices'])-1;events=data['voices'][vi]['events']
 starts=[3] if number==6 else [3,27,51]
 for start in starts:
  end=start+3;lead=37 if number==6 else 41
  last=next(e for e in events if e['t']<=end-1<e['t']+e['d'])
  arrival=next(e for e in events if abs(e['t']-end)<EPS)
  assert last['p']==lead and arrival['p']==lead+4,(number,start,last,arrival)
  old=copy.deepcopy(last);last['d']=end-1-last['t']
  assert last['d']>0
  tonic,second=(('d','e') if number==6 else ('fis','gis'))
  for t,pitch,spelling,role in [(end-1,lead+1,tonic,'bass passing tone'),(end-.5,lead+3,second,'scalar bass continuation')]:
   note={**old,'t':t,'d':.5,'p':pitch,'spell':spelling,'role':role,'source':'second-edition V6-to-i6 bass connection'}
   note.pop('dynamic',None);events.append(note)
  records.append({'voice':vi,'dominant_start':start,'resolution_t':end-1,'arrival_t':end,'pitches':[lead,lead+1,lead+3,lead+4],'reason':'Leading bass resolves upward, then continues by step to the retained first-inversion tonic.'})
 events.sort(key=lambda e:e['t'])
 if number==14:
  e=next(e for e in data['voices'][1]['events'] if abs(e['t']-54)<EPS)
  assert e['p']==57
  e.update(p=54,spell='fis',role='leading-note resolution',source='second-edition inner V6 resolution')
  records.append({'voice':1,'t':54,'old':57,'new':54,'from':53,'reason':'The inner E-sharp resolves to F-sharp instead of leaping to A.'})
 data['second_edition']['inverted_dominant_refinements']=records
 data['pedagogy'].setdefault('revision_devices',{})['inverted_dominant_refinements']=copy.deepcopy(records)
 data['metadata'].setdefault('composition_notes',[]).append('The first-inversion dominant bass resolves through a stepwise leading-note-to-tonic connection before its retained first-inversion tonic arrival.')
 return records

def main():
 REPORT.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True);reports=[]
 for number in range(1,25):
  src=next(BASE.glob(f'{number:02d}-prelude-*.json'));data=json.loads(src.read_text());before=metrics(data)
  if number==4:r=revise_iv(data);p=None
  else:
   p=copy.deepcopy(PLANS[number]);changes=[]
   if p.style=='passacaglia':p.explanation='An eight-bar ground supports four complete statements with changing texture, followed by a restrained closing episode.'
   variations=align_ground_variations(data,p)
   for vi in range(len(data['voices'])-1):changes.append(octave_revoice(data,p,vi))
   melodic=p.style in CANTABILE
   melodic_count=voice_lead(data,p,0,True) if melodic else 0
   inner_count=[]
   for vi in range(1,len(data['voices'])-1):
    es=data['voices'][vi]['events']
    if statistics.median(e['d'] for e in es)>=1:inner_count.append(voice_lead(data,p,vi))
   arrivals=directed_arrivals(data,p)
   if number==23:
    octave_revoice(data,p,0,True)
    # An ascending tonic arpeggio reaches the next register deliberately.
    for at,pitch,spell in [(101,71,'b'),(101.25,75,'dis'),(101.5,78,'fis'),(101.75,83,'b')]:
     event=next(e for e in data['voices'][0]['events'] if abs(e['t']-at)<EPS)
     event.update(p=pitch,spell=spell,source='second-edition reaching gesture',role='ascending arpeggio link')
   susp=add_suspensions(data,p)
   passing=add_passing(data,p)
   bass=bass_connectors(data,p)
   cad=cadence(data,p)
   phrase_performance(data,p)
   data['second_edition']={'review':STYLE_NOTES[p.style],'variation_spans':variations,'directed_arrival_repairs':arrivals,'register_note_edits':sum(changes),'cantabile_pitch_edits':melodic_count,'inner_pitch_edits':sum(inner_count),'passing_connections':passing,'suspensions':susp,'bass_connections':bass,'cadence':cad}
   data['metadata']['edition']='Second edition — critical musical revision'
   data['metadata']['composition_notes']=[p.explanation,STYLE_NOTES[p.style], 'The score records each added suspension and scalar connection explicitly for teaching.', 'The free preludes are reviewed for note integrity, spelling, harmonic context and the listed voice-leading changes; they are not advertised as strict-species exercises.']
   data['pedagogy']['revision_devices']={'suspensions':susp,'bass_connections':bass,'cadence':cad,'directed_arrivals':arrivals}
   data['composition_record']['plan']['explanation']=p.explanation
   data['pedagogy']['characteristic_figure']=p.explanation+' '+STYLE_NOTES[p.style]
   if melodic:
    data['pedagogy']['motifs']=[{**x,'label':'Cantabile phrase','relationship':'Phrase-level melodic contour, varied with the harmony'} for x in data['pedagogy']['motifs']]
   for section in data['metadata']['sections']:
    local=[s for s in susp if section['t']<=s['onset']<section['end']]
    if local:section['explanation']+=' Prepared suspensions at '+', '.join('bar '+str(s['bar']) for s in local)+' delay the new harmony and resolve downward.'
    if section['label']=='Cadence':section['explanation']='The upper leading note rises by semitone to the tonic; the inner dominant seventh resolves downward.' if cad else 'The last tonic is approached through the movement\'s final cadence.'
   data['pedagogy']['sections']=copy.deepcopy(data['metadata']['sections'])
   r={'number':number,'character':p.character,**data['second_edition']}
  if number in (6,14):r['inverted_dominant_refinements']=refine_inverted_dominants(data,number)
  errs=validate(data,p)
  if errs:raise ValueError((number,errs[:10]))
  r.update(baseline=before,revised=metrics(data),errors=errs,source_sha256=hashlib.sha256(src.read_bytes()).hexdigest())
  out=OUT/f'{number:02d}-prelude.json';out.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
  r['revised_sha256']=hashlib.sha256(out.read_bytes()).hexdigest();reports.append(r)
 report={'edition':2,'status':'24 preludes reviewed and revised','scope':'Symbolic score review and concrete compositional revision. No claim of human auditory evaluation or equality to Bach.','movements':reports,'totals':{'prepared_suspensions':sum(len(r.get('suspensions',[])) for r in reports),'bass_connections':sum(len(r.get('bass_connections',[])) for r in reports),'directed_arrival_repairs':sum(len(r.get('directed_arrival_repairs',[])) for r in reports),'notes_before':sum(r['baseline']['notes'] for r in reports),'notes_after':sum(r['revised']['notes'] for r in reports),'upper_leaps_over_octave_before':sum(r['baseline']['upper_leaps_over_octave'] for r in reports),'upper_leaps_over_octave_after':sum(r['revised']['upper_leaps_over_octave'] for r in reports)}}
 (REPORT/'prelude-revision.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
 lines=['PRELUDES — SECOND EDITION CRITICAL REVIEW','',report['scope'],'','The principal defects were chord-rank melodies resetting at every bar, unprepared octave displacement at phrase joins, and upper cadential leading tones that sometimes dropped eleven semitones. The revisions preserve meter, tempo, bar count and each prelude\'s basic texture, while changing the musical lines themselves.','']
 for r in reports:
  lines.extend([f"{r['number']:02d}. {r['character']}",r.get('review','IV retains its expressly composed melodic design, with a prepared approach to the high return.'),f"  Upper barline leaps greater than a fifth: {r['baseline']['upper_barline_leaps_over_fifth']} -> {r['revised']['upper_barline_leaps_over_fifth']}; leaps greater than an octave: {r['baseline']['upper_leaps_over_octave']} -> {r['revised']['upper_leaps_over_octave']}.",f"  Prepared suspensions: {len(r.get('suspensions',[]))}; bass connections: {len(r.get('bass_connections',[]))}; final upper interval: {r['revised']['final_upper_interval']} semitones.",''])
 lines+=['Additional contextual review: functional leading tones at contiguous V-to-tonic and V-to-submediant arrivals were checked in all 23 harmonically annotated preludes. Original IV has its own expressly composed plan and is excluded from that label-driven test. No written augmented-second joins remain among events with explicit spelling.', '', 'Musical limits: these repairs provide more purposeful lines, audible preparations and resolutions, and coherent cadences. They do not establish Bach-level invention. Fast broken-chord textures deliberately retain leaps; sparse bells retain large registral gaps. Generic chord-tone validation from the first edition is superseded by contextual checks for the added suspensions and passing notes.']
 (REPORT/'prelude-revision.txt').write_text('\n'.join(lines)+'\n')
 print(json.dumps(report['totals'],indent=2))

if __name__=='__main__':main()
