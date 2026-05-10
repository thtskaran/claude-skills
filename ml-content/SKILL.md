---
name: ml-content
description: Use for ML content creation — Instagram carousels, 3Blue1Brown-style explainer videos, infographics, posters, paper figures, blog headers, or any visual or written deliverable explaining an ML paper or concept to a public audience. Trigger on "make a carousel about [paper]", "explain [concept] in 3B1B style", "video on [ML topic]", "infographic for [paper]", "research thumbnail", "ML one-pager", "viral post about [paper]", "Instagram post on [arXiv ID]", "newsletter graphic", "design for my AI startup", or any variant where the deliverable is ML content for a public audience. Combines deep paper recon (5-file bundle), worldbuilder hook construction, real-3D-only design discipline, phone-readable annotations, full grounding pass, and a locked render pipeline (weasyprint+pdftoppm for static, matplotlib3D for charts, Manim for videos). Prefer this over pro-graphic-designer or worldbuilder-writing alone when the topic is specifically an ML paper, model, or research result.
---

# ml-content Skill

Generate publication-ready ML content — carousels, 3Blue1Brown-style explainer videos, infographics, posters, paper figures — with deep paper recon, real-3D-only design discipline, phone-readable annotations, and a full grounding pass before posting.

This skill compresses methodology developed across six published ML carousels. It treats ML content as applied research communication, not graphic design with science vocabulary on top.

---

## Workflow Decision Tree

```
User has...                      → Start at...
────────────────────────────────────────────────────
A paper / topic only             → Stage 1 (Recon) → full pipeline
A finished recon bundle          → Stage 2 (Audit) → Build → Ground
A finished design-spec           → Stage 4 (Build)
A finished carousel/video        → Stage 5 (Grounding pass)
Edits on a posted piece          → Grounding-pass + correction comment
```

Always ask what they have and what they need. Don't assume full pipeline.

---

## The Four Locks (non-negotiable)

Skip any one of these and the output devolves into AI slop.

**1. Grounding lock** — every claim verifiable against a primary source. Run the grounding pass (Stage 5) before posting. CONFIRMED / WRONG / UNVERIFIED per claim.

**2. 3D lock** — real geometry only. No faux-3D parallelogram-on-rect. 3D is earned only when the math is genuinely a 3-axis quantity. Decide which slides earn 3D before any rendering.

**3. Phone-readable lock** — annotations work at 50% phone zoom. Inter Tight 600 24–32pt bold pills, lw 2.4 arrows, max 3 per chart.

**4. Differentiation lock** — each piece earns its own visual fingerprint. Same brand baseline, different aesthetic per project. Reuse the same fingerprint twice = the audience sees a template.

---

## Stage 1: Recon (the 5-file bundle)

For each ML paper or topic, produce these five files in a project subfolder before any design begins. They are not interchangeable — each solves a specific problem.

### File 1 — `paper-summary.md`

Audience: future-you reviewing what you actually understood about the paper.

Structure:
- Title + arXiv ID + authors with affiliations
- NOTE on uncertainty — flag every claim DIRECT (from abstract/extraction), INFERRED (from prior knowledge), or UNCERTAIN (needs verification)
- Section 1: The thing being studied
- Section 2: Problem framing (math / setup / objective, verbatim where possible)
- Section 3: Method (Stage 1, Stage 2, theorem/guarantee)
- Section 4: Numbers that matter (headline / supporting / pragmatism)
- Section 5: Lineage — closest predecessors (3-5), foundational (2-3), adjacent (2-3)
- Section 6: Limitations from the paper's own limitations section
- Section 7: Why this paper is interesting now (3 reasons in order of strength)
- Section 8: Hook angles already in tension (3-5 ranked)

Length: 1500–3000 words.

### File 2 — `related-work.md`

Audience: a domain expert who wants to know how this paper sits in the field.

