"""
ml-content — manimGL scene template (3Blue1Brown engine, NOT Manim Community Edition).

This is REAL manimGL grammar. It will NOT run under `pip install manim` (Community
Edition). It runs under 3b1b's manim:  https://github.com/3b1b/manim

    pip install manimgl            # or install from the 3b1b/manim repo
    manimgl manim_scene.py HookScene -w          # render to file
    manimgl manim_scene.py HookScene -se 80      # drop into IPython at line 80 (dev loop)
    manimgl manim_scene.py HookScene             # preview window

Inside the embed, iterate with checkpoint_paste() on a block that starts with a
`# Beat name` comment — first run saves a checkpoint, re-paste rewinds to it.

Hard rules demonstrated here (see SKILL.md §1-3):
  • base class is InteractiveScene (2D and 3D alike) — never Scene/ThreeDScene
  • camera is self.frame; 3D via self.frame.reorient(theta, phi, gamma, center, height)
  • Tex (never MathTex); per-substring color via t2c / eq["sym"].set_color(...)
  • layout is RELATIVE (next_to/arrange/match_*/SurroundingRectangle/buff-ladder) — no
    absolute content coordinates; the only move_to([x,y,z]) is the camera/light
  • objects are BORN FROM their referent (TransformFromCopy), never FadeIn from nothing
  • the metronome: bare self.wait()=1s default; run_time=2 for deliberate reveals;
    LaggedStartMap for ensembles; rate_func left default ~97% of the time
"""

from manim_imports_ext import *   # in the 3b1b/videos repo
# Standalone fallback:  from manimlib import *


# Per-project color roles — bind each concept to ONE named color, reuse everywhere.
INPUT_COLOR  = BLUE_B     # data flowing
WEIGHT_COLOR = BLUE       # learned weights
HERO_COLOR   = ORANGE     # the project's innovation / "look here"
AHA_COLOR    = YELLOW     # the single aha pulse (one per video)


def value_to_color(value, max_value=10.0):
    """Signed colormap: + -> blue, - -> red, magnitude -> lightness.
    Self-contained mirror of the 3b1b video helper (helpers.py:51); NOT in the
    engine, so define it per project. Unsigned data should use GREY_C->WHITE instead.
    """
    alpha = clip(abs(value) / max_value, 0, 1)
    lo, hi = (BLUE_E, BLUE_B) if value >= 0 else (RED_E, RED_B)
    return interpolate_color(lo, hi, alpha)


# =============================================================================
# Domain DSL (Law 3) — a tiny vocabulary of self-arranging objects.
# In a real project these live in helpers.py; inlined here so the file runs alone.
# =============================================================================

class LabeledVector(VGroup):
    """A column of numbers with a symbol label — builds and arranges ITSELF.

    Recipe: build parts -> lay out relatively -> super().__init__ -> name parts
    -> set_value mutator (geometry+style from logical value) -> animate_* methods.
    """
    def __init__(self, values, symbol=R"\vec{E}", height=2.6,
                 pos_color=INPUT_COLOR, **kwargs):
        super().__init__(**kwargs)
        values = np.asarray(values, dtype=float)

        # entries as a real DecimalMatrix (auto-tiled cells, auto-fit brackets).
        # num_decimal_places is a NAMED param — putting it inside decimal_config
        # collides with the default and raises TypeError.
        matrix = DecimalMatrix(
            values.reshape(-1, 1),
            num_decimal_places=1,
            decimal_config=dict(include_sign=True),
        )
        matrix.set_height(height)
        # color is a pure function of value (sign -> hue, magnitude -> lightness)
        for entry in matrix.get_entries():
            entry.set_color(value_to_color(entry.get_value(), max_value=3.0))

        label = Tex(symbol)
        label.set_height(0.5)
        label.next_to(matrix, UP, buff=MED_SMALL_BUFF)   # RELATIVE placement
        label.set_color(pos_color)

        self.add(matrix, label)
        self.matrix, self.label = matrix, label   # name every meaningful part

    def get_entries(self):
        return self.matrix.get_entries()


