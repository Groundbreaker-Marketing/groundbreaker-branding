"""Make option 7 the episode thumbnail: copy its lines, headline_w and mirrored guest into thumbnail{}.
Ashley stays at 3209.0 (photo_crop [525, 0, 1125, 1080]), cutout on black. Title and render untouched."""
import json
from pathlib import Path

P = Path("/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-13-podcast-episode")
f = P / "06_scripts/episode.json"
ep = json.loads(f.read_text())
th = ep["thumbnail"]
o7 = th["variants"]["option-7"]
th["lines"] = o7["lines"]
th["headline_w"] = o7["headline_w"]
th["guest"] = {**th.get("guest", {}), "at": o7["guest"]["at"], "mirror": True}
assert th["at"] == 3209.0 and th["photo_crop"] == [525, 0, 1125, 1080] and th["layout"] == "cutout" and th["bg"] == "black"
assert th["guest"]["at"] == 2211.9 and th["headline_w"] == 440
f.write_text(json.dumps(ep, indent=1) + "\n")
print(json.dumps({k: v for k, v in th.items() if k != "variants"}))
