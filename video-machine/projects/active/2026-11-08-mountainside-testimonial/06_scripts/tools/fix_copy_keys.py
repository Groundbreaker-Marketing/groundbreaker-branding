import json
P = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial/06_scripts/copy.json"
c = json.load(open(P))
m = {"no-third-leg-recognition-h1b1c1": "no-third-leg-recognition-h1c1",
     "leads-to-hires-proof-h1b1": "leads-to-hires-proof-h1", "new-services-proof-h1b1": "new-services-proof-h1"}
c["variants"] = {m.get(k, k): v for k, v in c["variants"].items()}
open(P, "w").write(json.dumps(c, indent=2) + "\n")
print(list(c["variants"]))
