import json
P = '/Users/josh/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-13-podcast-episode/'
ep = json.load(open(P + '06_scripts/episode.json'))
efx = ep['fixes']['135607']
SRC = '01_footage/zoom-135607-synced.mov'
WORDS = '02_audio/words/135607-synced.json'
TAGS = '#septic #septicbusiness #septicpumper'

# id, (start, end), title, yt title, yt body, tiktok body, ig, fb, cover_at, slot, networks
clips = [
 dict(id='cheapest', r=(596, 809), cover=190.0, slot='2026-12-23T12:00:00', big=True,
  title='Don\'t be the *cheapest*\nseptic company in town',
  yt='Why the cheapest septic company in town is the one losing money',
  ytb='{jason} of {aas} was the cheapest septic guy around, and his trucks were falling apart. Then a competitor told him to stop. He raised his prices, and he went from one pump truck to eleven.',
  tt='A competitor told Jason Harris: you don\'t have to be the cheapest. His trucks were broken down and he was always working on them. He sat on that advice for two years, then raised his prices. He went from one pump truck to eleven. {jason} of {aas} says he was tired of working for nothing. Ever been there?',
  ig='"I\'m just tired of working for nothing." {jason} of {aas} was the cheapest septic guy around, with trucks that were always broken down. A competitor told him to stay in the middle. Two years later he raised his prices, and one pump truck turned into eleven.',
  fb='A septic owner is buried in calls, and his trucks are falling apart. Another septic company calls a meeting and tells him to stop being the cheapest. {jason} of {aas} says he thought he would lose all his customers, so the advice sat in his head for two years. Then he got tired of working for nothing and raised his prices. He went from one pump truck to eleven.'),
 dict(id='pickup-truck', r=(71, 171), cover=40.0, slot='2026-12-23T17:00:00',
  title='I started my septic company\nwith *shoe polish* on a pickup',
  yt='He started a septic company with shoe polish on a pickup truck',
  ytb='{jason} of {aas} started his septic company in 2011 with a pickup truck and shoe polish on the side. Within two months he bought his first pump truck.',
  tt='Jason Harris started his septic company in 2011 with a pickup truck and the words septic contractor written on the side in shoe polish. He drove around parking lots hoping customers would call. People remembered him from his old job, and within two months he bought his first pump truck. {jason} of {aas} tells the whole story.'),
 dict(id='wastewater-plant', r=(3990, 4161), cover=1204.0, slot='2026-12-24T12:00:00', big=True,
  title='I built my own septic\n*wastewater plant* from scratch',
  yt='A septic owner built his own wastewater treatment plant from scratch',
  ytb='{jason} of {aas} ran out of places to dump his trucks, so he built a wastewater treatment plant from scratch with help from his friend Ryan Gascon.',
  tt='Where are you going to dump your trucks? Jason Harris kept getting more calls in Highlands County, but the dump site closed by 10 in the morning. So he built his own wastewater treatment plant from scratch. A friend, Ryan Gascon, helped him set it up. {jason} of {aas} says it took a lot of learning. Would you do it?',
  ig='"Where are we going to dump our trucks?" {jason} of {aas} had more septic calls than he could handle, and the local dump closed by 10 in the morning. So he built his own wastewater treatment plant from scratch, with help from his friend Ryan Gascon. It took a lot of learning.',
  fb='More septic calls than you can handle sounds like a good problem, until you ask where all that waste is going. {jason} of {aas} ran into it in Highlands County. The local dump site told him to come first thing in the morning because they closed by 10. So he jumped in knee-deep and built his own wastewater treatment plant from scratch, with advice from his friend Ryan Gascon.'),
 dict(id='fire-first', r=(1291, 1357), cover=396.0, slot='2026-12-24T17:00:00',
  title='When to *fire*\na septic employee',
  yt='When to fire a septic employee, from a septic owner who has done it',
  ytb='{jason} of {aas} was told that the first time you need to fire someone is the first time you think about it. Here is how he applies it with his septic crew.',
  tt='Jason Harris was told a long time ago that the first time you need to fire somebody is when you first think about it. That moment you ask yourself whether you should let someone go is your cue. {jason} of {aas} says if an employee keeps messing up, you have to make that sacrifice and keep looking. Agree?'),
 dict(id='lose-customers', r=(924, 1071), cover=296.0, slot='2026-12-26T12:00:00',
  title='Raise your septic prices and\n*lose* the wrong customers',
  yt='Raise your septic prices and lose the wrong customers',
  ytb='{jason} of {aas} raised his septic prices and lost customers, and he says those were not the customers he wanted anyway.',
  tt='Jason Harris raised his septic prices and lost customers, just like he feared. But the people who left were the ones always using him, and then going to the next guy. {jason} of {aas} says those are not good customers, and you have to want to be an A-rated company. That was the hardest thing for him to understand.'),
 dict(id='invoice-checklist', r=(2204, 2333), cover=680.0, slot='2026-12-26T17:00:00',
  title='The septic tank *checklist*\non every invoice',
  yt='The septic tank checklist this company puts on every invoice',
  ytb='{jason} of {aas} has his pump truck drivers fill out a checklist on every invoice: the tank, the outlet tee, the baffle, the drain field and more.',
  tt='Jason Harris does not want his drivers to just pump 1,000 gallons and hand over an invoice. Every invoice has a checklist. What did the tank look like? Was there an outlet tee and a baffle? Were baby wipes in there? Was the drain field working? How was the level? {jason} of {aas} wants to know it all.'),
 dict(id='rolling-billboard', r=(2545, 2630), cover=770.0, slot='2026-12-27T12:00:00',
  title='A clean septic truck is\na *rolling billboard*',
  yt='A clean septic truck is free advertising, says a Florida septic owner',
  ytb='{jason} of {aas} keeps parts and toolboxes off his trucks so the space can be advertising. A clean truck is a rolling billboard.',
  tt='Jason Harris does not hang a bunch of toolboxes and parts off his septic trucks. The space on the truck is advertisement. A clean truck is a rolling billboard driving down the road, and it is free. {jason} of {aas} says if your trucks are not clean, you will not get the A-rated customers you want.'),
 dict(id='phone-lesson', r=(3178, 3272), cover=960.0, slot='2026-12-27T17:00:00',
  title='My septic drivers teach customers\nhow to use their *phone*',
  yt='His septic drivers teach customers how to use their phones',
  ytb='{jason} of {aas} has customers who tell him his driver taught them how to use their phone. He says it is worth it for customer satisfaction.',
  tt='Customers call Jason Harris to say their septic driver taught them how to use their phone. His first thought: I am not paying my drivers to do that. But it is customer satisfaction. {jason} of {aas} says the days of paper invoices are obsolete, and some customers need a little help getting set up.'),
 dict(id='dont-wear-it', r=(1426, 1544), cover=450.0, slot='2026-12-28T12:00:00', big=True,
  title='Just because we\'re in septic\ndoesn\'t mean we *wear* it',
  yt='Just because you are in the septic business does not mean you wear it',
  ytb='{jason} of {aas} on how to hire in the septic business: you see how I come to work? This is how I leave work.',
  tt='Everybody thinks the septic business means you get covered in poop. Jason Harris tells people: you see how I come to work? This is how I leave work. Just because we are in the septic business does not mean we need to wear it. {jason} of {aas} on why finding drivers starts with education. Agree?',
  ig='"You see how I come to work? This is how I leave work." {jason} of {aas} says everyone thinks the septic business means getting covered in poop. His answer: just because we are in septic does not mean we need to wear it. Finding good drivers starts with education.',
  fb='Why is it so hard to find people who will drive a pump truck? {jason} of {aas} says it begins with education. Everybody thinks you will get covered in poop. He tells them: see how I come to work? This is how I leave work. Just because we are in the septic business does not mean we need to wear it.'),
 dict(id='start-slow', r=(8201, 8268), cover=2450.0, slot='2026-12-28T17:00:00',
  title='Expanding to a new septic\ncounty? Start *slow*',
  yt='Expanding your septic company into a new county? Start slow',
  ytb='{jason} of {aas} serves seven counties from two offices. His advice for expanding into a new one: do not jump in feet deep. Start slow and feel out the market.',
  tt='Thinking about expanding your septic company into another county? Jason Harris says do not jump in feet deep. Start slow, feel for the market, and do not put everything you have into that county. Learn your spacing. {jason} of {aas} keeps his two offices about an hour and 20 minutes apart.'),
 dict(id='terralift', r=(6504, 6614), cover=1925.0, slot='2026-12-29T12:00:00', big=True,
  title='When to *TerraLift* a drain field\n(and when to jet it)',
  yt='When to TerraLift a drain field and when to jet it instead',
  ytb='{jason} of {aas} says a lot of people TerraLift a drain field that is dry. You do it when it is soaking wet. If it is dry, it needs to be jetted.',
  tt='A lot of septic pros are out TerraLifting a drain field because it is dry and not taking water. Jason Harris says that is backwards. You TerraLift when it is soaking wet and has nowhere left to go. If it is dry, it needs to be jetted. {jason} of {aas} has seen pipes that look like the ocean inside. Agree?',
  ig='"If it\'s dry, it needs to be jetted." {jason} of {aas} says many septic pros TerraLift a dry drain field, and that is the wrong time. You TerraLift when it is soaking wet and the water has no more passages to go to. Get it wrong and it can disrupt the field badly.',
  fb='A drain field is not taking water, so the crew shows up with a TerraLift machine. {jason} of {aas} says that is not when you use it. You TerraLift a drain field when it is soaking wet and has no more passages to go to. If it is dry, it needs to be jetted. He has seen pipes that look like the ocean inside from people who got it wrong.'),
 dict(id='ninth-grade', r=(6850, 6933), cover=2030.0, slot='2026-12-29T17:00:00',
  title='My dad said I\'d never\n*amount* to anything',
  yt='A septic owner who dropped out in 9th grade and kept learning',
  ytb='{jason} of {aas} dropped out in 9th grade and got his GED. His dad said he would never amount to anything, and that is what pushes him.',
  tt='Jason Harris dropped out of high school in 9th grade and got his GED. His dad told him he was never going to amount to anything. That is what pushes him. {jason} of {aas} also has some advice on business partners, based on how his dad\'s went: do not recommend them.'),
 dict(id='flood', r=(7700, 7872), cover=2300.0, slot='2026-12-30T12:00:00', big=True,
  title='We charged *normal rates*\nduring the flood',
  yt='Septic company kept normal rates during a flood and served 300 customers',
  ytb='{jason} of {aas} says competitors charged emergency rates during the flood. His crews charged the same rate as any weekday, and not one tank popped out of the ground.',
  tt='After a flood, a lot of septic companies charged emergency rates. Jason Harris did not. His crews did about 300 customers at the same rate as a regular Monday through Friday. And out of all of them, not one broken tank and not one that popped out of the ground. {jason} of {aas} says storms are not the time to make money.',
  ig='"It\'s not the time to make money in a crisis." After a flood, {jason} of {aas} moved his trucks to help out. His crews charged the same rate as a normal weekday. Out of all the customers they did, not one tank popped out of the ground.',
  fb='When the neighborhoods flood, the calls come in left and right. A lot of septic companies called it an emergency and charged emergency rates. {jason} of {aas} did the opposite. His crews did around 300 customers at the same rate as any Monday through Friday, and out of all of them, not one broken tank and not one that popped out of the ground.'),
 dict(id='wife-fire', r=(3739, 3842), cover=1115.0, slot='2026-12-30T17:00:00',
  title='How my wife got my septic\ndrivers to *respect* her',
  yt='How a septic owner\'s wife got her drivers to respect her',
  ytb='{jason} of {aas} was running one office while his wife ran the other, and her drivers were not listening. His advice: find the one who will not listen and fire them.',
  tt='Jason Harris was running one septic office while his wife ran the other. Her drivers were not listening. His advice: find the one person who does not listen and fire them in front of everybody. She did that, and everybody started respecting her. {jason} of {aas} says it set the ground. Would you?'),
]

