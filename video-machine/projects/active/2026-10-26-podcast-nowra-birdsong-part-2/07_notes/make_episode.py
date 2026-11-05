import json, os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))   # run.sh cds into video-machine
W = json.load(open('02_audio/words/c0031.json'))['words']

# Stammered repeats (first of each, from 07_notes/reps.py); emphasis repeats stay
# ("quite, quite", "way, way", "leverage. Leverage", "very very strong", "so so good", "one one for all").
single = [210, 335, 349, 400, 482, 724, 800, 947, 1003, 1174, 1211, 1301, 1350, 1735, 1785, 1814, 1828,
          2118, 2189, 2247, 2541, 2608, 2612, 3197, 4153, 4269, 4270, 4277, 4476, 4479, 4495, 4597, 4598,
          4645, 4649, 4691, 4692, 4912, 4983, 5009, 5120, 5142, 5434, 5465, 5490, 5766, 5774, 5781]
drops = [[i, i] for i in single]
drops += [[445, 446],      # "such a such a big key"
          [4162, 4164],    # "do you do do you do holiday bonuses"
          [5115, 5116],    # "have that have that willingness"
          [5226, 5228]]    # "you gets you you would get"
drops.sort()
# First render (episode_cuts.json): these joins landed on speech, not silence (words run together), so
# the stammer stays in the audio and is only hidden from the captions: smoother than a hard cut.
PLAYED = [[335, 335], [400, 400], [4162, 4164], [4476, 4476], [4479, 4479], [4597, 4597], [4598, 4598],
          [5115, 5116], [5226, 5228]]
drops = [d for d in drops if d not in PLAYED]

fixes = {}
SIMPLE = {"i": "I", "i'm": "I'm", "i'll": "I'll", "i've": "I've", "i'd": "I'd", "hvac": "HVAC",
          "ai": "AI", "jason": "Jason", "ceo": "CEO", "ebitda": "EBITDA", "cpa": "CPA", "kpis": "KPIs",
          "kpi": "KPI", "tv": "TV"}
for i, x in enumerate(W):
    core = re.sub(r'[^A-Za-z\']', '', x['word'])
    low = core.lower()
    if low in SIMPLE and core != SIMPLE[low]:
        fixes[str(i)] = x['word'].replace(core, SIMPLE[low])
# NAWT (National Association of Wastewater Technicians; Jason is its president, nawt.org officers page),
# heard by Whisper as "not". OOWA = Oklahoma Onsite Wastewater Association, heard as "UWA".
for i in (26, 5464, 5478, 5490, 5491, 5602, 5670, 5783):
    fixes[str(i)] = W[i]['word'].lower().replace('not', 'NAWT')
fixes["37"] = "OOWA"
fixes.update({
    "2790": "55%", "2791": "", "2792": "", "2793": "",     # "50 % 5 %" (he says fifty-five percent)
    "3880": "SPIFF", "4144": "SPIFF",                       # sales incentive ("SPF program")
    "4047": "TV",                                           # "a tiki commercial": "you're looking at the TV"
    "4689": "Kevin", "4690": "Harrington's", "4694": "Grant", "4695": "Cardones,",
    "5306": "Alcoholics", "5307": "Anonymous",
    "5522": "O&M,",                                         # "Owen operations and maintenance"
    "1973": "P&L,", "1974": "",
})
for a, b in PLAYED:
    for i in range(a, b + 1):
        fixes[str(i)] = ""
# hyphenated words and percents come out as two tokens ("break" "-even", "20" "%"): join them
for i in range(1, len(W)):
    t = W[i]['word'].strip()
    if (t.startswith('-') or t == '%') and str(i) not in fixes:
        k = i - 1
        while k > 0 and fixes.get(str(k)) == "":     # "day" "-to" "-day": join onto the first
            k -= 1
        fixes[str(k)] = fixes.get(str(k), W[k]['word']) + t
        fixes[str(i)] = ""
