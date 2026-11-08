"""check_spec.py <spec.json>: locate every talk piece verbatim and print its source times and length."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from vsl_lib import *  # noqa

spec = json.loads(Path(sys.argv[1]).read_text())
total = 0.0
for it in spec["items"]:
    if it["type"] != "talk":
        total += float(it["dur"])
        continue
    try:
        a, b = locate_piece(it["clip"], it["text"])
    except ValueError as e:
        print("ERROR", e)
        continue
    total += b - a
    print(f"{it['clip']} {a:8.2f} {b:8.2f} {b - a:5.1f}s  {it['text'][:70]}")
print("total", round(total, 1))
