---
name: pro-graphic-designer
description: Use this skill for any graphic design task — posters, flyers, social media posts, carousels, LinkedIn banners, YouTube thumbnails, infographics, ad creatives, brand visuals, pitch decks, event invites, merch, or any "design me a ___ / make a visual for ___ / I need a poster / create a graphic / design a thumbnail" request. Trigger even when the user just hands over a topic ("design something for my AI startup") and expects a finished visual. Runs the full pro workflow: iterative BrightData scraping of Reddit/LinkedIn/Facebook/Instagram/research papers to understand the topic, audience modeling via the worldbuilder lens, copy written via worldbuilder-writing, real visual references mined from Behance/Pinterest/Dribbble, and output through Canva, HTML/CSS, SVG, or PDF. Prefer this over frontend-design when the deliverable is a marketing/graphic asset rather than a web UI.
---

# Pro Graphic Designer

A real designer doesn't start in Figma. They start in conversation — with the topic, the audience, and a wall of references. Only after all three are locked do they open a tool. This skill makes Claude work that way.

## Core premise

AI slop happens when a model invents "design" from priors. Real designers borrow aggressively from real references, then remix. Your novelty comes from the **combination** plus the **context-specific content**, not from pulling aesthetics out of thin air.

So the rule is: **never design from zero. Always design from research.** Research the topic, the audience, and the references — then execute.

## The workflow

Six phases. Each one writes to a scratchpad so context survives long runs.

```
1. Intake         → pin down the brief
2. Topic research → scrape sources (only if topic is thin)
3. Audience model → worldbuilder lens
4. Copy           → worldbuilder-writing skill
5. Visual mining  → Behance / Pinterest / Dribbble
6. Execute        → Canva / HTML / SVG / PDF
```

Skip phases that are already done. If the user hands you a full brief with copy and references, jump straight to execution. Match effort to the job — don't do research theater.

---

## Phase 0: Scratchpad first

Before anything else, create a scratchpad so you don't lose context five steps in.

```bash
mkdir -p /home/claude/design-work
cp references/scratchpad-template.md /home/claude/design-work/brief.md
# or create inline from the template below
```

The scratchpad lives at `/home/claude/design-work/brief.md`. Write to it as you go — don't batch. Every scraping round, every insight, every reference URL gets appended under the right section. The template is in `references/scratchpad-template.md`.

Why this matters: later phases pull from earlier ones. If you don't record the audience's in-group language in Phase 3, you'll write generic copy in Phase 4. If you don't log reference URLs in Phase 5, you'll forget which composition you were going to steal. Treat the scratchpad as your working memory.

---

## Phase 1: Intake

Pin down the brief in the scratchpad before doing anything else:

- **Topic** — what's the design about?
- **Deliverable** — poster, IG post, carousel, LinkedIn banner, YT thumbnail, flyer, deck, ad?
- **Dimensions / platform** — this constrains layout. IG post is 1080×1350, story is 1080×1920, YT thumb is 1280×720, A4 poster is 2480×3508 at 300 DPI, etc.
- **Purpose** — what should the viewer do/feel/believe after seeing this?
- **Constraints** — brand colors, logos, existing assets, tone restrictions, "must include X"?
- **Existing content** — did the user provide copy, or do you need to write it?

If the brief is vague ("design something for my pentesting course"), ask 1–2 targeted questions before spinning up research. Don't ask a wall of questions — ask the ones that actually change what you build.

---

## Phase 2: Topic research (iterative multi-step scraping)

Skip this phase entirely if the user provided enough content. Otherwise, do it properly — one search is never enough.

### The iterative loop

Topic research is not "Google it once." It's a multi-round loop where each round is informed by what the previous round found. Roughly:

**Round 1 — Discovery (broad).** Figure out *where* the conversation around this topic lives. Is this a Reddit topic? A LinkedIn topic? A Twitter/X topic? An academic topic? A TikTok topic? All of them?

Use `bd:discover` or `bd:search_engine_batch` with queries like:
- `"<topic>" site:reddit.com` → find the active subreddits
- `"<topic>" site:linkedin.com` → find the thought leaders / companies posting
- `"<topic>" arxiv` or `"<topic>" research paper` → find the academic angle
- `"<topic>" tiktok` / `"<topic>" instagram` → find the visual/cultural angle

Write the top findings to scratchpad under "Round 1 — Discovery."

**Round 2 — Deep dive into the best sources.** Now scrape the specific sources that looked richest. This is where the platform-specific BrightData tools shine:

