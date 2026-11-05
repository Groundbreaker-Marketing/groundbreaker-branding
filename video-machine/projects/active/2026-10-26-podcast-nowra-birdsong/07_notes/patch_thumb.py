import json
e = json.load(open('06_scripts/episode.json'))
e['thumbnail'] = {
    "layout": "center", "at": 1584.0, "source": "01_footage/c0030.mp4", "photo_crop": [1300, 0, 1900, 1080],
    "guest": {"at": 59.5, "photo_crop": [140, 0, 740, 1080]},
    "lines": [["ADD PLUMBING", "big"], ["OR HVAC?", "box"], ["PART 1 OF 2", "small"]],
    "out": "07_notes/episode/thumbnail.jpg",
}
json.dump(e, open('06_scripts/episode.json', 'w'), indent=1)
