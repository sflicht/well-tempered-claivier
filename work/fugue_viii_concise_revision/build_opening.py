#!/usr/bin/env python3
"""Build the 112-beat opening, with clarinet's boundary phrase through 116.

The source is immutable. All musical replacements below are literal phrases;
no statistical consonance optimizer or chord-grid filler is used.
"""
from pathlib import Path
import copy, hashlib, json, re, sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
SOURCE=ROOT/'work/fugue_viii_passage_revision/08-fugue-passage-revised.json'
EXPECTED='8875eb04af5b75105fa2dddb1fae68b11a59fbc9fbd32a73fdccc6c16a85daa6'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED
old=json.loads(SOURCE.read_text())
s=copy.deepcopy(old)
windows=[(0,56,0),(72,128,-16)]
repairs=[]

def midi(p):
    m=re.fullmatch(r'([A-G])([b#]?)([0-8])',p)
    return 12*(int(m[3])+1)+dict(C=0,D=2,E=4,F=5,G=7,A=9,B=11)[m[1]]+{'':0,'b':-1,'#':1}[m[2]]

def spelling(p):
    return p[0].lower()+('es' if 'b' in p else 'is' if '#' in p else '')

def parse(text):
    return [(p,float(d)) for p,d in (x.split(':') for x in text.split())]

# Each selected window begins/ends on note boundaries in this source. Assert
# that instead of silently truncating a sustained note.
for vi,v in enumerate(s['voices']):
    ev=[]
    for a,b,delta in windows:
        for e in old['voices'][vi]['events']:
            if e['t']<b and e['t']+e['d']>a:
                assert a<=e['t'] and e['t']+e['d']<=b, ('cut-note',vi,a,b,e)
                q=copy.deepcopy(e);q['t']+=delta;ev.append(q)
    # Preserve the whole relative-major bridge across the new episode join.
    if vi==2:
        for e in old['voices'][vi]['events']:
            if 128<=e['t']<132:
                q=copy.deepcopy(e);q['t']-=16;ev.append(q)
    v['events']=ev

s['phrase_map']=[]
for p in old['phrase_map']:
    for a,b,delta in windows:
        lo=max(a,p['t']);hi=min(b,p['t']+p['d'])
        if lo<hi:
            q=copy.deepcopy(p);q['t']=lo+delta;q['d']=hi-lo
            if lo!=p['t'] or hi!=p['t']+p['d']:
                q['description']='Retained portion: '+q.get('description','')
            s['phrase_map'].append(q)
for p in s['phrase_map']:
    if p['voice']==2 and p['t']==108:
        p['d']=8;p['description']='Complete relative-major bridge, carried through the episode join'

# Map candidate annotations, then retain only literal matches after composing.
s['subject_entries']=[];s['motivic_fragments']=[]
for field in ('subject_entries','motivic_fragments'):
    for e in old[field]:
        for a,b,delta in windows:
            if a<=e['t']<b:
                q=copy.deepcopy(e);q['t']+=delta;s[field].append(q)

base=[58,60,63,67,66,62,65,67,68]
def replace(vi,t,text,d,description,family='continuation'):
    notes=parse(text)
    assert abs(sum(x[1] for x in notes)-d)<1e-9
    end=t+d;kept=[]
    for e in s['voices'][vi]['events']:
        if e['t']<end and e['t']+e['d']>t:
            assert e['t']>=t and e['t']+e['d']<=end, ('replacement-cuts-note',vi,t,end,e)
        else:kept.append(e)
    cursor=t
    for j,(p,dur) in enumerate(notes):
        if p!='r':
            kept.append(dict(t=cursor,d=dur,p=midi(p),spell=spelling(p),v=base[vi]+(2 if j==0 else 0),
                             gate=.94 if dur<1 else .975,family=family,
                             phrase_description=description,source='Fugue VIII concise opening: composed harmonic join'))
        cursor+=dur
    s['voices'][vi]['events']=sorted(kept,key=lambda x:x['t'])
    s['phrase_map']=[p for p in s['phrase_map'] if not(p['voice']==vi and p['t']<end and p['t']+p['d']>t)]
    s['phrase_map'].append(dict(voice=vi,t=t,d=d,family=family,description=description))
    repairs.append(dict(voice=vi,start=t,end=end,description=description))

