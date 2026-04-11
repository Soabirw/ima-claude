# ima-claude

FP patterns, architecture guidance, and team standards for AI coding agents.

**Supports Claude Code, Junie CLI, Gemini CLI, and GitHub Copilot** — with an extensible adapter architecture ready for more platforms.

Built by [Independent Medical Alliance](https://imahealth.org) (formerly FLCCC)

**Core Philosophy: `Simple > Complex | Evidence > Assumptions`**

> These skills are built for IMA's team context — but most of the patterns (FP principles, architecture guidance, hooks, MCP integration, memory system) are general enough to be useful to anyone. If you're building your own AI coding toolkit, this repo can serve as a reference for structure, conventions, and what's possible. Fork it, strip the IMA-specific skills, and build your own.

## Install

### Claude Code — Plugin System (Recommended)

Inside Claude Code, run:

```
/plugin marketplace add https://github.com/Soabirw/ima-claude
/plugin install ima-claude
```

Then **restart Claude Code** to load the plugin. Verify with:

```
/quickstart
```

Skills are namespaced (`/ima-claude:task-master`, `/ima-claude:quickstart`, etc.) and isolated from other plugins.

**Upgrade:**

```
claude plugin marketplace update ima-claude
claude plugin update ima-claude
```

Or use `/plugin` inside Claude Code to manage updates interactively via the **Installed** tab.

### Junie CLI / Gemini CLI / GitHub Copilot — Multi-Platform Installer

For Junie, Gemini, GitHub Copilot, or any non-plugin platform, use the interactive CLI installer:

```bash
npx ima-claude install
```

The installer auto-detects which platforms are available and walks you through installation:

1. **Detects platforms** — scans for Claude Code (`~/.claude`), Junie CLI (`~/.junie`), Gemini CLI (`~/.gemini`), and GitHub Copilot (`~/.copilot`)
2. **Shows preview** — lists all skills, agents, and platform-specific items to install
3. **Allows exclusions** — skip specific skills or agents you don't need
4. **Installs with feedback** — step-by-step progress for each item

You can also target a specific platform directly:

```bash
npx ima-claude install --target junie       # Junie only
npx ima-claude install --target gemini      # Gemini CLI only
npx ima-claude install --target gh-copilot  # GitHub Copilot only
npx ima-claude install --target claude      # Claude Code only (plugin recommended instead)
npx ima-claude detect                       # Show detected platforms
```

**What's different per platform?**

| | Claude Code | Junie CLI | Gemini CLI | GitHub Copilot |
|---|---|---|---|---|
| **Skills** | Plugin system (auto) | Copied to `~/.junie/skills/` | Copied to `~/.gemini/skills/` | Copied to `~/.copilot/skills/` |
| **Agents** | Plugin system (auto) | Strips `permissionMode` | Strips `model` + `permissionMode`, maps tool names | Strips `model` + `permissionMode`, maps tool names, renames to `.agent.md` |
| **Hooks** | 24 Python hook scripts | No hook system — behavioral guidelines | Translated events + tool names, translator shim | Translated events + tool names, translator shim, flattened config |
| **Guidelines** | Plugin's `CLAUDE.md` injection | Generated `AGENTS.md` | Generated `GEMINI.md` | Generated `copilot-instructions.md` |

Junie doesn't support hooks, so behaviors become guidelines in `AGENTS.md`. Gemini and GitHub Copilot have hooks but use different event/tool names — a translator shim normalizes input so all existing hooks work unmodified. Copilot additionally uses a flat hook config format with `bash` field and `version: 1` wrapper.

### Adding New Platforms

The installer uses an adapter pattern. Adding support for a new platform means creating one file implementing the `PlatformAdapter` interface:

```
platforms/
├── shared/types.ts          # PlatformAdapter interface
├── claude/adapter.ts        # Claude Code adapter
├── junie/adapter.ts         # Junie CLI adapter
├── gemini/adapter.ts        # Gemini CLI adapter
└── gh-copilot/adapter.ts    # GitHub Copilot adapter
```

See [platforms/shared/types.ts](platforms/shared/types.ts) for the interface contract.

---

## What's Included

- **Multi-Platform Installer**: Interactive CLI with auto-detection, install preview, and per-item exclusion — supports Claude Code, Junie CLI, Gemini CLI, and GitHub Copilot
- **49 Skills**: Foundational + FP implementation + domain expert + integration + meta-skills
- **6 Named Agents**: Explorer (haiku), Implementer (sonnet), Reviewer (sonnet), Tester (sonnet), WP Developer (sonnet), Memory (sonnet) — enforced constraints
- **23 Hooks**: Automatic behavioral enforcement (security, memory, workflow, Serena, code quality) — translated to guidelines for platforms without hook support
- **Default Persona**: "The Practitioner" - 25-year veteran mindset, collaborative, plan-first
- **3-Tier Memory**: Vestige (neural decay) + Qdrant (permanent library) + Serena (project workbench)
- **IMA Workflow**: Brainstorm → Plan → Implement → Test → Review → Document (habit-driven, not tool-enforced)
- **Session Management**: MCP-based save/resume via Serena (no file path confusion)
- **Meta-skills**: Create and analyze skills
- **Personalities**: Token-efficient modes (efficient, terse) + themed fun (40K, Templars)

## Prerequisites

- [Claude Code](https://claude.ai/code), [Junie CLI](https://www.jetbrains.com/help/idea/junie.html), [Gemini CLI](https://github.com/google-gemini/gemini-cli), or [GitHub Copilot](https://github.com/features/copilot) installed

## MCP Servers (Highly Recommended)

ima-claude includes helper skills for these MCP servers. Install any that fit your workflow:

### Core MCP Servers

| MCP Server | Purpose | Setup |
|------------|---------|-------|
| **[Serena](https://github.com/oraios/serena)** | Code symbol operations, refactoring, session memory | JetBrains IDE + Serena plugin |
| **[Vestige](https://github.com/samvallad33/vestige)** | Cognitive memory engine (preferences, decisions, patterns) | Cargo or binary install |
| **[ima-qdrant-mcp-server](https://github.com/Soabirw/ima-qdrant-mcp-server)** | Permanent library (standards, PRDs, architecture, code samples) | [Docker](https://github.com/qdrant/qdrant) + Ollama + pip |
| **[Tavily](https://docs.tavily.com/documentation/mcp)** | Web research and current information | API key ([tavily.com](https://tavily.com)) |
| **[Context7](https://github.com/upstash/context7)** | Official library documentation lookup | npx |
| **[Sequential Thinking](https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking)** | Structured reasoning for complex problems | npx |

### Optional MCP Servers

| MCP Server | Purpose | Setup |
|------------|---------|-------|
| **[Memory](https://github.com/modelcontextprotocol/servers/tree/main/src/memory)** | Basic knowledge graph memory (deprecated by Vestige) | npx |
| **Fetch** | Web page content extraction | uvx |
| **Chrome DevTools** | Browser debugging capabilities | npx |

> **Recommended minimum**: Serena + Vestige + Context7 + Tavily. These four cover code ops, memory, docs, and web research.

### Marketplace Plugin (Optional)

| Plugin | Purpose | Install |
|--------|---------|---------|
| **[Compound Engineering](https://every.to/guides/compound-engineering)** | Structured workflows with 15 specialized review agents, brainstorm workflows, and research agents. | Claude Code marketplace |

> **Honorable mention**: Compound Engineering and [SuperClaude](https://github.com/SuperClaude-Org/SuperClaude_Framework) both inspired ima-claude's workflow thinking. They're excellent starting points if you don't have established workflows yet. ima-claude takes the same principles and specializes them for IMA's team context — habit-driven rather than tool-enforced.

The `compound-bridge` skill provides optional integration with Compound Engineering for teams that use both. **Only install Compound Engineering if your team actively uses it** — `compound-bridge` is a no-op without it.

### Installation Commands

> **Tip**: Many of these are available directly in the Claude Code marketplace (`/marketplace` or Settings → Marketplace). The commands below are for manual/CLI installs.

```bash
# Serena (requires JetBrains IDE running with Serena plugin)
# See: https://github.com/oraios/serena
claude mcp add --scope user serena -- uvx --from git+https://github.com/oraios/serena \
  serena start-mcp-server --context=claude-code --language-backend JetBrains --project-from-cwd

# Vestige (cognitive memory)
cargo install vestige-mcp
claude mcp add --scope user vestige -- vestige-mcp

# Qdrant (document RAG) — uses ima-qdrant-mcp-server (NOT the official mcp-server-qdrant)
# See: https://github.com/Soabirw/ima-qdrant-mcp-server
docker run -d --restart unless-stopped --name qdrant -p 6333:6333 -v qdrant_storage:/qdrant/storage qdrant/qdrant:latest
ollama pull nomic-embed-text
pip install -e ~/dev/qdrant-mcp-server  # or wherever you cloned it
claude mcp add --transport stdio --scope user qdrant-memory \
  --env QDRANT_URL="http://localhost:6333" \
  --env COLLECTION_NAME="ima-knowledge" \
  -- qdrant-mcp

# Tavily (requires API key from https://tavily.com)
claude mcp add --scope user tavily -e TAVILY_API_KEY=your-key -- npx -y tavily-mcp@latest

# Context7
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp@latest

# Sequential Thinking
claude mcp add --scope user sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking@latest

# Memory (basic knowledge graph — deprecated by Vestige)
claude mcp add --scope user memory -- npx -y @modelcontextprotocol/server-memory@latest

# Fetch
claude mcp add --scope user fetch -- uvx mcp-server-fetch

# Chrome DevTools
claude mcp add --scope user chrome-devtools -- npx -y chrome-devtools-mcp@latest
```

Verify installation:
```bash
claude mcp list
```

### MCP Skills

ima-claude includes skills that teach Claude how to use each MCP server effectively:

| Skill | Purpose |
|-------|---------|
| **mcp-vestige** | Cognitive memory: semantic search, spaced repetition, proactive storage |
| **mcp-qdrant** | Permanent library: standards, PRDs, architecture, code samples |
| **mcp-serena** | Code symbol operations, refactoring, semantic analysis |
| **mcp-tavily** | Web research patterns and query optimization |
| **mcp-context7** | Library documentation lookup strategies |
| **mcp-sequential** | Structured reasoning workflows |
| **mcp-atlassian** | Jira & Confluence operations (Claude's bundled integration) |
| **mcp-gitea** | Internal Git management: PRs, issues, releases, branches, tags, wikis, CI/CD actions |
| **mcp-github** | FOSS/public repo management: PRs, issues, code review, repo search (`gh` CLI fallback) |
| **gh-cli** | GitHub CLI (`gh`) for PRs, issues, releases, Actions, code review, search, and raw API access |
| ~~**compound-bridge**~~ | Compound Engineering integration — **deprecated**, only useful if your team actively uses Compound Engineering |

### Session Management Skills

| Skill | Purpose |
|-------|---------|
| **save-session** | Save session state to Serena MCP memory |
| **resume-session** | Resume previous session from Serena MCP memory |

> **Requires Serena MCP** for cross-session persistence.

These skills auto-activate based on context.

## Tips

> **Tip:** When using `task-runner` to spawn multiple agents, sub-agents may get stuck waiting for permission prompts. Use `--dangerously-skip-permissions` to let agents run autonomously:
>
> ```bash
> claude --dangerously-skip-permissions
> ```
>
> **Use with care** — this skips all permission checks. Best for local development on trusted codebases.

## IMA Workflow

Our development workflow is habit-driven, not tool-enforced. No plugins required — just good practice.

| Step | Where | What |
|------|-------|------|
| **1. Brainstorm** | Claude Web Project spaces | Initial ideation, flush out early concepts into viable plans. Project spaces give Claude rich context without cluttering Code sessions. |
| **2. Plan** | Claude Code — Plan Mode | Enter Plan Mode with the finalized concept. Claude Code knows the specific project and codebase. Produce a concrete implementation plan. |
| **3. Implement** | Claude Code — `task-planner` → `task-runner` | Break the plan into tasks (`task-planner`), then delegate to agents (`task-runner`). Each agent gets relevant skills and the right model. |
| **4. Test** | Claude Code + browser/manual | Unit tests for logic. Human testing for UX and edge cases. |
| **5. Review** | Fresh Claude Code terminal | Run `/scorecard` and targeted reviews. Findings may cycle back to step 3, 4, or even step 2 if significant. |
| **6. Document** | Confluence, Jira, Qdrant, Serena, Vestige | Update everything. This is what makes the system smarter over time. |

> **Why habit over tools?** Enforced workflows create overhead. When the habits are genuinely useful, they stick naturally. When they don't fit the task, skip a step — no tool will argue.

## Available Agents

Named subagents with hard constraints — model, tools, and permissions enforced at runtime, not just by prompt. Skills are pre-loaded at startup. The orchestrator (`task-runner`) delegates to these automatically.

| Agent | Model | Mode | Pre-loaded Skills | Use For |
|-------|-------|------|-------------------|---------|
| `ima-claude:explorer` | haiku | read-only | `mcp-serena` | File discovery, architecture understanding, code search |
| `ima-claude:implementer` | sonnet | full access | `functional-programmer`, `mcp-serena` | Feature dev, bug fixes, refactoring, tests |
| `ima-claude:reviewer` | sonnet | read-only | `functional-programmer`, `mcp-serena` | Code review, security audit, FP compliance |
| `ima-claude:tester` | sonnet | full access | `unit-testing`, `functional-programmer`, `mcp-serena` | Test creation, TDD, test running, debugging failures |
| `ima-claude:wp-developer` | sonnet | full access | `php-fp`, `php-fp-wordpress`, `wp-ddev`, `wp-local`, `ima-forms-expert`, `ima-bootstrap`, `jquery`, `mcp-serena` | WordPress plugins, themes, WP-CLI, forms |
| `ima-claude:memory` | sonnet | full access | `mcp-vestige`, `mcp-qdrant`, `mcp-serena` | Memory search, storage, consolidation across Vestige/Qdrant/Serena |

Agents are auto-discovered from `plugins/ima-claude/agents/`. No manifest changes needed to add new ones.

## Available Skills

### Foundational Skills

| Skill | Description |
|-------|-------------|
| `functional-programmer` | FP principles and philosophy (no code - concepts only) |
| `task-master` | Orchestration umbrella — dispatches to task-planner and task-runner |
| `task-planner` | Decomposition: Epic > Story > Task hierarchy, storage strategy |
| `task-runner` | Delegation: model selection, skill assignment, agent execution |

### FP Implementation Skills

| Skill | Description |
|-------|-------------|
| `js-fp` | JavaScript FP core - anti-over-engineering, native patterns |
| `js-fp-api` | Node.js API patterns with security-first SQL |
| `js-fp-react` | React FP patterns with hooks and HOCs |
| `js-fp-vue` | Vue 3 FP patterns with composables |
| `js-fp-wordpress` | WordPress JS patterns for Bootstrap/jQuery |
| `jquery` | jQuery patterns and API reference (WordPress-native) |
| `php-fp` | PHP FP core principles |
| `php-fp-wordpress` | Security-first WordPress PHP development |
| `py-fp` | Python FP core - comprehensions, generators, frozen dataclasses |
| `quasar-fp` | Quasar Framework with utility-first CSS |

### CRM Skills

| Skill | Description |
|-------|-------------|
| `espocrm` | EspoCRM skill family router (intent detection, Salesforce mapping, child skill routing) |
| `espocrm-api` | EspoCRM v9.x REST API (auth, CRUD, WHERE filtering, relationships, webhooks, mass ops) |

### Domain Expert Skills

| Skill | Description |
|-------|-------------|
| `architect` | System design expertise and principles |
| `ima-brand` | IMA Brand Book v4.0 (identity, voice, logo, content) |
| `ima-bootstrap` | Bootstrap 5.3 + IMA brand (utility-first CSS, SCSS) |
| `playwright` | E2E testing with Playwright + TypeScript |
| `docs-organize` | Three-tier documentation organization |
| `wp-ddev` | WP-CLI commands for DDEV WordPress environments |
| `wp-local` | WP-CLI commands for Flywheel Local WP |
| `jira-checkpoint` | Jira awareness checkpoints for team visibility |
| `phpunit-wp` | PHPUnit testing for WordPress plugins with FP principles |
| `rg` | Ripgrep usage patterns |
| `ima-forms-expert` | WordPress form components (IMA Forms) |
| `discourse-admin` | Discourse admin API (site settings, config export/import, groups) |
| `design-to-code` | Convert design screenshots → implementation prompt → working WordPress code (two-phase workflow) |
| `ima-cancer-care-guides` | Cancer care guide document pipeline (DOCX → markdown → HTML → PDF, Canva mapping) |
| `ima-copywriting` | IMA editorial voice across all formats (newsletters, blogs, press releases, fundraising, social) |
| `ima-editorial-scorecard` | Score IMA content against editorial standards (Brand Voice, Evidence, Audience, Structure, CTA) |
| `ima-editorial-workflow` | Orchestrates Plan → Write → Review → Approve → Learn editorial process |
| `ima-email-creator` | Render branded email-client-safe HTML (table layouts, inline CSS, EspoCRM compatibility) |
| `prompt-starter` | Zero-friction prompt templates (quick, brainstorm, plan-implement) with Jira pre-fill and editor spawn |

### Agentic Workflow Skills

| Skill | Description |
|-------|-------------|
| `agentic-workflows` | Headless workflow phases, recipes, and standards for Jira-triggered content creation (gather → outline → draft → review → deliver) |

### Integration Skills

| Skill | Description |
|-------|-------------|
| `compound-bridge` | Compound Engineering integration (memory bridge, role separation) |
| `mcp-vestige` | Cognitive memory: preferences, decisions, patterns |
| `mcp-qdrant` | Permanent library: standards, PRDs, architecture, code samples |
| `mcp-serena` | Code symbol operations, refactoring, semantic analysis |
| `mcp-atlassian` | Jira & Confluence operations |
| `mcp-tavily` | Web research and query optimization |
| `mcp-context7` | Library documentation lookup strategies |
| `mcp-sequential` | Structured reasoning workflows |
| ~~`mcp-memory`~~ | **Deprecated** — replaced by `mcp-vestige` |

### Meta Skills

| Skill | Description |
|-------|-------------|
| `skill-analyzer` | Analyze and improve existing skills |
| `skill-creator` | Create new skills following best practices |

## How Skills Work

Skills are automatically discovered by Claude Code. Simply mention the skill's domain:

```
"Help me implement this React component following FP patterns"
# → js-fp-react skill auto-activates

"Design a scalable API for user authentication"
# → js-fp-api skill auto-activates

"Create a WordPress plugin for forms"
# → php-fp-wordpress skill auto-activates
```

Or explicitly request a skill:

```
"Use the js-fp skill to review this code"
```

## Hooks (23 Behavioral Hooks)

Hooks enforce skill behaviors automatically — Claude can't skip them. All hooks are soft warnings (exit 0) that guide without blocking.

| Category | Hooks | What They Enforce |
|----------|-------|-------------------|
| **Tool Redirection** | `enforce_rg_over_grep`, `webfetch_to_tavily`, `websearch_to_tavily`, `tavily_extract_advanced` | Use preferred tools (rg over grep, Tavily over WebFetch/WebSearch) |
| **Memory System** | `memory_bootstrap`, `memory_store_reminder`, `vestige_before_external` | Search Vestige/Qdrant at session start; store after edits; check memory before external lookups |
| **Workflow** | `task_master_after_plan`, `task_master_before_impl`, `jira_issue_fetch` | Delegate after planning; task-master before implementation; auto-fetch Jira issues |
| **Security** | `wp_security_check`, `sql_injection_check` | WordPress AJAX security 5-pack + strict_types; SQL injection detection in JS/TS |
| **Atlassian** | `atlassian_prereqs` | cloudId bootstrap, getTransitions before transition, ADF body serialization |
| **Serena** | `serena_project_check`, `serena_over_grep` | WP plugin subdirectory project path fix; prefer Serena symbol tools over Grep for code navigation |
| **Code Quality** | `fp_utility_check`, `jquery_in_wordpress`, `bootstrap_utility_check`, `composer_autoload_check`, `docs_organization` | No custom FP utilities; jQuery in WP; Bootstrap utilities over inline CSS; composer autoload bug; docs organization |
| **Prompt Coaching** | `prompt_coach` | Haiku-powered prompt feedback (experimental) |

See [hooks/README.md](hooks/README.md) for details.

## Prompt Coach (Experimental)

**Haiku-powered prompt feedback system** that analyzes your prompts before they reach Claude, suggesting relevant skills and catching anti-patterns. Stays silent when you're on track, speaks up when it can help.

See [docs/PROMPT_COACH.md](docs/PROMPT_COACH.md) for setup, configuration, and usage.

## Personalities

### Functional (Token-Efficient)

Communication styles that reduce output tokens. Based on research showing brevity constraints improve model accuracy ([arxiv.org/abs/2604.00025](https://arxiv.org/abs/2604.00025)).

| Personality | Style | Target Savings |
|---|---|---|
| **enable-efficient** | Precise, no filler, full sentences (Star Trek Data-like) | ~30-40% |
| **enable-terse** | Blunt fragments, bullets over prose, compressed | ~50-65% |

Both include an **auto-clarity rule** — automatically revert to normal English for security warnings, irreversible operations, or user confusion.

### Flavor (Themed Fun)

Themed response styles that change Claude's tone without affecting expertise:

| Personality | Style |
|---|---|
| **enable-40k** | Warhammer 40K themed code purification |
| **enable-templars** | Templar crusader themed responses |

Usage:
```
"Enable terse mode"
"Enable 40k mode and review this code"
"Return to normal mode"
```

## Projects (Manual Setup)

Example research projects for **Claude Web Projects** and **Claude Code**. These are not part of the automated install—use them manually or as templates for building your own domain-specific assistants.

| Project | Description |
|---------|-------------|
| `patristic-researcher` | Early Church Fathers research (~30-430 AD) |
| `mecha-thomas` | Thomistic research with Chestertonian voice |
| `mecha-alphonsus` | Marian theology in St. Alphonsus' style |

**Usage:**
```bash
# Claude Code: Launch from project directory
cd ~/dev/ima-claude/projects/patristic-researcher
claude

# Claude Web: Copy instructions.md, upload files/ to Project Knowledge
```

See [projects/README.md](projects/README.md) for setup guide and instructions for building your own projects.

## Token Efficiency

All skills, agents, and instruction files are written for LLM consumption, not human reading. A systematic optimization pass reduced the skill corpus by **35% (~33,700 tokens)** without losing any functionality.

| Category | Before | After | Saved |
|----------|--------|-------|-------|
| Skills (62) | 70,401 words | 44,990 words | 36% |
| Agents (6) | 1,726 words | 1,451 words | 16% |
| Hooks (3) | 1,109 words | 891 words | 20% |

The writing convention (`.claude/rules/llm-optimized-writing.md`) ensures all future content follows the same rules: imperatives over explanations, tables over prose, drop filler/hedging/pleasantries, one concept per line.

Based on research showing brevity constraints actually improve LLM accuracy: [Brevity Constraints Reverse Performance Hierarchies in Language Models](https://arxiv.org/abs/2604.00025) (March 2026).

**Output token savings** are available via the `enable-efficient` and `enable-terse` personalities (see [Personalities](#personalities)).

## Architecture

ima-claude follows a **Persona + Skills** architecture:

- **Default Persona** - "The Practitioner" provides foundational mindset (FP, composition, plan-first)
- **Skills contain expertise** - Domain knowledge, patterns, implementation guidance
- **Personalities overlay tone** - Fun themes (40K, Templars) without changing expertise
- **MCP integration** - Serena for code ops, Vestige for memory, Qdrant for RAG, Tavily for research
- **Platform adapters** - Shared `PlatformAdapter` interface; each platform implements detect, preview, install, and guideline generation

This makes ima-claude:
1. **Multi-platform** - Same skills and agents across Claude Code, Junie CLI, Gemini CLI, and GitHub Copilot
2. **Fully standalone** - Complete system without dependencies
3. **Consistent** - Same mindset across all interactions
4. **Efficient** - Skills load on-demand based on context
5. **Extensible** - Add your own skills, agents, or platform adapters

## For Teams

### Onboarding

See [docs/ONBOARDING.md](docs/ONBOARDING.md) for team onboarding guide.

### Private Skills

Create project-specific skills in `templates/local-skills/`:

```
~/.claude/skills/
├── js-fp/              # From ima-claude (public)
├── php-fp/             # From ima-claude (public)
└── my-company-api/     # Your private skill
```

Private skills are gitignored and not published.

### Customization

Copy `templates/CLAUDE.md.example` to `~/.claude/CLAUDE.md` and customize:

```markdown
# My Team's Claude Config

@skills/js-fp/SKILL.md
@skills/my-company-api/SKILL.md

## Our Standards
- All code must follow FP patterns from js-fp skill
- Use our company API patterns for backend work
```

## Migration

- **Legacy → Plugin**: See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
- **Old `/fp:*` commands**: See [docs/MIGRATING-FROM-COMMANDS.md](docs/MIGRATING-FROM-COMMANDS.md)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test your changes locally
5. Submit a pull request

## License

MIT - See [LICENSE](LICENSE)
