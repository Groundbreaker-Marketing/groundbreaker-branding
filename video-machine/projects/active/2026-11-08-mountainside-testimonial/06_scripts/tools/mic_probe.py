"""mic_probe.py <clip>: per-channel level, crosstalk and band energy on a two-mic clip."""
import subprocess, sys
import numpy as np

clip = sys.argv[1]
SR = 48000
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f"/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial/01_footage/{clip}.MP4",
                      "-vn", "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout
a = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2)
L, R = a[:, 0], a[:, 1]
W = int(0.1 * SR)
n = len(L) // W


def db(x):
    return 20 * np.log10(np.sqrt(np.mean(x ** 2, axis=-1)) + 1e-9)


l = db(L[:n * W].reshape(n, W))
r = db(R[:n * W].reshape(n, W))
d = l - r
print(f"{clip} {len(L) / SR:.0f}s  L median {np.median(l):.1f} dB  R median {np.median(r):.1f} dB")
print("L-R difference percentiles 5/25/50/75/95:", np.percentile(d, [5, 25, 50, 75, 95]).round(1))
hist, edges = np.histogram(d, bins=np.arange(-30, 36, 3))
for h, e in zip(hist, edges):
    print(f"  {e:+4.0f} dB {'#' * int(60 * h / hist.max())}")
# band energy of loud L windows
loud = np.where(l > np.percentile(l, 70))[0]
seg = np.concatenate([L[i * W:(i + 1) * W] for i in loud[:600]])
sp = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) ** 2
fr = np.fft.rfftfreq(len(seg), 1 / SR)
for lo, hi in ((60, 200), (200, 500), (500, 1000), (1000, 2000), (2000, 4000), (4000, 8000), (8000, 16000)):
    m = (fr >= lo) & (fr < hi)
    print(f"  L {lo:>5}-{hi:<5} Hz  {10 * np.log10(sp[m].sum() + 1e-12) - 10 * np.log10(m.sum()):6.1f} dB/bin")
