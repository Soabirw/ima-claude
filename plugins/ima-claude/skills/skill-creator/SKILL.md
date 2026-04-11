---
name: skill-creator
description: Guide for creating effective skills that extend Claude's capabilities. Use when users want to create a skill, build a skill, make a skill, design a skill, or update an existing skill. Also triggers for skill template, skill structure, skill format, skill authoring, skill development, or questions about how skills work and how to write them.
license: Complete terms in LICENSE.txt
---

# Skill Creator

## Core Principles

### Concise is Key

Context window is shared. Only add context Claude doesn't already have. Challenge each piece: "Does Claude need this?" and "Does this justify its token cost?" Prefer concise examples over verbose explanations.

### Set Appropriate Degrees of Freedom

| Freedom | When to use |
|---------|-------------|
| High (text instructions) | Multiple valid approaches, context-dependent decisions |
| Medium (pseudocode + params) | Preferred pattern exists, some variation acceptable |
| Low (specific scripts) | Fragile operations, critical consistency, fixed sequence |

### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter: name (required), description (required), compatibility (optional)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/     - Executable code (Python/Bash/etc.)
    ├── references/  - Documentation loaded into context as needed
    └── assets/      - Files used in output (templates, icons, fonts)
```

#### SKILL.md

- **Frontmatter**: `name` and `description` are the only fields Claude reads for triggering. Make `description` comprehensive — "when to use" info belongs here, not in the body (body loads only after triggering).
- **Body**: Instructions and guidance. Loaded after skill triggers.

#### Scripts (`scripts/`)

Include when same code is rewritten repeatedly or deterministic reliability is needed.
- Token efficient, deterministic, may execute without loading into context
- Scripts may still be read for patching or environment-specific adjustments

#### References (`references/`)

Documentation loaded as needed into context to inform Claude's process.
- Use for: database schemas, API docs, domain knowledge, company policies, workflow guides
- Keeps SKILL.md lean. Information lives in either SKILL.md or references — not both.
- If files >10k words, include grep search patterns in SKILL.md
- For files >100 lines, include table of contents so Claude can preview scope

#### Assets (`assets/`)

Files used in output, not loaded into context.
- Use for: templates, images, boilerplate code, fonts, sample documents

#### What Not to Include

No auxiliary documentation: README.md, INSTALLATION_GUIDE.md, QUICK_REFERENCE.md, CHANGELOG.md, etc. Only files that directly support functionality.

### Progressive Disclosure

Three loading levels:
1. **Metadata (name + description)** — always in context (~100 words)
2. **SKILL.md body** — when skill triggers (<5k words, under 500 lines)
3. **Bundled resources** — as needed by Claude

Keep SKILL.md body lean. Reference other files clearly with when-to-read guidance.

**Pattern 1: Guide with references**
```markdown
## Advanced features
- **Form filling**: See [FORMS.md](FORMS.md) for complete guide
- **API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
```

**Pattern 2: Domain-specific organization**
```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md
    ├── sales.md
    └── product.md
```
Claude reads only the relevant domain file.

**Pattern 3: Conditional details**
```markdown
**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

Avoid deeply nested references — keep all reference files one level from SKILL.md.

## Skill Creation Process

1. Understand the skill with concrete examples
2. Plan reusable skill contents (scripts, references, assets)
3. Initialize the skill (`init_skill.py`)
4. Edit the skill (implement resources, write SKILL.md)
5. Package the skill (`package_skill.py`)
6. Iterate based on real usage

### Step 1: Understand with Concrete Examples

Clarify usage patterns before building. Ask:
- "What functionality should this skill support?"
- "Can you give examples of how it would be used?"
- "What would a user say to trigger this skill?"

Avoid multiple questions in one message. Conclude when functionality is clear.

### Step 2: Plan Reusable Contents

Analyze each example:
1. How would you execute this from scratch?
2. What scripts, references, or assets would help when repeating this?

Examples:
- `pdf-editor` → rotate PDF repeatedly → `scripts/rotate_pdf.py`
- `frontend-webapp-builder` → same boilerplate each time → `assets/hello-world/` template
- `big-query` → re-discover schemas each time → `references/schema.md`

### Step 3: Initialize the Skill

Run `init_skill.py` for all new skills:

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

Creates: skill directory, SKILL.md template with frontmatter, example `scripts/`, `references/`, `assets/` dirs.

Skip only if skill already exists and needs iteration or packaging.

### Step 4: Edit the Skill

Write for another Claude instance. Include procedural knowledge, domain details, and reusable assets that would be non-obvious.

**Consult design pattern guides:**
- Multi-step processes → `references/workflows.md`
- Output formats/quality standards → `references/output-patterns.md`

**Start with reusable contents** (scripts, references, assets) before writing SKILL.md. Test scripts by running them. Delete unused example files from initialization.

**Frontmatter rules:**
- `name`: skill name
- `description`: primary trigger mechanism — include what skill does AND when to use it. Put all "when to use" info here.
- No other YAML fields.

**Body writing:** Use imperative/infinitive form ("Use X", not "You should consider using X").

### Step 5: Package

```bash
scripts/package_skill.py <path/to/skill-folder>
# Optional output dir:
scripts/package_skill.py <path/to/skill-folder> ./dist
```

Validates then packages. Validation checks: YAML format, required fields, naming conventions, description quality, file organization. Fix errors and re-run if validation fails.

### Step 6: Iterate

After real usage:
1. Notice struggles or inefficiencies
2. Identify SKILL.md or resource updates needed
3. Implement changes and test again
