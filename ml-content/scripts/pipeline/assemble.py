"""Assemble the final reel: SPEED-FIT each scene to its narration span, concat, burn
captions, mux the continuous VO (loudness-normalized).

The key idea is SPEED-FIT, not trim/freeze. Each rendered scene is time-scaled (setpts) to
exactly its narration span — so no content is ever cut and no frame is ever frozen (no dead
air). Keep the per-scene factor in ~0.8x..1.2x; if a scene reports a factor below ~0.78
(i.e. it would play >1.28x), it's too long for its span — rebuild THAT scene shorter rather
than let it feel rushed.

Render scenes first at HD:  manimgl scenes.py SceneName -w --hd --video_dir ./out
Then run this from the project dir.
"""
import json, pathlib, subprocess

PROJECT = pathlib.Path.cwd()
OUT = PROJECT / "out"          # where manimgl wrote the scene mp4s
SEG = OUT / "seg"; SEG.mkdir(parents=True, exist_ok=True)
spans = json.loads((PROJECT / "audio" / "scene_spans.json").read_text())["spans"]

# ---- CONFIG: (span_key, scene_video_filename) in playback order ----
SCENES = [
    ("S01", "S01_Hook.mp4"),
    ("S02", "S02_Wall.mp4"),
    # ...
]
# --------------------------------------------------------------------
V = ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", "-an"]


def vdur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                 "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip())


seg_files = []
for key, fname in SCENES:
    src, out = OUT / fname, SEG / fname
    span = spans[key][1] - spans[key][0]
    d = vdur(src)
    factor = span / d
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src),
                    "-vf", f"setpts={factor:.5f}*PTS", "-t", f"{span:.3f}", *V, str(out)], check=True)
    flag = "  <-- RUSHED, rebuild shorter" if factor < 0.78 else ""
    print(f"{fname:18s} {d:5.1f}s x{1 / factor:.2f} -> {span:.2f}s{flag}")
    seg_files.append(out)

(SEG / "list.txt").write_text("\n".join(f"file '{p.name}'" for p in seg_files) + "\n")
concat = OUT / "_concat.mp4"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                "-i", str(SEG / "list.txt"), "-c", "copy", str(concat)], check=True)

final = OUT / "FINAL.mp4"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(concat), "-i", str(PROJECT / "audio" / "vo_final.mp3"),
                "-vf", f"ass={PROJECT / 'captions.ass'}",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k",
                "-map", "0:v", "-map", "1:a", "-shortest", str(final)], check=True)
print("FINAL:", final, "->", round(vdur(final), 2), "s")
