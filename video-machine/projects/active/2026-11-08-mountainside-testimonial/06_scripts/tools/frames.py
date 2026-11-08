"""frames.py <out.jpg> clip:sec [clip:sec ...]: one labeled contact row of frames from the footage."""
import subprocess, sys, glob

P = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial"
out = sys.argv[1]
font = glob.glob("/Users/josh/apps/video-machine/podcast/fonts/*.ttf")[0]
specs = sys.argv[2:]
cmd = ["ffmpeg", "-y", "-v", "error"]
fc = []
for i, s in enumerate(specs):
    c, t = s.split(":")
    cmd += ["-ss", t, "-i", f"{P}/01_footage/{c}.MP4"]
    fc.append(f"[{i}:v]scale=640:360,drawtext=fontfile={font}:text='{c} {t}s':x=6:y=6:fontsize=22:"
              f"fontcolor=white:box=1:boxcolor=black@0.6[v{i}]")
cols = min(3, len(specs))
rows = -(-len(specs) // cols)
lay = "|".join(f"{(i % cols) * 640}_{(i // cols) * 360}" for i in range(len(specs)))
fcs = ";".join(fc) + ";" + "".join(f"[v{i}]" for i in range(len(specs))) + \
    f"xstack=inputs={len(specs)}:layout={lay}:fill=black"
cmd += ["-filter_complex", fcs, "-frames:v", "1", "-q:v", "4", out]
subprocess.run(cmd, check=True)
