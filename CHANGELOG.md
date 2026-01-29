# Changelog

All notable changes to ima-claude will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
