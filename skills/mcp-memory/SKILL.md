---
name: "mcp-memory"
description: "Memory MCP for persistent knowledge graph across sessions. Store project decisions, user preferences, architectural patterns, and important context. Use when information should persist beyond current conversation."
triggers:
  - "remember this"
  - "save this"
  - "note this"
  - "store this"
  - "for next time"
  - "don't forget"
  - "recall"
  - "what did we"
  - "what was"
  - "previously"
  - "last time"
  - "user preference"
  - "project decision"
  - "architectural decision"
---

# Memory MCP - Persistent Knowledge Graph

Use Memory MCP to store and retrieve information across sessions as a knowledge graph.

## Available Tools

| Tool | Purpose |
|------|---------|
| `mcp__memory__create_entities` | Create new entities (things/concepts) |
| `mcp__memory__create_relations` | Link entities together |
| `mcp__memory__add_observations` | Add facts to existing entities |
| `mcp__memory__search_nodes` | Search the knowledge graph |
| `mcp__memory__open_nodes` | Get specific entities by name |
| `mcp__memory__read_graph` | Read entire knowledge graph |
| `mcp__memory__delete_entities` | Remove entities |
| `mcp__memory__delete_relations` | Remove relations |
| `mcp__memory__delete_observations` | Remove observations |

## When to Use

**Store (create/add):**
- Project architectural decisions
- User preferences and conventions
- Important code patterns specific to a project
- Configuration choices and rationale
- Team standards and agreements
- Bug fixes and their root causes (for reference)

**Retrieve (search/read):**
- "What did we decide about X?"
- "What's the user's preference for Y?"
- "How did we solve this before?"
- Session start: Load relevant project context

## Create Entities

Entities are the nodes in your knowledge graph - things, concepts, decisions.

```
mcp__memory__create_entities
  entities: [
    {
      "name": "project-acme-api",
      "entityType": "project",
      "observations": [
        "Uses Node.js with Express",
        "PostgreSQL database",
        "REST API architecture chosen over GraphQL"
      ]
    },
    {
      "name": "user-eric",
      "entityType": "user",
      "observations": [
        "Prefers functional programming patterns",
        "Uses Quasar for Vue projects",
        "Wants minimal comments in code"
      ]
    }
  ]
```

## Create Relations

Relations connect entities - use active voice verbs.

```
mcp__memory__create_relations
  relations: [
    {
      "from": "user-eric",
      "to": "project-acme-api",
      "relationType": "owns"
    },
    {
      "from": "project-acme-api",
      "to": "decision-rest-over-graphql",
      "relationType": "uses"
    }
  ]
```

## Add Observations

Add new facts to existing entities.

```
mcp__memory__add_observations
  observations: [
    {
      "entityName": "project-acme-api",
      "contents": [
        "Added rate limiting on 2024-01-15",
        "Uses Redis for session storage"
      ]
    }
  ]
```

## Search Knowledge Graph

Find relevant entities by query.

```
mcp__memory__search_nodes
  query: "authentication"
```

## Get Specific Entities

Retrieve entities by name.

```
mcp__memory__open_nodes
  names: ["user-eric", "project-acme-api"]
```

## Read Full Graph

Get everything (use sparingly for large graphs).

```
mcp__memory__read_graph
```

## Entity Types (Suggested)

| Type | Use For |
|------|---------|
| `project` | Projects, repos, codebases |
| `user` | User preferences, conventions |
| `decision` | Architectural/design decisions |
| `pattern` | Code patterns, conventions |
| `technology` | Tools, frameworks, libraries |
| `bug` | Notable bugs and their fixes |
| `standard` | Team/org standards |

## Naming Conventions

Use consistent, searchable names:
- `project-{name}` - Projects
- `user-{name}` - Users
- `decision-{topic}` - Decisions
- `pattern-{name}` - Patterns
- `tech-{name}` - Technologies

## Best Practices

1. **Be specific in observations** - "Uses JWT with 24h expiry" not "uses auth"
2. **Include rationale** - "Chose X because Y" helps future decisions
3. **Use consistent entity types** - Makes searching easier
4. **Create relations** - The graph structure is valuable
5. **Search before creating** - Avoid duplicates
6. **Update, don't duplicate** - Use `add_observations` for existing entities

## Example: Storing a Project Decision

```
# Create the decision entity
mcp__memory__create_entities
  entities: [{
    "name": "decision-api-versioning",
    "entityType": "decision",
    "observations": [
      "Decided to use URL path versioning (/v1/, /v2/)",
      "Rejected header versioning due to caching complexity",
      "Made on 2024-01-20 by Eric",
      "Applies to all REST endpoints"
    ]
  }]

# Link to project
mcp__memory__create_relations
  relations: [{
    "from": "project-acme-api",
    "to": "decision-api-versioning",
    "relationType": "follows"
  }]
```

## Example: Storing User Preferences

```
mcp__memory__create_entities
  entities: [{
    "name": "user-eric-code-style",
    "entityType": "preference",
    "observations": [
      "Prefer const over let when possible",
      "Use arrow functions for callbacks",
      "No semicolons (StandardJS style)",
      "Prefer early returns over nested if/else",
      "Minimal inline comments - code should be self-documenting"
    ]
  }]
```

## Example: Session Start - Load Context

```
# Search for relevant project context
mcp__memory__search_nodes
  query: "project-acme"

# Get user preferences
mcp__memory__open_nodes
  names: ["user-eric", "user-eric-code-style"]
```

## Setup

No API key required. Install with:
```bash
bun run scripts/setup-mcp.ts
```

Or manually:
```bash
claude mcp add --scope user memory -- npx -y @modelcontextprotocol/server-memory@latest
```
