"""Numbers for the Round 2 section of REVIEW.md."""
import json, subprocess, sys
sys.path.insert(0, "/Users/josh/apps/video-machine")
import numpy as np
from dialogue import chain, twomic

P = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial/"
ab = json.load(open(P + "07_notes/audio_ab.json"))
print("A/B sample, 30 s of John (C0066 28.3 to 58.3 s):")
r1 = ab["1_round1"]["bands"]
print("  1 round 1 :", r1["bands"], "gap", r1["hf_gap_db"], "| LUFS", ab["1_round1"]["after"]["lufs"], "LRA", ab["1_round1"]["after"]["lra"], "TP", ab["1_round1"]["after"]["true_peak_db"])
for k, n in (("2_chain", "2 chain    "), ("3_enhance_chain", "3 enhance  ")):
    d = ab[k]
    print(" ", n, ":", d["after"]["bands"], "gap", d["after"]["hf_gap_db"], "| LUFS", d["loudness"]["after"]["lufs"], "LRA", d["loudness"]["after"]["lra"], "TP", d["loudness"]["after"]["true_peak_db"])
print("channels as recorded (round 1 file), same 30 s:", ab["1_round1_channels"])
a = twomic.load("/Users/josh/inbox/2026-10-28-mountainside-er/C0066.MP4")
print("whole C0066 as recorded: left", chain.measure(a[:, 0])["level_db"], "dB, right", chain.measure(a[:, 1])["level_db"], "dB")
v = P + "05_renders/review/vsl/mountainside-er-john-vandervalk-video-sales-letter-16x9.mp4"
l = chain.loudness(v)
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", P + "10_work/vsl/dialog.wav", "-f", "f32le", "-ac", "1", "-ar", "48000", "-"], capture_output=True).stdout
m = chain.measure(np.frombuffer(raw, dtype=np.float32))
print("VSL final (with music):", l)
print("VSL dialogue track:", m["bands"], "gap", m["hf_gap_db"])
st = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=channels", "-of", "csv=p=0", v], capture_output=True, text=True).stdout
print("VSL audio channels:", st.strip())