# capitalize the first word of a sentence when Whisper lowercased it
for i, x in enumerate(W):
    prev = W[i - 1]['word'] if i else '.'
    cur = fixes.get(str(i), x['word'])
    if cur and prev.rstrip().endswith(('.', '?', '!')) and cur[0].islower():
        fixes[str(i)] = cur[0].upper() + cur[1:]

chapters = [
    [0, "c0031", "Why so many septic owners don't know their numbers"],
    [128, "c0031", "The cash-is-king wake-up call"],
    [903, "c0031", "Why Jason meets with his CPA every week"],
    [1111, "c0031", "Your break-even number, for the month and for every job"],
    [2058, "c0031", "Cash flow, reserves and leverage"],
    [2321, "c0031", "Setting prices from your numbers"],
    [3076, "c0031", "Targets, shared numbers and bonuses tied to KPIs"],
    [4377, "c0031", "Where to start, and why you should want to pay taxes"],
    [5005, "c0031", "Stop the limiting beliefs"],
    [5449, "c0031", "What NAWT does for the septic industry"],
]

titles = [
    "Do You Know Your Septic Company's Break-Even Number? (Part 2 of 2)",
    "Why a $6 Million Septic Company Meets With Its CPA Every Week (Part 2 of 2)",
    "Price Is Never the Problem: Know Your Septic Numbers (Part 2 of 2)",
    "Why This Septic Owner Wants to Pay More Taxes (Part 2 of 2)",
    "Know Your Numbers: Lessons From JT Services (Part 2 of 2)",
]

rec = {
    "_how": "Recipe for podcast.episode (video-machine). Part 2 of 2 of the NOWRA booth series with Jason Birdsong of JT Services, recorded in person 2026-10-26 at 12:34 CT at the NOWRA Mega-Conference, right after Part 1 (2026-10-26-podcast-nowra-birdsong): same setup, Jason on the left, Ashley Christian on the right, one static wide shot. One take, c0031 = Sony C0031.MP4 (1920x1080, 29.97 fps, two wireless mics: LEFT channel Ashley, RIGHT channel Jason). No B-roll. keep = inclusive word-index ranges of 02_audio/words/c0031.json; drop = stammered repeats (first of each, from 07_notes/reps.py; emphasis repeats stay). fixes = word index -> caption text: NAWT (National Association of Wastewater Technicians, heard as 'not'; Jason is its president per nawt.org), OOWA (Oklahoma Onsite Wastewater Association, heard as 'UWA'), SPIFF, 55%, O&M, joined hyphens and percents, lowercase i/cpa/kpis/tv. 'a sold hour tool' (word 1903) is left as heard: the tool's name is not confirmed. Generated by 07_notes/make_episode.py from the indexed transcript.",
    "slug": "know-your-numbers",
    "title": titles[0],
    "title_options": titles,
    "fps": "30000/1001",
    "takes": {"c0031": {"source": "01_footage/c0031.mp4", "words": "02_audio/words/c0031.json"}},
    "keep": [[0, len(W) - 1, "c0031"]],
    "drop": {"c0031": drops},
    "fixes": {"c0031": fixes},
    "fillers": True,
    "lower_third": {
        "y": 970,
        "people": [
            {"name": "Ashley Christian", "org": "Groundbreaker Marketing", "cx": 1620,
             "show": [[0, "c0031", 6.0], [5449, "c0031", 5.0]]},
            {"name": "Jason Birdsong", "org": "JT Services", "cx": 440,
             "show": [[14, "c0031", 7.0], [128, "c0031", 6.0], [5477, "c0031", 6.0]]},
        ],
    },
    "chapters": chapters,
}
old = {}
if os.path.exists('06_scripts/episode.json'):
    old = json.load(open('06_scripts/episode.json'))
for k in ("thumbnail", "publish", "grade"):   # keep blocks written after the first run
    if k in old:
        rec[k] = old[k]
json.dump(rec, open('06_scripts/episode.json', 'w'), indent=1)
print(len(drops), 'drops', len(fixes), 'fixes')