def edit(vi,t,p,reason):
    found=[e for e in s['voices'][vi]['events'] if e['t']==t]
    assert len(found)==1,(vi,t,found)
    e=found[0];e['p']=midi(p);e['spell']=spelling(p)
    e['source']='Fugue VIII concise opening: targeted pitch repair'
    e['revision_reason']=reason
    repairs.append(dict(voice=vi,start=t,end=t+e['d'],description=reason))

# Specific unexplained chromatic splits in the retained exposition.
edit(4,39,'Cb4','The inner descent uses C-flat with the simultaneous bassoon, eliminating the split sixth')
edit(2,43,'Cb4','D-flat descends through C-flat to B-flat before the dominant')
edit(6,45,'D3','The first dominant bassoon figure now has the major third of B-flat')

# The first nine-part cadence now has a directed predominant and dominant.
# At40 the earlier C-flat in cello belongs to A-flat minor; at42 the bass
# and supporting thirds identify F half-diminished. The fifth and seventh
# of B-flat then have clear roles before the tonic arrival at48.
replace(8,40,'Ab1:2 F2:1 Ab1:1 Bb1:2 F2:1 Bb1:1',8,
        'The ninth voice moves through A-flat minor and F half-diminished into B-flat dominant')
edit(1,42,'Ab5','The upper held A-flat belongs to the F half-diminished predominant')
edit(2,42,'Cb4','The clarinet gives the diminished fifth of F before the dominant')
edit(5,42,'Ab3','The horn supports the F half-diminished predominant with its minor third')
edit(5,43,'F3','The horn turns to the predominant root instead of adding an unrelated ninth')
edit(6,43,'Eb3','The bassoon seventh belongs to the F half-diminished approach')
edit(7,42,'Cb3','The cello C-flat continues the predominant before descending to A-flat')
edit(3,42.5,'F5','The dance head bends to the prevailing predominant instead of adding a flat ninth')
edit(3,43.5,'Ab5','The altered dance head closes onto the predominant third')
replace(5,44,'Ab3:1 Gb3:.5 F3:2.5',4,
        'The dominant seventh descends through a brief sixth into a held fifth')
replace(7,44,'F2:2 Ab2:1 Bb2:1',4,
        'A separate low fifth-seventh-root route supports the first dominant cadence')

# The cut deletes old56–72. A short dominant now joins old48–56 to an
# E-flat-minor arrival at new56; old72's C-flat bass is not pasted under it.
replace(1,52,'Db5:2 F5:1 Eb5:.5 D5:.5',4,
        'The oboe turns from the relative-major fifth through a resolved fourth into the leading note')
replace(7,52,'Cb3:1 Bb2:1 D3:1 F3:1',4,
        'The cello upper neighbor resolves, then rises through the dominant third and fifth')
replace(8,52,'Gb2:2 Bb1:2',4,
        'A brief relative-major support turns directly to the dominant at the cut')
edit(6,55,'D3','The bridge ending takes the leading note of E-flat before the tonic join')
for vi,p in [(2,'D4'),(3,'D5')]:
    edit(vi,55.5,p,'The dance tail becomes a tonal cadential variant, resolving its E-flat appoggiatura to D')

replace(1,56,'Eb5:1.5 F5:.5 Gb5:1 Bb4:1',4,
        'A new tonic continuation replaces the oboe phrase that formerly began before the cut')
replace(2,56,'Bb3:2 Eb4:1 Gb4:1 F4:1 Eb4:.5 D4:.5 Bb3:1 D4:1',8,
        'The clarinet rises through the tonic and contracts into a dominant reply')
replace(4,56,'Gb4:1.5 F4:.5 Gb4:1 Eb4:1 F4:.5 D4:.5 Eb4:1 D4:1.5 Eb4:.5',8,
        'A cadential chant variant turns its ending through a prepared fourth and a leading-note resolution',family='chant-cadential-variant')
