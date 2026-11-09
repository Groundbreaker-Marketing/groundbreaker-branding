"""Build one long 16:9 cut from a spec (round 2: dialogue audio, centered close-ups, Ashley's wide two-shot).

    build_long.py <spec.json>      (run prep_close.py on the specs first)

Talk item: clip, text (or in/out), who "L" (default: the left mic, John or Max) or "R" (Ashley's mic),
frame "close" (default, the AI-upscaled centered close-up) or "wide" (the two-shot), wide_inserts
[[offset, seconds]] (the two-shot laid over the close-up, same sound), blocked (no B-roll), lt.
Sound is always the speaker's own mic from 04_project-files/audio/<clip>-<who>.wav (dialogue package).
Other keys: name, out, burn, srt, vtt, music, broll, crf, maxrate, poster, lufs.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from vsl_lib import *  # noqa
sys.path.insert(0, "/Users/josh/apps/video-machine")
from dialogue import chain as dchain  # noqa

PREP = P / "10_work" / "prep"
FRAME_FIX = "setpts=PTS*30/29.97"     # the working shots are 29.97 fps frames written at 30


def jid(clip, a, b, kind):
    return f"{kind}_{clip}_{int(round(a * 1000))}_{int(round(b * 1000))}"


def piece_loudness(wav, t_in, d):
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-ss", f"{t_in:.3f}", "-t", f"{d:.3f}", "-i", str(wav),
                          "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", err)
    return float(m[-1]) if m else -16.0


def render_piece(i, it, work, cmap):
    out = work / f"p{i:02d}.mp4"
    if it["type"] != "talk":
        img = {"title": CARDS / f"title-{it.get('key')}.png", "review": CARDS / "review.png",
               "end": CARDS / "endcard-16x9.png"}[it["type"]]
        d = float(it["dur"])
        sh(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", str(FPS), "-t", f"{d}", "-i", str(img),
            "-f", "lavfi", "-t", f"{d}", "-i", "anullsrc=r=48000:cl=stereo",
            "-vf", f"scale={W}:{H},setsar=1,fade=t=in:d=0.2,fade=t=out:st={d - 0.2:.2f}:d=0.2,format=yuv420p",
            "-c:v", "libx264", "-preset", "fast", "-crf", "14", "-c:a", "aac", "-b:a", "256k", str(out)])
        return out
    clip, who = it["clip"], it.get("who", "L")
    a, b = it["_in"], it["_out"]
    d = b - a
    kind = it.get("frame", "close")
    wav = mic_wav(clip, who)
    # per piece level match (speakers and clips sit at slightly different levels): to -16 LUFS, clamped
    gain = max(-9.0, min(9.0, -16.0 - piece_loudness(wav, a, d)))
    cmd = ["ffmpeg", "-y", "-v", "error"]
    if kind == "close":
        j = cmap[jid(clip, a, b, "close")]
        cmd += ["-ss", f"{j['off']:.4f}", "-t", f"{j['n'] / 30:.4f}", "-i", str(PREP / "allclose-up.mp4")]
    else:
        cmd += ["-i", str(PREP / "wide" / f"{jid(clip, a, b, 'wide')}.mp4")]
    cmd += ["-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", str(wav)]
    chains = [f"[0:v]scale={W}:{H}:flags=lanczos,{FRAME_FIX},fps={FPS},tpad=stop_mode=clone:stop_duration=0.3,setsar=1,format=yuv420p[base]"]
    last = "[base]"
    for k, (off, dd) in enumerate(it.get("wide_inserts", []), start=2):
        cmd += ["-i", str(PREP / "wide" / f"{jid(clip, a + off, a + off + dd, 'wide')}.mp4")]
        chains.append(f"[{k}:v]scale={W}:{H}:flags=lanczos,{FRAME_FIX},fps={FPS},setsar=1,format=yuv420p,setpts=PTS-STARTPTS+{off:.3f}/TB[w{k}]")
        chains.append(f"{last}[w{k}]overlay=enable='between(t,{off:.3f},{off + dd:.3f})':eof_action=pass[o{k}]")
        last = f"[o{k}]"
    chains.append(f"[1:a]aresample=48000,aformat=channel_layouts=stereo,volume={gain:.2f}dB,afade=t=in:d=0.01,"
                  f"afade=t=out:st={max(0.0, d - 0.04):.3f}:d=0.04[a]")
    cmd += ["-filter_complex", ";".join(chains), "-map", last, "-map", "[a]", "-t", f"{d:.3f}",
            "-c:v", "libx264", "-preset", "fast", "-crf", "14", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", str(out)]
    sh(cmd)
    return out


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    name = spec["name"]
    work = P / "10_work" / name
    work.mkdir(parents=True, exist_ok=True)
    out_mp4 = P / spec["out"]
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    items = spec["items"]
    cmap = json.loads((PREP / "close_map.json").read_text())

    for it in items:
        if it["type"] == "talk":
            if "in" in it:
                it["_in"], it["_out"] = it["in"], it["out"]
            else:
                a, b = locate_piece(it["clip"], it["text"], it.get("who", "L"))
                it["_in"], it["_out"] = round(a, 3), round(b, 3)
    parts = [render_piece(i, it, work, cmap) for i, it in enumerate(items)]
    lst = work / "concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    joined = work / "joined.mp4"
    sh(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(joined)])
    total = dur_of(joined)

    t = 0.0
    spans, joins, blocked, cues, plan, lts, seeds = [], [], [], [], [], [], []
    prev_end = None
    for i, it in enumerate(items):
        d = dur_of(parts[i])
        it["_t0"], it["_dur"] = t, d
        if it["type"] == "talk":
            who = it.get("who", "L")
            if prev_end is not None and abs(prev_end - t) < 0.01:
                joins.append(t)
            prev_end = t + d
            spans.append((t, t + d))
            if it.get("blocked") or it["clip"] == "C0070":
                blocked.append((t, t + d))
            if it.get("frame") == "wide":
                seeds.append((t, t + d))
            for off, dd in it.get("wide_inserts", []):
                blocked.append((t + off - 0.1, t + off + dd + 0.1))
                seeds.append((t + off, t + off + dd))
            cues += caption_cues(words_for(it["clip"]), t, it["_in"], it["_out"])
            if it.get("lt"):
                lts.append((t + it.get("lt_at", 0.9), t + it.get("lt_at", 0.9) + 4.2, it["lt"][0], it["lt"][1]))
        else:
            prev_end = None
        plan.append({"i": i, "type": it["type"], "clip": it.get("clip"), "who": it.get("who", "L") if it["type"] == "talk" else None,
                     "frame": it.get("frame", "close") if it["type"] == "talk" else None, "text": it.get("text"),
                     "src_in": it.get("_in"), "src_out": it.get("_out"), "t0": round(t, 2), "dur": round(d, 2)})
        t += d
    blocked.append((0, spec.get("first_clear", 8.0)))
    cut = plan_broll(spans, joins, blocked=blocked, offset=spec.get("broll_offset", 0), seed=seeds) if spec.get("broll", True) else []
    json.dump({"items": plan, "broll": cut, "joins": joins, "total": total}, open(work / "plan.json", "w"), indent=2)

    if spec.get("srt"):
        write_srt(cues, P / spec["srt"])
    if spec.get("vtt"):
        write_vtt(cues, P / spec["vtt"])
    ass = work / "cut.ass"
    ev = ass_caption_events(cues) if spec.get("burn") else []
    if spec.get("lower_thirds", True):
        for a, b, n, s in lts:
            ev += ass_lower_third(a, b, n, s)
    ass.write_text(ass_header() + "\n".join(ev) + "\n")

    raw, dialog = work / "raw.wav", work / "dialog.wav"
    sh(["ffmpeg", "-y", "-v", "error", "-i", str(joined), "-vn", "-ac", "2", "-ar", "48000", str(raw)])
    levels = dchain.normalize(raw, dialog, lufs=spec.get("lufs", -16))

    music = None
    if spec.get("music"):
        music = work / "music.wav"
        if not music.exists() or abs(dur_of(music) - total) > 1.0:
            if music.exists():
                music.unlink()
            sh([sys.executable, "-m", "meta_ad.epidemic", "edit", spec["music"], f"{total:.1f}", str(music)],
               cwd="/Users/josh/apps/video-machine")

    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(joined), "-i", str(dialog)]
    nin = 2
    if music:
        cmd += ["-i", str(music)]
        nin += 1
    chains, last = [], "[0:v]"
    for k, c in enumerate(cut):
        cmd += ["-ss", f"{c['ss']:.3f}", "-t", f"{c['dur']:.3f}", "-i", str(FOOT / f"{c['clip']}.MP4")]
        idx = nin + k
        chains.append(f"[{idx}:v]scale={W}:{H}:flags=lanczos,fps={FPS},setsar=1,format=yuv420p,"
                      f"setpts=PTS-STARTPTS+{c['at']:.3f}/TB[b{k}]")
        chains.append(f"{last}[b{k}]overlay=enable='between(t,{c['at']:.3f},{c['at'] + c['dur']:.3f})':eof_action=pass[o{k}]")
        last = f"[o{k}]"
    vf = f"{last}{GRADE}"
    if ev:
        vf += f",ass={ass}:fontsdir={FONTS}"
    chains.append(vf + ",format=yuv420p[vout]")
    if music:
        chains.append(f"[2:a]aformat=channel_layouts=stereo,loudnorm=I={spec.get('music_lufs', -33)}:TP=-3:LRA=7,"
                      f"afade=t=in:d=1.5,afade=t=out:st={total - 2.5:.2f}:d=2.5[mus]")
        chains.append("[1:a][mus]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.84:level=disabled[aout]")
        amap = "[aout]"
    else:
        amap = "1:a"
    cmd += ["-filter_complex", ";".join(chains), "-map", "[vout]", "-map", amap]
    cmd += ["-c:v", "libx264", "-preset", spec.get("preset", "medium"), "-crf", str(spec.get("crf", 18)), "-pix_fmt", "yuv420p"]
    if spec.get("maxrate"):
        cmd += ["-maxrate", spec["maxrate"], "-bufsize", spec["bufsize"]]
    cmd += ["-c:a", "aac", "-b:a", spec.get("abr", "192k"), "-ar", "48000", "-movflags", "+faststart", str(out_mp4)]
    sh(cmd)
    if spec.get("poster"):
        sh(["ffmpeg", "-y", "-v", "error", "-ss", f"{spec.get('poster_at', 6.0)}", "-i", str(out_mp4), "-frames:v", "1", "-q:v", "2",
            str(P / spec["poster"])])
    print(name, "ok", round(total, 1), "s", out_mp4.stat().st_size // 1000, "KB", json.dumps(levels["after"]))


if __name__ == "__main__":
    main()
