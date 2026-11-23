import json, sys
P = '/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-13-podcast-episode/'
w = json.load(open(P + '02_audio/words/135607-synced.json'))['words']
spans = [(1288, 1300), (1380, 1412), (1420, 1432), (1520, 1546), (2196, 2212), (2325, 2340),
         (2540, 2548), (2600, 2640), (3720, 3730), (3735, 3745), (3960, 3980), (4150, 4180),
         (6505, 6520), (8200, 8225), (8240, 8250), (6905, 6920)]
for a, b in spans:
    print(a, ' '.join('%d:%s(%.1f)' % (n, w[n]['word'], w[n]['start']) for n in range(a, b)))
