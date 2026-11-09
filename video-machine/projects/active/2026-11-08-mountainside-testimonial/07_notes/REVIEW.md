# Mountainside ER+ testimonial: first drafts for Josh's review

Project: `~/apps/clients/groundbreaker-branding/video-machine/projects/active/2026-11-08-mountainside-testimonial`
Footage: `~/inbox/2026-10-28-mountainside-er/` (32 Sony files, 1080p). Interview = C0066 to C0070 (about 20 min). Everything else is B-roll or walk-and-talk
(split confirmed by transcript and contact sheets; see `broll-log.md`). All transcripts: large-v3-turbo (`02_audio/`, readable copies in `07_notes/transcripts/`).

Review folder: `05_renders/review/` (vsl, ads, website, employee). Nothing was uploaded, scheduled or sent. The Meta account was not touched (no upload, no dry run).
Per Josh's go-ahead, I picked the angles, selects and hooks myself; the reasons are below.

## Round 2 (2026-11-09): Josh's three notes

Every file in `05_renders/review/` was re-rendered under the same name. New there: `audio-ab/` (three samples to compare by ear). Nothing was uploaded, no Meta account touched, no Ops task, no feed, R2 or YouTube.

### What changed

| Josh's note | What I found and did |
|---|---|
| 1. John must be centered; show Ashley with him at times | **VSL, website clips, Max's clip:** John (Max in his clip) is centered in a medium close-up cut from the 1080p two-shot, tracked frame by frame. That is a **3.5x to 4.2x crop** of the original for the wide interview clips C0066 and C0067 (windows 460 to 550 pixels wide), 2.3x for C0068 (his closing lines, where the camera is closer) and 2.0 to 2.4x for Max, kept sharp with `podcast/upscale.py` (the Real-ESRGAN model, `--fps 30`, blended 60% AI and 40% plain, the same method as the podcast). It runs at the edge of what the footage gives; the plain crop is soft, the upscaled one is acceptable but still not 4K. A margin keeps Ashley out of every close-up. **The two-shot with Ashley** (cropped to 1.4x so both are fully in frame) opens each of the first three sections with her own question in place of the title card: "...how have you seen things grow in the last six months since we've been working together" (0:09), "so why hire a marketing agency instead of just do it yourself" (0:46), "John just tell us real quick about your business and what is it you do" (1:16). The first two seconds of John's answer stay on the two-shot, and the "Working with the team" and "His advice" sections open on it for 2.5 s. Two reaction shots: Ashley smiling as he says "no shortage of work" (C0066 about 422 to 425 s, VSL 1:53) and as he says "doubled each summer" (VSL 2:21). The "Team" and "Advice" title cards stay (her question before the team section was about lead tracking, and there is no question before his advice). Her question before "Why" is only the last clause of a 20 s question; the long part ("we gave it all for free, there is a whole playbook online...") is cut. **Ads (9:16):** the crop was already tracked on John; I measured his face on the finished frame: 0.50 of the width, every sampled frame, in all three clips. |
| 2. John in the left speaker only | **Confirmed**, on all 5 interview clips: left = John (Max in C0070), right = Ashley. While John talks, his voice is about 12 dB down on Ashley's mic. Every cut now uses only the speaking person's own mic, copied to both ears, never summed. Ashley's mic is used only where she speaks. Checked on every file: left and right carry the same voice (`06_scripts/tools/check_channels.py`: levels equal to within 0.1 dB; the VSL's small L-R difference is the music bed's stereo width). |
| 3. Audio sounds low quality | **It was the mic, not noise.** On C0066 the quiet between his words is 44 dB under his speech. His lav under a jacket has **37.5 dB** between the voice band (500 to 2000 Hz) and 4 to 8 kHz; a normal voice has 20 to 28. Round 1 only normalized loudness. Now: high-pass 80 Hz, an EQ sized from the measurement (a presence bell at 3.2 kHz and a high shelf at 6 kHz, about +4 dB and +11.5 dB for John), a de-esser, a gentle compressor, then two-pass loudness. VSL, website clips and Max's clip: -16 LUFS; ads: -14 LUFS (the Meta gate target); true peak under -1 dBTP everywhere. Max's mic is brighter (24.8 dB gap), so his chain boosts nothing. |

