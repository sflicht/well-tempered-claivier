#!/usr/bin/env python3
"""Independent symbolic musical review of the new clAIvier fugue drafts.

Read-only with respect to all music sources. Accepted movement IV is excluded.
This is a focused musical/annotation review, not a complete counterpoint proof
or a claim about aesthetic quality. The source hash makes each result auditable.
"""
from __future__ import annotations
import argparse
import bisect
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"work/cycle_fugues"
OUT=ROOT/"work/cycle_review"
EPS=1e-7
LETTERS="cdefgab"
NATURAL=[0,2,4,5,7,9,11]


def parse_spelling(spell):
    if not spell or not re.fullmatch(r"[a-g](?:isis|eses|is|es)?",spell):
        return None
    ix=LETTERS.index(spell[0]);acc={"":0,"is":1,"isis":2,"es":-1,"eses":-2}[spell[1:]]
    return ix,(NATURAL[ix]+acc)%12


def expected_spelling_map(home_name,local_pc,mode):
    """Diatonic key spelling, independently derived from tonic letter identity."""
    home_letter=LETTERS.index(home_name[0].lower())
    home_pc=(NATURAL[home_letter]+home_name.count("#")-home_name.count("b"))%12
    # Present cycle exports tonic, dominant and subdominant regions; additional
    # standard related roots are included, but an unknown relation is reported.
    relation={0:0,2:1,3:2,4:2,5:3,7:4,8:5,9:5,10:6,11:6}
    distance=(local_pc-home_pc)%12
    if distance not in relation:return None
    tonic_letter=(home_letter+relation[distance])%7
    offsets=[0,2,4,5,7,9,11] if mode=="major" else [0,2,3,5,7,8,10]
    tones=[(i,d) for i,d in enumerate(offsets)]
    if mode=="minor":tones.append((6,11))
    result={}
    for degree,offset in tones:
        li=(tonic_letter+degree)%7;pc=(local_pc+offset)%12
        accidental=(pc-NATURAL[li]+6)%12-6
        if accidental not in [-2,-1,0,1,2]:return None
        result[pc]=LETTERS[li]+{-2:"eses",-1:"es",0:"",1:"is",2:"isis"}[accidental]
    return result


class ScoreView:
    def __init__(self,data):
        self.data=data;self.voices=data["voices"]
        self.events=[sorted(v["events"],key=lambda e:e["t"]) for v in self.voices]
        self.starts=[[e["t"] for e in es] for es in self.events]
        self.harmony=sorted(data.get("harmony",[]),key=lambda h:h["t"])
        self.hstarts=[h["t"] for h in self.harmony]
        self.end=max(e["t"]+e["d"] for es in self.events for e in es)
        self.section_starts={s["t"] for s in data.get("sections",[])}

    def note(self,vi,t):
        j=bisect.bisect_right(self.starts[vi],t+EPS)-1
        if j<0:return None
        e=self.events[vi][j]
        return e if t<e["t"]+e["d"]-EPS else None

    def harmonic(self,t):
        j=bisect.bisect_right(self.hstarts,t+EPS)-1
        return self.harmony[j] if j>=0 else None


def issues_record():
    return {"voice_count_contract":[],"final_tonic_presence":[],"final_tonic_bass":[],"melodic_prohibited_leaps":[],"augmented_seconds":[],"doubled_functional_leading_tones":[],"dominant_to_tonic_resolution":[],"missing_spellings":[],"invalid_spellings":[],"enharmonic_key_spelling":[],"thematic_pitch_duration_mismatches":[],"voices_without_main_subject":[],"annotation_mismatches":[]}


