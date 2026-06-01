"""Finalize audio + compute per-scene narration spans from the alignment.

Two jobs:
  1. Tempo-fit the VO to a target length (subtle atempo, preserves pitch). The ElevenLabs
     prosody varies run-to-run, so don't chase exact length by re-generating (burns credits) —
     nudge tempo here instead. Cap the tempo so the voice never sounds rushed (~1.12 max).
  2. Find where each SCENE's narration starts (by an anchor phrase) and emit its [start,end]
     time-span. The scenes are later time-fit to these spans so the voice never desyncs.

CONFIG below is the only thing you edit per project. The anchor is the first few words of
each scene's narration, NORMALIZED (lowercase, no punctuation).
"""
import json, pathlib, re, subprocess

PROJECT = pathlib.Path.cwd()
A = PROJECT / "audio"

# ---- CONFIG (edit per project) ----------------------------------------------
TARGET_SECONDS = 119.0     # aim just under your length cap
TEMPO_CAP = 1.12           # never speed the voice past this (keeps it human)
ANCHORS = [
    ("S01", "a model just read"),
    ("S02", "to pay attention a transformer"),
    ("S03", "deepseeks approach is almost"),
    # ... one (scene_key, normalized first-words) per scene, in narration order
]
# -----------------------------------------------------------------------------

raw = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", str(A / "vo.mp3")], capture_output=True, text=True).stdout.strip())
TEMPO = max(1.0, min(TEMPO_CAP, raw / TARGET_SECONDS))
print(f"raw VO {raw:.1f}s -> TEMPO {TEMPO:.3f}")

subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(A / "vo.mp3"),
                "-filter:a", f"atempo={TEMPO}", str(A / "vo_final.mp3")], check=True)
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", str(A / "vo_final.mp3")], capture_output=True, text=True).stdout.strip())

al = json.loads((A / "vo_alignment.json").read_text())["alignment"]
chars, st, et = al["characters"], [t / TEMPO for t in al["character_start_times_seconds"]], [t / TEMPO for t in al["character_end_times_seconds"]]

words, cur, cs, pe = [], "", None, 0.0
for c, s, e in zip(chars, st, et):
    if c.isspace():
        if cur:
            words.append((cur, cs, pe))
        cur, cs = "", None
    else:
        cs = s if cs is None else cs; cur += c; pe = e
if cur:
    words.append((cur, cs, pe))
nwords = [re.sub(r"[^a-z0-9]", "", w.lower()) for w, _, _ in words]


def find(anchor, frm):
    a = anchor.split()
    for i in range(frm, len(nwords) - len(a) + 1):
        if nwords[i:i + len(a)] == a:
            return i
    raise AssertionError(f"anchor not found: {anchor}")


starts, idx = [], 0
for key, anc in ANCHORS:
    i = find(anc, idx); starts.append((key, words[i][1])); idx = i + 1
spans = {key: [round(s, 3), round(starts[k + 1][1] if k + 1 < len(starts) else dur, 3)]
         for k, (key, s) in enumerate(starts)}
(A / "scene_spans.json").write_text(json.dumps({"total": round(dur, 3), "tempo": TEMPO, "spans": spans}, indent=2))
print(f"VO final: {dur:.2f}s")
for key, (s, e) in spans.items():
    print(f"  {key:8s} {s:6.2f} -> {e:6.2f}   ({e - s:.2f}s)")
