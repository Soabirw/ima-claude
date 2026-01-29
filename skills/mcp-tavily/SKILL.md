---
name: mcp-tavily
description: Use Tavily MCP for web research and current information beyond knowledge cutoff (post-January 2025). Triggers on 'latest', 'current', '2025', '2026', 'what's new', 'recent updates', 'modern approach', 'compare options', research questions requiring multiple sources, or any question about events/releases/changes after January 2025. Provides 60-70% token savings over multiple WebFetch calls.
---

# Tavily MCP - Web Research & Current Information

Use Tavily for current information and research instead of multiple WebFetch calls.

## Setup: Airis Gateway

Tavily runs through the Airis MCP gateway. The server may be "cold" (not loaded) initially.

**Tool access pattern**: `mcp__airis-mcp-gateway__airis-exec` with `tool: "tavily:tool-name"`

## MCP Tools

| Tool | Purpose |
|------|---------|
| `tavily:tavily_search` | Web search with depth control (note: underscore, not hyphen) |
| `tavily:tavily_research` | Comprehensive research for complex questions |

## Workflow

### 1. Check if Server is Loaded (Optional)

If you get "Unknown tool" errors, the server is cold. Load it first:
```
mcp__airis-mcp-gateway__airis-find
  server: "tavily"
  query: "search"
```

### 2. Execute Search

```
mcp__airis-mcp-gateway__airis-exec
  tool: "tavily:tavily_search"
  arguments: {
    "query": "Vue 4 new features 2026",
    "search_depth": "basic",
    "max_results": 10
  }
```

**Key parameters**:
- `query` (required): Search query string
- `search_depth`: "basic" | "advanced" | "fast" | "ultra-fast"
- `max_results`: Number of results (default: 10)
- `time_range`: "day" | "week" | "month" | "year" (optional)
- `include_domains`: Array of domains to include
- `exclude_domains`: Array of domains to exclude

### 3. Search Depth Selection

| Depth | Use Case |
|-------|----------|
| `ultra-fast` | Quick facts, latency-critical |
| `fast` | Balanced speed and relevance |
| `basic` | Standard factual lookups |
| `advanced` | Comprehensive research, comparisons |

### 4. Query Optimization

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

### 5. For Complex Research

Use `tavily_research` instead:
```
mcp__airis-mcp-gateway__airis-exec
  tool: "tavily:tavily_research"
  arguments: {
    "query": "Compare state management solutions React 2026"
  }
```

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

## Error Recovery

| Error | Recovery |
|-------|----------|
| "Unknown tool" error | Server is cold - use airis-find to load it first |
| No results | Broaden query, remove date constraints |
| Timeout | Use native WebSearch as fallback |
| Conflicting info | Note uncertainty, cite multiple sources |

## When NOT to Use

- Library API documentation (use Context7)
- Code symbol searches (use Serena)
- Questions Claude already knows (pre-cutoff knowledge)
- Single URL content extraction (use WebFetch)

## Examples

| User Request | Action |
|--------------|--------|
| "What's new in Vue 4?" | tavily_search(query: "Vue 4 new features 2026", search_depth: "basic") |
| "Compare Bun vs Node 2026" | tavily_search(query: "Bun vs Node.js comparison 2026", search_depth: "advanced") |
| "Latest Vite features" | tavily_search(query: "Vite latest features 2026") |
| "How does useState work?" | Native Claude (known knowledge) |
| "Quasar QDialog API" | Use Context7 (library docs) |

## Source Attribution

After using Tavily, include sources section:

```
Sources:
- [Official Vue Blog](https://blog.vuejs.org/...)
- [Release Notes](https://github.com/vuejs/...)
```
