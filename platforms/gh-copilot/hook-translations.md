# Hook-to-Copilot Translation Map

This document tracks the relationship between Claude Code hooks and their
GitHub Copilot equivalents. GitHub Copilot has full hook support (preToolUse,
postToolUse, userPromptSubmitted, sessionStart), so all hooks translate 1:1
via the hooks-translator.py shim — the same strategy as Gemini CLI.

## Translation Strategy

Copilot's hook system is functionally equivalent to Claude Code's. The
`hooks-translator.py` shim sits between Copilot and each hook script,
translating Copilot tool names to Claude Code equivalents so hook scripts
work unmodified.

Key differences from Claude Code:
- Hook config uses `{ "version": 1, "hooks": { ... } }` format
- Event names are camelCase: `preToolUse`, `postToolUse`, `userPromptSubmitted`
- Each hook entry is flat: `{ matcher, type, bash }` (not grouped)
- Uses `bash` field (not `command`)

## Hook → Copilot Mapping

### Tool Redirection Hooks → Translated (via shim)

| Hook | Copilot Event | Matcher | Notes |
|------|--------------|---------|-------|
| `enforce_rg_over_grep.py` | preToolUse | run_terminal_command | Translates to Bash before hook runs |
| `webfetch_to_tavily.py` | preToolUse | fetch_url | Translates to WebFetch before hook runs |
| `websearch_to_tavily.py` | preToolUse | web_search | Translates to WebSearch before hook runs |
| `tavily_extract_advanced.py` | preToolUse | mcp__tavily__tavily-extract | MCP matcher passthrough |

### Memory Hooks → Translated (via shim)

| Hook | Copilot Event | Notes |
|------|--------------|-------|
| `memory_bootstrap.py` | preToolUse | Runs on multiple tool matchers |
| `memory_store_reminder.py` | postToolUse | Runs on Edit/Write |
| `vestige_before_external.py` | preToolUse | Runs on Tavily/Context7 MCP tools |

### Serena Hooks → Translated (via shim)

| Hook | Copilot Event | Notes |
|------|--------------|-------|
| `serena_over_read.py` | preToolUse | read_file → Read translation |
| `serena_over_grep.py` | preToolUse | search_code → Grep translation |
| `serena_project_check.py` | preToolUse | MCP matcher passthrough |

### Workflow Hooks → Translated (via shim)

| Hook | Copilot Event | Notes |
|------|--------------|-------|
| `prompt_coach.py` | userPromptSubmitted | Calls Anthropic API — requires ANTHROPIC_API_KEY |
| `task_master_before_impl.py` | userPromptSubmitted | Works unmodified |
| `task_master_after_plan.py` | postToolUse | ExitPlanMode matcher passthrough |
| `jira_issue_fetch.py` | userPromptSubmitted | Works unmodified |

### Security Hooks → Translated (via shim)

| Hook | Copilot Event | Notes |
|------|--------------|-------|
| `wp_security_check.py` | postToolUse | edit_file/write_file → Edit/Write translation |
| `sql_injection_check.py` | postToolUse | edit_file/write_file → Edit/Write translation |

### Code Quality Hooks → Translated (via shim)

| Hook | Copilot Event | Notes |
|------|--------------|-------|
| `fp_utility_check.py` | postToolUse | edit_file/write_file → Edit/Write translation |
| `jquery_in_wordpress.py` | postToolUse | edit_file/write_file → Edit/Write translation |
| `bootstrap_utility_check.py` | postToolUse | edit_file/write_file → Edit/Write translation |
| `composer_autoload_check.py` | postToolUse | edit_file/write_file → Edit/Write translation |
| `docs_organization.py` | postToolUse | write_file → Write translation |
| `block_sed_edits.py` | preToolUse | run_terminal_command → Bash translation |

### Sequential Thinking → Translated (via shim)

| Hook | Copilot Event | Notes |
|------|--------------|-------|
| `sequential_thinking_check.py` | userPromptSubmitted | Works unmodified |

### Atlassian Hooks → Translated (via shim)

| Hook | Copilot Event | Notes |
|------|--------------|-------|
| `atlassian_prereqs.py` | preToolUse | MCP matcher passthrough |

### Session Hooks

| Hook | Copilot Event | Notes |
|------|--------------|-------|
| `bootstrap.sh` | sessionStart | Content becomes copilot-instructions.md guidelines |
