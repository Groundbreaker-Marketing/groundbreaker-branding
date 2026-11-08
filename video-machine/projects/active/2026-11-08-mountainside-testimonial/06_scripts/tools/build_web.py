"""Build the four website cuts and the employee insert, one after another."""
import subprocess, sys
P = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial/06_scripts/"
for s in ("web-highlight", "web-google-leads", "web-more-work", "web-coaching", "employee-insert"):
    r = subprocess.run([sys.executable, P + "tools/build_long.py", P + s + ".json"], capture_output=True, text=True)
    print(s, r.stdout.strip()[-200:], r.stderr.strip()[-800:], flush=True)
