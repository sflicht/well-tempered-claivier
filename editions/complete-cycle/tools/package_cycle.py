#!/usr/bin/env python3
"""Assemble the second working edition from final canonical event scores.

This is an editor/exporter, not a composer. The 48 final canonical JSON scores
are authoritative. Historical first-edition generators are retained as sources,
not offered as commands that reproduce the revised edition in one step.
"""
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone
import argparse, csv, hashlib, html, json, os, shutil, subprocess, sys, wave, zipfile
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
if (ROOT/'vendor').is_dir():sys.path.insert(0,str(ROOT/'vendor'))
from audit_music import audit
from render_music import score_duration, bpm_of, meta_of
KEYS=[('C','major'),('C','minor'),('C#','major'),('C#','minor'),('D','major'),('D','minor'),('Eb','major'),('Eb','minor'),('E','major'),('E','minor'),('F','major'),('F','minor'),('F#','major'),('F#','minor'),('G','major'),('G','minor'),('Ab','major'),('G#','minor'),('A','major'),('A','minor'),('Bb','major'),('Bb','minor'),('B','major'),('B','minor')]
ROMANS=['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV','XVI','XVII','XVIII','XIX','XX','XXI','XXII','XXIII','XXIV']
EDITION='Second working edition'
SF=Path('/usr/share/sounds/sf2/FluidR3_GM.sf2')
EPS=1e-7

def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()
def time_label(seconds):
 seconds=round(seconds)
 return f'{seconds//3600}:{seconds//60%60:02d}:{seconds%60:02d}' if seconds>=3600 else f'{seconds//60}:{seconds%60:02d}'
def ascii_text(s):
 return str(s).replace('♯','#').replace('♭','b').replace('—','-').replace('–','-').replace('’',"'").replace('→','to').replace('\u00a0',' ')
def key_slug(n):
 key,mode=KEYS[n-1]
 return key.lower().replace('#','sharp').replace('eb','eflat').replace('ab','aflat').replace('bb','bflat')+'-'+mode
def canonical(n,kind):return ROOT/f'work/cycle_{kind}s/{n:02d}-{kind}.json'
def baseline(n,kind):
 paths=list((ROOT/'baseline/scores').glob(f'{n:02d}-{kind}-*.json'))
 if len(paths)!=1:raise ValueError(f'Ambiguous/missing immutable baseline for {n} {kind}')
 return paths[0]
def atomic_text(path,text):
 path=Path(path);temp=path.with_name(path.name+'.writing');temp.write_text(text)
 with temp.open('rb') as f:os.fsync(f.fileno())
 temp.replace(path)
def atomic_json(path,data):atomic_text(path,json.dumps(data,indent=2)+'\n')

def musical_metrics(data):
 """Written-time measurements; rests count as zero, synth tails are excluded."""
 duration=float(score_duration(data));bpm=bpm_of(meta_of(data));voices=data['voices'];changes=defaultdict(list)
 notes=[e for v in voices for e in v['events'] if e.get('p') is not None]
 for vi,v in enumerate(voices):
  for e in v['events']:
   if e.get('p') is not None:
    changes[float(e['t'])].append((vi,1));changes[float(e['t'])+float(e['d'])].append((vi,-1))
 changes[0.0];changes[duration];active=[0]*len(voices);weighted=0;full=0;maximum=0;runs=[]
 times=sorted(changes)
 for i,t in enumerate(times[:-1]):
  for vi,delta in changes[t]:active[vi]+=delta
  end=times[i+1];n=sum(x>0 for x in active);span=end-t
  weighted+=span*n;maximum=max(maximum,n)
  if n==len(voices):
   full+=span
   if runs and abs(runs[-1]['end']-t)<EPS:runs[-1]['end']=end
   else:runs.append({'start':t,'end':end})
 upper=sorted((e for e in voices[0]['events'] if e.get('p') is not None),key=lambda e:e['t'])
 record=data.get('composition_record',{});rhythm=record.get('second_edition_rhythmic_revision',{})
 second=data.get('second_edition',{})
 return {'notes':len(notes),'voices':len(voices),'quarter_beats':duration,'bpm':bpm,'musical_seconds':duration*60/bpm,
  'offbeat_attacks':sum(abs(float(e['t'])-round(float(e['t'])))>EPS for e in notes),
  'upper_leaps_over_octave':sum(abs(a['p']-b['p'])>12 for a,b in zip(upper,upper[1:])),
  'mean_sounding_parts':weighted/duration if duration else 0,'maximum_sounding_parts':maximum,
  'full_texture_beats':full,'full_texture_seconds':full*60/bpm,'full_texture_runs':runs,
  'new_prepared_suspensions':len(second.get('suspensions',[]))+sum(e.get('kind')=='prepared suspension' for e in rhythm.get('edits',[])),
  'free_passing_connections':sum(e.get('kind')=='free passing connection' for e in rhythm.get('edits',[])),
  'melodic_joint_repairs':len(record.get('melodic_joint_revision',[])),
  'rhythmic_revision_counts':rhythm.get('counts',{}),'remaining_context_flags':rhythm.get('remaining_context_flags',[]),
  'performance_shaped':bool(record.get('performance_revision'))}

