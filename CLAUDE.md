# ima-claude Entry Point

IMA's Claude Code Skills for functional programming, architecture, and team standards.

## Available Skills

### FP Skills (Auto-discovered by domain)
- `js-fp` - JavaScript FP core (anti-over-engineering, native patterns)
- `js-fp-api` - Node.js API patterns (security-first SQL, middleware DI)
- `js-fp-react` - React FP patterns (hooks, HOCs, pure components)
- `js-fp-vue` - Vue 3 FP patterns (composables, wrappers)
- `js-fp-wordpress` - WordPress JS (Bootstrap/jQuery, pure business logic)
- `php-fp` - PHP FP core (strict types, native patterns)
- `php-fp-wordpress` - WordPress PHP (security-first, nonce verification)
- `quasar-fp` - Quasar Framework (utility-first CSS, composables)

### Domain Expert Skills
- `architect` - System design, scalability, long-term architecture
- `docs-organize` - Three-tier documentation (Active/Archive/Transient)

### Meta Skills
- `skill-analyzer` - Analyze and improve skills
- `skill-creator` - Create new skills

## Core Philosophy

**"Simple solutions > Complex abstractions | Native patterns > Utilities | MVP > Enterprise"**

All skills enforce:
1. **Anti-over-engineering** - Start simple, add complexity only with evidence
2. **Native patterns** - Use language idioms, not FP utilities
3. **Testability** - Pure functions enable comprehensive testing
4. **Context-appropriate** - CLI script ≠ production service

## Usage

Skills auto-activate based on context. Mention the domain and relevant skills load:

```
"Implement a React component with custom hooks"
# → js-fp-react auto-loads

"Create a WordPress REST API endpoint"
# → php-fp-wordpress auto-loads
```

Or explicitly invoke:

```
"Use the js-fp skill to review this validation logic"
```

## Personalities (Optional)

Fun themed response styles (tone only, no expertise change):

```
"Enable 40k mode"  # Warhammer 40K themed
"Enable templars"  # Templar crusader themed
```

## Integration with SuperClaude

If SuperClaude is installed, these skills integrate with:
- Persona auto-activation (`--persona-functional`)
- MCP server coordination (Context7, Sequential)
- Quality gates and validation

Without SuperClaude, skills work independently with full functionality.
