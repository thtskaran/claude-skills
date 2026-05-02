# Sourcing Brief — <project name>

> Created: <YYYY-MM-DD>
> Target N: <number>
> Status: <intake | scraping | enriching | personalizing | done>

---

## Current state (update as you go)

A 3-line summary of where you are. Rewrite this every phase change. Keeping this fresh means if the run gets long and you lose context, you can re-orient in 10 seconds.

Example:
> Discovery done (Round 2 complete). 67 raw candidates in `candidates.jsonl`. Skewed all-LinkedIn — need 1 more round on Reddit and X. Then enrichment.

---

## Phase 1: Persona

- **Persona** — <role + seniority + function. Be specific.>
- **Signals** — <what publicly-visible behavior identifies them?>
  - <signal 1>
  - <signal 2>
- **N target** — <number>
- **Purpose** — <recruiting / sales / podcast / research / outreach / ?>
- **Geography** — <countries, cities, language>
- **Custom fields user wants** — <field 1, field 2, ...>
- **Output preference** — <xlsx / Google Sheet / CSV>

### Out of scope (write down so you don't drift)
- <thing 1 NOT to source>
- <thing 2 NOT to source>

---

## Phase 2: Source strategy

### Platforms (ranked)
1. <Primary platform + why>
2. <Secondary>
3. <Tertiary if relevant>

### Query plan
| # | Query | Tool | Platform | Expected yield |
|---|---|---|---|---|
| 1 | `"…"` | `bd:search_engine_batch` | Discovery | watering holes |
| 2 | … | … | … | … |

(Update as you go — log actual queries you ran, not just planned ones.)

---

## Phase 3: Discovery — round logs

### Round 1 — Discovery (<date>)
- Tools: …
- Watering holes found:
  - <URL or subreddit or page>
  - …
- Notes: <what surprised you, what to dig into next>

### Round 2 — Pull candidates (<date>)
- Sources scraped: …
- Candidates added: <count>
- Running total in candidates.jsonl: <count>
- Notes: …

### Round 3 — Gap fill (<date>)
- Gap identified: <e.g., "all-US, no EU">
- Targeted queries: …
- Candidates added: <count>

---

## Phase 3.5: Audience model (worldbuilder pass)

> Read /mnt/skills/user/worldbuilder-writing/SKILL.md Phase 0 first.

- **World they live in** — <their mental environment>
- **In-group language** — <exact phrases they use, not your translations>
  - Example phrases scraped: "<phrase 1>", "<phrase 2>"
- **What they already believe** (atomic units to use as openers) — <bullets>
- **Deepest desire / fear on this topic** — <one line>
- **Status hierarchy in their world** — <what's high-status vs. low-status>
- **The ONE thing user wants them to believe/do after outreach** — <one line>

This becomes the "Outreach Playbook" sheet in the final output.

---

## Phase 4: Enrichment notes

- Batch size: <e.g., 15 at a time>
- Issues encountered: <e.g., "5 LinkedIn URLs returned 404 — likely renamed handles">
- Contact discovery yield: <X of N had public emails>

---

## Phase 5: Personalization notes

- Anti-pattern check: did any "Outreach angle" sound generic? <list rows that did and got rewritten>
- Risk flags raised: <count + sample>

---

## Phase 6: Output

- File: `/mnt/user-data/outputs/<filename>.xlsx`
- Sheets: People, Sources, Outreach Playbook
- N delivered: <number>
- N dropped at QA + reasons: <list>

---

## Hand-off message draft

(Three things — see SKILL.md Phase 7.)

1. N delivered: …
2. Audience insight (one paragraph): …
3. Concrete next step: …
