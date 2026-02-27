# Changelog

All notable changes to ima-claude will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.19.0] - 2026-02-26

### Added

- **Memory architecture overhaul** — unified 3-tier decision tree (decay/permanent/project) across INIT and skill files
  - `IMA_CLAUDE_INIT.md` — new "Memory: What Goes Where" section replaces scattered memory logic
  - `mcp-vestige` Skill — Architecture table and Decision Logic updated with decay/permanent/project framing
  - `mcp-qdrant` Skill — reframed as "The Permanent Library" with expanded proactive triggers and new metadata types (`standard`, `sample`)
- **`.claude/rules/memory-after-work.md`** — first rules file (procedural brain); auto-injects memory storage reminders after task completion
- **Rules installer support** — `RULES_DIR`, `RULES_TO_INSTALL` in utils.ts; rules deployment step in install.ts
- **16 new hooks** (23 total) for automatic behavioral enforcement:
  - **Memory hooks**: `memory_bootstrap.py` (session-start Vestige/Qdrant reminder), `memory_store_reminder.py` (nudge after 5 edits), `vestige_before_external.py` (check Vestige before Context7/Tavily)
  - **Workflow hooks**: `task_master_after_plan.py` (delegate after ExitPlanMode), `task_master_before_impl.py` (catch non-trivial impl without task breakdown), `jira_issue_fetch.py` (auto-fetch Jira issue keys in prompts)
  - **Security hooks**: `wp_security_check.py` (WordPress AJAX nonce/capability/sanitize/prepare + strict_types + function_exists), `sql_injection_check.py` (SQL string interpolation in JS/TS)
  - **Atlassian hooks**: `atlassian_prereqs.py` (cloudId bootstrap, getTransitions before transition, ADF body serialization)
  - **Serena hooks**: `serena_project_check.py` (WP plugin subdirectory project path fix — walks up to find `.serena/project.yml` at WP root), `serena_over_grep.py` (nudge toward Serena symbol tools when Grep used for code navigation)
  - **Code quality hooks**: `fp_utility_check.py` (custom pipe/compose/curry detection), `jquery_in_wordpress.py` (vanilla DOM in WP context), `bootstrap_utility_check.py` (hardcoded CSS vs Bootstrap utilities), `composer_autoload_check.py` (autoload files PHPUnit bug), `docs_organization.py` (markdown scattered in project root)
- **PostToolUse hook support** in `mergeHooksIntoSettings()` — handles Edit, Write, ExitPlanMode matchers
- **Hooks config** now covers 29 PreToolUse matchers, 3 PostToolUse matchers, and 3 UserPromptSubmit hooks

## [1.18.0] - 2026-02-26

### Changed

- **README.md** — replaced Compound Engineering "Recommended" with IMA Workflow in What's Included; demoted Marketplace Plugin from Recommended to Optional; added honorable mention for Compound Engineering and SuperClaude
- **README.md** — added IMA Workflow section documenting the 6-step habit-driven cycle (Brainstorm → Plan → Implement → Test → Review → Document)
- **quickstart Skill** — replaced Compound Engineering pipeline with IMA Workflow table; updated Reviewing and Documenting sections to lead with native tools
- **docs/ONBOARDING.md** — removed SuperClaude from prerequisites; added IMA Workflow to Quick Start; updated Q&A to give honorable mention to both SuperClaude and Compound Engineering

## [1.17.0] - 2026-02-26

### Added

- **Orchestrator Protocol** in `IMA_CLAUDE_INIT.md` — assertive mandate for Opus to plan and delegate via `task-master` instead of implementing directly
  - 3-step workflow: receive → decompose → delegate → review
  - Model selection table (opus for orchestration, sonnet default for agents, haiku for trivial)
  - Domain-to-skills mapping table for automatic agent skill assignment
  - Self-correction trigger: "If you catch yourself implementing, stop and delegate"

### Changed

