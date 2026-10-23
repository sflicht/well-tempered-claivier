#!/usr/bin/env python3
"""Let the outer choirs complete full phrases around the long dominant.

Parts that cannot sustain a strict triadic route through every change are
phrased through the opening and tonic answer, with a substantial central rest.
This is an audible choral exchange, not a delayed attack concealing parallels.
"""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'vendor'));sys.path.insert(0,str(ROOT/'tools'))
import revise_dense_fugues as r
OUT=ROOT/'work/revision/dense_fugues'
def finish(n):
 p=OUT/f'{n:02d}-fugue.json';d=json.loads(p.read_text());sec=next(s for s in d['sections']if s['label']=='Gathered development');a,b=sec['t'],sec['t']+sec['d'];core=r.getgrid(d,a,b);missing=[v for v,ps in core.items()if all(p is None for p in ps)];rec=[]
 # Opening progression lasts five full two-bar stages in these late fugues.
 for stop in [a+40,a+24]:
  todo=[v for v in missing if all(p is None for p in r.getgrid(d,a,stop)[v])]
  if not todo:continue
  rec.append(r.insert_continuations(d,a,stop,todo,.30,'Opening choir continuation',common_boundaries=True))
 # Reply after the long dominant; the rest is formal and lasts several bars.
 start=b-16
 todo=[v for v in missing if all(p is None for p in r.getgrid(d,start,b)[v])]
 if todo:rec.append(r.insert_continuations(d,start,b,todo,.30,'Returning choir reply',common_boundaries=True))
 sec['voices']=sorted(v for v,ps in r.getgrid(d,a,b).items()if any(x is not None for x in ps))
 sec['detail']='All choirs join the opening sequence; the outer choirs breathe through the long dominant and return for the tonic reply. Two exact augmented subject-head fragments anchor the paragraph.'
 r.cf.apply_spellings(d);d['composition_record']['dense_revision']['phrase_replies']=rec
 audit=r.audit_music.audit(d,max_examples=100);p.write_text(json.dumps(d,indent=2));(OUT/f'{n:02d}-dense-audit.json').write_text(json.dumps(audit,indent=2));print(json.dumps({'number':n,'records':rec,'after':r.density(d)}),flush=True)
if __name__=='__main__':
 for n in list(map(int,sys.argv[1:])):finish(n)