replace(7,56,'Eb3:2 Bb2:1 Eb3:1 Ab2:1 F2:1 Bb2:1 F3:1',8,
        'A fresh cello answer names the tonic, then approaches the retort paragraph through the dominant')
replace(8,56,'Eb2:4 Bb1:2 F2:1 Bb1:1',8,
        'A concise tonic and B-flat dominant replace the cut bass circuit')
replace(5,60,'Gb3:1 F3:.5 Eb3:.5 D3:1 F3:1',4,
        'The horn continuation resolves its sixth and fourth into the dominant third')
replace(6,60,'Ab3:1 C4:.5 Bb3:.5 F3:1 Ab3:1',4,
        'An independent dominant-seventh reply rises briefly through its ninth, then falls to the fifth')
edit(0,63,'D5','The rising figure ends with the tonic leading note inside the B-flat dominant')
edit(3,63,'D5','The violin fourth resolves to the dominant third before the retort paragraph')
for t in (61,62.5):
    edit(1,t,'D5','The dominant dance answer uses D-natural while the bass establishes B-flat major')
edit(1,66.75,'Cb5','The answer tail returns to the E-flat-minor collection after the tonic arrival')

# Keep all five new retorts exactly. A lower supporting line is adjusted
# so its held fourth resolves into G-flat while the bassoon's F remains a
# short passing ninth; the previous duplicate low F is removed.
replace(5,68,'Ab3:1.5 Gb3:.5 Cb3:1 Bb2:1',4,
        'The horn fourth is prepared over the passing harmony and resolves to the tonic third')

# Add explicitly named tonal variants, not false exact-original labels.
def variant(sid,vi,t,d,parent,description):
    events=[]
    for e in s['voices'][vi]['events']:
        if t<=e['t']<t+d:
            events.append({k:(e[k]-t if k=='t' else e[k]) for k in ('t','d','p','spell')})
    s['subjects'][sid]=dict(duration=d,events=events,derived_from=parent,technique=description)
    s['subject_entries'].append(dict(voice=vi,t=t,subject_id=sid,transpose=0,scale=1,label=description))

variant('dance_cadential',2,48,8,'dance','Dance with a tonal cadence')
s['subject_entries'].append(dict(voice=3,t=48,subject_id='dance_cadential',transpose=12,scale=1,label='Cadential dance in the upper voice'))
variant('bridge_cadential_low',6,48,8,'bridge','Rising companion with leading-note cadence')
variant('bridge_cadential_high',0,56,8,'bridge','Rising companion directed through the dominant')
variant('chant_cadential',4,56,8,'chant','Chant with cadential ending')
variant('dance_tonal_answer',1,60,8,'dance','Tonal dominant answer returning to minor')

# Compare literal note triples, including durations, for every annotation.
def note_triples(vi,t,end):
    return [(e['t'],e['d'],e['p']) for e in s['voices'][vi]['events'] if t<=e['t']<end]
def entry_match(e):
    template=s['subjects'][e['subject_id']];scale=e.get('scale',1);tr=e.get('transpose',0);t=e['t']
    expected=[(t+x['t']*scale,x['d']*scale,x['p']+tr) for x in template['events']]
    return note_triples(e['voice'],t,t+template['duration']*scale)==expected
removed=[];entries=[]
for e in s['subject_entries']:
    if entry_match(e):entries.append(e)
    else:removed.append(e)
s['subject_entries']=sorted(entries,key=lambda e:(e['t'],e['voice']))
def fragment_match(e):
    temp=s['subjects'][e['source_subject']]['events'];sel=[temp[i] for i in e['source_note_indices']]
    start=sel[0]['t'];scale=e.get('scale',1);tr=e.get('transpose',0);t=e['t']
    expected=[(t+(x['t']-start)*scale,x['d']*scale,x['p']+tr) for x in sel]
    return note_triples(e['voice'],t,t+e['d'])==expected
