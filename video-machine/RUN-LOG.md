# Groundbreaker Marketing video-machine run log

One entry per project, newest first. This is the client half of the SOP; the rules and the
engine lessons live in `documentation/ads-workflow-SOP.md` in the video-machine repo. Fill this
in at the end of EVERY project (ad-machine SOP step 7): what worked, what broke, what the agent
misunderstood, what was done by hand. A producer who cannot push to the engine repo puts engine
lessons under "For the engine"; whoever maintains the engine ports them into the SOP.

### 2026-10-06 podcast-episode (first Zoom podcast episode + 15 Shorts)
- Worked: podcast.zoom pull of a 30-minute personal-room recording (two parts); podcast.transcribe
  (large-v3-turbo, ~0.7x real time); podcast.episode built a 25:15 episode from 26:44 (61 fillers,
  22 stammered repeats, 4 talking-through-it phrases cut; -16.1 LUFS; MP3, SRT, chapters). 15
  Shorts 32 to 51 s from the same transcript; copy lint clean; audit-audio and audit-captions PASS
  on all 15. Delivered to Drive Podcast/Solo Episode - Publish Your Prices (Oct 6 2026) with a
  review doc of titles, descriptions and chapters.
- Broke: Zoom returned 404 on every download until the whole meeting finished processing (about
  8 minutes). A flat 104-term select expression crashed FFmpeg's parser ("Cannot allocate memory");
  nested as a balanced tree it works. A zero-length caption event (two words with one timestamp)
  made FFmpeg drop the lower third for the entire episode; caught on the review stills, fixed in
  both builders, episode and 3 clips re-rendered. Shell expansion ate "$500" in a chapter title.
  audit-visual FAILs 11 clips on Zoom's own 0.3 to 0.7 s picture holds (in the source, not the cut).
- Agent misunderstood: first read part 2 as a continuation; it was a full retake (part 1 unused).
- Done by hand: show name captioned WEQ from Emma's 10-06 email (Whisper heard WEC); title of the
  car-shopping clip says "five new drivers" since the ages were not stated.
- For the engine: turn on Zoom HD + "optimize for 3rd-party editor" before the 10-14 taping.
- v2 the same evening (Ashley: "a little too aggressively edited for ums and pauses, it gets cut
  off and awkward in a few places"; AI upscale look approved): measured 91 of 103 episode joins and
  77 of 88 Shorts joins in sound. Rebuilt with podcast/cutpoints.py (video-machine#13): ums and
  stammers cut only where the sound dips 25 dB both sides (17 of 61 ums), pauses up to 1 s kept,
  cuts placed by real voice edges. Episode 26:09, 27 joins, none in speech. Shorts: glued trims
  restored and hidden from captions, a few boundaries moved by hand (google-ai-calls lost its
  "first client" ending; description updated). Source AI-upscaled to 1080p (63 min). v1 kept in
  Drive under "v1 (first edit)". audit-visual "frozen" flags on 12 clips checked: no hold over
  4 frames; low motion after the upscaler removed compression noise.
- v3 2026-10-07: Ashley found the full AI look too strong ("about half way"; the editing itself
  "is great"), then loved half strength. Source = zoom-144723-ai50.mp4 (podcast.upscale --strength
  0.5, video-machine#15), same cut. Drive: main files = half AI; v1 and v2 (full AI) under
  "Older versions". Half strength is now the engine default.

### 2026-10-05 day-hooks (first organic Shorts)
- Worked: Zoom API pull (S2S app "GBM Recordings") of 11 takes recorded from the end-of-day hook
  scripts; 5 Shorts built with shorts.build (framed layout), copy lint clean, audit-audio and
  audit-captions PASS on all five.
- Broke: Zoom cloud recordings are 640x360 (no HD setting on), so a full-screen 9:16 crop looked
  soft; framed layout chosen by Ashley. Zoom froze the video 2.5 s mid-sentence in take 153052, so
  that sentence was spliced from take 152806. A 0.6 s freeze remains in the first second of
  lifetime-value (single take); two 0.36 s hitches mid-clip in smaller-map and are-you-staying.
- Agent misunderstood: nothing flagged yet.
- Done by hand: Ashley picked the layout, cut "Google headquarters in San Francisco" (Google's HQ
  is Mountain View), kept the "comment value" CTA (she sends the follow-up), confirmed the pump-truck
  client is OK with the clip.
- For the engine: whisper starts the first word early; build now trims to the first sustained voice.

### YYYY-MM-DD <project>
- Worked:
- Broke:
- Agent misunderstood:
- Done by hand:
- For the engine:
