---
name: "compound-bridge"
description: "Compound Engineering integration — memory bridge (Compound → Vestige/Qdrant), Vestige → Compound research, role separation (plan vs task-master), per-project config template. Triggers when Compound workflows complete or when orchestrating plan/review workflows."
triggers:
  - "/workflows:compound"
  - "/workflows:plan"
  - "/workflows:review"
  - "compound engineering"
  - "compound-engineering.local"
---

# Compound Bridge — Compound Engineering + ima-claude Integration

Minimal connective tissue between Compound Engineering (structured workflows) and ima-claude (coding standards + memory). Removing this skill returns both systems to standalone behavior.

## Memory Bridge: Compound → Vestige/Qdrant

After Compound workflow events, **automatically store insights** without being asked:

| After This Event | Store This | Where |
|---|---|---|
| `/workflows:compound` writes a solution | Root cause + key insight (1-2 sentences) | Vestige `smart_ingest`, node_type: `pattern` |
| `/workflows:compound` writes a solution (>500 words) | Full solution content | Qdrant `qdrant-store`, collection: `compound-solutions` |
| `/workflows:plan` completes with research | Key decisions + approach chosen | Vestige `smart_ingest`, node_type: `decision` |
| `/workflows:review` finds P1/P2 issues | Pattern summary of findings | Vestige `smart_ingest`, node_type: `pattern` |

### Compound → Vestige Example

After `/workflows:compound` finishes writing to `docs/solutions/`:

```
mcp__vestige__smart_ingest
  content: "Root cause: {concise root cause}. Fix: {approach taken}. Key insight: {what we learned}"
  node_type: "pattern"
```

### Compound → Qdrant Example (Large Solutions)

For solutions over ~500 words, also store the full document in Qdrant for RAG retrieval:

```
mcp__qdrant-memory__qdrant-store
  information: "{full solution content}"
  metadata: {"type": "compound-solution", "source": "docs/solutions/{filename}"}
```

## Memory Bridge: Vestige → Compound Research

When orchestrating `/workflows:plan`, **search Vestige before/alongside** the learnings-researcher agent:

```
mcp__vestige__search query: "{feature keywords}" limit: 5
```

Include Vestige results alongside file-based learnings, marked as cross-project provenance:

```markdown
### Prior Knowledge (Cross-Project — Vestige)
- {vestige result 1}
- {vestige result 2}

### Prior Solutions (Project — docs/solutions/)
- {learnings-researcher results}
```

This supplements but does not replace the learnings-researcher's `docs/solutions/` grep.

## Role Separation: Planning

Both `task-master` and `/workflows:plan` handle planning. They have different lanes:

| Need | Use | Why |
|---|---|---|
| Formal feature planning with research | `/workflows:plan` | Research agents, structured documentation, living plan file |
| Ad-hoc work breakdown during implementation | `task-master` | Decomposition patterns, storage strategy, agent delegation |
| Breaking a plan into executable tasks | Both | Plan creates the doc; task-master principles guide breakdown |

### task-master Principles That Enhance Compound Workflows

These apply when `/workflows:work` creates its task list:

- **Two-level max** agent delegation (Compound's swarm already respects this)
- **Model selection**: Sonnet for execution, Opus for orchestration
- **Minimal context principle** for subagents — only include what they need
- **Vertical decomposition** for sequential work, **horizontal** for parallel

## Per-Project Config: `compound-engineering.local.md`

Create this file in project roots where both systems are used. It tells Compound's review agents about our coding standards.

### Template

```markdown
---
review_agents:
  - code-simplicity-reviewer
  - security-sentinel
  - performance-oracle
  - kieran-typescript-reviewer
  - kieran-python-reviewer
  - architecture-strategist
  - pattern-recognition-specialist
  - julik-frontend-races-reviewer
  - agent-native-reviewer
---

## Coding Standards (ima-claude)

FP-first: pure functions, composition, immutability. Anti-over-engineering: YAGNI strictly, boring code wins. Native patterns only — no custom pipe/compose/curry utilities.

Language skills auto-activate by context:
- JavaScript: js-fp | PHP: php-fp | Vue: js-fp-vue | React: js-fp-react
- WordPress JS: js-fp-wordpress, jquery | WordPress PHP: php-fp-wordpress
- Quasar: quasar-fp | Bootstrap: ima-bootstrap

## Work Decomposition (task-master)

- Two-level max agent delegation
- Sonnet for execution, Opus for orchestration
- Minimal context principle for subagents
```

### When to Create

Create `compound-engineering.local.md` when:
- A project uses both ima-claude skills AND Compound Engineering workflows
- You're about to run `/workflows:review` for the first time in a project

Don't create it for projects that only use one system.

## What Works Without This Skill

These integrate naturally — no bridge needed:

- ima-claude language/FP skills auto-activate during `/workflows:work` by file type
- Compound's research agents (learnings-researcher, best-practices-researcher) fill gaps ima-claude doesn't cover
- Compound's 15 specialized review agents complement our FP-focused standards
- Compound's brainstorm workflow is genuinely new capability

## What This Skill Does NOT Do

- Modify the Compound Engineering plugin — it stays as-is from the marketplace
- Create custom scripts or utilities — all integration is skill instructions
- Add new MCP servers — uses existing Vestige, Qdrant, Serena
- Force workflows — both systems remain independently functional
