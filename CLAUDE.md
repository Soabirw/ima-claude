# ima-claude Entry Point

IMA's Claude Code Skills for functional programming, architecture, and team standards.

## Critical: Source of Truth

**This repo is the source. `~/.claude/` is the deployment target. NEVER edit `~/.claude/` directly.**

```
Repo Source                    → Deployed To
skills/                        → ~/.claude/skills/
hooks/                         → ~/.claude/hooks/
IMA_CLAUDE_INIT.md             → ~/.claude/IMA_CLAUDE_INIT.md
.claude/rules/                 → ~/.claude/rules/
```

All changes go in the repo first, then `bun run scripts/install.ts` deploys them. Editing `~/.claude/` directly means the next install overwrites your work.

## Commands

```bash
bun run scripts/install.ts     # Deploy all skills/hooks/rules to ~/.claude/
bun run scripts/upgrade.ts     # Upgrade existing installation
bun run scripts/backup.ts      # Backup current ~/.claude/ state
bunx ima-claude install         # One-liner install (npm)
```

## Directory Structure

```
skills/                 # Skill source files (SKILL.md + optional references/)
hooks/                  # Python hook scripts (.py) + support files (.md)
scripts/                # Install/upgrade/backup tooling (TypeScript)
  utils.ts              # VERSION, SKILLS_TO_INSTALL, HOOKS_TO_INSTALL, HOOKS_CONFIG
  install.ts            # Deployment logic (copies repo → ~/.claude/)
personalities/          # Fun themed response overlays (.md files, not directories)
templates/              # CLAUDE.md.example, local-skills template
projects/               # Claude Web/Code research project templates
docs/                   # Onboarding, migration, MCP setup, prompt coach
.claude/rules/          # Rules files deployed to ~/.claude/rules/
IMA_CLAUDE_INIT.md      # Bootstrap file deployed to ~/.claude/IMA_CLAUDE_INIT.md
commands/               # Legacy (commands moved to skills in v1.6.0)
```

## Key Files

- **`scripts/utils.ts`** — the central registry. Contains `VERSION`, `SKILLS_TO_INSTALL`, `HOOKS_TO_INSTALL`, `HOOKS_CONFIG`, and `RULES_TO_INSTALL`. Any new skill/hook must be registered here.
- **`scripts/install.ts`** — deployment logic. Copies from repo dirs to `~/.claude/` and merges hooks into `~/.claude/settings.json`.
- **`IMA_CLAUDE_INIT.md`** — bootstrap file with persona, memory patterns, orchestrator protocol. Deployed to `~/.claude/`.

## Adding New Content

### New Skill

1. Create `skills/{name}/SKILL.md` with frontmatter (`name`, `description`)
2. Add `"{name}"` to `SKILLS_TO_INSTALL` in `scripts/utils.ts`
3. Add entry to the Available Skills section below
4. Run `bun run scripts/install.ts` to deploy

### New Hook

1. Create `hooks/{name}.py` (exit 0 = soft warning via stderr)
2. Add `"{name}.py"` to `HOOKS_TO_INSTALL` in `scripts/utils.ts`
3. Add matcher entry to `HOOKS_CONFIG` in `scripts/utils.ts` (PreToolUse, PostToolUse, or UserPromptSubmit)
4. Run `bun run scripts/install.ts` to deploy

### Version Bump

1. Update `VERSION` in `scripts/utils.ts`
2. Update `version` in `package.json`
3. Add entry to `CHANGELOG.md`

## Gotchas

- **Hooks need two registrations**: `HOOKS_TO_INSTALL` (file copy) AND `HOOKS_CONFIG` (settings.json matcher). Missing either = hook doesn't work.
- **Personalities are `.md` files**, not directories like skills. They live flat in `personalities/`.
- **package.json version** drifts from `scripts/utils.ts` VERSION — keep both in sync.
- **`settings.json` merge** is additive. Removing a hook from `HOOKS_CONFIG` doesn't remove it from a user's existing `settings.json`. Users must manually clean stale entries.
- **Skill frontmatter `description`** is what appears in the skills list sidebar. Keep it under ~200 chars and keyword-rich for auto-discovery.

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
- `quasar-fp` - Quasar Framework (utility-first CSS, composables)

### Payment & API Skills
- `php-authnet` - Authorize.Net PHP SDK (transactions, CIM profiles, ARB subscriptions, Accept.js, webhooks)

### Domain Expert Skills
- `architect` - System design, scalability, long-term architecture
- `ima-brand` - IMA Brand Book v4.0 (identity, voice, logo rules, content guidelines, audience)
- `ima-bootstrap` - Bootstrap 5.3 + IMA brand (utility-first CSS, components, SCSS)
- `playwright` - E2E testing and QA automation (Playwright + TypeScript, POM, fixtures, mocking)
- `docs-organize` - Three-tier documentation (Active/Archive/Transient)
- `wp-local` - WP-CLI commands in Flywheel Local WP environments
- `jira-checkpoint` - Jira awareness checkpoints for team visibility (before/during/after work sync)
- `rg` - Ripgrep usage patterns (prefer over grep/find)

### Integration Skills
- `compound-bridge` - Compound Engineering integration (memory bridge, role separation, per-project config)
- `mcp-atlassian` - Jira & Confluence operations (issues, pages, search, user mentions)
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

## Compound Engineering

The `compound-bridge` skill integrates with the [Compound Engineering](https://every.to/guides/compound-engineering) marketplace plugin. Memory bridges, role separation, and per-project config are documented there. Runtime workflow instructions are in `IMA_CLAUDE_INIT.md`.
