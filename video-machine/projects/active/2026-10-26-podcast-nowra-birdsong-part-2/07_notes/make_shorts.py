import json, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))   # run.sh cds into video-machine
W = json.load(open('02_audio/words/c0031.json'))['words']
ep = json.load(open('06_scripts/episode.json'))
labs = json.load(open('07_notes/labels.json'))
epfix = ep['fixes']['c0031']
dropped = set(i for a, b in ep['drop']['c0031'] for i in range(a, b + 1))
EP = "{episode}"
JASON_X, ASHLEY_X = 0.23, 0.74
# Edges measured on each speaker's own channel with 07_notes/edges.py (Whisper's times run early or
# late by up to 0.3 s): trim_start < 0 starts earlier, > 0 skips the tail of the word before;
# end_pad lets the last word finish. Every clip ends on Jason, so end_channel "right" keeps only his
# mic from the last word on (Ashley's "yeah" can't force the cut).
# First render, re-transcribed (07_notes/check_renders.py): every clip opened on its first word and
# closed after its last, except bonus-bob ("bonuses" heard as "bonus"). Openings with a pause before
# them start a little earlier so the first syllable isn't clipped; the rest start right after the word
# before. Every ending gets a short pad; bonus-bob enough to finish its last word.
TS = {"break-even-job": -0.15, "disposal-crisis": -0.15, "hourly-rate": -0.12, "cpa-every-week": 0.04}
EPAD = {"break-even-job": 0.15, "price-never-problem": 0.12, "cover-payroll": 0.08, "cpa-every-week": 0.12,
        "cash-is-king": 0.12, "pay-more-taxes": 0.12, "bonus-bob": 0.3, "disposal-crisis": 0.12,
        "hourly-rate": 0.12}
BACK = {'yeah', 'yep', 'right', 'okay', 'wow', 'interesting', 'absolutely', 'mm', 'hm', 'mhm', 'hmm'}

F = "Full episode: " + EP
FT = "Full episode on our YouTube: " + EP

