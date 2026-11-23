import json, re, os
P = '/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-13-podcast-episode/'
w = json.load(open(P + '02_audio/words/135607.json'))['words']
T = '135607'
fx = {}


def core(s):
    m = re.match(r"^(\W*)([A-Za-z'’]+)(\W*)$", s)
    return m.groups() if m else None


def idx_at(t):
    return min(range(len(w)), key=lambda k: abs(w[k]['start'] - t))


simple = {"i": "I", "i'm": "I'm", "i've": "I've", "i'll": "I'll", "i'd": "I'd", "florida": "Florida",
          "jobber": "Jobber", "ai": "AI", "ais": "AIs", "crm": "CRM", "crms": "CRMs", "ocd": "OCD",
          "atu": "ATU", "ged": "GED", "highlands": "Highlands", "fort": "Fort", "pierce": "Pierce",
          "sebring": "Sebring", "alabama": "Alabama", "pensacola": "Pensacola", "indiana": "Indiana",
          "daytona": "Daytona", "texas": "Texas", "okeechobee": "Okeechobee", "lehigh": "Lehigh",
          "carolina": "Carolina", "hardy": "Hardee", "peterbelts": "Peterbilts", "peterbelt": "Peterbilt",
          "kenworths": "Kenworths", "dep": "DEP", "myers": "Myers", "avon": "Avon", "placid": "Placid",
          "polk": "Polk", "martin": "Martin", "claude": "Claude", "severn": "Sebring"}
for i, x in enumerate(w):
    c = core(x['word'])
    if not c:
        continue
    a, b, z = c
    l = b.lower().replace('’', "'")
    pc = core(w[i - 1]['word']) if i else None
    nc = core(w[i + 1]['word']) if i + 1 < len(w) else None
    prev = pc[1].lower() if pc else ''
    nxt = nc[1].lower() if nc else ''
    new = None
    if l == 'chat' and nxt == 'gpt':
        new = 'ChatGPT'
    elif l == 'gpt' and prev == 'chat':
        new = ''
    elif l == 'tear' and nxt == 'lift':
        new = 'TerraLift'
    elif l == 'tear' and nxt == 'lifting':
        new = 'TerraLifting'
    elif l in ('lift', 'lifting') and prev == 'tear':
        new = ''
    elif i in (4271, 4272):
        new = ''
    elif l == 'edgy' and i == 6260:
        new = ''
    elif l == 'st' and nxt == 'louise':
        new = 'St.'
    elif l == 'louise' and prev == 'st':
        new = 'Lucie'
    elif l == 'county' and prev in ('highlands', 'lucie', 'louise', 'martin', 'hardy', 'hardee', 'polk'):
        new = 'County'
    elif l == 'crust' and nxt == 'busters':
        new = 'Crust'
    elif l == 'busters' and prev == 'crust':
        new = 'Busters'
    elif l == 'north' and nxt == 'carolina':
        new = 'North'
    elif l in simple:
        new = simple[l]
    if new is None:
        continue
    if new == '':
        fx[str(i)] = ''
    elif new != b:
        fx[str(i)] = a + new + z
assert w[4099]['word'] == 'Ryan' and w[4100]['word'].startswith('Grayson')
fx['4100'] = 'Gascon,'
last = len(w) - 1
ch = [(0, "How Jason started with a pickup truck and shoe polish"),
      (idx_at(180), "Why he raised his prices and went from 1 pump truck to 11"),
      (idx_at(330), "Why an A-rated company beats being the cheapest"),
      (idx_at(507), "How ChatGPT and Jobber run his septic company"),
      (idx_at(660), "The tank checklist on every invoice"),
      (idx_at(976), "Running 7 counties from 2 offices"),
      (idx_at(1164), "How he built his own wastewater treatment plant"),
      (idx_at(1594), "Why he never stops learning"),
      (idx_at(2235), "Keeping rates fair after a flood"),
      (idx_at(2355), "How to expand into a new county without burning out"),
      (idx_at(2873), "What's next, and his one piece of advice")]
titles = ["He Raised His Septic Prices and Went From 1 Pump Truck to 11",
          "Florida's Poo King: How to Run 7 Counties and 11 Pump Trucks",
          "Should You Be the Cheapest Septic Company? Jason Harris Says No",
          "How a Septic Owner Built His Own Wastewater Treatment Plant",
          "Why Jason Harris Keeps His Septic Standards High in 7 Counties"]
desc = """Jason Harris of All About Septic Services joins me to talk about what happened when he stopped being the cheapest septic company in town. He started in 2011 with a pickup truck and shoe polish on the side. After he raised his prices, he went from one pump truck to eleven, and now he serves seven counties in Florida from offices in Fort Pierce and Sebring.

Jason, who goes by Florida's Poo King, shares how he holds his crews to an A-rated standard, why every invoice carries a tank checklist, how ChatGPT and Jobber run the back office, and why he built his own wastewater treatment plant when he ran out of places to dump. We also talk about keeping rates fair after a flood and how to expand into a new county without burning out.

What we cover:
- How Jason started with a pickup truck and shoe polish in 2011
- Why he raised his prices and went from 1 pump truck to 11
- Why an A-rated company beats being the cheapest
- How ChatGPT and Jobber run his septic company
- The tank checklist his drivers fill out on every invoice
- Running 7 counties from 2 offices
- How he built his own wastewater treatment plant
- Why he never stops learning
- Keeping rates fair after a flood
- How to expand into a new county without burning out

Find All About Septic Services at allaboutsepticservices.com."""
ep = {"slug": "poo-king-prices", "title": titles[0], "title_options": titles,
      "takes": {T: {"source": "01_footage/zoom-135607-synced.mov", "words": "02_audio/words/135607-synced.json"}},
      "keep": [[0, last, T]], "drop": {}, "fixes": {T: fx}, "fillers": False,
      "lower_third": {"y": 970, "people": [
          {"name": "Ashley Christian", "org": "Groundbreaker Marketing", "at": 12.0},
          {"name": "Jason Harris", "org": "All About Septic Services Inc.", "at": 40.0}]},
      "chapters": [[i, T, t] for i, t in ch],
      "pause": {"max_gap": 1000000.0, "pre": 0.3, "post": 0.45},
      "publish": {"approved": False, "youtube": {
          "title": titles[0], "description": desc,
          "playlist_id": "PLCj0Nkh3V00C-S17nnEE4psF-DgefPWh4", "category": "EDUCATION",
          "tags": ["septic", "septic business", "septic pricing", "septic company growth",
                   "wastewater treatment plant", "Jobber", "septic pumping", "All About Septic Services",
                   "Jason Harris", "The #2 Septic Podcast"]}},
      "_how": "Recipe for podcast.episode. Guest episode, Jason Harris of All About Septic Services Inc. (allaboutsepticservices.com, Fort Pierce and Sebring, Florida), recorded on Zoom 2026-11-13 (meeting 6620561605, one part, 135607, 1280x720 at 25 fps; no AI upscale at 720p). One continuous keep, first word to last, no drops, fillers off. Caption fixes: word 4100 Grayson to Gascon (Ryan Gascon, confirmed by Ryan); words 4271 and 4272 (Zoom heard TNJD Watering, unconfirmed) are hidden from captions, the audio still says it. Lowercase Whisper words (I, Florida, Jobber, ChatGPT, county names) fixed in fixes."}
os.makedirs(P + '06_scripts', exist_ok=True)
json.dump(ep, open(P + '06_scripts/episode.json', 'w'), indent=1)
print(len(fx), ch)
