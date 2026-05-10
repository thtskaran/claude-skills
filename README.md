# Claude Skills

Personally curated, self-tested skills for Claude Code — an experimental attempt to make vibe coding actually useful.

Every skill here is a top-level directory containing a `SKILL.md`. That's the whole convention. Drop a folder in, follow that shape, and the installer below picks it up automatically — no list to update, no manifest to edit.

## Install everything (one command)

Run from inside this repo. Both commands install every top-level directory that contains a `SKILL.md` into `~/.claude/skills/`. Re-running upgrades in place. Add a new skill tomorrow that follows the same structure → re-run the same command, it just works.

**Linux / macOS (bash, zsh):**

```bash
mkdir -p "$HOME/.claude/skills" && for d in */; do [ -f "${d}SKILL.md" ] || continue; rm -rf "$HOME/.claude/skills/${d%/}"; cp -R "$d" "$HOME/.claude/skills/"; done
```

**Windows (PowerShell):**

```powershell
$dst = "$HOME\.claude\skills"; New-Item -ItemType Directory -Force -Path $dst | Out-Null; Get-ChildItem -Directory | Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') } | ForEach-Object { $t = Join-Path $dst $_.Name; if (Test-Path $t) { Remove-Item -Recurse -Force $t }; Copy-Item -Recurse -Force -Path $_.FullName -Destination $dst }
```

Want one skill instead of all of them? Just `cp -R <skill-name>/ ~/.claude/skills/`.

## What each skill does

| Skill | One-liner |
|---|---|
| [`deslop`](deslop/) | Audit and harden AI-generated codebases. Two-phase workflow: structured multi-pass `AUDIT.md`, then safety-tiered fixes. Never touches business logic. |
| [`autonomous-research`](autonomous-research/) | Reads files in your active directory, runs exhaustive multi-round literature research, self-critiques in loops, and produces a publication-quality PDF. Built for "find the gap, write the thing." |
| [`ml-content`](ml-content/) | Ship publication-quality ML content — IG carousels, 3Blue1Brown-style explainer videos, posters, paper figures. Deep paper recon (5-file bundle) → real-3D-only design discipline → phone-readable annotations → grounding pass before posting. Locked render pipeline: weasyprint+pdftoppm for static, matplotlib3D for charts, Manim for videos. |
| [`people-sourcer`](people-sourcer/) | Builds real prospect / candidate / outreach lists. Iterative scraping across LinkedIn, Reddit, X, Instagram, TikTok, YouTube, GitHub. Per-person commentary, not generic blurbs. Outputs a multi-sheet xlsx. |
| [`pro-graphic-designer`](pro-graphic-designer/) | End-to-end graphic design — posters, carousels, banners, thumbnails, decks, ad creatives. Audience research → reference mining (Behance / Pinterest / Dribbble) → copy → output as Canva / HTML / SVG / PDF. |
| [`worldbuilder-writing`](worldbuilder-writing/) | Treats writing as applied psychology, not self-expression. The reusable engine for any blog post, email, pitch, script, landing page, or sales copy. |
| [`academic-paper`](academic-paper/) | Format text as a publication-ready PDF using reportlab — title block, sectioning, tables, figures, references. White-papers, preprints, lit reviews. |
| [`consolidate-memory`](consolidate-memory/) | Reflective pass over your `CLAUDE.md` / memory directory — merges duplicates, prunes stale facts, fixes the index. |
| [`docx`](docx/) | Read / edit / create Word documents. Tables of contents, headings, page numbers, tracked changes, comments, image insertion, find-replace. |
| [`pdf`](pdf/) | Read text + tables, merge / split, rotate, watermark, fill forms, encrypt / decrypt, OCR scanned pages, extract images. |
| [`pptx`](pptx/) | Read / edit / create PowerPoint decks. Templates, layouts, speaker notes, comments, combine / split. |
| [`xlsx`](xlsx/) | Read / edit / create spreadsheets. Formulas, formatting, charts, cleanup of malformed tabular data. |
| [`schedule`](schedule/) | Create a scheduled task that runs on demand or on an interval. |

## How they connect

Some skills explicitly read another skill's `SKILL.md` mid-run. If you cherry-pick rather than installing the whole set, install the dependencies too — those skills degrade silently without them.

```
autonomous-research ──▶ academic-paper

people-sourcer ─┬─▶ worldbuilder-writing
                ├─▶ xlsx
                └─▶ pro-graphic-designer ──▶ worldbuilder-writing

ml-content ─┬─▶ worldbuilder-writing      (hook + caption construction)
            ├─▶ pro-graphic-designer      (design discipline, brand-constrained)
            ├─▶ autonomous-research       (find the paper / fact-check at scale)
            ├─▶ academic-paper            (when the deliverable is a PDF, not a carousel)
            └─▶ pptx                       (when the deliverable is a native slide deck)
```

