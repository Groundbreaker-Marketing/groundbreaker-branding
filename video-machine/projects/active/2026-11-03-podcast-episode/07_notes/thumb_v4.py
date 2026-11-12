import json, sys
P = sys.argv[1]
contrast = float(sys.argv[2])
bright = float(sys.argv[3])
f = P + '/06_scripts/episode.json'
d = json.load(open(f))
th = d['thumbnail']
v = th.setdefault('variants', {})
v['lane']['guest'] = {"brighten": 1.0, "gamma": 1.0, "contrast": 1.0}
if 'trucking-v2' not in v:
    v['trucking-v2'] = {
        "note": "round 2 (job #144): the full title as the headline, SEPTIC PUMPING on one row; Justin gamma 1.5, brighten 1.15, no contrast",
        "lines": [["SEPTIC PUMPING", "big"], ["IS A", "big"], ["TRUCKING", "box"], ["BUSINESS.", "box"],
                  ["RUN IT", "big"], ["LIKE ONE.", "big"]],
        "guest": {"gamma": 1.5, "brighten": 1.15, "contrast": 1.0}, "out": "07_notes/episode/thumbnail-trucking-v2.jpg"}
th['lines'] = [["PUMPING IS A", "big"], ["TRUCKING", "box"], ["BUSINESS.", "box"], ["RUN IT", "big"], ["LIKE ONE.", "big"]]
th['guest'] = {"at": 1257.0, "gamma": 1.5, "brighten": bright, "contrast": contrast}
json.dump(d, open(f, 'w'), indent=1)
print(th['lines'], th['guest'])
