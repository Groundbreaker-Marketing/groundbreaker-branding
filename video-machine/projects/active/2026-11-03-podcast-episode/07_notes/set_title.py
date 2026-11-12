import json, sys
P = sys.argv[1]
f = P + '/06_scripts/episode.json'
d = json.load(open(f))
t = "Septic Pumping Is a Trucking Business. Run It Like One."
d['title_options'] = [t] + [o for o in d['title_options'] if o != t]
d['title'] = t
d['publish']['youtube']['title'] = t
json.dump(d, open(f, 'w'), indent=1)
print(d['title_options'])