Structure:
- ASCII tree showing the lineage threads
- Thread 1: foundational papers, one-sentence delta each
- Thread 2: direct competitors with comparison table
- Thread 3: adjacent / practical / commercial context
- "What Paper #N contributes that wasn't already there" — 3 things ranked by strength
- "What it does NOT contribute and why that matters"
- "Counter-arguments worth pre-empting"

Length: 1500–2500 words.

### File 3 — `discussions.md`

Audience: someone calibrating the social-media reception.

Structure:
- The macro frame: "[one-sentence consensus]"
- 3+ camps in the conversation, each with: who they are, atomic units, predicted reaction
- Specific surfaces to cite or push against
- Prediction: which hook will the conversation latch onto
- Things NOT yet in the public conversation that this content can introduce

Length: 1000–2000 words.

### File 4 — `brainstorm.md`

Audience: future-you writing copy. This file decides everything that comes next.

Structure:
- Worldbuilder pass — audience personas with atomic units they nod at + what can break their head
- Hook tier list (5 tiers, 10+ hooks total)
- Final recommendation — which hook for slide 1, which for caption
- Slide arc / scene arc / poster layout (10 slides typical)
- Caption draft (separate writing surface — can be sharper than carousel)
- "What this content uniquely contributes vs prior content"

Length: 1500–2500 words.

### File 5 — `README.md`

Audience: future-you returning to this project six months later, or a collaborator joining mid-project.

Structure:
- Index of files in the folder
- Recommended hook (from brainstorm.md Tier 1) with reasoning
- Top viral surfaces predicted (in order of likelihood)
- "Why this project matters in the series" — comparison table
- Status checklist
- Open uncertainties to resolve before posting

Length: 500–1000 words.

### Discipline notes for the recon stage

- **Always flag uncertainty.** "DIRECT", "INFERRED", "UNCERTAIN". This is what makes the bundle re-usable for grounding.
- **Citation counts always approximate.** Scholar fluctuates. Never claim "348 citations" — say "widely cited" or "Tier 1 cited" or "~hundreds."
- **Avoid generic adjectives.** "Innovative" / "groundbreaking" / "exciting" mean nothing. Replace with specific shape.
- **Numbered + bulleted lists** work better than prose paragraphs in working documents.

---

## Stage 2: Audit + Moodboard

Two files before any code:

### `3d-audit.md` — when 3D is earned

For every slide / scene / panel, ask:

> Does the math underneath have a third dimension that 3D would expose, or am I forcing depth onto something flat?

Three verdicts:
- **YES — PRIME** — hero 3D moment. Render it real.
- **PARTIAL — small inset** — data has 3 dimensions but the slide hero is something else. 3D goes in a corner.
- **NO** — flat data. Don't 3D it.

Aim for **two hero 3D moments per carousel** (≈10 slides). More than that and 3D loses its "look here" power.

**Math that wants 3D:**

| Math shape | 3D primitive | Example |
|---|---|---|
| `f(x, y) = z` surface | `plot_surface` | accuracy(x_difficulty, b_budget) |
| Discrete bars across 2D grid | `bar3d` | model × benchmark gain |
| Volumetric structure | `Poly3DCollection` cuboids | KV cache cube split into PCIe / GPU / CPU |
| Two surfaces compared | two `plot_surface` calls | dense vs MoE polysemanticity gap |
| Step / piecewise function | `plot_surface` with discrete colormap | Lagrangian b*(x; λ) step-pyramid |
| Stacked translucent slabs | `Poly3DCollection` | two-tier serving stack |

**Math that does NOT want 3D:**

- Time series (use 2D line plot)
- Bar chart over single category axis (use 2D bars)
- Pipeline / flowchart (use 2D box-and-arrow)
- Tree structure (use 2D dendrogram)
- Citation count comparison (use 2D bars)
- Benchmark leaderboard (use 2D table)
- Confusion matrix (use 2D heatmap)

If you reach for 3D on any of these, reconsider.

### `moodboard.md` — mining design references

Six phases:

