---
name: mcp-context7
description: Use Context7 MCP for official library documentation, framework APIs, best practices, code examples. Triggers on library/framework questions like 'how to use [library]', 'show [library] example', '[library] docs', '[library] API', or framework names (React, Vue, Quasar, Next.js, Express, Fastify, Prisma, tRPC, Zod, Tailwind, etc). Also triggers on import statements detected in code or package.json library lookups. Provides 70-80% token savings over web searching.
---

# Context7 MCP - Library Documentation

Use Context7 for official library documentation instead of web searching or guessing APIs.

## MCP Tools

| Tool | Purpose |
|------|---------|
| `mcp__context7__search` | Search for libraries and get documentation |

## Basic Usage

Context7 combines library resolution and documentation retrieval into a single tool.

```
mcp__context7__search
  query: "How to use QDialog component in Quasar"
```

**Parameters**:
- `query` (required): Your question or search query including the library name

The tool will:
1. Identify the library from your query
2. Find the relevant documentation
3. Return focused, relevant docs

## Query Optimization

**Be specific and include**:
- Component/function names: "QDialog component API props events slots"
- What you want to do: "How to set up authentication with JWT"
- Context: "React useState hook example with TypeScript"

**Good queries**:
| Query | Why It's Good |
|-------|---------------|
| "Quasar QDialog props and events" | Specific component, clear intent |
| "React useEffect cleanup function" | Specific hook, specific aspect |
| "Prisma findMany where clause syntax" | Specific method, specific feature |
| "Express middleware error handling" | Framework + feature |

**Avoid vague queries**:
- ❌ "How does Quasar work?"
- ✅ "How to create a Quasar button with icon"

## Decision Logic

```
IF question about library/framework API:
    → Use Context7
ELSE IF import statement detected AND user asks about that library:
    → Use Context7
ELSE IF general programming concept (closures, promises, etc.):
    → Use native Claude knowledge
ELSE IF library not found:
    → Fallback to WebSearch or Tavily
ELSE IF asking for "latest" or "new" features post-cutoff:
    → Use Tavily instead
```

## When NOT to Use

- General programming questions (no specific library)
- Debugging code that doesn't involve library APIs
- Simple syntax questions Claude already knows
- User wants current/latest info post-cutoff (use Tavily instead)

## Common Libraries Supported

**Frontend**: React, Vue, Quasar, Next.js, Nuxt, Svelte, Angular, Tailwind, Bootstrap
**Backend**: Express, Fastify, Nest.js, tRPC, Prisma, Sequelize, TypeORM
**Utilities**: Lodash, Ramda, date-fns, Zod, Yup, Joi
**Build**: Vite, Webpack, Rollup, ESBuild
**Testing**: Jest, Vitest, Playwright, Cypress

## Examples

| User Request | Action |
|--------------|--------|
| "How to use QDialog in Vue?" | search(query: "QDialog component Quasar Vue") |
| "React useState example" | search(query: "React useState hook example") |
| "Prisma query syntax" | search(query: "Prisma findMany where query") |
| "What's a closure?" | Native Claude (no library) |
| "Latest React 19 features" | Use Tavily (current info needed) |

## Multiple Queries

If initial results aren't sufficient, refine your query:
1. First attempt: "Quasar form validation"
2. If needed: "Quasar QForm validation rules API"
3. If needed: "Quasar field validation with Vuelidate"

## Setup

No API key required. Install with:
```bash
bun run scripts/setup-mcp.ts
```

Or manually:
```bash
claude mcp add --scope user context7 -- npx -y @upstash/context7-mcp@latest
```