def show_dot_product(scene, row, col, result_entry, run_time=2):
    """show_*(scene, ...) choreography verb (Law 3).

    Sweeps matched rectangles down `row` and `col` in lockstep while `result_entry`
    ticks to the true dot product. Owns its transient highlights; returns nothing
    persistent here. Model: helpers.py:show_matrix_vector_product.
    """
    def boxes(elems):
        return VGroup(*(SurroundingRectangle(e, buff=0.05).set_stroke(AHA_COLOR, 2)
                        for e in elems))
    row_rects, col_rects = boxes(row), boxes(col)
    total = float(sum(r.get_value() * c.get_value() for r, c in zip(row, col)))
    scene.play(
        ShowIncreasingSubsets(row_rects),
        ShowIncreasingSubsets(col_rects),
        ChangeDecimalToValue(result_entry, total),
        rate_func=linear, run_time=run_time,
    )
    scene.play(FadeOut(row_rects), FadeOut(col_rects))


# =============================================================================
# Beat 1 — Hook. Born-from morph + content-sized boxes + staggered entrance.
# =============================================================================

class HookScene(InteractiveScene):
    def construct(self):
        # Add the sentence (one play, then a 1s breath — the metronome)
        phrase = "a fluffy blue creature roamed the verdant forest"
        sentence = Text(phrase)
        sentence.to_edge(UP, buff=LARGE_BUFF)
        words = VGroup(*(sentence[w][0] for w in phrase.split()))
        self.play(LaggedStartMap(FadeIn, words, shift=0.25 * DOWN, lag_ratio=0.1))
        self.wait()

        # Box the adjectives — boxes are CONTENT-SIZED, color bound to role
        adjs = VGroup(*(sentence[w][0] for w in ["fluffy", "blue", "verdant"]))
        adj_rects = VGroup(*(SurroundingRectangle(w, buff=0.05) for w in adjs))
        adj_rects.set_submobject_colors_by_gradient(BLUE_C, BLUE_D, GREEN)
        adj_rects.set_stroke(width=2)
        self.play(LaggedStartMap(DrawBorderThenFill, adj_rects), Animation(adjs))
        self.wait()

        # Embeddings are BORN FROM the words — not faded in from nowhere
        vecs = VGroup(*(
            LabeledVector(np.random.uniform(-3, 3, 6), symbol=Rf"\vec{{E}}_{i}", height=2.2)
            for i in range(3)
        ))
        vecs.arrange(RIGHT, buff=LARGE_BUFF)          # group arranges itself
        vecs.next_to(sentence, DOWN, buff=LARGE_BUFF)  # then place the whole group
        self.play(LaggedStart(*(
            TransformFromCopy(adjs[i], vecs[i]) for i in range(3)
        ), lag_ratio=0.2, run_time=2))
        self.wait(2)   # let the reveal land


# =============================================================================
# Beat 2 — Equation reveal. Tex + substring color + grounded-from-concrete.
# =============================================================================

class EquationScene(InteractiveScene):
    def construct(self):
        # Eyebrow + headline (chrome pinned to the screen plane)
        eyebrow = Text("THE FRAMING", font_size=30).set_color(HERO_COLOR)
        eyebrow.to_corner(UL, buff=MED_LARGE_BUFF)
        eyebrow.fix_in_frame()
        self.add(eyebrow)

        # Color load-bearing symbols at construction via t2c (no glyph-slice counting)
        eq = Tex(
            R"\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{K^{T} Q}{\sqrt{d_k}}\right) V",
            t2c={"Q": AHA_COLOR, "K": TEAL, "V": RED},
            isolate=[R"\sqrt{d_k}"],   # make the substring selectable for highlight/morph
        )
        eq.set_width(FRAME_WIDTH - 2)
        self.play(Write(eq))      # Write is the text/equation reveal (auto run_time)
        self.wait()

        # Intuition-as-relief: highlight the scaling term when the viewer wants it
        scale_term = eq[R"\sqrt{d_k}"]
        self.play(FlashAround(scale_term, time_width=1.5, run_time=2))
        self.play(scale_term.animate.set_color(HERO_COLOR))
        self.wait(2)