**Phase 0 — locate the audience's visual world.** Name the audience and their visual literacy. Examples:
- Mech interp researchers → Distill.pub, Transformer Circuits, SAE feature dashboards
- Long-context infra → NVIDIA tech blog, vLLM benchmarks, FlashAttention figures, 3B1B
- Reasoning + inference operators → Boyd & Vandenberghe, Bertsekas, OpenAI usage console, Datadog APM

**Phase 1 — survey 10–12 aesthetic ideologies.** Score on audience match, differentiation, phone-readability, 3D compatibility. Pick top 2-3 and synthesize one direction: *"[A] × [B] × [C], rendered for a phone."*

**Phase 2 — mine 30+ references** across 5–6 buckets:
- A: canonical reference for the audience
- B: production analogs
- C: contemporary writing in the register
- D: 3D / animation references
- E: foundational / textbook visual idiom
- F: adjacent / texture

Each reference: URL + one-sentence note on what to steal.

**Phase 3 — synthesize cross-cutting patterns** (8–10 patterns observed across multiple buckets).

**Phase 4 — lock the direction** in one paragraph naming canvas, primary accent, secondary accent, type stack, chrome, hero idiom.

**Phase 5 — list 3–5 risks** with mitigations.

**Phase 6 — declare what to inherit and refuse from prior content** in the series.

---

## Stage 3: Design Spec Lock

Write `design-spec.md` translating the locked direction into concrete CSS tokens, type ramp, slide-by-slide layout. Lock before HTML/Manim work begins.

Standard structure:
- Direction (one sentence)
- Color tokens (CSS variables)
- Typography stack
- Type ramp for 1080×1350
- Layout system (frame, margins, grid)
- Slide chrome (top + bottom)
- Slide-by-slide spec (one block per slide)
- Asset checklist (PNG renders to produce before HTML lock)
- Risks restated
- Greenlight criteria

---

## Stage 4: Build

Pick deliverable type and use the matching template.

### Carousel pipeline

Output: 1080×1350 PNGs, one per slide. Build via HTML → weasyprint → PDF → pdftoppm.

Folder structure:
```
project/
├── carousel.html          # source — all slides as <section class="slide">
├── 3d/                    # rendered 3D PNGs (built first)
└── slides/                # final output PNGs
```

**Step 1** — write `carousel.html` using `scripts/carousel_template.html` as skeleton. Keep ALL slides in one HTML file as separate `<section class="slide" id="sN">` blocks. Embed 3D images as `<img src="3d/foo.png">` from local paths.

The HTML loads:
- CMU Serif from dreampulse CDN
- Inter Tight + JetBrains Mono from Google Fonts
- All CSS inline in `<style>` blocks (no external CSS)

**Step 2** — render 3D PNGs first via `scripts/render_3d.py`.

**Step 3** — render the carousel via `scripts/render_carousel.py`. Accepts `start end` args:
```bash
python render_carousel.py        # all slides
python render_carousel.py 5 5    # just slide 5
python render_carousel.py 1 3    # slides 1-3
```

**Step 4** — sanity check. Read every slide's PNG visually before posting. Phone-readable check at 50% zoom.

**Common slide types** (vocabulary, not template):
1. **Hook** — typography moment, no visual. Big headline + small sub + citation strip.
2. **Premise / why now** — timeline + supporting visual or 2-section split.
3. **The waste / problem** — 3D landscape if data has shape.
4. **The framing / abstraction** — math hero with one sentence underneath.
5. **The mechanism** — Stage 1 / Stage 2. 3D step-pyramid or pipeline diagram.
6. **The supporting math** — classifier diagram, trees, pipeline.
7. **The guarantee** — theorem statement + plain English explanation.
8. **The numbers** — hero number + 3D bar chart + per-cell legend.
9. **The taxonomy / examples** — card grid of 4 archetype examples.
10. **The composition / vision** — schematic + closing line.

### Video pipeline (3B1B-style explainers via Manim)

Use when math has *motion* (gradient descent, attention sliding, sampling, iteration), or concept reveals over time, or audience is YouTube/Reels rather than IG static.

