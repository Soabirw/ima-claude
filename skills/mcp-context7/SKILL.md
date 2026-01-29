---
name: mcp-context7
description: Use Context7 MCP for official library documentation, framework APIs, best practices, code examples. Triggers on library/framework questions like 'how to use [library]', 'show [library] example', '[library] docs', '[library] API', or framework names (React, Vue, Quasar, Next.js, Express, Fastify, Prisma, tRPC, Zod, Tailwind, etc). Also triggers on import statements detected in code or package.json library lookups. Provides 70-80% token savings over web searching.
---

# Context7 MCP - Library Documentation

Use Context7 for official library documentation instead of web searching or guessing APIs.

## Setup: Airis Gateway

Context7 runs through the Airis MCP gateway. The server may be "cold" (not loaded) initially.

**Tool access pattern**: `mcp__airis-mcp-gateway__airis-exec` with `tool: "context7:tool-name"`

## MCP Tools

| Tool | Purpose |
|------|---------|
| `context7:resolve-library-id` | Find Context7-compatible library ID from name |
| `context7:query-docs` | Get curated docs with specific topic focus |

## Workflow

### 1. Check if Server is Loaded (Optional)

If you get errors, the server may be cold. Load it first:
```
mcp__airis-mcp-gateway__airis-find
  server: "context7"
  query: "resolve"
```

### 2. Resolve Library ID

**Required before querying docs** (unless user provides ID like `/org/project`).

```
mcp__airis-mcp-gateway__airis-exec
  tool: "context7:resolve-library-id"
  arguments: {
    "query": "How to use QDialog component",
    "libraryName": "quasar"
  }
```

**Both parameters required**:
- `query`: The user's actual question (helps rank results)
- `libraryName`: The library name to search for

Returns library ID like `/quasarframework/quasar`. Store for next call.

### 3. Query Documentation

```
mcp__airis-mcp-gateway__airis-exec
  tool: "context7:query-docs"
  arguments: {
    "libraryId": "/quasarframework/quasar",
    "query": "QDialog component API props events slots"
  }
```

**Query optimization tips**:
- Be specific: "How to set up authentication with JWT" not "auth"
- Include component/function names
- Add "API", "props", "events" for reference docs
- Add "example", "usage" for implementation guidance

### 4. Apply Patterns

- Extract relevant code patterns from docs
- Note version compatibility requirements
- Apply with proper attribution if significant

## Decision Logic

```
IF question about library/framework API:
    → Use Context7
ELSE IF import statement detected AND user asks about that library:
    → Use Context7
ELSE IF general programming concept (closures, promises, etc.):
    → Use native Claude knowledge
ELSE IF library not found in Context7:
    → Fallback to WebSearch or Tavily
```

## Error Recovery

| Error | Recovery |
|-------|----------|
| "Schema not found" / tool error | Server is cold - use airis-find to load it first |
| Library not found | WebSearch for "[library] official documentation" |
| No good matches after 3 tries | Use best result, note limitations |
| Invalid library ID | Retry resolve-library-id with different libraryName |

## Important Limits

- **Max 3 calls per question** for each tool
- If you can't find what you need after 3 attempts, use best available result

## When NOT to Use

- General programming questions (no specific library)
- Debugging code that doesn't involve library APIs
- Simple syntax questions Claude already knows
- User wants current/latest info post-cutoff (use Tavily instead)

## Examples

| User Request | Action |
|--------------|--------|
| "How to use QDialog in Vue?" | resolve-library-id(libraryName: "quasar") → query-docs(query: "QDialog") |
| "React useState example" | resolve-library-id(libraryName: "react") → query-docs(query: "useState hook example") |
| "Prisma query syntax" | resolve-library-id(libraryName: "prisma") → query-docs(query: "query findMany where") |
| "What's a closure?" | Native Claude (no library) |
| "Latest React 19 features" | Use Tavily (current info needed) |
