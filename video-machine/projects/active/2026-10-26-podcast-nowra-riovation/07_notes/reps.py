import json, os, re, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W = json.load(open('02_audio/words/c0021.json'))['words']
n = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
r = []
for i in range(1, len(W)):
    if n(W[i]['word']) == n(W[i - 1]['word']) and n(W[i]['word']):
        ctx = ' '.join(x['word'] for x in W[max(0, i - 3):i + 4])
        gap = round(W[i]['start'] - W[i - 1]['end'], 2)
        r.append((i - 1, W[i - 1]['word'], round(W[i - 1]['start']), gap, ctx))
for x in r:
    print(x)
print(len(r))
print([(i, W[i]['word']) for i in range(4020, len(W))])
