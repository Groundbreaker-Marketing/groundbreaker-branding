import json, re, sys
P = sys.argv[1]
ep = json.load(open(P + '/06_scripts/episode.json'))
w = json.load(open(P + '/02_audio/words/160057-synced.json'))['words']
efix = ep['fixes']['160057']
edrop = ep['drop']['160057']
dropped = set()
for a, b in edrop:
    dropped.update(range(a, b + 1))
dropped.update([1720, 1721, 3546])
COMMA_ENDS = {2697}
TRIM = {'go-empty': (-0.19, 0.10), 'walk-right-over': (-0.2, 0.04), 'call-100': (0, 0.05), 'neighbor-deal': (0, -0.02),
        'wish-i-hadnt': (-0.2, 0.10), 'stay-in-your-lane': (0, 0.12), 'bread-and-butter': (0.06, 0.08),
        'roller-coaster': (-0.13, -0.01), 'senior-military': (0.06, 0.11), 'dawson-springs': (-0.19, -0.02),
        'not-cheapest': (-0.13, 0.09), 'check-the-truck': (-0.11, 0.12), 'problem-solver': (0.06, -0.01)}

T = '{hendricks}'
E = '{episode}'
FE = 'Full episode: ' + E
FT = 'Full episode on our YouTube: ' + E

