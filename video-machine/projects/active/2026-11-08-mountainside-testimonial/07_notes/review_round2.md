## Round 2 (2026-11-09): Josh's three notes

Every file in `05_renders/review/` was re-rendered under the same name. New there: `audio-ab/` (three samples to compare by ear). Nothing was uploaded, no Meta account touched, no Ops task, no feed, R2 or YouTube.

### What changed

| Josh's note | What I found and did |
|---|---|
| 1. John must be centered; show Ashley with him at times | **VSL, website clips, Max's clip:** John (Max in his clip) is centered in a medium close-up cut from the 1080p two-shot, tracked frame by frame. That is a **3.5x to 3.9x crop** of the original (about 520 by 290 pixels of the frame), kept sharp with `podcast/upscale.py` (the Real-ESRGAN model, `--fps 30`, blended 60% AI and 40% plain, the same method as the podcast). It runs at the edge of what the footage gives; the plain crop is soft, the upscaled one is acceptable but still not 4K. A margin keeps Ashley out of every close-up. **The two-shot with Ashley** (cropped to 1.4x so both are fully in frame) opens each of the first three sections with her own question in place of the title card: "...how have you seen things grow in the last six months since we've been working together" (0:09), "so why hire a marketing agency instead of just do it yourself" (0:46), "John just tell us real quick about your business and what is it you do" (1:16). The first two seconds of John's answer stay on the two-shot, and the "Working with the team" and "His advice" sections open on it for 2.5 s. Two reaction shots: Ashley smiling as he says "no shortage of work" (C0066 about 422 to 425 s, VSL 1:53) and as he says "doubled each summer" (VSL 2:21). The "Team" and "Advice" title cards stay (her question before the team section was about lead tracking, and there is no question before his advice). Her question before "Why" is only the last clause of a 20 s question; the long part ("we gave it all for free, there is a whole playbook online...") is cut. **Ads (9:16):** the crop was already tracked on John; I measured his face on the finished frame: 0.50 of the width, every sampled frame, in all three clips. |
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

