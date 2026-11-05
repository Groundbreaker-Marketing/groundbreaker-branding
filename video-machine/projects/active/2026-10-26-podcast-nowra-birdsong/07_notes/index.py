import json, wave, numpy as np
d = json.load(open('02_audio/words/c0030.json'))
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
    '== take c0030 %d words (labels: louder wireless mic per word; left=Jason, right=Ashley)' % len(W) + ''.join(txt))
json.dump(labs, open('07_notes/labels.json', 'w'))
