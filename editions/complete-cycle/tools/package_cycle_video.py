#!/usr/bin/env python3
"""Package already verified score-bound films, with deterministic chapters."""
from pathlib import Path
import argparse,csv,hashlib,html,json,os,shutil,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[1]
ROMANS=['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII','XIII','XIV','XV','XVI','XVII','XVIII','XIX','XX','XXI','XXII','XXIII','XXIV']

def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-show_chapters','-of','json',str(p)],text=True))
def check_source(path,source):
    report=json.loads(path.read_text())
    if report.get('score_sha256')!=digest(source):raise ValueError(f'Stale report {path}')
    return report

def build_video(out):
    folder=ROOT/'work/cycle_animation';paths=[];rows=[];cursor=0
    for n in range(1,25):
        for kind in ['prelude','fugue']:
            stem=f'{n:02d}-{kind}'
            p=folder/(stem+'.mp4');source=ROOT/f'work/cycle_{"preludes" if kind=="prelude" else "fugues"}'/(stem+'.json')
            check_source(folder/(stem+'.animation.json'),source)
            info=probe(p);v=next(s for s in info['streams'] if s['codec_type']=='video');a=next(s for s in info['streams'] if s['codec_type']=='audio')
            if (v['width'],v['height'],v['r_frame_rate'],v['codec_name'],a['codec_name'],a['sample_rate'])!=(1280,720,'12/1','h264','aac','44100'):raise ValueError(f'Incompatible stream {p}')
            duration=float(info['format']['duration']);label=ROMANS[n-1]+'. '+kind.title()
            rows.append({'track':len(rows)+1,'pair':n,'movement':kind,'title':label,'start_seconds':cursor,'duration_seconds':duration,'filename':p.name,'source_sha256':digest(source),'video_sha256':digest(p)})
            cursor+=duration;paths.append(p)
    sequence=out/'video-sequence.txt';sequence.write_text('\n'.join("file '"+str(p)+"'" for p in paths)+'\n')
    meta=out/'video-chapters.ffmeta';lines=[';FFMETADATA1','title=The Well-Tempered clAIvier - Complete Animated Cycle','artist=Composed with ChatGPT for Sam']
    for row in rows:lines+=['[CHAPTER]','TIMEBASE=1/1000',f"START={round(row['start_seconds']*1000)}",f"END={round((row['start_seconds']+row['duration_seconds'])*1000)}",'title='+row['title']]
    meta.write_text('\n'.join(lines)+'\n')
    target=out/'well-tempered-clAIvier-complete-animated-cycle.mp4';temp=out/'complete-animated-cycle-building.mp4'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(sequence),'-i',str(meta),'-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1','-c','copy','-movflags','+faststart',str(temp)],check=True)
    with temp.open('rb') as f:os.fsync(f.fileno())
    verify=probe(temp)
    if len(verify['chapters'])!=48 or abs(float(verify['format']['duration'])-cursor)>.25:raise ValueError('Joined duration or chapters incorrect')
    result=subprocess.run(['ffmpeg','-hide_banner','-v','error','-i',str(temp),'-map','0:v:0','-map','0:a:0','-f','null','-'],capture_output=True,text=True)
    if result.returncode or result.stderr.strip():raise ValueError('Full video decode failed: '+result.stderr[-2000:])
    temp.replace(target)
    with target.open('rb') as f:os.fsync(f.fileno())
    with (out/'animation-index.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    report={'movements':48,'chapters':48,'duration_seconds':float(verify['format']['duration']),'full_decode_passed':True,'sha256':digest(target),'source_clips':rows,'scope':'Container, exact source-hash binding, streams, chapter timing and full A/V decode; human visual review of selected frames is documented separately.'}
    (out/'animated-cycle-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'video':str(target),'seconds':report['duration_seconds'],'bytes':target.stat().st_size,'chapters':48}),flush=True)

def build_archives(out):
    src=ROOT/'work/cycle_lessons';rows=[]
    for n in range(1,25):
        stem=f'{n:02d}-fugue-lesson';movie=src/(stem+'.mp4');source=ROOT/f'work/cycle_fugues/{n:02d}-fugue.json'
        report=check_source(src/(stem+'.animation.json'),source)
        info=probe(movie);duration=float(info['format']['duration'])
        rows.append((n,movie,duration))
    index=src/'index.html'
    index.write_text('<!doctype html><meta charset="utf-8"><title>clAIvier: 24 guided fugue lessons</title><style>body{max-width:950px;margin:50px auto;background:#f6f2ea;color:#24333a;font:18px Georgia}li{margin:18px 0}a{color:#a64f36}p{line-height:1.5}</style><h1>24 guided fugue lessons</h1><p>Hear each subject and countersubject alone, then together; trace related-key statements, sequences, prepared suspensions and the assembled texture. Overlaps of a held tail are explicitly identified. Complete themes and short fragments have distinct markings. IV is narrated; the other lessons use on-screen explanations. The later fugues also demonstrate augmentation and expanded ensemble development. These are selected score excerpts; the complete cycle contains every movement in full.</p><ol>'+''.join(f'<li><a href="{html.escape(p.name)}">Fugue {ROMANS[n-1]}: {n+1} parts</a> — {round(d/60,1)} min'+(' · narrated' if n==4 else '')+'</li>' for n,p,d in rows)+'</ol>')
    lessons_archive=out/'well-tempered-clAIvier-24-guided-lessons.zip';lessons_temp=out/'guided-lessons-building.zip'
    with zipfile.ZipFile(lessons_temp,'w',zipfile.ZIP_STORED) as z:
        z.write(index,'index.html')
        for n,p,d in rows:z.write(p,p.name)
    with lessons_temp.open('rb') as f:os.fsync(f.fileno())
    with zipfile.ZipFile(lessons_temp) as z:
        if z.testzip() is not None:raise ValueError('Lesson archive CRC failure')
    lessons_temp.replace(lessons_archive)
    cuearchive=out/'well-tempered-clAIvier-animation-cues.zip';cue_temp=out/'animation-cues-building.zip'
    with zipfile.ZipFile(cue_temp,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for sub in ['cycle_animation','cycle_lessons']:
            for p in sorted((ROOT/'work'/sub).glob('*.json')):z.write(p,sub+'/'+p.name)
        for p in sorted((ROOT/'work/animation').glob('*qc*.json')):z.write(p,'quality/'+p.name)
        for name in ['animated-cycle-verification.json','animation-index.csv','listening-index.csv']:
            p=out/name
            if p.exists():z.write(p,'delivery/'+p.name)
        for name in ['voice-palette-25.json','fugue-lessons.batch.json']:
            p=ROOT/'work/animation'/name
            if p.exists():z.write(p,'animation/'+name)
        narration=json.loads((ROOT/'work/animation/narration-completed.json').read_text())
        clean=[{k:v for k,v in row.items() if k in ['id','text','duration','voice','model']} for row in narration]
        z.writestr('narration/script.json',json.dumps(clean,indent=2)+'\n')
        for p in sorted((ROOT/'work/animation/narration').glob('*.mp3')):z.write(p,'narration/'+p.name)
        for p in sorted((ROOT/'work/animation/lessons').glob('*.json')):z.write(p,'lesson-configs/'+p.name)
        for p in sorted((ROOT/'work/animation/lesson-captions').glob('*')):
            if p.is_file():z.write(p,'lesson-captions/'+p.name)
    with cue_temp.open('rb') as f:os.fsync(f.fileno())
    with zipfile.ZipFile(cue_temp) as z:
        if z.testzip() is not None:raise ValueError('Cue archive CRC failure')
    cue_temp.replace(cuearchive)
    shutil.copy2(src/'04-fugue-lesson.mp4',out/'well-tempered-clAIvier-IV-narrated-lesson.mp4')
    shutil.copy2(ROOT/'work/cycle_animation/24-spatial-rehearsal.mp4',out/'well-tempered-clAIvier-XXIV-spatial-rehearsal.mp4')
    print(json.dumps({'lessons':24,'lesson_seconds':sum(r[2] for r in rows),'cue_archive':str(cuearchive)}),flush=True)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--only',choices=['video','archives','all'],default='all');args=ap.parse_args()
    out=ROOT/'output/complete-cycle';out.mkdir(parents=True,exist_ok=True)
    if args.only in ['video','all']:build_video(out)
    if args.only in ['archives','all']:build_archives(out)
if __name__=='__main__':main()
