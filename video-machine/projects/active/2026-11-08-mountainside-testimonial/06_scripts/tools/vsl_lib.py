"""Shared helpers for the long 16:9 cuts (VSL, website highlight and topic clips, employee short).

A cut is a list of items (spec JSON):
  {"type": "talk",  "clip": "C0067", "text": "verbatim words", "lt": ["Name", "Subtitle"] (optional)}
  {"type": "title", "key": "before", "dur": 1.8}
  {"type": "review", "dur": 5.5}              # John's verbatim Google review as a card
  {"type": "end", "dur": 5}
Talk pieces are located verbatim in the word transcript (like meta_ad.variants), cut from the
face-tracked 16:9 working crop (04_project-files/crops/<clip>-h.mp4), and joined. B-roll cutaways
(muted, from the raw footage) are planned automatically: one over every jump cut and one at least
every ~10 s of talking head. Captions are burned (ASS) or written as .srt/.vtt only.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, "/Users/josh/apps/video-machine")
from meta_ad.variants import load_words, locate, tighten, brand_corrections  # noqa: E402
from meta_ad.common import load_brand  # noqa: E402

P = Path("/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial")
FOOT = P / "01_footage"
CROPS = P / "04_project-files/crops"
CARDS = P / "04_project-files/cards"
FONTS = "/Users/josh/apps/video-machine/kit/skills/caption-clips/fonts/free_font"
W, H, FPS = 1920, 1080, 30
GRADE = "eq=contrast=1.05:saturation=1.06:gamma=0.98"

BRAND = load_brand("groundbreaker-branding")
FIX = brand_corrections(BRAND)   # lowercase wrong -> canonical
FIX.update({"ashley": "Ashley", "josh": "Josh", "google": "Google", "zoom": "Zoom", "colorado": "Colorado",
            "zoho": "Zoho", "facebook": "Facebook", "i": "I", "john": "John", "max": "Max"})

# raw footage with no speech worth keeping: (clip, start sec, usable sec). All shown muted.
BROLL_POOL = [
    ("C0053", 1.0, 26), ("C0056", 2.0, 14), ("C0055", 1.5, 14), ("C0051", 1.0, 11), ("C0063", 2.0, 17),
    ("C0057", 3.0, 17), ("C0059", 4.0, 32), ("C0058", 2.0, 15), ("C0060", 0.5, 11), ("C0061", 1.5, 7),
    ("C0041", 0.5, 8), ("C0047", 0.3, 7.5), ("C0050", 0.5, 7.5), ("C0040", 0.3, 8.5), ("C0039", 0.2, 5.5),
    ("C0044", 7.0, 3.6),
]


def sh(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode:
        raise RuntimeError(" ".join(map(str, cmd))[:300] + "\n" + r.stderr[-1500:])
    return r


def dur_of(path) -> float:
    return float(sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]).stdout)


def clean_word(w: str) -> str:
    base = re.sub(r"[^A-Za-z0-9'$%]+$", "", w.strip())
    tail = w.strip()[len(base):]
    key = re.sub(r"[^a-z0-9']+", "", base.lower())
    if key in FIX:
        return FIX[key] + tail
    if re.fullmatch(r"i'(m|ll|ve|d)", key):
        return "I" + key[1:] + tail
    return base + tail


def words_for(clip: str):
    raw = json.loads((P / "02_audio" / f"{clip}.json").read_text())
    ws = raw["words"] if "words" in raw else [w for s in raw["segments"] for w in s["words"]]
    out = []
    for w in ws:
        t = w.get("word", w.get("text", "")).strip()
        if t:
            out.append({"word": t, "start": float(w["start"]), "end": float(w["end"])})
    return out


_cache = {}


AUDIO = P / "04_project-files" / "audio"


def mic_wav(clip: str, who: str = "L") -> Path:
    """Round 2 dialogue track (dialogue.process): the speaker's own mic, both ears, voice chain."""
    return AUDIO / f"{clip}-{who}.wav"


def locate_piece(clip: str, text: str, who: str = "L"):
    if clip not in _cache:
        _cache[clip] = load_words(P / "02_audio" / f"{clip}.json")
    a, b = locate(text, _cache[clip])
    wav = mic_wav(clip, who)
    return tighten(wav if wav.exists() else FOOT / f"{clip}.MP4", a, b)


