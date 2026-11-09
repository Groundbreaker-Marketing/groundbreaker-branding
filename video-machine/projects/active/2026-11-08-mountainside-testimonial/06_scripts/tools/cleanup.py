"""Delete intermediates: working crops, dialogue wavs, close-up/wide prep, long-cut work dirs, kit stage caches.
Keeps renders, scripts, notes, the cached face tracks are deleted too (they re-make in minutes)."""
import glob, os, shutil, subprocess
P = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial/"
for d in [P + "04_project-files/crops", P + "04_project-files/audio", P + "10_work"] + glob.glob(P + "03_selects/*/10_WORK/stages") + \
        glob.glob(P + "03_selects/*/10_WORK/cut_preview_segments") + glob.glob(P + "03_selects/*/10_WORK/cut_preview.mp4"):
    if os.path.isdir(d):
        shutil.rmtree(d, ignore_errors=True)
    elif os.path.exists(d):
        os.remove(d)
    print("removed", d.replace(P, ""))
print(subprocess.run(["df", "-h", "/Users/josh"], capture_output=True, text=True).stdout)