s['motivic_fragments']=[e for e in s['motivic_fragments'] if fragment_match(e)]

s['metadata']['edition']='Concise piano revision: opening component'
s['metadata']['instrument']='Piano, nine contrapuntal lines'
s['metadata']['lesson_rendering']='piano'
s['metadata']['key_changes']=[]
s['metadata']['markers']=[dict(t=0,label='Subject and answers'),dict(t=40,label='First dominant'),dict(t=56,label='Compressed return'),dict(t=64,label='Three-beat retorts'),dict(t=96,label='Relative-major respite')]
s['sections']=[dict(t=a,end=b,d=b-a,label=label,detail=detail) for a,b,label,detail in [
    (0,48,'Subject and answers','The first cadence is clarified through a predominant and B-flat dominant.'),
    (48,64,'A shorter exchange','Tonal endings bridge the removed four-bar circuit.'),
    (64,96,'Three-beat retorts','The short question migrates through five voices; the bass reaches the relative-major dominant.'),
    (96,112,'Relative-major respite','The quiet space lasts four bars, with a clarinet phrase carried into the next episode.')]]
s['pedagogy']['annotations']=[dict(t=0,end=40,title='Subject and answers',text='The measured subject, rising companion and quicker idea enter in different registers.'),dict(t=40,end=48,title='A clear first cadence',text='A-flat minor and F half-diminished lead into B-flat dominant.'),dict(t=48,end=64,title='The exchange is shortened',text='Cadential variants give the cut a tonal destination. D-natural resolves toward E-flat.'),dict(t=64,end=80,title='The three-beat retort',text='Clarinet, violin, cello, viola and horn exchange a short question across the barlines.'),dict(t=80,end=96,title='The relative major approaches',text='The longer lines gather around a D-flat dominant; the short replies continue independently.'),dict(t=96,end=112,title='A brief room of light',text='The upper resolutions arrive in stages. The clarinet carries its rising figure into the next episode.')]
s['phrase_map']=sorted(s['phrase_map'],key=lambda x:(x['t'],x['voice']))
s['composition_record']['concise_opening']={
    'source_sha256':EXPECTED,'retained_source_windows':windows,'structural_end':112,
    'boundary_extension':{'voice':2,'start':112,'end':116,'notes':'Db5:1.5 Cb5:.5 Ab4:1 F4:1'},
    'repairs':repairs,'original_annotations_removed_after_changes':removed,
    'claim':'Literal composition and score checking only; not auditory or historical-style certification'}

for vi,v in enumerate(s['voices']):
    v['events'].sort(key=lambda x:x['t'])
    prev=0
    for e in v['events']:
        assert e['t']>=prev-1e-9 and e['d']>0,(vi,e,prev)
        prev=e['t']+e['d']
        assert prev<= (116 if vi==2 else 112)+1e-9
assert all(entry_match(e) for e in s['subject_entries'])
assert all(fragment_match(e) for e in s['motivic_fragments'])
# The identity of the five newly composed retorts must survive literally.
retorts=[e for e in s['motivic_fragments'] if e['source_subject']=='chant_retort']
assert len(retorts)==5
assert note_triples(2,112,116)==[(112,1.5,midi('Db5')),(113.5,.5,midi('Cb5')),(114,1,midi('Ab4')),(115,1,midi('F4'))]
(HERE/'opening.json').write_text(json.dumps(s,indent=2,ensure_ascii=False)+'\n')
(HERE/'opening-checks.json').write_text(json.dumps({'monophonic':True,'structural_beats':112,'boundary_extension_beats':4,'exact_entries':len(s['subject_entries']),'exact_fragments':len(s['motivic_fragments']),'five_retorts_intact':True,'notes':sum(len(v['events']) for v in s['voices'])},indent=2)+'\n')
print(json.dumps({'output':str(HERE/'opening.json'),'sha256':hashlib.sha256((HERE/'opening.json').read_bytes()).hexdigest(),'notes':sum(len(v['events']) for v in s['voices']),'entries':len(s['subject_entries']),'fragments':len(s['motivic_fragments'])},indent=2))
