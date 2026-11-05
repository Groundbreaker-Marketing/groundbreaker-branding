import json, os, wave, numpy as np
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))   # run.sh cds into video-machine
# Indexed transcript with a speaker label per word: the louder wireless mic wins
# (LEFT channel = Ashley, RIGHT channel = Jason, same as Part 1).
d = json.load(open('02_audio/words/c0031.json'))
W = d['words']
w = wave.open('07_notes/stereo16k.wav')
n = w.getnframes()
a = np.frombuffer(w.readframes(n), dtype=np.int16).reshape(-1, 2).astype(float)
sr = 16000
txt = []
cur = None
labs = []
for i, x in enumerate(W):
    s = int(x['start'] * sr)
    e = max(int(x['end'] * sr), s + 160)
    seg = a[s:e]
    L = np.sqrt((seg[:, 0] ** 2).mean() + 1e-9)
    R = np.sqrt((seg[:, 1] ** 2).mean() + 1e-9)
    lab = 'ASHLEY' if L > R else 'JASON'
    labs.append(lab)
    if lab != cur:
        txt.append('\n\n%s: [%d@%d] ' % (lab, i, x['start']))
        cur = lab
    elif i % 10 == 0 or (i and x['start'] - W[i - 1]['end'] > 1.0):
        txt.append('[%d@%d] ' % (i, x['start']))
    txt.append(x['word'] + ' ')
open('07_notes/transcript-indexed.txt', 'w').write(
    '== take c0031 %d words (labels: louder wireless mic per word; left=Ashley, right=Jason)' % len(W) + ''.join(txt))
json.dump(labs, open('07_notes/labels.json', 'w'))
