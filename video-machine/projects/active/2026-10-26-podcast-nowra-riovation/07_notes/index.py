import json, os, sys, wave, numpy as np
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# usage (from the project folder): python index.py <left-label> <right-label>
LEFT, RIGHT = (sys.argv[1], sys.argv[2]) if len(sys.argv) > 2 else ('GUEST', 'ASHLEY')
d = json.load(open('02_audio/words/c0021.json'))
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
    lab = LEFT if L > R else RIGHT
    labs.append(lab)
    if lab != cur:
        txt.append('\n\n%s: [%d@%d] ' % (lab, i, x['start']))
        cur = lab
    elif i % 10 == 0 or (i and x['start'] - W[i - 1]['end'] > 1.0):
        txt.append('[%d@%d] ' % (i, x['start']))
    txt.append(x['word'] + ' ')
open('07_notes/transcript-indexed.txt', 'w').write(
    '== take c0021 %d words (labels: louder wireless mic per word; left=%s, right=%s)' % (len(W), LEFT, RIGHT) + ''.join(txt))
json.dump(labs, open('07_notes/labels.json', 'w'))
print(len(W), 'words;', labs.count(LEFT), LEFT, labs.count(RIGHT), RIGHT)
# first 12 s per channel, to see whose mic is which
for t in (0, 4, 8):
    seg = a[t * sr:(t + 4) * sr]
    print('t=%d-%d  L rms %.0f  R rms %.0f' % (t, t + 4, np.sqrt((seg[:, 0] ** 2).mean()), np.sqrt((seg[:, 1] ** 2).mean())))
