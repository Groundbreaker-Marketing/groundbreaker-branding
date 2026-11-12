import json, sys
P = sys.argv[1]
f = P + '/06_scripts/episode.json'
d = json.load(open(f))
opts = ["I Bought a Jetter and a Belt Press. Now We Just Pump Septic Tanks.",
        "Septic Pumping Is a Trucking Business. Run It Like One.",
        "Call 100 Past Customers, Book 10 to 15 Septic Pumps",
        "Why This Septic Owner Said No to Extra Money",
        "Installs Are Seasonal. Septic Pumping Isn't.",
        "Sometimes I Wish I Hadn't Bought This Septic Company"]
d['title_options'] = opts
d['title'] = opts[0]
old = d['thumbnail']
d['thumbnail'] = {
    "layout": "cutout", "bg": "black", "at": 1133.0, "source": "01_footage/zoom-160057.mp4",
    "lines": old['lines'], "guest": {"at": 1257.0}, "out": "07_notes/episode/thumbnail.jpg",
    "single": {"note": "the earlier one-person thumbnail (Ashley only, side layout), kept as 07_notes/episode/thumbnail-single.jpg",
               "at": old['at'], "source": old['source'], "lines": old['lines'], "photo_crop": old['photo_crop'],
               "out": "07_notes/episode/thumbnail-single.jpg"}}
json.dump(d, open(f, 'w'), indent=1)
