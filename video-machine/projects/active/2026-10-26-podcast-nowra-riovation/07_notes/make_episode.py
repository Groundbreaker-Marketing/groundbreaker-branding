import json, os, re
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
W = json.load(open('02_audio/words/c0021.json'))['words']
N = len(W)

# stammered repeats: the first of each pair (07_notes/reps.py). Kept: emphasis ("very, very", "very very",
# "pretty pretty common"), and "yeah yeah" pairs that are two people answering each other.
single = [178, 204, 225, 248, 330, 399, 407, 452, 470, 523, 549, 657, 747, 807, 867, 894, 1056, 1100, 1148,
          1252, 1333, 1358, 1369, 1381, 1383, 1463, 1861, 1938, 1970, 2335, 2657, 2728, 2969, 3067, 3106,
          3338, 3340, 3378, 3389, 3407, 3441, 3444, 3491, 3543, 3558, 3733, 3736, 3794, 3927, 3969, 3979]
drops = [[i, i] for i in single]
drops += [[131, 132]]            # "thanks for thanks for having me"
drops += [[1256, 1256]]          # Ashley's stray "provide" while he answers
drops += [[2275, 2280]]          # "once the product is installed so" false start; the retake follows
drops += [[2286, 2286]]          # "it aeration product" -> "the aeration product"
drops += [[3735, 3742]]          # "willing to to try new technology so be" -> the clean "willing to try new technology"
drops.sort()

fixes = {}
SIMPLE = {"i": "I", "i'm": "I'm", "i'll": "I'll", "i've": "I've", "i'd": "I'd", "rv": "RV", "atu": "ATU",
          "bod": "BOD", "tss": "TSS", "florida": "Florida", "texas": "Texas", "liberia": "Liberia",
          "ghana": "Ghana", "gig": "Gig", "alabama": "Alabama", "purdue": "Purdue", "pvc": "PVC",
          "diy": "DIY", "nowra": "NOWRA", "stephen": "Stephen", "oh": "oh"}
for i, x in enumerate(W):
    core = re.sub(r"[^A-Za-z']", '', x['word'])
    low = core.lower()
    if low in SIMPLE and core != SIMPLE[low]:
        fixes[str(i)] = x['word'].replace(core, SIMPLE[low])

# glue words the transcript split around punctuation: "u" ".s" -> "U.S.", "$25" ",000" -> "$25,000",
# "three" "-quarter", "R" "&D", "reovation" ".com."
for i in range(N - 1):
    nxt = W[i + 1]['word']
    if len(nxt) > 1 and nxt[0] in ".,-&%" and str(i) not in fixes:
        cur = W[i]['word']
        if cur.lower() == 'u':
            cur = 'U'
        fixes[str(i)] = cur + nxt
        fixes[str(i + 1)] = ""
for i in (301, 630):
    fixes[str(i)] = "U.S."
for i in (2610, 3811):                 # "U .S.," / "U .S." already carry their period
    pass
fixes.update({
    "6": "#2", "7": "",                              # "the number two septic podcast"
    "21": "Moeller.",                                # heard as "Miller": spelling from riovation.com/about-us
    "159": "RioVation", "332": "RioVation", "352": "RioVation",   # heard as "renovation" / "reovation"
    "333": "BioMaze",
    "214": "Drewery",                                # "Gig Drury": riovation.com/about-us spells Drewery
    "222": "Hydro-Action", "223": "", "237": "Hydro-Action", "238": "", "279": "Hydro-Action", "280": "",
    "325": "R&D", "326": "", "339": "R&D", "340": "", "415": "R&D", "416": "",
    "1662": "RioVation.com.", "1663": "", "4015": "RioVation.com", "4016": "",
    "464": "University", "466": "West", "467": "Virginia",
    "511": "biomat", "512": "",
    "709": "HiBlow", "710": "", "711": "XP-80",
    "2753": "HiBlow", "2754": "",
    "3465": "HiBlow", "3466": "",
    "3520": "HiBlow", "3521": "",
    "2768": "FPZ", "3524": "FPZ",
})
# "gig drury": 213 is Gig
fixes["213"] = "Gig"
# "that" / "that" cross-talk: his answer is "That's a great question"
fixes["1253"] = "That's"
# capitalise the first word of a sentence when Whisper lowercased it
for i, x in enumerate(W):
    prev = W[i - 1]['word'] if i else '.'
    cur = fixes.get(str(i), x['word'])
    if cur and prev.rstrip().endswith(('.', '?', '!')) and cur[0].islower():
        fixes[str(i)] = cur[0].upper() + cur[1:]
