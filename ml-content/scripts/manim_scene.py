"""
ml-content — Manim scene template for 3B1B-style explainer videos.

Install:
  pip install manim

Render:
  manim -pqh manim_scene.py HookScene     # preview, high quality
  manim -qk manim_scene.py                # 4K, all scenes
  manim -ql manim_scene.py HookScene      # low quality for fast iteration
"""

from manim import *

# -----------------------------------------------------------------------------
# Locked palette (Manim canonical) — same brand baseline as ml-content carousels
# -----------------------------------------------------------------------------

ML_BG = "#0E1014"
ML_TEXT = "#ECECEC"
ML_BODY = "#A8AEB8"
ML_MUTE = "#5A6175"

# Manim canonical color palette (verbatim 3B1B values)
ML_BLUE = "#58C4DD"
ML_RED = "#FC6255"
ML_YELLOW = "#F7D96F"
ML_GREEN = "#83C167"
ML_TEAL = "#5CD0B3"
ML_PURPLE = "#9A72AC"
ML_ORANGE = "#FF862F"
ML_GOLD = "#F0AC5F"
ML_AMBER = "#F0AC5F"

# Per-project — override these
PRIMARY = ML_AMBER
SECONDARY = ML_BLUE
HIGHLIGHT = ML_ORANGE


# -----------------------------------------------------------------------------
# Scene 1 — Hook
# -----------------------------------------------------------------------------

class HookScene(Scene):
    """The opening hook — typography moment with reveal animation."""

    def construct(self):
        self.camera.background_color = ML_BG

        # Hook text
        line1 = Text(
            "Add 200 lines of XGBoost",
            font="Inter Tight", weight=600,
            font_size=48, color=ML_TEXT,
        )
        line2 = Text(
            "before your reasoning calls.",
            font="Inter Tight", weight=600,
            font_size=48, color=ML_TEXT,
        ).next_to(line1, DOWN, buff=0.2)

        line3 = Text(
            "Get",
            font="Inter Tight", weight=600,
            font_size=48, color=ML_TEXT,
        )
        accent = Text(
            "+12.8%",
            font="Inter Tight", weight=600,
            font_size=64, color=HIGHLIGHT,
        ).next_to(line3, RIGHT, buff=0.4)
        line3_grp = VGroup(line3, accent)
        line4 = Text(
            "accuracy at the same average cost.",
            font="Inter Tight", weight=600,
            font_size=48, color=ML_TEXT,
        )

        bottom = VGroup(line3_grp, line4).arrange(DOWN, buff=0.3)
        bottom.next_to(line2, DOWN, buff=0.6)

        all_text = VGroup(line1, line2, bottom).move_to(ORIGIN)

        # Animations
        self.play(Write(line1), run_time=1.2)
        self.play(Write(line2), run_time=1.0)
        self.wait(0.4)
        self.play(Write(line3), run_time=0.5)
        self.play(FadeIn(accent, scale=1.3), run_time=0.6)
        self.play(Write(line4), run_time=1.0)
        self.wait(2)


# -----------------------------------------------------------------------------
# Scene 2 — Math equation reveal
# -----------------------------------------------------------------------------

class FramingScene(Scene):
    """Math hero — reveal a centered equation with a subtitle."""

    def construct(self):
        self.camera.background_color = ML_BG

        # Eyebrow
        eyebrow = Text(
            "THE FRAMING",
            font="JetBrains Mono", weight=500,
            font_size=20, color=PRIMARY,
        ).to_edge(UP, buff=1.0)

        # Title
        title = Text(
            "Test-time compute is a knapsack.",
            font="Inter Tight", weight=600,
            font_size=56, color=ML_TEXT,
        ).next_to(eyebrow, DOWN, buff=0.6)

        # Math (LaTeX)
        math = MathTex(
            r"\max_\pi \quad \mathbb{E}_x[\,\text{Acc}(x, \pi(x))\,]",
            r"\\",
            r"\text{s.t.} \quad \mathbb{E}_x[\,C(\pi(x))\,] \leq \bar{B}",
            r"\\",
            r"\pi(x) \in \{1, 2, 4, 8, 16\}",
            font_size=44, color=ML_TEXT,
        ).next_to(title, DOWN, buff=1.0)
        # color the multiplier and budget
        math.set_color_by_tex(r"\bar{B}", HIGHLIGHT)
        math.set_color_by_tex(r"\pi", PRIMARY)

        body = Text(
            "Maximize accuracy under an average budget.\nOperators care about $/QPS, not $/query.",
            font="Inter Tight", weight=400,
            font_size=22, color=ML_BODY,
            line_spacing=1.4,
        ).next_to(math, DOWN, buff=0.8)

        self.play(FadeIn(eyebrow, shift=DOWN), run_time=0.6)
        self.play(Write(title), run_time=1.5)
        self.play(Write(math), run_time=2.5)
        self.wait(0.5)
        self.play(FadeIn(body, shift=UP * 0.3), run_time=1.0)
        self.wait(3)


