import json, os
# 2026-11-04 (Part 2's job): the intro's "president of NOT" is NAWT, the National Association of
# Wastewater Technicians (nawt.org lists Jason Birdsong as president). Put the clause back, caption it
# NAWT, and name it in the YouTube description. make_episode.py carries the same change.
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
p = '06_scripts/episode.json'
e = json.load(open(p))
e['drop']['c0030'] = [d for d in e['drop']['c0030'] if d != [15, 21]]
e['fixes']['c0030']['20'] = 'NAWT,'
e['_how'] = e['_how'].replace(
    "the garbled 'president of NOT' (word 20; the organization name is not confirmed, so the clause is cut: say so in the review notes), ",
    "")
e['_how'] += " Word 20 'NOT' is NAWT (National Association of Wastewater Technicians; Jason is its president per nawt.org): the intro clause was cut on the first run and restored 2026-11-04."
yt = e['publish']['youtube']
old = "This is Part 1 of 2. Jason started out"
if old in yt['description']:
    yt['description'] = yt['description'].replace(
        old, "This is Part 1 of 2. Jason is the president of NAWT, the National Association of Wastewater Technicians. He started out")
json.dump(e, open(p, 'w'), indent=1)
print(e['drop']['c0030'][:2], e['fixes']['c0030']['20'])
print(yt['description'][:400])
