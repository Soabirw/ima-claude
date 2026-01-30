# Changelog

All notable changes to ima-claude will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.0] - 2026-01-30

### Changed - BREAKING

- **Migrated from Airis MCP Gateway to direct MCP servers**
  - Removed Airis Gateway dependency for simpler, more reliable MCP integration
  - Updated all MCP skills to use direct tool patterns (e.g., `mcp__tavily__search` instead of `mcp__airis-mcp-gateway__airis-exec`)
  - Direct servers are faster (no cold start), more reliable (no gateway layer), and easier to configure

### Added

- **Interactive MCP Setup Script** (`scripts/setup-mcp.ts`)
  - Bun-based CLI with interactive prompts for server selection
  - Handles API key input (Tavily)
  - Uses official `claude mcp add` commands (safe, no JSON editing)
  - Option to remove Airis Gateway and stop Docker containers
  - Supports all recommended MCP servers: Tavily, Context7, Memory, Sequential Thinking, Fetch, Chrome DevTools

### Updated

- **MCP Skills** - Complete rewrite for direct server usage
  - `mcp-tavily` - Direct Tavily tools with query optimization patterns
  - `mcp-context7` - Direct Context7 tools with library lookup strategies
  - `mcp-memory` - Direct Memory tools with knowledge graph best practices
  - `mcp-sequential` - Direct Sequential Thinking tools with reasoning workflows
  - Removed all "cold server" workarounds and Airis gateway patterns
  - Cleaner, simpler tool patterns with better documentation

- **Hooks** - Updated for direct MCP tool patterns
  - `tavily_extract_advanced.py` - Now suggests `mcp__tavily__tavily_extract` with extract_depth
  - `webfetch_to_tavily.py` - Updated to suggest direct Tavily extract pattern
  - `websearch_to_tavily.py` - Updated to suggest direct Tavily search pattern
  - All hooks now reference direct MCP tools instead of Airis gateway

- **README.md**
  - Replaced Airis Gateway section with direct MCP server documentation
  - Added manual installation commands for each server
  - Updated skill counts (17 total) and descriptions
  - Added MCP Integration Skills section
  - Updated "What's Included" to highlight MCP integration

### Migration Guide

If you were using Airis Gateway:

1. Run the interactive setup: `bun run scripts/setup-mcp.ts`
2. Select "Remove Airis Gateway" to clean up old configuration
3. Install desired MCP servers (Tavily requires API key from tavily.com)
4. Stop Airis Docker containers when prompted

Or manually:
```bash
# Remove Airis
claude mcp remove airis-mcp-gateway
docker stop airis-mcp-gateway airis-serena airis-mcp-gateway-core

# Install direct servers (see README.md for full commands)
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp@latest
# ... etc
```

Your MCP skills will now use direct tool patterns automatically.

## [1.4.0] - 2026-01-29

### Added

- **Prompt Coach** - Haiku-based prompt evaluation system
  - `UserPromptSubmit` hook evaluates prompts against team standards
  - Suggests relevant skills when missing (e.g., "Consider: mcp-serena")
  - Flags anti-patterns (custom FP utilities, over-engineering, security gaps)
  - Stays silent on good prompts to avoid noise
  - Disabled by default: `export PROMPT_COACH_ENABLED=true` to activate
  - Optional logging: `export PROMPT_COACH_LOG=true`
  - New files: `hooks/prompt_coach.py`, `hooks/prompt_coach_system.md`, `hooks/prompt_coach_digest.md`
  - Documentation: `docs/PROMPT_COACH.md`

### Technical

- Skills digest (~80 lines) provides Haiku with skill context via raw API call
- Pre-filtering skips short prompts (<20 chars) and common follow-ups
- Cost: ~$0.0003 per evaluation (~$0.30 per 1,000 prompts)

## [1.3.1] - 2025-01-29

### Added

- **MCP Skills from testing**: Added skills that were previously only in ~/.claude/skills
  - `mcp-tavily` - Web research via Airis gateway
  - `mcp-context7` - Library documentation lookup
  - `mcp-serena` - Code symbol operations (find references, rename, refactor)

### Fixed

- Correct `PreToolUse` casing in hooks configuration (was `preToolUse`)
- Added all MCP skills to `SKILLS_TO_INSTALL` array

## [1.3.0] - 2025-01-29

### Added

- **New Skills**:
  - `rg` - Ripgrep usage patterns (prefer over grep/find)
  - `mcp-sequential` - Sequential Thinking MCP for complex reasoning
  - `mcp-memory` - Persistent knowledge graph across sessions
- **MCP Integration Skills section** in CLAUDE.md

### Changed

- **Hooks converted to soft warnings** - All hooks now allow commands to proceed while showing helpful suggestions:
  - `enforce_rg_over_grep.py` - Warns on grep/find, suggests rg
  - `websearch_to_tavily.py` - Suggests Tavily search
  - `webfetch_to_tavily.py` - Suggests Tavily extract
  - `tavily_extract_advanced.py` - Informational about Airis gateway
- Updated Tavily hooks with correct Airis gateway syntax
- Hook warning messages now reference relevant skills

## [1.2.2] - 2025-01-28

### Added

- `ima-forms-expert` skill for WordPress form component library
- `wp-local` skill for Flywheel Local WP environments
- `save-session` and `resume-session` commands

## [1.2.1] - 2025-01-27

### Fixed

- VERSION constant in utils.ts now matches package.json

### Changed

- Reorganized skills with progressive disclosure pattern
- Clarified FP utility rule: don't CREATE custom utilities, but using established libraries is fine

## [1.2.0] - 2025-01-27

### Added

- Auto-install hooks with settings.json configuration
- MCP gateway guide documentation
- Backup utility script
- Projects directory for Claude Web/Code research assistants

### Fixed

- Handle read-only files during installation
- Auto-detect upgrades vs fresh installs

## [1.1.0] - 2025-01-26

### Added

- Hook system for tool interception:
  - `enforce_rg_over_grep.py` - Enforce ripgrep over grep
  - `websearch_to_tavily.py` - Redirect to Tavily search
  - `webfetch_to_tavily.py` - Redirect to Tavily extract
  - `tavily_extract_advanced.py` - Auto-upgrade Tavily extract

## [1.0.0] - 2025-01-26

### Added

- **Skills-first Architecture**: Complete migration from commands to skills
- **FP Skills**:
  - `js-fp` - JavaScript FP core with anti-over-engineering focus
  - `js-fp-api` - Node.js API patterns with security-first SQL
  - `js-fp-react` - React FP patterns with hooks and HOCs
  - `js-fp-vue` - Vue 3 FP patterns with composables
  - `js-fp-wordpress` - WordPress JavaScript patterns
  - `php-fp` - PHP FP core principles
  - `php-fp-wordpress` - Security-first WordPress PHP
  - `quasar-fp` - Quasar Framework patterns
- **Domain Expert Skills**:
  - `architect` - System design and architecture guidance
  - `docs-organize` - Three-tier documentation organization
- **Meta Skills**:
  - `skill-analyzer` - Analyze and improve existing skills
  - `skill-creator` - Create new skills following best practices
- **Personalities**: Fun themed response styles (40K, Templars)
- **Installation Scripts**: bun-based install and upgrade
- **Documentation**: Onboarding guide, migration guide, user guide

### Changed

- Separated personality (tone) from skillset (expertise)
- Made SuperClaude optional (works standalone)
- Archived deprecated `/fp:*` commands

### Removed

- SuperClaude dependency (now optional)
- Command-based routing
