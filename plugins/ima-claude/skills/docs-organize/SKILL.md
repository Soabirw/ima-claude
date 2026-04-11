---
name: "docs-organize"
description: "Three-tier documentation organization system - Active (permanent) | Archive (historical) | Transient (ephemeral, git-ignored)"
---

# Documentation Organization System

Three-tier structure separating permanent, historical, and ephemeral content.

## Tiers

| Tier | Purpose | Git |
|------|---------|-----|
| **Active** | Current docs used daily | committed |
| **Archive** | Historical reference, completed phases | committed |
| **Transient** | Working docs, spikes, investigation logs | git-ignored |

## Folder Structure

```
docs/
├── README.md                          # Central navigation hub
├── active/
│   ├── README.md
│   ├── architecture/                  # System design, plugins, dependencies
│   ├── development/                   # Testing, code standards, patterns
│   │   └── testing-guides/
│   ├── integrations/                  # Third-party connections
│   │   └── [integration-name]/
│   ├── features/
│   │   └── [feature-name]/
│   ├── operations/                    # Security, troubleshooting, deployment
│   └── reference/                     # Templates, quick commands, standards
├── archive/
│   ├── README.md
│   └── [YYYY-phase-name]/
│       └── README.md                  # Phase summary with outcomes
└── transient/
    ├── .gitignore                     # Excludes *.md (keeps README.md)
    └── README.md
```

## Setup

```bash
mkdir -p docs/{active,archive,transient}
mkdir -p docs/active/{architecture,development,integrations,features,operations,reference}
mkdir -p docs/active/development/testing-guides
echo '*.md
!README.md' > docs/transient/.gitignore
```

Templates: [`templates/docs-README.md`](templates/docs-README.md) · [`templates/active-README.md`](templates/active-README.md) · [`templates/archive-README.md`](templates/archive-README.md) · [`templates/phase-archive-README.md`](templates/phase-archive-README.md) · [`templates/transient-README.md`](templates/transient-README.md) · [`templates/section-README.md`](templates/section-README.md)

## Document Lifecycle

```
TRANSIENT ──▶ ACTIVE ──▶ ARCHIVE
git-ignored    committed   committed
```

**Transient → Active**: planning becomes guide, investigation becomes troubleshooting doc, spike becomes ADR

**Active → Archive**: phase complete, feature deprecated, pattern replaced

**Direct to Archive**: completed work docs, phase summaries, historical reviews

## Theme Categories

| Dir | Content |
|-----|---------|
| `architecture/` | Plugin/module architecture, system design, refactoring roadmaps |
| `development/` | Testing infrastructure, code examples, standards |
| `integrations/` | Third-party APIs, webhooks, auth flows |
| `features/` | Feature docs, user workflows, config options |
| `operations/` | Security, troubleshooting, deployment, monitoring |
| `reference/` | Cheatsheets, templates, brand guidelines, onboarding |

## Quality Gates

1. Correct tier: Active vs. Archive vs. Transient
2. Right subdirectory for content theme
3. README links updated
4. Related docs cross-referenced
5. Naming convention: `UPPER_SNAKE_CASE.md` or `lowercase-kebab/`

## Migration Checklist

- [ ] Create folder structure
- [ ] Create `transient/.gitignore`
- [ ] Create `docs/README.md` navigation hub
- [ ] Create section READMEs in each `active/` subdirectory
- [ ] Move existing docs to correct locations
- [ ] Update project CLAUDE.md/README.md references
- [ ] Verify all internal links
- [ ] Clean up root-level scattered MD files

## Root CLAUDE.md Reference

```markdown
**Key Documentation:**
- [Documentation Index](docs/README.md) - Central hub
- [Testing](docs/active/development/testing-guides/)
- [Architecture](docs/active/architecture/)
```

## Anti-Patterns

- Scattered MD files in project root
- Flat `/docs/` with no theme subdirs
- Subdirectories without README navigation
- Stale transient docs never cleaned up
- Active docs archived prematurely
- Completed phase docs never archived
