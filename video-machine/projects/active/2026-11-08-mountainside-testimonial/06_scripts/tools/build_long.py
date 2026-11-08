"""Build one long 16:9 cut from a spec (see vsl_lib).

    build_long.py <spec.json>

Spec keys: name, out (mp4 path under the project), items, burn (bool), music (Epidemic id or null),
broll (bool), crf, maxrate (web), poster (path or null), srt, vtt (paths or null), lower_thirds (bool),
broll_offset (int; rotates the pool so two cuts do not open on the same cutaway).
Writes the render, the caption files and 10_work/<name>/plan.json (the cut list, for REVIEW.md).
"""
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from vsl_lib import *  # noqa


def render_piece(i, item, work):
    out = work / f"p{i:02d}.mp4"
    if item["type"] == "talk":
        clip = item["clip"]
        t_in, t_out = item.get("_in"), item.get("_out")
        sh(["ffmpeg", "-y", "-v", "error", "-ss", f"{t_in:.3f}", "-t", f"{t_out - t_in:.3f}",
            "-i", str(CROPS / f"{clip}-h.mp4"),
            "-vf", ("" if clip == "C0070" else "crop=iw*0.93:ih*0.93:iw*0.07:0,")
                   + f"scale={W}:{H}:flags=lanczos,fps={FPS},setsar=1,format=yuv420p",
            "-af", f"aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.01,afade=t=out:st={t_out - t_in - 0.04:.3f}:d=0.04",
            "-c:v", "libx264", "-preset", "fast", "-crf", "14", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", str(out)])
    else:
        img = {"title": CARDS / f"title-{item.get('key')}.png", "review": CARDS / "review.png",
               "end": CARDS / "endcard-16x9.png"}[item["type"]]
        d = float(item["dur"])
        sh(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-framerate", str(FPS), "-t", f"{d}", "-i", str(img),
            "-f", "lavfi", "-t", f"{d}", "-i", "anullsrc=r=48000:cl=stereo",
            "-vf", f"scale={W}:{H},setsar=1,fade=t=in:d=0.2,fade=t=out:st={d - 0.2:.2f}:d=0.2,format=yuv420p",
            "-c:v", "libx264", "-preset", "fast", "-crf", "14", "-c:a", "aac", "-b:a", "256k", str(out)])
    return out


def main():
    spec = json.loads(Path(sys.argv[1]).read_text())
    name = spec["name"]
    work = P / "10_work" / name
    work.mkdir(parents=True, exist_ok=True)
    out_mp4 = P / spec["out"]
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    items = spec["items"]

    # 1. locate every talk piece
    for it in items:
        if it["type"] == "talk":
            it["_in"], it["_out"] = (it["in"], it["out"]) if "in" in it else locate_piece(it["clip"], it["text"])
            it["_in"] = round(it["_in"], 3)
            it["_out"] = round(it["_out"], 3)
    # 2. render pieces, concat
    parts = [render_piece(i, it, work) for i, it in enumerate(items)]
    lst = work / "concat.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    joined = work / "joined.mp4"
    sh(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(joined)])
    total = dur_of(joined)

    # 3. timeline
    t = 0.0
    spans, joins, blocked, cues, events, plan = [], [], [], [], [], []
    lts = []
    prev_talk_end = None
    for i, it in enumerate(items):
        d = dur_of(parts[i])
        it["_t0"], it["_dur"] = t, d
        if it["type"] == "talk":
            if prev_talk_end is not None and abs(prev_talk_end - t) < 0.01:
                joins.append(t)
            prev_talk_end = t + d
            spans.append((t, t + d))
            if it.get("hold") or it["clip"] == "C0070" or it.get("blocked"):
                blocked.append((t, t + d))
            words = words_for(it["clip"])
            cues += caption_cues(words, t, it["_in"], it["_out"])
            if it.get("lt"):
                lts.append((t + it.get("lt_at", 0.9), t + it.get("lt_at", 0.9) + 4.2, it["lt"][0], it["lt"][1]))
        else:
            prev_talk_end = None
        plan.append({"i": i, "type": it["type"], "clip": it.get("clip"), "text": it.get("text"),
                     "src_in": it.get("_in"), "src_out": it.get("_out"), "t0": round(t, 2), "dur": round(d, 2)})
        t += d
    blocked += [(0, spec.get("first_clear", 8.0))]
    cut = plan_broll(spans, joins, blocked=blocked, offset=spec.get("broll_offset", 0)) if spec.get("broll", True) else []
    json.dump({"items": plan, "broll": cut, "joins": joins, "total": total},
              open(work / "plan.json", "w"), indent=2)

    # 4. captions
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

    # 5. dialog audio, normalized
    dialog = work / "dialog.wav"
    sh(["ffmpeg", "-y", "-v", "error", "-i", str(joined), "-vn", "-ac", "2", "-ar", "48000", str(work / "raw.wav")])
    lufs = spec.get("lufs", -16)
    m = sh(["ffmpeg", "-hide_banner", "-nostats", "-i", str(work / "raw.wav"), "-af",
            f"loudnorm=I={lufs}:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"]).stderr
    j = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
    sh(["ffmpeg", "-y", "-v", "error", "-i", str(work / "raw.wav"), "-af",
        f"loudnorm=I={lufs}:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:"
        f"measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true",
        "-ar", "48000", str(dialog)])

    # 6. music
    music = None
    if spec.get("music"):
        music = work / "music.wav"
        if not music.exists():
            env = dict(os.environ)
            sh([sys.executable, "-m", "meta_ad.epidemic", "edit", spec["music"], f"{total:.1f}", str(music)],
               cwd="/Users/josh/apps/video-machine", env=env)

    # 7. final pass
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
        chains.append(f"{last}[b{k}]overlay=enable='between(t,{c['at']:.3f},{c['at'] + c['dur']:.3f})'"
                      f":eof_action=pass[o{k}]")
        last = f"[o{k}]"
    vf = f"{last}{GRADE}"
    if ev:
        vf +=f",ass={ass}:fontsdir={FONTS}"
    chains.append(vf + ",format=yuv420p[vout]")
    if music:
        fade_out = 2.5
        chains.append(f"[2:a]aformat=channel_layouts=stereo,loudnorm=I={spec.get('music_lufs', -33)}:TP=-3:LRA=7,afade=t=in:d=1.5,afade=t=out:st={total - fade_out:.2f}:d={fade_out}[mus]")
        chains.append("[1:a][mus]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.89[aout]")
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
        pt = spec.get("poster_at", 1.2)
        sh(["ffmpeg", "-y", "-v", "error", "-ss", f"{pt}", "-i", str(out_mp4), "-frames:v", "1", "-q:v", "2",
            str(P / spec["poster"])])
    print(name, "ok", round(total, 1), "s", out_mp4.stat().st_size // 1000, "KB")


if __name__ == "__main__":
    main()
