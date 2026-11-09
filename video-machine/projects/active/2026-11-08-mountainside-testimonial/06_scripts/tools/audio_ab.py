"""Three A/B samples of the same 30 s of John (C0066 28 to 58 s) -> 05_renders/review/audio-ab/.

  1  round 1 as delivered: left mic as recorded on the left ear only, loudness fix only
  2  channel fix + voice chain (his mic in both ears; EQ, de-esser, compression, loudnorm)
  3  channel fix + enhancement + voice chain (Resemble Enhance if installed, else the harmonic exciter)
Writes mp4s with the sample's picture (the original two-shot) so they play anywhere, and a JSON of measurements.
"""
import json, os, subprocess, sys
sys.path.insert(0, "/Users/josh/apps/video-machine")
import dialogue
from dialogue import chain, twomic

P = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial/"
SRC = "/Users/josh/inbox/2026-10-28-mountainside-er/C0066.MP4"
OUT = P + "05_renders/review/audio-ab/"
WORK = P + "10_work/audio-ab/"
os.makedirs(OUT, exist_ok=True)
os.makedirs(WORK, exist_ok=True)
T0, DUR = 28.3, 30.0


def mux(wav, mp4):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(T0), "-t", str(DUR), "-i", SRC, "-i", wav,
                    "-map", "0:v", "-map", "1:a", "-vf", "crop=iw*0.5:ih*0.5:iw*0.45:0,scale=960:540",
                    "-c:v", "libx264", "-crf", "22", "-preset", "fast", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", mp4], check=True)


res = {}
# 1: round 1 as delivered. John's mic is the LEFT channel; the stereo file played him in the left ear only.
a1 = twomic.load(SRC, T0, DUR)
raw = WORK + "r1_raw.wav"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(T0), "-t", str(DUR), "-i", SRC, "-vn", "-ac", "2", "-ar", "48000", raw], check=True)
r1 = WORK + "r1.wav"
res["1_round1"] = chain.normalize(raw, r1, lufs=-16.0)
# round 1 measured per channel
for ch, name in ((0, "left"), (1, "right")):
    m = chain.measure(a1[:, ch])
    res.setdefault("1_round1_channels", {})[name] = {"level_db": m["level_db"], "bands": m["bands"], "hf_gap_db": m["hf_gap_db"]}
res["1_round1"]["bands"] = chain.measure(a1[:, 0])
mux(r1, OUT + "1-round1-as-delivered.mp4")
# 2 and 3
w2, w3 = WORK + "s2.wav", WORK + "s3.wav"
res["2_chain"] = dialogue.process(SRC, w2, who="L", lufs=-16.0, start=T0, dur=DUR)
mux(w2, OUT + "2-channel-fix-plus-voice-chain.mp4")
res["3_enhance_chain"] = dialogue.process(SRC, w3, who="L", lufs=-16.0, enhance=True, start=T0, dur=DUR)
mux(w3, OUT + "3-channel-fix-plus-enhancement-plus-voice-chain.mp4")
json.dump(res, open(P + "07_notes/audio_ab.json", "w"), indent=2, default=float)
for k, v in res.items():
    print(k, json.dumps(v, default=float)[:700])