- Reddit post URL → `bd:web_data_reddit_posts` (gets post + comments, clean)
- LinkedIn post URL → `bd:web_data_linkedin_posts`
- Instagram post → `bd:web_data_instagram_posts`
- TikTok post → `bd:web_data_tiktok_posts`
- YouTube → `bd:web_data_youtube_videos` / `bd:web_data_youtube_comments`
- Facebook post → `bd:web_data_facebook_posts`
- Generic article/blog/paper → `bd:scrape_as_markdown`
- Several URLs at once → `bd:scrape_batch` (max 10)

Grab the *actual language* people use. Copy exact phrases, slang, jargon, gripes, jokes. Save to scratchpad with source URLs. These become raw material for Phase 3 (audience) and Phase 4 (copy).

**Round 3 — Gap filling.** Look at what you have. What's missing? A demographic angle? A pain point? A counter-view? Run one more targeted round to fill the gaps. Stop when you have enough, not when you've exhausted the web.

### Source matrix (which platform for which topic?)

See `references/source-matrix.md` for a decision table. Quick version:

| Topic type | Primary source | Why |
|---|---|---|
| B2B / SaaS / enterprise | LinkedIn posts, founder blogs, case studies | Where buyers and sellers talk |
| Consumer product / D2C | Instagram, TikTok, Reddit (product subs), YouTube reviews | Where customers react |
| Dev tools / technical | Reddit (r/programming, specific subs), Hacker News, GitHub, arxiv | Where devs vent and praise |
| Pentesting / security | Reddit (r/netsec, r/hacking), Twitter/X infosec, ctftime, research papers | Where the tribe lives |
| ML / AI | arxiv, Twitter/X, r/MachineLearning, Papers with Code, LessWrong | Academic + culture |
| Academic / research | Google Scholar, arxiv, researchgate, university press releases | Primary literature |
| Cultural / lifestyle | TikTok, Instagram, niche subreddits, Pinterest | Visual and vibe-led |
| Local event / community | Facebook groups/events, local subreddits, community sites | Hyperlocal |

### Know when to stop

After each round, ask: do I understand (a) what this topic actually is, (b) who cares about it, (c) what words they use, and (d) what they're excited or angry about? Once yes, move on. Two solid rounds usually beats five half-hearted ones.

---

## Phase 3: Audience model (worldbuilder lens)

Read `/mnt/skills/user/worldbuilder-writing/SKILL.md` Phase 0 before doing this phase — it's the authoritative source on audience modeling. This section is the graphic-design-specific overlay on top of that.

From the scraped data plus any brief info, build an audience profile in the scratchpad:

**Psychology (from worldbuilder):**
- What world do they live in? (their mental environment)
- What language do they use? (exact in-group terms, not translations)
- What do they already believe? (atomic units you can use as entry points)
- What's their deepest desire or fear on this topic?
- What's the ONE thing you want them to believe/feel/do after seeing this design?

**Visual dimension (specific to design):**
- How do they *look*? What does their Instagram feed look like? Their Notion? Their desk?
- What aesthetics signal "one of us" to them? (hacker aesthetic = green-on-black terminals; yoga teacher aesthetic = sage/cream/arched type; Gen-Z meme page = cursed blur + Impact font)
- What aesthetics signal "outsider trying to sell me something" to them?
- What colors, fonts, and imagery are already in their world?

You learn the visual dimension by looking at what they *already consume*. Pinterest boards they follow. Instagram accounts they like. YouTube channels they watch. Scrape a few representative profiles if needed. This is anthropology, not creativity.

Write all of this to the scratchpad under "Audience Model." This becomes the brief for both the copy and the visuals.

---

## Phase 4: Copy (worldbuilder-writing)

Every piece of copy on the design — headline, subhead, body, CTA, even the captions on an infographic — should go through the worldbuilder-writing skill. Read `/mnt/skills/user/worldbuilder-writing/SKILL.md` and apply it.

Concretely:
1. Identify the single leverage point (one sentence).
2. Draft the hook using the audience's exact language.
3. Structure the copy as atomic unit → modification → grounding (the zoom-in or zoom-out pattern).
4. Kill AI-slop patterns — no "In today's fast-paced world," no "It's not just X, it's Y," no meaningless transition sentences.
5. Run the worldbuilder execution checklist on the copy before committing.

Write all copy into the scratchpad under "Copy." Include a one-line rationale per block ("this hook uses their word 'lobby' instead of 'reception' because...").

**Design-specific copy rules:**
- Headlines are short. If it doesn't fit in one glance, it's not a headline.
- Every word on a design is real estate. Cut ruthlessly.
- CTAs are verbs. "Start free," "See how," "Book a demo" > "Click here."
- Numbers beat adjectives. "3x faster" > "much faster."

---

## Phase 5: Visual reference mining

