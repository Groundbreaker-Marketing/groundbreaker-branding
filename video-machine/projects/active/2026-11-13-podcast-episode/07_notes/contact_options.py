"""Numbered contact sheet of 08_docs/thumbnail-options/option-1..7.jpg -> options.jpg"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

D = Path("/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-13-podcast-episode/08_docs/thumbnail-options")
TW, TH, GAP = 640, 360, 8
cols, n = 2, 7
rows = (n + cols - 1) // cols
sheet = Image.new("RGB", (cols * TW + (cols + 1) * GAP, rows * TH + (rows + 1) * GAP), (24, 24, 24))
font = None
for p in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/System/Library/Fonts/Helvetica.ttc"):
    if Path(p).exists():
        font = ImageFont.truetype(p, 44)
        break
font = font or ImageFont.load_default()
for i in range(1, n + 1):
    im = Image.open(D / f"option-{i}.jpg").convert("RGB").resize((TW, TH), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([10, 10, 66, 64], radius=8, fill=(205, 236, 96))
    d.text((38, 37), str(i), font=font, fill=(10, 10, 10), anchor="mm")
    r, c = divmod(i - 1, cols)
    sheet.paste(im, (GAP + c * (TW + GAP), GAP + r * (TH + GAP)))
sheet.save(D / "options.jpg", quality=92)
print("options.jpg", sheet.size)
