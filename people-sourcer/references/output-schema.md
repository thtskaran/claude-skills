# Output Schema — what goes in the spreadsheet

The output workbook has three sheets. This file describes each.

## Sheet 1: People

One row per candidate. Header row formatted (bold + filled). Frozen top row. Auto-sized columns. URLs hyperlinked.

### Default columns (in order)

| # | Column | Type | Description |
|---|---|---|---|
| 1 | `Row` | int | Auto-numbered 1..N |
| 2 | `Full Name` | text | Verified against source, not just handle |
| 3 | `Headline` | text | Their own one-line description (LinkedIn headline, X bio, etc.) |
| 4 | `Role` | text | Job title, normalized |
| 5 | `Company / Org` | text | Where they work / their own company |
| 6 | `Location` | text | City, Country |
| 7 | `Primary Platform` | text | LinkedIn / X / GitHub / etc. |
| 8 | `Primary URL` | hyperlink | Their profile URL on the primary platform |
| 9 | `Other URLs` | text (semicolon-separated) | Cross-platform handles found in Phase 4 |
| 10 | `Public Email` | text | Only if publicly listed; otherwise empty |
| 11 | `Best Contact Channel` | text | "Public email" / "X DM" / "Contact form: <url>" / "LinkedIn DM" |
| 12 | `Recent Signal` | text | The specific post/talk/repo/milestone that landed them on the list. Date if available. |
| 13 | `Signal URL` | hyperlink | Link to the signal source — user must be able to click and verify |
| 14 | `Why They Fit` | text | One sentence, anchored in the signal. Phase 5.1. |
| 15 | `Outreach Angle` | text | 1–2 sentences from the worldbuilder lens. Phase 5.2. |
| 16 | `Risk / Caveat` | text | Empty if none. Phase 5.3. |
| 17 | `Confidence` | text | High / Medium / Low — how strong is the fit? |
| 18 | `Source Query` | text | Which scrape query/tool surfaced this row (for audit) |
| 19 | `Date Sourced` | date | YYYY-MM-DD |

After column 19, append the user's custom fields. If they asked for "MRR (public)" or "Years of experience" or "Technologies used," those go here.

### Confidence rubric

- **High** — strong signal (specific recent post, talk, repo, milestone), full enrichment, public contact. Easy to write a real outreach line.
- **Medium** — has a signal but it's older than 6 months, OR enrichment partial (no cross-platform handles found), OR contact only via DM.
- **Low** — weak signal (generic bio, no recent activity), low confidence the persona definition fits. Mark these so the user can deprioritize.

Don't pad with Lows to hit N. If the persona only yields 22 Highs/Mediums, deliver 22.

### Formatting rules

- Hyperlink columns (`Primary URL`, `Signal URL`, anything in `Other URLs` if a single URL): use real Excel hyperlinks (not just text URLs that look clickable).
- Truncate any column to 300 chars max in the cell — wrap if needed. Outreach angles longer than 2 sentences are a sign you're padding.
- Sort by `Confidence` descending, then by `Date Sourced` descending.

---

## Sheet 2: Sources

The audit trail. One row per scrape operation. Lets the user re-run, verify, or extend the list later.

| Column | Description |
|---|---|
| `Round` | Discovery round (1, 2, 3) |
| `Query` | Exact query string used |
| `Tool` | bd tool name (e.g., `bd:web_data_linkedin_people_search`) |
| `Platform` | LinkedIn, Reddit, X, etc. |
| `Source URL` | The page scraped, if applicable |
| `Candidates Yielded` | How many rows from this query made it to the People sheet |
| `Notes` | Any quirks (e.g., "Geographic block — only EU results returned") |
| `Timestamp` | When you ran it (YYYY-MM-DD HH:MM) |

This sheet is small — usually 5–20 rows for a typical run. Don't pad it; if a query yielded 0 useful rows, still log it (negative results matter).

---

## Sheet 3: Outreach Playbook

A one-page briefing memo, not a bulleted FAQ. Written in real prose. The audience model from Phase 3.5 of the scratchpad, distilled for the user's actual outreach work.

Structure (use real headers, not bullets):

### Who these people are
A paragraph — the persona model. Not demographics. Their psychology, their world, what they care about.

### How they talk
The in-group language you observed in the scrape. List 5–10 specific phrases the user should mirror (and 3–5 phrases they should NEVER use because they'd flag the user as an outsider).

### Atomic units to open with
What does this audience already believe? These are your entry points. List 3–5.

### What to avoid
The immune triggers — phrases, framings, or pitch shapes that will make this audience reject the message. Be specific.

### Calibration recipe
Suggested sequencing: which 5–10 rows to message first, what message shape to test, what to learn before scaling to the rest of the list. One paragraph.

This sheet should be ~half a page of dense prose. The user is going to actually use it before they send a single outreach message — write it like a memo to a colleague, not like a corporate deliverable.

---

## File-level details

- File name pattern: `people-<purpose-slug>-<YYYYMMDD>.xlsx`
- Save to: `/mnt/user-data/outputs/`
- Workbook tab order: People → Sources → Outreach Playbook
- Set People sheet as the active sheet on save (so it opens there).
- Use the `xlsx` skill's openpyxl patterns — read `/mnt/skills/public/xlsx/SKILL.md` first.

## Custom field handling

When the user asks for custom fields, append them after column 19. If a field requires Phase 4 enrichment (e.g., "GitHub stars on top repo," "MRR if public"), capture the actual data from the scrape — don't leave columns half-filled. If a value isn't publicly available, write `"not public"` rather than leaving the cell blank, so the user knows you looked.
