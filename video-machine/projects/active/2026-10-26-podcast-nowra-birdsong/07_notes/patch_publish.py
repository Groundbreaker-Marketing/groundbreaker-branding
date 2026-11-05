import json
e = json.load(open('06_scripts/episode.json'))
desc = (
    "I recorded this one live at the NOWRA Mega-Conference with Jason Birdsong of JT Services in Claremore, Oklahoma. "
    "This is Part 1 of 2. Jason started out as a repo man, then built what began as J&T Service Company into JT Services, "
    "a full home service company that is on track to do a little over six million dollars this year.\n\n"
    "In this part, Jason walks through the hard lessons of adding plumbing, HVAC and electrical to a septic company: "
    "how he got a plumbing license without working for a plumber for four years, why you master one trade before you add the next, "
    "why one is none and two is some, and why he doesn't believe in shoulder season. Part 2 goes out Wednesday, November 11, "
    "and goes deeper on knowing your numbers.\n\n"
    "What we cover:\n"
    "- How a repo man started a septic company\n"
    "- Why plumbing came first and how Jason got the license\n"
    "- Why investing in yourself comes before growth\n"
    "- Finding the right business coach and a why strong enough to push through\n"
    "- Mastering one trade before you add the next\n"
    "- One is none, two is some: hiring and onboarding\n"
    "- Why promoting your best person can fail them\n"
    "- Marketing a new service line, and why there's no shoulder season\n"
    "- Why HVAC is its own breed and electrical comes last\n"
    "- The board that shows what you're saying no to\n\n"
    "Find JT Services at https://jtserviceco.com"
)
e['publish'] = {
    "approved": False,
    "youtube": {
        "title": e['title'],
        "description": desc,
        "playlist_id": "PLCj0Nkh3V00C-S17nnEE4psF-DgefPWh4",
        "category": "EDUCATION",
        "tags": ["septic", "septic business", "septic company", "plumbing", "HVAC", "home services",
                 "business growth", "NOWRA", "JT Services", "The #2 Septic Podcast"],
    },
    "thumbnail": "07_notes/episode/thumbnail.jpg",
}
json.dump(e, open('06_scripts/episode.json', 'w'), indent=1)