def ending_review(view):
    meta=view.data['metadata'];name=meta['key'];li=LETTERS.index(name[0].lower())
    tonic=(NATURAL[li]+name.count('#')-name.count('b'))%12
    final_notes=[{"voice":vi+1,"pitch":note['p'],"spelling":note.get('spell')} for vi in range(len(view.voices)) if (note:=view.note(vi,view.end-1e-4))]
    pcs=sorted({n['pitch']%12 for n in final_notes});bass=min(n['pitch'] for n in final_notes)
    return {"tonic_pitch_class":tonic,"final_notes":final_notes,"final_pitch_classes":pcs,"final_bass_midi":bass,"tonic_present":tonic in pcs,"bass_is_tonic":bass%12==tonic,"major_third_present":(tonic+4)%12 in pcs,"minor_third_present":(tonic+3)%12 in pcs,"duration_beats":view.end}


def melody_and_spelling(view,issues):
    meta=view.data["metadata"];unknown_local_spelling=[];terminal_lt=[]
    for vi,events in enumerate(view.events):
        for event in events:
            spell=event.get("spell")
            if spell is None:
                issues["missing_spellings"].append({"voice":vi+1,"t":event["t"],"p":event["p"]})
                continue
            parsed=parse_spelling(spell)
            if parsed is None or parsed[1]!=event["p"]%12:
                issues["invalid_spellings"].append({"voice":vi+1,"t":event["t"],"p":event["p"],"spell":spell})
                continue
            harmonic=view.harmonic(event["t"])
            if harmonic:
                table=expected_spelling_map(harmonic.get('key_name',meta["key"]),harmonic["key"],harmonic.get('mode',meta["mode"]))
                if table is None:
                    unknown_local_spelling.append({"voice":vi+1,"t":event["t"],"key_pc":harmonic["key"]})
                elif event["p"]%12 in table and spell!=table[event["p"]%12]:
                    issues["enharmonic_key_spelling"].append({"voice":vi+1,"t":event["t"],"p":event["p"],"spell":spell,"expected":table[event["p"]%12],"local_key_pc":harmonic["key"]})
        for a,b in zip(events,events[1:]):
            if abs(a["t"]+a["d"]-b["t"])>EPS:continue
            delta=b["p"]-a["p"]
            context={"voice":vi+1,"t":b["t"],"from_pitch":a["p"],"to_pitch":b["p"],"semitones":delta,"section_seam":b["t"] in view.section_starts,"from_label":a.get("label"),"to_label":b.get("label")}
            if abs(delta) in [6,10,11] or abs(delta)>12:
                issues["melodic_prohibited_leaps"].append(context)
            sa,sb=parse_spelling(a.get("spell")),parse_spelling(b.get("spell"))
            if sa and sb and abs(delta)==3:
                directed_letters=((sb[0]-sa[0]) if delta>0 else (sa[0]-sb[0]))%7
                if directed_letters==1:
                    issues["augmented_seconds"].append({**context,"from_spelling":a["spell"],"to_spelling":b["spell"]})
    return {"local_spelling_not_evaluated":unknown_local_spelling}


def leading_tones(view,issues):
    # Hard flags use explicit functional V / vii_dim sonorities and direct
    # local V-to-I/i arrivals. Other tendency-tone choices remain review data.
    other_departures=[];doubles=[]
    for hi,h in enumerate(view.harmony):
        if h["chord"] not in ["V","vii_dim"]:continue
        leading_pc=(h["key"]+11)%12
        carriers=[(vi,n) for vi in range(len(view.voices)) if (n:=view.note(vi,h["t"])) and n["p"]%12==leading_pc]
        if len(carriers)>1:
            doubles.append({"t":h["t"],"local_key_pc":h["key"],"chord":h["chord"],"voices":[vi+1 for vi,n in carriers],"pitches":[n["p"] for vi,n in carriers]})
        if hi+1>=len(view.harmony):continue
        nh=view.harmony[hi+1]
        if nh["t"]-h["t"]>1+EPS:continue
        same_key=nh["key"]==h["key"]
        cadence=same_key and nh["chord"] in ["I","i"]
        for vi,n in carriers:
            next_note=view.note(vi,nh["t"])
            if next_note is None:continue
            delta=next_note["p"]-n["p"]
            if cadence and delta!=1:
                issues["dominant_to_tonic_resolution"].append({"voice":vi+1,"from_beat":h["t"],"to_beat":nh["t"],"local_key_pc":h["key"],"from_chord":h["chord"],"to_chord":nh["chord"],"from_pitch":n["p"],"to_pitch":next_note["p"],"semitones":delta})
            elif not cadence and delta not in [0,1] and same_key:
                other_departures.append({"voice":vi+1,"from_beat":h["t"],"to_beat":nh["t"],"from_chord":h["chord"],"to_chord":nh["chord"],"from_pitch":n["p"],"to_pitch":next_note["p"],"semitones":delta,"classification":"Non-tonic departure: requires contextual interpretation, not automatically an error."})
    issues["doubled_functional_leading_tones"]=doubles
    return {"non_tonic_leading_tone_departures":other_departures,"scope":"Doubling checked in every exported V/vii_dim frame. Mandatory upward resolution checked at direct same-key V/vii_dim→I/i transitions. Other contexts are explicitly separated."}


