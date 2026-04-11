---
name: mcp-context7
description: Use Context7 MCP for official library documentation, framework APIs, best practices, code examples. Triggers on library/framework questions like 'how to use [library]', 'show [library] example', '[library] docs', '[library] API', or framework names (React, Vue, Quasar, Next.js, Express, Fastify, Prisma, tRPC, Zod, Tailwind, etc). Also triggers on import statements detected in code or package.json library lookups. Provides 70-80% token savings over web searching.
---

# Context7 MCP - Library Documentation

Use Context7 for official library docs instead of web searching or guessing APIs.

## Tool

| Tool | Purpose |
|------|---------|
| `mcp__context7__search` | Search libraries and retrieve documentation |

```
mcp__context7__search
  query: "How to use QDialog component in Quasar"
```

## Query Optimization

Include component/function name + what you want to do + context. Be specific.

| Good Query | Why |
|------------|-----|
| "Quasar QDialog props and events" | Specific component, clear intent |
| "React useEffect cleanup function" | Specific hook + aspect |
| "Prisma findMany where clause syntax" | Specific method + feature |
| "Express middleware error handling" | Framework + feature |

Avoid: "How does Quasar work?" — use: "How to create a Quasar button with icon"

## Decision Logic

```
IF library/framework API question → Context7
IF import detected AND user asks about that library → Context7
IF general programming concept (closures, promises) → native Claude knowledge
IF library not found → fallback to Tavily
IF "latest" / post-cutoff features → Tavily instead
```

## When NOT to Use

- No specific library involved
- Debugging business logic (no library APIs)
- Simple syntax Claude already knows
- Current/latest info post-cutoff → use Tavily

## Supported Libraries

**Frontend**: React, Vue, Quasar, Next.js, Nuxt, Svelte, Angular, Tailwind, Bootstrap  
**Backend**: Express, Fastify, Nest.js, tRPC, Prisma, Sequelize, TypeORM  
**Utilities**: Lodash, Ramda, date-fns, Zod, Yup, Joi  
**Build**: Vite, Webpack, Rollup, ESBuild  
**Testing**: Jest, Vitest, Playwright, Cypress

## Examples

| Request | Action |
|---------|--------|
| "How to use QDialog in Vue?" | `search("QDialog component Quasar Vue")` |
| "React useState example" | `search("React useState hook example")` |
| "Prisma query syntax" | `search("Prisma findMany where query")` |
| "What's a closure?" | Native Claude |
| "Latest React 19 features" | Tavily |

If initial results insufficient, refine: "Quasar form validation" → "Quasar QForm validation rules API"

## Setup

```bash
bun run scripts/setup-mcp.ts
# or manually:
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp@latest
```
