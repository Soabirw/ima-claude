# Hook-to-Guideline Translation Map

This document tracks the relationship between Claude Code hooks and their
Junie AGENTS.md guideline equivalents. When a hook is updated, the corresponding
guideline text in `agents-template.md` should be reviewed.

## Translation Strategy

Junie has no hook system. Hook behaviors are translated into:
1. **AGENTS.md guidelines** — persistent instructions loaded every session
2. **Skill content** — where the behavior is skill-specific (no change needed)
3. **Dropped** — where the behavior is Claude-specific with no Junie equivalent

## Hook → Guideline Mapping

### Tool Redirection Hooks → Search & Tool Preferences

| Hook | Guideline Section | Notes |
|------|-------------------|-------|
| `enforce_rg_over_grep.py` | Search Preference | "Prefer rg (ripgrep) over grep/find" |
| `webfetch_to_tavily.py` | MCP Tool Routing | "Prefer Tavily extract over WebFetch" |
| `websearch_to_tavily.py` | MCP Tool Routing | "Prefer Tavily search over WebSearch" |
| `tavily_extract_advanced.py` | MCP Tool Routing | "Use advanced extraction for complex pages" |

### Memory Hooks → Memory Routing Guidelines

| Hook | Guideline Section | Notes |
|------|-------------------|-------|
| `memory_bootstrap.py` | Memory Bootstrap | "Check Vestige/Qdrant at session start" |
| `memory_store_reminder.py` | Memory Routing | "After completing work, store outcomes" |
| `vestige_before_external.py` | Memory Routing | "Check Vestige before external tools" |

### Serena Hooks → Code Navigation Guidelines

| Hook | Guideline Section | Notes |
|------|-------------------|-------|
| `serena_over_read.py` | Code Navigation | "Prefer Serena symbol overview over Read" |
| `serena_over_grep.py` | Code Navigation | "Prefer Serena find_symbol over Grep" |
| `serena_project_check.py` | Code Navigation | "Verify Serena project path before ops" |

### Workflow Hooks → Orchestrator Protocol

| Hook | Guideline Section | Notes |
|------|-------------------|-------|
| `prompt_coach.py` | Dropped | Claude-specific prompt evaluation hook |
| `task_master_before_impl.py` | Orchestrator Protocol | "Non-trivial work → task decomposition" |
| `task_master_after_plan.py` | Orchestrator Protocol | "After planning, delegate to agents" |
| `jira_issue_fetch.py` | Dropped | Requires Claude-specific hook stdin |

### Security Hooks → Code Quality Guidelines

| Hook | Guideline Section | Notes |
|------|-------------------|-------|
| `wp_security_check.py` | Security | "Verify nonce/sanitization in WordPress PHP" |
| `sql_injection_check.py` | Security | "Never concatenate user input into SQL" |

### Code Quality Hooks → Code Style Guidelines

| Hook | Guideline Section | Notes |
|------|-------------------|-------|
| `fp_utility_check.py` | FP Principles | "Don't create custom pipe/compose/curry utilities" |
| `jquery_in_wordpress.py` | WordPress JS | "Use jQuery patterns when in WP context" |
| `bootstrap_utility_check.py` | CSS Patterns | "Use Bootstrap utility classes, avoid custom CSS" |
| `composer_autoload_check.py` | PHP Patterns | "Run composer dump-autoload after new PHP files" |
| `docs_organization.py` | Documentation | "Follow Active/Archive/Transient doc tiers" |
| `block_sed_edits.py` | Tool Usage | "Use Edit tool, not sed, for code changes" |

### Session Hooks → Session Management

| Hook | Guideline Section | Notes |
|------|-------------------|-------|
| `bootstrap.sh` | Full AGENTS.md | Entire bootstrap content becomes AGENTS.md |

### Atlassian Hooks → Dropped

| Hook | Guideline Section | Notes |
|------|-------------------|-------|
| `atlassian_prereqs.py` | Dropped | Requires Claude-specific hook mechanism |

### Sequential Thinking → Complex Reasoning

| Hook | Guideline Section | Notes |
|------|-------------------|-------|
| `sequential_thinking_check.py` | Complex Reasoning | "Use sequential thinking for debugging/analysis" |