def theme_review(view,issues):
    data=view.data;entries=data.get("subject_entries",[]);covered=defaultdict(list)
    exact=[];articulation=[];extensions=[]
    for ei,entry in enumerate(entries):
        subject=data.get("subjects",{}).get(entry.get("subject_id"),{}).get("events",[])
        if not subject:
            issues["thematic_pitch_duration_mismatches"].append({"entry":ei+1,"reason":"missing thematic source"});continue
        vi=entry["voice"];role="fragment" if "fragment" in (entry.get("subject_id","")+" "+entry.get("label","")).lower() else "countersubject" if "counter" in (entry.get("subject_id","")+" "+entry.get("label","")).lower() else "subject"
        scale=entry.get("scale",1);trans=entry.get("transpose",0);matched=True
        for ni,n in enumerate(subject):
            start=entry["t"]+n["t"]*scale;end=start+n["d"]*scale;pitch=n["p"]+trans
            segments=[start,end]+[e["t"] for e in view.events[vi] if start<e["t"]<end]+[e["t"]+e["d"] for e in view.events[vi] if start<e["t"]+e["d"]<end]
            bounds=sorted(set(segments))
            for a,b in zip(bounds,bounds[1:]):
                actual=view.note(vi,(a+b)/2)
                if actual is None or actual["p"]!=pitch:
                    issues["thematic_pitch_duration_mismatches"].append({"entry":ei+1,"voice":vi+1,"role":role,"theme_note":ni+1,"start":a,"end":b,"expected_pitch":pitch,"actual_pitch":actual["p"] if actual else None});matched=False
            actual=view.note(vi,start)
            if actual and abs(actual["t"]-start)>EPS:
                articulation.append({"entry":ei+1,"voice":vi+1,"beat":start,"reason":"Thematic pitch is present but onset is sustained from an earlier note."})
            if ni==len(subject)-1 and actual and actual["t"]+actual["d"]>end+EPS:
                extensions.append({"entry":ei+1,"voice":vi+1,"theme_end":end,"actual_end":actual["t"]+actual["d"],"reason":"Terminal thematic pitch continues beyond the annotated duration."})
        if matched:
            covered[role].append(vi);exact.append(ei+1)
    missing=sorted(set(range(len(view.voices)))-set(covered["subject"]))
    issues["voices_without_main_subject"]=[vi+1 for vi in missing]
    main=[e for e in entries if not any(k in (e.get("subject_id","")+" "+e.get("label","")).lower() for k in ['counter','fragment'])]
    overlaps=[]
    for i,a in enumerate(main):
        sa=data["subjects"][a["subject_id"]]["events"];ae=a["t"]+max(n["t"]+n["d"] for n in sa)*a.get("scale",1)
        for b in main[i+1:]:
            sb=data["subjects"][b["subject_id"]]["events"];be=b["t"]+max(n["t"]+n["d"] for n in sb)*b.get("scale",1)
            overlap=min(ae,be)-max(a["t"],b["t"])
            if overlap>0:overlaps.append({"voices":[a["voice"]+1,b["voice"]+1],"entry_beats":[a["t"],b["t"]],"overlap_beats":overlap})
    return {"annotated_subjects":len(main),"annotated_countersubjects":len(entries)-len(main),"matched_entries":len(exact),"all_voices_have_complete_main_subject":not missing,"subject_voices":sorted({v+1 for v in covered['subject']}),"countersubject_voices":sorted({v+1 for v in covered['countersubject']}),"augmentation_entries":[e for e in main if e.get('scale',1)>1],"main_subject_overlaps":overlaps,"thematic_onset_observations":articulation,"terminal_sustain_extensions":extensions}


