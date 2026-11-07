import json, os, re
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EP = json.load(open('06_scripts/episode.json'))
EPFIX = EP['fixes']['c0021']
W = json.load(open('02_audio/words/c0021.json'))['words']
STAMMERS = {a for a, b in EP['drop']['c0021'] for a in range(a, b + 1)}   # words the episode cuts; Shorts keep the audio and hide them

TAGS = {
    "tiktok": " #septic #drainfield #septicbusiness #wastewater",
    "instagram": " #septic #drainfield #septicbusiness #wastewater #septicowner",
    "facebook": " #septic #drainfield",
}
YT = " #septic #drainfield #septicbusiness"
EP_LINE_YT = "\n\nFull episode: {episode}\n\n"
EP_LINE_TT = "\n\nFull episode on our YouTube: {episode}\n\n"
EP_LINE_IG = "\n\nFull episode: {episode}\n\n"


def fixes_for(keep):
    out = {}
    for a, b in keep:
        for i in range(a, b + 1):
            if str(i) in EPFIX:
                out[str(i)] = EPFIX[str(i)]
            elif i in STAMMERS and not (i in (131, 132)):
                out[str(i)] = ""
    return out


clips = []


def add(cid, keep, title, yt_title, yt_desc, tt, ig, fb, when, nets, cover_at, crop_at=None, extra=None):
    c = {
        "id": cid,
        "source": "01_footage/c0021.mp4",
        "words": "02_audio/words/c0021.json",
        "keep": keep,
        "title": title,
        "youtube": {"title": yt_title, "description": yt_desc + EP_LINE_YT.rstrip("\n") + "\n" + YT.strip()},
        "approved": False,
        "fixes": fixes_for(keep),
        "layout": "crop",
        "crop_x": 0.33,
        "publish_at": when,
        "networks": nets,
        "captions": {"tiktok": tt + EP_LINE_TT + TAGS["tiktok"].strip()},
        "end_pad": 0.12,
        "cover_at": cover_at,
    }
    if "instagram" in nets:
        c["captions"]["instagram"] = ig + EP_LINE_IG + TAGS["instagram"].strip()
    if "facebook" in nets:
        c["captions"]["facebook"] = fb + "\n\n" + TAGS["facebook"].strip()
    if crop_at:
        c["crop_at"] = crop_at
    if extra:
        c.update(extra)
    clips.append(c)


ALL = ["youtube", "tiktok"]
FIVE = ["youtube", "tiktok", "instagram", "facebook"]

add("mound-or-five-thousand",
    [[2435, 2516]],
    "A $25,000 septic mound,\nor a *$5,000* fix?",
    "A $25,000 septic mound replacement avoided for about $5,000",
    "Stephen Moeller of {riovation} shares a job on the border of Lowndes County, Alabama. The option on the table was a $25,000 mound "
    "replacement. Instead they put RioVation's product in the existing tank for about $5,000, and four years later it is "
    "still running.",
    "A $25,000 mound replacement, or about $5,000 for a different fix? Stephen Moeller of {riovation} says a homeowner on the border of "
    "Lowndes County, Alabama put the product in for about $5,000. Four years later the system is still running and the "
    "problem is resolved. If a failing system is headed for a mound, would you pitch this first?",
    "A $25,000 mound, or about $5,000 to treat what's already in the tank.\n\nStephen Moeller of {riovation} shares a job "
    "in Lowndes County, Alabama where the homeowner skipped the mound replacement. The system has been running for about "
    "four years and the problem is resolved. In the Black Belt region, he says, there are so many problems like it. Would "
    "you pitch this first?",
    "Picture the call: a homeowner in Alabama is looking at a $25,000 mound replacement. Stephen Moeller of RioVation told "
    "me about that job. Instead of the mound, they put RioVation's product into the tank and paid about $5,000 for it. "
    "It's been running for about four years and the problem is resolved. He said that part of Alabama, the Black Belt "
    "region, has so many problems like it. If you install or maintain septic systems, how often do you see a customer "
    "who could have skipped the big bill?",
    "2026-11-18T12:00:00", FIVE, 846.0,
    extra={"broll": [{"clip": "trade-show-video.mp4", "at": "This is a grab", "dur": 8.0, "ss": 56.0, "over_show": True, "fill": "blur"}],
           "hook_clear": 0.05})