def inspect(out):
 rows=[]
 for n in range(1,25):
  row={'number':n,'roman':ROMANS[n-1],'key':' '.join(KEYS[n-1]),'fugue_voices':n+1}
  for kind in ['prelude','fugue']:
   path=canonical(n,kind);oldpath=baseline(n,kind);data=json.loads(path.read_text());old=json.loads(oldpath.read_text())
   if 'second' not in str(data.get('metadata',{}).get('edition','')).lower():raise ValueError(f'{path}: second edition is not finalized')
   info=musical_metrics(data);before=musical_metrics(old)
   if not info['performance_shaped']:raise ValueError(f'{path}: final performance shaping missing')
   info.update({'source':str(path.relative_to(ROOT)),'sha256':sha(path),'baseline_source':str(oldpath.relative_to(ROOT)),'baseline_sha256':sha(oldpath),'baseline':before,
    'title':data['metadata']['subtitle'],'character':data['metadata'].get('character','Invocation and current' if kind=='prelude' and n==4 else ''),
    'sections':data.get('sections',data['metadata'].get('sections',[]))})
   if kind=='fugue':
    a=audit(data,max_examples=50);a['source_sha256']=sha(path)
    atomic_json(out/'audits'/f'{n:02d}-fugue-audit.json',a);info['audit_summary']=a['summary']
    main=[e for e in data.get('subject_entries',[]) if not any(k in (e.get('subject_id','')+' '+e.get('label','')).lower() for k in ['counter','fragment'])]
    info['main_subject_statements']=len(main);info['voices_with_main_subject']=len({e['voice'] for e in main})
    info['main_theme_templates_unchanged']=all(old['subjects'].get(k)==v for k,v in data.get('subjects',{}).items() if 'counter' not in k.lower() and 'fragment' not in k.lower())
    if len(data['voices'])!=n+1 or info['voices_with_main_subject']!=n+1:raise ValueError(f'Fugue {n}: expected {n+1} parts each with a full main subject')
    if a['summary']['data_errors'] or a['summary']['matched_subject_entries']!=a['summary']['documented_subject_entries']:raise ValueError(f'Fugue {n}: invalid events or thematic annotations')
    for field in ['parallel_perfect_interval_candidates_at_shared_attacks','structural_grid_parallel_candidates','outer_similar_motion_into_perfect_with_upper_leap_candidates','exact_octave_duplicate_pairs']:
     if a['summary'].get(field,0):raise ValueError(f'Fugue {n}: unresolved {field}')
    if info['remaining_context_flags']:raise ValueError(f'Fugue {n}: unresolved contextual revision flags')
   row[kind]=info
  rows.append(row)
 totals={}
 for label,use_before in [('baseline',True),('revised',False)]:
  all_info=[r[k]['baseline'] if use_before else r[k] for r in rows for k in ['prelude','fugue']]
  fugues=[r['fugue']['baseline'] if use_before else r['fugue'] for r in rows]
  preludes=[r['prelude']['baseline'] if use_before else r['prelude'] for r in rows]
  totals[label]={'total_notes':sum(x['notes'] for x in all_info),'musical_seconds':sum(x['musical_seconds'] for x in all_info),
   'fugue_notes':sum(x['notes'] for x in fugues),'prelude_notes':sum(x['notes'] for x in preludes),
   'fugue_offbeat_attacks':sum(x['offbeat_attacks'] for x in fugues),'prelude_upper_leaps_over_octave':sum(x['upper_leaps_over_octave'] for x in preludes),
   'new_fugue_prepared_suspensions':sum(x['new_prepared_suspensions'] for x in fugues),'new_prelude_prepared_suspensions':sum(x['new_prepared_suspensions'] for x in preludes),
   'fugue_full_texture_seconds':sum(x['full_texture_seconds'] for x in fugues)}
 manifest={'edition':EDITION,'date':datetime.now(timezone.utc).date().isoformat(),'movements':rows,'comparison':totals,
  'total_musical_seconds':totals['revised']['musical_seconds'],'total_notes':totals['revised']['total_notes'],
  'soundfont':{'file':str(SF),'sha256':sha(SF) if SF.exists() else None},
  'metric_definitions':{'offbeat_attacks':'Note onsets at noninteger quarter-beat positions, counted across parts.','full_texture':'Written time when every notated part contains a sounding note, including holds; tails excluded.','mean_sounding_parts':'Time-weighted sounding part count over the entire written duration, including rests.','upper_leaps_over_octave':'Consecutive upper-part pitches more than 12 semitones apart, including joins separated by rests.','new_prepared_suspensions':'Explicit added suspension records in the revision annotations; not a count of every dissonance in the music.'},
  'scope':'Original symbolic compositions and synthesized studies. A critical score and engineering review, not a human auditory assessment, Bach-equivalence claim, or proof of every historical contrapuntal convention.'}
 atomic_json(out/'cycle-manifest.json',manifest);return manifest

