import json
W = json.load(open('02_audio/words/c0030.json'))['words']
ep = json.load(open('06_scripts/episode.json'))
labs = json.load(open('07_notes/labels.json'))
epfix = ep['fixes']['c0030']
single = [d[0] for d in ep['drop']['c0030'] if d[0] == d[1] and d[0] not in (104,)]
EP = "{episode}"
# Edges measured on Jason's own (right) channel in 07_notes/edges.py: Whisper's start/end times were
# early or late by up to 0.3 s; trim_start < 0 starts earlier, > 0 skips the tail of the word before.
TS = {"repo-man": -0.25, "prison": 0.12, "one-is-none": 0.15, "promoted-best-tech": 0.07,
      "electrical-last": -0.22, "no-shoulder-season": -0.1, "saying-no": -0.2}
EPAD = {"repo-man": 0.08, "prison": 0.12, "get-on-your-phone": 0.1, "one-is-none": 0.08,
        "promoted-best-tech": 0.08, "master-experts": 0.08, "electrical-last": 0.1,
        "no-shoulder-season": 0.08, "saying-no": 0.04}
BACK = {'yeah', 'yep', 'right', 'okay', 'wow', 'interesting', 'absolutely', 'mm', 'hm', 'mhm'}

F = "Full episode: " + EP
FT = "Full episode on our YouTube: " + EP