This is the anti-slop phase. You go find 15–30 real, strong references from designers who've already solved similar problems, then either adapt one heavily or merge a few.

### Where to mine

- **Behance** (`behance.net`) — highest-quality curated work, full case studies, often shows process
- **Pinterest** (`pinterest.com`) — fastest moodboard builder, great for aesthetic direction
- **Dribbble** (`dribbble.com`) — shot-based, great for small UI/illustration details
- **Awwwards** (`awwwards.com`) — web-leaning but great for typography/layout ideas
- **Are.na** (`are.na`) — curated indie taste, often niche and fresh
- **Designspiration** (`designspiration.com`) — color-forward
- **Fonts in Use** (`fontsinuse.com`) — for typography-specific inspiration
- **Brand New** (`underconsideration.com/brandnew`) — for identity/branding references

### How to mine (not "search and hope")

1. **Start from the audience aesthetic, not the topic.** Search "cyberpunk minimal poster" or "editorial magazine grid" — a *style direction* — not "pentesting poster." Styles have established visual languages; topics don't.
2. **Use `bd:search_engine` with `site:behance.net` / `site:pinterest.com`** to find collection pages and specific posts.
3. **Use `bd:scrape_as_markdown` or `bd:scrape_as_html`** on Behance/Pinterest pages to get structured content. For Pinterest, scraping a board URL gives you dozens of pins with image URLs.
4. **Save to scratchpad** under "Visual Research" — URL + one-line note on *what* you're stealing from it (composition? palette? typography? texture?).

### Pattern analysis

Once you have 15–30 refs, look for patterns. In the scratchpad, note:
- Recurring color moves (e.g., "warm black + electric cyan + soft cream appears in 8 of 15")
- Recurring typographic moves (e.g., "huge serif display + tiny monospace captions")
- Recurring compositional moves (e.g., "heavy asymmetric grid, big negative space top-right")
- Recurring textures/effects (grain, noise, chromatic aberration, halftone, etc.)

This pattern analysis is what you'll execute from. Individual references give you ideas; patterns give you a *language*.

### The honest approach to "copying"

Be clear with yourself about what you're doing:
- **Adapt one reference heavily**: take the composition and typographic hierarchy, swap in your content, shift the palette slightly. Note the source in the scratchpad. This is standard designer practice.
- **Merge 2–3 references**: composition from A, palette from B, typography from C. The synthesis plus your content is the novelty.
- **Do NOT reproduce protected creative elements verbatim** — someone else's photograph, illustration, or logo. That's not reference use; that's theft.

Record which references you're adapting in the scratchpad. Under "Design Direction," write one paragraph: "I'm adapting X's composition with Y's color move and Z's type treatment, for this audience because..."

---

## Phase 6: Execute

Pick the output format based on the deliverable. Decision tree:

### Canva — when the user wants an editable deliverable

Use when:
- User asked specifically for Canva
- Deliverable is presentation, doc, social post, email, flyer — and they might want to edit later
- User mentioned templates or brand kits
- Output needs to go into a non-technical workflow

Tool: `Canva:generate-design` (for fresh designs) or `Canva:import-design-from-url` (to import from URL). For presentations specifically, go through `Canva:request-outline-review` first — it's the gate for presentation generation.

Pass a detailed `query` parameter — don't just say "a poster about pentesting." Include:
- The audience
- The copy (from Phase 4)
- The aesthetic direction (from Phase 5)
- Specific reference cues ("editorial minimal with serif display type over muted black")

### HTML / CSS — when you want pixel control

Use when:
- The user wants a web-embeddable graphic
- You need precise typography and layout control
- Output is going into an artifact for preview
- Budget allows iterating on the code

Read `/mnt/skills/public/frontend-design/SKILL.md` before writing HTML. Render inline via `visualize:show_widget` (for quick inline display) or save as an HTML file and present it. Do NOT use localStorage/sessionStorage in artifacts — not supported.

### SVG — when the output is a logo, icon, or vector illustration

Use when:
- Output needs to be infinitely scalable
- It's a logo, icon set, or flat illustration
- Output needs to be editable in Figma/Illustrator later

Write the SVG directly. Use `visualize:show_widget` to preview inline.

### PDF — when output is print-ready

Use when:
- User needs to print (A4 poster, flyer, business card)
- User asked for PDF specifically

Read `/mnt/skills/public/pdf/SKILL.md`. Typically: build the design in HTML with print-friendly CSS, then convert via the pdf skill's tooling.

### Whichever format — execution principles

