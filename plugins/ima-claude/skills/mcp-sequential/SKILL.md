---
name: "mcp-sequential"
description: "Sequential Thinking MCP — use for debugging, root cause analysis, trade-off evaluation, architectural decisions, and any multi-step problem where the approach may need revision mid-stream. Triggers on: think through, step by step, debug this, figure out why, what's causing, root cause, troubleshoot, analyze, trade-offs, pros and cons, why is this failing, complex problem, design decision, how should we approach. Prevents expensive trial-and-error by structuring reasoning before acting."
---

# Sequential Thinking MCP - Structured Reasoning

Use for: debugging, root cause analysis, trade-off evaluation, architectural decisions, multi-step problems requiring mid-stream revision.

Skip for: simple tasks, obvious answers, single-step operations.

## Tool

| Tool | Purpose |
|------|---------|
| `mcp__sequential-thinking__sequentialThinking` | Execute one thought in a reasoning chain |

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `thought` | Yes | Current thinking step |
| `nextThoughtNeeded` | Yes | `true` to continue, `false` when done |
| `thoughtNumber` | Yes | Current step (1, 2, 3...) |
| `totalThoughts` | Yes | Estimated total — adjust freely |
| `isRevision` | No | `true` if revising a previous thought |
| `revisesThought` | No | Which thought number being revised |
| `branchFromThought` | No | Branch point thought number |
| `branchId` | No | Branch identifier |

## Usage Patterns

### Start chain
```
mcp__sequential-thinking__sequentialThinking
  thought: "The bug report says form submits but data isn't saved. Failure points: frontend validation, AJAX request, backend handler, DB write."
  nextThoughtNeeded: true
  thoughtNumber: 1
  totalThoughts: 5
```

### Continue
```
mcp__sequential-thinking__sequentialThinking
  thought: "Based on step 1, checking AJAX request first..."
  nextThoughtNeeded: true
  thoughtNumber: 2
  totalThoughts: 5
```

### Revise
```
mcp__sequential-thinking__sequentialThinking
  thought: "My assumption in thought 2 was wrong. Reconsidering..."
  nextThoughtNeeded: true
  thoughtNumber: 3
  totalThoughts: 6
  isRevision: true
  revisesThought: 2
```

### Branch for alternatives
```
mcp__sequential-thinking__sequentialThinking
  thought: "Exploring alternative approach from step 2..."
  nextThoughtNeeded: true
  thoughtNumber: 4
  totalThoughts: 7
  branchFromThought: 2
  branchId: "alternative-approach"
```

### Conclude
```
mcp__sequential-thinking__sequentialThinking
  thought: "Root cause: field name mismatch — frontend sends 'user_email', backend expects 'email'."
  nextThoughtNeeded: false
  thoughtNumber: 5
  totalThoughts: 5
```

## Best Practices

- Adjust `totalThoughts` freely — it's an estimate
- Express uncertainty inline: "I'm not sure, but..."
- Revise with `isRevision` when understanding changes
- Keep `nextThoughtNeeded: true` until confident
- Branch to compare approaches, not just to explore

## Setup

```bash
claude mcp add --scope user sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking@latest
```
