---
name: "docs-organize"
description: "Three-tier documentation organization system - Active (permanent) | Archive (historical) | Transient (ephemeral, git-ignored)"
---

# Documentation Organization System

A structured approach to documentation organization that separates permanent, historical, and ephemeral content with clear navigation and lifecycle management.

## When to Use This Skill

- Starting a new project and setting up documentation structure
- Reorganizing existing scattered documentation files
- Need clear separation between active docs and historical reference
- Want local-only working documents that won't clutter git
- Improving documentation discoverability and navigation
- Establishing documentation standards for a team

## Core Philosophy

**Three-Tier Documentation**:
- **Active**: Current, permanent documentation used daily (committed to git)
- **Archive**: Historical reference, completed phases, deprecated patterns (committed to git)
- **Transient**: Ephemeral working documents, investigation logs, spike results (git-ignored)

**Key Principles**:
- **Clear Lifecycle**: Documents flow from transient → active → archive
- **Theme Organization**: Group by function (architecture, development, integrations, features, operations)
- **Navigation First**: README files at every level for discoverability
- **Minimal Clutter**: Root directory stays clean, no scattered MD files

## Folder Structure

```
docs/
├── README.md                          # Central navigation hub
├── active/                            # Current permanent documentation
│   ├── README.md                      # Active docs overview
│   ├── architecture/                  # System design, plugins, dependencies
│   │   └── README.md
│   ├── development/                   # Testing, code standards, patterns
│   │   ├── README.md
│   │   └── testing-guides/            # Phase-specific test suites
│   ├── integrations/                  # Third-party system connections
│   │   ├── README.md
│   │   └── [integration-name]/        # Per-integration documentation
│   ├── features/                      # Feature-specific documentation
│   │   └── [feature-name]/            # Per-feature documentation
│   ├── operations/                    # Security, troubleshooting, deployment
│   │   └── README.md
│   └── reference/                     # Templates, quick commands, standards
│       └── README.md
├── archive/                           # Historical documentation
│   ├── README.md                      # Archive overview & browsing guide
│   └── [YYYY-phase-name]/             # Completed phases/milestones
│       └── README.md                  # Phase summary with outcomes
└── transient/                         # Ephemeral working documents
    ├── .gitignore                     # Excludes *.md from git
    └── README.md                      # Transient usage guide
```

## Implementation Guide

### Step 1: Create Folder Structure

```bash
# Create main structure
mkdir -p docs/{active,archive,transient}

# Create active subdirectories
mkdir -p docs/active/{architecture,development,integrations,features,operations,reference}
mkdir -p docs/active/development/testing-guides

# Create .gitignore for transient
echo '# Exclude all markdown files in transient/
*.md
!README.md' > docs/transient/.gitignore
```

### Step 2: Create Navigation Hub (docs/README.md)

```markdown
# Project Documentation

Central hub for all project documentation.

## 📂 Documentation Structure

### [`active/`](active/README.md) - Current Documentation ⭐
Active, maintained documentation used in daily development.
**All files committed to git.**

- **[architecture/](active/architecture/)** - System design, plugins, dependencies
- **[development/](active/development/)** - Testing, code standards, patterns
- **[integrations/](active/integrations/)** - Third-party integrations
- **[features/](active/features/)** - Feature-specific documentation
- **[operations/](active/operations/)** - Security, troubleshooting, deployment
- **[reference/](active/reference/)** - Templates, quick commands

### [`archive/`](archive/README.md) - Historical Reference 📚
Completed phases, deprecated patterns, historical context.
**Committed to git for reference.**

### [`transient/`](transient/) - Working Documents 🚧
Local-only ephemeral documents for investigation and planning.
**Git-ignored, not committed.**

## Quick Navigation

| Category | Key Files | Purpose |
|----------|-----------|---------|
| Development | [Testing Guide](active/development/testing-guides/) | Test setup and patterns |
| Architecture | [Plugin Layers](active/architecture/PLUGIN_LAYERS.md) | System architecture |
| Operations | [Security](active/operations/SECURITY_GUIDE.md) | Security best practices |

## Documentation Standards

- **Naming**: `UPPER_SNAKE_CASE.md` for documents, `lowercase-kebab/` for folders
- **Cross-References**: Always link to related documentation
- **Last Updated**: Include date at bottom of each document
- **Structure**: Use consistent heading hierarchy (H1 title, H2 sections)

---

**Last Updated**: YYYY-MM-DD
```

