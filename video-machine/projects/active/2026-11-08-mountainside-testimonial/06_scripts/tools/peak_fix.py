"""Hold the true peak of every long render under -1 dBTP (audio-only remux, video copied)."""
import glob, re, subprocess, os
R = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial/05_renders/review/"


def tp(f):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", f, "-af", "ebur128=peak=true", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", err)
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", err)
    return float(m[-1]), float(i[-1])


for f in sorted(glob.glob(R + "*/*.mp4")):
    if "/ads/" in f:
        continue
    p, i = tp(f)
    print(os.path.basename(f), "peak", p, "I", i, flush=True)
    if p > -1.0:
        tmp = f[:-4] + ".tmp.mp4"
        abr = "128k" if "/website/" in f else "192k"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f, "-map", "0:v", "-map", "0:a", "-c:v", "copy", "-af",
                        "alimiter=limit=0.80:level=disabled", "-c:a", "aac", "-b:a", abr, "-ar", "48000",
                        "-movflags", "+faststart", tmp], check=True)
        os.replace(tmp, f)
        print("   ->", tp(f), flush=True)