- **task-master Skill** — updated frontmatter to trigger on ALL non-trivial tasks (was: planning keywords only)
- **Skills System** in `IMA_CLAUDE_INIT.md` — expanded auto-load lists: added `js-fp-wordpress`, `php-authnet`, `ima-forms-expert`, `phpunit-wp`
- **scripts/utils.ts** — bumped VERSION to 1.17.0

## [1.16.0] - 2026-02-26

### Added

- **php-authnet Skill** - Authorize.Net PHP SDK patterns for payment processing
  - Three-layer FP architecture: pure request builders → SDK adapters → pure response parsers
  - Transaction types: auth/capture, auth-only, refund, void, prior auth capture
  - Accept.js integration: opaque payment nonce consumption, PCI compliance patterns
  - CIM customer profiles: create, update, delete, payment profiles, charge stored profiles
  - ARB recurring billing: subscriptions, schedules, trials, cancel, status checks
  - Webhook handling: HMAC-SHA512 signature validation, event types, idempotency
  - Error handling: two-level response parsing, E00039 duplicate recovery, common error codes
  - References: full API reference (`references/api-reference.md`), sandbox & testing guide (`references/sandbox-testing.md`)
  - Complements `php-fp` and `php-fp-wordpress` skills
- **CLAUDE.md** - Added "Payment & API Skills" section with `php-authnet`
- **scripts/utils.ts** - Added `php-authnet` to `SKILLS_TO_INSTALL`

## [1.15.1] - 2026-02-26

### Fixed

- **scorecard Skill** - Clarified grading format rules to prevent rendering issues
  - Added explicit rule: use exact emoji characters (`🟢` `🟡` `🔴`), never GitHub shortcodes or geometric shapes
  - Added explicit rule: whole letter grades only (A–F), no `+`/`-` modifiers
  - Added explicit format: `🟢 A` (emoji + space + letter), no backticks in README output
  - Updated grading scale table to show full indicator format (e.g., `🟢 A`) instead of color name only

## [1.15.0] - 2026-02-25

### Added

- **scorecard Skill** - Project quality scorecard for READMEs
  - Scores codebase on 5 categories: Code Standards, Security, Test Coverage, Documentation, Maintainability
  - Compact Markdown table with letter grades (A-F) and color indicators (🟢🟡🔴)
  - Domain skills passed as arguments define the "Code Standards" rubric (e.g., `/scorecard js-fp js-fp-api`)
  - Auto-detects project language/framework when no skills specified
  - Uses `task-master` for orchestration with parallel Sonnet agents per category
  - Date-stamped for freshness; inserts/replaces `## Scorecard` section in README

### Changed

- **php-fp-wordpress Skill** - Added inter-plugin communication section
  - Rule: all cross-plugin calls use WordPress hooks (`do_action`/`apply_filters`), never `function_exists()`
  - Hooks are safe no-ops; `function_exists()` is tight coupling disguised as loose coupling
  - Added checklist item for cross-plugin hook usage
- **CLAUDE.md** - Added scorecard to Quick Reference section
- **scripts/utils.ts** - Added `scorecard` to `SKILLS_TO_INSTALL`

### Fixed

- **wp-local** - Fixed WP-CLI 2.12+ MySQL socket resolution
  - WP-CLI 2.12+ passes `--no-defaults` to mysql binary, bypassing `MYSQL_HOME/my.cnf`
  - Now exports `MYSQL_UNIX_PORT` from `my.cnf` socket path as fallback
  - Fixes `ERROR 2002: Can't connect to local MySQL server through socket '/tmp/mysql.sock'`

## [1.14.2] - 2026-02-24

### Changed

- **compound-bridge Skill** - Added "Artifact Resilience" section to prevent data loss during branch switches
  - Rule 1: Shadow copy all workflow artifacts to `.claude/compound/` (gitignored, survives branch switches)
  - Rule 2: Eager memory bridge — store to Vestige immediately after each artifact write, not just at workflow completion
  - Rule 3: Pre-branch-switch checkpoint — verify shadow copies exist before any `git checkout`/`git switch`
  - Rule 4: Recovery from shadow copies — restore lost artifacts from `.claude/compound/` + Vestige
  - Rule 5: Commit `compound-engineering.local.md` early (persistent config, not transient)
