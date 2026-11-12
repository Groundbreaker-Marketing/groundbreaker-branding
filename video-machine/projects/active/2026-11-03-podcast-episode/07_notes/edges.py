import json, subprocess, sys
import numpy as np
P = sys.argv[1]
w = json.load(open(P + '/02_audio/words/160057-synced.json'))['words']
S = json.load(open(P + '/06_scripts/shorts.json'))


def load(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 's16le', '-ac', '1', '-ar', '16000', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0


tr = {'J': load(P + '/01_footage/zoom-people/160057-iphone-2.m4a'),
      'A': load(P + '/01_footage/zoom-people/160057-ashley-christian.m4a')}


def db(x, t0, t1):
    a = int(max(t0, 0) * 16000)
    b = int(t1 * 16000)
    seg = x[a:b]
    if len(seg) == 0:
        return -99
    return 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9)


def prof(x, t, off=0.055):
    t += off
    return ' '.join('%4.0f' % db(x, t + k * 0.1, t + k * 0.1 + 0.1) for k in range(-4, 5))


for c in S['clips']:
    print(c['id'])
    for n, (a, b) in enumerate(c['keep']):
        s = w[a]['start']
        e = w[b]['end']
        print('  range %d  start %s %.2f  J[-0.4..+0.4]: %s' % (n, w[a]['word'], s, prof(tr['J'], s)))
        print('            end   %s %.2f  J[-0.4..+0.4]: %s   A: %s' % (w[b]['word'], e, prof(tr['J'], e), prof(tr['A'], e)))
