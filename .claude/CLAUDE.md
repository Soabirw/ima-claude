# ima-claude Developer Guide

IMA's Claude Code Skills for functional programming, architecture, and team standards.

## Critical: Source of Truth

**This repo is the source.** Skills, hooks, and agents are deployed via the plugin system.

```
Repo Source                              → Deployed By
plugins/ima-claude/skills/               → Plugin system (auto)
plugins/ima-claude/hooks/                → Plugin system (auto)
plugins/ima-claude/hooks/hooks.json      → Plugin system (auto)
plugins/ima-claude/hooks/bootstrap.sh    → SessionStart hook
.claude-plugin/marketplace.json          → Plugin catalog
```

Install: `/plugin marketplace add Soabirw/ima-claude` then `/plugin install ima-claude`

## Commands

```bash
# Plugin mode (recommended)
/plugin marketplace add Soabirw/ima-claude
/plugin install ima-claude
```

## Directory Structure

```
.claude-plugin/
  marketplace.json      # Plugin marketplace catalog
plugins/ima-claude/     # THE PLUGIN (all skills, hooks, agents, personalities)
  .claude-plugin/
    plugin.json         # Plugin manifest
  agents/               # Subagent definitions (YAML frontmatter + system prompt)
  skills/               # Skill source files (SKILL.md + optional references/)
  hooks/                # Python hook scripts (.py) + support files (.md)
    hooks.json          # Plugin hook configuration (${CLAUDE_PLUGIN_ROOT} paths)
    bootstrap.sh        # SessionStart hook
  personalities/        # Fun themed response overlays
templates/              # CLAUDE.md.example, local-skills template
projects/               # Claude Web/Code research project templates
docs/                   # Onboarding, migration, MCP setup, prompt coach
```

## Adding New Content

### New Skill

1. Create `plugins/ima-claude/skills/{name}/SKILL.md` with frontmatter (`name`, `description`)
2. Add entry to the Available Skills section below
3. **Keep skills lean** — large files (examples, sample documents, datasets, binary assets) must not be committed to the repo. Store them on your team's internal shared storage and reference them in the SKILL.md. Only instruction text, small code snippets, and lightweight references belong in the skill directory.

### New Hook

1. Create `plugins/ima-claude/hooks/{name}.py` (exit 0 = soft warning via stderr)
2. Add matcher entry to `plugins/ima-claude/hooks/hooks.json` (PreToolUse, PostToolUse, or UserPromptSubmit)

### New Agent

1. Create `plugins/ima-claude/agents/{name}.md` with YAML frontmatter (`name`, `description`, `model`, optionally `tools`, `permissionMode`, `skills`)
2. The plugin system auto-discovers `agents/` — no manifest changes needed
3. Reference as `ima-claude:{name}` when delegating via the Agent tool
4. Add entry to the Available Agents section below

### Version Bump (Release Checklist)

All version strings must match or the plugin system thinks you're testing locally.
When adding new skills or hooks, the registries and docs must also be updated.

**Version strings** (must all match):

1. `scripts/utils.ts` — `VERSION` constant
2. `package.json` — `version`
3. `plugins/ima-claude/.claude-plugin/plugin.json` — `version`
4. `.claude-plugin/marketplace.json` — plugin `version`

**Registries** (when adding new skills/hooks):

5. `scripts/utils.ts` — `SKILLS_TO_INSTALL` array (new skills)
6. `scripts/utils.ts` — `HOOKS_TO_INSTALL` array (new hooks)

**Documentation** (always update):

7. `CHANGELOG.md` — new version entry
8. `README.md` — skills tables, MCP tables, agent tables as needed
9. `.claude/CLAUDE.md` — Available Skills table

**Counts** (keep accurate):

10. `plugins/ima-claude/.claude-plugin/plugin.json` — `description` field skill/hook counts

## Gotchas

- **Personalities are `.md` files**, not directories like skills. They live flat in `personalities/`.
- **package.json version** drifts from `scripts/utils.ts` VERSION — keep both in sync.
- **Skill frontmatter `description`** is what appears in the skills list sidebar. Keep it under ~200 chars and keyword-rich for auto-discovery.
- **No large or binary files in the repo.** Example documents, sample outputs, datasets, images, fonts, and other bulky assets belong on internal shared storage, not in git. Skills should contain instructions and lightweight references only. This keeps the repo fast to clone and FOSS-friendly.

## Available Agents

Named subagents with enforced constraints (model, tools, permissions, skills). The plugin auto-discovers `agents/` — agents appear as `ima-claude:{name}`.

| Agent | Model | Mode | Skills | Purpose |
|-------|-------|------|--------|---------|
| `explorer` | haiku | read-only (`plan`) | — | File discovery, codebase exploration, architecture understanding |
| `implementer` | sonnet | full access | `functional-programmer` | Feature dev, bug fixes, refactoring, test writing |
| `reviewer` | sonnet | read-only (`plan`) | `functional-programmer` | Code review, security audit, FP compliance |
| `tester` | sonnet | full access | `unit-testing`, `functional-programmer` | Test creation, TDD, test running, debugging test failures |
| `wp-developer` | sonnet | full access | `php-fp`, `php-fp-wordpress`, `wp-local`, `ima-forms-expert`, `ima-bootstrap`, `jquery` | WordPress plugins, themes, WP-CLI, forms, Bootstrap |
| `memory` | sonnet | full access | `mcp-vestige`, `mcp-qdrant`, `mcp-serena` | Memory search, storage, consolidation across Vestige/Qdrant/Serena |