SLOTS = {'cheapest': '2026-12-23T12:00:00', 'pickup-truck': '2026-12-23T17:00:00',
         'wastewater-plant': '2026-12-24T12:00:00', 'lose-customers': '2026-12-24T17:00:00',
         'invoice-checklist': '2026-12-26T12:00:00', 'rolling-billboard': '2026-12-26T17:00:00',
         'phone-lesson': '2026-12-27T12:00:00', 'wife-fire': '2026-12-27T17:00:00',
         'dont-wear-it': '2026-12-28T12:00:00', 'start-slow': '2026-12-28T17:00:00',
         'terralift': '2026-12-29T12:00:00', 'ninth-grade': '2026-12-29T17:00:00',
         'flood': '2026-12-30T12:00:00'}
clips = [c for c in clips if c['id'] in SLOTS]
for c in clips:
    c['slot'] = SLOTS[c['id']]
out = []
for c in clips:
    a, b = c['r']
    fx = {k: v for k, v in efx.items() if a <= int(k) <= b}
    tag = ' ' .join(['#septic', '#septicbusiness', '#septicpumper'])
    y = {'title': c['yt'], 'description': c['ytb'] + '\n\nFull episode: {episode}\n\n' + TAGS}
    caps = {'tiktok': c['tt'] + '\n\nFull episode on our YouTube: {episode}\n\n' + TAGS + ' #septictank' if False else c['tt'] + '\n\nFull episode on our YouTube: {episode}\n\n' + TAGS + ' #wastewater'}
    nets = ['youtube', 'tiktok']
    if c.get('big'):
        caps['instagram'] = c['ig'] + '\n\nFull episode: {episode}\n\n' + TAGS + ' #wastewater #septicservice'
        caps['facebook'] = c['fb'] + '\n\n#septic'
        nets += ['instagram', 'facebook']
    out.append({'id': c['id'], 'source': SRC, 'words': WORDS, 'keep': [[a, b]], 'title': c['title'],
                'youtube': y, 'captions': caps, 'approved': False, 'layout': 'crop', 'crop_x': 0.5,
                'publish_at': c['slot'], 'networks': nets, 'cover_at': c['cover'], 'fixes': fx})
