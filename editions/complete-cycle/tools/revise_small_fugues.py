#!/usr/bin/env python3
"""Second-edition structural revisions for fugues I--III and V--VII.

The first draft reused one form and made its short stretto by overlapping
only a sustained tonic. These revisions give the smaller fugues distinct
tonal journeys, literal subject-head sequences, and (where the theme permits)
earlier imitative overlaps. Fugue V--VII now retain all six to eight voices
through their closing return and cadence. Rhythmic/dissonance refinement is
a separate, later project pass.
"""
from pathlib import Path
import argparse, copy, json, math, sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'vendor'))
sys.path.insert(0, str(ROOT / 'tools'))
from compose_cycle_fugues import (FugueBuilder, KEY_NAMES, KEY_PCS, TITLES,
    TEMPOS, ROMANS, THEMES, theme_events, expand_events, compress_line,
    solve_counterpoint, tonic_near, vocab)
import audit_music

OUT = ROOT / 'work/revision/small_fugues'
LETTERS = 'cdefgab'
NATURALS = [0, 2, 4, 5, 7, 9, 11]


def tonic_name(home_name, home_pc, local_pc, home_mode, local_mode):
    interval = (local_pc - home_pc) % 12
    if interval == 0:
        return home_name
    if home_mode != local_mode and interval == (9 if home_mode == 'major' else 3):
        shift = 5 if home_mode == 'major' else 2
    else:
        shift = {2:1, 3:2, 4:2, 5:3, 7:4, 8:5, 9:5, 10:6, 11:6}.get(interval)
        if shift is None:
            raise ValueError(('unsupported tonal region', interval))
    li = (LETTERS.index(home_name[0].lower()) + shift) % 7
    alt = (local_pc - NATURALS[li] + 6) % 12 - 6
    return LETTERS[li].upper() + ('#' * alt if alt >= 0 else 'b' * (-alt))


def spelling_table(name, pc, mode):
    li = LETTERS.index(name[0].lower())
    scale = [0,2,4,5,7,9,11] if mode == 'major' else [0,2,3,5,7,8,10]
    items = list(enumerate(scale)) + ([(6,11)] if mode == 'minor' else [])
    result = {}
    for deg, offset in items:
        letter = (li + deg) % 7
        pitch = (pc + offset) % 12
        alt = (pitch - NATURALS[letter] + 6) % 12 - 6
        result[pitch] = LETTERS[letter] + ('is' * alt if alt >= 0 else 'es' * (-alt))
    return result


