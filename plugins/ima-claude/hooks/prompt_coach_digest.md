# IMA Skills Digest for Prompt Coaching

## Skill Triggers

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
| WP-CLI, DDEV, ddev wp, wp plugin, wp db query | `wp-ddev` (DDEV) or `wp-local` (Flywheel) |
| Find in files, search code, grep | `rg` |
| Latest, current, 2025/2026, recent updates, research | `mcp-tavily` |
| Library docs, React API, how to use [library] | `mcp-context7` |
| Find references, rename symbol, refactor, what calls X | `mcp-serena` |
| Think through, step by step, debug, complex problem | `mcp-sequential` |
| Remember this, save preference, architectural decision | `mcp-vestige` |
| IMA Forms, form validation, repeater field | `ima-forms-expert` |
| Analyze skill, audit skill, skill review | `skill-analyzer` |
| Create skill, build skill, skill template | `skill-creator` |

## Anti-Patterns (flag these)

- **FP Utilities**: custom pipe/compose/curry/partial → use native patterns
- **Over-Engineering**: "make generic", "add wrapper", "create utility" without evidence
- **Premature Abstraction**: helpers before 3+ genuine reuses
- **Security Gaps**: raw SQL, missing nonces (WP), unsanitized input, hardcoded secrets
- **Wrong Tool**: grep→rg, WebSearch→mcp-tavily, Read files→mcp-serena

## Philosophy

Simple > Complex. Evidence > Assumptions. Specific > Generic. Add complexity only when proven needed.

## Stay Silent When

- Prompt names a skill
- Clear, specific requirements
- Bug fix with reproduction steps
- Exploring/reading without modification
- Simple follow-ups
