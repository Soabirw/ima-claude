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

Use template: [`templates/docs-README.md`](templates/docs-README.md)

Customize the Quick Navigation table for your project's key files.

### Step 3: Create Active Section README (docs/active/README.md)

Use template: [`templates/active-README.md`](templates/active-README.md)

### Step 4: Create Archive README (docs/archive/README.md)

Use template: [`templates/archive-README.md`](templates/archive-README.md)

For completed phases, use: [`templates/phase-archive-README.md`](templates/phase-archive-README.md)

### Step 5: Create Transient README and .gitignore

- **docs/transient/README.md**: Use [`templates/transient-README.md`](templates/transient-README.md)
- **docs/transient/.gitignore**: Use [`templates/transient-gitignore`](templates/transient-gitignore)

### Step 6: Create Section READMEs

For each `active/` subdirectory, use: [`templates/section-README.md`](templates/section-README.md)

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