clips = [
 dict(id="break-even-job", keep=[(1463, 1504), (1514, 1521), (1523, 1543), (1560, 1670)],
  crop_at=[[1535, ASHLEY_X], [1540, JASON_X]],
  title="Do you know your break-even\non a *septic* job?",
  yt="Are you losing money on septic jobs? Know your break-even number",
  yd="Jason Birdsong of {jt} walks through an aerobic treatment unit call: leave with a $99 diagnostic and you've lost money, do the job at your $500 break-even and you still paid the bills. Part 2 of our conversation is all about knowing your numbers.\n\n" + F + "\n\n#septic #septicbusiness #knowyournumbers",
  tt="If you leave a job with a $99 diagnostic, you lost money. Jason Birdsong of {jt} says once you count the fuel, the time and the call center, $99 doesn't cover it. Do the same job at your $500 break-even and you kept the lights on. Breaking even isn't losing. Do you know your break-even on a job? Agree?\n\n" + FT + "\n\n#septic #septicbusiness #knowyournumbers #smallbusiness",
  ig="Breaking even isn't losing.\n\nJason Birdsong of {jt} says if you leave an aerobic unit call with a $99 diagnostic, you lost money once you count the fuel, the time and the call center. Do it at your $500 break-even and you still paid the bills and kept your tech's family fed. Agree?\n\n" + F + "\n\n#septic #septicbusiness #knowyournumbers #breakeven #septicowner",
  fb="Here's a question Jason Birdsong of JT Services asked me: your break-even to change an air pump on an aerobic unit is $500. Are you winning or losing if you do the job for $500? I said losing. He said most people would. But if your tech drives out, burns the fuel and the time, the call center books it, and you leave with a $99 diagnostic, you lost. At $500 you still paid the bills and kept Johnny and his family fed. You don't want to do that every time, but it's not losing. Do you know your break-even on a job?\n\n#septic #smallbusiness",
  when="2026-11-11T12:00:00", nets=["youtube", "tiktok", "instagram", "facebook"], cover=10),
 dict(id="price-never-problem", keep=[(2554, 2661)],
  title="Septic prices are\nnever the *problem*",
  yt="Price is never the problem for a septic company. Value is.",
  yd="Jason Birdsong of {jt} on raising your septic prices: yes, go up, but if you can't back it with the value, you won't sell anything. And if you don't know your numbers, how do you sell the value?\n\n" + F + "\n\n#septic #septicbusiness #pricing",
  tt="Price is never the problem. Everybody tells everybody to go up on prices, and Jason Birdsong of {jt} agrees you should. But why 10%? Why 5%? If you can't back it with the value, you won't sell anything. And if you don't know your numbers, how do you sell the value? Agree?\n\n" + FT + "\n\n#septic #septicbusiness #pricing #sales",
  ig="Price is never the problem.\n\nJason Birdsong of {jt} says yes, you should go up on your prices. But if you can't back it with the value, you're not going to sell anything. So many people have sales trauma and blame the price. And if you don't know your numbers, how do you sell the value? Agree?\n\n" + F + "\n\n#septic #septicbusiness #pricing #sales #septicowner",
  fb="Everybody in this industry tells everybody to raise their prices. Jason Birdsong of JT Services agrees, but he wants to know why. Is it 10%? 5%? What's the strategy? His point is that if you can't back a price with the value, you're not going to sell anything. So many people have what he calls sales trauma: they can't sell it, so they decide the price is too high. He says price is never the problem. And if you don't know your own numbers, how do you sell the value? Have you raised your prices this year?\n\n#septic #smallbusiness",
  when="2026-11-12T12:00:00", nets=["youtube", "tiktok", "instagram", "facebook"], cover=8),
 dict(id="cover-payroll", keep=[(589, 641), (644, 693)],
  title="We had to move money\nto cover *payroll*",
  yt="The septic owner's wake-up call: we had to move money to cover payroll",
  yd="Jason Birdsong of {jt} and his wife learned their numbers, hired leadership and got complacent. Then came the call that they'd have to move money around to cover payroll.\n\n" + F + "\n\n#septic #septicbusiness #knowyournumbers",
  tt="Hey, we're going to have to move some money around to cover payroll. That's the call Jason Birdsong of {jt} got from his wife after they learned their numbers, hired leadership and stopped looking every day. He thought they were way past that. Her answer: we've been lazy. Have you ever gotten complacent with your numbers?\n\n" + FT + "\n\n#septic #septicbusiness #knowyournumbers #payroll",
  ig="I thought we were way past this.\n\nJason Birdsong of {jt} and his wife learned their numbers, hired some leadership and got complacent. Then she called: we're going to have to move some money around to cover payroll. Her answer for how it happened was simple. We've been lazy.\n\n" + F + "\n\n#septic #septicbusiness #knowyournumbers #payroll #septicowner",
  fb="Jason Birdsong of JT Services told me about a phone call from his wife. They had learned their numbers, hired some leadership, and stopped looking at those numbers every day. Then she called and said they were going to have to move some money around to cover payroll. He said he thought they were way past this. She said, we've been lazy. He called it his self-reflection moment, and they had to get right back into knowing their numbers and dig their way back out. Has that ever happened to you?\n\n#septic #smallbusiness",
  when="2026-11-13T12:00:00", nets=["youtube", "tiktok", "instagram", "facebook"], cover=20),
 dict(id="cpa-every-week", keep=[(932, 1095)],
  title="I meet with my CPA\n*every* week",
  yt="Why a $6 million septic company meets with its CPA every week",
  yd="Jason Birdsong of {jt} meets with his CPA, tax guy and financial advisor once a week. At six million dollars a lot of money moves through in a week, and a leak is a lot harder to catch and fix when you meet once a month.\n\n" + F + "\n\n#septic #septicbusiness #knowyournumbers",
  tt="I meet with my CPA, tax guy and financial advisor once a week. Jason Birdsong of {jt} used to meet with his tax guy once a year, then quarterly, then monthly. At six million dollars, a lot of money moves through in a week. If you only meet once a month, how big can your leak be? How often do you meet with yours?\n\n" + FT + "\n\n#septic #septicbusiness #knowyournumbers #cpa",
  when="2026-11-14T12:00:00", nets=["youtube", "tiktok"], cover=34.7),
 dict(id="cash-is-king", keep=[(265, 371)],
  title="Paying *cash* for everything\ncaught up with us",
  yt="Why paying cash for septic equipment caught up with us",
  yd="Jason Birdsong of {jt} and his wife believed cash is king. Over three or four years they paid cash for a building addition and equipment that should have been financed, and it caught up with them.\n\n" + F + "\n\n#septic #septicbusiness #cashflow",
  tt="We paid cash for everything, and it caught up with us. Jason Birdsong of {jt} and his wife believed cash is king. They paid cash for a $150,000 building addition and all their equipment, then learned that was good debt they should have financed. All of a sudden: where's all the money? Do you pay cash for equipment?\n\n" + FT + "\n\n#septic #septicbusiness #cashflow #smallbusiness",
  when="2026-11-15T12:00:00", nets=["youtube", "tiktok"], cover=16.0),
 dict(id="pay-more-taxes", keep=[(4528, 4562), (4564, 4573), (4578, 4593), (4823, 4828), (4830, 4858)],
  title="Why I want my septic\nbusiness to pay *more* taxes",
  yt="Why this septic business owner wants to pay more taxes",
  yd="Jason Birdsong of {jt} on the mindset shift that comes as you grow to a three, five or six million dollar company: if you're paying taxes, you're profitable. And a balance sheet that shows no money makes it hard to borrow.\n\n" + F + "\n\n#septic #septicbusiness #taxes",
  tt="So many people fight so hard not to pay taxes. Jason Birdsong of {jt} says if you're paying taxes, you're profitable, and he wants to pay more. As you scale, you need money, and if your balance sheet shows you're not making any because you don't want to pay taxes, it's hard to borrow. Agree?\n\n" + FT + "\n\n#septic #septicbusiness #taxes #smallbusiness",
  ig="If you're paying taxes, you're profitable.\n\nJason Birdsong of {jt} says that's the mind shift that has to happen as you grow. He wants to pay more taxes. As you scale, you need money, and if your balance sheet shows no profit because you're dodging taxes, it's hard to borrow. Agree?\n\n" + F + "\n\n#septic #septicbusiness #taxes #smallbusiness #septicowner",
  fb="Most business owners I know work hard to pay as little in taxes as they can. Jason Birdsong of JT Services says that has to change as you grow into a three, five or six million dollar company. His mindset now is that if you're paying taxes, you're profitable, so he wants to pay more. Here's the part people miss: as you scale, you need money. If your balance sheet shows you're not making any because you didn't want to pay taxes, it's hard to borrow. Do you see it that way?\n\n#septic #smallbusiness",
  when="2026-11-16T12:00:00", nets=["youtube", "tiktok", "instagram", "facebook"], cover=6),
 dict(id="bonus-bob", keep=[(4155, 4179), (4181, 4263)],
  crop_at=[[4189, ASHLEY_X], [4193, JASON_X]],
  title="Do you give Bob a bonus\nbecause you *like* him?",
  yt="How to set bonuses for your septic crew: KPIs, not favorites",
  yd="Jason Birdsong of {jt} asks owners what the parameters are on their holiday bonuses, and most just look at him. His team has KPIs: a revenue target for the month and a labor rate of 20 percent or less, then bonuses.\n\n" + F + "\n\n#septic #septicbusiness #kpi",
  tt="Do you give Bob a bonus because you like him? What if you don't like him? Jason Birdsong of {jt} asks owners what the parameters are on their holiday bonuses, and most just look at him. His team has KPIs: a revenue target for the month and a labor rate of 20 percent or less. Then they get bonuses. What are your parameters?\n\n" + FT + "\n\n#septic #septicbusiness #kpi #smallbusiness",
  when="2026-11-16T17:00:00", nets=["youtube", "tiktok"], cover=17.3),
 dict(id="disposal-crisis", keep=[(5682, 5779)],
  title="Florida lost half its\n*septage* disposal sites",
  yt="The septage disposal crisis: Florida went from 42 sites to 24",
  yd="Jason Birdsong of {jt}, president of NAWT, on the septage disposal crisis. He heard at the NOWRA conference that Florida went from 42 statewide disposal sites to 24 in less than a year, and NAWT is teaching pumpers how to treat or dispose of their own septage.\n\n" + F + "\n\n#septic #septicpumping #septage",
  tt="Florida went from 42 statewide septage disposal sites to 24 in less than a year. Jason Birdsong of {jt}, president of NAWT, says several states are in crisis over where to take septage. He thinks the government fix will take time, so NAWT is teaching pumpers to treat their own septage or find a way to dispose of it properly. Is disposal getting harder where you are?\n\n" + FT + "\n\n#septic #septicpumping #septage #septicbusiness",
  ig="Florida went from 42 septage disposal sites to 24 in less than a year.\n\nJason Birdsong of {jt}, president of NAWT, says several states are in crisis over where to take septage. The government fix will take time, so NAWT is teaching pumpers to treat their own septage or dispose of it properly. Is it getting harder where you are?\n\n" + F + "\n\n#septic #septicpumping #septage #septicbusiness #pumper",
  fb="If you pump septic tanks, this one matters. Jason Birdsong of JT Services is the president of NAWT, and he told me several states are in a real crisis over where to take septage. At the NOWRA conference he heard that Florida went from 42 statewide disposal sites to 24, cut in half in less than a year. He believes it's going to take some time for the government to fix it, so NAWT is building programs to teach pumpers how to treat their own septage or at least dispose of it properly. Is disposal getting harder where you are?\n\n#septic #septicpumping",
  when="2026-11-17T12:00:00", nets=["youtube", "tiktok", "instagram", "facebook"], cover=14),
 dict(id="hourly-rate", keep=[(2353, 2451), (2453, 2513)],
  title="Your septic tech costs more\nthan their *hourly* rate",
  yt="What your septic tech really costs you per hour",
  yd="Jason Birdsong of {jt} on why the hourly rate isn't the cost: vacation time off, insurance, workers comp and a set of tires on the van once a year all have to be built in, or you probably didn't even break even.\n\n" + F + "\n\n#septic #septicbusiness #pricing",
  tt="Johnny's out there for an hour and you think you made good money. Jason Birdsong of {jt} says you probably didn't even break even. Nobody thinks about vacation time off, insurance, workers comp, or the set of tires you'll put on that van once a year. It all has to be built into your price. Do you build it in?\n\n" + FT + "\n\n#septic #septicbusiness #pricing #smallbusiness",
  when="2026-11-17T17:00:00", nets=["youtube", "tiktok"], cover=50.7),
]
EXTRA = {   # clip-only caption fixes
    "price-never-problem": {"2641": "they", "2642": "failed", "2643": "to", "2554": "Everybody"},
    "disposal-crisis": {"5746": "we're", "5747": ""},
    "cpa-every-week": {"932": "So"},
    "pay-more-taxes": {"4593": "right?", "4823": "As", "4564": "The"},
    "cash-is-king": {"265": "My", "283": ""},
    "cover-payroll": {"589": "My"},
        "bonus-bob": {"4155": "I", "4198": "Bob"},
}

