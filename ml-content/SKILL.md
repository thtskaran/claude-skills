---
name: ml-content
description: Generate publication-grade ML explainer videos and carousels the way 3Blue1Brown actually builds them — in real manimGL (NOT Manim Community Edition), as a tiny domain DSL of self-arranging Mobjects choreographed into transform-driven beats where every motion carries meaning. Overlap is prevented at construction time, not policed after render. Use for: 3b1b-style ML videos, paper-figure animations, IG carousels, infographics, posters.
---

# ml-content

Generate ML explainer content that looks like 3Blue1Brown, not like AI slop.

> ## ⚠️ PRIME DIRECTIVE — treat every video as nuclear. ZERO errors ship.
> The content goes public to an audience that **will** fact-check it. A single wrong number, mislabeled quantity, or overstated claim destroys trust in everything else and gets screenshotted. So: **nothing — not even slightly — may be wrong.** Every spoken line, every on-screen number and label, every caption, and the thumbnail must be **verified against the primary source before it is rendered, and audited again on the rendered video before it ships** (§10, the non-negotiable gate). If you cannot cite the exact source line for a claim, you do not say it, write it, or put it on screen. Soften it or cut it. **No "dramatic license" on numbers.** When in doubt, it is wrong until proven right.

This skill was rebuilt from a full read of **Grant Sanderson's actual production code** (`github.com/3b1b/videos`, 503K LOC, 2015→2026) and **the real manimGL engine** (`github.com/3b1b/manim`). Every rule below is grounded in that source with `file:line` citations. Where this skill once guessed, it now measures.

**The video engine is manimGL** (the 3b1b version), driven by `manimgl`. Manim Community Edition (CE) is a *different library with a different, incompatible API* — code written for one crashes on the other. Static IG carousels use HTML/matplotlib (see the Carousel section); everything animated is manimGL.

---

## 0. Why the old output was slop (read this once)

The previous version of this skill produced overlapping elements, weak animation, no consistency, and infographic-feeling stills. The root causes, now fixed:

1. **It shipped Manim CE code while preaching manimGL.** The old template used `from manim import *`, `MathTex`, `ThreeDScene`, `set_camera_orientation`, `set_fill_by_value`, `Create`, `begin_ambient_camera_rotation` — **none of which exist in manimGL** (`grep` over the entire engine = 0 hits). It would not even run.
2. **100% of real output was actually built in matplotlib**, hand-placing ~57 text calls + ~20 boxes per scene with absolute coordinates. That is the worst possible tool for animation: no relative layout, no transform system, no camera. Overlap is guaranteed.
3. **It treated overlap as a validation problem** (bbox asserts, frame validators, ffmpeg caption-pads) instead of a *construction* problem. 3b1b never validates overlap — it makes overlap structurally impossible by building self-arranging objects.
4. **It treated motion as decoration.** Elements faded in from nowhere as disconnected islands. In real 3b1b, objects are *born from the thing they abstract* (`TransformFromCopy`), so every motion teaches.
5. **Planning was marketing copy with word-count targets.** Real 3b1b planning is an ordered list of named teaching beats that reads top-to-bottom as the narration.

The fix is a different mental model, encoded as the Six Laws below.

---

## 1. The engine reality (the single most important section)

**Start every manim file with:**
```python
from manim_imports_ext import *      # in the 3b1b/videos repo
# or, standalone:  from manimlib import *
```

**Scene base class is `InteractiveScene`** (`interactive_scene.py:66`) — for 2D *and* 3D. In the entire 2025 corpus: `InteractiveScene` subclassed 385 times, `ThreeDScene` (`scene.py:930`) 0 times — it exists but 3b1b never uses it. 3D is achieved on an `InteractiveScene` by moving `self.frame`.

**The camera is `self.frame`** (a `CameraFrame` mobject; `scene.py:112`). Local alias `frame = self.frame` appears 114× in 2025 code. `self.camera.frame` appears 0×.

**Render / iterate:**
```bash
manimgl file.py SceneName              # render
manimgl file.py SceneName -se 120      # drop into IPython at line 120 (the dev loop)
manimgl file.py SceneName -w           # write to file
# inside the embed: checkpoint_paste() runs clipboard code with checkpoint rewind
```

### CE landmines — Table A: these genuinely CRASH on manimGL (absent symbols)

| You must NOT emit (CE) | Use instead (manimGL) | Evidence |
|---|---|---|
| `from manim import *` | `from manim_imports_ext import *` / `from manimlib import *` | CLAUDE.md:59 (loads the wrong library) |
| `MathTex(...)` | `Tex(...)` | grep MathTex over repo = 0; CLAUDE.md:82 |
| `self.set_camera_orientation(phi=,theta=,zoom=)` | `self.frame.reorient(theta, phi, gamma, center, height)` | absent; `camera_frame.py:172` |
| `self.move_camera(...)` | `self.play(self.frame.animate.reorient(...))` | absent |
| `self.begin_ambient_camera_rotation()` | `self.frame.add_ambient_rotation(1 * DEG)` | absent; `camera_frame.py:212` |
| `self.add_fixed_in_frame_mobjects(m)` | `m.fix_in_frame()` | absent (no scene-level helper) |
| `Create(m)` | `ShowCreation(m)` | absent; `creation.py:48` |
| `Unwrite(m)` | `Uncreate(m)` or `FadeOut(m)` | absent |
| `surface.set_fill_by_value(...)` | `surface.set_color(c, opacity)` / `set_color_by_xyz_func(...)` | absent |
| `Circumscribe(m)` | `FlashAround(m)` | absent in engine (the one truly-missing indicator) |
| `Wiggle(m)` (class) | `WiggleOutThenIn(m)` or `rate_func=wiggle` | no `Wiggle` class; `indication.py:355` |
| `ease_in_out_*`, `smoothstep`, `easeOutCubic` | the 15 real rate funcs (§7) | not in `rate_functions.py` |
| `FadeInFrom`, `FadeOutAndShift`, `SpinInFromNothing`, `AddTextLetterByLetter` | `FadeIn(m, shift=, scale=)`, `AddTextWordByWord` | absent |

**Self-check (must return nothing):**
```
grep -nE 'MathTex|from manim import \*|set_camera_orientation|begin_ambient_camera_rotation|move_camera|add_fixed_in_frame_mobjects|set_fill_by_value|\bCreate\(|\bCircumscribe\b|\bWiggle\(|\bUnwrite\(|FadeInFrom|SpinInFromNothing|AddTextLetterByLetter' your_file.py
```

### Table B: these RUN on manimGL but are wrong/stale style — don't emit anyway