| Skill | Depends on | Why |
|---|---|---|
| `autonomous-research` | `academic-paper` | Final deliverable is a formatted PDF. autonomous-research literally `Read`s academic-paper before writing, then follows its reportlab workflow. |
| `people-sourcer` | `worldbuilder-writing` | Phase 0 (audience modeling) and the per-person commentary step both delegate to it. The skill explicitly states "this skill depends on it." |
| `people-sourcer` | `xlsx` | Phase 6 output is a multi-sheet xlsx. Read before generating. |
| `people-sourcer` | `pro-graphic-designer` | Architectural sibling — same scratchpad-driven, iterative-scraping shape. Cross-referenced for shared patterns. |
| `pro-graphic-designer` | `worldbuilder-writing` | Phase 0 (audience model) and Phase 4 (copy) both run through it. |
| `ml-content` | `worldbuilder-writing` | The "Hook Construction" stage is worldbuilder's audience-persona / leverage-point / reaction-map pass inlined for ML audiences. Read once before drafting any hook or caption. |
| `ml-content` | `pro-graphic-designer` | When you want extra design references beyond ml-content's locked brand, lean on pro-graphic-designer's reference-mining workflow — but keep ml-content's brand baseline. |
| `ml-content` | `autonomous-research` | For full grounding pass on 10+ claims, or when you need to find the right paper to make content about, delegate to autonomous-research. |

`worldbuilder-writing` is the most-depended-on node — install it first if you're picking and choosing. The installer above grabs everything in one shot, so this only matters for cherry-pickers.

## Why a BrightData token is required (for three of the skills)

Three skills are not "search the web a couple of times" skills — they are scraping pipelines:

- **`autonomous-research`** — multi-round structured scraping of search engines, papers, and arbitrary websites for its literature sweep.
- **`people-sourcer`** — ~40 calls per run across LinkedIn / Reddit / X / Instagram / TikTok / YouTube / GitHub to discover, dedupe, and enrich named individuals.
- **`pro-graphic-designer`** — Reddit / LinkedIn / Facebook / Instagram / research papers for audience signal, plus Behance / Pinterest / Dribbble for visual references.

All three load BrightData MCP tools at runtime via `tool_search` — `search_engine`, `scrape_as_markdown`, `scrape_batch`, and the platform-specific `web_data_*` extractors (`web_data_linkedin_person_profile`, `web_data_reddit_posts`, etc.). Those tools authenticate against your BrightData account using an API token.

Without the token:

- The `tool_search` calls return tools that fail at first invocation.
- Plain `WebSearch` + `WebFetch` cannot substitute. Most target platforms (LinkedIn, Instagram, TikTok, paywalled news, Behance) either block direct fetches, return JS-only shells, or rate-limit aggressively. BrightData's residential / unblocker layer is exactly what gets you past that — and the structured `web_data_*` endpoints return clean JSON instead of a brittle DOM scrape.
- The skills' iteration loops (round 1 broad → round 2 deep → enrichment) collapse to round 1 and the output is shallow.

The other skills don't need it. If you only run `docx`, `pdf`, `pptx`, `xlsx`, `worldbuilder-writing`, `academic-paper`, `consolidate-memory`, `schedule`, `deslop`, or `ml-content`, you can skip BrightData entirely.

### Extra runtime deps for `ml-content`

`ml-content` doesn't need BrightData, but it does shell out to a render pipeline. Install once:

```bash
# Static carousels / posters
pip install weasyprint matplotlib numpy
brew install poppler          # provides pdftoppm

# Videos (only if you do the 3B1B-style explainers)
pip install manim
brew install ffmpeg
# LaTeX — full MacTeX, or BasicTeX + the packages Manim needs
brew install --cask mactex-no-gui
```

Fonts: Inter Tight + JetBrains Mono load from Google Fonts at render time; CMU Serif loads from the dreampulse CDN — no local install needed.

**Setup:** add the BrightData MCP server to your Claude config with your API token. The token belongs to *you* — never paste it into a `SKILL.md` or commit it to this repo.

## Adding your own skill

1. Create a top-level folder: `my-skill/`.
2. Inside it, write a `SKILL.md` with frontmatter (`name`, `description`) and the body.
3. Add any `scripts/`, `references/`, `assets/`, `examples/` it needs alongside `SKILL.md`.
4. Re-run the install one-liner. Done.

The installer detects skills by the presence of `SKILL.md`, so anything in this repo without one (LICENSE, README.md, `.git/`) is left alone.

## Contributing

Open PRs welcome — new skills, improvements, fixes.

## License

MIT

## Contact

Karan Prasad — hello@KaranPrasad.com
