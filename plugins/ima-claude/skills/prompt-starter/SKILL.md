---
name: prompt-starter
description: Build better prompts from rough ideas. Selects template, pre-fills from Jira, opens in GUI editor, returns refined prompt. Does NOT execute the work — only crafts the prompt.
---

# Prompt Starter

**Role: prompt builder, not executor.** Take a rough idea, produce a well-structured prompt. Never execute the work described — only craft and return it.

- **prompt-starter** = "What should my prompt say?" (template + context + editor)
- **prompt_coach.py** = "Is my prompt good enough?" (quality evaluation)

## Template Selection

| User says | Template |
|---|---|
| `brainstorm`, `research`, `explore` | `references/brainstorm.md` |
| `plan`, `implement`, `build`, `execute` | `references/plan-implement.md` |
| `review`, `code review`, `audit`, `PR review`, Gitea/GitHub PR URL | `references/code-review.md` |
| `quick` or short one-liner | `references/quick.md` |
| Jira key only (ambiguous) | Ask which template |

## Flow

**Step 1: Select template** — read from `references/`.

**Step 2: Fetch Jira context** (if key present) — use mcp-atlassian. Map fields to template `[bracket]` placeholders:
- Summary → one-line goal / user story
- Description → Problem section
- Acceptance Criteria → Acceptance / Test sections
- For code-review template: PR URL or branch from description/linked branch → pre-fill `Scope` section

Use judgment — if Jira description is sparse, leave bracket hints for user.

**Step 3: Check prior work** (plan-implement only) — search Serena memory for `{feature-name}-brainstorm`. If found, pre-fill Prior Work section and incorporate key decisions into Plan section.

**Step 4: Write pre-filled template**

```bash
mkdir -p ~/.claude/prompts
```

Write to `~/.claude/prompts/{session-name}.md` — name descriptively:
- `brainstorm-pdf-export.md`
- `quick-email-validation.md`
- `plan-fnr-1234.md`

**Step 5: Open in editor**

Quick templates (12 lines): present inline, skip editor. Go to Step 7.

For brainstorm and plan-implement, spawn GUI editor. Claude Code owns the terminal — terminal editors (nano, vim) cannot be used.

Editor resolution order:
1. `$VISUAL`
2. `$EDITOR` — only if known GUI: `zed`, `code`, `subl`, `gedit`, `kate`
3. Auto-detect: `which zed` → `which code` → `which subl` (first found)
4. Fallback: present inline, edit via conversation

```bash
# Spawn with run_in_background: true
zed --wait ~/.claude/prompts/{session-name}.md
```

Tell user: `"Template is open in {editor}. Edit and close the tab when done — I'll pick up from there."`

**Step 6: Read result** — when background task completes, read `~/.claude/prompts/{session-name}.md`.

**Step 7: Present finished prompt — STOP**

> Here's your refined prompt. You can paste it into a new conversation, adjust it further, or tell me to run it.

Do NOT execute. Only execute if user explicitly says "run it" or "execute this".

## Team Setup

```bash
echo 'export VISUAL="zed --wait"' >> ~/.bashrc   # Zed
echo 'export VISUAL="code --wait"' >> ~/.bashrc  # VS Code
echo 'export VISUAL="subl --wait"' >> ~/.bashrc  # Sublime Text
```