class RevisedBuilder(FugueBuilder):
    def __init__(self, num, seconds=2.5):
        super().__init__(num, seconds)
        self.home_mode = self.mode
        self.home_key = self.key
        self.home_name = KEY_NAMES[num-1]
        self.templates = {
            'subject': {'events': copy.deepcopy(self.subject), 'mode': self.mode},
            'countersubject': {'events': copy.deepcopy(self.countersubject), 'mode': self.mode}
        }
        self.fragments = []
        self.revision_notes = []

    def realize(self, *args, **kwargs):
        old = len(self.harmonies)
        start = super().realize(*args, **kwargs)
        for h in self.harmonies[old:]:
            h['mode'] = self.mode
            h['key_name'] = tonic_name(self.home_name, self.home_key % 12,
                                       h['key'], self.home_mode, self.mode)
        return start

    def relative_material(self):
        mode = 'minor' if self.home_mode == 'major' else 'major'
        sid, cid = 'subject_relative', 'countersubject_relative'
        if sid not in self.templates:
            subject = theme_events(self.num, mode)
            spec = dict(n=2, length=self.length, key=0, mode=mode,
                        centers=[66,55], active=[[True]*self.length for _ in range(2)],
                        pins={f'0,{q}':p for q,p in enumerate(expand_events(subject))},
                        invertible=True, seconds=10, seed=701+self.num)
            cs = compress_line(solve_counterpoint(spec)['pitches'][1])
            for e in cs:
                for k in ['source','v','label']:
                    e.pop(k, None)
            self.templates[sid] = {'events':subject, 'mode':mode,
                                  'relationship':'Diatonic modal variant of the main subject'}
            self.templates[cid] = {'events':cs, 'mode':mode,
                                  'relationship':'Countersubject for the relative-key variant'}
        return mode, self.home_key + (9 if self.home_mode=='major' else 3), sid, cid

    def relative_statement(self, voice, indices, cs_voice=None, section='Relative-key development'):
        mode, key, sid, cid = self.relative_material()
        old_mode, old_s, old_cs = self.mode, self.subject, self.countersubject
        self.mode = mode
        self.subject = self.templates[sid]['events']
        self.countersubject = self.templates[cid]['events']
        before = len(self.entries)
        self.statement(voice, indices, key=key, cs_voice=cs_voice,
                       label='Relative-key subject', section=section)
        for entry in self.entries[before:]:
            entry['subject_id'] = sid if entry['subject_id']=='subject' else cid
        region = tonic_name(self.home_name, self.home_key%12, key%12,
                            self.home_mode, mode)
        self.sections[-1]['detail'] += f'; {region} {mode}, a change of tonal mode as well as root'
        self.mode, self.subject, self.countersubject = old_mode, old_s, old_cs

    def motif_sequence(self, indices, chords=None, local_relative=False,
                       leader=None, section='Subject-head sequence'):
        """Sequence the opening third/fifth, not a generic solver contour.

        The source head has two distinct pitches in every selected subject.
        Its rhythm is compressed to two equal quarter beats; its interval is
        adjusted to the current diatonic chord, a conventional tonal sequence.
        No fragment is falsely logged as a complete subject statement.
        """
        old_mode = self.mode
        key = self.home_key
        source_id = 'subject'
        if local_relative:
            mode,key,source_id,_ = self.relative_material()
            self.mode = mode
        if chords is None:
            chords = ['vi','ii','V','I'] if self.mode=='major' else ['iv','VII','III','VI']
        harmony = [c for c in chords for _ in range(2)]
        leader = indices[0] if leader is None else leader
        tones = dict(vocab(key%12, self.mode))
        prototype = self.templates[source_id]['events']
        interval_class = (prototype[1]['p'] - prototype[0]['p']) % 12
        chord_position = 2 if interval_class == 7 else 1
        # A fifth above a chord root belongs in an upper part here. Putting
        # the literal fifth in the lowest part would create an unsupported
        # six-four chord under this deliberately consonant structural frame.
        if chord_position==2 and leader==max(indices):
            leader=indices[-2]
        pins={}
        fragment_entries=[]
        partner=indices[-1] if leader!=indices[-1] else indices[0]
        if chord_position==2 and partner==max(indices):
            partner=indices[0] if leader!=indices[0] else indices[-2]
        for j, chord in enumerate(chords):
            voice=leader if j%2==0 else partner
            chordtones=tones[chord]
            root=tonic_near(chordtones[0], self.centers[voice]-2)
            upper=root+(chordtones[chord_position]-chordtones[0])%12
            # A diminished fifth is not inserted as an unprepared melodic leap.
            if upper-root==6:
                upper=root+(chordtones[1]-chordtones[0])%12
            pins.setdefault(voice,[]).extend([dict(t=2*j,d=1,p=root,label='Subject-head fragment'),
                       dict(t=2*j+1,d=1,p=upper,label='Subject-head fragment')])
            fragment_entries.append(dict(voice=voice,t=2*j,d=2,
                                          source_subject=source_id,source_note_indices=[0,1],
                                          technique='tonal sequential head fragment',harmony=chord))
        start=self.realize(indices,len(harmony),pins,harmony=harmony,key=key,
                           label=section,
                           detail='A two-note head of the subject is passed through a directed harmonic sequence; rhythm and intervals are tonally adapted.')
        self.fragments.extend(dict(e,t=e['t']+start) for e in fragment_entries)
        self.mode=old_mode

    def harmonic_link(self, indices, chords, local_relative=False,
                      section='Cadential link'):
        old=self.mode;key=self.home_key
        if local_relative:
            self.mode,key,_,_=self.relative_material()
        plan=[c for c in chords for _ in range(2)]
        self.realize(indices,len(plan),harmony=plan,key=key,label=section,
                     detail='A directed bass and harmonic progression prepares the next thematic entry.')
        self.mode=old

    def close_stretto(self, indices, first, second, lag, second_shift=0):
        length=4*math.ceil((self.length+lag)/4)
        pins={}; trans={}
        for v,offset,shift in [(first,0,0),(second,lag,second_shift)]:
            anchor=tonic_near(self.key+shift,self.centers[v])
            trans[v]=anchor-60
            pins[v]=[dict(e,t=e['t']+offset,p=e['p']+anchor-60,label='Stretto subject') for e in self.subject]
        overlap=self.length-lag
        detail=f'Two complete subjects overlap for {overlap} beats at an entry distance of {lag} beats; the overlap includes motion in the first subject.'
        if second_shift:
            # The overlapping part is consonant in the home key. After the
            # first statement finishes, the second statement's chromatic
            # scale degrees establish its own key. Keep that real modulation
            # in the harmony clock instead of forcing it into home-key triads.
            def excerpt(a,b):
                return {v:[dict(e,t=max(a,e['t'])-a,d=min(b,e['t']+e['d'])-max(a,e['t']))
                           for e in es if e['t']<b and e['t']+e['d']>a]
                        for v,es in pins.items()}
            old_sections=len(self.sections)
            start=self.realize(indices,self.length,excerpt(0,self.length),
                               label='Stretto',detail=detail,velocity=79)
            self.realize(indices,length-self.length,excerpt(self.length,length),
                         key=self.key+second_shift,label='Stretto continuation',
                         detail='The second entry completes its own tonal region.',velocity=79)
            self.sections[old_sections:]=[dict(t=start,d=length,label='Stretto',
                                              detail=detail,voices=list(indices))]
        else:
            start=self.realize(indices,length,pins,label='Stretto',detail=detail,velocity=79)
        for v,offset in [(first,0),(second,lag)]:
            self.entries.append(dict(voice=v,t=start+offset,transpose=trans[v],scale=1,
                                     subject_id='subject',label='Stretto subject'))
        self.revision_notes.append(f'Main-subject overlap enlarged to {overlap} beats, including active tail material.')

    def full_cadence(self):
        indices=list(range(self.n))
        plan=(['IV','IV','V','V','I','I','I','I'] if self.home_mode=='major'
              else ['iv','iv','V','V','i','i','i','i'])
        root=tonic_near(self.key,self.centers[-1])
        top=tonic_near(self.key,self.centers[0])
        pins={self.n-1:[dict(t=4,d=4,p=root,label='Cadential tonic bass')],
              0:[dict(t=4,d=4,p=top,label='Cadential tonic arrival')]}
        self.realize(indices,8,pins,harmony=plan,label='Final cadence',
                     detail=f'All {self.n} parts complete the dominant-to-tonic cadence; the outside voices arrive on tonic.',velocity=72)
        for v in indices:
            self.voices[v]['events'].append(dict(t=self.t,d=4,p=self.previous[v],v=65,
                                                source='supporting counterpoint',label='Final tonic'))
        self.sections[-1]['d']+=4
        self.t+=4

    def exposition(self):
        orders={1:[0,1],2:[1,0,2],3:[1,0,2,3],
                5:[2,1,3,0,4,5],6:[3,2,4,1,5,0,6],7:[3,2,4,1,5,0,6,7]}
        active=[];previous=None
        for j,v in enumerate(orders[self.num]):
            active.append(v)
            self.statement(v,active,key=self.key+(7 if j%2 else 0),cs_voice=previous,
                           label='Real answer' if j%2 else 'Subject',section='Continuous exposition')
            previous=v
        if self.n>=6:
            self.revision_notes.append('One continuous exposition introduces every part; the texture is not reset to a new solo choir after five entries.')

    def compose_revision(self):
        self.exposition()
        full=list(range(self.n));core=sorted(set([0,self.n//2,self.n-1]))
        if self.num==1:
            self.motif_sequence(full,['vi','ii','V','I'],leader=0)
            self.relative_statement(1,full,cs_voice=0)
            self.motif_sequence(full,['iv','VII','III','VI'],local_relative=True,leader=1,
                                section='Minor-coloured sequential answer')
            self.harmonic_link(full,['ii','V','I','I'],section='Return to C')
            self.close_stretto(full,1,0,5)
            self.statement(0,full,cs_voice=1,section='Closing conversation')
        elif self.num==2:
            self.motif_sequence(full,['iv','VII','III','III'],leader=2,
                                section='Sequence toward the relative major')
            self.relative_statement(0,full,cs_voice=2)
            self.motif_sequence(full,['vi','ii','V','I'],local_relative=True,leader=1,
                                section='Major-mode episode')
            self.harmonic_link(full,['VI','iv','V','i'],section='Minor-mode return')
            # This particular theme does not admit a closer consonant overlap.
            self.stretto(full,2,0)
            self.sections[-1]['detail']='The final held tonic of the first subject overlaps the next subject by two beats; this is a mild tail overlap, not dense stretto.'
            self.statement(1,full,cs_voice=0,section='Middle-voice final return')
            self.revision_notes.append('The genuine two-beat tail overlap is retained and explicitly qualified; no stronger stretto is claimed.')
        elif self.num==3:
            self.motif_sequence(full,['vi','ii','V','I'],leader=3)
            self.relative_statement(2,[0,2,3],cs_voice=0,
                                    section='Shadow in the relative minor')
            self.motif_sequence([0,2,3],['iv','VII','III','VI'],local_relative=True,leader=3)
            self.harmonic_link(full,['ii','V','I','IV'],section='Subdominant preparation')
            self.close_stretto(full,3,0,4,5)
            self.statement(1,full,cs_voice=2,section='Four-part final return')
        elif self.num==5:
            self.motif_sequence(full,['vi','ii','V','I'],leader=5,
                                section='Six-part sequential release')
            self.relative_statement(2,[0,2,4,5],cs_voice=4,
                                    section='Relative-minor interior')
            self.motif_sequence([0,2,4,5],['iv','VII','III','VI'],local_relative=True,leader=0)
            self.harmonic_link(full,['ii','V','I','I'],section='The six parts reconvene')
            self.close_stretto(full,5,0,8)
            self.statement(3,full,cs_voice=1,section='Six-part final return')
            self.motif_sequence(full,['IV','ii','V','I'],leader=4,section='Cadential head sequence')
        elif self.num==6:
            self.motif_sequence(full,['iv','VII','III','III'],leader=6,
                                section='Seven-part ascent to the relative major')
            self.relative_statement(1,[0,1,3,6],cs_voice=3)
            self.motif_sequence([0,1,3,6],['vi','ii','V','I'],local_relative=True,leader=6)
            self.harmonic_link(full,['VI','iv','V','i'],section='The seven parts reconvene')
            self.close_stretto(full,6,0,8,7)
            self.statement(4,full,cs_voice=2,section='Seven-part final return')
        elif self.num==7:
            self.motif_sequence(full,['vi','ii','V','I'],leader=7,
                                section='Eight-part sequential release')
            self.relative_statement(3,[1,3,5,7],cs_voice=5,
                                    section='Relative-minor quartet')
            self.motif_sequence([1,3,5,7],['iv','VII','III','VI'],local_relative=True,leader=7)
            self.statement(2,[0,2,4,6],key=self.key+5,cs_voice=4,
                           label='Subdominant subject',section='Answering quartet')
            self.harmonic_link(full,['ii','V','I','IV'],section='Eight-part reunion')
            self.close_stretto(full,7,0,8,5)
            self.statement(3,full,cs_voice=4,section='Eight-part final return')
        self.full_cadence()
        for voice in self.voices:
            voice['events'].sort(key=lambda e:e['t'])
            for e in voice['events']:
                h=self.harmonies[min(int(e['t']),len(self.harmonies)-1)]
                table=spelling_table(h['key_name'],h['key'],h['mode'])
                if e['p']%12 not in table:
                    raise ValueError(('unspelled pitch',e,h))
                e['spell']=table[e['p']%12]
        data=dict(metadata=dict(title='The Well-Tempered clAIvier',
                  subtitle=f'{ROMANS[self.num-1]}. Fugue in {self.home_name} {self.home_mode} — {TITLES[self.num-1]}',
                  number=self.num,movement_number=self.num,piece_type='fugue',character=TITLES[self.num-1],
                  key=self.home_name,mode=self.home_mode,meter=[4,4],bpm=TEMPOS[self.num-1],
                  composer='ChatGPT / composed for Sam',instrument='Piano; optional spatial chamber ensemble',
                  draft=True,edition='Second compositional pass',structural_step=1,voice_order='high_to_low',
                  markers=[dict(t=s['t'],label=s['label']) for s in self.sections],
                  style_note='Structural revision: directed tonal regions, thematic episodes, earlier compatible overlaps, and full-part cadences. Subsequent rhythmic refinement is recorded separately.'),
                  voices=self.voices,subjects=self.templates,subject_entries=self.entries,
                  sections=self.sections,harmony=self.harmonies,motivic_fragments=self.fragments,
                  composition_record=dict(method='Authored formal revision with exact subject variants, tonal head-fragment sequences and constraint-assisted supporting voices.',
                       total_beats=self.t,parts=self.n,solver_sections=self.stats,
                       revision_notes=self.revision_notes,
                       limitations=['Structural frame uses triads before the separate diminution/suspension pass.',
                                    'Symbolic checks do not establish equivalence to Bach or perceptual independence.']))
        return data


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--numbers',nargs='+',type=int,default=[1,2,3,5,6,7])
    parser.add_argument('--seconds',type=float,default=2.5)
    args=parser.parse_args();OUT.mkdir(parents=True,exist_ok=True)
    for num in args.numbers:
        print(json.dumps({'start':num}),flush=True)
        data=RevisedBuilder(num,args.seconds).compose_revision()
        path=OUT/f'{num:02d}-fugue.json'
        path.write_text(json.dumps(data,indent=2))
        report=audit_music.audit(data,max_examples=300)
        (OUT/f'{num:02d}-audit.json').write_text(json.dumps(report,indent=2))
        print(json.dumps({'number':num,'path':str(path),'summary':report['summary']}),flush=True)


if __name__=='__main__':
    main()
