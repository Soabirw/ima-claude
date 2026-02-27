# Hook Testing Playbook

Human-facing verification guide for ima-claude hooks. Hooks fire silently during Claude Code
sessions — this playbook explains what to look for and how to confirm each one is working.

---

## Section 1: How Hook Output Works

Claude Code hooks run as subprocesses and communicate with Claude in two ways:

**Advisory hooks (exit 0)**
- Write warnings to **stderr**
- Claude receives them as a `<system-reminder>` tag injected into its context
- **You do NOT see this output** unless Claude explicitly acts on it (rephrases its response,
  suggests a different tool, adds a warning comment, etc.)
- The hook still ran — Claude just absorbed the nudge silently

**Blocking hooks (exit non-zero)**
- Claude Code shows a dialog to the user asking whether to proceed
- Used for hard gates (not currently used in ima-claude — all hooks are advisory)

**SessionStart hooks**
- Run when a session begins (startup, resume, clear, compact)
- Output goes to **stdout**, which is injected as a `<system-reminder>` at the top of the
  conversation context
- You CAN confirm this one fired by seeing its marker in Claude's first response

**The practical implication**: Most hooks cannot be verified by watching the screen. You verify
them by observing Claude's *behavior* — whether it uses `rg` instead of `grep`, whether it
flags a security issue after you write vulnerable PHP, etc.

---

## Section 2: Install Verification

Before testing individual hooks, confirm the hooks are wired into `~/.claude/settings.json`.

### 2.1 Confirm hooks are present

```bash
# Should print lines containing the hook script path
grep "enforce_rg_over_grep" ~/.claude/settings.json

# Should return a non-zero count (typically 50+ lines for a full install)
grep "hooks" ~/.claude/settings.json | wc -l

# Quick sanity check: see all hook commands in one view
python3 -c "
import json
data = json.load(open(open.__module__ and '/dev/null' or '', 'r') if False else open('/root/.claude/settings.json' if __import__('os').path.exists('/root/.claude/settings.json') else __import__('os.path', fromlist=['expanduser']).expanduser('~/.claude/settings.json')))
hooks = data.get('hooks', {})
for event, matchers in hooks.items():
    for m in matchers:
        for h in m.get('hooks', []):
            print(event, '|', m.get('matcher','*'), '|', h.get('command',''))
" 2>/dev/null | sort
```

### 2.2 Confirm CLAUDE_PLUGIN_ROOT is set

