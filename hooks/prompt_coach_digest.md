# IMA Skills Digest for Prompt Coaching

## Skill Triggers (suggest when prompt matches)

| Prompt Contains | Suggest |
|----------------|---------|
| React, hooks, useCallback, component optimization | `js-fp-react` |
| Vue 3, composable, Composition API | `js-fp-vue` |
| Quasar, QBtn, QCard, q-pa-, utility classes | `quasar-fp` |
| Node.js API, REST, middleware, route handlers | `js-fp-api` |
| WordPress JavaScript, jQuery, AJAX, Gravity Forms | `js-fp-wordpress` |
| PHP function, pure functions, composition | `php-fp` |
| WordPress plugin, nonce, sanitization, capability | `php-fp-wordpress` |
| Architecture, new project, scaling, microservices | `architect` |
| Documentation structure, organize docs | `docs-organize` |
| WP-CLI, Local WP, wp plugin, wp db query | `wp-local` |
| Find in files, search code, grep | `rg` |
| Latest, current, 2025/2026, recent updates, research | `mcp-tavily` |
| Library docs, React API, how to use [library] | `mcp-context7` |
| Find references, rename symbol, refactor, what calls X | `mcp-serena` |
| Think through, step by step, debug, complex problem | `mcp-sequential` |
| Remember this, save preference, architectural decision | `mcp-memory` |
| IMA Forms, form validation, repeater field | `ima-forms-expert` |
| Analyze skill, audit skill, skill review | `skill-analyzer` |
| Create skill, build skill, skill template | `skill-creator` |

## Core Anti-Patterns (flag these)

**FP Utilities**: Creating custom pipe/compose/curry/partial - use native patterns
**Over-Engineering**: "make it generic", "add wrapper", "create utility" without evidence
**Premature Abstraction**: Extracting helpers before 3+ genuine reuses
**Security Gaps**: Raw SQL, missing nonces (WP), unsanitized input, hardcoded secrets
**Wrong Tool**: grep instead of rg, WebSearch instead of mcp-tavily, reading files instead of mcp-serena

## Team Philosophy

- Simple > Complex
- Native patterns > Custom utilities
- MVP > Enterprise
- Specific > Generic (generalize with evidence)
- Start small, add complexity when needed

## When Skills Already Apply (stay silent)

- Prompt mentions a skill by name
- Prompt has clear, specific requirements
- Bug fix with reproduction steps
- Exploring/reading code without modification
- Simple follow-ups
