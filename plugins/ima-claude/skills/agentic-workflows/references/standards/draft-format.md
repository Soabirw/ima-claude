# Draft Format

Structural rules for drafts produced by the draft phase. Injected by the consumer when the recipe declares this file.

---

## What a Draft Is

A draft is a complete post blueprint that reads like the published page. Every structural element is in place. Every placeholder is marked with the exact placeholder format. An editor reading the draft should be able to move it to production with minimal changes.

A draft is not a partial document. It is not a summary of what will be written. It is not an outline with some prose filled in. If an element is missing, the draft is incomplete.

---

## 10 Required Elements

Produce all 10 elements in this order. Recipes may modify the sequence or add elements — follow recipe overrides when they conflict with this default.

### 1. Meta Description

150–160 characters. Keyword-rich. Describes what the reader will get from the page. Written as a complete sentence or two fragments. Does not begin with the site name.

```
Meta: [150–160 character description]
```

### 2. Title

Clear, specific, benefit-oriented. Not a topic label — a claim, a promise, or a question the reader is already asking. The title from the outline is a starting point; refine it for the draft.

```
# [Title]
```

### 3. Excerpt

The first paragraph of the piece, set apart as the excerpt. Must contain one bolded key phrase — the most important idea for a scanner to land on. The bolded phrase should be a noun phrase or short clause, not a single word.

```
**[bolded key phrase]** — [rest of excerpt paragraph]
```

Or the bold can fall mid-paragraph where it is most impactful.

### 4. Hero Element

One of:
- `[VIDEO EMBED: brief description of video content]`
- `[HERO IMAGE: brief description — subject, mood, source if known]`

Do not place a second visual element immediately after the hero. The prose intro follows.

### 5. Prose Intro

Two to three paragraphs that hook, frame, and set up the piece. Follows the hook/frame/setup structure from the outline's intro. Written in full prose — not bullets, not headers.

The intro should give the reader a reason to keep reading. It does not summarize the entire piece. It earns the reader's next scroll.

### 6. Citation Block

For content based on a study or published research, include the citation immediately after the intro:

```
**Citation:** [Author Last Names]. "[Study Title]." *[Journal Name]*. [Year]. [DOI or URL if available]
```

For content not based on a primary study, omit this element.

### 7. Body Sections

For each section from the outline, produce:

- An H2 header that states the section's core argument (not just the topic)
- Prose developing the argument, incorporating key points from the outline
- At least one bolded key phrase per section
- Inline blockquotes where the outline marked quote placements
- Asset placeholders where the outline marked asset placements
- A subheader (`###`) if the section covers more than two distinct sub-topics

No section should run more than four consecutive paragraphs without a visual break (image, quote, or subheader). Wall-of-text sections will be flagged in review.

Blockquote format:
```
> [Speaker Name]: "[near-verbatim quote]"
```

### 8. Related Reading

A list of three to five related resources with brief descriptions. Format:

```
## Related Reading

- **[Resource Title]** — [one sentence description] [URL or placeholder]
- **[Resource Title]** — [one sentence description] [URL or placeholder]
```

### 9. Forums Button

A call to action pointing to the IMA community forums. Use the standard placeholder:

```
[Forums Button]
```

Recipes may specify different community CTAs — follow the recipe override.

### 10. Asset Table

A reference block listing all embeds, downloads, and CTAs used in the piece. The editor uses this to confirm all assets are live before publishing.

```
## Asset Table

| Asset | Type | Location in Draft | Status |
|-------|------|-------------------|--------|
| [description] | Video embed | After intro | [URL or "TBD"] |
| [description] | Image | Section 2 | [URL or "TBD"] |
| [description] | PDF download | Related Reading | [URL or "TBD"] |
```

---

## Placeholder Conventions

Use these exact formats. Do not improvise placeholder syntax — the consumer may parse them.

| Placeholder | Use For |
|-------------|---------|
| `[VIDEO EMBED: description]` | Video that should be embedded |
| `[HERO IMAGE: description]` | Hero image at top of piece |
| `[STUDY SCREENSHOT: description]` | Figure or table from a study |
| `[Figure N: description]` | Any numbered figure |
| `[Interstitial: CTA name]` | Mid-content CTA (between sections) |
| `[Forums Button]` | Standard IMA forums CTA |
| `[specific missing data]` | Any specific fact not in source material — describe what is needed |

---

## Naming Rule

If the source material names it, the draft names it. There is no acceptable substitution of a specific reference for a generic one when the specific reference is available.

- Named study → use the study name
- Named drug or protocol → use the exact name as it appears in the source
- Named speaker → full name on first mention, last name only after
- Named institution → exact name, no abbreviation on first mention

If the source material does not name something, use the appropriate placeholder.

---

## What Does NOT Belong

- Body prose without structural elements — every piece of prose must live inside a named structural element
- Deferred decisions — "the editor can decide X" — make the decision and note it in editorial watch items if it is uncertain
- Generic references when specific ones are available in the source material
- Assets that have not been seen or confirmed — use a placeholder, not an invented description
- Prose summaries of what sections will contain — write the sections, do not summarize them
