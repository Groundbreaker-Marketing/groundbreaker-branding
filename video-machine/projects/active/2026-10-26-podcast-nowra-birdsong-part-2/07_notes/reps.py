import json, os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))   # run.sh cds into video-machine
# Consecutive identical words (stammered repeats): (index of the first, word, second, next word)
W = json.load(open('02_audio/words/c0031.json'))['words']
n = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
r = []
for i in range(1, len(W)):
    if n(W[i]['word']) == n(W[i - 1]['word']) and n(W[i]['word']):
        r.append((i - 1, W[i - 1]['word'], round(W[i - 1]['start']), n(W[i + 1]['word']) if i + 1 < len(W) else ''))
for x in r:
    print(x)
print(len(W), 'words')