def copy_sources(out,manifest):
 score_dir=out/'editable-scores';score_dir.mkdir(exist_ok=True);audio_dir=out/'individual-audio';audio_dir.mkdir(exist_ok=True)
 for row in manifest['movements']:
  n=row['number']
  for kind in ['prelude','fugue']:
   stem=f'{n:02d}-{kind}-{key_slug(n)}';shutil.copy2(canonical(n,kind),score_dir/(stem+'.json'));prefix=ROOT/f'work/cycle_render/{n:02d}-{kind}'
   for ext in ['musicxml','mid','ly','pdf']:shutil.copy2(prefix.with_suffix('.'+ext),score_dir/(stem+'.'+ext))
   shutil.copy2(prefix.with_suffix('.mp3'),audio_dir/(stem+'.mp3'))

def revision_lines(manifest):
 b=manifest['comparison']['baseline'];r=manifest['comparison']['revised'];iv=manifest['movements'][3]['fugue'];xx=manifest['movements'][-1]['fugue']
 return [
 ('A phrase must go somewhere','The melodic preludes replace root-based broken-triad resets with continuous cantabile lines. Register choices now join gestures; leading-note arrivals, bass approaches and cadential inner parts have been revised.'),
 ('Variation follows the ground','XII, XIV and XXII change their rhythmic treatment at complete ground returns. Their statements now progress through long notes, replies, subdivisions and release, while retaining each prelude\'s meter, tempo and length.'),
 ('Themes need different rhythmic identities',f"Recurring subject or countersubject variants introduce unequal values, passing figures and delayed resolutions where the texture admits them. There are {r['new_fugue_prepared_suspensions']} explicitly added prepared fugue suspensions and {r['new_prelude_prepared_suspensions']} in the preludes."),
 ('The episode must grow from the theme','I, II, III, V, VI and VII receive formal revisions: subject-head sequences, genuinely changed relative-key modes, continued earlier voices and more consequential returns. A fragment is labeled as a fragment and is excluded from full-subject coverage.'),
 ('Repair the five-part test',f"IV retains its main subject. Its supporting lines have {iv['melodic_joint_repairs']} documented pitch repairs, {iv['free_passing_connections']} added passing connections and {iv['new_prepared_suspensions']} new prepared suspensions. The revision changes the music as well as its rendering."),
 ('Make the large ensemble earn its entrance',f"VIII-XXIV continue earlier choirs and develop the full ensemble more extensively. XXIV's time-weighted mean sounding texture rises from {xx['baseline']['mean_sounding_parts']:.2f} to {xx['mean_sounding_parts']:.2f} parts; its all-part duration rises from {xx['baseline']['full_texture_seconds']:.1f} to {xx['full_texture_seconds']:.1f} seconds.")]

