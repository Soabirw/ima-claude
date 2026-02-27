---
name: mcp-tavily
description: Use Tavily MCP for web research and current information beyond knowledge cutoff (post-January 2025). Triggers on 'latest', 'current', '2025', '2026', 'what's new', 'recent updates', 'modern approach', 'compare options', research questions requiring multiple sources, or any question about events/releases/changes after January 2025. Provides 60-70% token savings over multiple WebFetch calls.
---

# Tavily MCP - Web Research & Current Information

Use Tavily for current information and research instead of multiple WebFetch calls.

## MCP Tools

| Tool | Purpose |
|------|---------|
| `mcp__tavily__search` | Web search with depth control |
| `mcp__tavily__extract` | Extract content from specific URLs |

## Basic Search

```
mcp__tavily__search
  query: "Vue 4 new features 2026"
  search_depth: "basic"
  max_results: 10
```

**Key parameters**:
- `query` (required): Search query string
- `search_depth`: "basic" | "advanced" (default: "basic")
- `max_results`: Number of results (default: 5)
- `topic`: "general" | "news" (default: "general")
- `days`: Limit results to last N days (optional)
- `include_domains`: Array of domains to include (optional)
- `exclude_domains`: Array of domains to exclude (optional)

## Search Depth Selection

| Depth | Use Case | Response Time |
|-------|----------|---------------|
| `basic` | Standard factual lookups, quick answers | Fast |
| `advanced` | Comprehensive research, comparisons, multiple perspectives | Slower, more thorough |

## Query Optimization

**Effective queries**:
- Include year: "React 19 features 2026"
- Be specific: "Vite 6 breaking changes" not "Vite updates"
- Add context: "TypeScript 5.5 new utility types"

**Query patterns**:
| Need | Query Pattern |
|------|---------------|
| Latest version features | "[library] [version] new features [year]" |
| Breaking changes | "[library] [version] migration breaking changes" |
| Comparisons | "[tool A] vs [tool B] comparison [year]" |
| Best practices | "[topic] best practices [year]" |

## Extract Content

```
mcp__tavily__extract
  urls: ["https://example.com/article"]
```

Extracts clean content from specific URLs.

## Decision Logic

```
IF question requires post-January-2025 information:
    → Use Tavily
ELSE IF research needs multiple web sources:
    → Use Tavily
ELSE IF single known URL needed:
    → Use native WebFetch
ELSE IF question within Claude's knowledge:
    → Use native Claude
ELSE IF asking about library API (not "what's new"):
    → Use Context7 instead
```

## When NOT to Use

- Library API documentation (use Context7)
- Code symbol searches (use Serena)
- Questions Claude already knows (pre-cutoff knowledge)
- Single URL content extraction where native WebFetch works

## Examples

| User Request | Action |
|--------------|--------|
| "What's new in Vue 4?" | tavily search(query: "Vue 4 new features 2026", search_depth: "basic") |
| "Compare Bun vs Node 2026" | tavily search(query: "Bun vs Node.js comparison 2026", search_depth: "advanced") |
| "Latest Vite features" | tavily search(query: "Vite latest features 2026") |
| "How does useState work?" | Native Claude (known knowledge) |
| "Quasar QDialog API" | Use Context7 (library docs) |

## Source Attribution

After using Tavily, always include sources section:

```
Sources:
- [Official Vue Blog](https://blog.vuejs.org/...)
- [Release Notes](https://github.com/vuejs/...)
```

## Setup

Requires Tavily API key. Install with:
```bash
bun run scripts/setup-mcp.ts
```

Or manually:
```bash
claude mcp add --scope user -e TAVILY_API_KEY=your-key -- tavily npx -y tavily-mcp@latest
```
