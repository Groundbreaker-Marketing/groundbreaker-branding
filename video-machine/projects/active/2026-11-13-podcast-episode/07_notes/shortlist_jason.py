"""Shortlist Jason frames: head pointing straight or toward the screen's left, wide mouth, spread out.
Writes 07_notes/jason_shortlist.jpg (face crops labeled with time and yaw) and prints the list.
Run: ./run.sh --no-secrets python <this file>  [min_gap_seconds] [count] [yaw_lo] [yaw_hi]
"""
import json
import subprocess
import sys
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

P = Path("/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-13-podcast-episode")
gap = float(sys.argv[1]) if len(sys.argv) > 1 else 45
count = int(sys.argv[2]) if len(sys.argv) > 2 else 40
lo = float(sys.argv[3]) if len(sys.argv) > 3 else -0.35
hi = float(sys.argv[4]) if len(sys.argv) > 4 else 0.04
scan = json.loads((P / "07_notes" / "jason_scan.json").read_text())
ok = [r for r in scan if lo <= r["yaw"] <= hi and r["score"] >= 0.85 and r["box"][3] >= 190 and abs(r["pitch"] - 0.65) < 0.25]
ok.sort(key=lambda r: -r["mouth_w"])
picked = []
for r in ok:
    if all(abs(r["t"] - p["t"]) >= gap for p in picked):
        picked.append(r)
    if len(picked) >= count:
        break
picked.sort(key=lambda r: r["t"])
tiles = []
font = ImageFont.load_default()
for r in picked:
    png = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(r["t"]), "-i", str(P / "01_footage" / "zoom-135607.mp4"),
                          "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    im = Image.open(BytesIO(png)).convert("RGB")
    x, y, w, h = r["box"]
    cx, cy = x + w / 2, y + h / 2
    s = 190
    tile = im.crop((int(cx - s), int(cy - s), int(cx + s), int(cy + s))).resize((300, 300))
    d = ImageDraw.Draw(tile)
    d.rectangle([0, 0, 190, 16], fill=(0, 0, 0))
    d.text((3, 2), f"{r['t']:.0f}s yaw {r['yaw']:+.2f} mw {r['mouth_w']:.2f}", fill=(205, 236, 96), font=font)
    tiles.append(tile)
cols = 6
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 300, rows * 300), (20, 20, 20))
for i, t in enumerate(tiles):
    sheet.paste(t, ((i % cols) * 300, (i // cols) * 300))
sheet.save(P / "07_notes" / "jason_shortlist.jpg", quality=90)
print(len(picked), [r["t"] for r in picked])