clips = [
 dict(id="repo-man", rng=(168, 268), title="I was a *repo man*\nbefore my septic company",
  yt="From repo man to running a septic company: Jason Birdsong's story",
  yd="Jason Birdsong of {jt} was a repo man before he started the company that became JT Services. He tells how the 2008 recession made the work dangerous and pushed him to make a change so he could always come home to his family.\n\n" + F + "\n\n#septic #septicbusiness #smallbusiness",
  tt="I legally stole cars for a living. Jason Birdsong of {jt} was a repo man before he started what became a septic company. Coming out of the 2008 recession, people were losing their houses, their cars and their jobs, and the work got dangerous. He knew something had to change so he could always come home to his family. When did you know it was time for a change?\n\n" + FT + "\n\n#septic #septicbusiness #repoman #smallbusiness",
  ig="I legally stole cars for a living.\n\nThat's how Jason Birdsong of {jt} describes his life before the septic business. He was a repo man. After 2008, people were losing their houses, cars and jobs, and the work got dangerous. He knew something had to change so he could always come home to his family.\n\n" + F + "\n\n#septic #septicbusiness #repoman #smallbusiness #septicowner",
  fb="Before Jason Birdsong started JT Services, he was a repo man. He says it plainly: he legally stole cars for a living. Then came the 2008 recession. People were losing their houses, their cars and their jobs, and the work got dangerous. He had a little girl at home and knew something had to change so he could always come home to his family. He grew up on a farm and a ranch and knew a little about machinery, so he started a septic company. Have you ever had to change careers for your family?\n\n#septic #smallbusiness",
  when="2026-11-10T17:00:00", nets=["youtube","tiktok","instagram","facebook"], cover=8),
 dict(id="prison", rng=(802, 915), title="Is your septic business\na *prison* with your name on it?",
  yt="Is your septic business a prison with your name on it?",
  yd="Jason Birdsong of {jt} on why so many people go into business for freedom and end up building a prison with their name on it. Instead of owning the business, the business owns and runs you, and the way out is going from the guy in the trench to a CEO mindset.\n\n" + F + "\n\n#septic #septicbusiness #businessowner",
  tt="So many people start a business for freedom and quickly find they've built a prison with their name on it. Jason Birdsong of {jt} says instead of owning the business, the business owns and runs you. It's not a bad problem. You just don't know what you don't know. Going from the guy in the trench to a CEO mindset is the hard part. Agree?\n\n" + FT + "\n\n#septic #septicbusiness #ceomindset #businessowner",
  ig="You're building a prison with your name on it.\n\nJason Birdsong of {jt} says so many people go into business for freedom, whether that's financial freedom or time freedom. Then the business ends up owning and running them. The hardest lesson is going from the guy in the trench to a CEO mindset. Agree?\n\n" + F + "\n\n#septic #septicbusiness #ceomindset #businessowner #smallbusiness",
  fb="Most of us start a business for freedom. Financial freedom, time freedom. Jason Birdsong of JT Services says a lot of owners quickly realize they've built a prison with their name on it. Instead of owning the business, the business owns and runs you. He says that's one of the hardest lessons, and it's not a bad problem. You just don't know what you don't know. Getting from the guy in the trench to a CEO mindset takes a skill set most of us were never taught. Sound familiar?\n\n#septic #smallbusiness",
  when="2026-11-09T17:00:00", nets=["youtube","tiktok","instagram","facebook"], cover=10),
 dict(id="get-on-your-phone", rng=(1043, 1164), title="She said get off the phone.\nNow: *get on it*",
  yt="The mindset shift that helped a septic owner stop being the guy in the field",
  yd="Jason Birdsong of {jt} on the nights he spent on his phone and what his wife used to say about it. Now she tells him to get on it and make more money. What changed was what he calls changing the channel, from the guy in the field to a CEO.\n\n" + F + "\n\n#septic #septicbusiness #mindset",
  tt="My wife used to say get off your phone and pay attention to your family. Now she says get on your phone and make more money. Jason Birdsong of {jt} says the phone didn't change. His mindset did. He calls it changing the channel, from the guy in the field to a CEO instead of the doer. That's when you can start to grow and scale.\n\n" + FT + "\n\n#septic #septicbusiness #mindset #ceomindset",
  ig=None, fb=None,
  when="2026-11-09T15:00:00", nets=["youtube","tiktok"], cover=None),
 dict(id="one-is-none", rng=(3122, 3300), title="In a septic business,\none is none,\ntwo is *some*",
  yt="One is none, two is some: how a septic company adds a service line",
  yd="Jason Birdsong of {jt} on a hard lesson from adding plumbing to a septic company: one is none, two is some. He needed two plumbers and enough work to keep them busy before he would think about the next trade.\n\n" + F + "\n\n#septic #septicbusiness #hiring",
  tt="One is none, two is some. Jason Birdsong of {jt} learned it adding plumbing to his septic company. He had three full-time septic service experts, then brought on one plumber. Sometimes that one doesn't work out, and now you're back to none while you're working hard to book calls. So he made sure he had two plumbers, and kept them busy, before adding anything else. Do you hire before you need to?\n\n" + FT + "\n\n#septic #septicbusiness #hiring #smallbusiness",
  ig="One is none, two is some.\n\nJason Birdsong of {jt} learned it adding plumbing to his septic company. Bring on one plumber and sometimes it doesn't work out, and now you're back to none while you're working hard to book those calls. So he made sure he had two plumbers, and kept them busy, before he'd entertain another trade. Agree?\n\n" + F + "\n\n#septic #septicbusiness #hiring #smallbusiness #septicowner",
  fb="You work hard to book the calls, and then you don't have a plumber. That's what Jason Birdsong of JT Services ran into when he added plumbing to his septic company. He brought on one plumber, and sometimes that one doesn't work out, so now you're back to none. His lesson: one is none, two is some. He made sure he had two plumbers and kept them busy before he'd entertain adding anything else. Have you ever lost the one person you were counting on?\n\n#septic #smallbusiness",
  when="2026-11-11T15:00:00", nets=["youtube","tiktok","instagram","facebook"], cover=12),
 dict(id="promoted-best-tech", rng=(3882, 4027), title="Promoting your best tech\ncan *fail* them",
  yt="The mistake septic owners make when they promote their best tech",
  yd="Jason Birdsong of {jt} on a mistake he made more than once: promoting a top revenue producer without giving them the skill set to lead people. Years later he called those people to apologize.\n\n" + F + "\n\n#septic #septicbusiness #leadership",
  tt="The lesson I took from hiring people is that I didn't have the skill set to make a bunch of me's. Jason Birdsong of {jt} promoted top revenue producers because they were really good at what they do, then didn't give them the skill set to lead people. Years later he called them to apologize. Being good at the job doesn't mean you can create a bunch more of you. Agree?\n\n" + FT + "\n\n#septic #septicbusiness #leadership #hiring",
  ig="Just because you're really good at what you do doesn't mean you can create a bunch more of you.\n\nJason Birdsong of {jt} promoted top revenue producers and didn't give them the skill set to lead people. Later in life, he called them to apologize. Agree?\n\n" + F + "\n\n#septic #septicbusiness #leadership #hiring #smallbusiness",
  fb="Jason Birdsong of JT Services told me he's made this mistake several times. He had a really good person, a top revenue producer, so he promoted them. He didn't give them the skill set to lead people. Later in life, he called a few of them and said he needed to apologize, because he'd failed them. His point: being really good at what you do doesn't mean you have the skill set to create a bunch more of you. Has that ever happened where you work?\n\n#septic #smallbusiness",
  when="2026-11-12T15:00:00", nets=["youtube","tiktok","instagram","facebook"], cover=14),
 dict(id="master-experts", rng=(6139, 6258), title="Any CDL driver can\npump a *septic tank*",
  yt="Why a septic pumper should also do a plumbing inspection",
  yd="Jason Birdsong of {jt} on why he doesn't hire people who only pump septic tanks. He wants a master expert who can do a heating and cooling checkup or a 21-point plumbing inspection while they're pumping the tank.\n\n" + F + "\n\n#septic #septicpumping #septicbusiness",
  tt="With technology today, any CDL driver can pump a septic tank. Jason Birdsong of {jt} says he's not hiring that person. He wants someone who can do a heating and cooling checkup or a 21-point plumbing inspection while they're pumping. They may not do the work, but they know when something needs to be looked at by an expert. Would you hire that way?\n\n" + FT + "\n\n#septic #septicpumping #septicbusiness #hiring",
  ig="Any CDL driver can pump a septic tank.\n\nJason Birdsong of {jt} says he's hiring for something more: a tech who can do a heating and cooling checkup or a 21-point plumbing inspection while they're pumping. They may not do the work, but they know when an expert needs to look. Would you hire that way?\n\n" + F + "\n\n#septic #septicpumping #septicbusiness #hiring #septicowner",
  fb="Jason Birdsong of JT Services says he doesn't hire people who just pump septic tanks, because with technology today, any CDL driver can do that. He's hiring for what he calls master experts. His septic tech can do a plumbing inspection, and his plumber can pump. While they're pumping the tank, they can do a heating and cooling checkup or a 21-point plumbing inspection. They may not be the ones doing the work, but they know when something needs an expert. Would you hire that way?\n\n#septic #smallbusiness",
  when="2026-11-13T15:00:00", nets=["youtube","tiktok","instagram","facebook"], cover=10),
 dict(id="electrical-last", rng=(5224, 5359), title="Why *electrical* comes last\nin a home service company",
  yt="Why a septic company should add electrical last",
  yd="Jason Birdsong of {jt} wanted to start with electrical, not plumbing. After some research he found the margins are typically lowest in electrical and the repeat business is thin, so it came last.\n\n" + F + "\n\n#septic #septicbusiness #homeservices",
  tt="I actually wanted to start with electrical, not plumbing. Jason Birdsong of {jt} did the research and found that in whole-home service, the margins are typically lowest in electrical. And when was the last time you had an electrician replace a light switch? So electrical came last. It still completed the circle once he was doing generators and new HVAC systems.\n\n" + FT + "\n\n#septic #septicbusiness #homeservices #hvac",
  ig=None, fb=None,
  when="2026-11-10T15:00:00", nets=["youtube","tiktok"], cover=None),
 dict(id="no-shoulder-season", rng=(4601, 4728), title="I don't believe in\n*shoulder season*",
  yt="Is there really a shoulder season for septic and HVAC?",
  yd="Jason Birdsong of {jt} on why he doesn't believe in shoulder season. If you start your marketing soon enough, there's no lull, and waiting until the phone stops ringing is reactive marketing.\n\n" + F + "\n\n#septic #septicmarketing #septicbusiness",
  tt="Marketing is everything. Everything is marketing. Jason Birdsong of {jt} doesn't believe in shoulder season. If you start marketing early enough, there's no lull. Too many people do reactive marketing and wait until the phone's not ringing. His team starts fall messaging in July. When do you start yours?\n\n" + FT + "\n\n#septic #septicmarketing #septicbusiness #hvac",
  ig=None, fb=None,
  when="2026-11-14T15:00:00", nets=["youtube","tiktok"], cover=None),
 dict(id="saying-no", rng=(5700, 5818), title="How much money are you\nsaying *no* to?",
  yt="How much money is your septic company saying no to?",
  yd="Jason Birdsong of {jt} asks how much money you're saying no to, and what you could add on or sub out. His office staff knows that if enough calls come in for teeth work, he'll hire a dentist.\n\n" + F + "\n\n#septic #septicbusiness #homeservices",
  tt="How much money are you saying no to? Jason Birdsong of {jt} tells his office staff that if they get enough calls for teeth work, he'll hire a dentist. What are you turning away that you could add on or sub out? He has partnerships where they sell it and take a percentage. On a bathroom remodel, they do the plumbing and a contractor does the rest. It's a win-win.\n\n" + FT + "\n\n#septic #septicbusiness #homeservices #smallbusiness",
  ig=None, fb=None,
  when="2026-11-15T15:00:00", nets=["youtube","tiktok"], cover=None),
]

