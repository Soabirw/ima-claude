---
content_type: webinar-summary
label: webinar-summary
description: "Webinar recording → blog post summary with speaker matching and transcript analysis"
phases:
  - gather
  - outline
  - draft
  - review
  - deliver
standards:
  gather: []
  outline:
    - editorial-standards
    - outline-format
  draft:
    - editorial-standards
    - draft-format
  review:
    - editorial-standards
    - draft-format
  deliver:
    - editorial-standards
templates:
  deliver:
    - avada-construction-guide
    - avada-webinar-example
    - cta-block-catalog
    - espo-email-preparation
    - webinar-recap-email-espo
requires_transcript: true
transcript_model: gpt-4o-transcribe-diarize
---

## gather

- Source material is primarily a video transcript (multi-speaker, diarized)
- Match ALL speakers against the IMA speaker catalog (provided by consumer)
- Note speaker credentials carefully — flag if transcript doesn't include full credentials
- Look for: key claims with timestamps, audience Q&A segments, slides/visuals referenced
- Word target guidance for webinars: 60-min webinar with rich discussion → 1,200-1,500 words; 30-min or thin content → 800-1,000 words
- Asset inventory should specifically note: video embed URL (always present for webinars), any slides shown, any studies/papers referenced by speakers

## outline

- Structure around themes/insights, NOT chronological webinar order
- Introduce speakers in a "Meet the Experts" section (after intro, before body)
- Each body section should draw from multiple parts of the transcript if relevant
- Quote selection priority: patient impact statements > crystallizing insights > mechanism explanations
- Place video embed as hero element
- For multi-speaker webinars: ensure each speaker gets proportional representation unless one clearly drove the key insights
- Word target inherited from gather phase

## draft

- Hero element is always `[VIDEO EMBED: video URL from gather phase assets]`
- Opening formula: hook with the webinar's most impactful finding, then frame why this matters for patients, then introduce the webinar context
- Citation block: not typically needed for webinars (no single study to cite), but include if speakers reference a pivotal study
- Speaker attribution: "Dr. [Last], [brief credential]" on first mention, "Dr. [Last]" thereafter
- Quotes: clean up verbal stumbles and fillers, but preserve the speaker's distinctive phrasing and word choices
- If webinar covers multiple topics with variable evidence strength, lead with the strongest findings
- Webinar-specific asset table entries: video embed (confirmed), speaker headshots (check catalog), slides (if referenced)

## review

- Check speaker credential accuracy against catalog entries
- Verify all speakers are attributed proportionally to their contributions
- Verify quotes are near-verbatim (compare against transcript excerpts in gather output)
- Check that chronological webinar structure hasn't leaked into the post structure
- Webinar-specific AI tells: "In this webinar, the speakers discussed..." (replace with specific claims), "The panel explored..." (name what they found)

## deliver

- Produce ALL THREE deliverables: markdown draft, Avada Fusion Builder markup, and EspoCRM recap email HTML
- Avada markup: use the webinar example template as structural reference — match its container/row/column nesting exactly
- Video embed: use `[fusion_code]` block with the actual video URL from gather phase assets
- CTA selection: webinar posts typically get the Webinar Donation CTA (Global ID 67674) as primary interstitial; match secondary CTAs to the specific topic
- Speaker headshots: if available in catalog, include headshot+bio layout per the construction guide's two-column pattern
- Recap email: derive subject line from the draft's hook, pull 2-3 key takeaways from body sections, link to the full blog post as primary CTA
- Catalog additions to check: new speakers not in catalog, new CTAs mentioned by speakers, new resource links shared during webinar
- Next deliverables to suggest after these three: social media posts (1 per platform), webinar replay promotion email, newsletter inclusion