### The A/B samples: `audio-ab/` (same 30 s of John, C0066 28.3 to 58.3 s)
1. `1-round1-as-delivered.mp4`: round 1: left mic on the left ear only, loudness fix only.
2. `2-channel-fix-plus-voice-chain.mp4`: his mic in both ears + the voice chain. **The renders use this one.**
3. `3-channel-fix-plus-enhancement-plus-voice-chain.mp4`: his mic in both ears + ffmpeg's harmonic exciter + the chain.

| Measurement (30 s of John) | 1 round 1 | 2 chain (used) | 3 exciter + chain |
|---|---|---|---|
| Voice band minus 4 to 8 kHz (dB; lower is brighter) | 37.5 | 30.2 | 22.2 |
| Level in 2 to 4 kHz (dB per bin) | 15.8 | 27.9 | 25.2 |
| Level in 4 to 8 kHz (dB per bin) | 2.5 | 18.4 | 25.6 |
| Loudness (LUFS) / range (LU) / true peak (dBTP) | -16.1 / 2.9 / -1.5 | -15.9 / 1.9 / -1.5 | -16.0 / 1.8 / -1.5 |
| Ears | left only | both | both |

Why 2: it brings the voice-to-highs gap from 37.5 to 30.2 dB, just above a normal voice, and the dynamic range tightens from 2.9 to 1.9 LU. Sample 3 overshoots to a 22 dB gap: the exciter makes highs out of harmonics rather than finding the real ones, which can sound brittle or hissy on "s" sounds. Josh and Ashley: listen to 2 and 3 on headphones and tell me if 3 sounds better; switching is one flag.
**Resemble Enhance was not tried.** Setting it up needs a new venv and a pip install (`.venv-enhance`, lines in `dialogue/enhance.py`), and this unattended job could not get the approval for either one. Sample 3 is therefore the harmonic exciter, which is a filter, not a speech model. The installable path is ready: with that venv in place `python -m dialogue ... --enhance` uses Resemble first. Its license (open source, MIT as far as I know) still needs checking in the installed package before commercial use. DeepFilterNet: no noise problem showed up, so not tried.

### Engine (video-machine, by PR)
New `dialogue/` package (`python -m dialogue <camera file> <out.wav> --who L|R|auto --lufs -16`): each person's own mic, who-speaks-when from the mic levels, the voice chain, loudness. `meta_ad.variants` takes it as selects.json `"audio"`; `podcast.upscale` gained `--fps`; 16 tests in `tests/test_dialogue.py` and `tests/test_variants.py` (full suite passes). README section "Dialogue audio". The long-form builder (VSL and web cuts) is still this project's scripts (`06_scripts/tools/build_long.py`), not an engine path; porting it is on the list.

