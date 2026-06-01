"""Continuous voiceover via ElevenLabs WITH character timestamps (the 3b1b/15-day way).

One flowing VO track (natural prosody, no per-clip silence) + an alignment JSON used to
time captions and per-scene spans. This is the path that actually works on manimGL
(manim-voiceover's VoiceoverScene is a CE plugin and does NOT subclass InteractiveScene).

Project layout expected:
  project/.env                 # ELEVENLABS_API_KEY=...  and  ELEVEN_VOICE_ID=...
  project/audio/vo_script.txt  # the narration, paragraphs separated by blank lines

Run from the project dir:  python3 .../pipeline/vo_continuous.py
Writes audio/vo.mp3 + audio/vo_alignment.json. Skips nothing — rerun only when the script changes.
"""
import base64, json, os, pathlib, subprocess, sys

PROJECT = pathlib.Path.cwd()
for line in (PROJECT / ".env").read_text().splitlines():
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1); os.environ.setdefault(k, v)
KEY, VOICE = os.environ["ELEVENLABS_API_KEY"], os.environ["ELEVEN_VOICE_ID"]

text = (PROJECT / "audio" / "vo_script.txt").read_text().strip()
text = " ".join(p.strip() for p in text.split("\n\n"))   # one continuous read

import requests
url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}/with-timestamps"
r = requests.post(url, headers={"xi-api-key": KEY, "Content-Type": "application/json"},
                  json={"text": text, "model_id": "eleven_multilingual_v2",
                        "voice_settings": {"stability": 0.38, "similarity_boost": 0.85,
                                           "style": 0.20, "use_speaker_boost": True}},
                  timeout=180)
if r.status_code != 200:
    print("ERROR", r.status_code, r.text[:300], file=sys.stderr); sys.exit(1)
data = r.json()
(PROJECT / "audio" / "vo.mp3").write_bytes(base64.b64decode(data["audio_base64"]))
(PROJECT / "audio" / "vo_alignment.json").write_text(json.dumps({"alignment": data["alignment"]}))

dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                      "-of", "csv=p=0", str(PROJECT / "audio" / "vo.mp3")],
                     capture_output=True, text=True).stdout.strip()
print(f"VO written: {dur} s, {len(data['alignment']['characters'])} chars aligned")
