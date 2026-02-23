---
name: jira-checkpoint
description: >-
  Jira awareness checkpoints for team visibility around development work.
  Lightweight companion to task-master — adds before/during/after Jira sync
  without modifying execution workflow. Use when: "let's work on", "implement",
  "build", "fix", "finished", "completed", "done with", "FNR-", "Jira story",
  planning discussions about features or fixes, or when referencing Jira issue keys.
  Triggers on: FNR-, Jira, story, sprint work, significant feature/fix starts,
  work completion signals.
---

# Jira Checkpoint - Team Visibility Layer

**"Work gets done. Does the team know?"**

Claude Code makes us 3-5x faster. Jira becomes the bottleneck — not the work, but remembering to update it. This skill adds lightweight checkpoints so team visibility stays current without breaking flow.

## Responsibility Separation

```
task-master      = "How do I organize my work?"    (execution, tactical)
jira-checkpoint  = "Does the team know?"           (visibility, strategic)
mcp-atlassian    = "How do I talk to Jira's API?"  (implementation, reference)
```

**No overlap.** task-master owns TaskList, decomposition, and delegation. jira-checkpoint owns the question "should we sync with Jira?" mcp-atlassian owns the API mechanics. Each skill stays in its lane.

## The Three Checkpoints

### 1. Before Work (Planning)

**When:** User starts significant work — "let's implement", "build the", "fix the", "work on FNR-".

**Action:** Ask one question:

> "Should I search Jira (FNR project) for related stories before we start?"

**Decision tree:**

```
Is this significant work (feature, fix, refactor)?
├── YES → Ask about Jira search
│   User says yes → searchJiraIssuesUsingJql with FNR project
│   User says skip → Proceed, no Jira
└── NO (trivial utility, config tweak, typo fix) → Stay silent
```

**What counts as "significant":**
- New feature or component
- Bug fix with user impact
- Refactor touching multiple files
- Anything that would reasonably be a Jira story

**What stays silent:**
- Adding a utility function
- Config file tweaks
- Formatting/linting fixes
- Internal refactors with no external impact

### 2. During Work (Context)

**When:** User references a Jira issue key (e.g., `FNR-123`).

**Action:** Auto-fetch the issue details and surface relevant context:

```
Detected FNR-123. Fetching story context...

→ "As a user, I want to reset my password via email"
→ Acceptance criteria: [list]
→ Status: In Progress | Assignee: Eric
```

**Implementation:** Use `getJiraIssue` with fields: `summary,description,status,assignee,customfield_10016` (acceptance criteria). See mcp-atlassian skill for field filtering patterns.

**Decision tree:**

```
Did user mention an issue key (FNR-NNN)?
├── YES → Auto-fetch, surface summary + acceptance criteria
│   Already fetched this session? → Skip (don't re-fetch)
└── NO → Stay silent
```

### 3. After Work (Sync)

**When:** Work completes and a Jira story was referenced or discovered during the session.

**Action:** Ask one question:

> "We referenced FNR-123 during this work. Want to update its status or add a progress comment?"

**Decision tree:**

```
Is work wrapping up AND was a Jira story involved?
├── YES → Ask about status update / comment
│   User says yes → Use transitionJiraIssue or addCommentToJiraIssue
│   User says skip → Done, no update
└── NO story involved → Stay silent
```

**What "wrapping up" looks like:**
- User says "done", "finished", "that's it", "ship it"
- Commit created for the feature/fix
- PR created or ready

## Integration Points

### mcp-atlassian (API Reference)

All Jira operations use tools from mcp-atlassian. Do NOT duplicate API docs here — refer to that skill for:
- Tool catalog and parameters
- Token-saving field filtering
- JQL query patterns
- Comment and transition workflows

**Key tools used by checkpoints:**
- `searchJiraIssuesUsingJql` — Before Work search
- `getJiraIssue` — During Work context fetch
- `transitionJiraIssue` — After Work status update
- `addCommentToJiraIssue` — After Work progress comment
- `getAccessibleAtlassianResources` — Required bootstrap (cloudId)

### task-master (No Overlap)

task-master manages TaskList items and work decomposition. jira-checkpoint never:
- Creates or modifies TaskList items
- Changes task decomposition strategy
- Interferes with delegation patterns

They complement: task-master breaks work down, jira-checkpoint ensures Jira reflects it.

### Vestige (Learning Preferences)

Store user checkpoint preferences via Vestige:

```
User says "skip Jira" repeatedly → smart_ingest preference: "User prefers minimal Jira checkpoints"
User always updates after work   → smart_ingest preference: "User wants post-work Jira sync prompts"
User never wants before-work     → smart_ingest preference: "Skip before-work Jira checkpoint"
```

Check Vestige at session start for stored Jira checkpoint preferences.

## User Control

**Every checkpoint is a question, never a mandate.**

- User can always say "skip Jira", "not now", "no Jira today"
- Preferences accumulate in Vestige — skill adapts over time
- No checkpoint ever blocks work from proceeding
- If user seems annoyed by prompts, reduce frequency and store preference

## Project Configuration

**Default project key:** `FNR`

When searching Jira without a specific issue key, scope to the FNR project:

```
JQL: project = FNR AND summary ~ "keyword" ORDER BY updated DESC
```

## Experimental Status

This skill is built for vetting. Expected evolution:

1. **v1 (now):** Three manual checkpoints with questions
2. **v2 (after feedback):** Adjusted trigger sensitivity based on usage patterns
3. **v3 (if valuable):** Deeper task-master integration (auto-suggest Jira links for TaskList items)

**Feedback signals to watch:**
- How often does the user accept vs skip checkpoints?
- Are before-work searches actually useful?
- Does after-work sync feel natural or forced?
- Is the FNR project scope too narrow?
