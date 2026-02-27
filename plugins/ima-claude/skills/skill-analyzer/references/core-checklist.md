# Core Quality Checklist

Use this checklist when analyzing any Skill.

## Frontmatter Validation

- [ ] `name` field present
- [ ] `name` ≤64 characters
- [ ] `name` uses only lowercase letters, numbers, hyphens
- [ ] `name` contains no reserved words (anthropic, claude)
- [ ] `description` field present and non-empty
- [ ] `description` ≤1024 characters
- [ ] `description` contains no XML tags
- [ ] `description` uses third person (not "I can..." or "You can...")

## Description Quality

- [ ] Describes what the skill does
- [ ] Includes when/triggers for activation
- [ ] Contains key terms users would mention
- [ ] Specific enough to distinguish from other skills
- [ ] Not vague ("helps with", "processes", "does stuff")

## Content Efficiency

- [ ] SKILL.md body <500 lines
- [ ] No explanations of concepts Claude already knows
- [ ] Prefers concise code examples over verbose explanations
- [ ] Each section justifies its token cost
- [ ] No redundant information between SKILL.md and reference files

## Progressive Disclosure

- [ ] Large content (>100 lines) split into reference files
- [ ] Reference files have clear pointers in SKILL.md
- [ ] SKILL.md describes when to read each reference
- [ ] Reference files >100 lines have table of contents
- [ ] References are one level deep (no A→B→C chains)

## Organization

- [ ] No unnecessary files (README, CHANGELOG, INSTALLATION_GUIDE)
- [ ] Clear directory structure (scripts/, references/, assets/)
- [ ] Domain-specific content organized by domain
- [ ] File names are descriptive (not doc2.md, file1.md)

## Content Quality

- [ ] Consistent terminology throughout
- [ ] No time-sensitive information (or in "old patterns" section)
- [ ] No Windows-style paths (backslashes)
- [ ] Examples are concrete, not abstract
- [ ] Templates match strictness requirements

## Workflow Clarity

- [ ] Multi-step processes have clear sequential steps
- [ ] Decision points have conditional guidance
- [ ] Validation steps precede irreversible actions
- [ ] Provides single recommended approach (not multiple equivalent options)
