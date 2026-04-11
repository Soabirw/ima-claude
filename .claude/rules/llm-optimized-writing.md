# LLM-Optimized Writing Convention

All skills, agents, personalities, and instruction files in this repo are machine-consumed.
Write for LLM comprehension, not human reading. Every token costs money and context window.

## Rules

### Drop
- Articles (a/an/the) where meaning stays clear
- Filler: just, really, basically, actually, simply, quite, rather, certainly
- Hedging: maybe, perhaps, might want to, could potentially, it seems like
- Pleasantries and throat-clearing
- "Why it matters" sections — if principle is clear, why is implied
- Redundant emphasis (bold + caps + exclamation = pick one)
- Philosophical quotes and "Final Word" sections
- "When to use this skill" prose that duplicates frontmatter description
- "Integration Points" lists that just name other skills (frontmatter handles discovery)
- Repeated cross-references scattered throughout (consolidate to one location)

### Structure
- Imperatives: "Use X" not "You should consider using X"
- Tables over prose for reference material
- Bullets over paragraphs for rules and lists
- One concept per line
- Decision trees: compact notation, no narrative wrapping
- Code examples: minimal, show pattern not story. One good example beats three mediocre ones.

### Preserve Exactly
- Code blocks, commands, file paths
- Technical terms and proper nouns
- Frontmatter (needed by plugin system)
- Table structure (already efficient)
- Decision trees and flowcharts (already compact)

### Compress
- "Why it matters:" + 4 bullets → 1-2 bullets max, or drop entirely if obvious
- "The key insight:" → just state the insight inline
- Before/After code examples → keep the good example, drop or minimize the bad one
- Section headers → flatten where nesting adds no value (### under ## under # = too deep)
- Cross-skill references → single table at end, not scattered throughout body

## Calibration

Skills that are already table-heavy and directive (gh-cli, mcp-atlassian tool catalog) need less work.
Skills that are philosophy-heavy and educational (functional-programmer, architect) need the most compression.
Code-example-heavy skills (py-fp, js-fp) — keep examples but trim surrounding prose.

## Quality Check

After compression, verify:
1. Every directive is actionable — LLM can follow it without interpretation
2. No information lost — compressed version covers same scenarios
3. Code examples still make sense without removed narrative
4. Decision logic still has clear branching criteria
