---
name: "compound-bridge"
description: "Compound Engineering integration — memory bridge (Compound → Vestige/Qdrant), Vestige → Compound research, role separation (plan vs task-master), per-project config template. Triggers when Compound workflows complete or when orchestrating plan/review workflows. Triggers on: /workflows:compound, /workflows:plan, /workflows:review, compound engineering, compound-engineering.local."
---

# Compound Bridge — Compound Engineering + ima-claude Integration

Minimal connective tissue between Compound Engineering (structured workflows) and ima-claude (coding standards + memory).

## Memory Bridge: Compound → Vestige/Qdrant

After Compound workflow events, store insights automatically:

| After This Event | Store This | Where |
|---|---|---|
| `/workflows:compound` writes solution | Root cause + key insight (1-2 sentences) | Vestige `smart_ingest`, node_type: `pattern` |
| `/workflows:compound` writes solution (>500 words) | Full solution content | Qdrant `qdrant-store`, collection: `compound-solutions` |
| `/workflows:plan` completes with research | Key decisions + approach chosen | Vestige `smart_ingest`, node_type: `decision` |
| `/workflows:review` finds P1/P2 issues | Pattern summary of findings | Vestige `smart_ingest`, node_type: `pattern` |

```
# Vestige (all solutions)
mcp__vestige__smart_ingest
  content: "Root cause: {cause}. Fix: {approach}. Key insight: {learning}"
  node_type: "pattern"

# Qdrant (large solutions only)
mcp__qdrant-memory__qdrant-store
  information: "{full solution content}"
  metadata: {"type": "compound-solution", "source": "docs/solutions/{filename}"}
```

## Memory Bridge: Vestige → Compound Research

Before/alongside `/workflows:plan`, search Vestige:

```
mcp__vestige__search query: "{feature keywords}" limit: 5
```

Include results marked as cross-project provenance:

```markdown
### Prior Knowledge (Cross-Project — Vestige)
- {vestige result 1}

### Prior Solutions (Project — docs/solutions/)
- {learnings-researcher results}
```

## Role Separation: Planning

| Need | Use |
|---|---|
| Formal feature planning with research | `/workflows:plan` |
| Ad-hoc work breakdown during implementation | `task-master` |
| Breaking a plan into executable tasks | Both |

task-master principles that apply inside `/workflows:work`:
- Two-level max agent delegation
- Sonnet for execution, Opus for orchestration
- Minimal context for subagents
- Vertical decomposition for sequential, horizontal for parallel

## Per-Project Config: `compound-engineering.local.md`

Create in project roots where both systems are used. Commit it early — it's persistent config, not a transient artifact.

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

Create when: project uses both ima-claude AND Compound workflows, or before first `/workflows:review`. Don't create for single-system projects.

## Artifact Resilience

Compound writes artifacts to working tree (`docs/brainstorms/`, `docs/plans/`, `docs/solutions/`, `todos/`) but doesn't commit them. Branch switches destroy them. Context compaction loses references.

### Rule 1: Shadow Copy to `.claude/compound/`

After every workflow artifact write, copy to `.claude/compound/`:

```bash
cp docs/brainstorms/{file}.md .claude/compound/brainstorms/{file}.md
cp docs/plans/{file}.md .claude/compound/plans/{file}.md
cp docs/solutions/{category}/{file}.md .claude/compound/solutions/{category}/{file}.md
cp todos/{file}.md .claude/compound/todos/{file}.md
```

Also shadow-copy on checkbox updates (`- [ ]` → `- [x]`). `.claude/` is gitignored and survives branch switches.

### Rule 2: Eager Memory Bridge

Store immediately after each artifact write, not at workflow completion:

| After Writing | Store Immediately |
|---|---|
| Brainstorm | Vestige `smart_ingest`: key decisions + open questions, node_type: `decision` |
| Plan | Vestige `smart_ingest`: approach + task list summary, node_type: `decision` |
| Plan checkbox update | Vestige `smart_ingest`: progress snapshot (X of Y tasks done), node_type: `observation` |
| Review todo | Vestige `smart_ingest`: finding summary + priority, node_type: `pattern` |
| Solution | Vestige + Qdrant (per rules above) |

### Rule 3: Pre-Branch-Switch Checkpoint

Before any `git checkout`, `git switch`, or worktree operation during a Compound workflow:

1. Verify all artifacts have shadow copies in `.claude/compound/`
2. Create any missing copies
3. Vestige `smart_ingest`: current workflow state (phase, done, next), node_type: `observation`

### Rule 4: Recovery

If artifacts are lost: check `.claude/compound/` → restore to working-tree locations → check Vestige for latest state snapshot → resume.

## What This Skill Does NOT Do

- Modify the Compound Engineering plugin
- Create custom scripts or utilities
- Add new MCP servers
- Force workflows — both systems remain independently functional
