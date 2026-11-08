#!/bin/bash
# Duration, size and time stamp of every source clip.
cd /Users/josh/apps/video-machine
for f in /Users/josh/inbox/2026-10-28-mountainside-er/*.MP4; do
  d=$(./run.sh --no-secrets ffprobe -v error -show_entries format=duration -of csv=p=0 "$f")
  echo "$(basename "$f") $d $(stat -f '%z %Sm' -t %H:%M "$f")"
done