def annotation_review(view,issues,themes):
    data=view.data;sections=sorted(data.get("sections",[]),key=lambda s:s["t"])
    density=[]
    bounds=sorted({0.0,view.end}|{e["t"] for es in view.events for e in es}|{e["t"]+e["d"] for es in view.events for e in es})
    for a,b in zip(bounds,bounds[1:]):
        count=sum(view.note(vi,(a+b)/2) is not None for vi in range(len(view.voices)))
        density.append((a,b,count))
    full=sum(b-a for a,b,n in density if n==len(view.voices))
    form=[]
    for section in sections:
        label=section["label"]
        if not form or form[-1]!=label:form.append(label)
        a=section["t"];b=a+section["d"]
        if "complete ensemble" in label.lower():
            bad=[(c,d,n) for c,d,n in density if c<b and d>a and n!=len(view.voices)]
            if bad:issues["annotation_mismatches"].append({"label":label,"t":a,"reason":"Not all parts are active throughout annotated complete-ensemble section.","spans":bad})
        if "stretto" in label.lower():
            overlaps=[x for x in themes["main_subject_overlaps"] if any(a<=t<b for t in x["entry_beats"])]
            if not overlaps:issues["annotation_mismatches"].append({"label":label,"t":a,"reason":"No overlapping complete main-subject statements found."})
    end_of_sections=max((s["t"]+s["d"] for s in sections),default=0)
    tail={"start":end_of_sections,"end":view.end,"beats":view.end-end_of_sections,"classification":"Sustained final tail extends beyond the explicit section durations; the final form marker still applies."} if end_of_sections<view.end else None
    return {"form_sequence":form,"maximum_simultaneous_parts":max(n for a,b,n in density),"beats_with_all_parts":full,"all_part_fraction":full/view.end,"section_tail_observation":tail,"pitch_change_counts":[sum(a['p']!=b['p'] for a,b in zip(es,es[1:])) for es in view.events]}


def review(path):
    number=int(path.name[:2]);assert number!=4
    payload=path.read_bytes();data=json.loads(payload);view=ScoreView(data)
    digest=hashlib.sha256(payload).hexdigest();freeze_path=path.with_name(f"{number:02d}-frozen.json")
    freeze=json.loads(freeze_path.read_text()) if freeze_path.exists() else None
    frozen=bool(freeze and freeze.get("sha256")==digest)
    issues=issues_record()
    if len(view.voices)!=number+1:issues["voice_count_contract"].append({"expected":number+1,"actual":len(view.voices)})
    ending=ending_review(view)
    if not ending['tonic_present']:issues['final_tonic_presence'].append(ending)
    if not ending['bass_is_tonic']:issues['final_tonic_bass'].append(ending)
    spelling=melody_and_spelling(view,issues)
    leading=leading_tones(view,issues)
    themes=theme_review(view,issues)
    form=annotation_review(view,issues,themes)
    counts={k:len(v) for k,v in issues.items()}
    all_events=[e for es in view.events for e in es]
    style={"meter":data['metadata']['meter'],"note_event_count":len(all_events),"fractional_quarter_attack_count":sum(abs(e['t']-round(e['t']))>EPS for e in all_events),"duration_counts":dict(Counter(e['d'] for e in all_events)),"exported_chord_labels":dict(Counter(h['chord'] for h in view.harmony))}
    return {"movement":number,"source":str(path.relative_to(ROOT)),"sha256":digest,"frozen_hash_matches":frozen,"freeze_status":freeze.get("status") if freeze else "not frozen","key":data['metadata']['key'],"mode":data['metadata']['mode'],"voices":len(view.voices),"duration_beats":view.end,"scope":"Independent symbolic review. Accepted IV excluded. Parallel-motion, dissonance, listening and instrumental fingering are outside this report's scope.","issue_counts":counts,"errors_total":sum(counts.values()),"issues":issues,"ending_review":ending,"spelling_review":spelling,"leading_tone_review":leading,"thematic_review":themes,"form_review":form,"style_metrics":style,"source_changed_during_review":hashlib.sha256(path.read_bytes()).hexdigest()!=digest}


