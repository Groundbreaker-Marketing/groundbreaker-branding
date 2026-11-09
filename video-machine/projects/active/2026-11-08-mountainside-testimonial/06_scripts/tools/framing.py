"""Round 2 framing: John (or Max) centered in a medium close-up, and a wide two-shot with Ashley.

Per frame, from the speaker's tracked face (crop_tracks.track): smoothed center, eyeline and face size.

  close  window centered on the speaker, face about 28% of the picture height, the interviewer kept out
         of frame. Rendered at 640x360 (the size podcast.upscale's model expects), then AI-upscaled.
  wide   window centered between the two people, both fully in frame. Rendered at 1920x1080 directly.

    framing.py <jobs.json>     jobs: [{"id", "clip", "t_in", "t_out", "kind": "close"|"wide"}] -> out dir
"""
import json, os, subprocess, sys
import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import crop_tracks as ct

P = ct.P
FOOT = P + "/01_footage/"
CACHE = P + "/10_work/tracks/"
os.makedirs(CACHE, exist_ok=True)
FACE_FRAC = 0.28           # face height / picture height in the close-up
EYE_FRAC = 0.36            # eyeline from the top of the close-up


def tracks(clip):
    f = CACHE + clip + ".npz"
    pick = "left" if clip == "C0070" else "right"
    if os.path.exists(f):
        z = np.load(f)
        return int(z["w"]), int(z["h"]), int(z["n"]), {k: z[k] for k in ("cx", "ey", "fh", "ox", "ow")}, pick
    w, h, n, t = ct.track(clip, pick)
    np.savez(f, w=w, h=h, n=n, **t)
    return w, h, n, t, pick


def close_window(t, i, pick, w, h):
    fh, cx, ey = float(t["fh"][i]), float(t["cx"][i]), float(t["ey"][i])
    ox, ow = float(t["ox"][i]), float(t["ow"][i])
    H = fh / FACE_FRAC
    W = H * 16 / 9
    # keep the interviewer's body out: her edge is about 1.2 face widths from her face center
    if pick == "right":
        room = cx - (ox + 1.55 * ow)
    else:
        room = (ox - 1.55 * ow) - cx
    W = min(W, 2 * room)
    W = max(W, 400.0)
    H = W * 9 / 16
    x0 = min(max(0, cx - W / 2), w - W)
    y0 = min(max(0, ey - EYE_FRAC * H), h - H)
    return x0, y0, W, H


def wide_window(t, i, pick, w, h):
    cx, ey = float(t["cx"][i]), float(t["ey"][i])
    ox, ow = float(t["ox"][i]), float(t["ow"][i])
    mid = (cx + ox) / 2
    W = float(np.clip(abs(cx - ox) * 3.4, 1100, 1700))
    H = W * 9 / 16
    x0 = min(max(0, mid - W / 2), w - W)
    y0 = min(max(0, ey - 0.34 * H), h - H)
    return x0, y0, W, H


def render(job, outdir):
    clip, kind = job["clip"], job["kind"]
    out = f"{outdir}/{job['id']}.mp4"
    if os.path.exists(out):
        return out
    w, h, n, t, pick = tracks(clip)
    cap = cv2.VideoCapture(f"{FOOT}{clip}.MP4")
    fps = cap.get(cv2.CAP_PROP_FPS)
    f0, f1 = int(round(job["t_in"] * fps)), int(round(job["t_out"] * fps))
    cap.set(cv2.CAP_PROP_POS_FRAMES, f0)
    ow_, oh_ = (640, 360) if kind == "close" else (1920, 1080)
    p = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{ow_}x{oh_}",
                          "-r", "30", "-i", "-", "-c:v", "libx264", "-preset", "fast", "-crf", "10", "-pix_fmt", "yuv420p", out],
                         stdin=subprocess.PIPE)
    for i in range(f0, min(f1, n)):
        ok, fr = cap.read()
        if not ok:
            break
        x0, y0, cw, ch = (close_window if kind == "close" else wide_window)(t, i, pick, w, h)
        s = ow_ / cw
        M = np.array([[s, 0, -x0 * s], [0, s, -y0 * s]], dtype=np.float32)
        img = cv2.warpAffine(fr, M, (ow_, oh_), flags=cv2.INTER_CUBIC if s >= 1 else cv2.INTER_AREA,
                             borderMode=cv2.BORDER_REPLICATE)
        p.stdin.write(img.tobytes())
    p.stdin.close()
    p.wait()
    cap.release()
    return out


if __name__ == "__main__":
    jobs = json.load(open(sys.argv[1]))
    outdir = sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    for j in jobs:
        print("render", j["id"], flush=True)
        render(j, outdir)
