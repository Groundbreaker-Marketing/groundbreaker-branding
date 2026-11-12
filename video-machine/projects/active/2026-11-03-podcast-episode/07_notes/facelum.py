import sys
import numpy as np
from PIL import Image
im = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float)
L = 0.2126 * im[..., 0] + 0.7152 * im[..., 1] + 0.0722 * im[..., 2]
# face centers at 1280x720 (from the 960x540 view): host (195,250)*4/3, guest (765,240)*4/3
for name, (cx, cy) in (('Ashley', (260, 333)), ('Justin', (1020, 320))):
    box = L[cy - 70:cy + 70, cx - 55:cx + 55]
    rgb = im[cy - 70:cy + 70, cx - 55:cx + 55].reshape(-1, 3).mean(axis=0)
    print('%s luma mean %.0f  p10 %.0f p90 %.0f  rgb %s' % (name, box.mean(), np.percentile(box, 10), np.percentile(box, 90), rgb.round()))