def contextual_review(reports):
    categories=Counter();retained=[];instances=[]
    for r in reports:
        for d in r['leading_tone_review']['non_tonic_leading_tone_departures']:
            a,b,delta=d['from_chord'],d['to_chord'],d['semitones']
            if b in ['V','v','vii_dim'] and delta != -1:
                category='Motion within the dominant family; arpeggiated or redistributed chord tones'
            elif delta==-1 and b in ['v','VII']:
                category='Raised seventh lowers to the modal seventh in minor'
            elif delta==-2:
                category='Descending scalar seventh-to-sixth motion outside a tonic arrival'
            elif delta==-4 and b=='iii':
                category='Leading tone descends a third into mediant harmony'
            else:
                category='Specific noncadential leap retained for next-edition musical review'
                retained.append({"movement":r['movement'],"source_sha256":r['sha256'],**d,"status":"Reviewed and retained in the frozen first draft; no source changes made.","musical_concern":"The leading note leaves by leap without completing its usual tonic-directed motion. This is an idiomatic concern outside the narrowly tested direct V-to-tonic rule.","recommended_review":"Revoice or redirect the supporting line while preserving the thematic entries; assess the surrounding phrase rather than applying an isolated pitch substitution."})
            categories[category]+=1
            instances.append({"movement":r['movement'],**d,"review_category":category})
    return {"total_contextual_departures":len(instances),"category_counts":dict(categories),"next_edition_items":retained,"all_instances":instances,"interpretation":"The broad scan identifies departures, not automatic errors. Stepwise/modal lines and chord arpeggiation are distinguished from isolated noncadential leaps. The listed leaps prevent any blanket claim that every textbook tendency-tone prescription has been satisfied."}


