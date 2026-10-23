#!/usr/bin/env python3
"""Assemble the score, audition and inspectable source package for Draft 1."""
from pathlib import Path
import json
import subprocess
import shutil
import zipfile

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from pypdf import PdfReader, PdfWriter

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'
FONT=Path('/usr/share/fonts/truetype/dejavu')
for name,file in [('Serif','DejaVuSerif.ttf'),('Sans','DejaVuSans.ttf'),
                  ('SansBold','DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONT/file)))
INK=colors.HexColor('#19232d')
BLUE=colors.HexColor('#285c79')
MUTED=colors.HexColor('#596673')
LIGHT=colors.HexColor('#edf3f6')
W,H=A4

def text(c,x,y,s,size=10,font='Sans',color=INK):
    c.setFillColor(color);c.setFont(font,size);c.drawString(x,y,s)

def para(c,x,y,s,width=499,size=10.5,leading=15,color=INK,font='Sans'):
    style=ParagraphStyle('body',fontName=font,fontSize=size,leading=leading,textColor=color)
    p=Paragraph(s,style);_,h=p.wrap(width,600);p.drawOn(c,x,y-h);return y-h

def line(c,y):
    c.setStrokeColor(colors.HexColor('#cbd6dc'));c.setLineWidth(.6);c.line(48,y,W-48,y)

def footer(c,label):
    line(c,48)
    text(c,48,32,'The Well-Tempered clAIvier · First audition · October 2026',8,color=MUTED)
    c.setFont('Sans',8);c.drawRightString(W-48,32,label)

def roman(n):
    s=''
    for value,letters in [(10,'X'),(9,'IX'),(5,'V'),(4,'IV'),(1,'I')]:
        while n>=value:s+=letters;n-=value
    return s

def make_notes():
    audit=json.loads((OUT/'final-audit.json').read_text())
    plan=json.loads((OUT/'cycle-plan.json').read_text())
    p=OUT/'program-notes.pdf';c=canvas.Canvas(str(p),pagesize=A4)
    c.setTitle('The Well-Tempered clAIvier — IV: first audition')
    c.setAuthor('ChatGPT / composed for Sam')
    text(c,48,778,'THE WELL-TEMPERED',12,'SansBold',BLUE)
    text(c,45,717,'clAIvier',49,'Serif')
    text(c,48,671,'IV · C-sharp minor',24,'Serif')
    text(c,48,640,'Prelude and five-voice fugue',15,'Sans')
    text(c,48,612,'DRAFT 1  /  FIRST AUDITION',9,'SansBold',BLUE)
    para(c,48,580,
         'One newly composed pair from a planned cycle of 24. Fugue N will have '
         'N + 1 independent voices. IV is the first test: five named parts, each '
         'with a complete subject or answer entry.',size=11,leading=16)
    for x,title,detail in [(48,'PRELUDE','32 bars · quarter = 80 · about 1:39'),
                           (307,'FUGUE','76 bars · quarter = 82 · about 3:45')]:
        c.setFillColor(LIGHT);c.roundRect(x,474,240,58,5,fill=1,stroke=0)
        text(c,x+13,510,title,9,'SansBold',BLUE)
        text(c,x+13,489,detail,9.5)
    text(c,48,449,'LISTENING MAP',10,'SansBold')
    text(c,48,430,'Times are relative to the start of the fugue.',9,color=MUTED)
    rows=[('0:00','1','Exposition: Alto II, Alto I, Soprano, Tenor, Bass'),
          ('0:47','17','The fifth voice enters; the full texture is heard'),
          ('1:22','29','The subject appears in the relative major'),
          ('2:09','45','Three entries overlap at two-bar distances'),
          ('2:44','57','The bass subject moves at half speed'),
          ('3:25','71','Last tonic statement and the closing cadence')]
    for i,(time,bar,event) in enumerate(rows):
        y=405-i*23
        text(c,48,y,time,10,'SansBold',BLUE)
        text(c,99,y,'m. '+bar,9.5,color=MUTED)
        text(c,154,y,event,9.5)
    line(c,270)
    text(c,48,246,'WHAT WAS CHECKED',10,'SansBold')
    para(c,48,230,
         'All 16 complete subject entries match their intended pitches and durations. '
         'All five parts sound together for 192 of the 304 beats. The event audit found '
         'no parallel fifths or octaves, no flagged direct outer perfect intervals with '
         'an upper leap, and no voice crossings. Five prepared suspensions were reviewed '
         'individually. The detailed audit and editable note data are included.',size=10,leading=14)
    para(c,48,135,
         '<b>Musical status.</b> This is a first draft for critical listening. Mechanical '
         'checks do not establish beauty, complete historical style, or parity with Bach. '
         'The audio is a sampled piano realization. The score uses separate staves to '
         'make the contrapuntal parts visible; human playability was not a constraint.',
         size=9.5,leading=14,color=MUTED)
    footer(c,'Program note');c.showPage()

    text(c,48,778,'THE COMPLETE CYCLE · COMPOSITION PLAN',11,'SansBold',BLUE)
    text(c,48,741,'A voice added with every fugue',22,'Serif')
    para(c,48,711,'Only IV is composed in this package. The other 23 pairs are planned.',
         size=11,leading=16,font='SansBold')
    text(c,48,666,'NO.',9,'SansBold',MUTED);text(c,89,666,'MAJOR KEY',9,'SansBold',MUTED)
    text(c,234,666,'VOICES',9,'SansBold',MUTED)
    text(c,301,666,'NO.',9,'SansBold',MUTED);text(c,352,666,'MINOR KEY',9,'SansBold',MUTED)
    text(c,495,666,'VOICES',9,'SansBold',MUTED)
    line(c,655)
    for i in range(12):
        y=634-i*24
        if i==1:
            c.setFillColor(LIGHT);c.roundRect(294,y-7,253,24,3,fill=1,stroke=0)
        for side,index in enumerate([2*i,2*i+1]):
            m=plan['movements'][index];x=48 if side==0 else 301
            bold=m['number']==4
            text(c,x,y,roman(m['number']),10,'SansBold' if bold else 'Sans',BLUE if bold else INK)
            name=m['key'].replace(' major','').replace(' minor','')
            text(c,x+(41 if side==0 else 51),y,name,10.5,'SansBold' if bold else 'Sans')
            text(c,234 if side==0 else 495,y,str(m['voices']),10.5,'SansBold' if bold else 'Sans')
    line(c,352)
    text(c,48,325,'WHAT COUNTS AS A VOICE',10,'SansBold')
    y=306
    for s in [
        'A stable monophonic part with its own melodic and rhythmic life.',
        'A complete subject, answer or justified thematic variant in every part.',
        'Octave doubling alone does not add a voice to the count.',
        'A substantial passage where all the advertised parts sound together.'
    ]:
        text(c,50,y-11,'•',11,color=BLUE)
        y=para(c,66,y,s,width=481,size=10,leading=14)-9
    para(c,48,190,
         'The later fugues can use contrasting instruments and groups of voices to '
         'make the counterpoint audible. Rests, changing density and clear phrasing '
         'remain available. Twenty-five simultaneous parts are a musical problem of '
         'clarity as well as a problem of correct note combinations.',size=10.5,leading=15)
    para(c,48,106,
         'Total across the proposed cycle: 324 part assignments. The final fugue has '
         '300 pairs of voices to inspect. The full key-by-key plan is in cycle-plan.json.',
         size=9.5,leading=14,color=MUTED)
    footer(c,'Cycle plan');c.save()
    return p

def assemble_score(notes):
    writer=PdfWriter()
    paths=[notes,OUT/'04-prelude-csharp-minor.pdf',OUT/'04-fugue-csharp-minor.pdf']
    starts=[]
    for p in paths:
        starts.append(len(writer.pages));writer.append(str(p),import_outline=False)
    writer.add_outline_item('Program note',0)
    writer.add_outline_item('Cycle plan',1)
    writer.add_outline_item('IV. Prelude',starts[1])
    writer.add_outline_item('IV. Fugue a 5',starts[2])
    writer.add_metadata({'/Title':'The Well-Tempered clAIvier — IV. Prelude and Fugue',
                         '/Author':'ChatGPT / composed for Sam',
                         '/Subject':'Original piano music, five-voice fugue, Draft 1'})
    target=OUT/'well-tempered-clAIvier-IV-score.pdf'
    with target.open('wb') as f:writer.write(f)
    return target

def assemble_audio():
    target=OUT/'04-prelude-and-fugue-csharp-minor.mp3'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
        '-i',str(OUT/'04-prelude-csharp-minor.wav'),
        '-i',str(OUT/'04-fugue-csharp-minor.wav'),
        '-filter_complex','[0:a]apad=pad_dur=2[a];[a][1:a]concat=n=2:v=0:a=1[out]',
        '-map','[out]','-codec:a','libmp3lame','-b:a','192k',
        '-metadata','title=The Well-Tempered clAIvier - IV. Prelude and Fugue',
        '-metadata','artist=ChatGPT / composed for Sam',str(target)],check=True)
    return target

