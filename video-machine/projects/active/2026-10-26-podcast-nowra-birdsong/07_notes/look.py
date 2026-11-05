import json, re, sys
W = json.load(open('02_audio/words/c0030.json'))['words']
for a in sys.argv[1:]:
    if re.fullmatch(r'\d+-\d+', a):
        lo, hi = map(int, a.split('-'))
        print(a, ' '.join('%d:%s' % (i, W[i]['word']) for i in range(lo, hi + 1)))
    else:
        print(a, [(i, W[i]['word']) for i in range(len(W)) if re.sub(r'[^a-z]', '', W[i]['word'].lower()) == a])
