import sys
import numpy as np
from PIL import Image
im = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float)
L = 0.2126 * im[..., 0] + 0.7152 * im[..., 1] + 0.0722 * im[..., 2]
for name, x0, x1 in (('Ashley', 0, 520), ('Justin', 760, 1280)):
    reg = L[:, x0:x1]
    person = reg[reg > 12]            # drop the black background
    print('%s: pixels %d  >=250: %.2f%%  <=25: %.2f%%  p1 %.0f p99 %.0f' % (
        name, person.size, 100 * (person >= 250).mean(), 100 * (person <= 25).mean(),
        np.percentile(person, 1), np.percentile(person, 99)))
