"""Round 2: re-cut the leads-to-hires ad and the three long cuts that use the pinned in-point."""
import subprocess, sys
T = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial/06_scripts/"
P = "groundbreaker-branding/2026-11-08-mountainside-testimonial"
steps = [
    [sys.executable, "-u", T + "tools/prep_words.py", "leads-to-hires-proof-h1"],
    [sys.executable, "-u", "-m", "meta_ad.build", P, "--only", "leads-to-hires-proof-h1"],
    [sys.executable, "-u", T + "tools/build_long.py", T + "web-google-leads.json"],
    [sys.executable, "-u", T + "tools/build_long.py", T + "web-highlight.json"],
    [sys.executable, "-u", T + "tools/build_long.py", T + "vsl.json"],
]
for s in steps:
    print("RUN", " ".join(s[-3:]), flush=True)
    r = subprocess.run(s, cwd="/Users/josh/apps/video-machine")
    print("EXIT", r.returncode, flush=True)
print("ROUND2 DONE", flush=True)
