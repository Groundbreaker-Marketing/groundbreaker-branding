import json, wave
import numpy as np
W = json.load(open('02_audio/words/c0030.json'))['words']
S = json.load(open('06_scripts/shorts.json'))['clips']
w = wave.open('07_notes/stereo16k.wav')
a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2).astype(float)
sr = 16000
R = a[:, 1]  # Jason's mic
def db(t0, t1):
    seg = R[int(t0 * sr):int(t1 * sr)]
    return 20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-3)
for c in S:
    f = c['keep'][0][0]
    l = c['keep'][-1][1]
    s = W[f]['start']
    e = W[l]['end']
    pre = ' '.join('%4.0f' % db(s + o, s + o + 0.05) for o in np.arange(-0.4, 0.3, 0.05))
    post = ' '.join('%4.0f' % db(e + o, e + o + 0.05) for o in np.arange(-0.3, 0.6, 0.05))
    print(c['id'], 'START', W[f]['word'], round(s, 2))
    print('   -0.4..+0.25 by .05:', pre)
    print(c['id'], 'END', W[l]['word'], round(e, 2))
    print('   -0.3..+0.55 by .05:', post)