def make_guide(out,manifest):
 from reportlab.pdfgen import canvas
 from reportlab.lib.colors import HexColor
 from reportlab.lib.pagesizes import A4
 from reportlab.pdfbase.pdfmetrics import stringWidth,registerFont
 from reportlab.pdfbase.ttfonts import TTFont
 fonts=Path('/usr/share/fonts/truetype/dejavu')
 for name,file in [('GuideSans','DejaVuSans.ttf'),('GuideSansBold','DejaVuSans-Bold.ttf'),('GuideSerifBold','DejaVuSerif-Bold.ttf')]:registerFont(TTFont(name,str(fonts/file)))
 path=out/'well-tempered-clAIvier-cycle-guide.pdf';temporary=path.with_name(path.stem+'-building.pdf');c=canvas.Canvas(str(temporary),pagesize=A4);w,h=A4;page=0
 c.setTitle('The Well-Tempered clAIvier - Second working edition');c.setAuthor('Composed with ChatGPT for Sam')
 date=datetime.fromisoformat(manifest['date']).strftime('%d %B %Y')
 def begin(kicker,title):
  nonlocal page
  if page:c.showPage()
  page+=1;c.setFillColor(HexColor('#f6f2ea'));c.rect(0,0,w,h,fill=1,stroke=0);c.setFillColor(HexColor('#a64f36'));c.setFont('GuideSansBold',9);c.drawString(42,h-42,ascii_text(kicker.upper()))
  c.setFillColor(HexColor('#24333a'));size=min(24,24*(w-84)/stringWidth(ascii_text(title),'GuideSerifBold',24));c.setFont('GuideSerifBold',size);c.drawString(42,h-79,ascii_text(title));c.setStrokeColor(HexColor('#d8d1c5'));c.line(42,h-95,w-42,h-95)
  c.setFont('GuideSans',7.5);c.setFillColor(HexColor('#697174'));c.drawString(42,25,f'The Well-Tempered clAIvier | Second working edition | {date}');c.drawRightString(w-42,25,str(page));return h-120
 def paragraph(text,y,size=9.5,leading=14,bold=False,gap=9):
  font='GuideSansBold' if bold else 'GuideSans';c.setFont(font,size);c.setFillColor(HexColor('#263238'));lines=[];line=''
  for word in ascii_text(text).split():
   proposed=(line+' '+word).strip()
   if stringWidth(proposed,font,size)>w-84 and line:lines.append(line);line=word
   else:line=proposed
  if line:lines.append(line)
  if y-len(lines)*leading<47:raise ValueError(f'Guide page {page} overflows: {text[:70]}')
  for line in lines:c.drawString(42,y,line);y-=leading
  return y-gap
 def fit(text,width,font='GuideSans',size=9):
  text=ascii_text(text)
  while stringWidth(text,font,size)>width and text:text=text[:-1]
  return text
 def heading(text,y):return paragraph(text,y,10.6,15,True,4)
 b=manifest['comparison']['baseline'];r=manifest['comparison']['revised'];xx=manifest['movements'][-1]['fugue']
 y=begin('24 keys / 2 to 25 parts / Second edition','The Well-Tempered clAIvier')
 y=paragraph('24 preludes and 24 fugues. Original compositions for Sam, made with ChatGPT. Fugue N has N+1 separately written parts: from a two-part conversation to an ensemble of twenty-five.',y,12.5,19,gap=16)
 y=paragraph(f"This revised cycle contains {manifest['total_notes']:,} note events and {time_label(manifest['total_musical_seconds'])} of written music. The original edition remains available as an immutable score baseline. Recording release tails add to these written durations.",y,10.5,16)
 y=heading('The question behind this revision',y)
 y=paragraph('What would J. S. Bach ask of a line: where does it come from, where is it going, and why does it enter now? This pass treats that as an editorial test. It revises melodic continuity, thematic rhythm, harmonic arrivals, the purpose of episodes and the relationship between the choirs.',y)
 y=heading('Begin with the comparison',y)
 y=paragraph('The revision audition places four passages from the first and second editions next to each other: Prelude VI, Fugue I, Fugue IV and the first 25-part tutti in XXIV. Both use the same FluidR3 piano and one common gain per pair. Phrasing, articulation and balance are included in the revision. A final excerpt identifies new XXIV development as new material.',y)
 y=heading('Then follow the complete sequence',y)
 for text in ['The continuous piano recording follows Prelude I, Fugue I, Prelude II, Fugue II, and so on. The individual-recordings archive lets you choose a movement.',
  'The animated performances follow the canonical notes. Voice colors remain fixed; theme outlines distinguish complete subjects, countersubjects and fragments. The preludes instead teach their own motives, harmonies and formal changes.',
  'The guided fugue lessons isolate and recombine thematic material. The five-part IV is the first extended test; XXIV also has an orchestral study and a 25-player spatial rehearsal.']:y=paragraph(text,y)
 y=heading('What this edition is',y)
 y=paragraph('It is a revised composition and a reproducible study package. The audio is synthesized. The work has had score-based and technical review; no human auditory evaluation or claim of equality to Bach is represented. Numerical improvements document changes, not musical beauty.',y)
 for start in [0,12]:
  y=begin('Cycle index',f'Pairs {ROMANS[start]} to {ROMANS[start+11]}');c.setFont('GuideSansBold',8.5);c.setFillColor(HexColor('#6b5a4c'))
  for x,label in [(42,'PAIR / KEY'),(177,'CHARACTER'),(409,'PARTS / ALL IN'),(507,'TIME')]:c.drawString(x,y,label)
  y-=23
  for row in manifest['movements'][start:start+12]:
   n=row['number'];dur=row['prelude']['musical_seconds']+row['fugue']['musical_seconds'];c.setFont('GuideSansBold',10);c.setFillColor(HexColor('#263238'));c.drawString(42,y,row['roman']+'  '+row['key'])
   c.setFont('GuideSans',9);c.drawString(177,y,fit('P: '+row['prelude']['character'],220));c.drawString(409,y,f'{n+1} parts');c.drawRightString(w-42,y,time_label(dur));y-=15
   c.setFont('GuideSans',8.5);c.setFillColor(HexColor('#697174'));c.drawString(177,y,fit('F: '+(row['fugue']['character'] or row['fugue']['title']),220,size=8.5));c.drawString(409,y,f"{row['fugue']['full_texture_seconds']:.1f} s together");y-=28;c.setStrokeColor(HexColor('#dfd8cf'));c.line(42,y+10,w-42,y+10)
  y-=7;y=paragraph('P = prelude; F = fugue. Time is the pair\'s written music, excluding release tails. "Together" is the measured sum of spans with a written note sounding in every fugue part. Sustained notes count; it does not mean every part attacks at once or stays equally perceptible.',y,9,13)
 y=begin('Critical revision / before and after','What changed, and why')
 c.setFont('GuideSansBold',9);c.setFillColor(HexColor('#6b5a4c'));c.drawString(42,y,'WRITTEN SCORE MEASURE');c.drawRightString(432,y,'FIRST');c.drawRightString(w-42,y,'SECOND');y-=20
 measures=[('All note events',f"{b['total_notes']:,}",f"{r['total_notes']:,}"),('Fugue onsets between quarter beats',f"{b['fugue_offbeat_attacks']:,}",f"{r['fugue_offbeat_attacks']:,}"),('Prelude upper-part leaps over an octave',str(b['prelude_upper_leaps_over_octave']),str(r['prelude_upper_leaps_over_octave'])),('XXIV: average sounding parts',f"{xx['baseline']['mean_sounding_parts']:.2f}",f"{xx['mean_sounding_parts']:.2f}"),('XXIV: seconds with all 25 sounding',f"{xx['baseline']['full_texture_seconds']:.1f}",f"{xx['full_texture_seconds']:.1f}")]
 for label,old,new in measures:
  c.setFont('GuideSans',9);c.setFillColor(HexColor('#263238'));c.drawString(42,y,label);c.drawRightString(432,y,old);c.drawRightString(w-42,y,new);y-=19
 y-=9
 for title,text in revision_lines(manifest):y=heading(title,y);y=paragraph(text,y,9.2,13,gap=7)
 y=begin('Evidence, performance and limits','How to judge this edition')
 for title,text in [
  ('Parts and thematic identity','Each fugue has exactly N+1 monophonic written streams. Every part has a documented full subject or answer. The audit matches annotated statements to actual pitches, onsets and durations; countersubjects and fragment labels are excluded from main-subject coverage. Exact duplicate whole parts are screened.'),
  ('Counterpoint in context','The checks examine shared-attack and structural-grid perfect-interval parallels, outer similar motion into a perfect interval with an upper leap, overlap within a part, and context around added passing notes and suspensions. Preparation, continuation and resolution matter. A zero candidate count is specific evidence, not a certificate of every historical rule.'),
  ('The preludes have their own grammar','Their review follows phrasing, register, harmonic arrivals, the actual flanking notes of scalar decoration, and the timing of whole ground statements. Free preludes are not presented as strict-species exercises. Their original meter, tempo and written length are retained.'),
  ('Performance follows musical function','FluidR3 General MIDI piano samples replace the earlier small soundfont. Deterministic velocity shaping differentiates themes and accompaniment, arches phrases and marks meter; explicit articulation connects suspensions and releases cadences. Keyboard-register stereo aids separation. Written onsets, tempo and durations are preserved; no random timing is added.'),
  ('One source for the exports','Final canonical JSON is authoritative. MusicXML, LilyPond, MIDI, audio and animated cues derive from it. The supplied export checks compare written pitches, onsets and durations; manifests retain source hashes. MIDI gates are performance values, not shortened written notes. Above 15 parts, preserve MIDI ports and track assignments.'),
  ('Remaining musical limits','The harmonic frameworks remain conservative and some episode designs recur. A brief overlap is less demanding than a closely interlocked multi-subject stretto. Twenty-five sounding parts can mask one another, particularly on one piano; the longer full ensemble is still a compositional experiment. Detailed auditory revision and orchestral balancing remain valuable next judgments.'),
  ('Reproduction without losing the revision','The archive contains canonical scores, immutable first-edition baseline JSON, revision reports and source programs. The old compose_iv.py, compose_cycle_* and build_delivery.py describe earlier stages. Start from the final canonical scores to render this edition; rerunning an old composer does not reconstruct the second edition.')]:
  y=heading(title,y);y=paragraph(text,y,9.3,13.5,gap=9)
 y=begin('XXIV / Spatial study and film','Twenty-five players, one score clock')
 y=paragraph(f"The revised XXIV lasts {time_label(xx['musical_seconds'])} of written music. Its mean sounding texture is {xx['mean_sounding_parts']:.2f} parts; all 25 sound for {xx['full_texture_seconds']:.1f} seconds in total. These measurements include sustained notes and the full written span, including rests.",y,10,15)
 for section in xx['sections']:
  if section['label'] in ('Complete ensemble','Gathered development','Final return','Final cadence'):
   start=float(section['t']);end=start+float(section.get('d',section.get('end',start)-start));detail=section.get('detail','')
   if section['label']=='Final cadence':
    end=xx['quarter_beats'];detail+=' This range includes the final written tonic hold.'
   bar=int(start/4)+1;endbar=int((end-EPS)/4)+1
   y=paragraph(f"{section['label']}: bars {bar}-{endbar}, {time_label(start*60/xx['bpm'])}-{time_label(end*60/xx['bpm'])} on the score clock. "+detail,y,9.1,13,gap=7)
 y=heading('The pedagogical and cinematic layers',y)
 for text in [
  'The spatial rehearsal assigns a permanent player ID and location to each of the 25 parts. Entries and changes in sounding texture follow the exact score clock. Subject portraits, returning viewpoints and wider shots can teach how individual lines join the ensemble.',
  'The proposed digital setting is inspired by the Sagrada Familia: branching columns, colored side light and distributed groups. The floor plan is an exact-count conceptual layout. It is not a surveyed building plan, a recording made in the venue, or a measured room-acoustic model.',
  'The orchestral study retains the written concert pitches and timing. Sampled timbres and artistic reverberation explore separation; they do not establish idiomatic instrumental technique or a final spatial mix. Illustrative player motions are not validated fingering instruction.',
  'No Slopcannon render has been completed. The present film material is a score-synchronized rehearsal and a cinematic production concept. A generated location film remains a separate production stage.']:y=paragraph(text,y,9.3,13.5,gap=8)
 y=heading('Reference links for the production concept',y)
 for label,url in [('Sagrada Familia: stone-forest columns','https://blog.sagradafamilia.org/en/columns-sagrada-familia-geometry-mechanics-materials-stone-forest/'),('Sagrada Familia: stained-glass light','https://blog.sagradafamilia.org/en/stained-glass-light-colour-creation/'),('Sagrada Familia: choirs and music','https://blog.sagradafamilia.org/en/music-sagrada-familia-choirs/'),('Slopcannon for agents','https://slop.cc/for-agents')]:
  if y<48:raise ValueError('Guide references overflow')
  c.setFillColor(HexColor('#a64f36'));c.setFont('GuideSans',8.5);c.drawString(42,y,label);c.linkURL(url,(42,y-2,w-42,y+10),relative=0);y-=18
 c.save()
 with temporary.open('rb') as f:os.fsync(f.fileno())
 temporary.replace(path);return path

