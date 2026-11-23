"""Scan the Zoom recording for frames of Jason and measure which way his head points.

yaw = (nose x - midpoint of the eyes x) / distance between the eyes, in the picture's own
left-to-right direction. Negative = nose points toward the screen's LEFT (toward the middle of the
thumbnail, since he sits on the right); about 0 = straight at the camera; positive = toward the
screen's right (the outer edge).
Run from the video-machine repo:  ./run.sh --no-secrets python <this file>
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, "/Users/josh/apps/video-machine")
import cv2  # noqa: E402
from podcast.thumbnail import YUNET  # noqa: E402

P = Path("/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-13-podcast-episode")
SRC = P / "01_footage" / "zoom-135607.mp4"
STEP = 2.0                       # seconds between frames
W, H = 1280, 720

det = cv2.FaceDetectorYN.create(str(YUNET), "", (W, H), 0.7, 0.3, 50)
cmd = ["ffmpeg", "-v", "error", "-i", str(SRC), "-vf", f"fps=1/{STEP}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"]
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
out = []
i = 0
while True:
    buf = proc.stdout.read(W * H * 3)
    if len(buf) < W * H * 3:
        break
    t = i * STEP + STEP / 2 if False else i * STEP
    i += 1
    img = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
    if img[:, :300].mean() > 12:     # Ashley's full-frame picture, not Jason's portrait with black bars
        continue
    _, faces = det.detect(img)
    if faces is None or not len(faces):
        continue
    f = max(faces, key=lambda r: r[14])
    x, y, w, h = f[:4]
    re_, le_, nose, ml, mr = [(float(f[4 + 2 * k]), float(f[5 + 2 * k])) for k in range(5)]
    eye_mid = ((re_[0] + le_[0]) / 2, (re_[1] + le_[1]) / 2)
    iod = abs(le_[0] - re_[0]) or 1.0
    yaw = (nose[0] - eye_mid[0]) / iod
    # mouth width against eye distance: a smile or laugh widens it
    mw = abs(mr[0] - ml[0]) / iod
    # corners higher than the mouth center line below the nose = smile (image y grows downward)
    lift = ((ml[1] + mr[1]) / 2 - nose[1]) / iod
    out.append({"t": round(t, 1), "score": round(float(f[14]), 3), "box": [round(float(v), 1) for v in (x, y, w, h)],
                "yaw": round(yaw, 3), "mouth_w": round(mw, 3), "mouth_drop": round(lift, 3),
                "pitch": round((nose[1] - eye_mid[1]) / iod, 3)})
(P / "07_notes" / "jason_scan.json").write_text(json.dumps(out))
print(len(out), "frames with Jason's face of", i)
