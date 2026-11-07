import json, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
p = '06_scripts/episode.json'
d = json.load(open(p))

d['thumbnail'] = {
    "layout": "center",
    "at": 1392.0,
    "source": "01_footage/c0021.mp4",
    "photo_crop": [850, 0, 1750, 1080],
    "guest": {"at": 1392.0, "photo_crop": [50, 0, 950, 1080]},
    "lines": [["FAILING", "big"], ["DRAIN FIELD?", "box"], ["FIX IT FOR", "big"], ["ABOUT $5,000", "box"]],
    "out": "07_notes/episode/thumbnail.jpg",
    "swap": True,
    "brighten": 1.7,
    "cool": 0.1,
    "headline_w": 500,
    "gamma": 1.6,
    "panel_w": 600,
    "fade_px": 100,
}

desc = (
    "I recorded this one live at the NOWRA Mega-Conference with Stephen Moeller of RioVation. Stephen runs the "
    "business side of the company, and Gig Drewery, who developed the product, handles R&D and engineering. "
    "RioVation's BioMaze drops pods and ceramic diffusers into an existing septic tank and turns it into an "
    "aerobic tank.\n\n"
    "Stephen explains how clean, class one effluent can bring a clogged drain field back, what the job costs "
    "(he puts it in the $5,000 range), how a contractor installs it, and how a 24 unit townhome complex and "
    "two big projects in Liberia and Ghana came out. You will see footage from the Liberia and Ghana installs "
    "and their BMT63HS aerator demo in the episode. The installs are not online anywhere, but RioVation's "
    "YouTube channel has more: https://www.youtube.com/@riovation\n\n"
    "What we cover:\n"
    "- What RioVation does and how the BioMaze got started\n"
    "- Why treated water can bring a failing drain field back\n"
    "- How the pods, diffusers and attached growth work\n"
    "- When it fits a failing system, and what it costs\n"
    "- How installers get started, how long an install takes and why maintenance agreements matter\n"
    "- A $25,000 mound replacement that cost about $5,000 to fix instead\n"
    "- The Liberia and Ghana projects\n"
    "- Design help, commercial jobs and odor control\n"
    "- How long the parts last\n"
    "- Stephen's advice: be willing to try new technology\n\n"
    "Find RioVation at https://www.riovation.com/\n"
    "RioVation's own overview, \"RioVation BioMaze Brief Overview, Time to Get on Board!\": https://youtu.be/zsGWnR26WrM\n"
    "A different demo of the BMT63HS, \"BioMaze BMT63HS, Commercial Wastewater Made Simple\": https://www.youtube.com/shorts/494pjXVBGfw"
)
d['publish'] = {
    "approved": False,
    "youtube": {
        "title": d['title'],
        "description": desc,
        "playlist_id": "PLCj0Nkh3V00C-S17nnEE4psF-DgefPWh4",
        "category": "EDUCATION",
        "tags": ["septic", "drain field", "failing septic system", "septic tank aeration", "wastewater treatment",
                 "septic contractors", "NOWRA", "RioVation", "BioMaze", "The #2 Septic Podcast"],
    },
    "thumbnail": "07_notes/episode/thumbnail.jpg",
}
json.dump(d, open(p, 'w'), indent=1)
print('ok')
