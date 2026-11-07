import json, os, sys
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W = json.load(open('02_audio/words/c0021.json'))['words']
# usage: look.py a b [a b ...]  -> words a..b with start/end seconds
args = [int(x) for x in sys.argv[1:]]
for a, b in zip(args[::2], args[1::2]):
    print('--', a, b)
    print(' '.join('%d:%s(%.2f-%.2f)' % (i, W[i]['word'], W[i]['start'], W[i]['end']) for i in range(a, b + 1)))
