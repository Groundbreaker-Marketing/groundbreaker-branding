import json, os, wave
import numpy as np
# Level (dB, 50 ms windows) around each clip's first and last word on the speaker's own mic, to set
# trim_start / end_pad from the audio instead of Whisper's clock. Prints where speech starts (first
# window above -38 dB counting back from the word) and where it ends (last window above -38 dB before
# 0.3 s of quiet).
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))   # run.sh cds into video-machine
W = json.load(open('02_audio/words/c0031.json'))['words']
labs = json.load(open('07_notes/labels.json'))
S = json.load(open('06_scripts/shorts.json'))['clips']
w = wave.open('07_notes/stereo16k.wav')
a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2).astype(float) / 32768
sr = 16000
def db(ch, t0, t1):
    seg = a[int(t0 * sr):int(t1 * sr), ch]
    return 20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-6)
TH = -38
for c in S:
    f = c['keep'][0][0]
    l = c['keep'][-1][1]
    chf = 0 if labs[f] == 'ASHLEY' else 1
    s, e = W[f]['start'], W[l]['end']
    # onset: walk back from the word start while the speaker's mic is above threshold
    t = s
    while t > s - 0.5 and db(chf, t - 0.05, t) > TH:
        t -= 0.05
    prev_end = W[f - 1]['end'] if f else 0
    pre = ' '.join('%4.0f' % db(chf, s + o, s + o + 0.05) for o in np.arange(-0.4, 0.3, 0.05))
    # offset: walk forward from the word end on Jason's mic until 0.15 s stays below threshold
    t2 = e - 0.1
    while t2 < e + 0.8 and not all(db(1, t2 + k * 0.05, t2 + (k + 1) * 0.05) < TH for k in range(3)):
        t2 += 0.05
    nxt = W[l + 1]['start'] if l + 1 < len(W) else e + 1
    post = ' '.join('%4.0f' % db(1, e + o, e + o + 0.05) for o in np.arange(-0.3, 0.6, 0.05))
    print('%-20s START %-12s whisper %.2f  onset %.2f (%+.2f)  prev word ends %.2f' % (c['id'], W[f]['word'], s, t, t - s, prev_end))
    print('      -0.4..+0.3:', pre)
    print('%-20s END   %-12s whisper %.2f  speech ends %.2f (%+.2f)  next word %s at %.2f' % (c['id'], W[l]['word'], e, t2, t2 - e, W[l + 1]['word'] if l + 1 < len(W) else '-', nxt))
    print('      -0.3..+0.6:', post)
