"""Duration, size and time stamp of every source clip."""
import glob, os, subprocess, time

for f in sorted(glob.glob("/Users/josh/inbox/2026-10-28-mountainside-er/*.MP4")):
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "csv=p=0", f], capture_output=True, text=True).stdout.strip()
    st = os.stat(f)
    print(os.path.basename(f), d, st.st_size // 1_000_000, "MB", time.strftime("%H:%M", time.localtime(st.st_mtime)))
