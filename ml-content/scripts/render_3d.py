"""
ml-content — matplotlib 3D rendering template.

Use this as the starting point for any 3D PNG asset.
Locked: dark canvas, LightSource(315,45), phone-readable annotations.

Edit the render_*() functions for the specific math your slide needs.
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, LightSource
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import proj3d

# -----------------------------------------------------------------------------
# Locked palette + paths — change OUT for your project
# -----------------------------------------------------------------------------

OUT = "/path/to/project/3d"
os.makedirs(OUT, exist_ok=True)

BG = "#0E1014"
TEXT = "#ECECEC"
BODY = "#A8AEB8"
MUTE = "#5A6175"

# Manim canonical color palette
BLUE = "#58C4DD"
RED = "#FC6255"
YELLOW = "#F7D96F"
GREEN = "#83C167"
TEAL = "#5CD0B3"
PURPLE = "#9A72AC"
ORANGE = "#FF862F"
GOLD = "#F0AC5F"
AMBER = "#F0AC5F"  # alias

# -----------------------------------------------------------------------------
# Phone-readable annotation helper — locked
# -----------------------------------------------------------------------------

def annotate_pill(ax, x3, y3, z3, text, color, fxy=(0.5, 0.92), arrow=True):
    """Project a 3D point to axes-fraction and draw a bold pill annotation.

    Args:
      ax: 3D axes
      x3, y3, z3: 3D anchor point
      text: pill text (Inter Tight 600 24pt)
      color: pill fill (use Manim palette)
      fxy: axes-fraction position for the pill (top-right is (0.82, 0.84))
      arrow: whether to draw an arrow from pill to anchor

    Standard placements:
      top-left:     (0.18, 0.84)
      top-right:    (0.82, 0.84)
      bottom-left:  (0.18, 0.20)
      bottom-right: (0.82, 0.20)
    """
    x2, y2, _ = proj3d.proj_transform(x3, y3, z3, ax.get_proj())
    inv = ax.transAxes.inverted()
    disp = ax.transData.transform((x2, y2))
    axfrac = inv.transform(disp)
    if arrow:
        ax.annotate(
            text,
            xy=axfrac, xycoords="axes fraction",
            xytext=fxy, textcoords="axes fraction",
            fontsize=24, fontweight=600, color=BG,
            ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.55", fc=color, ec=color, lw=0),
            arrowprops=dict(arrowstyle="-|>", color=color, lw=2.4,
                             shrinkA=2, shrinkB=8,
                             connectionstyle="arc3,rad=0.12"),
            zorder=20,
            family=["Inter Tight", "Inter", "DejaVu Sans"],
        )
    else:
        ax.text(*fxy, text, transform=ax.transAxes,
                fontsize=24, fontweight=600, color=BG,
                ha="center", va="center",
                bbox=dict(boxstyle="round,pad=0.55", fc=color, ec=color, lw=0),
                zorder=20,
                family=["Inter Tight", "Inter", "DejaVu Sans"])


def style_axes(ax):
    """Apply locked axis styling — slate panels, mute ticks."""
    ax.set_facecolor(BG)
    for pane_axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        pane_axis.pane.set_facecolor(BG)
        pane_axis.pane.set_edgecolor(MUTE)
        pane_axis.pane.set_alpha(0.6)
        pane_axis.line.set_color(MUTE)
        pane_axis.label.set_color(BODY)
        for t in pane_axis.get_ticklabels():
            t.set_color(MUTE)
        pane_axis._axinfo["grid"]["color"] = (0.36, 0.38, 0.46, 0.18)
        pane_axis._axinfo["grid"]["linewidth"] = 0.5
    ax.tick_params(colors=MUTE, labelsize=10)


def cube_faces(x, y, z, dx, dy, dz):
    """Return six face polygons for a cuboid. Use with Poly3DCollection."""
    x2, y2, z2 = x + dx, y + dy, z + dz
    return [
        [(x, y, z), (x2, y, z), (x2, y2, z), (x, y2, z)],          # bottom
        [(x, y, z2), (x2, y, z2), (x2, y2, z2), (x, y2, z2)],      # top
        [(x, y, z), (x2, y, z), (x2, y, z2), (x, y, z2)],          # front
        [(x, y2, z), (x2, y2, z), (x2, y2, z2), (x, y2, z2)],      # back
        [(x, y, z), (x, y2, z), (x, y2, z2), (x, y, z2)],          # left
        [(x2, y, z), (x2, y2, z), (x2, y2, z2), (x2, y, z2)],      # right
    ]


# -----------------------------------------------------------------------------
# Example 1 — 3D landscape (Acc(x, b) surface)
# -----------------------------------------------------------------------------

def render_landscape():
    fig = plt.figure(figsize=(13, 9.5), facecolor=BG)
    ax = fig.add_subplot(111, projection="3d")
    style_axes(ax)
    ax.set_position([0.02, 0.06, 0.96, 0.80])

    # Define the 2D domain
    n_x = 60
    n_b = 5
    diffs = np.linspace(0, 1, n_x)
    budgets = np.array([1, 2, 4, 8, 16])
    log_b = np.log2(budgets)

    D, B = np.meshgrid(diffs, log_b)

    # Define your function — replace with the paper's actual quantity
    Z = np.sin(D * np.pi) * (1 - np.exp(-B / 2))

    # Lit shading
    cmap = LinearSegmentedColormap.from_list(
        "amber", [(0.43, 0.34, 0.20), (0.94, 0.67, 0.37), (1.0, 0.83, 0.55)]
    )
    norm = (Z - Z.min()) / (Z.max() - Z.min() + 1e-9)
    facecolors = cmap(norm)
    ls = LightSource(azdeg=315, altdeg=45)
    rgb = ls.shade_rgb(facecolors[..., :3], Z, blend_mode="soft")
    fc = np.dstack([rgb, np.ones_like(Z) * 0.92])

    ax.plot_surface(D, B, Z, facecolors=fc, rstride=1, cstride=1,
                     linewidth=0, antialiased=True, shade=False)

    ax.set_xlabel("input difficulty (rank)", color=BODY, fontsize=12, labelpad=10)
    ax.set_ylabel("budget (log₂)", color=BODY, fontsize=12, labelpad=10)
    ax.set_zlabel("accuracy", color=BODY, fontsize=12, labelpad=10)
    ax.view_init(elev=24, azim=-58)

    # Title in the figure (large) — NOT in 3D plane
    fig.text(0.5, 0.96, "Acc(x, b) — landscape",
             color=TEXT, fontsize=26, fontweight=600, ha="center",
             family=["Inter Tight", "DejaVu Sans"])

    # Three phone-readable annotations max, spread to corners
    annotate_pill(ax, 0.10, 4.0, 0.99, "EASY  Acc≈1", GREEN, fxy=(0.18, 0.84))
    annotate_pill(ax, 0.45, 4.0, 0.85, "RESPONSIVE  climbs", YELLOW, fxy=(0.82, 0.84))
    annotate_pill(ax, 0.92, 0.0, 0.13, "HARD  flat low", RED, fxy=(0.82, 0.22))

    out = os.path.join(OUT, "landscape.png")
    fig.savefig(out, dpi=110, facecolor=BG, edgecolor="none")
    plt.close(fig)
    print(f"saved {out} {os.path.getsize(out)} bytes")


# -----------------------------------------------------------------------------
# Example 2 — 3D bar chart (model × benchmark)
# -----------------------------------------------------------------------------

def render_bars():
    fig = plt.figure(figsize=(13, 8), facecolor=BG)
    ax = fig.add_subplot(111, projection="3d")
    style_axes(ax)
    ax.set_position([0.04, 0.05, 0.92, 0.85])

    models = ["DeepSeek-V3", "GPT-4o-mini", "Qwen2.5-7B"]
    benchmarks = ["MATH", "GSM8K"]
    gains = np.array([
        [12.8, 6.4],   # row 0 = model 0
        [11.2, 5.9],
        [9.7,  4.3],
    ])

    xs, ys, zs, dxs, dys, dzs, colors = [], [], [], [], [], [], []
    cmap = [AMBER, ORANGE, BLUE]
    for i in range(3):
        for j in range(2):
            xs.append(i)
            ys.append(j)
            zs.append(0)
            dxs.append(0.62)
            dys.append(0.62)
            dzs.append(gains[i, j])
            colors.append(cmap[i])

    ax.bar3d(xs, ys, zs, dxs, dys, dzs, color=colors,
             edgecolor=BG, linewidth=0.8, alpha=0.96, shade=True)

    # No in-bar text labels — they overlap in projected space.
    # Number labels go in HTML legend below the figure.

    ax.set_xticks([0.31, 1.31, 2.31])
    ax.set_xticklabels(models, color=BODY)
    ax.set_yticks([0.31, 1.31])
    ax.set_yticklabels(benchmarks, color=BODY)
    ax.set_zlim(0, 16)
    ax.set_zlabel("gain (%)", color=BODY, fontsize=12, labelpad=8)
    ax.view_init(elev=20, azim=-58)

    out = os.path.join(OUT, "bars.png")
    fig.savefig(out, dpi=110, facecolor=BG, edgecolor="none")
    plt.close(fig)
    print(f"saved {out} {os.path.getsize(out)} bytes")


# -----------------------------------------------------------------------------
# Example 3 — translucent volume cube (knapsack idiom)
# -----------------------------------------------------------------------------

def render_cube():
    fig = plt.figure(figsize=(8, 8), facecolor=BG)
    ax = fig.add_subplot(111, projection="3d")
    style_axes(ax)
    ax.set_position([0.0, 0.0, 1.0, 1.0])

    # Outer translucent budget cube
    big = cube_faces(0, 0, 0, 4, 4, 4)
    ax.add_collection3d(Poly3DCollection(
        big, facecolors=(0.94, 0.67, 0.37, 0.10), edgecolors=AMBER, linewidths=1.6))

    # Inner archetype cubes
    g1 = cube_faces(0.4, 0.4, 0.4, 0.7, 0.7, 0.7)
    ax.add_collection3d(Poly3DCollection(
        g1, facecolors=(0.514, 0.757, 0.404, 0.92), edgecolors=GREEN, linewidths=1.0))

    y1 = cube_faces(1.4, 0.4, 0.4, 1.6, 1.6, 1.6)
    ax.add_collection3d(Poly3DCollection(
        y1, facecolors=(0.969, 0.851, 0.435, 0.92), edgecolors=YELLOW, linewidths=1.0))

    p1 = cube_faces(0.4, 1.6, 1.4, 1.2, 1.2, 1.2)
    ax.add_collection3d(Poly3DCollection(
        p1, facecolors=(0.604, 0.447, 0.674, 0.92), edgecolors=PURPLE, linewidths=1.0))

    r1 = cube_faces(2.6, 2.6, 0.4, 0.7, 0.7, 0.7)
    ax.add_collection3d(Poly3DCollection(
        r1, facecolors=(0.988, 0.384, 0.333, 0.92), edgecolors=RED, linewidths=1.0))

    ax.set_xlim(0, 4); ax.set_ylim(0, 4); ax.set_zlim(0, 4)
    ax.set_axis_off()
    ax.view_init(elev=22, azim=-58)

    fig.text(0.5, 0.04, "B̄ — the average budget",
             color=AMBER, fontsize=18, fontweight=600, ha="center",
             family=["JetBrains Mono", "DejaVu Sans Mono"])

    out = os.path.join(OUT, "cube.png")
    fig.savefig(out, dpi=110, facecolor=BG, edgecolor="none")
    plt.close(fig)
    print(f"saved {out} {os.path.getsize(out)} bytes")


# -----------------------------------------------------------------------------
# Main — CLI dispatch
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    targets = sys.argv[1:] or ["all"]
    if "all" in targets or "landscape" in targets:
        render_landscape()
    if "all" in targets or "bars" in targets:
        render_bars()
    if "all" in targets or "cube" in targets:
        render_cube()
    print("done.")
