# Migrating from Commands to Skills

If you were using the old `/fp:*` command system, this guide helps you transition to the new Skills-based approach.

## Why the Change?

### Commands (Old)
- Required manual invocation: `/fp:react UserComponent`
- Loaded entire command file each time
- Depended on SuperClaude routing
- Required remembering command names

### Skills (New)
- Auto-discovered by context
- Progressive loading (only what's needed)
- Works standalone without SuperClaude
- Always available across sessions

## Migration Reference

### Domain Commands → Skills

| Old Command | New Skill | How to Invoke |
|-------------|-----------|---------------|
| `/fp:core` | `js-fp` | Mention JavaScript FP patterns |
| `/fp:api` | `js-fp-api` | Mention API, Node.js, endpoints |
| `/fp:react` | `js-fp-react` | Mention React, components, hooks |
| `/fp:vue` | `js-fp-vue` | Mention Vue, composables |
| `/fp:wordpress` | `php-fp-wordpress` | Mention WordPress, PHP |

### Orchestration Commands

These don't have direct skill equivalents - they're now just natural requests:

| Old Command | New Approach |
|-------------|--------------|
| `/fp:implement` | "Implement this feature with FP patterns" |
| `/fp:workflow` | "Create a workflow for implementing X" |
| `/fp:design` | "Design the architecture for X" |
| `/fp:cleanup` | "Clean up this code following FP principles" |

### Utility Commands

| Old Command | New Approach |
|-------------|--------------|
| `/fp:document` | "Document this code" (docs-organize skill) |
| `/fp:explain` | "Explain this code using FP principles" |
| `/fp:troubleshoot` | "Debug this issue with FP analysis" |

## Before and After Examples

### React Component

**Before:**
```
/fp:react UserProfile --type component --pattern pure
```

**After:**
```
"Create a React component for UserProfile following FP patterns"
```

The js-fp-react skill auto-activates and provides the same guidance.

### API Endpoint

**Before:**
```
/fp:api user-authentication --method POST --security
```

**After:**
```
"Implement a user authentication API endpoint with security-first patterns"
```

The js-fp-api skill auto-activates with its security-first SQL patterns.

### Code Review

**Before:**
```
/fp:analyze --focus quality
```

**After:**
```
"Review this code using js-fp principles"
```

Or simply:
```
"Review this code for FP patterns and potential over-engineering"
```

### Architecture Decision

**Before:**
```
/fp:design --pattern architectural
```

**After:**
```
"Apply architect skill to evaluate this design decision"
```

## Explicit Skill Invocation

If you want to explicitly load a skill:

```
"Use the js-fp skill to review this code"
"Apply js-fp-react patterns to this component"
"What does php-fp-wordpress say about form handling?"
```

## Behavioral Differences

### Auto-Discovery
Skills now auto-activate based on context. You don't need to remember command names.

### Progressive Loading
Only the relevant parts of a skill load, reducing context usage.

### Always Available
Skills persist across sessions. No need to re-invoke commands.

### Standalone Operation
Skills work without SuperClaude. Commands required SuperClaude routing.

## FAQ

### Q: What happened to the lean/think variants?

**A:** Removed. Claude now handles complexity detection automatically. Just describe what you need.

### Q: What about SuperClaude integration?

**A:** Skills work with or without SuperClaude. With SuperClaude, you get persona auto-activation and MCP coordination. Without, skills provide the same expertise.

### Q: Can I still use commands?

**A:** The old commands are archived in `archive/commands/fp/` for reference, but they're not loaded. Use skills instead.

### Q: What about my custom commands?

**A:** Convert them to skills! Use the `skill-creator` skill:
```
"Use skill-creator to convert my custom command to a skill"
```

## Archived Commands

The old commands are preserved in:
```
ima-claude/archive/commands/fp/
```

Use them as reference for understanding the patterns, but don't rely on them for functionality.

## Getting Help

```
"How do I use skills instead of the old /fp:* commands?"
```

Or consult the [SKILLS-USER-GUIDE.md](SKILLS-USER-GUIDE.md) for comprehensive skill documentation.
