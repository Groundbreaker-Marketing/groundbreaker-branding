"""Poster frames at 6.0 s (after the lower third has gone, before any B-roll) for the website clips."""
import glob, subprocess
D = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial/05_renders/review/website/"
for mp4 in sorted(glob.glob(D + "*.mp4")):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "6.0", "-i", mp4, "-frames:v", "1", "-q:v", "2",
                    mp4[:-4] + "-poster.jpg"], check=True)
    print("poster", mp4.split("/")[-1])