Don't force motion onto stationary content (regret bound, comparison table, cost frontier) — carousel beats video there.

**Tooling:**
- **Manim Community Edition** — `pip install manim`. NOT 3Blue1Brown's private fork.
- **Renderer** — Cairo (default) for 2D, OpenGL for performance.
- **LaTeX** — required for math rendering. `MathTex(r"\frac{1}{2}")` produces real LaTeX.
- **FFmpeg** — Manim shells out for video assembly.

**Folder structure:**
```
project/
├── (full recon bundle)
├── 3d-audit.md            # which scenes earn 3D
├── moodboard.md
├── design-spec.md
├── script.md              # voice-over script + scene breakdown
├── manim_scenes.py        # Scene subclasses (template: scripts/manim_scene.py)
└── output/
    └── final.mp4
```

**Step 1** — write `script.md` with voice-over per scene. Don't animate against silence. Length: 30–60s for Reels, 4–10 minutes for YouTube. Scenes 5–15 seconds each.

**Step 2** — design scene arc (same shape as carousel, adapted for time):
1. Hook (10–15s)
2. Premise (20–30s)
3. The waste / problem (30–45s)
4. The framing (20–30s)
5. The mechanism (45–60s)
6. The supporting math (30–45s)
7. The guarantee (20–30s)
8. The numbers (30–45s)
9. The taxonomy / examples (45s)
10. The composition / vision (15–20s)

**Step 3** — copy `scripts/manim_scene.py` and edit per scene.

**Step 4** — render: `manim -qh manim_scenes.py SceneName`.

**Step 5** — narrate (ElevenLabs API or human VO with `add_voiceover` plugin).

**Step 6** — assemble via FFmpeg.

**3B1B idioms to steal:**
1. Mountains-of-mesh for high-D landscapes — `Surface(...).set_style(stroke_width=0.5)` gives the mesh-overlay look.
2. Camera pull-back to reveal new context.
3. Equation transformations via `TransformMatchingTex`.
4. Highlighting via `Indicate` (yellow pulse).
5. Animated arrows that draw themselves — `Create(Arrow(...))` not `FadeIn`.
6. Slow zoom-in on a punchline number.

### Poster / infographic pipeline

Use cases: A0/A1 conference posters, A4 one-pagers, blog OG images (1200×630), YouTube thumbnails (1280×720), Twitter cards (1200×675), newsletter graphics.

Same stack as carousel — adjust `@page` size in `render_carousel.py`:

```python
# A4 portrait (210 × 297 mm = 595 × 842 pt at 72dpi)
PAGE_CSS = '<style>@page { size: 595px 842px; margin: 0; } ... </style>'

# A0 landscape (1189 × 841 mm = 3370 × 2384 pt at 72dpi)
PAGE_CSS = '<style>@page { size: 3370px 2384px; margin: 0; } ... </style>'

# Twitter card (1200 × 675 px)
PAGE_CSS = '<style>@page { size: 1200px 675px; margin: 0; } ... </style>'
```

For A0 print, use vector PDF (not raster). Embed fonts. Test print at A4 first.

**Poster archetypes:**

*Conference one-pager (A4)* — Title + Problem + Method + Results + arXiv ID, single page, ~600 words + 2-3 figures.

*Conference wall poster (A0)* — Multi-zone, 3 columns, ~1500 words + 5-8 figures.

*Blog OG / Twitter card* — Hook + supporting visual + signature, 1200×630 landscape.

*YouTube thumbnail* — One BIG number or 3D geometry, dark canvas, single accent, no author face.

---

## Stage 5: Grounding Pass

Mandatory before shipping. The audit takes 30 minutes; correcting after posting takes a week.

### What counts as a claim