out = []
for c in clips:
    lo, hi = c['rng']
    # drop the other speaker's short interjections (<= 4 words) by splitting the keep range
    cut = set()
    i = lo
    while i <= hi:
        if labs[i] == 'ASHLEY':
            j = i
            while j <= hi and labs[j] == 'ASHLEY':
                j += 1
            words = [''.join(ch for ch in W[k]['word'].lower() if ch.isalpha()) for k in range(i, j)]
            if j - i <= 4 and i > lo and j <= hi and all(w in BACK for w in words):
                cut.update(range(i, j))
                print(c['id'], 'host interjection', i, ' '.join(W[k]['word'] for k in range(i, j)))
            i = j
        else:
            i += 1
    keep = []
    s = None
    for k in range(lo, hi + 1):
        if k in cut:
            if s is not None:
                keep.append([s, k - 1]); s = None
        elif s is None:
            s = k
    if s is not None:
        keep.append([s, hi])
    fixes = {}
    for k in range(lo, hi + 1):
        if str(k) in epfix:
            fixes[str(k)] = epfix[str(k)]
        if k in single and k not in cut:
            fixes[str(k)] = ""
    norm = lambda s: ''.join(ch for ch in s.lower() if ch.isalnum())
    for k in range(lo, hi - 2):
        if norm(W[k]['word']) == norm(W[k + 2]['word']) and norm(W[k + 1]['word']) == norm(W[k + 3]['word']) and k not in cut:
            fixes[str(k)] = ""
            fixes[str(k + 1)] = ""
    for k in range(lo, hi):
        nxt = W[k + 1]['word']
        if nxt.startswith('-') or nxt == '%':
            fixes[str(k)] = fixes.get(str(k), W[k]['word']) + nxt
            fixes[str(k + 1)] = ""
    if c['id'] == 'repo-man':
        fixes['193'] = "I"
        fixes['194'] = ""
    first = W[lo]['word']
    cur = fixes.get(str(lo), first)
    if cur and cur[0].islower():
        fixes[str(lo)] = cur[0].upper() + cur[1:]
    clip = {"id": c['id'], "source": "01_footage/c0030.mp4", "words": "02_audio/words/c0030.json",
            "keep": keep, "title": c['title'],
            "youtube": {"title": c['yt'], "description": c['yd']},
            "approved": False, "fixes": fixes, "layout": "crop", "crop_x": 0.23,
            "publish_at": c['when'], "networks": c['nets']}
    caps = {"tiktok": c['tt']}
    if c['ig']:
        caps["instagram"] = c['ig']
        caps["facebook"] = c['fb']
    clip["captions"] = caps
    if c['id'] in TS:
        clip['trim_start'] = TS[c['id']]
    if c['id'] in EPAD:
        clip['end_pad'] = EPAD[c['id']]
    if c['cover'] is not None:
        clip["cover_at"] = round(W[lo]['start'] + c['cover'], 1)
    out.append(clip)
    print(c['id'], keep, ' '.join(fixes.get(str(k), W[k]['word']) for k in range(lo, hi + 1) if k not in cut and fixes.get(str(k), W[k]['word']) != ''))
    print()