| Avoid (valid but off-style) | Prefer | Why |
|---|---|---|
| `class S(Scene)` / `class S(ThreeDScene)` | `class S(InteractiveScene)` | both exist & run, but 2025 corpus is 385× InteractiveScene, 0× ThreeDScene; 3D uses `self.frame` |
| `TransformMatchingTex(a, b)` | `TransformMatchingStrings(a, b)` | `TransformMatchingTex` exists (subclasses Strings) but 3b1b uses Strings |
| `eq.set_color_by_tex(tok, c)` | `Tex(R"...", t2c={tok: c})` or inline `eq[tok].set_color(c)` | `set_color_by_tex` is a real Tex method (`tex_mobject.py:207`) but ~unused; inline `set_color` dominates |
| `Indicate(m)` / `CircleIndicate(m)` | `FlashAround(m)` / `Flash` / `FlashUnder` | both exist & are used (`indication.py:73,142`); modern corpus just reaches for Flash* far more |
| `DEGREES` | `DEG` | `DEGREES` is a live alias of `DEG` (won't crash); 2025 uses `DEG` ~520× vs `DEGREES` 3× |

> The split matters: don't let a self-check grep reject valid 3b1b code. `Indicate`, `TransformMatchingTex`, `set_color_by_tex`, and `DEGREES` are *style* calls, not crashers — only Table A NameErrors.

---

## 2. The mental model (what makes it 3b1b, not slop)

> You are not laying out a frame. You are building a **small cast of self-arranging objects** and **transforming them through a sequence of beats** where each motion is the explanation.

Two layers, every video:

1. **`helpers.py` — the domain DSL.** 4–10 `Mobject` subclasses that build and arrange *themselves* (`WeightMatrix`, `NumericEmbedding`, `EmbeddingArray`, `Dial`, `NeuralNetwork`, `ContextAnimation` — `_2024/transformers/helpers.py`), plus 2–5 `show_*(scene, ...)` choreography verbs. **Define the cast before writing a single `construct()`.**
2. **Scene files** — thin `InteractiveScene` subclasses whose `construct()` is a flat list of `# Beat name` comments, each assembling DSL objects and animating them.

Everything below serves this model.

---

## 3. The Six Laws (non-negotiable)

### Law 1 — Relative layout only. Overlap is structural, not policed.

Real 3b1b layout is overwhelmingly relative: `next_to` used ~10,500×, `arrange` ~2,460× across the repo, versus only a handful of absolute `move_to([x,y,z])` content placements — and nearly all of those absolutes are the *camera*, never content. **Forbid absolute content coordinates.** `move_to([x,y,z])` and `frame.animate.move_to(...)` are for the camera/light source only.

Allowed positioning primitives — content position ALWAYS comes from one of these:
```python
a.next_to(b, DOWN, buff=MED_LARGE_BUFF)     # relative to another object
a.next_to(b, RIGHT).match_y(c)              # compound: x from b, y aligned to c
a.align_to(b, LEFT)                         # share an edge
a.to_edge(UP, buff=LARGE_BUFF)              # to a frame edge (chrome only)
a.to_corner(UL)                             # to a corner (chrome only)
VGroup(*items).arrange(DOWN, buff=MED_SMALL_BUFF, aligned_edge=LEFT)
VGroup(*items).arrange_in_grid(rows, cols, buff=...)
dots = Dot().get_grid(n_rows, n_cols, buff_ratio=0.5)
a.match_x(b) / a.match_y(b) / a.match_width(b) / a.match_height(b)
```

**Boxes and pills are content-sized, never hand-sized:**
```python
rect = SurroundingRectangle(label, buff=SMALL_BUFF)   # measures real glyph bounds
brace = Brace(group, DOWN); brace.get_text("12,288")   # fits the span, anchors at tip
under = Underline(word)                                 # width derived from content
```
`SurroundingRectangle` is used ~1,400× in the repo and **cannot clip or mis-center** because its size = `target.get_shape() + 2*buff` (`shape_matchers.py:22`). Delete every `text_width()` character-count heuristic — it has no analog in real code.

**The buff ladder is the ONLY source of gaps** (`default_config.yml:109`):
```
SMALL_BUFF=0.1   MED_SMALL_BUFF=0.25   MED_LARGE_BUFF=0.5   LARGE_BUFF=1.0
```
Never write `buff=0.37`. Consistent margins across scenes come for free from this ladder.

**Build the group, then place the group.** Assemble a `VGroup` declaratively, `.arrange()` its internals once, then position the whole thing. This is the dominant pattern across the repo's thousands of `VGroup`s. Never position leaf elements against screen coordinates.

**Labels on moving targets follow live:** `label.always.next_to(target, UP, buff=SMALL_BUFF)` (or `add_updater`). A single-frame bbox assert can't catch a mid-animation collision; a re-running `next_to` never collides.

> Because of Law 1, the old "Five-Layer Defense" (bbox asserts + frame validator + ffmpeg caption pad) is **retired**. Overlap is prevented at construction. Keep at most a light visual probe-frame check for *taste and timing*, not collision.

### Law 2 — Motion carries meaning. Born-from, never spawn.

The highest-frequency, highest-leverage technique in the corpus: **a key object enters by transforming from the concrete thing it abstracts**, so the causal link is visible.

```python
# the DALL·E image literally dissolves INTO the numeric vector entries (attention.py:128)
self.play(LaggedStart(*(bake_mobject_into_vector_entries(img, vec) for img, vec in ...)))
# 12,288 numbers collapse into a single symbol E_n  (attention.py:200)
self.play(FadeTransform(entry, sym))
# a formula term is delivered by morphing the data column it denotes (ml_basics.py:642)
self.play(TransformFromCopy(data_column, x_symbols))
```

Transform-family hard counts (attention.py): **`TransformFromCopy` 46 > `FadeTransform` 31 > `ReplacementTransform` 6 > plain `Transform` ~5 ; `TransformMatchingTex` 0.**
- **`TransformFromCopy(src, dst)` is THE workhorse** — source persists, a copy morphs to the destination, so the viewer sees "this *becomes* that" while "this" is still there.
- For equation retitles, `TransformMatchingStrings` (not `...Tex`).
- **Never `FadeIn` a load-bearing object from nothing.** Decorative scaffolding can fade in; the thing the lesson is about must be born from its referent.

**`time_span=(start, end)` choreographs a reveal inside ONE `self.play`** (used 638× in the repo) so a camera move and a multi-part reveal cascade together instead of firing simultaneously:
```python
# the softmax aha — one play, run_time=3, cascaded (attention.py:921)
self.play(
    self.frame.animate.reorient(...),
    GrowArrow(arrow, time_span=(1, 2)),
    FadeIn(label, time_span=(1, 2)),
    TransformFromCopy(ndp_col, softmax_col, time_span=(1.5, 3)),
    run_time=3,
)
```

**`generate_target` / `MoveToTarget`** (127 refs) is how dozens of objects snap into a new arrangement with zero hand-keyed coordinates:
```python
grp.target = grp.generate_target()
grp.target.arrange(RIGHT, buff=0.15)   # mutate the target with normal layout calls
grp.target.scale(0.65).next_to(anchor, DOWN)
self.play(MoveToTarget(grp))
```

### Law 3 — A tiny domain DSL gives consistency.

Every video defines ~6 custom Mobjects/Animations in a `helpers.py` plus ~6 scene-local `get_*`/`show_*` factories. A *vocabulary, not a framework*. This is the mechanism for both consistency and no-overlap (the objects arrange themselves).

> **For ML content, don't start from scratch — vendor 3b1b's transformer DSL** (`NumericEmbedding`, `WeightMatrix`, `EmbeddingArray`, `ContextAnimation`, `value_to_color`). It is the single fastest path to the authentic "columns of real numbers" look. See §13.

**Mobject-subclass recipe** (model: `Dial`, `helpers.py:655`; `MachineWithDials:761`):
```python
class WidgetThing(VGroup):
    def __init__(self, value=0, ...):
        # 1. build sub-parts
        body = Rectangle(...); needle = Line(...)
        # 2. lay them out RELATIVELY (ratio buffers, never move_to([x,y,0]))
        ticks = Line(...).get_grid(1, n, buff_ratio=0.5)
        ticks.set_width(body.get_width() - SMALL_BUFF); ticks.move_to(body)
        # 3. assemble, 4. name every meaningful part
        super().__init__(body, ticks, needle)
        self.body, self.needle = body, needle
        # 5. a state mutator that recomputes geometry+style from the logical value
        self.set_value(value)
    def set_value(self, v):
        self.needle.put_start_and_end_on(self.get_center(), self._value_to_point(v))
        self.needle.set_color(value_to_color(v))     # color is a pure function of value
    def animate_set_value(self, v, **kw):            # 6. methods that RETURN animations
        return AnimationGroup(self.animate.set_value(v), ...)
```

**`show_*(scene, ...)` choreography-verb recipe** (model: `show_matrix_vector_product`, `helpers.py:97`):
- first arg is `scene`; the function calls `scene.play/scene.wait` internally,
- owns its transient highlights via a `last_rects`/`to_fade` accumulator so **exactly one highlight is ever on screen**,
- **returns** the persistent mobjects it created.

**Variants are 2-line subclasses of a shared base overriding one class attribute** — never a copy-pasted `construct()` (model `HighlightEarthOrbit(NearestPlanets)` with `highlighted_orbit = 2`, and its sibling `HighlightMarsOrbit(NearestPlanets)` with `= 3`; `planets.py:2202`). Domain numbers live in ALL-CAPS module constants with one `conversion_factor` (`planets.py:4`), so sizes can't disagree across scenes.

**Large data uses honest ellipsis:** render a finite set, swap one element for `Tex(R"\dots")` (or `ellipses_row=-2`, default in `WeightMatrix`), so big arrays read as big without overflowing (`helpers.py:478, 620`).

### Law 4 — Earned 3D only, and 3D is never static.

3D is earned **only when a quantity's dimensionality is the payload** (a vector space, a surface `f(x,y)=z`, a volumetric field). Roughly half of even the attention video is intentionally flat. A flat data series in 3D is the #1 faux-3D tell — and the old matplotlib "isometric stack of parallelograms" cube is exactly the slop to never produce.

> **Production lesson (§13): 3D actively HURTS a *stack of thin layers*** (interleaved attention layers, a residual tower) — viewed at an angle they collapse into one solid block and the per-layer colors vanish. Render those **flat, face-on**. Reserve 3D for clouds, surfaces, and collapsing volumes.

> **Counter-lesson — over-flattening is its own slop (learned shipping the DeepSeek/Qwen attention series).** Apply "flat by default" too zealously and every scene becomes the same colored square grid. A viewer's note, verbatim: *"it just seems like a single block matrix throughout the whole video, we're lacking elements."* Flatness is honest, but monotony kills retention, and the cure is **variety + rigor**, not decoration:
> - **Rotate the visual primitive across the reel.** Don't reuse the row-of-cells / n×n grid in more than ~half the scenes. Across ~10 beats budget at least: one **numeric-matrix** scene, one **on-screen equation**, one **earned-3D** scene — plus vectors / a plot / a code view.
> - **Earned-3D is earned more often than "half flat" implies — use it.** Three patterns that shipped clean (and read as *not* faux-3D because dimensionality IS the payload):
>   - **A memory/field as a `z=f(x,y)` surface that DEFORMS under its update.** e.g. the gated-delta-rule state: forget = scale heights down, erase = remove a bump, write = raise a new bump. `srf = ThreeDAxes((-3,3),(-3,3),(0,3)).get_graph(lambda x,y: sum_of_gaussians(x,y,bumps)); srf.set_opacity(0.7); srf.always_sort_to_camera(self.camera)` then `Transform(srf, make_surf(new_bumps))` between states; `frame.add_ambient_rotation(0.5*DEG)` to orbit.
>   - **A multi-dimensional tensor as a `Cube` volume that grows or collapses.** The KV cache is *tokens×layers×heads* (grow it: `cube.animate.set_width(w, stretch=True, about_edge=LEFT)`); attention compute is *L×L×d* collapsing to *L×k×d* (`set_width(0.8, stretch=True)`). `box3d(w,h,d)=Cube(opacity=0.3).set_width/height/depth(.., stretch=True)`.
>   - **An embedding space as 3D vectors / a `GlowDots` point cloud** for relevance-as-alignment or nearest-neighbour selection.
>   - **A feature/representation geometry as a polytope of unit vectors** (the superposition reel): `Line(ORIGIN, v)` rays + `GlowDot` tips + faint hull `Line`s, `set_floor_plane('xz')`, and *escalate the dimension* — show the 2-D cases face-on (antipodal pair, then a triangle in-plane), then `reorient` into 3-D for the tetrahedron with `add_ambient_rotation`. The directions in space ARE the payload (a genuine vector space), so it never reads as faux-3D. Sequence the corner readout swaps (`D=\frac{2}{3}` → `D=\frac{3}{4}`) with non-overlapping `time_span` or the speed-fit stretch garbles them.
> - **Show the REAL math, not abstract blocks — the single biggest density win.** Replace a colored grid with the actual numbers + the actual equation:
>   - Numeric matrices/vectors with **exact, consistent** values: `WeightMatrix(values=...)`, `NumericEmbedding(values=...)` (compute the numbers so `Δ = v − Sk` literally checks out on a pause), then `show_matrix_vector_product(scene, M, v)` to animate `o = S q` row-by-row.
>   - Animate a **dot product accumulating** pair-by-pair: `for i: FlashAround(q[i]); FlashAround(k[i]); ChangeDecimalToValue(running_sum, partials[i])`.
>   - Pin the **actual update/score equation** as `Tex` (`S_t = S_{t-1}\alpha_t(I-\beta_t k_t k_t^\top)+\beta_t k_t v_t^\top`, `I_{t,s}=\sum_h w_h\,\mathrm{ReLU}(q_h\cdot k_s)`) with `fix_in_frame()` — **but above `CAP_FLOOR`**: a `to_edge(DOWN)` HUD equation lands *inside* the burned-caption band, so place it at y ≈ −2.4, not −3.4.

There is one camera verb. All five DOF specified together:
```python
self.frame.reorient(theta_deg, phi_deg, gamma_deg, center_tuple, height)
#                   azimuth     polar    roll       look-at      zoom(=visible height)
# static set, or animated inside a play that ALSO moves content:
self.play(self.frame.animate.reorient(-21, 79, 0, (1.13, 0.35, 0.88), 3.81), run_time=5)
```
- Angles in **degrees**. `reorient(0, 0, 0, center, height)` is a flat pan/zoom used constantly even in 2D — the camera is the pointer.
- **Camera args must look hand-tuned, not round.** `reorient(-178, 9, 178, (2.15, 1.12, 0.56), 6.84)`, never `reorient(45, 60, 0)`. (Grant copies exact numbers out of interactive mode.)
- **A 3D scene is never static.** Either chain multiple reorients with multi-second `run_time`s, or `self.frame.add_ambient_rotation(0.5 * DEG)` during holds. Call `self.frame.clear_updaters()` before a new scripted reorient so ambient + scripted motion don't compound.
- `self.set_floor_plane('xz')` when Y is up and Z is depth (makes hand-tuned angles compose intuitively).

3D legibility kit (from the holograms video, the 3D gold standard):
- **Vectors/arrows in 3D** get `vector.always.set_perpendicular_to_camera(self.frame)` so they don't foreshorten edge-on (`geometry.py:798` — it's a `Line` method; every real call site applies it to a vector, never a `Text`). **Text labels** in 3D are kept readable a different way: either lay them into the plane (`label.rotate(PI/2, RIGHT)` + `set_backstroke(BLACK, 3)`) as spatial labels that move with the camera, **or** pin them as a HUD with `fix_in_frame()` (titles/equations/readouts). That two-layer split — spatial vectors face-camera, text labels either in-plane or fixed-in-frame — is the legibility rule.
- Light sources/sparks/dots are **`GlowDot`/`GlowDots`/`TrueDot`/`DotCloud`** (additive glow), **never a shaded `Sphere`** (a Lambert ball reads as a solid ball — faux-3D tell). A beam = ~50 stacked `GlowDots` of rising radius, ~3/n opacity.
- Coplanar stacks separate by tiny graded offsets along `IN`/`OUT` (1e-3…2e-2) to kill z-fighting.
- `surface.always_sort_to_camera(self.camera)` on any translucent surface that will be orbited.
- Real 3D solids use real depth (`Cube().set_shape(w,h,depth)`), never an extruded flat rect — so a side view doesn't collapse.
- **The 3D should not be able to lie:** drive the render from a real point array / real projected data (`basis @ model[word]`), so the picture is a computed consequence of the geometry.

