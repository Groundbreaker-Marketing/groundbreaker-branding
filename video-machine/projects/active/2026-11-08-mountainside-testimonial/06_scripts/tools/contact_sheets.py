"""Timestamped contact sheet per B-roll clip (one frame every STEP seconds) into 07_notes/contact/."""
import glob, os, subprocess, sys

P = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial"
os.makedirs(P + "/07_notes/contact", exist_ok=True)
STEP = float(sys.argv[1]) if len(sys.argv) > 1 else 3.0
lo, hi = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 else (39, 65)
FONT = "/Users/josh/apps/video-machine/podcast/fonts"
fonts = glob.glob(FONT + "/*.ttf")
font = fonts[0] if fonts else "/System/Library/Fonts/Helvetica.ttc"
for n in range(lo, hi + 1):
    f = f"{P}/01_footage/C{n:04d}.MP4"
    out = f"{P}/07_notes/contact/C{n:04d}.jpg"
    if not os.path.exists(f) or os.path.exists(out):
        continue
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                               capture_output=True, text=True).stdout)
    cols = 5
    rows = max(1, -(-int(dur / STEP + 1) // cols))
    vf = (f"fps=1/{STEP},scale=384:216,drawtext=fontfile={font}:text='%{{pts\\:hms}}':x=6:y=6:fontsize=20:"
          f"fontcolor=white:box=1:boxcolor=black@0.6,tile={cols}x{rows}")
    r = subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f, "-vf", vf, "-frames:v", "1", "-q:v", "4", out],
                       capture_output=True, text=True)
    print(f"C{n:04d}", round(dur, 1), "s", "ok" if r.returncode == 0 else r.stderr[-300:], flush=True)
