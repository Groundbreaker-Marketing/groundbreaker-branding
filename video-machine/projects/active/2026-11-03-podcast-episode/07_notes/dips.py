import json, subprocess, sys
import numpy as np
P = sys.argv[1]
w = json.load(open(P + '/02_audio/words/160057-synced.json'))['words']
S = json.load(open(P + '/06_scripts/shorts.json'))


def load(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 's16le', '-ac', '1', '-ar', '16000', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0


J = load(P + '/01_footage/zoom-people/160057-iphone-2.m4a')
OFF = 0.055
F = 160  # 10 ms
THR = -42.0


def frames(t0, t1):
    a = int(max(t0 + OFF, 0) * 16000)
    b = int((t1 + OFF) * 16000)
    seg = J[a:b]
    n = len(seg) // F
    r = np.sqrt(np.mean(seg[:n * F].reshape(n, F) ** 2, axis=1)) + 1e-9
    return 20 * np.log10(r)


def start_gap(s):
    # nearest silence at or before the word start (within 0.35 s): return the offset to move the start to
    db = frames(s - 0.35, s + 0.05)
    t = s - 0.35
    idx = [i for i, v in enumerate(db) if v < THR]
    if not idx:
        return None
    i = idx[-1]
    return round(i * 0.01 - 0.35 + 0.01, 2)


def end_gap(e):
    db = frames(e - 0.05, e + 0.45)
    idx = [i for i, v in enumerate(db) if v < THR]
    if not idx:
        return None
    return round(idx[0] * 0.01 - 0.05, 2)


for c in S['clips']:
    a, b = c['keep'][0][0], c['keep'][-1][1]
    s = w[a]['start']
    e = w[b]['end']
    print('%-18s start %-8s gap@%s   end %-9s gap@%s' % (c['id'], w[a]['word'], start_gap(s), w[b]['word'], end_gap(e)))