- **IMA_CLAUDE_INIT.md** - Added artifact resilience note to Compound Engineering workflows section

## [1.14.1] - 2026-02-23

### Added

- **quickstart Skill** - Scannable team cheat sheet for new members
  - Organized by intent: starting sessions, planning, writing code, reviewing, research, memory
  - Table-heavy, zero narrative — just what to type
  - Covers all key workflows: Compound Engineering pipeline, FP skill auto-activation, MCP tool selection, memory tiers
  - Triggers on "quickstart", "cheat sheet", "what can I do", "getting started"

## [1.14.0] - 2026-02-23

### Added

- **compound-bridge Skill** - Compound Engineering + ima-claude integration
  - Memory bridge: Compound → Vestige (root causes, decisions, review findings auto-stored)
  - Memory bridge: Compound → Qdrant (full solutions >500 words stored for RAG)
  - Memory bridge: Vestige → Compound research (cross-project knowledge supplements learnings-researcher)
  - Role separation: `/workflows:plan` for formal planning, `task-master` for ad-hoc breakdown
  - `compound-engineering.local.md` template for per-project review agent config + coding standards
  - Boring on purpose: removing the skill returns both systems to standalone behavior

- **mcp-qdrant Skill** - Persistent knowledge base with semantic search
  - Local RAG system for document-scale knowledge (PRDs, architecture docs, plans, solutions)
  - Complements Vestige (atomic decisions) with document-scale retrieval
  - Proactive behavior: auto-store PRDs and plans, auto-search before implementation
  - Chunking guidance for large documents, metadata conventions
  - Docker + uvx setup, FastEmbed (no API keys, all data stays local)

- **jquery Skill** - jQuery patterns and API reference for WordPress/Bootstrap environments
  - FP-aligned: chaining as composition, $.map/$.grep as declarative transforms, pure logic extraction
  - Decision tree: when to use jQuery vs vanilla JS (jQuery is default for DOM work in WordPress)
  - Quick reference: selectors, traversal, manipulation, events, AJAX, utilities
  - Common patterns: IIFE wrapper, caching selections, delegated events, UI state management
  - WordPress coding standards integration (tabs, spaces in parens, var declarations)
  - Context7 library ID `/jquery/jquery` for deep API lookups

- **jira-checkpoint Skill** - Lightweight Jira awareness checkpoints for team visibility
  - Three checkpoints: Before Work (search FNR for related stories), During Work (auto-fetch issue context), After Work (prompt to update status/comment)
  - Companion to task-master (no overlap): task-master = execution, jira-checkpoint = team visibility
  - References mcp-atlassian for all API operations (no duplication)
  - Decision trees for when to checkpoint vs stay silent (significant work only)
  - Vestige integration: learns user preferences over time (skip patterns, sync habits)

### Changed

- **mcp-vestige Skill** - Added Compound workflow events to proactive storage table
  - `/workflows:compound` solutions → Vestige pattern
  - `/workflows:plan` research → Vestige decision
  - `/workflows:review` P1/P2 findings → Vestige pattern
- **IMA_CLAUDE_INIT.md** - Added Qdrant to MCP tool selection decision tree, jQuery to auto-detected skills, Compound Engineering workflows section
- **CLAUDE.md** - Renamed "MCP Integration Skills" to "Integration Skills", added compound-bridge/mcp-qdrant, replaced SuperClaude section with Compound Engineering note
- **README.md** - Modernized ecosystem: added Vestige, Qdrant, Compound Engineering marketplace plugin to recommendations; updated all skill tables; reduced SuperClaude prominence; updated skill count to 30+
- **scripts/install.ts** - Removed SuperClaude check (purely optional, no install impact), added MCP server recommendation on fresh install
- **scripts/utils.ts** - Removed `checkSuperClaude()`, added `compound-bridge`, `jquery`, `jira-checkpoint`, `mcp-qdrant` to `SKILLS_TO_INSTALL`