if W[0]['word'][0].islower():
    fixes["0"] = W[0]['word'].capitalize()

chapters = [
    [0, "c0021", "What RioVation does and how the BioMaze started"],
    [450, "c0021", "How treated water can bring a failing drain field back"],
    [704, "c0021", "How the BioMaze works: pods, diffusers and attached growth"],
    [1155, "c0021", "When it fits a failing system, and what it costs"],
    [1606, "c0021", "How installers get started, install time and maintenance"],
    [2247, "c0021", "What a working tank looks like, and a $25,000 mound avoided"],
    [2517, "c0021", "Where it works, and the Liberia and Ghana projects"],
    [3085, "c0021", "Design help, commercial jobs and odor control"],
    [3360, "c0021", "How long the parts last"],
    [3696, "c0021", "One piece of advice: be willing to try new technology"],
]

titles = [
    "Failing Drain Field? RioVation's $5,000 Alternative to Replacement",
    "A $25,000 Mound Replacement Avoided for About $5,000",
    "Can Treating the Tank Bring a Failing Drain Field Back?",
    "Class 1 Water in Any Septic Tank: RioVation's BioMaze Explained",
    "Septic Odor Gone on Day One: RioVation's BioMaze in Liberia",
]

# B-roll: RioVation's own footage only where the talk is about it. i = word index; ss = seconds into the clip.
# Ghana's portrait phone shots sit inside black bars: cut the bars off and fill the frame over a blur.
GH_PORTRAIT = [248, 2, 354, 474]
broll = [
    # the product, as he lists the parts (booth)
    {"clip": "c0024.mp4", "i": 706, "take": "c0021", "dur": 4.5, "ss": 3.5},      # pump housing: "high blow pump with a housing and alarm package"
    # (no cutaway over 750-850: he holds the pod cluster up to the camera, which is the live demonstration)
    # his website
    {"clip": "c0026.mp4", "i": 1652, "take": "c0021", "dur": 4.0, "ss": 0.5},     # RioVation banner: "our website, riovation.com"
    # the booth video he is explaining ("I see you have a really great video behind you")
    {"clip": "trade-show-video.mp4", "i": 2281, "take": "c0021", "dur": 5.0, "ss": 7.0},    # the SBG animation: installed in the tank
    {"clip": "trade-show-video.mp4", "i": 2337, "take": "c0021", "dur": 5.0, "ss": 24.0},   # the tank aerating: "robust biofilm, attached growth"
    {"clip": "trade-show-video.mp4", "i": 2405, "take": "c0021", "dur": 5.0, "ss": 41.0},   # microscope: "rotifer, stalk ciliate, water mite"
    {"clip": "c0027.mp4", "i": 2422, "take": "c0021", "dur": 4.0, "ss": 14.5},      # the booth's microorganism chart
    {"clip": "trade-show-video.mp4", "i": 2441, "take": "c0021", "dur": 5.5, "ss": 57.0},   # the clear effluent: "a grab sample... class one water"
    # Liberia: 8,000 gallons a day (2655 to 2930)
    {"clip": "liberia-install.mp4", "i": 2660, "take": "c0021", "dur": 5.0, "ss": 0.0},    # the pod clusters
    # (no cutaway over 2740-2890 [about 947-1003 s]: he holds up the pod cluster and the PVC header on camera)
    {"clip": "liberia-install.mp4", "i": 2750, "take": "c0021", "dur": 3.5, "ss": 29.5},   # the blowers: "regenerative blowers" (just before he lifts the pods)
    {"clip": "liberia-install.mp4", "i": 2902, "take": "c0021", "dur": 3.5, "ss": 35.0},   # inside the tank: "we installed the product, day one the odor issue was resolved"
    # Ghana: 20,000 gallons a day
    {"clip": "ghana-install.mp4", "i": 2948, "take": "c0021", "dur": 4.0, "ss": 1.0, "src_crop": GH_PORTRAIT, "fill": "blur"},   # portrait: the pump going into the riser
    # the one-horsepower unit: the BMT63HS demo
    {"clip": "bmt63hs-demo.mp4", "i": 2988, "take": "c0021", "dur": 5.0, "ss": 27.0},      # the one-horsepower blower in its housing
    {"clip": "bmt63hs-demo.mp4", "i": 3016, "take": "c0021", "dur": 4.5, "ss": 15.0},      # the header over the tank
    {"clip": "ghana-install.mp4", "i": 3066, "take": "c0021", "dur": 4.5, "ss": 56.5, "src_crop": GH_PORTRAIT, "fill": "blur"},  # the jar: "BOD was 18... clear water"
    # Ghana and Liberia, standby blowers and 30 years of maintenance kits
    {"clip": "ghana-install.mp4", "i": 3600, "take": "c0021", "dur": 4.0, "ss": 19.0},    # the blowers on their pad
]

