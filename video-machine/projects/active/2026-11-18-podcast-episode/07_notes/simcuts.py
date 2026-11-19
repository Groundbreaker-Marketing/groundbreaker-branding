import json, sys
from pathlib import Path
sys.path.insert(0, '/Users/josh/apps/video-machine')
from podcast import episode as E
from podcast.cutpoints import decode_audio, cut_points, speech_ref

project = Path('/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-18-podcast-episode')
recipe = json.load(open(project / '06_scripts/episode.json'))
takes = E.load_takes(project, recipe)
audio = {k: decode_audio(project / t['source']) for k, t in takes.items()}
sel, cut = E.selection(takes, recipe, audio)
p = {**E.PAUSE, **recipe.get('pause', {})}
segs = E.segments(takes, sel, **p)
refs = {k: speech_ref(v) for k, v in audio.items()}
for n, sg in enumerate(segs):
    W = takes[sg['take']]['w']
    kept_prev = n > 0 and segs[n - 1]['words'][-1]['i'] == sg['words'][0]['i'] - 1
    kept_next = n + 1 < len(segs) and segs[n + 1]['words'][0]['i'] == sg['words'][-1]['i'] + 1
    cut_points(audio[sg['take']], sg, W, p['pre'], p['post'], refs[sg['take']],
               removed_before=n > 0 and not kept_prev, removed_after=n + 1 < len(segs) and not kept_next)
    print('seg%d words %d-%d  start %.2f (in_db %.1f)  end %.2f (out_db %.1f)  first=%s last=%s' % (
        n, sg['words'][0]['i'], sg['words'][-1]['i'], sg['s'], sg['in_db'], sg['e'], sg['out_db'],
        sg['words'][0]['word'], sg['words'][-1]['word']))
