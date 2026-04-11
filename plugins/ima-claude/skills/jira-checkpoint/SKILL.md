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

```
task-master      = "How do I organize my work?"    (execution, tactical)
jira-checkpoint  = "Does the team know?"           (visibility, strategic)
mcp-atlassian    = "How do I talk to Jira's API?"  (implementation, reference)
```

Each skill stays in its lane. jira-checkpoint never touches TaskList, decomposition, or delegation.

## The Three Checkpoints

### 1. Before Work

**Trigger**: User starts significant work — "let's implement", "build the", "fix the", "work on FNR-".

Ask: `"Should I search Jira (FNR project) for related stories before we start?"`

```
Significant work (feature, bug fix, multi-file refactor)?
├── YES → Ask about Jira search
│   yes → searchJiraIssuesUsingJql (FNR project)
│   skip → proceed
└── NO (utility function, config tweak, lint fix) → stay silent
```

### 2. During Work

**Trigger**: User mentions an issue key (e.g., `FNR-123`).

Auto-fetch and surface:
```
Detected FNR-123. Fetching story context...
→ Summary
→ Acceptance criteria
→ Status | Assignee
```

Use `getJiraIssue` with fields: `summary,description,status,assignee,customfield_10016`. Don't re-fetch if already retrieved this session.

### 3. After Work

**Trigger**: Work wraps up AND a Jira story was referenced (user says "done"/"finished"/"ship it", commit created, PR ready).

Ask: `"We referenced FNR-123 during this work. Want to update its status or add a progress comment?"`

```
Work wrapping up AND Jira story was involved?
├── YES → Ask about status update / comment
│   yes → transitionJiraIssue or addCommentToJiraIssue
│   skip → done
└── NO story involved → stay silent
```

## Key Tools

| Tool | Checkpoint |
|------|-----------|
| `searchJiraIssuesUsingJql` | Before Work |
| `getJiraIssue` | During Work |
| `transitionJiraIssue` | After Work |
| `addCommentToJiraIssue` | After Work |
| `getAccessibleAtlassianResources` | Required bootstrap (cloudId) |

See `mcp-atlassian` for field filtering patterns and JQL.

## Project Config

**Default project**: `FNR`

```
JQL: project = FNR AND summary ~ "keyword" ORDER BY updated DESC
```

## User Control

Every checkpoint is a question, never a mandate. Store preferences via Vestige `smart_ingest`:

```
"skip Jira" repeatedly         → "User prefers minimal Jira checkpoints"
always updates after work      → "User wants post-work Jira sync prompts"
never wants before-work prompt → "Skip before-work Jira checkpoint"
```

Check Vestige at session start for stored preferences.
