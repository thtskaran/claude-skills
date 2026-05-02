# BrightData tool cheatsheet — for sourcing

All `bd:` tools are deferred. Call `tool_search` first with a relevant query (e.g., `tool_search(query="linkedin profile")`) to load the schema, then use the exact parameter names returned. Don't guess parameter names.

This cheatsheet is for reference — to remind you which tool exists for which purpose. The exact schema comes from `tool_search`.

---

## Discovery (figuring out where to scrape)

### `bd:search_engine_batch`
Run multiple search queries at once. The fastest way to scope a sourcing job.

Use for:
- Finding watering-hole pages (subreddits, conference speaker lists, GitHub orgs).
- Triangulating cross-platform handles for a known person.
- Comparing how a persona shows up across Google / Bing.

Pattern: queue 3–8 queries, scan returned URLs, decide which deserve a deep scrape.

### `bd:search_engine`
Single-query version. Use when you only need one targeted search.

### `bd:discover`
AI-ranked discovery. Use for fuzzier exploration ("who's writing about RAG evaluation in 2026") where you want ranked results, not raw SERP order.

---

## LinkedIn

### `bd:web_data_linkedin_people_search`
The workhorse for B2B sourcing. Search for people by role + location + company keywords.

Use when:
- You need to surface a list of candidates by criteria.
- You're starting from "find me 50 senior X in Y" with no specific names yet.

Output is a list — extract `profile_url` for each, then enrich with `_person_profile` if you need full data.

### `bd:web_data_linkedin_person_profile`
Full profile pull for a single LinkedIn URL. Returns experience, skills, education, location, headline, and posts (often).

Use when:
- You have a profile URL and want everything.
- You're doing the per-row enrichment in Phase 4.

Cost note: this is a "heavier" call — don't run on all 200 candidates. Filter to your shortlist first, then enrich.

### `bd:web_data_linkedin_posts`
Pull posts from a LinkedIn profile or post URL.

Use when:
- You need recent activity to personalize.
- The signal you're looking for IS a post (e.g., "people who posted about hiring in the last quarter").

### `bd:web_data_linkedin_company_profile`
Pull company data. Useful when sourcing employees of a target account list — pull the company first, then look at its people.

### `bd:web_data_linkedin_job_listings`
Indirect sourcing: companies hiring for X are often also good leads for selling-to-X. Niche but useful for sales workflows.

---

## Reddit

### `bd:web_data_reddit_posts`
Pull a Reddit post + its comments. The comments are gold — you get usernames, their stated context, and links they share.

Use when:
- A subreddit has a "who's hiring" or "share what you're working on" thread.
- You want to source from a specific viral post's commenters.
- You want voice-of-customer for a niche community.

Pattern: identify the right thread URL via `bd:search_engine`, then pull the full thread, then for each interesting commenter, search their username on cross-platforms.

---

## Twitter / X

### `bd:web_data_x_posts`
Pull X posts. Useful for surfacing what someone has actually said, vs. their corporate-LinkedIn version.

Use when:
- You've identified a candidate via LinkedIn and want their *real* voice for personalization.
- You're sourcing from a specific hashtag or thread.

X is especially strong for: indie hackers, infosec, ML researchers, journalists, designers, gamedev.

---

## Instagram

### `bd:web_data_instagram_profiles`
Profile-level data: bio, follower count, posts.

### `bd:web_data_instagram_posts`
Specific post data.

### `bd:web_data_instagram_reels`
Reels data — useful for creator sourcing where reels engagement is the signal.

### `bd:web_data_instagram_comments`
Comment data — useful for finding engaged audience members of a creator.

Use Instagram for: lifestyle creators, visual brands, local businesses, certain coaching niches, fashion, food.

---

## TikTok

### `bd:web_data_tiktok_profiles`
Profile data.

### `bd:web_data_tiktok_posts`
Post data.

### `bd:web_data_tiktok_comments`
Comments — useful for sourcing engaged audience.

### `bd:web_data_tiktok_shop`
TikTok Shop sellers.

Use TikTok for: Gen-Z creators, niche micro-influencers, certain consumer-product audiences.

---

## YouTube

### `bd:web_data_youtube_profiles`
Channel data.

### `bd:web_data_youtube_videos`
Video metadata + transcripts where available.

### `bd:web_data_youtube_comments`
Comments on videos — strong for sourcing engaged audience members.

Use YouTube for: long-form creators, educators, devlogs, podcasters with YT presence.

---

## Facebook

### `bd:web_data_facebook_posts`
Post data.

### `bd:web_data_facebook_events`
Event data — strong for local community sourcing.

### `bd:web_data_facebook_marketplace_listings`
Niche sourcing for sellers / local commerce personas.

### `bd:web_data_facebook_company_reviews`
Company reviews — useful for understanding a target company's reputation, less for sourcing people.

---

## GitHub, personal sites, niche forums, anything else

### `bd:scrape_as_markdown`
The general-purpose tool. Returns clean markdown of any URL.

Use for:
- GitHub profiles + their `/graphs/contributors` or repo READMEs.
- Personal blogs, Substacks (use the archive page), Notion pages.
- Conference speaker lists.
- IndieHackers milestone posts.
- ProductHunt launch pages.
- Any niche forum (HackerNews user pages, dev.to, Lobste.rs, etc.).

### `bd:scrape_batch`
Same as above but up to 10 URLs at once. Use for parallel pulls.

### `bd:scrape_as_html`
When you need the raw HTML structure (rare for sourcing — markdown is usually enough).

---

## Browser-based scraping (heavier, use sparingly)

`bd:scraping_browser_*` tools are for when a page requires JS execution or interaction (clicking, scrolling, filling forms). Most sourcing flows don't need these. Reach for them only when `bd:scrape_as_markdown` returns empty/blocked content on a page that clearly has the data you want.

---

## Specialized data tools (when the persona maps to e-commerce/business surfaces)

These are less common in pure people-sourcing but useful for adjacent jobs:

- `bd:web_data_amazon_product_reviews` — find reviewers (e.g., "people who reviewed pentesting books") by handle.
- `bd:web_data_etsy_products` / `bd:web_data_walmart_seller` — sellers on these platforms.
- `bd:web_data_zillow_properties_listing` — real-estate agent sourcing via listing agents.
- `bd:web_data_crunchbase_company` — company data (combine with LinkedIn for founder names).
- `bd:web_data_zoominfo_company_profile` — company profiles. Use carefully — verify any people data against primary sources.

---

## Pacing and pacing rules

- Rough budget: 30–50 BrightData calls for a list of N=30–100. If you blow past 60 calls, something's off — go back to the persona definition.
- Run discovery in batches (`search_engine_batch`, `scrape_batch`) — sequential calls waste time.
- For enrichment, batch in groups of 10–20 candidates at a time. Errors are easier to recover from in small batches.
- If a tool returns empty/error, don't retry blindly. Inspect the input — wrong URL format, expired URL, or geographic block are the usual causes.