add("designing-to-fail",
    [[518, 605]],
    "Why are we designing\n*septic* systems to fail?",
    "Why are we designing septic systems to fail?",
    "At conferences, engineers explain how to site a drain field and tell you to leave the alternate area alone. Stephen "
    "Moeller of {riovation} says Gig Drewery would raise his hand and ask why we design for a 20 to 30 year life and "
    "failure, when we could use treated effluent and avoid it.",
    "Why are we designing septic systems to fail? Stephen Moeller of {riovation} says Gig Drewery asks it at conferences "
    "when an engineer explains how to site a drain field. Leave the alternate area alone, don't build on it, plan for a 20 "
    "to 30 year life and then failure. Gig's answer is to use treated effluent and avoid it. Agree?",
    "Why are we designing septic systems to fail?\n\nThat's the question Gig Drewery of {riovation} keeps asking at "
    "conferences, according to Stephen Moeller. The engineer explains how to site a drain field, says to save the "
    "alternate area and don't build on it, and the plan quietly assumes a 20 to 30 year life and then failure. Use "
    "treated effluent and avoid it. Agree?",
    "At a conference, an engineer explains how to site a drain field. Leave the alternate area alone. You can't put a "
    "gazebo on it. Stephen Moeller of RioVation told me that Gig Drewery, who developed their product, would raise his "
    "hand every time and ask why we are designing for a 20 to 30 year life and then failure. Why not use treated "
    "effluent and avoid it? When you design a system, do you plan for the replacement or the fix?",
    "2026-11-19T12:00:00", FIVE, 196.0)

add("drain-field-cost",
    [[1450, 1555]],
    "What a failing septic\ndrain field *really* costs to fix",
    "What does it cost to rejuvenate a failing septic drain field? About $5,000",
    "I asked Stephen Moeller of {riovation} what drain field rejuvenation costs. States differ: some require permitting, "
    "you need a riser to the surface, and the tank gets pumped. All in, he says it's usually in the $5,000 range, a "
    "little under or a little over.",
    "What does it cost to rejuvenate a failing drain field? I asked Stephen Moeller of {riovation}. Some states require "
    "permitting, you need a riser to the surface and the tank gets pumped. He says all in it's usually in the $5,000 "
    "range, maybe a little under or over. That's a very different bill from replacing a whole system that may not need "
    "it. Agree?",
    "A failing drain field doesn't always mean a new system.\n\nI asked Stephen Moeller of {riovation} what the cost "
    "looks like. Every state is a little different, some require permitting, you need a riser to the surface if there "
    "isn't one, and the tank gets pumped. All in, he says it's usually in the $5,000 range. Replacing a system that "
    "maybe doesn't need to be replaced is quite a bit different. Agree?",
    "Someone told me about their area last night: very rural, a lot of older people on fixed incomes, and systems backing "
    "up and failing. Then they're looking at a $20,000, $30,000 or $50,000 bill for a whole new system. So I asked "
    "Stephen Moeller of RioVation what drain field rejuvenation costs. His answer: usually in the $5,000 range, "
    "depending on your state, permitting, a riser and pumping the tank. It would not work in every case, but it's a "
    "conversation worth having before anyone signs for a new system.",
    "2026-11-20T12:00:00", FIVE, 520.0, crop_at=[[1450, 0.70], [1462, 0.34]])

