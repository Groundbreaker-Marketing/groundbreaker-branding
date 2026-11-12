import json, sys
P = sys.argv[1]
f = P + '/06_scripts/episode.json'
d = json.load(open(f))
undo = [[1490, 1492], [1664, 1670], [2884, 2886]]
d['drop']['160057'] = [r for r in d['drop']['160057'] if r not in undo]
fx = d['fixes']['160057']
for a, b in undo:
    if a == 1490:
        continue  # kept as spoken ("I would definitely probably")
    for i in range(a, b + 1):
        fx[str(i)] = ''
fx['1663'] = 'So'
fx['1671'] = 'the'
d['chapters'][1][2] = 'Buying the company from the man who started it'
d['_how'] += " Three phrase drops that landed inside loud speech (1490-1492, 1664-1670, 2884-2886) stay in the audio; the two later ones are hidden from the captions with \"\" fixes."
json.dump(d, open(f, 'w'), indent=1)
print(len(d['drop']['160057']))