### Rechecked
All six ads: the three kit audits and the Meta gate pass on all 18 files; copy lint passes (still `approved: false`). Captions are re-made from a large-v3-turbo pass over each cut. The VSL is now 3:25 (was 3:17: Ashley's three questions replace three title cards and add about 14 s).

### New questions for Josh
- **Ashley's name** on her lower third is "Ashley Christian, Groundbreaker Marketing" (her name comes from John saying "Ashley" and from your note that she is the interviewer; no title, since none is said on camera). Keep?
- **Her question before "Why"** ("so why hire a marketing agency instead of just do it yourself") quotes the long question's last clause. It reads clean. Her longer question, with the free playbook, is not used.
- **Close-ups look like a close-up, not a medium shot**, because her body sits 340 px from his in the frame. A wider medium would show part of her. Say so if you prefer that.


## Files

| File | Length | Aspect | Where it runs | Opening line | Why this opening |
|---|---|---|---|---|---|
| `vsl/mountainside-er-john-vandervalk-video-sales-letter-16x9.mp4` (+ `.srt`) | 3:25.4 | 16:9 1920x1080 | Sales page, YouTube, email links | "I have a contractor friend that I met and he raved about Josh and Ashley and said that is the best hire I've made to grow a business" | A peer vouching for us is the most believable first thing an owner can hear. It starts at 0.0 s, before any logo, with the lower third at 0.7 s. |
| `ads/9x16/no-third-leg-recognition-h1c1-9x16.mp4` (+ 4x5, 1x1) | 25.6 s | 9:16, 4:5, 1:1 | Meta Reels, Stories, Feed | "Something inside of me kept saying I need that third and fourth leg on the stool for business..." | Fear: one lead source (Facebook Marketplace) that goes dead. Owners who live on one source see themselves. Close: "Josh and Ashley have helped me with the Google side of it and getting Google leads." |
| `ads/9x16/leads-to-hires-proof-h1-9x16.mp4` (+ 4x5, 1x1) | 21.8 s | same | same | "After Ashley and Josh started helping me with Google leads and I started booking work from that..." | Proof in his words: Google leads, booked jobs, "no shortage of work", a machine operator and a driver hired. |
| `ads/9x16/new-services-proof-h1-9x16.mp4` (+ 4x5, 1x1) | 27.3 s | same | same | "We have morphed into a lot more machine work and that is, I would say, in thanks to Ashley and her husband Josh helping us market and Google a little bit better..." | Proof that marketing brings work beyond the first service (site prep, excavation, grading). |
| `ads/9x16/personal-side-objection-h1b1-9x16.mp4` (+ 4x5, 1x1) | 32.7 s | same | same | "I realize in business that with all this new movement we are losing a personal side of it where I don't have someone that I can necessarily bounce ideas off." | Answers "why pay someone when software can do it" without repeating the interviewer's AI question. |
| `ads/9x16/too-many-hats-recognition-h1b1-9x16.mp4` (+ 4x5, 1x1) | 16.8 s | same | same | "If I'm trying to put on multiple hats to run a business I'm not being as effective as I can be in the role that I can crush it in." | Shortest cut; every owner recognizes the line. |
| `ads/9x16/contractor-referral-proof-h1b1-9x16.mp4` (+ 4x5, 1x1) | 23.7 s | same | same | "I have a contractor friend that I met and he raved about Josh and Ashley and said that is the best hire I've made to grow a business." | Peer word of mouth first, then his growth in his own words. |
| `ads/ad-copy-DRAFT.json` | | | | | Primary text, headline, description per variant (lint passes). `approved` is false: Ashley or Josh flips it. |
| `website/mountainside-er-john-vandervalk-testimonial-highlight.mp4` (+ `.vtt`, `-poster.jpg`) | 1:10.9 | 16:9 | Home page or reviews page | same referral line | Referral line, then new services, then the hire, then the coaching calls. 27.8 MB (23.5 MB per minute). |
| `website/mountainside-er-john-vandervalk-google-leads-testimonial.mp4` (+ `.vtt`, poster) | 24.9 s | 16:9 | Google Ads, local lead service pages | "Josh and Ashley have helped me with the Google side of it and getting Google leads." | Matches the service he names. 10.0 MB. |
| `website/mountainside-er-john-vandervalk-more-work-new-services-testimonial.mp4` (+ `.vtt`, poster) | 24.6 s | 16:9 | Pages about growth and more calls | "We have morphed into a lot more machine work..." | One continuous thought. 9.6 MB. |
| `website/mountainside-er-john-vandervalk-coaching-calls-testimonial.mp4` (+ `.vtt`, poster) | 26.8 s | 16:9 | Pages about working with the team and the strategy calls | "If I'm trying to put on multiple hats to run a business..." | Then "the most helpful thing for me ... is having the Zoom calls." 10.5 MB. |
| `employee/mountainside-er-max-driver-employee-clip-16x9.mp4` (+ `.srt`) | 18.3 s | 16:9 | Drop-in clip (see recommendation) | "I'm a driver here at Mountainside ER, I've been here going on three months..." | Max says his name and job on camera (see below). |

Web versions: no burned captions, `.vtt` each, poster JPG each (frame at 6 s, after the lower third), H.264 with faststart, AAC. A lower third (name and company) is burned in on the first 4 seconds; say if you want it off the web files.

### How the VSL runs (about, seconds; round 2 timings)
0:00 cold open (the referral line, John centered, lower third) · 0:09 Ashley asks "how have you seen things grow..." on the two-shot, then John's two legs on a stool · 0:46 Ashley asks "so why hire a marketing agency instead of just do it yourself", then why he hired us ·
1:16 Ashley asks "tell us real quick about your business", then what changed (more services, leads to hires, Max at 2:03, "doubled each summer") · 2:29 "Working with the team" title card, the Zoom calls · 2:49 his Google review card · 2:55 "His advice to other owners" title card · 3:20 end card.
No voiceover. 12 muted B-roll cutaways (3.6 s each), one over every jump cut except the one into Max's insert, and never more than about 14 s of one picture in a row (the two-shot cutaways count as picture changes).
Music: Epidemic Sound "Light Years" by Out To The World, recording id `e8da90fe-1284-48f9-aa10-0e9262e72a00`, cut to length, about 17 dB under the dialogue. The ads have no music bed.
Ads: each is hook, proof, then a 2.6 s end card (logo, Book a Strategy Call, groundbreakermarketing.com/calendar). Burned captions use the kit's caption preset (white, word weights). 2 to 4 muted cutaways per ad.

### Gates (ads)
Kit audits (audio, captions, visual): PASS on all six masters. The audits run on the clip before the end card (a still card with silence reads to them as frozen frames and dead air; see the SOP entry), and the cutaway stretches are exempted from the visual crop check. Meta gate: PASS on all 18 files (9:16, 4:5, 1:1), no warnings. Copy lint: PASS.

## The employee clip

**Who:** Max, a driver at Mountainside ER+ (his name is said on camera by the interviewer, "I'm here with Max from Mountainside ER"; his job he says himself). No last name is said, so none is used. File: C0070 (2:14 of raw footage).
**What he says:** he has been there about three months, mostly drives and runs the loader when needed, hauls material to sites and quarries; his favorite part is operating heavy equipment; his least favorite is the long hours in the truck; the biggest thing he learned is operating equipment; the life lesson is patience and responsibility. **He says nothing about Groundbreaker, marketing or leads.**
**Recommendation:** use him only as a proof beat inside the VSL (done: 1:54 to 2:08, right after John says the leads let him hire a machine operator and a driver), and not as his own Short or an ad. On his own he sells nothing about us and could read as a recruiting video for Mountainside. The 18 s file in `employee/` is the same insert plus his "favorite part" line, for anyone who wants a drop-in. Do not use any other line of his. Check with John first (open question 6).

## Every number or result claim John makes

Source times are in the original clip (seconds). "Used" = appears on screen in a cut.

| Claim (his words) | Clip, time | Used in |
|---|---|---|
| "year over year in the last two years we have doubled each summer and the goal is to double again next year" | C0066 436.4 to 444.5 | VSL, website highlight, ad contractor-referral |
| "allowed me to hire a machine operator and driver" / "I was able to hire another driver" | C0066 416.9 to 436.4 | VSL, highlight, google-leads clip, ads leads-to-hires and contractor-referral |
| "there is no shortage of work" (also "a there's a shortage of good contractors") | C0066 416.9 to 427.1 | same as above (copy quotes "no shortage of work") |
| "best hire I've made to grow a business" (a contractor friend's words, told by John) | C0067 74.2 to 83.0 | VSL, highlight, ad contractor-referral (copy quotes it) |
| "people ask us if we offer any other services such as site prep or excavation or grading" | C0066 39.9 to 49.5 | VSL, highlight, more-work clip, ad new-services |
| "June was a record month, July we were able to increase that by about 15 [unit not spoken] and we have been on that trajectory up to September and ... a record month in October" | C0066 154.7 to 175.1 | NOT used: the unit is missing ("about 15" what?). Confirm with John. |
| "we lost over a hundred thousand dollars" (his earlier building business, before us) | C0066 85.9 to 94.7 | NOT used |
| "I started in 2024 ... worked 80 hours a week", "by July of 2025 ... hire another employee" | C0066 252 to 292 | NOT used |
| "Can I afford to spend $100 a day?" (his question, ad spend) | C0068 77.2 to 80.1 | cut out on purpose (looks like pricing) |
| Max: "going on three months" | C0070 8.3 to 19.4 | VSL, employee clip |
| Google review (verbatim, 2026-08-19, from Josh): "Can't rave enough about Ashley and her team! Great communication, coaching and now I'm converting leads on Google. Thanks Ashley!" | n/a | VSL card |

Please confirm the first row before anything runs: John says the company doubled each summer, but he does not credit us for the doubling. Each cut puts it next to his Google-leads lines, which implies we helped; he does say the leads let him hire. Safest: keep it as his sentence, never as our claim.

## Decisions and open questions for Josh

1. **"Doubled each summer"** (row 1 above): keep, or drop it from the referral ad and the highlight?
2. **VSL closing lines.** I cut his "Can I afford to spend $100 a day?" (reads as pricing). Without it, "it depends on the capacity you have and the desire you want to truly grow with a good team..." answers "how can marketing help me" a little sideways. Option: end on the pie line and drop the last two pieces.
3. **Spoken letters.** He says "I realized a there's a shortage of good contractors and b there is no shortage of work". Captions keep it exactly, so "a" and "b" appear (VSL, highlight, google-leads clip, ad leads-to-hires).
4. **"Running your mind ragged"** (closing line, VSL): that is what the transcript heard; please listen once (C0068 about 87 to 89 s). It may be "running yourself ragged". Captions must be his exact words.
5. **No "call us" line.** He never tells anyone to call us on camera; the closest are his advice lines. The call to action is the end card only.
6. **Things in the footage John may not want public (not used):** the story of nearly not hiring Max "because of his life experiences and some poor choices" (C0066 about 292 to 308 s); the $100,000 loss; a personal-health remark in a walk-and-talk (C0045); customers and another company named or criticized in the walk-and-talks (C0046, C0048, C0050, C0043). Josh's note says permission covers the footage, but I would show him the Max story before posting anything with Max in it.
7. **Our "ER+" vs his "ER".** Captions show his words ("Mountainside ER"); the lower thirds and card say "Mountainside ER+" (the jackets say ER+).
8. **Website topics.** He says "Google leads" and "the Google side", never "Google Ads", the website or SEO on camera in what I used. So the topic clips are Google leads, more work and new services, and the coaching calls. A website or SEO clip is not possible from this footage.
9. **Look.** The sit-down is a 1080p two-shot with John small in frame. The 9:16 ads are punched in about 2.5x and are softer than the 16:9 cuts; a 4K re-shoot would fix it. Ad captions use the kit preset (white with word weights); the VSL captions turn lime as each word is spoken. Say if you want the ads in lime too.
10. **The Google review card** shows no star rating (not given) and credits him as "John Vandervalk, Mountainside ER+ · August 2026".
11. **The interviewer** (a woman, off the mic) is never heard in a cut and only seen from behind in one B-roll shot at 3:02 of the VSL. Fine?
12. **Not done by me:** no upload, no scheduling, no Meta dry run, no Ops task, no feed, R2 or YouTube. Ad copy is a draft, `approved: false`.
13. **Git.** See the run log: the video-machine engine changes are merged (PR #96); the client repo files (this project's notes, scripts, copy, `brand.json`, run log) are on disk but git in `groundbreaker-branding` needed an approval this unattended job could not give. See the end of the final message.