Anything one of your readers could check on Google:
- Paper titles, author names, affiliations
- arXiv IDs
- Citation counts
- Performance numbers (accuracies, F1, speedups, percentages)
- Conference venues (ICML 2024, NeurIPS 2025, ICLR 2026)
- Release / announcement dates
- Lab names
- Model identifiers (DeepSeek-R1, Claude Opus 4.5, GPT-5)
- Specific quotes
- Specific (layer, expert) coordinates in mech interp
- Specific table cells in benchmark results
- Statements like "first paper to do X"

### What does NOT need verification (but flag as illustrative)

- Educational metaphors ("TTC is a knapsack")
- Sample example questions
- Editorial commentary
- Predictions about future work

### How to grade specifics

Decimal precision past what the paper provides reads fabricated:

| Source says | OK to write | NOT OK |
|---|---|---|
| ">91%" (abstract) | ">91%" or "≈91%" | "92.3%" |
| "+12.8% on MATH" | "+12.8% on MATH" | per-cell decimals invented |
| "twelve models tested" | "twelve models" | listing all 12 unless paper does |
| "linear regret bound" | "linear in classifier error" | "regret = 0.34 × error" |

### How to grade citations

Citation counts age instantly. Either:
- Skip them entirely (best)
- Soften qualitatively ("widely cited", "Tier 1 cited")
- Pin a specific date ("~3215 cites at time of pull, Q1 2026")

Never quote a hard number like "348 citations".

### Workflow

1. **Extract** — list every claim from the carousel/script in a table.
2. **Search** — for each, run a focused web search. Read the abstract. Check arXiv ID matches. Check authors match.
3. **Grade** — CONFIRMED / WRONG / UNVERIFIED. Note the source URL.
4. **Fix** — for WRONG, correct. For UNVERIFIED, soften.
5. **Re-render** — if any fixes touched a slide, re-run the render pipeline.

For 10+ claims, delegate to a subagent:

```
FULL GROUNDING AUDIT — [project name].

Read [carousel.html path] and verify EVERY factual claim against the public web.

1. Extract every checkable claim — paper titles, authors, arXiv IDs, citation counts, venues, performance numbers, dates, model names, quotes.
2. Web-search each.
3. Verdict: CONFIRMED / UNVERIFIED / WRONG.

Anchor truths:
- Today's date is [DATE]
- arXiv ID format YYMM.NNNNN

Report format:
- CONFIRMED CLAIMS (one bullet each, with URL)
- WRONG CLAIMS (current text → correction → URL)
- UNVERIFIED (claim, what you searched)
- SUMMARY

Hard limit: 1500 words.
```

### Sample errors caught in past projects (use as test cases)

| Project | Wrong claim | Actual | Lesson |
|---|---|---|---|
| Carousel #6 | "DeepSeek R1 — Jan 2026" | Jan 20, 2025 | Date drift forward. Pin to actual release. |
| Carousel #6 | "OpenAI o3 — Dec 2025" | Announced Dec 20, 2024 | Same drift. |
| Carousel #5 | "RUC + WTM" affiliation | Hamburg only (no RUC) | Don't invent affiliations. |
| Carousel #5 | "L14 E59 D&D F1=0.82" | Not in paper body, only "high" | Don't invent decimals. |
| Carousel #4 | Operator speedup "1.7×–10.0×" | Paper abstract says "1.2×–10.0×" | Read the abstract carefully. |
| Carousel #2 | "DeepSeek-R1-70B" | "DeepSeek-R1-Distill-Llama-70B" | Don't shorten model names. |
| Carousel #2 | "348 citations" on Cemri | Counts vary; never citable | Skip hard citation counts. |
| Carousel #1 | "Hacks transfer to HumanEval" | Test domain is Countdown-Code | Read the paper, not just the title. |

### After-posting corrections

If the grounding pass catches errors after publication:

1. **Don't delete-and-repost.** Signals desperation.
2. **Comment under your own post** with the correction.
3. **Roll into next caption.** Turns it into a credibility moment.
4. **Update the project's README** to log the error.

---

## Brand Baseline (locked across all ml-content output)

Differentiation happens *within* this baseline (palette, accent, register), not by changing the baseline.