def caption_cues(words, piece_start, t_in, t_out, join_breaks=True):
    """Words inside [t_in, t_out] -> cue dicts on the cut's timeline. Brand terms fixed, I capitalized."""
    ws = [w for w in words if w["start"] >= t_in - 0.03 and w["end"] <= t_out + 0.12]
    # merge "Mountainside" + "ER"
    merged = []
    for w in ws:
        c = clean_word(w["word"])
        if merged and merged[-1]["c"].lower().strip(",.") == "mountainside" and c.lower().strip(",.") == "er":
            merged[-1]["c"] = "Mountainside ER" + re.sub(r"^[A-Za-z]+", "", c)
            merged[-1]["end"] = w["end"]
            continue
        merged.append({"c": c, "start": w["start"], "end": w["end"]})
    cues, cur = [], []

    def flush():
        if cur:
            cues.append({"words": list(cur)})
            cur.clear()

    for i, w in enumerate(merged):
        if cur:
            gap = w["start"] - cur[-1]["end"]
            chars = len(" ".join(x["c"] for x in cur + [w]))
            if gap > 0.55 or len(cur) >= 5 or chars > 30 or re.search(r"[.?!]$", cur[-1]["c"]):
                flush()
        cur.append(w)
    flush()
    out = []
    for k, cue in enumerate(cues):
        ws_ = cue["words"]
        s = piece_start + max(0.0, ws_[0]["start"] - t_in)
        e = piece_start + min(t_out - t_in, ws_[-1]["end"] - t_in) + 0.12
        out.append({"start": s, "end": e,
                    "words": [{"c": x["c"], "s": piece_start + max(0.0, x["start"] - t_in),
                               "e": piece_start + max(0.0, x["end"] - t_in)} for x in ws_]})
    for a, b in zip(out, out[1:]):
        a["end"] = min(a["end"], b["start"] - 0.01) if b["start"] > a["start"] else a["end"]
    return out


