"""find_q.py: locate Ashley's candidate questions verbatim in the turbo transcripts (source seconds)."""
import sys
sys.path.insert(0, "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial/06_scripts/tools")
from vsl_lib import *  # noqa

Q = [
    ("C0066", "we've been working together about six months how have you seen things grow in the last six months since we've been working together"),
    ("C0066", "john just tell us real quick about your business and what is it you do"),
    ("C0067", "so why hire a marketing agency instead of just do it yourself"),
    ("C0067", "has that been helpful for you having that tracking knowing where everything is coming from every call that you've gotten"),
]
for clip, text in Q:
    try:
        a, b = locate_piece(clip, text)
        print(clip, round(a, 2), round(b, 2), round(b - a, 1), text[:60])
    except Exception as e:
        print(clip, "NOT FOUND", str(e)[:200])