doc = {'_how': 'Recipe for shorts.build (video-machine). 13 clips (fire-first dropped: only 18 s) from Jason Harris (All About Septic Services Inc.) guest episode, take 135607 (Zoom HD 1280x720, speaker view, no upscale, lip-synced: Jason 40 ms earlier). keep = inclusive word-index ranges; per-clip fixes are the episode fixes inside the clip (Ryan Gascon in wastewater-plant). Posting plan: release week from 2026-12-23, every clip to YouTube + TikTok, two a day at noon and 5 PM CT, skipping Christmas Day (12-25), through 12-30; the five strongest (cheapest, wastewater-plant, dont-wear-it, terralift, flood) also to Instagram and Facebook at noon on weekdays (12-23, 12-24, 12-28, 12-29, 12-30). {jason} tags Jason Harris, {aas} tags All About Septic Services; no handles or Facebook page id yet (see final message), the full episode linked ({episode}) everywhere but Facebook.',
       'fillers': True, 'max_gap': 1.0,
       'guests': {'jason': {'name': 'Jason Harris'}, 'aas': {'name': 'All About Septic Services'}},
       'cover_with': 'with Jason Harris of All About Septic Services', 'title_y': 250, 'title_size': 58,
       'clips': out}
json.dump(doc, open(P + '06_scripts/shorts.json', 'w'), indent=1)
print(len(out))