### Law 5 — The metronome (measured pacing).

These numbers are counted from the source, not guessed.

- **play : wait ≈ 1.6 : 1.** Stable across the corpus (attention 216/148, 2025 aggregate 2287/1414). ~3 animated actions per 2 holds. Flag scenes below 1.2 or above 2.0.
- **The default hold is `self.wait()` with no argument = 1.0s, and it is 80% of all waits.** Write the bare call. Don't emit `wait(1)` or `wait(1.7)`.
- **Timed waits come from a small rounded set:** `{0.5, 2, 3, 4, 5}` for content; `{8,10,12,15,20,30}` only for ambient/3D holds. (One `wait(1.5)` and one `wait(0.25)` exist in the *entire* transformers corpus.)
- **95% of plays use the default `run_time=1.0`.** Emit a bare `self.play(...)`. Override only with purpose: `run_time=2` is the deliberate-reveal workhorse (~2× the next value), `3–5` for important/complex reveals, `0.5` for a snappy punch.
- **`run_time ≥ 8` is exclusively camera moves / axis `Rotate` / slow enumerations, almost always `rate_func=linear`.** Never on a text `FadeIn`.
- **`lag_ratio` is an intent dial:** `0.1` = standard gentle stagger (the default, ~2.3× the next value, usually with `FadeIn`); `0.25–0.5` = readable "enumerate, read each" cascade; `0.01–0.05` = near-simultaneous bulk reveal (matrix entries, dot fields); `1.0` = strict succession; `0` = simultaneous. Scale to count with `lag_ratio=1.0/len(items)` to hold total duration constant.
- **`rate_func` is left default (smooth ease) ~97% of the time.** The only overrides that earn their place: `there_and_back` (emphasis pulse returning to rest), `linear` (continuous camera/rotation), `there_and_back_with_pause`, `rush_from` (snappy entrance, often `run_time=0.5`). Never set `rate_func` unless the motion's *meaning* requires it.
- **The authoring unit is the labeled beat:** one `# Capitalized beat` comment ≈ one `self.wait()` (attention: 149 comments / 148 waits). Each beat = 1–2 plays then a wait. Avoid firing 5+ animations before a hold.
- **`self.add()` is the silent reveal** (1 instant add per ~3.5 plays): drop in scaffolding/re-layered elements with zero runtime; animate only the element the eye should follow.
- **Ensembles always stagger.** Many similar objects enter via `LaggedStartMap(FadeIn, group, shift=0.25*DOWN, lag_ratio=0.1)`, never a simultaneous `FadeIn(a), FadeIn(b)` (that stacks — the #1 slop tell). Nest `LaggedStart` + `.shuffle()` for a field of many things so timing isn't mechanical.

### Law 6 — One color per concept; figure/ground discipline.

- **Default everything WHITE on BLACK.** Greys (`GREY_A..E`) for chrome/de-emphasis. Spend a saturated hue only on a load-bearing role, **bound to a named variable reused everywhere** (`value_color = RED`; Q=`YELLOW`, K=`TEAL`, V=`RED`, input=`BLUE_B`). Never flood the frame with color.
- **Color is assigned inline per part** (`part.set_color(NAMED)` — 226× in transformers) and bound to a concept; `t2c=` is fine at construction but used far less. Do **not** color by hand-counted glyph slices — use substring indexing `eq["\\omega"].set_color(PINK)` or `t2c`.
- **Signed numeric grids use `value_to_color`** (`helpers.py:51`): positive→blue (`BLUE_E→BLUE_B`), negative→red (`RED_E→RED_B`), magnitude→lightness, blended in HSL. **Unsigned** data (raw embeddings) uses magnitude-only `GREY_C→WHITE` — never a good/bad diverging scale on neutral data. Forbid hand-setting per-element colors on number grids.
- Real palette is manimGL's `default_config.yml` (see §8 for the full A–E ladder + correct hexes). **`YELLOW` is pure `#FFFF00`**, not the old skill's invented `#F7D96F`.

---

## 4. Workflow

```
User has...                          → Start at...
─────────────────────────────────────────────────────────
Topic/paper, no plan                 → Recon → Beat-sheet → DSL → Build → Ground
A beat-sheet                         → DSL → Build → Ground
A helpers.py + beat-sheet            → Build → Ground
A finished video                     → Grounding pass
```

Always ask what they have and what they need; don't assume the full pipeline.

1. **AHA + Recon.** One sentence: the shift in perspective the viewer leaves with. If it's a fact, not a shift, stop. Then a *lean* recon (see §5) — primary source + 2 independent writeups for anything recent; flag every claim DIRECT/INFERRED/UNCERTAIN.
2. **Beat-sheet** (§6) — the ordered named beats that read as the narration. This replaces the old word-count `brainstorm.md`.
3. **Gate A — claims ledger (§10).** Before writing scene code, verify *every* number/label/claim the beats will assert against the primary source. Fix or cut anything not CONFIRMED. Cheaper to fix on paper than in a rendered scene.
4. **DSL** — write `helpers.py` (and vendor `tb_helpers.py`, §13): the self-arranging Mobjects + `show_*` verbs the beat-sheet needs.
5. **Build** — thin `InteractiveScene` files, beats as `# comments`. The continuous-VO + speed-fit + captions pipeline is §13.
6. **Render → read frames → fix** loop (§13): every scene, every overlap/garble. 3–8 cycles.
7. **Gate B — audit the rendered video (§10).** Sample frames across the whole cut, read each, confirm on-screen numbers/labels/captions/thumbnail are all correct and clean. **Nothing ships until this passes.**
8. **Caption + thumbnail + ship.**

The render→critique→re-render loop still applies: render, sample 5–10 key frames (`manimgl -w` then `ffmpeg -ss T -frames:v 1`, or `manim -ql -s --format=png` for a scene's last frame), read each frame, fix, re-render. 3–8 cycles. But you are now checking *taste, timing, and motion*, not hunting collisions — Law 1 already prevents those.

---

## 5. Recon (lean)

For the paper/topic, produce concise working docs (no word-count targets — quality is whether they're *usable*, not long):

- **`paper-summary.md`** — title + arXiv ID + authors; per-claim DIRECT/INFERRED/UNCERTAIN; the thing studied; method; the numbers that matter; lineage; limitations; why-now; hook angles in tension.
- **`related-work.md`** — lineage tree, predecessor/competitor deltas, what it does and does NOT contribute.
- **`discussions.md`** — the social reception: camps, surfaces to cite, which hook will latch.
- **`moodboard.md`** — references mined from the audience's visual world (Distill.pub, Anthropic Circuits, 3b1b itself), each with one line on what to steal. **For manim, the strongest moodboard is the relevant `_2024/transformers/*.py` scene itself** — point at the exact scene that already solves a similar visual.

Discipline: never quote hard citation counts ("widely cited", not "348 citations"); avoid generic adjectives; flag every recent (≤6 mo) claim for re-verification at publish time. Use BrightData (`mcp__brightdata__scrape_as_markdown`, `search_engine`) for primary + 2 secondary sources; fall back to `WebFetch`/`WebSearch`. **Large scrapes (a full paper/blog) overflow the tool result and save to a file, returning the path** — don't try to read the whole thing inline; spawn a fact-extraction **subagent** with the path + a precise brief ("read all N lines in chunks; return verbatim quotes + exact numbers for these claims"), so the raw text stays out of your context. `WebFetch`'s small model silently drops detail on long pages — prefer scrape-to-file + subagent when you need exact figures. **Gate B tip:** run a final **adversarial-reviewer subagent** — hand it the rendered video + the claims ledger and tell it to *refute* every on-screen number and recompute the arithmetic; it catches what your own frame-sweep rationalizes away.

---

## 6. The beat-sheet (replaces the old brainstorm.md)

The real 3b1b planning artifact is an **ordered, numbered list of named beats** that mirrors `SCENES_IN_ORDER` and the in-`construct()` section comments — it reads top-to-bottom as the spoken script. Model: `ml_basics.py`, `attention.py` section comments, `supplements.py` chapter banners.

`beat-sheet.md` format — one line per beat:
```
NN. BeatName — <imperative narration verb: Show/Ask/Label/Contrast/Highlight> + the single idea
     · operates-on: <which persistent object this beat moves>
     · [REVEAL]  (if this is THE aha: tag reorient + run_time≥2-6 + wait≥2 after)
     · objection: <predicted viewer confusion here> → <the interjection beat that resolves it>
     · caveat:    <if this beat simplifies, name the honesty beat that flags it>
```

Mandatory structure:
- **ESTABLISH** first: nest the topic in known categories (Transformer → Deep Learning → ML → "learn from data"), zooming down to the one concrete object the video manipulates. Never open on a labelled diagram or a definition. Open on the *phenomenon* (the crime scene).
- **GAME-PLAN** beat: an on-screen ordered checklist of the chapter's atomic teaching units.
- **One persistent worked example**, locked (the "fluffy blue creature" / "Michael Jordan → Basketball"), carried by the *same mobjects* from setup to payoff. If any beat introduces a NEW concrete example mid-thread, flag it.
- **Every formula is grounded:** the formula beat sits *after* its motivating concrete beats, and is immediately dismantled back to concrete arrays with color-coded symbol→object mapping (`DescribeAttentionEquation`, `attention.py:1850`).
- **Motivate-by-violation** for any normalizing op (softmax/normalization/masking): show the raw output *failing* the desired property first, then introduce the op as relief.
- **Tag exactly one beat `[REVEAL]`** and give it the reveal rhythm. Setup beats stay at default time.
- **Objection + caveat columns:** in-lesson, per-beat objection handling and scheduled honesty beats wherever you simplify (translate the recon's DIRECT/INFERRED/UNCERTAIN flags into on-screen caveats).
- **RECAP** beat mirrors the opening game-plan with units checked off; mark PREVIEW→PAYOFF pairs.

**Self-check before building:** read the beats top-to-bottom. Do they form a coherent spoken narration where (a) phenomenon precedes formalism, (b) one example carries throughout, (c) the AHA is tagged and paced, (d) every formula is grounded, (e) objections/caveats sit at their trigger points, (f) a recap mirrors the open? If it reads as a feature list, it fails.

---

## 7. manimGL grammar reference (the real catalog)

### Animations that exist (use these by exact name)
- **Reveal:** `FadeIn(m, shift=0.25*DOWN, scale=2)` (most common), `Write(m)` (text/equations; default `rate_func=linear`, auto run_time), `ShowCreation(m)` (strokes/paths), `DrawBorderThenFill(m)`, `GrowFromCenter/GrowFromPoint/GrowArrow`, `FadeInFromPoint(m, point)`.
- **Morph:** `TransformFromCopy(src, dst)` ⟵ workhorse, `FadeTransform(a, b)`, `Transform(a, b)`, `ReplacementTransform(a, b)`, `TransformMatchingStrings(eq1, eq2, key_map={...})`, `FadeTransformPieces`. Use `path_arc=PI/2` for an arced morph (~1,200× in repo).
- **Compose:** `LaggedStart(*anims, lag_ratio=0.1)`, `LaggedStartMap(FadeIn, group, shift=, lag_ratio=)`, `AnimationGroup(*anims)`, `Succession`. Schedule sub-anims with `time_span=(a,b)` and/or per-target `.set_anim_args(run_time=, rate_func=)`.
- **Emphasis (the real set):** `FlashAround(m, time_width=1.5, run_time=2)`, `Flash(point)`, `FlashUnder(m)`, `VShowPassingFlash(path, time_width=1.5, run_time=4)` (glowing pulse along a connection), `FocusOn`, `WiggleOutThenIn`.
- **Numbers:** `ChangeDecimalToValue(dec, target)`, `CountInFrom(dec, start)` — `dec` must be a `DecimalNumber`/`Integer`. For bespoke motion, `UpdateFromAlphaFunc(m, lambda m,a: ...)` (the escape hatch Grant actually uses) over inventing `Animation` subclasses.
- **Move/rotate:** `MoveToTarget(m)` (+ `m.generate_target()`), `Restore(m)` (+ `m.save_state()`), `MoveAlongPath`, `Rotate(m, PI)` (discrete) vs `Rotating(m, TAU, run_time=5, rate_func=linear)` (continuous), `m.animate.method(...)`.

### The 15 rate functions (the ONLY ones that exist)
`linear, smooth (default), rush_into, rush_from, slow_into, double_smooth, there_and_back, there_and_back_with_pause, running_start, overshoot, not_quite_there, wiggle, squish_rate_func(f,a,b), lingering, exponential_decay`. `smooth` is a quintic smoothstep. `squish_rate_func` is a *factory* returning a rate func (windows an ease into part of an animation).

### Text & math
- `Tex(R"...")` — pure math (raw strings always). `TexText("words $math$ words")` — prose with inline math. `Text("plain", alignment="LEFT")` — non-LaTeX (Pango).
- Substring access: `eq["Q"]` (all occurrences, a VGroup), `eq["Q"][0]` (first), `eq[R"\sqrt{d_k}"][0][1:3]` (specific glyphs). Mark selectable substrings with `isolate=[...]` or `t2c` keys (which auto-isolate). Substrings can't partially overlap.
- Color: `Tex(R"e^{i\omega t}", t2c={R"\omega": PINK, "t": BLUE})` at construction, or inline `eq["\\omega"].set_color(PINK)`.
- Animate a number inside an equation: `dec = eq.make_number_changeable("0.00")`, then drive `dec` with an updater/`ValueTracker` — don't rebuild the `Tex`.
- Braces: `Brace(mob, DOWN, buff=0.2)` then `brace.get_text("A.U.")` / `brace.get_tex(R"2R_E")`. There is no `brace_text()` free function. `BraceLabel`/`BraceText` when brace+label move as a unit.
- Legibility: `m.set_backstroke(BLACK, 5)` (width 3 small / 5 labels / 8 headline) on any text over busy content — 42× in transformers, preferred over background rectangles.

### Building blocks
- Matrices/vectors: `DecimalMatrix`, `IntegerMatrix`, `TexMatrix`, `MobjectMatrix`; address via `.get_rows()/.get_columns()/.get_entries()/.get_brackets()/.get_column(i)`. Entries auto-tile; brackets auto-fit. (Prefer the video DSL `WeightMatrix`/`NumericEmbedding`.)
- Graphs: place data-space objects with `axes.c2p(x,y)` / `number_line.n2p(x)`; labels via `add_coordinate_labels()/get_axis_labels()`. Never compute pixel positions.
- Bars are rectangles: `Rectangle(prob * width_100p, bar_height)` (width is positional, first arg = value); `VGroup(*bars).arrange(DOWN, aligned_edge=LEFT)`; `set_submobject_colors_by_gradient(TEAL, YELLOW)`. No `BarChart`/`Axes` for distributions — length-encoding is the point.
- Connectors: pass node *mobjects* as endpoints — `Arrow(boxA, boxB, buff=0.1)` — so endpoints resolve to boundaries. For data flow, *transform the data object* between stages rather than drawing arrow glyphs.
- Animated scalar: one `ValueTracker` + `always_redraw`/updaters + `DecimalNumber.set_value`, so one number drives all dependents and nothing drifts. (455 `ValueTracker`, 253 `always_redraw` in repo.) Two-tier sugar: `m.f_always.method(getter)` and `m.always.method(args)` over raw `add_updater` where it reads cleaner — pass *bound* getters (`orbit.get_start`), not calls.

### Camera / 3D
`self.frame.reorient(theta, phi, gamma, center, height)` (degrees) · `frame.animate.reorient(...)` inside a play · `frame.add_ambient_rotation(1*DEG)` · `frame.to_default_state()` (snap front-on) · `frame.set_height(h)` (zoom) · `self.set_floor_plane('xz')`. Surfaces: `ParametricSurface(lambda u,v: [...], u_range=, v_range=, resolution=(nu,nv))` or subclass `Surface`; built-ins `Sphere, Torus, Cylinder, Cube, Prism, Square3D, ThreeDAxes, TexturedSurface`. Color a surface with `set_color(c, opacity)` + `set_shading(refl, gloss, shadow)` (flat 2D mobjects use `set_shading(0,0,0)`); `always_sort_to_camera(self.camera)` for translucent. Light: `self.camera.light_source.move_to(...)`.

---

## 8. Brand baseline (manimGL `default_config.yml`)

Canvas is **pure black `#000000`**; default mobject color **WHITE**. manimGL's engine default bg is `#333333` — so to get the brand-black canvas, drop a `custom_config.yml` in the project dir (the way the videos repo does). **Verified working** (corner pixel renders `(0,0,0)`):
```yaml
# custom_config.yml — manimgl reads it from the working directory
camera:
  background_color: "#000000"
```

**Core hues** (each has a full A=light → E=dark ladder; `C` is the base alias):
```
BLUE_A #C7E9F1  B #9CDCEB  C/BLUE #58C4DD  D #29ABCA  E #1C758A
RED_A  #F7A1A3  B #FF8080  C/RED  #FC6255  D #E65A4C  E #CF5044
GREEN_A ...     ...        C/GREEN #83C167 ...        E ...
TEAL_C  #5CD0B3   PURPLE_C #9A72AC   GOLD_C #F0AC5F   MAROON ladder
YELLOW_C/YELLOW  #FFFF00 (pure!)   YELLOW_D #F4D345   YELLOW_E #E8C11C
ORANGE  #FF862F (no ladder)
GREY_A #DDDDDD  B #BBBBBB  C/GREY #888888  D #444444  E #222222
GREY_BROWN #736357   PINK #D147BD   WHITE #FFFFFF   BLACK #000000
COLORMAP_3B1B = [BLUE_E, GREEN, YELLOW, RED]   # the canonical 4-stop heatmap
```
Use named constants and their A–E steps — never invent hexes. `value_to_color` (signed blue/red) and `color_gradient(colors, n)` / `interpolate_color_by_hsl` for ramps.

**Color roles** (bind each to a named variable, reuse everywhere): orange = hero/innovation · yellow = single aha pulse (one per video) · blue = data/process · green = correct/converged · red = error/caveat · purple = secondary · grey = chrome/de-emphasis.

**Typography (manim scenes):** math `Tex` renders in `mathastext` (3b1b's look; `\minus` macro available). `Text`/`TexText` default to `CMU Serif`, `alignment="CENTER"` in the videos repo. **Inter Tight / JetBrains Mono are NOT used in manim** — they belong only to HTML/poster assets. `font_size` ladder (4K canvas, `frame_height=8`): `120/96/90` hero · `72/60` headline · `48` (default) `/42/36` body · `30/24` caption/inline · `16` fine print. Pass integers from this ladder.

Chrome (paper title, episode number, brand handle, scene dots) is pinned with `fix_in_frame()`, not an ffmpeg pad.

---

## 9. Audio sync (manimGL has no voiceover plugin — do it yourself)

> **For the proven, shipped pipeline → see §13.** It supersedes the sketch below: one *continuous* ElevenLabs VO with character timestamps, scenes **speed-fit** to narration spans, and burned `.ass` captions. Use `scripts/pipeline/`. The notes below explain why.

`manim-voiceover`'s `VoiceoverScene` is a **Manim CE plugin** and does NOT subclass manimGL's `InteractiveScene` — don't use it here. The entire `videos` corpus contains zero voiceover code (`grep voiceover` = 0 hits), so 3b1b records VO out-of-band and times animations to it. For an automated reels pipeline, do the DIY equivalent that *works on manimGL*:

1. Generate one ElevenLabs clip per narration line, cache to `audio/lines/NN.mp3` (skip if exists → zero re-cost).
2. Measure each clip's duration once (`ffprobe -show_entries format=duration` or `pydub`), store in a `dict`.
3. Drive `run_time` from that duration in the scene:
```python
DUR = json.load(open("audio/durations.json"))   # {"l01": 2.4, "l02": 3.1, ...}

# Beat: "Picture the attention matrix."
self.play(FadeIn(matrix), run_time=DUR["l01"]); self.wait(0.3)
# Beat: "Compression collapses every m columns."
self.play(TransformFromCopy(matrix, comp), run_time=DUR["l02"]); self.wait(0.3)
```
4. Concatenate the line clips (with the small inter-beat gaps) and mux onto the rendered video with ffmpeg. Because each block's `run_time` equals its line's audio length, picture and voice stay aligned by construction.

**TTS copy rules:** spell out acronyms with spaces ("M L P", "key value cache") so the engine reads letter-by-letter; spell out numbers for cadence ("eighty-seven cents"); the on-screen caption can still use the compact form. ElevenLabs SDK: export both `ELEVEN_API_KEY` and `ELEVENLABS_API_KEY`; if the key lacks `voices_read`, call the raw TTS endpoint with your `voice_id` directly (the SDK's `voices()` validation is what trips on that scope).

---

## 10. The zero-error gate (NON-NEGOTIABLE — the Prime Directive made concrete)

Every video is nuclear (see the top of this file). This gate runs **twice**: once on the *script + planned visuals* before rendering, and once on the *rendered video* before shipping. Nothing publishes until both pass clean.

A **claim** is anything a viewer could check, spoken OR on-screen OR captioned OR on the thumbnail: every number, ratio, label, model identifier, layer/expert count, benchmark, price, date, "first to X", and every quantity an axis or readout asserts.

### Gate A — the claims ledger (before rendering)
Build a table of **every** claim from the VO script + every planned on-screen number/label + captions + thumbnail. For each: grade **CONFIRMED** (with the exact primary-source quote + line/section), **WRONG**, or **UNVERIFIED**. Then: fix WRONG, soften UNVERIFIED (`≈`, "reportedly", "the released config", "see Table 1"), and **cut anything you cannot cite.** For 10+ claims, delegate to a subagent: read script + on-screen text → extract every checkable claim → verify against the primary source → CONFIRMED/WRONG/UNVERIFIED with the source line → literal edits.

### Gate B — audit the RENDERED video (before shipping)
The script being right is not enough — **a label or a dramatized number can still be wrong on screen.** Sample frames across the whole video (`ffmpeg -ss T -frames:v 1`, ~every 3–4s), **read each one**, and verify: on-screen numbers match the claims and each other; labels name the quantity correctly; captions match the VO word-for-word; the thumbnail's claims are true; and no title/transition is garbled. Distinguish a real error from a harmless mid-animation still (a counter ticking, a morph in progress) — but a *sustained* wrong frame ships as a wrong frame.

### The four failure modes that actually shipped a wrong video (learn these by name)
1. **Dramatized numbers.** "Stack **a thousand layers**" — the model was ~61 layers. *Never inflate a number for effect.* If the real number is undramatic, describe the phenomenon without a number ("layer after layer", "go deep enough"), don't invent one.
2. **Mislabeled quantities.** A relevance score in [0,1] labeled "**q · k**" (a raw dot product, which would be in the hundreds). The concept was right, the *label* lied. Name on-screen quantities by what they actually are.
3. **Scope overstatement.** "**Each weight** is reduced to four bits" — FP4 was only on the MoE expert weights + the indexer. Say exactly what the source says; "each/every/all" is almost always too broad.
4. **Thumbnail hooks that aren't true.** "for free" when the model is open-weights but priced. A hook may compress, never falsify.

### Standing rules
- Decimal precision past the source reads fabricated (source says ">91%" → write ">91%", not "92.3%").
- Config-specific values (top-k, layer counts, prices) are **not universal law** — anchor to the specific model/version ("V4-Pro", "Claude Opus 4.6") and note it's the released config.
- **Date-drift:** model versions/prices change weekly in 2026+; re-verify within 48h of publishing.
- If it's already posted and an error is found: write the corrected re-export AND a short, honest pinned-comment correction (own it; it builds trust).

---

## 11. Static carousels & posters (matplotlib / HTML — NOT manim)

Carousels are static, so manim is the wrong tool; matplotlib + HTML are right. Use `scripts/carousel_template.html` (brand baseline, 1080×1350 slides) → `scripts/render_carousel.py` (weasyprint → pdftoppm), and `scripts/render_3d.py` for any earned static 3D PNG. **The same Laws apply where they can:** relative layout (CSS flex/grid, not absolute px), one color per concept, content-sized boxes, earned-3D-only (no faux-isometric cubes), 3 phone-readable annotations max. The matplotlib palette in `render_3d.py` is the manimGL palette; **`YELLOW` is `#FFFF00`** (the old `#F7D96F` was wrong).

For the pixel discipline on a hand-placed matplotlib frame, still probe-render mid-scene frames and read them — but prefer building with relative transforms (`axes.transAxes` fractions, `arrange`-like helper functions) over absolute pixels.

---

## 12. Scripts in this skill

- **`scripts/manim_scene.py`** — the real manimGL starter: `from manim_imports_ext import *`, `InteractiveScene`, a small self-arranging DSL, transform-driven beats, `self.frame.reorient` 3D, `set_backstroke`, `SurroundingRectangle`, beat-comment structure. **Copy and adapt; never write CE.**
- **`scripts/helpers_template.py`** — the DSL pattern: a self-arranging `Mobject` subclass + a `show_*(scene, ...)` choreography verb, annotated with the recipe from Law 3.
- **`scripts/pipeline/`** — the proven render-to-ship audio/caption/assembly pipeline (see §13): `vo_continuous.py`, `timing.py`, `build_captions.py`, `assemble.py`.
- **`scripts/thumbnail_template.py`** — 9:16 thumbnail with the 1:1 / 4:5 safe-crop bands baked in (§13).
- **`scripts/render_3d.py`** — matplotlib 3D for *static carousel PNGs only* (palette fixed).
- **`scripts/carousel_template.html`** + **`scripts/render_carousel.py`** — static IG carousel pipeline.

---

## 13. The proven production pipeline (learned shipping reels)

The Laws above are the craft; this is the assembly line that actually shipped a 2-minute manimGL reel end to end. **manimGL renders fine** — `pip install manimgl` (1.7.x), then `manimgl scenes.py SceneName -w --hd --video_dir out --file_name SceneName` writes a flat `out/SceneName.mp4` at 1080p. The `--file_name` flag is what keeps the output flat-named (so `assemble.py` finds `out/<Scene>.mp4`); without it manimGL nests under a media/quality subdir. To re-render one fixed scene, just re-run that one command + re-run `assemble.py` (timing/spans come from the VO and don't change). **The render → read-the-frame → fix loop is not optional** — sampling a frame (`ffmpeg -ss T -frames:v 1`) and actually *looking* at it caught a real overlap on nearly every scene.

### Fast path to 3b1b density: vendor their transformer DSL
For ML content, do NOT hand-build matrices and vectors. Copy `3b1b/videos/_2024/transformers/helpers.py` into the project as `tb_helpers.py`, switch its top import to `from manimlib import *`, and drop the few functions that need external datasets/images. You instantly get the authentic look: `NumericEmbedding(length=N)` (a column of value-colored numbers), `WeightMatrix(shape=(r,c))`, `EmbeddingArray`, `ContextAnimation` (curved attention rays), `value_to_color`, `show_matrix_vector_product`. Scenes built from these read like 3b1b; scenes built from bare cubes read like AI slop.

### 3D vs flat — the decision that actually matters
Earned-3D is real (Law 4), but 3D *hurts* some concepts. Hard-won rule:
- **3D wins:** point clouds (a vast token field via `GlowDots`/`DotCloud`), `f(x,y)=z` surfaces (a loss landscape with descent paths), volumes that collapse (a KV-cache cube shrinking to 1/10), genuine vector spaces. Camera `reorient` + ambient drift.
- **3D loses → use flat face-on instead:** any *stack of thin layers* (interleaved attention layers, a residual-layer tower). Viewed at an angle, thin wide slabs collapse into one solid block and the per-layer colors disappear. A flat, head-on striped panel reads instantly. Never 3D a stack.
- **But don't let "flat" become monotony.** A reel whose scenes are all the same colored grid reads as slop regardless of correctness (real viewer note: *"a single block matrix throughout"*). Per reel, hit the density bar: **real numbers** (numeric matrices, an accumulating dot product) + **a real on-screen equation** + **at least one genuine earned-3D scene** (a deforming surface, a growing/collapsing tensor volume, a vector space). Rotate the visual primitive scene-to-scene. See the Law 4 counter-lesson for the copy-paste patterns.

### Audio + captions + assembly (`scripts/pipeline/`)
One **continuous** VO drives everything (manim-voiceover's `VoiceoverScene` is CE-only — don't use it):
1. **`vo_continuous.py`** — ElevenLabs `/v1/text-to-speech/{voice}/with-timestamps` → `vo.mp3` + `vo_alignment.json` (per-character times). A single continuous read gives natural prosody and zero per-clip silence. Working config: `model_id="eleven_multilingual_v2"`, `voice_settings={stability:0.38, similarity_boost:0.85, style:0.20, use_speaker_boost:True}`; the endpoint returns base64 audio + a per-character start/end alignment you keep verbatim for the captions. The script joins paragraph breaks to single spaces, so write one paragraph per scene.
2. **`timing.py`** — atempo-fit the VO to your length cap (ElevenLabs length varies run-to-run; *nudge tempo, capped ~1.12 so it stays human* — don't re-generate to chase a number, it burns credits; for a fixed-length series just set `TEMPO=1.0` and let the scenes speed-fit), scale the alignment, and emit each scene's narration **span** by matching an anchor phrase. **Anchor gotcha:** anchors match on words normalized to `[a-z0-9]` (lowercased, punctuation + hyphens stripped), so "grouped-query" becomes one token `groupedquery` and "down-project" becomes `downproject` — pick each scene's anchor as a short verbatim word-run that survives that normalization, and never lean on a hyphen as a word boundary.
3. Render scenes `--hd`, then **`assemble.py`** — **SPEED-FIT** each scene's video to its span via `setpts` (time-scale, so nothing is cut and nothing freezes — *no dead air*). Keep factors 0.8–1.2×. **Two-sided rule:** rebuild any scene that plays **>1.28×** (rushed — trim it), AND enrich any scene that plays **<0.6×** (draggy — its VO span ≫ its animation): *add holds, a second emphasis pass, or an extra beat to raise the scene's native duration so the factor climbs back toward ~0.8* — never speed the VO up to fill the gap. `assemble.py` prints every factor; scan that list before shipping. Then concat → burn `captions.ass` → mux VO → loudnorm to −16 LUFS.
4. **`build_captions.py`** — phrase-level `.ass` captions, char-offset-timed from the alignment (read `tempo` from `scene_spans.json` so captions and the tempo-fitted VO stay in sync — a mismatch desyncs them). Bottom-center, Inter Tight, semi-transparent box. **Keep all in-scene content above the bottom caption band** (y ≳ −2.7 at 1080p, the `CAP_FLOOR`) so captions never collide.

### The VO copy register (human, professional, TTS-safe)
- **Not robotic:** kill mechanical enumeration ("Bet one… Bet two… Bet three…"). One through-line, a real voice. Use the `worldbuilder-writing` skill.
- **Not slangy either:** a polished technical-narrator register beats casual slang. *"almost counterintuitive"* not "almost cheeky"; *"a familiar danger"* not "a nasty habit"; *"the accuracy loss is negligible"* not "barely flinched".
- **TTS landmines:** ElevenLabs read "V4" as *"deep 5 four"* — never make TTS speak a model version like "V4"; say "the latest model" or spell it out. Spell acronyms ("M H C") or use full words. Numbers like "1,024" and "128" read fine.

### Thumbnail (`scripts/thumbnail_template.py`)
Match the series: ONE bold 3-line headline (last line the accent color) + ONE hero visual + a serif (EB Garamond italic) payoff, on the dark dotted canvas. Build at **9:16 (1080×1920)** but keep the core (headline + hero + payoff) inside the **1:1 safe band y[420,1500]** (also inside 4:5 y[285,1635]); brand / eyebrow / CTA / footer live *outside* it. The template renders all three crops — verify the **1:1** (the IG-grid view) reads on its own.

### The IG caption
`worldbuilder-writing` method: open inside the reader's world with one concrete verifiable claim, ride a single leverage point (not a feature list), ground every claim with specifics. Keyword-dense for IG search, ≤2 paragraphs, ≤5 hashtags, **no em dashes**, no AI-slop phrases. Ship it twice: `ig-caption.md` (with a `# ` title line) and a plain `output/caption.txt` for copy-paste — strip the md header with `awk 'NR==1&&/^# /{next} NR==2&&/^$/{next} {print}' ig-caption.md > output/caption.txt`, then verify the `.txt` has **no em dashes** and **exactly 5** hashtags.

---

## Render-critique gotchas (add to this after every project)

Bugs the frame-reading loop caught, with the fix — check these before re-rendering:

| Symptom | Cause | Fix |
|---|---|---|
| `Only VMobjects can be passed into VGroup` | 3D `Cube`/`Prism` are `SGroup`s, not VMobjects | put 3D solids in `Group(...)`, not `VGroup(...)` |
| `'Cube' object has no attribute 'set_stroke'` | 3D surfaces have no stroke | use `.set_color(c, opacity)` / `.set_shading(...)` |
| A `fix_in_frame` `Integer` renders **gigantic** | manual `add_updater(set_value)` on a fixed decimal | animate with `ChangeDecimalToValue`, no manual updater |
| `could not broadcast (15,3) into (53,3)` | two animations on one `DecimalNumber` in one play (move + value change) | move via an `add_updater(next_to)`, change value with `ChangeDecimalToValue` |
| Stacked 3D layers look like a solid block | thin slabs viewed top-down hide their faces | flat face-on (see 3D-vs-flat above) |
| Label sits *on* a curve / another element | placed in an occupied region | move it to a measured-empty region; `set_backstroke(BLACK, 5)` |
| A risen/moved mobject covers a label | element animated over fixed text | don't move it over the label, or move the label out first |
| Captions overlap content | in-scene mobject below the caption band | keep content above `CAP_FLOOR` (y ≳ −2.7) |
| A scene plays rushed in the final | scene video ≫ its narration span (speed-fit >1.28×) | rebuild that scene shorter; don't rely on speed-fit alone |
| **Garbled title at a scene's title swap** | `FadeTransform(old_title, new_title)` morphs two *different* texts at the **same** position → ~0.5s of scrambled, illegible glyphs (looks like a render bug when paused) | never morph two unrelated titles in place. Do a clean **`FadeOut(old)` then `FadeIn(new)`**, or fade out/in with opposite `shift=`. Same for any in-scene annotation that swaps text (a label that becomes another). |
| **Two texts overlap mid-cross-fade in the FINAL only** (looked fine in the silent render) | a `FadeOut(a)` + `FadeIn(b)` at the **same spot** in **one** `self.play` — **speed-fit stretches** it (a 1.5× slow scene makes both co-exist ~50% longer), so the brief overlap becomes a readable garble | **sequence them inside the one play with non-overlapping `time_span`**: `FadeOut(a, time_span=(0,0.5))`, `FadeIn(b, time_span=(0.5,1.0))` (fractions of `run_time`). Survives any stretch. |
| **HUD equation/label collides with the burned captions** | a `fix_in_frame()` `Tex`/label placed with `to_edge(DOWN)` sits at y≈−3.4, *inside* the caption band | place HUD math at y ≈ −2.4 (above `CAP_FLOOR` −2.7); put step-labels for a 3D scene in the clear band *above* the surface, not below it |
| On-screen number is wrong even though the script is right | a label/number hand-set in a scene, never grounded | Gate B (§10): every on-screen number/label is a claim — verify it on the rendered frame, not just in the VO |
| **A small/exact `WeightMatrix` shows a phantom "…" dots row or column** | `WeightMatrix`/`NumericEmbedding` default to `ellipses_row=-2, ellipses_col=-2` (a deliberate ellipsis to imply a big array) | pass `ellipses_row=None, ellipses_col=None` for any matrix you want shown in full. For a 1-wide `NumericEmbedding` the col-ellipsis can blank the whole column — set `ellipses_col=None`, or build vectors from a plain cell-column helper |
| **A near-identity / small-valued `WeightMatrix` renders dark, low-contrast** | default `value_range=(-9.9, 9.9)` maps a value of `1.0` to ~10% intensity | pass a tight `value_range` (e.g. `(-1.5, 1.5)`) + explicit `high_positive_color=`/`high_negative_color=` so the diagonal reads bright and off-diagonals stay dim |
| **An auditor flags a matrix-product / dot-product entry as "wrong" on a sampled frame** | `show_matrix_vector_product` and dot-product accumulation animate the running **partial** sum — a mid-frame entry is a correct intermediate, not the full product | only the settled END/hold frame must equal the full product; verify *that* frame, not a mid-accumulation still. (Gate B: distinguish transient from sustained — a partial sum counting up is not an error) |
| **`timing.py`: "anchor not found"** | the anchor isn't a verbatim contiguous word-run after `[a-z0-9]` normalization (hyphens merge tokens) | re-pick the anchor from the exact VO words: "grouped-query"→`groupedquery`, "down-project"→`downproject` |
| **A scene plays draggy in the final (speed-fit < 0.6×)** | the scene's narration span is much longer than its animation | enrich the scene (add holds / a second emphasis pass / an extra beat) to raise native duration — do NOT speed the VO up |
| **A stroke-only ring/shape renders as a filled disk** (esp. faux-3D blobs) | `.set_opacity(x)` on a `Circle`/VMobject sets BOTH stroke AND fill opacity, so `Circle().set_stroke(c,2).set_opacity(0.5)` fills it | use `.set_stroke(c, w, opacity=x)` + an explicit `.set_fill(opacity=0)` for a hollow ring |
| **`Tex` throws a cryptic LaTeX error** (`\UseTextAccent has an extra }`, `\bBigg@ has an extra }`) | fragile constructs — `\big(`/`\bigg`, `{+}` spacing hacks, doubled `\;\;`, or coloring via fragile substring indexing `tex[r"..."]` | use plain `(` `)` (nesting `\cos(w(a+b))` is fine); `\begin{pmatrix}…\end{pmatrix}` works; split mixed math+prose into `Tex(...)` + `Text(...)`; color with `t2c=` at construction or color the whole mobject, not a post-hoc substring slice |

---

## Project folder convention

```
NN-short-slug/
├── paper-summary.md  related-work.md  discussions.md  moodboard.md   # lean recon
├── beat-sheet.md                                                     # ordered named beats
├── tb_helpers.py                                                     # vendored 3b1b transformer DSL (§13)
├── helpers.py                                                        # project-specific DSL (Law 3)
├── scenes.py                                                         # thin InteractiveScene files
├── custom_config.yml                                                # black canvas (§8)
├── .env                                                             # ELEVENLABS_API_KEY, ELEVEN_VOICE_ID
├── audio/  vo_script.txt  vo.mp3  vo_alignment.json  scene_spans.json
├── captions.ass
├── thumbnail.py   ig-caption.md
└── out/FINAL.mp4
```

---

## Appendix — copy-paste manimGL idioms (verbatim grammar)

```python
# Ensemble entrance — always staggered, small drift
self.play(LaggedStartMap(FadeIn, things, shift=0.25 * DOWN, lag_ratio=0.1))

# Born-from morph (the workhorse — source persists)
self.play(TransformFromCopy(data_column, x_symbols), run_time=2)
self.wait()

# Highlight one symbol in an equation
eq = Tex(R"\text{softmax}\left(\frac{K^T Q}{\sqrt{d_k}}\right)V")
self.play(FlashAround(eq[R"\sqrt{d_k}"], time_width=1.5, run_time=2))

# Content-sized box (never hand-sized)
box = SurroundingRectangle(label, buff=SMALL_BUFF).set_stroke(YELLOW, 2)

# Snap many objects into a new arrangement with no hand coords
grp.target = grp.generate_target()
grp.target.arrange(RIGHT, buff=0.15).next_to(anchor, DOWN, buff=MED_LARGE_BUFF)
self.play(MoveToTarget(grp))

# The aha reveal — one play: camera + born-from + cascade, then breathe
self.play(
    self.frame.animate.reorient(-110, 12, 0, payoff.get_center(), 6.7),
    TransformFromCopy(setup, payoff, time_span=(1.5, 3)),
    run_time=3,
)
self.wait(2)

# Real 3D hold — never static
self.frame.add_ambient_rotation(0.5 * DEG)
self.wait(8)
self.frame.clear_updaters()

# Animated number driving dependents
tracker = ValueTracker(100.0)
num = DecimalNumber(0).add_updater(lambda m: m.set_value(tracker.get_value()))
self.play(tracker.animate.set_value(10.0), run_time=2)

# Section-comment teleprompter (each block ≈ one narration sentence)
def construct(self):
    # Add the sentence
    ...
    self.play(LaggedStartMap(FadeIn, words, lag_ratio=0.25)); self.wait()
    # Box the adjectives
    ...
    self.play(LaggedStartMap(DrawBorderThenFill, adj_rects)); self.wait()
    # The reveal — why this works
    ...
    self.play(..., run_time=3); self.wait(2)
```

Add to this appendix after every project. Named idioms compound; named failures don't recur.