## [1.12.0] - 2026-02-13

### Added

- **mcp-vestige Skill** - Cognitive memory engine replacing Memory MCP
  - Vestige MCP integration: semantic search, FSRS-6 spaced repetition, prediction error gating, codebase awareness
  - 14 tools documented: search, smart_ingest, ingest, memory, codebase, intention, session_checkpoint, promote/demote, find_duplicates, consolidate, importance_score, memory_timeline, health_check
  - Smart ingest thresholds: >92% REINFORCE, 75-92% UPDATE, <75% CREATE (auto-dedup)
  - Node types: preference, decision, pattern, bug, codebase, intention, note
  - Memory states: Active, Dormant, Silent, Unavailable (natural decay via FSRS-6)
  - Proactive behavior rules: session start search, automatic storage triggers, intention checking
  - Migration mapping from Memory MCP entities/relations to Vestige equivalents

### Changed

- **Memory architecture** - 3-tier clean separation: Vestige (persistent knowledge), Serena (session state), Claude auto-memory (MEMORY.md)
- **mcp-memory Skill** - Deprecated with notice pointing to mcp-vestige; triggers narrowed to explicit reference only
- **IMA_CLAUDE_INIT.md** - Memory Bootstrap, MCP Tool Selection, Proactive Storage, and Session Lifecycle all updated from Memory MCP to Vestige
- **Global CLAUDE.md** - "Store decisions" summary updated to reference Vestige
- **Project CLAUDE.md** - mcp-vestige added to MCP Integration Skills, mcp-memory marked deprecated
- **task-master Skill** - Integration Points updated: mcp-memory → mcp-vestige
- **resume-session Skill** - Added Vestige search + intention check to resume protocol
- **save-session Skill** - Added note: persistent knowledge goes to Vestige, not Serena

## [1.11.0] - 2026-02-13

### Added

- **ima-brand Skill** - IMA Brand Book v4.0 knowledge for brand-aligned decisions
  - Brand identity: mission, vision, values (7 core values), audience profiles (consumer vs professional)
  - Brand persona: 5 tones (Professional, Friendly, Inspirational, Supportive, Informative) with channel mapping
  - Copywriting rules: do's, don'ts, terminology guide (FLCCC → IMA, precision language)
  - Visual system: full color palette (11 colors + gradient) with hex/CMYK/RGB, typography hierarchy
  - Logo system: 3 variants (horizontal, vertical, lettermark), 5 lockup colors, usage rules, improper uses
  - Imagery guidelines: photography style by content type, treatment rules
  - Digital standards: WCAG contrast ratios, social media specs (4 platforms, image sizes, content pillars)
  - Legal: medical disclaimer text, copyright format, sponsored content disclosure, approval workflow
  - Clear boundary: brand knowledge here, CSS/SCSS implementation in `ima-bootstrap`
  - SKILL.md (~110 lines) + 3 reference files (brand-identity.md, visual-system.md, digital-standards.md)

## [1.10.2] - 2026-02-12

### Changed

- **ima-bootstrap Skill** - Added IMA Container Grid documentation
  - New "Bootstrap Grid vs IMA Container Grid" decision section in SKILL.md
  - Container query grid: `.ima-row` + `.ima-col-{bp}-{n}` responds to parent container width, not viewport
  - Breakpoints: `sm`≥400px, `md`≥600px, `lg`≥800px (container-based)
  - Updated decision tree with container-responsive layout option
  - Added anti-patterns: `.col-md-6` in reusable components, inline flex hacks
  - Updated file structure to include `_container-grid.scss`
  - `references/ima-brand.md` - Full container grid reference with examples, breakpoint table, SCSS variables
  - `references/bootstrap-patterns.md` - Added viewport limitation note with container grid cross-reference

