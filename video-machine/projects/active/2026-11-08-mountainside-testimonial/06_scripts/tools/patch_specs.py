"""Pin the 'after ashley and josh started...' piece to a clean in-point (whisper times it 0.6 s early)."""
import json
P = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial/06_scripts/"
for n in ("vsl", "web-highlight", "web-google-leads"):
    s = json.load(open(P + n + ".json"))
    for it in s["items"]:
        if it.get("text", "").startswith("after ashley and josh started"):
            it["in"], it["out"] = 412.0, 431.18
            print(n, "pinned")
    open(P + n + ".json", "w").write(json.dumps(s, indent=2) + "\n")
