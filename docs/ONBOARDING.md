# Team Onboarding Guide

Welcome to ima-claude! This guide helps new team members get started with our Claude Code skills and standards.

## Prerequisites

1. **Claude Code** - The CLI tool from Anthropic
   ```bash
   # Follow instructions at https://claude.ai/code
   ```

2. **bun** - For installation scripts
   ```bash
   curl -fsSL https://bun.sh/install | bash
   ```

3. **Optional: SuperClaude** - Enhanced features
   ```bash
   # https://github.com/SuperClaude-Org/SuperClaude_Framework
   ```

## Installation

```bash
bunx ima-claude install
```

This installs our skills to `~/.claude/skills/`.

## Quick Start

### 1. Understand What Skills Are

Skills are domain-specific guidance that Claude auto-discovers based on your request:

```
"Help me implement a React component with FP patterns"
# → js-fp-react skill auto-loads

"Create a WordPress REST API endpoint"
# → php-fp-wordpress skill auto-loads
```

### 2. Know Your Skills

| Skill | Use For |
|-------|---------|
| `js-fp` | Core JavaScript FP patterns |
| `js-fp-api` | Node.js APIs with security-first SQL |
| `js-fp-react` | React components, hooks, HOCs |
| `js-fp-vue` | Vue 3 composables and wrappers |
| `js-fp-wordpress` | WordPress JS (Bootstrap/jQuery) |
| `php-fp` | Core PHP FP patterns |
| `php-fp-wordpress` | WordPress PHP (security, nonces) |
| `quasar-fp` | Quasar Framework patterns |
| `architect` | System design decisions |
| `docs-organize` | Documentation structure |

### 3. Core Philosophy

All our skills enforce:

1. **Simple > Complex** - Start with the simplest solution
2. **Native > Utilities** - Use language idioms, not FP libraries
3. **MVP > Enterprise** - Build what you need now, evolve later
4. **Evidence > Assumptions** - Measure before optimizing

### 4. Example Workflow

#### Starting a New Feature

```
"I need to implement user authentication for our React app"
```

Claude will:
1. Auto-load `js-fp-react` skill
2. Apply anti-over-engineering principles
3. Suggest pure functions with explicit dependencies
4. Recommend native patterns over libraries

#### Code Review

```
"Review this code using js-fp skill"
```

Claude will check for:
- Unnecessary complexity
- FP utility creation (should use native patterns)
- Mixed side effects and logic
- Appropriate error handling for context

#### Architecture Decisions

```
"As the Architect would, should we use microservices?"
```

Claude will:
- Apply the 4-Question Architecture Test
- Consider simplicity first
- Ask about evidence for complexity
- Suggest the appropriate complexity level

## Team Standards

### Do

- ✅ Start with simple implementations
- ✅ Use native language patterns
- ✅ Separate pure logic from side effects
- ✅ Test edge cases systematically
- ✅ Match complexity to actual requirements

### Don't

- ❌ Create FP utilities (pipe, compose, curry)
- ❌ Add abstractions without evidence of need
- ❌ Apply enterprise patterns to simple problems
- ❌ Optimize without measurements

## Private Skills

For project-specific patterns:

1. Create a skill in `~/.claude/skills/.local/`
2. Add a `SKILL.md` file
3. Reference it: "Use my-project skill"

Example structure:
```
~/.claude/skills/.local/my-company-api/
├── SKILL.md
└── references/
    └── api-conventions.md
```

## Getting Help

1. **Skill Usage**: "How do I use the js-fp-react skill?"
2. **Pattern Questions**: "What does js-fp say about error handling?"
3. **Architecture Help**: "Apply architect principles to this design"

## Keeping Updated

```bash
bunx ima-claude upgrade
```

This preserves your local modifications while updating our skills.

## Common Questions

### Q: Do I need SuperClaude?

No, but it's recommended. SuperClaude adds:
- Persona auto-activation
- MCP server coordination
- Advanced flags and modes

Skills work fully standalone without SuperClaude.

### Q: What if skills conflict with project patterns?

Create a project-specific skill in `.local/` that references and extends our skills:

```markdown
---
name: "my-project-patterns"
---

# My Project Patterns

Extends js-fp with project-specific conventions:

## Import Order
1. React imports
2. Third-party libraries
3. Our components
4. Styles
```

### Q: Can I modify installed skills?

Yes, but:
- Local changes are preserved during upgrades
- Consider creating an extending skill instead
- Submit improvements back to the team