### Canvas

```css
--bg:        #0E1014   /* slate near-black, page background */
--surface:   #14171F   /* slightly raised panels (sparingly) */
--grid:      #1A1F2B   /* hairline borders + faint dot grid */
--hairline:  #2A2F3A   /* subtle dividers */
```

Always dark canvas. ml-content does not use light themes.

### Text grays

```css
--text:      #ECECEC
--body:      #A8AEB8
--mute:      #5A6175
```

### Manim canonical color palette (locked)

The exact 3Blue1Brown / Manim hex values:

```css
--blue:    #58C4DD
--red:     #FC6255
--yellow:  #F7D96F
--green:   #83C167
--teal:    #5CD0B3
--purple:  #9A72AC
--orange:  #FF862F
--gold:    #F0AC5F
--amber:   #F0AC5F   /* alias for gold */
```

### Color role assignment (conventions)

- **Primary** — paper's main contribution / the answer
- **Highlight (orange)** — hero number / "look here" moment
- **Blue** — process / convergence / iteration
- **Green** — success / saturated / Easy archetype
- **Red** — uniform baseline / waste / Hard archetype
- **Yellow** — key transition / Responsive zone
- **Purple** — diminishing returns / mid-range archetype

### Typography stack (locked)

```css
--math:      'Computer Modern', 'EB Garamond', 'CMU Serif', serif
--body-font: 'Inter Tight', 'Inter', -apple-system, sans-serif
--mono:      'JetBrains Mono', 'IBM Plex Mono', monospace
```

CMU Serif via dreampulse CDN. Inter Tight + JetBrains Mono via Google Fonts. Three weights only: 400 (body), 500 (eyebrows), 600 (display).

### Type ramp for 1080×1350

| Element | Family | Weight | Size |
|---|---|---|---|
| Display hero | Inter Tight | 600 | 76–96 |
| Section headline | Inter Tight | 600 | 56–68 |
| Math equation (large) | CMU Serif italic | 400 | 48–96 |
| Math equation (inline) | CMU Serif italic | 400 | 22–28 |
| Sub / caption | Inter Tight | 400 | 22 |
| Body | Inter Tight | 400 | 18 |
| Eyebrow | JetBrains Mono | 500 | 12 (letter-spacing 0.22em uppercase) |
| Hero number | Inter Tight | 600 | 180–240 |
| Mono labels | JetBrains Mono | 500 | 13–14 |

### Layout

- Frame: 1080 × 1350
- Outer margin: 80px (left/right), 56px (top/bottom)
- Working canvas: 920 × 1238

### Chrome (every slide)

Top: LEFT mono 11px `[Paper Title] · [arXiv ID] · [Date]`, RIGHT mono 12px `[CHAPTER TAG] / Chapter NN` in primary color.

Bottom: LEFT mono 12px `→ @thtskaran · OBVIX LABS`, RIGHT N dots (current = primary, others = mute).

Standard chapter tags:

| Topic | Tag |
|---|---|
| RLVR / verifier hacking | `LAB NOTE` |
| Multi-agent | `BENCH ROOM` |
| KV cache / quant | `BITS & BANDWIDTH` |
| Sparse attention | `BITS & BANDWIDTH` |
| Mech interp | `INTERP LAB` |
| Optimization / serving | `RUNBOOK` |

---

## Hook Construction (Worldbuilder Discipline)

Writing layer for ml-content. Treats writing as applied psychology, not self-expression.

### Three things to model before writing

**1. Audience persona** — list 1–3 personas. For each: atomic units they nod at, what can break their head, what they reflexively reject.

**2. Leverage point** — the one specific thing that, said aloud, makes the audience pause. Always concrete + numeric + slightly weird.

Examples that worked:
- "Add 200 lines of XGBoost before your reasoning calls. Get +12.8% accuracy at the same average cost."
- "There's a single neuron in OLMoE-1B-7B that fires only on closing LaTeX brackets. F1 = 1.00."

