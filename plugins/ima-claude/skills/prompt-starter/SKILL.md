---
name: prompt-starter
description: Zero-friction prompt templates (quick, brainstorm, plan-implement). Selects template, pre-fills from Jira, opens in GUI editor, reads back on close.
---

# Prompt Starter

Load a structured prompt template, pre-fill it with Jira context, open it in the user's GUI editor, and execute the result when they close the file.

**Trigger words:**
- `brainstorm`, `research`, `explore` → `references/brainstorm.md`
- `plan`, `implement`, `build`, `execute` → `references/plan-implement.md`
- `quick`, or a short one-liner task → `references/quick.md`
- Just a Jira key with no clear workflow → ask the user which template

## Relationship to prompt_coach.py

- **prompt-starter** = "What should my prompt say?" (template + context + editor)
- **prompt_coach.py** = "Is my prompt good enough?" (quality evaluation)

Different lanes, complementary. The coach may fire on the final prompt — that's fine.

---

## Template Selection

Match the user's trigger words to select a template. Examples:

| User says | Template |
|---|---|
| "brainstorm FNR-1234" | brainstorm.md |
| "research auth options" | brainstorm.md |
| "plan and implement FNR-567" | plan-implement.md |
| "build the PDF export" | plan-implement.md |
| "quick task: add validation" | quick.md |
| "FNR-1234" (ambiguous) | Ask which workflow |

---

## Flow

### Step 1: Select template

Read the appropriate template from `references/`.

### Step 2: Fetch Jira context (if Jira key present)

Use mcp-atlassian to fetch the issue. Extract:
- **Summary** → fills the one-line goal / user story
- **Description** → fills the Problem section
- **Acceptance Criteria** (from description or subtasks) → fills Acceptance / Test sections

Map Jira fields to template `[bracket]` placeholders naturally — don't create a rigid substitution engine. Use judgment: if the Jira description is rich, use it; if sparse, leave the bracket hint for the user to fill in.

### Step 3: Check prior work (plan-implement only)

For plan-implement templates, search Serena memory for `{feature-name}-brainstorm`. If found, pre-fill the **Prior Work** section with a reference to it and incorporate key decisions into the **Plan** section.

### Step 4: Write the pre-filled template

Create the prompt directory if needed:
```bash
mkdir -p ~/.claude/prompts
```

Write the pre-filled template to `~/.claude/prompts/{session-name}.md` where session-name is descriptive:
- `brainstorm-pdf-export.md`
- `quick-email-validation.md`
- `plan-fnr-1234.md`

### Step 5: Open in editor (or present inline)

**Quick template exception:** Quick templates are short (12 lines). Present them inline in the conversation — no editor spawn. Skip to Step 7.

**For brainstorm and plan-implement templates**, spawn the user's GUI editor.

#### Editor Resolution

Claude Code owns the terminal, so terminal editors (nano, vim) cannot be used — the user can't interact with them. Only GUI editors work.

Resolution order:
1. `$VISUAL` — the Unix convention for GUI editors
2. `$EDITOR` — but **only** if it's a known GUI editor: `zed`, `code`, `subl`, `gedit`, `kate`
3. Auto-detect: check `which zed`, then `which code`, then `which subl` — use the first found
4. **Fallback:** no suitable editor found → present inline and modify via conversation

#### Spawning the editor

Use Bash with `run_in_background: true`:
```bash
zed --wait ~/.claude/prompts/{session-name}.md
```

All GUI editors use `--wait` so the process blocks until the user closes the file/tab.

Tell the user:
> Template is open in {editor}. Edit and close the tab when done — I'll pick up from there.

### Step 6: Read the result

When the background task completes (editor closed), read the file back:
```
Read ~/.claude/prompts/{session-name}.md
```

### Step 7: Confirm and execute

Present the final prompt to the user. Ask for confirmation:
> Here's your prompt. Ready to execute, or want to adjust anything?

On confirmation, treat the prompt content as working instructions and execute accordingly.

---

## Editor Notes for Team Onboarding

Team members should set `$VISUAL` in their shell profile for the best experience:

```bash
# Zed
echo 'export VISUAL="zed --wait"' >> ~/.bashrc

# VS Code
echo 'export VISUAL="code --wait"' >> ~/.bashrc

# Sublime Text
echo 'export VISUAL="subl --wait"' >> ~/.bashrc
```