# =============================================================================
# Beat 3 — Earned 3D. self.frame.reorient + ambient drift + real projected data.
# Only because an embedding SPACE is genuinely a multi-axis quantity (Law 4).
# =============================================================================

class EmbeddingSpaceScene(InteractiveScene):
    def construct(self):
        self.set_floor_plane("xz")
        frame = self.frame

        axes = ThreeDAxes((-4, 4), (-4, 4), (-4, 4))
        axes.set_stroke(GREY_C, 1)

        # Real-ish projected points (stand-in for basis @ model[word]); 3D can't lie
        np.random.seed(3)
        coords = np.random.normal(0, 1.4, (40, 3))
        cloud = DotCloud([axes.c2p(*c) for c in coords])
        cloud.set_color(INPUT_COLOR).set_radius(0.05)

        # Two named directions a viewer can hang meaning on.
        # SPATIAL layer: vectors (Arrows) get set_perpendicular_to_camera — that method
        # lives on Line/Arrow, NOT on Text, so labels can't use it.
        v1 = Vector(axes.c2p(2.6, 1.8, 0.4), thickness=3).set_color(HERO_COLOR)
        v2 = Vector(axes.c2p(-1.4, 2.4, 1.6), thickness=3).set_color(AHA_COLOR)
        for v in (v1, v2):
            v.always.set_perpendicular_to_camera(frame)

        # HUD layer: text labels are pinned to the SCREEN plane (fix_in_frame) so they
        # stay readable while the camera orbits — the two-layer legibility rule.
        hud = VGroup(
            Text("king − man", font_size=30).set_color(HERO_COLOR),
            Text("queen − woman", font_size=30).set_color(AHA_COLOR),
        ).arrange(DOWN, buff=SMALL_BUFF, aligned_edge=LEFT)
        hud.to_corner(UR, buff=MED_LARGE_BUFF).set_backstroke(BLACK, 4)
        hud.fix_in_frame()

        # Establishing fly-in: extreme reorient -> calm readable framing, one move.
        # Don't pre-add axes/cloud: self.play auto-adds animated mobjects, and a manual
        # add would flash them at full opacity for one frame before ShowCreation/FadeIn
        # restart from zero.
        frame.reorient(-30, 80, 0, (0, 0, 0), 12)
        self.play(ShowCreation(axes), FadeIn(cloud, lag_ratio=0.02), run_time=2)
        self.play(
            frame.animate.reorient(-21, 72, 0, (0.3, 0.4, 0.1), 9),
            run_time=4,
        )
        self.play(GrowArrow(v1), GrowArrow(v2), FadeIn(hud, lag_ratio=0.2), run_time=2)
        self.wait()

        # A 3D hold is NEVER static
        frame.add_ambient_rotation(0.6 * DEG)
        self.wait(8)
        frame.clear_updaters()
        self.wait()


# =============================================================================
# Beat 4 — Use the DSL verb. Computation shown honestly, one highlight on screen.
# =============================================================================

class DotProductScene(InteractiveScene):
    def construct(self):
        a = LabeledVector([2, -1, 3, 0, 1, -2], symbol=R"q", height=2.6)
        b = LabeledVector([1, 1, -1, 2, 0, 1], symbol=R"k", height=2.6)
        VGroup(a, b).arrange(RIGHT, buff=2.0)

        eq = Tex(R"q \cdot k = 0.0")
        eq.next_to(VGroup(a, b), DOWN, buff=LARGE_BUFF)
        result = eq.make_number_changeable("0.0")

        self.play(FadeIn(a), FadeIn(b))
        self.play(Write(eq))
        self.wait()
        show_dot_product(self, list(a.get_entries()), list(b.get_entries()), result)
        self.play(FlashAround(result, run_time=2))
        self.wait(2)