# -----------------------------------------------------------------------------
# Scene 3 — 3D landscape (only when math earns 3D)
# -----------------------------------------------------------------------------

class TerrainScene(ThreeDScene):
    """3D landscape — earned because Acc(x, b) is a 2-axis function."""

    def construct(self):
        self.camera.background_color = ML_BG
        self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES, distance=10)

        # Axes
        axes = ThreeDAxes(
            x_range=[0, 1, 0.5],
            y_range=[0, 4, 1],
            z_range=[0, 1, 0.5],
            x_length=6, y_length=4, z_length=3,
            axis_config={
                "include_tip": False,
                "stroke_color": ML_MUTE,
                "stroke_width": 1.5,
            },
        )

        # Surface — replace `acc` with the paper's actual function
        def acc(d, b):
            # toy mixture: easy plateau + responsive ridge + hard valley
            easy = np.exp(-((d - 0.10) ** 2) / 0.02) * (0.97 + 0.01 * (1 - np.exp(-b)))
            resp = np.exp(-((d - 0.40) ** 2) / 0.03) * (0.30 + 0.60 * (1 - np.exp(-b * 0.6)))
            dim = np.exp(-((d - 0.65) ** 2) / 0.02) * (0.45 + 0.42 * (1 - np.exp(-b * 1.5)))
            hard = np.exp(-((d - 0.92) ** 2) / 0.02) * (0.12 + 0.04 * (1 - np.exp(-b * 0.3)))
            w = easy + resp + dim + hard + 1e-9
            return (easy * 1.0 + resp * 1.0 + dim * 1.0 + hard * 1.0) / w

        surface = Surface(
            lambda u, v: axes.c2p(u, v, acc(u, v)),
            u_range=[0, 1], v_range=[0, 4],
            resolution=(40, 20),
        )
        surface.set_style(
            fill_opacity=0.85,
            stroke_width=0.4,
            stroke_color=ML_MUTE,
        )
        # Color by height
        surface.set_fill_by_value(
            axes=axes,
            colorscale=[(ML_RED, 0.0), (ML_YELLOW, 0.5), (ML_GREEN, 1.0)],
        )

        self.play(Create(axes), run_time=1.5)
        self.play(Create(surface), run_time=4)

        # Slow camera rotation
        self.begin_ambient_camera_rotation(rate=0.08)
        self.wait(8)
        self.stop_ambient_camera_rotation()
        self.wait(1)


# -----------------------------------------------------------------------------
# Scene 4 — Numbers reveal (counter animation)
# -----------------------------------------------------------------------------

class ResultsScene(Scene):
    """Hero number reveal — counter animation."""

    def construct(self):
        self.camera.background_color = ML_BG

        eyebrow = Text(
            "RESULTS",
            font="JetBrains Mono", weight=500,
            font_size=20, color=HIGHLIGHT,
        ).to_edge(UP, buff=1.5)

        # Counter that animates from 0 to 12.8
        counter = DecimalNumber(
            0.0,
            num_decimal_places=1,
            font_size=180,
            color=HIGHLIGHT,
        )
        plus = Text("+", font="Inter Tight", weight=600, font_size=180, color=HIGHLIGHT)
        pct = Text("%", font="Inter Tight", weight=600, font_size=180, color=HIGHLIGHT)
        counter_grp = VGroup(plus, counter, pct).arrange(RIGHT, buff=0.05)
        counter_grp.next_to(eyebrow, DOWN, buff=1.0)

        sub = Text(
            "relative improvement on MATH at fixed average cost",
            font="Inter Tight", weight=400,
            font_size=24, color=ML_BODY,
        ).next_to(counter_grp, DOWN, buff=0.8)

        self.play(FadeIn(eyebrow), run_time=0.5)
        self.add(plus, pct)
        self.play(
            ChangeDecimalToValue(counter, 12.8),
            run_time=2.5,
        )
        self.play(FadeIn(sub, shift=UP * 0.3), run_time=1.0)
        self.wait(3)