## Available Skills

### Quick Reference
- `quickstart` - Team cheat sheet (common workflows, commands, MCP tools at a glance)
- `scorecard` - Project quality scorecard for README (code standards, security, tests, docs, maintainability)

### Foundational Skills (Complement the Default Persona)
- `functional-programmer` - FP principles and philosophy (triggers on FP discussions)
- `task-master` - Orchestration umbrella: dispatches to task-planner and task-runner (triggers on planning)
  - `task-planner` - Decomposition: Epic > Story > Task hierarchy, storage strategy selection
  - `task-runner` - Delegation: model selection, skill assignment, agent execution

### FP Implementation Skills (Auto-discovered by domain)
- `js-fp` - JavaScript FP core (anti-over-engineering, native patterns)
- `js-fp-api` - Node.js API patterns (security-first SQL, middleware DI)
- `js-fp-react` - React FP patterns (hooks, HOCs, pure components)
- `js-fp-vue` - Vue 3 FP patterns (composables, wrappers)
- `js-fp-wordpress` - WordPress JS (Bootstrap/jQuery, pure business logic)
- `jquery` - jQuery patterns and API reference (FP-aligned, WordPress-native)
- `php-fp` - PHP FP core (strict types, native patterns)
- `php-fp-wordpress` - WordPress PHP (security-first, nonce verification)
- `py-fp` - Python FP core (comprehensions, generators, frozen dataclasses, pandas pipelines)
- `quasar-fp` - Quasar Framework (utility-first CSS, composables)

### Payment & API Skills
- `php-authnet` - Authorize.Net PHP SDK (transactions, CIM profiles, ARB subscriptions, Accept.js, webhooks)

### Testing Skills
- `unit-testing` - Test workflow orchestration (decision tree routing to phpunit-wp, playwright, js-fp, php-fp)

### Domain Expert Skills
- `architect` - System design, scalability, long-term architecture
- `ima-brand` - IMA Brand Book v4.0 (identity, voice, logo rules, content guidelines, audience)
- `ima-bootstrap` - Bootstrap 5.3 + IMA brand (utility-first CSS, components, SCSS)
- `livecanvas` - LiveCanvas page builder with Bootstrap 5, Loops & Logic (Tangible) templating, PicoStrap integration
- `playwright` - E2E testing and QA automation (Playwright + TypeScript, POM, fixtures, mocking)
- `docs-organize` - Three-tier documentation (Active/Archive/Transient)
- `wp-local` - WP-CLI commands in Flywheel Local WP environments
- `jira-checkpoint` - Jira awareness checkpoints for team visibility (before/during/after work sync)
- `rg` - Ripgrep usage patterns (prefer over grep/find)
- `ima-cancer-care-guides` - IMA cancer care guide document pipeline (DOCX extraction, markdown → HTML → PDF, Canva template mapping)

### Integration Skills
- `compound-bridge` - Compound Engineering integration (memory bridge, role separation, per-project config)
- `mcp-atlassian` - Jira & Confluence operations (issues, pages, search, user mentions)
- `mcp-gitea` - Gitea internal Git management (PRs, issues, releases, branches, tags, wikis, CI/CD actions)
- `mcp-github` - GitHub MCP for FOSS/public repos — PRs, issues, code review, repo search (github.com only; use mcp-gitea for internal)
- `gh-cli` - GitHub CLI (`gh`) for PRs, issues, releases, Actions, code review, search, and raw API access (reliable alternative to MCP)
- `mcp-vestige` - Cognitive memory engine (semantic search, spaced repetition, intentions, codebase awareness)
- `mcp-qdrant` - Persistent knowledge base with semantic search (local RAG for docs, plans, solutions)
- `mcp-tavily` - Web research via Tavily (prefer over WebSearch/WebFetch)
- `mcp-context7` - Library documentation lookup
- `mcp-serena` - Code symbol operations (find references, rename, refactor)
- `mcp-sequential` - Structured reasoning for complex problems
- ~~`mcp-memory`~~ - **Deprecated** — replaced by `mcp-vestige`

### Session Management Skills
- `save-session` - Save session state to Serena MCP memory (no file path confusion)
- `resume-session` - Resume previous session from Serena MCP memory

### Meta Skills
- `skill-analyzer` - Analyze and improve skills
- `skill-creator` - Create new skills

## Core Philosophy

**"Simple > Complex | Evidence > Assumptions"**

All skills enforce:
1. **Anti-over-engineering** - Start simple, add complexity only with evidence
2. **Native patterns** - Use language idioms, don't create custom FP utilities (pipe/compose/curry). Using established libraries is fine.
3. **Testability** - Pure functions enable comprehensive testing
4. **Context-appropriate** - CLI script ≠ production service

## Usage

Skills auto-activate based on context. Mention the domain and relevant skills load:

```
"Implement a React component with custom hooks"
# → js-fp-react auto-loads

"Create a WordPress REST API endpoint"
# → php-fp-wordpress auto-loads
```

Or explicitly invoke:

```
"Use the js-fp skill to review this validation logic"
```

## Personalities (Optional)

Fun themed response styles (tone only, no expertise change):

```
"Enable 40k mode"  # Warhammer 40K themed
"Enable templars"  # Templar crusader themed
```
