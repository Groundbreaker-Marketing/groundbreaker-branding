RioVation (NOWRA booth episode) sent four licensed videos as B-roll, two of them 852x480 with portrait phone shots inside black side bars. A broll pick now takes `src_crop` [x, y, w, h] (the clip's own pixels, to cut the bars off) and `fill: "blur"` (the whole picture over a blurred, enlarged copy of itself instead of a crop). Default behavior is unchanged.

Tested: tests/test_shorts_broll.py (9 pass, one new); used in the RioVation episode render.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
