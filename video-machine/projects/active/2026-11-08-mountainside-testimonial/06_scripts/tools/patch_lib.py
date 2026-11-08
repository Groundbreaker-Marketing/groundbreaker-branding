p = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial/06_scripts/tools/"
s = open(p + "vsl_lib.py").read()
s = s[:s.index("def plan_broll")] + open(p + "plan_new.txt").read()
open(p + "vsl_lib.py", "w").write(s)
print("patched")