### Step 3: Create Active Section README

```markdown
# Active Documentation

Current, maintained documentation for daily development and reference.

## Sections

### [`architecture/`](architecture/)
System design documents, plugin ecosystem, dependencies, refactoring strategy.

### [`development/`](development/)
Testing infrastructure, code examples, development patterns, standards.

### [`integrations/`](integrations/)
Third-party system integration documentation and patterns.

### [`features/`](features/)
Feature-specific documentation organized by feature name.

### [`operations/`](operations/)
Security guides, troubleshooting, deployment procedures.

### [`reference/`](reference/)
Quick reference materials, templates, command cheatsheets.

## Documentation Standards

- **Should be current**: Review quarterly, update when implementation changes
- **Should include examples**: Real code from the codebase
- **Should link to related docs**: Cross-reference architecture, features, operations

## When to Add Here vs. Transient

| Add to Active | Add to Transient |
|---------------|------------------|
| Stable implementation docs | Investigation logs |
| Permanent reference material | Spike/POC results |
| Team knowledge base | Phase planning notes |
| Onboarding materials | Temporary checklists |

---

**Last Updated**: YYYY-MM-DD
```

### Step 4: Create Archive README

```markdown
# Documentation Archive

Historical documentation, completed phases, and deprecated patterns.

## Purpose

This archive serves as:
- **Historical context** for understanding past decisions
- **Learning resource** for patterns that worked (or didn't)
- **Audit trail** for project evolution

## Archive Contents

### Completed Phases
- `YYYY-phase-name/` - Phase completion summary with outcomes

## Archive Naming Convention

```
YYYY-phase-name/           # Completed development phases
YYYY-MM-feature-name/      # Deprecated feature documentation
deprecated-pattern-name/   # Replaced patterns with migration notes
```

## When to Archive

| Archive When | Don't Archive |
|--------------|---------------|
| Phase/milestone complete | Still actively referenced |
| Pattern deprecated with replacement | Needed for current development |
| Historical reference value | No future reference value (delete instead) |

## Browsing Tips

- Start with the phase README for summary
- Look for "What Was Done" and "Lessons Learned" sections
- Check cross-references to current active docs

---

**Last Updated**: YYYY-MM-DD
```

### Step 5: Create Transient README and .gitignore

**docs/transient/README.md:**
```markdown
# Transient Documentation

Ephemeral local-only documents for active planning and investigation.

**⚠️ Files here are git-ignored and will NOT be committed.**

## Purpose

Use transient/ for:
- **Phase planning** before implementation starts
- **Investigation logs** during debugging
- **Spike results** from technical exploration
- **Collaborative notes** during pairing sessions
- **Temporary checklists** for one-time tasks

## Organization Suggestions

```
transient/
├── planning/              # Upcoming phase/feature planning
├── investigations/        # Debug sessions, root cause analysis
├── spikes/               # Technical explorations, POCs
└── notes/                # Miscellaneous working notes
```

## Workflow

### Creating Transient Docs
1. Create file in appropriate subfolder
2. Include date in filename: `YYYY-MM-DD-topic.md`
3. Work locally, iterate freely

### Moving to Active
When a transient doc becomes stable:
1. Clean up content for permanence
2. Move to appropriate `active/` section
3. Delete original transient file
4. Update navigation links

### Cleanup
- Review transient/ monthly
- Delete completed investigation logs
- Archive useful findings to `active/` or `archive/`

## Git Behavior

This folder contains a `.gitignore` that excludes all `*.md` files.

**To force-add a file** (rare, for intentional commits):
```bash
git add -f docs/transient/important-file.md
```

---

**Last Updated**: YYYY-MM-DD
```

**docs/transient/.gitignore:**
```
# Exclude all markdown files in transient/
# These are ephemeral local-only documents
*.md

# Keep this README (force-added)
!README.md

# Keep the .gitignore itself
!.gitignore
```

