import json, os, re, sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))   # run.sh cds into video-machine
# python 07_notes/look.py 120-180 word ...   print word ranges with indexes, or find a word
W = json.load(open('02_audio/words/c0031.json'))['words']
for a in sys.argv[1:]:
    if re.fullmatch(r'\d+-\d+', a):
        lo, hi = map(int, a.split('-'))
        print(a, ' '.join('%d:%s' % (i, W[i]['word']) for i in range(lo, hi + 1)))
    else:
        print(a, [(i, W[i]['word']) for i in range(len(W)) if re.sub(r'[^a-z]', '', W[i]['word'].lower()) == a])