rec = {
    "_how": "Recipe for shorts.build (video-machine). 9 clips from Part 1 of 2 of the NOWRA booth series with Jason Birdsong of JT Services (take c0030, Sony 1920x1080 at 29.97 fps, one static wide shot: Jason left, Ashley right; two wireless mics, LEFT channel Ashley, RIGHT channel Jason). keep = inclusive word-index ranges of 02_audio/words/c0030.json in play order; the host's 1 to 4 word interjections are split out; stammers stay in the audio and are hidden from the captions with \"\" fixes; fillers skip automatically; max_gap 1.0. layout crop at 0.23 (Jason's center; every clip is his answer). mono: true mixes the two mics into both ears. Posting plan: Part 1 releases Monday 2026-11-09 (special episode, 8:00 CT); Part 2 releases Wednesday 2026-11-11 and its own Shorts post that week, so these clips leave the noon and 5 PM slots alone from Wednesday on: Mon and Tue at 3 PM and 5 PM (noon on those days is the Bismarck Shorts), then one a day at 3 PM Wed to Sun. Every clip goes to YouTube and TikTok; the five strongest (repo-man, prison, one-is-none, promoted-best-tech, master-experts) also to Instagram and Facebook, Mon/Tue 5 PM and Wed to Fri 3 PM (move them if Ashley wants one Instagram post a day once Part 2's are planned). Captions: one per network; {jt} tags JT Services (jtserviceco.com lists no social accounts, so it is a plain name), the full episode linked ({episode}) everywhere but Facebook. approved = Ashley approved it in Ops. Generated by 07_notes/make_shorts.py.",
    "fillers": True, "max_gap": 1.0, "mono": True,
    "guests": {"jt": {"name": "Jason Birdsong of JT Services"}},
    "cover_with": "with Jason Birdsong of JT Services",
    "clips": out,
}
json.dump(rec, open('06_scripts/shorts.json', 'w'), indent=1)
