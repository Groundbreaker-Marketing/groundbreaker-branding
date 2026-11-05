import json, re
W = json.load(open('02_audio/words/c0030.json'))['words']
n = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
r = []
for i in range(1, len(W)):
    if n(W[i]['word']) == n(W[i - 1]['word']) and n(W[i]['word']):
        r.append((i - 1, W[i - 1]['word'], round(W[i - 1]['start']), n(W[i + 1]['word']) if i + 1 < len(W) else ''))
print(r)
print([(i, W[i]['word']) for i in range(6638, 6658)])
print([(i, W[i]['word']) for i in range(0, 36)])
