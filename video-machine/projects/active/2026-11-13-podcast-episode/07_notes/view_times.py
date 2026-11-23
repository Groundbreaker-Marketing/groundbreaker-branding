"""Face crops at given times, big, with a few neighbouring frames each (+-1 s) to catch blinks.
Run: ./run.sh --no-secrets python <this file> out.jpg t1 t2 ...   (writes into 07_notes/)
"""
import json
import subprocess
import sys
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

P = Path("/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-13-podcast-episode")
out = sys.argv[1]
times = [float(a) for a in sys.argv[2:]]
scan = json.loads((P / "07_notes" / "jason_scan.json").read_text())
font = ImageFont.load_default()
tiles = []
for t in times:
    r = min(scan, key=lambda s: abs(s["t"] - t))
    x, y, w, h = r["box"]
    cx, cy = x + w / 2, y + h / 2
    png = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", str(P / "01_footage" / "zoom-135607.mp4"),
                          "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    im = Image.open(BytesIO(png)).convert("RGB")
    s = 150
    tile = im.crop((int(cx - s), int(cy - s * 0.9), int(cx + s), int(cy + s * 1.1))).resize((480, 640))
    d = ImageDraw.Draw(tile)
    d.rectangle([0, 0, 200, 14], fill=(0, 0, 0))
    d.text((3, 2), f"{t:.1f}s yaw {r['yaw']:+.2f}", fill=(205, 236, 96), font=font)
    tiles.append(tile)
cols = min(len(tiles), 4)
rows = (len(tiles) + cols - 1) // cols
sheet = Image.new("RGB", (cols * 480, rows * 640), (20, 20, 20))
for i, tl in enumerate(tiles):
    sheet.paste(tl, ((i % cols) * 480, (i // cols) * 640))
sheet.save(P / "07_notes" / out, quality=92)
print(out, len(tiles))