out = []
for c in clips:
    keep = []
    for lo, hi in c['keep']:
        # split out the host's short interjections (<= 4 words, all back-channel)
        i, s = lo, None
        while i <= hi:
            j = i
            if labs[i] == 'ASHLEY':
                while j <= hi and labs[j] == 'ASHLEY':
                    j += 1
                words = [''.join(ch for ch in W[k]['word'].lower() if ch.isalpha()) for k in range(i, j)]
                if j - i <= 4 and i > lo and j <= hi and all(w in BACK for w in words):
                    if s is not None:
                        keep.append([s, i - 1]); s = None
                    print(c['id'], 'host interjection cut', i, ' '.join(W[k]['word'] for k in range(i, j)))
                    i = j
                    continue
            if s is None:
                s = i
            i = max(j, i + 1)
        if s is not None:
            keep.append([s, hi])
    kept = [k for a, b in keep for k in range(a, b + 1)]
    fixes = {}
    for k in kept:
        if str(k) in epfix:
            fixes[str(k)] = epfix[str(k)]
        if k in dropped:            # stammers stay in the audio, hidden from the captions
            fixes[str(k)] = ""
    fixes.update(EXTRA.get(c['id'], {}))
    first = kept[0]
    cur = fixes.get(str(first), W[first]['word'])
    if cur and cur[0].islower():
        fixes[str(first)] = cur[0].upper() + cur[1:]
    clip = {"id": c['id'], "source": "01_footage/c0031.mp4", "words": "02_audio/words/c0031.json",
            "keep": keep, "title": c['title'],
            "youtube": {"title": c['yt'], "description": c['yd']},
            "approved": False, "fixes": fixes, "layout": "crop", "crop_x": JASON_X,
            "publish_at": c['when'], "networks": c['nets'], "end_channel": "right"}
    if c.get('crop_at'):
        clip["crop_at"] = c['crop_at']
    caps = {"tiktok": c['tt']}
    if c.get('ig'):
        caps["instagram"] = c['ig']
        caps["facebook"] = c['fb']
    clip["captions"] = caps
    if c['id'] in TS:
        clip['trim_start'] = TS[c['id']]
    if c['id'] in EPAD:
        clip['end_pad'] = EPAD[c['id']]
    if c['cover'] is not None:
        clip["cover_at"] = round(W[first]['start'] + c['cover'], 1)
    out.append(clip)
    text = ' '.join(fixes.get(str(k), W[k]['word']) for k in kept if fixes.get(str(k), W[k]['word']) != '')
    dur = sum(W[b]['end'] - W[a]['start'] for a, b in keep)
    print(c['id'], keep, '%.0f s' % dur)
    print('  ', text)
    print()

