# Changelog

All notable changes to ima-claude will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-26

### Added

- **Skills-first Architecture**: Complete migration from commands to skills
- **11 FP Skills**:
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

### Deprecated

- `/fp:*` command system (use Skills instead)

### Removed

- SuperClaude dependency (now optional)
- Command-based routing

## Migration Notes

If you were using `/fp:*` commands:

1. Install ima-claude: `bunx ima-claude install`
2. Skills auto-activate based on context
3. See `docs/MIGRATING-FROM-COMMANDS.md` for details
