#!/usr/bin/env python3
"""Apply reviewed phrase repairs to the staged second-edition small fugues.

This is a guarded edit to specified, checked realizations, not a general rule
that every occurrence of scale degree seven must resolve upward immediately.
"""
from pathlib import Path
import copy,json,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import audit_music
from revise_small_fugues import spelling_table

DIRECTORY=ROOT/'work/revision/small_fugues'

def replace(data, voice, onset, pitch, fragments):
    es=data['voices'][voice]['events']
    ix=next(i for i,e in enumerate(es) if e['t']==onset and e['p']==pitch)
    old=es[ix]
    assert abs(sum(f[1] for f in fragments)-old['d'])<1e-7
    new=[];t=onset
    for p,d,classification in fragments:
        e=dict(old,t=t,d=d,p=p)
        h=next(h for h in reversed(data['harmony']) if h['t']<=t)
        e['spell']=spelling_table(h['key_name'],h['key'],h['mode'])[p%12]
        if classification:
            e['counterpoint_device']=classification
        new.append(e);t+=d
    es[ix:ix+1]=new

def repair(num,data):
    notes=[]
    if num==2:
        replace(data,0,60,83,[(83,.5,None),(84,.5,'Unaccented passing resolution of the leading tone')])
        notes.append('V01, beat60: B5 now rises through C6 on the weak eighth before D6, replacing B-to-D departure with a directed B-C-D line.')
    elif num==5:
        replace(data,2,127,73,[(61,1,None)])
        replace(data,2,130,69,[(62,1,None)])
        notes.append('V03, beats127–131: C-sharp remains in one register through iii and resolves to D on tonic; removed the gratuitous octave displacement and delayed leap to A.')
    elif num==6:
        replace(data,4,139,56,[(56,.5,None),(57,.5,'Unaccented passing resolution of the leading tone')])
        # E is common to V and iii in the relative major. Sustain it through
        # that chord; its upper escape F gives the tendency tone a real
        # resolution before the line releases down to D on IV.
        replace(data,3,104,60,[(64,1.5,None),(65,.5,'Unaccented upper escape tone after retained leading note')])
        entry=next(e for e in data['subject_entries'] if e['voice']==3 and e['subject_id']=='countersubject_relative')
        template=data['subjects']['countersubject_relative']['events']
        local=104-entry['t'];shift=entry['transpose']
        ix=next(i for i,e in enumerate(template) if e['t']==local and e['p']+shift==60)
        old=template[ix]
        template[ix:ix+1]=[dict(old,p=64-shift,d=1.5),dict(old,t=local+1.5,p=65-shift,d=.5)]
        notes.append('Relative countersubject: E is retained across V-to-iii, rises briefly to F, then releases to D; its template and written statement are changed together.')
        notes.append('V05, beat139: G-sharp now passes through A on the weak eighth before B in the A-minor stretto continuation.')
    elif num==7:
        replace(data,1,153,79,[(67,1,None)])
        replace(data,1,154,86,[(74,1,None)])
        replace(data,1,155,79,[(74,1,None),(75,1,None),(79,1,None)])
        replace(data,6,155,62,[(58,1,None)])
        notes.append('V02, beats153–157: D is retained through iii and rises to E-flat at vi, then continues to G. Removed the arbitrary octave lift and the unresolved D-to-G fall.')
        notes.append('V07 sustains B-flat at beat155 so its following move to E-flat does not duplicate V02 in parallel octaves.')
    data.setdefault('composition_record',{}).setdefault('reviewed_phrase_repairs',[]).extend(notes)
    return notes

def gates(data):
    r=audit_music.audit(data,max_examples=300)
    bad=[]
    for vi,v in enumerate(data['voices']):
        for a,b in zip(v['events'],v['events'][1:]):
            if a['t']+a['d']==b['t'] and (abs(a['p']-b['p']) in [6,10,11] or abs(a['p']-b['p'])>12):
                bad.append((vi,a['t'],b['t'],a['p'],b['p']))
    s=r['summary']
    fields=['data_errors','exact_octave_duplicate_pairs','parallel_perfect_interval_candidates_at_shared_attacks',
            'structural_grid_parallel_candidates','outer_similar_motion_into_perfect_with_upper_leap_candidates',
            'accented_dissonance_observations']
    return r,bad,{f:s[f] for f in fields if s[f]}

def main():
    report_path=DIRECTORY/'reviewed-phrase-repairs.json'
    reports=json.loads(report_path.read_text()) if report_path.exists() else []
    for num in [2,5,6,7]:
        p=DIRECTORY/f'{num:02d}-fugue.json'
        old=p.read_bytes();data=json.loads(old)
        if data.get('composition_record',{}).get('reviewed_phrase_repairs'):
            if not any(r['number']==num for r in reports):
                reports.append({'number':num,'after_sha256':hashlib.sha256(old).hexdigest(),
                                'notes':data['composition_record']['reviewed_phrase_repairs']})
            print(json.dumps({'number':num,'already_applied':True}));continue
        notes=repair(num,data)
        report,bad,flags=gates(data)
        summary={'number':num,'before_sha256':hashlib.sha256(old).hexdigest(),
                 'notes':notes,'flagged_gates':flags,'melodic_flags':bad,
                 'matched_entries':report['summary']['matched_subject_entries'],
                 'total_entries':report['summary']['documented_subject_entries']}
        print(json.dumps(summary),flush=True)
        (DIRECTORY/f'{num:02d}-repair-proposal.json').write_text(json.dumps(data,indent=2))
        if flags or bad or summary['matched_entries']!=summary['total_entries']:
            continue
        p.write_text(json.dumps(data,indent=2))
        (DIRECTORY/f'{num:02d}-audit.json').write_text(json.dumps(report,indent=2))
        summary['after_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
        reports=[r for r in reports if r['number']!=num]+[summary]
    report_path.write_text(json.dumps(sorted(reports,key=lambda r:r['number']),indent=2))

if __name__=='__main__':main()
