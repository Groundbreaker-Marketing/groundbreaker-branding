import json, sys, os, re, shutil, tempfile
import numpy as np, soundfile as sf

P = '/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-18-podcast-episode/'
WORDS = P + '02_audio/words/170537-synced.json'
EPJ = P + '06_scripts/episode.json'
WRITE = len(sys.argv) > 1 and sys.argv[1] == 'write'

# join number: (left cut time, right cut time), both inside real silences, chosen by listening-by-transcription
CUTS = {
    1: (84.84, 112.38), 2: (115.76, 140.28), 3: (249.02, 295.00), 4: (334.13, 363.25), 5: (483.06, 615.98),
    6: (672.79, 704.82), 7: (750.73, 782.46), 8: (816.06, 842.33), 9: (895.30, 926.46), 10: (1172.35, 1201.32),
    11: (1245.31, 1296.26), 12: (1373.18, 1470.02), 13: (1497.83, 1550.69), 14: (1598.23, 1759.79),
    15: (1798.33, 1823.43), 16: (1864.33, 1908.96), 17: (2070.29, 2118.43), 18: (2176.01, 2189.70),
    19: (2263.47, 2287.04), 20: (2331.04, 2477.01), 21: (2811.67, 2825.85),
}

db = np.load(P + '02_audio/db10ms.npy')
x, sr = sf.read(P + '02_audio/mix_clean_synced.wav')
src = json.load(open(WORDS))
w = src['words']


def sil_around(t, thr=-38):
    i = int(t * 100)
    a = i
    while a > 0 and db[a - 1] < thr:
        a -= 1
    b = i
    while b < len(db) - 1 and db[b + 1] < thr:
        b += 1
    return a / 100, (b + 1) / 100


def lastword(t):
    k = None
    for i, z in enumerate(w):
        if (z['start'] + z['end']) / 2 <= t:
            k = i
        else:
            break
    return k


def norm(s):
    s = re.sub(r'[^a-z0-9]', '', s.lower())
    return {'knot': 'nawt', 'not': 'nawt', 'naur': 'nawt'}.get(s, s)


from faster_whisper import WhisperModel
m = WhisperModel('large-v3-turbo', device='cpu', compute_type='int8', cpu_threads=8)


def asr(seg):
    f = tempfile.NamedTemporaryFile(suffix='.wav', delete=False); f.close()
    sf.write(f.name, seg.astype('float32'), sr)
    s, _ = m.transcribe(f.name, language='en', vad_filter=False, beam_size=1, condition_on_previous_text=False)
    t = ' '.join(z.text.strip() for z in s); os.unlink(f.name); return t


plan = []
for k in sorted(CUTS):
    lc, rc = CUTS[k]
    ls, le = sil_around(lc); rs, re_ = sil_around(rc)
    a0 = lastword(lc); b0 = lastword(rc) + 1
    tail = [norm(z) for z in asr(x[int((lc - 4) * sr):int(lc * sr)]).split()][-3:]
    head = [norm(z) for z in asr(x[int(rc * sr):int((rc + 4) * sr)]).split()][:3]

    def score_a(a):
        seq = [norm(w[i]['word']) for i in range(a - 2, a + 1)]
        return sum(p == q for p, q in zip(seq, tail)), -abs(a - a0)

    def score_b(b):
        seq = [norm(w[i]['word']) for i in range(b, b + 3)]
        return sum(p == q for p, q in zip(seq, head)), -abs(b - b0)

    a = max(range(a0 - 4, a0 + 5), key=score_a)
    b = max(range(b0 - 4, b0 + 5), key=score_b)
    print('J%d L %.2f (sil %.2f-%.2f) a=%d (midpoint a0=%d) asr-tail=%s whisper-tail=%s | R %.2f (sil %.2f-%.2f) b=%d (b0=%d) asr-head=%s whisper-head=%s | dropped %.1fs' % (
        k, lc, ls, le, a, a0, ' '.join(tail), ' '.join(norm(w[i]['word']) for i in range(a - 2, a + 1)),
        rc, rs, re_, b, b0, ' '.join(head), ' '.join(norm(w[i]['word']) for i in range(b, b + 3)), rc - lc), flush=True)
    plan.append((k, a, ls, le, b, rs, re_))

keep = []
start = 0
for k, a, ls, le, b, rs, re_ in plan:
    keep.append([start, a, '170537'])
    start = b
keep.append([start, len(w) - 1, '170537'])
print('keep', keep)
bad = [(keep[i][1], keep[i + 1][0]) for i in range(len(keep) - 1) if keep[i + 1][0] <= keep[i][1]]
print('overlaps', bad)

if WRITE:
    shutil.copy(WORDS, WORDS + '.pre-reedit.bak')
    for k, a, ls, le, b, rs, re_ in plan:
        w[a]['end'] = round(ls + 0.01, 3)
        if a + 1 < len(w):
            w[a + 1]['start'] = round(le - 0.01, 3)
        w[b - 1]['end'] = round(rs + 0.01, 3)
        w[b]['start'] = round(re_ - 0.01, 3)
    json.dump(src, open(WORDS, 'w'))
    d = json.load(open(EPJ))
    d['keep'] = keep
    json.dump(d, open(EPJ, 'w'), indent=1)
    print('written')