**3. Reaction map** — predict who reacts how (researchers / practitioners / skeptics). Optimize for two of three.

### The four hook construction principles (locked)

1. **Lead with the most specific weird artifact in the paper.** Generality is for the body.
   ❌ "MoE models are interpretable"
   ✅ "There's an entire expert dedicated to D&D rules"

2. **Pair the concrete with one number that makes you do a double-take.** F1 = 1.00. +12.8%. 4.7×.

3. **Pre-empt "so what?" with one sub-line that hints at the broader claim.** Hook can be specific; sub has to imply scope.

4. **Avoid dunking even when the temptation is highest.** Frame as "the unit shifted," not "your tools are obsolete."

### Hook tier list

- **Tier 1** — would over-perform. Picks up multiple atomic units, breaks one prior, lands the most specific weird artifact.
- **Tier 2** — strong but conventional. Solid backup if Tier 1 feels too risky.
- **Tier 3** — strong stat openers. Headline number alone.
- **Tier 4** — for a different audience register (alignment, safety, infra ops).
- **Tier 5** — keep in pocket. Provocations / reframes / arch claims for caption.

### Hook → caption decoupling

Hook is for slide 1. Caption is a separate writing surface — can be sharper because text-only and read after the visual stops the swipe.

Standard pattern: lead with Tier 1 hook on slide 1, deploy Tier 1C (provocation) in caption.

### Copy hygiene

- **No em dashes.** Use periods or commas. Em dashes feel AI-coded.
- **No "genuinely", "honestly", "straightforward".** Filler.
- **Vary sentence length.** Short. Then a longer one that builds in. Then short.
- **Match clause shape to claim shape.** "Two stages. One Lagrangian. One XGBoost." reads like the method.
- **Don't invent facts.** If unsure, soften ("≈", "reportedly", "see Table 1") or ask.
- **Use specific names, not generic categories.** "OLMoE-1B-7B" not "an MoE model."
- **Mono for IDs.** `OLMoE-L15-E17`, `arXiv 2604.14853` set in JetBrains Mono.

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

The locked spec for any annotation drawn on a 3D chart, 2D chart, diagram, or video frame.

### Locked rules

1. **Typeface:** Inter Tight 600 (or DejaVu Sans 600 fallback).
2. **Font size:** 24–32pt at rendering DPI. Scale up for video (60+).
3. **Background:** rounded pill — `boxstyle="round,pad=0.55"`, fc = role color, ec = role color, lw = 0.
4. **Text color:** `BG` (dark canvas) — high contrast on the pill.
5. **Arrow:** `arrowstyle="-|>"`, lw 2.4, `connectionstyle="arc3,rad=0.12"`.
6. **Maximum:** 3 annotations per chart.

### Color = role (locked)

| Role | Color |
|---|---|
| Method / answer | PRIMARY (per project) |
| Hero highlight | ORANGE #FF862F |
| Process / iteration | BLUE #58C4DD |
| Saturated / Easy | GREEN #83C167 |
| Wrong / Hard | RED #FC6255 |
| Transition / Responsive | YELLOW #F7D96F |
| Diminishing | PURPLE #9A72AC |

Don't introduce new colors for new annotations.

### Standard pill placements (axes-fraction)

| Position | (fx, fy) |
|---|---|
| Top-left | (0.18, 0.84) |
| Top-center | (0.50, 0.92) |
| Top-right | (0.82, 0.84) |
| Bottom-left | (0.18, 0.20) |
| Bottom-right | (0.82, 0.20) |

If 3 pills, prefer corners. If 1 pill, prefer top-center.

### matplotlib helper (in scripts/render_3d.py)