rec = {
    "_how": "Recipe for podcast.episode (video-machine). In-person NOWRA booth episode with RioVation, recorded 2026-10-26 at about 9:16 CT at the NOWRA Mega-Conference: the guest on the left of the frame, Ashley Christian on the right, one static wide shot. One take, c0021 = Sony C0021.MP4 (1920x1080, 29.97 fps, 23.3 min, two wireless mics: LEFT channel Ashley, RIGHT channel the guest). Guest: Stephen Moeller of RioVation. Ashley introduces him as 'Stephen' (heard as 'Miller'); he says he runs the business side and that Gig Drewery does R&D and engineering, so he is not Gig; riovation.com/about-us lists only Gig Drewery and Stephen Moeller (and Gig's wife Trina). The face match against the site photos could NOT be done on the Mini (no network downloads), so the name and spelling are unconfirmed by face: check before release. No title is shown: the site gives Stephen none (Ashley calls him a partner). B-roll: booth clips C0023-C0029 (C0022, 1.5 s of an aisle, and C0028, a hall, are unused) and four videos RioVation provided and licensed to us (Ghana Install, Liberia Install, 2026-01-26 Trade Show Video, BMT63HS 1 HP), used only where he talks about that footage; Ghana's portrait shots are cropped out of their black bars and filled over a blur. keep = inclusive word-index ranges of 02_audio/words/c0021.json; drop = stammered repeats (first of each, 07_notes/reps.py; emphasis repeats and two-person 'yeah yeah' stay), a stray 'provide', and two false starts. fixes = word index -> caption text (RioVation, BioMaze, Gig Drewery, Hydro-Action, HiBlow XP-80, FPZ, R&D, BOD/TSS, U.S., $25,000, joined hyphens). Generated by 07_notes/make_episode.py from the indexed transcript.",
    "slug": "riovation-biomaze",
    "title": titles[0],
    "title_options": titles,
    "fps": "30000/1001",
    "takes": {"c0021": {"source": "01_footage/c0021.mp4", "words": "02_audio/words/c0021.json"}},
    "keep": [[0, N - 1, "c0021"]],
    "drop": {"c0021": drops},
    "fixes": {"c0021": fixes},
    "fillers": True,
    "lower_third": {
        "y": 970,
        "people": [
            {"name": "Ashley Christian", "org": "Groundbreaker Marketing", "cx": 1340,
             "show": [[0, "c0021", 5.5], [4003, "c0021", 5.0]]},
            {"name": "Stephen Moeller", "org": "RioVation", "cx": 515,
             "show": [[133, "c0021", 7.0], [450, "c0021", 5.0], [4015, "c0021", 5.0]]},
        ],
    },
    "broll": broll,
    "chapters": chapters,
    "grade": True,
}
old = {}
if os.path.exists('06_scripts/episode.json'):
    old = json.load(open('06_scripts/episode.json'))
for k in ("thumbnail", "publish"):
    if k in old:
        rec[k] = old[k]
os.makedirs('06_scripts', exist_ok=True)
json.dump(rec, open('06_scripts/episode.json', 'w'), indent=1)
print(len(drops), 'drops', len(fixes), 'fixes', len(broll), 'broll')