add("customer-for-life",
    [[1911, 1996], [2177, 2246]],
    "How to get a *septic*\ncustomer for life",
    "Maintenance agreements: how to get a septic customer for life",
    "A RioVation system has blowers, and the blower filter needs to be cleaned a couple of times a year. Stephen Moeller "
    "of {riovation} says to put the homeowner on a maintenance agreement and the contractor has a customer for life. "
    "Some contractors build two years of maintenance into the bid for a few hundred dollars.",
    "The easiest upsell in septic might be one you build into the bid. Stephen Moeller of {riovation} says some of "
    "the contractors they work with include two years of maintenance in the base price, only a few hundred dollars. "
    "The customer gets used to you being out there, and re-upping every year gets easier. The contractor has a customer "
    "for life. Would you do it?",
    "Build the maintenance into the bid.\n\nStephen Moeller of {riovation} says the blowers need a filter cleaned a "
    "couple of times a year, so the best thing a contractor can do is put the homeowner on a maintenance agreement. "
    "Some of the contractors he works with include two years in the base for a few hundred dollars. After that, "
    "re-upping is easier because the customer is used to you being there. Would you do it?",
    "Some septic contractors don't want to offer a maintenance contract because they figure their customers are cheap. "
    "Stephen Moeller of RioVation told me the contractors they work with who are proactive just build two years of "
    "maintenance into the bid. It's only a few hundred dollars. The customer gets used to someone showing up, and "
    "re-upping on an annual basis is easier after that. He says the contractor ends up with a customer for life, "
    "because they're the one who gets the call when there's an issue.",
    "2026-11-18T17:00:00", ALL, 700.0)

add("install-time",
    [[1749, 1907]],
    "How long this *septic*\nupgrade takes to install",
    "How long does it take to install this septic system upgrade?",
    "I asked Stephen Moeller of {riovation} how long the install takes. He says they don't even publish it on their "
    "website because it's too easy: one person can do it in an hour or two once the riser is in, and half a day to a day "
    "all in.",
    "How long does it take to install? Stephen Moeller of {riovation} says they don't even publish it on their "
    "website because it's too easy. Once the riser is in, one person can do it in an hour or two: air pump by the "
    "house, an airline in a shallow trench, a simple manifold in the tank and the pods dropped in. All in, half a day to "
    "a day.",
    "\"We don't even publish that on our website because it's too easy.\"\n\nI asked Stephen Moeller of {riovation} how "
    "long the install takes. Once the riser is in, one person can do it in an hour or two. The air pump sits by the "
    "house, a three-quarter PVC airline runs to the tank in a shallow trench, and the pods drop in. Pump the tank first "
    "and it's half a day to a day all in.",
    "",
    "2026-11-19T17:00:00", ALL, 650.0, crop_at=[[1749, 0.70], [1760, 0.33]])

add("microbe-condos",
    [[756, 888]],
    "Condominiums for the\nmicrobes in your *septic* tank",
    "Condominiums for the microbes: how this septic tank upgrade works",
    "Stephen Moeller of {riovation} shows the pods that drop into a septic tank: attached growth he calls condominiums "
    "for the microbes, plus ceramic stone diffusers and an airline. Pump the tank first and start fresh, and he says "
    "the microorganisms populate within a day or two.",
    "We call it condominiums for the microbes. Stephen Moeller of {riovation} showed me the pods that drop into the "
    "tank: attached growth for the microorganisms, ceramic stone diffusers and an airline, weighted at the bottom with "
    "floats at the top. Pump the tank first and he says a full spectrum of microorganisms shows up within a day or two. "
    "Would you try it?",
    "",
    "",
    "2026-11-20T17:00:00", ALL, 285.0)

add("townhomes-one-tank",
    [[3029, 3084]],
    "24 townhomes, one 5,000\ngallon *septic* tank",
    "24 townhomes on one 5,000 gallon septic tank with clear water",
    "Stephen Moeller of {riovation} on how the system scaled from homes to RV parks and condominium complexes. A 24 unit "
    "townhome complex runs on one 5,000 gallon tank with two of the systems, and the last sample came back at a BOD of "
    "18 and a TSS of 4.",
    "A 24 unit townhome complex on one 5,000 gallon tank. Stephen Moeller of {riovation} says they put two of the "
    "systems on it, and the last sample came back with a BOD of 18 and a TSS of 4. Very low, clear water. That's the "
    "same technology that started in homes, now scaled up for RV parks and condominium complexes. Agree it's worth a "
    "look?",
    "",
    "",
    "2026-11-21T12:00:00", ALL, 1068.0)

