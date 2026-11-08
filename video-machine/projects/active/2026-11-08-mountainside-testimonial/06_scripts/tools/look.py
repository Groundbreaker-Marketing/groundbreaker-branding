"""look.py <video> <out.jpg> t1 t2 ...: stitch frames at the given seconds (3 columns) to review a render."""
import glob, subprocess, sys

video, out = sys.argv[1], sys.argv[2]
ts = sys.argv[3:]
font = glob.glob("/Users/josh/apps/video-machine/podcast/fonts/*.ttf")[0]
w, h = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                       "-of", "csv=p=0:s=x", video], capture_output=True, text=True).stdout.strip().split("x")
w, h = int(w), int(h)
tw = 640 if w >= h else 360
th = int(tw * h / w)
cmd = ["ffmpeg", "-y", "-v", "error"]
fc = []
for i, t in enumerate(ts):
    cmd += ["-ss", t, "-i", video]
    fc.append(f"[{i}:v]scale={tw}:{th},drawtext=fontfile={font}:text='{t}s':x=6:y=6:fontsize=20:fontcolor=white:"
              f"box=1:boxcolor=black@0.6[v{i}]")
cols = 3 if w >= h else 5
cols = min(cols, len(ts))
lay = "|".join(f"{(i % cols) * tw}_{(i // cols) * th}" for i in range(len(ts)))
cmd += ["-filter_complex", ";".join(fc) + ";" + "".join(f"[v{i}]" for i in range(len(ts))) +
        f"xstack=inputs={len(ts)}:layout={lay}:fill=black", "-frames:v", "1", "-strict", "unofficial", "-q:v", "3", out]
subprocess.run(cmd, check=True)
