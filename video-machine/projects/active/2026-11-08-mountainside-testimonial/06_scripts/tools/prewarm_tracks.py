import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import framing
for c in sys.argv[1:]:
    print("tracks", c, flush=True)
    framing.tracks(c)
print("done", flush=True)
