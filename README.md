# ima-claude

IMA's Claude Code Skills - FP patterns, architecture guidance, and team standards.

**Core Philosophy: `Simple > Complex | Evidence > Assumptions`**

## What's Included

- **30+ Skills**: Foundational + FP implementation + domain expert + integration + meta-skills
- **Default Persona**: "The Practitioner" - 25-year veteran mindset, collaborative, plan-first
- **MCP Integration**: Skills for Serena, Vestige, Qdrant, Tavily, Context7, Sequential Thinking
- **Compound Engineering**: Bridge skill for Every.to's structured workflows (brainstorm → plan → work → review → compound)
- **Session Management**: MCP-based save/resume via Serena (no file path confusion)
- **Meta-skills**: Create and analyze skills
- **Personalities**: Fun themed response styles (40K, Templars)

## Prerequisites

- [Claude Code](https://claude.ai/code) installed
- [bun](https://bun.sh) - For installation

## MCP Servers (Highly Recommended)

ima-claude includes helper skills for these MCP servers. Install any that fit your workflow:

### Core MCP Servers

| MCP Server | Purpose | Setup |
|------------|---------|-------|
| **Serena** | Code symbol operations, refactoring, session memory | JetBrains IDE + Serena plugin |
| **Vestige** | Cognitive memory engine (preferences, decisions, patterns) | Cargo or binary install |
| **Qdrant** | Document-scale RAG (PRDs, plans, solutions) | Docker |
| **Tavily** | Web research and current information | API key ([tavily.com](https://tavily.com)) |
| **Context7** | Official library documentation lookup | npx |
| **Sequential Thinking** | Structured reasoning for complex problems | npx |

### Optional MCP Servers

| MCP Server | Purpose | Setup |
|------------|---------|-------|
| **Fetch** | Web page content extraction | uvx |
| **Chrome DevTools** | Browser debugging capabilities | npx |

> **Recommended minimum**: Serena + Vestige + Context7 + Tavily. These four cover code ops, memory, docs, and web research.

### Marketplace Plugin (Recommended)

| Plugin | Purpose | Install |
|--------|---------|---------|
| **[Compound Engineering](https://every.to/guides/compound-engineering)** | Structured workflows: brainstorm → plan → work → review → compound. 15 specialized review agents, research agents, brainstorm workflows. | Claude Code marketplace |

The `compound-bridge` skill connects Compound workflows with ima-claude's memory (Vestige/Qdrant) and coding standards.

### Installation Commands

```bash
# Serena (requires JetBrains IDE running with Serena plugin)
# See: https://github.com/Serena-AI/Serena

# Vestige (cognitive memory)
cargo install vestige-mcp
claude mcp add --scope user vestige -- vestige-mcp

# Qdrant (document RAG)
docker run -d --name qdrant -p 6333:6333 -v qdrant_storage:/qdrant/storage qdrant/qdrant:latest
claude mcp add --transport stdio --scope user qdrant-memory \
  --env QDRANT_URL="http://localhost:6333" \
  --env COLLECTION_NAME="ima-knowledge" \
  -- uvx mcp-server-qdrant

# Tavily (requires API key)
claude mcp add --scope user -e TAVILY_API_KEY=your-key -- tavily npx -y tavily-mcp@latest

# Context7
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp@latest

# Sequential Thinking
claude mcp add --scope user sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking@latest

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
| **mcp-qdrant** | Document-scale RAG: PRDs, architecture docs, solutions |
| **mcp-serena** | Code symbol operations, refactoring, semantic analysis |
| **mcp-tavily** | Web research patterns and query optimization |
| **mcp-context7** | Library documentation lookup strategies |
| **mcp-sequential** | Structured reasoning workflows |
| **mcp-atlassian** | Jira & Confluence operations (Claude's bundled integration) |
| **compound-bridge** | Compound Engineering integration (memory bridge, role separation) |

### Session Management Skills

| Skill | Purpose |
|-------|---------|
| **save-session** | Save session state to Serena MCP memory |
| **resume-session** | Resume previous session from Serena MCP memory |

> **Requires Serena MCP** for cross-session persistence.

These skills auto-activate based on context.

## Quick Install

```bash
bunx ima-claude install
```

Or clone and install manually:

```bash
git clone https://github.com/your-org/ima-claude.git
cd ima-claude
bun run scripts/install.ts
```

## Upgrade

```bash
bunx ima-claude upgrade
```

## Tips

> **Tip:** When using `task-master` or Compound Engineering workflows that spawn multiple agents, sub-agents may get stuck waiting for permission prompts. Use `--dangerously-skip-permissions` to let agents run autonomously:
>
> ```bash
> claude --dangerously-skip-permissions
> ```
>
> **Use with care** — this skips all permission checks. Best for local development on trusted codebases.

## Available Skills

### Foundational Skills

| Skill | Description |
|-------|-------------|
| `functional-programmer` | FP principles and philosophy (no code - concepts only) |
| `task-master` | Hierarchical task breakdown, storage strategy, agent delegation |

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

### Integration Skills

| Skill | Description |
|-------|-------------|
| `compound-bridge` | Compound Engineering integration (memory bridge, role separation) |
| `mcp-vestige` | Cognitive memory: preferences, decisions, patterns |
| `mcp-qdrant` | Document-scale RAG: PRDs, plans, solutions |
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

## Hooks (Optional Enhancements)

Pre-tool-use hooks that enhance Claude Code's behavior:

| Hook | Purpose |
|------|---------|
| `enforce_rg_over_grep.py` | Enforces ripgrep over grep/find |
| `tavily_extract_advanced.py` | Auto-upgrades Tavily to advanced mode |
| `webfetch_to_tavily.py` | Redirects WebFetch to Tavily |
| `websearch_to_tavily.py` | Redirects WebSearch to Tavily |

See [hooks/README.md](hooks/README.md) for installation and configuration.

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

If you were using the old `/fp:*` command system, see [docs/MIGRATING-FROM-COMMANDS.md](docs/MIGRATING-FROM-COMMANDS.md).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `bun run scripts/install.ts`
5. Submit a pull request

## License

MIT - See [LICENSE](LICENSE)
