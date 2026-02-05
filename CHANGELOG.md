# Changelog

All notable changes to ima-claude will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.7.0] - 2026-02-05

### Added

- **Default Persona: The Practitioner** - Foundational operating mode in `IMA_CLAUDE_INIT.md`
  - 25-year veteran mindset: FP journey, composition, anti-over-engineering
  - Collaborative personality: uses "we", humble, light-hearted, loves puns ("LEAN into the KISS")
  - Working style: "Slow is smooth, smooth is fast" - plan before implementing
  - Always active; fun personalities (40k, templars) overlay tone only

- **functional-programmer Skill** - FP principles and philosophy (no code examples)
  - The Seven Pillars: pure functions, immutability, composition, first-class functions, referential transparency, side effect isolation, declarative style
  - Journey from OOP: why inheritance fails, composition wins
  - Anti-over-engineering: don't hand-roll utilities, use established libraries
  - References tech-specific skills (js-fp, php-fp) for implementation
  - 258 lines, purely conceptual

- **task-master Skill** - Structured task breakdown and delegation
  - Hierarchical decomposition: Epic → Story → Task
  - Storage decision tree: Serena memory vs TaskList vs Markdown
  - Agent delegation patterns: two-level max, minimal context principle
  - Vertical vs horizontal decomposition for sequential/parallel work
  - 330 lines, practical and actionable

### Changed

- **mcp-memory Skill rewritten for proactive usage**
  - From reactive ("use when asked") to proactive ("MUST use automatically")
  - Session start: automatically search for relevant context
  - During work: store decisions as they happen (with recognition patterns)
  - Session end: capture learnings
  - Before asking: check memory first
  - Added "What NOT to Store" to prevent over-storage
  - Key insight: "Memory works when wired into decision-making automatically"

- **Simplified core philosophy tagline** across all skills
  - From: `Simple > Complex | Native > Custom Utilities | MVP > Enterprise`
  - To: `Simple > Complex | Evidence > Assumptions`
  - Removes ambiguity: "MVP" was trimming features; "Native" was blocking libraries
  - Detailed skills still explain nuances; tagline is now hard to misinterpret

- **Reorganized skill categories** in `CLAUDE.md`
  - New "Foundational Skills" section for functional-programmer and task-master
  - Renamed "FP Skills" to "FP Implementation Skills" for clarity

- **Updated IMA_CLAUDE_INIT.md**
  - Added Default Persona section
  - Added Foundational Skills references
  - Clarified that personalities are tone overlays only

- **README.md comprehensively updated**
  - Added core philosophy tagline
  - Serena MCP now prominent in all tables and instructions
  - Added Foundational Skills section
  - Updated Architecture section to reflect Persona + Skills model
  - Updated skill count (22+)

### Fixed

- "MVP > Enterprise" no longer causes over-aggressive feature trimming
- "Native > Utilities" no longer blocks use of third-party libraries
- Performance section headers now say "Evidence-Based" instead of "MVP-First"

## [1.6.0] - 2026-01-30

### Changed - BREAKING

- **Session management migrated from file-based commands to MCP-based Skills**
  - Removed `~/.claude/commands/save-session.md` and `resume-session.md`
  - New Skills use Serena MCP memory storage (no file path confusion)
  - Memory name: `session-state` (project-specific, cross-session persistent)
  - Same markdown format, zero path resolution issues

### Added

- **save-session Skill** - Save session state to Serena MCP memory
  - Uses `mcp__serena__write_memory` (no file path confusion)
  - Project-specific storage (sessions belong to projects)
  - Cross-session persistent (survives Claude restarts)
  - Lean single checkpoint model
  - See skill at `skills/save-session/SKILL.md`

- **resume-session Skill** - Resume session from Serena MCP memory
  - Uses `mcp__serena__read_memory`
  - Presents status summary and waits for user direction
  - No auto-start work behavior
  - See skill at `skills/resume-session/SKILL.md`

- **Session Management Documentation** (`docs/Active/session-management.md`)
  - Technical comparison: file-based vs MCP-based
  - Advantages over file approach
  - Serena MCP requirements and rationale
  - Migration notes from old commands

### Fixed

- Session save/resume no longer experiences file path confusion
- Claude no longer gets confused about working directory when saving sessions
- No more `.claude/` directory creation issues
- Eliminated file write failures in session management

## [1.5.0] - 2026-01-30

### Changed - BREAKING

- **Migrated from Airis MCP Gateway to direct MCP servers**
  - Removed Airis Gateway dependency for simpler, more reliable MCP integration
  - Updated all MCP skills to use direct tool patterns (e.g., `mcp__tavily__search` instead of `mcp__airis-mcp-gateway__airis-exec`)
  - Direct servers are faster (no cold start), more reliable (no gateway layer), and easier to configure

### Added

- **phpunit-wp Skill** - PHPUnit testing for WordPress plugins with FP principles
  - Fast unit test setup for WordPress plugins
  - Documents the two critical setup bugs (silent execution, autoload files)
  - Environment-aware setup for Local WP
  - Pure function testing patterns with minimal mocking
  - Working templates for composer.json, phpunit.xml, bootstrap.php
  - See skill at `skills/phpunit-wp/SKILL.md`

- **Interactive MCP Setup Script** (`scripts/setup-mcp.ts`)
  - Bun-based CLI with interactive prompts for server selection
  - Handles API key input (Tavily)
  - Uses official `claude mcp add` commands (safe, no JSON editing)
  - Option to remove Airis Gateway from configuration
  - Provides guidance for managing Docker containers (no automatic operations)
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
4. Manually stop Airis Docker containers if no longer needed:
   ```bash
   docker ps | grep airis  # Check running containers
   docker stop <container-names>  # Stop specific containers
   ```

Or manually:
```bash
# Remove Airis configuration
claude mcp remove airis-mcp-gateway

# Manually stop Docker containers if no longer needed
docker ps | grep airis
docker stop <container-names>

# Install direct servers (see README.md for full commands)
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp@latest
# ... etc
```

Your MCP skills will now use direct tool patterns automatically.

## [1.4.0] - 2026-01-29

### Added

- **Prompt Coach (Experimental)** - Haiku-based prompt evaluation system
  - `UserPromptSubmit` hook evaluates prompts against team standards
  - Suggests relevant skills when missing (e.g., "Consider: mcp-serena")
  - Flags anti-patterns (custom FP utilities, over-engineering, security gaps)
  - Stays silent on good prompts to avoid noise
  - Disabled by default: `export PROMPT_COACH_ENABLED=true` to activate
  - Optional logging: `export PROMPT_COACH_LOG=true`
  - New files: `hooks/prompt_coach.py`, `hooks/prompt_coach_system.md`, `hooks/prompt_coach_digest.md`
  - See [docs/PROMPT_COACH.md](docs/PROMPT_COACH.md) for setup and usage

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