add("try-new-technology",
    [[3742, 3891]],
    "Be willing to try new\n*septic* technology",
    "Be willing to try new septic technology: advice for installers",
    "Stephen Moeller of {riovation}'s advice for installers and maintenance providers: be willing to try new technology. "
    "He says about 50 percent of U.S. soils aren't deemed suitable for treatment, and when you treat in the tank you can "
    "monitor it, see if it's working and fix it.",
    "If he could give septic installers one piece of advice, Stephen Moeller of {riovation} says it's this: be willing "
    "to try new technology. About 50 percent of U.S. soils aren't deemed suitable for treatment, he says, and we push the "
    "envelope anyway. Treat in the tank and you can monitor it, see if it's working and fix it. Agree?",
    "",
    "",
    "2026-11-22T12:00:00", ALL, 1325.0)

add("liberia-odor",
    [[2656, 2739], [2895, 2931]],
    "How a *septic* tank in Liberia\nlost its odor on day one",
    "How a septic tank in Liberia lost its odor on day one",
    "A customer in Liberia with an 8,000 gallon a day flow had an odor problem and a community complaining. Stephen "
    "Moeller of {riovation} says they pumped the 8,000 gallon tank, installed the product, and the odor was gone on day "
    "one. Anaerobic microorganisms off-gas hydrogen sulfide; aerobic ones off-gas carbon dioxide.",
    "The whole community around this facility in Liberia kept complaining about the odor. Stephen Moeller of {riovation} "
    "says they pumped the 8,000 gallon tank, installed the product, and the odor issue was resolved on day one. "
    "Anaerobic microorganisms off-gas hydrogen sulfide. Aerobic ones off-gas carbon dioxide. Have you ever fixed an odor "
    "problem that fast?",
    "The odor was gone on day one.\n\nA customer in Liberia with 8,000 gallons a day of flow had an anaerobic tank, a "
    "trickle filter and a community that kept complaining about the smell. Stephen Moeller of {riovation} says they "
    "pumped the tank, installed the product, and the odor was gone right away. Anaerobic microorganisms off-gas "
    "hydrogen sulfide. Aerobic microorganisms off-gas carbon dioxide. Have you ever fixed an odor problem that fast?",
    "Imagine a facility in Liberia where the whole community around it is constantly complaining about the smell. "
    "Stephen Moeller of RioVation told me about that job: 8,000 gallons a day, an anaerobic tank, a dosing tank and a "
    "trickle filter that treated pretty well but smelled. They pumped the 8,000 gallon tank and installed the product, "
    "and he says the odor issue was resolved on day one. Anaerobic microorganisms off-gas hydrogen sulfide, and aerobic "
    "ones off-gas carbon dioxide. If you deal with odor complaints, that's worth knowing.",
    "2026-11-23T12:00:00", FIVE, 925.0)

add("thirty-years-of-parts",
    [[3599, 3695]],
    "30 years of maintenance\nkits for a *septic* job",
    "A septic project with 30 years of maintenance kits included",
    "On the larger jobs in Ghana and Liberia, where replacement parts aren't easy to get, Stephen Moeller of {riovation} "
    "says RioVation ships standby blowers, maintenance kits and diffuser stones. They should not have to buy anything to "
    "run that project for about 30 years.",
    "How do you service a big septic project where you can't get parts? Stephen Moeller of {riovation} says on the larger "
    "jobs in Ghana and Liberia they ship duty and standby blowers, maintenance kits and diffuser replacements. If one "
    "blower goes down, switch to the standby. They should not have to buy anything to run that project for about 30 "
    "years. Agree?",
    "No ready access to parts? Send the parts.\n\nOn the larger jobs in Ghana and Liberia, Stephen Moeller of {riovation} "
    "says RioVation includes standby blowers, maintenance kits for the blowers and diffuser replacement stones. If one "
    "blower goes down, they switch to the standby. About 30 years of maintenance is on that project, and they should not "
    "have to buy anything to run it. Agree?",
    "Think about a big septic project in Ghana or Liberia, where nobody can pop over to the supply house. Stephen Moeller "
    "of RioVation told me they thought about that up front. They shipped duty and standby blowers, maintenance kits for "
    "the blowers and all the diffuser replacements and stones. If one blower goes down, they just switch to the "
    "standby. He says that project should not have to buy anything to run it for about 30 years. When you design a job, "
    "do you plan for the parts too?",
    "2026-11-24T12:00:00", FIVE, 1272.0)

