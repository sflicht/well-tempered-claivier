#!/usr/bin/env python3
"""An honest score-synchronized first/second-edition listening comparison.

Run only after the canonical second edition has been finalized:
    python tools/build_revision_sampler.py --canonical-ready

Without --canonical-ready the script prints its editorial plan and performs no
synthesis or video render. --preview-only renders stills after the same readiness
checks. --xxiv-start can explicitly select the revised all-part passage if its
section name has changed; --bonus-start optionally adds 12 seconds of new XXIV
material without pretending that it has a corresponding first-edition passage.

Both versions use the identical FluidR3 piano, synth settings, and a common gain
within each pair. Written velocities/articulation/pan remain those of each
edition: revised phrasing and balance are part of the change. This is an audition
for the listener, not a record of an independent human auditory assessment.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, math, os, subprocess, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if (ROOT/'vendor').is_dir():sys.path.insert(0,str(ROOT/'vendor'))
import numpy as np
from scipy.io import wavfile
from PIL import Image
import animate_cycle as ac
import render_music as rm

RATE=44100
OUT=ROOT/'output/complete-cycle'
WORK=ROOT/'work/revision/comparison'
SF=Path('/usr/share/sounds/sf2/FluidR3_GM.sf2')
PAIRS=[
 {'number':6,'kind':'prelude','start':0,'end':24,'title':'A melody that continues',
  'work':'Prelude VI in D minor','change':'The upper line is rewritten as a phrase, with scalar passing and neighbor tones.',
  'before':'Broken-triad shapes restart with the harmony. Hear the wide joins between measures.',
  'after':'A shaped upper melody crosses the harmony. Accented passing notes and neighbors resolve by step.'},
 {'number':1,'kind':'fugue','start':8,'end':24,'title':'An episode with a reason',
  'work':'Fugue I in C major','change':'The countersubject gains rhythmic contrast; the episode develops the subject head.',
  'before':'A quarter-note-based companion accompanies the answer; free chord tones form the following episode.',
  'after':'The companion has a different rhythmic profile. The following sequence develops the subject head.'},
 {'number':4,'kind':'fugue','start':144,'end':160,'title':'Mending the inner lines',
  'work':'Fugue IV in C-sharp minor','change':'Exposed melodic joins at quarter-beats 148 and 155 are revised.',
  'before':'Listen to the supporting voices around bars 38 and 39; the subject remains recognizable.',
  'after':'Two exposed melodic joins are repaired, with stepwise connections added to the supporting parts.'},
 {'number':24,'kind':'fugue','start':412,'end':444,'title':'Twenty-five parts together',
  'work':'Fugue XXIV in B minor','change':'The collective passage is recomposed. Follow the individual lines through the shared harmony.',
  'before':'The original eight-bar tutti contains long held or repeated tones in many of its 25 parts.',
  'after':'The revised collective counterpoint gives the lines more activity. Compare their continuity and direction.'},
]

def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()

def baseline_path(pair):
 return next((ROOT/'baseline/scores').glob(f"{pair['number']:02d}-{pair['kind']}-*.json"))

def canonical_path(pair):
 return ROOT/f"work/cycle_{pair['kind']}s/{pair['number']:02d}-{pair['kind']}.json"

def all_part_window(data,start,end):
 points=sorted(set([start,end]+[x for v in data['voices'] for e in v['events'] for x in [e['t'],e['t']+e['d']] if start<x<end]))
 active=[]
 for a,b in zip(points,points[1:]):
  mid=(a+b)/2
  n=sum(any(e.get('p') is not None and e['t']<=mid<e['t']+e['d'] for e in v['events']) for v in data['voices'])
  active.append((b-a,n))
 return {'written_parts':len(data['voices']),'mean_sounding_parts':sum(w*n for w,n in active)/(end-start),'peak_sounding_parts':max(n for _,n in active),'all_part_beats':sum(w for w,n in active if n==len(data['voices']))}

def revised_xxiv_start(data,explicit=None):
 if explicit is not None:return float(explicit)
 sections=data.get('sections',data.get('metadata',{}).get('sections',[]))
 candidates=[]
 for s in sections:
  label=s.get('label','').lower()
  if any(word in label for word in ['complete ensemble','complete-ensemble','all-part','all 25','tutti']):
   start=float(s['t']);length=float(s.get('d',s.get('end',start)-start))
   if length>=32 and all_part_window(data,start,start+32)['peak_sounding_parts']==25:candidates.append(start)
 if not candidates:raise ValueError('No unambiguous 32-beat revised XXIV all-part section. Pass its exact start using --xxiv-start.')
 return min(candidates)

def excerpt_manifest(path,start,end,edition,pair_index,pair):
 data=ac.load_score(path);score=ac.Score(data)
 if not 0<=start<end<=score.end:raise ValueError((path,start,end,score.end))
 return {'kind':'music','edition':edition,'pair_index':pair_index,'work':pair['work'],'change':pair['change'],
         'caption':pair['before'] if edition=='FIRST EDITION' else pair['after'],
         'path':str(path),'sha256':sha(path),'start_beat':start,'end_beat':end,
         'bpm':score.bpm,'meter':score.meta.get('meter',[4,4]),
         'first_bar':int(math.floor(start/score.bar))+1,'last_bar':int(math.ceil(end/score.bar)),
         'music_seconds':(end-start)*score.spb,'tail_seconds':1.0,
         'duration':(end-start)*score.spb+1.0,'density':all_part_window(data,start,end)}

def build_plan(args):
 items=[{'kind':'card','duration':8.0,'title':'A second hearing','eyebrow':'THE WELL-TEMPERED clAIvier · REVISION AUDITION',
  'text':'Four passages, first edition followed by second.\n\nBoth use the same piano samples and rendering settings. Revised phrasing, articulation and balance are part of the change.',
  'footer':'A comparison for listening · original scores remain available'}]
 sources={}
 for ix,pair in enumerate(PAIRS):
  first=baseline_path(pair);second=canonical_path(pair)
  old=ac.load_score(first);new=ac.load_score(second)
  if 'second' not in str(new.get('metadata',{}).get('edition','')).lower():raise RuntimeError(f'Second edition not finalized: {second}')
  if sha(first)==sha(second):raise RuntimeError(f'Unchanged source supplied as revised: {second}')
  start=pair['start'];end=pair['end'];revised_start=start
  if pair['number']==24:revised_start=revised_xxiv_start(new,args.xxiv_start)
  items.append({'kind':'card','duration':5.5,'title':pair['title'],'eyebrow':f"PAIR {ix+1} / 4 · {pair['work']}",'text':pair['change'],'footer':'FIRST EDITION, then SECOND EDITION'})
  a=excerpt_manifest(first,start,end,'FIRST EDITION',ix,pair)
  b=excerpt_manifest(second,revised_start,revised_start+end-start,'SECOND EDITION',ix,pair)
  if a['bpm']!=b['bpm'] or a['meter']!=b['meter']:raise ValueError('Paired excerpts must retain the same meter and tempo.')
  items.append(a)
  items.append({'kind':'card','duration':1.8,'title':'Second edition','eyebrow':pair['work'],'text':'Same passage length. Revised notes and phrasing.','footer':'Follow the colored parts.'})
  items.append(b)
  sources[str(first)]=a['sha256'];sources[str(second)]=b['sha256']
 if args.bonus_start is not None:
  pair=PAIRS[-1];path=canonical_path(pair);d=ac.load_score(path);spb=60/float(d['metadata']['bpm']);start=float(args.bonus_start);end=start+12/spb
  items.append({'kind':'card','duration':5.5,'title':'A new collective span','eyebrow':'FUGUE XXIV · SECOND EDITION ONLY','text':'This added passage has no matching first-edition excerpt.','footer':'Twelve seconds from the expanded development.'})
  extra=excerpt_manifest(path,start,end,'SECOND EDITION',4,pair)
  extra['caption']='New material: hear the gathered parts develop together.';extra['unpaired_new_material']=True
  items.append(extra)
 items.append({'kind':'card','duration':7.0,'title':'What would Bach ask of it?','eyebrow':'CONTINUE THE MUSICAL REVIEW',
  'text':'Listen for continuity, tension and release—and whether each part earns its place.\n\nThe full scores and revision report document the changes.',
  'footer':'Synthetic piano study · no claim of a human auditory review'})
 cursor=0
 for s in items:s['timeline_start']=cursor;cursor+=s['duration']
 return items,cursor,sources

def audio_for_excerpt(segment,soundfont):
 data=ac.load_score(segment['path']);start=segment['start_beat'];end=segment['end_beat'];spb=60/float(data['metadata']['bpm'])
 # Include every note already sounding at the excerpt entrance, plus pre-roll
 # for the piano's decay/reverb. Such notes are not reattacked at the cut itself.
 active_starts=[e['t'] for v in data['voices'] for e in v['events'] if e['t']<start<e['t']+e['d']]
 preroll=min([max(0,start-8)]+active_starts)
 key=hashlib.sha256(json.dumps({'source':segment['sha256'],'start':start,'end':end,'preroll':preroll,'renderer':sha(ROOT/'tools/render_music.py'),'soundfont':sha(soundfont)},sort_keys=True).encode()).hexdigest()[:20]
 cache=WORK/'audio';cache.mkdir(parents=True,exist_ok=True);prefix=cache/key
 receipt=prefix.with_suffix('.render.json');wav=prefix.with_suffix('.wav')
 if wav.exists() and receipt.exists():rendered=json.loads(receipt.read_text())
 else:
  excerpt={'metadata':copy.deepcopy(data['metadata']),'voices':[]}
  excerpt['metadata']['source_excerpt']={'file':segment['path'],'sha256':segment['sha256'],'original_start_beat':preroll,'original_end_beat':end}
  for voice in data['voices']:
   vv={k:copy.deepcopy(v) for k,v in voice.items() if k!='events'};vv['events']=[]
   for e in voice['events']:
    a=max(preroll,e['t']);b=min(end,e['t']+e['d'])
    if b>a:vv['events'].append({**e,'t':a-preroll,'d':b-a})
   excerpt['voices'].append(vv)
  prefix.with_suffix('.score.json').write_text(json.dumps(excerpt,indent=2)+'\n')
  rendered=rm.render_audio(excerpt,wav,prefix.with_suffix('.mp3'),soundfont)
  ac.atomic_json(receipt,rendered)
 rate,pcm=wavfile.read(wav)
 if rate!=RATE:raise ValueError('Unexpected sample rate')
 signal=pcm.astype(np.float64)/32767.0
 # render_music peak-normalizes each intermediate. Undo that normalization
 # before applying a single shared gain to the two members of the pair.
 signal*=float(rendered['raw_peak'])/.88
 begin=round((start-preroll)*spb*rate);length=round(segment['duration']*rate)
 audio=np.zeros((length,2),dtype=np.float64);take=min(length,max(0,len(signal)-begin));audio[:take]=signal[begin:begin+take]
 edge=min(round(.012*rate),length//2);audio[:edge]*=np.linspace(0,1,edge)[:,None]
 release=min(round(.25*rate),length//2);audio[-release:]*=np.linspace(1,0,release)[:,None]
 segment['audio_preroll_start_beat']=preroll;segment['audio_cache']=str(wav);segment['raw_excerpt_peak']=float(np.max(np.abs(audio),initial=0))
 return audio

def make_soundtrack(segments,length,soundfont):
 music=[s for s in segments if s['kind']=='music'];signals={}
 for s in music:
  signals[id(s)]=audio_for_excerpt(s,soundfont)
  print(json.dumps({'stage':'audio','work':s['work'],'edition':s['edition']}),flush=True)
 for pair in sorted(set(s['pair_index'] for s in music)):
  members=[s for s in music if s['pair_index']==pair]
  peak=max(float(np.max(np.abs(signals[id(s)]),initial=0)) for s in members)
  gain=.86/max(1e-9,peak)
  for s in members:s['shared_pair_gain']=gain;signals[id(s)]*=gain
 output=np.zeros((math.ceil(length*RATE),2),dtype=np.float32)
 for s in music:
  a=round(s['timeline_start']*RATE);arr=signals[id(s)];take=min(len(arr),len(output)-a);output[a:a+take]=arr[:take]
 path=WORK/'comparison-soundtrack.wav';temporary=path.with_name('comparison-soundtrack-writing.wav')
 wavfile.write(temporary,RATE,np.int16(np.clip(output,-1,1)*32767));ac.publish_file(temporary,path)
 return path,float(np.max(np.abs(output),initial=0))

class ComparisonPainter:
 def __init__(self,segments):
  self.segments=segments;self.starts=[s['timeline_start'] for s in segments];self.painters={}
  for s in segments:
   if s['kind']=='music' and s['path'] not in self.painters:self.painters[s['path']]=ac.Painter(ac.Score(ac.load_score(s['path'])))
 def card(self,s):
  im=Image.new('RGB',(ac.W,ac.H),ac.BG);d=ac.FastDraw(im)
  d.text((54,42),s.get('eyebrow','THE WELL-TEMPERED clAIvier'),font=ac.font(15,True),fill=ac.ACCENT)
  y=ac.textblock(d,(50,145),s['title'],size=49,serif=True,width=1140,max_lines=2,leading=64)
  ac.textblock(d,(55,y+46),s.get('text',''),size=27,width=1110,max_lines=6,leading=39)
  d.line((54,626,1226,626),fill=ac.GRID,width=2)
  ac.textblock(d,(55,651),s.get('footer',''),size=17,fill=ac.MUTED,width=1140,max_lines=2)
  return im
 def frame(self,t):
  import bisect
  ix=min(len(self.segments)-1,max(0,bisect.bisect_right(self.starts,t)-1));s=self.segments[ix]
  if s['kind']=='card':return self.card(s)
  painter=self.painters[s['path']];elapsed=t-s['timeline_start'];ended=elapsed>=s['music_seconds']
  beat=min(s['end_beat']-1e-7,s['start_beat']+elapsed/painter.s.spb)
  label=f"{s['work']} · bars {s['first_bar']}–{s['last_bar']}"
  im=painter.performance(beat,{'title':label,'text':s['caption'],'_excerpt_ended':ended,'window_beats':16 if painter.s.n<10 else 12})
  d=ac.FastDraw(im)
  d.rectangle((0,0,1280,44),fill=ac.BG)
  d.text((35,20),'THE WELL-TEMPERED clAIvier · REVISION AUDITION',font=ac.font(14,True),fill=ac.ACCENT)
  edition=s['edition'];color='#97513e' if edition=='FIRST EDITION' else '#306c60'
  w=d.textlength(edition,font=ac.font(16,True));x=1245-w-28
  d.rounded_rectangle((x,9,1250,40),radius=5,fill=color)
  d.text((x+15,15),edition,font=ac.font(16,True),fill='#ffffff')
  d.rectangle((34,96,1246,130),fill=ac.BG)
  d.text((36,102),f"{painter.s.n} WRITTEN PARTS · QUARTER = {painter.s.bpm:g} · BARS {s['first_bar']}–{s['last_bar']}",font=ac.font(14),fill=ac.MUTED)
  tag='NEW MATERIAL' if s.get('unpaired_new_material') else f"PAIR {s['pair_index']+1} / 4"
  tw=d.textlength(tag,font=ac.font(13,True));d.text((1244-tw,103),tag,font=ac.font(13,True),fill=color)
  return im

def write_chapters(segments,length):
 p=WORK/'comparison-chapters.ffmetadata'
 lines=[';FFMETADATA1','title=The Well-Tempered clAIvier — revision comparison','artist=ChatGPT / composed for Sam','comment=First edition followed by second edition in each pair. Identical FluidR3 piano; a common gain within each pair. Revised phrasing and balance are part of the change.']
 for s in segments:
  if s['kind']!='music':continue
  title=f"{s['work']} — {s['edition']} — bars {s['first_bar']}-{s['last_bar']}"
  lines+=['[CHAPTER]','TIMEBASE=1/1000',f"START={round(s['timeline_start']*1000)}",f"END={round((s['timeline_start']+s['duration'])*1000)}",'title='+title]
 p.write_text('\n'.join(lines)+'\n');return p

def verify_video(path,expected,fps):
 r=json.loads(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,width,height,duration','-of','json',str(path)],capture_output=True,text=True,check=True).stdout)
 # MP4 chapters may add a legitimate data stream alongside video and audio.
 if not {'video','audio'}.issubset({s['codec_type'] for s in r['streams']}):raise RuntimeError('Missing video/audio stream')
 video=next(s for s in r['streams'] if s['codec_type']=='video')
 if (video.get('width'),video.get('height'))!=(1280,720):raise RuntimeError('Unexpected video dimensions')
 if abs(float(r['format']['duration'])-expected)>1/fps+.04:raise RuntimeError('Video duration mismatch')
 p=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(path),'-map','0:v:0','-map','0:a:0','-f','null','-'],capture_output=True,text=True)
 if p.returncode or p.stderr.strip():raise RuntimeError('Video full-decode failed: '+p.stderr)
 return r

def main():
 ap=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
 ap.add_argument('--canonical-ready',action='store_true');ap.add_argument('--preview-only',action='store_true')
 ap.add_argument('--xxiv-start',type=float);ap.add_argument('--bonus-start',type=float)
 ap.add_argument('--fps',type=int,default=12);ap.add_argument('--soundfont',type=Path,default=SF)
 args=ap.parse_args()
 if not args.canonical_ready:
  print(json.dumps({'status':'editorial plan only; awaiting finalized canonical second edition','pairs':PAIRS,'execution':'--canonical-ready after the score handoff; optional --xxiv-start and --bonus-start'},indent=2));return
 if not 1<=args.fps<=15:raise ValueError('Use 1–15 fps')
 WORK.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
 segments,length,sources=build_plan(args);renderer_hash=sha(ROOT/'tools/render_music.py');painter=ComparisonPainter(segments)
 previews=WORK/'previews';previews.mkdir(exist_ok=True)
 for ix,s in enumerate(segments):
  if s['kind']=='music':painter.frame(s['timeline_start']+min(3,s['music_seconds']/2)).save(previews/f"pair-{s['pair_index']+1}-{s['edition'].split()[0].lower()}.png")
 painter.frame(0).save(previews/'intro.png')
 plan={'status':'preview only' if args.preview_only else 'rendering','duration_seconds':length,'fps':args.fps,'segments':segments,'sources':sources,'previews':str(previews)}
 ac.atomic_json(WORK/'editorial-plan.json',plan)
 if args.preview_only:print(json.dumps(plan,indent=2));return
 track,peak=make_soundtrack(segments,length,args.soundfont);chapters=write_chapters(segments,length)
 silent=WORK/'comparison-silent.mp4';proc=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1280x720','-r',str(args.fps),'-i','-','-an','-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-movflags','+faststart',str(silent)],stdin=subprocess.PIPE)
 try:
  for k in range(math.ceil(length*args.fps)):
   proc.stdin.write(painter.frame(k/args.fps).tobytes())
   if k and k%(args.fps*20)==0:print(json.dumps({'stage':'video','seconds':k/args.fps,'total':length}),flush=True)
 finally:proc.stdin.close()
 if proc.wait():raise RuntimeError('Silent video encoder failed')
 video=OUT/'well-tempered-clAIvier-revision-comparison.mp4';temp_video=WORK/'comparison-muxing.mp4'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(silent),'-i',str(track),'-i',str(chapters),'-map','0:v:0','-map','1:a:0','-map_metadata','2','-map_chapters','2','-c:v','copy','-c:a','aac','-b:a','192k','-t',str(length),'-movflags','+faststart',str(temp_video)],check=True)
 checked=verify_video(temp_video,length,args.fps)
 audio=OUT/'well-tempered-clAIvier-revision-comparison.mp3';temp_audio=WORK/'comparison-encoding.mp3'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(track),'-i',str(chapters),'-map','0:a:0','-map_metadata','1','-map_chapters','1','-codec:a','libmp3lame','-b:a','192k',str(temp_audio)],check=True)
 audio_seconds=ac.duration(temp_audio)
 if abs(audio_seconds-length)>.08:raise RuntimeError('MP3 duration mismatch')
 subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(temp_audio),'-f','null','-'],check=True)
 for path,expected in sources.items():
  if sha(path)!=expected:raise RuntimeError('Source changed during rendering: '+path)
 if sha(ROOT/'tools/render_music.py')!=renderer_hash:raise RuntimeError('Audio renderer changed during rendering')
 ac.publish_file(temp_video,video);ac.publish_file(temp_audio,audio)
 report={'schema':'clAIvier-revision-comparison/v1','status':'complete; full audio/video decode passed','duration_seconds':length,'mp3_duration_seconds':audio_seconds,'width':1280,'height':720,'fps':args.fps,'soundfont':str(args.soundfont),'soundfont_sha256':sha(args.soundfont),'audio_renderer_sha256':renderer_hash,
  'comparison_method':'Same FluidR3 piano and synth settings for both editions. Intermediate peak normalization is undone; a common gain is applied within each pair. Written velocity, articulation and panning remain edition-specific. A pre-roll includes every note already sounding at each entrance; excerpt edges have 12 ms/250 ms fades.',
  'limits':'Score-synchronized synthetic audition. The film does not claim an independent human auditory assessment, Bach-level quality or perceptual independence merely from the number of written parts.',
  'peak_pcm':peak,'sources':sources,'segments':segments,'outputs':{'video':str(video),'audio':str(audio)},'output_sha256':{'video':sha(video),'audio':sha(audio)},'output_bytes':{'video':video.stat().st_size,'audio':audio.stat().st_size},'ffprobe':checked,'previews':str(previews)}
 ac.atomic_json(ROOT/'work/revision/comparison-manifest.json',report)
 silent.unlink(missing_ok=True)
 print(json.dumps({'status':report['status'],'duration_seconds':length,'outputs':report['outputs'],'bytes':report['output_bytes']},indent=2))

if __name__=='__main__':main()