- **Commit to one bold direction.** Timid, evenly-distributed aesthetics are AI slop. Pick a clear aesthetic point of view (per frontend-design skill) and execute precisely.
- **Typography carries the design.** Avoid Inter/Roboto/Arial/system defaults — they're the visual equivalent of writing in Helvetica. Pick a distinctive display pairing.
- **Color: dominant + accent > five equal colors.** Look at the color pattern you extracted in Phase 5 and honor it.
- **Detail at the edges.** Grain overlay, subtle textures, deliberate margins, real shadows. The 10% of craft time at the end separates a real design from a template.
- **Kill AI aesthetics on sight.** Purple gradients on white, centered everything, stock-photo hero + bullet list — if you catch yourself doing this, go back to Phase 5 and look at the references again.

---

## Phase 7: Review before delivering

Before presenting the design, walk the checklist:

- [ ] Does the opening (hook / primary visual) land within the audience's world?
- [ ] Does it speak their in-group language, not a translation?
- [ ] Is there ONE clear leverage point, not a laundry list?
- [ ] Does the aesthetic match the audience's visual vocabulary?
- [ ] Is there a clear visual hierarchy (one dominant element, clear secondary, quiet tertiary)?
- [ ] Do the typography choices feel intentional and distinctive?
- [ ] Does any element look like AI slop (generic gradient, cliché stock vibe, centered-everything, default system font)?
- [ ] Did I record the references used in the scratchpad?

If something fails the checklist, fix it before delivering. If the user asks for variants, produce 2–3 with *genuinely different* directions (not three shades of the same thing) — different composition, different aesthetic family.

---

## Scratchpad hygiene

- One file per project: `/home/claude/design-work/<project-slug>/brief.md`.
- Append as you go. Don't wait until the end to document.
- Keep raw scrapes separate from distilled notes. Raw scrapes go in `/home/claude/design-work/<project-slug>/raw/` as individual markdown files per source.
- When the scratchpad gets long, add a "Current state" section at the top that summarizes where you are — so if you lose context, you can reorient fast.

Template is at `references/scratchpad-template.md`. Copy it and fill in.

---

## Anti-patterns

Things that look like work but aren't:

- **Scraping for the sake of scraping.** If the user gave you a clear brief, don't spend 20 minutes "researching the audience." Just design.
- **Reference hoarding.** 30 refs is a ceiling, not a target. 10 great refs beats 30 mediocre ones.
- **Describing the design instead of making it.** If you've written four paragraphs about "the design will evoke a sense of..." and haven't produced the design, you're stalling.
- **Generating three nearly-identical variants.** If the user asked for options, make them actually different directions.
- **Skipping the worldbuilder step.** The copy is half the design. Weak copy sinks strong visuals.
- **Defaulting to Canva for everything.** Canva is for editable deliverables. HTML/SVG is for pixel-perfect or unusual formats. Don't reach for Canva out of habit.

---

## Example shape of a run

User says: "design me an Instagram carousel to announce my pentesting bootcamp launch."

Rough flow:
1. **Intake** — confirm 1080×1350, 5–7 slides, audience (aspiring pentesters? working devs pivoting?), launch date, price.
2. **Research** — if audience is "aspiring pentesters," scrape r/netsec, r/hacking, r/AskNetsec for how they talk about learning and certs. One LinkedIn round on how existing bootcamps (OffSec, HackTheBox Academy) position themselves. Scratchpad gets filled.
3. **Audience model** — they hate fluff, they love real CTFs and OSCP cred, they distrust marketing-speak. Visual world: terminal green, matrix-y but *not* cringe, understated confidence.
4. **Copy** — hook: something like "Eight weeks. Five CTFs. One real OSCP-style final." Built from the scraped language, not from generic bootcamp-speak.
5. **Visual mining** — Behance + Pinterest for "editorial cyberpunk," "terminal aesthetic poster," "minimal tech magazine." Extract palette (warm black + acid green + bone white), type (mono + condensed sans), composition (big negative space, small strong anchor).
6. **Execute** — HTML/CSS carousel as an artifact if they want preview-ready, or Canva if they want to edit. Seven slides, each earning its place. Grain overlay, hand-tuned margins.
7. **Review** — would a working pentester roll their eyes at any slide? If yes, fix.

That's the full flow. Most real runs are messier — the point isn't the sequence, it's the discipline of not skipping audience and reference research.

---

## Related skills

- `worldbuilder-writing` — authoritative on audience modeling and copy. This skill depends on it.
- `frontend-design` — authoritative on frontend aesthetics when output is HTML/CSS. Read before writing web UI.
- `pdf` — for print-ready output.
- `pptx` — if the deliverable turns out to be a slide deck and Canva isn't the right fit.

Don't reinvent what those skills already cover. Read them and dispatch.