clips = [
 dict(id='go-empty', keep=[[5164, 5280]], day='2026-12-09', time='12:00', nets='all',
  title='Go *empty* to the farthest\nseptic job first',
  yt=('Why septic trucks should drive empty to the farthest job first',
      f'Justin Gamblin of {T} calls septic pumping trucking, and he says the route is the whole game. Here is the rule he gives his drivers.\n\n{FE}\n\n#septic #septicpumping #septicbusiness'),
  tt=f'I call it trucking because that is really what it is. Justin Gamblin of {T} tells his guys to run empty to the farthest job and work their way back, because a truck that is loaded at the far end gets worse fuel mileage on the way home. With fuel around $6 a gallon, every route counts.\n\n{FT}\n\n#septic #septicpumping #septicbusiness #trucking',
  ig=f'Go empty to the farthest job, then work your way back. Justin Gamblin of {T} calls septic pumping trucking, and he says it is all logistics. A truck that is loaded at the far end gets worse fuel mileage on the way back, so he plans every route around the dump location.\n\n{FE}\n\n#septic #septicpumping #septictruck #septicbusiness #fuelcosts',
  fb=f'Ask a septic pumper what the job really is and Justin Gamblin of {T} in Madisonville, Kentucky will tell you it is trucking. He pumps septic tanks and grease traps, but the money is in the logistics. He tells his guys all the time to run empty to the farthest job and work their way back toward the dump location, because a truck that is loaded at the far end gets worse fuel mileage on the way home. With fuel around $6 a gallon, that kind of planning adds up.\n\n#septic'),
 dict(id='walk-right-over', keep=[[1706, 1850]], day='2026-12-10', time='12:00', nets='all',
  title='I walk right over to\nthe *septic tank*',
  yt=('Septic trade secret: how to find a tank by reading the yard',
      f'Justin Gamblin of {T} says once you find one septic tank, you can pretty much find them all. He explains the trade secret behind it, and why his crew gets frustrated when he walks right over to a tank they could not find.\n\n{FE}\n\n#septic #septictank #septicpumping'),
  tt=f'Once you find one septic tank, you can pretty much find them all. Justin Gamblin of {T} says there is a trade secret to it: knowing what a yard looks like and where you would have put the system, so you do not have to flush a transmitter. His guys cannot find the tank, he walks right over to it, and he still cannot explain how.\n\n{FT}\n\n#septic #septictank #septicpumping #septiclife',
  ig=f'Once you find one septic tank, you can find them all. Justin Gamblin of {T} says there is a trade secret to it: you learn what a yard looks like, and where you would put a septic system in it, before you ever reach for a transmitter. His crew says they cannot find the tank, and he walks right over to it.\n\n{FE}\n\n#septic #septictank #septicpumping #septicpro #septiclife',
  fb=f'His guys get frustrated with him, and Justin Gamblin of {T} understands why. They will say they cannot find the septic tank, then he walks out in the yard, goes right to it, and they ask how he did that. He says he honestly does not know. The man he bought the business from showed him an easier way to find tanks early on, and he says once you find one you can pretty much find them all. He would rather read the yard than flush a transmitter.\n\n#septic'),
 dict(id='call-100', keep=[[3381, 3498]], day='2026-12-11', time='12:00', nets='all',
  title='Call *100* past septic\ncustomers, 10 to 15 book',
  yt=('Septic reminder calls: call 100 customers and 10 to 15 book on the spot',
      f'Justin Gamblin of {T} moved his septic customer list into QuickBooks and asks every customer if they want a reminder. When his office calls the list, 10 to 15 out of 100 book right then.\n\n{FE}\n\n#septic #septicmarketing #septicpumping'),
  tt=f'You might call 100 people, but 10 to 15 of them book right then. A few years back Justin Gamblin of {T} converted his septic customer history into QuickBooks. When a crew services a tank, they ask if the customer wants a reminder, write it on the invoice, and it goes in the computer. Then they call the list.\n\n{FT}\n\n#septic #septicmarketing #septicpumping #septicbusiness',
  ig=f'Call 100 past customers and 10 to 15 will book right then. Justin Gamblin of {T} built a big list in QuickBooks by asking every septic customer if they want a reminder. The answer goes on the invoice, then into the computer, and the callouts book jobs.\n\n{FE}\n\n#septic #septicmarketing #septicpumping #septicbusiness #customerservice',
  fb=f'The septic business is a roller coaster, and Justin Gamblin of {T} has felt every dip. One thing that helps: a few years ago his team converted their customer history into QuickBooks. When they pump a tank, they ask if the customer wants a reminder and write it on the invoice, and it goes in the computer. Then they call the list. He says if you call 100 people, 10 to 15 of them will book right then.\n\n#septic'),
 dict(id='neighbor-deal', keep=[[3514, 3540], [3545, 3654]], day='2026-12-14', time='12:00', nets='all',
  title='Door hangers flopped,\nthe *neighbor deal* didn\'t',
  yt=('Septic neighbor discounts: door hangers flopped, the deal still works',
      f'Justin Gamblin of {T} tried the neighbor discount idea he heard on this podcast. The door hangers did not bring much turnout, but honoring the neighbor deal still gets him jobs.\n\n{FE}\n\n#septic #septicmarketing #septicpumping'),
  tt=f'Door hangers on the next house did not bring much turnout for Justin Gamblin of {T}. The neighbor discount itself still works. He heard the idea on this podcast, has honored it for a year, and says you would be surprised how often it pays off.\n\n{FT}\n\n#septic #septicmarketing #septicpumping #neighbordiscount',
  ig=f'Door hangers did not do much. The neighbor discount did. Justin Gamblin of {T} heard the idea on this podcast and has run it for a year. He kept door hangers in the truck and hung one on the house next door, but says honoring the neighbor deal is what still gets him jobs.\n\n{FE}\n\n#septic #septicmarketing #septicpumping #neighbordiscount #septicbusiness',
  fb=f'Justin Gamblin of {T} listened to this podcast, heard about the neighbor discount, and gave it a real try. He kept door hangers in the truck and hung one on the house next door after a job. He says they did not see much turnout from that. But when a customer brings up the neighbor deal, he honors it, and he says you would be surprised how often that works.\n\n#septic'),
 dict(id='wish-i-hadnt', keep=[[1111, 1223]], day='2026-12-15', time='12:00', nets='all',
  title='Do I wish I hadn\'t\nbought my *septic* company?',
  yt=('Should you buy a septic company? A Kentucky owner on what he would tell you',
      f'Justin Gamblin of {T} bought his septic company in 2012. Does he wish he hadn\'t? The answer is yes and no, and he explains what the purchase gave him and what you could do instead.\n\n{FE}\n\n#septic #septicbusiness #buyingabusiness'),
  tt=f'A lot of times Justin Gamblin of {T} says he wishes he had not bought his septic company. Then he thinks about what came with it: an established name, an existing customer list, and grease traps already on the books. His advice if you are thinking about it: buy a truck, keep your day job, and build from there.\n\n{FT}\n\n#septic #septicbusiness #buyingabusiness #septicpumping',
  ig=f'Yes and no. Justin Gamblin of {T} bought his septic company in 2012, and some days he wishes he had not. But it gave him an established name, a customer list and grease traps already on the books. He says you could also buy a truck, keep your day job, and build up from there.\n\n{FE}\n\n#septic #septicbusiness #buyingabusiness #septicpumping #smallbusiness',
  fb=f'Does Justin Gamblin of {T} regret buying his septic company? Yes and no. He bought it in 2012 from the man who started it, and some days he says he wishes he had not. But it gave him a head start: an established name, an existing customer list, and grease traps that were already on the books. He does not think buying is a necessity. He says you could start with a truck and a day job and grow from there.\n\n#septic'),
 dict(id='stay-in-your-lane', keep=[[1991, 2159]], day='2026-12-10', time='17:00', nets='yt-tt',
  title='Stay in your *lane*\nin the septic business',
  yt=('Stop buying new septic equipment before you master one job',
      f'Justin Gamblin of {T} bought a jetter, then a mobile belt press, then tried dewatering. Now he says if you are good at one thing, stay there.\n\n{FE}\n\n#septic #septicbusiness #septicpumping'),
  tt=f'Let us buy a jetter. Let us do dewatering. Let us buy a mobile belt press. Justin Gamblin of {T} did all of it after he bought his septic company, and now he says if you are good at one thing, stay there. He is teaching his 20-year-old son the same lesson: stay in our lane. Agree?\n\n{FT}\n\n#septic #septicbusiness #septicpumping #businessadvice'),
 dict(id='bread-and-butter', keep=[[499, 565]], day='2026-12-09', time='17:00', nets='yt-tt',
  title='Find your septic\n*bread and butter*',
  yt=('Hard to say no to extra money: why one septic company went back to pumping',
      f'Justin Gamblin of {T} on the moment he put pen to paper and asked what his septic company actually does best.\n\n{FE}\n\n#septic #septicpumping #septicbusiness'),
  tt=f'It is a hard thing to say no to extra money. Justin Gamblin of {T} says what changed his mind was putting pen to paper: what can we actually do versus what were we doing? His answer was pumping, since you can pump septic tanks pretty much year round.\n\n{FT}\n\n#septic #septicpumping #septicbusiness'),
 dict(id='roller-coaster', keep=[[2525, 2584], [2638, 2682], [2691, 2697], [2702, 2714]], day='2026-12-11', time='17:00', nets='yt-tt',
  title='Septic calls are\na *roller coaster*',
  yt=('Septic calls are a roller coaster: Justin Gamblin on smoothing it out',
      f'Justin Gamblin of {T} on residential septic work: one week you do not have enough trucks, the next the phone is not ringing.\n\n{FE}\n\n#septic #septicmarketing #septicpumping'),
  tt=f'Residential septic work is a roller coaster. Justin Gamblin of {T} says one week you are so busy you do not have enough trucks, and the next the phone is not ringing at all. He wants it either all the way up or flat across. If he ever figures that out, he says he could be a multimillionaire. Does your phone do this too?\n\n{FT}\n\n#septic #septicmarketing #septicpumping #septicbusiness'),
 dict(id='senior-military', keep=[[4493, 4620]], day='2026-12-12', time='12:00', nets='yt-tt',
  title='Senior and *military*\ndiscounts on septic pumping',
  yt=('Why one septic company offers senior and military discounts',
      f'Justin Gamblin of {T} on why he offers senior and military discounts, and how many people ask about them.\n\n{FE}\n\n#septic #septicpumping #septicbusiness'),
  tt=f'We just think it is a good idea. Justin Gamblin of {T} offers septic customers senior and military discounts, and he says you would be surprised how many people ask about them. He has grandparents of his own and wants to give back to the military. He still feels a little awkward asking someone if they are a senior.\n\n{FT}\n\n#septic #septicpumping #septicbusiness'),
 dict(id='dawson-springs', keep=[[4735, 4873]], day='2026-12-13', time='17:00', nets='yt-tt',
  title='The night the tornado\nhit *Dawson Springs*',
  yt=('A septic pumper on the night a tornado hit his wife\'s hometown',
      f'Justin Gamblin of {T} on the Dawson Springs tornado, his wife\'s family, and helping people who needed it.\n\n{FE}\n\n#septic #septicpumping #kentucky'),
  tt=f'Justin Gamblin of {T} was in Dawson Springs the night the tornado hit, looking for his wife\'s family. Her parents lost their home. A giant tree demolished her brother\'s house. He spent a lot of time in the area after that, helping people who needed it.\n\n{FT}\n\n#septic #septicpumping #kentucky'),
 dict(id='not-cheapest', keep=[[5303, 5325], [5330, 5431]], day='2026-12-12', time='17:00', nets='yt-tt',
  title='Not the *cheapest* septic\ncompany, not the priciest',
  yt=('Septic pricing with fuel at $6 a gallon: not the cheapest, not the priciest',
      f'Justin Gamblin of {T} on raising prices when fuel and truck parts keep climbing, in a town with only three or four haulers.\n\n{FE}\n\n#septic #septicpricing #septicpumping'),
  tt=f'Fuel is about $6 a gallon and truck parts are crazy. Justin Gamblin of {T} says he raised prices because his area was behind, and there are only three or four haulers in town. His rule: not the most expensive, not the cheapest. Where does your price sit?\n\n{FT}\n\n#septic #septicpricing #septicpumping #septicbusiness'),
 dict(id='check-the-truck', keep=[[5713, 5747], [5750, 5782], [5794, 5819]], day='2026-12-13', time='12:00', nets='yt-tt',
  title='Check a driver\'s *truck*\nbefore you hire',
  yt=('How to judge a septic driver before you hire: look at their own truck',
      f'Justin Gamblin of {T} on what a driver\'s own vehicle tells you before you hire.\n\n{FE}\n\n#septic #septicbusiness #hiring'),
  tt=f'Want to know if someone will take care of your truck? Look at what they pull up in. Justin Gamblin of {T} says if they do not care about theirs much, they probably will not care about yours. He admits maybe that is wrong, but it is how he sees it. Agree?\n\n{FT}\n\n#septic #septicbusiness #hiring #cdl'),
 dict(id='problem-solver', keep=[[5935, 6020], [6101, 6147]], day='2026-12-14', time='17:00', nets='yt-tt',
  title='Be a septic\n*problem solver*',
  yt=('Septic owners are problem solvers: fix it yourself or find someone who can',
      f'Justin Gamblin of {T} on never giving up, and what he tells his son and brother-in-law when something breaks.\n\n{FE}\n\n#septic #septicbusiness #septicpumping'),
  tt=f'Do not give up. Justin Gamblin of {T} says when something breaks, you just have to be a problem solver: fix it yourself or find someone who can. He is teaching his son and brother-in-law the same thing. When they pull up, park and say fix this, his answer is no, we are getting out and fixing it together.\n\n{FT}\n\n#septic #septicbusiness #septicpumping #problemsolving'),
]

