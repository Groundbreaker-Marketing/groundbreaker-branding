"""ashley_sheet.py clip t0 t1 [step]: Ashley's face region at each step, to find where she visibly reacts."""
import glob, os, subprocess, sys
import cv2
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import framing

clip, t0, t1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
step = float(sys.argv[4]) if len(sys.argv) > 4 else 0.75
w, h, n, t, pick = framing.tracks(clip)
cap = cv2.VideoCapture(framing.FOOT + clip + ".MP4")
fps = cap.get(cv2.CAP_PROP_FPS)
tiles = []
tt = t0
while tt < t1:
    i = int(tt * fps)
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    ok, fr = cap.read()
    ox, ey = float(t["ox"][i]), float(t["ey"][i])
    x0 = int(max(0, ox - 150)); y0 = int(max(0, ey - 130))
    tile = cv2.resize(fr[y0:y0 + 260, x0:x0 + 300], (300, 260))
    cv2.putText(tile, f"{tt:.1f}", (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    tiles.append(tile)
    tt += step
cols = 6
rows = [np.hstack(tiles[i:i + cols] + [np.zeros_like(tiles[0])] * (cols - len(tiles[i:i + cols]))) for i in range(0, len(tiles), cols)]
cv2.imwrite(os.path.dirname(framing.P + "/x") + f"/07_notes/contact/_ashley_{clip}_{int(t0)}.jpg", np.vstack(rows))