```python
def annotate_pill(ax, x3, y3, z3, text, color, fxy=(0.5, 0.92), arrow=True):
    """Phone-readable pill with optional arrow."""
    x2, y2, _ = proj3d.proj_transform(x3, y3, z3, ax.get_proj())
    inv = ax.transAxes.inverted()
    disp = ax.transData.transform((x2, y2))
    axfrac = inv.transform(disp)
    if arrow:
        ax.annotate(
            text, xy=axfrac, xycoords="axes fraction",
            xytext=fxy, textcoords="axes fraction",
            fontsize=24, fontweight=600, color=BG, ha="center", va="center",
            bbox=dict(boxstyle="round,pad=0.55", fc=color, ec=color, lw=0),
            arrowprops=dict(arrowstyle="-|>", color=color, lw=2.4,
                             shrinkA=2, shrinkB=8,
                             connectionstyle="arc3,rad=0.12"),
            zorder=20,
            family=["Inter Tight", "Inter", "DejaVu Sans"])
```

### Common annotation mistakes

1. **Pill too small** — fontsize=12 is invisible at IG resolution. Always 24+.
2. **Pill text too long** — 5 words max.
3. **Arrow too thin** — lw=1 disappears. Always 2.4.
4. **Arrow color != pill color** — visual disunity.
5. **More than 3 pills** — clutter. Move overflow to HTML below the chart.
6. **In-3D-plane text via `ax.text(x, y, z, ...)` for titles** — gets projected with perspective, reads slanted. Use HTML overlay for titles.

---

## Composition with other skills

| Need | Use alongside |
|---|---|
| Paper PDF as final deliverable | `academic-paper` instead |
| Persuasive caption | `worldbuilder-writing` for the caption, ml-content for the carousel |
| More design references | `pro-graphic-designer` discipline, constrained by ml-content brand |
| Fact-check at scale | `autonomous-research` agent |
| Find the right paper | `autonomous-research` |
| Native pptx slide deck | `pptx` instead — ml-content does HTML→PNG only |

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
├── carousel.html              # if carousel
├── manim_scenes.py            # if video
├── 3d/
│   ├── hero_chart.png
│   └── ...
└── slides/
    ├── slide_01.png
    └── ...
```

Naming: `01-llms-gaming-verifiers`, `04-asynctls-sparse-attention`, etc.

---

## Quick start for a new carousel

```
1. Pick paper. Note arXiv ID.
2. Create project folder: ~/Documents/ml-content/NN-short-slug/
3. Stage 1: Write the 5-file recon bundle.
4. Stage 2: Write 3d-audit.md and moodboard.md.
5. Stage 3: Lock design-spec.md.
6. Stage 4:
   - Copy scripts/carousel_template.html → carousel.html and edit per slide
   - Copy scripts/render_3d.py → render_3d_NN.py (edit OUT path), run to produce 3D PNGs
   - Copy scripts/render_carousel.py → render_NN.py (edit SRC/OUT), run to produce slides/
7. Stage 5: Run the grounding pass. Fix WRONG. Soften UNVERIFIED.
8. Write caption. Post.
```

## Quick start for a new video

```
1. Stage 1: Recon bundle (same 5 files — re-use).
2. Stage 2: 3d-audit.md (which scenes earn 3D — usually 2-3 of 8).
3. Stage 3: design-spec.md (palette, scene transitions, narration timing).
4. Write script.md (voice-over per scene with visual directions).
5. Stage 4: Copy scripts/manim_scene.py → manim_scenes.py. One Scene class per scene.
6. Render: manim -qh manim_scenes.py SceneName.
7. Concatenate + narrate via FFmpeg.
8. Stage 5: Grounding pass.
```

## Reference: scripts/

Templates in `scripts/`:
- `render_3d.py` — matplotlib 3D template with `annotate_pill`, `cube_faces`, three example renders (landscape, bars, cube).
- `render_carousel.py` — weasyprint+pdftoppm pipeline. Edit SRC/OUT for your project.
- `carousel_template.html` — HTML skeleton with all brand tokens, chrome, and one example slide. Duplicate `<section class="slide">` for each slide.
- `manim_scene.py` — four scene archetypes (Hook, Framing, 3D Terrain, Results counter).

All scripts are self-contained — copy, edit paths, run.