def join_audio(out,manifest):
 # Encode once from complete PCM masters. Concatenating compressed MP3 files
 # can retain padding/header artefacts and must not hide an interrupted export.
 sequence=out/'audio-sequence.txt';files=[];masters=[];rows=[];cursor=0
 for movement in manifest['movements']:
  n=movement['number']
  for kind in ['prelude','fugue']:
   p=out/'individual-audio'/f'{n:02d}-{kind}-{key_slug(n)}.mp3'
   wav=ROOT/f'work/cycle_render/{n:02d}-{kind}.wav'
   with wave.open(str(wav)) as f:
    if (f.getframerate(),f.getnchannels(),f.getsampwidth())!=(44100,2,2):raise ValueError(f'Incompatible PCM master: {wav}')
    frames=f.getnframes();duration=frames/f.getframerate()
   mp3_seconds=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(p)],text=True))
   if abs(mp3_seconds-duration)>.1:raise ValueError(f'Incomplete individual MP3: {p}; {mp3_seconds} vs PCM {duration}')
   decoded=subprocess.run(['ffmpeg','-hide_banner','-v','error','-i',str(p),'-map','0:a:0','-f','null','-'],capture_output=True,text=True)
   if decoded.returncode or decoded.stderr.strip():raise ValueError('Individual MP3 decode failed: '+str(p)+' '+decoded.stderr[-1000:])
   rows.append({'track':len(rows)+1,'pair':n,'movement':kind,'key':' '.join(KEYS[n-1]),'start_seconds':round(cursor,6),'duration_seconds':round(duration,6),'filename':p.name,'source_sha256':sha(canonical(n,kind)),'pcm_sha256':sha(wav),'mp3_sha256':sha(p),'pcm_frames':frames,'encoded_seconds':mp3_seconds,'full_decode_passed':True})
   cursor+=duration;files.append(p);masters.append(wav)
 sequence.write_text('\n'.join("file '"+str(p).replace("'","'\\''")+"'" for p in masters)+'\n');target=out/'well-tempered-clAIvier-complete-piano-cycle.mp3';temporary=out/'complete-piano-cycle-building.mp3'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(sequence),'-codec:a','libmp3lame','-b:a','192k','-metadata','title=The Well-Tempered clAIvier - Second Edition Complete Piano Cycle','-metadata','artist=Composed with ChatGPT for Sam',str(temporary)],check=True)
 with temporary.open('rb') as f:os.fsync(f.fileno())
 with (out/'listening-index.csv').open('w',newline='') as f:
  fields=['track','pair','movement','key','start_seconds','duration_seconds','filename']
  writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');writer.writeheader();writer.writerows(rows)
 actual=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','default=noprint_wrappers=1:nokey=1',str(temporary)],text=True))
 if abs(actual-cursor)>.1:raise ValueError(f'Joined audio duration {actual} differs from PCM total {cursor}')
 decoded=subprocess.run(['ffmpeg','-hide_banner','-v','error','-i',str(temporary),'-map','0:a:0','-f','null','-'],capture_output=True,text=True)
 if decoded.returncode or decoded.stderr.strip():raise ValueError('Complete MP3 decode failed: '+decoded.stderr[-1000:])
 temporary.replace(target)
 atomic_text(out/'piano-cycle-verification.json',json.dumps({'movements':48,'pcm_duration_seconds':cursor,'encoded_duration_seconds':actual,'encoding':'One 192 kbps MP3 encode from 48 complete 44.1 kHz stereo PCM masters','all_individual_full_decodes_passed':True,'master_full_decode_passed':True,'sha256':sha(target),'sources':rows},indent=2)+'\n')
 return target

