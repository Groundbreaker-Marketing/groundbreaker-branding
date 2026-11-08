"""Re-run meta_ad.build with large-v3-turbo transcribing the cut (the kit default is `small`).

    rebuild_ads.py [--only id ...]    re-captions from the cut transcript onward (--from captions)
Deletes each variant's 10_WORK/cut_words.json first so the caption words are re-made.
"""
import os, sys, json, runpy
from pathlib import Path

os.environ["VIBE_WHISPER_MODEL"] = "large-v3-turbo"
P = Path("/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial")
sys.path.insert(0, "/Users/josh/apps/video-machine")
only = sys.argv[1:]
if only and only[0] == "--only":
    only = only[1:]
for v in json.loads((P / "06_scripts/variants.json").read_text()):
    if only and v["id"] not in only:
        continue
    f = P / v["render_dir"] / "10_WORK" / "cut_words.json"
    if f.exists():
        f.unlink()
sys.argv = ["meta_ad.build", "groundbreaker-branding/2026-11-08-mountainside-testimonial", "--from", "captions"] + \
    (["--only"] + only if only else [])
runpy.run_module("meta_ad.build", run_name="__main__")
