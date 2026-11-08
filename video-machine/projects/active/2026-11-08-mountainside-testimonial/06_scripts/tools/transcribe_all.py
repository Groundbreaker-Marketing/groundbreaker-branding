"""Transcribe every clip with large-v3-turbo into 02_audio/<clip>.json (interview first)."""
import glob, os, subprocess, sys

P = "/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial"
clips = sorted(glob.glob(P + "/01_footage/C00*.MP4"))
clips.sort(key=lambda f: (int(os.path.basename(f)[1:5]) < 66, os.path.basename(f)))
env = dict(os.environ, VIBE_WHISPER_MODEL="large-v3-turbo")
for f in clips:
    out = P + "/02_audio/" + os.path.basename(f)[:5] + ".json"
    if os.path.exists(out):
        continue
    print("transcribing", f, flush=True)
    subprocess.run([sys.executable, "/Users/josh/apps/video-machine/kit/skills/long-form-ingest/scripts/transcribe_local.py",
                    f, "--out", out, "--model", "large-v3-turbo"], env=env)
print("done", flush=True)
