# ima-claude

IMA's Claude Code Skills - FP patterns, architecture guidance, and team standards.

Built by [Independent Medical Alliance](https://imahealth.org) (formerly FLCCC)

**Core Philosophy: `Simple > Complex | Evidence > Assumptions`**

> These skills and hooks are built for IMA's team context — but most of the patterns (FP principles, architecture guidance, hooks design, MCP integration, memory system) are general enough to be useful to anyone. If you're building your own Claude Code toolkit, this repo can serve as a reference for structure, conventions, and what's possible. Fork it, strip the IMA-specific skills, and build your own.

## Install

### Plugin System (Recommended)

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

### Upgrade

```
claude plugin marketplace update ima-claude
claude plugin update ima-claude
```

Or use `/plugin` inside Claude Code to manage updates interactively via the **Installed** tab.

---

## What's Included

- **40+ Skills**: Foundational + FP implementation + domain expert + integration + meta-skills
- **5 Named Agents**: Explorer (haiku), Implementer (sonnet), Reviewer (sonnet), WP Developer (sonnet), Memory (sonnet) — enforced constraints
- **23 Hooks**: Automatic behavioral enforcement (security, memory, workflow, Serena, code quality)
- **Default Persona**: "The Practitioner" - 25-year veteran mindset, collaborative, plan-first
- **3-Tier Memory**: Vestige (neural decay) + Qdrant (permanent library) + Serena (project workbench)
- **IMA Workflow**: Brainstorm → Plan → Implement → Test → Review → Document (habit-driven, not tool-enforced)
- **Session Management**: MCP-based save/resume via Serena (no file path confusion)
- **Meta-skills**: Create and analyze skills
- **Personalities**: Fun themed response styles (40K, Templars)

## Prerequisites

- [Claude Code](https://claude.ai/code) installed

## MCP Servers (Highly Recommended)

ima-claude includes helper skills for these MCP servers. Install any that fit your workflow:

### Core MCP Servers

| MCP Server | Purpose | Setup |
|------------|---------|-------|
| **[Serena](https://github.com/oraios/serena)** | Code symbol operations, refactoring, session memory | JetBrains IDE + Serena plugin |
| **[Vestige](https://github.com/samvallad33/vestige)** | Cognitive memory engine (preferences, decisions, patterns) | Cargo or binary install |
| **[Qdrant MCP](https://github.com/qdrant/mcp-server-qdrant)** | Permanent library (standards, PRDs, architecture, code samples) | [Docker](https://github.com/qdrant/qdrant) + uvx |
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

# Qdrant (document RAG)
docker run -d --name qdrant -p 6333:6333 -v qdrant_storage:/qdrant/storage qdrant/qdrant:latest
claude mcp add --transport stdio --scope user qdrant-memory \
  --env QDRANT_URL="http://localhost:6333" \
  --env COLLECTION_NAME="ima-knowledge" \
  -- uvx mcp-server-qdrant

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
| `ima-claude:explorer` | haiku | read-only | — | File discovery, architecture understanding, code search |
| `ima-claude:implementer` | sonnet | full access | `functional-programmer` | Feature dev, bug fixes, refactoring, tests |
| `ima-claude:reviewer` | sonnet | read-only | `functional-programmer` | Code review, security audit, FP compliance |
| `ima-claude:wp-developer` | sonnet | full access | `php-fp`, `php-fp-wordpress`, `wp-local`, `ima-forms-expert`, `ima-bootstrap`, `jquery` | WordPress plugins, themes, WP-CLI, forms |
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
| `quasar-fp` | Quasar Framework with utility-first CSS |

### Domain Expert Skills

| Skill | Description |
|-------|-------------|
| `architect` | System design expertise and principles |
| `ima-brand` | IMA Brand Book v4.0 (identity, voice, logo, content) |
| `ima-bootstrap` | Bootstrap 5.3 + IMA brand (utility-first CSS, SCSS) |
| `playwright` | E2E testing with Playwright + TypeScript |
| `docs-organize` | Three-tier documentation organization |
| `wp-local` | WP-CLI commands for Flywheel Local WP |
| `jira-checkpoint` | Jira awareness checkpoints for team visibility |
| `phpunit-wp` | PHPUnit testing for WordPress plugins with FP principles |
| `rg` | Ripgrep usage patterns |
| `ima-forms-expert` | WordPress form components (IMA Forms) |
| `discourse-admin` | Discourse admin API (site settings, config export/import, groups) |

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

## Hooks (21 Behavioral Hooks)

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

## Personalities (Optional Fun)

Themed response styles that change Claude's tone without affecting expertise:

- **enable-40k**: Warhammer 40K themed code purification
- **enable-templars**: Templar crusader themed responses

Usage:
```
"Enable 40k mode and review this code"
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

## Architecture

ima-claude follows a **Persona + Skills** architecture:

- **Default Persona** - "The Practitioner" provides foundational mindset (FP, composition, plan-first)
- **Skills contain expertise** - Domain knowledge, patterns, implementation guidance
- **Personalities overlay tone** - Fun themes (40K, Templars) without changing expertise
- **MCP integration** - Serena for code ops, Vestige for memory, Qdrant for RAG, Tavily for research

This makes ima-claude:
1. **Fully standalone** - Complete system without dependencies
2. **Consistent** - Same mindset across all interactions
3. **Efficient** - Skills load on-demand based on context
4. **Extensible** - Add your own skills in `~/.claude/skills/`

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