out = []
for c in clips:
    keep = c['keep']
    fixes = {}
    for a, b in keep:
        for i in range(a, b + 1):
            if str(i) in efix:
                fixes[str(i)] = efix[str(i)]
            if i in dropped:
                fixes[str(i)] = ''
    # first word capitalized, last word ends a sentence
    a = keep[0][0]
    cur = fixes.get(str(a), w[a]['word'])
    if cur:
        fixes[str(a)] = cur[0].upper() + cur[1:]
    prev_dot = True
    for n, (a2, b2) in enumerate(keep):
        if n and prev_dot:
            cur = fixes.get(str(a2), w[a2]['word'])
            if cur:
                fixes[str(a2)] = cur[0].upper() + cur[1:]
        cur = fixes.get(str(b2), w[b2]['word'])
        prev_dot = True
        if b2 in COMMA_ENDS:
            prev_dot = False
        elif cur and cur[-1] not in '.?!':
            fixes[str(b2)] = cur.rstrip(',;:') + '.'
    for a2, b2 in keep:
        for i in range(a2 + 1, b2 + 1):
            if w[i - 1]['word'][-1] in '.?!' and fixes.get(str(i), w[i]['word']):
                cur = fixes.get(str(i), w[i]['word'])
                fixes[str(i)] = cur[0].upper() + cur[1:]
    cap = {}
    if c['nets'] == 'all':
        nets = ['youtube', 'tiktok', 'instagram', 'facebook']
        cap = {'tiktok': c['tt'], 'instagram': c['ig'], 'facebook': c['fb']}
    else:
        nets = ['youtube', 'tiktok']
        cap = {'tiktok': c['tt']}
    cs = w[keep[0][0]]['start']
    out.append({
        'id': c['id'], 'source': '01_footage/zoom-160057-synced.mov', 'words': '02_audio/words/160057-synced.json',
        'keep': keep, 'title': c['title'],
        'youtube': {'title': c['yt'][0], 'description': c['yt'][1]},
        'captions': cap, 'approved': False, 'fixes': fixes,
        'layout': 'crop', 'crop_x': 0.5, 'trim_start': TRIM[c['id']][0], 'end_pad': TRIM[c['id']][1],
        'publish_at': c['day'] + 'T' + c['time'] + ':00', 'networks': nets,
        'cover_at': round(cs + 3.0, 1),
    })
