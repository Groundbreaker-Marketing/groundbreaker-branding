"""personal-side ad: the C0044 cutaway crops to a tire edge in 9:16; use the foothills pan (C0041) instead."""
import json
P = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial/06_scripts/extras.json"
e = json.load(open(P))
for c in e["personal-side-objection-h1b1"]["broll"]:
    if c["clip"] == "C0044":
        c.update(clip="C0041", ss=0.6, src=c["src"].replace("C0044", "C0041"), cx=0.5)
        print("swapped")
open(P, "w").write(json.dumps(e, indent=2) + "\n")
