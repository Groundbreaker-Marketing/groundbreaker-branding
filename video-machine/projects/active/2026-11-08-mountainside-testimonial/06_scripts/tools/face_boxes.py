"""Find the on-camera speaker's face in each interview clip (static camera): median box + sway.

John is the right-most face in C0066 to C0069; Max is the left-most face in C0070 (the other
person in frame is the interviewer). Writes 07_notes/face_boxes.json.
"""
import json, sys
import cv2
import numpy as np

P = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial"
YUNET = "/Users/josh/apps/video-machine/kit/skills/horizontal-to-vertical/scripts/yunet.onnx"
out = {}
for clip, pick in (("C0066", "right"), ("C0067", "right"), ("C0068", "right"), ("C0069", "right"), ("C0070", "left")):
    cap = cv2.VideoCapture(f"{P}/01_footage/{clip}.MP4")
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    w, h = int(cap.get(3)), int(cap.get(4))
    det = cv2.FaceDetectorYN.create(YUNET, "", (w, h), 0.6, 0.3, 50)
    boxes = []
    for i in range(60):
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(n * (i + 0.5) / 60))
        ok, fr = cap.read()
        if not ok:
            continue
        _, faces = det.detect(fr)
        if faces is None or not len(faces):
            continue
        faces = sorted(faces, key=lambda f: f[0])
        f = faces[-1] if pick == "right" else faces[0]
        if len(faces) >= 2 or True:
            boxes.append([float(f[0]), float(f[1]), float(f[2]), float(f[3]),
                          float((f[5] + f[7]) / 2), float(len(faces))])
    a = np.array(boxes)
    cx = a[:, 0] + a[:, 2] / 2
    out[clip] = {"frame": [w, h], "n": len(boxes), "cx": float(np.median(cx)), "cx_min": float(cx.min()),
                 "cx_max": float(cx.max()), "eye_y": float(np.median(a[:, 4])), "face_w": float(np.median(a[:, 2])),
                 "face_h": float(np.median(a[:, 3])), "faces_per_frame": float(np.median(a[:, 5]))}
    print(clip, out[clip], flush=True)
json.dump(out, open(P + "/07_notes/face_boxes.json", "w"), indent=2)