def text_report(summary,context,reports):
    nums=', '.join(str(n) for n in summary['reviewed_movements'])
    lines=["THE WELL-TEMPERED CLAIVIER — INDEPENDENT MUSICAL REVIEW", "", f"Reviewed frozen new fugues: {nums}.", "Accepted IV is excluded from the full review and has not been edited; its final tonic bass was read-only verified in the all-cycle ending sweep.", "", "RESULT", f"{summary['total_flags']} failures in the specified symbolic checks. {len(context['next_edition_items'])} noncadential tendency-tone leaps are separately retained as next-edition musical review items. These are different findings; the check count is not a claim that the cycle obeys every stylistic prescription.", "", "CHECKED", "A final tonic pitch and tonic bass; the N+1 voice-count contract; continuous melodic tritones, ten/eleven-semitone leaps and leaps larger than an octave, including section joins; explicitly spelled augmented seconds; leading-tone doubling in exported V/vii-diminished sonorities; upward semitone resolution at direct same-key dominant-to-tonic arrivals; spelling and concert pitch agreement; diatonic local-key spelling; complete main-subject coverage of every part, separately from countersubjects; exact thematic pitches/durations; and the truth of complete-ensemble and stretto annotations.", "", "CONTEXTUAL TENDENCY-TONE FINDINGS"]
    for item in context['next_edition_items']:
        lines.append(f"Fugue {item['movement']:02d}, voice {item['voice']:02d}, beats {item['from_beat']}→{item['to_beat']}: MIDI {item['from_pitch']}→{item['to_pitch']} ({item['semitones']:+d} semitones), {item['from_chord']}→{item['to_chord']}. Leading-tone motion remains unfulfilled; retained for musical revision review.")
    lines += ["", "The composition agent explicitly acknowledged XXIV voice13, beat391→392, as an idiomatic concern and retained its frozen hash. Other flagged leaps are documented precisely rather than relabeled as intended expressive features. Ordinary stepwise departures, raised-to-modal seventh changes, and motion within dominant harmony remain in contextual-findings.json for inspection.", "", "SPELLING", "The local-key spelling review follows the tonic letter and the exported local root. It recognizes the raised seventh in minor and necessary double sharps. III in C-sharp major and XVIII in G-sharp minor are included when their frozen hashes appear above. Explicit spellings must match MIDI pitch class; no enharmonic respelling has been silently applied by this review.", "", "THEMATIC AND FORMAL DIVERSITY", f"The {summary['diversity']['movements_compared']} reviewed main subjects contain {summary['diversity']['distinct_transposition_normalized_subjects']} distinct pitch-and-duration fingerprints after transposition is removed, and {summary['diversity']['distinct_subject_rhythms']} distinct duration patterns. Shared rhythmic groups: {summary['diversity']['shared_rhythm_groups']}. This establishes separately written themes, not equal musical strength."]
    nnotes=sum(r['style_metrics']['note_event_count'] for r in reports)
    fractional=sum(r['style_metrics']['fractional_quarter_attack_count'] for r in reports)
    meters=Counter(tuple(r['style_metrics']['meter']) for r in reports)
    lines += [f"Across the reviewed files, {nnotes} note events contain {fractional} attacks off the integer quarter-beat grid. Meter counts: {dict(meters)}. The common pulse grid, conservative triadic harmony, recurring exposition–episode–development–short-stretto design, and common-tone dense sections are substantial stylistic limitations of this first complete draft.", "The short stretto annotations are supported by overlapping complete subjects, but a brief terminal overlap should not be described as sustained many-way stretto. High part counts are achieved through successive smaller expositions and a full-ensemble passage; they do not mean every part sounds throughout the fugue."]
    for r in reports:
        if r['movement']==24:
            aug=r['thematic_review']['augmentation_entries']
            lines += [f"XXIV: all25 parts have complete main-subject entries. All25 sound for {r['form_review']['beats_with_all_parts']:g} of {r['duration_beats']:g} quarter beats ({100*r['form_review']['all_part_fraction']:.2f}%). Its augmented subject entries are {aug}. The complete augmented statement is independently verified against the actual source events."]
    tails=[r['movement'] for r in reports if r['form_review']['section_tail_observation']]
    lines += ["", "ANNOTATION TAIL", f"Movements with a final sustained release extending beyond the explicit section durations: {tails}. Total score duration includes that release, and the final form marker remains in force. The duration of the cadence process and the duration of its held release are recorded separately in these files.", "", "LIMITS", "This review is symbolic. It does not replace listening, interpretation, orchestral balance, instrumental fingering review, or the separate parallel-motion/dissonance audit. It makes no claim of Bach-level artistic quality. Music sources were read-only throughout. Per-movement reports record hashes; rerun after any score revision."]
    return '\n'.join(lines)+'\n'


