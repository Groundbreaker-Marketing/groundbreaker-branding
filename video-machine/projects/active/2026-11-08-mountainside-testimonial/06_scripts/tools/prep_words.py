"""Make each ad's caption words with large-v3-turbo and drop a stray first or last word.

The kit transcribes the CUT clip for its captions. Whisper sometimes invents a low-confidence word
at an abrupt start ("But something inside of me...", the cut starts on "something") or end. A
caption must be John's exact words, so a first or last word that is not the script's first or last
word and has probability under 0.85 is dropped. Anything else is left alone and reported.
Run before meta_ad.build (build keeps a cut_words.json newer than cuts.json).
"""
import json, os, re, sys
from pathlib import Path

os.environ["VIBE_WHISPER_MODEL"] = "large-v3-turbo"
sys.path.insert(0, "/Users/josh/apps/video-machine")
from meta_ad.build import pin_caption_words  # noqa

P = Path("/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial")


def n(w):
    return re.sub(r"[^a-z0-9']+", "", w.lower())


for v in json.loads((P / "06_scripts/variants.json").read_text()):
    if sys.argv[1:] and v["id"] not in sys.argv[1:]:
        continue
    rdir = P / v["render_dir"]
    f = rdir / "10_WORK" / "cut_words.json"
    if f.exists():
        f.unlink()
    pin_caption_words(rdir)
    data = json.loads(f.read_text())
    words = data["words"] if "words" in data else [w for s in data["segments"] for w in s["words"]]
    script = v["script"].split()
    changed = []
    while len(words) > 1 and n(words[0]["word"]) != n(script[0]) and words[0].get("prob", 1) < 0.85:
        changed.append(("head", words.pop(0)["word"]))
    while len(words) > 1 and n(words[-1]["word"]) != n(script[-1]) and words[-1].get("prob", 1) < 0.85:
        changed.append(("tail", words.pop()["word"]))
    if "words" in data:
        data["words"] = words
    else:
        data["segments"] = [{"start": words[0]["start"], "end": words[-1]["end"], "text": " ".join(w["word"] for w in words), "words": words}]
    f.write_text(json.dumps(data, indent=2))
    print(v["id"], "dropped", changed, "| first:", words[0]["word"], "| last:", words[-1]["word"], flush=True)