d = {'_how': "Recipe for shorts.build (video-machine). 13 clips from Justin Gamblin's (Hendricks Septic Tank Service Inc., Madisonville, Kentucky) guest episode, take 160057 (Zoom HD 1280x720, speaker view, no upscale). Source is the lip-synced file (zoom-160057-synced.mov, Justin 55 ms earlier) with its words file; keep = inclusive word-index ranges in play order; fillers skip automatically; stammers stay in the audio and are hidden from the captions with \"\" fixes, max_gap 1.0. Justin's phone picture is a portrait window in the middle of the frame, so layout crop at 0.5 frames him exactly. Posting plan: release week 2026-12-09..12-15, every clip to YouTube + TikTok at noon or 5 PM CT; the five strongest (go-empty, walk-right-over, call-100, neighbor-deal, wish-i-hadnt) also to Instagram and Facebook at noon on weekdays. Captions: one per network; {hendricks} tags Hendricks Septic Tank Service (Facebook page id from the company's own site; no Instagram, TikTok or YouTube listed), the full episode linked ({episode}) everywhere but Facebook. approved = Ashley approved it in Ops.",
     'fillers': True, 'max_gap': 1.0,
     'guests': {'hendricks': {'name': 'Hendricks Septic Tank Service', 'facebook': {'id': '523699351141242', 'name': 'Hendricks Septic Tank Service'}}},
     'cover_with': 'with Justin Gamblin of Hendricks Septic Tank Service',
     'clips': out}
json.dump(d, open(P + '/06_scripts/shorts.json', 'w'), indent=1)
for c in out:
    ws = []
    for a, b in c['keep']:
        ws += [c_ for c_ in range(a, b + 1)]
    txt = ' '.join((c['fixes'].get(str(i), w[i]['word'])) for i in ws)
    print(c['id'], c['publish_at'], '\n   ', re.sub(r'\s+', ' ', txt))