# trim_start / end_pad measured on each speaker's own mic (07_notes/edges.py, lvl.py), not Whisper's clock
EDGES = {
    "mound-or-five-thousand": (0.0, 0.10),
    "designing-to-fail": (-0.10, 0.03),
    "drain-field-cost": (0.62, 0.20),        # her "yeah" runs to 504.38; "what" starts at 505.08
    "customer-for-life": (0.0, 0.05),
    "install-time": (-0.05, 0.05),
    "microbe-condos": (0.12, 0.05),          # skips the tail of "pods" (-24 dB at the cut)
    "townhomes-one-tank": (-0.10, 0.08),
    "try-new-technology": (-0.05, 0.03),
    "liberia-odor": (-0.10, 0.12),
    "thirty-years-of-parts": (-0.10, 0.04),
}
for c in clips:
    ts, ep = EDGES[c["id"]]
    c["end_pad"] = ep
    if ts:
        c["trim_start"] = ts

rec = {
    "_how": "Recipe for shorts.build (video-machine). 10 clips from the RioVation NOWRA booth episode (take c0021, Sony 1920x1080 at 29.97 fps; the guest is on the left of the frame, Ashley on the right; two wireless mics, LEFT channel Ashley, RIGHT channel the guest; one static wide shot except about 775-845 s, when the camera is on the booth TV, and 955-990 s and 1040-1055 s, when he holds the pod cluster and header up). keep = inclusive word-index ranges of 02_audio/words/c0021.json; stammers stay in the audio and are hidden from captions with \"\" fixes (smoother, Ashley 2026-10-28); fillers skip automatically; max_gap 1.0. layout crop at 0.33 (the guest; he drifts between 0.25 and 0.41), crop_at 0.70 on Ashley's questions. mono: true mixes the two mics into both ears. mound-or-five-thousand starts while the camera is on the booth TV, so a cutaway of RioVation's trade show video (licensed to us) covers it. Guest: Stephen Moeller, NAME NOT FACE-CONFIRMED (riovation.com/about-us; see episode.json _how). Posting plan: the episode releases Wed 2026-11-18 8:00 CT; Shorts go out noon Wed to Tue 11-24 plus 5 PM Wed to Fri, every clip to YouTube and TikTok, the five strongest (mound-or-five-thousand, designing-to-fail, drain-field-cost, liberia-odor, thirty-years-of-parts) also to Instagram and Facebook at noon on a weekday. Captions: one per network; {riovation} tags RioVation (@riovation on YouTube; riovation.com lists no other account, so the other networks get the plain name), the full episode linked ({episode}) everywhere but Facebook. approved = Ashley approved it in Ops. Generated by 07_notes/make_shorts.py.",
    "fillers": True,
    "max_gap": 1.0,
    "mono": True,
    "grade": True,
    "guests": {"riovation": {"name": "RioVation", "youtube": "@riovation"}},
    "cover_with": "with Stephen Moeller of RioVation",
    "clips": clips,
}
old = {}
if os.path.exists('06_scripts/shorts.json'):
    old = json.load(open('06_scripts/shorts.json'))
    keep_keys = ("metricool", "youtube_upload", "cover")
    oldc = {c['id']: c for c in old.get('clips', [])}
    for c in clips:
        for k in keep_keys:
            if c['id'] in oldc and k in oldc[c['id']]:
                c[k] = oldc[c['id']][k]
json.dump(rec, open('06_scripts/shorts.json', 'w'), indent=1)
for c in clips:
    for net, t in [("yt", c['youtube']['description'])] + list(c['captions'].items()):
        n = len(re.sub(r'\{[a-z]+\}', 'x', t).split())
        print(c['id'], net, n)
