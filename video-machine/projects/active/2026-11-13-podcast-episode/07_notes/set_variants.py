"""Write thumbnail.variants option-1..7 into 06_scripts/episode.json (the main thumbnail block is untouched)."""
import json
from pathlib import Path

P = Path("/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-13-podcast-episode")
ep = json.loads((P / "06_scripts/episode.json").read_text())
LINES = [["HE RAISED HIS", "big"], ["SEPTIC PRICES", "box"], ["AND WENT FROM", "big"],
         ["1 PUMP TRUCK", "box"], ["TO 11", "box"]]
frames = {1: 1248.0, 2: 1542.0, 3: 2038.0, 4: 40.0, 5: 1298.0, 6: 346.0}
v = {}
for n, t in frames.items():
    v[f"option-{n}"] = {"out": f"08_docs/thumbnail-options/option-{n}.jpg", "guest": {"at": t},
                         "headline_w": 440, "lines": LINES}
v["option-7"] = {"out": "08_docs/thumbnail-options/option-7.jpg", "guest": {"at": 2211.9, "mirror": True},
                 "headline_w": 440, "lines": LINES}
ep["thumbnail"]["variants"] = v
(P / "06_scripts/episode.json").write_text(json.dumps(ep, indent=1) + "\n")
print(list(v))
