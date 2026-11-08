"""Overview sheets: one row per B-roll clip, 8 frames evenly spaced, labeled with clip and time."""
import glob, os, subprocess

P = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial"
font = glob.glob("/Users/josh/apps/video-machine/podcast/fonts/*.ttf")[0]
rows = []
for n in range(39, 66):
    f = f"{P}/01_footage/C{n:04d}.MP4"
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                               capture_output=True, text=True).stdout)
    out = f"{P}/07_notes/contact/_row{n}.jpg"
    k = 8
    vf = (f"fps={k}/{dur:.3f},scale=240:135,drawtext=fontfile={font}:text='C{n:04d} %{{pts\\:hms}}':x=4:y=4:"
          f"fontsize=16:fontcolor=white:box=1:boxcolor=black@0.6,tile={k}x1")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f, "-vf", vf, "-frames:v", "1", "-q:v", "5", out])
    rows.append(out)
for i in range(0, len(rows), 9):
    grp = rows[i:i + 9]
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for r in grp:
        cmd += ["-i", r]
    cmd += ["-filter_complex", "".join(f"[{j}:v]" for j in range(len(grp))) + f"vstack=inputs={len(grp)}",
            "-frames:v", "1", "-q:v", "4", f"{P}/07_notes/contact/overview_{i // 9 + 1}.jpg"]
    subprocess.run(cmd)
for r in rows:
    os.remove(r)
