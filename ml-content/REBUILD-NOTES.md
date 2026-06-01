# ml-content — rebuild notes (2026-05-31)

Why the skill kept producing slop, and what changed. Grounded in a full read of the
real source: `github.com/3b1b/videos` (503K LOC) + `github.com/3b1b/manim` (manimGL),
extracted by 18 parallel agents (288 patterns, 343 API facts, all with file:line cites).

## The diagnosis (root causes)

1. **CE-vs-manimGL engine mismatch.** The old `scripts/manim_scene.py` was Manim
   Community Edition (`from manim import *`, `MathTex`, `ThreeDScene`,
   `set_camera_orientation`, `set_fill_by_value`, `Create`, `begin_ambient_camera_rotation`).
   None of these exist in manimGL — the file could not run. Grant's own `videos/CLAUDE.md`
   mandates manimGL: `Tex` not `MathTex`, `InteractiveScene`, `self.frame`.
2. **The "Manim default" was fiction.** 100% of the old-series episodes were actually
   built in matplotlib `render.py`, hand-placing ~57 text + ~20 boxes per scene with
   absolute coordinates — the worst tool for animation. Output shipped as `_v5.mp4`
   (5 slop-fixing re-renders) and read as static infographic islands, including a
   faux-3D parallelogram cube the skill's own "3D lock" forbade.
3. **Overlap treated as a validation problem.** The old "Five-Layer Defense" (bbox
   asserts + frame validator + ffmpeg caption pad) policed overlap after render. 3b1b
   never validates overlap — it prevents it at construction (relative layout 1194:21
   over absolute; content-sized `SurroundingRectangle`; named buff ladder; `fix_in_frame`).
4. **Motion was decoration.** Elements faded in from nowhere. Real 3b1b objects are
   *born from* their referent (`TransformFromCopy` 46× > `Transform` 41 > `FadeTransform`
   30 >> `ReplacementTransform` 6; `TransformMatchingTex` 0). Every motion teaches.
5. **Planning was marketing copy** with word-count targets. Real planning is an ordered
   list of named teaching beats that reads as the narration (`SCENES_IN_ORDER` +
   in-`construct()` section comments).

## What changed

- **SKILL.md** rewritten around the engine reality + Six Laws (relative layout / motion
  carries meaning / tiny DSL / earned-3D-never-static / measured metronome / one color
  per concept). Added the CE ban-list, the real animation catalog, the 15 rate funcs,
  the corrected color hexes (`YELLOW = #FFFF00`, not the invented `#F7D96F`), the measured
  pacing (play:wait ≈ 1.6:1, bare `wait()`=1s is 80% of holds, `run_time=2` modal),
  and the beat-sheet planning artifact. Retired the Five-Layer Defense, the word-count
  recon targets, and the CE `manim-voiceover` mixin (replaced with a DIY duration-driven
  approach that works on manimGL).
- **scripts/manim_scene.py** replaced with runnable manimGL (InteractiveScene, self-
  arranging DSL, born-from morphs, `self.frame.reorient` 3D, two-layer legibility).
- **scripts/helpers_template.py** added: the domain-DSL recipe (self-arranging Mobject
  + `show_*` verb).
- **scripts/render_3d.py** fixed yellow hex + scoped to static carousels only.
- Originals preserved in `_backup_20260531/`.

## Source of truth (cloned, kept for reference)

- `/home/karan/Documents/cowork/insta_reels/.research/manim`  — manimGL engine
- `/home/karan/Documents/cowork/insta_reels/.research/videos` — 3b1b production code
- `/home/karan/Documents/cowork/insta_reels/.research/extraction_reports.json` — the 18-agent extraction

Key files to imitate: `videos/_2024/transformers/{attention,mlp,embedding,ml_basics,
network_flow,helpers}.py`, `videos/_2024/holograms/diffraction.py` (3D gold standard),
`videos/CLAUDE.md` (Grant's own rules).

---

## Update (2026-05-31) — folded in lessons from shipping the DeepSeek-V4 reel

Added the **proven production pipeline** (§13) the skill had only described in theory:
- `scripts/pipeline/{vo_continuous,timing,build_captions,assemble}.py` — one continuous
  ElevenLabs VO with character timestamps → per-scene narration spans → **speed-fit** each
  scene to its span (setpts; no cut, no freeze, no dead air) → burned `.ass` captions → mux.
- `scripts/thumbnail_template.py` — 9:16 with the 1:1/4:5 safe-crop bands baked in.
- **Vendor 3b1b's `transformers/helpers.py` as `tb_helpers.py`** (NumericEmbedding, WeightMatrix,
  EmbeddingArray, ContextAnimation) = fastest path to architecture density.
- **3D-vs-flat rule:** 3D wins for clouds/surfaces/collapsing volumes; 3D *hurts* stacks of
  thin layers (render those flat face-on).
- **Copy register:** human but professional (not robotic enumeration, not slang); TTS landmine
  noted ("V4" → "deep 5 four", so say "the latest model").
- **Render-critique gotchas table** (real bugs the frame-reading loop caught + fixes).

Verified end to end: a 2-min 1080p DeepSeek-V4 reel rendered on manimGL 1.7.2, with continuous
human VO, burned captions, and 9:16/1:1/4:5 thumbnails. Reference project:
`/home/karan/Documents/cowork/insta_reels/01-deepseek-v4/`.

---

## Update (2026-05-31, later) — the zero-error gate ("treat every video as nuclear")

A factual error reached a PUBLISHED reel (the DeepSeek-V4 video said "a thousand layers"; the
model is ~61), alongside a mislabeled quantity ("q·k" on relevance weights) and a scope
overstatement ("each weight" for FP4, which is only the MoE experts + indexer). Root cause:
the grounding pass wasn't run rigorously on BOTH the script and the rendered frames.

Added to SKILL.md:
- **PRIME DIRECTIVE** at the very top: every video is nuclear, zero errors ship, can't-cite-it-cut-it.
- **§10 rewritten as a two-stage gate:** Gate A (claims ledger before rendering) + Gate B (audit
  the RENDERED video — on-screen numbers/labels/captions/thumbnail, not just the script).
- The **four failure modes that shipped**, named: dramatized numbers, mislabeled quantities,
  scope overstatement, false thumbnail hooks.
- Workflow steps 3 & 7 are now the two gates; gotchas table gains the FadeTransform title-garble row.
