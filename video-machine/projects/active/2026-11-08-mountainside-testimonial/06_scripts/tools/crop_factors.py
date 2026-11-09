import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import framing
for clip, ranges in (("C0066", [(28, 53), (209, 250), (412, 445)]), ("C0067", [(74, 83), (88, 108), (141, 160)]), ("C0068", [(61, 89)]), ("C0070", [(10, 25)])):
    w, h, n, t, pick = framing.tracks(clip)
    ws = []
    for a, b in ranges:
        for i in range(int(a * 29.97), int(b * 29.97), 15):
            _, _, cw, ch = framing.close_window(t, i, pick, w, h)
            ws.append(cw)
    print(clip, "crop width px min/median/max", round(min(ws)), round(float(np.median(ws))), round(max(ws)), "zoom", round(1920 / max(ws), 1), "to", round(1920 / min(ws), 1))