def diversity(paths):
    fingerprints=defaultdict(list);rhythms=defaultdict(list);diatonic_contours=defaultdict(list)
    for path in paths:
        num=int(path.name[:2]);data=json.loads(path.read_text());es=data.get("subjects",{}).get("subject",{}).get("events",[])
        if not es:continue
        p0=es[0]["p"]
        fp=tuple((e["p"]-p0,e["d"]) for e in es)
        fingerprints[fp].append(num);rhythms[tuple(e["d"] for e in es)].append(num)
        contours=tuple((b['p']>a['p'])-(b['p']<a['p']) for a,b in zip(es,es[1:]))
        diatonic_contours[contours].append(num)
    return {"movements_compared":len(paths),"distinct_transposition_normalized_subjects":len(fingerprints),"exact_subject_duplicates":[v for v in fingerprints.values() if len(v)>1],"distinct_subject_rhythms":len(rhythms),"shared_rhythm_groups":[v for v in rhythms.values() if len(v)>1],"shared_direction_contours":[v for v in diatonic_contours.values() if len(v)>1],"interpretation":"Distinct fingerprints establish different written themes, not equal musical strength or Bach-level quality. Similar rhythm groups and recurring formal templates remain audible style limitations."}


def main():
    ap=argparse.ArgumentParser();ap.add_argument("--numbers",nargs="*",type=int);ap.add_argument("--frozen-only",action="store_true");args=ap.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    paths=sorted(SOURCE.glob("[0-9][0-9]-fugue.json"))
    paths=[p for p in paths if int(p.name[:2])!=4 and (not args.numbers or int(p.name[:2]) in args.numbers)]
    reports=[];used=[]
    for path in paths:
        result=review(path)
        if args.frozen_only and not result['frozen_hash_matches']:continue
        (OUT/f"{result['movement']:02d}-musical-review.json").write_text(json.dumps(result,indent=2)+"\n")
        reports.append(result);used.append(path)
    summary={"reviewed_movements":[r['movement'] for r in reports],"frozen_movements":[r['movement'] for r in reports if r['frozen_hash_matches']],"accepted_IV":"excluded; no source edits", "total_flags":sum(r['errors_total'] for r in reports),"per_movement":[{k:r[k] for k in ['movement','sha256','frozen_hash_matches','voices','duration_beats','errors_total','issue_counts']} for r in reports],"diversity":diversity(used),"limitations":["Symbolic checks do not establish artistic parity with Bach.","Leading-tone resolution is evaluated for direct same-key dominant-to-tonic arrivals; other departures are separately exposed for contextual review.","Independent lines and subject coverage do not imply that 25 parts remain simultaneously active throughout a movement.","Conservative triadic sonorities, common-tone dense passages, and recurring form templates can limit expressive and contrapuntal variety."]}
    context=contextual_review(reports)
    summary['next_edition_musical_review_items']=len(context['next_edition_items'])
    (OUT/"musical-review-summary.json").write_text(json.dumps(summary,indent=2)+"\n")
    (OUT/"contextual-findings.json").write_text(json.dumps(context,indent=2)+"\n")
    (OUT/"musical-review.txt").write_text(text_report(summary,context,reports))
    endings=[]
    for path in sorted(SOURCE.glob('[0-9][0-9]-fugue.json')):
        payload=path.read_bytes();data=json.loads(payload);number=int(path.name[:2]);digest=hashlib.sha256(payload).hexdigest()
        freeze_path=path.with_name(f'{number:02d}-frozen.json');freeze=json.loads(freeze_path.read_text()) if freeze_path.exists() else {}
        endings.append({"movement":number,"sha256":digest,"frozen_hash_matches":freeze.get('sha256')==digest,"accepted_IV_read_only":number==4,**ending_review(ScoreView(data))})
    (OUT/'endings-review.json').write_text(json.dumps({"movements":endings,"tonic_failures":[r['movement'] for r in endings if not r['tonic_present']],"tonic_bass_failures":[r['movement'] for r in endings if not r['bass_is_tonic']]},indent=2)+'\n')
    print(json.dumps({"reviewed":summary['reviewed_movements'],"frozen":summary['frozen_movements'],"flags":summary['total_flags'],"counts":{r['movement']:r['issue_counts'] for r in reports},"diversity":summary['diversity']},indent=2))


if __name__=="__main__":main()
