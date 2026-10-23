#!/usr/bin/env python3
"""Prepare a reviewable editorial handoff, not an authorized Slopcannon job."""
from pathlib import Path
import hashlib,json,math
ROOT=Path(__file__).resolve().parents[1]

def main():
    base=ROOT/'work/film_xxiv';design=json.loads((base/'production-design.json').read_text())
    report=json.loads((ROOT/'work/spatial_audio/spatial-audio-report.json').read_text())
    capability_path=base/'slopcannon-public-capabilities.json'
    capabilities=json.loads(capability_path.read_text());contract=capabilities['contract']
    generation=contract['generation'];minimum_ms=generation['sceneDurationMs']['minimum'];maximum_ms=generation['sceneDurationMs']['maximum']
    rate=generation['cannonCreditsPerOutputSecond']
    assert '2K' in generation['resolution'] and '16:9' in generation['aspectRatios']
    assert report['source_sha256']==design['score_binding']['sha256']
    duration=report['spatial_render']['duration_seconds'];shots=list(design['shot_timeline'])
    written=design['score_binding']['duration_seconds']
    shots.append({'shot_id':'TAIL','start_seconds':written,'end_seconds':duration,'type':'hold the whole architecture as the last sound decays','camera_station':'C05','subject_players':[],'countersubject_players':[]})
    players={p['player_id']:p for p in design['players']};scenes=[]
    for shot in shots:
        start=shot['start_seconds'];end=shot['end_seconds'];length=end-start
        count=max(1,math.ceil(length/(maximum_ms/1000)))
        for j in range(count):
            a=start+length*j/count;b=start+length*(j+1)/count
            requested_ms=max(minimum_ms,math.ceil((b-a)*1000-1e-9));requested=requested_ms/1000
            assert requested_ms<=maximum_ms
            focus=[players[p] for p in shot.get('subject_players',[]) if p in players]
            cast='; '.join(p['player_id']+': '+p['instrument']+', '+p['visible_identity'] for p in focus)
            direction=(
                'A restrained cinematic instrumental performance in a conceptual Sagrada Familia-inspired interior: '
                'branching pale stone columns, warm and cool stained-glass side light, quiet charcoal formal clothing. '
                'Use the locked 25-person cast and fixed world positions in production-design.json. '
                'No additional performers, audience or conductor. Keep the same instrument, appearance and position for every player. '
                f"This scene: {shot['type']}. Camera station {shot['camera_station']}. "
                +(f'Primary subject performer: {cast}. ' if cast else 'Preserve the ensemble geography in a sustained architectural view. ')
                +(f"Teaching inset: {shot['teaching_inset']}. " if shot.get('teaching_inset','none')!='none' else '')
                +('Maintain the previous framing through this cue change; do not introduce a hard cut. ' if j or not shot.get('cut_on_start',True) else '')
                +'Instrumental motion should follow the supplied isolated part cues; precise teaching text, player IDs, note graphics and sounding counts are composited from the deterministic cue layer. '
                'Preserve the original instrumental soundtrack; no generated singing, dialogue, applause or added music. '
                'This is a digital film concept, not documentary footage of a real event.'
            )
            scenes.append({'scene_id':f'SC{len(scenes)+1:03d}','editorial_shot_id':shot['shot_id'],
                           'source_start_seconds':round(a,6),'edit_end_seconds':round(b,6),
                           'edit_duration_seconds':round(b-a,6),'planned_generation_duration_seconds':round(requested,6),
                           'planned_generation_duration_ms':requested_ms,
                           'final_take_in_seconds':0,'final_take_out_seconds':round(b-a,6),
                           'cue_clock_offset_seconds':round(a,6),
                           'cue_clock_rule':'local cue time = canonical source seconds minus cue_clock_offset_seconds; preserve notes already active at the clip start',
                           'cut_on_start':bool(shot.get('cut_on_start',True) and j==0 and len(scenes)>0),
                           'camera_station':shot['camera_station'],'subject_players':shot.get('subject_players',[]),
                           'countersubject_players':shot.get('countersubject_players',[]),
                           'teaching_inset':shot.get('teaching_inset','none'),'direction':direction})
    estimated_seconds=sum(s['planned_generation_duration_seconds'] for s in scenes)
    handoff={'schema':'clAIvier.editorial-handoff.v1','status':'Prepared for review; no provider project, quote, approval or render has been created',
             'provider':'Slopcannon','provider_schema_warning':'This is a human-readable editorial plan, not a claimed Slopcannon production.json API schema.',
             'score_sha256':design['score_binding']['sha256'],'cast_count':25,
             'cast_index':[{'player_id':p['player_id'],'voice_id':p['voice_id'],'score_voice_index':p['score_voice_index'],'instrument':p['instrument'],'identity_color':p['identity_color']} for p in design['players']],
             'master_audio':'24-fugue-spatial-mix.mp3','clear_reference_audio':'24-fugue-orchestral-study.mp3',
             'final_duration_seconds':duration,'scene_count':len(scenes),'resolution_plan':'2K','aspect_ratio':'16:9',
             'timeline_policy':'Time zero is the first written score onset. The final timeline uses the PCM render duration; discard any MP3 encoder padding. Keep the supplied original soundtrack sample-aligned across all generated takes.',
             'representation_limit':'The deterministic rehearsal verifies count, location and note-clock activity. A cinematic generation remains a proposed production and cannot by itself certify exact identities, instruments, fingering or note synchronization.',
             'planning_basis':{'source':'https://api.slop.cc/v1/capabilities','retrieved_date':'2026-10-22',
                'snapshot_file':capability_path.name,'snapshot_sha256':hashlib.sha256(capability_path.read_bytes()).hexdigest(),
                'snapshot_provenance':'Public unauthenticated HTTP GET retrieved by the project on 2026-10-22; no account or project operation.',
                'minimum_scene_seconds':minimum_ms/1000,'maximum_scene_seconds':maximum_ms/1000,'public_credits_per_output_second':rate,
                'generation_duration_rounding':'Each proposed request is rounded upward to a whole millisecond, within the published limits.',
                'maximum_scenes_per_quote':generation['maximumScenesPerQuote'],
                'planned_generated_seconds':round(estimated_seconds,3),'arithmetic_credit_estimate':round(estimated_seconds*rate,2),
                'quote_status':'Not a server-issued quote. No money or credit spending approved. Excludes alternate takes and changes; live quotes govern.'},
             'approval_sequence':['Connect and personally sign in to Slopcannon.',
                 'Present the current exact service rights statement and obtain the human confirmation required by that service before uploading named assets.',
                 'Create the project, obtain an exact quote for the first scene and a current quote for each proposed later scene, then total the production exposure; the capability snapshot permits one scene per quote.',
                 'Obtain the user-approved credit ceiling and exact issued quote approval.',
                 'Render and review the first scene before the rest of the production.',
                 'Check persistent player identity, instrument, location, timing, exact overlays and original soundtrack, then assemble and verify the final film.'],
             'assets_to_prepare':['24-fugue-spatial-mix.mp3','24-fugue-orchestral-study.mp3','concept-keyframe.png','floorplan.png','production-design.json','24-score-cues.json'],
             'scenes':scenes}
    (base/'slopcannon-editorial-handoff.json').write_text(json.dumps(handoff,indent=2)+'\n')
    text=f'''SLOPCANNON EDITORIAL HANDOFF - XXIV / ALL THE THREADS

Prepared concept: exactly 25 recurring instrumentalists in a conceptual
Sagrada Familia-inspired interior, bound to the final 25-part B-minor fugue.
Master soundtrack: {duration:.3f} seconds including the artistic room tail.
Planned scenes: {len(scenes)}; generated material before editing: {estimated_seconds:.3f} seconds.

The public capability response retrieved 22 October 2026 listed 2K output,
5-15 second generations and {rate} Cannon Credits per generated second. Simple
arithmetic therefore gives about {estimated_seconds*rate:.2f} credits for one take of this
plan. THIS IS NOT A QUOTE OR SPENDING APPROVAL. The exact current server
quotes, allowed durations and user-approved ceiling govern any production.
The preserved capability snapshot and its SHA-256 accompany this handoff.
Request durations have been rounded upward to whole milliseconds. One scene
per quote is the published limit, so the batch total requires separate quotes.

Some editorial shots are shorter than the provider's stated five-second
minimum. The plan generates a longer take and retains only the exact scored
segment. Long shots are split into <=15-second generation segments. The
original music is restored on the final master timeline; the note-clock cue
layer remains authoritative across cuts. Cue-clock offsets convert global
score seconds to clip-local seconds, including notes active before a cut.
The master length follows the PCM render; discard MP3 encoder padding.

The JSON file is our editorial handoff schema, not an asserted provider
import format. It contains full scene directions and source/edit timing.
Adapt it to the current documented Slopcannon schema after connection.

No Slopcannon project, upload, generation, provider quote or paid render has
been made. The service requires human rights confirmation before uploads,
review of spending and a first-scene review. The finished rehearsal and
production assets make those decisions concrete.

Official references:
https://slop.cc/for-agents
https://slop.cc/wiki/make-films-with-an-agent
https://api.slop.cc/v1/capabilities
'''
    (base/'slopcannon-handoff.txt').write_text(text)
    print(json.dumps({'scenes':len(scenes),'planned_generation_seconds':estimated_seconds,'credit_estimate_not_quote':estimated_seconds*rate},indent=2))

if __name__=='__main__':main()
