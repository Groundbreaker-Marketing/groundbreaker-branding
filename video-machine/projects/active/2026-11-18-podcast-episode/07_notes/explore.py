import json, sys, os, tempfile
import numpy as np, soundfile as sf

P = '/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-18-podcast-episode/'
x, sr = sf.read(P + '02_audio/mix_clean_synced.wav')
w = json.load(open(P + '02_audio/words/170537-synced.json'))['words']
db = np.load(P + '02_audio/db10ms.npy')
from faster_whisper import WhisperModel
m = WhisperModel('large-v3-turbo', device='cpu', compute_type='int8', cpu_threads=8)


def runs(t0, t1, thr=-38, minf=5):
    a = max(0, int(t0 * 100)); b = min(len(db), int(t1 * 100)); out = []; i = a
    while i < b:
        if db[i] < thr:
            j = i
            while j < b and db[j] < thr:
                j += 1
            if j - i >= minf:
                out.append((i / 100, j / 100, float(db[i:j].mean())))
            i = j
        else:
            i += 1
    return out


def asr(seg):
    f = tempfile.NamedTemporaryFile(suffix='.wav', delete=False); f.close()
    sf.write(f.name, seg.astype('float32'), sr)
    s, _ = m.transcribe(f.name, language='en', vad_filter=False, beam_size=1, condition_on_previous_text=False)
    t = ' '.join(z.text.strip() for z in s); os.unlink(f.name); return t


def lastword(t):
    k = None
    for i, z in enumerate(w):
        if (z['start'] + z['end']) / 2 <= t:
            k = i
        else:
            break
    return k


def show_left(t0, t1):
    for r in runs(t0, t1):
        c = r[0] + min(0.12, (r[1] - r[0]) * 0.4)
        print('  L cut %.2f (sil %.2f-%.2f %.0fdB, after w%d): ...%s' % (c, r[0], r[1], r[2], lastword(c), ' '.join(asr(x[int((c - 5) * sr):int(c * sr)]).split()[-8:])), flush=True)


def show_right(t0, t1):
    for r in runs(t0, t1):
        c = r[1] - min(0.12, (r[1] - r[0]) * 0.4)
        print('  R cut %.2f (sil %.2f-%.2f %.0fdB, before w%d): %s...' % (c, r[0], r[1], r[2], lastword(c) + 1, ' '.join(asr(x[int(c * sr):int((c + 5) * sr)]).split()[:9])), flush=True)


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'drops':
        drops = json.loads(sys.argv[2])
        for k, (s, e) in drops:
            a, b = s - 1, e + 1
            print('J%d plan keep..%d: %s || resume %d: %s' % (k, a, ' '.join(w[i]['word'].strip() for i in range(a - 3, a + 1)), b, ' '.join(w[i]['word'].strip() for i in range(b, b + 4))), flush=True)
            show_left(w[a]['end'] - 1.5, w[a]['end'] + 1.2)
            show_right(w[b]['start'] - 1.2, w[b]['start'] + 1.5)
    elif mode == 'L':
        show_left(float(sys.argv[2]), float(sys.argv[3]))
    elif mode == 'R':
        show_right(float(sys.argv[2]), float(sys.argv[3]))
