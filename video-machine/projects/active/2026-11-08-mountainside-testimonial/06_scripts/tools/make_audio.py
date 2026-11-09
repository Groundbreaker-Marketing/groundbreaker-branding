"""Round 2 dialogue audio: per interview clip, the speaker's own mic in both ears, through the voice chain.

  <clip>-L.wav  the left mic (John; Max in C0070)       <clip>-R.wav  the right mic (Ashley)
Written to 04_project-files/audio/ with the camera file's timeline (same length), -16 LUFS integrated
over the whole clip. Also prints who-speaks-when checks against the transcript.
"""
import json, os, sys
sys.path.insert(0, "/Users/josh/apps/video-machine")
import numpy as np
import dialogue
from dialogue import twomic

P = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial/"
IN = "/Users/josh/inbox/2026-10-28-mountainside-er/"
OUT = P + "04_project-files/audio/"
os.makedirs(OUT, exist_ok=True)
clips = sys.argv[1:] or ["C0066", "C0067", "C0068", "C0069", "C0070"]
rep = {}
for c in clips:
    for who in ("L", "R"):
        dst = f"{OUT}{c}-{who}.wav"
        if os.path.exists(dst):
            continue
        info = dialogue.process(IN + c + ".MP4", dst, who=who, lufs=-16.0)
        rep[f"{c}-{who}"] = {"profile": info["profile"], "loudness": info["loudness"], "gap_before": info["before"]["hf_gap_db"],
                             "gap_after": info["after"]["hf_gap_db"]}
        print(c, who, json.dumps(rep[f"{c}-{who}"], default=float), flush=True)
# who-speaks check on C0070: Max talks 10.5 to 24.4 s
a = twomic.load(IN + "C0070.MP4")
lab, r = twomic.speaker_labels(a[:, 0], a[:, 1])
print("C0070 split", r, "label at 10.5 to 24.4 s (0 = left mic):", np.bincount(lab[int(10.5 / 0.05):int(24.4 / 0.05)], minlength=2))
json.dump(rep, open(P + "07_notes/audio_round2.json", "w"), indent=2, default=float)
