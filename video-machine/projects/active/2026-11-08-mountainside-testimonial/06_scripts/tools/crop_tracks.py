"""Face-tracked working crops of the interview clips (one speaker, static tripod, 1080p two-shot).

    crop_tracks.py C0066 [C0067 ...]

Pass 1 finds the speaker's face (right-most face for John, left-most for Max in C0070), every
6th frame, fills gaps and smooths (Gaussian, about 1.5 s). The other person in the frame is the
off-camera interviewer: windows keep her out of the picture.
Pass 2 renders two working files per clip into 04_project-files/crops/:
  <clip>-v.mp4   1080x1920 (head and shoulders, for the 9:16 ads)
  <clip>-h.mp4   1920x1080 (tighter 16:9 for the long cuts)
Both keep the clip's audio and timeline, so source times still match the transcripts.
"""
import json, os, subprocess, sys
import cv2
import numpy as np

P = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial"
YUNET = "/Users/josh/apps/video-machine/kit/skills/horizontal-to-vertical/scripts/yunet.onnx"
OUTD = P + "/04_project-files/crops"
os.makedirs(OUTD, exist_ok=True)
STEP = 6


def gauss_smooth(a, sigma):
    r = int(sigma * 3)
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2)
    k /= k.sum()
    pad = np.pad(a, (r, r), mode="edge")
    return np.convolve(pad, k, mode="valid")


def track(clip, pick):
    cap = cv2.VideoCapture(f"{P}/01_footage/{clip}.MP4")
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    w, h = int(cap.get(3)), int(cap.get(4))
    det = cv2.FaceDetectorYN.create(YUNET, "", (w, h), 0.6, 0.3, 50)
    idx, rows = [], []
    for i in range(n):
        ok = cap.grab()
        if not ok:
            break
        if i % STEP:
            continue
        ok, fr = cap.retrieve()
        _, faces = det.detect(fr)
        if faces is None or not len(faces):
            continue
        faces = sorted(faces, key=lambda f: f[0])
        f = faces[-1] if pick == "right" else faces[0]
        o = faces[0] if pick == "right" else faces[-1]
        other = (float(o[0] + o[2] / 2), float(o[2])) if len(faces) > 1 else (np.nan, np.nan)
        idx.append(i)
        rows.append([f[0] + f[2] / 2, (f[5] + f[7]) / 2, f[3], other[0], other[1]])
    cap.release()
    a = np.array(rows, dtype=float)
    idx = np.array(idx)
    # drop outliers (a wrong face for a moment): far from the rolling median
    for c in (0, 2):
        med = np.array([np.median(a[max(0, j - 8):j + 9, c]) for j in range(len(a))])
        bad = np.abs(a[:, c] - med) > (120 if c == 0 else 40)
        a[bad, c] = np.nan
    full = np.arange(n)
    out = {}
    for c, name in enumerate(["cx", "ey", "fh", "ox", "ow"]):
        col = a[:, c]
        ok = ~np.isnan(col)
        interp = np.interp(full, idx[ok], col[ok])
        out[name] = gauss_smooth(interp, 45 if name in ("cx", "ey", "fh") else 90)
    return w, h, n, out


def windows(t, i, pick, w, h):
    fh = float(t["fh"][i])
    cx, ey = float(t["cx"][i]), float(t["ey"][i])
    ox, ow = float(t["ox"][i]), float(t["ow"][i])
    # 9:16 head and shoulders
    Hv = min(h, fh * 8.6)
    Wv = Hv * 9 / 16
    v = (min(max(0, cx - Wv / 2), w - Wv), min(max(0, ey - 0.30 * Hv), h - Hv), Wv, Hv)
    # 16:9: keep the interviewer out
    if pick == "right":
        lo, hi = ox + 1.7 * ow, w
    else:
        lo, hi = 0, ox - 1.7 * ow
    W = min(fh * 11.5, hi - lo, w)
    Hh = W * 9 / 16
    frac = 0.36 if pick == "right" else 0.64
    x0 = min(max(lo, cx - frac * W), hi - W)
    y0 = min(max(0, ey - 0.38 * Hh), h - Hh)
    return v, (x0, y0, W, Hh)


def render(clip, pick, w, h, n, t):
    src = f"{P}/01_footage/{clip}.MP4"
    procs = []
    for suffix, (ow_, oh_) in (("v", (1080, 1920)), ("h", (1920, 1080))):
        out = f"{OUTD}/{clip}-{suffix}.mp4"
        p = subprocess.Popen(
            ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{ow_}x{oh_}",
             "-r", "30000/1001", "-i", "-", "-i", src, "-map", "0:v", "-map", "1:a:0",
             "-c:v", "h264_videotoolbox", "-b:v", "14M", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
             "-shortest", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
        procs.append((p, (ow_, oh_)))
    cap = cv2.VideoCapture(src)
    for i in range(n):
        ok, fr = cap.read()
        if not ok:
            break
        v, hh = windows(t, i, pick, w, h)
        for (p, (ow_, oh_)), (x0, y0, cw, ch) in zip(procs, (v, hh)):
            s = ow_ / cw
            M = np.array([[s, 0, -x0 * s], [0, s, -y0 * s]], dtype=np.float32)
            img = cv2.warpAffine(fr, M, (ow_, oh_), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
            p.stdin.write(img.tobytes())
    for p, _ in procs:
        p.stdin.close()
        p.wait()
    cap.release()


if __name__ == "__main__":
    for clip in sys.argv[1:]:
        pick = "left" if clip == "C0070" else "right"
        print(clip, "tracking", flush=True)
        w, h, n, t = track(clip, pick)
        json.dump({k: [round(float(x), 1) for x in v[::15]] for k, v in t.items()},
                  open(f"{P}/07_notes/track_{clip}.json", "w"))
        print(clip, "rendering", n, "frames", flush=True)
        render(clip, pick, w, h, n, t)
        print(clip, "done", flush=True)
