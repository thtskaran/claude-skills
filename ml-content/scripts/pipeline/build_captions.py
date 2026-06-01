"""Burned-caption builder (.ass), char-offset timed from the VO alignment.

Style mirrors the ML-in-15 series: Inter Tight, white, bottom-center, semi-transparent
back box. Because the alignment is per-CHARACTER for the EXACT text sent, captions are
timed by character offset (no fuzzy word matching) — robust and exact.

IMPORTANT: read TEMPO from scene_spans.json (written by timing.py) so captions and the
tempo-fitted vo_final.mp3 stay in sync. Hardcoding a different tempo desyncs them.

Keeps every caption <= ~55 chars (wraps awkwardly otherwise). Content in your scenes must
stay ABOVE the bottom caption band (keep in-scene mobjects above y ~= -2.7 at 1080p).
"""
import json, pathlib

PROJECT = pathlib.Path.cwd()
A = PROJECT / "audio"
TEMPO = json.loads((A / "scene_spans.json").read_text())["tempo"]
LEAD = 0.10

text = " ".join(p.strip() for p in (A / "vo_script.txt").read_text().strip().split("\n\n"))
al = json.loads((A / "vo_alignment.json").read_text())["alignment"]
cs = [t / TEMPO for t in al["character_start_times_seconds"]]
ce = [t / TEMPO for t in al["character_end_times_seconds"]]
assert len(al["characters"]) == len(text), f"alignment {len(al['characters'])} != text {len(text)}"

chunks, i, start, n = [], 0, 0, len(text)
while i < n:
    c = text[i]
    cut = ((c in ".!?" and (i + 1 >= n or text[i + 1] == " "))
           or (c == "," and (i - start) > 22) or (c == " " and (i - start) > 48))
    if cut:
        chunks.append((start, i + 1)); i += 1
        while i < n and text[i] == " ":
            i += 1
        start = i
    else:
        i += 1
if start < n:
    chunks.append((start, n))

events = []
for k, (s, e) in enumerate(chunks):
    t0 = max(0.0, cs[s] - LEAD)
    t1 = ce[e - 1] + 0.2
    if k + 1 < len(chunks):
        t1 = min(t1, max(0.0, cs[chunks[k + 1][0]] - LEAD) - 0.02)
    events.append((t0, t1, text[s:e].strip()))


def fmt(t):
    h = int(t // 3600); m = int((t % 3600) // 60)
    return f"{h}:{m:02d}:{t - 60 * (h * 60 + m):05.2f}"


HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: cap, Inter Tight, 44, &H00ECECEC, &H00FFFFFF, &H00000000, &H90000000, 1, 0, 0, 0, 100, 100, 0, 0, 1, 3, 1, 2, 120, 120, 70, 1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
(PROJECT / "captions.ass").write_text(
    HEADER + "\n".join(f"Dialogue: 0,{fmt(a)},{fmt(b)},cap,,0,0,0,,{t}" for a, b, t in events) + "\n")
print(f"wrote {len(events)} caption lines, span 0 -> {events[-1][1]:.1f}s")
