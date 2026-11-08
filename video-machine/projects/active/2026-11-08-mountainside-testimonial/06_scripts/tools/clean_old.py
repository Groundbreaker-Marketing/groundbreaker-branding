"""Delete the renders of the three superseded variant ids (hook and body overlapped; see SOP)."""
import glob, shutil
P = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial/"
OLD = ["no-third-leg-recognition-h1b1c1", "leads-to-hires-proof-h1b1", "new-services-proof-h1b1"]
for o in OLD:
    shutil.rmtree(P + "03_selects/" + o, ignore_errors=True)
    for f in glob.glob(P + f"05_exports/*/{o}-*") + glob.glob(P + f"08_docs/audits/{o}-*"):
        if f.endswith("/") or "audits" in f:
            shutil.rmtree(f, ignore_errors=True)
        else:
            import os
            os.remove(f)
    print("removed", o)
