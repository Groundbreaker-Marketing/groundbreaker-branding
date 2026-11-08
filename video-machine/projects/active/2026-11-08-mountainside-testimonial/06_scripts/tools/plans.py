import json
W = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial/10_work/"
for n in ("vsl", "web-highlight", "web-google-leads", "web-more-work", "web-coaching", "employee-insert"):
    p = json.load(open(W + n + "/plan.json"))
    print(n, "total", round(p["total"], 1))
    for i in p["items"]:
        print("  ", i["i"], i["type"], i["clip"], i["src_in"], i["src_out"], "t0", i["t0"], "dur", i["dur"])
    print("   broll", [(b["at"], b["clip"]) for b in p["broll"]])
