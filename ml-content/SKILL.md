---
name: ml-content
description: Generate publication-ready ML content — carousels, 3Blue1Brown-style explainer videos, infographics, posters, paper figures — with deep paper recon, real-3D-only design discipline, phone-readable annotations, exhaustive multi-pass internet research, AHA-first planning, mandatory iteration loops for pixel-perfection, and a full grounding pass before posting.
---

Generate publication-ready ML content. **Manim is the default video pipeline**; matplotlib is fallback when the environment can't run Manim or the user insists. When we can render ourselves, we render → critique → re-render until the result is pixel-perfect.

This skill compresses methodology developed across published ML carousels + videos + a full reverse-engineering of the github.com/3b1b/videos repo (Grant Sanderson's actual production code) and his explanation psychology. It treats ML content as applied research communication, not graphic design with science vocabulary on top.

---

## Workflow Decision Tree

```
User has...                              → Start at...
────────────────────────────────────────────────────────────
Topic / paper, no plan                   → Stage 0 (AHA) → full pipeline
A 5-file recon bundle                    → Stage 1 (Audit) → Build → Critique
A finished design-spec                   → Stage 3 (Build) → Critique
A finished video / carousel              → Stage 5 (Grounding pass)
Edits on a posted piece                  → Grounding pass + correction comment
```

Always ask what they have and what they need. Don't assume full pipeline.

---

## The Five Locks (non-negotiable)

Skip any one of these and the output devolves into AI slop.

**1. AHA lock** — every project starts with a pre-built AHA moment. The single shift-in-perspective the viewer will leave with. If you can't articulate it in one sentence, **do not start the project**. Grant: *"You shouldn't start the project unless there's one of those Aha moments and you have a big bag of Aha moments already that you could just pull at."*

**2. Grounding lock** — every claim verifiable against a primary source. Run the grounding pass (Stage 5) before posting. CONFIRMED / WRONG / UNVERIFIED per claim. **Date-drift catches** — for any recent ML release, re-verify within the week of publication (model versions and prices change weekly).

**3. Structural separation lock** — caption strip, chrome, and content live in **physically distinct pixel zones of the final frame**. NOT enforced by code discipline (it always breaks). Enforced by geometry: Manim renders into a smaller canvas, ffmpeg pads the remainder with a dedicated caption strip the camera cannot address. See "The Five-Layer Defense" below. Burned-in captions sharing a canvas with content WILL eventually collide — make it geometrically impossible.

**4. 3D lock** — real geometry only. No faux-3D parallelogram-on-rect. 3D is earned only when the math is genuinely a 3-axis quantity. Decide which scenes earn 3D before any rendering. Two-to-three hero 3D moments per video, max.

**5. Differentiation lock** — each piece earns its own visual fingerprint. Same brand baseline, different aesthetic per project. Reuse the same fingerprint twice = the audience sees a template.

---

## Stage 0 — AHA Discovery (Worldbuilder pass before anything)

Before writing a single recon file, answer these on paper:

### 0.1 — The AHA sentence

In one sentence, **what is the shift in perspective the viewer leaves with**?

Bad: *"DeepSeek V4 is cheap."*
Better: *"DeepSeek V4 is cheap because it stores the past at two different resolutions across the layers, and the model learns which resolution each layer needs."*

If the AHA is just a fact, not a shift, **stop**. Find the shift or pick a different paper.

### 0.2 — The crime scene (the hook)

What's the *concrete*, *weird*, *surprising* thing on screen at second 0?

Grant: *"In math especially, topic definitions should not be seen as a starting point, but an ending point."*

For ML content this means: open with the behavior the architecture explains, not the architecture. Open with the price gap, not the MoE diagram. Open with the cube of memory, not the formula.

### 0.3 — The audience model

Specific persona, not demographic. Worldbuilder discipline — see the writing layer below.

- What atomic units do they already nod at?
- What can break their head (in a good way)?
- What will they reflexively reject?

### 0.4 — The single leverage point

One sentence. The flawed premise to dismantle, or the new mental model to install.

If you can't write the leverage point in 25 words, you don't have one yet.

### 0.5 — The five rules from Grant himself (always apply)

1. **Never start without a pre-built AHA.** Project doesn't begin until you have it.
2. **Open with a crime scene, not a definition.** Mystery-novel framing. Concrete, weird, surprising.
3. **Intuition first; formalism as relief.** The equation arrives when the viewer already wants it.
4. **Every animation reinforces narration, never competes with it.** Cut anything that's motion-for-motion's-sake.
5. **Trust the niche. Trust the viewer.** Go deeper than feels safe. The audience reward is real.

These five are the worldbuilder lens for ML video content. Bake them into the recon bundle.

---

## Stage 1 — Recon (the 5-file bundle)

For each ML paper or topic, produce these five files in a project subfolder before any design begins. They are not interchangeable.

### File 1 — `paper-summary.md`

Audience: future-you reviewing what you actually understood.

Structure: title + arXiv ID + authors, NOTE on uncertainty (DIRECT / INFERRED / UNCERTAIN per claim), the thing being studied, problem framing (math verbatim where possible), method (Stage 1, Stage 2, theorem/guarantee), numbers that matter (headline / supporting / pragmatism), lineage (predecessors, foundational, adjacent), limitations from the paper's own limitations section, why this paper is interesting now, hook angles already in tension.

Length: 1500–3000 words.

### File 2 — `related-work.md`

Audience: a domain expert who wants to know how this paper sits in the field.

Structure: ASCII tree of lineage threads, predecessor table with one-sentence deltas, competitor table, adjacent context, what the paper contributes that wasn't already there (ranked), what it does NOT contribute and why that matters, counter-arguments worth pre-empting.

Length: 1500–2500 words.

### File 3 — `discussions.md`

Audience: someone calibrating the social-media reception.

Structure: macro-frame ("one-sentence consensus"), 3+ camps in the conversation (atomic units + predicted reaction), specific surfaces to cite or push against, prediction of which hook will the conversation latch onto, things NOT yet in the public conversation.

Length: 1000–2000 words.

### File 4 — `brainstorm.md`

Audience: future-you writing copy. This file decides everything that comes next.

Structure: worldbuilder audience pass, **the AHA sentence (locked from Stage 0)**, hook tier-list (10+ hooks across 5 tiers), final hook pick with reasoning, slide arc / scene arc / poster layout, caption draft (separate writing surface), what this content uniquely contributes vs prior content.

Length: 1500–2500 words.

### File 5 — `README.md`

Audience: future-you returning six months later, or a collaborator joining mid-project.

Structure: file index, recommended hook, top viral surfaces predicted, why this project matters in the series, status checklist, open uncertainties.

Length: 500–1000 words.

### Recon discipline

- **Always flag uncertainty.** "DIRECT", "INFERRED", "UNCERTAIN". Reusable for grounding pass.
- **Citation counts always approximate.** Scholar fluctuates. Never claim "348 citations" — say "widely cited."
- **Avoid generic adjectives.** "Innovative" / "groundbreaking" / "exciting" mean nothing.
- **Numbered + bulleted lists** beat prose in working docs.

### Exhaustive multi-pass internet recon (mandatory for recent papers)

For any paper or model from the last 6 months, do **two scrape passes**:

**Pass 1 — primary sources:** the paper PDF, the model card on HuggingFace, the authors' announcement post.

**Pass 2 — secondary verification:** at least two independent writeups from technical press (MarkTechPost, Sebastian Raschka's substack, Latent Space, AI Papers Academy, etc.), plus pricing/benchmark verification from at least two distinct hosting providers if applicable (HuggingFace, OpenRouter, DeepInfra, Together AI).

**Use BrightData (bd) tools when available** (`mcp__bd__scrape_as_markdown`, `mcp__bd__scrape_batch`, `mcp__bd__search_engine`). They bypass paywalls and rate-limits. Fall back to `mcp__workspace__web_fetch` and `WebSearch` only when bd is unavailable or returns insufficient content.

For technical claims that require code-level confirmation (specific values of hyperparameters, layer interleave ratios, etc.), fetch the actual technical-report PDF and grep. If a value isn't in any public source, **do not invent it** — the recon bundle flags it UNVERIFIED and the VO + visuals avoid quoting it.

---

## Stage 2 — Audit + Moodboard

### `3d-audit.md` — when 3D is earned

For every scene / panel, ask: *Does the math underneath have a third dimension that 3D would expose?*

Three verdicts: **YES — PRIME** (hero 3D moment, render it real), **PARTIAL — small inset** (data has 3 dims but the scene hero is something else), **NO** (flat data, don't 3D it).

Aim for 2-3 hero 3D moments per video. More and 3D loses its "look here" power.

| Math that wants 3D | Math that does NOT want 3D |
|---|---|
| `f(x, y) = z` surface | Time series → 2D line |
| 3D-axis cube (KV cache, embeddings) | Bar chart over one category |
| Volumetric tensor | Pipeline / flowchart |
| Two surfaces compared | Tree / dendrogram |
| Step / piecewise over 2D domain | Citation count comparison |
| Stacked translucent slabs | Benchmark leaderboard |

### `moodboard.md` — mining design references

Phases:
- **Phase 0** — locate the audience's visual world (Distill.pub, Anthropic Circuits, NVIDIA blog).
- **Phase 1** — survey 10–12 aesthetic ideologies, score on audience match + differentiation + phone-readability + 3D compatibility.
- **Phase 2** — mine 30+ references across 5–6 buckets (canonical, production analogs, contemporary writing, 3D/animation, foundational, adjacent). Each reference gets URL + one-sentence note on what to steal.
- **Phase 3** — synthesize 8–10 cross-cutting patterns.
- **Phase 4** — lock the direction in one paragraph.
- **Phase 5** — list 3–5 risks with mitigations.
- **Phase 6** — declare what to inherit and refuse from prior content.

---

## Stage 3 — Design Spec Lock

Write `design-spec.md` translating the locked direction into concrete tokens, type ramp, scene-by-scene layout. Lock before any code begins.

Standard structure: direction (one sentence), color tokens (CSS variables), typography stack, type ramp for 1920×1080, **safe-zone grid** (see below), chrome (top + bottom), per-scene spec, asset checklist, risks restated, greenlight criteria.

### The safe-zone grid (locked across all video output)

A 1920×1080 frame is divided into fixed reserved zones. **In-scene content lives only inside the content zone. Captions live only in the caption zone. Chrome lives only in the chrome zone.** Violating any of these zones is a pixel-perfect-lock failure.

```
y=0     ────────────────────────────────────────────────────────
        │                                                      │
y=80    │  ─── TOP CHROME ZONE ──── (chrome only) ───────────  │
        │                                                      │
y=120   │                                                      │
        │             SAFE CONTENT ZONE                        │
        │             (1920 × 700 working area)                │
        │                                                      │
y=820   │                                                      │
        │  ─── BOTTOM CHROME ZONE ─── (chrome only) ─────────  │
y=900   │                                                      │
        │      ─── CAPTION ZONE ─── (burned captions only) ─   │
y=1080  ────────────────────────────────────────────────────────
```

In numbers:
- Top chrome strip: y = 30 → 80 (paper title left, paper number right)
- Safe content zone: y = 120 → 820 (this is where everything happens)
- Bottom chrome strip: y = 1020 → 1070 (brand left, scene dots right)
- Caption zone: y = 920 → 1010 (burned subtitle, MarginV = 80)

The 100px buffer between content (y ≤ 820) and caption (y ≥ 920) is the **anti-collision buffer**. It is sacred.

---

## Stage 4 — Build

Two pipelines: **Manim (default)** and **matplotlib (fallback)**. Pick the right one for the environment.

### Pipeline selection

**Default = Manim Community Edition.** Use Manim when:
- The environment has Python 3.10+, FFmpeg, LaTeX (TeX Live or MacTeX), and Cairo+Pango.
- The user has not explicitly requested matplotlib.
- Math morphs, real 3D, equation transforms, or 3B1B-grammar idioms are required.

**Fallback = matplotlib.** Use matplotlib only when:
- The environment can't install Manim/LaTeX (sandboxed runner, restricted box).
- The user explicitly asks for matplotlib ("I don't want to install LaTeX," "use the matplotlib approach").
- Static carousel (10 PNGs for IG carousel), not video — matplotlib is actually the better tool here.

When Manim *could* be used but the user insists on matplotlib, **note this in the design-spec and ship matplotlib with the pixel-perfect iteration loop discipline below**.

### Manim pipeline (default — for video)

**Folder structure:**
```
project/
├── (full recon bundle)
├── 3d-audit.md
├── moodboard.md
├── design-spec.md
├── script.md                  # voice-over script + scene breakdown
├── audio/
│   └── vo.mp3                 # ElevenLabs render, -16 LUFS
├── manim/
│   ├── manim_scenes.py        # Scene subclasses, one per beat
│   ├── INSTALL.sh             # one-shot env setup
│   ├── RENDER.sh              # render all + concat + mux + caption burn
│   └── media/                 # Manim output (gitignore)
├── captions.ass               # libass, hand-authored + whisper timing
└── output/
    └── final.mp4              # deliverable
```

**Manim style guide (from Grant's own CLAUDE.md + observed grammar):**

- Use `Tex(r"…")` not `MathTex(...)` for inline math. Raw strings always for LaTeX.
- Substring color via `tex_to_color_map={"sym": COLOR}` (legacy) or substring indexing `equation["sym"][0].set_color(COLOR)` (modern).
- Per-character color assignments via zip: `for part, vect in zip([em, ew, ek, eq], word_vects): part.set_fill(vect.get_color())`.
- Construct `VGroup` declaratively: `VGroup(*[Mob() for _ in range(N)])`. Reserve `.add()` for cases with non-trivial side effects per iteration.
- Arrange via `.arrange(RIGHT, buff=...)`, `.next_to(...)`, `.to_corner(...)`, `.to_edge(...)`. Don't compute coordinates manually unless required.
- Color gradients via `color_gradient(colors, n)`, not hand-rolled `interpolate_color` loops.
- **Do not include indentation spaces on blank lines.**

**Manim animation grammar (extracted from 3b1b/videos repo across 4 iconic scene files):**

| Bedrock idiom | Frequency | Notes |
|---|---|---|
| `self.play(...) / self.wait()` cadence | 200+ plays + ~150 waits per file | The metronome. `self.wait()` default = 1s. |
| `run_time=2` as default animation length | Modal value across all files | Faster (`=1`, `=0.5`) for micro, slower (`=3-5`) for reveals, `=10-30` for meditative sweeps. |
| `LaggedStartMap(FadeIn, things, shift=0.5*DOWN/UP, lag_ratio=0.05–0.25)` | Heavy in all files | Standard ensemble entrance. |
| `ReplacementTransform(old, new)` / `TransformFromCopy(src, dest)` | Math morph workhorse | Grant does NOT use `TransformMatchingTex` in production. Explicit mobject-to-mobject. |
| Section comments as script structure | Every monolithic `construct()` | `# Show embeddings`, `# Move question`. Reads as a teleprompter outline. |
| Color minimalism + role consistency | ~5-8 colors per file, stable roles | YELLOW always = highlight/active; GREY_B = de-emphasis. |
| Math equation pieces coloured per substring | Universal | Letters colored to match the geometric object they describe. |
| Custom domain Mobject DSLs | One per video | `NumericEmbedding`, `Dial`, `WeightMatrix`, `ContextAnimation`. Tiny vocabulary per project. |
| No voiceover markers in code | Universal | VO recorded separately against section beats. |
| Aha moment staged with longer run_time + camera/layout shift + long wait afterward | Universal | Setup scenes are multi-anim plays at default; reveal scenes are one focused play at `run_time=5-10` then long wait. |

**Manim 2024 grammar (the modern style — use this):**
- `class S0X(InteractiveScene):` (not `Scene` / `ThreeDScene` — `InteractiveScene` is his 2024 base).
- Monolithic `construct()` with `# Section name` comments every 20-80 lines.
- `.animate.X(args).set_anim_args(run_time=N)` chains for in-place animation.
- 3D via `self.frame.animate.reorient(theta, phi, gamma, center, height)`. `run_time=5–12` for reorients.
- `self.frame.add_ambient_rotation(1 * DEGREES)` for subtle constant drift during long holds.
- `.always.set_perpendicular_to_camera(self.frame)` for labels that face the camera in 3D.
- Reusable factory functions: `get_*`, `make_*`, `show_*` — domain DSL per video.

### Audio sync — `manim-voiceover` with ElevenLabs (the auto-sync path)

The naive approach (render one big VO mp3, hand-time scenes to whisper alignment) drifts: any TTS pacing variance, any scene edit, and visuals desync silently. The right approach is per-line voiceover bound to each animation block:

```python
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.elevenlabs import ElevenLabsService

class S05_CSA(VoiceoverScene):
    def construct(self):
        self.set_speech_service(ElevenLabsService(
            voice_id="YOUR_VOICE_ID",
            model="eleven_multilingual_v2",
            voice_settings={...},
            transcription_model=None,    # skip whisper alignment (heavy)
        ))

        # build mobjects...

        with self.voiceover(text="Picture the attention matrix.") as t:
            self.play(FadeIn(matrix), run_time=t.duration)
        with self.voiceover(text="Compression collapses every m columns.") as t:
            self.play(ReplacementTransform(mat, comp_mat), run_time=t.duration)
```

`t.duration` is the actual generated audio length. Animation `run_time` is bound to it — visuals and voice stay in sync by construction. Each line cached to `media/voiceovers/` after first generation (zero API cost on subsequent runs).

### Gotchas observed in the field (every one of these cost ~30 min of debugging)

| Symptom | Real cause | Fix |
|---|---|---|
| `Error: No such option '--subcaptions'` | The CLI flag doesn't exist in Manim CE 0.19. Plugin auto-emits SRT when `create_subcaption=True` (default). | Just remove `--subcaptions` from your manim CLI. |
| `AuthorizationError` from ElevenLabs SDK | SDK env-var pickup is unreliable across versions. v0.x wants `ELEVEN_API_KEY`, v1.x wants `ELEVENLABS_API_KEY`. | Export both. Plus call `elevenlabs.set_api_key(...)` explicitly in Python before instantiating the service. |
| `APIError: missing voices_read permission` | `ElevenLabsService.__init__()` calls `voices()` to validate `voice_id`, requiring the `voices_read` scope. Many keys lack it. | Either regenerate the key with `voices_read`, OR monkey-patch `voices()` to return a stub list containing only your target `voice_id`. The actual TTS `generate()` call only needs `voice_id`. |
| `Missing packages. Run pip install manim-voiceover[transcribe]` then `openai-whisper` install fails on `pkg_resources` | `ElevenLabsService` defaults `transcription_model="base"` (overrides `SpeechService` default of `None`), triggering whisper extras. | Pass `transcription_model=None` to the service. No transcription needed if you don't use per-word bookmarks. |
| MRO error for 3D + Voiceover | Multiple inheritance order matters. | Try `class S(VoiceoverScene, ThreeDScene)` first; if it errors, swap to `(ThreeDScene, VoiceoverScene)`. |
| Captions never appear in final mp4 | `subtitles=...` filter needs the SRT path resolved correctly. | Use absolute path in the ffmpeg filter; set `fontsdir=` to your system font path so libass finds Inter Tight. |

### The interactive loop (when developing on your own machine)

Grant codes via the `manimgl <file> <Scene> -se <line>` interactive mode plus `checkpoint_paste()`. Sub-second iteration. If you're writing scenes on your local machine, install this workflow:

```bash
manimgl <file> <SceneName> -se <line>     # drop into IPython at a checkpoint
# in IPython, paste a block of animation code starting with a `# label` comment
checkpoint_paste()                          # runs the block; first sight of `# label` saves state
# edit code, re-paste — automatic rewind to the `# label` checkpoint
checkpoint_paste(skip=True)                 # zero-runtime scrub (no animation)
checkpoint_paste(record=True)               # writes the block to disk
```

When iterating, comments-as-checkpoints lets you treat the scene like a DAW timeline. Edit a paragraph, paste, watch, repeat.

**The render-critique-render loop (when we render ourselves):**

When the environment supports Manim and we're rendering, treat it as a discipline:

1. **Initial render** — `bash RENDER.sh all` (or render single scene with `manim -qm`).
2. **Critique pass** — sample 5–10 key frames via `ffmpeg -ss T -frames:v 1`. Read each frame. List every overlap, every margin-violation, every visual ambiguity.
3. **Patch** — edit the scene code to fix what's broken.
4. **Re-render only affected scenes** — Manim caches partial movie files, so only the changed `self.play(...)` re-renders.
5. **Re-critique.**
6. **Loop until critique returns clean.**

Acceptable number of critique-render cycles per video: **3–8**. Anything less and you've left bugs; anything more and you're over-engineering.

### Matplotlib pipeline (fallback — when user insists)

When Manim isn't available or the user wants matplotlib, follow the legacy carousel/video pipeline. Output: 1920×1080 PNGs per frame, stitched via FFmpeg, audio muxed in post.

**Folder structure:**
```
project/
├── (full recon bundle)
├── design-spec.md
├── render.py             # matplotlib + numpy + Pillow, hand-rolled scene functions
├── audio/vo.mp3
├── captions.ass
├── frames/               # per-frame PNGs (often 1000s of files)
├── output/final.mp4
└── critique/             # spot-check frame screenshots
```

#### The pixel-perfect matplotlib iteration loop (MANDATORY)

The matplotlib pipeline is more fragile than Manim because every element is hand-positioned. Without aggressive iteration discipline, scenes ship with caption-vs-element overlaps, off-screen text, misaligned chips. **This must not happen.**

For every scene in a matplotlib video:

**Phase 1 — Probe (after first writeup of render.py)**

Render one frame per scene at mid-scene timepoints via `--probe` mode:

```python
if args[0] == "--probe":
    for i, (name, s, e) in enumerate(SCENES):
        mid = (s + e) / 2
        render_frame(int(mid * FPS), out_dir="preview")
```

Read every preview frame with the Read tool. For each frame, walk this checklist:

- [ ] **Caption zone clear?** All in-scene text bottom-edges are at y ≤ 820. No element appears below y = 900 except chrome.
- [ ] **Chrome zone clear?** No content overlaps the top chrome strip (y ≤ 80) or bottom strip (y ≥ 1020).
- [ ] **Element-vs-element collisions?** Pills, text labels, math equations, panels — every bounding box is non-overlapping with every other.
- [ ] **Text fits inside containers?** Numbers inside chips, labels inside boxes, math inside panels — nothing spills out.
- [ ] **Color contract?** Every element uses the role-color from the design-spec. No surprise hues.
- [ ] **Margins consistent?** Same padding around similar elements across scenes.
- [ ] **Anti-collision buffer respected?** The 100px gap between content (y=820) and captions (y=920) is intact.

For every checkbox that fails, **note the exact fix needed** (move element, resize, change color, etc).

**Phase 2 — Patch**

Edit render.py per the critique list. Re-probe. Re-read frames. Iterate until all checkboxes pass.

Typical iteration count for a 9-scene video: **3–8 probe-patch cycles**.

**Phase 3 — Late-scene + early-scene check**

Probe at scene_t = 0.5s (just after fade-in) AND scene_t = scene_dur - 0.5s (just before fade-out) for every scene. These are the edge frames most likely to have:
- Elements still mid-animation overlapping
- Elements not yet faded in but blocking
- Elements that overshoot their dwell time

**Phase 4 — Full render**

Only when all probe frames pass: render all frames, mux audio, burn captions.

**Phase 5 — Post-mux spot check**

Sample 8–12 captioned timestamps from the final mp4 via `ffmpeg -ss T -frames:v 1`. Read each. Verify:

- Captions appear at the right time (anchor words land at the right scene)
- Captions don't overlap in-scene hero text
- Captions don't overrun the bottom of the frame

If any frame fails, return to Phase 1.

**Don't ship until critique returns clean.** This is non-negotiable.

#### Matplotlib pacing discipline

The 3b1b "metronome" — `self.play(...)` + `self.wait()` — has a direct matplotlib analog:

- **Animate** an element over a defined duration (e.g., `fadein(t, dur=0.5, delay=delay)`).
- **Hold** after the animation completes — at least 0.3s of no change before the next element appears.
- **Default animation duration:** ~0.4-0.6s. **Default hold:** 0.5-1.0s.
- **Reveal animation duration:** 0.8-1.5s. **Reveal hold:** 1.5-3.0s.

Pacing too tight = "AI slop frenetic." Pacing too loose = "viewer scrolls away." 0.5s animate + 0.6s hold is the safe default.

#### Matplotlib pixel measurement helpers

For text width estimation (since `text.get_window_extent()` requires a rendered figure), use these conservative rules:

```python
# Inter Tight at weight 600
char_w_inter_bold  = fontsize * 0.62
# Inter Tight at weight 400
char_w_inter_book  = fontsize * 0.55
# JetBrains Mono
char_w_mono        = fontsize * 0.60
# CMU Serif italic
char_w_cmu_italic  = fontsize * 0.50

def text_width(text, fontsize, font="inter_bold"):
    cw = {"inter_bold": 0.62, "inter_book": 0.55,
          "mono": 0.60, "cmu_italic": 0.50}[font]
    return len(text) * fontsize * cw
```

For pills and rounded boxes around text, use a 24px horizontal pad + 20% vertical pad:

```python
pill_w = text_width(label, fontsize) + 48
pill_h = fontsize * 1.95
```

These are the values that survived 5+ iteration cycles. Don't shrink them.

---

## Stage 5 — Grounding Pass

Mandatory before shipping. The audit takes 30 minutes; correcting after posting takes a week.

### What counts as a claim

Anything one of your readers could check on Google:
- Paper titles, author names, affiliations
- arXiv IDs
- Citation counts (always soften — never quote hard numbers)
- Performance numbers (accuracies, F1, speedups, percentages)
- Conference venues (ICML 2024, NeurIPS 2025, ICLR 2026)
- Release / announcement dates
- Lab names
- Model identifiers (DeepSeek-V4-Pro, Claude Opus 4.8, GPT-5.5)
- Specific quotes
- Specific (layer, expert) coordinates in mech interp
- Specific table cells in benchmark results
- Statements like "first paper to do X"

### Date-drift watch (heightened priority for recent releases)

Model versions, benchmark scores, and prices change weekly in 2026+. If your content references any of these:

- **Re-verify within 48 hours of publishing**, not at recon time.
- **Anchor every comparison to a specific version**: "Claude Opus 4.6" not "Claude Opus". When 4.8 ships, the un-anchored claim becomes wrong overnight.
- **Note the snapshot date on screen** for pricing visuals.
- **Run a subagent grounding pass** the morning of publication, not the morning of recording.

### How to grade specifics

Decimal precision past what the source provides reads fabricated. If the abstract says ">91%", you write ">91%" — not "92.3%".

### Workflow

1. **Extract** every claim from script + visuals + captions + IG copy into a table.
2. **Search** each via WebSearch / bd / web_fetch.
3. **Grade** CONFIRMED / WRONG / UNVERIFIED + URL.
4. **Fix** WRONG. **Soften** UNVERIFIED.
5. **Re-render** any scenes touched.

For 10+ claims, delegate to a subagent:

```
FULL GROUNDING AUDIT — [project name].

Read [script.md path] and [ig-caption.md path]. Extract every checkable
factual claim into a table. Web-search each. Verdict: CONFIRMED /
UNVERIFIED / WRONG. For WRONG, supply current text → correction → URL.
For UNVERIFIED, supply what you searched and why ambiguous.

Anchor truths:
- Today's date is [DATE]
- arXiv ID format YYMM.NNNNN
- For ML releases from past 6 months: re-verify against the model card
  AND a second independent technical writeup AND current pricing on
  at least two providers.

Report format:
- CONFIRMED CLAIMS (one bullet each, with URL)
- WRONG CLAIMS (current text → correction → URL)
- UNVERIFIED (claim, what you searched)
- SUMMARY: how many CONFIRMED / WRONG / UNVERIFIED + ship/no-ship rec
- RECOMMENDED EDITS: literal text changes

Hard limit: 1500 words.
```

---

## The Five-Layer Defense for Pixel-Perfect Animated Video

Five iterations of "fix the overlaps" eventually proved that absolute-coordinate placement + burned-in captions on the same canvas is a structural failure mode, not a discipline failure mode. The Five-Layer Defense fixes this at five compounding levels — each catches what the layer below missed.

### Why this exists (the failure pattern in plain English)

We kept shipping videos where:
- Captions overlapped in-scene text (caption fonts spill above their reserved zone)
- Top chrome ("PAPER · 01") overlapped scene titles
- Hero numbers collided with stat strips
- Arrows arrived at the same time as labels and stacked on each other

Every time, the diagnosis was "I set the y coordinate wrong" and the fix was "I'll move it by 0.3 units." Then the next render exposed a different overlap and we repeated. This isn't a personal failure — it's the predictable result of:

1. **Hand-placed absolute coordinates drift** when font metrics, text length, or canvas dims change.
2. **Burned-in captions share the canvas with content**, so the caption renderer (libass) and the scene renderer (Manim) both write into the same pixel rows. The system has no way to coordinate.

The fix: stop trying to coordinate. Make collision geometrically impossible.

### Layer 1 — Zone reservation (the structural fix)

**Reserve the bottom band of the frame for captions. Place no in-scene mobjects there. Enforce by code, asserts, and post-render validator.**

There are two valid implementations of this:

**Strategy A (geometric, attempted in passes 4-5):** render Manim at a smaller canvas (e.g. 1920×940), ffmpeg-pad the remainder with bg color, captions burn into the pad. The advantage is "the camera physically cannot address the caption zone." The disadvantage: Manim's quality presets (`-qh`, `-qm`, `-qk`) and various other CLI/config plumbing keep overriding the smaller `config.pixel_height`. We spent two passes fighting this and never got it to land reliably. **Don't recommend.**

**Strategy B (code-enforced zones, what we ship):** render at native 1920×1080. Reserve y_pixel bands by convention, enforce with `assert_inside_safe()` at render time and `validate_frames.py` at post-render time. Simpler, fewer moving parts, no ffmpeg pad gymnastics.

For 1920×1080 final output (Strategy B), the proven zoning is:

```
y_pixel:  0    80                                     905    980   1020      1080
          ├────┼─────────────────────────────────────┼──────┼─────┼──────────┤
          │TOP │              CONTENT                │BOTTOM│ BUF │ CAPTION  │
          │CHR │              ZONE                   │CHROME│ FER │  STRIP   │
          └────┴─────────────────────────────────────┴──────┴─────┴──────────┘
          ↑ Manim renders here, native 1920×1080                  ↑
          to_corner UL/UR buff=0.30                          libass MarginV=20

           Bottom-chrome zone (905-980): brand mark + scene dots,
           to_corner DL/DR buff=1.0 → y_manim -3.0 → y_pixel 945
           BUFFER zone (980-1019): MUST stay bg color — validator enforces
           Caption strip (1020-1080): libass burns text here, 30-px tall
```

Manim config:
```python
config.pixel_width  = 1920
config.pixel_height = 1080
config.frame_height = 8.0          # Manim default; 1 unit = 135 px
config.frame_rate   = 30

CONTENT_FLOOR = -2.7              # in-scene y must be > this; matches y_pixel 905
CONTENT_CEIL  =  3.4              # in-scene y must be < this; matches y_pixel 81
```

Caption burned with libass, no ffmpeg pad needed:
```bash
ffmpeg -i scenes_concat.mp4 \
    -vf "subtitles=cap.srt:force_style='Alignment=2,MarginV=20,FontSize=22,FontName=Inter Tight,Bold=1,PrimaryColour=&H00ECECEC&'" \
    -c:v libx264 ...
```

The 40-pixel **buffer zone** at y_pixel 980-1019 is the heart of the validator. Nothing in Manim should reach it (chrome ends at y_pixel ~960, content stops at y_pixel ~900). Captions can't reach it (caption text top is at y_pixel ~1030 with MarginV=20). If the validator detects any non-bg pixel in this band, **something drifted** — either a Manim mobject extended too far down OR the caption renderer pushed text above the band. Either way, fix it.

**Why this works:** SMPTE ST 2046-1 (Safe Title Area), EBU R 95 (graphics safe area), and the BBC subtitle guidelines all reserve outer pixel bands for captions/chrome. The BBC docs explicitly recommend "captions in any black bars present within the video." This is the broadcast standard, not a workaround.

### Layer 2 — Constraint-based positioning (prevents drift)

In Manim, **forbid absolute `.move_to([x, y, z])`**. Allowed primitives:

- `.next_to(other, direction, buff=...)`
- `.align_to(other, direction)`
- `.to_corner(EDGE, buff=...)` (only for chrome — never content)
- `.to_edge(EDGE, buff=...)` (only for chrome)
- `VGroup(*things).arrange(direction, buff=...)`
- `VGroup(*things).arrange_in_grid(rows, cols, buff=...)`
- `SurroundingRectangle(target, buff=...)`

Jérôme Eertmans codified the rule in *How I write long Manim presentations*: *"prefer positioning your objects relative to each other... you never know the final position of each object in the canvas, because you can always add or remove slides in between."*

For complex multi-region scenes, wrap a `kiwisolver`-based mini layout engine (Cassowary constraints — the same algorithm behind iOS AutoLayout, already a matplotlib dep). Or use [`poga`](https://github.com/dzhsurf/poga) — Python bindings for Facebook's Yoga (the Flexbox engine behind React Native). Motion Canvas (Manim's JS spiritual successor) adopted Flexbox for the same reason.

In matplotlib, the analog is `.set_position()` only via `axes_grid1` toolkit / `constrained_layout` — never via `bbox_to_anchor` raw coords.

### Layer 3 — Programmatic bbox guard (`layout_guards.py`)

At the end of each scene's `construct()`, walk the bounding-box matrix and assert no two non-whitelisted mobjects intersect with less than the required gap:

```python
from layout_guards import assert_no_overlap, assert_inside_safe

class MyScene(Scene):
    def construct(self):
        ...
        # before the final wait, validate the layout
        visible = [title, math_eq, hero_number, strip]
        assert_inside_safe(*visible)
        assert_no_overlap(*visible, min_gap=gap_units(12))   # 12-px gap
```

Helper:
```python
def assert_no_overlap(*mobs, min_gap=0.1, allow=None):
    for a in mobs:
        for b in mobs[i+1:]:
            if (id(a), id(b)) in allow_set: continue
            # check bbox intersection with min_gap buffer
            ...

def assert_inside_safe(*mobs, top=2.85, bottom=-2.85, left=-7.0, right=7.0):
    # check every mob's bbox is inside the safe content area
```

Soft mode: `LAYOUT_GUARDS_SOFT=1` makes the helpers print warnings instead of raising. Use it on the first pass, then turn it off.

### Layer 4 — Visual frame validator (`validate_frames.py`)

After the final mp4 is built, sample N frames and check that the buffer zone is uniform background color.

**DO NOT use MSER text detection** — it produces tens of thousands of false-positive "overlaps" because it detects each character at multiple scales as separate regions. We tried this in pass 4; the output was unusable.

**DO use color-variance per zone:**
```python
buf_zone = img[940:959, :, :]                # the hard buffer
diff = np.abs(buf_zone - bg_color).sum(axis=2)
assert diff.std() < 4.0,  "buffer not uniform"
assert diff.mean() < 6.0, "buffer is not bg color"
```

If the buffer std > 4 → something rendered there (impossible if Layer 1 is correct, so this is a smoke alarm). Exit 1.

For text-vs-text overlap detection (within the content zone), the right tool is a **vision-language model** (Claude Vision, GPT-4V): sample 4 frames into a 2×2 grid, ask "are any text regions overlapping?" Costs cents per validation. Vastly more accurate than any classical CV approach.

### Layer 5 — Cheap iteration loop (`preview.sh`)

3b1b iterates via `manimgl`'s live OpenGL preview + Sublime `checkpoint_paste()` — sub-second feedback. We can't have that in an async workflow, but we can get close: `manim -ql -s --format=png` renders only the LAST frame of a scene as a PNG in ~10 seconds, no audio cost, no video encode.

```bash
# preview.sh
manim -ql -s --format=png manim_scenes.py "$SCENE"
cp media/images/.../scene.png preview/$SCENE_last.png
echo "preview ready: preview/$SCENE_last.png"
```

Use this for layout iteration: change a coord, run `bash preview.sh S05_CSA`, open the PNG, adjust, repeat. ElevenLabs voiceover cache means zero API cost on iteration.

### Practical run order with all 5 layers

```bash
# 1) iterate layout on one scene (Layer 5 — fast)
bash preview.sh S05_CSA       # look at preview/S05_CSA_last.png

# 2) full build (Layers 1+3 kick in automatically)
NOCACHE=1 bash RENDER.sh all  # outputs ../output/final.mp4

# 3) validate (Layer 4)
python3 validate_frames.py ../output/final.mp4
# any HARD failure (buffer zone violated) → Layer 1 broke
# any soft failure → text-on-text or font metric surprise → use VLM check

# 4) first pass with soft assertions:
LAYOUT_GUARDS_SOFT=1 NOCACHE=1 bash RENDER.sh all
# get warnings, then turn soft off
```

### Failure modes specifically caught by each layer

| Failure | Caught by | Mechanism |
|---|---|---|
| Caption overlaps in-scene element | Layer 1 (structural) | Caption physically can't reach content rows |
| Element at y=-3.0 in Manim coords (chrome zone) | Layer 3 (`assert_inside_safe`) | Bbox check fires |
| Two text labels arrive simultaneously and stack | Layer 3 (`assert_no_overlap`) | Pairwise IoU check |
| ffmpeg pad accidentally not applied | Layer 4 (color-variance) | Buffer zone has content → buffer std spikes |
| Font fallback to Arial (different metrics → drift) | Layer 5 (preview) | Visible immediately |
| Subtle text-on-text within content zone | Layer 4 with `--vlm` | VLM catches what CV misses |

### Don't skip layers

Each layer is cheap. Layer 1 is one ffmpeg flag change. Layer 3 is a 50-line helper module. Layer 5 is a 30-line shell script. Layer 4 is 100 lines of Python. The cost of NOT having them is the cost of every overlap bug shipped. We learned this the hard way across 5 iteration passes.

---

## Brand Baseline (locked across all ml-content output)

Differentiation happens *within* this baseline, not by changing it.

### Canvas

```css
--bg:        #0E1014   /* slate near-black */
--surface:   #14171F   /* raised panels (sparingly) */
--grid:      #1A1F2B   /* hairline borders + dot grid */
--hairline:  #2A2F3A   /* subtle dividers */
```

Always dark canvas. ml-content does not use light themes.

### Text grays

```css
--text:      #ECECEC
--body:      #A8AEB8
--mute:      #5A6175
```

### Manim canonical color palette (locked, from Manim CE)

```css
--blue:    #58C4DD
--red:     #FC6255
--yellow:  #F7D96F
--green:   #83C167
--teal:    #5CD0B3
--purple:  #9A72AC
--orange:  #FF862F
--gold:    #F0AC5F
```

### Color role assignment (sacred — never violate)

- **Orange** — hero / "look here" / the project-specific innovation
- **Yellow** — single-use transition / aha pulse / one moment per video
- **Blue** — data flowing / process / iteration
- **Green** — correct / parity / converged answer
- **Red** — error / wrong / caveat
- **Purple** — secondary structure / supporting role
- **Mute grey** — de-emphasis / chrome

### Typography stack (locked)

```css
--math:      'CMU Serif', 'EB Garamond', serif
--body-font: 'Inter Tight', 'Inter', -apple-system, sans-serif
--mono:      'JetBrains Mono', 'IBM Plex Mono', monospace
```

Three weights only: 400 (body), 500 (eyebrows / mono), 600 (display / bold).

### Type ramp for 1920×1080

| Element | Family | Weight | Size |
|---|---|---|---|
| Display hero | Inter Tight | 600 | 96–110 |
| Section headline | Inter Tight | 600 | 56–72 |
| Math equation (hero) | CMU Serif italic | — | 44–72 |
| Math equation (inline) | CMU Serif italic | — | 24–32 |
| Sub / caption | Inter Tight | 400 | 22–28 |
| Body | Inter Tight | 400 | 18–24 |
| Eyebrow / chrome | JetBrains Mono | 500 | 17–22 (uppercase, letter-spacing 0.22em) |
| Hero number | Inter Tight | 600 | 180–240 |
| Mono labels | JetBrains Mono | 500 | 14–18 |

### Chrome (locked per video)

Top-left mono mute: paper-title strip with arXiv-style ID.
Top-right mono orange: paper number ("PAPER · 01") or episode number.
Bottom-left mono mute: brand handle (@thtskaran).
Bottom-right: N-dot scene indicator (current = orange, others = mute).

Chrome stays static through every frame. Only the dot indicator changes per scene.

---

## Hook Construction (Worldbuilder Discipline)

Writing layer for ml-content. Treats writing as applied psychology, not self-expression.

### Three things to model before writing

**1. Audience persona** — list 1–3 personas. For each: atomic units they nod at, what can break their head, what they reflexively reject.

**2. Leverage point** — the one specific thing that, said aloud, makes the audience pause. Always concrete + numeric + slightly weird.

Examples that worked:
- *"DeepSeek built two readers of the past. One reads carefully. One skims. Together they read a million tokens at one tenth of the memory."*
- *"There's a single neuron in OLMoE-1B-7B that fires only on closing LaTeX brackets. F1 = 1.00."*

**3. Reaction map** — predict who reacts how (researchers / practitioners / skeptics). Optimize for two of three.

### The four hook principles (locked)

1. **Lead with the most specific weird artifact in the paper.** Generality is for the body.
2. **Pair the concrete with one number that makes you do a double-take.** F1 = 1.00. +12.8%. 4.7×.
3. **Pre-empt "so what?" with one sub-line that hints at the broader claim.** Hook can be specific; sub has to imply scope.
4. **Avoid dunking even when the temptation is highest.** Frame as "the unit shifted," not "your tools are obsolete."

### Hook tier list

- **Tier 1** — would over-perform. Picks up multiple atomic units, breaks one prior, lands the most specific weird artifact.
- **Tier 2** — strong but conventional.
- **Tier 3** — strong stat openers. Headline number alone.
- **Tier 4** — different register (alignment, safety, infra ops).
- **Tier 5** — pocket / provocations / caption.

### Copy hygiene

- **No em dashes.** Use periods or commas. Em dashes feel AI-coded.
- **No "genuinely", "honestly", "straightforward".** Filler.
- **Vary sentence length.** Short. Then a longer one that builds in. Then short.
- **Match clause shape to claim shape.** "Two stages. One Lagrangian. One XGBoost." reads like the method.
- **Don't invent facts.** If unsure, soften ("≈", "reportedly", "see Table 1") or ask.
- **Use specific names, not generic categories.** "OLMoE-1B-7B" not "an MoE model."
- **Mono for IDs.** `OLMoE-L15-E17`, `arXiv 2604.14853` set in JetBrains Mono.
- **Spell out shorthand in VO.** "key-value cache" not "KV cache" when spoken (TTS). "Compressed Sparse Attention" not "CSA" when spoken. Acronyms read aloud are jarring; full names land.
- **Acronyms get spaces in TTS script** so the TTS reads letter-by-letter: "M L P" not "MLP" (the latter slurs as "mlp").
- **Numbers spelled out in VO** for cadence: "eighty seven cents" not "$0.87".

### Caption structure

```
[Hook from Tier 1 or 1C]

[3–4 lines of body — atomic units → reframe → number → action item]

[Optional: provocation or open question]

[Citation: paper title · authors · arXiv ID]

[Hashtags — 5 max]
```

Total: 80–120 words. Captions over 200 words don't get read on IG.

---

## Annotation Language (phone-readable)

Locked spec for any annotation drawn on a 3D chart, 2D chart, diagram, or video frame.

### Locked rules

1. **Typeface:** Inter Tight 600 (or DejaVu Sans 600 fallback).
2. **Font size:** 22–32pt at rendering DPI. Scale up for 4K (60+).
3. **Background:** rounded pill — rectangle filled with role color.
4. **Text color:** `BG` (dark canvas) — high contrast on the pill.
5. **Arrow:** lw 2.4, `arrowstyle="-|>"`, `connectionstyle="arc3,rad=0.12"`.
6. **Maximum:** 3 annotations per chart.

### Color = role

| Role | Color |
|---|---|
| Method / project's contribution | ORANGE |
| Hero highlight | ORANGE (saturated) |
| Process / iteration | BLUE |
| Correct / parity | GREEN |
| Wrong / caveat | RED |
| Single-use transition | YELLOW |
| Diminishing / secondary | PURPLE |
| De-emphasis / chrome | MUTE GREY |

Don't introduce new colors for new annotations.

### Standard pill placements

For matplotlib (axes-fraction coordinates):

| Position | (fx, fy) |
|---|---|
| Top-left | (0.18, 0.84) |
| Top-center | (0.50, 0.92) |
| Top-right | (0.82, 0.84) |
| Bottom-left | (0.18, 0.20) |
| Bottom-right | (0.82, 0.20) |

If 3 pills, prefer corners. If 1 pill, prefer top-center.

### Common annotation mistakes

1. **Pill too small** — fontsize=12 is invisible at IG resolution. Always 22+.
2. **Pill text too long** — 7 words max.
3. **Arrow too thin** — lw=1 disappears. Always 2.4.
4. **Arrow color ≠ pill color** — visual disunity.
5. **More than 3 pills** — clutter.
6. **In-3D-plane text via `ax.text(x, y, z, ...)` for titles** — gets projected with perspective. Use HTML / fixed-in-frame overlay for titles.
7. **Pill text not centered** — break left/right alignment if not deliberate.
8. **Pill collides with axis labels** — leave 60px buffer.

---

## Composition with other skills

| Need | Use alongside |
|---|---|
| Paper PDF as final deliverable | `academic-paper` instead |
| Persuasive caption | `worldbuilder-writing` for caption, ml-content for visuals |
| More design references | `pro-graphic-designer` discipline, constrained by ml-content brand |
| Fact-check at scale | `autonomous-research` agent |
| Find the right paper | `autonomous-research` |
| Native pptx slide deck | `pptx` instead — ml-content does video/PNG only |

---

## Project folder convention

```
NN-short-slug/
├── paper-summary.md
├── related-work.md
├── discussions.md
├── brainstorm.md
├── README.md
├── 3d-audit.md
├── moodboard.md
├── design-spec.md
├── script.md
├── audio/
│   ├── vo_script.txt
│   ├── vo.mp3
│   └── vo_alignment.json
├── captions.ass
├── build_captions.py
├── ig-caption.md
├── output/
│   └── final.mp4
└── (one of:)
├── manim/                 # if Manim pipeline (default)
│   ├── manim_scenes.py
│   ├── INSTALL.sh
│   ├── RENDER.sh
│   └── media/
└── render.py + frames/    # if matplotlib pipeline (fallback)
```

Naming: `01-deepseek-v4`, `02-asynctls-sparse-attention`, etc.

---

## Quick start for a new video

```
1. Pick paper. Note arXiv ID.
2. Stage 0: write the AHA sentence on paper. If you can't, defer.
3. Create project folder.
4. Stage 1: write the 5-file recon bundle. Two-pass internet recon.
5. Stage 2: write 3d-audit.md and moodboard.md.
6. Stage 3: lock design-spec.md (including safe-zone grid).
7. Choose pipeline:
   - Manim (default): write manim_scenes.py + INSTALL.sh + RENDER.sh.
   - Matplotlib (fallback): write render.py.
8. Render audio via ElevenLabs. Align with whisper.
9. Stage 4 build:
   - Manim: render-critique-render loop (3–8 cycles).
   - Matplotlib: pixel-perfect probe-patch loop (3–8 cycles).
10. Caption: build_captions.py against whisper alignment.
11. Stage 5: grounding pass (subagent for 10+ claims).
12. Write IG caption. Mux final. Ship.
```

---

## Quick start for a new carousel (static PNGs for IG)

(Carousels are static, not animated; matplotlib is the right tool regardless.)

```
1. Stages 0-3 as above.
2. carousel.html using the brand baseline.
3. render_3d.py for any earned 3D PNGs.
4. render_carousel.py via weasyprint + pdftoppm.
5. Stage 5 grounding pass.
6. Write caption. Post.
```

---

## Appendix A — Bedrock Manim grammar idioms (cheat sheet)

Copy-paste blocks from real 3b1b/videos code (extracted across `attention.py`, `nn/part1.py`, `fourier.py`, `embedding.py`).

### Ensemble entrance
```python
self.play(LaggedStartMap(
    FadeIn, things, shift=0.5 * UP, lag_ratio=0.25,
))
```

### Math morph (his actual idiom — NOT TransformMatchingTex)
```python
new_eq = Tex(R"\text{cost} = L \times \tfrac{L}{m}")
new_eq.move_to(old_eq)
self.play(ReplacementTransform(old_eq, new_eq), run_time=1.5)
self.wait()
```

### Substring rectangle (highlight one variable in an equation)
```python
equation = Tex(R"\text{Attention}(Q, K, V) = \text{softmax}\left({K^T Q \over \sqrt{d_k}}\right) V")
q_rect = SurroundingRectangle(equation["Q"][0], color=YELLOW)
self.play(ShowCreation(q_rect))
```

### 3D camera reorient (2024 modern grammar)
```python
self.frame.animate.reorient(
    -179, 19, 179,         # theta, phi, gamma
    (2.49, 1.96, 0.4),     # center
    4.76,                  # height
).set_anim_args(run_time=5)
```

### Ambient drift (for long contemplative beats)
```python
self.frame.add_ambient_rotation(1 * DEGREES)
self.wait(15)  # the drift makes the wait feel alive
```

### Slot-machine number counter
```python
val = ValueTracker(100.0)
num = always_redraw(
    lambda: Text(f"{int(val.get_value())}%",
                 font="Inter Tight", weight="BOLD",
                 color=ORANGE, font_size=200).move_to(target)
)
self.add(num)
self.play(val.animate.set_value(10.0), run_time=0.6,
          rate_func=rate_functions.ease_out_cubic)
```

### The "aha" reveal staging
```python
# setup is multiple small plays...
self.play(FadeIn(setup_a)); self.wait(0.3)
self.play(FadeIn(setup_b)); self.wait(0.3)
self.play(FadeIn(setup_c)); self.wait(0.3)

# ...the aha is one focused play at longer run_time + camera shift, then LONG wait
self.play(
    ReplacementTransform(setup_b, payoff),
    self.frame.animate.reorient(-110, 10, 110, payoff.get_center(), 6.72),
    run_time=10,
)
self.wait(3.0)  # let the viewer breathe
```

### Curved highlight rays (custom ContextAnimation pattern, from `_2024/transformers/helpers.py`)
```python
self.play(ContextAnimation(
    target_word, source_words,
    strengths=[1, 1],
    path_arc=150 * DEGREES,
))
```

### Per-character color via zip (visually link math to geometry)
```python
for part, vect in zip([em, ew, ek, eq], [man_vec, woman_vec, king_vec, queen_vec]):
    part.set_fill(vect.get_color())
```

### Two-color paired concepts
```python
colors = [YELLOW, TEAL]              # Q, K, V style
# or
colors = [BLUE_B, RED_B]             # male/female style
# or
colors = [BLUE_C, BLUE_D, GREEN]     # gradient strength
```

### Section-comment teleprompter
```python
def construct(self):
    # Setup the network
    ...
    self.play(...); self.wait()

    # Show the input
    ...
    self.play(...); self.wait()

    # The reveal — explain why
    ...
    self.play(..., run_time=8); self.wait(3)
```

### Pi creature (still valid for explainer videos in 2024+)
```python
randy = Randolph().to_corner(DOWN + LEFT)
self.play(randy.change("pondering", target_mob))
self.play(randy.says("Wait, why does this work?", mode="confused"))
self.play(randy.debubble(mode="hooray"))
```

---

## Appendix B — Pacing reference (Grant's actual numbers)

From counting `self.play(...)` and `self.wait()` calls across 4 iconic scene files (attention.py 4093 LOC, nn/part1.py 4664 LOC, fourier.py 4309 LOC, embedding.py 3047 LOC):

| Metric | Median | Note |
|---|---|---|
| `self.play()` per file | ~220 | A 20-minute video has ~220 distinct beats |
| `self.wait()` per file | ~140 | About one wait per 1.5 plays |
| Default `wait()` (bare) | 60-70% of all waits | The 1-second metronome |
| `wait(2)` | 20-30% | Beat after a reveal |
| `wait(5)` | rare, reserved | After a 3D reorient |
| `wait(10)` to `wait(20)` | very rare, reserved | After the AHA |
| `run_time=2` | modal animation length | Default heartbeat |
| `run_time=5-10` | reserved | For the AHA scene |
| `run_time=15-30` | very rare | Meditative sweeps (Fourier winding, 3D camera arcs) |

For a 2-minute Instagram explainer: scale these down. Target **~40 plays, ~25 waits**. The reveal scene still gets `run_time=5-10` even at IG scale.

---

## Appendix C — The five 3b1b psychology rules (copy these into every brainstorm.md)

1. **Never start without a pre-built AHA.** Project doesn't begin until you have it.
2. **Open with a crime scene, not a definition.** Mystery-novel framing. Concrete, weird, surprising.
3. **Intuition first; formalism as relief.** The equation arrives when the viewer already wants it.
4. **Every animation reinforces narration, never competes with it.** Cut anything that's motion-for-motion's-sake.
5. **Trust the niche. Trust the viewer.** Go deeper than feels safe.

These five rules are the worldbuilder lens for ML video content. Bake them into the recon bundle.

---

## Appendix D — Failure modes observed in practice (and how to catch them)

| Failure | Cause | Fix |
|---|---|---|
| Caption overlaps in-scene text | Tried to coordinate caption position via code discipline alone | **Layer 1 structural separation.** Manim renders smaller (e.g. 1920×940), ffmpeg pads bottom strip for captions. Camera can't reach the strip. |
| Chrome ("PAPER · 01") overlaps content title | Chrome too tall + content too high; coordinate-based gap drift | Tighten chrome to fontsize ≤18pt; `to_corner(buff>=0.4)`; `assert_inside_safe()` with `top<=2.85` in 940-tall frame |
| Hero number cut off at edge / spills out of chip | Hardcoded text width didn't match rendered metrics | Use `.next_to()` + `.arrange()` instead of `.move_to([x,y,z])`. Build pills/chips via `SurroundingRectangle(text, buff=...)` so the box sizes to content, not vice-versa. |
| Element overflows panel in matplotlib | Conservative `char_w` constants drift across fonts | Pad +48px on pill width; use the `text_width()` helper, always add +24px horizontal margin |
| Two text labels arrive at same time and stack | Used `self.play(FadeIn(a), FadeIn(b))` instead of staggering | Use `LaggedStart(FadeIn(a), FadeIn(b), lag_ratio=0.5)`. Grant uses `LaggedStartMap` 74× in `attention.py` alone. |
| Caption fires at wrong time (anchor mismatch) | Caption anchor word has multiple occurrences | Use occurrence index (e.g. `"holds"` 2 not 1). With manim-voiceover, the issue disappears — each VO line owns its own SRT timing. |
| Pacing too fast ("AI slop frenetic") | Animation `run_time < 0.4s`, holds `< 0.3s` | Lengthen animations to 0.5-0.6s, holds to 0.5-1.0s. Grant's metronome is `self.wait()` (1.0s default) after every play. |
| Date-drifted claim | Compared to model version now superseded | Anchor every model claim to a specific version. Re-verify within 48hrs of publish. |
| Acronym mispronounced by TTS | Used `"CSA"` instead of `"C S A"` or full name | Spell out acronyms in TTS script. Spaces force letter reading. Better: write `"Compressed Sparse Attention"` in full and let captions use the acronym. |
| Manim font fallback to Arial | Pango couldn't find Inter Tight | Install fonts system-wide (`~/.local/share/fonts/` on Linux, `~/Library/Fonts/` on Mac). Run `fc-cache -fv`. |
| Render time too long | Re-rendering everything when only one scene changed | Use Manim's partial movie file cache. Only re-render affected scenes via `manim --disable_caching ... S0X`. |
| MSER text detector reports 57k overlaps | MSER detects the same character at multiple scales as separate "regions" | **DO NOT use MSER for layout validation.** Use color-variance per zone (Layer 4 in the Five-Layer Defense) or a vision-LM. |
| ElevenLabs `AuthorizationError` | SDK env-var pickup is unreliable | Set both `ELEVEN_API_KEY` and `ELEVENLABS_API_KEY`. Call `elevenlabs.set_api_key(...)` explicitly in Python. |
| ElevenLabs `missing voices_read permission` | Plugin's `__init__` calls `voices()` to validate `voice_id` | Either regenerate key with `voices_read`, or monkey-patch `voices()` to return a stub list containing only your `voice_id`. |
| `pip install manim-voiceover[transcribe]` fails on `openai-whisper` | `pkg_resources` missing | `pip install --upgrade setuptools wheel` first. Better: pass `transcription_model=None` to ElevenLabsService — skips the whole transcription path. |
| `Error: No such option '--subcaptions'` from manim CLI | Plugin auto-emits SRT when `create_subcaption=True` (default). No flag. | Just don't pass `--subcaptions`. |
| **Validator's HARD buffer-zone failures on every frame even though `config.pixel_height=940` is set in Python** | **Manim's quality presets (`-ql`, `-qm`, `-qh`, `-qk`) OVERRIDE Python config for resolution + fps.** With `-qh`, scene mp4s render at 1920×1080@60fps no matter what your `config.pixel_height` says. Output dir name `media/videos/manim_scenes/1080p60/` proves it. ffmpeg pad then becomes a no-op and captions burn over content. | Use `-r WIDTH,HEIGHT --fps N` explicitly. The `-r` flag wins over quality presets. Strip all `-q*` flags from render commands. |
| ffmpeg pad puts content in wrong location | `pad=W:H:X:Y` means "input video positioned at (X,Y) in the new canvas" | `pad=1920:1080:0:0` puts content at top-left, pad at bottom. To put content at bottom and pad at top, use `pad=1920:1080:0:140`. |
| Caption fontsize too small at 4K | Caption FontSize in ASS doesn't auto-scale with PlayResY | Set `PlayResX` and `PlayResY` in the ASS header to match the final mp4. Or use libass `force_style` and pre-compute pt size = `desired_px * 72 / 96`. |

Add to this table after every project. Failure modes compound; named failures don't.

---

## Appendix E — Lessons from programmatic-video tools (Remotion / Motion Canvas / Konva)

We did the layout work for ml-content using Manim's hand-coordinate placement and kept hitting overlaps. Research into how other programmatic-video tools (Remotion, Motion Canvas, Konva, Vizrt) solve the same problem produced five borrowable patterns. Apply them when authoring new content.

### Pattern 1 — `AbsoluteFill` zoning + safe-zone constants

Remotion ships `<AbsoluteFill>` — a `<div>` that's `position:absolute; inset:0; flex column`. Every scene is built by stacking AbsoluteFills, intentionally overlapping by DOM order.

The **community standard for 9:16 Reels/TikTok safe zones** that emerged on Remotion (from the `neversight/remotion-ads` skill spec):

> "All text within safe zones (80px+ from edges) — No critical content in top 285px — No critical content in bottom 400px — Text minimum 40px font size — Logo visible in center 1080×1080 (grid thumbnail)."

For Manim/ml-content's 16:9 frames the analogous safe constants are: chrome bands at top 80px + bottom 175px, content in y_pixel 80-905, caption strip 1020-1080. These numbers are LOCKED — do not improvise.

### Pattern 2 — Measure text BEFORE you render it (Remotion's `fitText`)

Remotion has `@remotion/layout-utils`: `fitText`, `fitTextOnNLines`, `measureText`, `fillTextBox`. They exist because **CSS layout can't size text correctly if the font isn't loaded** — silent overflow happens otherwise. Their best-practices doc warns:

- **`validateFontIsLoaded: true`** — if measurement uses the fallback font, throw.
- Match every font property between measurement and render (family, size, weight, letterSpacing, fontVariantNumeric, textTransform).
- Avoid `padding`/`border` on measured text — use `outline` instead so `box-sizing` doesn't shrink the container.

For Manim/matplotlib, the analog is: before placing a `Text(...)`, compute its `.width` and verify it fits inside the panel. If not, shrink the font (binary search) or break the text. Helpers added to `layout_guards.py` should include a `fit_text(text, max_width, font_size_cap)` that does this.

### Pattern 3 — Opt-in layout root + cardinal anchors (Motion Canvas)

Motion Canvas's killer move: a `<Rect>` is a normal node UNTIL you add `layout`. Then Flexbox controls children's sizes and positions:

```jsx
<Rect layout direction="column" gap={40} padding={60} width={1920}>
  <Txt fontSize={72}>Title</Txt>
  <Circle width={320} height={320} />
</Rect>
```

Every node exposes **reactive cardinal-direction signals**: `top()`, `bottom()`, `left()`, `right()`, `topLeft()` ... that are *live* — when the target moves, dependent positions update automatically. Compare:

```jsx
// Motion Canvas — reactive, follows the rect through rotation
<Rect ref={small} size={50} right={big().left} />

// Manim — one-shot snapshot, breaks if `big` moves later
small.next_to(big, LEFT)
```

The borrow: when authoring a Manim scene, **declare relationships once at construct time, even if Manim won't reactively update them**. Then if you need to move `big` later in the same scene, also call `small.next_to(big, LEFT)` again. Don't hardcode `small.move_to([x, y, 0])` — that decouples them.

### Pattern 4 — AABB collision check (Konva)

Konva's collision-detection sandbox is 4 lines of axis-aligned bbox intersection:

```js
function haveIntersection(r1, r2) {
  return !( r2.x > r1.x + r1.width  || r2.x + r2.width  < r1.x ||
            r2.y > r1.y + r1.height || r2.y + r2.height < r1.y );
}
```

This is exactly what our `layout_guards.assert_no_overlap()` does. We've had it since pass 4; the lesson is **call it at end of every `construct()`**, not just optionally. Make it a render-time guard, not a comment.

### Pattern 5 — Templates + named field substitution (Vizrt broadcast CG)

Vizrt Template Builder treats every lower-third / overlay as a "scene with named field IDs." Operators fill text fields; the scene's pre-designed layout reflows around them. **Overlap is impossible** because the scene designer pre-placed every variant.

The Manim equivalent: when you have 10 chip-style boxes (e.g. the price chips in our payoff scene), write a single `chip_row(items)` factory function with explicit `arrange(RIGHT, buff=0.4)` plus a stroke-color parameter per item. Don't hand-position each chip with `move_to([cx, cy, 0])`. The factory is the template; the items list is the fields.

### Synthesis: when to use which

| Pattern | When to use | Effort |
|---|---|---|
| 1 — Safe-zone constants | Always. Lock the y_pixel band reservation at project start. | ~5 lines of constants |
| 2 — Measure before render | Any text that depends on dynamic data (model names, numbers) | ~50 lines for `fit_text()` helper |
| 3 — Cardinal anchors | Any scene with 3+ elements that depend on each other's positions | Refactor: `.next_to()` everywhere instead of `.move_to(...)` |
| 4 — AABB collision check | Every scene, end of every `construct()`. Use `LAYOUT_GUARDS_SOFT=1` first | Already in `layout_guards.py` |
| 5 — Template factories | Repeating element groups (chips, icons, ranks) | One factory function per pattern |

**What we deliberately do NOT borrow:**
- A full Cassowary/kiwisolver constraint engine. No programmatic video tool has shipped one successfully; Motion Canvas's reactive signals get 90% of the value at 10% of the complexity. Reactive bindings > linear constraints.
- HTML/CSS-as-source (Remotion, Helios). Manim's `MathTex` and 3D primitives have no clean web analog. The migration cost would dwarf the layout benefit.

### Sources

- Remotion AbsoluteFill: https://www.remotion.dev/docs/absolute-fill
- Remotion layout-utils best practices: https://www.remotion.dev/docs/layout-utils/best-practices
- Remotion fitText: https://www.remotion.dev/docs/layout-utils/fit-text
- Motion Canvas layouts: https://github.com/motion-canvas/motion-canvas/blob/main/packages/docs/docs/getting-started/layouts.mdx
- Motion Canvas positioning: https://github.com/motion-canvas/motion-canvas/blob/main/packages/docs/docs/getting-started/positioning.mdx
- Konva collision: https://konvajs.org/docs/sandbox/Collision_Detection.html
- Vizrt Template Builder: https://documentation.vizrt.com/template-builder-guide-3.5.pdf
- Manim → Motion Canvas migration: https://slama.dev/motion-canvas/introduction/
- Community safe zones: https://lobehub.com/skills/neversight-skills_feed-remotion-ads

---

## Appendix F — The brainstorm that produced the Five-Layer Defense

When this skill kept producing layouts with overlaps despite the "Pixel-perfect lock" rule, the diagnosis was: code discipline alone CANNOT enforce non-overlap. The failure modes are:

1. **Drift.** Fonts render at slightly different metrics across Cairo / Pango / freetype versions. Text length depends on data. Coordinates set in dev don't match prod.
2. **Coordination.** Captions are rendered by libass (a separate compositor). Content is rendered by Manim/matplotlib. Neither knows about the other's bounding boxes.
3. **Compounding errors.** Each manual coordinate is a 95%-likely-to-work guess. Stack 50 of them per scene, 10 scenes per video — joint probability is ~7%.

A brainstorm + research pass (reading Manim docs, broadcast standards, Motion Canvas source, kiwisolver examples, 3b1b's actual workflow from interviews) surfaced the five-layer pattern. The summary:

- **Layer 1: geometric separation.** Use what TV broadcast figured out in the 1970s. Caption strips live in pixel rows the renderer doesn't address.
- **Layer 2: relative positioning.** Motion Canvas uses Flexbox. iOS uses AutoLayout. Both compute positions from constraints — never hand-place.
- **Layer 3: runtime asserts.** Fail loudly in code when bboxes collide. Cheaper than fixing it after the render.
- **Layer 4: visual checks.** Sample frames, run a vision check (color variance, VLM). Catches what 1-3 missed.
- **Layer 5: cheap iteration.** Sub-second feedback loop turns layout discipline from a chore into a game. Grant's `checkpoint_paste()` is this. `manim -ql -s` is the poor-man's version.

The biggest unlock was Layer 1: realizing that captions overlapping content is a SOLVED PROBLEM (broadcast TV figured it out, SMPTE/EBU standardized it, BBC's subtitle guide tells you to use black bars), and we were re-creating the bug by burning captions on top of content. Once that one structural change is in, the remaining layers catch the rare edge cases.

Cost-effectiveness: Layer 1 is ~5 lines of ffmpeg + Manim config. Layer 3 is ~50 lines. Layer 5 is ~30 lines. Together they prevent the most common failure shipping has ever produced.
