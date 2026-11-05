import subprocess, sys
from PIL import Image, ImageDraw
src = '01_footage/c0030.mp4'
times = [float(t) for t in sys.argv[2:]]
out = sys.argv[1]
tiles = []
for t in times:
    p = '07_notes/frames/s_%s.jpg' % t
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', src, '-frames:v', '1', '-vf', 'scale=640:-1', p], check=True)
    im = Image.open(p)
    ImageDraw.Draw(im).text((8, 8), '%.1f' % t, fill=(255, 255, 0))
    tiles.append(im)
cols = 3
rows = (len(tiles) + cols - 1) // cols
w, h = tiles[0].size
sheet = Image.new('RGB', (cols * w, rows * h))
for k, im in enumerate(tiles):
    sheet.paste(im, ((k % cols) * w, (k // cols) * h))
sheet.save(out, quality=88)