def source_archive():
    requirements='ortools\nmido\nnumpy\nscipy\npyfluidsynth\nreportlab\npypdf\n'
    (OUT/'requirements.txt').write_text(requirements)
    archive=OUT/'well-tempered-clAIvier-IV-source.zip'
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in ['README.txt','requirements.txt','cycle-plan.json','final-audit.json',
                     'audit-notes.txt','fugue_iv.json','prelude_iv.json',
                     'well-tempered-clAIvier-IV-score.pdf']:
            z.write(OUT/name,'clAIvier/'+name)
        for stem in ['04-prelude-csharp-minor','04-fugue-csharp-minor']:
            for ext in ['ly','musicxml','mid','pdf']:
                z.write(OUT/f'{stem}.{ext}',f'clAIvier/scores/{stem}.{ext}')
        z.write(OUT/'04-fugue-csharp-minor-chamber.mid','clAIvier/scores/04-fugue-csharp-minor-chamber.mid')
        for name in ['compose_iv.py','compose_prelude_iv.py','refine_fugue_rhythm.py',
                     'audit_music.py','render_music.py','package_project.py','build_delivery.py']:
            z.write(ROOT/'tools'/name,'clAIvier/tools/'+name)
        z.write(ROOT/'work'/'review_dissonances.py','clAIvier/work/review_dissonances.py')
        z.write(ROOT/'work'/'fugue_iv_v5.json','clAIvier/work/fugue_iv_structural.json')
        z.write(ROOT/'work'/'subject_proposal.txt','clAIvier/work/subject_proposal.txt')
    return archive

def main():
    subprocess.run(['python',str(ROOT/'tools/package_project.py')],check=True)
    notes=make_notes();score=assemble_score(notes);audio=assemble_audio();archive=source_archive()
    print(json.dumps({'score':str(score),'score_pages':len(PdfReader(score).pages),
                      'paired_audio':str(audio),'source_archive':str(archive)},indent=2))

if __name__=='__main__':main()
