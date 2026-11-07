import json, os, re, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W = json.load(open('02_audio/words/c0021.json'))['words']
pat = re.compile(sys.argv[1], re.I)
for i, x in enumerate(W):
    if pat.search(x['word']):
        print(i, '%.1f' % x['start'], ' '.join(w['word'] for w in W[max(0, i - 3):i + 4]))
