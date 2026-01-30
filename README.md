# ima-claude

IMA's Claude Code Skills - FP patterns, architecture guidance, and team standards.

## What's Included

- **17 Skills**: FP patterns for JS, PHP, React, Vue, Quasar, WordPress + MCP helpers
- **Architecture guidance**: System design principles
- **MCP Integration**: Setup script + skills for Tavily, Context7, Memory, Sequential Thinking
- **Meta-skills**: Create and analyze skills
- **Personalities**: Fun themed response styles (40K, Templars)

## Prerequisites

- [Claude Code](https://claude.ai/code) installed
- [bun](https://bun.sh) - For installation

## Optional (Recommended)

- [SuperClaude](https://github.com/SuperClaude-Org/SuperClaude_Framework) - Enhanced commands & personas

ima-claude works completely standalone, but integrates beautifully with SuperClaude for additional features like personas, commands, and MCP orchestration.

## MCP Servers (Highly Recommended)

ima-claude includes helper skills and an interactive setup script for essential MCP servers:

| MCP Server | Purpose | Requires API Key |
|------------|---------|------------------|
| **Tavily** | Web research and current information | ✓ Yes ([tavily.com](https://tavily.com)) |
| **Context7** | Official library documentation lookup | ✗ No |
| **Memory** | Persistent knowledge graph across sessions | ✗ No |
| **Sequential Thinking** | Structured reasoning for complex problems | ✗ No |
| **Fetch** | Web page content extraction | ✗ No |
| **Chrome DevTools** | Browser debugging capabilities | ✗ No |

### Interactive Setup

```bash
bun run scripts/setup-mcp.ts
```

The interactive script will:
- Show currently installed MCP servers
- Let you select which servers to install
- Handle API key input (Tavily)
- Configure servers using official `claude mcp add` commands
- Optionally remove Airis Gateway if installed

### Manual Installation

Install individual servers:

```bash
# Tavily (requires API key)
claude mcp add --scope user -e TAVILY_API_KEY=your-key -- tavily npx -y tavily-mcp@latest

# Context7
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp@latest

# Memory
claude mcp add --scope user memory -- npx -y @modelcontextprotocol/server-memory@latest

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

ima-claude includes skills that help you use MCP servers effectively:

- **mcp-tavily** - Web research patterns and query optimization
- **mcp-context7** - Library documentation lookup strategies
- **mcp-memory** - Knowledge graph best practices
- **mcp-sequential** - Structured reasoning workflows

These skills auto-activate when you use the MCP tools.

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

## Available Skills

### FP Domain Skills

| Skill | Description |
|-------|-------------|
| `js-fp` | JavaScript FP core - anti-over-engineering, native patterns |
| `js-fp-api` | Node.js API patterns with security-first SQL |
| `js-fp-react` | React FP patterns with hooks and HOCs |
| `js-fp-vue` | Vue 3 FP patterns with composables |
| `js-fp-wordpress` | WordPress JS patterns for Bootstrap/jQuery |
| `php-fp` | PHP FP core principles |
| `php-fp-wordpress` | Security-first WordPress PHP development |
| `quasar-fp` | Quasar Framework with utility-first CSS |

### Domain Expert Skills

| Skill | Description |
|-------|-------------|
| `architect` | System design expertise and principles |
| `docs-organize` | Three-tier documentation organization |
| `wp-local` | WP-CLI commands for Flywheel Local WP |
| `rg` | Ripgrep usage patterns |
| `ima-forms-expert` | WordPress form components (IMA Forms) |

### MCP Integration Skills

| Skill | Description |
|-------|-------------|
| `mcp-tavily` | Web research and query optimization |
| `mcp-context7` | Library documentation lookup strategies |
| `mcp-memory` | Knowledge graph best practices |
| `mcp-sequential` | Structured reasoning workflows |

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

ima-claude follows a **Skills-first** architecture:

- **Skills contain expertise** - Domain knowledge, patterns, guidance
- **Personalities set tone** - How Claude communicates (fun themes)
- **Commands are deprecated** - Skills replace command-based routing

This makes ima-claude:
1. **Fully independent** - Works without SuperClaude
2. **Efficient** - Only loads what's needed
3. **Maintainable** - Clear separation of concerns

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
