"""2026-11-23 Ashley's two swaps: lose-customers on Instagram + Facebook (terralift's 12-29 noon slot);
terralift YouTube + TikTok only (lose-customers's 12-24 5 PM slot). No other clip moves."""
import json
from pathlib import Path

f = Path("/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-13-podcast-episode/06_scripts/shorts.json")
rec = json.loads(f.read_text())
by = {c["id"]: c for c in rec["clips"]}
lc, tl = by["lose-customers"], by["terralift"]
assert lc["publish_at"] == "2026-12-24T17:00:00" and tl["publish_at"] == "2026-12-29T12:00:00"
lc["publish_at"] = "2026-12-29T12:00:00"
lc["networks"] = ["youtube", "tiktok", "instagram", "facebook"]
lc["captions"]["instagram"] = (
    "\"I thought, man, I'm going to lose so many customers. And I did.\" {jason} of {aas} raised his septic "
    "prices and lost customers, just like he feared. But he says those weren't the customers he wanted. They "
    "were always using him, then went to the next guy as soon as he raised his rate. His take: that's not a "
    "good customer, and you have to want to be an A-rated company.\n\nFull episode: {episode}\n\n"
    "#septic #septicbusiness #septicpumper #pricing #smallbusiness")
lc["captions"]["facebook"] = (
    "You raise your prices, and the customers you were most afraid of losing do exactly what you feared. "
    "{jason} of {aas} says he thought, man, I'm going to lose so many customers, and he did. But he says those "
    "weren't the customers he wanted. They were the ones always using him, and when he raised his rate they "
    "said they'd just go to the next guy. His take: someone who does that is not a good customer, and you have "
    "to want your company to be an A-rated company.\n\n#septic")
tl["publish_at"] = "2026-12-24T17:00:00"
tl["networks"] = ["youtube", "tiktok"]
tl["captions"].pop("instagram", None)
tl["captions"].pop("facebook", None)
f.write_text(json.dumps(rec, indent=1) + "\n")
for k in ("instagram", "facebook"):
    print(k, len(lc["captions"][k].split()), "words")
print({c["id"]: (c["publish_at"], c["networks"]) for c in rec["clips"] if c["id"] in ("lose-customers", "terralift")})
print("lose-customers cover:", lc.get("cover"))