def join_score(out,guide):
 from pypdf import PdfWriter
 writer=PdfWriter();writer.append(str(guide),outline_item='Second edition: listening and study guide')
 for n in range(1,25):
  for kind in ['prelude','fugue']:writer.append(str(out/'editable-scores'/f'{n:02d}-{kind}-{key_slug(n)}.pdf'),outline_item=f'{ROMANS[n-1]}. {kind.title()} in '+' '.join(KEYS[n-1]))
 writer.add_metadata({'/Title':'The Well-Tempered clAIvier - Second Edition Complete Study Score','/Author':'Composed with ChatGPT for Sam'});target=out/'well-tempered-clAIvier-complete-study-score.pdf';temporary=target.with_name(target.stem+'-building.pdf')
 with temporary.open('wb') as f:writer.write(f);f.flush();os.fsync(f.fileno())
 temporary.replace(target);return target

def archive(path,items):
 path=Path(path);temporary=path.with_name(path.stem+'-building.zip');seen=set()
 with zipfile.ZipFile(temporary,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for source,arc in items:
   source=Path(source);files=[(p,str(Path(arc)/p.relative_to(source))) for p in sorted(source.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'] if source.is_dir() else [(source,str(arc))]
   for p,name in files:
    if name in seen:continue
    if not p.exists():raise FileNotFoundError(p)
    z.write(p,name);seen.add(name)
 with temporary.open('rb') as f:os.fsync(f.fileno())
 with zipfile.ZipFile(temporary) as z:
  if z.testzip() is not None:raise ValueError('Archive integrity failure: '+str(temporary))
 temporary.replace(path)

def readme(out,manifest):
 b=manifest['comparison']['baseline'];r=manifest['comparison']['revised'];xx=manifest['movements'][-1]['fugue'];changes='\n\n'.join(title.upper()+'\n'+text for title,text in revision_lines(manifest))
 text=f'''THE WELL-TEMPERED clAIvier
{EDITION} - {manifest['date']}
Original compositions for Sam, made with ChatGPT.

48 movements; 24 major/minor keys; fugues with 2 through 25 written parts.
Written music: {time_label(manifest['total_musical_seconds'])}; note events: {manifest['total_notes']:,}.
The first-edition baseline is retained unchanged under baseline/scores.

BEGIN WITH THE REVISION AUDITION
The comparison MP4/MP3 juxtaposes Prelude VI, Fugue I, Fugue IV and the first
25-part tutti of XXIV. The same FluidR3 piano and one common gain per pair
are used; revised velocity, articulation and balance are part of the change.
The appended new-development excerpt is explicitly second-edition-only.
This is an audition for the listener, not a claim of human auditory review.

LISTEN AND WATCH
The complete piano MP3 follows Prelude I, Fugue I, Prelude II, Fugue II,
and so on. Individual recordings use the same order. Release tails add to
written musical duration. Animated performances use canonical note data;
voice IDs remain fixed and annotated themes/fragments retain their identity.
Guided fugue lessons isolate and recombine the musical material. XXIV has
an orchestral study and a score-bound spatial rehearsal for 25 players.

WHAT CHANGED
{changes}

MEASURED BEFORE / AFTER
Total note events: {b['total_notes']:,} / {r['total_notes']:,}.
Fugue onsets between quarter beats: {b['fugue_offbeat_attacks']:,} / {r['fugue_offbeat_attacks']:,}.
Prelude upper-part leaps over an octave: {b['prelude_upper_leaps_over_octave']} / {r['prelude_upper_leaps_over_octave']}.
XXIV mean sounding parts: {xx['baseline']['mean_sounding_parts']:.2f} / {xx['mean_sounding_parts']:.2f}.
XXIV all-25 sounding seconds: {xx['baseline']['full_texture_seconds']:.1f} / {xx['full_texture_seconds']:.1f}.
Metrics describe written events, not artistic quality. Mean density includes
rests; full texture includes held notes. These definitions and exact source
hashes are recorded in cycle-manifest.json.

PERFORMANCE AND EDITING
The final canonical JSON scores are authoritative. Each movement also has
concert-pitch MusicXML, LilyPond, MIDI and an open study-score PDF. Performance
gates and velocities shape articulation, phrase and thematic balance while
preserving written note onsets and durations. Explicit suspension gates stay
connected. No random onset displacement or tempo fluctuation is added.
The soundfont is FluidR3_GM.sf2, a General MIDI study instrument.
Large scores use A3/A2 pages. Zoom to read; physical piano playability is not
required. MIDI uses a second port above 15 parts; retain tracks and ports.

CHECKS AND LIMITS
Every fugue has N+1 monophonic streams, each with an exact main-subject or
answer statement. Countersubjects and fragments do not satisfy that coverage.
Current canonical audits check event integrity, thematic matches, specified
perfect-interval motions and exact whole-part duplicates. Added dissonances
are reviewed in their preparation, flanking motion and resolution. Export
checks compare the written pitches, onsets and durations across formats.
Free preludes follow their own textures and harmonic plans; they are not
strict-species exercises. The framework remains harmonically conservative;
some episodic patterns recur, and dense piano textures can mask individual
lines. These checks do not prove Bach-level quality or every historical rule.
The review is symbolic and technical. Human auditory judgment and further
orchestral balancing have not been represented as completed.

REPRODUCE THIS EDITION
Use final canonical JSON in work/cycle_preludes and work/cycle_fugues, also
provided as named JSON in scores/. Run render_music.py --help and
animate_cycle.py --help for rendering. The archive includes the immutable
baseline JSON because revision helpers depend on it, plus revision reports
and source helper programs. Historical compose_iv.py, compose_cycle_* and
build_delivery.py implement earlier stages; running them alone does not
recreate the second edition. Intermediate revision reports are labeled by
stage; audits/NN-fugue-audit.json and cycle-manifest.json refer to delivery.
Dependencies: Python 3.12, mido, numpy, scipy, pyfluidsynth, ortools, Pillow,
reportlab, pypdf; external LilyPond, FFmpeg and Poppler. The soundfont and
optional vendor directory are not redistributed. Default soundfont path:
/usr/share/sounds/sf2/FluidR3_GM.sf2

SPATIAL FILM STATUS
The Sagrada Familia-inspired environment is a conceptual layout, not a
surveyed building, venue filming or a measured acoustic response. The exact
25-player floor plan, score-bound rehearsal and cinematic concept are the
current deliverables. Illustrative motions are not fingering instruction.
No Slopcannon render has been completed. A final generated location film
remains a separate production stage.
'''
 atomic_text(out/'README.txt',ascii_text(text))
 rows=[]
 for row in manifest['movements']:
  n=row['number'];cells=[]
  for kind in ['prelude','fugue']:
   fn=f'{n:02d}-{kind}-{key_slug(n)}.mp3';cells.append(f'<a href="{html.escape(fn)}">{kind.title()}</a> ({time_label(row[kind]["musical_seconds"])})')
  rows.append(f'<tr><th>{row["roman"]}</th><td>{row["key"]}</td><td>{cells[0]}</td><td>{cells[1]}</td><td>{n+1}</td></tr>')
 atomic_text(out/'individual-audio'/'index.html','<!doctype html><html lang="en"><meta charset="utf-8"><title>The Well-Tempered clAIvier - Second Edition</title><style>body{max-width:1000px;margin:50px auto;padding:0 20px;background:#f6f2ea;color:#24333a;font:17px Georgia}table{border-collapse:collapse;width:100%}td,th{padding:12px;border-bottom:1px solid #d8d1c5;text-align:left}a{color:#a64f36}h1{font-size:38px}p{line-height:1.5}</style><h1>The Well-Tempered clAIvier</h1><p>Second working edition. Open a movement to listen. These are synthesized FluidR3 piano studies. Durations below are written music; recording tails are additional.</p><table><tr><th>Pair</th><th>Key</th><th>Prelude</th><th>Fugue</th><th>Fugue parts</th></tr>'+''.join(rows)+'</table></html>')

def refresh_archives(out,guide):
 archive(out/'well-tempered-clAIvier-individual-recordings.zip',[(out/'individual-audio','recordings'),(out/'README.txt','README.txt'),(out/'listening-index.csv','listening-index.csv'),(guide,guide.name)])
 items=[(out/'editable-scores','scores'),(out/'audits','audits'),(out/'cycle-manifest.json','cycle-manifest.json'),(out/'README.txt','README.txt'),(guide,guide.name)]
 # Code only: no third-party Bach engravings, cached assets or binaries.
 for p in sorted((ROOT/'tools').rglob('*.py')):
  if '__pycache__' not in p.parts:items.append((p,str(p.relative_to(ROOT))))
 for p in sorted((ROOT/'baseline/scores').glob('*.json')):items.append((p,str(p.relative_to(ROOT))))
 for n in range(1,25):
  for kind in ['prelude','fugue']:
   p=canonical(n,kind);items.append((p,str(p.relative_to(ROOT))))
 # Keep editorial evidence while excluding transient renders and score prototypes.
 revision=ROOT/'work/revision'
 for p in sorted(revision.rglob('*')):
  relative=p.relative_to(revision)
  if not p.is_file() or p.suffix not in ('.json','.txt'):continue
  if any(part in ('comparison','listen','rhythm-prototype','formal-audio','dense-audio') for part in relative.parts):continue
  if p.parent==revision or any(word in p.name.lower() for word in ('review','audit','verification','manifest','report','correction','check')):items.append((p,str(p.relative_to(ROOT))))
 for p in [ROOT/'work/cycle_render/prelude-musicxml-roundtrip.json',ROOT/'work/cycle_render/cycle-export-verification.json',ROOT/'work/animation/all-animation-qc.json',ROOT/'work/animation/annotation-assets-qc.json',ROOT/'work/animation/second-edition-media-qc.json',ROOT/'work/cycle_fugues/freeze_manifest.json',ROOT/'work/final_video_qa/review.json',out/'animated-cycle-verification.json',out/'piano-cycle-verification.json',out/'animation-index.csv',out/'listening-index.csv']:
  if p.exists():items.append((p,'audits/exports/'+p.name))
 archive(out/'well-tempered-clAIvier-complete-source.zip',items)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=ROOT/'output/complete-cycle');ap.add_argument('--skip-audio',action='store_true');ap.add_argument('--archives-only',action='store_true');args=ap.parse_args();out=args.output.resolve();out.mkdir(parents=True,exist_ok=True);(out/'audits').mkdir(exist_ok=True)
 if args.archives_only:refresh_archives(out,out/'well-tempered-clAIvier-cycle-guide.pdf');print('Second-edition archives refreshed and CRC-verified.');return
 manifest=inspect(out);copy_sources(out,manifest);guide=make_guide(out,manifest);readme(out,manifest)
 if not args.skip_audio:join_audio(out,manifest)
 join_score(out,guide);refresh_archives(out,guide)
 print(json.dumps({'edition':EDITION,'output':str(out),'musical_duration':time_label(manifest['total_musical_seconds']),'notes':manifest['total_notes']},indent=2))
if __name__=='__main__':main()
