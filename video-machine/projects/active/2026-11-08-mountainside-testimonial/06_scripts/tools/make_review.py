"""Write 07_notes/REVIEW.md from the renders and plans (lengths and openings come from the files)."""
import json, subprocess
from pathlib import Path

P = Path("/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial")
R = P / "05_renders/review"


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                                capture_output=True, text=True).stdout)


def mb(f):
    return f.stat().st_size / 1e6


def line(f, where, opening, why):
    d = dur(f)
    w, h = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                           "-of", "csv=p=0:s=x", str(f)], capture_output=True, text=True).stdout.strip().split("x")
    return (f"| `{f.relative_to(R)}` | {int(d // 60)}:{d % 60:04.1f} | {w}x{h} | {mb(f):.1f} MB | {where} | \"{opening}\" | {why} |")


rows = []
vsl = next((R / "vsl").glob("*.mp4"))
rows.append(line(vsl, "Sales page or YouTube, 16:9", "I have a contractor friend that I met and he raved about Josh and Ashley and said that is the best hire I've made to grow a business",
                 "A peer vouching is the most believable way to start; it lands inside the first 9 seconds, before any logo."))
variants = json.loads((P / "06_scripts/variants.json").read_text())
ad_why = {
    "no-third-leg-recognition-h1c1": ("Cold traffic, recognition", "Owners who live off one lead source will see their own worry in John's \"third and fourth leg on the stool\"."),
    "leads-to-hires-proof-h1": ("Proof", "The result as John tells it: Google leads became booked jobs and then hires."),
    "new-services-proof-h1": ("Proof", "Shows marketing bringing customers who ask for more than the first service."),
    "personal-side-objection-h1b1": ("Objection (DIY or AI)", "Answers \"why pay someone\" with a person to bounce ideas off."),
    "too-many-hats-recognition-h1b1": ("Cold traffic, recognition (shortest)", "Every owner wearing every hat recognizes this line."),
    "contractor-referral-proof-h1b1": ("Social proof", "Peer word of mouth first, then John's growth in his own words."),
}
for v in variants:
    for fmt in ("9x16", "4x5", "1x1"):
        f = P / "05_exports" / fmt / f"{v['id']}-{fmt}.mp4"
        if f.exists():
            role, why = ad_why[v["id"]]
            rows.append(f"| `ads/{fmt}/{f.name}` | {dur(f):.1f}s | {fmt.replace('x', ':')} | {mb(f):.1f} MB | Meta Feed and Reels, {role} | \"{v['script'][:110]}...\" | {why if fmt == '9x16' else 'Same cut, cropped for the Feed.'} |")
print("\n".join(rows))
