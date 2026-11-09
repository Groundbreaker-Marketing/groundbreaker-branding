"""sidebyside.py out.jpg a.mp4:sec b.mp4:sec ... : stitch frames (each scaled to 640 wide) into one image."""
import subprocess, sys
out, specs = sys.argv[1], sys.argv[2:]
cmd = ["ffmpeg", "-y", "-v", "error"]
fc = []
for i, s in enumerate(specs):
    f, t = s.rsplit(":", 1)
    cmd += ["-ss", t, "-i", f]
    fc.append(f"[{i}:v]scale=640:360[v{i}]")
cols = min(3, len(specs))
lay = "|".join(f"{(i % cols) * 640}_{(i // cols) * 360}" for i in range(len(specs)))
cmd += ["-filter_complex", ";".join(fc) + ";" + "".join(f"[v{i}]" for i in range(len(specs))) + f"xstack=inputs={len(specs)}:layout={lay}",
        "-frames:v", "1", "-strict", "unofficial", out]
subprocess.run(cmd, check=True)