rec = {
    "_how": "Recipe for shorts.build (video-machine). 9 clips from Part 2 of 2 of the NOWRA booth series with Jason Birdsong of JT Services (take c0031, Sony 1920x1080 at 29.97 fps, one static wide shot: Jason left, Ashley right; two wireless mics, LEFT channel Ashley, RIGHT channel Jason). keep = inclusive word-index ranges of 02_audio/words/c0031.json in play order; the host's 1 to 4 word back-channel interjections are split out; stammers stay in the audio and are hidden from the captions with \"\" fixes; fillers skip automatically; max_gap 1.0. layout crop at 0.23 (Jason), crop_at cuts to Ashley (0.74) for her lines in break-even-job and bonus-bob. end_channel right keeps only Jason's mic from the last word on. mono: true mixes the two mics into both ears. Posting plan: Part 2 releases Wednesday 2026-11-11 (8:00 CT). Part 1's Shorts (2026-10-26-podcast-nowra-birdsong) hold 3 PM CT Wed to Sun and 3 and 5 PM Mon/Tue 11-09/10, so these take noon every day Wed 11-11 to Tue 11-17 plus 5 PM Mon 11-16 and Tue 11-17: two Shorts a day across both parts. Every clip goes to YouTube and TikTok; the five strongest (break-even-job, price-never-problem, cover-payroll, pay-more-taxes, disposal-crisis) also to Instagram and Facebook, one a weekday at noon (Wed to Fri overlap Part 1's 3 PM Instagram posts: move one part's if Ashley wants one Instagram post a day). Captions: one per network; {jt} tags JT Services (jtserviceco.com lists no social accounts, so it is a plain name), the full episode linked ({episode}) everywhere but Facebook. NAWT = National Association of Wastewater Technicians (Jason is its president). approved = Ashley approved it in Ops. Generated by 07_notes/make_shorts.py.",
    "fillers": True, "max_gap": 1.0, "mono": True,
    "guests": {"jt": {"name": "Jason Birdsong of JT Services"}},
    "cover_with": "with Jason Birdsong of JT Services",
    "clips": out,
}
old = {}
if os.path.exists('06_scripts/shorts.json'):
    old = {c['id']: c for c in json.load(open('06_scripts/shorts.json'))['clips']}
for c in out:                       # keep measured edges and covers written after the first run
    for k in ("trim_start", "end_pad", "end_mute", "cover", "cover_at", "cover_raise"):
        if k in old.get(c['id'], {}) and k not in c:
            c[k] = old[c['id']][k]
json.dump(rec, open('06_scripts/shorts.json', 'w'), indent=1, ensure_ascii=False)
