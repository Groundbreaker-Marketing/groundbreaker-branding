"""Copy the ad renders into 05_renders/review/ads/<format>/ and print a table of every review file."""
import glob, json, os, shutil, subprocess
P = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial/"
R = P + "05_renders/review/"
for fmt in ("9x16", "4x5", "1x1"):
    os.makedirs(R + f"ads/{fmt}", exist_ok=True)
    for f in glob.glob(P + f"05_exports/{fmt}/*.mp4"):
        shutil.copy2(f, R + f"ads/{fmt}/" + os.path.basename(f))
shutil.copy2(P + "06_scripts/copy.json", R + "ads/ad-copy-DRAFT.json")


def info(f):
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                             capture_output=True, text=True).stdout)
    w, h = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                           "-of", "csv=p=0:s=x", f], capture_output=True, text=True).stdout.strip().split("x")
    return d, f"{w}x{h}", os.path.getsize(f) / 1e6


for f in sorted(glob.glob(R + "*/*.mp4") + glob.glob(R + "ads/*/*.mp4")):
    d, wh, mb = info(f)
    print(f"{f.replace(R, ''):<110} {d:6.1f}s {wh:>10} {mb:6.1f}MB")
