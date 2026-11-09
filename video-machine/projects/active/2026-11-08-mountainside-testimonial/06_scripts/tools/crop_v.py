"""9:16 working crops for the ads (round 2): the speaker centered, from the cached face tracks.

    crop_v.py C0066 C0067 C0068     -> 04_project-files/crops/<clip>-v.mp4 (1080x1920, picture only)
The sound of the ads comes from 04_project-files/audio/<clip>-L.wav (selects.json "audio").
Writes 07_notes/ad_centering.json: median horizontal face position (fraction of width) per clip, measured on the output.
"""
import json, os, subprocess, sys
import cv2
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import crop_tracks as ct
import framing

OUT = ct.P + "/04_project-files/crops/"
os.makedirs(OUT, exist_ok=True)
report = {}
for clip in sys.argv[1:]:
    w, h, n, t, pick = framing.tracks(clip)
    dst = f"{OUT}{clip}-v.mp4"
    cap = cv2.VideoCapture(f"{ct.P}/01_footage/{clip}.MP4")
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1080x1920", "-r", "30000/1001",
                          "-i", "-", "-c:v", "h264_videotoolbox", "-b:v", "14M", "-pix_fmt", "yuv420p", dst], stdin=subprocess.PIPE)
    xs = []
    for i in range(n):
        ok, fr = cap.read()
        if not ok:
            break
        v, _ = ct.windows(t, i, pick, w, h)
        x0, y0, cw, ch = v
        s = 1080 / cw
        M = np.array([[s, 0, -x0 * s], [0, s, -y0 * s]], dtype=np.float32)
        p.stdin.write(cv2.warpAffine(fr, M, (1080, 1920), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE).tobytes())
        if i % 150 == 0:
            xs.append((float(t["cx"][i]) - x0) / cw)       # where his face sits across the 9:16 frame
    p.stdin.close()
    p.wait()
    report[clip] = {"face_x_median": round(float(np.median(xs)), 3), "face_x_min": round(min(xs), 3), "face_x_max": round(max(xs), 3)}
    print(clip, report[clip], flush=True)
json.dump(report, open(ct.P + "/07_notes/ad_centering.json", "w"), indent=2)