## [1.10.1] - 2026-02-11

### Changed

- **task-master Skill** - Added model selection guidance for subagent delegation
  - New "Model Selection for Subagents" section: Opus orchestrates, Sonnet executes, Haiku for trivial
  - Decision tree for choosing model per subtask based on complexity
  - Added model choice as question #5 in Delegation Decision Framework
  - New anti-pattern: "Every agent needs Opus" → default to Sonnet for delegated work

## [1.10.0] - 2026-02-11

### Added

- **mcp-atlassian Skill** - Jira & Confluence operations via Claude's bundled Atlassian MCP
  - Complete catalog of all 28 MCP tools organized by category with token-saving tips
  - User mention (@tagging) patterns that actually work - the critical missing piece:
    - Confluence pages: ADF format with mention nodes (reliable)
    - Jira descriptions: `editJiraIssue` with ADF fields (reliable)
    - Comments: Markdown-only limitation documented with workarounds
  - `lookupJiraAccountId` → `accountId` flow for both Jira and Confluence
  - 6 common mention pitfalls with symptoms and fixes (JSON.stringify, inline nodes, wiki notation)
  - Token-saving strategies: field filtering, Markdown reads, result limits, session caching
  - Decision logic for search tools (Rovo vs JQL vs CQL)
  - Common workflows: create+assign issues, transition status, create pages with mentions
  - SKILL.md: 339 lines

## [1.9.0] - 2026-02-06

### Added

- **playwright Skill** - E2E testing and QA automation with Playwright + TypeScript
  - Combined QA strategy layer (what/why to test) with Playwright implementation (how to test)
  - QA strategy: test pyramid for E2E, test independence, what makes a good E2E test
  - Locator strategy: priority table (role > label > placeholder > text > testid > CSS)
  - Web-first assertions: auto-wait patterns with common anti-patterns
  - Page Object Model: full POM class pattern with fixture registration
  - Custom fixtures: auth state persistence, global setup, composable fixtures
  - Project structure: recommended folder layout for scalable test suites
  - Configuration: complete `playwright.config.ts` with projects, webServer, CI settings
  - Anti-patterns: hard-coded waits, brittle selectors, manual assertions, shared state
  - Linting: eslint-plugin-playwright integration
  - Four progressive-disclosure reference files:
    - `references/network-mocking.md` - HAR recording/playback, error simulation, API-first setup, route management
    - `references/visual-regression.md` - Deterministic screenshots, animation handling, CI baselines, diff workflow
    - `references/accessibility-testing.md` - axe-core/WCAG fixtures, targeted scanning, common violations
    - `references/ci-cd.md` - GitHub Actions, sharding with report merging, Docker, reporters
  - SKILL.md: 434 lines, references: 906 lines total

## [1.8.0] - 2026-02-06

### Added

- **ima-bootstrap Skill** - Bootstrap 5.3 + IMA brand integration
  - Utility-first CSS approach with decision tree and anti-patterns table
  - Bootstrap utility quick reference (spacing, display, flex, grid, text, colors, borders)
  - Key component patterns (cards, modals, accordions, buttons, tables)
  - IMA brand color/typography/mixin reference integrated with Bootstrap class mappings
  - Three progressive-disclosure reference files:
    - `references/ima-brand.md` - Full IMA color palette, typography mixins, component mixins
    - `references/theme-integration.md` - Picostrap5 SCSS pipeline, variable override chain
    - `references/bootstrap-patterns.md` - Extended Bootstrap patterns, Sass customization, JS API
  - Context7 integration for deep Bootstrap API lookups (`/websites/getbootstrap`)
  - Follows quasar-fp structural pattern
  - SKILL.md: 248 lines, references: 787 lines total

### Changed

- Added `*.skill` to `.gitignore` (packaged skill bundles are build artifacts)
- Synced `package.json` version with `utils.ts` VERSION constant

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