The hooks use `${CLAUDE_PLUGIN_ROOT}` to locate scripts. If this is unset, every hook silently
does nothing (python3 can't find the file).

```bash
# Check the env var is in your shell
echo $CLAUDE_PLUGIN_ROOT

# It should resolve to the ima-claude plugin directory, e.g.:
# /home/eric/IMA/dev/ima-claude/plugins/ima-claude

# Confirm the scripts are reachable from that root
ls $CLAUDE_PLUGIN_ROOT/hooks/enforce_rg_over_grep.py
```

If `CLAUDE_PLUGIN_ROOT` is empty, add it to your shell profile (`~/.bashrc`, `~/.zshrc`):

```bash
export CLAUDE_PLUGIN_ROOT="$HOME/IMA/dev/ima-claude/plugins/ima-claude"
```

### 2.3 Manual hook invocation test

Run any hook directly to confirm it parses input correctly:

```bash
echo '{"tool_name":"Bash","tool_input":{"command":"grep -r foo src/"}}' \
  | python3 $CLAUDE_PLUGIN_ROOT/hooks/enforce_rg_over_grep.py
echo "Exit code: $?"
```

Expected: output on stderr with the `rg` suggestion, exit code 0.

---

## Section 3: Quick Smoke Test — SessionStart

The `bootstrap.sh` SessionStart hook is the easiest to confirm because its stdout becomes
visible context at the start of every session.

**What to look for**: At the start of a new Claude Code session (or after `/clear`), Claude's
first response or the conversation header should reflect the bootstrap content — the persona
description ("25-year software development veteran"), memory routing table, or Orchestrator
protocol text.

If Claude mentions "The Practitioner" persona, references Vestige/Qdrant routing, or uses the
"we" pronoun pattern from the bootstrap, SessionStart is confirmed working.

You can also trigger it explicitly:

```bash
# Force a new session by clearing and watching Claude's opening behavior
# In Claude Code: /clear
# Then ask: "What persona are you operating as right now?"
# Claude should describe The Practitioner without you having told it anything
```

---

## Section 4: Per-Hook Trigger Prompts

For each hook below: send the listed prompt to Claude, then check the expected behavior.
Since advisory hook output goes to Claude (not you), judge success by Claude's *response*.

### 4.1 PreToolUse Hooks — Bash tool

| Hook | Trigger prompt | Expected Claude behavior | Confirmed? |
|------|---------------|--------------------------|------------|
| `enforce_rg_over_grep` | "Run `grep -r TODO src/`" | Claude should either switch to `rg -r TODO src/` or note that `rg` is preferred before running | [ ] |
| `enforce_rg_over_grep` (find) | "Use `find . -name '*.ts'` to list TypeScript files" | Claude should pivot to `rg --files -g '*.ts'` | [ ] |
| `memory_bootstrap` | Start a fresh session, then ask Claude to read any file | Claude's first tool use should be preceded by a Vestige/Qdrant search, or it should acknowledge memory context | [ ] |

### 4.2 PreToolUse Hooks — Read tool

| Hook | Trigger prompt | Expected Claude behavior | Confirmed? |
|------|---------------|--------------------------|------------|
| `serena_over_read` | "Read the file `src/services/UserService.ts`" (must be >5KB) | Claude should first try `mcp__serena__jet_brains_get_symbols_overview` or note it's checking Serena first | [ ] |
| `memory_bootstrap` | Same as above — fires on first non-memory tool | Claude searches memory before reading | [ ] |

### 4.3 PreToolUse Hooks — Grep tool

| Hook | Trigger prompt | Expected Claude behavior | Confirmed? |
|------|---------------|--------------------------|------------|
| `serena_over_grep` | "Find all places where `UserService` class is defined" | On every other symbol-like Grep, Claude should suggest `mcp__serena__jet_brains_find_symbol` instead | [ ] |
| `memory_bootstrap` | Same session-start behavior as other tools | [ ] |

### 4.4 PreToolUse Hooks — Web / External tools

| Hook | Trigger prompt | Expected Claude behavior | Confirmed? |
|------|---------------|--------------------------|------------|
| `webfetch_to_tavily` | "Fetch the content at https://example.com/docs" | Claude should note that Tavily extract may give cleaner results, then either switch or proceed | [ ] |
| `websearch_to_tavily` | "Search the web for React 19 release notes" | Claude should use `mcp__tavily__tavily_search` or note Tavily is preferred over WebSearch | [ ] |
| `tavily_extract_advanced` | "Extract content from https://linkedin.com/in/someone" | Claude should suggest `extract_depth: "advanced"` for LinkedIn | [ ] |
| `vestige_before_external` | Without doing any Vestige search first, ask Claude to look up something via Tavily | Claude should note it hasn't checked Vestige yet and search there first | [ ] |

### 4.5 PreToolUse Hooks — Serena JetBrains tools (WordPress context)

| Hook | Trigger prompt | Expected Claude behavior | Confirmed? |
|------|---------------|--------------------------|------------|
| `serena_project_check` | Use any Serena JetBrains tool while cwd is inside `wp-content/plugins/` | Claude should warn that the Serena project root is the WP root, not the plugin dir | [ ] |

### 4.6 PreToolUse Hooks — Atlassian MCP

| Hook | Trigger prompt | Expected Claude behavior | Confirmed? |
|------|---------------|--------------------------|------------|
| `atlassian_prereqs` (cloudId) | Ask Claude to get a Jira issue without first calling `getAccessibleAtlassianResources` | Claude should call `getAccessibleAtlassianResources` first to get cloudId | [ ] |
| `atlassian_prereqs` (transitions) | Ask Claude to transition a Jira issue without first fetching transitions | Claude should call `getTransitionsForJiraIssue` before `transitionJiraIssue` | [ ] |
| `atlassian_prereqs` (ADF body) | Ask Claude to create a Confluence page with `contentFormat: "adf"` | Claude should ensure the body is a JSON string, not a raw object | [ ] |

### 4.7 PostToolUse Hooks — Edit / Write on PHP files

| Hook | Trigger prompt | Expected Claude behavior | Confirmed? |
|------|---------------|--------------------------|------------|
| `wp_security_check` (nonce) | Ask Claude to write a PHP file with an `add_action('wp_ajax_...')` handler but no nonce check | Claude should flag H1: missing nonce verification | [ ] |
| `wp_security_check` (sanitization) | Ask Claude to write PHP that reads `$_GET['foo']` without sanitizing | Claude should flag H1: raw `$_GET` access | [ ] |
| `wp_security_check` (wpdb) | Ask Claude to write `$wpdb->query("SELECT * WHERE id = $id")` | Claude should flag H1: missing `->prepare()` | [ ] |
| `wp_security_check` (strict_types) | Ask Claude to write any new `.php` file | Claude should flag M4: missing `declare(strict_types=1)` | [ ] |
| `composer_autoload_check` | Ask Claude to add a PHP `require 'path/to/file.php'` in a project with composer | Claude should note that `composer autoload` should be used instead of manual requires | [ ] |

### 4.8 PostToolUse Hooks — Edit / Write on JS/TS files

| Hook | Trigger prompt | Expected Claude behavior | Confirmed? |
|------|---------------|--------------------------|------------|
| `sql_injection_check` | Ask Claude to write a `.ts` file with `` `SELECT * FROM users WHERE id = ${userId}` `` | Claude should flag H2: SQL string interpolation | [ ] |
| `fp_utility_check` | Ask Claude to write a custom `pipe()` or `compose()` function in a `.ts` file | Claude should warn against custom FP utilities, suggest native patterns | [ ] |
| `jquery_in_wordpress` | Ask Claude to write a WordPress theme `.js` file using `$()` without `jQuery` alias | Claude should flag the jQuery conflict issue | [ ] |
| `bootstrap_utility_check` | Ask Claude to write a component using Bootstrap utility classes in a Quasar project | Claude should note the Bootstrap/Quasar utility collision | [ ] |

### 4.9 PostToolUse Hooks — Write tool only

| Hook | Trigger prompt | Expected Claude behavior | Confirmed? |
|------|---------------|--------------------------|------------|
| `docs_organization` | Ask Claude to write a new `.md` file to the repo root | Claude should note whether it belongs in `docs/` per the docs-organize skill | [ ] |
| `memory_store_reminder` | Make 5 or more Edit/Write calls in one session without any Vestige/Qdrant store | After the 5th edit, Claude should prompt about storing decisions | [ ] |

### 4.10 UserPromptSubmit Hooks

| Hook | Trigger prompt | Expected Claude behavior | Confirmed? |
|------|---------------|--------------------------|------------|
| `prompt_coach` | Send a vague prompt like "fix the bug" | Claude should note the prompt is missing context (which bug, which file, what behavior) | [ ] |
| `jira_issue_fetch` | Include a Jira key in your prompt: "Can you help me with IMA-123?" | Claude should automatically call `getJiraIssue` for IMA-123 to pull context | [ ] |
| `sequential_thinking_check` | Send a debugging or analysis prompt: "Why isn't my login form working?" | Claude should invoke `mcp__sequential-thinking__sequentialthinking` before acting | [ ] |
| `task_master_before_impl` | Ask Claude to implement a non-trivial feature | Claude should invoke task-planner first rather than implementing directly | [ ] |

### 4.11 PostToolUse Hooks — ExitPlanMode

| Hook | Trigger prompt | Expected Claude behavior | Confirmed? |
|------|---------------|--------------------------|------------|
| `task_master_after_plan` | Exit plan mode (approve a plan) | Claude should trigger task-runner delegation after plan approval | [ ] |

---

## Section 5: Activity Log (Debug Mode)

When you need a persistent record of which hooks fired — useful when Claude's behavior is
ambiguous and you can't tell whether the hook ran at all — enable the debug logger.

### 5.1 Enable the logger

Set the env var before launching Claude Code:

```bash
export CLAUDE_HOOK_DEBUG=1
claude  # or however you launch Claude Code
```

### 5.2 Add logging to a hook

`hook_logger.py` is a standalone utility. To instrument a hook, import and call it:

```python
# At the top of any hook script:
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from hook_logger import log_hook

# Then before sys.exit(0) where the hook fires:
log_hook("enforce_rg_over_grep", triggered=True, reason="grep found in command")

# And on the skip paths:
log_hook("enforce_rg_over_grep", triggered=False, reason="no grep pattern matched")
```

The logger only writes when `CLAUDE_HOOK_DEBUG=1`. When the env var is absent, `log_hook()`
is a no-op — no overhead in production.

### 5.3 Read the log

```bash
# Tail the log in real time while running Claude Code in another terminal
tail -f ~/.claude/hook-activity.log

# See the last 50 entries
tail -50 ~/.claude/hook-activity.log

# Filter to a specific hook
grep "enforce_rg_over_grep" ~/.claude/hook-activity.log
```

### 5.4 Sample log output

```
2026-02-27 14:23:01 | enforce_rg_over_grep | TRIGGERED | grep found in command
2026-02-27 14:23:05 | serena_over_read     | SKIPPED   | non-code file extension
2026-02-27 14:23:12 | wp_security_check    | TRIGGERED | raw $_GET access without sanitization
2026-02-27 14:23:18 | memory_bootstrap     | SKIPPED   | already bootstrapped this session
2026-02-27 14:24:01 | jira_issue_fetch     | TRIGGERED | key IMA-123 detected in prompt
```

### 5.5 Log file location

```
~/.claude/hook-activity.log
```

The file is append-only. Rotate manually if it grows large:

```bash
mv ~/.claude/hook-activity.log ~/.claude/hook-activity.log.bak
```