## Document Lifecycle Workflow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  TRANSIENT  │ ──▶ │   ACTIVE    │ ──▶ │   ARCHIVE   │
│             │     │             │     │             │
│ • Planning  │     │ • Stable    │     │ • Complete  │
│ • Research  │     │ • Reference │     │ • Historical│
│ • Spikes    │     │ • Standards │     │ • Deprecated│
└─────────────┘     └─────────────┘     └─────────────┘
   git-ignored        committed           committed
```

### Lifecycle Triggers

**Transient → Active**:
- Planning becomes implementation guide
- Investigation findings become troubleshooting docs
- Spike results become architecture decisions

**Active → Archive**:
- Phase/milestone completed
- Feature deprecated with replacement
- Pattern replaced with better approach

**Direct to Archive** (skip transient):
- Completed work documentation
- Phase summaries with outcomes
- Historical code reviews

## Theme Categories Reference

### `architecture/`
- Plugin/module architecture
- Dependency management
- System design decisions
- Refactoring roadmaps

### `development/`
- Testing infrastructure (PHPUnit, Jest, etc.)
- Code examples and patterns
- Development standards
- Template patterns

### `integrations/`
- Third-party API connections
- Webhook handling
- Data sync patterns
- Authentication flows

### `features/`
- Feature-specific documentation
- User workflows
- Configuration options
- Feature flags

### `operations/`
- Security best practices
- Troubleshooting guides
- Deployment procedures
- Monitoring setup

### `reference/`
- Quick command cheatsheets
- Template files
- Brand/style guidelines
- Onboarding materials

## Quality Gates

Before adding documentation, verify:

1. ✅ **Correct Location**: Active vs. Archive vs. Transient
2. ✅ **Theme Match**: Right subdirectory for the content
3. ✅ **Navigation Updated**: README links added
4. ✅ **Cross-References**: Related docs linked
5. ✅ **Date Included**: "Last Updated" at bottom
6. ✅ **Naming Convention**: UPPER_SNAKE_CASE.md or lowercase-kebab/

## Migration Checklist

When applying this pattern to existing projects:

- [ ] Create folder structure with `mkdir -p` commands
- [ ] Create `.gitignore` in transient/
- [ ] Create hub README at `docs/README.md`
- [ ] Create section READMEs in each active/ subdirectory
- [ ] Create archive README with naming conventions
- [ ] Create transient README with workflow guidance
- [ ] Move existing documentation to appropriate locations
- [ ] Update project CLAUDE.md/README.md references
- [ ] Verify all internal links work
- [ ] Clean up root-level scattered MD files

## Integration with Project Files

### Update Root CLAUDE.md

Add documentation hub reference:
```markdown
**📚 Key Documentation:**
- **[📖 Documentation Index](docs/README.md)** - Central hub for all documentation
- [Testing Guide](docs/active/development/testing-guides/) - Test setup
- [Architecture](docs/active/architecture/) - System design
```

### Update Navigation References

Change scattered references from:
```markdown
[Testing](TESTING.md)
[Security](docs/SECURITY_GUIDE.md)
```

To centralized structure:
```markdown
[Testing](docs/active/development/testing-guides/TESTING.md)
[Security](docs/active/operations/SECURITY_GUIDE.md)
```

## Success Metrics

Documentation organization is successful when:

- **Discoverability**: New team members find docs within 2 clicks from hub
- **Cleanliness**: Root directory has no scattered MD files
- **Currency**: Active docs are up-to-date with implementation
- **Lifecycle**: Clear workflow from planning to archive
- **Navigation**: README at every level provides guidance

## Anti-Patterns to Avoid

❌ **Scattered root files**: MD files in project root instead of /docs/
❌ **Flat structure**: All docs in single /docs/ folder without themes
❌ **Missing READMEs**: Subdirectories without navigation guides
❌ **Broken links**: References to moved/deleted files
❌ **Stale transient**: Investigation logs never cleaned up
❌ **Over-archiving**: Active docs moved to archive prematurely
❌ **Under-archiving**: Completed phase docs never archived

## Related Patterns

- **CLAUDE.md**: Project-level quick reference (references this structure)
- **ADR (Architecture Decision Records)**: Can live in `active/architecture/adr/`
- **Changelogs**: Can live in `active/reference/CHANGELOG.md`
- **API Documentation**: Can live in `active/reference/api/`

---

**Last Updated**: 2025-01-20
