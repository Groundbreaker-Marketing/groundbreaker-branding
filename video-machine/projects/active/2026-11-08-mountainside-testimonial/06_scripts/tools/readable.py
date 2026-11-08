"""Write 07_notes/transcripts/<clip>.txt: one line per segment with start-end seconds."""
import glob, json, os

P = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial"
os.makedirs(P + "/07_notes/transcripts", exist_ok=True)
for f in sorted(glob.glob(P + "/02_audio/C*.json")):
    d = json.load(open(f))
    segs = d.get("segments")
    lines = []
    if segs:
        for s in segs:
            lines.append(f"[{s['start']:7.2f}-{s['end']:7.2f}] {s['text'].strip()}")
    else:
        w = d["words"]
        cur, st = [], None
        for x in w:
            if st is None:
                st = x["start"]
            cur.append(x["word"].strip())
            if x["word"].strip()[-1:] in ".?!" or len(cur) > 25:
                lines.append(f"[{st:7.2f}-{x['end']:7.2f}] {' '.join(cur)}")
                cur, st = [], None
        if cur:
            lines.append(f"[{st:7.2f}-{w[-1]['end']:7.2f}] {' '.join(cur)}")
    open(P + "/07_notes/transcripts/" + os.path.basename(f)[:-5] + ".txt", "w").write("\n".join(lines) + "\n")
    print(os.path.basename(f), len(lines), "lines")
