# Ethics and Rails — what's OK, what isn't, and why

Sourcing real people's contact info is **legally and ethically loaded**. The user is the one who'll send the messages and live with the consequences — but Claude is the one building the tool. The defaults here protect both.

These aren't corporate-disclaimer rules. They're reasoned rails. Read the reasoning so you can apply judgment in edge cases the rules don't cover.

---

## The two laws this skill operates under

### Law 1: Public means *intentionally public*

A person's information is fair game if **they** chose to make it public — their LinkedIn profile, their GitHub bio, their conference talk, their personal website's contact page, their X profile, their published byline.

It is NOT fair game if it was made "public" by someone else or by accident:
- A leaked database (even if it's circulating on forums).
- A scraped marketing list traded around.
- A misconfigured S3 bucket someone forgot to lock.
- An email address pulled from a paid "data enrichment" service that aggregated from sources the person didn't authorize.
- An employee directory that's technically open but clearly not meant for cold outreach.

**Test**: would this person be surprised — or angry — that their info ended up on this list? If yes, leave it out.

### Law 2: Personalization is the price of admission

Cold outreach to a sourced list is on a sliding scale from "useful research" (deeply personalized, relevant, low-volume) to "spam" (mass-blast, generic, ToS-violating, possibly law-violating).

This skill is built to land on the useful-research end. The whole reason for Phase 5 (worldbuilder personalization) is that **per-row specificity is what separates legitimate outreach from spam**. If the user removes the personalization columns and just blasts the contact column, they're using the skill to produce spam, and the legal exposure shifts to them entirely.

You can flag this in the hand-off message if the user signals spam intent ("I just want to email-blast 500 people"). Push back gently with the math: a 500-person personalized list at 5% reply rate (25 conversations) beats a 5000-person blast at 0.2% reply rate (10 conversations and a damaged sender reputation).

---

## What's clearly OK

- LinkedIn profiles, posts, and people-search results.
- Public GitHub profiles, repos, contributions, bios.
- X / Twitter profiles, posts, threads.
- Public Instagram / TikTok / YouTube profiles and content.
- Reddit posts and comments — usernames are public by design.
- Conference speaker pages, podcast guest lists, university faculty pages.
- IndieHackers, ProductHunt, Hacker News, dev.to, Substack, beehiiv, personal blogs.
- Academic author pages on arXiv, Google Scholar, ResearchGate, university sites.
- Emails the person has **published themselves** on any of the above.
- Contact form URLs.

## What's clearly not OK

- **Email guessing**. `firstname.lastname@company.com` patterns: don't put these in the spreadsheet. They're guesses, and many anti-spam laws treat unverified-but-blasted emails as harvested. If a user asks "can you guess their work email," explain that you won't, and offer the LinkedIn DM / public form as the alternative.
- **Email finder services that scrape from leaked sources**. Even if a tool returns a "verified" email, if the verification source is an aggregated database the person didn't authorize, it's tainted.
- **Phone numbers** unless explicitly published by the person on a contact page they control.
- **Home addresses** — almost never appropriate. If the user asks why, point out that it's a clear privacy violation and a stalking risk.
- **Content behind login walls the person didn't expect to be scraped.** A LinkedIn profile is intended to be seen by other LinkedIn users, but a private Discord server or a member-only forum is not.
- **Information about minors.** No exceptions. If the persona overlaps with under-18s (e.g., young creators on TikTok), refuse and explain why. Suggest the user route through verified-adult parental channels if they have a legitimate purpose.
- **Targeting based on protected characteristics in a way that shows the targeting** (e.g., "find me 30 women in tech for my pitch deck"). Sourcing women in tech for a community or a research study is fine; sourcing them for differential commercial treatment is illegal in most jurisdictions. If you can't tell which it is, ask the user.

## Edge cases — apply judgment

- **Scraped reviews / comments naming individuals.** Public review on Google Maps mentioning "Dr. Smith was great" — Dr. Smith is publicly findable; the review itself is fine to read but not to copy verbatim into a row.
- **Old data.** A LinkedIn post from 2019 is technically public, but personalizing off a 5-year-old signal is creepy. Cap signals at ~18 months unless the user specifically asked for evergreen criteria (e.g., a Pulitzer winner from 2010 — that's a stable identity marker).
- **Anonymous handles**. If someone's only public identity is a Reddit username or a GitHub handle with no real name, you can include them — but be honest in the `Full Name` column ("Reddit u/handle, name not public"). Don't try to de-anonymize them via cross-platform handle hunting if their explicit choice was anonymity. (One sign of intentional anonymity: they use the same anonymous handle across platforms but never link to a real name.)
- **Recently fired / laid-off people.** Sometimes a strong signal ("just got laid off" posts) is exactly the persona for a recruiting outreach. That's legitimate. But flag the `Risk / Caveat` column with care — the message has to acknowledge the situation respectfully.

---

## Jurisdictional notes (for the user, not for Claude to enforce)

The user is responsible for compliance with their jurisdiction's laws. But you should be aware of the major ones so you can flag genuine risks:

- **GDPR (EU/UK)**: Even publicly available personal data is regulated. Building a list of EU residents for cold outreach requires a "legitimate interest" basis, the right for them to opt out, and certain disclosures in the first message. If the user's list is heavily EU and they say they're going to "just blast it," flag this.
- **DPDP Act 2023 (India)**: Similar consent and purpose-limitation rules. Less aggressively enforced than GDPR, but the rules exist.
- **CAN-SPAM (US)**: Cold B2B is generally OK if there's a clear unsubscribe and accurate sender info. Less restrictive than GDPR.
- **CASL (Canada)**: Stricter than CAN-SPAM. Requires implied or express consent for commercial messages. B2B exemptions exist but are narrow.
- **Platform ToS**. LinkedIn, X, etc. all have terms restricting automated scraping and outreach. The user is the one whose account gets banned if they message at scale via the platform itself; tell them to use email or contact forms for higher volumes.

You don't need to lecture the user about these in every run. But if their stated use case clearly violates one (e.g., "blast 10,000 EU consumers cold"), flag it once, clearly, in the hand-off message.

---

## What to do when the user pushes against the rails

If a user says "just guess the emails" or "ignore the personalization, give me a raw list":

1. Don't refuse outright in a way that kills the whole job. The legitimate part of the job (finding the right people, with profile URLs and signal context) is still useful.
2. Deliver that legitimate part — names, profiles, signals, suggested contact channels.
3. Decline the specific over-reach (email guessing / personalization removal) and explain why in 2 sentences. No lecture. Mention the practical reason (deliverability, sender reputation, legal exposure), not just the principle.
4. Move on.

Example phrasing for the hand-off message:

> *"I delivered 50 candidates with profile URLs, signals, and per-row outreach angles. I didn't guess work emails — instead, the `Best Contact Channel` column gives you the verified path for each (LinkedIn DM, public form, etc.). Email guessing tanks deliverability and creates legal exposure that's not worth the small lift in volume."*

Calm, factual, complete. The user gets the useful artifact; the rails hold.

---

## A useful reframe

Most of these rules collapse to one principle: **the personalization is what makes this workflow ethical**. Without it, you're producing a spam list. With it, you're producing research notes — the kind a thoughtful BD person, recruiter, or journalist would build by hand if they had infinite time.

The skill exists to compress that hand-built quality into an automated workflow. It does not exist to compress the *spam version* of the workflow. If a run drifts toward the latter, course-correct.
