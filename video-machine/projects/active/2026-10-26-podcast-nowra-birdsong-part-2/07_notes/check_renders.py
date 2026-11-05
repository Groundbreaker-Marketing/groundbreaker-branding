import json, os, subprocess, sys, tempfile
# Re-transcribe the first and last 4 s of each rendered Short (the audio as it plays) and print the
# words with their times, so a clipped first syllable, a half word at the start or a cut-off last word
# shows up without relying on the source transcript's clock. Also prints the render's length.
#   python 07_notes/check_renders.py [id ...]
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from faster_whisper import WhisperModel
S = json.load(open('06_scripts/shorts.json'))['clips']
only = set(sys.argv[1:])
m = WhisperModel('large-v3-turbo', device='cpu', compute_type='int8', cpu_threads=os.cpu_count() or 4)
tmp = tempfile.mkdtemp()
for c in S:
    if only and c['id'] not in only:
        continue
    mp4 = '05_exports/shorts/%s.mp4' % c['id']
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', mp4],
                               capture_output=True, text=True).stdout)
    for side, ss in (('START', 0.0), ('END', max(0.0, dur - 4.0))):
        wav = os.path.join(tmp, '%s-%s.wav' % (c['id'], side))
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-t', '4', '-i', mp4, '-ac', '1', '-ar', '16000', wav], check=True)
        segs, _ = m.transcribe(wav, word_timestamps=True, language='en', vad_filter=False,
                               condition_on_previous_text=False)
        ws = [w for s in segs for w in (s.words or [])]
        txt = ' '.join('%s[%.2f-%.2f]' % (w.word.strip(), w.start, w.end) for w in ws)
        print('%-20s %5s (%.1f s): %s' % (c['id'], side, dur, txt))