def ts(t, comma=True):
    h, m, s = int(t // 3600), int(t % 3600 // 60), t % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", "," if comma else ".")


def write_srt(cues, path):
    lines = []
    for i, c in enumerate(cues, 1):
        lines += [str(i), f"{ts(c['start'])} --> {ts(c['end'])}", " ".join(w["c"] for w in c["words"]), ""]
    Path(path).write_text("\n".join(lines))


def write_vtt(cues, path):
    lines = ["WEBVTT", ""]
    for c in cues:
        lines += [f"{ts(c['start'], False)} --> {ts(c['end'], False)}", " ".join(w["c"] for w in c["words"]), ""]
    Path(path).write_text("\n".join(lines))


def ass_header(font_size=66, margin_v=64):
    return f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Montserrat ExtraBold,{font_size},&H0060ECCD,&H00FFFFFF,&H00101010,&H90000000,0,0,0,0,100,100,0,0,1,4,2,2,120,120,{margin_v},1
Style: LTname,Montserrat ExtraBold,52,&H00FFFFFF,&H00FFFFFF,&H00101010,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: LTsub,Montserrat Medium,35,&H0060ECCD,&H0060ECCD,&H00101010,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1
Style: Box,Montserrat,20,&H00000000,&H00000000,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def ass_time(t):
    h, m, s = int(t // 3600), int(t % 3600 // 60), t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def ass_caption_events(cues):
    ev = []
    for c in cues:
        text = ""
        for w in c["words"]:
            cs = max(1, int(round((w["e"] - w["s"]) * 100)))
            text += "{\\k%d}%s " % (cs, w["c"].replace("{", "").replace("}", ""))
        ev.append(f"Dialogue: 1,{ass_time(c['start'])},{ass_time(c['end'])},Cap,,0,0,0,,{text.strip()}")
    return ev


def ass_lower_third(t0, t1, name, sub, x=110, y=770):
    # dark translucent bar with a lime edge, then two text lines
    bw, bh = 780, 128
    draw = f"{{\\pos({x},{y})\\p1\\1c&H1B1B1B&\\1a&H40&\\bord0\\shad0\\fad(250,250)}}m 0 0 l {bw} 0 l {bw} {bh} l 0 {bh}{{\\p0}}"
    edge = f"{{\\pos({x},{y})\\p1\\1c&H60ECCD&\\bord0\\shad0\\fad(250,250)}}m 0 0 l 8 0 l 8 {bh} l 0 {bh}{{\\p0}}"
    return [
        f"Dialogue: 2,{ass_time(t0)},{ass_time(t1)},Box,,0,0,0,,{draw}",
        f"Dialogue: 3,{ass_time(t0)},{ass_time(t1)},Box,,0,0,0,,{edge}",
        f"Dialogue: 4,{ass_time(t0)},{ass_time(t1)},LTname,,0,0,0,,{{\\pos({x + 28},{y + 12})\\fad(250,250)}}{name}",
        f"Dialogue: 4,{ass_time(t0)},{ass_time(t1)},LTsub,,0,0,0,,{{\\pos({x + 28},{y + 74})\\fad(250,250)}}{sub}",
    ]


def broll_windows(seg=3.6):
    """Round-robin windows of `seg` seconds from the pool, so neighbors come from different clips."""
    per = []
    for clip, ss, usable in BROLL_POOL:
        wins, t = [], ss
        while t + seg <= ss + usable:
            wins.append((clip, round(t, 2)))
            t += seg + 0.4
        per.append(wins)
    out, i = [], 0
    while any(per):
        for wins in per:
            if wins:
                out.append(wins.pop(0))
    return out


def plan_broll(spans, joins, seg=3.6, first_clear=8.0, gap=10.5, offset=0, blocked=(), seed=()):
    """Plan muted B-roll cutaways on the cut's timeline.

    spans:   [(t0, t1)] stretches of talking head (one per talk piece; cards are not in here)
    joins:   times of jump cuts between talk pieces (each gets a cutaway from 1.0 s before to 2.6 s after)
    blocked: [(t0, t1)] stretches that must stay on camera (the employee's insert, the cold open)
    Fills so that no stretch of talking head runs longer than `gap` seconds.
    Returns [{at, dur, clip, ss}] sorted by time.
    """
    wins = broll_windows(seg)
    cuts = [tuple(s) for s in seed]      # other picture changes (the wide two-shot): they break up the head too
    merged = []
    for s0, s1 in sorted(spans):          # talk pieces that touch form one run (jump cuts inside it)
        if merged and abs(merged[-1][1] - s0) < 0.01:
            merged[-1] = (merged[-1][0], s1)
        else:
            merged.append((s0, s1))
    spans = merged

    def free(a, b):
        if a < first_clear:
            return False
        if any(not (b <= x0 or a >= x1) for x0, x1 in blocked):
            return False
        return any(a >= s0 + 0.3 and b <= s1 - 0.3 for s0, s1 in spans)

    for j in joins:
        for lead in (1.0, 0.5, 0.0):      # slide later when a protected stretch sits just before the cut
            a = j - lead
            if free(a, a + seg) and not any(not (a + seg <= c0 or a >= c1) for c0, c1 in cuts):
                cuts.append((a, a + seg))
                break
    cuts.sort()
    # break up long stretches of head
    changed = True
    while changed:
        changed = False
        pts = sorted(cuts)
        for s0, s1 in spans:
            # head stretches inside this span, between cutaways
            inside = [c for c in pts if c[0] >= s0 - 0.01 and c[1] <= s1 + 0.01]
            edges = [s0] + [x for c in inside for x in c] + [s1]
            for a, b in zip(edges[0::2], edges[1::2]):
                if b - a > gap:
                    for off in (6.5, 4.5, 8.5, 3.0, 2.0):
                        at = a + off
                        if free(at, at + seg) and at + seg <= b - 1.0:
                            cuts.append((at, at + seg))
                            changed = True
                            break
                    if changed:
                        break
            if changed:
                break
    cuts = [c for c in sorted(cuts) if c not in {tuple(s) for s in seed}]
    out = []
    for k, (a, b) in enumerate(cuts):
        clip, ss = wins[(k + offset) % len(wins)]
        out.append({"at": round(a, 3), "dur": round(b - a, 3), "clip": clip, "ss": ss})
    return out
