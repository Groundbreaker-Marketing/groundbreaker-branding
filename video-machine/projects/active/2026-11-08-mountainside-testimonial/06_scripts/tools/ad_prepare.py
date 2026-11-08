"""Plan B-roll cutaways and the end card for every ad variant -> 06_scripts/extras.json.

Runs each variant's kit cut stage to get the real segment lengths (the stage snaps cuts to silence,
so the timeline is not exactly the selects), then plans cutaways with vsl_lib.plan_broll:
hook on camera for the first ~3 s, one cutaway over every jump cut, and no more than ~7.5 s of
talking head in a row. Cutaways are cover-cropped from the 16:9 footage into 9:16.
"""
import importlib.util
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import vsl_lib as L  # noqa

KIT = Path("/Users/josh/apps/video-machine/kit/skills/render/stages")
sys.path.insert(0, str(KIT))
spec = importlib.util.spec_from_file_location("cut_stage", KIT / "cut.py")
cut = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cut)

# where to center the 9:16 crop of a landscape B-roll clip (0 left .. 1 right); default 0.5
CX = {"C0053": 0.55, "C0056": 0.5, "C0055": 0.45, "C0051": 0.5, "C0063": 0.5, "C0057": 0.5, "C0059": 0.5,
      "C0058": 0.5, "C0060": 0.5, "C0061": 0.5, "C0041": 0.5, "C0047": 0.5, "C0050": 0.5, "C0040": 0.55,
      "C0039": 0.4, "C0044": 0.5}

variants = json.loads((L.P / "06_scripts/variants.json").read_text())
extras = {}
for k, v in enumerate(variants):
    rdir = L.P / v["render_dir"]
    manifest = json.loads((rdir / "manifest.json").read_text())
    out = rdir / "10_WORK" / "cut_preview.mp4"
    res = cut.run(work_dir=rdir / "10_WORK", config=manifest["stages"]["cut"], inputs={}, inputs_meta={},
                  project=rdir, manifest=manifest, out_path=out)
    durs = [s["duration_s"] for s in res["meta"]["segments"]]
    total = sum(durs)
    joins, t = [], 0.0
    for d in durs[:-1]:
        t += d
        joins.append(round(t, 3))
    plan = L.plan_broll([(0.0, total)], joins, seg=2.2, first_clear=3.0, gap=7.5, offset=k * 5)
    cut_list = [{"at": c["at"], "dur": c["dur"], "src": str(L.FOOT / f"{c['clip']}.MP4"), "ss": c["ss"],
                 "cx": CX.get(c["clip"], 0.5), "clip": c["clip"]} for c in plan]
    extras[v["id"]] = {"broll": cut_list,
                       "endcard": {"image": str(L.CARDS / "endcard-9x16.png"), "dur": 2.6, "fade": 0.25}}
    print(v["id"], round(total, 1), "s", "joins", joins, "broll", [(c["at"], c["clip"]) for c in plan])
(L.P / "06_scripts/extras.json").write_text(json.dumps(extras, indent=2) + "\n")
