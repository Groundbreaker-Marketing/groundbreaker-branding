import json, re, sys
P = sys.argv[1]
w = json.load(open(P + '/02_audio/words/160057-synced.json'))['words']
singles = [118,235,274,498,546,628,666,696,716,756,759,957,1042,1115,1133,1227,1260,1319,1322,1506,1520,1579,1612,1705,2019,2026,2031,2039,2043,2198,2343,2514,2518,2532,2533,2892,2906,3143,3145,3196,3362,3380,3394,3462,3503,3557,3636,3652,3773,3842,3950,4001,4055,4100,4125,4160,4264,4397,4487,4557,4667,4819,4825,4933,5103,5137,5328,5389,5595,5655,5880,5903,5946,5979,6085,2648]
ranges = [[1490,1492],[1627,1628],[1643,1644],[1664,1670],[2628,2637],[2685,2690],[2698,2701],[2884,2886],[3692,3693],[4426,4426],[4429,4429],[5310,5311],[5410,5411]]
drop = sorted([[i, i] for i in singles] + ranges)
fix = {}
for i, x in enumerate(w):
    m = re.match(r"^(i)(('m|'ll|'ve|'d)?)(\W*)$", x['word'])
    if m:
        fix[str(i)] = 'I' + m.group(2) + m.group(4)
caps = {'kentucky': 'Kentucky', 'madisonville': 'Madisonville', 'facebook': 'Facebook', 'google': 'Google',
        'quickbooks': 'QuickBooks', 'cdl': 'CDL', 'hendrix': 'Hendricks', 'justin': 'Justin'}
for i, x in enumerate(w):
    k = re.sub(r'\W', '', x['word'].lower())
    if k in caps and x['word'][0].islower():
        fix[str(i)] = caps[k] + re.sub(r'^\w+', '', x['word'])
fix.update({'5': 'The', '6': '#2', '7': '', '8': 'Septic', '9': 'Podcast.', '89': 'grease trap',
            '2745': 'Hibu', '2746': '', '3542': 'John', '3543': 'Juvenot', '4111': 'Hibu',
            '821': 'El', '822': 'Nino', '4675': 'Sunday'})
ch = [[0, 'Why he went back to pumping septic tanks and grease traps'],
      [853, 'Buying a 30-year-old septic company in 2012'],
      [1432, 'Learning the business side the hard way'],
      [1905, 'Stay in your lane before you buy the next truck'],
      [2480, 'Grease traps and the residential roller coaster'],
      [3360, 'Reminder lists, neighbor discounts and calling your own customers'],
      [4437, 'Senior, military and neighbor discounts'],
      [4620, 'The tornado and helping Dawson Springs'],
      [5010, 'Trucking routes, $6 fuel and raising prices'],
      [5480, 'Hiring drivers in a family-run crew'],
      [5870, 'The one piece of advice: be a problem solver']]
titles = ["Why a Kentucky Septic Owner Quit Installs and Stuck to Pumping",
          "Bought a Septic Company in 2012? What He'd Do Differently",
          "Full Service or Just Pumping? Advice From a Kentucky Septic Owner",
          "How a Septic Pumper Evens Out the Phone Roller Coaster",
          "Stay in Your Lane: A Septic Owner on Pumping and Grease Traps"]
desc = """Justin Gamblin, owner of Hendricks Septic Tank Service Inc. in Madisonville, Kentucky, joins me to talk about going back to basics. He bought the company in 2012 from the man who started it, tried installs, repairs, drain cleaning and dewatering, and today he runs a three-person family crew that just pumps septic tanks and grease traps.

A lot of you feel pressure to be full service, so we dig into what he gave up, why the numbers made the decision easy, and how he keeps the phones steady when residential calls come in waves.

What we cover:
- Why he stopped doing installs and repairs and went back to pumping
- Buying an established septic company, and what he would tell the next buyer
- Why you only add a new service when the numbers line up first
- Evening out the roller coaster with reminder lists, outbound calls and neighbor discounts
- Senior and military discounts, and why people ask for them
- Helping out after the Dawson Springs tornado
- Routing trucks for fuel, and raising prices when you are behind
- Hiring CDL drivers and running a family crew
- His one piece of advice: be a problem solver

Find Justin at hendricksseptictankservice.com."""
d = {"_how": "Recipe for podcast.episode (video-machine). Guest episode, Justin Gamblin of Hendricks Septic Tank Service Inc. (Madisonville, Kentucky; the booking has his name and email only, the company's site names no owner), recorded on Zoom 2026-11-03 (meeting 82637989347, one part, 160057, 1280x720 at 25 fps; no AI upscale at 720p). Justin joined by phone: Zoom shows him as 'iPhone (2)' in a portrait picture inside black bars. keep = inclusive word-index ranges of 02_audio/words/160057-synced.json; drop = stammered repeats and false starts; fillers drop automatically; fixes = word index -> caption text (I casing, Kentucky, Hibu, Juvenot, grease trap). Source is 01_footage/zoom-160057-synced.mov: Justin's voice measured 55 ms behind his lips, so his Zoom track is remixed 55 ms earlier (podcast.avsync apply).",
     "slug": "stay-in-your-lane", "title": titles[0], "title_options": titles,
     "takes": {"160057": {"source": "01_footage/zoom-160057-synced.mov", "words": "02_audio/words/160057-synced.json"}},
     "keep": [[0, len(w) - 1, "160057"]],
     "drop": {"160057": drop}, "fixes": {"160057": fix}, "fillers": True,
     "lower_third": {"y": 970, "people": [{"name": "Ashley Christian", "org": "Groundbreaker Marketing", "at": 12.0},
                                          {"name": "Justin Gamblin", "org": "Hendricks Septic Tank Service", "at": 33.0}]},
     "chapters": [[i, "160057", t] for i, t in ch],
     "publish": {"approved": False,
                 "youtube": {"title": titles[0], "description": desc,
                             "playlist_id": "PLCj0Nkh3V00C-S17nnEE4psF-DgefPWh4", "category": "EDUCATION",
                             "tags": ["septic", "septic business", "septic pumping", "grease trap", "grease trap cleaning",
                                      "buying a septic company", "Kentucky", "Hendricks Septic Tank Service", "The #2 Septic Podcast"]},
                 "thumbnail": "07_notes/episode/thumbnail.jpg"}}
json.dump(d, open(P + '/06_scripts/episode.json', 'w'), indent=1)
print(len(drop), len(fix))
