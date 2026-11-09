"""Render every close-up and wide shot the round 2 specs need, then AI-upscale the close-ups once.

    prep_close.py spec1.json spec2.json ...

For each talk piece (located verbatim, in/out from the speaker's own mic) it collects:
  close  (the speaker, centered)        640x360 -> all joined -> podcast.upscale -> 1920x1080
  wide   (the two-shot, main picture of an Ashley question, and the inserts over a piece)  1920x1080
Writes 10_work/prep/close_map.json {job id: {"off": seconds into allclose-up.mp4, "n": frames}}.
Nothing is re-rendered if its file exists, so a restart loses at most one clip.
"""
import json, os, subprocess, sys
from pathlib import Path
sys.path.insert(0, os.path.dirname(__file__))
from vsl_lib import *  # noqa
import framing

PREP = P / "10_work" / "prep"
(PREP / "close").mkdir(parents=True, exist_ok=True)
(PREP / "wide").mkdir(parents=True, exist_ok=True)
STRENGTH = 0.6


def jid(clip, a, b, kind):
    return f"{kind}_{clip}_{int(round(a * 1000))}_{int(round(b * 1000))}"


def collect(specs):
    jobs = {}
    for sp in specs:
        for it in sp["items"]:
            if it["type"] != "talk":
                continue
            who = it.get("who", "L")
            if "in" in it:
                a, b = it["in"], it["out"]
            else:
                a, b = locate_piece(it["clip"], it["text"], who)
            it["_in"], it["_out"] = round(a, 3), round(b, 3)
            kind = it.get("frame", "close")
            for k, aa, bb in [(kind, a, b)] + [("wide", a + o, a + o + d) for o, d in it.get("wide_inserts", [])]:
                jobs[jid(it["clip"], aa, bb, k)] = {"id": jid(it["clip"], aa, bb, k), "clip": it["clip"], "t_in": round(aa, 3),
                                                    "t_out": round(bb, 3), "kind": k}
    return list(jobs.values())


def nframes(f):
    return int(sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries", "stream=nb_read_frames",
                   "-of", "csv=p=0", str(f)]).stdout.strip())


def main():
    specs = [json.loads(Path(f).read_text()) for f in sys.argv[1:]]
    jobs = collect(specs)
    print(len(jobs), "jobs:", sum(j["kind"] == "close" for j in jobs), "close,", sum(j["kind"] == "wide" for j in jobs), "wide", flush=True)
    for j in jobs:
        out = PREP / j["kind"]
        print("render", j["id"], flush=True)
        framing.render(j, str(out))
    close = [j for j in jobs if j["kind"] == "close"]
    cmap, off, lst = {}, 0, []
    for j in close:
        f = PREP / "close" / f"{j['id']}.mp4"
        n = nframes(f)
        cmap[j["id"]] = {"off": off / 30.0, "n": n}
        off += n
        lst.append(f"file '{f}'\n")
    (PREP / "close_list.txt").write_text("".join(lst))
    allc = PREP / "allclose.mp4"
    sh(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(PREP / "close_list.txt"), "-f", "lavfi", "-i",
        "anullsrc=r=48000:cl=stereo", "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-shortest", str(allc)])
    up = PREP / "allclose-up.mp4"
    if not up.exists():
        print("upscaling", off, "frames", flush=True)
        subprocess.run(["/Users/josh/apps/video-machine/run.sh", "--no-secrets", ".venv-upscale/bin/python", "-m", "podcast.upscale",
                        str(allc), str(up), "--strength", str(STRENGTH), "--fps", "30"], cwd="/Users/josh/apps/video-machine", check=True)
    json.dump(cmap, open(PREP / "close_map.json", "w"), indent=1)
    print("prep done", len(cmap), "close,", off / 30.0, "s", flush=True)


if __name__ == "__main__":
    main()
