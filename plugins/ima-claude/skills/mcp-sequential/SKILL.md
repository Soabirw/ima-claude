---
name: "mcp-sequential"
description: "Sequential Thinking MCP — use for debugging, root cause analysis, trade-off evaluation, architectural decisions, and any multi-step problem where the approach may need revision mid-stream. Triggers on: think through, step by step, debug this, figure out why, what's causing, root cause, troubleshoot, analyze, trade-offs, pros and cons, why is this failing, complex problem, design decision, how should we approach. Prevents expensive trial-and-error by structuring reasoning before acting."
---

# Sequential Thinking MCP - Structured Reasoning

Use Sequential Thinking for complex problems that benefit from structured, revisable analysis.

## Available Tool

| Tool | Purpose |
|------|---------|
| `mcp__sequential-thinking__sequentialThinking` | Execute a thought in a reasoning chain |

## When to Use

**Use Sequential Thinking for:**
- Breaking down complex problems into steps
- Debugging issues where the cause isn't obvious
- Architectural/design decisions with trade-offs
- Problems where you might need to revise your approach
- Multi-step analysis that needs context maintained
- Filtering irrelevant information from complex scenarios
- Hypothesis generation and verification

**Don't use for:**
- Simple, straightforward tasks
- Questions with obvious answers
- Tasks that don't require multi-step reasoning

## Basic Usage

Each call represents one thought in your reasoning chain.

```
mcp__sequential-thinking__sequentialThinking
  thought: "First, let me understand the problem. We have X happening when Y..."
  nextThoughtNeeded: true
  thoughtNumber: 1
  totalThoughts: 5
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `thought` | Yes | Current thinking step content |
| `nextThoughtNeeded` | Yes | `true` to continue, `false` when done |
| `thoughtNumber` | Yes | Current step number (1, 2, 3...) |
| `totalThoughts` | Yes | Estimated total (can adjust up/down) |
| `isRevision` | No | `true` if revising previous thought |
| `revisesThought` | No | Which thought number being revised |
| `branchFromThought` | No | Thought number to branch from |
| `branchId` | No | Identifier for the branch |

## Continue Chain

```
mcp__sequential-thinking__sequentialThinking
  thought: "Based on step 1, the likely cause is Z because..."
  nextThoughtNeeded: true
  thoughtNumber: 2
  totalThoughts: 5
```

## Revise if Needed

```
mcp__sequential-thinking__sequentialThinking
  thought: "Actually, my assumption in thought 2 was wrong. Let me reconsider..."
  nextThoughtNeeded: true
  thoughtNumber: 3
  totalThoughts: 6
  isRevision: true
  revisesThought: 2
```

## Branch for Alternatives

```
mcp__sequential-thinking__sequentialThinking
  thought: "Let me explore an alternative approach from step 2..."
  nextThoughtNeeded: true
  thoughtNumber: 4
  totalThoughts: 7
  branchFromThought: 2
  branchId: "alternative-approach"
```

## Conclude

```
mcp__sequential-thinking__sequentialThinking
  thought: "Based on my analysis, the solution is X because of Y and Z."
  nextThoughtNeeded: false
  thoughtNumber: 5
  totalThoughts: 5
```

## Best Practices

1. **Start with estimate, adjust as needed** - `totalThoughts` is flexible
2. **Express uncertainty** - It's OK to say "I'm not sure, but..."
3. **Revise freely** - Use `isRevision` when your understanding changes
4. **Branch for alternatives** - Explore multiple approaches
5. **Verify hypotheses** - Don't just guess, test your reasoning
6. **Filter noise** - Focus on relevant information per step
7. **Only conclude when confident** - Keep `nextThoughtNeeded: true` until satisfied

## Example: Debugging a Bug

```
Thought 1: "The bug report says the form submits but data isn't saved. Let me identify possible failure points: 1) Frontend validation, 2) AJAX request, 3) Backend handler, 4) Database write."

Thought 2: "Starting with the AJAX request - I should check if the request is being sent and what response comes back."

Thought 3: "The request is sent but returns 500. So the issue is backend. Let me check the error logs."

Thought 4: "Error log shows 'undefined index: email'. The frontend is sending 'user_email' but backend expects 'email'. This is a field name mismatch."

Thought 5 (conclusion): "Root cause: Field name mismatch between frontend ('user_email') and backend ('email'). Solution: Update frontend to use 'email' or backend to accept 'user_email'."
```

## Example: Architecture Decision

```
Thought 1: "Need to decide between REST API and GraphQL for this project. Let me list the requirements: multiple clients, varying data needs, team experience."

Thought 2: "REST pros: Team knows it well, simple caching, established patterns. Cons: Over-fetching for mobile, multiple endpoints."

Thought 3: "GraphQL pros: Single endpoint, client specifies data needs, good for mobile. Cons: Learning curve, caching complexity."

Thought 4 (revision): "Wait, I should also consider that we're using WordPress backend. REST is native to WordPress, GraphQL would need WPGraphQL plugin."

Thought 5 (conclusion): "Recommendation: REST API. Reasons: 1) Native WordPress support, 2) Team expertise, 3) Simpler caching. The over-fetching concern can be mitigated with sparse fieldsets."
```

## Setup

No API key required. Install with:
```bash
bun run scripts/setup-mcp.ts
```

Or manually:
```bash
claude mcp add --scope user sequential-thinking -- npx -y @modelcontextprotocol/server-sequential-thinking@latest
```
