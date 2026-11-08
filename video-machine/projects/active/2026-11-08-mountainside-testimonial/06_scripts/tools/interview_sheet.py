"""Interview overview: a frame every STEP seconds for one clip -> 07_notes/contact/_iv_<clip>.jpg"""
import glob, subprocess, sys

P = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial"
clip, step = sys.argv[1], float(sys.argv[2])
font = glob.glob("/Users/josh/apps/video-machine/podcast/fonts/*.ttf")[0]
f = f"{P}/01_footage/{clip}.MP4"
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                           capture_output=True, text=True).stdout)
rows = -(-int(dur / step + 1) // 6)
vf = (f"fps=1/{step},scale=320:180,drawtext=fontfile={font}:text='%{{pts\\:hms}}':x=4:y=4:fontsize=16:"
      f"fontcolor=white:box=1:boxcolor=black@0.6,tile=6x{rows}")
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", f, "-vf", vf, "-frames:v", "1", "-q:v", "5",
                f"{P}/07_notes/contact/_iv_{clip}.jpg"], check=True)
