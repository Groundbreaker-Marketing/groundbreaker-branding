import os, sys, wave
import numpy as np
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
# usage: lvl.py <channel 0=Ashley 1=guest> <start s> <end s>   (50 ms windows, dB)
ch, t0, t1 = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
w = wave.open('07_notes/stereo16k.wav')
a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, 2).astype(float) / 32768
sr = 16000
t = t0
out = []
while t < t1:
    seg = a[int(t * sr):int((t + 0.05) * sr), ch]
    out.append('%.2f:%d' % (t, 20 * np.log10(np.sqrt((seg ** 2).mean()) + 1e-6)))
    t += 0.05
print(' '.join(out))
