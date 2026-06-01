"""Thumbnail template — modeled on the ML-in-15 series (ep 9/12/13).

The recipe (don't deviate): ONE bold headline (3 short lines, last line the accent color)
+ ONE strong hero visual + a serif payoff. No multi-element competition.

Canvas is 9:16 (1080x1920). Put the CORE message (headline + hero + payoff) inside the
1:1 safe band so it survives every crop:
    1:1  crop -> y in [420, 1500]
    4:5  crop -> y in [285, 1635]
    9:16      -> full (brand strip, eyebrow, CTA, footer live OUTSIDE the 1:1 band)

Fonts: Inter Tight (headline, bold), JetBrains Mono (chrome), EB Garamond italic (payoff).
Edit HEADLINE / HERO / PAYOFF for your episode. Renders thumb_9x16, thumb_1x1, thumb_4x5.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

for f in font_manager.findSystemFonts():
    try:
        font_manager.fontManager.addfont(f)
    except Exception:
        pass
plt.rcParams["font.family"] = "Inter Tight"

C = dict(bg="#0E1014", deep="#3A3F4A", text="#ECECEC", body="#A8AEB8", mute="#5A6175",
         blue="#58C4DD", orange="#FF862F", yellow="#F7D96F", green="#83C167", red="#FC6255")
MONO, SERIF = "JetBrains Mono", "EB Garamond"
W, H = 1080, 1920
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "output"); os.makedirs(OUT, exist_ok=True)

fig = plt.figure(figsize=(W / 100, H / 100), dpi=100, facecolor=C["bg"])
ax = fig.add_axes([0, 0, 1, 1], facecolor=C["bg"]); ax.set_xlim(0, W); ax.set_ylim(H, 0); ax.set_axis_off()

# background dot field + corner vignettes (the series texture)
rng = np.random.default_rng(7)
ax.scatter(rng.uniform(0, W, 300), rng.uniform(0, H, 300), s=0.8, c=C["deep"], alpha=0.30, edgecolors="none", zorder=1)
ax.scatter(rng.uniform(0, W, 110), rng.uniform(0, H, 110), s=2.2, c=C["deep"], alpha=0.36, edgecolors="none", zorder=1)
for cx, cy in [(0, 0), (W, 0), (0, H), (W, H)]:
    for r, a in [(920, 0.09), (620, 0.10), (360, 0.10)]:
        ax.add_patch(Circle((cx, cy), r, color="#000000", alpha=a, zorder=2))

# chrome (top, outside 1:1)
ax.text(60, 74, "YOUR BRAND", fontsize=25, color=C["mute"], family=MONO, fontweight=500, ha="left", va="center", zorder=20)
ax.text(W - 60, 74, "EP NN / NN", fontsize=25, color=C["orange"], family=MONO, fontweight=500, ha="right", va="center", zorder=20)
ax.text(W / 2, 330, "EYEBROW · ONE LINE", fontsize=27, color=C["orange"], family=MONO, fontweight=600, ha="center", va="center", zorder=20)

# ===== HEADLINE (3 short lines; keep within the 1:1 band, y ~470-720) =====
for y, line, col in [(502, "line one.", C["text"]), (607, "line two.", C["text"]), (712, "the accent line.", C["orange"])]:
    ax.text(W / 2, y, line, fontsize=86, color=col, fontweight="bold", ha="center", va="center", zorder=20)

# ===== HERO (one visual, y ~800-1300) — replace with your episode's hero =====
# (example placeholder box; swap for your real diagram)
ax.add_patch(FancyBboxPatch((W / 2 - 200, 950), 400, 250, boxstyle="round,pad=2,rounding_size=14",
             linewidth=2, edgecolor=C["orange"], facecolor=C["orange"], alpha=0.18, zorder=10))
ax.text(W / 2, 1075, "HERO", fontsize=44, color=C["orange"], fontweight="bold", ha="center", va="center", zorder=12)

# ===== PAYOFF (serif italic) + sub =====
ax.text(W / 2, 1430, "the payoff, in a phrase.", fontsize=58, color=C["text"], family=SERIF, style="italic", ha="center", va="center", zorder=20)
ax.text(W / 2, 1505, "supporting line, smaller", fontsize=27, color=C["body"], ha="center", va="center", zorder=20)

# CTA + footer (9:16 only)
ax.text(W / 2, 1690, "→  how it works, inside", fontsize=32, color=C["orange"], fontweight=600, ha="center", va="center", zorder=20)
ax.text(W / 2, 1858, "@yourhandle   ·   YOUR BRAND", fontsize=24, color=C["mute"], family=MONO, ha="center", va="center", zorder=20)

out9 = os.path.join(OUT, "thumb_9x16.png")
fig.savefig(out9, dpi=100, facecolor=C["bg"]); plt.close(fig)
from PIL import Image
im = Image.open(out9)
im.crop((0, 420, 1080, 1500)).save(os.path.join(OUT, "thumb_1x1.png"))   # IG grid
im.crop((0, 285, 1080, 1635)).save(os.path.join(OUT, "thumb_4x5.png"))   # IG feed
print("thumbnails: 9x16, 1x1, 4x5")
