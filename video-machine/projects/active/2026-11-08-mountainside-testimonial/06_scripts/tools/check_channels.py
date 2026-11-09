"""Every deliverable: left and right must carry the same voice (dual mono). Prints L, R level and the L-R residual."""
import glob, sys
sys.path.insert(0, "/Users/josh/apps/video-machine")
import numpy as np
from dialogue import twomic

R = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial/05_renders/review/"
bad = 0
for f in sorted(glob.glob(R + "*/*.mp4") + glob.glob(R + "ads/*/*.mp4")):
    if "audio-ab" in f:
        continue
    a = twomic.load(f)
    L, Rr = a[:, 0], a[:, 1]
    rms = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)   # noqa: E731
    resid = rms(L - Rr) - rms(L)
    ok = abs(rms(L) - rms(Rr)) < 0.5 and resid < -25
    bad += not ok
    print(("OK  " if ok else "BAD ") + f.replace(R, "")[:90], f"L {rms(L):.1f} R {rms(Rr):.1f} dB, L-R residual {resid:.0f} dB relative")
print("bad:", bad)
