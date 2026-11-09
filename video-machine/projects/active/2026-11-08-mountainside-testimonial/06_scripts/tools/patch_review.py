"""Update REVIEW.md for round 2: file lengths in the table, the VSL chapter list, and the Round 2 section."""
P = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial/07_notes/REVIEW.md"
s = open(P).read()
rep = [
    ("| 3:16.6 |", "| 3:25.4 |"),
    ("| 25.2 s | 9:16, 4:5, 1:1", "| 25.6 s | 9:16, 4:5, 1:1"),
    ("| 27.1 s | same", "| 27.3 s | same"),
    ("| 23.6 s | same", "| 23.7 s | same"),
    ("| 16.7 s | same", "| 16.8 s | same"),
    ("26.4 MB (22 MB per minute)", "27.8 MB (23.5 MB per minute)"),
    ("| 24.7 s | 16:9 | Google Ads", "| 24.9 s | 16:9 | Google Ads"),
    ("9.4 MB.", "10.0 MB."),
    ("| 24.5 s | 16:9 | Pages about growth", "| 24.6 s | 16:9 | Pages about growth"),
    ("One continuous thought. 9.3 MB.", "One continuous thought. 9.6 MB."),
    ("| 26.9 s | 16:9 | Pages about working", "| 26.8 s | 16:9 | Pages about working"),
    ("9.8 MB.", "10.5 MB."),
    ("| 18.2 s | 16:9 | Drop-in", "| 18.3 s | 16:9 | Drop-in"),
]
for a, b in rep:
    if a not in s:
        print("MISSING", a)
    s = s.replace(a, b)
a = s.index("### How the VSL runs")
b = s.index("### Gates (ads)")
s = s[:a] + """### How the VSL runs (about, seconds; round 2 timings)
0:00 cold open (the referral line, John centered, lower third) · 0:09 Ashley asks "how have you seen things grow..." on the two-shot, then John's two legs on a stool · 0:46 Ashley asks "so why hire a marketing agency instead of just do it yourself", then why he hired us ·
1:16 Ashley asks "tell us real quick about your business", then what changed (more services, leads to hires, Max at 2:03, "doubled each summer") · 2:29 "Working with the team" title card, the Zoom calls · 2:49 his Google review card · 2:55 "His advice to other owners" title card · 3:20 end card.
No voiceover. 12 muted B-roll cutaways (3.6 s each), one over every jump cut except the one into Max's insert, and never more than about 14 s of one picture in a row (the two-shot cutaways count as picture changes).
Music: Epidemic Sound "Light Years" by Out To The World, recording id `e8da90fe-1284-48f9-aa10-0e9262e72a00`, cut to length, about 17 dB under the dialogue. The ads have no music bed.
Ads: each is hook, proof, then a 2.6 s end card (logo, Book a Strategy Call, groundbreakermarketing.com/calendar). Burned captions use the kit's caption preset (white, word weights). 2 to 4 muted cutaways per ad.

""" + s[b:]
r2 = open(P.replace("REVIEW.md", "review_round2.md")).read()
marker = "## Files"
s = s.replace(marker, r2 + "\n" + marker, 1)
open(P, "w").write(s)
print("patched")
