import json, sys
P = sys.argv[1]
gamma = float(sys.argv[2])
bright = float(sys.argv[3])
f = P + '/06_scripts/episode.json'
d = json.load(open(f))
th = d['thumbnail']
old_lines = th.get('variants', {}).get('lane', {}).get('lines') or th['lines']
th.setdefault('variants', {})
th['variants']['lane'] = {
    "note": "the first two-person version (headline Stay in your lane, nobody brightened), 2026-11-12 job #140",
    "lines": old_lines, "guest": {"brighten": 1.0, "gamma": 1.0}, "out": "07_notes/episode/thumbnail-lane.jpg"}
th['lines'] = [["SEPTIC PUMPING", "big"], ["IS A", "big"], ["TRUCKING", "box"], ["BUSINESS.", "box"],
               ["RUN IT", "big"], ["LIKE ONE.", "big"]]
th['guest'] = {"at": 1257.0, "gamma": gamma, "brighten": bright}
json.dump(d, open(f, 'w'), indent=1)
print(th['lines'], th['guest'])
